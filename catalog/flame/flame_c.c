#include "flame_c.h"
#include <stdlib.h>

// Маємо: цифровий поріг (D0) і сирий аналоговий вихід (A0) датчика полум'я KY-026.
// Завдання: підготувати обидва входи і повертати обидва значення.

struct flame_t {
    uint8_t digital_gpio;
    int     adc_channel;
};

flame_handle_t flame_init(uint8_t digital_gpio, int adc_channel)
{
    return NULL;
}

void flame_free(flame_handle_t f)
{
}

bool flame_detected(flame_handle_t f)
{
    return false;
}

int flame_read_raw(flame_handle_t f)
{
    return -1;
}
