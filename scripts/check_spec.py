# /// script
# requires-python = ">=3.11"
# ///
"""Static checks on a generated prdfy-spec/ folder.

These mirror the deterministic part of prdfy-verifier: required files, the
heading contract, code fences, source and decision columns, memory IDs,
aggregate names shared by 06 and 07, and a short technology denylist.
Judgement checks (invented claims, consistent meanings) stay with the
verifier sub-agent.
"""

import re
import sys
from pathlib import Path

C4_LEVEL_SUBSECTIONS = [
    "Purpose",
    "Diagram",
    "Narrative",
    "Boundaries considered and rejected",
]

CONTRACT = {
    "00-decision-log.md": ("Decision log", ["Decisions", "Rules"]),
    "01-business-plan.md": (
        "Business plan",
        [
            "Problem",
            "Value proposition",
            "Payer and user",
            "Alternatives",
            "Market notes",
            "Revenue model",
            "Success metrics",
            "Assumptions",
        ],
    ),
    "02-prd.md": (
        "Product requirements",
        [
            "Problem statement",
            "Goals and non-goals",
            "Actors",
            "Jobs to be done",
            "Journeys",
            "Functional requirements",
            "Non-functional requirements",
            "Constraints",
            "Out of scope",
            "Open questions",
        ],
    ),
    "03-specifications.md": (
        "Specifications",
        [
            "Ubiquitous language",
            "Invariants",
            "Commands",
            "Queries",
            "Domain events",
            "Policies",
            "Lifecycles",
            "Contracts between actors",
        ],
    ),
    "04-strategy-roadmap.md": (
        "Strategy and roadmap",
        ["MVP", "Now, Next, Later", "Dependencies", "Signals", "Non-roadmap"],
    ),
    "05-risk-compliance.md": (
        "Risk and compliance",
        ["Risk register", "Compliance matrix", "Not legal advice"],
    ),
    "06-domain-architecture.md": (
        "Domain architecture",
        [
            "Bounded contexts",
            "Context relationships",
            "Context map",
            "Aggregates",
            "Fact ownership",
            "Published language",
        ],
    ),
    "07-c4-architecture.md": (
        "C4 architecture",
        [
            "Level 1: System context",
            "Level 2: Containers",
            "Level 3: Components",
            "Level 4: Domain structure",
        ],
    ),
    "README.md": ("Prdfy specification", ["Documents", "Open assumptions", "Sources"]),
}

# Files that may quote a technology Rule. For 02, only the Constraints section.
TECH_ALLOWED = {"00-decision-log.md": None, "02-prd.md": "Constraints"}

TECH_DENYLIST = [
    "PostgreSQL", "Postgres", "MySQL", "SQL Server", "SQLite", "MongoDB",
    "DynamoDB", "Cosmos DB", "Firestore", "Firebase", "Supabase", "Redis",
    "Memcached", "Kafka", "RabbitMQ", "Elasticsearch", "OpenSearch",
    "Airflow", "Django", "Flask", "FastAPI", "Rails", "Laravel",
    "Spring Boot", "Express.js", "Next.js", "Nuxt", "Angular", "Vue.js",
    "Svelte", "Node.js", "Python", "Java", "Kotlin", "TypeScript",
    "JavaScript", "Golang", "Rust", "C#", ".NET", "Kubernetes", "Docker",
    "AWS", "Azure", "GCP", "Google Cloud", "Auth0", "Okta", "Cognito",
]

LABELS = ("user", "research", "assumption")


def strip_fences(text: str) -> tuple[str, list[str]]:
    """Return text with fenced blocks blanked, plus each fence's info string."""
    out, infos, in_fence = [], [], False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_fence:
                infos.append(stripped[3:].strip())
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out), infos


def mermaid_blocks(text: str) -> list[str]:
    return re.findall(r"```mermaid\s*\n(.*?)```", text, re.DOTALL)


def headings(text: str, level: int) -> list[str]:
    prefix = "#" * level + " "
    return [l[len(prefix):].strip() for l in text.splitlines() if l.startswith(prefix)]


