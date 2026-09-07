#include "tof_c.h"
#include <stdlib.h>

// Маємо: I2C до лазерного далекоміра TOF250 (сам чіп рахує час прольоту).
// Завдання: підготувати I2C, запустити одноразовий вимір і прочитати готову відстань.

struct tof_t {
    int     i2c_port;
    uint8_t i2c_addr;
    uint8_t sda_gpio, scl_gpio;
};

tof_handle_t tof_init(int i2c_port, uint8_t i2c_addr, uint8_t sda_gpio, uint8_t scl_gpio)
{
    return NULL;
}

void tof_free(tof_handle_t t)
{
}

int tof_read_mm(tof_handle_t t)
{
    return -1;
}
