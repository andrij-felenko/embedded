#!/usr/bin/env python3
"""Тягне мініатюри товарів з arduino.ua у catalog/pics/<hash>.<jpg|png|webp>

Карта «хеш -> productID» лежить у catalog/shop_ids.txt.
Темп: одна дія на 4 секунди, як домовлено.
Уже завантажене не перезавантажується — скрипт можна перезапускати.

Головне фото береться з <meta property="og:image"> — це те, що сайт сам
вважає фото товару. Далі — картинки з кодом самого товару («код: ABC123»),
і лише потім будь-які інші. Старі товари мають фото у .webp або з
описовими іменами, тож обмежуватись jpg/png не можна.

Що звідки взято, пишеться в catalog/pics/_source.txt (хеш, ID, код, файл) —
щоб потім можна було перевірити, чи фото від того товару.
"""
import io
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, "catalog", "shop_ids.txt")
OUT = os.path.join(ROOT, "catalog", "pics")
SRC = os.path.join(OUT, "_source.txt")
PAUSE = 4
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
EXTS = (".jpg", ".png", ".webp")

OG = re.compile(r'<meta property="og:image" content="[^"]*products_pictures/([^"]+)"')
IMG = re.compile(r"products_pictures/((?:small|medium|large)_([A-Za-z]{3}\d{3})"
                 r"(?:[-_]\d+)?\.(?:jpg|png|webp))")
CODE = re.compile(r"код:\s*([A-Za-z]{3}\d{3})")


def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def ext_of(data):
    if data[1:4] == b"PNG":
        return ".png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    return ".jpg"


def variants(fname):
    """small -> medium -> як є: менше байтів, але без порожніх відповідей."""
    base = re.sub(r"^(small|medium|large)_", "", fname)
    out = []
    for size in ("small_", "medium_"):
        if size + base not in out:
            out.append(size + base)
    if fname not in out:
        out.append(fname)
    return out


def fetch_pic(fname):
    for name in variants(fname):
        try:
            data = get("https://arduino.ua/products_pictures/" + name, binary=True)
        except Exception:
            data = b""
        time.sleep(PAUSE)
        if len(data) > 900:
            return name, data
    return None, b""


def main():
    global OUT, SRC
    # --out DIR: качати в іншу папку (напр. для повного перекачування і порівняння)
    if len(sys.argv) > 2 and sys.argv[1] == "--out":
        OUT = os.path.abspath(sys.argv[2])
        SRC = os.path.join(OUT, "_source.txt")
    os.makedirs(OUT, exist_ok=True)
    pairs = []
    for line in io.open(MAP, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        h, pid = line.split()
        pairs.append((h, pid))

    src = io.open(SRC, "a", encoding="utf-8")
    done = miss = skip = 0
    for h, pid in pairs:
        exist = [os.path.join(OUT, h + e) for e in EXTS]
        if any(os.path.exists(x) and os.path.getsize(x) > 900 for x in exist):
            skip += 1
            continue
        try:
            page = get("https://arduino.ua/index.php?productID=" + pid)
        except Exception as e:
            print("page fail", h, pid, e, flush=True)
            miss += 1
            time.sleep(PAUSE)
            continue
        time.sleep(PAUSE)

        m = CODE.search(page)
        own = (m.group(1) if m else "").lower()
        og = OG.search(page)
        hits = IMG.findall(page)
        cands = []
        if og:
            cands.append(og.group(1))
        cands += [f for f, c in hits if own and c.lower() == own]
        cands += [f for f, c in hits]
        seen, order = set(), []
        for f in cands:
            if f not in seen:
                seen.add(f)
                order.append(f)

        got = False
        for fname in order[:3]:
            name, data = fetch_pic(fname)
            if data:
                dst = os.path.join(OUT, h + ext_of(data))
                open(dst, "wb").write(data)
                src.write("%s\t%s\t%s\t%s\t%s\n" % (h, pid, own, name,
                                                    "og" if og and fname == og.group(1)
                                                    else "code" if own and own in fname.lower()
                                                    else "any"))
                src.flush()
                done += 1
                got = True
                print("ok", h, name, len(data), flush=True)
                break
        if not got:
            miss += 1
            print("no image", h, pid, own, flush=True)

    src.close()
    print("done=%d miss=%d skip=%d total=%d" % (done, miss, skip, len(pairs)), flush=True)


if __name__ == "__main__":
    sys.exit(main())
