#include "gas_c.h"
#include <stdlib.h>

// Маємо: аналоговий канал газового датчика MQ (потребує часу прогріву).
// Завдання: підготувати вхід і повертати сирий рівень.

struct gas_t {
    int channel;
};

gas_handle_t gas_init(int adc_channel)
{
    return NULL;
}

void gas_free(gas_handle_t g)
{
}

int gas_read_raw(gas_handle_t g)
{
    return -1;
}
