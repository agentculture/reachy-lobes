"""``reachy-mini-cli app`` — app management noun group.

Lists available apps, reports the running app, and starts/stops apps via the
selected transport. App management is a daemon-side concern, so these verbs
require ``--transport http`` (the default); the ``sdk`` flavor reports them as
unsupported.
"""

from __future__ import annotations

import argparse

from reachy.cli._commands._robot import (
    add_robot_args,
    emit_payload,
    get_transport,
    noun_overview,
)

_VERBS = [
    "app list — available apps (installed and installable)",
    "app status — the currently running app, if any",
    "app start <name> — start an installed app",
    "app stop — stop the currently running app",
    "app overview — this summary",
]


def cmd_app_overview(args: argparse.Namespace) -> int:
    noun_overview(
        "reachy-mini-cli app",
        _VERBS,
        json_mode=bool(getattr(args, "json", False)),
    )
    return 0


def cmd_app_list(args: argparse.Namespace) -> int:
    data = get_transport(args).apps_list()
    emit_payload(data, json_mode=bool(getattr(args, "json", False)), empty="(no apps)")
    return 0


def cmd_app_status(args: argparse.Namespace) -> int:
    data = get_transport(args).app_status()
    emit_payload(data, json_mode=bool(getattr(args, "json", False)), empty="(no app running)")
    return 0


def cmd_app_start(args: argparse.Namespace) -> int:
    data = get_transport(args).app_start(args.name)
    emit_payload(data, json_mode=bool(getattr(args, "json", False)), empty="(start requested)")
    return 0


def cmd_app_stop(args: argparse.Namespace) -> int:
    data = get_transport(args).app_stop()
    emit_payload(data, json_mode=bool(getattr(args, "json", False)), empty="(stop requested)")
    return 0


def _no_verb(args: argparse.Namespace) -> int:
    return cmd_app_overview(args)


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser(
        "app",
        help="App management (see 'reachy-mini-cli app overview').",
    )
    p.add_argument("--json", action="store_true", help="Emit structured JSON.")
    p.set_defaults(func=_no_verb, json=False)
    noun_sub = p.add_subparsers(dest="app_command", parser_class=type(p))

    ov = noun_sub.add_parser("overview", help="Describe the app noun group.")
    ov.add_argument("--json", action="store_true", help="Emit structured JSON.")
    ov.set_defaults(func=cmd_app_overview)

    ls = noun_sub.add_parser("list", help="List available apps.")
    add_robot_args(ls)
    ls.set_defaults(func=cmd_app_list)

    stt = noun_sub.add_parser("status", help="Show the currently running app.")
    add_robot_args(stt)
    stt.set_defaults(func=cmd_app_status)

    start = noun_sub.add_parser("start", help="Start an installed app by name.")
    start.add_argument("name", help="App name to start.")
    add_robot_args(start)
    start.set_defaults(func=cmd_app_start)

    stop = noun_sub.add_parser("stop", help="Stop the currently running app.")
    add_robot_args(stop)
    stop.set_defaults(func=cmd_app_stop)
