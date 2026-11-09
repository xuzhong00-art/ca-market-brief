# -*- coding: utf-8 -*-
import json, re, datetime, sys
from collections import Counter
r = json.load(open("data/_raw.json"))
TODAY = "2026-11-09"
def day(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d") if ts else None
def norm(n):
    n = (n or "").upper()
    n = re.sub(r"\b(INC|CORP|CORPORATION|LTD|LIMITED|CO|COMPANY|THE|CLASS A|CLASS B|SUBORDINATE VOTING|NON-VOTING|SHARES|CDR|CAD HEDGED|COMMON)\b|[.,&]|\bAND\b", "", n)
    return re.sub(r"\s+", " ", n).strip()
pri = {".TO": 0, ".V": 1, ".CN": 2, ".NE": 3}
def dedupe(qs):
    best = {}
    for q in qs:
        suf = "." + q["symbol"].rsplit(".", 1)[-1]
        k = norm(q.get("longName") or q.get("shortName"))
        if k not in best or pri.get(suf, 9) < pri.get("." + best[k]["symbol"].rsplit(".", 1)[-1], 9):
            best[k] = q
    return list(best.values())
if __name__ == "__main__":
    for side in ("yg", "yl"):
        qs = r[side]
        stale = [(q["symbol"], day(q["regularMarketTime"]), q["regularMarketChangePercent"]) for q in qs if day(q["regularMarketTime"]) != TODAY]
        print(side, "stale:", stale)
        fresh = [q for q in qs if day(q["regularMarketTime"]) == TODAY]
        dd = dedupe(fresh)
        dd.sort(key=lambda q: q["regularMarketChangePercent"], reverse=(side == "yg"))
        for i, q in enumerate(dd[:40], 1):
            vr = q["regularMarketVolume"] / q["averageDailyVolume3Month"] if q.get("averageDailyVolume3Month") else None
            print(i, q["symbol"], (q.get("longName") or q.get("shortName"))[:30], q["regularMarketPrice"], round(q["regularMarketChangePercent"], 2),
                  q["marketCap"], q.get("sector"), q.get("industry"), q["regularMarketVolume"], q.get("averageDailyVolume3Month"), round(vr, 1) if vr else None)
    print("=== TV")
    for k, v in r["tv"].items():
        print("--", k)
        for d in v[:35]:
            print(d["s"], d["d"][1][:28], d["d"][2], round(d["d"][3], 2), d["d"][4], d["d"][5], d["d"][7], d["d"][8], day(d["d"][11]), d["d"][12])
