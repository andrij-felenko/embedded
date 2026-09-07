#ifndef CATALOG_STEPPER_H
#define CATALOG_STEPPER_H

#include <stdint.h>

typedef struct stepper_t stepper_t;
typedef stepper_t *stepper_handle_t;

// 28BYJ-48 + ULN2003: чотири виводи котушок, керування напівкроковою
// послідовністю.
stepper_handle_t stepper_init(uint8_t in1, uint8_t in2, uint8_t in3, uint8_t in4);
void             stepper_free(stepper_handle_t s);

// steps/sec, зі знаком: знак = напрямок, 0 = стоп і знеструмити котушки.
void stepper_set_speed(stepper_handle_t s, int16_t steps_per_sec);

// Клич часто (кожну ітерацію циклу або з задачі) — сама вирішує, чи час
// робити наступний крок, залежно від пройденого часу.
void stepper_tick(stepper_handle_t s);

#endif // CATALOG_STEPPER_H
