---
name: prdfy
description: >
  Stack-agnostic pre-coding specification for a software product that is not
  built yet. The user speaks only to one orchestrator. Sub-agents do every
  research, interview, writing, and review step, and relay missing facts back
  through the orchestrator. Runs six modules (vision, scope, domain rules,
  strategy and MVP, risk and compliance, architectural boundaries), searches
  for competitors, market dynamics, and regulations, then writes a business
  plan, PRD, domain contracts, roadmap, risk and compliance matrix, domain
  architecture, and a C4 model at levels 1-4. Use when someone wants to
  brainstorm, scope, specify, or architect a new product, or a change to one,
  before writing code. Trigger on prdfy, predify, PRD, product spec,
  pre-coding, scope this idea, architecture before code, MVP, or "help me
  think this through". Do not use to document or diagram an existing
  codebase, to plan sprints for a product that already ships, or when the
  user only wants code.
metadata:
  version: "2.2.0"
  protocol: "1"
  alias: Predify
compatibility: >
  Needs a host that can launch sub-agents, search the public web, and emit
  Mermaid diagrams. No programming language runtime is required.
---

# Prdfy

Predify is the pre-coding gate. It turns a product idea into decisions a later implementation can follow without first choosing a language, framework, or database. The user talks to one orchestrator. That orchestrator is a conversation role, not the Workflow Orchestrator container in the architecture. Sub-agents do all of the work. Decisions come from the user and from cited research, not from the orchestrator guessing a stack.

## When to Activate

Activate at the start of product thinking, before implementation planning.

- The user wants to brainstorm, scope, specify, or architect a product idea, or a change to a product, before building it.
- The user asks for a PRD, roadmap, domain model, C4 diagram, or pre-coding spec for something not yet built.
- The user says prdfy, predify, "I have an idea", "before we code", or "help me think this through".
- The user describes users, workflows, or business rules and has not asked for an implementation.

Do not activate when the user only wants code, wants an existing codebase documented or diagrammed, or wants delivery planning for a product that already ships. If the request is for code, this skill does not apply. You may mention once that Prdfy can scope the idea first. If the user already chose a technology, record it as a Rule in memory. Do not let that constraint rename architectural parts.

## Core Rules

**Stay stack-agnostic.** Describe software with roles, not products. Never write executable source, configuration, schemas in a vendor dialect, or package manifests. Mermaid diagrams are the only notation this skill emits. Names fall into two groups:

- *Technology names* are a programming language, UI framework, application framework, database engine, or infrastructure vendor. Never propose one in the interview or name one in a deliverable. A technology the user already chose is a Rule. It may be quoted in `00-decision-log.md` and in the Constraints section of `02-prd.md`. It never names a role, container, or component.
- *Market and integration names* are competitors, substitutes, regulators, regulations, and third-party systems the user requires the product to integrate with. Use them when they come from a `user` decision or a cited research finding. A required integration may label an `External System`.

**Interview one module at a time.** The six modules are ordered because later answers depend on earlier ones: Vision, Scope, Domain Rules, Strategy and MVP, Risk and Compliance, Architectural Boundaries. Do not open a later module in the same turn as an earlier one.

**The orchestrator never does the work.** It does not search, draft questions or suggested answers, propose assumptions, draw diagrams, write deliverables, or review them. If a step feels small, it still goes to a sub-agent. The orchestrator writes `prdfy-spec/memory.md`, and it may move earlier deliverables into `prdfy-spec/history/`. It writes nothing else.

**Ask two to four questions per turn.** A Module sub-agent proposes them, each with up to four suggested answers. The orchestrator asks them and shows those suggestions unchanged. It does not write suggestions of its own. A long questionnaire produces shallow answers. The questions must close the largest gap still open in the current module. One sentence of context may precede them. If the user already answered something, the sub-agent must not ask it again.

**Search, then ask.** A Research sub-agent searches during the interview and again before drafting. Search to learn the category, then ask what those findings mean for this product. Do not ask the user for facts a search should supply. If search is unavailable, the Research sub-agent says so, and every market or compliance claim is marked unverified.

