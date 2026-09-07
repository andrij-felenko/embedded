#ifndef CATALOG_LASER_C_H
#define CATALOG_LASER_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct laser_t laser_t;
typedef laser_t *laser_handle_t;

// KY-008: лазерний модуль, просте цифрове увімкнення/вимкнення, ШІМ не
// потрібен.
laser_handle_t laser_init(uint8_t gpio);
void           laser_free(laser_handle_t l);

void laser_set(laser_handle_t l, bool on);

#endif // CATALOG_LASER_C_H
