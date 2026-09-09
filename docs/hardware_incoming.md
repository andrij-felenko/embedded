---
name: Hardware incoming (arduino.ua order)
description: Everything in the arduino.ua cart, numbered to continue hardware.md. Read together with hardware.md to see the full bench after delivery.
type: project
---

# Hardware Incoming — arduino.ua

**Order № 651018 · 171 positions · 569 units · 42 443 UAH** (delivered 07.09.2026)

Placed 2026-09-06 02:48, status *Новий*, payment pending, Nova Poshta to Cherkasy.
Every line was in stock at the time of ordering.

Numbering continues [hardware.md](hardware.md) (#1–112), so `#118` means the same
thing in both files. Rationale for each choice lives in [shopping.md](shopping.md);
the machines these parts serve are in [vehicles.md](vehicles.md).

> Quantities are what was ordered. Prices are cart line totals in UAH
> (not per-unit), as computed by the site.

## Microcontrollers and dev boards

113. **WeAct STM32G431CBU6** — 2 pcs. Cortex-M4F @ 170 MHz, 128 KB Flash, 32 KB SRAM. The real-time half of every vehicle: timer PWM, encoder mode, ADC on timer trigger with DMA, PID, failsafe. A genuine ST part, unlike the HK32 clone.
114. **Waveshare ESP32-S3R2** — 16 MB Flash, **2 MB PSRAM** (that is what the `R2` suffix means). The only board here with PSRAM, so the only one that can hold a JPEG frame buffer. Reserved for the video half of the remote.
115. **ESP32-S3-Zero Type-C 4 MB** — 2 pcs. Small, USB-C, native USB. General ESP32 workhorses.
116. **WeAct ESP32-C6-Mini** — RISC-V, Wi-Fi 6 + BLE 5 + **802.15.4** (Thread/Zigbee). The control half of the remote: sticks, switches, radio, small TFT.
117. **WeAct Mini Debugger DAPLink / ST-Link V2.1** — flashes and debugs the bare G431 boards, **and exposes a virtual COM port**, which the onboard ST-LINK of the STM32F072B-DISCO (#11) does not.
118. **ESP32 + OV3640 2 MP camera module** — 2 pcs. On-vehicle camera. Note: almost no free GPIO is left after camera + SD.
119. **ESP32-CAM programming adapter CH340 Type-C** — for the ESP32-CAM already owned (#8), which has no USB of its own.
120. **ESP-01 power/breakout adapter** — 2 pcs. For the ESP-01/ESP-01S already owned (#9, #10).

## Radio

121. **nRF24L01+PA+LNA, external SMA antenna** — the long-range 2.4 GHz module. Goes on the remote.
122. **Ai-Thinker nRF24L01+** — 4 pcs. Plain modules: rover, racing car, remote, plus one spare.
123. **nRF24L01 adapter boards** — 4 pcs, one per plain module. **These carry the regulator. Brownout on the 3.3 V rail is the number-one cause of nRF24 failures** — never wire a bare module straight to a 3.3 V pin on a dev board.
124. **CC1101 433 MHz with SMA** — 2 pcs. A pair is one link. Raw packets over SPI, so the protocol (CRC, ACK, sequence numbers, hopping) gets written by hand. This is the teaching radio.
125. **433 MHz SMA antenna 3 dBi** — 2 pcs, one per CC1101.
126. **2.4 GHz Wi-Fi SMA antenna 2 dBi** — 2 pcs, for #121 plus a spare.
127. **Elecrow ThinkNode M2 (Meshtastic)** — 2 pcs. ESP32-S3 + **SX1262**, 868/915 MHz, 1.3" OLED, 1000 mAh battery. Ships with Meshtastic **but is reflashable**, so it doubles as an SX1262 dev board for writing a LoRa driver over SPI. Two of them, because a mesh cannot be tested from one node.
128. **SMA-jack to U.FL pigtail, 15 cm** — 3 pcs. Brings the antenna outside a printed enclosure. Mandatory for the sealed boat.
129. **SMA-female solder pigtail, 15 cm** — 2 pcs. Own connector on own board.

> **RP-SMA and SMA look identical and are not compatible** — pin and socket are
> swapped. Check before ordering more antennas.
>
> **LoRa cannot carry stick control.** SF7 is ~5.5 kbps; SF12 is ~250 bps with
> packets over a second long. It is for commands and telemetry on a vehicle that
> drives itself, not for a control loop. 868 MHz also has a ~1 % duty-cycle limit.

## Motors, drivers, servos

130. **6 V 100 RPM gearmotor** — 6 pcs. Rover drive, one per wheel. About 4 kg·cm each, 24 kg·cm total against a calculated requirement of 11.4. The 300 RPM variant was rejected: only 9 kg·cm, not enough.
131. **6 V 600 RPM gearmotor** — 2 pcs. Racing car. On Ø65 wheels that is about 2.0 m/s.
132. **MC33886 H-bridge driver module** — 2 pcs (a third, #91, is already owned). 5 A per channel. Six motors is not six channels: each side turns as one, so **three motors in parallel per channel** = 4.5 A stall per channel.
133. **MG90S V2 servo, metal gears** — 4 pcs. Rover pan/tilt (2), racing car Ackermann steering (1), boat rudder (1).
134. **BLHeli 30 A ESC with 2 A / 5 V BEC** — boat propeller. Takes servo PWM, so the ESP32 drives it with no second board.
135. **Mini water pump RS-360SH** — brushed, submersible. Boat bilge, watering rig, or any liquid-moving experiment. Quiet type, which was the stated requirement.
136. **CCPM servo/ESC mini tester** — exercises a servo or ESC with no firmware. The fastest way to tell a dead actuator from a dead signal.

## Bearings and mechanical

137. **623-2RS 3×10×4** — 10 pcs. **Rubber-sealed.** Pan/tilt, GT2 idlers, small pivots.
138. **685ZZ 5×11×5** — 10 pcs. Metal shield, so indoor and dry only. Rocker-bogie pivots, steering knuckles.
139. **625-2RS 5×16×5** — 6 pcs. **Rubber-sealed.** Wheels, and anywhere there is mud.
140. **686ZZ 6×13×5** — 6 pcs. Metal shield. Largest axles.

> **ZZ is not 2RS.** ZZ is a metal shield: it keeps chips out, not water. 2RS is a
> rubber seal. Only #137 and #139 go outside.
>
> **Shafts are printed.** No Ø5/Ø6 rod exists in this shop and no screw larger than
> M3. A printed Ø5 shaft comes out at ±0.2 mm against a 5.00 mm bore — print
> oversize and finish with the needle files (#221). **PLA will creep** under a 3 kg
> standing load within weeks; Nylon (#225) is the right material, since abrasion
> resistance is its main property.

141. **GT2-6 belt with cord, 1 m** — 2 pcs.
142. **GT2 pulley 16 T** ×2 and **GT2 pulley 20 T, Ø5 bore** ×2. A 20:16 reduction removes backlash and moves the motor off the rotating axis on a pan/tilt turret.
143. **GT2 belt tensioner spring** — 4 pcs.
144. **Flexible coupler 5×5×25 mm** — 2 pcs. Absorbs the misalignment that would otherwise load the bearing.
145. **Silicone grease SI-180, 10 ml syringe** — for printed-on-printed sliding surfaces; unlike petroleum grease it does not attack the plastic.

## Power — conversion

146. **Mini560 fixed 5 V buck** — 3 pcs. The workhorse: tiny, high efficiency.
147. **MP1482 (MINI360-V2) adjustable buck** — 3 pcs. The smallest adjustable one.
148. **XL4015E 5 A adjustable buck** — 2 pcs. High-current rail.
149. **LM2596 adjustable buck** — 1 pc. The classic reference part.
150. **LM2596S with CC/CV** — 1 pc. Limits **current as well as voltage**: a pocket lab supply and a crude charger.
151. **Boost converters** — MT3608 2 A/28 V ×2, 0.9–4.2 V → 5 V ×2, XL6009 3–32 V → 5–35 V ×2, IP5310 5 V/3 A USB-A+C ×2.
152. **Hobbywing UBEC 3 A, 2–6S** — the vehicle logic rail. Covers the ESP32 (~0.5 A peaks) and STM32 (~50 mA) with margin.
153. **B0505S-1W isolated 5 V → 5 V** — 2 pcs. Galvanic isolation for a measurement or comms leg.
154. **Single-to-bipolar 5 V → ±12 V converter** — for op-amp and analogue experiments.
155. **ESC power distribution board** — one battery in, several ESCs out.

> **Separate supplies for motors and logic, but grounds joined at a single star
> point.** Without a common ground the STM32-to-driver signal has no reference.

## Power — batteries, charging, protection

156. **LiitoKala HG2 18650 3000 mAh, solder tabs** — 9 pcs.
157. **LiitoKala NCR18650B 3200 mAh, solder tabs** — 3 pcs.
158. **EVE INR21700-40P 4000 mAh 50 A** — 8 pcs. **Bare cells with no tabs, so these must be spot-welded.** A soldering iron holds the can hot long enough to damage the separator.
159. **MECHANIC PN360 spot welder** — 650 A, dual pulse (the first breaks the oxide, the second welds), 4000 mAh, TFT, 3 profiles. Test method: weld a strip and pull it with pliers — if the strip tears while the weld holds, the setting is right. 0.15 mm nickel is its limit; for more current use two strips in parallel, never a thicker one.
160. **Nickel strip 0.15×10 mm, 1 m** — 5 pcs.
161. **SkyRC iMAX B6 Mini (genuine)** — balance charger. The genuine one specifically: clones misread cell voltage, and 0.1 V past 4.2 swells a pack.
162. **Protection boards** — BMS 1S 3 A with tabs ×5, BMS 1S 5 A ×5, BMS 2S 20 A balancing ×2, BMS 3S 11.1 V ×2, BMS 4S 14.8 V ×2, 4S 40 A balanced charge/protect ×2.
163. **TP4056 Type-C with protection** — 5 pcs. Linear 1S charger. **Not MPPT** — roughly 60–70 % efficient from a solar panel.
164. **TP5100 1S/2S charger** ×2 and **MH-CD42 1S charge+discharge 5 V/2 A** ×2.
165. **Solar panel 6 V / 2 W, 136×110 mm** — 2 pcs. Cannot drive the rover (4.8 W against a ~2.5 A draw) but will run a sleeping LoRa node indefinitely.
166. **LiPo 1–8S low-voltage alarm** and **Lipo Guard bag 23×29 cm**.
167. **18650 insulator washers** ×12 and **18650 heat-shrink sleeves** ×12.

## Displays

168. **OLED 0.91" 128×32 I2C, white** — 1 pc. A 4:1 strip.
169. **OLED 0.96" 128×64 I2C, yellow** — 4 pcs. 2:1, nearly square, twice the pixels, same price as the strip. Robot faces and status readouts. 1024 bytes per frame, about 26 ms over I2C at 400 kHz, so roughly 35 fps.
170. **IPS 1.3" 240×240 SPI (ST7789)** ×1 and **TFT 1.77" 128×160 SPI (ST7735S)** ×1 — two different controllers and two different panel types (IPS against TN), deliberately, to compare. The 1.77" has **PWM backlight control**, which is real battery saving: the backlight draws more than the matrix.
171. **WS2812B 5050 addressable LED** — 20 pcs. One data line, chainable.

> **OLED burn-in is real** — a static face leaves a ghost within hours. The cure is
> what makes a robot look alive anyway: blink, change expression, shift the image a
> few pixels, dim when idle.

## Sensors

172. **VL53L0X-V2 laser ToF, 940 nm** — 3 pcs. About 50 readings per second. Enough for slow room mapping on a turntable, not for obstacle avoidance at speed.
173. **Sharp GP2Y0A21YK0F IR distance, 10–80 cm** — analogue, and a different physical principle from ToF: triangulation, not time of flight.
174. **TCRT5000 IR reflective module** — 6 pcs. Encoder discs and line following.
175. **HC-SR505 PIR motion** — 3 pcs. A plain 5 V sensor with a logic output; nothing to do with mains.
176. **MPU-6050 GY-521 6DOF** ×2, **ADXL345 3-axis accelerometer** ×1, **QMC5883L compass** ×1.

> **Accelerometer plus gyro alone cannot hold a heading.** The gyro drifts and the
> accelerometer only gives the direction of gravity; yaw needs a magnetometer.
> MPU-6050 + QMC5883L is the same sensor set as a BNO055, with the fusion written
> in software instead of hidden inside the chip — which is the point.

177. **DS18B20 digital 1-Wire** ×6 — 64-bit addresses, many sensors on one pin.
178. **SHT30 I2C temperature and humidity** ×2, **AHT20+BMP280** ×2 (adds pressure).
179. **PT100 platinum RTD, waterproof** ×1 — resistance-based, needs signal conditioning.
180. **LM35DZ analogue** ×2 — 10 mV per °C straight into an ADC.
181. **A3144 Hall module** ×3 — position and RPM sensing off a magnet. (SS41F ×10 was dropped: out of stock.)
182. **Water flow sensor G1/2"** — turbine plus Hall. The output is a **frequency**, so it is measured by counting pulses, not with the ADC.
183. **Liquid level sensor** ×2.
184. **MQ-7 carbon monoxide** ×1 — a plain 5 V sensor; needs a heater duty cycle.
185. **Red line laser 5 mW, adjustable focus** — structured lighting for machine vision.
186. **Current sensing** — ACS712 5 A ×2 (185 mV/A, one per drive channel), ACS712 30 A ×1 (main bus), INA219 I2C ×1 (telemetry). Battery voltage is measured with a divider on resistors already owned (#97).
187. **MEMS microphone module for ESP32** ×2 — I2S, digital. The recording end of the audio path.

## Audio playback (deliberately minimal)

188. **XPT8871 mono 5 W amplifier** ×2 — **analogue input**, so it is fed from the built-in 8-bit DAC of the ESP32. That is the weak-and-minimal playback by design; clean audio would need an I2S DAC (MAX98357A), which this shop does not carry.
189. **Waveshare 5 W 8 Ω stereo speakers** ×1 pair — the only real speakers in the catalogue; everything else there is a buzzer.

## Mains switching (220 V)

> Two distinct roles, and nothing here works on its own: a relay waits for 5 V on
> its IN pin, a sensor produces a signal something has to read. The ESP-01S and
> ESP-01 modules that drive them are already owned (#9, #10).

190. **HLK-PM01 220 V → 5 V 3 W** ×3, **HLK-PM12 → 12 V** ×2, **HLK-PM03 → 3.3 V** ×2. Mains **input**: a matchbox-sized supply that replaces a wall wart. The PM03 feeds an ESP32 directly with no converter in between.
191. **ESP-01S relay board V1** ×3 — a socket for an ESP-01S plus a relay. A finished smart socket.
192. **Relay modules 5 V 10 A** — 1-channel ×3, 2-channel opto-isolated ×2, 8-channel ×1. Mechanical, audible, switch anything.
193. **G3MB-202P solid-state relay 2 A / 240 V** ×3 — no contacts, silent, **AC only**.
194. **30 A opto-isolated relay** ×2.
195. **BTA16-600B triac** ×3 with **MOC3063 opto-triac** ×5 — the triac alone has no isolation between an MCU pin and the mains and must never be driven directly. The MOC3063 supplies the isolation **and** a zero-cross detector, which means **silent on/off switching, not dimming**: it only fires near the zero crossing, so a whole half-cycle conducts. Phase-angle dimming needs a random-phase opto (MOC3021/3023), not stocked here.

## Semiconductors, protection, prototyping

196. **IRLZ44N** ×10, **IRL540N** ×5, **IRL2203N** ×5, **FDD8447L** ×5. All **logic-level** (`IRL`, not `IRF`): they open fully at 5 V and work at 3.3 V. An `IRF` part needs 10 V on the gate and will sit in its linear region and burn.
197. **Glass fuses 5×20, 0.2–20 A, 100 pcs** and **ceramic 10 A** ×10 — ceramic is better at high current, since glass can strike an arc inside the envelope.
198. **PolySwitch resettable 1 A** ×5 and **2 A** ×5 — the polymer expands, resistance jumps thousands of times, and it recovers on cooling. On a breadboard this is what prevents burning a board while hunting a short.
199. **Fuse holders 10 A with 18 AWG leads** ×4.
200. **Bakelite perfboard 220×100** ×3, **stripboard 133×48** ×3, **SYB-170 mini breadboard** ×4.
201. **Breadboard power module 5 V/3.3 V** ×2, **1.8/3.3 V plus bipolar 5 V** ×1.

## Connectors, wire, cables

202. **XT60 male+female pair** ×5, **XT30 pair** ×3.
203. **JST-SM 4-pin** ×5, **JST-SM 3-pin** ×5, **JST-SYP-2P with 22 AWG leads** ×5 — bought pre-wired, because no open-barrel crimper (SN-28B) is sold here.
204. **18 AWG hookup wire set, 4 m** and **20 AWG set, 6 m**.
205. **USB cables** — mini-USB 30 cm ×2, micro-USB 30 cm ×2, micro-USB right-angle 1 m ×1, Type-C silicone 5 A 1.5 m ×3.
206. **Cable ties** 2.5×200 and 4.8×300, plus **hook-and-loop straps** 5 m and 2 m.

## Controls (remote)

207. **MTS-103 ON-OFF-ON toggle** ×4, **MTS-102** ×2, **MTS-101 SPST** ×1, **IP54 toggle boots** ×6, **illuminated tactile buttons 6.5×5.4 mm** ×6.

## Instruments

208. **FNIRSI 2C53T** — 2×50 MHz oscilloscope, signal generator and multimeter in one. The meter is **4.5 digits / 19999 counts, True RMS, 10 A**, so it genuinely replaces a standalone multimeter. FPGA + ARM + ADC, 250 MSa/s, ±400 V peak input protection. Caveat: one instrument does one job at a time.
209. **WeAct DLA Mini logic analyzer** — 24 MHz, 8 channels. Decodes I2C, SPI, UART. For the ESP32-to-STM32 link this gets used more than the scope does.
210. **DT-838 multimeter** — a cheap second meter, so one can sit in a circuit while the other probes.
211. **Reinforced 10 A test probes** — thick copper and silicone. At a 4.5 A stall through two 0.2 Ω leads, 1.8 V is lost in the probes alone; on a 7.4 V pack that is a quarter of the supply and a wrong reading.
212. **Crocodile clip lead set** ×10 pcs.
213. **MESTEK IR01B pyrometer, −50 to +550 °C** — non-contact. Finds the hot driver, the hot cell, the hot MOSFET without touching anything live.

## Soldering and hand tools

214. **BAKU BK-8033 hot air gun, 1600 W, 400/600 °C** — heat-shrink and SMD rework.
215. **Sn63Pb37 solder with NC flux, 0.5 mm, 100 g** — fine work; thicker solder is already on hand (#111).
216. **FVS-7 liquid no-clean flux, 100 ml** — wires and connectors.
217. **Short heat-shrink assortment, 328 pcs** — chosen over the long set for its size range.
218. **Automatic wire stripper INTERTOOL HT-7024, 200 mm** — with a terminal crimping jaw.
219. **INTERTOOL HT-7056 crimping pliers (0.5–6.0 mm)** — ring, spade and butt terminals. The household-useful crimper: car wiring, appliances, speakers. **It does not crimp JST or Dupont**; that needs an open-barrel SN-28B, which is not sold here.
220. **HSS drill set 2.0–8.0 mm, 13 pcs** — printed holes come out undersize (Ø3.2 prints as 3.0–3.1); twisting a bit by hand opens them without tearing layers.
221. **Needle file set, 10 pcs, 140 mm** and **scalpel set, 13 pcs**.
222. **Plastic organizer 195×130×35, 12 compartments** ×5.

## Fasteners and magnets

223. **M3 socket-head screws with nuts, 280 pcs**, **M3 countersunk DIN7991 with nuts, 200 pcs**, **M2.5 nickel-plated hardware, 660 pcs**, **M2 brass standoffs with screws, 260 pcs**, **M3 nylon hex standoffs, 180 pcs**.

> **Captive nuts in hex pockets instead of heat-set inserts** (inserts are not sold
> here). For a structural joint this is arguably stronger: the nut bears against the
> whole face of the pocket rather than hanging in melted plastic.
>
> **Nothing larger than M3 exists in this shop.** M5/M6 axle bolts, if printed
> shafts prove inadequate, come from a hardware store.

224. **Neodymium magnets, 120 pcs total** — 3×0.7 ×15, 5×1.6 ×20, 8×1.5 ×20, 10×2.5 ×20, 10×4.5 ×15, 12×1.6 ×15, 11.5×2.4 countersunk ring ×10, 19.3×2.6 ×5.

> Magnets go in by **pause-and-insert** at the closing layer: pocket 0.2–0.3 mm
> oversize in X and Y, 0.1–0.2 in Z, polarity marked before insertion. Neodymium
> demagnetises above about 80 °C, so **never press one in with a soldering iron.**
> Small ones jump to steel nozzles and magnetic beds. Since the part is printed, the
> magnet size is an input rather than a constraint: design the pocket to the magnet.
>
> **Cyanoacrylate is not in this order** — not stocked. Buy it anywhere.

## Filament

225. **Nylon, black, 300 m / 0.825 kg / 1.75 mm** — 240–270 °C nozzle, 70–90 °C bed, **hygroscopic** (absorbs moisture within hours and then spits, so it must be dried). Tough and flexible rather than rigid, excellent abrasion resistance, service temperature around 150 °C. For gears, bushings, hinges and printed shafts. **It is not simply a better PLA.**

> PETG is not stocked here (the PET category is empty). TPU is already on hand
> (1.5 spools) and is what the wheel treads are made from: μ ≈ 0.6 against about
> 0.3 for bare rigid plastic, which more than doubles the traction ceiling.

## Not available at arduino.ua

| Item | Note |
|---|---|
| Screws larger than M3 | nothing above M3 in the whole catalogue |
| Ø5 / Ø6 round shaft | only 8/10/16 mm linear precision rod |
| Cyanoacrylate glue | needed for 120 magnets |
| Steel M3/M4 washers | only insulating electrical-board ones |
| SN-28B open-barrel crimper | needed for custom JST/Dupont leads |
| Hook grabber probes | out of stock — wanted for the logic analyzer on SMD legs |
| I2S DAC (MAX98357A) | for clean audio playback |
| Random-phase opto-triac (MOC3021/3023) | for true phase dimming |
| Vernier caliper | all four listings out of stock |
| PETG filament | category empty |
| 2D lidar | none in catalogue; DIY path is VL53L7CX plus a slip ring |
| Gimbal sticks for a remote | none |
| BTS7960, AS5600 | none |
| Threaded heat-set inserts | none |
| Balance charger alternatives | only found late; iMAX B6 Mini chosen |
