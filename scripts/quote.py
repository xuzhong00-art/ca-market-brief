# -*- coding: utf-8 -*-
"""Yahoo v7 quote for given symbols (cookie+crumb)."""
import json, sys, urllib.request, urllib.parse, http.cookiejar
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [("User-Agent", UA), ("Accept", "*/*")]
try: op.open("https://fc.yahoo.com", timeout=30)
except Exception: pass
crumb = op.open("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=30).read().decode()
syms = ",".join(sys.argv[1:])
url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%s&crumb=%s" % (urllib.parse.quote(syms), urllib.parse.quote(crumb))
d = json.load(op.open(url, timeout=60))
import datetime
for q in d["quoteResponse"]["result"]:
    t = q.get("regularMarketTime"); dt = datetime.datetime.fromtimestamp(t) if t else None
    print(q["symbol"], q.get("shortName"), q.get("regularMarketPrice"), round(q.get("regularMarketChangePercent") or 0,2),
          "vol", q.get("regularMarketVolume"), "avg", q.get("averageDailyVolume3Month"), "cap", q.get("marketCap"), dt)
