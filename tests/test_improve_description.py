import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILL_CREATOR = ROOT / ".agents" / "skills" / "skill-creator"
sys.path.insert(0, str(SKILL_CREATOR))
improve_description = importlib.import_module("scripts.improve_description")
run_eval = importlib.import_module("scripts.run_eval")

CURRENT = "OLD DESCRIPTION MARKER"


def _eval_results() -> dict:
    return {
        "results": [
            {
                "should_trigger": True,
                "pass": False,
                "query": "plan a product before writing code",
                "triggers": 0,
                "runs": 3,
            }
        ],
        "summary": {"passed": 0, "failed": 1, "total": 1},
    }


class _Completed:
    def __init__(self, stdout: str, returncode: int = 0):
        self.stdout = stdout
        self.stderr = ""
        self.returncode = returncode


def _propose(monkeypatch, command: str, *, use_env: bool) -> tuple[dict, str]:
    calls = {"argv": None}
    if use_env:
        monkeypatch.setenv("PRDFY_AGENT_CMD", command)
    else:
        monkeypatch.delenv("PRDFY_AGENT_CMD", raising=False)

    def fake_run(cmd, *_args, **_kwargs):
        calls["argv"] = list(cmd)
        return _Completed(
            "<new_description>Use this skill to plan a product before code.</new_description>"
        )

    monkeypatch.setattr(improve_description.subprocess, "run", fake_run)
    description = improve_description.improve_description(
        skill_name="prdfy",
        skill_content="Interview, then write a specification.",
        current_description=CURRENT,
        eval_results=_eval_results(),
        history=[],
        model="some-model",
        agent_cmd=None if use_env else command,
    )
    return calls, description


def test_improve_description_uses_agent_command_not_claude(monkeypatch):
    calls, description = _propose(
        monkeypatch,
        "agent-under-test {query}",
        use_env=True,
    )
    assert calls["argv"][0] == "agent-under-test"
    assert "claude" not in calls["argv"]
    assert calls["argv"][:2] != ["claude", "-p"]
    assert any(CURRENT in part for part in calls["argv"])
    assert description == "Use this skill to plan a product before code."
    assert description != CURRENT


def test_agent_cmd_argument_is_used_when_env_is_unset(monkeypatch):
    calls, description = _propose(
        monkeypatch,
        "agent-under-test {query} --model {model}",
        use_env=False,
    )
    assert calls["argv"] == [
        "agent-under-test",
        calls["argv"][1],
        "--model",
        "some-model",
    ]
    assert calls["argv"][0] != "claude"
    assert CURRENT in calls["argv"][1]
    assert description != CURRENT


def test_missing_agent_command_is_an_error_not_a_guessed_description(monkeypatch):
    monkeypatch.delenv("PRDFY_AGENT_CMD", raising=False)

    def fail_run(*_args, **_kwargs):
        raise AssertionError("spawned a process without an agent command")

    monkeypatch.setattr(improve_description.subprocess, "run", fail_run)
    with pytest.raises(run_eval.AgentCommandError, match="PRDFY_AGENT_CMD") as exc_info:
        improve_description.improve_description(
            skill_name="prdfy",
            skill_content="Interview, then write a specification.",
            current_description=CURRENT,
            eval_results=_eval_results(),
            history=[],
            model="some-model",
        )
    message = str(exc_info.value)
    assert "claude" not in message.lower()
    assert CURRENT not in message


def test_main_missing_agent_command_exits(monkeypatch, capsys):
    monkeypatch.delenv("PRDFY_AGENT_CMD", raising=False)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "improve_description.py",
            "--eval-results",
            "missing.json",
            "--skill-path",
            "missing-skill",
            "--model",
            "some-model",
        ],
    )

    def fail_run(*_args, **_kwargs):
        raise AssertionError("spawned a process without an agent command")

    monkeypatch.setattr(improve_description.subprocess, "run", fail_run)
    with pytest.raises(SystemExit) as exc_info:
        improve_description.main()
    assert exc_info.value.code == 1
    error = capsys.readouterr().err
    assert "PRDFY_AGENT_CMD" in error
    assert "claude" not in error.lower()
    assert CURRENT not in error
