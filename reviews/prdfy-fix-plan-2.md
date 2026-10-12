# Prdfy fix plan 2: rest of section 2, and sections 3 and 4

Source: `reviews/prdfy-skills-review.md`. The first pass (`reviews/prdfy-fix-plan.md`) covered section 1 and items 2.1, 2.2, and 2.10. This pass covers everything else: 2.3 to 2.9, 2.11, all of section 3, and all of section 4.

Tick each box when the edit is in.

**Status: done (2026-10-12).** Checks run:

- All seven skills pass `quick_validate.py`.
- `scripts/check_skills.py` passes: protocol 1, 15 roles.
- `scripts/check_spec.py` passes on `tests/fixtures/minimal-spec`.
- `pytest tests` passes 16 tests.
- mermaid-cli renders the C4Context, C4Container, C4Component, and classDiagram templates, so no fallback template was needed. A flowchart fallback is still described for viewers that can't render C4.

Versions: `prdfy` 2.0.0, `prdfy-writer` 1.4.0, every other sub-skill 1.3.0. Every skill declares protocol 1.

The scenario and trigger evals are written but have not been run. Running them needs the `skill-creator` harness and a model session.

## Design decisions

These resolve the open options in the review. Every step follows them.

- **Changing a decision (2.3).** Decisions gain a `superseded` status and a `Superseded by` column. If the user changes a confirmed decision, the orchestrator relaunches the owning module with `revise D-<n>`. That module returns new rows with `supersedes D-<n>`. The orchestrator marks the old row `superseded`, and any finished file that cites it becomes `stale`.
- **Progress in memory (2.4).** Memory gains a `## Progress` section with the phase, the active module, and one status row per file. The status is one of `pending`, `written`, `verified`, `failed`, or `stale`. A new session resumes from it.
- **History (2.4).** Before rewriting deliverables for an existing product, the orchestrator moves the current deliverables to `prdfy-spec/history/<YYYY-MM-DD>/`. Moving files is housekeeping, not product work.
- **Research files are versioned (3.5).** A rerun of a mode writes `research-<mode>-2.md`, then `-3`, and so on. Earlier files are never overwritten.
- **Relaunch is the default (2.5).** The orchestrator relaunches a sub-agent with the updated memory and the user's verbatim answer. It resumes the sub-agent only if the host supports that.
- **Parallel writers (2.6).** Files 01 to 06 run in parallel. A relay from one Writer does not pause the others. After the answer, every finished file that depends on it becomes `stale` and is rewritten and re-verified.
- **Fewer launches (4.5).** One final Writer launch writes the decision log and `README.md` together, after every other file. A single Verifier launch may check several files, still writing one verify file each.
- **Inline mode (2.7).** When the host cannot launch sub-agents, the orchestrator tells the user once. It then runs each sub-skill as a separate, clearly marked step, producing only that skill's return block.
- **Send-back limit (2.8).** The orchestrator sends a bad relay back once. After that, it relays the first four valid questions and drops the rest.
- **Review loop (2.9).** Review lists verification failures, and "None" is always an option.
  - Promoting an assumption marks the `A-` row `confirmed` and adds a `user` decision row.
  - Rejecting one marks it `rejected`.
  - Every file citing that row becomes `stale`.
  - Review runs at most once more.
- **Early draft (2.11).** Each unfinished module is relaunched with `skip`, in order. The run then proceeds as normal, so every gap is an `A-` row.
- **Exact headings (3.1).** Each Writer file has a fixed H1 and fixed H2 headings, in order. `Not applicable: <reason>` is allowed under a heading that doesn't apply. C4 headings live in `prdfy-c4`.
- **Cross-document check (3.2).** The verifier gains a `cross` mode, run once after every per-file pass, which writes `findings/verify-cross.md`.
- **Traceability (3.3).** FR, NFR, and RSK rows carry a `Decisions` column, and INV rows carry an `Aggregate` column. Compliance rows link to `RSK-` IDs.
- **Source fields (3.4).** Each finding records `Type: primary|secondary` and `Accessed: <date>`.
- **Risk owner (3.6).** The Owner column holds an actor or role from memory, or `unassigned`, and never a person.
- **Mermaid (3.7).** Render-test the templates with mermaid-cli and add `stateDiagram-v2` for lifecycles. If a C4 template fails to render, add a `flowchart` fallback.
- **Role list (4.3).** Every sub-skill carries the same full list of 15 roles on a `Role names:` line. A repo script checks that the lists match the orchestrator's terminology table.
- **Protocol version (4.8).** Every skill declares `metadata.protocol: "1"`. The orchestrator stops if a sub-skill differs, and the repo script checks it too.
- **Evals (4.4):**
  - `prdfy/evals/evals.json` holds the scenario evals.
  - `prdfy/evals/trigger-evals.json` holds the trigger evals.
  - `scripts/check_spec.py` runs static checks on a generated `prdfy-spec/`.
  - `scripts/check_skills.py` checks that the role lists and protocol versions match across skills.
  - Run both scripts with `uv`.

