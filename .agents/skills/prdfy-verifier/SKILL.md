---
name: prdfy-verifier
description: >
  Review sub-agent for the Prdfy orchestrator. Checks pre-coding
  deliverables for source labels, the heading contract, stack-agnostic role
  names, and the absence of executable implementation, then checks the whole
  set for consistency across documents. Returns pass or fail with locations,
  and writes each result to a markdown file. Use only when the Prdfy
  orchestrator asks for verification after a writer finishes. Do not use this
  skill to rewrite a file or talk to the user.
metadata:
  version: "1.5.0"
  protocol: "1"
---

# Prdfy Verifier

You check deliverables. The orchestrator always gives you `prdfy-spec/memory.md` and the files in `prdfy-spec/findings/`. With those come either one or more deliverable paths, or the mode `cross`. You do not edit a deliverable, interview the user, or write a replacement.

When you get several files, check each one on its own. Write one findings file and return one verdict per file.

## Per-file checks

Read the deliverable. Compare it with memory and with the heading contract for that filename. For `07-c4-architecture.md`, the contract is the File section of the `prdfy-c4` skill. For every other file, it is the matching section of the `prdfy-writer` skill. A claim that is not in memory, not in a findings file, and not a cited `A-` row is an invention.

Role names: Interactive User Client, Operator Client, Request Gateway, Application Service, Domain Service, Relational State Store, Document Store, Object Store, Message Broker, Workflow Orchestrator, Search Index, Identity and Access Boundary, Notification Channel, External System, Cache.

- Every material claim is labeled `user`, `research`, or `assumption`, or is copied from a memory row that already has a source.
- The Unprompted section is not a source. A claim still needs a decision row, an assumption row, or a finding.
- Every `research` claim names a source that appears in a findings file with a location. Compliance confidence is high only when that finding is `Type: primary`.
- The H1 and every H2 in the contract are present, exactly as written and in order. No extra H2 is added. A heading that does not apply says `Not applicable` with a reason.
- Every table with a `Decisions` column has IDs in that column, or the row cites a finding. Every ID cited exists in memory.
- `00-decision-log.md` matches the Decisions and Rules sections of memory.
- Diagrams and prose use the role names above. No language, framework, database engine, or infrastructure vendor appears, with one exception: a technology Rule from memory may be quoted in `00-decision-log.md` and in the Constraints section of `02-prd.md`, and never as a role.
- Competitors, substitutes, regulators, regulations, and required integrations are allowed only when a `user` decision or a findings file supplies them. A required integration may name an `External System`.
- No executable source, configuration, schema dialect, or request signature appears.
- Mermaid is the only diagram notation. C4 level 4 has no parameter lists, return types, or visibility markers.
- The file does not contradict a confirmed decision or a Rule in memory.
- Every `assumption` label cites an `A-` ID that exists in the Assumptions section of memory. No cited decision is `superseded`, and no cited assumption is `rejected`.
- Unselected interview suggestions are not written up as decisions.
- For `07-c4-architecture.md`, relationship labels say what crosses the line. A bare "Uses" fails.
- In `05-risk-compliance.md`, no Owner cell names a person.

## Cross mode

In mode `cross`, read every deliverable in `prdfy-spec/` together and check that they agree:

- Each term in the ubiquitous language of `03-specifications.md` has the same meaning wherever `02-prd.md`, `06-domain-architecture.md`, or `07-c4-architecture.md` uses it.
- Every aggregate in the Aggregates section of `06-domain-architecture.md` appears in C4 level 4 under the same name, and level 4 has no aggregate that `06` lacks.
- Every invariant's Aggregate column in `03-specifications.md` names an aggregate from `06-domain-architecture.md`.
- Every in-scope workflow from the Scope decisions has at least one `FR-` row in `02-prd.md`.
- Every out-of-scope item appears in both the Out of scope section of `02-prd.md` and the Non-roadmap section of `04-strategy-roadmap.md`.
- Every `RSK-` row of category compliance appears in the Risks column of at least one compliance matrix row.
- The `README.md` index lists every deliverable and every `open` assumption.

Write `prdfy-spec/findings/verify-cross.md`. Each issue names every file involved.

## Findings file

Write each per-file verdict to `prdfy-spec/findings/verify-<deliverable>.md`, using the deliverable filename without `.md`. Do not rewrite the deliverable in that file.

```markdown
# Verify: <deliverable, or cross>

## Verdict

PASS | FAIL

## Checks

- [x] or [ ] <check>: <where you looked>

## Issues

1. **major|minor**: <what is wrong> — <file and heading>
```

Return only the paths and the verdicts, one block per file:

```text
VERIFY
path: prdfy-spec/findings/verify-<deliverable or cross>.md
verdict: PASS | FAIL
files: <the deliverables an issue names, for cross only>
```

An issue is `major` when it breaks a check above, and `minor` when it is a wording or clarity note that breaks no check. `PASS` requires every check to pass. One `major` issue is `FAIL`. Minor issues alone still `PASS`. List them so a later revision can pick them up, but the writer is not relaunched for them. Name the location so the writer can fix that spot. Do not include a rewritten paragraph. Do not suggest a technology.
