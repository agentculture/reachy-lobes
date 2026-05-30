"""Shared helpers for the robot noun groups (``device``, ``app``, ``move``).

Keeps the per-noun command modules thin: they import :func:`get_transport` and
:func:`add_robot_args` (re-exported from :mod:`reachy.robot`), render results
with :func:`emit_payload`, and describe themselves with :func:`noun_overview`.
"""

from __future__ import annotations

from typing import Any

from reachy.cli._commands.overview import emit_overview
from reachy.cli._output import emit_result
from reachy.robot import add_robot_args, get_transport

__all__ = ["add_robot_args", "get_transport", "emit_payload", "noun_overview"]


def _text_lines(data: Any, indent: int = 0) -> list[str]:
    """Render a JSON-ish value as readable ``key: value`` / bullet lines."""
    pad = "  " * indent
    lines: list[str] = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.extend(_text_lines(value, indent + 1))
            else:
                lines.append(f"{pad}{key}: {value}")
    elif isinstance(data, list):
        if not data:
            lines.append(f"{pad}(none)")
        for item in data:
            if isinstance(item, dict):
                head = item.get("name") or item.get("id")
                if head:
                    lines.append(f"{pad}- {head}")
                    rest = {k: v for k, v in item.items() if k != "name"}
                    lines.extend(_text_lines(rest, indent + 1))
                else:
                    lines.extend(_text_lines(item, indent + 1))
            else:
                lines.append(f"{pad}- {item}")
    else:
        lines.append(f"{pad}{data}")
    return lines


def emit_payload(data: Any, *, json_mode: bool, empty: str = "(no data)") -> None:
    """Emit a transport result to stdout: raw JSON, or flattened text lines."""
    if json_mode:
        emit_result(data, json_mode=True)
        return
    if data is None:
        emit_result(empty, json_mode=False)
        return
    text = "\n".join(_text_lines(data)) or empty
    emit_result(text, json_mode=False)


def noun_overview(subject: str, verbs: list[str], *, json_mode: bool) -> None:
    """Emit a per-noun overview (verbs + the shared robot conventions)."""
    sections: list[dict[str, object]] = [
        {"title": "Verbs", "items": list(verbs)},
        {
            "title": "Transports",
            "items": [
                "http (default) — daemon REST API, no extra runtime deps",
                "sdk — in-process reachy_mini client (needs the [sdk] extra)",
            ],
        },
        {
            "title": "Conventions",
            "items": [
                "every command supports --json",
                "action verbs accept --transport {http,sdk}, --base-url, --timeout",
                "exit codes: 0 ok, 1 user error, 2 environment (daemon unreachable)",
            ],
        },
    ]
    emit_overview(subject, sections, json_mode=json_mode)
