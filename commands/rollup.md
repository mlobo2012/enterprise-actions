---
name: rollup
description: Synthesize recent work and metrics, draft the stakeholder update in the audience's register, and post or send it through a gated delivery step.
argument-hint: "<audience, cadence, project, and delivery channel>"
---

# /rollup

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Deliver a stakeholder update by running triage -> synthesize -> draft -> ACT -> log.

This is not `/digest`: `/digest` summarizes for you and stops; `/rollup` drafts in the audience's register and posts or sends the artifact. A draft without delivery is incomplete unless the gate blocks delivery.

## Usage

```
/rollup $ARGUMENTS
```

## Workflow

1. **TRIAGE**: Identify audience, cadence, scope, delivery channel, and required register.
2. **SYNTHESIZE**: Use `search-strategy`, `knowledge-synthesis`, and `source-management` across ~~chat, ~~knowledge base, ~~project tracker, ~~analytics, and ~~email.
3. **DRAFT**: Prepare the stakeholder update with cited facts, cited metrics, risks, asks, and next milestones.
4. **ACT**: Consult `skills/action-safety`. Numbers to leadership and wide sends require confirmation; uncited or conflicting metrics escalate.
5. **LOG**: Record the draft, delivery action, recipients/channel, evidence IDs, and gate decision.

## Done

A stakeholder-targeted rollup posted or sent after confirmation when required.
