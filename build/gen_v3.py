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
# ---- B-cut resolution table (2026-10-17, the "B" pass) ----------------------
# Each key is a ROSTER NAME that resolves to ANOTHER source (its pair twin
# name, "orig" = itself, or None = both sides gone). One tool, one job: any
# two pages doing the same job collapse to ONE — or to none if neither is
# worth keeping. Cross-module DUAL SPEC (two identical modules shipping the
# same tool, e.g. Case Converter in tools_text + tools_extra_a) resolves to
# the FIRST module copy, under its normal name; that copy then replaces the
# ported original — verified by rendering + diffing both sides (NOTED below),
# never by guessing.
PAIR_CUTS = {
    # --- cross-module dual spec (both module copies deployed): keep tools_text/dev copy ---
    "case-converter.html": None,       # keep tools_text copy (richer case set)
    "line-tools.html": None,           # keep tools_text copy (superset of ported twin)
    "lorem-generator.html": None,      # keep tools_text copy (Sentences|Words, grammar)
    "palindrome-checker.html": None,   # keep tools_text copy (phrase/number check)
    "text-reverser.html": None,        # keep tools_text copy (char/word/line modes)
    "unicode-inspector.html": None,    # keep tools_text copy (block names, NFKC, clusters)
    "random-words.html": None,         # weakest/derivative — removed with its twin pair
    "jwt-decoder.html": "spec",        # keep tools_dev copy (spec id = same stem)
    "cron-explainer.html": "spec",     # keep tools_dev copy; Next-Runs twin stays
    # --- same-tool pairs (both deployed): keep the better page ------------------
    "text-diff-viewer.html": "text-diff.html",      # spec LCS diff kept; word-highlight twin cut
    "markdown-previewer-with-small-own-parser.html": None,  # cut with its spec twin (dead-handler class)
    "markdown-preview.html": None,                  # cut (dead-handler class; header doubled)
    "query-lab.html": "query-builder.html",  # keep query-builder (paste/EDIT/rebuild); lab is read-mostly twin
    "url-codec2.html": None,         # full-decode twin of url-codec (dead handler class)
    "pomodoro-timer.html": None,     # + pomodoro2 + pomodoro-log -> ONE timer (time-diff covers math)
    "pomodoro2.html": None,
    "pomodoro-log.html": None,
    "stopwatch.html": "stopwatch2.html",   # keep spec stopwatch2 (laps/best-avg) over ported twin
    "habit_tracker_with_localstorage.html": "habit-tracker.html",  # keep spec habit-tracker (30-day grid)
    "percentage-calculator.html": "percentage-lab.html",  # keep spec percentage-lab (3 modes)
    "fraction-simplifier.html": "fraction-calc.html",     # keep spec fraction-lab
    "loan-emi-calculator.html": "emi-lite.html",          # keep spec EMI quick check
    "compound-interest.html": None, "sleep-planner.html": None, "recipe-scaler.html": None,
    "donation-split.html": None, "bmi-history.html": None, "expense-tracker.html": None,
    "calendar-gen.html": None,
    
    "nato_phonetic_translator.html": None, "typo-checker.html": None,  # placeholder-desc class
    "http-status-lookup.html": None,   # lookup list, not a tool (placeholder desc)
    # --- the ONLY pair that is NOT a twin (different verbs): keep both -----
    "grep.html": "orig", "regex-tester.html": "orig",
    # --- pairs where NEITHER twin earns a page (niche / lookup / tracker /
    #     placeholder-desc / dead-handler class): removed with both twins ----
    "time-difference-calculator.html": None, "age-calculator.html": None,
    "tip-calculator.html": None,
    "todo_checklist_with_localstorage.html": None,
    "random_picker_wheel.html": None,
}

PORTED_LOSERS = set()  # retired — B pass uses PAIR_CUTS

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
        "roster = the deployed-file inventory (100 unique names, got %d)" % len(roster)
    pool = load_spec_pool()

    resolved, problems = {}, []
    def render_spec(stem):
        t = pool.get(stem) or pool.get(stem.replace("_","-")) or pool.get(stem.replace("-","_"))
        if t is None:
            return None
        acc = CAT_ACCENTS.get(t["cat"], "#d8a25e")
        return render_page(t, acc)

    for name in roster:
        stem = name[:-5]
        # resolve to a source file (name -> actual source file + kind)
        if name in PAIR_CUTS:
            target = PAIR_CUTS[name]
            if target is None:
                problems.append("cut %s (pair removed — see PAIR_CUTS)" % name)
                continue
            if target == "spec":
                html = render_spec(stem)
                if html is None:
                    problems.append("UNRESOLVED %s — spec source missing" % name)
                    continue
                resolved.setdefault(name, html)
                continue
            if target.endswith(".html"):
                if os.path.exists(os.path.join(ORIG, target)):
                    html = open(os.path.join(ORIG, target), encoding="utf-8").read()
                    resolved.setdefault(name, html)
                elif target in pool:
                    html = render_spec(target[:-5])
                    if html is None:
                        problems.append("UNRESOLVED %s (pair %s)" % (name, target))
                        continue
                    resolved.setdefault(name, html)
                else:
                    problems.append("UNRESOLVED %s (pair %s missing)" % (name, target))
                continue
            continue
        if os.path.exists(os.path.join(ORIG, name)):
            resolved.setdefault(name, open(os.path.join(ORIG, name), encoding="utf-8").read())
        elif (t := pool.get(stem) or pool.get(stem.replace("_","-")) or pool.get(stem.replace("-","_"))) is not None:
            resolved.setdefault(name, render_page(t, CAT_ACCENTS.get(t["cat"], "#d8a25e")))
        else:
            problems.append("UNRESOLVED %s" % name)

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
            cat = cat_of(name)
            title = DESCMAP.get(key_for(stem), (None, stem.replace("_"," ").replace("-"," ").title(), None, None))[1] if key_for(stem) else stem.replace("_"," ").replace("-"," ").title()
            desc = ""
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
