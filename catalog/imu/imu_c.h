#ifndef CATALOG_IMU_C_H
#define CATALOG_IMU_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct imu_t imu_t;
typedef imu_t *imu_handle_t;

typedef struct { float x, y, z; } imu_vec3_t;

// Pololu IMU (LSM6DS33 / MinIMU-9): I2C, 6 осей (акселерометр + гіроскоп).
// Сирі значення нічого не означають без знання діапазону, який ти
// налаштував при ініціалізації.
imu_handle_t imu_init(int i2c_port, uint8_t sda_gpio, uint8_t scl_gpio);
void         imu_free(imu_handle_t i);

bool imu_read(imu_handle_t i, imu_vec3_t *accel_g, imu_vec3_t *gyro_dps);

#endif // CATALOG_IMU_C_H
