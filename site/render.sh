#!/bin/bash
# Render a standalone figure/page HTML to PDF + PNG via headless Chrome.
# Usage: render.sh <input.html> <out_basename> <width> <height>
set -e
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
IN="$1"; OUT="$2"; WIDTH="$3"; HEIGHT="$4"
UDD="$(mktemp -d /tmp/chr.XXXXXX)"
"$CHROME" --headless=new --disable-gpu --no-first-run --no-default-browser-check \
  --log-level=3 --user-data-dir="$UDD" --no-pdf-header-footer \
  --print-to-pdf="$OUT.pdf" "file://$IN" >/dev/null 2>&1 || true
"$CHROME" --headless=new --disable-gpu --no-first-run --no-default-browser-check \
  --log-level=3 --user-data-dir="$UDD" --hide-scrollbars \
  --force-device-scale-factor=2 --default-background-color=FFFFFFFF \
  --window-size="$WIDTH,$HEIGHT" --screenshot="$OUT.png" "file://$IN" >/dev/null 2>&1 || true
rm -rf "$UDD"
echo "rendered $OUT.pdf / $OUT.png"
