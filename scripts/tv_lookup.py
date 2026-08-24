# -*- coding: utf-8 -*-
"""TV symbol lookup for tickers missing in scan results."""
import json, urllib.request
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
tickers = ["TSXV:LGC","TSXV:TTS","TSX:VGC","TSX:BBD.B","TSX:DC.A","TSX:HPS.A","TSX:DFN","TSX:DF","TSX:BK","TSX:ACX","TSX:MRE","TSX:CF.PR.A","TSXV:GORO","TSX:CADY","TSX:VMET"]
body = {"symbols":{"tickers":tickers},
        "columns":["name","description","close","change","volume","market_cap_basic","sector","industry","update_mode"]}
req = urllib.request.Request("https://scanner.tradingview.com/canada/scan",
    data=json.dumps(body).encode(), method="POST",
    headers={"Content-Type":"application/json","User-Agent":UA,"Origin":"https://www.tradingview.com"})
with urllib.request.urlopen(req, timeout=60) as r:
    d = json.load(r)
for x in d["data"]:
    print(x["s"], x["d"])
