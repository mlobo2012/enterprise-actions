---
name: crm-log
description: Log interactions and update in-scope CRM records with stage, next step, contacts, and account context. Use after calls, email threads, meetings, or customer conversations.
argument-hint: "<account, opportunity, contact, or interaction reference>"
---

# CRM Log

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Run the Enterprise Actions loop for CRM hygiene: triage -> synthesize -> draft -> ACT -> log. This skill only touches records the user can already edit and only within the requested account, contact, or opportunity scope.

## Workflow

### 1. TRIAGE

Identify the CRM scope and interaction sources:

- **~~CRM**: account, opportunity, contact, activity history
- **~~email**: customer or prospect correspondence
- **~~meeting notes**: call transcript or notes
- **~~chat**: internal account discussion

Determine whether the requested update is a simple activity log, next-step update, contact update, stage update, forecast update, or out-of-scope change.

### 2. SYNTHESIZE

Use `skills/search-strategy`, `skills/knowledge-synthesis`, and `skills/source-management` to gather the interaction context and deduplicate across sources. Cite every CRM note, stage rationale, next step, and contact detail to a real source.

If the record is ambiguous, out of scope, or not editable by the user, stop and ask for clarification.

### 3. DRAFT

Draft the CRM changes:

- activity log summary
- linked emails, calls, or meetings
- next step and date
- contact additions or corrections
- proposed stage or forecast change
- fields that should remain unchanged

Show before and after values for every trusted field.

### 4. ACT

Consult `skills/action-safety` before every write.

Allowed low-risk examples:

- Add a cited activity note to the correct account.
- Update a next-step field when the user is the owner and the source is explicit.

Hard gates:

- Stage, forecast, close date, amount, or other trusted record overwrite -> `overwrite_trusted_record` and confirm.
- Commitments on behalf of account owners, CS, sales, or delivery teams -> `commitment_on_others_behalf` and confirm.
- Bulk account updates or destructive merges -> `bulk_destructive` and escalate.

Apply only in-scope writes through ~~CRM. Do not infer a stage or forecast from weak evidence.

### 5. LOG

Append ledger entries for every CRM write with evidence IDs, gate decision, actor `enterprise-actions/crm-log`, target connector category, record ID, and before/after values.

## Done Artifact

An up-to-date, trustworthy CRM record with logged interactions and gated updates to stage, next step, or contacts. Stage and forecast overwrites always require confirmation.
