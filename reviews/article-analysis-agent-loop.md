# Article analysis: agent loop vs Prdfy sub-agents

Article: Anthropic, "Building agents: When to fold subagents into your main agent loop" (2026).
Skills read: `prdfy` 2.2.0, `prdfy-module` 1.5.0, `prdfy-research` 1.4.0, `prdfy-writer` 1.5.0, `prdfy-c4` 1.4.0, `prdfy-verifier` 1.5.0, `prdfy-review` 1.4.0.
Measured facts: `reviews/eval-results-2026-10-12.md`.
Date: 2026-11-02.

This is analysis only. No skill, script, or eval was edited.

## Decision

Kept Writer and C4 as separate agents because C4 needs `06`'s aggregates and Writer files run in parallel. The `NEED_USER` relay already keeps the orchestrator talking to the user; that format is unchanged.

## Status

The article is relevant. Prdfy is the design the article warns about: an orchestrator plus six specialist sub-agents, split by job, with a nested launch for almost every step.

It is not a copy of an org chart. One skill owns the system prompt. Sub-agents never speak to the user. Returns are compact. Those parts already match the article.

The parts that do not: Research and Module chain on each other inside the same module. A full run is many nested loops. Every scenario eval could only run the inline fallback, and that fallback already completed the work.

## Summary

A single loop with skills often beats both one-prompt-for-everything and orchestrator-sub-agent designs on quality, cost, and latency. Sub-agents stay justified for black-box verification, for parallel work that needs a fresh discardable window, and for conflicting instructions or tool-choice failures.

Verdicts, using those three tests:

- **Research: merge into Module** for category, compliance, and boundaries. **Keep** the Research agent for pressure-test only.
- **Module: keep.** Do not fold it into the orchestrator until a comparison eval exists.
- **Writer: keep.** `01`, `02`, and `04` are real parallel work. `03` and `05` are batched, not independent.
- **C4: keep.** Do not merge it with Writer.
- **Verifier: keep.** Clearest black-box case.
- **Review: keep.** Close-out, not a second verifier, and it must not rewrite.

Do not change the relay format. Do not make inline the default just because the evals had no `Task` tool. Change one thing at a time, and rerun the affected scenario evals before keeping the change.

---

## 1. What the article claims, mapped to Prdfy

The article's keep-tests, in the form this review uses:

1. **Black-box verification.** A checker that must not share the writer's window.
2. **Parallel work with a fresh, discardable context.** Independent research paths, separate components, then a compact result.
3. **Conflicting instructions or tool-choice failure.** The main loop cannot hold both jobs without degrading.

It also says: split by context, not by problem type. Specialists that chain, or that are always called together, are merge candidates. Progressive disclosure (short descriptions, load the body only when needed) is what makes one loop workable. One owner holds the system prompt and end-to-end quality. Task-completion evals gate every architectural change. When a sub-agent stays, call it as a tool so the main agent keeps talking to the user.

Prdfy already does several of those. The rest of this file says which.

---

## 2. Measured facts from the evals

From `reviews/eval-results-2026-10-12.md`:

- Every scenario eval used the documented fallback "When the host cannot launch sub-agents" (`prdfy/SKILL.md:194-196`). The executors had no `Task` tool. **Sub-agents inside a run: none.**
- First run: **24/34 expectations (70.6%)**. After the `prdfy-fix-plan-3` edits, evals 2, 4, 5, 6, and 7 went **16/25 → 23/25**. Eval 1 stayed **6/6**. Eval 3 rerun **3/3**. Eval 6 after the fixture fix **4/4**.
- The remaining eval 2 fail is Env: "A- rows proposed by the Module sub-agent, not the orchestrator." The same runner played both roles. Separation was not shown, and cannot be shown on that host.
- Eval 6: the Verifier accepted Hallkeeper as a researched competitor, and the orchestrator did not edit `01-business-plan.md`. Inline verification is still documented as weaker than a separate sub-agent.
- Eval 7: C4 ran only after `06` returned `WROTE`. `00` and `README` waited. That order held even in the inline fallback.
- Trigger evals were not run. `claude -p` could not reach a model.
- Timing and token counts were not captured.

Sub-agent interview (same file, "Sub-agent interview"): a real orchestrator launched a fresh `generalPurpose` agent per step. The nine deliverables were not written. Approximate launch count through pressure-test: **about 20–23 nested agents** for the interview alone.

Observed in that interview:

- Vision was Module → Module (`NEED_RESEARCH`) → Research → Module → Module (`MODULE_READY`). Five launches for one module.
- Compliance research ran twice (`research-compliance.md`, then `research-compliance-2.md`) because jurisdiction was unnamed, then explicit unknown.
- Architectural Boundaries aborted twice on relaunch (`Subagent was aborted`), then recovered in a continuation.
- Host summaries twice addressed the user ("needs your answers"). The protocol blocks themselves went to the orchestrator.
- Modules closed several `Unknown` answers without `A-` rows. That was a skill bug, later fixed. It is not an architecture lesson.

The old cost note in `reviews/prdfy-skills-review.md` §4.5 still applies: a full run is on the order of **40–60 launches** (6 modules × Module+Research, plus writers, verifiers, retries, review). The interview used ~20 before writing started. That is the latency the article is about.

The inline fallback is the article's single loop: one model, read the sub-skill, act as that role, switch back, talk to the user. It completed the scenario evals. That is evidence for the article. It is not a measured quality win against real sub-agents, because those evals never ran the sub-agent path.

---

## 3. Progressive disclosure, relay, and one voice

### Progressive disclosure

Prdfy's skills already are progressive disclosure at the role boundary.

- The orchestrator skill lists each role in one line (`prdfy/SKILL.md:177-184`).
- "Launch a sub-agent and tell it to read and follow that skill. Do not follow the sub-agent skill yourself" (`prdfy/SKILL.md:175`).
- The orchestrator reads sub-skill **frontmatter** only, to check `metadata.protocol` (`prdfy/SKILL.md:190`). It does not load the bodies.
- Each sub-skill says "Use only when the Prdfy orchestrator delegates". The body loads when that role launches.

There are no `references/` files under the sub-skills. Disclosure is one file per role, not a catalog of sections inside a role. That is still the article's pattern: short description in the main loop, full instructions only when needed.

### Sub-agents as tools vs full handoff

The article: keep a sub-agent only when one of the three tests holds, and then **call it as a tool** so the main agent keeps the conversation. Full handoff only when the specialist must talk to the user.

Prdfy: "The user has one counterpart: the orchestrator. Sub-agents do not speak to the user" (`prdfy/SKILL.md:63`). Every specialist returns a block (`NEED_USER`, `NEED_RESEARCH`, `MODULE_READY`, `RESEARCH`, `WROTE`, `VERIFY`, `REVIEW`). The orchestrator asks the questions in its own voice.

That is the article's tool-call pattern, not a handoff. It fits the one-voice rule. A full handoff would break it. Host one-line summaries that say "needs your answers" are a leak of the nested agent's voice. That is a host problem, not a missing protocol.

`NEED_USER` already is "Module/Research/Writer/C4 called as tools". There is no remaining schema change that cuts relay latency. What still costs time is the nested model loop and a full relaunch on every answer. `prdfy/SKILL.md:162` already allows resume when the host can resume. Folding the Research-Module chain is the latency change that is left.

### Why Prdfy should not adopt the article's "main agent does the work"

The article wants one model that talks **and** executes skills. Prdfy wants one model that talks **and does not** draft questions, search, or write deliverables (`prdfy/SKILL.md:51`).

That is a conflicting-instructions split, which is the article's third keep-test. It is also a product rule: leading questions and suggested answers must come from a specialist, then be relayed unchanged. Folding Module into the orchestrator would make the same window chat with the user and draft those suggestions.

Keep the relay. Do not treat "the main agent should do the work" as a Prdfy requirement. Treat it as an experiment, gated by evals, and only after the Research-Module merge is measured.

---

## 4. Role by role

Each role against the three keep-tests. **Keep** = stay a sub-agent. **Fold** = run as a skill inside the orchestrator loop. **Merge** = combine with another specialist.

### Research — merge into Module (interview modes); keep for pressure-test

What it does: search the public web in one named mode, write `findings/research-<mode>.md`, return a path. It does not interview and does not write a deliverable (`prdfy-research/SKILL.md:17`). Returns are compact: "Do not paste the whole file back" (`prdfy-research/SKILL.md:77`).

| Test | Applies? |
| --- | --- |
| Black-box verification | No. It produces evidence. |
| Parallel fresh context | Yes for noisy search, and the article names independent research paths as a keep. Interview modes are **not** parallel with Module. They run, then Module runs on the file. Pressure-test is one shot after all six modules, discarded before writing. |
| Conflicting instructions | Yes if merged into Module: Module is forbidden to search (`prdfy-module/SKILL.md:17`). Research is forbidden to interview. |

