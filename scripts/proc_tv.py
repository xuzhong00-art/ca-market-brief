#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""tv_raw.json -> top30 gainers/losers, exchange-priority dedupe, full-day VR."""
import json, re
from datetime import datetime, timezone, timedelta

raw = json.load(open("tv_raw.json", encoding="utf-8"))
ET = timezone(timedelta(hours=-4))
today = datetime.now(ET).strftime("%Y-%m-%d")

COLS = ["name","description","close","change","market_cap_basic","sector","volume","avg90","type","exchange","update_mode","time"]
EX_PRI = {"TSX": 0, "TSXV": 1, "CSE": 2, "NEO": 3}
SUF = {"TSX": ".TO", "TSXV": ".V", "CSE": ".CN", "NEO": ".NE"}

def norm_name(desc):
    s = re.sub(r"[^A-Za-z0-9 ]", " ", desc.upper())
    for w in ("INCORPORATION","CORPORATION","UNSPONSORED","DEPOSITORY","RECEIPT","CANADIAN","INC","CORP","LTD","LIMITED","AND","THE","CO","PLC","GROUP","HOLDINGS","CDR","CAD","HEDGED","SHS","CLASS","A","B"):
        s = re.sub(rf"\b{w}\b", " ", s)
    return " ".join(s.split())

def collect(order):
    best = {}
    for t in ("stock", "dr"):
        blob = raw.get(f"{order}_{t}")
        if not blob: continue
        for item in blob["data"]:
            d = dict(zip(COLS, item["d"]))
            ex, sym = item["s"].split(":")
            d["ex"], d["sym"] = ex, sym
            d["is_dr"] = (t == "dr")
            bd = datetime.fromtimestamp(d["time"], ET).strftime("%Y-%m-%d") if d.get("time") else None
            if bd != today:
                continue
            key = norm_name(d["description"])
            if key not in best or EX_PRI.get(ex, 9) < EX_PRI.get(best[key]["ex"], 9):
                best[key] = d
    rows = sorted(best.values(), key=lambda d: d["change"] or 0, reverse=(order == "desc"))
    return rows[:30]

out = {}
for order in ("desc", "asc"):
    rows = collect(order)
    lst = []
    for d in rows:
        vr = round(d["volume"] / d["avg90"], 1) if d["avg90"] else None
        cap = d["market_cap_basic"]
        caps = f"{cap/1e9:.1f}B" if cap and cap >= 1e9 else (f"{cap/1e6:.0f}M" if cap else "?")
        lst.append({
            "code": d["sym"] + SUF.get(d["ex"], ""), "name": d["description"],
            "price": f"{d['close']:.2f}", "chg": f"{'+' if d['change']>=0 else ''}{d['change']:.2f}%",
            "cap": caps, "sector": d["sector"], "vr": vr, "dr": d["is_dr"],
            "vol": d["volume"], "avg90": d["avg90"],
        })
    out[order] = lst

json.dump(out, open("movers30.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for order, label in (("desc","GAINERS"),("asc","LOSERS")):
    print(f"=== {label} ===")
    for i, d in enumerate(out[order], 1):
        print(f"{i:2d} {d['code']:10s} {d['name'][:34]:34s} {d['price']:>8s} {d['chg']:>8s} {d['cap']:>7s} {str(d['sector'])[:24]:24s} vr={d['vr']}{' DR' if d['dr'] else ''}")
