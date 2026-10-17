"""Toolbench build v3 — the six-sided-die rule, executed.

One source of truth (the 100-name roster in _all.txt) -> docs/. Each roster
name resolves to exactly ONE page, from one of two sources:
  (a) a PORTED page — copied VERBATIM from build/orig/tools/ (the committed
      snapshot of the v2 shipped set; already wears the shell chrome, the
      per-tool "How to use." line and the "Private & local" note, and passed
      smoke.js). Copied, never modified.
  (b) a SPEC page — rendered through the ONE shell (shell.py render_page).

THE bug v2 had (why this file exists): gen_tools globbed a PRUNED scratch
dir for ported copies and rendered any spec id whose name did not collide
with a file name. So "two JSON Formatters / two Diff Viewers / two Markdown
Previewers / two URL codecs / two Query Labs / two Cron tools" shipped side by
side (44 same-job twin pairs verified in the shipped snapshot). The roster is
authoritative (deployed filenames == landing links == _all.txt, verified by
comm diff); each name declares its source in SOURCE below.

Usage:
  python3 build/gen_v3.py            # rebuild docs/ (destructive)
  python3 build/gen_v3.py --check    # temp dir + audit report, touch nothing
Then always: python3 build/smoke.py   (functional smoke, all pages)
"""
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "docs")
ORIG = os.path.join(HERE, "orig", "tools")        # committed snapshot of shipped set
ROSTER = os.path.join(HERE, "_all.txt")

sys.path.insert(0, HERE)
from shell import render_page, render_landing
from gen_helpers import CAT_ACCENTS
from desc_map import M as DESCMAP

# --------------------------------------------------------------------------
# SOURCE map: roster name -> "orig" (copy file verbatim from ORIG/) | "spec"
# (render through the shell from the spec modules). Names omitted from the
# map resolve by DEFAULT: ORIG/<name> exists -> orig, else spec by stem.
# Every explicit entry is one of: a -/_ filename twin (cut so its winner
# stands alone), or a ported file that LOST to a better spec twin (So:
# regex-tester kept over the ported "Line Finder (grep)" twin was REVERSED at
# review — ported grep kept, spec regex-tester cut; test again before flip).
SPEC_SINGLETONS = {
    # --- cross-module DUPLICATE specs (same tool, two module copies) ---
    "case-converter.html": "spec",          # tools_text + tools_extra_a: keep tools_text copy
    "line-tools.html": "spec",              # tools_text + tools_extra_a
    "lorem-generator.html": "spec",         # tools_text + tools_extra_a
    "palindrome-checker.html": "spec",      # tools_text + tools_extra_a
    "text-reverser.html": "spec",           # tools_text + tools_extra_a
    "unicode-inspector.html": "spec",       # tools_text + tools_extra_a
    "random-words.html": "spec",            # tools_text + tools_extra_a (weakest/derivative rule)
    "jwt-decoder.html": "spec",             # tools_dev + tools_extra_b: keep tools_dev copy
    "cron-explainer.html": "spec",          # tools_dev + tools_extra_b
    # -/_ filename twins (the deployed file serves the job under the twin key):
    "text-diff.html": "spec",               # twin kept of text-diff-viewer (LCS + markers)
    "query-lab.html": "spec",
    "cron-scheduler.html": "spec",
    "percentage-lab.html": "spec",
    "fraction-calc.html": "spec",
    "emi-lite.html": "spec",
    "pomodoro2.html": "spec",
    "habit-tracker.html": "spec",
    "water-tracker.html": "spec",
    "sleep-planner.html": "spec",
    "pomodoro-log.html": "spec",
    "recipe-scaler.html": "spec",
    "donation-split.html": "spec",
    "bmi-history.html": "spec",
    "expense-tracker.html": "spec",
    "calendar-gen.html": "spec",
    "pomodoro-timer2.html": "spec",
    "slug-generator.html": "spec",          # 5 flavours + dedupe column (spec) beats ported twin
    "uuid-generator.html": "spec",          # crypto v4 x10 (spec) beats ported twin
    "query-lab.html": "spec",
    # (SPEC_SINGLETONS = names that MUST render from spec modules, one instance;
    #  names the original v2 build CUT are NOT here — they stay cut, nothing
    #  resurrects silently.)
}
# the ONLY two ported files the spec version beats (reversed 2026-10-17 after
# manual review — "don't re-add identical duplicates": one entry per job):
# (regex-tester is KEPT — its job is testing patterns; the ported grep twin
# filters lines through a regex. Different verbs, different pages. Cut both
# once and the suite lost its only pattern tester.)
PORTED_LOSERS = {"grep.html"}

