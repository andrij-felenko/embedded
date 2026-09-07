#ifndef CATALOG_RAIN_C_H
#define CATALOG_RAIN_C_H

#include <stdint.h>

typedef struct rain_t rain_t;
typedef rain_t *rain_handle_t;

// Funduino: відкрита плата + модуль LM358, та сама схема, що й
// water_level, тільки під дощ, не під воду.
rain_handle_t rain_init(int adc_channel);
void          rain_free(rain_handle_t r);

int rain_read_raw(rain_handle_t r);

#endif // CATALOG_RAIN_C_H
