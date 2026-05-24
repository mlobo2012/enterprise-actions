from __future__ import annotations

from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))

from action_safety import (  # noqa: E402
    HARD_GATED_ACTION_CLASSES,
    classify,
    classify_action,
    evaluate_proposed_action,
)


def test_irreversible_always_not_auto() -> None:
    assert classify("irreversible", "low", 1.0, True) == "confirm"
    assert classify("irreversible", "medium", 0.99, True) != "auto"
    assert classify("destructive", "low", 0.99, True) != "auto"


def test_uncited_blocks_auto() -> None:
    assert classify("reversible", "low", 1.0, False) == "escalate"
    result = evaluate_proposed_action(
        {
            "reversibility": "reversible",
            "blast_radius": "low",
            "confidence": 1.0,
            "sources_cited": False,
        }
    )
    assert result["allowed"] is False
    assert result["decision"] == "escalate"


def test_low_confidence_or_conflict_escalates() -> None:
    assert classify("reversible", "low", 0.649, True) == "escalate"
    assert classify("reversible", "conflict", 0.99, True) == "escalate"
    assert classify("irreversible", "low", 0.849, True) == "escalate"


def test_reversible_confident_cited_low_blast_can_auto() -> None:
    assert classify("reversible", "low", 0.90, True) == "auto"


def test_confidence_boundaries() -> None:
    assert classify("reversible", "low", 0.85, True) == "auto"
    assert classify("reversible", "low", 0.849, True) == "confirm"
    assert classify("reversible", "low", 0.65, True) == "confirm"
    assert classify("reversible", "low", 0.649, True) == "escalate"


@pytest.mark.parametrize("confidence", [-0.1, 1.1])
def test_confidence_out_of_range_raises(confidence: float) -> None:
    with pytest.raises(ValueError):
        classify("reversible", "low", confidence, True)


@pytest.mark.parametrize(
    "action_class",
    [
        "external_send",
        "overwrite_trusted_record",
        "commitment_on_others_behalf",
        "numbers_to_leadership",
        "bulk_destructive",
    ],
)
def test_hard_gated_action_classes_never_auto(action_class: str) -> None:
    decision = classify_action("reversible", "low", 1.0, True, action_class=action_class)
    assert decision in {"confirm", "escalate"}
    assert decision != "auto"


def test_hard_gated_table_contains_exact_five_classes() -> None:
    assert set(HARD_GATED_ACTION_CLASSES) == {
        "external_send",
        "overwrite_trusted_record",
        "commitment_on_others_behalf",
        "numbers_to_leadership",
        "bulk_destructive",
    }


def test_confirmed_hard_gate_can_allow_but_unconfirmed_blocks() -> None:
    payload = {
        "reversibility": "reversible",
        "blast_radius": "low",
        "confidence": 1.0,
        "sources_cited": True,
        "action_class": "external_send",
        "evidence_ids": ["ev-1"],
        "known_ids": ["ev-1"],
    }
    assert evaluate_proposed_action(payload)["allowed"] is False
    payload["confirmed"] = True
    assert evaluate_proposed_action(payload)["allowed"] is True
