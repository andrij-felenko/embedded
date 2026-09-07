#ifndef CATALOG_PHOTORESISTOR_C_H
#define CATALOG_PHOTORESISTOR_C_H

#include <stdint.h>

typedef struct photoresistor_t photoresistor_t;
typedef photoresistor_t *photoresistor_handle_t;

// KY-018: фоторезистор + подільник напруги, один канал АЦП. 0..4095,
// напрям (світліше = більше чи менше) залежить від того, як увімкнено.
photoresistor_handle_t photoresistor_init(int adc_channel);
void                    photoresistor_free(photoresistor_handle_t p);

int photoresistor_read_raw(photoresistor_handle_t p);

#endif // CATALOG_PHOTORESISTOR_C_H
