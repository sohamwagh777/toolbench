"""Toolbench build: assemble exactly 100 tool pages + landing (101 HTML) into ../out.

Sources:
(a) ported self-contained pages from ~/.hermes/cache/scratch/htmltools (copied verbatim)
(b) spec tools in tools_text/dev + tools_extra_a/b/c, rendered through shell.py

Run: python3 gen_tools.py
"""
import os, sys, json, shutil, glob

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from shell import render_page, render_landing
from gen_helpers import CAT_ACCENTS

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "out")
SCRATCH = os.path.expanduser("~/.hermes/cache/scratch/htmltools")

from desc_map import M as DESCMAP

# skip ported near-dupes and the weaker duplicate specs so we land on exactly 100 tools
SKIP_PORTED = {"emoji_picker_with_built_in_search_list.html"}          # duplicate of hyphen twin
SKIP_SPEC = {"word-counter", "slug-generator", "regex-tester", "uuid-generator",   # same tool, ported version wins
             "cron-explainer", "fraction-calc", "emi-lite", "percentage-lab",      # stronger ported twins
             "pomodoro2", "habit-tracker", "stopwatch2", "water-tracker",          # duplicate ported timers/trackers
             "sleep-planner", "pomodoro-log", "recipe-scaler", "donation-split",
             "random-words",   # weakest/derivative
             "bmi-history", "expense-tracker", "calendar-gen", "pomodoro-timer2"}

def collect_specs():
    from tools_text import TOOLS as T1
    from tools_dev import TOOLS as T2
    from tools_extra_a import TOOLS as A
    from tools_extra_b import TOOLS as B
    from tools_extra_c import TOOLS as C
    out, seen = [], set()
    for t in T1 + T2 + A + B + C:
        if t["id"] in SKIP_SPEC or t["id"] in seen:
            continue
        seen.add(t["id"])
        if t["id"] in DESCMAP:                     # authoritative title/desc/howto
            cat, title, desc, howto = DESCMAP[t["id"]]
            t["cat"], t["title"], t["desc"], t["howto"] = cat, title, desc, howto
        out.append(t)
    return out

def cat_of(name):
    low = name.lower()
    for cat, keys in [("Encoding & Hashing", ["base64", "base-converter", "morse", "morse-code", "cipher", "hash", "fnv", "barcode"]),
                     ("Developer", ["regex", "json", "curl", "yaml", "env", "markdown", "js-scratch", "minifier", "subnet", "ipv4", "ipv6", "jwt", "batch-string", "csv"]),
                     ("Color", ["color-converter", "gradient", "contrast", "pixel", "draw", "shape", "flexbox", "grid-layout"]),
                     ("Math & Finance", ["calculator", "calc", "fraction", "simplifier", "equation", "percentage"]),
                     ("Time & Productivity", ["timer", "stopwatch", "pomodoro", "countdown", "tracker", "todo", "flashcard", "history", "clock", "emoji"]),
                     ("Text", ["counter", "generator", "replacer", "replacer", "preview", "translator", "picker", "slug", "checker", "scanner"]),
                     ]:
        if any(k in low for k in keys):
            return cat
    if any(k in low for k in ["game", "puzzle", "minesweeper", "simon", "hangman", "guess", "flip", "dice", "wheel", "maze"]):
        return "Games & Play"
    if any(k in low for k in ["converter", "codec", "conversion", "base64"]):
        return "Encoding & Hashing"
    return "Misc"

def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    tdir = os.path.join(OUT, "tools")
    os.makedirs(tdir)
    # (a) ported
    ported = []
    for src in sorted(glob.glob(os.path.join(SCRATCH, "*.html"))):
        fn = os.path.basename(src)
        if fn.startswith("test_tool") or fn in SKIP_PORTED:
            continue
        with open(src, encoding="utf-8") as fh:
            html = fh.read()
        if len(html) < 1500:
            continue
        shutil.copyfile(src, os.path.join(tdir, fn))
        ported.append(fn[:-5])
    # (b) rendered from specs
    specs = collect_specs()
    assert not (set(ported) & {t["id"] for t in specs}), "duplicate id between ported and specs"
    total = ported + [t["id"] for t in specs]
    tools = [{"id": i, "cat": cat_of(i), "title": i.replace("-", " ").replace("_", " ").title(),
              "desc": "Standalone offline utility.", "body": None} for i in ported]
    for t in specs:
        html = render_page(t, CAT_ACCENTS.get(t["cat"], "#d8a25e"))
        with open(os.path.join(tdir, t["id"] + ".html"), "w", encoding="utf-8") as f:
            f.write(html)
    # landing needs real dicts for ported too (title/desc read by render_landing)
    for t in tools:
        if t["id"] in DESCMAP:
            cat, title, desc, howto = DESCMAP[t["id"]]
            t["cat"], t["title"], t["desc"] = cat, title, desc
    landing_tools = tools + [{"id": t["id"], "cat": t["cat"], "title": t["title"], "desc": t["desc"]} for t in specs]
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_landing(landing_tools, CAT_ACCENTS, "Built Oct 2026"))
    print("ported=%d rendered=%d TOTAL=%d (+landing)" % (len(ported), len(specs), len(total)))
    assert len(set(total)) == len(total), "dup ids"
    return total

if __name__ == "__main__":
    total = build()
    assert len(total) == 100, "expected 100 tools, got %d" % len(total)
    n = len(glob.glob(os.path.join(OUT, "**", "*.html"), recursive=True))
    print("html files on disk (incl landing):", n)
    manifest = {"count": len(total), "tools": sorted(total)}
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    print("OK")
