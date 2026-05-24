---
name: crm-log
description: Log interactions and update in-scope CRM records with stage, next step, contacts, and account context.
argument-hint: "<account, opportunity, contact, or interaction reference>"
---

# /crm-log

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Update CRM hygiene by running triage -> synthesize -> draft -> ACT -> log. Only touch records the user can already edit and only inside the requested scope.

## Usage

```
/crm-log $ARGUMENTS
```

## Workflow

1. **TRIAGE**: Identify CRM scope and interaction sources from ~~CRM, ~~email, ~~meeting notes, and ~~chat.
2. **SYNTHESIZE**: Use `search-strategy`, `knowledge-synthesis`, and `source-management` to ground activity logs and field updates in cited evidence.
3. **DRAFT**: Prepare activity notes, next steps, contact edits, and before/after field changes.
4. **ACT**: Consult `skills/action-safety`. Stage/forecast overwrites require confirmation; bulk or destructive CRM changes escalate.
5. **LOG**: Record every CRM write, record ID, before/after value, evidence ID, and gate decision.

## Done

An up-to-date CRM record with logged interactions and gated updates to stage, next step, or contacts.
