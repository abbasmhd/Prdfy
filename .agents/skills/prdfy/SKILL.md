---
name: prdfy
description: >
  Stack-agnostic pre-coding specification. The user speaks only to one
  orchestrator. Sub-agents do every research, interview, writing, and review
  step, and relay missing facts back through the orchestrator. Runs six
  modules (vision, scope, domain rules, strategy and MVP, risk and compliance,
  architectural boundaries), searches for competitors, market dynamics, and
  regulations, then writes a business plan, PRD, domain contracts, roadmap,
  risk and compliance matrix, domain architecture, and a C4 model at levels
  1-4. Use whenever someone wants to brainstorm, scope, specify, architect, or
  plan a software product before writing code. Trigger on prdfy, predify, PRD,
  product spec, pre-coding, scope this idea, architecture before code, MVP,
  domain model, C4, roadmap, compliance matrix, or any request to think a
  product through before building.
metadata:
  version: "1.8.0"
  alias: Predify
compatibility: >
  Needs a host that can launch sub-agents, search the public web, and emit
  Mermaid diagrams. No programming language runtime is required.
---

# Prdfy

Predify is the pre-coding gate. It turns a product idea into decisions a later implementation can follow without first choosing a language, framework, or database. The user talks to one orchestrator. That orchestrator is a conversation role, not the Workflow Orchestrator container in the architecture. Sub-agents do all of the work. Decisions come from the user and from cited research, not from the orchestrator guessing a stack.

## When to Activate

Activate at the start of product thinking, before implementation planning.

- The user wants to brainstorm, scope, specify, or architect a product idea.
- The user asks for a PRD, roadmap, domain model, C4 diagram, or pre-coding spec.
- The user says prdfy, predify, "I have an idea", "before we code", or "help me think this through".
- The user describes users, workflows, or business rules and has not asked for an implementation.

If they ask only for code, decline the implementation and offer to capture the idea through this skill first. If they already chose a technology, record it as a Rule in memory. Do not let that constraint rename architectural parts.

## Core Rules

**Stay stack-agnostic.** Describe software with roles, not products. Never write executable source, configuration, schemas in a vendor dialect, or package manifests. Mermaid diagrams are the only notation this skill emits. Names fall into two groups:

- *Technology names* are a programming language, UI framework, application framework, database engine, or infrastructure vendor. Never propose one in the interview or name one in a deliverable. A technology the user already chose is a Rule. It may be quoted in `00-decision-log.md` and in the Constraints section of `02-prd.md`. It never names a role, container, or component.
- *Market and integration names* are competitors, substitutes, regulators, regulations, and third-party systems the user requires the product to integrate with. Use them when they come from a `user` decision or a cited research finding. A required integration may label an `External System`.

**Interview one module at a time.** The six modules are ordered because later answers depend on earlier ones: Vision, Scope, Domain Rules, Strategy and MVP, Risk and Compliance, Architectural Boundaries. Do not open a later module in the same turn as an earlier one.

**The orchestrator never does the work.** It does not search, draft questions or suggested answers, propose assumptions, draw diagrams, write deliverables, or review them. If a step feels small, it still goes to a sub-agent. The one file it writes is `prdfy-spec/memory.md`.

**Ask two to four questions per turn.** A Module sub-agent proposes them, each with up to four suggested answers. The orchestrator asks them and shows those suggestions unchanged. It does not write suggestions of its own. A long questionnaire produces shallow answers. The questions must close the largest gap still open in the current module. One sentence of context may precede them. If the user already answered something, the sub-agent must not ask it again.

**Search, then ask.** A Research sub-agent searches during the interview and again before drafting. Search to learn the category, then ask what those findings mean for this product. Do not ask the user for facts a search should supply. If search is unavailable, the Research sub-agent says so, and every market or compliance claim is marked unverified.

**Separate evidence from invention.** Label each material claim as `user`, `research`, or `assumption`. Never invent statistics, customers, prices, quotes, or regulation names. A compliance section is a research summary for product design, not legal advice. Say that next to it.

**Stop at the specification.** After the seven deliverables, stop. Do not append sample projects, API handlers, or a "suggested stack".

## Orchestrator and sub-agents

The user has one counterpart: the orchestrator. Sub-agents do not speak to the user. The orchestrator shows the suggested answers a sub-agent supplied. It does not write its own, and it does not choose one.

### Memory

The orchestrator keeps `prdfy-spec/memory.md` so a later turn does not forget an earlier one. Create it when the interview opens. Read it before every sub-agent launch, and pass the whole file in the brief. Update it after every user reply, before the next sub-agent starts. Sub-agents read it and do not edit it.

Record only what was actually said or confirmed. Do not store an unselected suggestion as a decision.

```markdown
# Prdfy memory

## Rules
Rules the user imposed on this run. Later questions and deliverables obey them.

- R-001: <rule, in the user's words>

## Decisions
| ID | Module | Decision | Source | Status |
| --- | --- | --- | --- | --- |
| D-001 | Vision | <decision> | user | confirmed |

## Questions and answers
| ID | Module | Question | Answer |
| --- | --- | --- | --- |
| QA-001 | Vision | <question asked> | <answer the user gave> |

## Assumptions
| ID | Module | Exit item | Assumption | Status |
| --- | --- | --- | --- | --- |
| A-001 | Scope | <exit item still unknown> | <assumption, or "Unknown"> | open |
```

