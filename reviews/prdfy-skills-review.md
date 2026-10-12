# Prdfy skills review

Reviewed: `prdfy` 1.7.0, `prdfy-module` 1.1.0, `prdfy-research` 1.1.0, `prdfy-writer` 1.2.0, `prdfy-c4` 1.1.0, `prdfy-verifier` 1.1.0, `prdfy-review` 1.1.0.
Date: 2026-10-12.

## Status

Fixed on 2026-10-12, following `reviews/prdfy-fix-plan.md`: section 1 (1.1 to 1.8) and items 2.1, 2.2, and 2.10. Everything else is still open.

## Summary

All seven skills pass `skill-creator/scripts/quick_validate.py`, and the core design holds up. One voice faces the user, the sub-agents are stateless, a single memory file is the source of truth, every claim carries a source label, and the vocabulary is role-based. The problems are in the contracts between the skills. Several rules contradict each other, so a run that follows them literally would loop, fail verification by design, or be unable to reach "Done".

The fixes fall into three groups:

1. **Blocking contradictions** (section 1). These are cases where a sub-agent obeying its own skill causes another skill to reject its output. Fix these first.
2. **Protocol gaps** (section 2). These are states the protocol never defines: assumption IDs, superseded decisions, resuming a run, hosts without sub-agents, and parallel writers that need a new fact.
3. **Quality and maintainability** (sections 3 and 4). These cover cross-document consistency checks, traceability, duplicated role lists, evals, and the README.

---

## 1. Blocking contradictions

### 1.1 The verifier fails every business plan that names a competitor

- `prdfy-verifier/SKILL.md:25` says: "No language, framework, database engine, or vendor product appears."
- `prdfy-writer/SKILL.md:58` requires "Alternatives and why they fail, each tied to research". `prdfy-research` exists partly to find competitors (description, line 4).

Competitors are vendor products, so a correct `01-business-plan.md` fails verification. The same applies to an `External System` the user explicitly requires (`prdfy/SKILL.md:164`) and to a technology the user already chose (`prdfy/SKILL.md:37`). Every rule allows these names, and the verifier rejects all of them.

**Fix:** Split the ban into two lists.
- *Technology names* (language, framework, database engine, infrastructure vendor) are banned everywhere, except a user-imposed constraint recorded in memory Rules. That constraint appears only in a dedicated "Constraints" section and never as a container name.
- *Market and integration names* (competitors, substitutes, regulators, required third-party integrations) are allowed in prose and in `System_Ext` boxes when they are sourced from research or from a `user` decision.

Update the verifier check to match.

### 1.2 Research asks a one-question relay, and the orchestrator must reject it

- `prdfy-research/SKILL.md:24`: "Return `NEED_USER` asking only for the jurisdiction."
- `prdfy/SKILL.md:116`: "If the sub-agent returns fewer than two or more than four questions, send the relay back and tell it to correct the count."

These two rules loop. Research also uses a different relay format (`prdfy-research/SKILL.md:60-65`: `NEED_USER:` as a list nested inside `RESEARCH`, with no `module` or `blocked` fields), so the orchestrator's relay parser doesn't match it either.

**Fix:** Either allow one to four questions in a relay (simplest), or have Research ask jurisdiction plus one related question, such as which regulated activities apply. In both cases, Research should return the same `NEED_USER` block every other sub-agent uses.

### 1.3 Writer assumptions are treated as inventions by the verifier

- `prdfy-writer/SKILL.md:18` says to label claims `assumption`.
- `prdfy-verifier/SKILL.md:18` says: "A claim that is not in memory and not in a findings file is an invention."

Any assumption that a Writer introduces fails verification. The Writer's `WROTE` return lists only "`<id used>`" (line 42), which suggests Writers may only *reuse* assumptions. But memory's Open gaps have no IDs to reuse (see 2.1).

