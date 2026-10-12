# Prdfy fix plan 3: scenario-eval skill bugs

Source: `reviews/eval-results-2026-10-12.md`, section "Skill problems the runs reveal". The first pass (`reviews/prdfy-fix-plan.md`) and the second (`reviews/prdfy-fix-plan-2.md`) are already done. This pass fixes the eight skill problems from that eval run, then the eval-side faults the same file names. It does not re-open earlier review items.

**Status: done (2026-10-12).** Checks run:

- All seven skills pass `quick_validate.py`.
- `scripts/check_skills.py` passes: protocol 1, 15 roles, 7 skills.
- `scripts/check_spec.py` passes on `tests/fixtures/minimal-spec` (9 files).
- `pytest tests` passes 17 tests.
- Scenario evals 2, 4, 5, 6, and 7 were rerun with inline fallback. Those five went from 16/25 to 23/25. Remaining fails: eval 2 sub-agent separation (this host cannot launch sub-agents), and eval 6's verdict (the success-metric mislabel is fixed; the rerun verifier fails other sentences the results file did not name).

Versions: `prdfy` 2.1.0, `prdfy-writer` 1.5.0, `prdfy-verifier` 1.5.0, `prdfy-module` 1.4.0, `prdfy-research` 1.4.0, `prdfy-c4` 1.4.0, `prdfy-review` 1.4.0. Every skill still declares protocol 1.

Tick each box when the edit is in. Each step lists the files it touches.

## Design decisions

These resolve the open choices in the results file. Every step follows them.

- **A clear revise lands immediately.** The replacement is clear when the user's words state the new decision, including who is in and who is out. The Module returns `MODULE_READY` at once. It asks only when the replacement itself is ambiguous: the words do not say what replaces the old decision, or they name two replacements that cannot both be true. The question is only about that ambiguity. Progress keeps the active module. The orchestrator writes the new rows, marks the old row superseded, and does not ask the revise return's closing questions. It does not restart the revised module or the active module.
- **Unprompted words have their own section.** Memory gains `## Unprompted` for the opening pitch and for a correction that is not the answer to a question. The orchestrator writes those words there before the next launch. Sub-agents read them. They are not a Questions and answers row, and they are not a decision until a Decisions row records them.
- **Compliance research has one owner.** The Module returns `NEED_RESEARCH` mode `compliance` only when jurisdiction is known and the compliance findings do not yet cover it. Jurisdiction is known when memory names a place the product serves, or records an explicit unknown. Research in mode `compliance` assumes jurisdiction is in memory and does not relay to ask for it. If none is named, it writes the findings file with no statute. The orchestrator launches that research before any Risk and Compliance question, without reading the module skill. A findings file that only says jurisdiction was not named does not count as covering a jurisdiction named later.
- **Two relays are two turns.** If two relays arrive in one turn, the orchestrator asks the first relay, waits, and only then asks the second. It does not merge the questions. If arrival order is unclear, deliverable order wins, and a Module relay comes before a Writer relay.
- **Prerequisites beat the recorded phase.** Before writing a file, the required findings must exist. Pressure-test research comes before files 01 to 06. Compliance research comes before `05-risk-compliance.md`. `06-domain-architecture.md` comes before C4. If one is missing, that step runs first. A Writer is launched only for a file that is `pending`, `stale`, or `failed`.
- **A module skip is one time.** "Skip" on the active module is the skip step. It is not a Rule. A Rule is written only when the user says to skip that topic from then on.
- **An empty horizon is words, not a blank cell.** In `04-strategy-roadmap.md`, Now, Next, and Later are three table rows. An empty horizon writes `None confirmed` in Decisions and in Source. The checker already treats a non-empty cell as filled, so `None confirmed` passes. A blank cell still fails.
- **The inline warning has a moment.** When the host cannot launch sub-agents, the warning is given once, at the start of the first inline step, and is not repeated. It is not given before that step.
- **Return blocks stay protocol 1.** `NEED_USER`, `NEED_RESEARCH`, `MODULE_READY`, and the other return blocks stay as they are. `metadata.protocol` stays `"1"`.
- **Eval expectations.** Eval 6's business plan is mislabeled; fix the fixture so a correct verifier can pass it. Eval 3 expectation 1 and eval 7 expectations 4 and 5 cannot be reached at the first user wait; rewrite those expectations to what that stop can show. Leave eval 4's compliance-file expectation in place: the skill change makes the file get written. Do not weaken an expectation that caught a real skill bug.

## Steps

