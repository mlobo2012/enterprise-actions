---
name: action-safety
description: Apply Enterprise Actions' deterministic safety gate before any write, send, overwrite, commitment, leadership-number, bulk, or destructive action. Use before the ACT step of every acting workflow.
argument-hint: "<proposed action JSON or action description>"
user-invocable: false
---

# Action Safety

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Action Safety is the trust gate every Enterprise Actions skill must consult before the ACT step. It is not optional prose guidance. The runtime implementation lives in `lib/action_safety.py`, `lib/action_ledger.py`, and `hooks/action-gate.sh`.

## Gate Contract

Before any write or external action, build a proposed-action record:

```
{
  "what": "short description of the action",
  "why": "why this action closes the loop",
  "action_class": "external_send | overwrite_trusted_record | commitment_on_others_behalf | numbers_to_leadership | bulk_destructive | null",
  "reversibility": "reversible | irreversible",
  "blast_radius": "low | medium | high | conflict",
  "confidence": 0.0,
  "sources_cited": true,
  "evidence_ids": ["retrieved-source-id"],
  "known_ids": ["retrieved-source-id"]
}
```

Then run the gate:

```
classify(reversibility, blast_radius, confidence, sources_cited) -> auto | confirm | escalate
```

Use the decision exactly:

- `auto`: the action may run through the connected MCP tool and must be logged.
- `confirm`: show the exact diff, destination, recipients, and evidence; act only after explicit user confirmation.
- `escalate`: do not act. Surface the conflict, missing evidence, or risk and ask for a human decision.

## Five Hard-Gated Action Classes

These classes are always forced to `confirm` or `escalate`; they can never be `auto`:

| Class | Examples | Minimum gate |
|---|---|---|
| `external_send` | Customer email, prospect reply, ticket response leaving the company | `confirm` |
| `overwrite_trusted_record` | CRM stage or forecast, closing work, marking a ticket done | `confirm` |
| `commitment_on_others_behalf` | Assigning work, setting due dates, promising another team's delivery | `confirm` |
| `numbers_to_leadership` | Metrics or forecast numbers in stakeholder and executive updates | `confirm` |
| `bulk_destructive` | Mass archive, delete, bulk reassign, bulk close | `escalate` |

## Evidence Rules

- Every factual claim in a drafted artifact must cite a real synthesized source.
- `evidence_ids` must resolve against retrieved `known_ids`; fabricated or unresolved IDs block the action.
- Empty evidence is not acceptable for acting workflows. If the action is purely mechanical, record the source that justifies the mechanical operation, such as the queue item or ticket ID.
- Low confidence or conflicting sources escalates. Do not ask the user to confirm a hallucination.

## Ledger Rules

After every allowed action, append to the action ledger:

```
{
  "what": "...",
  "why": "...",
  "evidence_ids": ["..."],
  "reversibility": "reversible",
  "blast_radius": "low",
  "gate_decision": "auto | confirm",
  "actor": "enterprise-actions/<skill-name>",
  "target": "~~chat | ~~email | ~~ticketing | ~~project tracker | ~~CRM | ~~meeting notes | ~~knowledge base | ~~analytics"
}
```

The ledger is append-only. Do not rewrite or delete prior entries.
