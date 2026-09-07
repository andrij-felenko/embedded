#include "pulse_ox_c.h"
#include <stdlib.h>

// Маємо: I2C до пульсоксиметра MAX30102 (GY-MAX30102), з власним FIFO.
// Завдання: підготувати I2C, налаштувати режим SpO2 і вичитувати FIFO
// (обробка сигналу для пульсу/SpO2 — окрема складна частина).

struct pulse_ox_t {
    int     i2c_port;
    uint8_t sda_gpio, scl_gpio;
};

pulse_ox_handle_t pulse_ox_init(int i2c_port, uint8_t sda_gpio, uint8_t scl_gpio)
{
    return NULL;
}

void pulse_ox_free(pulse_ox_handle_t p)
{
}

bool pulse_ox_read_raw(pulse_ox_handle_t p, uint32_t *red, uint32_t *ir)
{
    if (red) *red = 0;
    if (ir) *ir = 0;
    return false;
}
