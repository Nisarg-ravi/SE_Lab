import pytest
from solar_panel_estimate import panels_needed, install_cost, payback_years


# ================= panels_needed =================
# Branches: panel type valid/invalid, input valid/invalid,
# remainder yes/no, panels < 2 yes/no

def test_mono_exact():
    # no remainder, panels >= 2
    assert panels_needed(300, "mono", 5) == 5


def test_poly_panels():
    # 300 units -> 10000 Wh/day, 330*5 = 1650 Wh/panel -> 6 rem 100 -> 7
    assert panels_needed(300, "poly", 5) == 7


def test_panels_round_up():
    # remainder present -> round up
    assert panels_needed(310, "mono", 5) == 6


def test_panels_minimum_two():
    # tiny usage -> 1 panel -> bumped to minimum of 2
    assert panels_needed(10, "mono", 5) == 2


def test_unknown_panel_type():
    with pytest.raises(ValueError, match="unknown panel type"):
        panels_needed(300, "thin-film", 5)


def test_zero_units():
    with pytest.raises(ValueError, match="invalid input"):
        panels_needed(0, "mono", 5)


def test_negative_units():
    with pytest.raises(ValueError, match="invalid input"):
        panels_needed(-50, "mono", 5)


def test_zero_sun_hours():
    with pytest.raises(ValueError, match="invalid input"):
        panels_needed(300, "mono", 0)


# ================= install_cost =================
# Branches: panels < 1, roof tin / tiled / concrete / unknown,
# battery yes/no, panels >= 10 yes/no

def test_invalid_panel_count():
    with pytest.raises(ValueError, match="invalid panel count"):
        install_cost(0, "concrete", False)


def test_concrete_roof():
    assert install_cost(4, "concrete", False) == 100000


def test_tin_roof():
    assert install_cost(4, "tin", False) == 108000


def test_tiled_roof():
    # 4*25000 + 4*2000 = 108000
    assert install_cost(4, "tiled", False) == 108000


def test_unknown_roof():
    with pytest.raises(ValueError, match="unknown roof type"):
        install_cost(4, "thatch", False)


def test_with_battery():
    assert install_cost(4, "concrete", True) == 160000


def test_bulk_discount_exactly_ten():
    # 250000 - 10% = 225000
    assert install_cost(10, "concrete", False) == 225000


def test_just_below_discount():
    # 9 panels, no discount
    assert install_cost(9, "concrete", False) == 225000


def test_bulk_tiled_with_battery():
    # 12*25000 + 12*2000 + 60000 = 384000, minus 10% = 345600
    assert install_cost(12, "tiled", True) == 345600


# ================= payback_years =================
# Branches: saving <= 0, subsidy > 40 yes/no, remainder yes/no

def test_zero_saving():
    assert payback_years(100000, 30, 0) == -1


def test_negative_saving():
    assert payback_years(100000, 30, -500) == -1


def test_subsidy_capped():
    # 50% capped at 40% -> net 60000, yearly 12000 -> exactly 5
    assert payback_years(100000, 50, 1000) == 5


def test_subsidy_exactly_forty():
    assert payback_years(100000, 40, 1000) == 5


def test_subsidy_below_cap_round_up():
    # 30% -> net 70000, yearly 12000 -> 5 rem -> 6
    assert payback_years(100000, 30, 1000) == 6


def test_no_subsidy():
    # net 120000, yearly 12000 -> exactly 10
    assert payback_years(120000, 0, 1000) == 10
