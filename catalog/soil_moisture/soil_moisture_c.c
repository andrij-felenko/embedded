#include "soil_moisture_c.h"
#include <stdlib.h>

// Маємо: аналоговий канал датчика вологості ґрунту (два щупи + LM393).
// Завдання: підготувати вхід і перевести сирий сигнал у відсотки вологості
// (потрібна власна калібровка "сухо"/"мокро").

struct soil_moisture_t {
    int channel;
};

soil_moisture_handle_t soil_moisture_init(int adc_channel)
{
    return NULL;
}

void soil_moisture_free(soil_moisture_handle_t s)
{
}

int soil_moisture_read_percent(soil_moisture_handle_t s)
{
    return -1;
}
