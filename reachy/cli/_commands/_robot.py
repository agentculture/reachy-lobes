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


def _dict_lines(data: dict, indent: int) -> list[str]:
    pad = "  " * indent
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            lines.append(f"{pad}{key}:")
            lines.extend(_text_lines(value, indent + 1))
        else:
            lines.append(f"{pad}{key}: {value}")
    return lines


def _item_lines(item: Any, indent: int) -> list[str]:
    pad = "  " * indent
    if not isinstance(item, dict):
        return [f"{pad}- {item}"]
    head = item.get("name") or item.get("id")
    if not head:
        return _text_lines(item, indent + 1)
    rest = {k: v for k, v in item.items() if k != "name"}
    return [f"{pad}- {head}", *_text_lines(rest, indent + 1)]


def _text_lines(data: Any, indent: int = 0) -> list[str]:
    """Render a JSON-ish value as readable ``key: value`` / bullet lines."""
    pad = "  " * indent
    if isinstance(data, dict):
        return _dict_lines(data, indent)
    if isinstance(data, list):
        if not data:
            return [f"{pad}(none)"]
        lines: list[str] = []
        for item in data:
            lines.extend(_item_lines(item, indent))
        return lines
    return [f"{pad}{data}"]


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