They chain on each other's output in the same module. Vision: ask, then `NEED_RESEARCH` category, then ask again (`prdfy-module/SKILL.md:95`). Risk: orchestrator launches compliance research, then Module, which can `NEED_RESEARCH` again (`prdfy/SKILL.md:254`, `prdfy-module/SKILL.md:134`). Boundaries: first action is `NEED_RESEARCH` (`prdfy-module/SKILL.md:145`). The article's merge rule is written for this pattern.

What folding interview-research into Module gains: one window sees the search and then asks; one fewer nested loop per gate; less telephone game through a findings file the orchestrator must pass onward (`prdfy/SKILL.md:171`).

What it loses: search noise in the interview window; a skill that both searches and asks; a second owner for "do not invent a statute". The findings **file** can stay. The separate **agent** does not need to, except for pressure-test.

Pressure-test is different. It runs after Architectural Boundaries, is not a question-gate, and dumps competitors, switching costs, and extra duties into a file every Writer reads (`prdfy/SKILL.md:264-272`). That is a fresh, discardable window. Keep it as `prdfy-research` mode `pressure-test`.

**Verdict: merge** category, compliance, and boundaries into `prdfy-module`. **Keep** `prdfy-research` for pressure-test (and for a standalone pressure-test rerun).

### Module — keep (do not fold into the orchestrator)

What it does: one module at a time, two to four questions, `NEED_USER` / `NEED_RESEARCH` / `MODULE_READY`, writes `findings/module-<name>.md` on close. The six briefs already live in **one** skill. That is the article's "do not split by problem type" done right.

| Test | Applies? |
| --- | --- |
| Black-box verification | No. |
| Parallel fresh context | No. Modules are ordered. "Do not open a later module in the same turn as an earlier one" (`prdfy/SKILL.md:49`). Sequential relaunch on every answer is not parallel work. |
| Conflicting instructions | Yes, with the orchestrator. One role must never draft questions (`prdfy/SKILL.md:51`). The other role's job is to draft them. |

Folding Module into the orchestrator is the inline fallback. The evals show that fallback can pass question-count, skip, revise, and resume checks. They do not show it is as good as a separate Module agent, because that path never ran.

Eval 2 still wants A-rows from the Module sub-agent, not from the orchestrator. Making inline the default would retire that expectation, not satisfy it.

**Verdict: keep** as a sub-agent. Merge Research **into it**. Do not fold Module into the orchestrator until evals 1, 2, and 5 are rerun on a host that can launch sub-agents, then compared with the same evals run inline.

### Writer — keep

What it does: one deliverable per launch, except the pair `00-decision-log.md` and `README.md` (`prdfy-writer/SKILL.md:18`). Compact `WROTE` (path + cite IDs). `07` is forbidden in this skill (`prdfy-writer/SKILL.md:157`).

The orchestrator launches `01`–`06` "all at the same time" (`prdfy/SKILL.md:288`). That looks like the article's parallel keep. Check whether it is real parallel work or batching:

- **`01`, `02`, `04`:** independent given memory and findings. Real parallel, fresh windows, discard after `WROTE`.
- **`05`:** waits on compliance findings (`prdfy/SKILL.md:288`), and its Requirements column lists `FR-` / `NFR-` IDs from `02` (`prdfy-writer/SKILL.md:133`). That is a chain, launched as if it were parallel.
- **`03`:** the Invariants table's Aggregate column "names an aggregate from `06-domain-architecture.md`" (`prdfy-writer/SKILL.md:104`). Launched with `06`, not after it. That is batching. Cross-verify exists in part because these two can drift (`prdfy-verifier/SKILL.md:49`).
- **`00` + `README`:** already one launch, after every other file (`prdfy/SKILL.md:290`). Correct.

Eval 7 never exercised six parallel writers. The inline host ran them as sequential role steps. The sub-agent interview never reached writing. So "parallel writers" is a design claim, not a measured speedup.

Still: each of `01`–`06` is a long document. A fresh window per file is the article's second keep-test for the ones that are actually independent. Folding all six into the orchestrator would bloat the conversation that still has to relay.

**Verdict: keep.** Do not fold Writers into the orchestrator. Do not merge C4 into this skill (see next). Optional later work, not in the first shortlist: write `06` before `03`, and `02` before `05`, so "all at the same time" only covers files that do not chain.

### C4 — keep (do not merge with Writer)

What it does: write `07-c4-architecture.md` from memory, findings, and `06-domain-architecture.md`. Same `WROTE` / `NEED_USER` shape as Writer. Different heading contract, C4 Mermaid templates, "Uses" ban, and "Level 4 must use the same aggregates as the domain architecture" (`prdfy-c4/SKILL.md:63`).

