---
name: rollup
description: Synthesize recent work across tools and metrics, draft the stakeholder update in the audience's register, and post or send it through a gated delivery step. Use for weekly updates, exec rollups, launch status, and cross-team status posts.
argument-hint: "<audience, cadence, project, and delivery channel>"
---

# Stakeholder Rollup

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Run the Enterprise Actions loop for stakeholder updates: triage -> synthesize -> draft -> ACT -> log.

This is not `/digest`. `/digest` summarizes activity for the user and stops. `/rollup` synthesizes the week, drafts in the stakeholder audience's register, and delivers the artifact to that audience through a gated post or send. A draft that is not posted or sent is incomplete unless the gate blocks delivery.

## Workflow

### 1. TRIAGE

Identify audience, cadence, delivery channel, scope, and required register:

- executive or leadership
- cross-functional stakeholders
- engineering team
- launch team
- customer-facing status group

Determine which facts require metric precision, which items need an ask, and which updates are safe to omit.

### 2. SYNTHESIZE

Use `skills/search-strategy`, `skills/knowledge-synthesis`, and `skills/source-management` to gather:

- **~~chat**: decisions, blockers, asks
- **~~knowledge base**: plans, specs, status docs
- **~~project tracker**: completed, in-progress, at-risk, and blocked work
- **~~analytics**: metrics, adoption, incidents, revenue, funnel, or usage signals
- **~~email**: stakeholder asks and prior update threads

Every factual statement and number must cite a source. Conflicting numbers escalate instead of being averaged or guessed.

### 3. DRAFT

Draft the stakeholder artifact:

- title and time range
- TL;DR
- progress, risks, asks, next milestones
- cited metrics and source notes
- audience-specific tone and detail
- delivery target and recipients

Make the delta from `/digest` visible in the draft: this is a message to stakeholders, not a private summary for the user.

### 4. ACT

Consult `skills/action-safety` before posting or sending. Delivery is load-bearing; do not stop at the draft.

Hard gates:

- Numbers to leadership -> `numbers_to_leadership` and confirm.
- Wide channel post or external send -> `external_send` or high blast radius and confirm.
- Uncited metrics, low confidence, or conflicting sources -> escalate.

Post to ~~chat, send via ~~email, or update the stakeholder artifact in ~~knowledge base only after the gate allows it. If the user declines confirmation, log the blocked delivery and mark the run incomplete rather than calling the draft done.

### 5. LOG

Append ledger entries for the rollup draft and delivery action with evidence IDs, gate decision, actor `enterprise-actions/rollup`, target connector category, recipients/channel, and time range.

## Done Artifact

A stakeholder-targeted rollup that is posted or sent after confirmation when required. `/digest` stops at a private summary; `/rollup` delivers.