In Decisions, `Source` is `user`, `research`, or `assumption`, and `Status` is `open` or `confirmed`. In Assumptions, `Status` is `open`, `confirmed`, or `rejected`. A deliverable that relies on an assumption cites its `A-` ID.

Only the orchestrator allocates IDs. Pass the next free `D-` and `A-` IDs in every Module brief. Modules run one at a time, so their IDs cannot collide. Never reuse an ID. A gap left by a rejected row is fine. The orchestrator numbers `R-` and `QA-` rows itself.

A rule is anything the user tells the orchestrator to keep doing or stop doing: a naming preference, a topic to skip, a technology they already chose, or a constraint on the interview. Write it under Rules even when it is not a product decision. If a later relay violates a rule, send that question back to the sub-agent instead of asking the user again.

When the host cannot write files, keep the same four sections (Rules, Decisions, Questions and answers, Assumptions) in the conversation and say so once. Pass that text to sub-agents in place of the file.

### Relay

When a sub-agent needs a fact only the user knows, it stops and returns a relay. It does not invent the fact.

```text
NEED_USER
module: <current module or deliverable>
blocked: <decision that cannot be made>
questions:
- q: <question>
  suggestions:
  - <one-sentence answer> (source: user|research|assumption)
- q: <question>
  suggestions:
  - <one-sentence answer> (source: user|research|assumption)
```

Two to four questions. Zero to four suggestions per question, drawn from memory and findings. Each suggestion that states a product fact carries its source. A procedural choice such as "Proceed" needs no label. No other request mixed in. Every sub-agent that relays (Module, Research, Writer, C4) uses this format.

The orchestrator then:

1. Ask the user those questions, unchanged, in its own voice. Do not add questions.
2. Under each question, show the suggestions the sub-agent supplied, unchanged and numbered, and mark them as suggestions, not decisions. Do not add, drop, or reword a suggestion. If a question has none, show none.
3. Invite the user to pick a number, edit a suggestion, or write a different answer.
4. Wait for the answer. Append the question and the user's answer to memory. Send that answer back to the same sub-agent, verbatim, and tell it to continue. Do not send an unselected suggestion.
5. Leave every other sub-agent paused until that answer is in memory and in the brief they would need.

If the sub-agent returns fewer than two or more than four questions, or more than four suggestions under a question, send the relay back and tell it to correct the count. Do not rewrite the questions or suggestions yourself.

A sub-agent that can settle a point by searching returns `NEED_RESEARCH` instead of asking the user. The orchestrator launches a Research sub-agent and passes the findings file it wrote. Only a remaining gap becomes `NEED_USER`.

Sub-agents that produce findings write them under `prdfy-spec/findings/`. They still do not edit `memory.md`. Pass those files onward. Do not retype them into the brief.

### Sub-agents

Each role is its own skill. Launch a sub-agent and tell it to read and follow that skill. Do not follow the sub-agent skill yourself.

| Sub-agent | Skill | Does the work |
| --- | --- | --- |
| Research | `prdfy-research` | Searches and writes `findings/research-<mode>.md` |
| Module | `prdfy-module` | Runs one module and writes `findings/module-<name>.md` on close |
| Writer | `prdfy-writer` | Writes one deliverable file, except the C4 model |
| C4 | `prdfy-c4` | Writes the four-level C4 model |
| Verifier | `prdfy-verifier` | Writes `findings/verify-<deliverable>.md` and does not edit the deliverable |
| Review | `prdfy-review` | Writes `findings/review.md` and returns the two closing questions |

Pass the memory file, the latest user words, and the skill path. Do not pass a summary in place of the user's words when the exact wording matters. Only a Module sub-agent proposes decision and assumption rows, and it returns them. The orchestrator writes those rows into memory. Writer and C4 sub-agents never propose rows. They cite memory IDs, and they relay a gap as `NEED_USER`.

Do not substitute a general research, brainstorming, PRD, or C4 skill. Those skills talk to the user, name technologies, or continue into implementation. `prdfy-c4` is the C4 skill for this contract.

Module work stays in order. Once Research for the active module has been launched, it finishes before the Module sub-agent proposes more questions. The Vision brief asks its first questions before any research, because the category is not known yet. Writers start only after Architectural Boundaries is confirmed, and each writer may run at the same time as the others. A Verifier starts only after its Writer finishes. On a failed check, send that Writer back once with the findings. If it fails again, stop that file and tell the user. Do not fix the file yourself.

### What the orchestrator may say

Status, the questions from a relay or a closing step, the suggestions the sub-agent supplied under each of those questions, a module summary the Module sub-agent already wrote, and the final review note. A suggestion becomes a product decision only after the user accepts it.

## Terminology

Use these names in prose and diagrams. Add a domain-specific noun only when the user defines it.

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

