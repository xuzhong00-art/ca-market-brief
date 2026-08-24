# -*- coding: utf-8 -*-
"""Yahoo screener via cookie+crumb over plain HTTP."""
import json, urllib.request, http.cookiejar

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [("User-Agent", UA), ("Accept", "*/*")]

# seed cookie
try:
    op.open("https://fc.yahoo.com", timeout=30)
except Exception as e:
    print("fc:", e)
crumb = op.open("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=30).read().decode()
print("crumb:", repr(crumb))

def screener(sort):
    body = {"size":60,"offset":0,"sortField":"percentchange","sortType":sort,"quoteType":"EQUITY",
      "query":{"operator":"AND","operands":[
        {"operator":"eq","operands":["region","ca"]},
        {"operator":"gte","operands":["intradayprice",2]},
        {"operator":"gte","operands":["intradaymarketcap",200000000]},
        {"operator":"gt","operands":["dayvolume",15000]}]},
      "userId":"","userIdType":"guid"}
    req = urllib.request.Request(
        "https://query1.finance.yahoo.com/v1/finance/screener?crumb=" + urllib.parse.quote(crumb),
        data=json.dumps(body).encode(), method="POST")
    req.add_header("Content-Type","application/json")
    with op.open(req, timeout=60) as r:
        return json.load(r)["finance"]["result"][0]["quotes"]

import urllib.parse
fields = ["symbol","shortName","longName","regularMarketPrice","regularMarketChangePercent",
          "regularMarketVolume","averageDailyVolume3Month","marketCap","regularMarketTime",
          "exchange","fullExchangeName","quoteType"]
out = {}
for name, sort in [("gainers","DESC"),("losers","ASC")]:
    qs = screener(sort)
    out[name] = [{k:q.get(k) for k in fields} for q in qs]
    print(name, len(qs))
with open("C:/Users/Elliott/Downloads/claude/ca-market-brief/data/_yh_raw.json","w",encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("saved")
