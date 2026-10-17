#!/usr/bin/env python3
"""Functional smoke for Toolbench: run EVERY page's inline <script> under the
Node DOM-stub harness (build/smoke.js) and report throws.

Why this exists: the v2-era "100/100 PASS" smoke banner ran against a scratch
dir that was later PRUNED — stale evidence. Re-verify the tree you actually
built; never re-claim an old banner.

Usage:  python3 build/smoke.py [dir=default: docs/tools]
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.join(HERE, "smoke.js")           # the Node DOM-stub harness
DEFAULT_DIR = os.path.join(HERE, "..", "docs", "tools")


def main():
    d = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR)
    files = [f for f in os.listdir(d) if f.endswith(".html")] if os.path.isdir(d) else []
    if not files:
        print("SMOKE FAIL: no .html files under", d)
        return 1
    if subprocess.run(["node", "--version"], capture_output=True).returncode != 0:
        print("SMOKE FAIL: node not found — the DOM-stub harness (smoke.js) cannot run.\n"
              "Do NOT fall back to static-only checks and call them a smoke pass.")
        return 1
    r = subprocess.run(["node", HARNESS, d], capture_output=True, text=True, timeout=300)
    out = (r.stdout or "").strip() or (r.stderr or "").strip()[:500]
    print(out[:1200])
    return 0 if out.startswith("PASS:") and "%d pages" % len(files) in out else 1


if __name__ == "__main__":
    sys.exit(main())
