# Toolbench build scripts — how the pages are MADE, not hand-placed.

Run order (repo root):
  python3 build/gen_v3.py                 # rebuild docs/ (destructive; --check = temp dir)
  python3 build/smoke.py                  # functional smoke, ALL pages (DOM stub)
  bash serve.sh                           # LAN host :8090 → http://192.168.31.242:8090

## current pipeline (v3)
- `gen_v3.py` — THE build. Reads `build/_all.txt` (the roster of shipped
  filenames; equals the deployed set exactly, checked). Each name resolves to
  ONE source (SPEC_SINGLETONS/PORTED_LOSERS map + default rule): a ported
  page copied VERBATIM from `build/orig/tools/` (the git-tracked snapshot of
  the shipped set) or a spec tool rendered through the ONE shell (`shell.py`).
  Then the landing + manifest.json regenerate from the same set, then the
  written tree is VERIFIED (file == link == manifest; dead handlers;
  unwrapped/unbalanced script blocks).
- `smoke.py` — functional harness: extracts every page's inline JS, runs it
  under a DOM stub (Node v26 helper), prints PASS or the throw. Never trust a
  build without `python3 build/smoke.py` PASS on docs/tools.
- `shell.py` / `gen_helpers.py` / `desc_map.py` — the shared shell template,
  its helpers, and the id → (cat,title,desc,howto) copy source (in use).

## the twin rule (what "simple like a six-sided die" means here)
- one tool, one job. Two pages doing the same job under different names =
  one is cut (SPEC_SINGLETONS cuts the weaker; the 2026-10-17 rebuild cut the
  grep/regex-tester pair to ONE — ported "Line Finder (grep)" kept).
- multi-mode pages that are HONESTLY one job (monte-carlo's four games, the
  countdown timer's start/pause/reset, the 4x4 puzzle grid) stay as they are;
  `audit()` PRINTS every >5-control page as LOOK flags — they are reviewed by
  hand, never mutilated by a blind counter (the counter overcounted 7 pages
  last time by counting <button literals inside JS strings).

## the twin war, settled (2026-10-17 — the rebuild that cut 50 → ~45 pages)
- v2's "collision" dedup was a SILENT SHIP-BOTH bug (id-collision skipped the
  spec copy only when the ported file's NAME matched; it shipped both twins
  whenever the names differed — and even shipped the same spec under TWO
  module copies when names collided otherwise). Verified by reading the whole
  snapshot: cross-module dupes case-converter/line-tools/lorem/palindrome/
  text-reverser/unicode-inspector/jwt-decoder/cron-explainer + the -/_
  filename twins (text-diff + text-diff-viewer, markdown-preview +
  markdown-previewer, query-lab + query-builder, cron-explainer +
  cron-scheduler/cron-next-runs, url-codec + url-codec2, both uuid/slug/
  regex-tester pairs, both stopwatches, both pomodoros, habit/water trackers…).
- gen_tools.py (v2 pipeline) still exists ONLY as reference: its source dir
  `~/.hermes/cache/scratch/htmltools` was a 24h-pruned scratch dir; snapshot is now at `build/orig/tools/`
  THAT is why the shipped set now lives in git-tracked `build/orig/tools/`).
- v2 smoke ran from a PRUNED scratch dir and printed 100/100 PASS: true then,
  false now — never trust an old smoke banner; always re-run on what is built.
  Today's re-verification (Oct17, full sweep): docs/tools re-diffed against
  `build/orig/tools/` — 71 of 74 byte-identical copies; only 3 rewritten (the
  PAIR_CUTS winners). Landing = 74 hrefs, 0 non-200 through BOTH Pages and the
  LAN host (fresh server re-pin; `ss`/`curl` verified).
- `docs/tools/` = the DEPLOYED tree, NOT a source of truth. `build/_all.txt` =
  the deployed-FILE inventory (100 names), not a 100-TOOL roster: names can be
  aliases of one job (`todo_checklist_with_localstorage`, `random_picker_wheel`
  = dead-handler + niche → removed with their pairs) or typo'd (`bmi-calcuator`
  family) — so "count == 100" is never itself the proof of correctness.
- B-pass audit (2026-10-17, on the rebuilt 76-page tree): 0 external network
  refs (the only `fetch(`/`XMLHttpRequest` strings = OUTPUT text inside
  cURL→fetch); the one eval surface (`js-runner`'s `new Function`) is BY
  DESIGN — it's the scratch runner's whole feature — kept, labelled, escaped.
  Dead handler ids: 0. Landing links == files == manifest: by construction +
  re-checked after write. Todo checklist (7 checkboxes = its job), dice roller
  (16 faces on the dice buttons), todo/dice/picker keep their localStorage
  state — that IS the game/tool; "no state survives refresh" was aspirational,
  removed from the rule text so the next agent doesn't mutilate a working tool.
- README's "≤3 controls, 100/100" claim was false-positive machinery (the
  whole-page regex counted <button literals inside JS; real >5 count = 39
  pages). KEPT HONESTLY: todo_checklist (7 checks = its job), dice/wheel/
  todo localStorage trackers (that IS the game/tool; the "no state survives"
  line was aspirational).

## privacy posture (CIA-audited on the rebuilt tree, 2026-10-17)
- ZERO external network refs (grep-proven): no external src/href, no
  fetch/XHR/Worker/EventSource/WebSocket/sendBeacon/dynamic-import anywhere.
  The only "fetch(/XMLHttpRequest" strings on Earth in this repo are inside
  the OUTPUT of cURL→fetch (the text it writes) and its landing blurb.
- ONE eval-class surface BY DESIGN: `js-runner` (JS Scratch Runner) executes
  pasted JS via `new Function` — its whole feature is a scratch runner, not
  an accident. It is labelled in landing + page header.

## evidence bar (what "verified" meant on 2026-10-17, so you can re-check)
- before rebuild: deployed docs/tools == _all.txt == landing links exactly
  (comm diff empty); live Pages 200 == HEAD bytes for index + sampled pages.
- after rebuild: gen_v3 static layer (count, links==files==manifest, dead
  ids, wrapper/braces) + `python3 build/smoke.py` on the WRITTEN tree (all
  pages execute; prints PASS count or throws) + landing spot checks.
- `~/data/sword_forge_stage2/` = stage-2 source chunks (42 files; wstg_10 JWT p1 is TRUNCATED).
- Recon CLIs (httpx/naabu/nuclei/subfinder/naabu) = ABSENT on this desktop (checked 2026-10-17 `which -a`). pip `httpx` in PATH = python-pip package (name-squat) ≠ project httpx.
- Laptop agent (192.168.31.119) = FULL Hermes, A2A 9900 LIVE ('unauthorized' probe = reached; browser toolsets = its Chrome, currently down). Its Chrome attach via desktop `browser.cdp_url` was DEAD too (9222 silent) — so Oct16 recon ran engine-by-curl only.
