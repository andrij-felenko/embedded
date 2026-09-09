#!/usr/bin/env python3
"""Збирає сайт з теки catalog/.

catalog/<section>.md   — інвентар: "Назва [hash]    кількість"
catalog/desc/<sec>.md  — [hash] Людська назва / опис / Ідеї: / Теми:
catalog/ideas.md       — ## Назва / речення / хеші через ·

Головна сторінка — ідеї. Каталог — за кнопкою вгорі справа.
Результат: <out>/index.html, без залежностей.
"""
import argparse
import json
import shutil
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = os.path.join(ROOT, "catalog")
DESC = os.path.join(CAT, "desc")
IDEAS = os.path.join(CAT, "ideas.md")
PICDIR = os.path.join(CAT, "pics")
ANSWERS = os.path.join(CAT, "answers.md")
KINDSF = os.path.join(CAT, "kinds.md")
SKIP = {"index.md", "ideas.md", "answers.md"}

ITEM_RE = re.compile(r"^(.+?) \[([0-9a-z]{6})\]\s+(\S.*?)\s*$", re.M)

THEMES = [
    ("погода",     "Погода й середовище", "Температура, волога, дощ, газ, дим, світло"),
    ("відстань",   "Відстань і перешкоди","Як далеко до предмета і чи є щось на шляху"),
    ("положення",  "Рух і положення",     "Нахил, поворот, напрямок, магніт, вібрація"),
    ("дотик",      "Дотик і звук",        "Мікрофони, датчики шуму, стуку й дотику"),
    ("рухоме",     "Рухомі частини",      "Мотори, серви, помпи, механіка"),
    ("інтерфейс",  "Інтерфейс",           "Екрани, лампочки, звук, кнопки, крутилки"),
    ("плати",      "Плати",               "Мікроконтролери, комп'ютери, програматори"),
    ("звязок",     "Зв'язок",             "Радіо, Wi-Fi, Bluetooth, супутники, мітки"),
    ("енергія",    "Енергія",             "Батареї, заряд, перетворювачі, сонце"),
    ("комутація",  "Комутація й захист",  "Реле, ключі, запобіжники"),
    ("корпус",     "Корпус",              "Кріплення, провід, роз'єми, пластик"),
    ("інструмент", "Інструмент",          "Паяльник, мультиметр, осцилограф"),
]
BASIS = []

PICS = {
 "home": "M4 11l8-6 8 6v8a1 1 0 01-1 1h-4v-6H9v6H5a1 1 0 01-1-1z",
 "wheel": "M12 3a9 9 0 100 18 9 9 0 000-18zm0 4.5v9m-4.5-4.5h9",
 "boat": "M4 15h16l-2.5 5H6.5zM12 3v9M12 5l6 6H6z",
 "drone": "M6 6l4 4m8-4l-4 4M6 18l4-4m8 4l-4-4M4 6a2 2 0 104 0 2 2 0 00-4 0m12 0a2 2 0 104 0 2 2 0 00-4 0M4 18a2 2 0 104 0 2 2 0 00-4 0m12 0a2 2 0 104 0 2 2 0 00-4 0M10 10h4v4h-4z",
 "watch": "M9 3h6l.5 4M9 21h6l.5-4M12 8a5 5 0 100 10 5 5 0 000-10z",
 "tree": "M12 3l5 7h-3l4 6H6l4-6H7zM12 16v5",
 "race": "M6 3v18M6 4h11l-2 4 2 4H6z",
 "box": "M4 8l8-4 8 4v9l-8 4-8-4zM4 8l8 4 8-4M12 12v9",
 "line": "M3 17c4 0 4-10 8-10s4 10 8 10",
 "drop": "M12 3s6 6.5 6 10.5A6 6 0 016 13.5C6 9.5 12 3 12 3z",
 "turn": "M12 20a8 8 0 118-8M12 20V12l6-3",
 "step": "M4 20v-4h4v-4h4V8h4V4h4",
 "push": "M4 12h11m0-4l4 4-4 4M18 5v14",
 "pump": "M7 20V9l5-5 5 5v11zM12 9v6m-2-3h4",
 "fan": "M12 12a4 4 0 01-4-8 4 4 0 018 0 4 4 0 01-4 8zm0 0a4 4 0 018 4 4 4 0 01-8 4 4 4 0 010-8z",
 "walk": "M13 4a1.5 1.5 0 110 3 1.5 1.5 0 010-3zM10 21l2-6-2-3 1-4 3 2 2 3M10 12l-3 2",
 "ruler": "M3 12h18M3 9v6M21 9v6M8 10v4m4-4v4m4-4v4",
 "wall": "M4 20V8h16v12zM4 14h16M9 8v6m6-6v6M7 14v6m10-6v6",
 "sun": "M12 3v2m0 14v2M5 12H3m18 0h-2M6 6l1.5 1.5M16.5 16.5L18 18M18 6l-1.5 1.5M7.5 16.5L6 18M12 8a4 4 0 100 8 4 4 0 000-8z",
 "thermo": "M14 14.8V5a2 2 0 10-4 0v9.8a4 4 0 104 0zM12 8v7",
 "humid": "M12 3s5 5.5 5 9a5 5 0 01-10 0c0-3.5 5-9 5-9zM9 20h6",
 "plant": "M12 21V11m0 0C12 7 9 5 6 5c0 4 3 6 6 6zm0 0c0-4 3-6 6-6 0 4-3 6-6 6zM7 21h10",
 "rain": "M7 15a4 4 0 010-8 5.5 5.5 0 0110.5-1.2A3.9 3.9 0 0117 15zM8 18l-.6 2M12 18l-.6 2M16 18l-.6 2",
 "ear": "M6 10v4m4-7v10m4-13v16m4-12v8",
 "knock": "M9 12V6a1.5 1.5 0 013 0v5m0-2a1.5 1.5 0 013 0v2m0-1a1.5 1.5 0 013 0v4a6 6 0 01-6 6h-1a6 6 0 01-6-6v-2a1.5 1.5 0 013 0",
 "touch": "M12 4a4 4 0 00-4 4m4-7a7 7 0 00-7 7m9 0V6a1.5 1.5 0 013 0v7m0-2a1.5 1.5 0 013 0v4a6 6 0 01-6 6h-2l-4-4",
 "door": "M6 20V4h10v16zM6 20h12M13 12h.01",
 "tilt": "M3 17l7-11 11 7zM7 20h14",
 "compass": "M12 3a9 9 0 100 18 9 9 0 000-18zm3.5 5.5L14 14l-5.5 1.5L10 10z",
 "pin": "M12 21s7-6.2 7-11a7 7 0 10-14 0c0 4.8 7 11 7 11zm0-13.2a2.6 2.6 0 110 5.2 2.6 2.6 0 010-5.2z",
 "camera": "M4 8h3l1.5-2h7L17 8h3v11H4zm8 2.5a3.5 3.5 0 100 7 3.5 3.5 0 000-7z",
 "fire": "M12 3c1 3-2 4-2 7a2 2 0 004 0c0-1 1-2 1-2 2 2 2 3.5 2 5a5 5 0 01-10 0c0-4 5-6 5-10z",
 "gas": "M6 16a3 3 0 010-6 4.5 4.5 0 018.5-1A3.2 3.2 0 0117 16zM8 19h9M10 21h5",
 "bulb": "M9 18h6M10 21h4M12 3a6 6 0 00-3.5 10.9c.5.4.8 1 .8 1.6h5.4c0-.6.3-1.2.8-1.6A6 6 0 0012 3z",
 "rgb": "M9 8a4 4 0 100 8 4 4 0 000-8zm6 0a4 4 0 100 8 4 4 0 000-8z",
 "bell": "M6 16V11a6 6 0 1112 0v5l2 3H4zM10 21h4",
 "note": "M9 18V6l10-2v12M9 18a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0zm10-2a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z",
 "speaker": "M4 9h4l5-4v14l-5-4H4zM17 9a4 4 0 010 6",
 "screen": "M4 5h16v11H4zM9 20h6M12 16v4",
 "digits": "M6 5h4v6H6zM6 13h4v6H6zM14 5h4v6h-4zM14 13h4v6h-4z",
 "button": "M12 5a7 7 0 100 14 7 7 0 000-14zm0 4a3 3 0 100 6 3 3 0 000-6z",
 "switch": "M8 8h8a4 4 0 010 8H8a4 4 0 010-8zm8 1.5a2.5 2.5 0 100 5 2.5 2.5 0 000-5z",
 "knob": "M12 4a8 8 0 108 8M12 4v8l5.5-3",
 "stick": "M12 4a2.5 2.5 0 100 5 2.5 2.5 0 000-5zm0 5v7M7 20h10l-2-4H9z",
 "keypad": "M5 5h4v4H5zM10 5h4v4h-4zM15 5h4v4h-4zM5 10h4v4H5zM10 10h4v4h-4zM15 10h4v4h-4zM5 15h4v4H5zM10 15h4v4h-4zM15 15h4v4h-4z",
 "key": "M14 4a5 5 0 100 10 5 5 0 000-10zm-3.5 8.5L4 19v2h3v-2h2v-2h2z",
 "remote": "M9 3h6v18H9zM12 6h.01M10 10h4M10 13h4M10 16h4",
 "phone": "M8 3h8v18H8zM11 18h2",
 "radio": "M12 12a1.5 1.5 0 100-3 1.5 1.5 0 000 3zm0 0v9M8 7a6 6 0 000 7m8-7a6 6 0 010 7M5 4a10 10 0 000 13M19 4a10 10 0 010 13",
 "battery": "M4 8h14v8H4zM18 11h2v2h-2zM7 11h5",
 "plug": "M9 3v5m6-5v5M7 8h10v3a5 5 0 01-10 0zM12 16v5",
 "solar": "M3 16h18l-2-9H5zM8 7l-1 9m5-9v9m4-9l1 9M3 20h18",
    "baro": "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 12l3-5M12 12h.01M8 16h8",
    "bath": "M4 12h16v3a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4zM6 12V6a2 2 0 0 1 4 0M5 19l-1 2M19 19l1 2",
    "clock": "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 7v5l3 2",
    "dim": "M12 6a6 6 0 0 0 0 12V6zM12 6a6 6 0 0 1 0 12M12 2v2M12 20v2M2 12h2M20 12h2",
    "feed": "M3 13h18l-2 6H5zM8 9h.01M12 8h.01M16 9h.01M10 5h.01M14 5h.01",
    "fence": "M5 6v14M12 6v14M19 6v14M3 11h18M3 16h18",
    "flow": "M3 8c2-2 4-2 6 0s4 2 6 0 4-2 6 0M3 13c2-2 4-2 6 0s4 2 6 0 4-2 6 0M3 18c2-2 4-2 6 0s4 2 6 0 4-2 6 0",
    "gate": "M5 4v16M19 4v16M7 12h3M14 12h3M12 12h.01",
    "grid": "M4 4h4v4H4zM10 4h4v4h-4zM16 4h4v4h-4zM4 10h4v4H4zM10 10h4v4h-4zM16 10h4v4h-4zM4 16h4v4H4zM10 16h4v4h-4zM16 16h4v4h-4z",
    "hand": "M8 13V6a1.5 1.5 0 0 1 3 0v5M11 11V4a1.5 1.5 0 0 1 3 0v7M14 11V6a1.5 1.5 0 0 1 3 0v8a6 6 0 0 1-6 6h-1a5 5 0 0 1-4-2l-3-5a1.5 1.5 0 0 1 2.5-1.5L8 13",
    "heart": "M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z",
    "height": "M12 3v18M8 7l4-4 4 4M8 17l4 4 4-4M4 12h4M16 12h4",
    "laser": "M12 10a2 2 0 1 0 0 4 2 2 0 0 0 0-4zM3 12h5M16 12h5M12 3v5M12 16v5",
    "level": "M5 4v16h14V4M8 13c1.3-1 2.7-1 4 0s2.7 1 4 0M8 17c1.3-1 2.7-1 4 0s2.7 1 4 0",
    "lift": "M6 21h12V11H6zM12 3v6M9 6l3-3 3 3",
    "lock": "M6 11h12v9H6zM9 11V7a3 3 0 0 1 6 0v4M12 15v2",
    "magnet": "M6 3h4v9a2 2 0 0 0 4 0V3h4v9a6 6 0 0 1-12 0zM6 7h4M14 7h4",
    "message": "M4 4h16v11H9l-5 5zM8 9h8",
    "mic": "M12 3a3 3 0 0 1 3 3v5a3 3 0 0 1-6 0V6a3 3 0 0 1 3-3zM6 11a6 6 0 0 0 12 0M12 17v4M9 21h6",
    "plugin": "M9 3v5M15 3v5M6 8h12v3a6 6 0 0 1-12 0zM12 17v4",
    "shake": "M8 8h8v8H8zM3 5l2 2M21 5l-2 2M3 19l2-2M21 19l-2-2",
    "smoke": "M9 21c-2-2-2-4 0-6s2-4 0-6M15 21c-2-2-2-4 0-6s2-4 0-6M5 21h14",
    "speed": "M4 16a8 8 0 1 1 16 0M12 16l5-6M12 16h.01M4 16h16",
    "spin": "M20 12a8 8 0 1 1-2.3-5.7M20 4v4h-4",
    "steps": "M7 4c2 0 3 2 3 5s-1 5-3 5-3-2-3-5 1-5 3-5zM17 10c2 0 3 2 3 5s-1 5-3 5-3-2-3-5 1-5 3-5z",
    "storm": "M7 15a4 4 0 0 1 0-8 5 5 0 0 1 10 0h1a3 3 0 0 1 0 6M13 12l-2 4h3l-2 4",
    "usb": "M12 20V4M9 7l3-3 3 3M12 17l-5-3v-3M12 14l5-3V8M12 20h.01",
    "web": "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18",
    "book": "M4 4h7a2 2 0 0 1 2 2v14a1 1 0 0 0-1-1H4zM20 4h-7a2 2 0 0 0-2 2v14a1 1 0 0 1 1-1h8z",
    "route": "M5 21a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM19 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM5 17c0-6 14-4 14-10",
    "balance": "M3 17l18-4M12 6v9M5 21h14M12 6a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3",
    "grip": "M8 21V11a2 2 0 0 1 4 0v10M16 21V11a2 2 0 0 0-4 0M8 11l-3-5M16 11l3-5M5 6h.01M19 6h.01",
    "wave": "M6 12v-1a1.5 1.5 0 0 1 3 0v1M9 11V6a1.5 1.5 0 0 1 3 0v5M12 10V5a1.5 1.5 0 0 1 3 0v6M15 12V8a1.5 1.5 0 0 1 3 0v6a6 6 0 0 1-12 0v-1M3 5l2 1M20 3l-1 2",
    "vibr": "M9 5h6v14H9zM5 8v8M19 8v8M2 10v4M22 10v4",
    "stir": "M5 12h14v6a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3zM12 12l6-9M9 15c1 1 2 1 3 0s2-1 3 0",
    "pour": "M6 3h8l-2 8v10H8V11zM14 6l5 2v4M5 21h14",
    "keyboard": "M3 7h18v10H3zM6 10h.01M9 10h.01M12 10h.01M15 10h.01M18 10h.01M7 14h10",
    "tv": "M3 5h18v12H3zM8 21h8M12 17v4",
    "face": "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM9 10h.01M15 10h.01M8.5 14.5c1 1.5 6 1.5 7 0",
    "wifi": "M2 9c6-5 14-5 20 0M5 13c4-3 10-3 14 0M8.5 16.5c2-1.5 5-1.5 7 0M12 20h.01",
    "moon": "M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z",
    "battery2": "M2 8h8v8H2zM10 11h1v2h-1M13 8h8v8h-8zM21 11h1v2h-1M4 10v4M15 10v4",
    "belt": "M6 8a3 3 0 1 0 0 6M18 8a3 3 0 1 1 0 6M6 8h12M6 14h12M9 4l2 4M15 4l2 4",
    "broom": "M14 3l7 7M12 5l7 7M11 6l-6 6 4 4 6-6M5 12l-2 9 9-2",
    "co": "M4 12a4 4 0 0 1 8 0M12 12a4 4 0 1 0 8 0 4 4 0 0 0-8 0M8 16v2M16 16v2",
    "coin": "M12 4a8 8 0 1 0 0 16 8 8 0 0 0 0-16zM9 12h6M12 9v6",
    "drum": "M5 10c0-2 3-3 7-3s7 1 7 3v7c0 2-3 3-7 3s-7-1-7-3zM5 10c0 2 3 3 7 3s7-1 7-3M9 3l3 4M15 3l-3 4",
    "eye": "M2 12c3-5 7-7 10-7s7 2 10 7c-3 5-7 7-10 7s-7-2-10-7zM12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6z",
    "flower": "M12 12a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM12 12a3 3 0 1 0 0 6M12 12a3 3 0 1 0-6 0M12 12a3 3 0 1 0 6 0M12 18v3",
    "ghost": "M6 21V10a6 6 0 0 1 12 0v11l-2-2-2 2-2-2-2 2-2-2zM10 11h.01M14 11h.01",
    "hold": "M4 12a8 8 0 1 0 8-8M4 12l3-3M4 12l3 3M12 8v4l3 2",
    "legs": "M6 6h12M8 6v5l-3 9M16 6v5l3 9M12 6v5l-2 9M12 11l2 9",
    "mouth": "M4 12c2-4 5-5 8-5s6 1 8 5c-2 4-5 5-8 5s-6-1-8-5zM4 12h16",
    "nopower": "M13 2L4 14h7l-1 8 9-12h-7l1-8zM3 3l18 18",
    "page": "M6 3h9l4 4v14H6zM15 3v4h4M9 12h6M9 16h6",
    "pen": "M4 20l4-1L19 8l-3-3L5 16zM13 7l3 3",
    "pop": "M5 21h14V11H5zM5 11l7-8 7 8M12 3v8",
    "press": "M6 3h12M9 3v5M15 3v5M6 8h12v3H6zM9 11v3h6v-3M12 14v7M5 21h14",
    "puppet": "M5 3h14M12 3v4M12 7a2 2 0 1 0 0 4 2 2 0 0 0 0-4zM12 11v5M8 13l4 3 4-3M9 21l3-5 3 5",
    "rack": "M3 9h13M3 15h13M6 9v6M10 9v6M14 9v6M18 7v10M21 7v10",
    "rail": "M3 18h18M6 18V9M18 18V9M9 9h6v4H9zM6 13h12",
    "release": "M12 3v9M8 8l4 4 4-4M5 16h14M5 20h14",
    "screen2": "M3 5h18v12H3zM8 21h8M12 17v4M8 10h.01M12 10h.01M16 10h.01",
    "shutter": "M4 4h16v16H4zM4 12h16M12 4v16M4 4l16 16M20 4L4 20",
    "sort": "M4 4h16M12 4v6M12 10l-5 6M12 10l5 6M4 20h6M14 20h6",
    "swing": "M4 4h16M7 4v9M17 4v9M7 13h10M12 13v3M9 20h6",
    "throw": "M4 20l6-6M9 9l3-4 3 4-3 4zM15 9l5-4M17 5h3v3",
    "track": "M4 12a4 4 0 0 1 4-4h8a4 4 0 0 1 0 8H8a4 4 0 0 1-4-4zM8 12h.01M12 12h.01M16 12h.01",
    "turntable": "M12 6a8 3 0 1 0 0 6 8 3 0 0 0 0-6zM4 9v6a8 3 0 0 0 16 0V9M12 9h.01",
    "usbout": "M12 20V4M9 7l3-3 3 3M6 12h12M6 12l-2 2M6 12l-2-2M18 12l2 2M18 12l2-2",
    "valve": "M4 12h16M12 12V8M8 8h8M12 12v5a3 3 0 0 0 3 3",
    "winch": "M4 5h9a3 3 0 0 1 0 6H4zM4 5v6M9 11v9M6 20h6",
    "wind": "M3 8h10a3 3 0 1 0-3-3M3 12h15a3 3 0 1 1-3 3M3 16h8a2 2 0 1 1-2 2",
    "wipe": "M4 20L16 8M13 5l6 6M4 20a4 4 0 0 1 2-5",
    "chair": "M6 10V4h12v6M4 10h16v4H4zM6 14v7M18 14v7",
    "dip": "M4 12h16v8H4zM12 3v9M9 6l3-3 3 3M7 16c2-1 3-1 5 0s3 1 5 0",
    "flip": "M4 6h16v8H4zM4 10h16M12 6v8M8 18l4 3 4-3",
    "frost": "M12 3v18M3 12h18M6 6l12 12M18 6L6 18M12 3l-2 2M12 3l2 2",
    "jack": "M4 21h16M6 21v-3l6-4 6 4v3M12 14V4M9 7l3-3 3 3",
    "nod": "M12 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8zM12 12v4M8 20l4-4 4 4M5 9l2 2M19 9l-2 2",
    "palette": "M12 3a9 9 0 0 0 0 18c2 0 2-2 1-3s0-2 2-2h2a4 4 0 0 0 4-4 9 9 0 0 0-9-9zM8 9h.01M12 6h.01M16 9h.01M7 13h.01",
    "screw": "M12 3v18M8 6c3 1 5 3 8 4M8 11c3 1 5 3 8 4M8 16c3 1 5 3 8 4",
    "stamp": "M9 3h6v6H9zM6 9h12l2 6H4zM5 19h14v2H5z",
}

