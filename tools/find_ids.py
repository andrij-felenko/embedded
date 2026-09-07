#!/usr/bin/env python3
"""Шукає productID на arduino.ua для деталей, яких немає в shop_ids.txt.

Це ті, що були в наявності до замовлення №651018 — карта хешів робилася
зі сторінки замовлення, тож своїх деталей у ній немає.

Справжня форма пошуку на сайті: GET /?search=<текст>, UTF-8, назви
українською. Для кожного хеша пробує запити по черзі, доки щось не
знайде, і записує до 5 перших результатів — обирати треба очима,
бо пошук дає «схоже», а не «те саме».

Результат — catalog/found_ids.tsv: хеш, запит, далі «id|слаг» до 5 штук.
Темп: одна дія на 4 секунди.
"""
import io
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "catalog", "found_ids.tsv")
PAUSE = 4
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
LINK = re.compile(r'href="(?:https://arduino\.ua)?/(prod(\d+)[^"]*)"')

# хеш -> запити в порядку спадання точності
WANT = [
    ("ar747p", ["безколекторний двигун", "безколекторний", "brushless"]),
    ("nfka2d", ["JF-0530B", "соленоїд", "електромагніт"]),
    ("2g5zcs", ["вентилятор 5В", "вентилятор"]),
    # коди KY-xxx дають лише набір 37-в-1 — шукаємо за призначенням
    ("wp6xq3", ["датчик перешкод", "інфрачервоний датчик перешкод", "FC-51"]),
    ("mde6mj", ["фоторезистор", "модуль фоторезистора"]),
    ("666cx7", ["вологості ґрунту", "вологість ґрунту", "датчик вологості"]),
    ("g4z2gk", ["датчик дощу", "дощу"]),
    ("rkpnz2", ["датчик звуку", "мікрофон модуль", "мікрофон"]),
    ("qjc6he", ["датчик удару", "датчик вібрації", "датчик нахилу"]),
    ("a3k774", ["геркон", "герконовий"]),
    ("wzvhz6", ["BE-182", "BE-180", "GPS модуль", "GPS"]),
    ("yxs4q5", ["ESP32-CAM", "ESP32 CAM"]),
    ("4852tg", ["датчик полум'я", "полум'я", "датчик вогню"]),
    ("fb7rbz", ["світлодіод 5мм", "набір світлодіодів", "світлодіоди"]),
    ("q7ed7c", ["KY-012", "зумер активний", "активний зумер", "зумер"]),
    ("3w42yq", ["KY-006", "зумер пасивний", "пасивний зумер"]),
    ("p8ze7n", ["5641AS", "семисегментний індикатор", "індикатор 4 розряди"]),
    ("66j48p", ["тактова кнопка", "кнопка тактова", "кнопки з ковпачками"]),
    ("97hvjp", ["KY-040", "енкодер модуль", "енкодер"]),
    ("gb63b8", ["джойстик", "модуль джойстика"]),
    ("ran246", ["мембранна клавіатура", "клавіатура 4х4", "клавіатура матрична", "keypad"]),
    ("r8tg7n", ["RC522", "RFID-RC522", "зчитувач RFID"]),
    ("g7g6td", ["брелок RFID", "брелок Mifare", "RFID брелок"]),
    ("j6qe9t", ["ІЧ приймач", "інфрачервоний приймач", "приймач ІЧ"]),
    ("vcmmhg", ["HC-05", "HC-06", "Bluetooth модуль", "bluetooth"]),
]

