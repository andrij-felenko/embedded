#include "rain_c.h"
#include <stdlib.h>

// Маємо: аналоговий канал дощового датчика Funduino (та сама схема, що й water_level).
// Завдання: підготувати вхід і повертати сирий рівень опадів.

struct rain_t {
    int channel;
};

rain_handle_t rain_init(int adc_channel)
{
    return NULL;
}

void rain_free(rain_handle_t r)
{
}

int rain_read_raw(rain_handle_t r)
{
    return -1;
}
