#ifndef CATALOG_COMPASS_C_H
#define CATALOG_COMPASS_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct compass_t compass_t;
typedef compass_t *compass_handle_t;

// GY-271 / HMC5883L: I2C магнітометр, адреса за замовчуванням 0x1E.
// Порядок осей у регістрах для цього чіпа не X,Y,Z — уточни в даташиті.
compass_handle_t compass_init(int i2c_port, uint8_t sda_gpio, uint8_t scl_gpio);
void              compass_free(compass_handle_t c);

bool compass_heading_deg(compass_handle_t c, float *heading_deg);

#endif // CATALOG_COMPASS_C_H