ICONS = {
 "погода": "M7 17a4 4 0 010-8 5.5 5.5 0 0110.5-1.2A3.9 3.9 0 0117 17H7zM8 20l.6-1.4M12 20.5l.6-1.4M16 20l.6-1.4",
 "відстань": "M3 12h18M3 9v6M21 9v6M9 10.5l-1.5 1.5L9 13.5M15 10.5l1.5 1.5-1.5 1.5",
 "положення": "M12 21s7-6.2 7-11a7 7 0 10-14 0c0 4.8 7 11 7 11zm0-13.2a2.6 2.6 0 110 5.2 2.6 2.6 0 010-5.2z",
 "дотик": "M6 10v4m4-8v12m4-9v6m4-4v2M3 12h.5m17 0h.5",
 "рухоме": "M12 3a9 9 0 100 18 9 9 0 000-18zm0 5.5v7m-3.5-3.5h7",
 "інтерфейс": "M4 5h16v10H4zM9 19h6M12 15v4M8.5 9.5h1m5 0h1",
 "плати": "M9 3v2M15 3v2M9 19v2M15 19v2M3 9h2M3 15h2M19 9h2M19 15h2M6.5 6.5h11v11h-11z",
 "звязок": "M12 12a1.5 1.5 0 100-3 1.5 1.5 0 000 3zm0 0v9M8 7a6 6 0 000 7m8-7a6 6 0 010 7M5 4a10 10 0 000 13M19 4a10 10 0 010 13",
 "енергія": "M13 2.5L5.5 13H11l-1.5 8.5L18 11h-5.5l1.5-8.5z",
 "комутація": "M4 12h5l2-3 2 6 2-3h5",
 "корпус": "M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3zm0 0v18m8-13.5L12 12 4 7.5",
 "інструмент": "M12 20a8 8 0 118-8M12 20V12l5.5-3.5M8 20H5m14 0h-3",
}


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def parse_inventory():
    inv = {}
    for f in sorted(os.listdir(CAT)):
        if not f.endswith(".md") or f in SKIP:
            continue
        for n, h, q in ITEM_RE.findall(read(os.path.join(CAT, f))):
            inv[h] = {"tech": n.strip(), "qty": q.strip()}
    return inv


def parse_desc():
    out, cur = {}, None
    for f in sorted(os.listdir(DESC)):
        if not f.endswith(".md"):
            continue
        for line in read(os.path.join(DESC, f)).split("\n"):
            m = re.match(r"^\[([0-9a-z]{6})\]\s*(.*)$", line.strip())
            if m:
                cur = m.group(1)
                out[cur] = {"name": m.group(2).strip(), "what": "",
                            "ideas": [], "themes": [], "lvl": "видима", "q": ""}
                continue
            s = line.strip()
            if not s or cur is None or s.startswith("#"):
                continue
            if s.startswith("Ідеї:"):
                out[cur]["ideas"] = [p.strip() for p in s[5:].split("·") if p.strip()]
            elif s.startswith("Теми:"):
                out[cur]["themes"] = [p.strip() for p in s[5:].split("·") if p.strip()]
            elif s.startswith("Рівень:"):
                out[cur]["lvl"] = s[7:].strip()
            elif s.startswith("Питання:"):
                out[cur]["q"] = s[8:].strip()
            else:
                out[cur]["what"] = (out[cur]["what"] + " " + s).strip()
    return out


def parse_ideas():
    out, cur = [], None
    for line in read(IDEAS).split("\n"):
        s = line.strip()
        if s.startswith("## "):
            cur = {"name": s[3:].strip(), "what": "", "parts": []}
            out.append(cur)
        elif cur is None or not s or s.startswith("#"):
            continue
        elif re.fullmatch(r"[0-9a-z]{6}(\s*·\s*[0-9a-z]{6})*", s):
            cur["parts"] = [p.strip() for p in s.split("·")]
        else:
            cur["what"] = (cur["what"] + " " + s).strip()
    return out


BLOCK_RE = r"^\[([\w'-]+)\]\s+(.+)$"


def parse_blocks(path, fields):
    """Ð¡Ð¿ÑÐ»ÑÐ½Ð¸Ð¹ Ð¿Ð°ÑÑÐµÑ: [ÐºÐ»ÑÑ] ÐÐ°Ð·Ð²Ð° / Ð¿Ð¾Ð»Ñ / ÑÑÐ´Ð¾Ðº Ð¾Ð¿Ð¸ÑÑ."""
    out, cur, fence = [], None, False
    for line in read(path).split(chr(10)):
        t = line.strip()
        if t.startswith("```"):
            fence = not fence
            continue
        if fence or t.startswith("#"):
            continue
        m = re.match(BLOCK_RE, t)
        if m:
            cur = {"key": m.group(1), "name": m.group(2).strip(), "what": ""}
            cur.update({k: ([] if v else "") for k, v in fields.items()})
            out.append(cur)
            continue
        if cur is None or not t:
            continue
        hit = False
        for pre, multi in fields.items():
            if t.startswith(pre + ":"):
                v = t[len(pre) + 1:].strip()
                cur[pre] = [x.strip() for x in v.split("·") if x.strip()] if multi else v
                hit = True
                break
        if not hit and not cur["what"]:
            cur["what"] = t
    return out


def parse_kinds():
    return parse_blocks(KINDSF, {"батько": False, "значок": False,
                                 "одразу": True})


def pic_data():
    """Мініатюри як data-URI, щоб сторінка була самодостатня (працює і з файлу,
    і зі знімка, і з GitHub Pages). Через Pillow — стискаємо до 120 px JPEG."""
    import base64
    import io as _io
    out = {}
    if not os.path.isdir(PICDIR):
        return out
    try:
        from PIL import Image
    except ImportError:
        Image = None
    for f in sorted(os.listdir(PICDIR)):
        if not f.endswith((".jpg", ".png", ".webp")):
            continue
        p = os.path.join(PICDIR, f)
        if os.path.getsize(p) < 900:
            continue
        data, mime = open(p, "rb").read(), None
        if Image is not None:
            try:
                im = Image.open(p)
                if im.mode in ("RGBA", "LA", "P"):
                    bg = Image.new("RGB", im.size, (255, 255, 255))
                    bg.paste(im.convert("RGBA"), mask=im.convert("RGBA").split()[3])
                    im = bg
                else:
                    im = im.convert("RGB")
                im.thumbnail((96, 96))
                buf = _io.BytesIO()
                im.save(buf, "JPEG", quality=68, optimize=True)
                data, mime = buf.getvalue(), "image/jpeg"
            except Exception:
                pass
        if mime is None:
            mime = {"jpg": "image/jpeg", "png": "image/png", "webp": "image/webp"}[f.rsplit(".", 1)[1]]
        out[f] = "data:%s;base64,%s" % (mime, base64.b64encode(data).decode("ascii"))
    return out


def parse_recipes():
    """Готові сутності: з чого зліплюються (варіанти складника через |)."""
    path = os.path.join(os.path.dirname(KINDSF), "recipes.md")
    if not os.path.exists(path):
        return []
    out = parse_blocks(path, {"з": True})
    secs = recipe_sections(path)
    for x in out:
        x["need"] = [[a.strip() for a in alt.split("|") if a.strip()]
                     for alt in x.pop("з")]
        x["sec"], x["sub"] = secs.get(x["key"], ("Інше", "Інше"))
    return out


def recipe_sections(path):
    """ключ рецепту -> (категорія, підгрупа): «## Категорія» і «### Підгрупа» з recipes.md."""
    out, cat, sub = {}, "Інше", None
    for line in open(path, encoding="utf-8"):
        t = line.strip()
        if t.startswith("### "):
            sub = t[4:].strip()
            continue
        if t.startswith("## "):
            cat, sub = t[3:].strip(), None
            continue
        m = re.match(r"^\[([^\]]+)\]\s+\S", t)
        if m:
            out[m.group(1)] = (cat, sub or cat)
    return out


def parse_answers():
    out = parse_blocks(ANSWERS, {"типи": True, "деталі": True, "значок": False,
                                 "група": False, "напрям": False, "ідеї": True})
    for x in out:
        x["q"] = x.pop("key")
        x["kinds"] = x.pop("типи")
        x["parts"] = x.pop("деталі")
        x["ideas"] = x.pop("ідеї")
        x["icon"] = x.pop("значок")
        x["g"] = x.pop("група")
        x["dir"] = x.pop("напрям")
    return out


