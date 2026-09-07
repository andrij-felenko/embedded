#include "bme280_c.h"
#include <stdlib.h>
#include <string.h>
#include "driver/i2c_master.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"

#define REG_CHIP_ID     0xD0
#define REG_RESET       0xE0
#define REG_CTRL_HUM    0xF2
#define REG_CTRL_MEAS   0xF4
#define REG_CONFIG      0xF5
#define REG_PRESS_MSB   0xF7   // пакетне читання 8 байт: тиск(3) темп.(3) вологість(2)
#define REG_CALIB_00    0x88   // пакетне читання 26 байт: dig_T1..T3, dig_P1..P9
#define REG_CALIB_H1    0xA1   // 1 байт: dig_H1
#define REG_CALIB_H2    0xE1   // пакетне читання 7 байт: dig_H2..H6, упаковані в біти

static const char *TAG = "bme280";
#define I2C_TIMEOUT_MS 1000

struct bme280_t {
    i2c_master_bus_handle_t bus;
    i2c_master_dev_handle_t dev;

    uint16_t dig_T1;
    int16_t  dig_T2, dig_T3;
    uint16_t dig_P1;
    int16_t  dig_P2, dig_P3, dig_P4, dig_P5, dig_P6, dig_P7, dig_P8, dig_P9;
    uint8_t  dig_H1;
    int16_t  dig_H2;
    uint8_t  dig_H3;
    int16_t  dig_H4, dig_H5;
    int8_t   dig_H6;

    int32_t t_fine;   // виставляє compensate_temperature(), читають тиск/вологість
};

static esp_err_t read_regs(bme280_handle_t b, uint8_t reg, uint8_t *buf, size_t len)
{
    return i2c_master_transmit_receive(b->dev, &reg, 1, buf, len, I2C_TIMEOUT_MS);
}

static esp_err_t write_reg(bme280_handle_t b, uint8_t reg, uint8_t value)
{
    uint8_t payload[2] = {reg, value};
    return i2c_master_transmit(b->dev, payload, sizeof(payload), I2C_TIMEOUT_MS);
}

static uint16_t le16u(const uint8_t *p) { return (uint16_t)(p[0] | (p[1] << 8)); }
static int16_t  le16s(const uint8_t *p) { return (int16_t)(p[0] | (p[1] << 8)); }

bme280_handle_t bme280_init(int i2c_port, uint8_t i2c_addr, uint8_t sda_gpio, uint8_t scl_gpio)
{
    bme280_handle_t self = malloc(sizeof(struct bme280_t));
    memset(self, 0, sizeof(struct bme280_t));

    i2c_master_bus_config_t bus_cfg = {
        .i2c_port = i2c_port,
        .sda_io_num = sda_gpio,
        .scl_io_num = scl_gpio,
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7,
        .flags.enable_internal_pullup = true,
    };
    if (i2c_new_master_bus(&bus_cfg, &self->bus) != ESP_OK) {
        free(self);
        return NULL;
    }

    i2c_device_config_t dev_cfg = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address  = i2c_addr,
        .scl_speed_hz    = 100000,
    };
    if (i2c_master_bus_add_device(self->bus, &dev_cfg, &self->dev) != ESP_OK) {
        i2c_del_master_bus(self->bus);
        free(self);
        return NULL;
    }

    uint8_t chip_id = 0;
    if (read_regs(self, REG_CHIP_ID, &chip_id, 1) != ESP_OK ||
        (chip_id != 0x58 && chip_id != 0x60)) {
        ESP_LOGW(TAG, "unexpected chip id 0x%02X (want 0x58 BMP280 / 0x60 BME280)", chip_id);
        i2c_master_bus_rm_device(self->dev);
        i2c_del_master_bus(self->bus);
        free(self);
        return NULL;
    }

    write_reg(self, REG_RESET, 0xB6);
    vTaskDelay(pdMS_TO_TICKS(10));

    uint8_t calib1[26];
    read_regs(self, REG_CALIB_00, calib1, sizeof(calib1));
    self->dig_T1 = le16u(&calib1[0]);
    self->dig_T2 = le16s(&calib1[2]);
    self->dig_T3 = le16s(&calib1[4]);
    self->dig_P1 = le16u(&calib1[6]);
    self->dig_P2 = le16s(&calib1[8]);
    self->dig_P3 = le16s(&calib1[10]);
    self->dig_P4 = le16s(&calib1[12]);
    self->dig_P5 = le16s(&calib1[14]);
    self->dig_P6 = le16s(&calib1[16]);
    self->dig_P7 = le16s(&calib1[18]);
    self->dig_P8 = le16s(&calib1[20]);
    self->dig_P9 = le16s(&calib1[22]);

    uint8_t h1 = 0;
    read_regs(self, REG_CALIB_H1, &h1, 1);
    self->dig_H1 = h1;

    uint8_t calib2[7];
    read_regs(self, REG_CALIB_H2, calib2, sizeof(calib2));
    self->dig_H2 = le16s(&calib2[0]);
    self->dig_H3 = calib2[2];
    self->dig_H4 = (int16_t)(((int8_t)calib2[3] << 4) | (calib2[4] & 0x0F));
    self->dig_H5 = (int16_t)(((int8_t)calib2[5] << 4) | (calib2[4] >> 4));
    self->dig_H6 = (int8_t)calib2[6];

    write_reg(self, REG_CTRL_HUM, 0x01);   // oversampling вологості x1
    write_reg(self, REG_CTRL_MEAS, 0x27);  // темп. x1, тиск x1, normal mode
    write_reg(self, REG_CONFIG, 0x00);     // без IIR-фільтра, standby 0.5мс

    return self;
}

