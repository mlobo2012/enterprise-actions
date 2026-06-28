# Enterprise Actions

**Your tools already tell you what happened. Enterprise Actions does something about it.**

Enterprise Actions is a plugin for [Cowork](https://claude.com/product/cowork) —
Anthropic's agentic desktop application — and Claude Code. It is built directly on top of
Anthropic's **[enterprise-search](https://github.com/anthropics/knowledge-work-plugins/tree/main/enterprise-search)**
plugin, and it adds the one thing enterprise-search deliberately leaves to you: **the work
after the answer.**

enterprise-search finds things across all your connected tools and hands you a tidy
summary. Then you still triage the queue, gather the context, write the reply, file the
ticket, update the board, and send the rollup — by hand. Enterprise Actions runs that loop
for you: it **triages, synthesizes, drafts, and acts** across Slack, Gmail, Linear, Jira,
Asana, Notion, Confluence, Intercom, Salesforce, Fireflies and the rest of your stack —
and it never takes a risky action without your say-so.

## Install

**Claude Cowork (recommended):** download
**[enterprise-actions-cowork-plugin.zip](https://github.com/mlobo2012/enterprise-actions/releases/latest/download/enterprise-actions-cowork-plugin.zip)**
(or from the [AI Heroes page](https://www.ai-heroes.co/en-gb/free-tools/enterprise-actions)),
then in Cowork open **Customize -> create and upload plugins**, upload the zip, and install
**Enterprise Actions**.

**Claude Code:**

```
/plugin marketplace add mlobo2012/enterprise-actions
/plugin install enterprise-actions
```

---

## Why this exists

Most of your day is not spent *finding* information. Surveys put **58–60% of the workday
on "work about work"** — communicating, chasing status, switching tools — versus a third on
the actual skilled work ([Asana](https://asana.com/resources/anatomy-of-work)). McKinsey's
classic time split is **28% email + 14% internal communication versus only 19% searching**
([McKinsey](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/the-social-economy)).
Search tools attack the 19%. The 42%+ — triaging, drafting, coordinating, following up —
is still done by a human, one tab at a time.

Enterprise Actions goes after that 42%. Not by being smarter at search — by **closing the
loop** that search opens.

---

## Built on enterprise-search (and honest about it)

Enterprise Actions does **not** reimplement search. It keeps Anthropic's three
enterprise-search retrieval skills **byte-identical** and calls them as its context engine:

| Kept from enterprise-search (unchanged) | What Enterprise Actions uses it for |
|---|---|
| `search-strategy` | gathers cross-tool context before any action |
| `knowledge-synthesis` | dedupes, attributes, and confidence-scores that context |
| `source-management` | checks which connectors are live and in-scope first |
| `/search` and `/digest` | retained verbatim — your out-of-the-box search and daily/weekly digest still work exactly as before |

**They retrieve; we close the loop.** That is the whole value-add, and the boundary is
deliberately crisp.

---

## What it does

Every Enterprise Actions agent runs the same five-step loop:
**triage → synthesize → draft → act → log.** The synthesize step *is* enterprise-search.
The act step is new — and it is always governed (see [Safety](#safety-acting-without-the-risk)).

### `/triage` — clear the queue, don't just read it

Pulls your unread inbox, Slack mentions, assigned tickets, and board items into one ranked
queue, classifies each by urgency, type, and owner — then **acts**: labels, sets priority,
assigns, snoozes, and routes. You get back a sorted, owned queue and a short list of open
loops, instead of 200 unreads.

> *Monday, 8:50am. Instead of 40 minutes of inbox archaeology, `/triage` hands you a queue
> where the three things that actually need you are at the top, the FYIs are labeled and
> filed, and two threads have already been routed to the right owner.*

**Use it for:** the morning inbox/Slack pile-up · support queue intake · "what did I miss
while I was out."

### `/draft-reply` — the reply, written and ready to send

For any message, email, or ticket, it synthesizes the full thread plus related docs and
account history, then **drafts a reply in your voice** with every factual claim cited to a
real source. Internal drafts are staged automatically; **anything sent to an outside party
waits for your explicit confirmation.**

> *A customer asks where their integration stands. `/draft-reply` reads the Slack thread,
> the Linear ticket, and the last two emails, and stages a reply that quotes the actual
> ship date from the ticket — not a guess. You read it, tweak one line, hit send.*

**Use it for:** customer and prospect replies · long internal threads · ticket responses.

### `/meeting-to-work` — turn the meeting into tracked work

Takes a meeting transcript or notes, extracts the decisions and action items, and **acts**:
files real tickets with owners and due dates, drafts the follow-up emails, and posts a clean
recap to the channel. No more meetings where the majority of attendees leave unsure who owns
what — a problem **54% of meetings** have
([Fellow](https://fellow.ai/resources/state-of-meetings-2024)).

> *The planning call ends. By the time you're back at your desk, the four decisions are a
> posted recap and the six action items are Linear tickets with owners — each one waiting
> for your confirm before it pings anyone.*

**Use it for:** planning and standup meetings · client calls · incident retros.

### `/board-sync` — keep the board honest

Compares what your chat says is happening against what the tracker shows, finds the **drift**
("this shipped Tuesday but the ticket's still In Progress"), and **acts**: updates statuses,
flags real blockers with the evidence attached, and drafts nudges to the owners. Moving or
closing a ticket always asks first.

> *Friday. `/board-sync` notices five tickets whose Slack threads say "done" while the board
> says "in progress," flags one genuinely blocked item with a link to the blocking thread,
> and drafts three short nudges — then waits for you to approve the status changes.*

**Use it for:** end-of-week board hygiene · sprint cleanup · blocker chasing.

### `/rollup` — the stakeholder update, drafted *and delivered*

This is **not** `/digest`. `/digest` summarizes activity *for you* and stops. `/rollup`
synthesizes the week across tools and metrics, **drafts it in your stakeholders' register**,
and **delivers it** — posts to the channel or sends the email. Because it can put numbers in
front of leadership, every metric and every wide send is held for your confirmation.

> *`/rollup --weekly` assembles the exec update from Linear, Notion, and your analytics,
> drafts it the way your VP likes to read it, and shows it to you with the two metrics
> highlighted for a final check before it posts.*

**Use it for:** weekly stakeholder/exec updates · launch status · cross-team status posts.

### `/crm-log` — the CRM hygiene nobody wants to do

Logs your calls, emails, and meetings against the right account and **updates stage,
next-step, and contacts** — the data-entry chore **68% of sellers call their #1 time sink,
and only 2% trust** ([Salesforce](https://www.salesforce.com/news/stories/sales-research-2023/)).
Overwriting a stage or forecast always asks first, and it only ever touches records you
already have permission to edit.

> *After a customer call, `/crm-log` reads the Fireflies transcript, logs the notes to the
> opportunity, sets the next step and date, and proposes moving the stage — then waits for
> your nod before changing the forecast number anyone relies on.*

**Use it for:** post-call CRM updates · pipeline hygiene · contact maintenance.

---

## Safety: acting without the risk

Acting agents are only useful if you can trust them not to do something irreversible and
wrong. Enterprise Actions ships a **deterministic action-safety gate** on every write or
external action — the propose → approve → execute pattern the serious enterprise players
converged on. (We are not unique in having a gate; Glean and Dust ship versions of it too.
We're unique in shipping cross-vendor acting *as a lightweight plugin on the seats and
connectors you already have* — see below.)

Every action is classified by **reversibility × blast-radius × confidence × evidence**:

- **Reversible, confident, every claim cited** (apply a label, stage a draft, add a private
  comment, create a ticket assigned to yourself) → can run, and is logged so you can undo it.
- **Five action classes are always held for your confirmation** — never auto-fired:
  1. Anything **sent to an outside party** (customer/prospect emails, ticket replies)
  2. Anything that **overwrites a trusted record** (CRM stage/forecast, closing tickets, marking work "done")
  3. **Commitments on someone else's behalf** (assigning tasks, due dates, promises)
  4. **Numbers put in front of leadership** (metrics in rollups and status)
  5. **Bulk or destructive operations** (mass archive, delete, reassign)
- **Uncited claim, low confidence, or conflicting sources** → blocked or escalated, with the
  conflict shown.

Two more guarantees:

- **Evidence-grounded actions.** Every factual claim in anything it drafts must cite a real
  retrieved source. An action whose evidence doesn't check out is rejected — anti-
  hallucination for *actions*, not just answers.
- **A full action ledger.** Every action it takes is logged — what, why, the evidence, and
  whether it was reversible — so there's always an audit trail.

It also never acts outside your own connector permissions: if you can't do it by hand,
neither can the agent.

---

## What makes it different

- **vs. enterprise-search (out-of-the-box):** enterprise-search retrieves and stops.
  Enterprise Actions runs triage → synthesize → draft → **act → log** on top of it. You keep
  `/search` and `/digest` unchanged and gain six acting agents.
- **vs. heavyweight platforms** (Glean, Moveworks, Copilot Studio): those need their own
  index, their own seats, and an admin rollout. Enterprise Actions is a plugin you install in
  minutes that rides the Cowork seats and MCP connectors you've **already** authorized.
- **vs. single-vendor agents** (Notion-in-Notion, Atlassian Rovo, Salesforce Agentforce,
  Sierra): those act inside one product. Enterprise Actions acts **across** your whole stack —
  a Slack thread becomes a Linear ticket becomes a customer reply becomes a CRM update.

The real moat is distribution: **nobody else ships cross-vendor acting at near-zero adoption
friction, on your existing Anthropic surface, built on Anthropic's own retrieval.**

---

## Installation

**Claude Cowork (recommended).** Download
[enterprise-actions-cowork-plugin.zip](https://github.com/mlobo2012/enterprise-actions/releases/latest/download/enterprise-actions-cowork-plugin.zip),
open Cowork, go to **Customize -> create and upload plugins**, upload the zip, and install it.

**Claude Code.** Run:

```
/plugin marketplace add mlobo2012/enterprise-actions
/plugin install enterprise-actions
```

Enterprise Actions uses the same tool-agnostic connector model as enterprise-search — it
works with whatever you've connected in each category (chat, email, cloud storage, knowledge
base, project tracker, CRM, meeting notes, analytics). See
[CONNECTORS.md](./CONNECTORS.md) for the full list and how to add sources.

**Requirements:** Cowork or Claude Code, and at least one connected MCP source. The more
sources you connect, the more of the loop Enterprise Actions can close.

---

## Commands at a glance

| Command | What it does | Always asks first when… |
|---|---|---|
| `/triage` | sorts + labels + routes your queue | bulk archive / destructive ops |
| `/draft-reply` | drafts a cited reply, stages or sends | sending to an outside party |
| `/meeting-to-work` | files tickets + drafts follow-ups from a meeting | committing others to work |
| `/board-sync` | fixes status drift, flags blockers, nudges owners | closing/moving a ticket |
| `/rollup` | drafts **and delivers** the stakeholder update | numbers to leadership / wide sends |
| `/crm-log` | logs interactions, updates the record | overwriting stage/forecast |
| `/search` | *(retained from enterprise-search)* cross-tool search | — |
| `/digest` | *(retained from enterprise-search)* daily/weekly summary | — |

---

*Built on Anthropic's enterprise-search plugin. Enterprise Actions is the layer that closes
the loop — safely.*
