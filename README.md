# Toolbench

A self-contained workbench of **74 distinct client-side tools** (one page per job — twins + non-tools removed Oct 2026, see build/NOTES.md) (one page per job — the twins were cut Oct 2026, see build/NOTES.md) — text & code utilities,
ciphers, converters, calculators, puzzles and games — packaged as plain HTML
files with a premium landing page. No frameworks, no CDNs, no build step, no
network calls: open any page and it works offline.

**The audit workflow that got Toolbench to the finish line** — this repo is a
demo of a verified build pipeline, not hand-placed HTML. The suite was rebuilt
onto one dark "workbench" design shell, then (Oct 2026) the **twin war was
settled**: the same-job twins (two JSON formatters, two diff tools, two
markdown previewers, two query labs, two cron tools…) were cut to one page
per job — the "six-sided die" rule: people use one die, not a 20-faced one.

To regenerate the whole suite from source and prove every page executes clean:

```bash
python3 build/gen_v3.py            # rebuilds docs/ from build/orig/tools + specs
python3 build/smoke.py             # functional smoke over ALL pages (DOM-stub)
node build/smoke.js docs/tools     # same harness direct (Node v26)
```

A rebuild is only trustworthy if the harnesses match the tree they check:
`gen_tools.py`/`reskin.py` are v2-era reference files — the scratch dir they
read was PRUNED, so they build 50 pages today and their smoke banner is
STALE evidence, not current proof. Re-run, never re-claim.

## What's inside

- **~99 tools** in `docs/tools/` — each a single self-contained HTML file
  (embedded CSS/JS, ~1.2 MB for the entire suite); twins cut to one per job
- **Landing page** (`docs/index.html`) — dark editorial catalog with live search
  (type to filter, `/` to focus, `Esc` to clear), category chips, and per-tool
  descriptions + how-to-use lines
- **Generator** (`build/`) — the suite is *built, not hand-placed*:
  - `gen_v3.py` (current) assembles from `build/orig/tools/` (git-tracked
    snapshot of the shipped set) + the spec modules, through ONE shell
  - `gen_tools.py` + `reskin.py` are v2-era reference files (do not run;
    `build/NOTES.md` explains the twin-cut history and evidence)
  - `smoke.py`/`smoke.js` is the functional smoke harness: runs **every**
    page's inline JS under a DOM stub and fails the build on the first throw

## Tool categories

| Category | Count | Examples |
|---|---|---|
| Games & Play | 11 | 15 Puzzle, Maze Maker (DFS), KenKen, Blackjack (S17), Wordle Helper, Simon Says, Minesweeper, Coin-Flip/Dice-roller stats, Number Guess, Random Picker Wheel |
| Math & Finance | 3 | Expression Solver, Monte-Carlo Odds Simulator, Compound Interest |
| Text | 12 | Text Diff (LCS + side-by-side), Regex Replace, Line Tools, Case Converter, Unicode Inspector, ASCII Banner, Typo Scanner |
| Encoding & Hashing | 18 | Base64, Hex⇄Text, Binary⇄Text, ROT13+Caesar, Vigenère, CRC32/FNV-1a, SHA-256 (WebCrypto), Entropy Scanner, URL codecs |
| Color | 4 | Gradient Lab, Box-Shadow Lab, Contrast Checker (WCAG), Hex/HSL/RGB converter |
| Time & Productivity | 6 | Stopwatch + laps, Typing Speed, Reaction Time, Emoji Picker, Countdown, Timezone Compare, Flashcards, Habit Tracker |
| Developer | 19 | JSON Formatter/Validator, JSON→TS/CSV, JWT Decoder, YAML→JSON, cURL→fetch, Regex Tester, JS Scratch Runner, HTML Preview/Minifier, Cron Explainer/Next Runs, Query Lab/Builder, Slug/UUID |
| Misc | 1 | (heuristic groupings — see build/NOTES.md) |

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
python3 build/gen_v3.py            # rebuilds docs/ from build/orig/tools + spec modules
python3 build/smoke.py             # DOM-stub functional smoke over EVERY page (Node harness)
```

The build regenerates landing + manifest.json from the same set it writes, then
verifies the WRITTEN tree (index links == files == manifest; dead-handler
audit; script-wrapper balance) and the smoke harness runs the WRITTEN tree.
Old docs/ deleted mid-rebuild is a recoverable accident (git), but it is
still an accident — that is why `serve.sh` exists and why docs/ stays tracked.

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
│   └── tools/*.html      the tool pages (99) + landing + manifest.json + .nojekyll
├── build/                the build system (sources)
│   ├── gen_v3.py         THE build (roster → resolution → shell → verify)
│   ├── gen_tools.py      v2-era reference only (pruned source dir — do not run)
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

Built Oct 2026 (v3 rebuild) · 99 tools, one page per job · no deps · no tracking
