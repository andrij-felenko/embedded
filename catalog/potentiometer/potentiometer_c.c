#include "potentiometer_c.h"
#include <stdlib.h>

// Маємо: аналоговий канал звичайного потенціометра.
// Завдання: підготувати вхід і повертати сире положення.

struct potentiometer_t {
    int channel;
};

potentiometer_handle_t potentiometer_init(int adc_channel)
{
    return NULL;
}

void potentiometer_free(potentiometer_handle_t p)
{
}

int potentiometer_read_raw(potentiometer_handle_t p)
{
    return -1;
}
