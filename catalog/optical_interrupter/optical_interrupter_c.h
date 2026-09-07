#ifndef CATALOG_OPTICAL_INTERRUPTER_C_H
#define CATALOG_OPTICAL_INTERRUPTER_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct optical_interrupter_t optical_interrupter_t;
typedef optical_interrupter_t *optical_interrupter_handle_t;

// KY-010: оптична вилка (ІЧ-світлодіод + фототранзистор навпроти одне
// одного через щілину). LOW, коли щось перекриває щілину.
optical_interrupter_handle_t optical_interrupter_init(uint8_t gpio);
void                          optical_interrupter_free(optical_interrupter_handle_t o);

bool optical_interrupter_blocked(optical_interrupter_handle_t o);

#endif // CATALOG_OPTICAL_INTERRUPTER_C_H
