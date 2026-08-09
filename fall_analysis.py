#!/usr/bin/env python3
"""Mine data/town_events.jsonl to test hypotheses for the "most active resident"
town-inheritance rule.

Keeps only clean algorithm cases — an inactive mayor's town that passed to a
resident with NO councillors present (councillors inherit first, so those don't
exercise the rule) and did not ruin — then, for each, ranks the residents by
several observable metrics and checks which metric put the actual heir at #1.
The metric that wins most often is the best observable model of the rule.

Hypotheses tested (all from API-visible fields):
  last_online   heir = resident with the most recent lastOnline
  tenure        heir = resident who joined the town earliest (longest tenure)
  acct_oldest   heir = resident with the oldest Minecraft account
  acct_newest   heir = resident with the newest account

Usage: python3 fall_analysis.py [-i data/town_events.jsonl] [-o data] [--inactive-days 40]
"""
import argparse
import json
import os
from datetime import datetime, timezone

METRICS = {
    # name: (key, reverse)  reverse=True means larger value ranks first
    "last_online": ("lastOnline", True),
    "tenure":      ("joinedTownAt", False),
    "acct_oldest": ("registered", False),
    "acct_newest": ("registered", True),
}


def _epoch(iso):
    return datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def load(path):
    if not os.path.exists(path):
        return []
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def is_clean_fall(e, inactive_days):
    if e.get("had_councillors") or not e.get("new_mayor_was_resident"):
        return False
    if e.get("new_mayor_was_councillor") or e.get("town_ruined_now"):
        return False
    if e["new_mayor"]["uuid"] == e["old_mayor"]["uuid"]:
        return False
    lo = e["old_mayor"].get("lastOnline")
    if not lo:
        return False
    idle_days = (_epoch(e["detected_at"]) - lo / 1000.0) / 86400.0
    return idle_days >= inactive_days


def heir_rank(e, key, reverse):
    """Rank (1=best) of the actual heir among residents by a metric; None if the
    heir's metric is missing."""
    heir = e["new_mayor"]["uuid"]
    vals = [(r["uuid"], r.get(key)) for r in e["residents"] if r.get(key) is not None]
    if not any(u == heir for u, _ in vals):
        return None, len(e["residents"])
    vals.sort(key=lambda x: x[1], reverse=reverse)
    order = [u for u, _ in vals]
    return order.index(heir) + 1, len(vals)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default="data/town_events.jsonl")
    ap.add_argument("-o", "--outdir", default="data")
    ap.add_argument("--inactive-days", type=float, default=40.0)
    args = ap.parse_args(argv)

    events = load(args.input)
    clean = [e for e in events if is_clean_fall(e, args.inactive_days)]

    result = {"generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "total_mayor_changes": len(events),
              "clean_most_active_falls": len(clean),
              "inactive_days_threshold": args.inactive_days,
              "hypotheses": {}}

    for name, (key, rev) in METRICS.items():
        top1 = 0
        ranks = []
        scored = 0
        for e in clean:
            rank, n = heir_rank(e, key, rev)
            if rank is None:
                continue
            scored += 1
            ranks.append(rank / n)     # normalized rank (0=best)
            if rank == 1:
                top1 += 1
        result["hypotheses"][name] = {
            "scored_events": scored,
            "heir_ranked_1st": top1,
            "top1_rate": round(top1 / scored, 3) if scored else None,
            "mean_normalized_rank": round(sum(ranks) / len(ranks), 3) if ranks else None,
        }

    os.makedirs(args.outdir, exist_ok=True)
    json.dump(result, open(os.path.join(args.outdir, "fall_analysis.json"), "w"), indent=2)

    print(f"Mayor changes logged: {len(events)} | clean 'most-active-resident' falls: {len(clean)}")
    if not clean:
        print("Not enough clean falls yet — the observatory needs to run for a while.\n"
              "(Councillor-less inactivity falls are rare; evidence accrues over weeks.)")
        return 0
    print(f"\n{'hypothesis':14s} {'heir #1':>8s} {'of':>4s} {'top-1 rate':>11s} {'mean rank':>10s}")
    for name in sorted(result["hypotheses"], key=lambda n: -(result["hypotheses"][n]["top1_rate"] or 0)):
        h = result["hypotheses"][name]
        print(f"{name:14s} {h['heir_ranked_1st']:>8d} {h['scored_events']:>4d} "
              f"{(h['top1_rate'] if h['top1_rate'] is not None else 0):>11.2f} "
              f"{(h['mean_normalized_rank'] if h['mean_normalized_rank'] is not None else 0):>10.2f}")
    print("\nThe hypothesis with the highest top-1 rate best models the rule.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
