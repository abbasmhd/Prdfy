# Prdfy fix plan 4: agent-loop recommendations

Source: `reviews/article-analysis-agent-loop.md`. The user approved all three recommendations, in that order. Earlier passes (`reviews/prdfy-fix-plan.md`, `prdfy-fix-plan-2.md`, `prdfy-fix-plan-3.md`) are already done. This pass records the keep-reasons, records the Writer/C4 non-merge, then folds interview research into the Module skill.

**Status: done (2026-11-02).** The merge shipped. Protocol stays `"1"` on every skill. Checks run:

- All seven skills pass `quick_validate.py`.
- `scripts/check_skills.py` passes: protocol 1, 15 roles, 7 skills.
- `scripts/check_spec.py` passes on `tests/fixtures/minimal-spec` (9 files).
- `pytest tests` passes 27 tests.
- Scenario evals 1, 3, 4, 6, and 8 were rerun with inline fallback. All 21/21 expectations passed. Eval 1 and 4 did not regress, so change 3 was not reverted.

Versions at end: `prdfy` 2.4.0, `prdfy-module` 1.6.0, `prdfy-research` 1.5.0, `prdfy-verifier` 1.6.0, `prdfy-review` 1.5.0, `prdfy-writer` 1.5.0, `prdfy-c4` 1.4.0.

Tick each box when the edit is in. Each step lists the files it touches.

## Design decisions

These resolve the open choices in the analysis. Every step follows them.

- **Verifier and Review stay separate agents.** One short line each, in the existing voice. Verifier: an independent black-box check that does not share the writer's context. Review: a close-out that judges across all files, not one. The orchestrator Sub-agents section states that both stay separate by design.
- **Writer and C4 stay separate.** No skill merge. No `NEED_USER` schema change. C4 needs `06`'s aggregates, and Writer files run in parallel. The relay already keeps the orchestrator talking to the user. Record that under a Decision heading in the analysis file.
- **Interview research moves into Module. Pressure-test stays in Research.** Category, compliance, and boundaries search run inside `prdfy-module` before that module proposes questions. `prdfy-research` runs only the standalone pressure-test before drafting. The findings **file** format stays. The separate **agent** for those three interview modes does not.
- **`NEED_RESEARCH` is dropped from Module and from the orchestrator interview flow.** Protocol stays `"1"` because every remaining return block (`NEED_USER`, `MODULE_READY`, `RESEARCH`, `WROTE`, `VERIFY`, `REVIEW`) is unchanged. Nothing still returns `NEED_RESEARCH`.
- **Vision searches first unless the file already exists.** The existing guard is the findings file in the prompt: if `research-category` is already there, do not search again. The old "ask the first questions because the category is not known yet" wait is gone. Eval 3 expectation 1 is rewritten to match: when search is unavailable, a `research-category` file exists and is marked unverified, then Vision questions are asked. No unsourced market claim.
- **Risk still asks jurisdiction before any statute search.** If jurisdiction is unknown, that is `NEED_USER`. Do not guess a statute. To keep eval 4, the Module still writes `research-compliance.md` when none exists (Findings: None; jurisdiction not named; no statute searched), then asks. A file that only says jurisdiction was not named does not cover a jurisdiction named later.
- **Architectural Boundaries still researches first.** The Module runs that search itself. Do not return `NEED_USER` on that first launch before the search.
- **Orchestrator does not launch Research per interview module.** Execution §2 step 1 passes any existing findings files. Execution §3 (pressure-test) is unchanged. If `research-compliance` is missing before `05-risk-compliance.md`, the Module sub-agent writes that file (search if jurisdiction is known; otherwise no statute). Do not launch `prdfy-research` for compliance.
- **Return blocks and file formats stay identical** across skills for `NEED_USER` and for findings files (Findings, Contradictions, Superseded, Unverified, with Source/Type/Location/Accessed).
- **Eval 8 can reach Review.** Memory with Phase `review`, open `A-` rows, and a `verify-cross` note is enough. The run stops at the two REVIEW questions. Include one deliverable so "no rewrite" can be checked.
- **Launch-count check runs only when a sub-agent host is available.** The inline fallback has no sub-agent host to count launches. Do not treat a missing count as a fail.
- **If eval 1 or 4 regresses after change 3, revert change 3 only.** Keep changes 1 and 2. Note the revert in the results file. Do not ship the merge.

## Steps

### Step 1: Plan
Files: `reviews/prdfy-fix-plan-4.md`
- [x] Write this plan.

