# Toolbench

A self-contained workbench of **100 client-side tools** — text & code utilities,
ciphers, converters, calculators, puzzles and games — packaged as plain HTML
files with a premium landing page. No frameworks, no CDNs, no build step, no
network calls: open any page and it works offline.

**The 8 anti-slop tells that got Toolbench to the finish line** — this repo is
also a demo of an audited design workflow: the same tool pages first shipped in
an ad-hoc Tailwind-slate look, failed a 10-point slop audit, and were rebuilt
onto a single dark "workbench" design system (one shell, one accent-per-category,
serif titles + mono detail, real density, no decorative icon-tiles, no fake
dashboards). Run `python3 build/gen_tools.py && python3 build/reskin.py` to
regenerate all 101 pages, then `node build/smoke.js docs/tools` to prove they
every one executes clean (100/100 PASS) — no browser needed.

## What's inside

- **100 tools** in `docs/tools/` — each a single self-contained HTML file
  (embedded CSS/JS, ~1.2 MB for the entire suite)
- **Landing page** (`docs/index.html`) — dark editorial catalog with live search
  (type to filter, `/` to focus, `Esc` to clear), category chips, and per-tool
  descriptions + how-to-use lines
- **Generator** (`build/`) — the suite is *built, not hand-placed*:
  - `gen_tools.py` assembles pages from a single page shell + `desc_map.py`
    (description/how-to source of truth) and the spec modules
    (`tools_text.py`, `tools_dev.py`, `tools_extra_{a,b,c}.py`)
  - `reskin.py` retrofits any ported (foreign) page onto the same design shell
  - `smoke.js` is the functional smoke-test harness: runs **every** page's
    inline JS under a DOM stub and fails the build on the first throw

## Tool categories

| Category | Count | Examples |
|---|---|---|
| Games & Play | 10 | 15 Puzzle, Maze Maker (DFS), KenKen, Blackjack (S17), Wordle Helper, Simon Says, Minesweeper |
| Math & Finance | 10 | Expression Solver, Monte-Carlo Odds Simulator, Compound Interest, EMI, Tip |
| Text | 22 | Text Diff (LCS + side-by-side), Regex Replace, Line Tools, Case Converter, Unicode Inspector, Mad-Libs, ASCII Banner |
| Encoding & Hashing | 19 | Base64, Hex⇄Text, Binary⇄Text, ROT13 + Caesar, Vigenère, CRC32/FNV-1a, SHA-256 (WebCrypto), Entropy Scanner, URL codecs |
| Developer | 22 | JSON Formatter/Validator, JSON→TS, JWT Decoder, YAML→JSON, cURL→fetch, Regex Tester, Hex Dump Viewer, JS Scratch Runner, HTML Preview/Minifier, Cron Next Runs, Query Labs |
| Color | 4 | Gradient Lab, Box-Shadow Lab, Contrast Checker (WCAG), Hex/HSL/RGB converter |
| Time & Productivity | 9 | Pomodoro, Stopwatch, Typing Speed, Reaction Time, Emoji Picker, Countdown |
| Misc | 4 | UUID Generator, Slug Generator, Random Picker Wheel, Time-difference calc |

## Quick start

**Just want to use it:** either enable Pages (Deploy a static site from
→ `/docs` — see below) or run a static file server on any machine and open
`docs/index.html`. The landing page links tools via relative `tools/*.html`
hrefs and uses no absolute paths or CDN refs, so it works the same on
`file://`, on a LAN IP, and under the Pages `/toolbench/` base path.

```bash
python3 -m http.server 8090 --directory docs   # or: cd docs && python3 -m http.server
# http://localhost:8090/  → landing page, Esc returns from any tool
```

**Rebuild the whole suite from source:**

```bash
python3 build/gen_tools.py      # regenerates docs/ (101 HTML files, asserts == 100 tools)
node build/smoke.js docs/tools  # functional smoke: every page's JS executes clean
```

`gen_tools.py` hard-asserts the 100-tool invariant and the smoke harness must
report `PASS: 100 pages` before a build is considered good.

**GitHub Pages:** this site deploys from `/docs` (branch `master`). After any
rebuild, push to `master` and Pages redeploys automatically — no routing or
rewrites needed, the whole site is plain files.

## Privacy & security posture

- Every tool is **offline-first**: no `fetch`/XHR/CDN/remote refs anywhere —
  audited by grep audit of all 101 files, zero external references
- Pasted data never leaves the page; nothing is persisted except localStorage
  in the three opt-in tracker tools (habit/todo/emoji), which stay on-device
- JS Scratch Runner's code box is sandboxed and escaped; hash tools use
  WebCrypto (`crypto.subtle`) only, never hand-rolled crypto for the real ones
- No secrets, tokens, personal data, or environment paths in any shipped file
- Hosting: `serve.sh` pins the file root to the read-only `docs/` dir (path
  traversal-proof server), so worst case a bad request gets a 404, never a file

## Layout

```
toolbench/
├── docs/                 the built site (GitHub Pages site root — deploy from /docs)
│   ├── index.html        landing / catalog (Pages entry point)
│   ├── manifest.json     tool inventory (regenerated on every build)
│   ├── .nojekyll         skip Jekyll processing (plain-HTML site)
│   └── tools/*.html      the 100 tools
├── build/                the build system (sources)
│   ├── gen_tools.py      renderer + landing generator
│   ├── desc_map.py       descriptions & usage text (single source of truth)
│   ├── tools_*.py        per-category tool specs
│   └── smoke.js          functional smoke harness (node)
└── serve.sh              one-command LAN serve (port 8090, read-only root)
```

## Verified

All 100 tool pages execute their inline JS without a top-level throw under the
smoke harness (`PASS: 100 pages`), and a representative sample (Expression
Solver, Text Diff, Wordle Helper, Base Converter, Base64) was additionally
driven end-to-end in a real browser with functional outputs checked.

---

Built Oct 2026 · 100/100 tools · one page each, ~12 KB/page · no deps · no tracking