# другий раунд: деталі, які з'явились у конструкторі після розширення answers.md
WANT += [
    ("9jhkjg", ["HC-SR501", "датчик руху PIR", "датчик руху"]),
    ("kpq9sh", ["HC-SR04", "ультразвуковий датчик відстані"]),
    ("hxz8v5", ["фотопереривник", "оптопара", "оптичний датчик щілинний", "KY-010"]),
    ("gcmb7j", ["лазерний випромінювач", "лазер 650", "лазерний діод модуль", "KY-008"]),
    ("fx6sq7", ["датчик рівня рідини", "рівня рідини", "water level"]),
    ("td3vsc", ["датчик вібрації", "SW-18020P", "вібрації"]),
    ("mz2zj8", ["модуль геркона", "геркон модуль", "геркон"]),
    ("e3cfhg", ["модуль датчика Холла", "датчик Холла", "A3144"]),
    ("3fyyks", ["SW-520D", "кульковий датчик нахилу", "датчик нахилу"]),
    ("39tfwq", ["датчик нахилу модуль", "датчик нахилу"]),
    ("j8wsvc", ["ADXL335", "GY-61", "акселерометр"]),
    ("erd24e", ["Magic Light Cup", "KY-027"]),
    ("nm953c", ["LSM6DS33", "MinIMU-9", "Pololu IMU"]),
    ("ckys6f", ["KY-037", "датчик звуку мікрофон", "датчик звуку"]),
    ("s7nvfb", ["датчик звуку LM393", "датчик звуку"]),
    ("254sj6", ["AS3935", "датчик блискавки", "датчик грози"]),
    ("dv9d7g", ["BMP280", "BME280", "барометр"]),
    ("bsfpm6", ["ESP32-S3 SuperMini", "ESP32-S3 Super Mini", "ESP32-S3"]),
    ("bvh8h7", ["TOF250", "лазерний далекомір", "TOF"]),
    ("x7fern", ["термістор модуль", "термістор", "KY-013"]),
    ("vqezaw", ["KY-028", "датчик температури цифровий"]),
    ("khwjp6", ["DHT11"]),
    ("afe23h", ["GY-21", "HTU21D", "Si7021"]),
    ("r5tqaz", ["INMP441", "I2S мікрофон", "мікрофон MEMS"]),
    ("syqp28", ["GY-271", "HMC5883L", "компас"]),
    ("3wd6g2", ["DS3231", "модуль годинника", "RTC"]),
    ("t2qq5c", ["MAX30102", "датчик пульсу"]),
    ("4q2xtw", ["KY-039", "датчик пульсу пальця", "датчик пульсу"]),
    ("vmxhma", ["N20", "мотор N20", "мотор-редуктор N20"]),
    ("3rjywg", ["SG90"]),
    ("hvzh7s", ["HD-1370A", "Power HD", "сервопривід"]),
    ("v7zhta", ["SRD-05VDC", "модуль реле 5В 1 канал", "реле 5В"]),
    ("jkjd3m", ["інфрачервоний світлодіод", "ІЧ світлодіод", "IR LED"]),
    ("w6n6dd", ["KY-034", "семиколірний світлодіод", "світлодіод миготливий"]),
    ("mmfffr", ["KY-016", "RGB світлодіод модуль", "RGB світлодіод"]),
    ("3m6p5k", ["KY-009", "RGB SMD світлодіод"]),
    ("pxh74d", ["матриця 8x8", "світлодіодна матриця", "1588BS"]),
    ("bayjpy", ["зумер 5В", "п'єзодинамік", "buzzer 5V", "активний зумер"]),
    ("9k45hy", ["OLED 0.96", "SSD1306", "OLED 128x64"]),
    ("7wf5cm", ["LCD 1602", "1602", "дисплей 1602"]),
    ("46kths", ["PCF8574", "I2C адаптер 1602", "перехідник I2C LCD"]),
    ("3kfhgx", ["5161AS", "семисегментний індикатор 1 розряд", "індикатор семисегментний"]),
    ("xjyxpm", ["ESP32-S3-Pico", "ESP32 S3 Pico", "Waveshare ESP32-S3"]),
    ("j8343y", ["KY-004", "кнопка модуль", "тактова кнопка модуль"]),
    ("wbjxcv", ["потенціометр 10 кОм", "змінний резистор 10к", "потенціометр 10k"]),
    ("scyddw", ["клавіатура 4х4 кнопки", "матрична клавіатура тактова", "клавіатура 16 кнопок"]),
    ("ss7wn8", ["VS1838B", "VS1838", "ІЧ приймач"]),
    ("gwcvzd", ["телеметрія 433", "3DR radio", "radio telemetry"]),
    ("e29kxj", ["radio telemetry", "телеметрія"]),
    ("838vre", ["ESP32-C6-Zero", "ESP32-C6", "ESP32 C6"]),
    ("3ncgwv", ["14500", "акумулятор 14500"]),
    ("m8b5j5", ["Li-Po 11.1", "LiPo 2200", "акумулятор Li-Po", "Li-Po"]),
]

# набори (37-в-1, стартові) — фото набору для окремого модуля не годиться
KIT = re.compile(r"nabor|nabir|starter|-kit|kit-", re.I)


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        body = r.read().decode("utf-8", "replace")
    return body.replace("\\/", "/")


def search(q):
    url = "https://arduino.ua/?search=" + urllib.parse.quote(q)
    page = get(url)
    time.sleep(PAUSE)
    seen, out = set(), []
    for slug, pid in LINK.findall(page):
        if pid not in seen:
            seen.add(pid)
            out.append((pid, slug))
    return out


def main():
    done = set()
    if os.path.exists(OUT):
        for line in io.open(OUT, encoding="utf-8"):
            if line.strip():
                done.add(line.split("\t")[0])

    # що сайт показує на порожній видачі — це не результати
    noise = {pid for pid, _ in search("qwertyzzz")}
    print("фонових посилань:", len(noise), flush=True)

    fh = io.open(OUT, "a", encoding="utf-8")
    for h, queries in WANT:
        if h in done:
            print("skip", h, flush=True)
            continue
        hit = None
        for q in queries:
            try:
                found = [(p, s) for p, s in search(q)
                         if p not in noise and not KIT.search(s)]
            except Exception as e:
                print("fail", h, q, e, flush=True)
                time.sleep(PAUSE)
                continue
            if found:
                hit = (q, found[:5])
                break
        if hit:
            q, found = hit
            fh.write("%s\t%s\t%s\n" % (h, q, "\t".join("%s|%s" % f for f in found)))
            fh.flush()
            print("ok", h, q, "->", found[0][1][:60], "(+%d)" % (len(found) - 1),
                  flush=True)
        else:
            print("MISS", h, flush=True)
    fh.close()


if __name__ == "__main__":
    sys.exit(main())
