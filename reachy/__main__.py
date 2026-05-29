"""Entry point for ``python -m reachy``."""

from __future__ import annotations

import sys

from reachy.cli import main

if __name__ == "__main__":
    sys.exit(main())
