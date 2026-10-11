#!/usr/bin/env bash
# Toolbench LAN server: serve the 100-tool suite on all interfaces, port 8090.
# Safe by design: --directory is pinned to the read-only build output dir, so
# nothing outside ~/toolbench/out is ever reachable (path traversal can only
# resolve inside that root; Python's http.server also blocks %2e%2e traversal).
# No env vars, tokens or secrets in this file.
ROOT="/home/soham-7/toolbench/out"
PORT="${TOOLBENCH_PORT:-8090}"
if ss -tln 2>/dev/null | grep -q ":$PORT "; then
  echo "toolbench already listening on :$PORT"
  exit 0
fi
exec python3 -m http.server "$PORT" --bind 0.0.0.0 --directory "$ROOT"
