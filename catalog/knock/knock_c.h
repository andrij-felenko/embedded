#ifndef CATALOG_KNOCK_C_H
#define CATALOG_KNOCK_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct knock_t knock_t;
typedef knock_t *knock_handle_t;

// KY-031: п'єзодиск, короткий сплеск при ударі. Здебільшого лише
// цифровий компаратор — той самий "короткий імпульс", що й vibration_c.h.
knock_handle_t knock_init(uint8_t gpio);
void           knock_free(knock_handle_t k);

bool knock_detected(knock_handle_t k);

#endif // CATALOG_KNOCK_C_H
