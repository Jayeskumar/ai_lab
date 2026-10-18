#!/usr/bin/env bash
# Skeptic check: compile the four Lean files of C05/C08/C11/C12 and scan them for
# forbidden constructs.  Outputs: out/lean_<file>.txt (compiler output incl. #print axioms)
# and out/lean_grep.txt.  Usage: bash lean_check.sh   (from any directory)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/out"
LEAN_DIR="$(cd "$HERE/../../../proofs/lean" && pwd)"
export PATH="$HOME/.elan/bin:$PATH"
mkdir -p "$OUT"
: > "$OUT/lean_grep.txt"
for f in C05_Magmas C08_Knuth C11_Codes C12_Games; do
  echo "== $f" | tee -a "$OUT/lean_grep.txt"
  grep -nE "sorry|admit|native_decide|^axiom| axiom |unsafe|implemented_by|extern|opaque|@\[csimp\]" \
       "$LEAN_DIR/Infinity/$f.lean" >> "$OUT/lean_grep.txt" || echo "   (no hits)" >> "$OUT/lean_grep.txt"
  start=$(date +%s)
  ( cd "$LEAN_DIR" && nice -n 10 lake env lean "Infinity/$f.lean" ) > "$OUT/lean_$f.txt" 2>&1
  rc=$?
  end=$(date +%s)
  echo "exit=$rc seconds=$((end-start))" >> "$OUT/lean_$f.txt"
  echo "$f exit=$rc seconds=$((end-start))"
done
