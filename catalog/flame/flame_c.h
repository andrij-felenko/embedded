#ifndef CATALOG_FLAME_C_H
#define CATALOG_FLAME_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct flame_t flame_t;
typedef flame_t *flame_handle_t;

// KY-026: має і цифровий поріг (D0, з підстроювальним резистором на
// платі), і сирий аналоговий вихід (A0). Передай 0xFF / -1 для невживаної
// сторони.
flame_handle_t flame_init(uint8_t digital_gpio, int adc_channel);
void           flame_free(flame_handle_t f);

// TODO: перевір активний рівень на своєму модулі.
bool flame_detected(flame_handle_t f);
int  flame_read_raw(flame_handle_t f);

#endif // CATALOG_FLAME_C_H
