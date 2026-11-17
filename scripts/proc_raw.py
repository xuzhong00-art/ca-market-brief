# -*- coding: utf-8 -*-
"""Process ca_raw.json (from fetch_raw.py): dedupe, freshness, TV cross-check. Prints compact tables."""
import json, datetime, re, os, sys
from datetime import timezone, timedelta
TMP = os.environ.get("LOCALAPPDATA", ".") + "/Temp"
raw = json.load(open(TMP + "/ca_raw.json", encoding="utf-8"))
TODAY = datetime.date(2026, 11, 17)
FRAC = float(sys.argv[1]) if len(sys.argv) > 1 else 0.077
ET = timezone(timedelta(hours=-5))

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
EXP = {"TSX":0,"TSXV":1,"CSE":2,"NEO":3}
tvmap = {}
for k in ("tvg","tvl","tvgd","tvld"):
    for d in raw[k]:
        ex, sym = d["ticker"].split(":"); d["ex"], d["sym"] = ex, sym
        d["bd"] = datetime.datetime.fromtimestamp(d["time"], ET).strftime("%m-%d %H:%M") if d.get("time") else None
        if sym not in tvmap or EXP.get(ex,9) < EXP.get(tvmap[sym]["ex"],9): tvmap[sym] = d

def fmtcap(c):
    if not c: return "?"
    return f"{c/1e9:.1f}B" if c >= 1e9 else f"{c/1e6:.0f}M"

results = {}
for side, key in (("gainers","yg"),("losers","yl")):
    seen, rows = {}, []
    for q in raw[key]:
        sym = q["symbol"]; t = q.get("regularMarketTime")
        dt = datetime.datetime.fromtimestamp(t, ET) if t else None
        fresh = dt and dt.date() == TODAY
        nk = norm(q.get("longName") or q.get("shortName"))
        base = sym.rsplit(".",1)[0].replace("-",".")
        tvr = tvmap.get(base)
        vol = q.get("regularMarketVolume") or 0; avg = q.get("averageDailyVolume3Month") or 0
        rec = {"sym":sym, "name":q.get("longName") or q.get("shortName"), "price":q.get("regularMarketPrice"),
               "chg":round(q.get("regularMarketChangePercent") or 0, 2), "cap":q.get("marketCap"), "vol":vol, "avg":avg,
               "vr": round(vol/(avg*FRAC),1) if avg else None, "time":dt.strftime("%m-%d %H:%M") if dt else None, "fresh":bool(fresh),
               "tv_chg": round(tvr["change"],2) if tvr else None, "tv_sector": tvr["sector"] if tvr else None,
               "tv_ind": tvr["industry"] if tvr else None, "tv_ex": tvr["ex"] if tvr else None, "tv_bd": tvr["bd"] if tvr else None,
               "tv_cap": tvr["market_cap_basic"] if tvr else None, "is_dr": bool(tvr and tvr["type"]=="dr"), "drop": None}
        if not fresh: rec["drop"]="stale"
        elif nk in seen:
            old = seen[nk]
            if suf(sym) < suf(old["sym"]): old["drop"]="xdup"; seen[nk]=rec
            else: rec["drop"]="xdup"
        else: seen[nk]=rec
        rows.append(rec)
    results[side]=rows

yh_bases = {r["sym"].rsplit(".",1)[0].replace("-",".") for s in ("gainers","losers") for r in results[s]}
tvonly = {"gainers":[], "losers":[]}
for side, keys in (("gainers",("tvg","tvgd")),("losers",("tvl","tvld"))):
    for k in keys:
        for d in raw[k]:
            if d["sym"] in yh_bases: continue
            tvonly[side].append(d)

json.dump({"results":results, "tvonly":tvonly, "frac":FRAC}, open(TMP+"/ca_proc.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

for side in ("gainers","losers"):
    print(f"==== {side} (Yahoo rows, kept first) ====")
    n=0
    for r in results[side]:
        if r["drop"]: continue
        n+=1
        print(f"{n:2d} {r['sym']:10s} {str(r['name'])[:28]:28s} {r['price']:>8} {r['chg']:>7}% cap={fmtcap(r['cap']):>6} vol={r['vol']:>9} avg={r['avg']:>9} vr={r['vr']} t={r['time']} tv={r['tv_chg']} {r['tv_ex']} {r['tv_sector']}/{r['tv_ind']} tvcap={fmtcap(r['tv_cap'])}{' DR' if r['is_dr'] else ''}")
    print("-- dropped:")
    for r in results[side]:
        if r["drop"]: print(f"   {r['drop']:5s} {r['sym']:10s} {str(r['name'])[:28]:28s} {r['chg']}% t={r['time']}")
    print(f"-- TV-only ({side}):")
    for d in tvonly[side]:
        print(f"   {d['ticker']:14s} {str(d['description'])[:30]:30s} {d['close']:>8} {round(d['change'],2):>7}% cap={fmtcap(d['market_cap_basic'])} vol={d['volume']} {d['type']} {d['sector']} bd={d['bd']}")
