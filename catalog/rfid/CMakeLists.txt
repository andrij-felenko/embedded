idf_component_register(SRCS "rfid_c.c"
                        INCLUDE_DIRS "."
                        REQUIRES esp_driver_spi esp_driver_gpio)
