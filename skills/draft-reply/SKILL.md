---
name: draft-reply
description: Synthesize context for a message, email, or ticket, then draft a cited reply in the user's voice and stage or send it through the appropriate connector. Use for customer replies, internal threads, and ticket responses.
argument-hint: "<message, email, ticket, thread, or reply goal>"
---

# Draft Reply

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Run the Enterprise Actions loop for replies: triage -> synthesize -> draft -> ACT -> log. The artifact is a staged draft or a sent reply, not a summary.

## Workflow

### 1. TRIAGE

Identify the reply target, channel, audience, urgency, and whether the response is internal or external. Determine the reply's needed action: answer, defer, ask a clarifying question, commit to a next step, or route to another owner.

### 2. SYNTHESIZE

Use `skills/search-strategy`, `skills/knowledge-synthesis`, and `skills/source-management` to gather context from:

- **~~chat**: related threads and decisions
- **~~email**: prior correspondence
- **~~ticketing**: support or issue history
- **~~project tracker**: status, owners, dates
- **~~CRM**: account context and contacts
- **~~knowledge base**: policy, product, or process references

Every factual claim in the reply must cite a synthesized source. If a claim cannot be cited, remove it or ask for human input.

### 3. DRAFT

Draft a reply in the user's voice. Include:

- direct answer or next step
- source-backed facts
- clear owner/date only when supported
- concise signoff appropriate to the channel
- citations or source notes visible for review

### 4. ACT

Consult `skills/action-safety` before staging or sending.

Allowed low-risk examples:

- Create an internal draft with cited facts.
- Add a private ticket note or suggested response.

Hard gates:

- Any message sent to a customer, prospect, vendor, or outside party -> `external_send` and confirm.
- Any reply that commits another person or team to work -> `commitment_on_others_behalf` and confirm.
- Any uncited claim, low confidence, or conflicting source -> escalate.

Create the draft in ~~chat, ~~email, ~~ticketing, or ~~CRM. Send only after an explicit confirmation gate when the destination is external or wide.

### 5. LOG

Append one ledger entry with the draft/send action, recipients or channel, evidence IDs, gate decision, actor `enterprise-actions/draft-reply`, and target connector category.

## Done Artifact

A staged cited draft, or a sent reply after confirmation. External sends always require confirmation.
