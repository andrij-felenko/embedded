#ifndef CATALOG_SOIL_MOISTURE_C_H
#define CATALOG_SOIL_MOISTURE_C_H

#include <stdint.h>

typedef struct soil_moisture_t soil_moisture_t;
typedef soil_moisture_t *soil_moisture_handle_t;

// Два щупи + модуль LM393, аналоговий вихід. Потрібна власна калібровка
// "сухо"/"мокро" — відрізняється від щупа до щупа.
soil_moisture_handle_t soil_moisture_init(int adc_channel);
void                    soil_moisture_free(soil_moisture_handle_t s);

int soil_moisture_read_percent(soil_moisture_handle_t s);

#endif // CATALOG_SOIL_MOISTURE_C_H
