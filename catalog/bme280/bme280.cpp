#include "bme280.hpp"
#include <stdexcept>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"

namespace {
constexpr uint8_t REG_CHIP_ID   = 0xD0;
constexpr uint8_t REG_RESET     = 0xE0;
constexpr uint8_t REG_CTRL_HUM  = 0xF2;
constexpr uint8_t REG_CTRL_MEAS = 0xF4;
constexpr uint8_t REG_CONFIG    = 0xF5;
constexpr uint8_t REG_PRESS_MSB = 0xF7;
constexpr uint8_t REG_CALIB_00  = 0x88;
constexpr uint8_t REG_CALIB_H1  = 0xA1;
constexpr uint8_t REG_CALIB_H2  = 0xE1;
constexpr const char *TAG = "bme280";
constexpr int I2C_TIMEOUT_MS = 1000;

uint16_t le16u(const uint8_t *p) { return static_cast<uint16_t>(p[0] | (p[1] << 8)); }
int16_t  le16s(const uint8_t *p) { return static_cast<int16_t>(p[0] | (p[1] << 8)); }
} // namespace

Bme280::Bme280(int i2cPort, uint8_t i2cAddr, uint8_t sdaGpio, uint8_t sclGpio)
{
    i2c_master_bus_config_t busCfg = {};
    busCfg.i2c_port = i2cPort;
    busCfg.sda_io_num = static_cast<gpio_num_t>(sdaGpio);
    busCfg.scl_io_num = static_cast<gpio_num_t>(sclGpio);
    busCfg.clk_source = I2C_CLK_SRC_DEFAULT;
    busCfg.glitch_ignore_cnt = 7;
    busCfg.flags.enable_internal_pullup = true;

    if (i2c_new_master_bus(&busCfg, &bus_) != ESP_OK) {
        throw std::runtime_error("Bme280: i2c_new_master_bus failed");
    }

    i2c_device_config_t devCfg = {};
    devCfg.dev_addr_length = I2C_ADDR_BIT_LEN_7;
    devCfg.device_address  = i2cAddr;
    devCfg.scl_speed_hz    = 100000;

    if (i2c_master_bus_add_device(bus_, &devCfg, &dev_) != ESP_OK) {
        i2c_del_master_bus(bus_);
        throw std::runtime_error("Bme280: i2c_master_bus_add_device failed");
    }

    uint8_t reg = REG_CHIP_ID;
    uint8_t chipId = 0;
    if (i2c_master_transmit_receive(dev_, &reg, 1, &chipId, 1, I2C_TIMEOUT_MS) != ESP_OK ||
        (chipId != 0x58 && chipId != 0x60)) {
        ESP_LOGW(TAG, "unexpected chip id 0x%02X (want 0x58 BMP280 / 0x60 BME280)", chipId);
        i2c_master_bus_rm_device(dev_);
        i2c_del_master_bus(bus_);
        throw std::runtime_error("Bme280: chip id mismatch");
    }

    uint8_t resetCmd[2] = {REG_RESET, 0xB6};
    i2c_master_transmit(dev_, resetCmd, sizeof(resetCmd), I2C_TIMEOUT_MS);
    vTaskDelay(pdMS_TO_TICKS(10));

    uint8_t calib1[26];
    reg = REG_CALIB_00;
    i2c_master_transmit_receive(dev_, &reg, 1, calib1, sizeof(calib1), I2C_TIMEOUT_MS);
    digT1_ = le16u(&calib1[0]);
    digT2_ = le16s(&calib1[2]);
    digT3_ = le16s(&calib1[4]);
    digP1_ = le16u(&calib1[6]);
    digP2_ = le16s(&calib1[8]);
    digP3_ = le16s(&calib1[10]);
    digP4_ = le16s(&calib1[12]);
    digP5_ = le16s(&calib1[14]);
    digP6_ = le16s(&calib1[16]);
    digP7_ = le16s(&calib1[18]);
    digP8_ = le16s(&calib1[20]);
    digP9_ = le16s(&calib1[22]);

    reg = REG_CALIB_H1;
    uint8_t h1 = 0;
    i2c_master_transmit_receive(dev_, &reg, 1, &h1, 1, I2C_TIMEOUT_MS);
    digH1_ = h1;

    uint8_t calib2[7];
    reg = REG_CALIB_H2;
    i2c_master_transmit_receive(dev_, &reg, 1, calib2, sizeof(calib2), I2C_TIMEOUT_MS);
    digH2_ = le16s(&calib2[0]);
    digH3_ = calib2[2];
    digH4_ = static_cast<int16_t>((static_cast<int8_t>(calib2[3]) << 4) | (calib2[4] & 0x0F));
    digH5_ = static_cast<int16_t>((static_cast<int8_t>(calib2[5]) << 4) | (calib2[4] >> 4));
    digH6_ = static_cast<int8_t>(calib2[6]);

    uint8_t ctrlHum[2]  = {REG_CTRL_HUM, 0x01};
    uint8_t ctrlMeas[2] = {REG_CTRL_MEAS, 0x27};
    uint8_t config[2]   = {REG_CONFIG, 0x00};
    i2c_master_transmit(dev_, ctrlHum, sizeof(ctrlHum), I2C_TIMEOUT_MS);
    i2c_master_transmit(dev_, ctrlMeas, sizeof(ctrlMeas), I2C_TIMEOUT_MS);
    i2c_master_transmit(dev_, config, sizeof(config), I2C_TIMEOUT_MS);
}