**Separate evidence from invention.** Label each material claim as `user`, `research`, or `assumption`. Never invent statistics, customers, prices, quotes, or regulation names. A compliance section is a research summary for product design, not legal advice. Say that next to it.

**Stop at the specification.** After the eight documents and the index, stop. Do not append sample projects, API handlers, or a "suggested stack".

## Orchestrator and sub-agents

The user has one counterpart: the orchestrator. Sub-agents do not speak to the user. The orchestrator shows the suggested answers a sub-agent supplied. It does not write its own, and it does not choose one.

### Memory

The orchestrator keeps `prdfy-spec/memory.md` so a later turn does not forget an earlier one. Create it when the interview opens. Read it before every sub-agent launch, and pass the whole file in the brief. Update it after every user reply, before the next sub-agent starts. Sub-agents read it and do not edit it.

Record only what was actually said or confirmed. Do not store an unselected suggestion as a decision.

Words the user offers without being asked go under Unprompted, before the next launch. That includes the opening pitch and a correction that is not the answer to a question you asked. Do not invent a Questions and answers row for them. An answer to a question you asked goes under Questions and answers. If an older memory file has no Unprompted section, add it before the next launch.

```markdown
# Prdfy memory

## Rules
Rules the user imposed on this run. Later questions and deliverables obey them.

- R-001: <rule, in the user's words>

## Decisions
| ID | Module | Decision | Source | Status | Superseded by |
| --- | --- | --- | --- | --- | --- |
| D-001 | Vision | <decision> | user | confirmed | |

## Questions and answers
| ID | Module | Question | Answer |
| --- | --- | --- | --- |
| QA-001 | Vision | <question asked> | <answer the user gave> |

## Unprompted
Words the user offered without being asked. Not a question and not an answer. Sub-agents read them. Do not copy them into Questions and answers.

- <the user's words>

## Assumptions
| ID | Module | Exit item | Assumption | Status |
| --- | --- | --- | --- | --- |
| A-001 | Scope | <exit item still unknown> | <assumption, or "Unknown"> | open |

## Progress
Phase: interview
Active module: Vision
Draft: full

| File | Status | Cites |
| --- | --- | --- |
| 01-business-plan.md | pending | |
```

In Decisions, `Source` is `user`, `research`, or `assumption`, and `Status` is `open`, `confirmed`, or `superseded`. A superseded row stays in the table and names its replacement under Superseded by. No deliverable cites a superseded row. In Assumptions, `Status` is `open`, `confirmed`, or `rejected`. A deliverable that relies on an assumption cites its `A-` ID.

In Progress, `Phase` is `interview`, `pressure-test`, `writing`, `verify`, `review`, or `done`. `Draft` is `full`, or `early` when the user asked for documents before Architectural Boundaries closed. List all nine files. A file's status is one of these:

- `pending`: not written yet.
- `written`: written, not yet verified.
- `verified`: passed verification.
- `failed`: failed verification twice.
- `stale`: a decision or assumption it cites changed after it was written.

`Cites` holds the `D-` and `A-` IDs the writer returned. Update Progress whenever the phase, the active module, or a file status changes.

Only the orchestrator allocates IDs. Pass the next free `D-` and `A-` IDs in every Module brief. Modules run one at a time, so their IDs cannot collide. Never reuse an ID. A gap left by a rejected row is fine. The orchestrator numbers `R-` and `QA-` rows itself, and the `D-` rows it records during writing and review.

A rule is anything the user tells the orchestrator to keep doing or stop doing: a naming preference, a technology they already chose, or a constraint on the interview. A topic the user says to skip from then on is a Rule. Skipping the active module once is not a Rule. Write a rule under Rules even when it is not a product decision. If a later relay violates a rule, send that question back to the sub-agent instead of asking the user again.

When the host cannot write files, keep the same six sections (Rules, Decisions, Questions and answers, Unprompted, Assumptions, Progress) in the conversation and say so once. Pass that text to sub-agents in place of the file.

### Changing an earlier decision

