#ifndef CATALOG_SEVEN_SEGMENT_C_H
#define CATALOG_SEVEN_SEGMENT_C_H

#include <stdint.h>

typedef struct seven_segment_t seven_segment_t;
typedef seven_segment_t *seven_segment_handle_t;

// 5641AS (4 розряди) або 5161AS (1 розряд): без драйвера, прямі GPIO —
// 8 виводів сегментів спільні на всі розряди, плюс один вивід вибору на
// розряд. Щоб показати різне на кожному розряді одночасно — потрібен
// мультиплекс (швидке перемикання розрядів).
seven_segment_handle_t seven_segment_init(const uint8_t segment_gpio[8], const uint8_t digit_gpio[4]);
void                     seven_segment_free(seven_segment_handle_t s);

void seven_segment_set_digits(seven_segment_handle_t s, const uint8_t digits[4], uint8_t count);
void seven_segment_refresh(seven_segment_handle_t s);   // просуває мультиплекс на один розряд

#endif // CATALOG_SEVEN_SEGMENT_C_H