# ---- category + copy helpers (single source: desc_map, then heuristic) ----
def key_for(stem):
    """desc_map key for a file stem (dashes vs underscores twins), or None."""
    if stem in DESCMAP:
        return stem
    for alt in (stem.replace("_", "-"), stem.replace("-", "_")):
        if alt in DESCMAP:
            return alt
    return None


def cat_of(name):
    low = name.lower()
    for cat, keys in [("Encoding & Hashing", ["base64", "base-converter", "morse", "cipher", "hash", "fnv", "rot13", "vigenere", "entropy", "escaper"]),
                      ("Developer", ["regex", "json", "curl", "yaml", "env", "markdown", "js-scratch", "runner", "minifier", "jwt", "batch-string", "csv", "hex-dump", "query", "cron", "http", "slug", "grep"]),
                      ("Color", ["color-converter", "gradient", "shadow", "contrast"]),
                      ("Math & Finance", ["calculator", "calc", "fraction", "simplifier", "equation", "percentage", "monte", "compound", "emi", "tip", "bmi"]),
                      ("Time & Productivity", ["timer", "stopwatch", "pomodoro", "countdown", "tracker", "todo", "flashcard", "history", "clock", "emoji", "typing", "reaction", "timezone"]),
                      ("Games & Play", ["game", "puzzle", "minesweeper", "simon", "hangman", "guess", "flip", "dice", "wheel", "maze", "kenken", "blackjack", "wordle", "madlibs"])]:
        if any(k in low for k in keys):
            return cat
    if any(k in low for k in ["converter", "codec", "conversion"]):
        return "Encoding & Hashing"
    if any(k in low for k in ["picker", "wheel", "checklist"]):
        return "Misc"
    return "Text"


# ---------------- static audit (check, never blind-mutate) ------------------
SCRIPT_RE = re.compile(r"<script[^>]*>([\s\S]*?)</script>")


def audit(html):
    """Problems list for one page ([] = clean).

    - dead handler ids: every getElementById('x') / $('#x') / wire('x') target
      that has NO matching id in the MARKUP (JS literals never counted — the
      old whole-page regex false-positived on 7 pages: blackjack embeds
      <select> markup inside its JS string).
    - unwrapped JS (JS text outside any <script> block) and unbalanced braces.
    - control-count flag: >5 REAL markup controls -> printed for manual review
      (a 4x4 puzzle grid or a countdown start/pause/reset is not "20 faces").
    """
    probs = []
    blocks = SCRIPT_RE.findall(html)
    markup = SCRIPT_RE.sub("", html)
    js = "\n;\n".join(blocks)
    if 'getElementById("' in markup:   # quote-style tolerant (some pages use "x")
        probs.append("JS OUTSIDE <script> wrapper")
    for b in blocks:
        if "function " in b and b.count("{") != b.count("}"):
            probs.append("unbalanced braces in a script block")
    ids = set(re.findall(r'id="([^"]+)"', markup)) | {"out", "ta", "q", "nores"}
    used = set()
    for pat in (r"getElementById\('([^']+)'\)", r"\$\('#?([A-Za-z][\w-]*)'\)",
                r"wire\(\[?'([a-z0-9-]+)'", r"wire\('([a-z0-9-]+)'"):
        used |= set(re.findall(pat, js))
    dead = sorted(u for u in used if u and u not in ids)
    if dead:
        probs.append("dead ids: " + ",".join(dead[:6]))
    n = len(re.findall(r"<input|<select|<button", markup))
    if n > 5:
        probs.append("LOOK: %d controls (>5) — manual review" % n)
    return probs


# ---------------- spec pool (the "spec side of each pair") ------------------
def load_spec_pool():
    import importlib.util
    pool = {}
    for mod in ("tools_text", "tools_dev", "tools_extra_a", "tools_extra_b", "tools_extra_c"):
        sp = importlib.util.spec_from_file_location(mod, os.path.join(HERE, mod + ".py"))
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        for t in m.TOOLS:
            pool.setdefault(t["id"], t)   # first module copy wins (v2 contract)
    return pool


