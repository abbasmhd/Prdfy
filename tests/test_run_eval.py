import importlib
import json
import queue
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILL_CREATOR = ROOT / ".agents" / "skills" / "skill-creator"
sys.path.insert(0, str(SKILL_CREATOR))
run_eval = importlib.import_module("scripts.run_eval")

NEGATIVE_QUERY = "Draw a C4 container diagram of this repository's current services."
CLEAN_NAME = "prdfy-skill-abcd1234"


class _UUID:
    hex = "abcd1234"


class _Stdout:
    def __init__(self, payload: bytes, fail: bool):
        self._payload = payload
        self.fail = fail
        self.done = False

    def fileno(self):
        return 7

    def read1(self, _n):
        if self.fail:
            raise OSError(10093, "select failed")
        if self.done:
            return b""
        self.done = True
        return self._payload

    def read(self, n=-1):
        return self.read1(n)


class _Process:
    def __init__(self, stdout: _Stdout):
        self.stdout = stdout
        self.killed = False

    def poll(self):
        if self.killed:
            return -9
        if self.stdout.done and not self.stdout.fail:
            return 0
        return None

    def kill(self):
        self.killed = True

    def wait(self, timeout=None):
        self.killed = True
        return -9


class _ImmediateFuture:
    def __init__(self, fn, args):
        self._fn = fn
        self._args = args

    def result(self):
        return self._fn(*self._args)


class _ImmediatePool:
    def __init__(self, max_workers):
        self.max_workers = max_workers

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def submit(self, fn, *args):
        return _ImmediateFuture(fn, args)


def _trigger_line() -> bytes:
    event = {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": CLEAN_NAME},
                }
            ]
        },
    }
    return (json.dumps(event) + "\n").encode()


def _install_agent(monkeypatch, payload: bytes, fail: bool, select_error: OSError | None):
    calls = {"select": 0, "argv": None}
    process = _Process(_Stdout(payload, fail))
    monkeypatch.setenv("PRDFY_AGENT_CMD", "agent-under-test {query}")

    def fake_select(*_args, **_kwargs):
        calls["select"] += 1
        if select_error is not None:
            raise select_error
        return ([process.stdout], [], [])

    def fake_popen(cmd, *_args, **_kwargs):
        calls["argv"] = list(cmd)
        return process

    monkeypatch.setattr(run_eval.select, "select", fake_select)
    monkeypatch.setattr(run_eval.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(run_eval.uuid, "uuid4", lambda: _UUID())
    return calls, process


def test_windows_select_error_is_not_scored_as_not_triggered(monkeypatch, tmp_path):
    calls, _process = _install_agent(
        monkeypatch,
        payload=b"",
        fail=True,
        select_error=OSError(10093, "select failed"),
    )

    with pytest.raises(run_eval.QueryUnobservable):
        run_eval.run_single_query(
            NEGATIVE_QUERY,
            "prdfy",
            "desc",
            2,
            str(tmp_path),
        )
    assert calls["select"] >= 1
    assert calls["argv"] == ["agent-under-test", NEGATIVE_QUERY]
    assert "claude" not in calls["argv"]

    monkeypatch.setattr(run_eval, "ProcessPoolExecutor", _ImmediatePool)
    monkeypatch.setattr(run_eval, "as_completed", lambda futures: list(futures))

    def pipe_error(*_args, **_kwargs):
        raise OSError(10093, "select failed")

    monkeypatch.setattr(run_eval, "run_single_query", pipe_error)
    with pytest.raises(run_eval.QueryUnobservable):
        run_eval.run_eval(
            [{"query": NEGATIVE_QUERY, "should_trigger": False}],
            skill_name="prdfy",
            description="desc",
            num_workers=1,
            timeout=1,
            project_root=tmp_path,
            runs_per_query=1,
        )


def test_windows_select_error_still_observes_a_trigger(monkeypatch, tmp_path):
    calls, _process = _install_agent(
        monkeypatch,
        payload=_trigger_line(),
        fail=False,
        select_error=OSError(10093, "select failed"),
    )

    triggered = run_eval.run_single_query(
        "prdfy: a marketplace for local tutors",
        "prdfy",
        "desc",
        2,
        str(tmp_path),
    )
    assert calls["select"] >= 1
    assert calls["argv"][0] == "agent-under-test"
    assert "claude" not in calls["argv"]
    assert triggered is True


def test_ready_select_still_observes_a_trigger(monkeypatch, tmp_path):
    payload = _trigger_line()
    calls, _process = _install_agent(
        monkeypatch,
        payload=payload,
        fail=False,
        select_error=None,
    )

    def fake_read(_fd, _n):
        return payload

    monkeypatch.setattr(run_eval.os, "read", fake_read)
    triggered = run_eval.run_single_query(
        "prdfy: a marketplace for local tutors",
        "prdfy",
        "desc",
        2,
        str(tmp_path),
    )
    assert calls["select"] >= 1
    assert calls["argv"][0] == "agent-under-test"
    assert "claude" not in calls["argv"]
    assert triggered is True


def test_missing_agent_command_names_the_variable_and_does_not_spawn(monkeypatch, tmp_path):
    monkeypatch.delenv("PRDFY_AGENT_CMD", raising=False)

    def fail_popen(*_args, **_kwargs):
        raise AssertionError("spawned a process without an agent command")

    monkeypatch.setattr(run_eval.subprocess, "Popen", fail_popen)
    with pytest.raises(run_eval.AgentCommandError, match="PRDFY_AGENT_CMD") as exc_info:
        run_eval.run_single_query(
            NEGATIVE_QUERY,
            "prdfy",
            "desc",
            2,
            str(tmp_path),
        )
    assert "claude" not in str(exc_info.value).lower()


def test_agent_command_placeholder_fills_query_and_model():
    argv = run_eval.build_agent_argv(
        "agent-under-test {query} --model {model}",
        "hello there",
        None,
    )
    assert argv == ["agent-under-test", "hello there"]
    argv = run_eval.build_agent_argv(
        "agent-under-test {query} --model {model}",
        "hello there",
        "some-model",
    )
    assert argv == ["agent-under-test", "hello there", "--model", "some-model"]


def test_real_pipe_stays_readable_when_select_cannot_watch_it():
    proc = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import sys; sys.stdout.buffer.write(b'ping\\n'); sys.stdout.buffer.flush()",
        ],
        stdout=subprocess.PIPE,
    )
    chunks = []
    try:
        try:
            chunk = run_eval._selectable_chunk(proc.stdout, 2.0)
        except run_eval._PipeNotSelectable:
            out = queue.Queue()
            thread = run_eval._start_stdout_reader(proc.stdout, out)
            while True:
                item = out.get(timeout=2)
                if isinstance(item, Exception):
                    raise item
                if not item:
                    break
                chunks.append(item)
            thread.join(timeout=1)
        else:
            if chunk:
                chunks.append(chunk)
            rest = proc.stdout.read()
            if rest:
                chunks.append(rest)
        assert b"ping" in b"".join(chunks)
    finally:
        if proc.poll() is None:
            proc.kill()
        proc.wait(timeout=5)
