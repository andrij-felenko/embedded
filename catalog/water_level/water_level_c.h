#ifndef CATALOG_WATER_LEVEL_C_H
#define CATALOG_WATER_LEVEL_C_H

#include <stdint.h>

typedef struct water_level_t water_level_t;
typedef water_level_t *water_level_handle_t;

// HW-038: відкриті паралельні доріжки, чим глибше занурено — тим менший
// опір. Та сама електрична схема, що й soil_moisture.
water_level_handle_t water_level_init(int adc_channel);
void                  water_level_free(water_level_handle_t w);

int water_level_read_raw(water_level_handle_t w);

#endif // CATALOG_WATER_LEVEL_C_H
