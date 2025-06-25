"""Geometry module defining canal cross-section classes."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Section(ABC):
    """Abstract base class for canal sections."""

    bottom_width: float  # in meters
    depth: float  # in meters
    side_slope: float = 0.0  # horizontal to vertical ratio (1:m)
    freeboard: float = 0.0  # additional freeboard height in meters

    @abstractmethod
    def area(self) -> float:
        """Return cross-sectional area in square meters."""

    @abstractmethod
    def wetted_perimeter(self) -> float:
        """Return wetted perimeter in meters."""

    def formwork_length(self) -> float:
        """Length of formwork needed per meter channel."""
        return self.wetted_perimeter()

    def concrete_area(self, length: float) -> float:
        """Concrete lining area for a given length."""
        return self.wetted_perimeter() * length

    def concrete_volume(self, length: float, thickness: float = 0.1) -> float:
        """Concrete volume for a given length and lining thickness."""
        return self.concrete_area(length) * thickness


@dataclass
class RectangularSection(Section):
    """Vertical sided rectangular section."""

    side_slope: float = 0.0

    def area(self) -> float:
        return self.bottom_width * (self.depth + self.freeboard)

    def wetted_perimeter(self) -> float:
        return 2 * (self.depth + self.freeboard) + self.bottom_width


@dataclass
class TrapezoidalSection(Section):
    """Symmetric trapezoidal section."""

    def area(self) -> float:
        top_width = self.bottom_width + 2 * self.side_slope * (self.depth + self.freeboard)
        return (self.bottom_width + top_width) / 2 * (self.depth + self.freeboard)

    def wetted_perimeter(self) -> float:
        slant = ( (self.side_slope ** 2 + 1) ** 0.5 ) * (self.depth + self.freeboard)
        return 2 * slant + self.bottom_width
