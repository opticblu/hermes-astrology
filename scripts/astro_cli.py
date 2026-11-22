#!/usr/bin/env python3
"""CLI entry point for hermes-astrology."""
import argparse, json, sys, os

# Windows consoles default to legacy codepages (cp1256 etc.) that cannot
# encode the retrograde glyph; force UTF-8 output before any printing.
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add scripts dir to path for importing astro_engine
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from astro_engine import calculate_full_profile, _demo


def _get_version():
    """Read version from pyproject.toml (single source of truth)."""
    pyproject = os.path.join(_SCRIPTS_DIR, "..", "pyproject.toml")
    try:
        with open(pyproject) as f:
            for line in f:
                if line.startswith("version"):
                    parts = line.split('"')
                    if len(parts) >= 2:
                        return parts[1]
    except OSError:
        pass
    return "unknown"


def _load_data(args):
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file) as f:
            return json.load(f)
    return _demo()


def _format_output(data, fmt):
    if fmt == "json":
        return json.dumps(data, indent=2, default=str)
    return json.dumps(data, indent=2, default=str)


def main():
    ap = argparse.ArgumentParser(
        description="hermes-astrology — deterministic multi-tradition chart engine",
        epilog="Modes: natal, transit, synastry, compatibility, composite, "
               "solar_return, lunar_return, planetary_return, navamsa, varga, "
               "panchang, moon_phase, numerology, progressions, planetary_hours, "
               "transit_natal_aspects, horary, astrocartography",
    )
    ap.add_argument("--version", action="version",
                    version=f"hermes-astrology {_get_version()}")
    ap.add_argument("--json", help="birth data as JSON string")
    ap.add_argument("--file", help="path to birth data JSON file")
    ap.add_argument("--mode", "-m",
                    help="chart mode (default: natal)")
    ap.add_argument("--systems", "-s", nargs="*",
                    help="systems: western vedic bazi")
    ap.add_argument("--summary", action="store_true",
                    help="short summary instead of full JSON")
    ap.add_argument("--date", help="transit date YYYY-MM-DD")
    ap.add_argument("--partner", type=str,
                    help="partner birth data JSON (for synastry/compatibility)")
    a = ap.parse_args()

    try:
        data = _load_data(a)
        if a.mode:
            data["mode"] = a.mode
        if a.systems:
            data["systems"] = a.systems
        if a.date:
            data["transit_date"] = a.date
        if a.partner:
            data["partner"] = json.loads(a.partner)

        result = calculate_full_profile(data)
    except ValueError as e:  # includes json.JSONDecodeError
        print(f"error: invalid input: {e}", file=sys.stderr)
        sys.exit(2)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(2)
    except KeyError as e:
        print(f"error: missing required field: {e}", file=sys.stderr)
        sys.exit(2)

    if result.get("error"):
        print(f"error: {result['error']}", file=sys.stderr)
        sys.exit(2)
    if a.summary and "charts" in result:
        _print_summary(result)
    else:
        print(json.dumps(result, indent=2, default=str))


def _print_summary(result):
    charts = result.get("charts", {})
    for sys_name, ch in charts.items():
        if not ch:
            continue
        print(f"\n=== {sys_name.upper()} ===")
        if ch.get("zodiac"):
            print(f"  Zodiac: {ch['zodiac']}")
            if ch.get("house_system"):
                print(f"  Houses: {ch['house_system']}")
        asc = ch.get("ascendant") or ch.get("lagna")
        if asc:
            print(f"  Rising: {asc['sign']} {asc['deg_in_sign']:.1f}°")
        planets = ch.get("planets", {})
        if not isinstance(planets, dict):
            planets = {p.get("name", f"#{i}"): p for i, p in enumerate(planets)}
        for name, p in planets.items():
            if isinstance(p, dict):
                ret = " ℞" if p.get("retrograde") else ""
                house = p.get("house", p.get("bhava"))
                house_text = f"  H{house}" if house is not None else ""
                degrees = p.get("degrees", p.get("deg_in_sign"))
                degree_text = f" {degrees:.1f}°" if degrees is not None else ""
                sign = p.get("sign") or " or ".join(p.get("possible_signs", []))
                print(f"  {name:12s} {sign}{degree_text}{house_text}{ret}")


if __name__ == "__main__":
    main()
