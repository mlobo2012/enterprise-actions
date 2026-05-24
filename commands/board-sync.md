---
name: board-sync
description: Detect chat-vs-tracker drift, then update statuses, flag blockers with evidence, and draft owner nudges.
argument-hint: "<board, project, sprint, or timeframe>"
---

# /board-sync

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Fix board drift by running triage -> synthesize -> draft -> ACT -> log. The applied status write is the hard done step; a drift report alone is incomplete.

## Usage

```
/board-sync $ARGUMENTS
```

## Workflow

1. **TRIAGE**: Load the target board from ~~project tracker and related evidence from ~~chat. Classify stale, blocked, done-but-open, and conflicted items.
2. **SYNTHESIZE**: Use `search-strategy`, `knowledge-synthesis`, and `source-management` to compare tracker status against cited chat evidence.
3. **DRAFT**: Prepare exact before/after status changes, blocker flags, and owner nudges.
4. **ACT**: Consult `skills/action-safety`. Apply allowed status writes. Closing, moving to Done, trusted status overwrites, assignments, and bulk moves require confirm/escalate.
5. **LOG**: Record each status change, blocker flag, nudge, evidence ID, and gate decision.

## Done

A current board with status writes applied or explicitly held at confirmation, plus blocker list and nudges.
