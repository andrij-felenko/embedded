#include "ir_remote_c.h"
#include <stdlib.h>

// Маємо: GPIO(и) для ІЧ-передавача (KY-005) і/або приймача (VS1838B/KY-022),
// протокол NEC на несучій 38кГц.
// Завдання: передавати і/або приймати коди пультів через периферію RMT
// (несучу й точний таймінг вручну бітбенгити важко).

struct ir_remote_t {
    uint8_t tx_gpio;
    uint8_t rx_gpio;
};

ir_remote_handle_t ir_remote_init(uint8_t tx_gpio, uint8_t rx_gpio)
{
    return NULL;
}

void ir_remote_free(ir_remote_handle_t ir)
{
}

void ir_remote_send(ir_remote_handle_t ir, uint32_t nec_code)
{
}

bool ir_remote_receive(ir_remote_handle_t ir, uint32_t *nec_code)
{
    if (nec_code) *nec_code = 0;
    return false;
}
