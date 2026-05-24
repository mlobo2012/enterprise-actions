#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

BLOCK_PAYLOAD='{"reversibility":"irreversible","blast_radius":"low","confidence":0.99,"sources_cited":true,"action_class":"external_send","evidence_ids":["ev-1"],"known_ids":["ev-1"]}'
ALLOW_PAYLOAD='{"reversibility":"reversible","blast_radius":"low","confidence":0.92,"sources_cited":true,"evidence_ids":["ev-1"],"known_ids":["ev-1"]}'

echo "BLOCK CASE: ungated external send"
if "$ROOT/hooks/action-gate.sh" <<<"$BLOCK_PAYLOAD" >"$TMPDIR/block.out" 2>&1; then
  cat "$TMPDIR/block.out"
  echo "FAIL: block case unexpectedly allowed"
  exit 1
fi
cat "$TMPDIR/block.out"

echo "ALLOW CASE: reversible confident cited action"
"$ROOT/hooks/action-gate.sh" <<<"$ALLOW_PAYLOAD" >"$TMPDIR/allow.out" 2>&1
cat "$TMPDIR/allow.out"

echo "PASS: hook blocked unsafe action and allowed safe action"
