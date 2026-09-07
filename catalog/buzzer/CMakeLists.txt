idf_component_register(SRCS "buzzer_c.c"
                        INCLUDE_DIRS "."
                        REQUIRES esp_driver_gpio esp_driver_ledc)