**Fix:** Pick one rule and state it in both skills. I recommend: Writers may only cite assumptions that already exist in memory. A new assumption is returned as `NEED_USER` or as a proposed `A-` row that the orchestrator writes into memory before verification.

### 1.4 The verifier has no heading contract for the C4 file

`prdfy-verifier/SKILL.md:18` checks "the heading contract in the Prdfy Writer skill for that filename". For `07-c4-architecture.md`, the Writer skill says only "Do not write this file" (line 120). The C4 contract lives in `prdfy-c4`.

**Fix:** Point the verifier at `prdfy-c4` for `07-c4-architecture.md`. Better still, see 3.1 on making heading contracts exact.

### 1.5 The C4 template breaks its own rule

`prdfy-c4/SKILL.md:50` says "'Uses' is not enough", and the template at line 81 has `Rel(actor, client, "Uses")`. Models copy templates, so expect "Uses" labels in the output.

**Fix:** Change the label to a domain placeholder, such as `"[Action the actor takes]"`.

### 1.6 The "Done" criteria can't be met on some valid paths

`prdfy/SKILL.md:237` requires `findings/` to contain "the research, module, verify, and review notes". However:
- a skipped module never writes `module-<name>.md`, because Module only writes that file on `MODULE_READY` (`prdfy-module/SKILL.md:53`);
- Research "skip[s] the file when you have none" (`prdfy-research/SKILL.md:37`).

**Fix:** On a skip, have the Module sub-agent write the close-out file with the proposed assumptions (see 1.7). Have Research always write a file, recording "no findings" plus the reason.

### 1.7 The orchestrator is told to do work it is forbidden to do

The orchestrator rule (`prdfy/SKILL.md:45`) forbids it from drafting anything, but two steps make it author content:

- **Skip handling.** `prdfy/SKILL.md:189` says the *orchestrator* writes an assumption for every missing exit item. `prdfy-module/SKILL.md:20` says the *Module* proposes them. Inventing an assumption is product work.
- **Suggested answers.** `prdfy/SKILL.md:47, 111, 190` have the orchestrator compose up to four suggested answers per question. That is up to 16 pieces of drafted product content per turn, with no source labels and no review.

**Fix:** Move both into the Module sub-agent (and into Writer, C4, and Research when they relay). Extend `NEED_USER` with suggestions:

```text
NEED_USER
module: <module>
blocked: <decision>
questions:
- q: <question>
  suggestions:
  - <one sentence> (source: user|research|assumption)
```

Then the orchestrator only relays. On a skip, it relaunches the Module with `skip`, and the Module returns `MODULE_READY` with `assumption`/`open` rows.

### 1.8 Vision runs before its research, though the orchestrator says research comes first

- `prdfy/SKILL.md:139`: "Research for the active module finishes before the Module sub-agent proposes questions."
- `prdfy-module/SKILL.md:66`: "Before the second turn, return `NEED_RESEARCH`…". This implies the first Vision turn runs *without* research.

"Before the second turn" also can't be evaluated. A freshly launched sub-agent doesn't know which turn it is on.

**Fix:** Say "If memory has no Vision QA row yet, ask first. If it has one or more and no `research-category.md` exists, return `NEED_RESEARCH`." Then change line 139 to "…unless the module brief says to ask first."

---

## 2. Protocol gaps

### 2.1 Assumptions have no IDs

Review lists `<id>: <assumption>` (`prdfy-review/SKILL.md:24`), and Writer and C4 return `assumptions: - <id used>`. But the memory template's Open gaps section is plain bullets (`prdfy/SKILL.md:83-85`).

**Fix:** Add an `A-` prefix and a table:

```markdown
## Assumptions
| ID | Module | Exit item | Assumption | Status |
| --- | --- | --- | --- | --- |
| A-001 | Scope | Release boundary | <assumption> | open |
```

### 2.2 No one owns ID allocation

Module returns `D-id` placeholders (`prdfy-module/SKILL.md:47`). Writers run in parallel. Nothing says who assigns `D-`, `QA-`, `R-`, or `A-` numbers, so collisions are likely.

