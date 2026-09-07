#!/usr/bin/env python3
"""Лишає в catalog/recipes.md тільки рецепти з catalog/proposals/cut/keep_*.txt.

Розділи (## / ###) зберігаються, порожні прибираються. Якщо обраний рецепт має
складником вилучений рецепт, той повертається (і про це пишеться). --dry: лише звіт.
"""
import glob
import io
import os
import re
import sys
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = os.path.join(ROOT, "catalog")
PATH = os.path.join(CAT, "recipes.md")
CUT = os.path.join(CAT, "proposals", "cut")


def main():
    dry = "--dry" in sys.argv
    keep = set()
    for f in sorted(glob.glob(os.path.join(CUT, "keep_*.txt"))):
        for ln in io.open(f, encoding="utf-8"):
            k = ln.strip().strip("[]").strip()
            if k and not k.startswith("#"):
                keep.add(k)
    text = io.open(PATH, encoding="utf-8").read()
    # розібрати на структуру
    lines = text.split("\n")
    head, items, cur = [], [], None   # items: dict(kind='h2'|'h3'|'block', ...)
    for ln in lines:
        if ln.startswith("## "):
            items.append({"kind": "h2", "text": ln}); cur = None; continue
        if ln.startswith("### "):
            items.append({"kind": "h3", "text": ln}); cur = None; continue
        m = re.match(r"^\[([^\]]+)\]\s+(.+)$", ln)
        if m:
            cur = {"kind": "block", "key": m.group(1), "name": m.group(2).strip(), "lines": [ln]}
            items.append(cur); continue
        if cur is not None:
            if ln.strip():
                cur["lines"].append(ln)
            continue
        if not items:
            head.append(ln)
    blocks = [it for it in items if it["kind"] == "block"]
    by_key = {b["key"]: b for b in blocks}
    by_name = {b["name"]: b for b in blocks}
    unknown = keep - set(by_key)
    if unknown:
        print("невідомі ключі у keep_*:", sorted(unknown))
    keep &= set(by_key)

    def ingredients(b):
        for ln in b["lines"]:
            if ln.startswith("з:"):
                return [a.strip() for ing in ln[2:].split("·") for a in ing.split("|") if a.strip()]
        return []

    # залежності: складник-рецепт має лишитись
    pulled = []
    changed = True
    while changed:
        changed = False
        for k in list(keep):
            for a in ingredients(by_key[k]):
                if a in by_name and by_name[a]["key"] not in keep:
                    keep.add(by_name[a]["key"]); pulled.append((by_key[k]["name"], a)); changed = True
    # звіт по категоріях
    cat = None; per = collections.Counter(); before = collections.Counter()
    for it in items:
        if it["kind"] == "h2":
            cat = it["text"][3:].strip()
        elif it["kind"] == "block":
            before[cat] += 1
            if it["key"] in keep:
                per[cat] += 1
    for c in before:
        print("%-32s %3d -> %2d" % (c, before[c], per[c]))
    print("разом:", sum(before.values()), "->", len(keep), "| повернуто залежностей:", len(pulled))
    for p in pulled:
        print("   ", p[0], "потребує", p[1])
    if dry:
        return 0
    # переписати файл без порожніх розділів
    out = "\n".join(head).rstrip("\n") + "\n"
    i = 0
    while i < len(items):
        it = items[i]
        if it["kind"] in ("h2", "h3"):
            # чи є далі в цьому розділі живі блоки до наступного заголовка того ж або вищого рівня
            j = i + 1; alive = False
            while j < len(items):
                nx = items[j]
                if nx["kind"] == "h2" or (nx["kind"] == "h3" and it["kind"] == "h3"):
                    break
                if nx["kind"] == "block" and nx["key"] in keep:
                    alive = True; break
                j += 1
            if alive:
                out += "\n" + it["text"] + "\n"
        elif it["key"] in keep:
            out += "\n" + "\n".join(it["lines"]) + "\n"
        i += 1
    io.open(PATH, "w", encoding="utf-8").write(out)
    print("записано:", len(keep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
