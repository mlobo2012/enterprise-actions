---
name: triage
description: Classify and rank an inbound queue, then label, prioritize, assign, snooze, or route items across chat, email, ticketing, and project trackers. Use for morning queue cleanup, backlog intake, or catching up after time away.
argument-hint: "<queue scope, timeframe, and routing rules>"
---

# Queue Triage

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Run the Enterprise Actions loop for queue cleanup: triage -> synthesize -> draft -> ACT -> log. This skill must mutate the queue; a ranked report alone is incomplete.

## Workflow

### 1. TRIAGE

Pull the requested queue from available sources:

- **~~chat**: mentions, DMs, channel asks, threads needing response
- **~~email**: unread inbox, starred mail, direct requests, pending threads
- **~~ticketing**: intake tickets, unassigned tickets, SLA risk
- **~~project tracker**: assigned issues, stale issues, blocked items

Classify each item by type, urgency, owner, needed action, reversibility, blast radius, and evidence ID. Rank the queue by urgency, user ownership, deadline, customer impact, and whether another person is blocked.

### 2. SYNTHESIZE

Use `skills/search-strategy`, `skills/knowledge-synthesis`, and `skills/source-management` to gather cross-tool context for the top items. Deduplicate duplicate asks across ~~chat, ~~email, ~~ticketing, and ~~project tracker. Every recommendation must cite the source item or synthesized source.

### 3. DRAFT

Draft the concrete queue mutations:

- labels to apply
- priority changes
- assignee changes
- snooze dates
- routing destinations
- owner nudges
- open-loop list for items that cannot be safely routed

Show the proposed queue diff before ACT when the action affects many items or changes ownership.

### 4. ACT

Consult `skills/action-safety` before every write. Run the gate for each proposed queue mutation.

Allowed low-risk examples:

- Apply a reversible internal label backed by a cited queue item.
- Add a private triage note to a ticket.
- Snooze a personal inbox item with clear source evidence.

Hard gates:

- Bulk archive, bulk close, bulk reassign, delete, or mass snooze -> `bulk_destructive` and confirm/escalate.
- Auto-archive or any destructive queue cleanup -> confirm/escalate.
- Assigning someone else or setting a deadline for them -> `commitment_on_others_behalf` and confirm.

Apply safe mutations through ~~chat, ~~email, ~~ticketing, or ~~project tracker. Do not stop after ranking.

### 5. LOG

Append one ledger entry per action with what changed, why, evidence IDs, reversibility, gate decision, actor `enterprise-actions/triage`, and target connector category.

## Done Artifact

A sorted and owned queue with labels, priorities, assignments, snoozes, or routes applied, plus an open-loops list for anything blocked by missing evidence or confirmation.
