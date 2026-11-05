import re

PANEL_AREA_SQFT = 18
MAX_SITE_NAME_LEN = 100

# Only ASCII digits are accepted (re.ASCII stops \d matching Unicode digits
# such as '٣' that int() would otherwise silently accept). Digit counts are
# capped so a huge input cannot trigger int()'s digit limit or a slow parse.
_UNITS_RE = re.compile(r"(\d{1,7})\s*(?:kwh)?", re.ASCII | re.IGNORECASE)
_ROOF_RE = re.compile(
    r"(\d{1,5})\s*(?:ft)?\s*x\s*(\d{1,5})\s*(?:ft)?", re.ASCII | re.IGNORECASE
)


def clean_site_name(name):
    """
    Trims a site name, removes '#' and '@', and title-cases it.
    Returns None if the input is not a string or nothing usable is left.
    """
    if not isinstance(name, str):
        return None
    for ch in ['#', '@']:
        name = name.replace(ch, '')
    name = name.strip()
    if not name:
        return None
    return name[:MAX_SITE_NAME_LEN].title()


def parse_monthly_units(text):
    """
    Converts a reading such as '320 kWh' into an int.
    Returns None if the input is not a string or not a valid
    non-negative whole-number reading (optionally followed by 'kWh').
    """
    if not isinstance(text, str):
        return None
    match = _UNITS_RE.fullmatch(text.strip())
    if match is None:
        return None
    return int(match.group(1))


def panels_for_roof(text):
    """
    Works out how many 18 sq ft panels fit on a roof given as 'Lft x Wft'.
    Returns None if the input is not a string, is not in the expected
    format, or has a zero dimension.
    """
    if not isinstance(text, str):
        return None
    match = _ROOF_RE.fullmatch(text.strip())
    if match is None:
        return None
    length, width = int(match.group(1)), int(match.group(2))
    if length == 0 or width == 0:
        return None
    return length * width // PANEL_AREA_SQFT


def _show(label, result, hint):
    if result is None:
        print(f"{label}: invalid input ({hint})")
    else:
        print(f"{label}:", result)


def main():
    print("==== Running clean_site_name ====")
    value = input("Enter the installation site name: ")
    _show("Site name", clean_site_name(value), "name cannot be empty")

    print("\n==== Running parse_monthly_units ====")
    value = input("Enter monthly electricity use (e.g. 320 kWh): ")
    _show("Monthly units", parse_monthly_units(value), "expected e.g. 320 kWh")

    print("\n==== Running panels_for_roof ====")
    value = input("Enter roof size as LENGTHft x WIDTHft (e.g. 20ft x 15ft): ")
    _show("Panels that fit", panels_for_roof(value), "expected e.g. 20ft x 15ft")


if __name__ == "__main__":
    main()