### Step 2: Change 1 — keep-reasons for Verifier and Review
Files: `.agents/skills/prdfy-verifier/SKILL.md`, `.agents/skills/prdfy-review/SKILL.md`, `.agents/skills/prdfy/SKILL.md`
- [x] Verifier: one short line near the top, why it stays a separate agent (independent black-box; does not share the writer's context). Bump to 1.6.0.
- [x] Review: one short line near the top, why it stays a separate agent (close-out across all files, not one). Bump to 1.5.0.
- [x] Orchestrator Sub-agents section: one or two sentences that these two roles stay separate agents by design. Bump `prdfy` to 2.3.0.

### Step 3: Change 1 — Review eval (eval 8)
Files: `.agents/skills/prdfy/evals/evals.json`, `.agents/skills/prdfy/evals/files/at-review/`
- [x] Add eval 8. Prompt copies `evals/files/at-review/` into `prdfy-spec/`, then runs the review close-out.
- [x] Fixture: memory with Phase `review`, open `A-` rows, Unprompted, Progress listing files; `findings/verify-cross.md`; one deliverable (`01-business-plan.md`) that must not be rewritten.
- [x] Expectations: `findings/review.md` exists; the reply asks exactly two questions; each has a `None` option; no deliverable rewrite.

### Step 4: Change 2 — record the Writer/C4 decision
Files: `reviews/article-analysis-agent-loop.md`
- [x] Short "Decision" heading: kept Writer and C4 separate because C4 needs `06`'s aggregates and Writer files run in parallel; the relay already keeps the orchestrator talking to the user. Do not merge. Do not change `NEED_USER`.

### Step 5: Change 3 — Module searches
Files: `.agents/skills/prdfy-module/SKILL.md`
- [x] Description: the Module may search for its own module. Do not forbid search.
- [x] Opening: search is allowed. Remove `NEED_RESEARCH` from the returns. Keep `NEED_USER` and `MODULE_READY` identical.
- [x] Copy research rules in spirit: never invent a statistic, customer, price, quote, or regulation name; a finding without a source name and location is not a finding; if search is unavailable, say so and mark claims unverified.
- [x] Write `prdfy-spec/findings/research-<mode>.md` in the same file format (Findings, Contradictions, Superseded, Unverified, with Source/Type/Location/Accessed). Numbered reruns. Never overwrite.
- [x] Vision: search for the category first unless `research-category` is already in the prompt.
- [x] Risk and Compliance: jurisdiction via `NEED_USER` if unknown; no statute guess; write a no-statute `research-compliance` file when none exists; search once jurisdiction is known and the file does not cover it.
- [x] Architectural Boundaries: run boundaries search first, then ask.
- [x] Bump to 1.6.0.

### Step 6: Change 3 — orchestrator
Files: `.agents/skills/prdfy/SKILL.md`
- [x] "Search, then ask": Module searches for the active module; launch `prdfy-research` only for the standalone pressure-test before drafting.
- [x] Execution §2 step 1: do not launch Research per module; pass any existing findings files.
- [x] Sub-agents table: Research row is pressure-test only. Module row may mention search.
- [x] Remove interview `NEED_RESEARCH` handling. Execution §3 unchanged.
- [x] Before `05`, if `research-compliance` is missing, the Module writes it. Do not launch `prdfy-research` in mode `compliance`.
- [x] Bump `prdfy` to 2.4.0.

### Step 7: Change 3 — Research is pressure-test only
Files: `.agents/skills/prdfy-research/SKILL.md`
- [x] Description and body: standalone pressure-test before drafting. Interview research moved into `prdfy-module`.
- [x] Remove category, compliance, and boundaries modes. Keep pressure-test, shared file rules, and the `NEED_USER` relay block.
- [x] Bump to 1.5.0.

### Step 8: Change 3 — eval 3 wording
Files: `.agents/skills/prdfy/evals/evals.json`
- [x] Eval 3 expected output and expectation 1: Vision now searches on the first turn. When search is unavailable, `research-category` exists and is unverified. Still no unsourced market claim. Still two to four Vision questions.

### Step 9: Verify
- [x] `quick_validate.py` on every changed skill dir.
- [x] `uv run scripts/check_skills.py`.
- [x] `uv run scripts/check_spec.py tests/fixtures/minimal-spec`.
- [x] `uv run --python 3.11 --with pytest --with pyyaml pytest tests -q`.
- [x] Grep: no `NEED_RESEARCH` in `prdfy-module` or `prdfy` (except a pressure-test mention, if any). No `Launch Research when this brief says to search`.

### Step 10: Rerun gating evals
- [x] Eval 6 after change 1 (Verifier keep). Eval 8 after the fixture exists. Both were scored on the post-merge skills; eval 6 still 4/4.
- [x] Evals 1, 3, and 4 after change 3. Fresh folders under `C:\tmp`, not in the repo. Copy each eval's files into `prdfy-spec/` per the Setup line. Follow the prdfy skill. Stop at the first user wait. Inline fallback if sub-agents cannot launch; say so. Launch-count only if a sub-agent host is available.
- [x] If eval 1 or 4 regresses, revert change 3 skill files only (`git checkout` those files), keep changes 1–2, and do not ship the merge. Neither regressed. The merge shipped.
- [x] Append a "Research-into-Module trial" section to `reviews/eval-results-2026-10-12.md` with before/after pass counts and remaining failures.

### Step 11: Commit and push
- [x] `Fix(prdfy): record verifier and review keep-reasons` (change 1 + eval 8).
- [x] `Fix(prdfy): fold interview research into the module skill` (change 3), only if the eval gate passed.
- [x] `Docs(reviews): record the agent-loop analysis decisions` (Decision heading, this plan, eval results section).
- [x] Push `origin main`.

## Out of scope

Trigger evals, `run_eval.py`, `.github/workflows/checks.yml`, folding Module or Writer into the orchestrator, merging Writer and C4, changing `NEED_USER`, making inline the default, and the optional later work to write `06` before `03` and `02` before `05`. README interview wording is not in this pass. Protocol stays `"1"`.
