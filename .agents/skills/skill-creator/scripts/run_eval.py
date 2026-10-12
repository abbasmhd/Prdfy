#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Tests whether a skill description causes an agent to trigger (read the skill)
for a set of queries. Outputs results as JSON.

The agent is not chosen for you. Set PRDFY_AGENT_CMD, or pass --agent-cmd, to
the command that runs one query. Put {query} where the query text should be
inserted. {model} is replaced when --model is set, and omitted otherwise.
{skill_file} is the temporary command file written under .claude/commands/ so
the agent can see the description under test. If neither the variable nor
--agent-cmd is set, the script exits with an error that names PRDFY_AGENT_CMD.
Stdout from that process is the only trigger signal. This script does not
score a query on its own.
"""

import argparse
import json
import os
import queue
import select
import shlex
import subprocess
import sys
import threading
import time
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from scripts.utils import parse_skill_md


class AgentCommandError(Exception):
    """The host did not provide a usable agent command."""


def agent_command_template(agent_cmd: str | None = None) -> str:
    """Return the agent command template from an argument or PRDFY_AGENT_CMD."""
    raw = agent_cmd if agent_cmd is not None else os.environ.get("PRDFY_AGENT_CMD")
    raw = (raw or "").strip()
    if not raw:
        raise AgentCommandError(
            "Set PRDFY_AGENT_CMD to the command that runs one trigger query, "
            "or pass --agent-cmd. Include {query} where the query text goes. "
            "No agent command is built in."
        )
    if "{query}" not in raw:
        raise AgentCommandError(
            "PRDFY_AGENT_CMD must include {query} where the query text goes."
        )
    return raw


def build_agent_argv(
    template: str,
    query: str,
    model: str | None = None,
    skill_file: str | None = None,
) -> list[str]:
    """Split an agent command template and fill its placeholders."""
    try:
        parts = shlex.split(template)
    except ValueError as exc:
        raise AgentCommandError(f"PRDFY_AGENT_CMD could not be parsed: {exc}") from exc

    argv: list[str] = []
    for part in parts:
        if "{query}" in part:
            part = part.replace("{query}", query)
        if "{skill_file}" in part:
            if not skill_file:
                raise AgentCommandError(
                    "PRDFY_AGENT_CMD uses {skill_file}, but no skill file was written."
                )
            part = part.replace("{skill_file}", skill_file)
        if "{model}" in part:
            if not model:
                if argv and argv[-1] in {"--model", "-m"}:
                    argv.pop()
                continue
            part = part.replace("{model}", model)
        if part == "":
            continue
        argv.append(part)
    if not argv:
        raise AgentCommandError("PRDFY_AGENT_CMD did not produce a command.")
    return argv


def find_project_root() -> Path:
    """Find the project root by walking up from cwd looking for .claude/.

    The temporary command file is written under that root's .claude/commands
    directory. PRDFY_AGENT_CMD chooses the process that answers the query.
    """
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".claude").is_dir():
            return parent
    return current


class QueryUnobservable(Exception):
    """Stdout could not be read, so this query has no trigger result."""


class _PipeNotSelectable(Exception):
    pass


def _start_stdout_reader(stream, out: queue.Queue) -> threading.Thread:
    def reader() -> None:
        try:
            while True:
                chunk = stream.read1(8192)
                out.put(chunk)
                if not chunk:
                    return
        except Exception as exc:
            out.put(exc)

    thread = threading.Thread(target=reader, daemon=True)
    thread.start()
    return thread


def _selectable_chunk(stream, wait_seconds: float):
    try:
        ready, _, _ = select.select([stream], [], [], wait_seconds)
    except OSError as exc:
        # Windows pipes are not sockets. select() raises WinError 10093 or 10038.
        raise _PipeNotSelectable() from exc
    if not ready:
        return None
    return os.read(stream.fileno(), 8192)


def _observe(fetch):
    """Return a trigger bool, or None when output could not be read.

    None is not a negative trigger. Callers must not count it as not triggered.
    A missing agent command is a configuration error, not a failed trigger.
    """
    try:
        return fetch()
    except AgentCommandError:
        raise
    except (QueryUnobservable, OSError) as exc:
        print(f"Warning: query output could not be read: {exc}", file=sys.stderr)
        return None
    except Exception as exc:
        print(f"Warning: query failed: {exc}", file=sys.stderr)
        return False


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
    agent_cmd: str | None = None,
) -> bool:
    """Run a single query and return whether the skill was triggered.

    Writes a command file under .claude/commands/ for the description under
    test, then runs the command from PRDFY_AGENT_CMD or agent_cmd. Early
    stream events (content_block_start) count as a trigger when they name
    that command file, so the check does not wait for the full assistant
    message.
    """
    template = agent_command_template(agent_cmd)
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{skill_name}-skill-{unique_id}"
    project_commands_dir = Path(project_root) / ".claude" / "commands"
    command_file = project_commands_dir / f"{clean_name}.md"

    try:
        project_commands_dir.mkdir(parents=True, exist_ok=True)
        # Use YAML block scalar to avoid breaking on quotes in description
        indented_desc = "\n  ".join(skill_description.split("\n"))
        command_content = (
            f"---\n"
            f"description: |\n"
            f"  {indented_desc}\n"
            f"---\n\n"
            f"# {skill_name}\n\n"
            f"This skill handles: {skill_description}\n"
        )
        command_file.write_text(command_content)

        cmd = build_agent_argv(template, query, model, str(command_file))

        # Drop CLAUDECODE when it is set so a nested Claude Code process is
        # allowed to start. Other agent commands ignore the missing variable.
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                cwd=project_root,
                env=env,
            )
        except FileNotFoundError as exc:
            raise QueryUnobservable(
                f"agent command {cmd[0]!r} was not found. "
                "PRDFY_AGENT_CMD must name an agent CLI installed on this host."
            ) from exc

        triggered = False
        start_time = time.time()
        buffer = ""
        # Track state for stream event detection
        pending_tool_name = None
        accumulated_json = ""
        pipe_queue = None
        reader_thread = None

        try:
            while time.time() - start_time < timeout:
                process_done = False
                if pipe_queue is None and process.poll() is not None:
                    remaining = process.stdout.read()
                    if remaining:
                        buffer += remaining.decode("utf-8", errors="replace")
                    process_done = True
                else:
                    if pipe_queue is None:
                        try:
                            chunk = _selectable_chunk(process.stdout, 1.0)
                        except _PipeNotSelectable:
                            pipe_queue = queue.Queue()
                            reader_thread = _start_stdout_reader(process.stdout, pipe_queue)
                            continue
                    else:
                        try:
                            chunk = pipe_queue.get(timeout=1.0)
                        except queue.Empty:
                            continue
                        if isinstance(chunk, Exception):
                            raise QueryUnobservable(
                                "could not read agent output after select() failed"
                            ) from chunk

                    if not chunk:
                        if chunk is None:
                            continue
                        process_done = True
                    else:
                        buffer += chunk.decode("utf-8", errors="replace")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # Early detection via stream events
                    if event.get("type") == "stream_event":
                        se = event.get("event", {})
                        se_type = se.get("type", "")

                        if se_type == "content_block_start":
                            cb = se.get("content_block", {})
                            if cb.get("type") == "tool_use":
                                tool_name = cb.get("name", "")
                                if tool_name in ("Skill", "Read"):
                                    pending_tool_name = tool_name
                                    accumulated_json = ""
                                else:
                                    return False

                        elif se_type == "content_block_delta" and pending_tool_name:
                            delta = se.get("delta", {})
                            if delta.get("type") == "input_json_delta":
                                accumulated_json += delta.get("partial_json", "")
                                if clean_name in accumulated_json:
                                    return True

                        elif se_type in ("content_block_stop", "message_stop"):
                            if pending_tool_name:
                                return clean_name in accumulated_json
                            if se_type == "message_stop":
                                return False

                    # Fallback: full assistant message
                    elif event.get("type") == "assistant":
                        message = event.get("message", {})
                        for content_item in message.get("content", []):
                            if content_item.get("type") != "tool_use":
                                continue
                            tool_name = content_item.get("name", "")
                            tool_input = content_item.get("input", {})
                            if tool_name == "Skill" and clean_name in tool_input.get("skill", ""):
                                triggered = True
                            elif tool_name == "Read" and clean_name in tool_input.get("file_path", ""):
                                triggered = True
                            return triggered

                    elif event.get("type") == "result":
                        return triggered

                if process_done:
                    break
        finally:
            # Clean up process on any exit path (return, exception, timeout)
            if process.poll() is None:
                process.kill()
                process.wait()
            if reader_thread is not None:
                reader_thread.join(timeout=1)

        return triggered
    finally:
        if command_file.exists():
            command_file.unlink()


def _rows_from_observations(
    query_items: dict[str, dict],
    query_triggers: dict[str, list],
    trigger_threshold: float,
) -> list[dict]:
    results = []
    for query, triggers in query_triggers.items():
        if any(trigger is None for trigger in triggers):
            raise QueryUnobservable(
                "query output could not be read, so it was not scored as not triggered"
            )
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append({
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })
    return results


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
    agent_cmd: str | None = None,
) -> dict:
    """Run the full eval set and return results."""
    template = agent_command_template(agent_cmd)
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                    template,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            query_triggers[query].append(_observe(future.result))

    results = _rows_from_observations(query_items, query_triggers, trigger_threshold)

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument(
        "--model",
        default=None,
        help="Optional model name. Replaces {model} in the agent command.",
    )
    parser.add_argument(
        "--agent-cmd",
        default=None,
        help="Command that runs one query. Defaults to PRDFY_AGENT_CMD. Include {query}.",
    )
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    try:
        agent_command_template(args.agent_cmd)
    except AgentCommandError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, content = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
        agent_cmd=args.agent_cmd,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}", file=sys.stderr)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
