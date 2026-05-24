"""Append-only action ledger and citation verification."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Any
from uuid import uuid4


_LEDGER: list[dict[str, Any]] = []


def _ledger_path() -> Path | None:
    value = os.environ.get("ENTERPRISE_ACTIONS_LEDGER")
    if not value:
        return None
    return Path(value)


def _append_to_file(record: dict[str, Any]) -> None:
    path = _ledger_path()
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def add_action(record: dict[str, Any]) -> dict[str, Any]:
    """Append an action record and return the immutable stored copy."""

    if not isinstance(record, dict):
        raise TypeError("record must be a dict")

    stored = deepcopy(record)
    stored.setdefault("id", str(uuid4()))
    stored.setdefault("created_at", datetime.now(timezone.utc).isoformat())

    _LEDGER.append(deepcopy(stored))
    _append_to_file(stored)
    return deepcopy(stored)


def get_action(action_id: str) -> dict[str, Any] | None:
    """Return an action by ID, or None when it is not present."""

    for record in _LEDGER:
        if record.get("id") == action_id:
            return deepcopy(record)
    return None


def all_actions() -> list[dict[str, Any]]:
    """Return a copy of all action records in append order."""

    return deepcopy(_LEDGER)


def verify_citations(evidence_ids: list[str] | tuple[str, ...] | set[str] | None,
                     known_ids: list[str] | tuple[str, ...] | set[str] | None) -> dict[str, Any]:
    """Check that every evidence ID resolves to a known retrieved source ID."""

    evidence = list(evidence_ids or [])
    known = set(known_ids or [])

    if not evidence:
        return {"ok": False, "missing": [], "reason": "empty evidence_ids"}

    missing = [evidence_id for evidence_id in evidence if evidence_id not in known]
    return {
        "ok": not missing,
        "missing": missing,
        "reason": "ok" if not missing else "unknown evidence_ids",
    }


def _reset_for_tests() -> None:
    _LEDGER.clear()
