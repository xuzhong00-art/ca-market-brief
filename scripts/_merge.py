# -*- coding: utf-8 -*-
import json, sys, datetime, re
sys.path.insert(0, "scripts")
import urllib.parse
from _fetch import quotes
from _proc import dedupe, day  # noqa
r = json.load(open("data/_raw.json"))
TODAY = "2026-11-09"
# Yahoo rows
rows = {}
for side in ("yg", "yl"):
    for q in dedupe([q for q in r[side] if day(q["regularMarketTime"]) == TODAY]):
        rows[q["symbol"]] = {"sym": q["symbol"], "name": q.get("longName") or q.get("shortName"), "price": q["regularMarketPrice"],
                             "chg": q["regularMarketChangePercent"], "cap": q["marketCap"], "vol": q["regularMarketVolume"],
                             "avg": q.get("averageDailyVolume3Month"), "src": "Y", "cdr": False}
# TV DR rows: TSX preferred over NEO
dr = {}
for k in ("dr_desc", "dr_asc"):
    for d in r["tv"][k]:
        ex, t = d["s"].split(":")
        if t not in dr or ex == "TSX":
            dr[t] = (ex, d["d"])
drsyms = []
for t, (ex, d) in dr.items():
    drsyms += [t + ".TO", t + ".NE"]
yq = {q["symbol"]: q for q in quotes(drsyms)}
for t, (ex, d) in dr.items():
    cands = [yq.get(t + ".TO"), yq.get(t + ".NE")]
    cands = [c for c in cands if c and day(c.get("regularMarketTime")) == TODAY]
    best = next((c for c in cands if c.get("averageDailyVolume3Month")), cands[0] if cands else None)
    if not best:
        print("no yahoo for", t, file=sys.stderr); continue
    sym = best["symbol"]
    # drop Yahoo duplicates for this CDR under other suffix
    for s in (t + ".TO", t + ".NE"):
        rows.pop(s, None)
    rows[sym] = {"sym": sym, "name": d[1], "price": best["regularMarketPrice"], "chg": best["regularMarketChangePercent"],
                 "cap": d[4], "vol": best["regularMarketVolume"], "avg": best.get("averageDailyVolume3Month"), "src": "TV-DR", "cdr": True,
                 "tvchg": d[3], "tvsector": d[5]}
# attach TV sector for stock rows
tvsec = {}
for k in ("stock_desc", "stock_asc"):
    for d in r["tv"][k]:
        tvsec[d["s"].split(":")[1].replace(".", "-")] = (d["d"][5], d["d"][6], d["d"][3])
for s, v in rows.items():
    base = s.rsplit(".", 1)[0]
    if base in tvsec and not v["cdr"]:
        v["tvsector"], v["tvind"], v["tvchg"] = tvsec[base]
allr = list(rows.values())
g = sorted(allr, key=lambda x: -x["chg"])[:30]
l = sorted(allr, key=lambda x: x["chg"])[:30]
def fmt(v):
    v["vr"] = round(v["vol"] / v["avg"], 1) if v.get("avg") else None
    return v
for name, lst in (("GAINERS", g), ("LOSERS", l)):
    print("==", name)
    for i, v in enumerate(lst, 1):
        fmt(v)
        print(i, v["sym"], v["name"][:28], v["price"], round(v["chg"], 2), "tv=%s" % v.get("tvchg"), "%.1fB" % (v["cap"] / 1e9), v.get("tvsector"), v.get("tvind", ""), v["vol"], v["avg"], v["vr"], "CDR" if v["cdr"] else "")
json.dump({"g": g, "l": l}, open("data/_merged.json", "w"), indent=1, ensure_ascii=False)
