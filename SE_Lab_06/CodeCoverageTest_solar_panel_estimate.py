import pytest
from solar_panel_estimate import panels_needed, install_cost, payback_years


# ---------- panels_needed ----------
def test_mono_exact():
    assert panels_needed(300, "mono", 5) == 5

def test_unknown_panel_type():
    with pytest.raises(ValueError):
        panels_needed(300, "thin_film", 5)

def test_invalid_units():
    with pytest.raises(ValueError):
        panels_needed(0, "mono", 5)

def test_round_up_panels():
    # 400 units -> 13333 Wh/day, 330*5 = 1650 Wh/panel -> 8.08 -> 9 panels
    assert panels_needed(400, "poly", 5) == 9

def test_minimum_two_panels():
    assert panels_needed(10, "mono", 6) == 2


# ---------- install_cost ----------
def test_concrete_roof():
    assert install_cost(4, "concrete", False) == 100000

def test_invalid_panel_count():
    with pytest.raises(ValueError):
        install_cost(0, "concrete", False)

def test_tin_roof():
    assert install_cost(4, "tin", False) == 108000

def test_tiled_roof():
    assert install_cost(4, "tiled", False) == 108000

def test_unknown_roof():
    with pytest.raises(ValueError):
        install_cost(4, "thatch", False)

def test_battery_and_bulk_discount():
    # 10*25000 + 60000 = 310000, minus 10% = 279000
    assert install_cost(10, "concrete", True) == 279000


# ---------- payback_years ----------
def test_zero_saving():
    assert payback_years(100000, 20, 0) == -1

def test_subsidy_capped_round_up():
    # subsidy capped at 40 -> net 60000; yearly 12000*... 1000*12 = 12000 -> 5 exactly
    # use 1100/month -> 13200/yr -> 60000/13200 = 4.54 -> 5
    assert payback_years(100000, 50, 1100) == 5
