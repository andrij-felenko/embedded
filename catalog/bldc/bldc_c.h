#ifndef CATALOG_BLDC_C_H
#define CATALOG_BLDC_C_H

#include <stdint.h>

typedef struct bldc_t bldc_t;
typedef bldc_t *bldc_handle_t;

// Керується через звичайний ESC, не напряму — комутацію фаз робить сам
// ESC. З боку МК електрично те саме, що й серво (50Гц, 1-2мс). Різниця
// в поведінці: більшість ESC вимагають послідовність армування при
// старті, інакше ігнорують команди.
bldc_handle_t bldc_init(uint8_t gpio);
void          bldc_free(bldc_handle_t m);

void bldc_arm(bldc_handle_t m);
void bldc_set_throttle(bldc_handle_t m, uint8_t percent);   // 0..100

#endif // CATALOG_BLDC_C_H
