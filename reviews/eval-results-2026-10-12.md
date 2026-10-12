# Prdfy eval results, 2026-10-12

First run of the `prdfy` orchestrator evals, following `.agents/skills/skill-creator/SKILL.md` ("Description Optimization" and "Running and evaluating test cases").

## Method

| Item | What happened |
| --- | --- |
| `claude` CLI | Installed (`2.1.241 (Claude Code)`), but unusable. `~/.claude/settings.json` routes all calls through `ANTHROPIC_BASE_URL=http://127.0.0.1:3001` with every model set to `auto`. Nothing listens on that port (curl exit 7), and a probe `claude -p` returned `API Error: Connection refused` after about 3 minutes. The user's settings were not changed. |
| Trigger evals | **Not run.** skill-creator says description optimization "requires the `claude` CLI tool (specifically `claude -p`)" and to skip it otherwise. It documents no judgment-based substitute, so no trigger results were produced or estimated. |
| Windows defect in `run_eval.py` | Found while preparing the run. `run_single_query` calls `select.select()` on a subprocess pipe, which raises `OSError [WinError 10093]` on Windows. `run_eval` catches that as "query failed" and records `False`, so on Windows every positive query fails and every negative passes (a fake 10/20). I patched a scratch copy only (a reader thread plus a queue). It was never exercised, because the CLI could not reach a model. The vendored script in the repo is unchanged. |
| Scenario evals | Run by 7 fresh, parallel `generalPurpose` subagents (not `claude -p`), each playing the Prdfy orchestrator from a scratch copy of the seven Prdfy skills. Each eval had its own working folder under `C:\tmp\prdfy-evals-2026-10-12\iteration-1\eval-<id>-<name>\with_skill\run-1\outputs\`, outside the repo. I did the Setup copies into each `prdfy-spec/` before launch. Executors were not shown the expectations. |
| Sub-agents inside a run | **None.** The executor subagents had no `Task` tool, so every run used the skill's documented fallback, "When the host cannot launch sub-agents". Any expectation about orchestrator/sub-agent separation is therefore weakly tested. |
| Baseline | Not run. skill-creator's baseline for an existing skill is the old version, and the skill was not edited, so an `old_skill` run would duplicate `with_skill`. |
| Grading | Inline, following `agents/grader.md` and using transcripts and output files. Programmatic checks: sha256 of fixture files against outputs, regex scans for technology and statute names, and `scripts/check_spec.py` on eval 7. Wrote `grading.json` and `eval_metadata.json` per run, `benchmark.json`/`.md` via `scripts.aggregate_benchmark`, and a static viewer at `iteration-1/review.html` via `eval-viewer/generate_review.py --static`. |
| Timing | Not captured. The subagent completion notices in this host do not include `total_tokens` or `duration_ms`. |
| Contamination | The eval 5 executor's Grep ignored its path argument and printed that eval's `expected_output` line from the repo's `evals.json`. It diverged from that output anyway. |
| Repo writes | Only this file. No commits. |

## Trigger evals (`evals/trigger-evals.json`)

Observed results: none. `claude -p` could not reach a model (see Method).

| # | Query | Expected | Observed | Pass |
| --- | --- | --- | --- | --- |
| 1 | I have an idea for an app that lets neighbours lend each other tools... | trigger | not run | n/a |
| 2 | prdfy: a marketplace for local tutors | trigger | not run | n/a |
| 3 | Before we write any code, I want a proper PRD and architecture for a clinic appointment system... | trigger | not run | n/a |
| 4 | help me scope an MVP for a subscription box for rare houseplants... | trigger | not run | n/a |
| 5 | ...internal tool for tracking equipment loans... domain model and boundaries... before we pick a stack? | trigger | not run | n/a |
| 6 | predify this: farmers sell surplus produce directly to restaurants | trigger | not run | n/a |
| 7 | I want a business plan, roadmap and compliance matrix for a new app... kids' sports club payments in the UK | trigger | not run | n/a |
| 8 | can we do a pre-coding spec for adding group bookings to our hall booking product?... | trigger | not run | n/a |
| 9 | My cofounder and I keep arguing about what the first release of our freelancer invoicing tool should include... | trigger | not run | n/a |
| 10 | Give me a C4 model for a product idea: a shared calendar for co-parents. Nothing exists yet. | trigger | not run | n/a |
| 11 | Draw a C4 container diagram of this repository's current services. | no trigger | not run | n/a |
| 12 | Write a FastAPI endpoint that creates a booking and returns 409 on a double booking. | no trigger | not run | n/a |
| 13 | Plan the next two sprints for our shipped mobile app based on the open Jira tickets. | no trigger | not run | n/a |
| 14 | Document the domain model of the existing codebase in src/ as markdown. | no trigger | not run | n/a |
| 15 | Fix the failing unit tests in the payments module. | no trigger | not run | n/a |
| 16 | Review this PRD I wrote and tell me if the acceptance criteria are testable. | no trigger | not run | n/a |
| 17 | What's the difference between a bounded context and an aggregate? | no trigger | not run | n/a |
| 18 | Convert this PlantUML sequence diagram to Mermaid. | no trigger | not run | n/a |
| 19 | Create a Next.js project with Tailwind and a login page. | no trigger | not run | n/a |
| 20 | Our app is live; write release notes for version 3.2 from the git log. | no trigger | not run | n/a |

Pass rate before: not measured. After: not measured.

## Description

**Unchanged.** The optimization loop could not run, so no held-out score exists to justify a change. The current description is 964 characters with no angle brackets. `quick_validate.py` returns "Skill is valid!" and `scripts/check_skills.py` returns "OK protocol 1, 15 roles, 7 skills".

To run this later:

1. Start the local gateway on port 3001, or point the CLI at a reachable endpoint.
2. Use a copy of skill-creator with the `select()` fix (or run under WSL).
3. Pass a concrete `--model` id; `auto` is rejected (`unrecognized_model`).
4. Run from a folder that has no `.claude/` above it. Otherwise `find_project_root` resolves to `C:\Users\Mo` and writes temporary command files into `~/.claude/commands`.

## Scenario evals (`evals/evals.json`)

Overall: **24/34 expectations (70.6%)**. The mean per-eval rate in `benchmark.json` is 69.6%. Its "+0.70 delta" compares against an empty baseline and is meaningless.

Failure kinds:
- **Skill**: the skill's own behaviour.
- **Env**: the host had no sub-agents.
- **Eval**: the expectation can't be reached at the stopping point, or the fixture is wrong.

### Eval 1: open the interview, technology recorded as a Rule (6/6)

| Expectation | Result | Evidence |
| --- | --- | --- |
| memory.md has a Rules row with an R- ID quoting PostgreSQL and React | PASS | `R-001: "We've already decided on PostgreSQL and React."` |
| Reply asks 2–4 questions, all about Vision | PASS | Four questions (current workaround, who requests, who pays, success); all four map to the Vision brief. |
| At most four suggestions each, presented as suggestions | PASS | Three per question; "Each option below is a suggestion, not a decision." |
| Does not open Scope or later | PASS | No Scope questions; Active module is Vision. |
| No file uses PostgreSQL or React as a role, container, or component | PASS | The only hit is the R-001 rule text in memory.md. |
| Orchestrator did not search or write findings itself | PASS (weak) | No search and no findings file, but no research was due and no sub-agent existed, so the second clause is vacuous. |

### Eval 2: skip Domain Rules (5/6)

| Expectation | Result | Evidence |
| --- | --- | --- |
| findings/module-domain-rules.md exists | PASS | Written by the inline Module role, "closed by `skip`". |
| At least one new open A- row for Domain Rules | PASS | A-001 to A-005, all `open`. |
| A- rows proposed by the Module sub-agent, not the orchestrator | FAIL (Env) | Rows came from the inline Module role's `MODULE_READY`. No separate sub-agent ran, so the separation can't be shown. |
| Reply shows both closing questions with suggestions | PASS | "What should be corrected…" (4 suggestions) and "Should we proceed…" (2). |
| No Strategy and MVP questions | PASS | Strategy appears only as the suggestion "Yes, proceed to Strategy and MVP." |
| Progress still names Domain Rules | PASS | `Active module: Domain Rules`. |

### Eval 3: no web search available (2/3)

| Expectation | Result | Evidence |
| --- | --- | --- |
| Any research-*.md says Unverified: yes and search unavailable | FAIL (Eval) | No research file exists. The Vision brief defers research until memory has a Vision answer, so this can't happen on turn one. |
| No unsourced market size, statistic, price, or competitor | PASS | None in memory.md or the reply; every suggestion is labelled `assumption`. |
| Reply asks 2–4 Vision questions | PASS | Four Vision questions. The no-search instruction was also recorded as R-001. |

### Eval 4: Risk and Compliance with no jurisdiction (3/4)

| Expectation | Result | Evidence |
| --- | --- | --- |
| Reply asks which jurisdictions the product serves | PASS | "Which countries, states, or regions will the product serve in its first release?" |
| 2–4 questions in total | PASS | Three. |
| No file names a statute or regulation | PASS | A regex scan of prdfy-spec/ and the reply found none. |
| A research-compliance findings file was written | FAIL (Skill) | Research never ran. The orchestrator ran the Module first because its brief gates on jurisdiction; `prdfy-research` would have written the file "before either return". |

### Eval 5: revise D-003 (operators out of v1) (1/5)

| Expectation | Result | Evidence |
| --- | --- | --- |
| D-003 still exists with status superseded | FAIL (Skill) | Still `confirmed`. |
| D-003's Superseded by names a new D- ID | FAIL (Skill) | Empty. |
| New Scope D- row, source user, operators out of v1 | FAIL (Skill) | None. The revise returned `NEED_USER` with two clarifying questions: what the single manager does, and whether that means one account or one role. |
| Original wording of D-003 unchanged | PASS | Byte-identical to the fixture. |
| Progress still names Risk and Compliance | FAIL (Skill) | Rewritten to "Scope (revise D-003, awaiting user answer); resume Risk and Compliance afterwards". |

### Eval 6: verify the business plan with a researched competitor (3/4)

| Expectation | Result | Evidence |
| --- | --- | --- |
| findings/verify-01-business-plan.md exists | PASS | Present. |
| Verdict is PASS | FAIL (Eval) | Verdict FAIL. One major issue: the success metric is labelled `user, D-003`, but D-003 is the MVP scope. The verifier is right; the fixture's business plan is wrong. |
| Hallkeeper not reported as a forbidden name | PASS | Accepted as a competitor sourced from research-category.md with a location. |
| Orchestrator did not edit 01-business-plan.md | PASS | sha256 matches the fixture. The Writer retry relayed `NEED_USER` and wrote nothing. |

### Eval 7: resume in the writing phase (4/6)

| Expectation | Result | Evidence |
| --- | --- | --- |
| One sentence says the run is in the writing phase | PASS | "We're picking up in the writing phase." |
| Does not restart the interview or ask Vision questions | PASS | The four questions are Writer/C4 relays about cancellation and the payment terminal. |
| 01 and 02 not rewritten | PASS | Both sha256 match the fixtures. |
| 07 written only after 06 | FAIL (Eval) | C4 ran after 06 returned `WROTE` (correct order), but it relayed, so 07 does not exist. |
| 00 and README written last, in one launch | FAIL (Eval) | Not written. They are correctly blocked, because 03 and 07 are still pending. |
| Every written file follows the H1/H2 contract | PASS | `check_spec.py` reports no heading issues for 04, 05, or 06. |

## Skill problems the runs reveal

These are not fixed. They are ordered by impact.

1. **A `revise` doesn't resolve in one turn when the user's change is clear.** `prdfy-module/SKILL.md` (opening section, the `revise D-<n>` paragraph) says "Ask with `NEED_USER` if the change leaves something unclear", with no test of what counts as unclear. It doesn't say to write the parts that are clear and record the rest as `A-` rows. In eval 5 the module relayed instead of superseding D-003. `prdfy/SKILL.md` "Changing an earlier decision" also doesn't say what happens to Progress during a revise, so the orchestrator rewrote `Active module`.
2. **Memory has no place for the user's own unprompted words.** In `prdfy/SKILL.md` "Memory", the template has Rules, Decisions (Module-proposed only), Q&A (answers to questions asked), and Assumptions. The opening pitch (evals 1 and 3) and a mid-run correction (eval 5) fit none of them. Executors either dropped the pitch from memory or invented a Q&A row whose question was "(none asked; unprompted change)".
3. **Jurisdiction is gated in two places, and the orchestrator must read a sub-skill to route.** `prdfy-module/SKILL.md` "Risk and Compliance" says to ask jurisdiction before any search. `prdfy-research/SKILL.md` "Compliance" mode also asks it and writes a findings file. `prdfy/SKILL.md` Execution §2 step 1 ("Launch Research when this brief says to search") makes the orchestrator read the module brief, which conflicts with "Do not follow the sub-agent skill yourself" in "Sub-agents". In eval 4 Research never ran and no compliance file was written.
4. **No rule for two relays in the same turn.** `prdfy/SKILL.md` "Relay" and Execution §4 assume one `NEED_USER` at a time. Parallel Writers plus C4 can relay together. In eval 7 two relays were merged into four questions, which fits the limit only by luck; three relays could not fit.
5. **A resume trusts Progress without checking prerequisites.** In `prdfy/SKILL.md` Execution §1, "continue from that phase" let eval 7 write `05-risk-compliance.md` with no pressure-test or compliance findings at all, even though Phase said `writing`. Nothing tells the orchestrator to check that §3's findings exist first.
6. **"Skip" is both a Rule and a module instruction.** `prdfy/SKILL.md` "Memory" counts "a topic to skip" as a Rule, and Execution §2 step 5 has a separate `skip` flow. In eval 2 the skip became a permanent R-001. The template's closing suggestion "Not yet. Keep working on…" then arguably breaks that rule.
7. **The roadmap contract doesn't say how to show an empty horizon.** `prdfy-writer/SKILL.md` `04-strategy-roadmap.md` says Now, Next, Later is "mapped to scope decisions by `D-` ID". The writer left Next and Later as "Not applicable" rows with empty Decisions and Source cells, and `scripts/check_spec.py` rejects those cells.
8. **When to give the inline-fallback warning is unspecified.** `prdfy/SKILL.md` "When the host cannot launch sub-agents" says "Tell the user once that inline verification is weaker" but not when. All seven runs said it in the first reply, even mid-interview.

## Eval-set problems (not skill problems)

- **Unreachable at the stopping point:**
  - Eval 3 expectation 1: research can't run on the first turn.
  - Eval 7 expectations 4 and 5: 07, 00, and README can't exist while Writer and C4 relays are open.
  - Eval 1 expectation 6 passes vacuously.
- **Wrong fixture in eval 6:** `files/spec-with-competitors/01-business-plan.md` labels the success metric `user, D-003`, but D-003 is the MVP scope, so a correct verifier must FAIL it.
- **Eval 4 expects a path the skill doesn't prescribe:** it requires a research-compliance file, but the skill (problem 3) allows the Module-first path that never writes one.
- **Odd data in the `files/writing/memory.md` fixture:**
  - D-007 is "superseded by" the lower ID D-002.
  - There is no `findings/` folder, although Phase is `writing`.
  - Its 01 cites claims memory doesn't hold (for example, "committee pays").
- **The host can't launch sub-agents:** any expectation about orchestrator/sub-agent separation (eval 1 expectation 6, eval 2 expectation 3) needs a host that can launch them.

## Rerun after fixes

Second run of scenario evals 2, 4, 5, 6, and 7, after the edits in `reviews/prdfy-fix-plan-3.md`. Evals 1 and 3 were not rerun. Eval 3 expectation 1 and eval 7 expectations 4 and 5 were rewritten before this run, because the first run could not reach them at the stopping point. Eval 4's compliance-file expectation was left as written.

### Method

Five fresh runners, one per eval. Each working folder is under `C:\tmp\prdfy-evals-2026-10-12\rerun-after-fixes\eval-<id>\`, outside the repo. The eval's `evals/files/<name>/` was copied into that folder's `prdfy-spec/` before launch. Runners were not shown the expectations. None of them could launch sub-agents, so every run used the inline fallback. The warning was given once, at the start of the first inline step. Scratch output stayed in those folders.

### Pass counts

| Eval | Before | After |
| --- | --- | --- |
| 2 Skip Domain Rules | 5/6 | 5/6 |
| 4 Risk, no jurisdiction | 3/4 | 4/4 |
| 5 Revise D-003 | 1/5 | 5/5 |
| 6 Verify business plan | 3/4 | 3/4 |
| 7 Resume in writing | 4/6 | 6/6 |
| These five | 16/25 | 23/25 |

Eval 7's after count uses the rewritten expectations 4 and 5. The first run's versions of those two could not be reached while a relay was open.

### Eval 2: skip Domain Rules (5/6)

| Expectation | Result | Evidence |
| --- | --- | --- |
| findings/module-domain-rules.md exists | PASS | Written by the inline Module role, closed by skip. |
| At least one new open A- row for Domain Rules | PASS | A-001, Domain Rules, status open. |
| A- rows proposed by the Module sub-agent, not the orchestrator | FAIL (Env) | The same runner played both roles. No separate sub-agent ran. |
| Reply shows both closing questions with suggestions | PASS | "What should be corrected…" and "Should we proceed…", each with suggestions. |
| No Strategy and MVP questions | PASS | Strategy appears only as the suggestion "Yes, proceed to Strategy and MVP." |
| Progress still names Domain Rules | PASS | Active module: Domain Rules. |

The skip was not written as a Rule. The user's words are under Unprompted.

### Eval 4: Risk and Compliance with no jurisdiction (4/4)

| Expectation | Result | Evidence |
| --- | --- | --- |
| Reply asks which jurisdictions the product serves | PASS | First question: "Which jurisdictions does the product serve, and which regulated activities apply?" |
| 2–4 questions in total | PASS | Four. |
| No file names a statute or regulation | PASS | `research-compliance.md` says jurisdiction is not named, so no statute was searched. No statute name appears. |
| A research-compliance findings file was written | PASS | `findings/research-compliance.md`, Findings: None. |

### Eval 5: revise D-003 (5/5)

| Expectation | Result | Evidence |
| --- | --- | --- |
| D-003 still exists with status superseded | PASS | Status `superseded`. Decision text unchanged. |
| D-003's Superseded by names a new D- ID | PASS | D-006. |
| New Scope D- row, source user, operators out of v1 | PASS | D-006, Scope, source user: operators are out of scope for v1; only residents and a single manager. |
| Original wording of D-003 unchanged | PASS | "Operators manage bookings through an Operator Client in the first release." |
| Progress still names Risk and Compliance | PASS | Phase interview. Active module: Risk and Compliance. |

The correction is under Unprompted. Questions and answers still has only QA-001. No clarifying questions were asked before the supersede. The reply then asks four Risk and Compliance questions.

### Eval 6: verify the business plan (3/4)

| Expectation | Result | Evidence |
| --- | --- | --- |
| findings/verify-01-business-plan.md exists | PASS | Present. |
| Verdict is PASS | FAIL | Verdict FAIL. The success metric now matches D-003, and that check is marked passed. Three major issues remain: two Alternatives sentences are not in the findings, and the revenue model is read as contradicting D-002 ("the hall committee pays"). |
| Hallkeeper not reported as a forbidden name | PASS | Accepted as a competitor from research-category.md. |
| Orchestrator did not edit 01-business-plan.md | PASS | sha256 matches the fixture copy made before the run. |

### Eval 7: resume in the writing phase (6/6)

| Expectation | Result | Evidence |
| --- | --- | --- |
| One sentence says the run is in the writing phase | PASS | "The run had reached writing with the business plan and the product requirements already written…" |
| Does not restart the interview or ask Vision questions | PASS | The two questions are about who may cancel a single booking. One relay only. A second writer relay was not asked. |
| 01 and 02 not rewritten | PASS | sha256 matches the copies made before the run. |
| 07 is not written before 06, and not while a relay is open | PASS | 06 exists. 07 does not. The specifications relay is unanswered. |
| 00 and README are not written while an earlier file is pending or a relay is open | PASS | Neither file exists. 03 and 05 are still pending. |
| Every written file follows the H1/H2 contract | PASS | 04 and 06 use the writer headings, in order. Next and Later are `None confirmed`. |

Pressure-test and compliance findings were written before any new deliverable. 05 was not written. The compliance file names no statute, because jurisdiction in memory is an explicit unknown.

## Artifacts (outside the repo)

`C:\tmp\prdfy-evals-2026-10-12\` holds:
- `iteration-1/` with per-run `outputs/` (prdfy-spec, `reply.md`, `transcript.md`, `user_notes.md`), `grading.json`, and `eval_metadata.json`;
- `benchmark.json`, `benchmark.md`, and the static viewer `review.html`;
- `write_grades.py`;
- the patched `skill-creator/` copy and the `skills/` snapshot used by the runs;
- `rerun-after-fixes/eval-<id>/` with `prdfy-spec/` and `reply.md` for evals 2, 4, 5, 6, and 7.
- `eval-6-fixture-fix/` with `prdfy-spec/` for the fixture fix below.

## Eval 6 fixture fix

The business plan fixture was rewritten, then eval 6 was rerun in `C:\tmp\prdfy-evals-2026-10-12\eval-6-fixture-fix\`. This host cannot launch sub-agents, so verification was inline and is weaker than a separate sub-agent. `check_spec.py` was not run: the fixture is not a full spec. The plan was judged against the verifier checks directly.

### What changed in `01-business-plan.md`

Alternatives now quotes the findings, with those source names:

- Community halls often use a shared paper or phone diary instead of software (research, Village Halls Weekly).
- Hallkeeper sells per-venue subscriptions aimed at commercial event spaces (research, Hallkeeper pricing page).

Revenue model now restates D-002 and keeps A-001 as an assumption. It does not say the committee is not the payer, and it does not mark revenue not applicable:

- The hall committee pays; residents and one manager use the product (user, D-002). The committee does not charge for the product (assumption, A-001).

The success metric is still the D-003 sentence. Memory and `research-category.md` were not edited.

### Verdict

PASS. One minor: the value proposition cites Hallkeeper for the shared phone diary as well as for Hallkeeper. That breaks no check. Scratch verdict: `eval-6-fixture-fix/prdfy-spec/findings/verify-01-business-plan.md`.

### Expectations (4/4)

| Expectation | Result | Evidence |
| --- | --- | --- |
| findings/verify-01-business-plan.md exists | PASS | Written in the scratch `prdfy-spec/findings/`. |
| Its verdict is PASS | PASS | Verdict PASS. Alternatives match the findings. Revenue restates D-002 and cites A-001. |
| It does not report Hallkeeper as a forbidden vendor or technology name | PASS | Hallkeeper is accepted as a competitor from research-category.md. |
| The orchestrator did not edit 01-business-plan.md | PASS | sha256 `1412d91513ac9897867428c72c0840f6e9285e764d59e9b88983f040d8195e40` matches the fixture copy made before verification. |
