#ifndef CATALOG_PIR_C_H
#define CATALOG_PIR_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct pir_t pir_t;
typedef pir_t *pir_handle_t;

// HC-SR501: цифровий HIGH, поки бачить рух, звичайний вхід GPIO, без шини,
// без калібрування при старті — найпростіший можливий компонент каталогу.
pir_handle_t pir_init(uint8_t gpio);
void         pir_free(pir_handle_t p);

bool pir_motion(pir_handle_t p);

#endif // CATALOG_PIR_C_H