| Test | Applies? |
| --- | --- |
| Black-box verification | No. |
| Parallel fresh context | No. `07` waits until `06` is `written` or `verified` (`prdfy/SKILL.md:284`, `288-289`). Eval 7 confirmed that order. |
| Conflicting instructions | Yes, with Writer. Writer is prose and tables. C4 is four experimental Mermaid diagrams and a class diagram with a closed stereotype list. Writer already says "Do not write this file" (`prdfy-writer/SKILL.md:157`). |

They chain, so the article's merge rule fires. The chain is a **file**, not a lossy summary. That is split-by-context: C4 needs little except `06` and memory, and it returns a path. Merging them into one launch would put domain architecture and four C4 levels in one window. Merging the skill files but keeping two launches would cut a folder, not a nested loop.

Failed `07` already goes back to `prdfy-c4`, not to `prdfy-writer` (`prdfy/SKILL.md:319`). Keep that retry path simple.

**Verdict: keep.** Reject merging Writer and C4.

### Verifier — keep

What it does: check one or more deliverables against memory, findings, and the heading contract. Write `findings/verify-<file>.md` (and `verify-cross.md`). Return paths and verdicts. "You do not edit a deliverable" (`prdfy-verifier/SKILL.md:18`). "Do not include a rewritten paragraph" (`prdfy-verifier/SKILL.md:87`).

| Test | Applies? |
| --- | --- |
| Black-box verification | Yes. This is the article's generator-verifier pattern. |
| Parallel fresh context | Optional. One launch may cover several files (`prdfy/SKILL.md:319`, `prdfy-verifier/SKILL.md:20`). Fresh relative to the writer matters more than one window per file. |
| Conflicting instructions | Yes. A writer that also "checks its own work" will pass what it meant, not what it wrote. The inline fallback already warns that this is weaker (`prdfy/SKILL.md:196`). Eval 6's method note says the same. |

**Verdict: keep**, permanently. Record that one-line reason in the skills when they are next edited.

### Review — keep

What it does: read memory, contradictions, and verifier results. Write `findings/review.md`. Return exactly two questions (promote/reject an assumption; revise a deliverable). It does not speak to the user, edit deliverables, or choose (`prdfy-review/SKILL.md:17, 27`).

| Test | Applies? |
| --- | --- |
| Black-box verification | No. Verifier already did that. Review lists leftovers and asks. |
| Parallel fresh context | No. One launch, after verify, at most twice (`prdfy/SKILL.md:331`). |
| Conflicting instructions | Yes, with Verifier (must not ask the user, must not pick an assumption) and with the orchestrator (must not draft the two questions itself). |

It chains on Verifier output. Merging them would put "pass/fail this file" and "which assumption should the user promote" in one prompt. That is the article's third keep-test.

Folding Review into the orchestrator would make the voice that talks to the user also choose which `A-` IDs to list first. The skill already says listing is not choosing (`prdfy-review/SKILL.md:62`). Keep the split.

There is no scenario eval that stops on Review. Eval 6 covers Verifier only. Add a Review eval before treating this keep as measured.

**Verdict: keep**, permanently, as a separate agent from Verifier.

---

## 5. Ideas, accepted or rejected

### Merge Research into Module, keep Research for pressure-test — accept (first experiment)

**Change:** `prdfy-module` searches when a brief currently returns `NEED_RESEARCH` (category, compliance, boundaries). It still writes `findings/research-<mode>.md`. `NEED_RESEARCH` remains in the protocol for nothing, or is dropped in a protocol bump. `prdfy-research` keeps pressure-test, and any later standalone rerun of that mode.

**Expected benefit:** fewer nested loops in the interview (the Vision path drops from five launches toward three; compliance stops being a mandatory extra agent before the first Risk question). Module asks from what it just retrieved, not from a file the orchestrator forwarded. Less telephone game.

**Expected loss:** search hits sit in the interview window. The Module skill holds two jobs the current split keeps apart.

**Eval gate:** scenario evals **1, 3, and 4**. Eval 1: the orchestrator still does not search in the orchestrator role; the Module role may. Eval 3: no `research-*.md` on the first Vision turn; no unsourced market claim. Eval 4: a `research-compliance` file exists; no statute if jurisdiction is unnamed. If a host can launch sub-agents, count launches on a short interview and compare with the ~20–23 baseline. Do not ship this on protocol 1 without deciding whether `NEED_RESEARCH` stays.

### Merge Writer and C4 into one writer skill — reject

`07` cannot start before `06`. That is a file handoff, which is the article's good split, not a telephone game. Writer and C4 have conflicting output rules. One launch that writes both would bloat context. One skill file with two launches would not cut latency. The orchestrator already batches `00`+`README`. Eval 7 already gates the order.

