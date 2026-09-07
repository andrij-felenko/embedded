#ifndef CATALOG_BUZZER_C_H
#define CATALOG_BUZZER_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct buzzer_t buzzer_t;
typedef buzzer_t *buzzer_handle_t;

// TODO: з'ясуй, чи в тебе KY-006 (пасивний, потребує ШІМ на потрібній
// частоті) чи KY-012 (активний, власний генератор, просто увімк/вимк).
// Виглядають однаково, код драйвера — ні.
buzzer_handle_t buzzer_init(uint8_t gpio);
void            buzzer_free(buzzer_handle_t b);

void buzzer_set(buzzer_handle_t b, bool on);             // активний зумер
void buzzer_tone(buzzer_handle_t b, uint32_t freq_hz);   // пасивний зумер, 0 = тиша

#endif // CATALOG_BUZZER_C_H
