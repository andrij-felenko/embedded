#ifndef CATALOG_SOUND_C_H
#define CATALOG_SOUND_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct sound_t sound_t;
typedef sound_t *sound_handle_t;

// KY-038 (або окремий модуль з LM393): цифровий поріг (D0) + аналогова
// обвідна (A0). Передай 0xFF / -1 для невживаної сторони.
sound_handle_t sound_init(uint8_t digital_gpio, int adc_channel);
void           sound_free(sound_handle_t s);

bool sound_threshold_hit(sound_handle_t s);
int  sound_read_raw(sound_handle_t s);

#endif // CATALOG_SOUND_C_H
