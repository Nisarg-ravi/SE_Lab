import pytest
from solar_panel_estimate import panels_needed, install_cost, payback_years

#Example test cases:
def test_mono_exact():
    assert panels_needed(300, "mono", 5) == 5

def test_concrete_roof():
    assert install_cost(4, "concrete", False) == 100000

#Write the rest of the test cases so that the code is 90- 100% covered.
