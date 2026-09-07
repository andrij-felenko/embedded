#ifndef CATALOG_JOYSTICK_C_H
#define CATALOG_JOYSTICK_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct joystick_t joystick_t;
typedef joystick_t *joystick_handle_t;

// KY-023: два потенціометри (осі X, Y) + кнопка під стиком. Комбінація
// potentiometer_c.h (x2) і звичайної кнопки. Значення в спокої не
// обов'язково точно посередині діапазону — виміряй своє.
joystick_handle_t joystick_init(int adc_channel_x, int adc_channel_y, uint8_t button_gpio);
void               joystick_free(joystick_handle_t j);

void joystick_read(joystick_handle_t j, int *x_raw, int *y_raw);
bool joystick_button_pressed(joystick_handle_t j);

#endif // CATALOG_JOYSTICK_C_H