**Fix:** Sub-agents return rows with `D-?`. The orchestrator assigns the next sequential ID when it writes the row into memory.

### 2.3 Earlier decisions can't be changed

`Status` is only `open` or `confirmed` (`prdfy/SKILL.md:87`). Suppose a user in module 5 says "actually, operators are out of scope". Nothing defines reopening Scope, superseding D-007, or which module and deliverable files are now stale.

**Fix:** Add a `superseded` status with a `Superseded by` column. Add an orchestrator rule: if a reply changes a confirmed decision, relaunch the owning module once to restate its exit items, and mark every finished deliverable that cites the old ID for rewrite and re-verification.

### 2.4 Resume is under-specified

Two gaps:

- Memory doesn't record where the run is: which module is active, which phase, which files exist, and which failed. If the user closes the chat mid-run, the next session has to guess. Add a `## Progress` section to memory, such as `Phase: interview | research | writing | verify | review`, `Active module: Domain Rules`, and file status rows.
- "Continuing an existing product" (`prdfy/SKILL.md:177`) reruns the pipeline. That overwrites deliverables, and research files are replaced (`prdfy-research/SKILL.md:40`). Add a revision note to each deliverable, or archive the previous `prdfy-spec/` under `prdfy-spec/history/<date>/`.

### 2.5 "Resume" and "relaunch" are used interchangeably

The relay says "send that answer back to the same sub-agent… tell it to continue" (line 113) and "resume that Writer" (line 209). Step 2.3 says "launch that same module again" (line 187). Many hosts can't resume a sub-agent.

**Fix:** Define one rule. *Relaunch with the updated memory file and the user's verbatim answer. Resume only if the host supports it.* This works because memory already holds every QA row.

### 2.6 Parallel writers and late facts

"Leave every other sub-agent paused" (line 114) assumes running sub-agents can be paused, and most hosts can't do that. "Also pass the answer to any Writer whose document depends on the same fact" (line 209) doesn't cover a Writer that has already finished.

**Fix:** When a relay from one Writer produces a new decision, finish the in-flight Writers. Then rerun, and re-verify, every finished file whose content depends on that decision. Also, `README.md` (the index) depends on every other file and on the final assumption list, so it should run last rather than in parallel.

### 2.7 No fallback when the host can't launch sub-agents

`compatibility` lists sub-agents as required, and there is a fallback for "cannot write files" (line 91). There is none for "cannot launch sub-agents". Under "the orchestrator never does the work", the run deadlocks.

**Fix:** Add a degraded mode. Tell the user once. Then run each sub-skill inline as a clearly separated role step: read the skill, produce only its return block, and switch back. Alternatively, decline explicitly.

### 2.8 Send-backs can loop forever

There is a one-retry limit for verifier failures, but none for sending a relay back over question count or a Rule violation (lines 89, 116).

**Fix:** Allow one send-back. After that, relay the first four valid questions and log the issue.

### 2.9 Review is open-ended and ignores verifier results

- The description says Review "reads… verifier results" (`prdfy-review/SKILL.md:5`), but the `review.md` template has no section for them. Files that failed twice should be listed.
- "Which assumption should be promoted or rejected?" changes memory, which can affect *several* deliverables. Line 230 only re-runs "the Writer for that deliverable".
- There is no exit answer and no stop rule after a revision.

**Fix:** Add a `## Verification` section. Allow "none" as an answer, which ends the skill. Re-run every file that cites a changed assumption. Run Review at most once more after a revision.

### 2.10 Writer can't return a proposed decision

`prdfy/SKILL.md:135` says "A Module or Writer sub-agent that proposes a decision row returns it", but the Writer's `WROTE` block (`prdfy-writer/SKILL.md:39-43`) has no `decisions:` field.

**Fix:** Add `decisions:` to `WROTE`, or state that Writers never propose decisions and use `NEED_USER` instead.

