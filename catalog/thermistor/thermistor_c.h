#ifndef CATALOG_THERMISTOR_C_H
#define CATALOG_THERMISTOR_C_H

#include <stdint.h>

typedef struct thermistor_t thermistor_t;
typedef thermistor_t *thermistor_handle_t;

// KY-013: NTC-термістор + подільник, один канал АЦП. Залежність від
// температури нелінійна.
thermistor_handle_t thermistor_init(int adc_channel);
void                 thermistor_free(thermistor_handle_t t);

float thermistor_read_c(thermistor_handle_t t);

#endif // CATALOG_THERMISTOR_C_H
