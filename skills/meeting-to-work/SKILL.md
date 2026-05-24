---
name: meeting-to-work
description: Turn meeting notes or transcripts into tracked work by extracting decisions and action items, filing tickets with owners and due dates, drafting follow-ups, and posting a recap.
argument-hint: "<meeting notes, transcript, or meeting reference>"
---

# Meeting To Work

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Run the Enterprise Actions loop for meetings: triage -> synthesize -> draft -> ACT -> log. The meeting is not closed until work is filed or the recap/follow-up is posted through the gate.

## Workflow

### 1. TRIAGE

Load the meeting from **~~meeting notes** or the user-provided transcript. Identify:

- decisions
- action items
- owners
- due dates
- unresolved questions
- dependencies and blockers
- audience for recap and follow-ups

Classify each proposed action by reversibility, blast radius, confidence, and whether it commits someone else.

### 2. SYNTHESIZE

Use `skills/search-strategy`, `skills/knowledge-synthesis`, and `skills/source-management` to connect the meeting content to:

- **~~project tracker**: existing epics, tickets, owners, milestones
- **~~chat**: related discussion threads
- **~~email**: prior commitments
- **~~knowledge base**: specs, decisions, policies

Merge duplicate action items with existing work. Cite the source transcript section or related system of record for every ticket and recap claim.

### 3. DRAFT

Draft the work package:

- tickets with title, description, owner, due date, source evidence, and linked meeting
- follow-up messages or emails for attendees
- recap with decisions, action items, owners, due dates, and open questions
- exceptions list for ambiguous or uncited items

### 4. ACT

Consult `skills/action-safety` before every write.

Allowed low-risk examples:

- Create a ticket assigned to the user when the source clearly asks the user to own it.
- Add a private draft recap with citations.

Hard gates:

- Assigning work to someone else, setting a due date for them, or promising delivery -> `commitment_on_others_behalf` and confirm.
- Posting a recap to a broad channel or sending it outside the team -> confirm.
- Closing or overwriting existing tracked work -> `overwrite_trusted_record` and confirm.

File tickets in ~~project tracker, draft follow-ups in ~~chat or ~~email, and post the recap after the gate decision allows it.

### 5. LOG

Append ledger entries for every ticket, follow-up draft/send, and recap post with evidence IDs, gate decision, actor `enterprise-actions/meeting-to-work`, and target connector category.

## Done Artifact

Real tickets with owners and due dates, plus a posted recap or staged follow-up package. Commitments on others' behalf require confirmation.