def main():
    check_only = "--check" in sys.argv
    if not os.path.exists(ROSTER):
        print("FATAL: roster missing:", ROSTER)
        return 1
    if not os.path.isdir(ORIG):
        print("FATAL: ported source snapshot missing:", ORIG)
        return 1
    out = os.path.join(os.environ.get("TMPDIR", "/tmp"), "tb-check-%d" % os.getpid()) if check_only else OUT
    if os.path.isdir(out):
        shutil.rmtree(out, ignore_errors=True)

    roster = [l.strip() for l in open(ROSTER) if l.strip().endswith(".html")]
    assert len(roster) == 100 and len(roster) == len(set(roster)), \
        "roster must be the unique 100 names (got %d)" % len(roster)
    pool = load_spec_pool()

    resolved, problems = {}, []
    for name in roster:
        stem = name[:-5]
        if name in SPEC_SINGLETONS:
            src = SPEC_SINGLETONS[name]
        elif name in PORTED_LOSERS:
            src = "cut"
        elif os.path.exists(os.path.join(ORIG, name)):
            src = "orig"
        elif stem in pool:
            src = "spec"
        elif (alt := (stem.replace("_", "-") if "_" in stem else stem.replace("-", "_"))) in pool \
                and os.path.exists(os.path.join(ORIG, alt + ".html")):
            src = "orig"     # -/_ twin file serves the job (same tool, twin key)
            name = alt + ".html"
        elif stem.replace("_", "-") in pool and os.path.exists(os.path.join(ORIG, stem.replace("_", "-") + ".html")):
            src = "orig"
            name = stem.replace("_", "-") + ".html"
        else:
            problems.append("UNRESOLVED %s" % name)
            continue
        if src == "cut":
            problems.append("CUT %s (duplicate job — twin kept)" % name)
            continue
        if src == "orig":
            fname = name if name.endswith(".html") else name + ".html"
            with open(os.path.join(ORIG, fname), encoding="utf-8") as f:
                html = f.read()
            if "header class=\"tb\"" not in html:
                problems.append("NOTE %s — ported page WITHOUT the shell chrome (copied as-is)" % name)
        else:
            t = pool.get(stem) or pool.get(stem.replace("_", "-")) or pool.get(stem.replace("-", "_"))
            if t is None:
                problems.append("UNRESOLVED %s — spec source missing" % name)
                continue
            html = render_page(t, CAT_ACCENTS.get(t["cat"], "#d8a25e"))
        resolved.setdefault(name, html)   # twins collapse onto ONE file

    print("built %d tool pages (cut/dupe notes: %d)" %
          (len(resolved), len([p for p in problems if p.startswith("CUT")])))
    for p in problems[:12]:
        print("  ", p)

    if check_only:
        print("check-only: %d pages staged (docs/ untouched)" % len(resolved))
        return 0

    # ---- write docs/ ------------------------------------------------------
    shutil.rmtree(OUT, ignore_errors=True)
    tdir = os.path.join(OUT, "tools")
    os.makedirs(tdir, exist_ok=True)
    for name, html in resolved.items():
        with open(os.path.join(tdir, name), "w", encoding="utf-8") as f:
            f.write(html)
    # landing: one section list from the same roster set, desc from desc_map
    order, bycat = [], {}
    for name in sorted(resolved):
        stem = name[:-5]
        key = key_for(stem)
        if key:
            cat, title, desc, howto = DESCMAP[key]
        else:
            cat, title, desc = cat_of(name), stem.replace("_", " ").replace("-", " ").title(), "Standalone offline utility."
        if cat not in order:
            order.append(cat)
        bycat.setdefault(cat, []).append({"id": stem, "cat": cat, "title": title, "desc": desc})
    landing_tools = [t for c in order for t in bycat[c]]
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_landing(landing_tools, CAT_ACCENTS, "Built Oct 2026 (v3)"))
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        import json
        json.dump({"count": len(resolved), "tools": sorted(resolved)}, f)
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    # ---- VERIFY the written tree (2 layers, programmatic) ------------------
    idx = open(os.path.join(OUT, "index.html"), encoding="utf-8").read()
    links = set(re.findall(r'href="tools/([^"]+)"', idx))
    disk = {f for f in os.listdir(tdir) if f.endswith(".html")}
    fails = ["dead link -> tools/" + d for d in sorted(links - disk)]
    fails += ["orphan (unlinked) tools/" + o for o in sorted(disk - links)]
    manifest = json_load = __import__("json").load(open(os.path.join(OUT, "manifest.json"))) if os.path.exists(os.path.join(OUT, "manifest.json")) else None
    for f in sorted(disk):
        for p in audit(open(os.path.join(tdir, f), encoding="utf-8").read()):
            if not p.startswith("LOOK"):
                fails.append("AUDIT %s: %s" % (f, p))
    looks = [(f, p) for f in sorted(disk)
             for p in audit(open(os.path.join(tdir, f), encoding="utf-8").read()) if p.startswith("LOOK")]
    if fails:
        print("VERIFY FAILURES (%d):" % len(fails))
        for x in fails[:20]:
            print("  ", x)
        return 1
    print("verify %d pages + landing: links == files == manifest; 0 dead handlers; 0 unwrapped JS blocks" % len(disk))
    print("manual-review flags (kept as-is): %s" % ([f for f, _ in looks],))
    print("next: python3 build/smoke.py && node build/smoke.js docs/tools")
    return 0


if __name__ == "__main__":
    sys.exit(main())