def num(q):
    m = re.match(r"^(\d+(?:[.,]\d+)?)", q)
    return float(m.group(1).replace(",", ".")) if m else None


def fmt(n):
    return str(int(n)) if n == int(n) else ("%g" % n)


def collect_cards(inv, desc, have_pic=()):
    groups = {}
    for h, it in inv.items():
        d = desc.get(h, {})
        key = d.get("name") or it["tech"]
        g = groups.setdefault(key, {"name": key, "themes": set(), "parts": []})
        g["themes"].update(d.get("themes", []))
        g["parts"].append({"id": h, "tech": it["tech"], "qty": it["qty"],
                           "what": d.get("what", ""), "ideas": d.get("ideas", []),
                           "lvl": d.get("lvl", "видима"), "q": d.get("q", "")})
    cards, by_hash = [], {}
    for g in groups.values():
        parts = sorted(g["parts"], key=lambda p: -len(p["what"]))
        head = parts[0]
        nums = [num(p["qty"]) for p in parts]
        total = fmt(sum(n for n in nums if n)) if all(n is not None for n in nums) \
                else parts[0]["qty"]
        card = {
            "name": g["name"], "what": head["what"], "ideas": head["ideas"],
            "qty": total,
            "lvl": head.get("lvl", "видима"), "q": head.get("q", ""),
            "themes": [t for t, _, _ in THEMES if t in g["themes"]],
            "basis": [t for t in BASIS if t in g["themes"]],
            "variants": [{"tech": p["tech"], "qty": p["qty"],
                          "note": (p["ideas"][0] if p is not head and p["ideas"]
                                   and len(p["ideas"]) == 1 else "")}
                         for p in parts],
        }
        card["pic"] = next((have_pic[p["id"]] for p in parts
                            if p["id"] in have_pic), "")
        cards.append(card)
        for p in g["parts"]:
            by_hash[p["id"]] = card["name"]
    cards.sort(key=lambda c: (-len(c["ideas"]), c["name"]))
    return cards, by_hash


