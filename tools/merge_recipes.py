#!/usr/bin/env python3
"""Зливає рецепти з catalog/proposals/recipes2_*.md у catalog/recipes.md.

Бере лише блоки, у яких кожен складник — назва вміння з answers.md або назва рецепту
(наявного чи з цієї ж порції), ключ і назва не повторюють наявні. Рядки «потрібно нове:»
відкидає разом із блоком. Друкує, що і чому відкинуто.
"""
import io
import os
import re
import sys
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = os.path.join(ROOT, "catalog")
PROP = os.path.join(CAT, "proposals")
HEAD_RE = re.compile(r"^\[([^\]]+)\]\s+(.+)$")


def rd(p):
    return io.open(p, encoding="utf-8").read()


def blocks_of(text):
    """[(ключ, назва, [рядки блоку], заголовок розділу)]"""
    out, cur, section = [], None, ""
    for ln in text.split("\n"):
        if ln.startswith("## "):
            section = ln[3:].strip()
            if cur:
                out.append(cur); cur = None
            continue
        m = HEAD_RE.match(ln)
        if m:
            if cur:
                out.append(cur)
            cur = [m.group(1).strip(), m.group(2).strip(), [ln], section]
        elif cur is not None:
            if ln.strip() == "" and cur[2] and cur[2][-1].strip() == "":
                continue
            cur[2].append(ln)
    if cur:
        out.append(cur)
    for b in out:
        while b[2] and not b[2][-1].strip():
            b[2].pop()
    return out


def ingredients(lines):
    for ln in lines:
        if ln.startswith("з:"):
            return [[a.strip() for a in ing.split("|") if a.strip()] for ing in ln[2:].split("·")]
    return None


def main():
    abilities = set(re.findall(r"^\[[\w'/-]+\]\s+(.+)$", rd(os.path.join(CAT, "answers.md")), re.M))
    rec_text = rd(os.path.join(CAT, "recipes.md"))
    existing = blocks_of(rec_text)
    keys = {b[0] for b in existing}
    names = {b[1] for b in existing}
    files = sorted(f for f in os.listdir(PROP) if f.startswith("recipes2_") and f.endswith(".md"))
    if not files:
        print("нема файлів recipes2_*.md"); return 1
    accepted, rejected = [], collections.Counter()
    pending = []
    for f in files:
        for b in blocks_of(rd(os.path.join(PROP, f))):
            b.append(f)
            pending.append(b)
    # назви цієї порції теж можуть бути складниками — але тільки ті, що пройдуть
    cand_names = {b[1] for b in pending}
    known = abilities | names | cand_names
    for key, name, lines, section, f in pending:
        ings = ingredients(lines)
        why = None
        if ings is None or not ings:
            why = "без складників"
        elif any(ln.startswith("потрібно нове:") for ln in lines):
            why = "потрібно нове вміння"
        elif key in keys:
            why = "ключ уже є"
        elif name in names or name in abilities:
            why = "назва вже є"
        elif len(name) > 30:
            why = "назва довша за 30"
        else:
            bad = [a for alts in ings for a in alts if a not in known]
            if bad:
                why = "невідомий складник: " + ", ".join(sorted(set(bad)))
        if why:
            rejected[why.split(":")[0]] += 1
            print("  -", f, "|", name, "|", why)
            continue
        lines = [ln for ln in lines if not ln.startswith("потрібно нове:")]
        accepted.append((key, name, lines, section, f))
        keys.add(key); names.add(name)
    # друга перевірка: складник міг посилатись на відкинутий рецепт цієї порції
    ok_names = abilities | {b[1] for b in existing} | {a[1] for a in accepted}
    final = []
    for key, name, lines, section, f in accepted:
        bad = [a for alts in ingredients(lines) for a in alts if a not in ok_names]
        if bad:
            print("  -", f, "|", name, "| посилається на відкинутий:", ", ".join(bad)); rejected["посилається на відкинутий"] += 1
            continue
        final.append((key, name, lines, section, f))
    if "--dry" in sys.argv:
        print("прийнято б:", len(final), "| відкинуто:", dict(rejected)); return 0
    out = rec_text.rstrip("\n") + "\n"
    cur_sec = None
    for key, name, lines, section, f in final:
        sec = "Ще: " + (section or f)
        if sec != cur_sec:
            out += "\n## " + sec + "\n"
            cur_sec = sec
        out += "\n" + "\n".join(lines) + "\n"
    io.open(os.path.join(CAT, "recipes.md"), "w", encoding="utf-8").write(out)
    total = len(re.findall(r"^\[[^\]]+\]\s+\S", out, re.M))
    print("додано:", len(final), "| відкинуто:", dict(rejected), "| разом рецептів:", total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
