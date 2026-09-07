#include "ir_obstacle_c.h"
#include <stdlib.h>

// Маємо: GPIO пін ІЧ-датчика перешкоди FC-51/KY-032 (своя пара TX+RX і компаратор).
// Завдання: підготувати пін і повертати, чи є перешкода в зоні дії.

struct ir_obstacle_t {
    uint8_t gpio;
};

ir_obstacle_handle_t ir_obstacle_init(uint8_t gpio)
{
    return NULL;
}

void ir_obstacle_free(ir_obstacle_handle_t o)
{
}

bool ir_obstacle_detected(ir_obstacle_handle_t o)
{
    return false;
}