CSS = r"""
/* світла тема: пісок і небо — від блакитного дня до закатного */
:root{
 --paper:#f5f2e9;--panel:#fcfbf7;--ink:#243040;--soft:#6b7886;--line:#d6e0e9;
 --accent:#3c7cb4;--tint:#e3edf6;
 --sens:#3f7fb5;--meas:#3f8f9c;--act:#d9823f;--talk:#8a6fb5;--pow:#c9962e;
 --up:#d1694f;--down:#4e9a63;
 --lift:0 1px 0 rgba(40,60,90,.04);
 --hi:rgba(255,255,255,.75);--sh:rgba(40,60,90,.07);
 --glow:color-mix(in srgb,var(--accent) 18%,transparent);
}
/* темна тема: темно-сіра, не чорна, щоб написи читались */
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){
 --paper:#30353b;--panel:#3a4047;--ink:#eef1f4;--soft:#b3bcc6;--line:#4b535c;
 --accent:#7fb6e6;--tint:#414b57;
 --sens:#8fbde6;--meas:#7fc4cf;--act:#e8a463;--talk:#bda6e0;--pow:#e2c069;
 --up:#ef9a84;--down:#8fcf9e;--lift:none;
 --hi:rgba(255,255,255,.05);--sh:rgba(0,0,0,.35);
}}
:root[data-theme=dark]{
 --paper:#30353b;--panel:#3a4047;--ink:#eef1f4;--soft:#b3bcc6;--line:#4b535c;
 --accent:#7fb6e6;--tint:#414b57;
 --sens:#8fbde6;--meas:#7fc4cf;--act:#e8a463;--talk:#bda6e0;--pow:#e2c069;
 --up:#ef9a84;--down:#8fcf9e;--lift:none;
 --hi:rgba(255,255,255,.05);--sh:rgba(0,0,0,.35);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;height:100%}
body{margin:0;height:100%;overflow:hidden;background:var(--paper);color:var(--ink);
 font:17px/1.6 ui-sans-serif,-apple-system,"Segoe UI",Roboto,system-ui,sans-serif}
.wrap{height:100%;height:100dvh;max-width:1060px;margin:0 auto;padding:0 6px;
 display:flex;flex-direction:column}
.stage[data-step=kinds] .bottom{display:none}
.stage[data-step=kinds] .top{flex:1;max-height:none}
/* верх у режимі збирання: зліва обране, справа зверху готове, справа знизу — що можна об'єднати */
.stage[data-step=build] .top{flex:0 0 40%;max-height:none;overflow:hidden;
 display:flex;flex-direction:column;padding:4px 6px 4px}
.tp{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:minmax(0,1fr);gap:6px;flex:1;min-height:0}
.tpl{overflow-y:auto;min-height:0;scrollbar-width:thin;scrollbar-color:var(--line) transparent}
.tpr{display:flex;flex-direction:column;gap:6px;min-height:0;
 border-left:1px solid var(--line);padding-left:6px}
.ready{flex:1;min-height:0;overflow-y:auto;scrollbar-width:thin;
 scrollbar-color:var(--line) transparent}
/* «можна об'єднати» — смужка з лічильником; розгортається кліком */
.combo{flex:none;display:flex;flex-direction:column;min-height:0}
.combo.open{flex:0 1 auto;max-height:55%}
.clist{overflow-y:auto;min-height:0;margin-top:6px;scrollbar-width:thin;
 scrollbar-color:var(--line) transparent}
.toList{display:none;flex:none;width:26px;height:26px;border:1px solid var(--line);
 background:transparent;color:var(--soft);border-radius:4px;font-size:1rem;line-height:1;padding:0;
 cursor:pointer;align-items:center;justify-content:center}
.lbl{display:block;font-weight:500;text-transform:uppercase;letter-spacing:.07em;
 font-size:.66rem;color:var(--soft);margin:0 0 6px}
.hint2{margin:0;color:var(--soft);font-size:.82rem;line-height:1.4}
.done{display:flex;align-items:center;gap:8px;border:1px solid var(--accent);border-radius:4px;
 padding:4px 7px;margin:0 0 3px;background:color-mix(in srgb,var(--accent) 9%,transparent)}
.done>span{min-width:0}
.done b{display:block;font-size:.85rem;font-weight:600;line-height:1.25;text-align:left}
.done i{display:block;font-style:normal;font-size:.71rem;color:var(--soft);line-height:1.3}
.done .x{margin-left:auto;flex:none;width:22px;height:22px;border:1px solid var(--line);
 background:transparent;border-radius:4px;cursor:pointer;color:var(--soft);font-size:.9rem;
 line-height:1;display:flex;align-items:center;justify-content:center}
.done .x:hover{border-color:var(--accent);color:var(--accent)}
.cmb{display:block;width:100%;text-align:left;border:1px dashed var(--accent);border-radius:4px;
 padding:4px 7px;margin:0 0 3px;cursor:pointer;background:transparent;color:var(--ink)}
.cmb:hover{background:color-mix(in srgb,var(--accent) 10%,transparent)}
.cmb b{display:block;font-size:.85rem;font-weight:500;line-height:1.25;text-align:left}
.cmb i{display:block;font-style:normal;font-size:.71rem;color:var(--soft);line-height:1.3}
.tpl .mrow{margin:4px 0 0}
.stage{flex:1;min-height:0;display:flex;flex-direction:column;gap:4px;
 padding:0 0 4px}
.top{flex:none;max-height:46%;overflow-y:auto;background:var(--panel);
 border:1px solid var(--line);border-radius:6px;padding:12px 12px;
 scrollbar-width:thin;scrollbar-color:var(--line) transparent}
.top h2{margin:0 0 3px;font:600 1.25rem/1.2 Georgia,serif}
.kinds{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(228px,1fr));
 margin:16px 0 0}
.kind{display:flex;align-items:flex-start;gap:12px;background:var(--paper);
 border:1px solid var(--line);border-radius:6px;padding:15px 17px;cursor:pointer;
 text-align:left;transition:border-color .18s ease,transform .18s ease,
 box-shadow .18s ease}
.kind:hover{border-color:var(--accent);transform:translateY(-2px);
 box-shadow:none}
.kind svg{width:24px;height:24px;flex:none;margin-top:1px;stroke:var(--accent);
 fill:none;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.kind span{min-width:0}
.kind b{display:block;font-size:1rem;line-height:1.3}
.kind i{display:block;margin-top:3px;font-style:normal;font-size:.82rem;
 color:var(--soft);line-height:1.4}
.top .back{margin:0 0 10px}
.top .hint{margin:0;color:var(--soft);font-size:.95rem;max-width:52ch}
.slot{margin:10px 0 0}
.slot ul{list-style:none;display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0}
.slot li{font-size:.85rem;background:var(--tint);color:var(--accent);
 border-radius:7px;padding:3px 9px;cursor:pointer}
.slot li:hover{background:var(--accent);color:var(--panel)}
.slot li::after{content:' ×';opacity:.55}
.guess{margin:16px 0 0;padding-top:13px;border-top:1px solid var(--line)}
.guess b{font-size:.8rem;color:var(--soft);text-transform:uppercase;
 letter-spacing:.07em;font-weight:500}
.guess ul{list-style:none;display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 0;padding:0}
.guess li{font-size:.86rem;border:1px solid var(--accent);color:var(--accent);
 border-radius:7px;padding:3px 10px;cursor:pointer}
.bottom{flex:none}
.bottom{flex:1;min-height:0;overflow-y:auto;padding:2px;
 scrollbar-width:thin;scrollbar-color:var(--line) transparent}
.bottom::-webkit-scrollbar{width:9px}
.bottom::-webkit-scrollbar-track{background:transparent}
.bottom::-webkit-scrollbar-thumb{background:var(--line);border-radius:99px;
 border:3px solid var(--paper);background-clip:padding-box}
.picks{display:grid;gap:8px;grid-template-columns:repeat(auto-fill,minmax(102px,1fr))}
.pick{--c:var(--accent);position:relative;display:flex;flex-direction:column;align-items:center;
 justify-content:flex-start;gap:6px;padding:11px 6px 9px;border:1px solid var(--line);
 border-radius:5px;background:var(--panel);cursor:pointer;min-width:0;
 transition:border-color .18s ease,background .18s ease,transform .18s ease,
 box-shadow .18s ease}
.pick[data-g=sens]{--c:var(--sens)}
.pick[data-g=meas]{--c:var(--meas)}
.pick[data-g=act]{--c:var(--act)}
.pick[data-g=talk]{--c:var(--talk)}
.pick[data-g=pow]{--c:var(--pow)}
.pick:hover{border-color:var(--c);transform:translateY(-2px);
 box-shadow:none}
.pick svg{width:24px;height:24px;stroke:var(--c);fill:none;stroke-width:1.6;
 stroke-linecap:round;stroke-linejoin:round;transition:stroke .18s ease}
.pick .dir{position:absolute;top:5px;right:6px;font-size:.68rem;line-height:1;
 font-style:normal;display:flex;gap:1px}
.pick .dir .up,.pick .dir.up{color:var(--up);font-weight:400}
.pick .dir .down,.pick .dir.down{color:var(--down);font-weight:400}
.pick.dim{opacity:.42}
.bottom{flex:1;min-height:0;display:flex;flex-direction:column;gap:0}
.tabs{flex:none;display:grid;grid-template-columns:repeat(5,1fr);gap:-1px}
.tab{--c:var(--accent);background:var(--panel);border:1px solid var(--line);
 margin-right:-1px;padding:5px 3px;font-size:.86rem;cursor:pointer;color:var(--soft);
 display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;
 line-height:1.2;min-width:0;
 transition:background .14s ease,color .14s ease,border-color .14s ease}
.tab span{white-space:nowrap;max-width:100%;overflow:hidden;text-overflow:ellipsis}
.tab .m{display:none}
.ver{margin:10px 0 0;font-size:.66rem;color:var(--soft);text-align:right}
.home{flex:none;margin-right:2px}
.rhead{display:flex;align-items:center;gap:8px;margin:0 0 4px}
.rhead .lbl{margin:0}
.copy{margin-left:auto;flex:none;width:24px;height:24px;border:1px solid var(--line);
 background:transparent;border-radius:4px;cursor:pointer;color:var(--soft);padding:0;
 display:flex;align-items:center;justify-content:center}
.copy svg{width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:1.8;
 stroke-linecap:round;stroke-linejoin:round}
.copy:hover{border-color:var(--accent);color:var(--accent)}
.copy.ok{border-color:var(--down);color:var(--down)}
.tab:first-child{border-radius:4px 0 0 0}
.tab:last-child{border-radius:0 4px 0 0;margin-right:0}
.tab[data-g=sens]{--c:var(--sens)}.tab[data-g=meas]{--c:var(--meas)}
.tab[data-g=act]{--c:var(--act)}.tab[data-g=talk]{--c:var(--talk)}
.tab[data-g=pow]{--c:var(--pow)}
.tab:hover{color:var(--c)}
.tab[aria-pressed=true]{background:color-mix(in srgb,var(--c) 13%,transparent);
 border-color:var(--c);color:var(--c);position:relative;z-index:1}
.pane{flex:1;min-height:0;display:grid;grid-template-columns:1fr 296px;
 grid-template-rows:1fr auto;
 border:1px solid var(--line);border-top:0;border-radius:0 0 4px 4px;overflow:hidden}
.plist{overflow-y:auto;padding:3px;display:grid;gap:3px;align-content:start;
 grid-template-columns:repeat(auto-fill,minmax(176px,1fr));
 scrollbar-width:thin;scrollbar-color:var(--line) transparent}
.plist::-webkit-scrollbar{width:8px}
.plist::-webkit-scrollbar-thumb{background:var(--line);border-radius:0}
.row{--c:var(--accent);display:flex;align-items:center;gap:6px;padding:5px 7px;
 border:1px solid transparent;border-radius:4px;cursor:pointer;min-width:0;
 text-align:left;justify-content:flex-start;
 background:var(--panel);transition:background .12s ease,border-color .12s ease}
.row.dim{opacity:.45}
.row[data-g=sens]{--c:var(--sens)}.row[data-g=meas]{--c:var(--meas)}
.row[data-g=act]{--c:var(--act)}.row[data-g=talk]{--c:var(--talk)}
.row[data-g=pow]{--c:var(--pow)}
.row:hover{border-color:var(--c)}
.row[aria-current=true]{background:color-mix(in srgb,var(--c) 13%,transparent);
 border-color:var(--c)}
.row svg{width:19px;height:19px;flex:none;stroke:var(--c);fill:none;stroke-width:1.6;
 stroke-linecap:round;stroke-linejoin:round}
.row b{font-size:.83rem;font-weight:500;min-width:0;line-height:1.2;text-align:left}
.row .dir{margin-left:auto}
.dir{display:flex;gap:2px;flex:none}
.dir svg{width:14px;height:14px;fill:none;stroke-width:2.6;stroke-linecap:round;
 stroke-linejoin:round}
.dir .up{stroke:var(--up)}.dir .down{stroke:var(--down)}
.pane .info{grid-column:2;grid-row:1/3}
.pane .legend{grid-column:1;grid-row:2;display:flex;gap:18px;align-items:center;
 justify-content:center;padding:4px 8px;font-size:.78rem;color:var(--soft);
 border-top:1px solid var(--line)}
.legend:empty{display:none}
.legend span{display:flex;align-items:center;gap:6px}
.info{--c:var(--accent);border-left:1px solid var(--line);padding:6px 8px;
 overflow:hidden;display:flex;flex-direction:column;gap:9px}
/* верх панелі (назва, опис, плюс) стоїть; «з чого це» гортається окремо */
.info .fixed{flex:none;display:flex;flex-direction:column;gap:9px}
.info .ihead{display:flex;align-items:center;gap:9px}
.info svg{width:26px;height:26px;stroke:var(--c);fill:none;stroke-width:1.6;
 stroke-linecap:round;stroke-linejoin:round}
.info h3{margin:0;font-size:1rem;font-weight:600}
.info p{margin:0;font-size:.87rem;color:var(--soft);line-height:1.5}
.info .ihead h3{flex:1;min-width:0}
.pm{flex:none;width:26px;height:26px;padding:0;border:1px solid var(--c);
 background:var(--c);color:#fff;border-radius:4px;font-size:1rem;line-height:1;
 cursor:pointer;display:flex;align-items:center;justify-content:center}
.pm.off{background:transparent;color:var(--c)}
.src{margin-top:auto;padding-top:10px;border-top:1px solid var(--line);
 display:flex;flex-direction:column;gap:7px;flex:1 1 0;min-height:0;
 overflow-y:auto;scrollbar-width:thin;scrollbar-color:var(--line) transparent}
.src .one[data-pic]{cursor:zoom-in}
/* спливаюче вікно з більшим фото деталі */
.modal{position:fixed;inset:0;background:rgba(0,0,0,.45);display:flex;align-items:center;
 justify-content:center;z-index:50;padding:16px}
.mbox{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:6px;
 padding:14px 14px 12px;max-width:min(92vw,560px);max-height:86vh;display:flex;
 flex-direction:column;gap:10px;align-items:center;box-shadow:0 8px 30px rgba(0,0,0,.25)}
.mbox .mpic{max-width:min(84vw,500px);max-height:62vh;object-fit:contain;border-radius:4px;
 background:#fff}
.mbox .mname{font-size:.9rem;font-weight:500;text-align:center;padding:0 24px}
.mt{margin:0;font-size:1rem;font-weight:600;padding:0 28px 0 0;align-self:flex-start}
.mq{margin:0;font-size:.95rem;text-align:center;padding:0 22px}
.mq.small{font-size:.8rem;color:var(--soft);text-align:left;padding:0;align-self:flex-start}
.mbtns{display:flex;gap:10px;justify-content:center}
.mb{border:1px solid var(--accent);background:transparent;color:var(--accent);border-radius:4px;
 padding:6px 14px;cursor:pointer;font:inherit;font-size:.86rem;flex:none}
.mb.yes,.mb.add{background:var(--accent);color:#fff}
.mb:hover{box-shadow:0 0 0 3px var(--glow)}
.alist{overflow-y:auto;min-height:0;width:100%;display:flex;flex-direction:column;gap:6px;
 scrollbar-width:thin;scrollbar-color:var(--line) transparent}
.al{display:flex;align-items:center;gap:10px;border:1px solid var(--line);border-radius:4px;
 padding:6px 9px;background:var(--paper)}
.alt{min-width:0;flex:1}
.al .pm{--c:var(--accent)}
.rhead .pm{--c:var(--accent);width:24px;height:24px;font-size:.95rem;margin-left:auto}
.rhead .copy{margin-left:0}
.mbox.wide{max-width:min(94vw,760px)}
.acat{width:100%}
.acat summary{cursor:pointer;list-style:none;display:flex;align-items:center;gap:8px;font-size:.86rem;
 font-weight:600;padding:6px 8px;border:1px solid var(--line);border-radius:4px;background:var(--paper);margin:0 0 4px}
.acat summary::-webkit-details-marker{display:none}
.acat summary::before{content:'▸';font-size:.8rem;color:var(--soft)}
.acat[open] summary::before{content:'▾'}
.acat .cnt{margin-left:auto;font-size:.72rem;font-weight:500;color:var(--soft)}
.acat .al{margin:0 0 4px 10px}
.asub{margin:0 0 4px 10px}
.asub summary{cursor:pointer;list-style:none;display:flex;align-items:center;gap:8px;font-size:.8rem;
 font-weight:500;padding:4px 8px;border:1px solid var(--line);border-radius:4px;margin:0 0 4px;color:var(--ink)}
.asub summary::-webkit-details-marker{display:none}
.asub summary::before{content:'▸';font-size:.75rem;color:var(--soft)}
.asub[open] summary::before{content:'▾'}
.asub .cnt{margin-left:auto;font-size:.7rem;font-weight:500;color:var(--soft)}
.mf{width:100%;border:1px solid var(--line);border-radius:4px;padding:6px 9px;font:inherit;font-size:.86rem;
 background:var(--paper);color:var(--ink)}
.mf:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--glow)}
.al.done2{opacity:.55}
.okmark{font-size:.72rem;color:var(--down);flex:none}
.al b{display:block;font-size:.88rem;font-weight:600;line-height:1.25}
.ings{display:flex;flex-wrap:wrap;gap:2px 10px;font-size:.74rem;margin-top:2px}
.ings i{font-style:normal}
.ings .ok{color:var(--down)}
.ings .no{color:var(--up);font-weight:600}
.cbar{display:flex;align-items:stretch;gap:6px}
.cbt{flex:1;display:flex;align-items:center;gap:8px;border:1px solid var(--line);border-radius:4px;
 padding:4px 8px;background:var(--paper);cursor:pointer;text-align:left;font:inherit;
 color:var(--soft);min-width:0}
.cbt:hover{border-color:var(--accent)}
.cbt b{font-size:.66rem;font-weight:500;text-transform:uppercase;letter-spacing:.07em}
.cbt .n{margin-left:auto;min-width:22px;height:20px;padding:0 7px;border-radius:10px;
 background:var(--accent);color:#fff;font-size:.74rem;font-weight:600;
 display:flex;align-items:center;justify-content:center}
.cbt .n.zero{background:var(--line);color:var(--soft)}
.cbt .chev{font-size:.8rem;line-height:1}
.q{flex:none;width:32px;border:1px solid var(--line);border-radius:4px;background:var(--paper);
 color:var(--accent);font:inherit;font-weight:600;cursor:pointer}
.q:hover{border-color:var(--accent);box-shadow:0 0 0 3px var(--glow)}
.mclose{position:absolute;top:6px;right:6px;width:26px;height:26px;border:1px solid var(--line);
 background:var(--panel);color:var(--soft);border-radius:4px;cursor:pointer;font-size:1rem;
 line-height:1;display:flex;align-items:center;justify-content:center}
.src>b{flex:none}
.src>b{font-weight:500;text-transform:uppercase;letter-spacing:.07em;
 font-size:.66rem;color:var(--soft)}
.src .one{display:flex;gap:9px;align-items:center}
.hints b{display:block;font-weight:500;text-transform:uppercase;letter-spacing:.07em;
 font-size:.66rem;color:var(--soft);margin-bottom:4px}
.hints ul{margin:0;padding-left:16px;font-size:.84rem;line-height:1.45;color:var(--ink)}
.hints li{margin:2px 0}
.src img,.src .nopic{width:46px;height:46px;flex:none;border:1px solid var(--line);
 border-radius:3px;object-fit:cover;background:var(--paper);
 display:flex;align-items:center;justify-content:center}
.src .nopic svg{width:20px;height:20px;stroke:var(--c);opacity:.55}
.src .one>div{min-width:0}
.src .one b{display:block;font-size:.76rem;font-weight:500;line-height:1.3;
 color:var(--ink);min-width:0}
.src .one span{display:block;margin-top:2px;font-size:.71rem;color:var(--soft);
 line-height:1.35;display:-webkit-box;-webkit-line-clamp:2;
 -webkit-box-orient:vertical;overflow:hidden}
.info .empty2{margin:auto 0;color:var(--soft);font-size:.87rem;text-align:center}
.mrow{display:flex;align-items:flex-start;gap:10px;margin:7px 0 0}
.mrow>b{--c:var(--accent);flex:none;width:86px;padding-top:4px;font-weight:500;
 font-size:.7rem;text-transform:uppercase;letter-spacing:.07em;color:var(--c)}
.mrow>b[data-g=sens]{--c:var(--sens)}.mrow>b[data-g=meas]{--c:var(--meas)}
.mrow>b[data-g=act]{--c:var(--act)}.mrow>b[data-g=talk]{--c:var(--talk)}
.mrow>b[data-g=pow]{--c:var(--pow)}
.micons{display:flex;flex-wrap:wrap;gap:5px}
.mini2{--c:var(--accent);display:flex;align-items:center;gap:6px;cursor:pointer;text-align:left;
 background:color-mix(in srgb,var(--c) 12%,transparent);border:1px solid transparent;
 border-radius:4px;padding:3px 7px 3px 6px;color:var(--c);font-size:.79rem}
.mini2[data-g=sens]{--c:var(--sens)}.mini2[data-g=meas]{--c:var(--meas)}
.mini2[data-g=act]{--c:var(--act)}.mini2[data-g=talk]{--c:var(--talk)}
.mini2[data-g=pow]{--c:var(--pow)}
.mini2:hover{border-color:var(--c)}
.mini2 svg{width:15px;height:15px;stroke:var(--c);fill:none;stroke-width:1.7;
 stroke-linecap:round;stroke-linejoin:round}
.pick b{font-size:.77rem;font-weight:500;line-height:1.2;text-align:center;
 word-break:break-word;transition:color .18s ease}
.pick[aria-current=true]{background:color-mix(in srgb,var(--c) 13%,transparent);
 border-color:var(--c);color:var(--c)}
.pick[aria-current=true]:hover{transform:none}
.picksep:first-child{margin-top:0}
.picksep{grid-column:1/-1;display:flex;align-items:center;gap:9px;margin:11px 0 2px;
 color:var(--soft);font-size:.74rem;text-transform:uppercase;letter-spacing:.09em}
.picksep::after{content:'';flex:1;height:1px;background:var(--line)}
.picksep[data-g=sens]{color:var(--sens)}
.picksep[data-g=meas]{color:var(--meas)}
.picksep[data-g=act]{color:var(--act)}
.picksep[data-g=talk]{color:var(--talk)}
.picksep[data-g=pow]{color:var(--pow)}
.picks .pick.dim{opacity:.5}
.scroll{flex:1;min-height:0;overflow-y:auto;overscroll-behavior:contain;
 padding:0 4px 22px;margin:0 -4px;scrollbar-width:thin;
 scrollbar-color:var(--line) transparent}
.scroll::-webkit-scrollbar{width:10px}
.scroll::-webkit-scrollbar-track{background:transparent}
.scroll::-webkit-scrollbar-thumb{background:var(--line);border-radius:99px;
 border:3px solid var(--paper);background-clip:padding-box}
button{font:inherit;color:inherit}
/* ── верхня смуга ────────────────────────────── */
.bar{flex:none;display:flex;align-items:center;gap:8px;padding:6px 0 4px}
.barmain{flex:1;min-width:0;display:flex;align-items:baseline;gap:12px}
.bar h1{margin:0;font:600 1.5rem/1.15 Georgia,serif;letter-spacing:-.01em;
 cursor:pointer;width:max-content}
.bar .lede{margin:5px 0 0}
.navbtns{display:flex;gap:7px;flex:none;margin-top:2px}
.switch.sq{padding:0;width:36px;height:36px;justify-content:center;flex:none}
.switch.sq svg{width:19px;height:19px}
.switch{background:var(--panel);border:1px solid var(--line);border-radius:4px;
 padding:8px 18px;cursor:pointer;font-size:.9rem;box-shadow:var(--lift);
 display:inline-flex;align-items:center;gap:8px;transition:border-color .15s}
.switch:hover{border-color:var(--accent);color:var(--accent)}
.switch[aria-pressed=true]{background:var(--accent);border-color:var(--accent);color:#fff}
.can{list-style:none;margin:13px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:7px}
.can li{font-size:.85rem;color:var(--accent);background:var(--tint);
 border-radius:8px;padding:4px 11px}
.switch svg{width:15px;height:15px;stroke:currentColor;fill:none;stroke-width:1.8}
/* ── шапка ───────────────────────────────────── */
.lede{margin:0;color:var(--soft);font-size:.8rem;flex:1;min-width:0;
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.eng{display:flex;align-items:center;gap:8px;margin:10px 0 0;color:var(--soft);
 font-size:.88rem;cursor:pointer;user-select:none;width:max-content}
.eng input{accent-color:var(--accent);width:15px;height:15px;cursor:pointer}
.searchbox{position:relative;flex:none;width:290px;margin-top:2px}
.searchbox svg{position:absolute;left:15px;top:50%;transform:translateY(-50%);
 width:16px;height:16px;stroke:var(--soft);fill:none;stroke-width:1.8}
.search{width:100%;padding:9px 16px 9px 41px;font:inherit;font-size:.94rem;
 color:var(--ink);background:var(--paper);border:1px solid var(--line);
 border-radius:4px}
.search::placeholder{color:var(--soft)}
.search:focus{outline:none;border-color:var(--accent);background:var(--panel)}
/* ── ідеї ────────────────────────────────────── */
.need li{font-size:.83rem;background:var(--tint);color:var(--accent);
 border-radius:8px;padding:4px 11px;cursor:pointer}
.need li:hover{background:var(--accent);color:var(--panel)}
.need li.miss{background:transparent;border:1px dashed var(--line);color:var(--soft);
 cursor:default}
.need li.miss:hover{background:transparent;color:var(--soft)}
/* ── плитки каталогу ─────────────────────────── */
.tiles{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));
 margin:12px 0 0}
.tile{display:flex;align-items:flex-start;gap:11px;background:var(--panel);
 border:1px solid var(--line);border-radius:6px;padding:13px 15px;cursor:pointer;
 text-align:left;box-shadow:var(--lift);min-width:0;overflow:hidden;
 transition:transform .16s ease,border-color .16s ease}
.tile>div{flex:1;min-width:0}
.tile:hover{transform:translateY(-3px);border-color:var(--accent)}
.tile svg{width:19px;height:19px;flex:none;margin-top:2px;stroke:var(--accent);
 fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.tile b{display:block;font-size:1.02rem;margin-bottom:2px;white-space:nowrap;
 overflow:hidden;text-overflow:ellipsis}
.tile span{display:block;color:var(--soft);font-size:.83rem;line-height:1.4;
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tile em{flex:none;color:var(--accent);font-style:normal;font-size:.8rem;
 font-variant-numeric:tabular-nums}
.tile u{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
 margin-top:6px;padding-top:6px;text-decoration:none;
 border-top:1px solid var(--line);color:var(--soft);font-size:.8rem;line-height:1.4}
.grid{display:grid;gap:8px;grid-template-columns:repeat(auto-fill,minmax(268px,1fr));
 align-items:start}
.card{min-width:0;overflow:hidden;background:var(--panel);
 border:1px solid var(--line);border-radius:5px;padding:10px 14px}
.card.haspic{display:flex;gap:11px;align-items:flex-start}
.card .cbody{min-width:0;flex:1}
.card .th{width:44px;height:44px;flex:none;object-fit:cover;border-radius:3px;
 border:1px solid var(--line);background:var(--paper)}
.card h3{display:flex;align-items:center;gap:8px;margin:0;min-width:0;font-size:.98rem;
 font-weight:600;line-height:1.3}
.card h3 svg{width:16px;height:16px;flex:none;stroke:var(--accent);fill:none;
 stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.card h3 i{margin-left:auto;font-style:normal;font-size:.78rem;color:var(--accent);
 background:var(--tint);border-radius:6px;padding:1px 7px;
 font-variant-numeric:tabular-nums}
.card p{margin:3px 0 0;color:var(--soft);font-size:.85rem;line-height:1.4;
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card .can{margin:2px 0 0;color:var(--accent);font-size:.81rem;line-height:1.4;
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tile.basis{background:transparent;box-shadow:none;grid-column:1/-1;
 display:flex;align-items:center;gap:16px;padding:18px 20px}
.tile.basis svg{margin:0;flex:none}
.tile.basis div{min-width:0}
.tile.basis b{font-size:1.03rem;margin-bottom:2px}
.tile.basis em{margin:0 0 0 auto;flex:none;padding-left:16px}
/* ── картки деталей ──────────────────────────── */
.head{display:flex;align-items:baseline;gap:12px;margin:6px 0 10px;
 padding-bottom:8px;border-bottom:1px solid var(--line)}
.head h2{font:600 1.3rem/1.1 Georgia,serif;margin:0;flex:none}
.head span{color:var(--soft);font-size:.9rem;margin-left:auto}
.back{background:none;border:0;font-size:.92rem;color:var(--accent);cursor:pointer;
 padding:0;margin:46px 0 0}
.back:hover{text-decoration:underline}
.ideas{display:grid;gap:16px;grid-template-columns:repeat(2,1fr);align-items:start}
.idea{min-width:0;background:var(--panel);border:1px solid var(--line);border-radius:6px;
 padding:22px 24px 18px;box-shadow:var(--lift)}
.idea h3{margin:0 0 9px;font:600 1.28rem/1.25 Georgia,serif;letter-spacing:-.01em}
.idea>p{margin:0;color:var(--soft);font-size:.97rem}
.need{list-style:none;display:flex;flex-wrap:wrap;gap:6px;margin:15px 0 0;padding:0}
.need li{font-size:.83rem;background:var(--tint);color:var(--accent);
 border-radius:8px;padding:4px 11px;cursor:pointer}
.need li:hover{background:var(--accent);color:var(--panel)}
.need li.miss{background:transparent;border:1px dashed var(--line);color:var(--soft);
 cursor:default}
details{margin:8px 0 0}
summary{cursor:pointer;color:var(--soft);font-size:.8rem;list-style:none}
summary::-webkit-details-marker{display:none}
summary:hover{color:var(--accent)}
details table{width:100%;border-collapse:collapse;margin-top:8px;font-size:.82rem}
details td{padding:4px 0;border-top:1px solid var(--line);color:var(--soft);
 vertical-align:top}
details td:last-child{text-align:right;white-space:nowrap;padding-left:12px;
 font-variant-numeric:tabular-nums}
.zero{opacity:.5}
.empty{text-align:center;color:var(--soft);padding:70px 0}
footer{margin:56px 0 0;padding-top:20px;border-top:1px solid var(--line);
 color:var(--soft);font-size:.85rem;text-align:center}
footer a{color:var(--accent)}
.hide{display:none}
@media(max-width:820px){.tiles{grid-template-columns:1fr}
 .tile u{display:none}
 .grid,.ideas{grid-template-columns:1fr}
 .nav{flex-wrap:wrap;gap:12px}
 .bar .searchbox{order:3;flex-basis:100%;max-width:none}
 .bar .navbtns{margin-left:auto}}
/* обране зверху: підпис групи рядком, під ним плашки — так місця більше */
.mrow{display:block;margin:3px 0 0}
.mrow:first-child{margin-top:0}
.mrow>b{--c:var(--accent);display:block;width:auto;padding:0;margin:0 0 2px;font-weight:500;
 font-size:.62rem;text-transform:uppercase;letter-spacing:.08em;color:var(--c)}
.micons{display:flex;flex-wrap:wrap;gap:5px}

/* ледь помітна підсвітка зверху і м'яка тінь — «рамка» на кнопках */
.row,.kind,.tab,.switch,.mini2,.cmb,.done,.cbar,.pm,.copy,.done .x,.mclose{
 box-shadow:inset 0 1px 0 var(--hi),0 1px 2px var(--sh)}
.row:hover,.kind:hover,.switch:hover,.cmb:hover,.cbar:hover,.copy:hover,.mini2:hover{
 box-shadow:inset 0 1px 0 var(--hi),0 0 0 3px var(--glow)}
.row[aria-current=true],.tab[aria-pressed=true]{
 box-shadow:inset 0 1px 0 var(--hi),0 0 0 2px var(--glow)}
.top,.pane,.tabs{box-shadow:0 1px 3px var(--sh)}

/* телефон: одна колонка зверху, список і панель по черзі знизу, менші відступи */
@media(max-width:640px){
 .wrap{padding:0 3px}
 .bar{padding:4px 0 3px;gap:5px}
 .bar h1{font-size:1.2rem}
 .lede{display:none}
 .stage{gap:3px;padding:0 0 3px}
 .stage[data-step=build] .top{flex:0 0 38%;padding:3px 5px 3px}
 .tp{gap:5px}
 .tpr{padding-left:5px}
 .mrow>b{width:58px;font-size:.6rem}
 .tab{font-size:.72rem;padding:6px 2px}
 .tab .d{display:none}
 .tab .m{display:block;white-space:normal}
 /* щільніше, але читабельно: менший шрифт і відступи замість обрізання */
 .row{padding:9px 6px;gap:5px;min-height:40px}
 .row b{font-size:.8rem}
 .row svg{width:16px;height:16px}
 .row .dir svg{width:12px;height:12px}
 .mini2{padding:3px 7px;gap:4px}
 .mini2 span{font-size:.76rem}
 .info p{font-size:.82rem}
 .hints ul{font-size:.8rem}
 .pane{grid-template-columns:1fr}
 .pane .info{grid-column:1;grid-row:1/2;display:none;border-left:0}
 .pane .legend{grid-column:1}
 .stage[data-look="1"] .plist{display:none}
 .stage[data-look="1"] .info{display:flex}
 .stage[data-look="1"] .legend{display:none}
 .toList{display:inline-flex}
 .info .fixed{flex:0 1 auto;min-height:0;overflow-y:auto}
 .src{min-height:38%}
 .plist{grid-template-columns:repeat(auto-fill,minmax(140px,1fr));padding:5px;gap:4px}
 .info{padding:6px 8px}
}
"""

