# -*- coding: utf-8 -*-
"""Process raw Yahoo+TV data: dedupe, freshness check, cross-validate, compute VR."""
import json, datetime, re

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
yh = json.load(open(D+"_yh_raw.json", encoding="utf-8"))
tv = json.load(open(D+"_tv_raw.json", encoding="utf-8"))

TODAY = datetime.date(2026, 8, 24)
# elapsed fraction of trading day (open 9:30 ET = 6:30 PT)
now = datetime.datetime.now()  # local = PT
open_t = now.replace(hour=6, minute=30, second=0)
frac = max((now - open_t).total_seconds() / 3600, 0.25) / 6.5
print("VR frac:", round(frac, 4))

def norm(name):
    n = (name or "").upper()
    n = re.sub(r"[^A-Z0-9 ]", " ", n)
    for w in ["INC","CORP","CORPORATION","LTD","LIMITED","AND","THE","CO","PLC","GROUP","HOLDINGS","COMPANY","NEW"]:
        n = re.sub(r"\b%s\b" % w, "", n)
    return " ".join(n.split())[:18]

SUFP = {".TO":0, ".V":1, ".CN":2, ".NE":3}
def suf(sym):
    for s,p in SUFP.items():
        if sym.endswith(s): return p
    return 9

# TV lookup: symbol -> row (both stock and dr), keyed by ticker base
tvmap = {}
drset = set()
for k, rows in tv.items():
    for r in rows:
        base = r["s"].split(":")[1]
        tvmap.setdefault(base, r)
        if r["type"] == "dr": drset.add(base)

results = {}
for side in ["gainers","losers"]:
    seen = {}
    rows = []
    for q in yh[side]:
        sym = q["symbol"]
        t = q.get("regularMarketTime")
        dt = datetime.datetime.fromtimestamp(t) if t else None
        fresh = dt and dt.date() == TODAY
        key = norm(q.get("longName") or q.get("shortName"))
        base = sym.split(".")[0].replace("-",".")
        tvr = tvmap.get(sym.split(".")[0])
        vol = q.get("regularMarketVolume") or 0
        avg = q.get("averageDailyVolume3Month") or 0
        vr = round(vol/(avg*frac), 1) if avg else None
        rec = {"sym":sym, "name":q.get("longName") or q.get("shortName"),
               "price":q.get("regularMarketPrice"),
               "chg":round(q.get("regularMarketChangePercent") or 0, 2),
               "cap":q.get("marketCap"), "vol":vol, "avg":avg, "vr":vr,
               "time":str(dt), "fresh":bool(fresh),
               "tv_chg": round(tvr["change"],2) if tvr else None,
               "tv_sector": tvr["sector"] if tvr else None,
               "tv_industry": tvr.get("industry") if tvr else None,
               "is_dr": sym.split(".")[0] in drset}
        if not fresh:
            rec["drop"] = "stale"
            rows.append(rec); continue
        if key in seen:
            # keep better suffix
            old = seen[key]
            if suf(sym) < suf(old["sym"]):
                old["drop"] = "xlist-dup"
                seen[key] = rec
            else:
                rec["drop"] = "xlist-dup"
            rows.append(rec); continue
        seen[key] = rec
        rows.append(rec)
    results[side] = rows

json.dump(results, open(D+"_proc.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

for side in ["gainers","losers"]:
    kept = [r for r in results[side] if "drop" not in r]
    dropped = [r for r in results[side] if "drop" in r]
    print(f"\n== {side}: kept {len(kept)}, dropped {len(dropped)} ==")
    for r in dropped: print("  DROP", r["sym"], r["drop"], r["time"], r["chg"])
    for i, r in enumerate(kept[:32], 1):
        cap = r["cap"]/1e9 if r["cap"] else 0
        flag = ""
        if r["tv_chg"] is not None and abs(r["tv_chg"] - r["chg"]) > 3: flag = " <<TVDIFF"
        print(f"  {i:2d} {r['sym']:10s} {str(r['name'])[:24]:24s} {r['price']:>8} {r['chg']:+6.2f} tv={r['tv_chg']} cap={cap:.2f}B vr={r['vr']} {r['tv_sector']}/{str(r['tv_industry'])[:20]}{' DR' if r['is_dr'] else ''}{flag}")
