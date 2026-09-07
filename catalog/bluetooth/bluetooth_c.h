#ifndef CATALOG_BLUETOOTH_C_H
#define CATALOG_BLUETOOTH_C_H

#include <stdint.h>
#include <stddef.h>

typedef struct bluetooth_t bluetooth_t;
typedef bluetooth_t *bluetooth_handle_t;

// HC-05/HC-06: класичний Bluetooth SPP, вже з'єднаний на рівні модуля —
// з боку МК це просто UART, ніякого BT-стеку тут не потрібно.
bluetooth_handle_t bluetooth_init(int uart_num, uint8_t tx_gpio, uint8_t rx_gpio, int baud);
void                bluetooth_free(bluetooth_handle_t b);

int bluetooth_write(bluetooth_handle_t b, const uint8_t *data, size_t len);
int bluetooth_read(bluetooth_handle_t b, uint8_t *buf, size_t buf_len, int timeout_ms);

#endif // CATALOG_BLUETOOTH_C_H
