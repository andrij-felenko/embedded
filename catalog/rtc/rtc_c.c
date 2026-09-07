#include "rtc_c.h"
#include <stdlib.h>
#include <string.h>

// Маємо: три GPIO піни годинника DS1302 (власний 3-провідний протокол, значення в BCD).
// Завдання: підготувати піни і читати/писати час, декодуючи/кодуючи BCD.

struct rtc_t {
    uint8_t clk, dat, rst;
};

rtc_handle_t rtc_init(uint8_t clk_gpio, uint8_t dat_gpio, uint8_t rst_gpio)
{
    return NULL;
}

void rtc_free(rtc_handle_t r)
{
}

bool rtc_get_time(rtc_handle_t r, rtc_time_t *out)
{
    if (out) memset(out, 0, sizeof(*out));
    return false;
}

bool rtc_set_time(rtc_handle_t r, const rtc_time_t *t)
{
    return false;
}
