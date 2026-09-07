#include "dht11_c.h"
#include <stdlib.h>

// Маємо: один GPIO пін датчика DHT11 (однопровідний протокол з жорстким таймінгом).
// Завдання: провести повний обмін з точним таймінгом (мікросекунди) і
// перевірити контрольну суму, інакше показання будуть хибними.

struct dht11_t {
    uint8_t gpio;
};

dht11_handle_t dht11_init(uint8_t gpio)
{
    return NULL;
}

void dht11_free(dht11_handle_t d)
{
}

bool dht11_read(dht11_handle_t d, float *humidity, float *temp_c)
{
    if (humidity) *humidity = -1.0f;
    if (temp_c)   *temp_c   = -1.0f;
    return false;
}
