from canal_app.utils import mm_to_m


def test_mm_to_m():
    assert mm_to_m(1000) == 1.0
    assert mm_to_m(250) == 0.25
