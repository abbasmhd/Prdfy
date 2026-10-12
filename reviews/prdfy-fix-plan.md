# Prdfy fix plan: section 1 of the review

Source: `reviews/prdfy-skills-review.md`. This plan covers the blocking contradictions (1.1 to 1.8). It also covers the memory changes they depend on: assumption IDs (2.1), ID ownership (2.2), and Writers not proposing decisions (2.10).

Tick each box when the edit is in. Each step lists the files it touches.

**Status: done (2026-10-12).** All seven skills pass `quick_validate.py`, and none of the stale terms remain. Versions: `prdfy` 1.8.0, `prdfy-writer` 1.3.0, all other sub-skills 1.2.0.

## Design decisions

These choices resolve the open options in the review. Every step below follows them.

- **Relays keep two to four questions.** Research's jurisdiction relay becomes two questions (jurisdiction, then regulated activities) instead of relaxing the count.
- **Suggestions come from sub-agents.** Each `NEED_USER` question carries up to four suggestions, each with a source label. The orchestrator shows them unchanged and adds none. The same applies to the `MODULE_READY` closing questions and the `REVIEW` questions.
- **Only the orchestrator allocates IDs.** It passes the next free `D-` and `A-` IDs in each Module brief. Modules run one at a time, so IDs can't collide. IDs are never reused, and gaps are allowed.
- **Writers and C4 never create decisions or assumptions.** They cite memory IDs only. A gap is `NEED_USER`. If the user skips that relay, the orchestrator records an `A-` row stating that the fact is unknown, without inventing a value, and relaunches the Writer.
- **Names policy:**
  - Technology names (language, framework, database engine, infrastructure vendor) are banned everywhere.
  - A technology the user chose is a Rule. It may be quoted in `00-decision-log.md` and in a `Constraints` section of `02-prd.md`, and never as a role.
  - Market and integration names (competitors, substitutes, regulators, regulations, integrations the user requires) are allowed when they come from a `user` decision or a cited finding.
- **Research always writes its findings file**, even when it has no findings or is blocked. Mode names are kebab-case: `category`, `compliance`, `boundaries`, `pressure-test`.

## Steps

### Step 1: Memory schema and ID ownership (2.1, 2.2)
Files: `prdfy/SKILL.md`
- [x] Replace `## Open gaps` with an `## Assumptions` table (`A-` ID, module, exit item, assumption, status `open|confirmed|rejected`).
- [x] Add an ID ownership rule: orchestrator allocates; next free IDs go in the Module brief; never reuse.
- [x] Update every reference to "Open gaps".

### Step 2: Names policy (1.1)
Files: `prdfy/SKILL.md`, `prdfy-writer/SKILL.md`, `prdfy-c4/SKILL.md`, `prdfy-verifier/SKILL.md`, `prdfy-research/SKILL.md`
- [x] Rewrite the stack-agnostic core rule as two lists.
- [x] Add `Constraints` to the `02-prd.md` contract.
- [x] Writer and C4: allow sourced market and integration names, including `System_Ext` for required integrations.
- [x] Verifier: check the technology ban with the two exceptions.

### Step 3: Unified relay with suggestions (1.2, 1.7)
Files: all seven skills
- [x] New `NEED_USER` format with per-question suggestions, used by Module, Research, Writer, and C4.
- [x] Research: replace its custom return. Make the compliance relay ask two questions.
- [x] Orchestrator relay steps: show the sub-agent's suggestions; add none.
- [x] `MODULE_READY` and `REVIEW` closing questions carry suggestions.
- [x] Update the core rule and "What the orchestrator may say".

### Step 4: Skip handling (1.7, 1.6)
Files: `prdfy/SKILL.md`, `prdfy-module/SKILL.md`
- [x] On a skip, the orchestrator relaunches the Module with `skip`. The Module returns `MODULE_READY` with `A-` rows and writes its file.
- [x] Writer skip path: the orchestrator records an "unknown" `A-` row and relaunches the Writer.

### Step 5: Assumptions in deliverables (1.3, 2.10)
Files: `prdfy-writer/SKILL.md`, `prdfy-c4/SKILL.md`, `prdfy-verifier/SKILL.md`, `prdfy/SKILL.md`
- [x] Writer and C4 cite `A-` IDs from memory only; new gap is `NEED_USER`.
- [x] Writers never propose decisions (fix line 135 of `prdfy/SKILL.md`).
- [x] Verifier: an `assumption` label must cite an `A-` ID present in memory.

### Step 6: Verifier contract for C4 (1.4)
Files: `prdfy-verifier/SKILL.md`
- [x] Point the verifier at `prdfy-c4` for `07-c4-architecture.md`.

### Step 7: C4 template label (1.5)
Files: `prdfy-c4/SKILL.md`
- [x] Replace `"Uses"` in the template.

### Step 8: Findings files always exist (1.6)
Files: `prdfy-research/SKILL.md`, `prdfy/SKILL.md`
- [x] Research always writes `research-<mode>.md`. Use the `pressure-test` mode name.
- [x] Orchestrator step 3 names the `pressure-test` mode.

### Step 9: Vision research timing (1.8)
Files: `prdfy-module/SKILL.md`, `prdfy/SKILL.md`
- [x] Replace "before the second turn" with a memory-based condition.
- [x] Align the orchestrator's "research finishes first" rule.

### Step 10: Verify
- [x] Bump `metadata.version` on every changed skill.
- [x] Run `quick_validate.py` on all seven skills.
- [x] Grep for stale terms: `Open gaps`, `D-id`, `"Uses"`, `asking only for the jurisdiction`, `suggest up to four`, `Pressure test`.
- [x] Mark section 1, 2.1, 2.2, and 2.10 as done in the review report.

## Out of scope for this pass

All of section 3 and section 4, and the remaining section 2 items: 2.3 to 2.9 and 2.11. These include superseded decisions, resume, the fallback for hosts without sub-agents, and the cross-document check.