JS = r"""
const PICS=__PICS__;
const ANSWERS=__ANSWERS__, KINDS=__KINDS__, IDEAS=__IDEAS__, DATA=__DATA__, THEMES=__THEMES__, ICONS=__ICONS__, RECIPES=__RECIPES__;
const PICDATA=__PICDATA__;
const BUILT=__BUILT__;
const picsrc=f=>PICDATA[f]||('pics/'+f);
const $=s=>document.querySelector(s);
const hero=$('#hero'), tiles=$('#tiles'), list=$('#list'), q=$('#q');
const ex=$('#ex'), cat=$('#cat'), sb=$('#sb'), scroller=$('#scroll');
const engBox=$('#engbox'), engRow=$('#eng'), ttl=$('#ttl');
const stage=$('#stage'), topPane=$('#top');
const tabsEl=$('#tabs'), plist=$('#plist'), infoEl=$('#info');
const QS=[["рух","Що воно робить"],["помічає","Що помічає"],
          ["каже","Як тобі каже"],["керує","Як ним керуєш"],
          ["енергія","Звідки енергія"]];
let qOpen='помічає', kind=null, sub=null, look=null;
const picked=new Set();
// чи пасує вміння обраному виду: явні «типи:» — як написано; інакше — чи є воно
// в рецептах категорії цього виду (живлення пасує завжди)
const relCache={};
function relevantSet(k){
  if(relCache[k]) return relCache[k];
  const cat=KIND_CAT[k], s=new Set();
  if(cat) RECIPES.filter(r=>r.sec===cat).forEach(r=>r.need.flat().forEach(n=>s.add(n)));
  let grew=true;   // складники-рецепти розгорнути до умінь
  while(grew){grew=false;RECIPES.forEach(r=>{ if(s.has(r.name)) r.need.flat().forEach(n=>{ if(!s.has(n)){s.add(n);grew=true;} }); });}
  return relCache[k]=s;
}
const fits=a=>{
  if(kind==='своє'||a.g==='живлення') return true;
  if(a.kinds.length) return a.kinds.includes(kind);
  const s=relevantSet(kind); return !s.size||s.has(a.name);
};
// ключ групи, два рядки підпису вкладки, два коротші рядки для телефону
const TABS=[["помічає","Реагує на","зовнішні зміни","Реагує","на зміни"],
            ["міряє","Вимірює","за нашим запитом","Вимірює","на запит"],
            ["робить","Віддаємо команду","робити","Робить","команди"],
            ["взаємодія","Відображення","і контроль","Показує","і керуєш"],
            ["живлення","Живлення","","Живлення",""]];
// рядки зведення обраного: група, підблок (або null), короткий підпис
const ROWS=[["помічає",null,"Реагує"],["міряє",null,"Вимірює"],
            ["робить",null,"Робить"],["взаємодія","каже","Показує"],
            ["взаємодія","керує","Керуєш"],["живлення",null,"Живлення"]];
const GCODE={"помічає":"sens","міряє":"meas","робить":"act",
             "взаємодія":"talk","живлення":"pow"};
const answersFor=q=>q==='інше'?ANSWERS.filter(a=>!fits(a))
                            :ANSWERS.filter(a=>a.q===q&&fits(a));
let mode='build', view=null;

const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const svg=k=>`<svg viewBox="0 0 24 24"><path d="${ICONS[k]}"/></svg>`;
const pic=k=>PICS[k]?`<svg viewBox="0 0 24 24"><path d="${PICS[k]}"/></svg>`:'';
const kidsOf=k=>KINDS.filter(x=>x['батько']===k);
const kindName=k=>(KINDS.find(x=>x.key===k)||{}).name||'';
const inTheme=(c,k)=>k==='основа'?(!c.themes.length&&c.basis.length):c.themes.includes(k);
const shown=c=>engBox.checked||c.lvl==='видима';
const pl=(n,f)=>{const a=n%10,b=n%100;
  return f[(a===1&&b!==11)?0:(a>=2&&a<=4&&(b<12||b>14))?1:2];};


/* ── картки ─────────────────────────────── */
// значок і назва в один рядок, ідеї — рядком під ними
const thumb=c=>c.pic?`<img class="th" src="${picsrc(c.pic)}" alt="" loading="lazy">`:'';

function ableCard(c){
  const ic=c.themes[0]||c.basis[0];
  const can=c.ideas.length
    ? `<p class="can">${c.ideas.map(esc).join(' · ')}</p>` : '';
  return `<article class="card${c.pic?' haspic':''}">${thumb(c)}<div class="cbody">
    <h3>${ic?svg(ic):''}${esc(c.name)}</h3>
    <p>${esc(c.what)}</p>${can}</div></article>`;
}

function partCard(c){
  const zero=String(c.qty)==='0';
  const ideas=c.ideas.length?`<p class="can">${c.ideas.map(esc).join(' · ')}</p>`:'';
  const rows=c.variants.map(v=>`<tr><td>${esc(v.tech)}${v.note?' — '+esc(v.note):''}</td>
    <td>${esc(v.qty)}</td></tr>`).join('');
  const ic=c.themes[0]||c.basis[0];
  return `<article class="card${zero?' zero':''}${c.pic?' haspic':''}">${thumb(c)}
    <div class="cbody"><h3>${ic?svg(ic):''}${esc(c.name)}
    <i>${zero?'нема':esc(c.qty)}</i></h3><p>${esc(c.what)}</p>${ideas}
    <details><summary>${c.variants.length>1
      ? c.variants.length+' '+pl(c.variants.length,['різновид','різновиди','різновидів'])
      : 'що це насправді'}</summary><table>${rows}</table></details></div></article>`;
}

/* ── плитки ─────────────────────────────── */
// у плитці видно справжні назви — щоб зрозуміти, не клікаючи
function peekNames(k,n){
  return DATA.filter(c=>inTheme(c,k)&&shown(c))
    .sort((a,b)=>b.ideas.length-a.ideas.length)
    .slice(0,n).map(c=>esc(c.name)).join(' · ');
}
function drawTiles(){
  let h='';
  for(const [k,title,sub] of THEMES){
    const n=DATA.filter(c=>inTheme(c,k)&&shown(c)).length;
    if(!n) continue;
    h+=`<button class="tile" data-k="${k}">${svg(k)}<div><b>${title}</b>
        <span>${sub}</span><u>${peekNames(k,3)}${n>3?' …':''}</u></div>
        <em>${n}</em></button>`;
  }
  tiles.innerHTML=h;
}

/* ── режими ─────────────────────────────── */
// значок і назва в один рядок, ідеї — рядком під ними
function ableCard(c){
  const ic=c.themes[0]||c.basis[0];
  const can=c.ideas.length
    ? `<p class="can">${c.ideas.map(esc).join(' · ')}</p>` : '';
  return `<article class="card${c.pic?' haspic':''}">${thumb(c)}<div class="cbody">
    <h3>${ic?svg(ic):''}${esc(c.name)}</h3>
    <p>${esc(c.what)}</p>${can}</div></article>`;
}

function partCard(c){
  const zero=String(c.qty)==='0';
  const ideas=c.ideas.length?`<p class="can">${c.ideas.map(esc).join(' · ')}</p>`:'';
  const rows=c.variants.map(v=>`<tr><td>${esc(v.tech)}${v.note?' — '+esc(v.note):''}</td>
    <td>${esc(v.qty)}</td></tr>`).join('');
  const ic=c.themes[0]||c.basis[0];
  return `<article class="card${zero?' zero':''}${c.pic?' haspic':''}">${thumb(c)}
    <div class="cbody"><h3>${ic?svg(ic):''}${esc(c.name)}
    <i>${zero?'нема':esc(c.qty)}</i></h3><p>${esc(c.what)}</p>${ideas}
    <details><summary>${c.variants.length>1
      ? c.variants.length+' '+pl(c.variants.length,['різновид','різновиди','різновидів'])
      : 'що це насправді'}</summary><table>${rows}</table></details></div></article>`;
}

function ideaCard(i){
  const need=i.parts.map(p=>p.have
    ? `<li data-go="${esc(p.name)}">${esc(p.name)}</li>`
    : `<li class="miss">${esc(p.name)} — нема</li>`).join('');
  return `<article class="idea"><h3>${esc(i.name)}</h3><p>${esc(i.what)}</p>
    <ul class="need">${need}</ul></article>`;
}

function themed(render){
  const t=q.value.trim().toLowerCase();
  const hits=t
    ? DATA.filter(c=>shown(c)&&(c.name+' '+c.what+' '+c.ideas.join(' ')+' '+
        c.variants.map(v=>v.tech).join(' ')).toLowerCase().includes(t))
    : (view?DATA.filter(c=>inTheme(c,view)&&shown(c)):null);
  if(!hits){tiles.classList.remove('hide');list.innerHTML='';return;}
  tiles.classList.add('hide');
  const m=THEMES.find(x=>x[0]===view);
  const head=t?`<div class="head"><h2>Знайшлось</h2><span>${hits.length}</span></div>`
    :`<div class="head"><button class="back" id="back">←</button>
      <h2>${m?m[1]:''}</h2><span>${m?m[2]:''}</span></div>`;
  list.innerHTML=head+(hits.length
    ?`<div class="grid">${hits.map(render).join('')}</div>`
    :`<div class="empty">Нічого не знайшлось</div>`);
  const b=$('#back'); if(b) b.onclick=()=>{view=null;draw();scroller.scrollTop=0;};
}

function renderIdeas(){
  const t=q.value.trim().toLowerCase();
  const hits=IDEAS.filter(i=>!t||(i.name+' '+i.what+' '+
    i.parts.map(p=>p.name).join(' ')).toLowerCase().includes(t));
  tiles.classList.add('hide');
  list.innerHTML=(hits.length?`<div class="ideas">${hits.map(ideaCard).join('')}</div>`
                :`<div class="empty">Нічого не знайшлось</div>`);
}

const HEAD={
 build:['Що зробимо','Обери, що воно має вміти — і дивись, що виходить.','—'],
 able:['Що це вміє','Кожна річ і те, на що вона здатна. Придумуй своє — поєднання ніхто не обмежував.','мотор, світло, вода, звук…'],
 examples:['Приклади','Кілька штук, які вже придумались. Не межа, а розгін — найцікавіше те, чого тут немає.','полив, замок, музика…'],
 catalog:['Каталог','Усі деталі з кількостями й моделями.','мотор, екран, батарея…'],
};

/* ── конструктор ────────────────────────── */
function drawKinds(){
  tabsEl.innerHTML=''; plist.innerHTML=''; infoEl.innerHTML='';
  const list=kind?kidsOf(kind):KINDS.filter(x=>!x['батько']);
  const back=kind?`<button class="back" data-kback="1">← назад</button>`:'';
  topPane.innerHTML=`${back}<div class="kinds">${list.map(k=>
      `<button class="kind" data-kind="${k.key}">${pic(k['значок'])}
       <span><b>${esc(k.name)}</b>${k.what?`<i>${esc(k.what)}</i>`:''}</span>
      </button>`).join('')}</div>${kind?'':`<div class="ver">збірка ${BUILT}</div>`}`;
}

// товсті стрілки: вниз (зелена) — воно показує тобі, вгору (червона) — ти керуєш
const ARR={up:'<svg class="up" viewBox="0 0 16 16"><path d="M8 13.5V2.5M3.5 7l4.5-4.5L12.5 7"/></svg>',
           down:'<svg class="down" viewBox="0 0 16 16"><path d="M8 2.5v11M3.5 9l4.5 4.5L12.5 9"/></svg>'};
const arrow=a=>a.dir==='від'?`<span class="dir">${ARR.up}</span>`
    :a.dir==='до'?`<span class="dir">${ARR.down}</span>`
    :a.dir==='обидва'?`<span class="dir">${ARR.up}${ARR.down}</span>`:'';

function drawRail(){
  tabsEl.innerHTML=TABS.map(([k,l1,l2,m1,m2])=>
    `<button class="tab" data-g="${GCODE[k]}" data-tab="${k}"${
      k===qOpen?' aria-pressed="true"':''}><span class="d">${l1}</span>${
      l2?`<span class="d">${l2}</span>`:''}<span class="m">${m1}</span>${
      m2?`<span class="m">${m2}</span>`:''}</button>`).join('');
  const items=ANSWERS.filter(a=>a.g===qOpen&&!picked.has(a.name))
    .sort((a,b)=>(fits(b)?1:0)-(fits(a)?1:0));
  plist.innerHTML=items.map(a=>
    `<button class="row${fits(a)?'':' dim'}" data-g="${GCODE[a.g]||''}"
      data-look="${esc(a.name)}"${a.name===look?' aria-current="true"':''}>${
      pic(a.icon)}<b>${esc(a.name)}</b>${arrow(a)}</button>`).join('')
    ||`<div class="empty2">Тут уже все обрано.</div>`;
  stage.dataset.look=look?'1':'';   // на телефоні панель підміняє список
  // підпис під списком: що означають стрілки (тільки де вони є)
  document.getElementById('legend').innerHTML=qOpen==='взаємодія'
    ?`<span><i class="dir">${ARR.down}</i>воно показує тобі</span>
      <span><i class="dir">${ARR.up}</i>ти керуєш ним</span>`:'';
  drawInfo();
}

function drawInfo(){
  const a=ANSWERS.find(x=>x.name===look);
  if(!a){infoEl.removeAttribute('data-g');
    infoEl.innerHTML=`<div class="empty2">Тицьни щось зліва — тут напишу,
      що це і з чого воно.</div>`;return;}
  infoEl.dataset.g=GCODE[a.g]||'';
  const has=picked.has(a.name);
  const src=(a.src||[]).map(s=>`<div class="one"${s.pic?` data-pic="${esc(s.pic)}" data-name="${esc(s.tech)}" title="показати більше"`:''}>${
      s.pic?`<img src="${picsrc(s.pic)}" alt="" loading="lazy"
              onerror="this.replaceWith(Object.assign(document.createElement('div'),
              {className:'nopic'}))">`:`<div class="nopic">${pic(a.icon)}</div>`}
      <b>${esc(s.tech)}</b></div>`).join('');
  // натяки, куди це може піти — з поля «ідеї:» в answers.md
  const hints=(a.ideas||[]).length?`<div class="hints"><b>куди це може піти</b><ul>${
      a.ideas.map(i=>`<li>${esc(i)}</li>`).join('')}</ul></div>`:'';
  infoEl.innerHTML=`<div class="fixed">
    <div class="ihead"><button class="toList" data-back="1" title="до списку">←</button>${pic(a.icon)}<h3>${esc(a.name)}</h3>
      <button class="pm${has?' off':''}" data-toggle="${esc(a.name)}"
       title="${has?'прибрати':'додати'}">${has?'−':'+'}</button></div>
    <p>${esc(a.what||'')}</p>${hints}</div>
    ${src?`<div class="src"><b>з чого це</b>${src}</div>`:''}`;
}

function partsOf(){
  const out=new Set();
  for(const n of picked){
    const a=ANSWERS.find(x=>x.name===n);
    if(a) a.names.forEach(x=>out.add(x));
  }
  return out;
}

/* ── збереження в браузері ── */
const KEY='ctor-v2';
let built=[];   // зліплені сутності: {key,name,used:[назви умінь],usedBuilt:[сутності]}
let comboOpen=false;   // чи розгорнута смужка «можна об'єднати»
let work={};   // збереження на кожен вид окремо: {"світло":{picked,built}, "машинка/ровер":{…}}
const slot=(k,sb)=>sb?k+'/'+sb:k;
function stash(){ if(kind) work[slot(kind,sub)]={picked:[...picked],built}; }
function save(){
  stash();
  try{localStorage.setItem(KEY,JSON.stringify({v:2,work,qOpen,comboOpen}));}catch(e){}
}
function clean(w){
  return {picked:(w.picked||[]).filter(n=>ANSWERS.some(a=>a.name===n)),
          built:(w.built||[]).filter(x=>x&&RECIPES.some(r=>r.key===x.key))};
}
function load(){
  try{
    let s=JSON.parse(localStorage.getItem(KEY)||'null');
    if(!s){   // перенести старе збереження (один проєкт) у новий формат
      const o=JSON.parse(localStorage.getItem('ctor-v1')||'null');
      if(o){ const k=o.workKind||o.kind, sb=o.workSub||o.sub;
        s={v:2,work:k?{[slot(k,sb)]:{picked:o.picked||[],built:o.built||[]}}:{},qOpen:o.qOpen,comboOpen:o.comboOpen}; }
    }
    if(!s) return;
    comboOpen=!!s.comboOpen;
    if(s.qOpen&&TABS.some(t=>t[0]===s.qOpen)) qOpen=s.qOpen;
    work={}; Object.keys(s.work||{}).forEach(k=>{ work[k]=clean(s.work[k]); });
    kind=null; sub=null;   // сторінка завжди відкривається з головного екрана
  }catch(e){}
}
// повернути збережене для виду; true, якщо щось було
function restore(k,sb){
  picked.clear(); built=[]; look=null;
  const w=work[slot(k,sb)]; if(!w) return false;
  w.picked.forEach(n=>picked.add(n)); built=w.built.slice(); return true;
}
function resetAll(){
  ask('Стерти все обране в цьому виді й почати спочатку?','Так, стерти',()=>{
    if(kind) delete work[slot(kind,sub)];
    picked.clear();built=[];kind=null;sub=null;look=null;
    save();mode='build';render();});
}

/* ── рецепти відносно обраного: що є, чого бракує ── */
function recipeRows(r,have){
  return r.need.map(alts=>{
    const got=alts.find(n=>have.has(n));
    if(got) return {ok:true,name:got};
    const cand=alts.find(n=>ANSWERS.some(a=>a.name===n));           // просте вміння — можна додати
    const sub=alts.map(n=>RECIPES.find(x=>x.name===n)).find(Boolean); // або інша готова сутність
    return {ok:false,name:cand||(sub&&sub.name)||alts[0],addable:!!(cand||sub)};
  });
}
// «майже зібрано»: бракує рівно одного складника; більші сутності першими
function almost(){
  const have=availNames(), out=[];
  for(const r of RECIPES){
    if(built.some(b=>b.key===r.key)) continue;
    const rows=recipeRows(r,have), miss=rows.filter(x=>!x.ok);
    if(miss.length!==1||!miss[0].addable) continue;
    out.push({r,rows,miss:1});
  }
  return out.sort((a,b)=>b.r.need.length-a.r.need.length||a.r.name.localeCompare(b.r.name,'uk'));
}
const ingsHtml=rows=>`<span class="ings">${rows.map(y=>
  `<i class="${y.ok?'ok':'no'}">${y.ok?'✓':'✗'} ${esc(y.name)}</i>`).join('')}</span>`;
function showAlmost(){
  const list=almost();
  openBox(`<h3 class="mt">Майже зібрано</h3>`+(list.length
    ?`<p class="mq small">Тут те, чому бракує рівно одного. Зелене вже є, червоне — бракує. Плюс бере його і одразу зліплює.</p>
      <div class="alist">${list.map(x=>`<div class="al"><div class="alt"><b>${esc(x.r.name)}</b>${ingsHtml(x.rows)}</div>
        <button class="pm" data-build="${esc(x.r.key)}" title="додати й зліпити">+</button></div>`).join('')}</div>`
    :`<p class="mq">Поки нічого, чому бракує лише одного. Усі рішення — плюс біля «готово».</p>`));
}
// «усі готові рішення»: категорія -> підгрупа -> рецепти; фільтр; категорія обраного виду першою
const KIND_CAT={"світло":"Світло","охорона":"Охорона і замки","погода":"Дім і затишок","грядка":"Рослини",
  "тварини":"Тварини","кухня":"Кухня","прилади":"Дім і затишок","замок":"Охорона і замки",
  "іграшки":"Ігри, іграшки, свята","насобі":"Здоров'я і старші","робот":"Машинки й роботи",
  "машинка":"Машинки й роботи","човен":"Машинки й роботи"};
function showAll(){
  const have=availNames(), cats=[], by={};
  RECIPES.forEach(r=>{ if(!by[r.sec]){by[r.sec]={subs:[],by:{}};cats.push(r.sec);}
    const c=by[r.sec]; if(!c.by[r.sub]){c.by[r.sub]=[];c.subs.push(r.sub);} c.by[r.sub].push(r); });
  const pref=KIND_CAT[kind]||'';
  cats.sort((x,y)=>(y===pref)-(x===pref)||RECIPES.filter(r=>r.sec===y).length-RECIPES.filter(r=>r.sec===x).length);
  const item=r=>{const rows=recipeRows(r,have);
    return {r,rows,miss:rows.filter(x=>!x.ok).length,done:built.some(b=>b.key===r.key)};};
  const itemHtml=x=>`<div class="al${x.done?' done2':''}" data-text="${esc((x.r.name+' '+x.r.need.flat().join(' ')).toLowerCase())}">
      <div class="alt"><b>${esc(x.r.name)}</b>${ingsHtml(x.rows)}</div>${
      x.done?`<span class="okmark">готово</span>`
            :`<button class="pm" data-build="${esc(x.r.key)}" title="${x.miss?'додати '+x.miss+' і зліпити':'зліпити'}">+</button>`}</div>`;
  openBox(`<h3 class="mt">Усі готові рішення</h3>
    <input class="mf" type="search" placeholder="Знайти за назвою або складником…" autocomplete="off">
    <p class="mq small">Розгорни категорію, потім підгрупу. Плюс додає все, чого бракує, і зліплює — навіть цілу сутність усередині.</p>
    <div class="alist">${cats.map((c,ci)=>{
      const cat=by[c]; const n=cat.subs.reduce((k,sname)=>k+cat.by[sname].length,0);
      return `<details class="acat"${ci===0&&pref?' open':''}><summary>${esc(c)}<span class="cnt">${n}</span></summary>${
        cat.subs.map(sname=>{
          const items=cat.by[sname].map(item).sort((p,q)=>(p.done?1:0)-(q.done?1:0)||p.miss-q.miss||q.r.need.length-p.r.need.length);
          return `<details class="asub"><summary>${esc(sname)}<span class="cnt">${items.length}</span></summary>${items.map(itemHtml).join('')}</details>`;
        }).join('')}</details>`;
    }).join('')}</div>`,'wide');
  mbox.querySelector('.mf').focus();
}
function filterAll(q){
  q=q.trim().toLowerCase();
  mbox.querySelectorAll('.al').forEach(el=>{ el.hidden=!!q&&!el.dataset.text.includes(q); });
  mbox.querySelectorAll('.asub').forEach(d=>{ const vis=[...d.querySelectorAll('.al')].some(el=>!el.hidden);
    d.hidden=!vis; if(q) d.open=vis; });
  mbox.querySelectorAll('.acat').forEach(d=>{ const vis=[...d.querySelectorAll('.asub')].some(el=>!el.hidden);
    d.hidden=!vis; if(q) d.open=vis; });
}
// зліпити будь-що: добрати відсутні вміння (перший варіант), вкладені сутності зібрати спершу
function buildFull(key,depth){
  depth=depth||0; if(depth>4) return false;
  const r=RECIPES.find(x=>x.key===key); if(!r) return false;
  if(built.some(b=>b.key===key)) return true;
  for(const alts of r.need){
    if(alts.some(n=>availNames().has(n))) continue;
    const a=alts.find(n=>ANSWERS.some(x=>x.name===n));
    if(a){
      const ab=ANSWERS.find(x=>x.name===a);
      if(ab.g==='живлення') ANSWERS.filter(z=>z.g==='живлення').forEach(z=>picked.delete(z.name));
      picked.add(a); continue;
    }
    const sub=alts.map(n=>RECIPES.find(x=>x.name===n)).find(Boolean);
    if(!sub||!buildFull(sub.key,depth+1)) return false;
  }
  make(key); return true;
}
// домівка: на головний екран, обране лишається — повернешся до того самого типу і все на місці
function goHome(){ save();kind=null;sub=null;look=null;mode='build';render(); }

/* ── усе обране як текст (щоб скопіювати й надіслати) ── */
function exportText(){
  const L=['Що робимо: '+(kindName(sub||kind)||'—')];
  if(picked.size){L.push('','Обрано:');[...picked].forEach(n=>L.push('• '+n));}
  if(built.length){L.push('','Готово:');built.forEach(b=>L.push('• '+b.name+' = '+partsLine(b)));}
  return L.join('\n');
}
function copyAll(btn){
  const text=exportText();
  const done=()=>{btn.classList.add('ok');btn.title='скопійовано';
    setTimeout(()=>{btn.classList.remove('ok');btn.title='Скопіювати все як текст';},1500);};
  const fallback=()=>{const t=document.createElement('textarea');t.value=text;
    document.body.appendChild(t);t.select();try{document.execCommand('copy');done();}catch(e){}
    t.remove();};
  if(navigator.clipboard&&navigator.clipboard.writeText)
    navigator.clipboard.writeText(text).then(done,fallback);
  else fallback();
}

/* ── зліплювання сутностей ── */
const availNames=()=>new Set([...picked, ...built.map(b=>b.name)]);
const canMake=r=>{const have=availNames();return r.need.every(alts=>alts.some(n=>have.has(n)));};
// готові до зліплювання — більші (з більшої кількості складників) першими
const combos=()=>RECIPES.filter(r=>!built.some(b=>b.key===r.key)&&canMake(r))
  .sort((a,b)=>b.need.length-a.need.length||a.name.localeCompare(b.name,'uk'));
function make(key){
  const r=RECIPES.find(x=>x.key===key); if(!r||!canMake(r)) return;
  const rec={key:r.key,name:r.name,used:[],usedBuilt:[]};
  r.need.forEach(alts=>{
    const n=alts.find(x=>picked.has(x));
    if(n){picked.delete(n);rec.used.push(n);return;}
    const bi=built.findIndex(b=>alts.includes(b.name));
    if(bi>=0){rec.usedBuilt.push(built[bi]);built.splice(bi,1);}
  });
  built.push(rec); look=null; save(); drawTop(); drawRail();
}
function unmake(i){
  const rec=built[i]; if(!rec) return;
  built.splice(i,1);
  rec.used.forEach(n=>picked.add(n));
  (rec.usedBuilt||[]).forEach(b=>built.push(b));
  save(); drawTop(); drawRail();
}
const partsLine=rec=>[...rec.used,...(rec.usedBuilt||[]).map(x=>x.name)].join(' + ');

function drawTop(){
  const rows=ROWS.map(([k,q,t])=>{
    const items=[...picked].map(n=>ANSWERS.find(a=>a.name===n))
                           .filter(a=>a&&a.g===k&&(!q||a.q===q));
    if(!items.length) return '';
    return `<div class="mrow"><b data-g="${GCODE[k]}">${t}</b><div class="micons">${
      items.map(a=>`<button class="mini2" data-g="${GCODE[k]}" data-drop="${esc(a.name)}"
        title="${esc(a.name)}">${pic(a.icon)}<span>${esc(a.name)}</span></button>`)
        .join('')}</div></div>`;}).join('');
  const left=rows||`<p class="hint">Тут з'являтиметься все, що ти обереш.</p>`;
  const ready=built.length?built.map((b,i)=>
      `<div class="done"><span><b>${esc(b.name)}</b><i>${esc(partsLine(b))}</i></span>
       <button class="x" data-unmake="${i}" title="розібрати назад">×</button></div>`).join('')
    :`<p class="hint2">Готові сутності з'являться тут.</p>`;
  const have=availNames(), cs=combos();
  const list=cs.length?cs.map(r=>
      `<button class="cmb" data-make="${esc(r.key)}"><b>${esc(r.name)}</b><i>${
        esc(r.need.map(alts=>alts.find(n=>have.has(n))).join(' + '))}</i></button>`).join('')
    :`<p class="hint2">${picked.size?'Додай ще щось — і тут з\'явиться, що з цього можна об\'єднати.'
                                    :'Коли обереш кілька умінь, тут буде видно, що з них виходить.'}</p>`;
  // смужка з лічильником; список видно лише коли розгорнуто
  const combo=`<div class="combo${comboOpen?' open':''}">
      <div class="cbar"><button class="cbt" data-ctoggle="1" aria-expanded="${comboOpen}"><b>можна об'єднати</b>
        <span class="n${cs.length?'':' zero'}">${cs.length}</span>
        <span class="chev">${comboOpen?'▾':'▴'}</span></button>
        <button class="q" data-almost-list="1" title="Що майже зібрано">?</button></div>
      ${comboOpen?`<div class="clist">${list}</div>`:''}</div>`;
  const copyBtn=`<button class="pm" data-all-list="1" title="Усі готові рішення">+</button>
      <button class="copy" data-copy="1" title="Скопіювати все як текст">
      <svg viewBox="0 0 24 24"><path d="M9 9h10v11H9zM5 15V4h10"/></svg></button>`;
  topPane.innerHTML=`<div class="tp"><div class="tpl">${left}</div>
    <div class="tpr"><div class="ready"><div class="rhead"><b class="lbl">готово</b>${copyBtn}</div>${ready}</div>${combo}</div></div>`;
}

function renderBuild(){
  if(!kind || (kidsOf(kind).length && !sub)){
    stage.dataset.step='kinds'; drawKinds(); return; }
  stage.dataset.step='build'; drawRail(); drawTop();
}

function draw(){
  if(mode==='build') renderBuild();
  else if(mode==='examples') renderIdeas();
  else themed(mode==='catalog'?partCard:ableCard);
}
function render(){
  const [h,p,ph]=HEAD[mode];
  if(mode==='build'){
    const deep=kind&&(!kidsOf(kind).length||sub);
    ttl.textContent = deep?kindName(sub||kind) : (kind?'Що саме?':'Що робимо?');
    hero.textContent = deep
      ? 'Обери знизу, що воно має вміти. Усе, що треба всередині, додасться саме.'
      : (kind?'Обери, на що це більше схоже.'
            :'Обери, на що це буде схоже. Усе, що не пасує, сховається в розділ «Інше».');
  } else { ttl.textContent=h; hero.textContent=p; }
  const bare=mode==='able'||mode==='build';
  $('#home').classList.toggle('hide',!kind);
  stage.classList.toggle('hide',mode!=='build');
  scroller.classList.toggle('hide',mode==='build');
  sb.classList.add('hide');   // пошук не потрібен — прибрано скрізь
  engRow.classList.toggle('hide',mode!=='catalog');
  if(bare) q.value='';
  q.placeholder=ph;
  ex.setAttribute('aria-pressed',String(mode==='examples'));
  cat.setAttribute('aria-pressed',String(mode==='catalog'));
  draw();
}
const go=m=>{mode=(mode===m?'build':m);view=null;q.value='';render();scroller.scrollTop=0;};
ex.onclick=()=>go('examples');
cat.onclick=()=>go('catalog');
ttl.onclick=goHome;
$('#home').onclick=goHome;
$('#rst').onclick=resetAll;
tiles.onclick=e=>{const b=e.target.closest('.tile');if(!b)return;
  view=b.dataset.k;draw();scroller.scrollTop=0;};
list.addEventListener('click',e=>{
  const li=e.target.closest('[data-go]');if(!li)return;
  mode='able';view=null;q.value=li.dataset.go;render();scroller.scrollTop=0;});
q.oninput=draw;
engBox.onchange=()=>{drawTiles();draw();};
tabsEl.onclick=e=>{const t=e.target.closest('[data-tab]');if(!t)return;
  qOpen=t.dataset.tab;look=null;save();drawRail();};
plist.onclick=e=>{const b=e.target.closest('[data-look]');if(!b)return;
  look=b.dataset.look;drawRail();};
/* спливаюче вікно поверх усього: фото, підтвердження, «майже зібрано» */
const modal=$('#modal'), mbox=$('#mbox');
function openBox(html,cls){ mbox.className='mbox'+(cls?' '+cls:''); mbox.innerHTML=html+'<button class="mclose" data-close="1" title="закрити">×</button>';
  modal.classList.remove('hide'); }
function closeBox(){ modal.classList.add('hide'); modal.onYes=null; }
function showPic(file,name){
  if(!file) return;
  openBox(`<img class="mpic" src="pics/${esc(file)}" alt=""><b class="mname">${esc(name||'')}</b>`);
}
function ask(text,yesLabel,yes){
  openBox(`<p class="mq">${esc(text)}</p><div class="mbtns">
    <button class="mb yes" data-yes="1">${esc(yesLabel)}</button>
    <button class="mb" data-close="1">Ні</button></div>`);
  modal.onYes=yes;
}
modal.onclick=e=>{
  if(e.target.closest('[data-yes]')){const f=modal.onYes;closeBox();if(f)f();return;}
  const bl=e.target.closest('[data-build]');
  if(bl){buildFull(bl.dataset.build);closeBox();render();return;}
  if(e.target===modal||e.target.closest('[data-close]')) closeBox();
};
document.addEventListener('keydown',e=>{ if(e.key==='Escape') closeBox(); });
modal.addEventListener('input',e=>{ if(e.target.classList.contains('mf')) filterAll(e.target.value); });
infoEl.onclick=e=>{
  if(e.target.closest('[data-back]')){look=null;drawRail();return;}
  const o=e.target.closest('[data-pic]');
  if(o){showPic(o.dataset.pic,o.dataset.name);return;}
  const b=e.target.closest('[data-toggle]');if(!b)return;
  const n=b.dataset.toggle, a=ANSWERS.find(x=>x.name===n);
  if(picked.has(n)) picked.delete(n);
  else {
    if(a&&a.g==='живлення')
      ANSWERS.filter(x=>x.g==='живлення').forEach(x=>picked.delete(x.name));
    picked.add(n);
  }
  look=null;save();drawRail();drawTop();render();};
topPane.addEventListener('click',e=>{
  if(e.target.closest('[data-kback]')){
    save();
    if(sub){sub=null;picked.clear();built=[];} else kind=null;
    render(); return;}
  const k=e.target.closest('[data-kind]');
  if(k){
    const node=KINDS.find(x=>x.key===k.dataset.kind);
    save();   // поточний вид — у свою шухляду
    if(node['батько']) sub=node.key; else { kind=node.key; sub=null; }
    // у цього виду вже щось є — повертаємо; інакше стартові вміння
    if(!restore(kind,sub))
      (node['одразу']||[]).forEach(n=>{ if(ANSWERS.some(a=>a.name===n)) picked.add(n); });
    save(); render(); return;}
  const d=e.target.closest('[data-drop]');
  if(d){look=d.dataset.drop;qOpen=(ANSWERS.find(x=>x.name===look)||{}).g||qOpen;
    drawRail();return;}
  const mk=e.target.closest('[data-make]');
  if(mk){make(mk.dataset.make);return;}
  if(e.target.closest('[data-ctoggle]')){comboOpen=!comboOpen;save();drawTop();return;}
  if(e.target.closest('[data-almost-list]')){showAlmost();return;}
  if(e.target.closest('[data-all-list]')){showAll();return;}
  const cp=e.target.closest('[data-copy]');
  if(cp){copyAll(cp);return;}
  const um=e.target.closest('[data-unmake]');
  if(um){unmake(+um.dataset.unmake);return;}});
/* тема: світла / темна; без вибору — як у системі */
const SUN='<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
const MOON='<svg viewBox="0 0 24 24"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>';
let theme=null; try{theme=localStorage.getItem('theme')||null;}catch(e){}
const isDark=()=>theme?theme==='dark':matchMedia('(prefers-color-scheme:dark)').matches;
function applyTheme(){
  if(theme) document.documentElement.dataset.theme=theme;
  else delete document.documentElement.dataset.theme;
  const b=$('#thm'); b.innerHTML=isDark()?SUN:MOON;
  b.title=isDark()?'Світла тема':'Темна тема';
}
$('#thm').onclick=()=>{theme=isDark()?'light':'dark';
  try{localStorage.setItem('theme',theme);}catch(e){} applyTheme();};
applyTheme();
load();drawTiles();render();
"""


