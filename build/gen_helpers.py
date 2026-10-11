"""Shared HTML assembly for Toolbench build. Shell styles live in shell.py (PAGE/LANDING templates)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import PAGE, LANDING, render_page, render_landing

CAT_ACCENTS = {
    "Text": "#d8a25e",
    "Developer": "#6fb3d2",
    "Encoding & Hashing": "#b07fd0",
    "Images": "#67b98a",
    "Color": "#e0736b",
    "Math & Finance": "#5fc4c0",
    "Time & Productivity": "#d2b45e",
}

def page_html(tool):
    acc = CAT_ACCENTS.get(tool["cat"], "#d8a25e")
    return render_page(tool, acc)

def build(outdir, tools):
    tdir = os.path.join(outdir, "tools")
    os.makedirs(tdir, exist_ok=True)
    for t in tools:
        with open(os.path.join(tdir, t["id"] + ".html"), "w") as f:
            f.write(page_html(t))
    landing = render_landing(tools, CAT_ACCENTS, "Built Oct 2026")
    with open(os.path.join(outdir, "index.html"), "w") as f:
        f.write(landing)
    return len(tools)

def mkpage(i, cat, title, desc, body, js):
    """Helper for tool data modules: build a tool dict."""
    return {"id": i, "cat": cat, "title": title, "desc": desc, "body": body, "script": js}