Bme280::~Bme280()
{
    if (dev_) i2c_master_bus_rm_device(dev_);
    if (bus_) i2c_del_master_bus(bus_);
}

double Bme280::compensateTemperature(int32_t adcT) const
{
    double var1 = (static_cast<double>(adcT) / 16384.0 - static_cast<double>(digT1_) / 1024.0) * digT2_;
    double var2 = ((static_cast<double>(adcT) / 131072.0 - static_cast<double>(digT1_) / 8192.0) *
                   (static_cast<double>(adcT) / 131072.0 - static_cast<double>(digT1_) / 8192.0)) * digT3_;
    tFine_ = static_cast<int32_t>(var1 + var2);
    return (var1 + var2) / 5120.0;
}

double Bme280::compensatePressure(int32_t adcP) const
{
    double var1 = static_cast<double>(tFine_) / 2.0 - 64000.0;
    double var2 = var1 * var1 * digP6_ / 32768.0;
    var2 = var2 + var1 * digP5_ * 2.0;
    var2 = (var2 / 4.0) + (static_cast<double>(digP4_) * 65536.0);
    var1 = (static_cast<double>(digP3_) * var1 * var1 / 524288.0 + static_cast<double>(digP2_) * var1) / 524288.0;
    var1 = (1.0 + var1 / 32768.0) * digP1_;
    if (var1 == 0.0) return 0.0;
    double p = 1048576.0 - static_cast<double>(adcP);
    p = (p - (var2 / 4096.0)) * 6250.0 / var1;
    var1 = static_cast<double>(digP9_) * p * p / 2147483648.0;
    var2 = p * digP8_ / 32768.0;
    p = p + (var1 + var2 + digP7_) / 16.0;
    return p;
}

double Bme280::compensateHumidity(int32_t adcH) const
{
    double varH = static_cast<double>(tFine_) - 76800.0;
    varH = (adcH - (digH4_ * 64.0 + digH5_ / 16384.0 * varH)) *
           (digH2_ / 65536.0 * (1.0 + digH6_ / 67108864.0 * varH * (1.0 + digH3_ / 67108864.0 * varH)));
    varH = varH * (1.0 - digH1_ * varH / 524288.0);
    if (varH > 100.0) varH = 100.0;
    else if (varH < 0.0) varH = 0.0;
    return varH;
}

std::optional<Bme280Reading> Bme280::read() const
{
    uint8_t raw[8];
    uint8_t reg = REG_PRESS_MSB;
    if (i2c_master_transmit_receive(dev_, &reg, 1, raw, sizeof(raw), I2C_TIMEOUT_MS) != ESP_OK) {
        return std::nullopt;
    }

    int32_t adcP = (static_cast<int32_t>(raw[0]) << 12) | (static_cast<int32_t>(raw[1]) << 4) | (raw[2] >> 4);
    int32_t adcT = (static_cast<int32_t>(raw[3]) << 12) | (static_cast<int32_t>(raw[4]) << 4) | (raw[5] >> 4);
    int32_t adcH = (static_cast<int32_t>(raw[6]) << 8) | raw[7];

    Bme280Reading result{};
    result.tempC       = static_cast<float>(compensateTemperature(adcT)); // обов'язково першою -- виставляє tFine_
    result.pressureHpa = static_cast<float>(compensatePressure(adcP) / 100.0);
    result.humidityPct = static_cast<float>(compensateHumidity(adcH));
    return result;
}