## Steps

### Step 1: Memory, progress, and supersede (2.3, 2.4)
Files: `prdfy/SKILL.md`, `prdfy-module/SKILL.md`
- [x] Add a `Superseded by` column and the `superseded` status to the Decisions table.
- [x] Add a `## Progress` section to the memory template, with resume rules.
- [x] Add the history archive rule for continuing an existing product.
- [x] Module: handle `revise D-<n>` and add a `supersedes` field to its rows.

### Step 2: Orchestration rules (2.5, 2.6, 2.7, 2.8, 2.11, 4.5, 4.6)
Files: `prdfy/SKILL.md`, `prdfy-writer/SKILL.md`, `prdfy-verifier/SKILL.md`
- [x] Relaunch is the default; resume only where the host supports it.
- [x] Parallel writers, stale files, and a final launch for the decision log and README.
- [x] Inline mode for hosts without sub-agents.
- [x] Send-back limit.
- [x] Early-draft path.
- [x] Use the host's structured question tool when it has one.
- [x] Writer: the decision-log and README pair. Verifier: batched files.

### Step 3: Review loop (2.9)
Files: `prdfy-review/SKILL.md`, `prdfy/SKILL.md`
- [x] Add a `## Verification` section to `review.md`.
- [x] Define promote, reject, and None; mark citing files stale; allow one more Review at most.

### Step 4: Writer heading contracts and traceability (3.1, 3.3, 3.6, 3.7)
Files: `prdfy-writer/SKILL.md`, `prdfy-c4/SKILL.md`
- [x] Exact H1 and H2 headings per file, plus the `Not applicable` rule.
- [x] Traceability columns in the FR, NFR, INV, RSK, and compliance tables.
- [x] Risk owner rule.
- [x] `stateDiagram-v2` for lifecycles.
- [x] Exact C4 headings.

### Step 5: Research sources and versioning (3.4, 3.5)
Files: `prdfy-research/SKILL.md`, `prdfy/SKILL.md`, `prdfy-module/SKILL.md`
- [x] Add `Type` and `Accessed` fields, with a definition of a primary source.
- [x] Versioned file names; never overwrite.

### Step 6: Verifier cross mode and source checks (3.2, 3.4)
Files: `prdfy-verifier/SKILL.md`, `prdfy/SKILL.md`
- [x] Add the `cross` mode and its checks.
- [x] Check that cited sources exist in findings, with a location.
- [x] Add the orchestrator step for the cross check.

### Step 7: Mermaid render test (3.7)
Files: `prdfy-c4/SKILL.md`, if a template fails
- [x] Render the C4Context, C4Container, C4Component, and classDiagram templates with mermaid-cli.
- [x] Fix any template that fails, or add a fallback.

### Step 8: Triggering and activation (4.1, 4.2)
Files: `prdfy/SKILL.md`
- [x] Add negative triggers to the description, keeping it under 1024 characters.
- [x] If the user only wants code, the skill does not apply. Don't decline the request.

### Step 9: Role list and protocol (4.3, 4.8)
Files: all seven skills
- [x] Put the full role list on a `Role names:` line in every sub-skill.
- [x] Add `metadata.protocol: "1"` to every skill, and the orchestrator's protocol check.

### Step 10: Deliverable count and README (4.7)
Files: `prdfy/SKILL.md`, `prdfy-research/SKILL.md`, `README.md`
- [x] Say "eight documents and an index" everywhere.
- [x] README: full deliverables table, a note that the skill is seven folders, and a Development section.

### Step 11: Evals and checks (4.4)
Files: `.agents/skills/prdfy/evals/evals.json`, `.agents/skills/prdfy/evals/trigger-evals.json`, `scripts/check_skills.py`, `scripts/check_spec.py`
- [x] Write the scenario evals.
- [x] Write the trigger evals.
- [x] Write `check_skills.py` (role lists and protocol versions) and run it.
- [x] Write `check_spec.py` (code fences, headings, source columns, `A-` IDs, aggregates in 06 against 07) and run it against a temporary fixture.

### Step 12: Verify
- [x] Bump `metadata.version` on every changed skill.
- [x] Run `quick_validate.py` on all seven skills.
- [x] Run `scripts/check_skills.py`.
- [x] Grep for stale terms.
- [x] Mark the review report as fully done.
