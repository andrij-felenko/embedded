#include "digital_temp_c.h"
#include <stdlib.h>

// Маємо: цифровий поріг (D0) і аналоговий термістор (A0) датчика KY-028.
// Завдання: підготувати обидва входи, повертати і поріг, і температуру
// (та сама Steinhart-Hart математика, що й у thermistor_c.c).

struct digital_temp_t {
    uint8_t digital_gpio;
    int     adc_channel;
};

digital_temp_handle_t digital_temp_init(uint8_t digital_gpio, int adc_channel)
{
    return NULL;
}

void digital_temp_free(digital_temp_handle_t d)
{
}

bool digital_temp_threshold_hit(digital_temp_handle_t d)
{
    return false;
}

float digital_temp_read_c(digital_temp_handle_t d)
{
    return -1.0f;
}