### 2.11 The early-draft path is ambiguous

Line 207 allows drafting "earlier if the user explicitly demands a draft", but the pressure-test research (section 3) and C4 both assume Boundaries is confirmed.

**Fix:** State which steps still run on an early draft. I suggest: pressure-test research runs, C4 is drafted only if module 6 has at least one confirmed boundary, and every gap becomes an `A-` row.

---

## 3. Output quality

### 3.1 Make heading contracts exact

The Writer contracts are bullet lists ("Problem and who feels it"). The verifier checks a "heading contract", but the skills never say whether those bullets are the literal H2 headings. Two runs will produce different headings, and the verifier will judge them inconsistently.

**Fix:** Give each file its exact required H2 headings, in order, and tell the verifier to match them literally. For non-commercial or internal products, allow `Not applicable: <reason>` under a heading such as "How value becomes revenue".

### 3.2 Add a cross-document consistency check

The verifier checks one file at a time. The highest-value check in a spec set is across files, and nothing does it:

- Glossary terms in `03` are used with the same meaning in `02`, `06`, and `07`.
- Aggregates and invariants in `06` match C4 level 4 in `07`. `prdfy-c4` requires this at line 52, but nobody verifies it.
- Every in-scope workflow from Scope has at least one `FR-`, every `FR-` traces to a `D-`, and every out-of-scope item appears in the roadmap's non-roadmap list.
- Every `RSK-` with compliance category maps to an obligation row.

**Fix:** Add a `cross` mode to `prdfy-verifier`, run once after all per-file passes, that writes `findings/verify-cross.md`.

### 3.3 Add traceability columns

Add a `Decisions` column to FR, NFR, and RSK rows, and an `Aggregate` column to INV rows. This makes 3.2 checkable, and a later implementation can trace any requirement back to the user's words.

### 3.4 Make research files support the confidence rule

The Writer sets compliance confidence to high "only when a primary source was retrieved" (`prdfy-writer/SKILL.md:107`), but the findings format (`prdfy-research/SKILL.md:42-56`) doesn't record whether a source is primary.

**Fix:** Extend each finding to `Source: <name>. Type: primary|secondary. Location: <url>. Accessed: <date>.` The access date matters because regulations change. The verifier should also check that each cited source exists in a findings file, not just that a name is present.

### 3.5 Fix research file names and overwrites

- The mode name "Pressure test" yields `research-pressure test.md`. Specify `research-pressure-test.md`.
- "Replace the file when the same mode runs again" deletes evidence that an earlier deliverable may already cite. Either append under a dated heading, or version the file (`research-category-2.md`).

### 3.6 Don't make Writers invent risk owners

The `Owner` column in the risk matrix (`prdfy-writer/SKILL.md:99`) invites invention, because the interview never asks who owns a risk. Make it a role (such as "Product owner" or "Operator") or `unassigned`. Alternatively, add an owner question to the Risk and Compliance module.

### 3.7 Check that the Mermaid renders

Mermaid's C4 diagrams are marked experimental, and renderers handle them unevenly. Class-diagram annotations with spaces (`<<Value Object>>`) should also be render-tested. Test the three templates in `prdfy-c4` against the renderers you target, such as GitHub, Cursor preview, and mermaid.live. Consider a `flowchart` fallback for levels 1-3 if `C4Context` doesn't render. Lifecycles in `03-specifications.md` would also benefit from a suggested `stateDiagram-v2`.

---

## 4. Triggering, UX, and maintainability

### 4.1 The orchestrator description over-triggers

The trigger list includes "MVP", "roadmap", "C4", and "domain model". Someone asking for "a C4 diagram of this existing repo" or "a roadmap for next quarter" would be pulled into a six-module interview. Add negative triggers, such as "Do not use for documenting existing code, sprint planning, or diagramming a system that already exists." Then test with trigger evals (4.4).

### 4.2 Don't decline coding requests

