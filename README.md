# EarthMC Vote Party Tracker

A dependency-free Python script that polls the [EarthMC API](https://earthmc.net/docs/api)
and logs vote party progress (plus a snapshot of server stats) to a file.

The vote party data lives on the root server endpoint
(`GET https://api.earthmc.net/v4/`) as:

```json
"voteParty": { "target": 5000, "numRemaining": 1646 }
```

`collected = target - numRemaining`, so the tracker derives the count and percentage
each poll.

## Usage

```bash
python3 voteparty_tracker.py            # adaptive, as fast as every 5 min
python3 voteparty_tracker.py -i 600     # base 10 minutes
python3 voteparty_tracker.py --max-interval 7200
python3 voteparty_tracker.py -f my.log  # custom log file
python3 voteparty_tracker.py --once     # single poll then exit
python3 voteparty_tracker.py --json     # also write machine-readable JSONL
```

Stop a running tracker with `Ctrl+C` (or `SIGTERM`); it logs a clean shutdown line.

## Adaptive polling

The interval is not fixed — it uses **AIMD** (additive-increase / multiplicative-decrease)
control so it collects as fast as the API tolerates without hammering it:

- Starts at the **base** interval (`-i`, default 300s = 5 min).
- On an HTTP **429 (rate limited)** it **doubles** the interval and honours the
  server's `Retry-After` header when present, up to `--max-interval`.
- On each successful poll it **eases back down** toward the base interval.
- Transient network errors trigger a mild (×1.5) back-off.

The current "next poll" spacing is shown on every log line and stored in the JSONL
`interval` field, so you can see the controller reacting.

> Note: the root endpoint is served through Cloudflare and may be briefly cached,
> so polling faster than the cache TTL can return identical data for a few seconds.

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `-u`, `--url` | `https://api.earthmc.net/v4/` | Server endpoint to poll |
| `-f`, `--logfile` | `voteparty.log` | Human-readable log file |
| `-i`, `--interval` | `300` | Base (fastest) seconds between polls (5 min) |
| `--max-interval` | `3600` | Slowest interval under throttling (1 hr) |
| `--once` | off | Poll once and exit |
| `--json [FILE]` | off (`voteparty.jsonl`) | Also append one JSON object per poll |

## What gets logged

Each poll appends a timestamped (UTC) line:

```
[2026-07-17T06:35:41Z] vote party 3398/5000 (68.0%) | 1602 remaining | players 406/800 | moon WAXING_CRESCENT
```

When the vote party fires (the remaining counter resets upward), it records a distinct event:

```
[...] *** VOTE PARTY FIRED! remaining reset 12 -> 4998 (+4986) ***
```

Network or parse errors are logged and the tracker keeps running.

The optional JSONL file captures the full snapshot per poll (target, remaining,
collected, percent, players, towns, nations, residents) for later analysis.