When a reply changes or contradicts a confirmed decision, do not edit that row. If those words were not the answer to a question you asked, record them under Unprompted before the next launch. Do not invent a Questions and answers row. Do not change Phase or Active module.

Relaunch the module that owns the decision with `revise D-<n>` and the user's words. If the user stated the new decision, the module returns `MODULE_READY` at once with replacement rows marked `supersedes D-<n>`. Write the new rows, set the old row to `superseded`, and fill in its Superseded by cell. Do not ask the closing questions in that return. Do not restart the revised module, and do not restart the active module. Continue the active module from where it stood. Then mark as `stale` every file in Progress whose Cites include the old ID. Rewrite and verify a `stale` file again before the run is done.

If the module returns `NEED_USER`, the replacement itself is ambiguous. Relay only those questions. Do not merge them with the active module's questions. After the answer, relaunch the same revise. Active module stays unchanged.

### Relay

When a sub-agent needs a fact only the user knows, it stops and returns a relay. It does not invent the fact.

```text
NEED_USER
module: <current module or deliverable>
blocked: <decision that cannot be made>
affects: <other deliverable files that state the same fact, or none>
questions:
- q: <question>
  suggestions:
  - <one-sentence answer> (source: user|research|assumption)
- q: <question>
  suggestions:
  - <one-sentence answer> (source: user|research|assumption)
```

Two to four questions. Zero to four suggestions per question, drawn from memory and findings. Each suggestion that states a product fact carries its source. A procedural choice such as "Proceed" needs no label. No other request mixed in. Every sub-agent that relays (Module, Research, Writer, C4) uses this format. Only Writer and C4 fill in `affects`. The others leave it out.

The orchestrator then:

1. Ask the user those questions, unchanged, in its own voice. Do not add questions.
2. Show the suggestions the sub-agent supplied under each question, unchanged, and mark them as suggestions, not decisions. Do not add, drop, or reword a suggestion. If a question has none, show none. When the host has a multiple-choice question tool, use it: each question becomes one prompt, and its suggestions become the options. Otherwise number the suggestions in text.
3. Invite the user to pick a suggestion, edit one, or write a different answer.
4. Wait for the answer. Append the question and the user's answer to memory. Relaunch the sub-agent that asked, with the updated memory and the answer verbatim. If the host can resume a sub-agent, resuming instead is fine. Do not send an unselected suggestion. When a relay answer is Unknown, still write the assumption rows the Module sub-agent returns into memory. Do not invent the row.
5. Sub-agents that are already running keep running. Do not launch a sub-agent that needs this answer until the answer is in memory.

If two relays arrive in the same turn, do not merge their questions into one set. Ask the first relay as its own turn and wait. Record the answer and relaunch that sub-agent. Then ask the second relay. More than two are asked one at a time, in the order they arrived. If you cannot tell which arrived first, ask a Module relay before a Writer or C4 relay, and otherwise use the deliverable order in section 4.

A relay may break the count (fewer than two or more than four questions, or more than four suggestions under a question) or break a Rule. Send it back once and say what to correct. If the second return still breaks a count or a Rule, relay the first four valid questions and drop the rest. If fewer than two remain, ask the ones that do. Never rewrite a question or a suggestion yourself.

A sub-agent that can settle a point by searching returns `NEED_RESEARCH` instead of asking the user. The orchestrator launches a Research sub-agent and passes the findings file it wrote. Only a remaining gap becomes `NEED_USER`.

Sub-agents that produce findings write them under `prdfy-spec/findings/`. They still do not edit `memory.md`. Pass those files onward. Do not retype them into the brief.

### Sub-agents

Each role is its own skill. Launch a sub-agent and tell it to read and follow that skill. Do not follow the sub-agent skill yourself.

| Sub-agent | Skill | Does the work |
| --- | --- | --- |
| Research | `prdfy-research` | Searches and writes `findings/research-<mode>.md`, or a numbered rerun |
| Module | `prdfy-module` | Runs one module and writes `findings/module-<name>.md` on close |
| Writer | `prdfy-writer` | Writes one deliverable file, or the decision log and index together, never the C4 model |
| C4 | `prdfy-c4` | Writes the four-level C4 model |
| Verifier | `prdfy-verifier` | Writes `findings/verify-<deliverable>.md` per file and `findings/verify-cross.md`, and edits no deliverable |
| Review | `prdfy-review` | Writes `findings/review.md` and returns the two closing questions |

