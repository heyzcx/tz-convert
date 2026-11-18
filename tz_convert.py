#!/usr/bin/env python3
"""tz-convert: convert a date/time between timezones.

Zero-dependency Python CLI (stdlib only, Python 3.9+).

Usage:
    python3 tz_convert.py "2026-11-18 09:00" --from America/New_York --to Asia/Shanghai
    python3 tz_convert.py --now --to Asia/Shanghai Europe/London
    python3 tz_convert.py --list shanghai
    python3 tz_convert.py "2026-11-18T09:00:00" --from UTC --to America/Los_Angeles America/New_York

Accepted input formats: "YYYY-MM-DD HH:MM", "YYYY-MM-DD HH:MM:SS",
"YYYY-MM-DDTHH:MM", "YYYY-MM-DDTHH:MM:SS", or a bare date "YYYY-MM-DD"
(which is treated as midnight in the source zone).
"""

import argparse
import sys
from datetime import datetime

try:
    from zoneinfo import ZoneInfo, available_timezones
except ImportError:  # pragma: no cover - Python < 3.9
    sys.exit("tz-convert needs Python 3.9 or newer (zoneinfo module).")

INPUT_FORMATS = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%d",
)


def parse_time(text):
    """Parse a date/time string; return a naive datetime or None."""
    for fmt in INPUT_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def load_zone(name):
    """Return a ZoneInfo, or exit with a helpful error."""
    try:
        return ZoneInfo(name)
    except Exception:
        print(f"error: unknown timezone {name!r} (try --list to search)", file=sys.stderr)
        sys.exit(2)


def fmt(dt):
    """Render an aware datetime with zone name and UTC offset."""
    return dt.strftime("%Y-%m-%d %H:%M:%S %Z (UTC%z)")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Convert a date/time between timezones."
    )
    parser.add_argument("time", nargs="?", help='date/time, e.g. "2026-11-18 09:00"')
    parser.add_argument("--from", dest="source", default="UTC",
                        help="source timezone (default: UTC)")
    parser.add_argument("--to", nargs="+", metavar="ZONE",
                        help="one or more target timezones")
    parser.add_argument("--now", action="store_true",
                        help="convert the current time instead of a given time")
    parser.add_argument("--list", metavar="QUERY", nargs="?", const="",
                        help="list timezones, optionally filtered by a substring")
    args = parser.parse_args(argv)

    if args.list is not None:
        query = args.list.lower()
        zones = sorted(z for z in available_timezones() if query in z.lower())
        if not zones:
            print(f'no timezone matches {args.list!r}')
            return 1
        print("\n".join(zones))
        return 0

    if not args.to:
        parser.error("--to is required (give at least one target timezone)")

    if args.now:
        if args.time:
            parser.error("give either a time or --now, not both")
        moment = datetime.now(ZoneInfo("UTC"))
    else:
        if not args.time:
            parser.error("give a time, or use --now")
        naive = parse_time(args.time)
        if naive is None:
            print(f"error: cannot parse time {args.time!r}", file=sys.stderr)
            print("expected e.g. '2026-11-18 09:00' or '2026-11-18T09:00:00'",
                  file=sys.stderr)
            return 2
        moment = naive.replace(tzinfo=load_zone(args.source))

    print(f"{fmt(moment)}  <- {args.source if not args.now else 'UTC (now)'}")
    for target in args.to:
        zone = load_zone(target)
        print(f"{fmt(moment.astimezone(zone))}  <- {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
