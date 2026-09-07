#ifndef CATALOG_IR_OBSTACLE_C_H
#define CATALOG_IR_OBSTACLE_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct ir_obstacle_t ir_obstacle_t;
typedef ir_obstacle_t *ir_obstacle_handle_t;

// FC-51 / KY-032: власна пара ІЧ-світлодіод + приймач з компаратором і
// підстроювальним резистором. Лише цифровий вихід.
ir_obstacle_handle_t ir_obstacle_init(uint8_t gpio);
void                  ir_obstacle_free(ir_obstacle_handle_t o);

bool ir_obstacle_detected(ir_obstacle_handle_t o);

#endif // CATALOG_IR_OBSTACLE_C_H
