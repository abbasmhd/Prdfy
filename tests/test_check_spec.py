import importlib.util
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests" / "fixtures" / "minimal-spec"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_spec = load("check_spec")
check_skills = load("check_skills")


def run(path: Path, capsys) -> tuple[int, str]:
    sys.argv = ["check_spec.py", str(path)]
    code = check_spec.main()
    return code, capsys.readouterr().out


@pytest.fixture
def spec(tmp_path: Path) -> Path:
    target = tmp_path / "prdfy-spec"
    shutil.copytree(FIXTURE, target)
    return target


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, f"fixture text not found: {old!r}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def test_fixture_passes(spec, capsys):
    code, out = run(spec, capsys)
    assert code == 0, out


def test_skills_agree(capsys):
    assert check_skills.main() == 0, capsys.readouterr().out


@pytest.mark.parametrize(
    "skill, old, new, expected",
    [
        ("prdfy-c4", ", Cache.", ".", "missing ['Cache']"),
        ("prdfy-writer", 'protocol: "1"', 'protocol: "2"', "metadata.protocol is '2'"),
    ],
)
def test_skill_drift_is_reported(tmp_path, monkeypatch, capsys, skill, old, new, expected):
    skills = tmp_path / "skills"
    shutil.copytree(check_skills.SKILLS_DIR, skills)
    edit(skills / skill / "SKILL.md", old, new)
    monkeypatch.setattr(check_skills, "SKILLS_DIR", skills)
    assert check_skills.main() == 1
    assert expected in capsys.readouterr().out


@pytest.mark.parametrize(
    "file, old, new, expected",
    [
        ("02-prd.md", "## Constraints", "## Limits", "H2 headings should be"),
        ("03-specifications.md", "```mermaid\nstateDiagram-v2", "```python\nstateDiagram-v2", "code fence 'python'"),
        ("02-prd.md", "| D-002 | user |", "| D-999 | user |", "cites D-999, which is not in memory"),
        ("02-prd.md", "| D-002 | user |", "| D-007 | user |", "cites D-007, which is superseded"),
        ("02-prd.md", "| D-004 | user |", "|  | user |", "empty Decisions and no research source"),
        ("05-risk-compliance.md", "| D-004 | user | open |", "| D-004 |  | open |", "empty Source"),
        ("06-domain-architecture.md", "anticorruption layer", "PostgreSQL layer", "technology name 'PostgreSQL'"),
        ("06-domain-architecture.md", "### Booking", "### Reservation", "aggregate 'Reservation' is in 06"),
        ("07-c4-architecture.md", '"Requests a slot")\nRel(client', '"Uses")\nRel(client', "bare 'Uses'"),
        ("07-c4-architecture.md", "### Narrative\n\nNo Message", "### Notes\n\nNo Message", "subsections should be"),
    ],
)
def test_breakage_is_reported(spec, capsys, file, old, new, expected):
    edit(spec / file, old, new)
    code, out = run(spec, capsys)
    assert code == 1
    assert expected in out, out


def test_technology_rule_allowed_in_constraints(spec, capsys):
    edit(spec / "02-prd.md", "existing payment terminal.\"", "existing payment terminal, on PostgreSQL.\"")
    code, out = run(spec, capsys)
    assert code == 0, out


def test_blank_horizon_cell_is_rejected(spec, capsys):
    edit(
        spec / "04-strategy-roadmap.md",
        "| None confirmed | None confirmed |",
        "|  | None confirmed |",
    )
    code, out = run(spec, capsys)
    assert code == 1
    assert "empty Decisions and no research source" in out


def test_missing_file(spec, capsys):
    (spec / "04-strategy-roadmap.md").unlink()
    code, out = run(spec, capsys)
    assert code == 1
    assert "04-strategy-roadmap.md: missing" in out