Pass the memory file, the latest user words, and the skill path. Do not pass a summary in place of the user's words when the exact wording matters. Only a Module sub-agent proposes decision and assumption rows, and it returns them. The orchestrator writes those rows into memory. Writer and C4 sub-agents never propose rows. They cite memory IDs, and they relay a gap as `NEED_USER`.

Do not substitute a general research, brainstorming, PRD, or C4 skill. Those skills talk to the user, name technologies, or continue into implementation. `prdfy-c4` is the C4 skill for this contract.

Every Prdfy skill declares `metadata.protocol`. The return blocks are a protocol, so a mismatched skill fails silently. Before the first launch in a session, read each sub-skill's frontmatter. If a sub-skill's protocol is missing or differs from this skill's, stop and tell the user which skill to update.

Module work stays in order. Once Research for the active module has been launched, it finishes before the Module sub-agent proposes more questions. The Vision brief asks its first questions before any research, because the category is not known yet. For Architectural Boundaries, launch boundaries research before the module proposes questions. Vision waits only for its first questions. Do not read the module skill to decide this. Writing order, verification, and retries are described under Execution.

### When the host cannot launch sub-agents

At the start of the first inline step, tell the user once that this host cannot launch sub-agents and that inline verification is weaker than a separate sub-agent. Do not say it before that step, and do not repeat it. Then run each step inline. Read the sub-skill, act only as that role, produce only its file and its return block, and switch back to the orchestrator role before speaking to the user. Keep the same order, relay rules, and memory updates. Run each verification as its own step after the writing step, and reread the file instead of relying on what the writing step intended.

### What the orchestrator may say

The orchestrator may say:

- status, including one sentence on where a resumed run stands;
- the questions from a relay or a closing step;
- the suggestions the sub-agent supplied under each of those questions;
- a module summary the Module sub-agent already wrote;
- the final review note.

A suggestion becomes a product decision only after the user accepts it.

## Terminology

Use these names in prose and diagrams. Add a domain-specific noun only when the user defines it. Every sub-skill carries the same list on its `Role names:` line.

| Say this | Never replace it with |
| --- | --- |
| Interactive User Client | a UI library or frontend framework |
| Operator Client | an admin framework |
| Request Gateway | a vendor API gateway |
| Application Service | a web framework |
| Domain Service | a language module |
| Relational State Store | a named relational database |
| Document Store | a named document database |
| Object Store | a named blob service |
| Message Broker | a named streaming product |
| Workflow Orchestrator | a named workflow engine |
| Search Index | a named search product |
| Identity and Access Boundary | a named identity vendor |
| Notification Channel | a named email or push vendor |
| External System | a named SaaS product, unless the user requires that integration |
| Cache | a named cache product |

C4 containers come from this list. If a capability does not fit, name the role ("Tariff Calculation Service") and say which responsibility it owns. Do not invent a vendor to make the diagram look concrete.

## Execution

The orchestrator follows this sequence and delegates every product step. It reads and updates `prdfy-spec/memory.md` itself. Module briefs, deliverable contracts, and checklists live in the sub-agent skills.

### 1. Open the interview

Check the sub-skill protocols first.

If `prdfy-spec/memory.md` exists, read its Progress section. Tell the user in one sentence where the run stands, then continue from that phase and module. Do not restart a finished module. Do not trust Phase alone. Before writing a deliverable, check the prerequisites in section 4. If one is missing, run that step first.

Otherwise, tell the user the contract in a few sentences: six modules, two to four questions at a time, sub-agents do the research and writing, and eight documents and an index only after Architectural Boundaries is confirmed. Do not ask whether they want a PRD, a roadmap, and a C4 separately. Those are the exit of this skill, not optional tracks.

