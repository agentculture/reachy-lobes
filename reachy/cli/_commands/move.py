"""``reachy-mini-cli move`` — runtime motion noun group.

Drives the robot's head/antennas. ``goto`` takes friendly units — millimetres
for translation, degrees for rotation — which the transport converts to the
daemon's metres + radians. ``wake`` / ``sleep`` play the built-in animations.
"""

from __future__ import annotations

import argparse

from reachy.cli._commands._robot import (
    add_robot_args,
    emit_payload,
    get_transport,
    noun_overview,
)
from reachy.robot import INTERPOLATIONS

_HEAD_KEYS = ("x", "y", "z", "roll", "pitch", "yaw")

_VERBS = [
    "move goto — move head/antennas (mm + degrees; --duration, --interpolation)",
    "move wake — play the wake-up animation",
    "move sleep — play the go-to-sleep animation",
    "move overview — this summary",
]


def cmd_move_overview(args: argparse.Namespace) -> int:
    noun_overview(
        "reachy-mini-cli move",
        _VERBS,
        json_mode=bool(getattr(args, "json", False)),
    )
    return 0


def cmd_move_goto(args: argparse.Namespace) -> int:
    head: dict[str, float] | None = None
    if any(getattr(args, key) is not None for key in _HEAD_KEYS):
        head = {key: (getattr(args, key) or 0.0) for key in _HEAD_KEYS}
    antennas = tuple(args.antennas) if args.antennas is not None else None
    data = get_transport(args).move_goto(
        head=head,
        antennas=antennas,
        body_yaw=args.body_yaw,
        duration=args.duration,
        interpolation=args.interpolation,
    )
    emit_payload(data, json_mode=bool(getattr(args, "json", False)), empty="(move accepted)")
    return 0


def cmd_move_wake(args: argparse.Namespace) -> int:
    data = get_transport(args).wake()
    emit_payload(data, json_mode=bool(getattr(args, "json", False)), empty="(wake accepted)")
    return 0


def cmd_move_sleep(args: argparse.Namespace) -> int:
    data = get_transport(args).sleep()
    emit_payload(data, json_mode=bool(getattr(args, "json", False)), empty="(sleep accepted)")
    return 0


def _no_verb(args: argparse.Namespace) -> int:
    return cmd_move_overview(args)


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser(
        "move",
        help="Runtime motion (see 'reachy-mini-cli move overview').",
    )
    p.add_argument("--json", action="store_true", help="Emit structured JSON.")
    p.set_defaults(func=_no_verb, json=False)
    noun_sub = p.add_subparsers(dest="move_command", parser_class=type(p))

    ov = noun_sub.add_parser("overview", help="Describe the move noun group.")
    ov.add_argument("--json", action="store_true", help="Emit structured JSON.")
    ov.set_defaults(func=cmd_move_overview)

    g = noun_sub.add_parser("goto", help="Move head/antennas to a target pose.")
    g.add_argument("--x", type=float, default=None, help="Head X offset in mm.")
    g.add_argument("--y", type=float, default=None, help="Head Y offset in mm.")
    g.add_argument("--z", type=float, default=None, help="Head Z offset in mm.")
    g.add_argument("--roll", type=float, default=None, help="Head roll in degrees.")
    g.add_argument("--pitch", type=float, default=None, help="Head pitch in degrees.")
    g.add_argument("--yaw", type=float, default=None, help="Head yaw in degrees.")
    g.add_argument(
        "--antennas",
        type=float,
        nargs=2,
        metavar=("RIGHT", "LEFT"),
        default=None,
        help="Antenna angles in degrees (right, left).",
    )
    g.add_argument(
        "--body-yaw",
        type=float,
        default=None,
        dest="body_yaw",
        help="Body yaw in degrees.",
    )
    g.add_argument(
        "--duration",
        type=float,
        default=2.0,
        help="Movement duration in seconds (default: 2.0).",
    )
    g.add_argument(
        "--interpolation",
        choices=INTERPOLATIONS,
        default="minjerk",
        help="Interpolation curve (default: minjerk).",
    )
    add_robot_args(g)
    g.set_defaults(func=cmd_move_goto)

    wake = noun_sub.add_parser("wake", help="Play the wake-up animation.")
    add_robot_args(wake)
    wake.set_defaults(func=cmd_move_wake)

    sleep = noun_sub.add_parser("sleep", help="Play the go-to-sleep animation.")
    add_robot_args(sleep)
    sleep.set_defaults(func=cmd_move_sleep)