`prdfy/SKILL.md:37` tells the agent to "decline the implementation" when the user asks only for code. If the skill triggered by mistake, that refuses the user's actual request. Prefer: "If they ask only for code, this skill does not apply. Mention once that it is available."

### 4.3 Keep one copy of the role list

The role list is duplicated in five places, and the copies already differ:

- `prdfy` (15 roles, with a "never replace with" column);
- `prdfy-writer` and `prdfy-c4` (15 roles);
- `prdfy-module` and `prdfy-research` (5 roles).

Research's Boundaries mode is limited to five names, so it can't describe an Identity and Access Boundary or a Workflow Orchestrator.

**Fix:** Keep the canonical table in one place, such as `prdfy/references/roles.md`, and have each sub-skill reference it. If the separate install folders make that impractical, keep the copies identical and add a short check to the eval suite that compares them.

### 4.4 Add evals

The repo ships `skill-creator` with a full eval harness, but none of the Prdfy skills has `evals/evals.json`. Suggested first set:

- **Trigger evals** for the `prdfy` description: should trigger on "I have an idea for an app that…"; should not trigger on "draw a C4 of this repo".
- **Scenario evals**, each with assertions:
  - The user names a technology at the start. It is recorded as R-001 and never appears as a container name.
  - The user skips Domain Rules. A-rows are created and a module file is still written.
  - Search is unavailable. Every market claim is marked unverified.
  - The jurisdiction is unknown. No statute is named.
  - The user changes a Scope decision during module 5. The old row is superseded and affected files are re-run.
  - A business plan names competitors. It passes verification.
- **Static checks** on the deliverables: no code fences other than `mermaid`, every `FR-` row has a source label, and the aggregates in `06` match `07`.

### 4.5 Cost and latency

A full run is roughly 6 modules × 2-3 turns (Module + Research) + 9 Writers + 9 Verifiers + retries + Review, which comes to about 40-60 sub-agent launches. Two cheap savings that don't break the "orchestrator never does the work" rule:

- `00-decision-log.md` is a pure copy of memory, so one Writer launch can produce it together with `README.md` at the end.
- The verifier could take a batch of files in one launch and still write one `verify-<file>.md` per file.

### 4.6 Use structured questions when the host has them

Two to four questions, each with up to four suggestions, is a lot to read as plain text. When the host has a multiple-choice question tool (Cursor's `AskQuestion`, for example), the orchestrator should use it. The suggestions become options, and the user can always choose "Other" to write their own answer.

### 4.7 Fix the README and deliverable count

- `README.md` (repo root) lists seven deliverables and omits `00-decision-log.md` and `prdfy-spec/README.md`, which the orchestrator requires.
- "Seven deliverables" appears in `prdfy/SKILL.md:53, 175` and `prdfy-research/SKILL.md:16`, but the table lists nine files. State "eight specification documents plus an index", or whatever count you intend, and use it everywhere.
- The README says "The skill is the `.agents/skills/prdfy/` folder" and "Cursor also loads `.cursor/skills/prdfy/`". The skill actually needs all seven folders. The copy commands do include them all, but the prose doesn't say so.

### 4.8 Version the skill set

The orchestrator is 1.7.0, and the sub-skills are 1.1.0 and 1.2.0. Because the return blocks form a protocol, a mismatched install (an old `prdfy-research` with a new `prdfy`) fails silently. Add `metadata.protocol: "1"` to every skill, and have the orchestrator refuse to delegate to a sub-skill with a different protocol value.

---

## Suggested order of work

1. Sections 1.1 to 1.8. These are small text edits, and they unblock a clean end-to-end run.
2. Sections 2.1 to 2.3. These are memory schema changes (assumption IDs, ID ownership, superseded decisions), and most other fixes depend on them.
3. Section 4.4. Build the evals now, so the remaining changes can be measured.
4. Sections 3.1 to 3.3. Exact headings, the cross-document check, and traceability give the biggest jump in output quality.
5. Everything else.
