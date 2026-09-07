#ifndef CATALOG_VIBRATION_C_H
#define CATALOG_VIBRATION_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct vibration_t vibration_t;
typedef vibration_t *vibration_handle_t;

// KY-002 (SW-18020P): пружинний контакт, замикається коротко при
// поштовху/вібрації — це імпульс, не рівень. Опитування може пропустити
// його; подумай про переривання по фронту.
vibration_handle_t vibration_init(uint8_t gpio);
void                vibration_free(vibration_handle_t v);

bool vibration_triggered(vibration_handle_t v);

#endif // CATALOG_VIBRATION_C_H
