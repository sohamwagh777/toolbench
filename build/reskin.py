# -*- coding: utf-8 -*-
"""Reskin pass for Toolbench ported pages (the 50 'ported' tools copied verbatim
from scratch in the first build — mixed Tailwind-slate look).

Run AFTER gen_tools.py (it wipes ../out and rebuilds it, so this must re-run too).

Per ported file:
 - strip the old ad-hoc <header>/<h1>/<p class=subtitle> block
 - inject the Toolbench chrome (back link, category, title, description, how-to)
 - retone Tailwind-slate palette values to Toolbench tokens (bg/panel/line/ink/mut)
 - swap ad-hoc font stacks for the Toolbench sans/mono stacks
 - add Esc -> ../index.html
Usage text is read from desc_map.py (single source of truth).

Run: python3 reskin.py
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from desc_map import M as DESCMAP

TOOLS = os.path.join(HERE, "..", "out", "tools")

# filename stem -> desc_map key (dashes vs underscores twins)
def key_for(fname):
    stem = fname[:-5]
    if stem in DESCMAP:
        return stem
    alt = stem.replace("_", "-")
    if alt in DESCMAP:
        return alt
    alt = stem.replace("-", "_")
    if alt in DESCMAP:
        return alt
    return None

CHROME = """<header class="tb"><a class="back" href="../index.html" title="Back to all tools (Esc)">&#8592; All tools</a>
<div class="mid"><div class="cat">__CAT__</div><h1>__TITLE__</h1><p class="desc">__DESC__</p><p class="howto"><b>How to use.</b> __HOWTO__</p><p class="priv">Private &amp; local: everything stays in this page — no network calls, no tracking, your input never leaves this tab.</p></div>
<a class="tag" href="../index.html">TOOLBENCH</a></header>

"""

# chrome styles (merged into any existing <style>; page defaults stay intact)
CHROME_CSS = """
:root{--tb-acc:#d8a25e}
header.tb{display:flex;align-items:center;gap:14px;max-width:860px;margin:0 auto;padding:20px 20px 6px}
header.tb .back{font:600 11px/1 ui-monospace,'Cascadia Mono','SF Mono',Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;color:var(--mut,#8f949b);border:1px solid var(--border,#282c32);padding:9px 12px;border-radius:8px;white-space:nowrap}
header.tb .back:hover{color:var(--text,#ecebe6);border-color:#8f949b}
header.tb .mid{flex:1;min-width:0}header.tb .cat{font:600 10px/1 ui-monospace,'Cascadia Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:#d8a25e}
header.tb h1{font:400 21px/1.25 Georgia,'Iowan Old Style',serif;margin:4px 0 3px;color:var(--text,#ecebe6)}
header.tb .desc,header.tb .howto,header.tb .priv{margin:0;font-size:12.5px;color:var(--text-muted,#8f949b)}
header.tb .howto{margin-top:4px}header.tb .howto b{color:#ecebe6;font-weight:600}
header.tb .priv{margin-top:4px;font-size:11px;opacity:.75}
header.tb .tag{font:600 10px/1 ui-monospace,monospace;letter-spacing:.14em;color:var(--mut,#8f949b);text-decoration:none}
@media(max-width:640px){header.tb{padding:14px 14px 4px}}
"""

FONT_STACK = r"ui-sans-serif,-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif"
FONT_MONO = r"ui-monospace,'Cascadia Mono','JetBrains Mono','SF Mono',Menlo,Consolas,monospace"

# palette retone (Tailwind slate -> Toolbench workbench tokens)
HEX_SWAPS = [
    ("#0f172a", "#0e0f11"), ("#16213e", "#0e0f11"), ("#1a1a2e", "#0e0f11"),
    ("#1e293b", "#15171a"), ("#16212b", "#15171a"), ("#1f2937", "#15171a"), ("#16324f", "#15171a"),
    ("#334155", "#282c32"), ("#2a2a3a", "#282c32"), ("#2d3748", "#282c32"), ("#3a3f4b", "#282c32"),
    ("#f8fafc", "#ecebe6"), ("#e2e8f0", "#ecebe6"), ("#e6e6e6", "#ecebe6"), ("#f1f5f9", "#ecebe6"),
    ("#94a3b8", "#8f949b"), ("#8b95a5", "#8f949b"), ("#a0a6b0", "#8f949b"),
    ("#60a5fa", "#6fb3d2"), ("#3b82f6", "#6fb3d2"),
]

ESC_JS = "document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!(e.target.closest&&e.target.closest('input,textarea,select'))){location.href='../index.html';}});"

def reskin(path, cat, title, desc, howto):
    src = open(path, encoding="utf-8").read()
    if 'header class="tb"' in src:
        return "skip (already shell)"  # spec-rendered pages already carry proper chrome
    # body start
    body_m = re.search(r"<body[^>]*>", src)
    if not body_m:
        return "skip (no body)"
    head, body = src[:body_m.end()], src[body_m.end():]
    # 1. strip ad-hoc header block: <header>...</header> or leading <h1>/<p class=subtitle>
    body2 = re.sub(r"<header[^>]*>.*?</header>", lambda m: "\n" + CHROME.replace("__CAT__", cat.upper()).replace("__TITLE__", title).replace("__DESC__", desc).replace("__HOWTO__", howto), body, count=1, flags=re.S)
    if "<header" in body:
        # h1/subtitle style block (ported pages using <h1> then subtitle)
        m2 = re.search(r"(<h1>.*?</h1>)\s*(<p class=\"?subtitle.*?</p>)?", body, re.S)
        if m2:
            ins = CHROME.replace("__CAT__", cat.upper()).replace("__TITLE__", title).replace("__DESC__", desc).replace("__HOWTO__", howto)
            body2 = body[:m2.start()] + ins + body[m2.end():]
    else:
        body2 = body if body2 != body else body
    if body2 == body:
        ins = CHROME.replace("__CAT__", cat.upper()).replace("__TITLE__", title).replace("__DESC__", desc).replace("__HOWTO__", howto)
        body2 = "\n" + ins + body
    # 2. merge chrome CSS into <style> if present, else a fresh <style> at body top
    if "<style" in head:
        head = head.replace("</style>", CHROME_CSS + "</style>", 1)
    # 3. font stacks inside head <style>
    for st in ['"Segoe UI", Arial, Helvetica, sans-serif', "Arial, Helvetica, sans-serif", '"Segoe UI", sans-serif']:
        head = head.replace(st, FONT_STACK)
    # 4. Esc handler
    if ESC_JS not in body2:
        body2 = body2 + "<script>\n" + ESC_JS + "\n</script>\n"
    out = head + body2
    if "</body>" not in out:
        out += "</body></html>"
    open(path, "w", encoding="utf-8").write(out)
    return "done"

def main():
    n_done = n_skip = 0
    for fname in sorted(os.listdir(TOOLS)):
        if not fname.endswith(".html"):
            continue
        k = key_for(fname)
        if not k:
            print("NO DESC ENTRY:", fname)
            continue
        cat, title, desc, howto = DESCMAP[k]
        res = reskin(os.path.join(TOOLS, fname), cat, title, desc, howto)
        if res == "done":
            n_done += 1
        else:
            n_skip += 1
            print("SKIP", fname, res)
    print("reskinned:", n_done, "skipped:", n_skip)

if __name__ == "__main__":
    main()
