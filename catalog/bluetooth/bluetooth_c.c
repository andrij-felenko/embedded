#include "bluetooth_c.h"
#include <stdlib.h>

// Маємо: UART, з'єднаний з модулем HC-05/HC-06 (Bluetooth-з'єднання вже на рівні модуля).
// Завдання: підготувати UART і передавати/приймати байти.

struct bluetooth_t {
    int     uart_num;
    uint8_t tx_gpio, rx_gpio;
    int     baud;
};

bluetooth_handle_t bluetooth_init(int uart_num, uint8_t tx_gpio, uint8_t rx_gpio, int baud)
{
    return NULL;
}

void bluetooth_free(bluetooth_handle_t b)
{
}

int bluetooth_write(bluetooth_handle_t b, const uint8_t *data, size_t len)
{
    return -1;
}

int bluetooth_read(bluetooth_handle_t b, uint8_t *buf, size_t buf_len, int timeout_ms)
{
    return -1;
}
