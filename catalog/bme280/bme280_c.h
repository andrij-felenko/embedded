#ifndef CATALOG_BME280_C_H
#define CATALOG_BME280_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct bme280_t bme280_t;
typedef bme280_t *bme280_handle_t;

// I2C, адреса 0x76 або 0x77 (залежить від піна SDO). Зчитує й зберігає
// заводські коефіцієнти калібрування (регістри 0x88-0xA1, 0xA1, 0xE1-0xE7)
// при ініціалізації, тоді налаштовує normal mode з x1 oversampling на всіх
// трьох вимірах. Повертає NULL, якщо шина/пристрій не відкрились або
// регістр ID чіпа (0xD0) не 0x58 (BMP280, без вологості) чи 0x60 (BME280).
bme280_handle_t bme280_init(int i2c_port, uint8_t i2c_addr, uint8_t sda_gpio, uint8_t scl_gpio);
void            bme280_free(bme280_handle_t b);

// Читає регістри 0xF7..0xFE (пакетом) і проганяє через формули компенсації
// з даташиту Bosch (розділ 4.2.3, double-precision варіант). Порядок
// важливий: температуру треба компенсувати першою — вона дає t_fine, від
// якого залежать і тиск, і вологість.
bool bme280_read(bme280_handle_t b, float *temp_c, float *pressure_hpa, float *humidity_pct);

#endif // CATALOG_BME280_C_H