def section(text: str, h2: str) -> str:
    match = re.search(rf"^## {re.escape(h2)}\s*$(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    found, lines, i = [], text.splitlines(), 0
    while i < len(lines) - 1:
        line, nxt = lines[i].strip(), lines[i + 1].strip()
        if line.startswith("|") and re.match(r"^\|[\s\-:|]+\|$", nxt):
            header = [c.strip() for c in line.strip("|").split("|")]
            rows, i = [], i + 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            found.append((header, rows))
        else:
            i += 1
    return found


def memory_ids(memory: str) -> dict[str, str]:
    """Map each D- and A- ID in memory to its status."""
    ids = {}
    for header, rows in tables(memory):
        if not header or header[0] != "ID" or "Status" not in header:
            continue
        status_at = header.index("Status")
        for row in rows:
            if row and re.fullmatch(r"[DA]-\d+", row[0]) and len(row) > status_at:
                ids[row[0]] = row[status_at]
    return ids


def check_file(name: str, text: str, ids: dict[str, str] | None) -> list[str]:
    issues = []
    prose, infos = strip_fences(text)

    for info in infos:
        if info != "mermaid":
            issues.append(f"code fence '{info or '(none)'}' is not mermaid")

    h1, h2s = CONTRACT[name]
    found_h1 = headings(prose, 1)
    if found_h1 != [h1]:
        issues.append(f"H1 should be '# {h1}', found {found_h1}")
    found_h2 = headings(prose, 2)
    if found_h2 != h2s:
        issues.append(f"H2 headings should be {h2s}, found {found_h2}")

    if name == "07-c4-architecture.md":
        for level in h2s:
            subs = headings(section(text, level), 3)
            if subs != C4_LEVEL_SUBSECTIONS:
                issues.append(f"'{level}' subsections should be {C4_LEVEL_SUBSECTIONS}, found {subs}")
        for block in mermaid_blocks(text):
            for rel in re.findall(r'Rel\([^)]*"Uses"\s*\)', block):
                issues.append(f"bare 'Uses' relationship label: {rel}")

    if name not in ("00-decision-log.md", "README.md"):
        for header, rows in tables(prose):
            src = header.index("Source") if "Source" in header else None
            dec = header.index("Decisions") if "Decisions" in header else None
            for row in rows:
                label = row[0] if row else "?"
                if src is not None and (len(row) <= src or not row[src]):
                    issues.append(f"row {label}: empty Source")
                if dec is not None and len(row) > dec and not row[dec]:
                    source = row[src].lower() if src is not None and len(row) > src else ""
                    if "research" not in source:
                        issues.append(f"row {label}: empty Decisions and no research source")

    if ids is not None and name != "00-decision-log.md":
        for cited in sorted(set(re.findall(r"\b[DA]-\d+\b", prose))):
            status = ids.get(cited)
            if status is None:
                issues.append(f"cites {cited}, which is not in memory")
            elif status in ("superseded", "rejected"):
                issues.append(f"cites {cited}, which is {status}")

    allowed = TECH_ALLOWED.get(name, False)
    if allowed is not None:
        scan = prose
        if allowed:
            scan = prose.replace(section(prose, allowed), "")
        for block in mermaid_blocks(text):
            scan += "\n" + block
        for term in TECH_DENYLIST:
            if re.search(rf"(?<![\w.]){re.escape(term)}(?![\w])", scan):
                issues.append(f"technology name '{term}' outside an allowed section")

    return issues


def aggregates_06(text: str) -> set[str]:
    return set(headings(section(text, "Aggregates"), 3))


def aggregates_07(text: str) -> set[str]:
    level4 = section(text, "Level 4: Domain structure")
    names = set()
    for block in mermaid_blocks(level4):
        for name, body in re.findall(r"class\s+(\w+)\s*\{(.*?)\}", block, re.DOTALL):
            if "<<Aggregate>>" in body:
                names.add(name)
    return names


def normalise(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: uv run scripts/check_spec.py <prdfy-spec folder>")
        return 2
    spec = Path(sys.argv[1])
    memory_path = spec / "memory.md"
    ids = memory_ids(memory_path.read_text(encoding="utf-8")) if memory_path.exists() else None
    if ids is None:
        print("WARN memory.md not found; skipping ID checks")

    failures, texts = 0, {}
    for name in CONTRACT:
        path = spec / name
        if not path.exists():
            print(f"FAIL {name}: missing")
            failures += 1
            continue
        texts[name] = path.read_text(encoding="utf-8")
        issues = check_file(name, texts[name], ids)
        for issue in issues:
            print(f"FAIL {name}: {issue}")
        failures += len(issues)

    if "06-domain-architecture.md" in texts and "07-c4-architecture.md" in texts:
        in_06 = {normalise(a): a for a in aggregates_06(texts["06-domain-architecture.md"])}
        in_07 = {normalise(a): a for a in aggregates_07(texts["07-c4-architecture.md"])}
        for key in sorted(in_06.keys() - in_07.keys()):
            print(f"FAIL cross: aggregate '{in_06[key]}' is in 06 but not in C4 level 4")
            failures += 1
        for key in sorted(in_07.keys() - in_06.keys()):
            print(f"FAIL cross: aggregate '{in_07[key]}' is in C4 level 4 but not in 06")
            failures += 1

    if failures:
        print(f"{failures} issue(s)")
        return 1
    print(f"OK {len(texts)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
