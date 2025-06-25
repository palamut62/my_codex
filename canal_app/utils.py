"""Utility functions for the canal app."""
from __future__ import annotations

import io
import json
from dataclasses import asdict
from typing import Dict, Any

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - optional dependency
    plt = None

from .geometry import Section


def mm_to_m(value_mm: float) -> float:
    """Convert millimeter input to meters."""
    return value_mm / 1000.0


def section_to_dict(section: Section, length: float) -> Dict[str, Any]:
    """Return calculation results as dictionary."""
    data = {
        "area_m2": section.area(),
        "formwork_m": section.formwork_length(),
        "concrete_area_m2": section.concrete_area(length),
        "concrete_volume_m3": section.concrete_volume(length),
    }
    data.update(asdict(section))
    data["length"] = length
    return data


def dict_to_yaml_json(data: Dict[str, Any]) -> str:
    """Return a simple YAML and JSON representation of data."""
    yaml_lines = [f"{k}: {v}" for k, v in data.items()]
    yaml_part = "\n".join(yaml_lines)
    json_part = json.dumps(data, indent=2, ensure_ascii=False)
    return f"---\n{yaml_part}\n---\n{json_part}"


def draw_section(section: Section) -> io.BytesIO:
    """Return PNG image bytes of the cross section."""
    if plt is None:
        raise RuntimeError("matplotlib is required for drawing")

    fig, ax = plt.subplots(figsize=(4, 3))
    b = section.bottom_width
    h = section.depth + section.freeboard
    m = section.side_slope

    if isinstance(section, Section):
        top = b + 2 * m * h
        ax.plot([0, b], [0, 0], color="black")  # bottom
        ax.plot([0, -m * h], [0, h], color="black")
        ax.plot([b, b + m * h], [0, h], color="black")
        ax.plot([-m * h, b + m * h], [h, h], color="black", linestyle="--")
        ax.set_aspect('equal')
        ax.set_xlabel('m')
        ax.set_ylabel('m')
        ax.set_title('Kesit')
        ax.set_xlim(-m * h - 0.5, b + m * h + 0.5)
        ax.set_ylim(0, h + 0.5)
        ax.grid(True, linestyle=':')

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)
    return buffer

