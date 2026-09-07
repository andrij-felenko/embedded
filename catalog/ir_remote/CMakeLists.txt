idf_component_register(SRCS "ir_remote_c.c"
                        INCLUDE_DIRS "."
                        REQUIRES esp_driver_gpio esp_driver_rmt)
