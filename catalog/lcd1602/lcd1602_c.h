#ifndef CATALOG_LCD1602_C_H
#define CATALOG_LCD1602_C_H

#include <stdint.h>

typedef struct lcd1602_t lcd1602_t;
typedef lcd1602_t *lcd1602_handle_t;

// Символьний LCD 16x2 за перехідником PCF8574 (I2C, адреса зазвичай 0x27
// або 0x3F). Контролер HD44780 під ним хоче 4-бітний протокол —
// кожен символ це два записи по I2C, не один.
lcd1602_handle_t lcd1602_init(int i2c_port, uint8_t i2c_addr, uint8_t sda_gpio, uint8_t scl_gpio);
void              lcd1602_free(lcd1602_handle_t l);

void lcd1602_clear(lcd1602_handle_t l);
void lcd1602_set_cursor(lcd1602_handle_t l, uint8_t col, uint8_t row);
void lcd1602_print(lcd1602_handle_t l, const char *text);

#endif // CATALOG_LCD1602_C_H
