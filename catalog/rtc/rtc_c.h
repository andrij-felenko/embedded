#ifndef CATALOG_RTC_C_H
#define CATALOG_RTC_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct rtc_t rtc_t;
typedef rtc_t *rtc_handle_t;

typedef struct {
    uint16_t year;
    uint8_t  month, day, hour, minute, second;
} rtc_time_t;

// DS1302: НЕ I2C, НЕ SPI — власний 3-провідний протокол (CLK/DAT/RST).
// Значення в BCD, не в звичайних числах. Живиться від CR2032, тримає
// час без основного живлення.
rtc_handle_t rtc_init(uint8_t clk_gpio, uint8_t dat_gpio, uint8_t rst_gpio);
void         rtc_free(rtc_handle_t r);

bool rtc_get_time(rtc_handle_t r, rtc_time_t *out);
bool rtc_set_time(rtc_handle_t r, const rtc_time_t *t);

#endif // CATALOG_RTC_C_H
