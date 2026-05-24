---
name: board-sync
description: Detect chat-vs-tracker drift, then update project tracker statuses, flag blockers with evidence, and draft owner nudges. Use for sprint cleanup, board hygiene, and blocker chasing.
argument-hint: "<board, project, sprint, or timeframe>"
---

# Board Sync

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Run the Enterprise Actions loop for board hygiene: triage -> synthesize -> draft -> ACT -> log. The applied status write is the headline and hard done step. A drift report without a tracker write or gated write attempt is incomplete.

## Workflow

### 1. TRIAGE

Load the target board, sprint, milestone, or project from **~~project tracker**. Pull related **~~chat** threads and comments. Classify each item as current, stale, blocked, done-but-open, open-but-claimed-done, owner-missing, or status-conflicted.

### 2. SYNTHESIZE

Use `skills/search-strategy`, `skills/knowledge-synthesis`, and `skills/source-management` to compare tracker state against chat evidence:

- status claims in ~~chat
- ticket comments and status history in ~~project tracker
- linked docs or specs in ~~knowledge base when needed

Each proposed status change must cite the tracker item and the evidence that justifies the change. Conflicting sources escalate.

### 3. DRAFT

Draft the exact board diff:

- status updates to apply
- blocker flags with evidence links
- owner nudges
- items requiring confirmation
- items blocked by missing or conflicting evidence

For every tracker mutation, include before state, after state, source evidence, and reversibility.

### 4. ACT

Consult `skills/action-safety` before every write. This step must fire when drift exists; do not stop at a report.

Allowed low-risk examples:

- Add a cited blocker note to an issue.
- Draft an owner nudge in ~~chat.

Hard gates:

- Closing an issue, moving it to Done, changing a trusted status, or overwriting status fields -> `overwrite_trusted_record` and confirm.
- Assigning a new owner or due date -> `commitment_on_others_behalf` and confirm.
- Bulk moving issues -> `bulk_destructive` and confirm/escalate.

Apply allowed status updates in ~~project tracker, flag blockers with evidence, and stage or send owner nudges through ~~chat as the gate allows. If every proposed status write is blocked, report the run as incomplete with the gate reason.

### 5. LOG

Append ledger entries for each status change, blocker flag, and nudge with evidence IDs, gate decision, actor `enterprise-actions/board-sync`, and target connector category.

## Done Artifact

A current board with status writes applied or explicitly held at confirmation, plus a blocker list and owner nudges. The status write path is mandatory when drift exists.
