---
name: triage
description: Classify and rank your inbound queue, then label, prioritize, assign, snooze, or route items across chat, email, ticketing, and project trackers.
argument-hint: "<queue scope, timeframe, and routing rules>"
---

# /triage

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Clear a queue by running triage -> synthesize -> draft -> ACT -> log. This command must produce a mutated queue, not just a ranked report.

## Usage

```
/triage $ARGUMENTS
```

## Workflow

1. **TRIAGE**: Pull queue items from ~~chat, ~~email, ~~ticketing, and ~~project tracker. Classify by urgency, owner, type, needed action, reversibility, and evidence.
2. **SYNTHESIZE**: Use `search-strategy`, `knowledge-synthesis`, and `source-management` to gather and cite cross-tool context.
3. **DRAFT**: Prepare labels, priority changes, assignments, snoozes, routes, and an open-loops list.
4. **ACT**: Consult `skills/action-safety` before any write. Apply safe labels/routes/snoozes; hold bulk archive, destructive cleanup, or commitments on others' behalf for confirm/escalate.
5. **LOG**: Append every queue mutation to the action ledger.

## Done

A sorted, owned queue with actual labels, priorities, assignments, snoozes, or routes applied, plus open loops for blocked items.
