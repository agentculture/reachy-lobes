"""``reachy-mini-cli device`` — device setup / status noun group.

Reports the Reachy daemon's status and the robot's live state. Both verbs route
through a transport flavor (``--transport http`` by default); a missing daemon
yields a clean exit-2 ``error:``/``hint:`` rather than a traceback.
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
    "device status — daemon status (state, version, wireless/lite, sim)",
    "device state — live robot state (head pose, antennas, body yaw)",
    "device overview — this summary",
]


def cmd_device_overview(args: argparse.Namespace) -> int:
    noun_overview(
        "reachy-mini-cli device",
        _VERBS,
        json_mode=bool(getattr(args, "json", False)),
    )
    return 0


def cmd_device_status(args: argparse.Namespace) -> int:
    data = get_transport(args).daemon_status()
    emit_payload(data, json_mode=bool(getattr(args, "json", False)))
    return 0


def cmd_device_state(args: argparse.Namespace) -> int:
    data = get_transport(args).robot_state()
    emit_payload(data, json_mode=bool(getattr(args, "json", False)))
    return 0


def _no_verb(args: argparse.Namespace) -> int:
    return cmd_device_overview(args)


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser(
        "device",
        help="Device setup and status (see 'reachy-mini-cli device overview').",
    )
    p.add_argument("--json", action="store_true", help="Emit structured JSON.")
    p.set_defaults(func=_no_verb, json=False)
    noun_sub = p.add_subparsers(dest="device_command", parser_class=type(p))

    ov = noun_sub.add_parser("overview", help="Describe the device noun group.")
    ov.add_argument("--json", action="store_true", help="Emit structured JSON.")
    ov.set_defaults(func=cmd_device_overview)

    st = noun_sub.add_parser("status", help="Report the Reachy daemon status.")
    add_robot_args(st)
    st.set_defaults(func=cmd_device_status)

    sta = noun_sub.add_parser("state", help="Report live robot state (pose, antennas).")
    add_robot_args(sta)
    sta.set_defaults(func=cmd_device_state)
