#ifndef CATALOG_ROTARY_ENCODER_C_H
#define CATALOG_ROTARY_ENCODER_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct rotary_encoder_t rotary_encoder_t;
typedef rotary_encoder_t *rotary_encoder_handle_t;

// KY-040: пара CLK/DT (квадратурна) + кнопка (SW). Схожа логіка вже
// написана в ardu/experiments/encoder_stepper/encoder_stepper.ino, можеш
// підглянути ідею (не копіювати як TODO-підказку, а зрозуміти принцип).
rotary_encoder_handle_t rotary_encoder_init(uint8_t clk_gpio, uint8_t dt_gpio, uint8_t sw_gpio);
void                      rotary_encoder_free(rotary_encoder_handle_t e);

int  rotary_encoder_poll(rotary_encoder_handle_t e);
bool rotary_encoder_button_pressed(rotary_encoder_handle_t e);

#endif // CATALOG_ROTARY_ENCODER_C_H
