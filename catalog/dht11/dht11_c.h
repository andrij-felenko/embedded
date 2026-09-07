#ifndef CATALOG_DHT11_C_H
#define CATALOG_DHT11_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct dht11_t dht11_t;
typedef dht11_t *dht11_handle_t;

// DHT11: один провід, бітбенгінг, суворий протокол таймінгу. Потрібна
// точність у мікросекундах і перевірка контрольної суми.
dht11_handle_t dht11_init(uint8_t gpio);
void            dht11_free(dht11_handle_t d);

bool dht11_read(dht11_handle_t d, float *humidity, float *temp_c);

#endif // CATALOG_DHT11_C_H