ROVER = os.path.join(ROOT, "apps", "rover")

# Вкладки міні-сайту ровера: (якір, назва, файл або None, група)
# групи: app — апарат, node — вузли, brd — плати
ROVER_TABS = [
    ("obrazy", "Образи",         "looks.html",        "app"),
    ("korpus", "Устрій корпусу", "frame-layers.html", "app"),
    ("zhyv",   "Живлення",       "power.html",        "app"),
    ("ideya",  "Опис ідеї",      None,                "app"),

    ("koleso", "Колесо",         "wheel-tilt.html",   "node"),
    ("ruka",   "Роборука",       "arm.html",          "node"),
    ("pult",   "Пульт",          "remote.html",       "node"),

    ("arch",   "Архітектура",    None,                "brd"),
    ("platy",  "Схема плат",     None,                "brd"),
    ("b1",     "1 · Привід",     None,                "brd"),
    ("b2",     "2 · Навігація",  None,                "brd"),
    ("b3",     "3 · Маршрути",   None,                "brd"),
    ("b4",     "4 · Зв'язок",    None,                "brd"),
    ("b5",     "5 · Камера",     None,                "brd"),
]
ROVER_DEFAULT = "obrazy"

ROVER_STUB = {
    "ideya": ("Опис ідеї",
              "Що це за апарат, для чого, і який у нього список функцій."),
    "arch":  ("Архітектура",
              "Хто що рахує, які контури де живуть, і як діляться задачі між платами."),
    "platy": ("Схема плат",
              "Дерево зв'язків: хто з ким говорить, якими шинами й через що йде живлення."),
    "b1":    ("Плата 1 · Привід",
              "STM32. Енкодери, PWM на драйвери, PID швидкості кожного колеса, "
              "міксер повороту. Найжорсткіший таймінг у ровері."),
    "b2":    ("Плата 2 · Навігація",
              "ESP32. IMU і компас, GNSS, ToF по периметру, одометрія, "
              "маршрут по точках, failsafe. Віддає команди на привід."),
    "b3":    ("Плата 3 · Маршрути",
              "ESP32-S3 з PSRAM. Карта з радара, аналіз перешкод, планування шляху."),
    "b4":    ("Плата 4 · Зв'язок",
              "ESP32. Радіоканал з пультом, розбір команд, телеметрія назад. "
              "Головна в дереві — решта плат висить на ній."),
    "b5":    ("Плата 5 · Камера",
              "ESP32. Відео по Wi-Fi, а коли Wi-Fi немає — обрізаний потік "
              "через плату зв'язку низьким пріоритетом."),
}