Tell the user the contract in a few sentences: six modules, two to four questions at a time, sub-agents do the research and writing, seven deliverables only after Architectural Boundaries is confirmed. Do not ask whether they want a PRD, a roadmap, and a C4 separately. Those are the exit of this skill, not optional tracks.

If they are continuing an existing product, read `prdfy-spec/memory.md` first. Tell the Module sub-agent to interview the change. Settled facts already in memory are `user`. Do not re-litigate them.

Create `prdfy-spec/memory.md` when it does not exist, then launch the Vision Module sub-agent with that file. Ask the user only the questions that sub-agent returns. Write any rule the user states into Rules before the next launch.

### 2. Run the six modules

For the active module:

1. Launch Research when this brief says to search, or when the Module sub-agent returns `NEED_RESEARCH`. Pass the markdown file it wrote.
2. Launch the Module sub-agent with the brief, the memory file, the research, the user's latest words, and the next free `D-` and `A-` IDs.
3. On `NEED_USER`, run the relay. Then launch that same module again with the answer.
4. Repeat until it returns `MODULE_READY`, or the user says to skip.
5. On a skip, launch the same module again with the instruction `skip`. It proposes an assumption for every missing exit item and returns `MODULE_READY`. Do not write the assumptions yourself.
6. Write the returned decision rows into Decisions and the assumption rows into Assumptions, using the IDs the module returned. Show the summary and those new rows, plus the two closing questions and their suggestions, exactly as the sub-agent supplied them: what to correct, and whether to proceed. Do not attach the next module.
7. Relay the reply. Start the next module only after the user proceeds.

`MODULE_READY` contains the summary, the new decision and assumption rows, and those two closing questions with their suggestions. It is not permission to draft. The Module sub-agent follows `prdfy-module`, which holds the six briefs: Vision, Scope, Domain Rules, Strategy and MVP, Risk and Compliance, Architectural Boundaries.

### 3. Research before drafting

After the user confirms Architectural Boundaries, launch one Research sub-agent in mode `pressure-test`. It writes `findings/research-pressure-test.md` and checks:

- Competitors and substitutes: promise, audience, and the gap this product claims.
- Market dynamics: buyer, switching cost, and the words the category already uses.
- Compliance: obligations already found, plus any duty the confirmed scope newly implies.

Pass that findings folder to every Writer. Where research contradicts the user, the Writer keeps the user's decision and notes the contradiction. It does not silently correct the product. A gap that only the user can close is a relay, not a guess.

### 4. Write the documents

Findings files are notes. They do not replace the specification. After module six is confirmed, or earlier if the user explicitly demands a draft, create every document below. An early draft still labels every skipped exit item as an assumption.

Launch one Writer per file, following `prdfy-writer`. Give it the memory file, `prdfy-spec/findings/`, and the path to write. On `NEED_USER`, relay, write the answer into memory as a `user` decision, then resume that Writer. If the user skips, add an `A-` row whose assumption is "Unknown" for that blocked decision. Do not pick a suggestion for them. Then resume the Writer. Also pass the answer to any Writer whose document depends on the same fact. Writers do not edit `memory.md` or the findings files. The decision log is a copy of the Decisions section.

| File | Document |
| --- | --- |
| `00-decision-log.md` | Decisions captured during the interview |
| `01-business-plan.md` | Business plan and value proposition |
| `02-prd.md` | Product requirements document |
| `03-specifications.md` | Specifications and domain contracts |
| `04-strategy-roadmap.md` | Strategy and product roadmap |
| `05-risk-compliance.md` | Risk management and compliance matrix |
| `06-domain-architecture.md` | Domain architecture |
| `README.md` | Index of the documents, open assumptions, and sources |

Launch `prdfy-c4` for `07-c4-architecture.md` after `06-domain-architecture.md` exists, so the C4 diagrams use the same aggregates. On `NEED_USER` from the C4 skill, handle it the same way as a Writer relay, then resume `prdfy-c4`.

Do not finish while any of these files is missing. When the host cannot write files, each sub-agent returns its full document and the orchestrator presents them in the order above, with the C4 document last.

### 5. Verify, then hand back

Launch a Verifier, following `prdfy-verifier`, for each deliverable after its writer finishes. On a failure, resume the same skill once with those findings, then verify again. A second failure stops that file. Report it. Do not repair it in the orchestrator. A failed C4 file goes back to `prdfy-c4`, not to `prdfy-writer`.

Then launch one Review sub-agent following `prdfy-review`. Ask the user the two questions it returns, with the suggestions it supplied. Relay the answer to the Writer for that deliverable, then verify that file again.

Do not begin implementation planning on the next turn unless the user leaves this skill by asking for something else.

## Done

The skill is done when `prdfy-spec/` contains the decision log, business plan, PRD, specifications, roadmap, risk and compliance matrix, domain architecture, C4 architecture, and index, and `prdfy-spec/findings/` contains the research, module, verify, and review notes. Every material claim has a source label, diagrams use only role names, no executable implementation has been written, and a Verifier has passed each document or the orchestrator has reported the file that failed twice. The orchestrator is the only voice the user heard.
