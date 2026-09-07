#include "laser_c.h"
#include <stdlib.h>

// Маємо: GPIO пін лазерного модуля KY-008.
// Завдання: підготувати пін і вмикати/вимикати лазер.

struct laser_t {
    uint8_t gpio;
};

laser_handle_t laser_init(uint8_t gpio)
{
    return NULL;
}

void laser_free(laser_handle_t l)
{
}

void laser_set(laser_handle_t l, bool on)
{
}
