# -*- coding: utf-8 -*-
"""Yahoo v7 quotes for extra symbols + TV symbol lookup. Usage: python scripts/extra.py SYM1,SYM2 TV:TICK1,TV:TICK2"""
import json, sys, urllib.request, urllib.parse, http.cookiejar
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [("User-Agent", UA), ("Accept", "*/*")]
try: op.open("https://fc.yahoo.com", timeout=30)
except Exception: pass
crumb = op.open("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=30).read().decode()
syms = sys.argv[1]
url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%s&crumb=%s" % (urllib.parse.quote(syms), urllib.parse.quote(crumb))
d = json.load(op.open(url, timeout=60))
import datetime
for q in d["quoteResponse"]["result"]:
    t = q.get("regularMarketTime"); dt = datetime.datetime.fromtimestamp(t) if t else None
    print(q["symbol"], q.get("longName") or q.get("shortName"), q.get("regularMarketPrice"), round(q.get("regularMarketChangePercent") or 0,2),
          "vol", q.get("regularMarketVolume"), "avg", q.get("averageDailyVolume3Month"), "cap", q.get("marketCap"), dt)
if len(sys.argv) > 2:
    tickers = sys.argv[2].split(",")
    body = {"symbols":{"tickers":tickers},"columns":["name","description","close","change","volume","average_volume_90d_calc","market_cap_basic","sector","industry","update_mode","type"]}
    req = urllib.request.Request("https://scanner.tradingview.com/canada/scan", data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type":"application/json","User-Agent":UA,"Origin":"https://www.tradingview.com"})
    for x in json.load(urllib.request.urlopen(req, timeout=60))["data"]:
        print("TV", x["s"], x["d"])
