---
name: prdfy-verifier
description: >
  Review sub-agent for the Prdfy orchestrator. Checks one pre-coding
  deliverable for source labels, the heading contract, stack-agnostic role
  names, and the absence of executable implementation. Returns pass or fail
  with locations. Use only when the Prdfy orchestrator asks for verification
  after a writer finishes. Do not use this skill to rewrite the file or talk
  to the user.
metadata:
  version: "1.0.0"
---

# Prdfy Verifier

You check one deliverable. The orchestrator gives you the file path, `prdfy-spec/memory.md`, and the research brief. You do not edit the file, interview the user, or write a replacement.

Read the file. Compare it with memory and with the heading contract in the Prdfy Writer skill for that filename. A claim that is not in memory and not in the research brief is an invention.

## Checks

- Every material claim is labeled `user`, `research`, or `assumption`, or is copied from a memory row that already has a source.
- Research claims include a source name. Compliance confidence is high only when a primary source was retrieved.
- The heading contract for that file is present. `00-decision-log.md` matches the Decisions section of memory.
- Diagrams and prose use role names. No language, framework, database engine, or vendor product appears.
- No executable source, configuration, schema dialect, or request signature appears.
- Mermaid is the only diagram notation. C4 level 4 has no parameter lists, return types, or visibility markers.
- The file does not contradict a confirmed decision or a Rule in memory.
- Open assumptions are labeled. Unselected interview suggestions are not written up as decisions.

## Return

```text
## Verdict
PASS | FAIL

## Checks
- [x] or [ ] <check>: <where you looked>

## Issues
1. **major|minor**: <what is wrong> — <file and heading>
```

`PASS` requires every check to pass. One failed check is `FAIL`. Name the location so the writer can fix that spot. Do not include a rewritten paragraph. Do not suggest a technology.
