from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Tuple

Location = Tuple[float, float]


def project_root() -> Path:
    """Return the project root (folder that contains the 'app' directory)."""
    return Path(__file__).resolve().parent.parent


def resolve_config_path(filename: str = "config.json") -> Path:
    """
    Try to find the config file in common locations.

    The tests usually expect `config.json` in the project root, but on some
    templates it might be inside other folders. We search a few safe places.
    """
    root = project_root()

    candidates = (
        Path.cwd() / filename,
        root / filename,
        root / "app" / filename,
        root / "configs" / filename,
        root / "config" / filename,
        root / "data" / filename,
    )

    for path in candidates:
        if path.exists():
            return path

    raise FileNotFoundError(
        f"Could not find '{filename}'. Looked in: "
        + ", ".join(str(p) for p in candidates)
    )


def load_config(filename: str = "config.json") -> Dict[str, Any]:
    """Load the JSON config file and return it as a dict."""
    config_path = resolve_config_path(filename)
    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def to_location(raw: List[float]) -> Location:
    """Convert [x, y] list from JSON into a typed (x, y) tuple."""
    if len(raw) != 2:
        raise ValueError("Location must have exactly 2 values: [x, y].")

    x, y = raw
    return float(x), float(y)


def euclidean_distance_km(a: Location, b: Location) -> float:
    """Compute Euclidean distance between two 2D points."""
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx * dx + dy * dy)


def money_fmt(value: float) -> str:
    """Format money with 2 decimals for printing (as required by the task)."""
    return f"{value:.2f}"
