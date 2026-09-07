#include "rgb_led_c.h"
#include <stdlib.h>

// Маємо: три GPIO піни (R/G/B) світлодіода KY-016, кожен окремий канал ШІМ.
// Завдання: підготувати три канали і виставляти колір, зваживши на спільний анод/катод.

struct rgb_led_t {
    uint8_t r_gpio, g_gpio, b_gpio;
};

rgb_led_handle_t rgb_led_init(uint8_t r_gpio, uint8_t g_gpio, uint8_t b_gpio)
{
    return NULL;
}

void rgb_led_free(rgb_led_handle_t l)
{
}

void rgb_led_set(rgb_led_handle_t l, uint8_t r, uint8_t g, uint8_t b)
{
}
