"""Test package setup.

Adds ``src/`` to ``sys.path`` so the suite runs from the repository root with
``python -m unittest discover -s tests -v`` without installing the package.
"""

from __future__ import annotations

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
