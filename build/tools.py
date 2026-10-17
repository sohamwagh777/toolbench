"""Toolbench v3 source of truth — the six-sided-die rule.

A tool page is SIMPLE iff it has <= 3 first-class controls, <= 4 options per
select, and <= 3 buttons. Anything above that is a Swiss-army knife and gets
either cut (twin/variant of another tool) or split into single-purpose tools.

Shape grammar (what a generated page may contain):
- an optional INPUT (textarea or one-line text field) — at most one
- optional OPTION selects — each <= 4 options, each option must be a real
  mode a user names out loud ("decode", "encode"), never a settings dial
- exactly one ACTION button, named after the verb people say:
  Decode / Encode / Convert / Count / Hash / Format / Compare / Draw / Play…
  (+ a Copy button when there is text output — Copy is plumbing, not a tool)
- an OUTPUT block

v3 rules that kill the "4, 10, 20 faces" problems:
- no input/output SWAP buttons (one tool, one direction — or both directions
  are ONE select-driven Convert action)
- no "Sample"/"Clear"/"Reset" utility buttons — a page that needs an undo
  button has too much state
- no hidden state that survives a refresh (no localStorage trackers)
- the output block and its Copy button appear once there is something to copy
- the landing page has ZERO decorative SVG glyphs (100 identical dice was slop)

API (consumed by gen_v3.py):
  CATEGORIES — ordered category names (landing section order)
  build_tools(ported_dir) -> (TOOLS, DROP_REPORT) where TOOLS lists Tool
  objects in build order and DROP_REPORT logs every cut with its reason.
  Tool.audit() -> (ok, (controls, options, buttons, dead_handler_ids))
  Tool.is_simple() -> bool (the die rule as a predicate)

Run via: python3 gen_v3.py   (destructive rebuild of ../docs)
"""
import importlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

MAX_CONTROLS = 3
MAX_OPTIONS = 4
MAX_BUTTONS = 3

CATEGORIES = ["Games & Play", "Math & Finance", "Text", "Encoding & Hashing",
              "Color", "Time & Productivity", "Developer", "Misc"]

SPEC_MODULES = ("tools_text", "tools_dev", "tools_extra_a", "tools_extra_b", "tools_extra_c")

# Ids dropped by the v2 build too (gen_tools.SKIP_SPEC) — twin/derivative cuts,
# NOT new tools. The rebuilt set = spec-pool ids minus SKIP_SPEC = the 50
# spec-pair tools. Nothing here re-deploys a cut twin.
SKIP_SPEC = {"word-counter", "slug-generator", "regex-tester", "uuid-generator",
             "cron-explainer", "fraction-calc", "emi-lite", "percentage-lab",
             "pomodoro2", "habit-tracker", "stopwatch2", "water-tracker",
             "sleep-planner", "pomodoro-log", "recipe-scaler", "donation-split",
             "random-words", "bmi-history", "expense-tracker", "calendar-gen",
             "pomodoro-timer2"}

# Cross-file duplicate specs (same tool shipped twice in the generator's own
# data — the first copy wins by module order; the second is a dead page).
SPEC_DUPES = {"case-converter", "cron-explainer", "jwt-decoder", "line-tools",
              "lorem-generator", "palindrome-checker", "random-words",
              "text-reverser", "unicode-inspector"}

# Same-tool twin pairs where BOTH sides were deployed. Spec side drops — the
# ported twin does the same job better (word-level inline diff, richer MD
# parser) or the pair is redundant (two query labs, three cron tools).
CUT_FOR_PORTED = {
    "text-diff": "text-diff-viewer (word-level inline diff wins)",
    "markdown-preview": "markdown-previewer-with-small-own-parser (richer parser wins)",
    "query-lab": "query-builder (same premise; decode-only twin cut)",
    "cron-scheduler": "cron-expression-explainer + cron-scheduler pair cut to one cron explainer",
}


class Tool:
    __slots__ = ("id", "cat", "title", "desc", "howto", "kind", "html", "js")

    def __init__(self, id, cat, title, desc, howto, kind, html, js):
        self.id, self.cat, self.title, self.desc, self.howto = id, cat, title, desc, howto
        self.kind, self.html, self.js = kind, html, js

    @property
    def complexity(self):
        """(controls, options, buttons) counted on the REAL rendered page."""
        controls = len(re.findall(r"<input|<select|<button", self.html))
        options = len(re.findall(r"<option", self.html))
        buttons = len(re.findall(r"<button", self.html))
        return controls, options, buttons

    def audit(self):
        c, o, b = self.complexity
        ok = c <= MAX_CONTROLS and o <= MAX_OPTIONS and b <= MAX_BUTTONS
        # every wire()/getElementById id must exist in the markup (dead-handler kill)
        ids = set(re.findall(r'id="([^"]+)"', self.html)) | {"out", "ta", "q", "nores"}
        used = set()
        for pat in (r"getElementById\('([^']+)'\)",
                    r"\$\('#?([A-Za-z][\w-]*)'\)",
                    r"wire\(\[?'([a-z0-9-]+)'",
                    r"wire\('([a-z0-9-]+)'"):
            used |= set(re.findall(pat, self.js))
        dead = sorted(u for u in used if u not in ids)
        return ok and not dead, (c, o, b, dead)

    def is_simple(self):
        return self.audit()[0]


