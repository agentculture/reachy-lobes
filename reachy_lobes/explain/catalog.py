"""Markdown catalog for ``reachy-lobes explain <path>``.

Each entry is verbatim markdown. Keys are command-path tuples. The empty tuple
and ``("reachy-lobes",)`` both resolve to the root entry.

Keep bodies self-contained: an agent reading one entry should get enough
context without chaining reads.
"""

from __future__ import annotations

_ROOT = """\
# reachy-lobes

A clonable template for AgentCulture mesh agents. It carries an agent-first CLI
(cited from the teken `python-cli` reference), a mesh identity (`culture.yaml` +
`CLAUDE.md`), the canonical guildmaster skill kit under `.claude/skills/`, and a
buildable/deployable package baseline. Clone it, rename the package, edit
`culture.yaml`, and you have a new agent.

## Verbs

- `reachy-lobes whoami` — identity probe from `culture.yaml`.
- `reachy-lobes learn` — structured self-teaching prompt.
- `reachy-lobes explain <path>` — markdown docs for any noun/verb.
- `reachy-lobes overview` — descriptive snapshot of the agent.
- `reachy-lobes doctor` — check the agent-identity invariants.
- `reachy-lobes cli overview` — describe the CLI surface.

## Exit-code policy

- `0` success
- `1` user-input error
- `2` environment / setup error
- `3+` reserved

## See also

- `reachy-lobes explain whoami`
- `reachy-lobes explain doctor`
"""

_WHOAMI = """\
# reachy-lobes whoami

Reports the agent's identity from `culture.yaml`: nick (`suffix`), backend,
served model, and the package version. Read-only.

## Usage

    reachy-lobes whoami
    reachy-lobes whoami --json
"""

_LEARN = """\
# reachy-lobes learn

Prints a structured self-teaching prompt covering purpose, command map,
exit-code policy, `--json` support, and the `explain` pointer.

## Usage

    reachy-lobes learn
    reachy-lobes learn --json
"""

_EXPLAIN = """\
# reachy-lobes explain <path>

Prints markdown documentation for any noun/verb path. Unlike `--help` (terse,
positional), `explain` is global and addressable by path.

## Usage

    reachy-lobes explain reachy-lobes
    reachy-lobes explain whoami
    reachy-lobes explain --json <path>
"""

_OVERVIEW = """\
# reachy-lobes overview

Read-only descriptive snapshot of the agent: identity (from `culture.yaml`), the
verb surface, and the sibling-pattern artifacts the template carries. Accepts an
ignored `target` so a stray path never hard-fails.

## Usage

    reachy-lobes overview
    reachy-lobes overview --json
"""

_DOCTOR = """\
# reachy-lobes doctor

Checks the agent-identity invariants `steward doctor` verifies:
prompt-file-present and backend-consistency (`colleague` → `AGENTS.colleague.md`), plus a
skills-present check. Exits 1 when unhealthy.

## Usage

    reachy-lobes doctor
    reachy-lobes doctor --json
"""

_CLI = """\
# reachy-lobes cli

Noun group for CLI-surface introspection. `cli overview` describes the CLI
itself (distinct from the global `overview`, which describes the agent).

## Usage

    reachy-lobes cli overview
    reachy-lobes cli overview --json
"""


ENTRIES: dict[tuple[str, ...], str] = {
    (): _ROOT,
    ("reachy-lobes",): _ROOT,
    ("whoami",): _WHOAMI,
    ("learn",): _LEARN,
    ("explain",): _EXPLAIN,
    ("overview",): _OVERVIEW,
    ("doctor",): _DOCTOR,
    ("cli",): _CLI,
    ("cli", "overview"): _CLI,
}
