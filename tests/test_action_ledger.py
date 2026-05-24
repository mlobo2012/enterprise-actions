from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))

from action_ledger import add_action, all_actions, get_action, verify_citations, _reset_for_tests  # noqa: E402


def test_add_get_round_trip() -> None:
    _reset_for_tests()
    record = add_action(
        {
            "what": "apply label",
            "why": "queue item is a direct request",
            "evidence_ids": ["queue-1"],
            "reversibility": "reversible",
            "gate_decision": "auto",
            "actor": "enterprise-actions/triage",
        }
    )

    assert record["id"]
    assert record["created_at"]
    fetched = get_action(record["id"])
    assert fetched == record
    assert all_actions() == [record]


def test_all_actions_returns_copy() -> None:
    _reset_for_tests()
    record = add_action({"what": "draft reply", "evidence_ids": ["msg-1"]})
    actions = all_actions()
    actions[0]["what"] = "mutated locally"
    assert get_action(record["id"])["what"] == "draft reply"


def test_verify_citations_rejects_fabricated_id() -> None:
    result = verify_citations(["real-1", "fake-1"], ["real-1"])
    assert result["ok"] is False
    assert result["missing"] == ["fake-1"]


def test_verify_citations_passes_real_ids() -> None:
    result = verify_citations(["real-1", "real-2"], ["real-1", "real-2", "real-3"])
    assert result["ok"] is True
    assert result["missing"] == []


def test_verify_citations_empty_is_not_ok() -> None:
    result = verify_citations([], ["real-1"])
    assert result["ok"] is False
    assert result["reason"] == "empty evidence_ids"