def load_specs():
    """Raw tool specs, deduped by id (first module order copy wins)."""
    raw = {}
    for mod in SPEC_MODULES:
        m = importlib.import_module(mod)
        for t in m.TOOLS:
            if t["id"] not in raw:
                raw[t["id"]] = dict(t)
    return raw


def spec_tool(raw):
    """Wrap a v2 spec dict (keys: id,cat,title,desc,howto,body,script) into a Tool.

    Spec JS written for v2 relied on the page calling run() itself; the shell
    keeps that contract (auto-run on input + Run button via data-act) so specs
    move over without logic rewrites.
    """
    body = raw.get("body", "")
    script = raw.get("script", "")
    # mirror of shell.render_page's #out guarantee, so audit() sees the REAL page
    if 'id="out"' not in body and ("OUT(" in script or "getElementById('out')" in script):
        body += '<div id="out"></div>'
    if "data-act" not in body:
        body = '<div class="row"><button data-act="run">Run</button></div>' + body
    return Tool(raw["id"], raw.get("cat", "Misc"),
                raw.get("title", raw["id"].replace("_", " ").title()),
                raw.get("desc", ""), raw.get("howto", ""), "spec", body, script)


def build_tools(ported_dir=None):
    """(tools, drop_report) — resolve drops, apply desc_map copy, build Tools.

    ported_dir: if given (normally ../docs/tools), ported pages living there
    are also checked against the die rule — nothing sneaks back in via the
    landing page that the audit would fail.
    """
    from desc_map import M as DESCMAP
    raw = load_specs()
    drops = {}
    for dead in SPEC_DUPES:
        if dead in raw:
            drops[dead] = "duplicate spec (first copy, earlier module, wins)"
            raw.pop(dead)
    for dead in SKIP_SPEC:
        if dead in raw:
            why = CUT_FOR_PORTED.get(dead, "twin/derivative cut — same decision as v2 gen_tools.SKIP_SPEC")
            drops[dead] = why
            raw.pop(dead)
    tools = []
    for t in raw.values():
        if t["id"] in DESCMAP:  # desc_map is authoritative for cat/title/desc/howto
            cat, title, desc, howto = DESCMAP[t["id"]]
            t["cat"], t["title"], t["desc"], t["howto"] = cat, title, desc, howto
        tools.append(spec_tool(t))
    if ported_dir and os.path.isdir(ported_dir):
        for fname in sorted(os.listdir(ported_dir)):
            if fname.endswith(".html"):
                tools.append(spec_tool({"id": fname[:-5], "cat": _cat_of(fname),
                                        "title": fname[:-5], "desc": "", "howto": "",
                                        "body": "<!-- ported page: copied verbatim -->",
                                        "script": ""}))
    tools.sort(key=lambda t: (CATEGORIES.index(t.cat) if t.cat in CATEGORIES
                              else len(CATEGORIES), t.id))
    return tools, drops


def _cat_of(fname):
    """Same heuristic v2 used for ported files (gen_tools.cat_of)."""
    low = fname.lower()
    for cat, keys in [("Encoding & Hashing", ["base64", "base-converter", "morse", "cipher", "hash", "fnv", "barcode"]),
                      ("Developer", ["regex", "json", "curl", "yaml", "env", "markdown", "js-scratch", "minifier", "subnet", "ipv4", "ipv6", "jwt", "batch-string", "csv"]),
                      ("Color", ["color-converter", "gradient", "contrast", "pixel", "draw", "shape", "flexbox", "grid-layout"]),
                      ("Math & Finance", ["calculator", "calc", "fraction", "simplifier", "equation", "percentage"]),
                      ("Time & Productivity", ["timer", "stopwatch", "pomodoro", "countdown", "tracker", "todo", "flashcard", "history", "clock", "emoji"]),
                      ("Text", ["counter", "generator", "replacer", "preview", "translator", "picker", "slug", "checker", "scanner"])]:
        if any(k in low for k in keys):
            return cat
    if any(k in low for k in ["game", "puzzle", "minesweeper", "simon", "hangman", "guess", "flip", "dice", "wheel", "maze"]):
        return "Games & Play"
    if any(k in low for k in ["converter", "codec", "conversion"]):
        return "Encoding & Hashing"
    return "Misc"
