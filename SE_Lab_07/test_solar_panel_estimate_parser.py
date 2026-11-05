from hypothesis import given, settings, strategies as st
from solar_panel_estimate_parser import clean_site_name, parse_monthly_units, panels_for_roof


@settings(max_examples=500)
@given(st.text() | st.none())
def test_clean_site_name_no_crash(s):
    try:
        result = clean_site_name(s)
    except Exception as e:
        assert False, f"clean_site_name crashed on {s!r} with: {type(e).__name__}: {e}"
    # A cleaned name is either a string or None (for invalid input)
    assert result is None or isinstance(result, str)
    if result is not None:
        assert '#' not in result and '@' not in result


@settings(max_examples=500)
@given(st.text() | st.none())
def test_parse_monthly_units_no_crash(s):
    try:
        result = parse_monthly_units(s)
    except Exception as e:
        assert False, f"parse_monthly_units crashed on {s!r} with: {type(e).__name__}: {e}"
    # Monthly usage is either a non-negative int or None (for invalid input)
    assert result is None or (isinstance(result, int) and result >= 0)


@settings(max_examples=500)
@given(st.text() | st.none())
def test_panels_for_roof_no_crash(s):
    try:
        result = panels_for_roof(s)
    except Exception as e:
        assert False, f"panels_for_roof crashed on {s!r} with: {type(e).__name__}: {e}"
    # Panel count is either a non-negative int or None (for invalid input)
    assert result is None or (isinstance(result, int) and result >= 0)
