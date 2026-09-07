#include "distance.h"
#include <stdlib.h>

// Маємо: два GPIO піни ультразвукового далекоміра HC-SR04 (trig/echo).
// Завдання: підготувати піни і виміряти відстань за часом ехо-імпульсу.

struct distance_t {
    uint8_t trig;
    uint8_t echo;
};

distance_handle_t distance_init(uint8_t trig_gpio, uint8_t echo_gpio)
{
    return NULL;
}

void distance_free(distance_handle_t d)
{
}

float distance_read_cm(distance_handle_t d)
{
    return -1.0f;
}
