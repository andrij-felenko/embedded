#ifndef CATALOG_HALL_C_H
#define CATALOG_HALL_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct hall_t hall_t;
typedef hall_t *hall_handle_t;

// KY-003/KY-024: вихід з відкритим стоком, тягне LOW біля магніту —
// потрібен підтягуючий резистор на вході.
hall_handle_t hall_init(uint8_t gpio);
void          hall_free(hall_handle_t h);

bool hall_magnet_present(hall_handle_t h);

#endif // CATALOG_HALL_C_H
