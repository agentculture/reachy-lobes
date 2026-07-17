"""Entry point for ``python -m reachy_lobes``."""

from __future__ import annotations

import sys

from reachy_lobes.cli import main

if __name__ == "__main__":
    sys.exit(main())
