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

After the architectural boundaries are confirmed, writers produce `prdfy-spec/`:

| File | Deliverable |
| --- | --- |
| `01-business-plan.md` | Business plan and value proposition |
| `02-prd.md` | Product requirements document |
| `03-specifications.md` | Specifications and domain contracts |
| `04-strategy-roadmap.md` | Strategy and product roadmap |
| `05-risk-compliance.md` | Risk management and compliance matrix |
| `06-domain-architecture.md` | Domain architecture |
| `07-c4-architecture.md` | C4 model, levels 1–4, in Mermaid |

A verifier checks each file. The skill stops at the specification.

## Install

The skill is the [`.agents/skills/prdfy/`](.agents/skills/prdfy/) folder. The host needs sub-agents, web search, and Mermaid. After installing, start a new Agent chat and invoke `/prdfy`, or ask the agent to scope a product idea.

### npx skills

The [skills CLI](https://github.com/vercel-labs/skills) installs a skill from a git repo or a local folder. This repository also contains `skill-creator`. Install Prdfy together with its sub-agent skills: `prdfy-research`, `prdfy-module`, `prdfy-writer`, `prdfy-c4`, `prdfy-verifier`, and `prdfy-review`.

List what the repo offers:

```bash
npx skills add abbasmhd/Prdfy --list
```

Install Prdfy for Cursor in the current project:

```bash
npx skills add abbasmhd/Prdfy --skill prdfy --skill prdfy-research --skill prdfy-module --skill prdfy-writer --skill prdfy-c4 --skill prdfy-verifier --skill prdfy-review -a cursor -y
```

Install it for every project on this machine:

```bash
npx skills add abbasmhd/Prdfy --skill prdfy --skill prdfy-research --skill prdfy-module --skill prdfy-writer --skill prdfy-c4 --skill prdfy-verifier --skill prdfy-review -a cursor -g -y
```

For Cursor, a project install lands in `.agents/skills/prdfy/`. A global install (`-g`) lands in `~/.cursor/skills/prdfy/`. Leave off `-y` if you want the CLI to ask which skill, which agent, and whether to symlink or copy.

Until this repo has a GitHub remote, point the CLI at the local folder:

```bash
npx skills add /path/to/Prdfy --skill prdfy --skill prdfy-research --skill prdfy-module --skill prdfy-writer --skill prdfy-c4 --skill prdfy-verifier --skill prdfy-review -a cursor -y
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

Cursor also loads `.cursor/skills/prdfy/`. Claude Code loads `.claude/skills/prdfy/`. Use whichever directory that project already uses.

### Every project on your machine

Copy it into your user skills directory:

```bash
mkdir -p ~/.agents/skills
cp -R .agents/skills/prdfy .agents/skills/prdfy-research .agents/skills/prdfy-module .agents/skills/prdfy-writer .agents/skills/prdfy-c4 .agents/skills/prdfy-verifier .agents/skills/prdfy-review ~/.agents/skills/
```

The same folder works at `~/.cursor/skills/prdfy/` for Cursor and `~/.claude/skills/prdfy/` for Claude Code. On Windows, `~` is your user profile (`C:\Users\<you>`).

User-level skills stay on that machine. Commit the project copy if teammates should get the skill with the repo.

### Other agents

Point the agent at `SKILL.md`, or paste its body into the agent instructions. Keep one orchestrator in front of the user and delegate every step to a sub-agent.

Start from a product idea, not from a request to write code. If a technology is already chosen, the skill records it as your constraint and still describes the architecture in role names.

## License

Prdfy is licensed under the [MIT License](LICENSE).

The bundled [skill-creator](.agents/skills/skill-creator/) skill comes from [anthropics/skills](https://github.com/anthropics/skills) and remains under the Apache License 2.0. See [its license](.agents/skills/skill-creator/LICENSE.txt).
