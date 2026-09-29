# -*- coding: utf-8 -*-
"""Merge Yahoo screener (_yh_raw.json) + TV scan (_tv_raw_scan.json) -> _proc.json + printed review.
Usage: python scripts/proc2.py YYYY-MM-DD [frac]
"""
import json, datetime, re, sys

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
TODAY = datetime.date.fromisoformat(sys.argv[1])
yh = json.load(open(D + "_yh_raw.json", encoding="utf-8"))
tv = json.load(open(D + "_tv_raw_scan.json", encoding="utf-8"))

if len(sys.argv) > 2:
    frac = float(sys.argv[2])
else:
    now = datetime.datetime.now()
    open_t = now.replace(hour=6, minute=30, second=0)
    frac = min(max((now - open_t).total_seconds() / 3600, 0.25) / 6.5, 1.0)
print("VR frac:", round(frac, 4))

COLS = ["name","description","close","change","market_cap_basic","sector","volume","avg90","type","exchange","update_mode","time"]
SUF = {"TSX": ".TO", "TSXV": ".V", "CSE": ".CN", "NEO": ".NE"}

def norm(name):
    n = (name or "").upper()
    n = re.sub(r"[^A-Z0-9 ]", " ", n)
    for w in ["INCORPORATION","CORPORATION","UNSPONSORED","DEPOSITORY","RECEIPT","CANADIAN","INC","CORP","LTD","LIMITED","AND","THE","CO","PLC","GROUP","HOLDINGS","COMPANY","NEW","CDR","CAD","HEDGED","SHS","CLASS","TRUST","REIT","REAL","ESTATE","INVESTMENT"]:
        n = re.sub(r"\b%s\b" % w, "", n)
    return " ".join(n.split())[:16]

SUFP = {".TO":0, ".V":1, ".CN":2, ".NE":3}
def suf(sym):
    for s,p in SUFP.items():
        if sym.endswith(s): return p
    return 9

# TV map: yahoo-style symbol -> row
tvrows = {}
for k, res in tv.items():
    if not res: continue
    for x in res["data"]:
        r = dict(zip(COLS, x["d"])); r["s"] = x["s"]
        ex, base = x["s"].split(":")
        ysym = base.replace(".", "-") + SUF.get(ex, "")
        tvrows[ysym] = r
        tvrows.setdefault(base, r)

results = {}
for side in ["gainers","losers"]:
    seen = {}; rows = []
    for q in yh[side]:
        sym = q["symbol"]
        t = q.get("regularMarketTime")
        dt = datetime.datetime.fromtimestamp(t) if t else None
        fresh = dt and dt.date() == TODAY
        key = norm(q.get("longName") or q.get("shortName"))
        tvr = tvrows.get(sym) or tvrows.get(sym.split(".")[0])
        vol = q.get("regularMarketVolume") or 0
        avg = q.get("averageDailyVolume3Month") or 0
        vr = round(vol/(avg*frac), 1) if avg else None
        rec = {"sym":sym, "name":q.get("longName") or q.get("shortName"),
               "price":q.get("regularMarketPrice"),
               "chg":round(q.get("regularMarketChangePercent") or 0, 2),
               "cap":q.get("marketCap"), "vol":vol, "avg":avg, "vr":vr,
               "time":str(dt), "fresh":bool(fresh),
               "tv_chg": round(tvr["change"],2) if tvr and tvr["change"] is not None else None,
               "tv_sector": tvr["sector"] if tvr else None,
               "tv_vol": tvr["volume"] if tvr else None,
               "is_dr": bool(tvr and tvr["type"] == "dr")}
        if not fresh:
            rec["drop"] = "stale"; rows.append(rec); continue
        if key in seen:
            old = seen[key]
            if suf(sym) < suf(old["sym"]):
                old["drop"] = "xlist-dup"; seen[key] = rec
            else:
                rec["drop"] = "xlist-dup"
            rows.append(rec); continue
        seen[key] = rec; rows.append(rec)
    results[side] = rows

# TV-only candidates (present in TV scan top rows but absent from Yahoo)
ysyms = {q["symbol"] for s in yh.values() for q in s}
ynames = {norm(q.get("longName") or q.get("shortName")) for s in yh.values() for q in s}
tvonly = {"gainers": [], "losers": []}
for k, res in tv.items():
    if not res: continue
    side = "gainers" if k.startswith("desc") else "losers"
    for x in res["data"][:40]:
        r = dict(zip(COLS, x["d"])); ex, base = x["s"].split(":")
        ysym = base.replace(".", "-") + SUF.get(ex, "")
        if ysym in ysyms or norm(r["description"]) in ynames: continue
        tvonly[side].append({"sym":ysym,"name":r["description"],"price":r["close"],"chg":round(r["change"],2),
                             "cap":r["market_cap_basic"],"vol":r["volume"],"avg":r["avg90"],
                             "vr": round(r["volume"]/(r["avg90"]*frac),1) if r["avg90"] else None,
                             "tv_sector":r["sector"],"is_dr":r["type"]=="dr","upd":r["update_mode"]})
results["tv_only"] = tvonly
json.dump(results, open(D+"_proc.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

for side in ["gainers","losers"]:
    kept = [r for r in results[side] if "drop" not in r]
    dropped = [r for r in results[side] if "drop" in r]
    print(f"\n== {side}: kept {len(kept)}, dropped {len(dropped)} ==")
    for r in dropped: print("  DROP", r["sym"], r["drop"], r["time"], r["chg"])
    for i, r in enumerate(kept[:34], 1):
        cap = r["cap"]/1e9 if r["cap"] else 0
        flag = " <<TVDIFF" if r["tv_chg"] is not None and abs(r["tv_chg"] - r["chg"]) > 2 else ""
        if r["tv_chg"] is None: flag += " <<NO-TV"
        print(f"  {i:2d} {r['sym']:10s} {str(r['name'])[:26]:26s} {r['price']:>8} {r['chg']:+6.2f} tv={r['tv_chg']} cap={cap:.2f}B vol={r['vol']} vr={r['vr']} {r['tv_sector']}{' DR' if r['is_dr'] else ''}{flag}")
    print(f"  -- TV-only {side}:")
    for r in tvonly[side][:15]:
        print(f"     {r['sym']:10s} {r['name'][:26]:26s} {r['price']:>8} {r['chg']:+6.2f} cap={(r['cap'] or 0)/1e9:.2f}B vol={r['vol']} vr={r['vr']} {r['tv_sector']}{' DR' if r['is_dr'] else ''} {r['upd']}")
