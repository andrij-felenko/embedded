#ifndef CATALOG_RELAY_C_H
#define CATALOG_RELAY_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct relay_t relay_t;
typedef relay_t *relay_handle_t;

// Songle SRD-05VDC-SL-C: GPIO керує власним транзистором модуля, не
// котушкою напряму — діод захисту вже на платі. Здебільшого активний LOW.
relay_handle_t relay_init(uint8_t gpio);
void           relay_free(relay_handle_t r);

// TODO: перевір активний рівень на своєму модулі.
void relay_set(relay_handle_t r, bool on);

#endif // CATALOG_RELAY_C_H
