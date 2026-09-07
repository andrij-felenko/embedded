#include "sound_c.h"
#include <stdlib.h>

// Маємо: цифровий поріг (D0) і аналогову обвідну (A0) звукового модуля KY-038.
// Завдання: підготувати обидва входи і повертати обидва значення.

struct sound_t {
    uint8_t digital_gpio;
    int     adc_channel;
};

sound_handle_t sound_init(uint8_t digital_gpio, int adc_channel)
{
    return NULL;
}

void sound_free(sound_handle_t s)
{
}

bool sound_threshold_hit(sound_handle_t s)
{
    return false;
}

int sound_read_raw(sound_handle_t s)
{
    return -1;
}
