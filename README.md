# tz-convert

Convert a date/time between timezones — zero-dependency Python CLI (stdlib only, Python 3.9+).

## Install

No dependencies. Just Python 3.9 or newer:

```sh
git clone https://github.com/heyzcx/tz-convert.git
cd tz-convert
```

## Usage

Convert a time from one zone to another:

```sh
python3 tz_convert.py "2026-11-18 09:00" --from America/New_York --to Asia/Shanghai
```

```
2026-11-18 09:00:00 EST (UTC-0500)  <- America/New_York
2026-11-18 22:00:00 CST (UTC+0800)  <- Asia/Shanghai
```

Convert the current time to several zones at once:

```sh
python3 tz_convert.py --now --to Asia/Shanghai Europe/London America/Los_Angeles
```

Convert from UTC (the default source zone):

```sh
python3 tz_convert.py "2026-11-18T15:00:00" --to America/New_York
```

Find a zone name:

```sh
python3 tz_convert.py --list shanghai
python3 tz_convert.py --list        # list every known zone
```

Accepted input formats: `YYYY-MM-DD HH:MM`, `YYYY-MM-DD HH:MM:SS`,
`YYYY-MM-DDTHH:MM`, `YYYY-MM-DDTHH:MM:SS`, or a bare date `YYYY-MM-DD`
(treated as midnight in the source zone).

## License

MIT
