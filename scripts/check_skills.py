# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Check that the Prdfy skills agree on their protocol version and role list."""

import re
import sys
from pathlib import Path

import yaml

SKILLS_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills"
ORCHESTRATOR = "prdfy"
SUB_SKILLS = [
    "prdfy-research",
    "prdfy-module",
    "prdfy-writer",
    "prdfy-c4",
    "prdfy-verifier",
    "prdfy-review",
]
# prdfy-review never names architecture, so it carries no role list.
ROLE_LIST_SKILLS = [s for s in SUB_SKILLS if s != "prdfy-review"]


def read_skill(name: str) -> tuple[dict, str]:
    text = (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.DOTALL)
    if not match:
        raise ValueError(f"{name}: no frontmatter")
    return yaml.safe_load(match.group(1)), text


def orchestrator_roles(text: str) -> list[str]:
    roles = []
    in_table = False
    for line in text.splitlines():
        if line.startswith("| Say this |"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                break
            cell = line.split("|")[1].strip()
            if cell and not set(cell) <= {"-"}:
                roles.append(cell)
    return roles


def sub_skill_roles(text: str) -> list[str] | None:
    match = re.search(r"^Role names: (.+)$", text, re.MULTILINE)
    if not match:
        return None
    return [r.strip() for r in match.group(1).rstrip(".").split(",")]


def main() -> int:
    errors = []

    front, text = read_skill(ORCHESTRATOR)
    protocol = (front.get("metadata") or {}).get("protocol")
    if not protocol:
        errors.append(f"{ORCHESTRATOR}: metadata.protocol is missing")
    roles = orchestrator_roles(text)
    if not roles:
        errors.append(f"{ORCHESTRATOR}: terminology table not found")

    for name in SUB_SKILLS:
        sub_front, sub_text = read_skill(name)
        sub_protocol = (sub_front.get("metadata") or {}).get("protocol")
        if sub_protocol != protocol:
            errors.append(
                f"{name}: metadata.protocol is {sub_protocol!r}, orchestrator has {protocol!r}"
            )
        if name in ROLE_LIST_SKILLS:
            sub_roles = sub_skill_roles(sub_text)
            if sub_roles is None:
                errors.append(f"{name}: no 'Role names:' line")
            elif sub_roles != roles:
                missing = [r for r in roles if r not in sub_roles]
                extra = [r for r in sub_roles if r not in roles]
                detail = []
                if missing:
                    detail.append(f"missing {missing}")
                if extra:
                    detail.append(f"extra {extra}")
                if not detail:
                    detail.append("same roles, different order")
                errors.append(f"{name}: role list differs from orchestrator ({'; '.join(detail)})")

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print(f"OK protocol {protocol}, {len(roles)} roles, {len(SUB_SKILLS) + 1} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