VIEWPORT = '<meta name="viewport" content="width=device-width,initial-scale=1">\n'


def copy_rover(out_dir):
    """Кладе міні-сайт ровера в <out>/rover/ окремим розділом. index.html каталогу не чіпає."""
    if not os.path.isdir(ROVER):
        return 0
    dst = os.path.join(out_dir, "rover")
    os.makedirs(dst, exist_ok=True)

    stamp = __import__("datetime").datetime.now().strftime("%Y%m%d%H%M%S")
    n = 0
    for f in sorted(os.listdir(ROVER)):
        if not f.lower().endswith(".html") or f.lower() == "index.html":
            continue  # index.html завжди генерується, а не копіюється
        with open(os.path.join(ROVER, f), encoding="utf-8") as fh:
            body = fh.read()
        if "http-equiv" not in body:
            body = NOCACHE + body
        if 'name="viewport"' not in body:
            body = VIEWPORT + body
        with open(os.path.join(dst, f), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(body)
        n += 1

    btns, panes = [], []
    prev_g = None
    for key, label, src, grp in ROVER_TABS:
        live = bool(src) and os.path.exists(os.path.join(ROVER, src))
        cls = "tab g-" + grp + ("" if live else " tab-off")
        if prev_g is not None and grp != prev_g:
            cls += " gap"
        prev_g = grp
        if key == ROVER_DEFAULT: cls += " on"
        btns.append('  <button class="%s" data-k="%s"%s>%s</button>'
                    % (cls, key, "" if live else ' title="поки порожньо"', label))
        if live:
            on = " on" if key == ROVER_DEFAULT else ""
            panes.append('<div class="pane%s" id="p-%s" data-src="%s"></div>' % (on, key, src))
        else:
            t, d = ROVER_STUB.get(key, (label, ""))
            on = " on" if key == ROVER_DEFAULT else ""
            panes.append('<div class="pane%s" id="p-%s"><div class="stub">'
                         '<div class="st">%s</div><div class="sd">%s</div>'
                         '<div class="sn">поки порожньо</div></div></div>' % (on, key, t, d))

    page = (ROVER_SHELL
            .replace("__BTNS__", "\n".join(btns))
            .replace("__PANES__", "\n".join(panes))
            .replace("__DEF__", ROVER_DEFAULT)
            .replace("__STAMP__", stamp))
    with open(os.path.join(dst, "index.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)
    return n


NOCACHE = ('<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\n'
           '<meta http-equiv="Pragma" content="no-cache">\n'
           '<meta http-equiv="Expires" content="0">\n')

ROVER_SHELL = """<!doctype html>
<html lang="uk"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<title>Ровер</title>
<style>
  :root{--bg:#14171a;--bar:#1b1f23;--line:#2c3339;--txt:#e6ebef;--dim:#93a1ab;--acc:#7fb3d5}
  *{box-sizing:border-box}
  body{background:var(--bg);color:var(--txt);margin:0;
       font:15px/1.6 "Segoe UI",system-ui,sans-serif}
  header{position:sticky;top:0;z-index:5;background:var(--bar);
         border-bottom:1px solid var(--line)}
  .hin{max-width:1120px;margin:0 auto;padding:12px 18px 0;
       display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
  .brand{font-size:17px;font-weight:600}
  .home{color:var(--dim);text-decoration:none;font-size:13px}
  .home:hover{color:var(--acc)}
  nav{max-width:1120px;margin:0 auto;padding:6px 18px 10px;display:flex;
      flex-wrap:wrap;gap:4px}
  .tab{flex:0 0 auto;background:transparent;border:1px solid var(--line);border-radius:0;
       color:var(--dim);font:inherit;font-size:12.5px;line-height:1.3;padding:5px 10px;
       cursor:pointer;white-space:nowrap;transition:border-color .12s,color .12s}
  .tab.g-app{border-color:#2e3f4c;color:#8fa6b8}
  .tab.g-node{border-color:#2c4030;color:#93b493}
  .tab.g-brd{border-color:#43352a;color:#bda07f}
  .tab.g-app:hover{border-color:#7fb3d5;color:#dbe7f0}
  .tab.g-node:hover{border-color:#8fd18b;color:#dff0dd}
  .tab.g-brd:hover{border-color:#d18b47;color:#f0e0cc}
  .tab.g-app.on{border-color:#7fb3d5;color:#eaf3fa;background:#1b2833}
  .tab.g-node.on{border-color:#8fd18b;color:#e9f7e7;background:#1a2a1e}
  .tab.g-brd.on{border-color:#d18b47;color:#fbeedd;background:#2c2219}
  .tab.gap{margin-left:14px}
  .tab-off{opacity:.5}
  main{max-width:1120px;margin:0 auto}
  .pane{display:none}
  .pane.on{display:block}
  iframe{display:block;width:100%;border:0;min-height:70vh}
  .stub{padding:90px 24px;text-align:center}
  .st{font-size:22px;font-weight:600;margin-bottom:8px}
  .sd{color:var(--dim);max-width:52ch;margin:0 auto 18px}
  .sn{display:inline-block;font-size:12px;color:var(--dim);
      border:1px solid var(--line);border-radius:20px;padding:4px 14px}
  @media (max-width:520px){
    .hin{padding:10px 12px 0}
    nav{padding:6px 10px 9px;gap:3px;flex-wrap:nowrap;overflow-x:auto;
        -webkit-overflow-scrolling:touch;scrollbar-width:none}
    nav::-webkit-scrollbar{display:none}
    .tab{font-size:12px;padding:5px 9px}
    .tab.gap{margin-left:9px}
    .stub{padding:56px 16px}
    .st{font-size:19px}
  }
</style></head><body>
<header>
  <div class="hin"><span class="brand">Ровер</span>
    <a class="home" href="../">← Конструктор ідей</a></div>
  <nav>
__BTNS__
  </nav>
</header>
<main>
__PANES__
</main>
<script>
var DEF="__DEF__";
function load(p){
  if(p.dataset.src && !p.firstChild){
    var f=document.createElement("iframe");
    var u=p.dataset.src+(p.dataset.src.indexOf("?")<0?"?":"&")+"v=__STAMP__&t="+Date.now();
    f.src=u; f.setAttribute("scrolling","no");
    f.onload=function(){
      try{
        var d=f.contentDocument;
        var fit=function(){f.style.height=d.documentElement.scrollHeight+"px";};
        fit(); setTimeout(fit,120);
        if(window.ResizeObserver) new ResizeObserver(fit).observe(d.body);
      }catch(e){f.style.height="1600px";}
    };
    p.appendChild(f);
  }
}
function show(k){
  var t=document.querySelector('.tab[data-k="'+k+'"]');
  var p=document.getElementById("p-"+k);
  if(!t||!p) return show(DEF);
  document.querySelectorAll(".tab").forEach(function(x){x.classList.toggle("on",x===t);});
  document.querySelectorAll(".pane").forEach(function(x){x.classList.toggle("on",x===p);});
  load(p);
  try{if(location.hash.slice(1)!==k) history.replaceState(null,"","#"+k);}catch(e){}
}
document.querySelectorAll(".tab").forEach(function(t){
  t.addEventListener("click",function(){show(t.dataset.k);});
});
window.addEventListener("hashchange",function(){show(location.hash.slice(1)||DEF);});
show(location.hash.slice(1)||DEF);
</script>
</body></html>
"""


def build(out_dir):
    inv, desc = parse_inventory(), parse_desc()
    have_pic = set()
    if os.path.isdir(PICDIR):
        have_pic = {f.rsplit(".", 1)[0]: f for f in os.listdir(PICDIR)
                    if f.endswith((".jpg", ".png", ".webp")) and os.path.getsize(
                        os.path.join(PICDIR, f)) > 900}
    cards, by_hash = collect_cards(inv, desc, have_pic)
    answers = parse_answers()
    kinds = parse_kinds()
    bad = [(a['name'], h) for a in answers for h in a['parts'] if h not in by_hash]
    qty = {c["name"]: c["qty"] for c in cards}

    ideas, missing = [], []
    for i in parse_ideas():
        parts = []
        for h in i["parts"]:
            name = by_hash.get(h)
            if not name:
                missing.append((i["name"], h))
                continue
            parts.append({"name": name, "have": str(qty.get(name, "0")) != "0"})
        seen, uniq = set(), []
        for p in parts:
            if p["name"] not in seen:
                seen.add(p["name"])
                uniq.append(p)
        ideas.append({"name": i["name"], "what": i["what"], "parts": uniq})

    tech = {h: it["tech"] for h, it in inv.items()}
    what = {h: (desc.get(h) or {}).get("what", "") for h in inv}
    for a in answers:
        a["names"] = [by_hash[h] for h in a["parts"] if h in by_hash]
        a["src"] = [{"id": h, "tech": tech.get(h, ""), "what": what.get(h, ""),
                     "pic": have_pic.get(h, "")}
                    for h in a["parts"] if h in tech]
    if bad:
        print("BAD HASH IN ANSWERS:", bad)

    page = """<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Конструктор ідей</title>
<meta name="description" content="Деталі й те, на що кожна здатна.">
<style>%s</style>
</head>
<body>
<div class="wrap">

<script>try{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t;}catch(e){}</script>
<div class="bar">
  <div class="barmain">
    <button class="switch sq home hide" id="home" title="На головну (обране збережеться)">
      <svg viewBox="0 0 24 24"><path d="M3 11l9-8 9 8M5 10v10h5v-6h4v6h5V10"/></svg></button>
    <h1 id="ttl"></h1>
    <p class="lede" id="hero"></p>
  </div>
  <div class="searchbox" id="sb">
    <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M16.5 16.5L21 21"/></svg>
    <input id="q" class="search" type="search" spellcheck="false" autocomplete="off">
  </div>
  <div class="navbtns">
    <button class="switch sq" id="rst" title="Почати спочатку: стерти все обране">
      <svg viewBox="0 0 24 24"><path d="M3 5a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1zM17 6h3a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1h-8v2M11 14a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-5a1 1 0 0 1 1-1z"/></svg></button>
    <button class="switch sq" id="ex" title="Приклади">
      <svg viewBox="0 0 24 24"><path d="M9 18h6M10 21h4M12 3a6 6 0 00-3.5 10.9c.5.4.8 1 .8 1.6h5.4c0-.6.3-1.2.8-1.6A6 6 0 0012 3z"/></svg></button>
    <button class="switch sq" id="cat" title="Каталог">
      <svg viewBox="0 0 24 24"><path d="M4 6h6v6H4zM14 6h6v6h-6zM4 14h6v4H4zM14 14h6v4h-6z"/></svg></button>
    <button class="switch sq" id="thm" title="Темна тема"></button>
  </div>
</div>

<div class="stage hide" id="stage">
  <div class="top" id="top"></div>
  <div class="bottom">
    <div class="tabs" id="tabs"></div>
    <div class="pane">
      <div class="plist" id="plist"></div>
      <div class="info" id="info"></div>
      <div class="legend" id="legend"></div>
    </div>
  </div>
</div>

<div class="modal hide" id="modal"><div class="mbox" id="mbox"></div></div>

<div class="scroll" id="scroll">
  <p class="lede" id="hero"></p>
<label class="eng hide" id="eng"><input type="checkbox" id="engbox"> показати інженерні деталі</label>
  <div class="tiles" id="tiles"></div>
  <div id="list"></div>
</div>

</div>
<script>%s</script>
</body>
</html>
""" % (CSS,
       JS.replace("__ANSWERS__", json.dumps(answers, ensure_ascii=False))
         .replace("__KINDS__", json.dumps(kinds, ensure_ascii=False))
         .replace("__IDEAS__", json.dumps(ideas, ensure_ascii=False))
         .replace("__DATA__", json.dumps(cards, ensure_ascii=False))
         .replace("__THEMES__", json.dumps(THEMES, ensure_ascii=False))
         .replace("__ICONS__", json.dumps(ICONS, ensure_ascii=False))
         .replace("__PICS__", json.dumps(PICS, ensure_ascii=False))
         .replace("__RECIPES__", json.dumps(parse_recipes(), ensure_ascii=False))
         # мініатюри з файлів pics/ (для Pages цього досить); --embed вбудовує їх у сторінку
         .replace("__PICDATA__", json.dumps(pic_data() if "--embed" in sys.argv else {}))
         .replace("__BUILT__", json.dumps(__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"))))

    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w",
              encoding="utf-8", newline="\n") as f:
        f.write(page)
    open(os.path.join(out_dir, ".nojekyll"), "w").close()

    src_pics = os.path.join(CAT, "pics")
    n_pics = 0
    if os.path.isdir(src_pics):
        dst = os.path.join(out_dir, "pics")
        os.makedirs(dst, exist_ok=True)
        for f in os.listdir(src_pics):
            if f.lower().endswith((".jpg", ".png", ".webp")):
                path = os.path.join(src_pics, f)
                if os.path.getsize(path) > 512:
                    shutil.copy2(path, os.path.join(dst, f))
                    n_pics += 1

    n_rover = copy_rover(out_dir)

    print("pics %d | rover %d | answers %d | ideas %d | cards %d | parts %d"
          % (n_pics, n_rover, len(answers), len(ideas), len(cards), len(inv)))
    if bad: return 1
    gaps = [(i["name"], p["name"]) for i in ideas for p in i["parts"] if not p["have"]]
    if gaps:
        print("nema:", len(gaps))
    if missing:
        print("BAD HASH:", missing)
        return 1
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="_site")
    sys.exit(build(ap.parse_args().out))
