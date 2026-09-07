#ifndef CATALOG_POTENTIOMETER_C_H
#define CATALOG_POTENTIOMETER_C_H

#include <stdint.h>

typedef struct potentiometer_t potentiometer_t;
typedef potentiometer_t *potentiometer_handle_t;

// Звичайний резистивний подільник, один канал АЦП, без мікросхеми —
// найпростіший аналоговий вхід у каталозі.
potentiometer_handle_t potentiometer_init(int adc_channel);
void                    potentiometer_free(potentiometer_handle_t p);

int potentiometer_read_raw(potentiometer_handle_t p);

#endif // CATALOG_POTENTIOMETER_C_H
