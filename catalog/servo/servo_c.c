#include "servo_c.h"
#include <stdlib.h>

// Маємо: GPIO пін серво SG90/HD-1370A (ШІМ 50Гц, кут кодується шириною імпульсу 1-2мс).
// Завдання: підготувати окремий канал ШІМ під цю частоту і переводити кут у ширину імпульсу.

struct servo_t {
    uint8_t gpio;
};

servo_handle_t servo_init(uint8_t gpio)
{
    return NULL;
}

void servo_free(servo_handle_t s)
{
}

void servo_set_angle(servo_handle_t s, uint8_t degrees)
{
}
