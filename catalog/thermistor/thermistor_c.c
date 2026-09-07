#include "thermistor_c.h"
#include <stdlib.h>

// Маємо: аналоговий канал термістора KY-013 (нелінійна залежність від температури).
// Завдання: підготувати вхід і перевести сирий сигнал у температуру.

struct thermistor_t {
    int channel;
};

thermistor_handle_t thermistor_init(int adc_channel)
{
    return NULL;
}

void thermistor_free(thermistor_handle_t t)
{
}

float thermistor_read_c(thermistor_handle_t t)
{
    return -1.0f;
}
