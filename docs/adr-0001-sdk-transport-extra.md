# ADR 0001 — The `sdk` transport flavor and the `[sdk]` optional extra

Status: accepted (2026-05-30)

## Context

`CLAUDE.md` sets a hard constraint: **zero runtime dependencies**
(`pyproject.toml` keeps `dependencies = []`), so the default install is a
self-contained runtime. The constraint explicitly allows changing this *with an
explicit decision*:

> Do not add a third-party runtime import without an explicit decision to change
> this — it would break the "self-contained runtime" property the README sells.

The robot tooling needs to reach a Reachy Mini. Two ways exist: the daemon's
REST API (stdlib-only) and the in-process `reachy_mini` SDK client. The operator
asked for **both**, selectable as a transport "flavor".

## Decision

Ship two transports:

- **`http`** (default) — talks to the daemon over REST using only `urllib`. The
  default install stays dependency-free; `dependencies = []` is unchanged.
- **`sdk`** — drives the robot through `reachy_mini`. This is the one sanctioned
  third-party runtime import, and it is contained so the zero-dep property of
  the *default* install is preserved:
  - it lives behind an **optional extra**, `[project.optional-dependencies]`
    `sdk = ["reachy-mini>=1.0"]` — `pip install reachy-cli` pulls nothing extra;
    only `pip install 'reachy-cli[sdk]'` adds it;
  - it is **lazily imported** inside `SdkTransport`'s methods, so importing the
    package or running any `http`-transport command never imports `reachy_mini`;
  - if the extra is not installed, the `sdk` path fails with a clean
    `CliError` ("the reachy_mini SDK is not installed", remediation: install the
    extra or use `--transport http`) — never an `ImportError` traceback.

## Consequences

- The "self-contained runtime" property the README sells holds for the default
  install and every `http`-transport command.
- Operators who want in-process control opt in explicitly via the extra.
- This ADR is the explicit decision `CLAUDE.md` requires; `sdk_transport.py` and
  the `[sdk]` extra in `pyproject.toml` reference it.
