#ifndef CATALOG_REED_SWITCH_C_H
#define CATALOG_REED_SWITCH_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct reed_switch_t reed_switch_t;
typedef reed_switch_t *reed_switch_handle_t;

// KY-021: механічний геркон, замикається біля магніту. Електрично як
// кнопка — той самий дребезг, підтягуючий резистор на вході.
reed_switch_handle_t reed_switch_init(uint8_t gpio);
void                  reed_switch_free(reed_switch_handle_t r);

bool reed_switch_closed(reed_switch_handle_t r);

#endif // CATALOG_REED_SWITCH_C_H
