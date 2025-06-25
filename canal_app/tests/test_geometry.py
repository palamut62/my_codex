import math
from canal_app.geometry import RectangularSection, TrapezoidalSection


def test_rectangular_area():
    sec = RectangularSection(bottom_width=2.0, depth=1.0)
    assert math.isclose(sec.area(), 2.0)
    assert math.isclose(sec.wetted_perimeter(), 2 * 1.0 + 2.0)


def test_trapezoidal_area():
    sec = TrapezoidalSection(bottom_width=2.0, depth=1.0, side_slope=1.0)
    assert math.isclose(sec.area(), 3.0)
    perim = 2 * math.sqrt(2) * 1.0 + 2.0
    assert math.isclose(sec.wetted_perimeter(), perim)
