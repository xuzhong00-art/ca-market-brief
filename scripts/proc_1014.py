# -*- coding: utf-8 -*-
"""Process _yh_raw.json + _tv_raw_scan.json for 2026-10-14 (post-close catch-up, FRAC=1.0)."""
import json, datetime, re
from datetime import timezone, timedelta

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
yh = json.load(open(D+"_yh_raw.json", encoding="utf-8"))
tv = json.load(open(D+"_tv_raw_scan.json", encoding="utf-8"))
TODAY = datetime.date(2026, 10, 14)
FRAC = 1.0
ET = timezone(timedelta(hours=-4))
COLS = ["name","description","close","change","market_cap_basic","sector","volume","avg90","type","exchange","update_mode","time"]

def norm(name):
    n = (name or "").upper()
    n = re.sub(r"[^A-Z0-9 ]", " ", n)
    for w in ["INC","CORP","CORPORATION","LTD","LIMITED","AND","THE","CO","PLC","GROUP","HOLDINGS","COMPANY","NEW","CDR","CAD","HEDGED","CANADIAN","DEPOSITARY","RECEIPT","RECEIPTS","CLASS","A","B","SHS","UNSPONSORED"]:
        n = re.sub(r"\b%s\b" % w, "", n)
    return " ".join(n.split())[:18]

SUFP = {".TO":0, ".V":1, ".CN":2, ".NE":3}
def suf(sym):
    for s,p in SUFP.items():
        if sym.endswith(s): return p
    return 9

# TV map: base ticker -> row (prefer TSX)
EXP = {"TSX":0,"TSXV":1,"CSE":2,"NEO":3}
tvmap, tvnames = {}, {}
for k, blob in tv.items():
    if not blob: continue
    for it in blob["data"]:
        d = dict(zip(COLS, it["d"])); ex, sym = it["s"].split(":")
        d["ex"], d["sym"] = ex, sym
        d["bd"] = datetime.datetime.fromtimestamp(d["time"], ET).strftime("%Y-%m-%d") if d.get("time") else None
        if sym not in tvmap or EXP.get(ex,9) < EXP.get(tvmap[sym]["ex"],9):
            tvmap[sym] = d
        tvnames.setdefault(norm(d["description"]), d)

results = {}
for side in ["gainers","losers"]:
    seen, rows = {}, []
    for q in yh[side]:
        sym = q["symbol"]; t = q.get("regularMarketTime")
        dt = datetime.datetime.fromtimestamp(t) if t else None
        fresh = dt and dt.date() == TODAY
        key = norm(q.get("longName") or q.get("shortName"))
        base = sym.rsplit(".",1)[0].replace("-",".")
        tvr = tvmap.get(base)
        vol = q.get("regularMarketVolume") or 0; avg = q.get("averageDailyVolume3Month") or 0
        rec = {"sym":sym, "name":q.get("longName") or q.get("shortName"), "price":q.get("regularMarketPrice"),
               "chg":round(q.get("regularMarketChangePercent") or 0, 2), "cap":q.get("marketCap"), "vol":vol, "avg":avg,
               "vr": round(vol/(avg*FRAC),1) if avg else None, "time":str(dt), "fresh":bool(fresh),
               "tv_chg": round(tvr["change"],2) if tvr else None, "tv_sector": tvr["sector"] if tvr else None,
               "tv_ex": tvr["ex"] if tvr else None, "tv_bd": tvr["bd"] if tvr else None,
               "is_dr": bool(tvr and tvr["type"]=="dr")}
        if not fresh: rec["drop"]="stale"; rows.append(rec); continue
        if key in seen:
            old = seen[key]
            if suf(sym) < suf(old["sym"]): old["drop"]="xlist-dup"; seen[key]=rec
            else: rec["drop"]="xlist-dup"
            rows.append(rec); continue
        seen[key]=rec; rows.append(rec)
    results[side]=rows

# TV-only names (in TV top lists but not in Yahoo kept set)
yh_bases = {r["sym"].rsplit(".",1)[0].replace("-",".") for s in results.values() for r in s}
tvonly = {}
for order, side in (("desc","gainers"),("asc","losers")):
    lst=[]
    for t in ("stock","dr"):
        blob = tv.get(f"{order}_{t}")
        if not blob: continue
        for it in blob["data"]:
            d = dict(zip(COLS, it["d"])); ex, sym = it["s"].split(":")
            if sym in yh_bases: continue
            bd = datetime.datetime.fromtimestamp(d["time"], ET).strftime("%Y-%m-%d") if d.get("time") else None
            lst.append((sym, ex, d["description"], d["close"], round(d["change"],2), d["market_cap_basic"], d["sector"], d["volume"], d["avg90"], t, bd))
    tvonly[side]=lst
results["tvonly"]=tvonly
json.dump(results, open(D+"_proc.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

for side in ["gainers","losers"]:
    kept=[r for r in results[side] if "drop" not in r]; dropped=[r for r in results[side] if "drop" in r]
    print(f"\n== {side}: kept {len(kept)}, dropped {len(dropped)} ==")
    for r in dropped: print("  DROP", r["sym"], r["drop"], r["time"], r["chg"])
    for i,r in enumerate(kept[:34],1):
        cap=(r["cap"] or 0)/1e9; flag=""
        if r["tv_chg"] is not None and abs(r["tv_chg"]-r["chg"])>2: flag=" <<TVDIFF"
        if r["tv_chg"] is None: flag+=" <<NOTV"
        print(f"  {i:2d} {r['sym']:10s} {str(r['name'])[:26]:26s} {r['price']:>8} {r['chg']:+6.2f} tv={r['tv_chg']} cap={cap:.2f}B vol={r['vol']} vr={r['vr']} {r['tv_sector']}{' DR' if r['is_dr'] else ''}{flag}")
    print("  -- TV-only (first 25):")
    for x in tvonly[side][:25]:
        if abs(x[4]) >= abs(kept[29]["chg"]) if len(kept)>29 else True:
            print("   ", x)