### Step 1: Unprompted section in memory
Files: `prdfy/SKILL.md`, `prdfy-module/SKILL.md`, `prdfy-research/SKILL.md`, `prdfy-writer/SKILL.md`, `prdfy-c4/SKILL.md`, `prdfy-verifier/SKILL.md`, `prdfy-review/SKILL.md`
- [x] Add `## Unprompted` to the memory template, between Questions and answers and Assumptions.
- [x] Orchestrator: record the opening pitch and any unasked correction there before the next launch. Do not invent a Questions and answers row. Add the section if an older memory file lacks it.
- [x] Say the six sections when the host cannot write files.
- [x] Each sub-skill: read Unprompted. It is not a Questions and answers row and not a decision by itself.

### Step 2: Clear revise, then back to the active module
Files: `prdfy/SKILL.md`, `prdfy-module/SKILL.md`
- [x] Module: supersede at once when the user stated the new decision. `NEED_USER` only when the replacement itself is ambiguous.
- [x] Orchestrator: do not change Active module. Do not ask the revise closing questions. Do not restart either module. Continue the active module from where it stood.

### Step 3: One owner for jurisdiction
Files: `prdfy/SKILL.md`, `prdfy-module/SKILL.md`, `prdfy-research/SKILL.md`
- [x] Module: ask jurisdiction while it is unknown. Return `NEED_RESEARCH` mode `compliance` only once it is known and the findings do not cover it.
- [x] Research compliance: do not relay for jurisdiction. If none is named, write the findings file and name no statute.
- [x] Orchestrator: launch that research before any Risk and Compliance question. Do not read the module skill to decide this. Replace "when this brief says to search".

### Step 4: Two relays, two turns
Files: `prdfy/SKILL.md`
- [x] In Relay, and again under writing: do not merge questions from two relays. Ask the first relay first.

### Step 5: Prerequisites before writing
Files: `prdfy/SKILL.md`
- [x] On resume, do not trust Phase alone.
- [x] Pressure-test findings before files 01 to 06. Compliance findings before `05-risk-compliance.md`. Domain architecture before C4. Run the missing step first.
- [x] Launch a Writer only for `pending`, `stale`, or `failed`.

### Step 6: Skip is not a standing Rule
Files: `prdfy/SKILL.md`
- [x] A one-time skip of the active module is the skip step, not a Rule.
- [x] A Rule is written only when the user says to skip that topic from then on.

### Step 7: Empty roadmap horizon
Files: `prdfy-writer/SKILL.md`, `scripts/check_spec.py`, `tests/fixtures/minimal-spec/04-strategy-roadmap.md`, `tests/test_check_spec.py`
- [x] Writer: Now, Next, Later is a three-row table. An empty horizon is `None confirmed` in Decisions and Source, not a blank cell and not `Not applicable`.
- [x] Checker: keep rejecting a blank cell. `None confirmed` stays a filled cell. Lock that with the fixture and a test.

### Step 8: Inline-fallback warning
Files: `prdfy/SKILL.md`
- [x] Give the warning once, at the start of the first inline step. Do not repeat it, and do not give it before that step.

### Step 9: Eval fixture and unreachable expectations
Files: `.agents/skills/prdfy/evals/files/spec-with-competitors/01-business-plan.md`, `.agents/skills/prdfy/evals/evals.json`
- [x] Eval 6: label the success metric with the decision it actually states (D-003 is the MVP slice).
- [x] Eval 3 expectation 1: research is not due on the first Vision turn.
- [x] Eval 7 expectations 4 and 5: 07, 00, and README need not exist while a relay is open; they must not be written out of order.
- [x] Do not change eval 4's compliance-file expectation. Do not edit `run_eval.py`.

### Step 10: Verify
- [x] Bump `metadata.version` on every changed skill. Leave `metadata.protocol` at `"1"`.
- [x] `quick_validate.py` on all seven skills.
- [x] `scripts/check_skills.py`.
- [x] `scripts/check_spec.py` on `tests/fixtures/minimal-spec`.
- [x] `pytest tests`.

### Step 11: Rerun scenario evals 2, 4, 5, 6, and 7
- [x] Fresh subagent per eval, working folder under `C:\tmp`, stop at the first user wait. Inline fallback if the host cannot launch sub-agents. No scratch output in the repo.
- [x] Append a "Rerun after fixes" section to `reviews/eval-results-2026-10-12.md` with before/after pass counts.
- [x] Tick this plan and put a status line at the top.

## Out of scope

Trigger evals, the vendored `run_eval.py`, `.github/workflows/checks.yml`, and the CI sentence in `README.md`. The odd rows in `evals/files/writing/memory.md` stay; the prerequisite check covers the missing findings. Eval 1's vacuous sub-agent expectation and eval 2's sub-agent separation stay env limits of this host.
