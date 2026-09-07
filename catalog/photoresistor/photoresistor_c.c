#include "photoresistor_c.h"
#include <stdlib.h>

// Маємо: аналоговий канал фоторезистора KY-018 (подільник напруги).
// Завдання: підготувати вхід і повертати сирий рівень освітленості.

struct photoresistor_t {
    int channel;
};

photoresistor_handle_t photoresistor_init(int adc_channel)
{
    return NULL;
}

void photoresistor_free(photoresistor_handle_t p)
{
}

int photoresistor_read_raw(photoresistor_handle_t p)
{
    return -1;
}