Do not take this.

### Reduce relay latency by calling Module/Research as tools that return `NEED_USER` — reject (already true)

The orchestrator already does this (`prdfy/SKILL.md:137-169`). Every relaying role uses the same block. The orchestrator keeps talking to the user. Resume is already allowed.

Nothing in the relay format is left to change. Remaining latency is nested loops and spawn. The Research→Module merge is the change that addresses that. Host summaries that address "you" should stay out of the user-visible reply; that is a launch-brief fix, not a protocol fix.

### Keep Verifier and Review as separate agents permanently — accept

One-liners to record when the skills are next edited (not in this pass):

- Verifier: stay a sub-agent because a black-box check must not share the writer's window; inline verification is weaker.
- Review: stay a sub-agent, and stay separate from Verifier, because it must not rewrite a file and must not choose the assumption or the revision.

**Eval gate:** eval **6** for Verifier (verdict file exists, competitor names allowed, orchestrator does not edit the deliverable). Add a Review scenario eval that expects `findings/review.md`, exactly two questions, a `None` option under each, and no deliverable rewrite. Do not call the Review keep measured until that eval exists.

### Fold Module (or Writer) into the orchestrator as the default — reject for now

The inline fallback is that design, and it is the only design the scenario evals have run. That is evidence it **can** work. It is not evidence it should be the default.

Eval 2's remaining fail is the separation the fold would delete. Eval 6's own method note says inline verification is weaker. The one-voice rule plus "the orchestrator never does the work" is the third keep-test.

**Later experiment, not the first:** on a host that can launch sub-agents, run evals 1, 2, 5, and 6 twice, once with launches and once forced inline. Keep the current default unless the inline run matches on task-completion **and** on eval 6's "did not edit the deliverable" spirit.

### Other article advice Prdfy already satisfies — do not redo

Say so explicitly:

- **One owner of the system prompt and end-to-end quality.** The `prdfy` orchestrator skill. Sub-skills must not talk to the user or replace it.
- **Progressive disclosure.** Orchestrator never loads sub-skill bodies. It launches a role and that role reads its own `SKILL.md`.
- **Compact returns instead of pasting files.** `RESEARCH` is a path. `WROTE` is path plus cite IDs. `VERIFY` is path plus verdict. Findings stay on disk. "Pass those files onward. Do not retype them into the brief" (`prdfy/SKILL.md:171`).
- **Shared response schema for sub-agents.** `NEED_USER` is the same block for Module, Research, Writer, and C4.
- **Sub-agents called as tools, main agent keeps the conversation.** The relay. Not a full handoff.
- **Task-completion evals, one change at a time.** `evals/evals.json` plus `reviews/prdfy-fix-plan-3.md`. The 16/25 → 23/25 rerun is that method working.
- **Verifier may batch files in one launch.** Already in `prdfy/SKILL.md:319`.
- **`00` and `README` are one Writer launch.** Already in `prdfy/SKILL.md:290`.
- **Six modules in one Module skill.** Problem types were not given six agents.
- **Memory as the note-taking layer.** `prdfy-spec/memory.md` is the source of truth. Sub-agents do not edit it.

The article's "measure, change one thing at a time, keep what holds up" is already how this repo changed after the 2026-10-12 evals. Keep doing that.

---

## 6. Order of work

No change in this list should be made without rerunning the affected scenario evals. Trigger evals still have no score; do not use them as a gate until `claude -p` (or an equivalent) can run.

1. **Record the Verifier and Review keep-reasons** in those two skills (and one line in the orchestrator table). Rerun **eval 6**. Write a Review close-out eval and run it once so the Review keep is not only a paper argument.
2. **Do not merge Writer and C4. Do not change the `NEED_USER` schema.** No eval needed for a non-change. If a later change touches writing order, rerun **eval 7**.
3. **Merge interview Research into Module. Keep `prdfy-research` for pressure-test.** Rerun **evals 1, 3, and 4**. On a host that can launch sub-agents, repeat a short interview and compare launch count with the 2026-10-12 baseline (~20–23 through pressure-test). If eval 4 or 3 regresses, revert this merge.
4. **Only if step 3 holds:** comparison eval of sub-agent Module vs inline Module on **evals 1, 2, 5, and 6**. Do not make inline the default on theory. Do not fold Writer into the orchestrator in the same step.
5. **Optional, after that:** launch `06` before `03`, and `02` before `05`, so parallel writers are the independent set. Rerun **eval 7** and the Verifier `cross` path (eval 6 does not cover `cross`).

Stop after any fail. Do not batch two architectural changes into one eval run.
