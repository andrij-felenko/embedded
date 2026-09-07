#ifndef CATALOG_GPS_C_H
#define CATALOG_GPS_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct gps_t gps_t;
typedef gps_t *gps_handle_t;

typedef struct {
    double  lat, lon;
    float   alt_m;
    uint8_t satellites;
    bool    fix;
} gps_fix_t;

// Beitian BE-182: звичайний UART, постійно шле речення NMEA 0183 (без
// запит-відповідь — просто читаєш і розбираєш). Розбір NMEA — це робота
// з текстом, не з регістрами.
gps_handle_t gps_init(int uart_num, uint8_t rx_gpio, int baud);
void         gps_free(gps_handle_t g);

bool gps_read(gps_handle_t g, gps_fix_t *out);

#endif // CATALOG_GPS_C_H
