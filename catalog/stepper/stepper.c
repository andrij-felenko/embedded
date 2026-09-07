#include "stepper.h"
#include <stdlib.h>

// Маємо: чотири GPIO піни крокового мотора 28BYJ-48 через драйвер ULN2003.
// Завдання: підготувати піни і крутити мотор із заданою швидкістю та
// напрямком, викликаючи tick() регулярно, щоб не блокувати виконання.

struct stepper_t {
    uint8_t pins[4];
    int16_t speed;
};

stepper_handle_t stepper_init(uint8_t in1, uint8_t in2, uint8_t in3, uint8_t in4)
{
    return NULL;
}

void stepper_free(stepper_handle_t s)
{
}

void stepper_set_speed(stepper_handle_t s, int16_t steps_per_sec)
{
}

void stepper_tick(stepper_handle_t s)
{
}
