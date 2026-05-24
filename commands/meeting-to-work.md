---
name: meeting-to-work
description: Turn meeting notes into tracked work by filing tickets with owners and due dates, drafting follow-ups, and posting a recap.
argument-hint: "<meeting notes, transcript, or meeting reference>"
---

# /meeting-to-work

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Turn a meeting into tracked work by running triage -> synthesize -> draft -> ACT -> log.

## Usage

```
/meeting-to-work $ARGUMENTS
```

## Workflow

1. **TRIAGE**: Extract decisions, action items, owners, due dates, unresolved questions, and dependencies from ~~meeting notes.
2. **SYNTHESIZE**: Use `search-strategy`, `knowledge-synthesis`, and `source-management` across ~~project tracker, ~~chat, ~~email, and ~~knowledge base.
3. **DRAFT**: Prepare tickets, follow-ups, recap, and exceptions with citations.
4. **ACT**: Consult `skills/action-safety`. File tickets and post recap only through the gate. Commitments on others' behalf require confirmation.
5. **LOG**: Record every ticket, follow-up, recap, evidence ID, and gate decision.

## Done

Real tickets with owners and due dates, plus a posted recap or staged follow-up package.