void bme280_free(bme280_handle_t b)
{
    if (!b) return;
    if (b->dev) i2c_master_bus_rm_device(b->dev);
    if (b->bus) i2c_del_master_bus(b->bus);
    free(b);
}

// Формули компенсації з даташиту Bosch BME280, розділ 4.2.3, double-precision.
static double compensate_temperature(bme280_handle_t b, int32_t adc_T)
{
    double var1 = (((double)adc_T) / 16384.0 - ((double)b->dig_T1) / 1024.0) * ((double)b->dig_T2);
    double var2 = ((((double)adc_T) / 131072.0 - ((double)b->dig_T1) / 8192.0) *
                   (((double)adc_T) / 131072.0 - ((double)b->dig_T1) / 8192.0)) * ((double)b->dig_T3);
    b->t_fine = (int32_t)(var1 + var2);
    return (var1 + var2) / 5120.0;
}

static double compensate_pressure(bme280_handle_t b, int32_t adc_P)
{
    double var1 = ((double)b->t_fine / 2.0) - 64000.0;
    double var2 = var1 * var1 * ((double)b->dig_P6) / 32768.0;
    var2 = var2 + var1 * ((double)b->dig_P5) * 2.0;
    var2 = (var2 / 4.0) + (((double)b->dig_P4) * 65536.0);
    var1 = (((double)b->dig_P3) * var1 * var1 / 524288.0 + ((double)b->dig_P2) * var1) / 524288.0;
    var1 = (1.0 + var1 / 32768.0) * ((double)b->dig_P1);
    if (var1 == 0.0) return 0.0;   // захист від ділення на нуль при поганому калібруванні
    double p = 1048576.0 - (double)adc_P;
    p = (p - (var2 / 4096.0)) * 6250.0 / var1;
    var1 = ((double)b->dig_P9) * p * p / 2147483648.0;
    var2 = p * ((double)b->dig_P8) / 32768.0;
    p = p + (var1 + var2 + ((double)b->dig_P7)) / 16.0;
    return p; // Па
}

static double compensate_humidity(bme280_handle_t b, int32_t adc_H)
{
    double var_H = (((double)b->t_fine) - 76800.0);
    var_H = (adc_H - (((double)b->dig_H4) * 64.0 + ((double)b->dig_H5) / 16384.0 * var_H)) *
            (((double)b->dig_H2) / 65536.0 * (1.0 + ((double)b->dig_H6) / 67108864.0 * var_H *
            (1.0 + ((double)b->dig_H3) / 67108864.0 * var_H)));
    var_H = var_H * (1.0 - ((double)b->dig_H1) * var_H / 524288.0);
    if (var_H > 100.0) var_H = 100.0;
    else if (var_H < 0.0) var_H = 0.0;
    return var_H;
}

bool bme280_read(bme280_handle_t b, float *temp_c, float *pressure_hpa, float *humidity_pct)
{
    uint8_t raw[8];
    if (read_regs(b, REG_PRESS_MSB, raw, sizeof(raw)) != ESP_OK) return false;

    int32_t adc_P = ((int32_t)raw[0] << 12) | ((int32_t)raw[1] << 4) | (raw[2] >> 4);
    int32_t adc_T = ((int32_t)raw[3] << 12) | ((int32_t)raw[4] << 4) | (raw[5] >> 4);
    int32_t adc_H = ((int32_t)raw[6] << 8) | raw[7];

    double t = compensate_temperature(b, adc_T);   // обов'язково першою -- виставляє t_fine
    double p = compensate_pressure(b, adc_P);
    double h = compensate_humidity(b, adc_H);

    if (temp_c)        *temp_c        = (float)t;
    if (pressure_hpa)  *pressure_hpa  = (float)(p / 100.0);
    if (humidity_pct)  *humidity_pct  = (float)h;
    return true;
}
