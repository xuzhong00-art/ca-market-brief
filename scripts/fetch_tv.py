# -*- coding: utf-8 -*-
"""Fetch TSX/TSXV/CSE/NEO movers from TradingView scanner (stock + dr), save raw json."""
import json, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
cols = ["name","description","close","change","market_cap_basic","sector","volume",
        "average_volume_90d_calc","exchange","type","update_mode","industry"]

def scan(typ, order, n=70):
    body = {"filter":[{"left":"close","operation":"greater","right":2},
                      {"left":"market_cap_basic","operation":"egreater","right":200000000},
                      {"left":"volume","operation":"greater","right":15000},
                      {"left":"type","operation":"in_range","right":[typ]}],
            "options":{"lang":"en"},"markets":["canada"],"columns":cols,
            "sort":{"sortBy":"change","sortOrder":order},"range":[0,n]}
    req = urllib.request.Request("https://scanner.tradingview.com/canada/scan",
        data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type":"application/json","User-Agent":UA,
                 "Origin":"https://www.tradingview.com","Referer":"https://www.tradingview.com/"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    return [{"s":x["s"], **dict(zip(cols,x["d"]))} for x in d["data"]]

out = {}
for typ in ["stock","dr"]:
    for order in ["desc","asc"]:
        out[f"{typ}_{order}"] = scan(typ, order)
        print(typ, order, len(out[f"{typ}_{order}"]))

with open("C:/Users/Elliott/Downloads/claude/ca-market-brief/data/_tv_raw.json","w",encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("saved")
