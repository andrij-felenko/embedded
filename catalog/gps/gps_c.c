#include "gps_c.h"
#include <stdlib.h>
#include <string.h>

// Маємо: UART, що постійно отримує речення NMEA 0183 від приймача Beitian BE-182.
// Завдання: підготувати UART і розбирати чергове речення (напр. $GPGGA)
// у координати/висоту/супутники/фікс.

struct gps_t {
    int     uart_num;
    uint8_t rx_gpio;
    int     baud;
};

gps_handle_t gps_init(int uart_num, uint8_t rx_gpio, int baud)
{
    return NULL;
}

void gps_free(gps_handle_t g)
{
}

bool gps_read(gps_handle_t g, gps_fix_t *out)
{
    if (out) memset(out, 0, sizeof(*out));
    return false;
}
