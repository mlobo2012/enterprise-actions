---
name: draft-reply
description: Synthesize context for a message, email, or ticket, then draft a cited reply in the user's voice and stage or send it.
argument-hint: "<message, email, ticket, thread, or reply goal>"
---

# /draft-reply

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Draft and stage or send a cited reply by running triage -> synthesize -> draft -> ACT -> log.

## Usage

```
/draft-reply $ARGUMENTS
```

## Workflow

1. **TRIAGE**: Identify the reply target, audience, urgency, channel, and whether the send is internal or external.
2. **SYNTHESIZE**: Use `search-strategy`, `knowledge-synthesis`, and `source-management` across ~~chat, ~~email, ~~ticketing, ~~project tracker, ~~CRM, and ~~knowledge base.
3. **DRAFT**: Write the reply in the user's voice with every factual claim cited.
4. **ACT**: Consult `skills/action-safety`. Stage safe internal drafts. External sends are `external_send` and always require confirmation.
5. **LOG**: Record draft or send details, evidence, recipients, and gate decision.

## Done

A staged cited draft, or a sent reply after confirmation.