If they are continuing an existing product, read `prdfy-spec/memory.md` first. Before any Writer runs, move the existing deliverables into `prdfy-spec/history/<YYYY-MM-DD>/`. Leave `memory.md` and `findings/` in place. Tell the Module sub-agent to interview the change. Settled facts already in memory are `user`. Do not re-litigate them.

Create `prdfy-spec/memory.md` when it does not exist. Write the user's opening words under Unprompted. Write any rule the user states into Rules before the next launch. Then launch the Vision Module sub-agent with that file. Ask the user only the questions that sub-agent returns.

### 2. Run the six modules

For the active module, set Phase to `interview` and record the Active module. Then:

1. For Risk and Compliance, before any question in that module, launch Research in mode `compliance` when no compliance findings file exists, and again when memory names a place the product serves that the latest compliance file does not cover. A file that only says jurisdiction was not named does not cover a place named later. Do not launch it again while jurisdiction is still unnamed and that file already exists. Do not read the module skill to decide this. Pass the markdown file it wrote. For Architectural Boundaries, before the module proposes questions, pass a `research-boundaries` findings file. When none exists, launch Research in mode `boundaries` and pass the file it wrote. Vision waits only for its first questions. Do not read the module skill to decide this. Also launch Research when the Module sub-agent returns `NEED_RESEARCH`, and pass that file.
2. Launch the Module sub-agent with the brief, the memory file, the research, the user's latest words, and the next free `D-` and `A-` IDs.
3. On `NEED_USER`, run the relay. Then launch that same module again with the answer.
4. Repeat until it returns `MODULE_READY`, or the user says to skip.
5. On a skip of the active module, launch the same module again with the instruction `skip`. It proposes an assumption for every missing exit item and returns `MODULE_READY`. Do not write the assumptions yourself. Do not write that skip under Rules. Write a Rule only when the user says to skip that topic from then on.
6. Write the returned decision rows into Decisions and the assumption rows into Assumptions, using the IDs the module returned. When a relay answer is Unknown, still write those assumption rows. Do not invent the row. Show the summary and those new rows. Also show the two closing questions and their suggestions, exactly as the sub-agent supplied them: what to correct, and whether to proceed. Do not attach the next module.
7. Relay the reply. Start the next module only after the user proceeds.

`MODULE_READY` contains the summary, the new decision and assumption rows, and those two closing questions with their suggestions. It is not permission to draft. The Module sub-agent follows `prdfy-module`, which holds the six briefs: Vision, Scope, Domain Rules, Strategy and MVP, Risk and Compliance, Architectural Boundaries.

### 3. Research before drafting

After the user confirms Architectural Boundaries, set Phase to `pressure-test` and launch one Research sub-agent in mode `pressure-test`. It writes the next `research-pressure-test` findings file and checks:

- Competitors and substitutes: promise, audience, and the gap this product claims.
- Market dynamics: buyer, switching cost, and the words the category already uses.
- Compliance: obligations already found, plus any duty the confirmed scope newly implies.

Pass that findings folder to every Writer. Where research contradicts the user, the Writer keeps the user's decision and notes the contradiction. It does not silently correct the product. A gap that only the user can close is a relay, not a guess.

### 4. Write the documents

Findings files are notes. They do not replace the specification.

The user may explicitly ask for documents before Architectural Boundaries is confirmed. In that case, set Draft to `early`. Relaunch each unfinished module with `skip`, in order, and write the assumption rows it returns. Then run the pressure-test research and continue below. Every gap is now an `A-` row the documents can cite.

Before writing a file, the required findings must exist. If a prerequisite is missing, run that step first. A recorded phase of `writing` does not skip this check.

- Before any of files `01` to `06`, a `research-pressure-test` findings file must exist. If it does not, set Phase to `pressure-test`, launch that research, then return to writing.
- Before `05-risk-compliance.md`, a `research-compliance` findings file must exist. If it does not, launch Research in mode `compliance` first. That mode does not ask for jurisdiction.
- Before `07-c4-architecture.md`, `06-domain-architecture.md` must exist and its status must be `written` or `verified`. If it does not, write `06` first.

