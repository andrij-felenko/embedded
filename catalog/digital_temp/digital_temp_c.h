#ifndef CATALOG_DIGITAL_TEMP_C_H
#define CATALOG_DIGITAL_TEMP_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct digital_temp_t digital_temp_t;
typedef digital_temp_t *digital_temp_handle_t;

// KY-028: попри назву, чутливий елемент — термістор (аналоговий, A0), як
// у thermistor_c.h. Ще є цифровий поріг (D0), як у flame_c.h.
digital_temp_handle_t digital_temp_init(uint8_t digital_gpio, int adc_channel);
void                   digital_temp_free(digital_temp_handle_t d);

bool  digital_temp_threshold_hit(digital_temp_handle_t d);
float digital_temp_read_c(digital_temp_handle_t d);

#endif // CATALOG_DIGITAL_TEMP_C_H
