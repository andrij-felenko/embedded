#include "imu_c.h"
#include <stdlib.h>
#include <string.h>

// Маємо: I2C до 6-осьового IMU (LSM6DS33).
// Завдання: підготувати I2C, налаштувати діапазони вимірів і зчитувати
// прискорення й кутову швидкість по трьох осях.

struct imu_t {
    int     i2c_port;
    uint8_t sda_gpio, scl_gpio;
};

imu_handle_t imu_init(int i2c_port, uint8_t sda_gpio, uint8_t scl_gpio)
{
    return NULL;
}

void imu_free(imu_handle_t i)
{
}

bool imu_read(imu_handle_t i, imu_vec3_t *accel_g, imu_vec3_t *gyro_dps)
{
    if (accel_g) memset(accel_g, 0, sizeof(*accel_g));
    if (gyro_dps) memset(gyro_dps, 0, sizeof(*gyro_dps));
    return false;
}
