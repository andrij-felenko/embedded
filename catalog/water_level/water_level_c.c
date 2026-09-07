#include "water_level_c.h"
#include <stdlib.h>

// Маємо: аналоговий канал датчика рівня води HW-038 (відкриті доріжки).
// Завдання: підготувати вхід і повертати сирий рівень занурення.

struct water_level_t {
    int channel;
};

water_level_handle_t water_level_init(int adc_channel)
{
    return NULL;
}

void water_level_free(water_level_handle_t w)
{
}

int water_level_read_raw(water_level_handle_t w)
{
    return -1;
}
