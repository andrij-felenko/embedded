#ifndef CATALOG_TOF_C_H
#define CATALOG_TOF_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct tof_t tof_t;
typedef tof_t *tof_handle_t;

// TOF250: I2C лазерний далекомір. На відміну від HC-SR04 (distance.h,
// вимір ехо-імпульсу вручну), тут вимір відстані робить сам чіп — ти
// лише читаєш готовий результат з регістра.
tof_handle_t tof_init(int i2c_port, uint8_t i2c_addr, uint8_t sda_gpio, uint8_t scl_gpio);
void         tof_free(tof_handle_t t);

int tof_read_mm(tof_handle_t t);

#endif // CATALOG_TOF_C_H
