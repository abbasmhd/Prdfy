# Prdfy

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Prdfy (Predify) is a pre-coding skill. It interviews you about a software product idea and writes the specification before any implementation starts.

You talk to one orchestrator. Sub-agents do the research, the interview, the writing, and the review. When a sub-agent needs a fact only you know, it stops. The orchestrator asks you, then sends your answer back to that sub-agent.

The specification stays stack-agnostic. It names roles such as Interactive User Client, Relational State Store, and Message Broker. It does not choose a language, framework, or database.

## Interview

The orchestrator runs six modules, in order, two to four questions at a time:

1. Vision
2. Scope
3. Domain Rules
4. Strategy and MVP
5. Risk and Compliance
6. Architectural Boundaries

During the interview, a research sub-agent looks up competitors, market dynamics, and regulations. Claims are labeled as coming from you, from research, or from an explicit assumption.

## Deliverables

After the architectural boundaries are confirmed, writers produce eight documents and an index in `prdfy-spec/`:

| File | Deliverable |
| --- | --- |
| `00-decision-log.md` | Decisions and rules captured during the interview |
| `01-business-plan.md` | Business plan and value proposition |
| `02-prd.md` | Product requirements document |
| `03-specifications.md` | Specifications and domain contracts |
| `04-strategy-roadmap.md` | Strategy and product roadmap |
| `05-risk-compliance.md` | Risk management and compliance matrix |
| `06-domain-architecture.md` | Domain architecture |
| `07-c4-architecture.md` | C4 model, levels 1–4, in Mermaid |
| `README.md` | Index of the documents, open assumptions, and sources |

A verifier checks each file, then checks that the documents agree with each other. The skill stops at the specification.

The run state lives in `prdfy-spec/memory.md`. That file records your rules, decisions, answers, assumptions, and progress, so you can stop and pick up the run in a later session. Research, module, and verification notes go to `prdfy-spec/findings/`.

## Install

The skill is seven folders under [`.agents/skills/`](.agents/skills/): the `prdfy` orchestrator and its six sub-agent skills (`prdfy-research`, `prdfy-module`, `prdfy-writer`, `prdfy-c4`, `prdfy-verifier`, `prdfy-review`). Install all seven, from the same version. The orchestrator checks that every skill declares the same `metadata.protocol`, and it stops if one differs. The host needs sub-agents, web search, and Mermaid. After installing, start a new Agent chat and invoke `/prdfy`, or ask the agent to scope a product idea.

### npx skills

List what the repo offers:

```bash
npx skills add abbasmhd/Prdfy --list
```

Install all skills for Cursor in the current project:

```bash
npx skills add abbasmhd/Prdfy --skill '*' -a cursor -y
```

Install all skills for Cursor on every project on this machine:

```bash
npx skills add abbasmhd/Prdfy --skill '*' -a cursor -g -y
```

Install all skills for every agent on this machine:

```bash
npx skills add abbasmhd/Prdfy --all
```

For Cursor, a project install lands in `.agents/skills/`. A global install (`-g`) lands in `~/.cursor/skills/`. `--all` is global across agents and does not take `-a`. Leave off `-y` if you want the CLI to ask which skill, which agent, and whether to symlink or copy.

To install from a local checkout instead:

```bash
npx skills add /path/to/Prdfy --skill '*' -a cursor -y
```

If a symlink fails on Windows, add `--copy`. Other agents use the same command with their own `--agent` name, such as `claude-code`.

### This repository

The skill is already installed for anyone who opens this repo in Cursor. Ask the agent to brainstorm, scope, or architect a product idea, or invoke `/prdfy`.

### Another project

From this repo, copy the folder into the other project:

```bash
mkdir -p /path/to/other-project/.agents/skills
cp -R .agents/skills/prdfy .agents/skills/prdfy-research .agents/skills/prdfy-module .agents/skills/prdfy-writer .agents/skills/prdfy-c4 .agents/skills/prdfy-verifier .agents/skills/prdfy-review /path/to/other-project/.agents/skills/
```

Cursor also loads skills from `.cursor/skills/`. Claude Code loads them from `.claude/skills/`. Use whichever directory that project already uses, and copy all seven folders into it.

### Every project on your machine

Copy it into your user skills directory:

```bash
mkdir -p ~/.agents/skills
cp -R .agents/skills/prdfy .agents/skills/prdfy-research .agents/skills/prdfy-module .agents/skills/prdfy-writer .agents/skills/prdfy-c4 .agents/skills/prdfy-verifier .agents/skills/prdfy-review ~/.agents/skills/
```

The same seven folders work under `~/.cursor/skills/` for Cursor and `~/.claude/skills/` for Claude Code. On Windows, `~` is your user profile (`C:\Users\<you>`).

User-level skills stay on that machine. Commit the project copy if teammates should get the skill with the repo.

### Other agents

Point the agent at `SKILL.md`, or paste its body into the agent instructions. Keep one orchestrator in front of the user and delegate every step to a sub-agent.

Start from a product idea, not from a request to write code. If a technology is already chosen, the skill records it as your constraint and still describes the architecture in role names. If the host cannot launch sub-agents, the orchestrator says so and runs each step inline as a separate role.

## Development

The skills need no runtime. The repository has two check scripts. Run them with [uv](https://docs.astral.sh/uv/):

```bash
# Role lists and protocol versions agree across the seven skills
uv run scripts/check_skills.py

# Static checks on a generated specification folder
uv run scripts/check_spec.py path/to/prdfy-spec

# Tests for both scripts, against tests/fixtures/minimal-spec
uv run --with pytest --with pyyaml pytest tests
```

CI runs these checks on every push and pull request to `main`.

Evals for the orchestrator live in [`.agents/skills/prdfy/evals/`](.agents/skills/prdfy/evals/):

- `evals.json` holds the end-to-end scenarios, in the `skill-creator` format.
- `trigger-evals.json` holds the description trigger set, for `skill-creator`'s `run_eval.py` and `run_loop.py`.

## License

Prdfy is licensed under the [MIT License](LICENSE).
