#ifndef CATALOG_TILT_C_H
#define CATALOG_TILT_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct tilt_t tilt_t;
typedef tilt_t *tilt_handle_t;

// SW-520D: кулька котиться між двома контактами всередині трубки — нахил
// понад певний кут замикає/розмикає контакт. Механічний, як кнопка —
// очікуй дребезгу при швидкому опитуванні.
tilt_handle_t tilt_init(uint8_t gpio);
void          tilt_free(tilt_handle_t t);

// TODO: перевір активний рівень (high/low) на своєму модулі.
bool tilt_active(tilt_handle_t t);

#endif // CATALOG_TILT_C_H
