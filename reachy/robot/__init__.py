"""Robot transport layer for reachy-mini-cli.

Robot verbs (``device``, ``app``, ``move``) call :func:`get_transport` to obtain
a :class:`~reachy.robot.transport.Transport` for the selected flavor and invoke
high-level operations on it. :func:`add_robot_args` adds the shared CLI flags
(``--json``, ``--transport``, ``--base-url``, ``--timeout``).
"""

from __future__ import annotations

from reachy.robot.transport import (
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT,
    INTERPOLATIONS,
    TRANSPORTS,
    Transport,
    add_robot_args,
    get_transport,
)

__all__ = [
    "DEFAULT_BASE_URL",
    "DEFAULT_TIMEOUT",
    "INTERPOLATIONS",
    "TRANSPORTS",
    "Transport",
    "add_robot_args",
    "get_transport",
]