Set Phase to `writing`, then launch in this order. Launch a Writer only for a file whose status is `pending`, `stale`, or `failed`. Leave a `written` or `verified` file as it is.

1. One Writer per pending, stale, or failed file among `01` to `06`, all at the same time, each following `prdfy-writer`. `05` waits until the compliance findings exist.
2. `prdfy-c4` for `07-c4-architecture.md`, after `06-domain-architecture.md` is written, so the C4 diagrams use the same aggregates.
3. One Writer for the pair `00-decision-log.md` and `README.md`, after every other file is written.

Give each the memory file, `prdfy-spec/findings/`, and the path or paths to write. Each `WROTE` return lists the IDs the file cites. Record them under Cites and set the file to `written`.

On `NEED_USER` from a Writer or from `prdfy-c4`, relay. The other Writers keep running. If two of those relays arrive in the same turn, ask them as two turns, first relay first, as Relay describes. Do not merge the questions.

- If the user answers, record the answer as a `user` decision.
- If the user skips, add an `A-` row whose assumption is "Unknown" for that blocked decision. Do not pick a suggestion for them.

Then relaunch the sub-agent that asked. Mark as `stale` every written file named under `affects`. Writers do not edit `memory.md` or the findings files.

| File | Document |
| --- | --- |
| `00-decision-log.md` | Decisions and rules captured during the interview |
| `01-business-plan.md` | Business plan and value proposition |
| `02-prd.md` | Product requirements document |
| `03-specifications.md` | Specifications and domain contracts |
| `04-strategy-roadmap.md` | Strategy and product roadmap |
| `05-risk-compliance.md` | Risk management and compliance matrix |
| `06-domain-architecture.md` | Domain architecture |
| `07-c4-architecture.md` | C4 model, levels 1 to 4 |
| `README.md` | Index of the documents, open assumptions, and sources |

Do not finish while any of these files is missing. When the host cannot write files, each sub-agent returns its full document and the orchestrator presents them in the order above.

### 5. Verify

Set Phase to `verify`.

1. Launch a Verifier, following `prdfy-verifier`, for every `written` or rewritten file. One launch may cover several files. It writes one verify file and returns one verdict per file. On `PASS`, set the file to `verified`. On `FAIL`, relaunch that file's writer once with its verify file, then verify again. A failed `07-c4-architecture.md` goes back to `prdfy-c4`, not to `prdfy-writer`. A second failure sets the file to `failed`. Report it. Do not repair it in the orchestrator.
2. When no file is `written` or `stale`, launch the Verifier once in mode `cross`. On `FAIL`, relaunch the writer of each file named in its issues once, verify those files again, then run `cross` once more. Report any issue that remains.

### 6. Hand back

Set Phase to `review` and launch one Review sub-agent following `prdfy-review`. Ask the user the two questions it returns, with the suggestions it supplied. Then apply the answer:

- **Promote `A-<n>`.** Set that row to `confirmed`, add a `user` decision that states it, and mark every file citing `A-<n>` as `stale`.
- **Reject `A-<n>`.** Set that row to `rejected`. If the user gives a replacement, add it as a `user` decision. Mark every file citing `A-<n>` as `stale`.
- **Revise a file.** Relaunch that file's writer with the user's words.
- **None to both.** Set Phase to `done`.

Rewrite and verify every `stale` or revised file, and run `cross` again. Then launch Review once more at most. After that second Review, report what is still open and set Phase to `done`.

Do not begin implementation planning on the next turn unless the user leaves this skill by asking for something else.

## Done

The skill is done when all of the following hold:

- `prdfy-spec/` contains the decision log, business plan, PRD, specifications, roadmap, risk and compliance matrix, domain architecture, C4 architecture, and index.
- `prdfy-spec/findings/` contains the research, module, verify, cross-verify, and review notes.
- In Progress, no file is `pending`, `written`, or `stale`, and Phase is `done`.
- Every material claim has a source label, diagrams use only role names, and no executable implementation has been written.
- A Verifier has passed each document, or the orchestrator has reported the file that failed twice.
- The orchestrator is the only voice the user heard.
