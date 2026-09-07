#ifndef CATALOG_OLED_C_H
#define CATALOG_OLED_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct oled_t oled_t;
typedef oled_t *oled_handle_t;

// 128x64 SSD1306, I2C, адреса зазвичай 0x3C. Простіший протокол за LCD
// (без нібл), але потрібна повна послідовність ініціалізації і буфер
// кадру 1024 байти (128x64 / 8 біт на байт).
oled_handle_t oled_init(int i2c_port, uint8_t i2c_addr, uint8_t sda_gpio, uint8_t scl_gpio);
void          oled_free(oled_handle_t o);

void oled_clear(oled_handle_t o);
void oled_set_pixel(oled_handle_t o, uint8_t x, uint8_t y, bool on);
void oled_flush(oled_handle_t o);

#endif // CATALOG_OLED_C_H
