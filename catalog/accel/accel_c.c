#include "accel_c.h"
#include <stdlib.h>

// Маємо: три аналогові канали (X/Y/Z) акселерометра GY-61 ADXL335.
// Завдання: підготувати три входи і перевести сирі значення в прискорення
// по осях (g), знаючи нуль і чутливість.

struct accel_t {
    int channel[3];
};

accel_handle_t accel_init(int adc_channel_x, int adc_channel_y, int adc_channel_z)
{
    return NULL;
}

void accel_free(accel_handle_t a)
{
}

void accel_read_g(accel_handle_t a, float *x, float *y, float *z)
{
    if (x) *x = 0.0f;
    if (y) *y = 0.0f;
    if (z) *z = 1.0f;
}
