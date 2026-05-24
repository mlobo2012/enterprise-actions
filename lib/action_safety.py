"""Deterministic action-safety classifier for Enterprise Actions."""

from __future__ import annotations

import json
import sys
from typing import Any


Decision = str

AUTO_CONFIDENCE_THRESHOLD = 0.85
MINIMUM_CONFIDENCE_THRESHOLD = 0.65

HARD_GATED_ACTION_CLASSES: dict[str, Decision] = {
    "external_send": "confirm",
    "overwrite_trusted_record": "confirm",
    "commitment_on_others_behalf": "confirm",
    "numbers_to_leadership": "confirm",
    "bulk_destructive": "escalate",
}

REVERSIBLE_VALUES = {"reversible", "undoable", "low-risk", "low_risk"}
IRREVERSIBLE_VALUES = {"irreversible", "destructive", "external", "overwrite"}
LOW_BLAST_VALUES = {"low", "limited", "personal", "single_record", "single-record"}
MEDIUM_BLAST_VALUES = {"medium", "team", "internal", "record"}
HIGH_BLAST_VALUES = {"high", "wide", "external", "org", "organization", "leadership", "bulk"}
CONFLICT_VALUES = {"conflict", "conflicted", "conflicting_sources", "conflicting-sources"}


def _norm(value: str | None) -> str:
    return str(value or "").strip().lower().replace(" ", "_")


def _validate_confidence(confidence: float) -> float:
    try:
        value = float(confidence)
    except (TypeError, ValueError) as exc:
        raise ValueError("confidence must be a number between 0 and 1") from exc

    if value < 0.0 or value > 1.0:
        raise ValueError("confidence must be between 0 and 1")
    return value


def classify(reversibility: str, blast_radius: str, confidence: float, sources_cited: bool) -> Decision:
    """Classify a proposed action as auto, confirm, or escalate."""

    confidence_value = _validate_confidence(confidence)
    reversibility_value = _norm(reversibility)
    blast_value = _norm(blast_radius)

    if not sources_cited:
        return "escalate"

    if blast_value in CONFLICT_VALUES:
        return "escalate"

    if confidence_value < MINIMUM_CONFIDENCE_THRESHOLD:
        return "escalate"

    if reversibility_value in IRREVERSIBLE_VALUES:
        if blast_value in HIGH_BLAST_VALUES or confidence_value < AUTO_CONFIDENCE_THRESHOLD:
            return "escalate"
        return "confirm"

    if reversibility_value not in REVERSIBLE_VALUES:
        return "escalate"

    if blast_value in HIGH_BLAST_VALUES:
        return "confirm"

    if blast_value in MEDIUM_BLAST_VALUES:
        return "confirm"

    if blast_value not in LOW_BLAST_VALUES:
        return "escalate"

    if confidence_value >= AUTO_CONFIDENCE_THRESHOLD:
        return "auto"

    return "confirm"


def hard_gate_decision(action_class: str | None, base_decision: Decision = "auto") -> Decision:
    """Apply the five hard-gated action classes to an existing decision."""

    normalized_class = _norm(action_class)
    forced = HARD_GATED_ACTION_CLASSES.get(normalized_class)
    if forced is None:
        return base_decision
    if forced == "escalate" or base_decision == "escalate":
        return "escalate"
    return "confirm"


def classify_action(
    reversibility: str,
    blast_radius: str,
    confidence: float,
    sources_cited: bool,
    action_class: str | None = None,
) -> Decision:
    """Classify a proposed action and then enforce hard-gated classes."""

    base_decision = classify(reversibility, blast_radius, confidence, sources_cited)
    return hard_gate_decision(action_class, base_decision)


def is_hard_gated_action(action_class: str | None) -> bool:
    return _norm(action_class) in HARD_GATED_ACTION_CLASSES


def _citation_result(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        from action_ledger import verify_citations
    except ImportError:
        return {"ok": True, "missing": [], "reason": "citation verification unavailable"}

    evidence_ids = payload.get("evidence_ids")
    known_ids = payload.get("known_ids")
    if evidence_ids is None and known_ids is None:
        return {"ok": True, "missing": [], "reason": "not provided"}
    return verify_citations(evidence_ids, known_ids)


def evaluate_proposed_action(payload: dict[str, Any]) -> dict[str, Any]:
    """Evaluate a hook payload and return an allow/block decision."""

    if not isinstance(payload, dict):
        return {"allowed": False, "decision": "escalate", "reason": "payload must be a JSON object"}

    citation = _citation_result(payload)
    if not citation.get("ok", False):
        return {
            "allowed": False,
            "decision": "escalate",
            "reason": f"citation verification failed: {citation.get('reason')}",
            "missing": citation.get("missing", []),
        }

    sources_cited = payload.get("sources_cited")
    if sources_cited is None:
        sources_cited = bool(payload.get("evidence_ids"))

    try:
        decision = classify_action(
            reversibility=payload.get("reversibility", ""),
            blast_radius=payload.get("blast_radius", ""),
            confidence=payload.get("confidence", 0),
            sources_cited=bool(sources_cited),
            action_class=payload.get("action_class"),
        )
    except ValueError as exc:
        return {"allowed": False, "decision": "escalate", "reason": str(exc)}

    if decision == "auto":
        return {"allowed": True, "decision": decision, "reason": "auto gate passed"}

    if decision == "confirm" and payload.get("confirmed") is True:
        return {"allowed": True, "decision": decision, "reason": "confirmed gate passed"}

    if decision == "confirm":
        return {"allowed": False, "decision": decision, "reason": "confirmation required"}

    return {"allowed": False, "decision": decision, "reason": "escalation required"}


def _main() -> int:
    raw_payload = sys.stdin.read()
    try:
        payload = json.loads(raw_payload)
    except json.JSONDecodeError as exc:
        print(f"BLOCK action-gate invalid JSON: {exc}", file=sys.stderr)
        return 2

    result = evaluate_proposed_action(payload)
    prefix = "ALLOW" if result.get("allowed") else "BLOCK"
    stream = sys.stdout if result.get("allowed") else sys.stderr
    print(f"{prefix} action-gate decision={result.get('decision')} reason={result.get('reason')}", file=stream)
    if result.get("missing"):
        print(f"missing_evidence={','.join(result['missing'])}", file=stream)
    return 0 if result.get("allowed") else 1


if __name__ == "__main__":
    raise SystemExit(_main())
