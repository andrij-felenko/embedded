---
name: Hardware inventory
description: Full list of physical components available on the bench — boards, sensors, actuators, supporting parts. Use to decide what experiments are feasible without ordering anything new.
type: project
---

# Hardware Inventory

Total positions: ~112. Quantities are listed where multiple units are present; otherwise assume 1.

Parts on order are in [hardware_incoming.md](hardware_incoming.md) (#113-225, arduino.ua). Numbering is continuous across both files, so read them together to see the full bench after delivery.

## Single-board computers (SBC)

1. **Raspberry Pi 5** — Broadcom BCM2712, GPIO, 2× HDMI, 2× USB 3.0, 2× USB 2.0, Ethernet, PCIe
2. **Raspberry Pi 4 Model B** — in 3D-printed case with copper heatsink

## Microcontrollers

3. **Arduino UNO R3** (clone, CH340 chip)
4. **Arduino Nano** — 4 pcs (USB-C, ATmega chip)
5. **Waveshare ESP32-C6-Zero**
6. **Waveshare ESP32-S3-Pico**
7. **ESP32-S3 SuperMini** (USB-C)
8. **ESP32-CAM** — with OV2640 camera and microSD slot
9. **ESP-01S** — Wi-Fi module on ESP8266 (several pcs)
10. **ESP-01** — Wi-Fi module on ESP8266
11. **STM32F072B-DISCO** — Discovery kit with STM32F072RBT6 (ARM Cortex-M0, 48 MHz, 128 KB Flash, 16 KB SRAM, LQFP64). Onboard: ST-LINK/V2 debugger (Mini-USB, flash + hardware debug), ST MEMS gyroscope, linear touch sensor + touch keys, RF-EEPROM (M24LR/NFC) connector, USB device connector. First bare ARM/STM32 board here — `arm-none-eabi` toolchain, CMake + Qt Creator. NOTE: ST-LINK/V2 has no virtual COM port → use the CP2102 (#108) for a serial console.

## Flight controller and telemetry

12. **Pixhawk 6C** — flight controller
13. **FPV Radio Telemetry — Air Module** (with antenna)
14. **FPV Radio Telemetry — Ground Module** (USB)
15. **PWM adapters for Pixhawk** — 2 pcs
16. **Beitian BE-182** — GNSS/GPS module
17. **JST-GH signal cable kit** (for Pixhawk)

## Motors and servos

18. **N20 micro-motor** with metal gearbox — 2 pcs
19. **Tower Pro SG90** servo — Micro Servo 9g
20. **Power HD HD-1370A** servo — with horns and mounting
21. **28BYJ-48 stepper motor** (5VDC) + ULN2003 driver board — user reported +2 more units on 2026-07-08. CONFIRM: total count now, and whether the new ones ship with their own ULN2003 drivers (two drivers are needed to run two steppers, e.g. a pan/tilt rig).
22. **Solenoid JF-0530B** — push-pull electromagnetic linear actuator, **12 V / 0.3 A** (≈40 Ω, ≈3.6 W) — 2 pcs. Inductive load on a 12 V rail, separate from MCU logic (the DPS buck-boost #112 supplies the 12 V; two firing together = ~0.6 A). Drive low-side with a logic-level N-MOSFET + flyback (freewheeling) diode — OR via a spare ULN2003 channel (same part as the stepper driver, #21: 500 mA / 50 V Darlington with a built-in clamp diode, so 0.3 A @ 12 V fits with margin).
23. **Brushless motor (BLDC)** — for drone/RC modeling

## Power and batteries

24. **Li-ion Battery HAT** for Raspberry Pi (Micro USB + USB-A + USB-C)
25. **Videx 14500** Li-ion cells (3.7V) — 3 pcs, without leads
26. **YP-08** — power module

## Displays and indicators

27. **LCD 1602A** — character display 16×2 (blue)
28. **I2C adapter for LCD 1602** (PCF8574 / HLF8574T, FC-113)
29. **Seven-segment display 5641AS** — 4-digit
30. **Seven-segment display 5161AS** — 1-digit
31. **LED matrix 8×8** (1588BS)
32. **Multi-function Shield for Arduino UNO** — with 7-segment display, buttons, potentiometer, buzzer
33. **OLED display 0.96" SSD1306** — 128×64 monochrome graphic OLED, I2C (typ. address 0x3C). Graphic HUD for FSM state / sensor readouts / menus; works on both ESP32 and STM32.

## Input (buttons, keypads, encoders)

34. **Matrix keypad 4×4** (membrane)
35. **Matrix keypad 4×4** with tactile buttons
36. **KY-023 joystick module** — 2 pcs
37. **KY-040 rotary encoder** — with push button
38. **Tactile buttons with caps** — ~4–5 pcs
39. **Rotary potentiometer** (with shaft)
40. **KY-004** — tactile button on board

## Radio and communication

41. **Bluetooth module HC-05/HC-06**
42. **RFID-RC522** — RFID reader 13.56 MHz
43. **RFID keychain tag** (13.56 MHz)

## Sensors — environment

44. **DHT11** — temperature/humidity — 2 pcs
45. **GY-21 (Si7021/HTU21D)** — temperature/humidity (I2C)
46. **DS1302** — RTC module with CR2032 holder
47. **DFRobot SEN0290 (AS3935)** — lightning sensor (I2C)
48. **BMP280 / BME280** — barometric pressure + temperature sensor (BME280 variant also measures humidity); I2C (address 0x76/0x77) or SPI. Identify the exact chip via ID register 0xD0: 0x58 = BMP280, 0x60 = BME280. Pressure → altitude (altimeter); same role as on a flight controller.

## Sensors — motion and orientation

49. **HC-SR04** — ultrasonic distance sensor — 5 pcs
50. **TOF250** — laser distance sensor
51. **HC-SR501** — PIR motion sensor
52. **GY-61 ADXL335** — 3-axis accelerometer
53. **Pololu IMU module** (LSM6DS33 / MinIMU-9)
54. **GY-271 / HMC5883L** — compass / magnetometer
55. **SW-520D** — tilt / vibration sensor
56. **KY-002** — vibration sensor (SW-18020P)
57. **KY-020** — tilt sensor
58. **KY-021** — mini reed switch (magnetic)
59. **KY-025** — reed switch in glass tube
60. **KY-003 / KY-024** — Hall-effect sensor

## Sensors — light and sound

61. **KY-018** — photoresistor
62. **KY-008** — laser module
63. **KY-005** — IR transmitter
64. **KY-022** — IR receiver (on board)
65. **VS1838B** — IR receiver (standalone)
66. **KY-026** — flame sensor
67. **Sound sensor with microphone** (LM393)
68. **KY-038** — microphone sound sensor — several pcs
69. **KY-037** — sound sensor (large microphone)
70. **TTP223** — touch sensor module

## Sensors — temperature and gas

71. **KY-013** — analog temperature sensor (thermistor)
72. **KY-028** — digital temperature sensor
73. **MQ gas sensor** (Keyes K869051)
74. **GY-MAX30102** — pulse / SpO2 sensor
75. **KY-039** — pulse sensor

## Sensors — water and soil

76. **Soil moisture sensor** — 3 sets (probes + LM393 modules)
77. **HW-038** — water level sensor
78. **Funduino rain sensor** — sensor plate + LM358 module

## Sensors — optical / IR

79. **IR obstacle sensors** (FC-51 / KY-032) — 4 pcs
80. **KY-010** — optical interrupter (photo interrupter)
81. **KY-031** — knock sensor

## LEDs and signaling

82. **5mm LED kit** — assorted colors, many pcs
83. **KY-016** — RGB LED (full color)
84. **KY-009** — RGB SMD LED module (3-color)
85. **KY-034** — 7-color flash LED module
86. **KY-027** — Magic Light Cup (with mercury switch)
87. **KY-006** — passive buzzer
88. **KY-012** — active buzzer
89. **Buzzer** — standalone

## Relays and drivers

90. **5V relay module** (1-channel, Songle SRD-05VDC-SL-C) — 2 pcs
91. **CJMCU MC33886** — motor driver (5A H-bridge)

## Cooling

92. **5V brushless fans** — 2 pcs (hydrodynamic bearing)

## Small components

93. **Pin headers** — male, large quantity
94. **DIP ICs** — several pcs (drivers)
95. **Servo horns** (white, spare)

## Fabrication

96. **3D printer** — operational. Custom STL parts authored in Blender by the user.

## Passive components

97. **Resistor kit** — large quantity, various values (330R, 1K, 2K2, 5K1 and others), carbon and metal-film
98. **Capacitors** — assortment (ceramic, electrolytic)
99. **Transistors** — organizer with ~10 sections, various types (TO-92)

## Tools and prototyping

100. **Side cutters / wire cutters** — in blister packs
101. **Breadboard (large)** — full-size prototyping board
102. **Breadboard (mini)** — small prototyping board
103. **GPIO Extension Board** — for Raspberry Pi (red board + ribbon cable)
104. **GPIO ribbon cable** — 40-pin rainbow
105. **Dupont jumper wires** — large quantity (M-M, M-F, F-F)
106. **Ethernet cable** — RJ45
107. **Cable organizer / hook-and-loop strap**
108. **USB-UART adapter CP2102** (Micro-USB) — USB↔TTL serial bridge (3.3/5V). Serial console (printf/monitor) and UART-bootloader flashing for boards without native USB (bare STM32 via BOOT0, ESP-01, etc.). Pairs with the STM32F072B-DISCO (#11), whose ST-LINK/V2 exposes no virtual COM port.

## Miscellaneous

109. **LiPo battery** — XT60 connector, ~3S
110. **Mini-PC Chuwi** (Intel) — compact x86 PC
111. **Solder / tin** — for soldering, kept in a repurposed jar
112. **Programmable DC-DC buck-boost converter** (DPS/DPH-type) — with LCD, encoder, buttons (V/A, SET, A/V, ON/OFF); separate power board with fan and IN+/OUT+ terminals
