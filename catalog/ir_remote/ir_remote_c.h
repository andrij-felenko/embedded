#ifndef CATALOG_IR_REMOTE_C_H
#define CATALOG_IR_REMOTE_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct ir_remote_t ir_remote_t;
typedef ir_remote_t *ir_remote_handle_t;

// KY-005 (ІЧ-світлодіод, TX) + VS1838B/KY-022 (приймач, RX). Два окремі
// GPIO — передай 0xFF для невживаної сторони. Протокол NEC на несучій
// 38кГц — вручну бітбенгити важко, є периферія RMT саме для цього.
ir_remote_handle_t ir_remote_init(uint8_t tx_gpio, uint8_t rx_gpio);
void                 ir_remote_free(ir_remote_handle_t ir);

void ir_remote_send(ir_remote_handle_t ir, uint32_t nec_code);
bool ir_remote_receive(ir_remote_handle_t ir, uint32_t *nec_code);

#endif // CATALOG_IR_REMOTE_C_H
