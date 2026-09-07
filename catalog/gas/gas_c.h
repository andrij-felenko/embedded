#ifndef CATALOG_GAS_C_H
#define CATALOG_GAS_C_H

#include <stdint.h>

typedef struct gas_t gas_t;
typedef gas_t *gas_handle_t;

// MQ-серія (Keyes K869051): аналоговий вихід, потребує часу прогріву
// перед тим, як показання матимуть сенс.
gas_handle_t gas_init(int adc_channel);
void         gas_free(gas_handle_t g);

int gas_read_raw(gas_handle_t g);

#endif // CATALOG_GAS_C_H
