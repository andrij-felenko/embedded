#ifndef CATALOG_PULSE_OX_C_H
#define CATALOG_PULSE_OX_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct pulse_ox_t pulse_ox_t;
typedef pulse_ox_t *pulse_ox_handle_t;

// GY-MAX30102: I2C, пульс/SpO2, червоний+ІЧ світлодіоди + фотодетектор,
// має власний FIFO. Складна частина тут — не протокол, а обробка
// сигналу (пульс і SpO2 з сирих хвиль).
pulse_ox_handle_t pulse_ox_init(int i2c_port, uint8_t sda_gpio, uint8_t scl_gpio);
void                pulse_ox_free(pulse_ox_handle_t p);

bool pulse_ox_read_raw(pulse_ox_handle_t p, uint32_t *red, uint32_t *ir);

#endif // CATALOG_PULSE_OX_C_H
