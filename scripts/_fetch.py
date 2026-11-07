# -*- coding: utf-8 -*-
import json, urllib.request, http.cookiejar, sys, time
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [("User-Agent", UA)]
try:
    op.open("https://fc.yahoo.com", timeout=20)
except Exception:
    pass
crumb = op.open("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=20).read().decode()
print("crumb", crumb, file=sys.stderr)

def screener(sort):
    body = {"size": 80, "offset": 0, "sortField": "percentchange", "sortType": sort, "quoteType": "EQUITY",
            "query": {"operator": "AND", "operands": [
                {"operator": "eq", "operands": ["region", "ca"]},
                {"operator": "gte", "operands": ["intradayprice", 2]},
                {"operator": "gte", "operands": ["intradaymarketcap", 2e8]},
                {"operator": "gt", "operands": ["dayvolume", 15000]}]},
            "userId": "", "userIdType": "guid"}
    req = urllib.request.Request("https://query1.finance.yahoo.com/v1/finance/screener?crumb=" + urllib.parse.quote(crumb),
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(op.open(req, timeout=30))["finance"]["result"][0]["quotes"]

def quotes(syms):
    out = []
    for i in range(0, len(syms), 50):
        url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%s&crumb=%s" % (",".join(syms[i:i+50]), urllib.parse.quote(crumb))
        out += json.load(op.open(url, timeout=30))["quoteResponse"]["result"]
    return out

def tv(body, market="canada"):
    req = urllib.request.Request("https://scanner.tradingview.com/%s/scan" % market, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "User-Agent": UA})
    return json.load(op.open(req, timeout=30))

if __name__ == "__main__":
    import urllib.parse
    g = screener("DESC"); l = screener("ASC")
    keys = ["symbol", "shortName", "longName", "regularMarketPrice", "regularMarketChangePercent", "regularMarketVolume",
            "averageDailyVolume3Month", "marketCap", "regularMarketTime", "exchange", "sector", "industry", "fullExchangeName"]
    slim = lambda qs: [{k: q.get(k) for k in keys} for q in qs]
    cols = ["name", "description", "close", "change", "market_cap_basic", "sector", "industry", "volume", "average_volume_30d_calc", "type", "exchange", "time", "update_mode"]
    filt = [{"left": "close", "operation": "greater", "right": 2}, {"left": "market_cap_basic", "operation": "egreater", "right": 2e8},
            {"left": "volume", "operation": "greater", "right": 15000}]
    tvres = {}
    for typ in ("stock", "dr"):
        for order in ("desc", "asc"):
            b = {"filter": filt + [{"left": "type", "operation": "in_range", "right": [typ]}], "options": {"lang": "en"}, "markets": ["canada"],
                 "columns": cols, "sort": {"sortBy": "change", "sortOrder": order}, "range": [0, 60]}
            tvres[typ + "_" + order] = tv(b)["data"]
    json.dump({"yg": slim(g), "yl": slim(l), "tv": tvres}, open("data/_raw.json", "w"), indent=1)
    print("done", len(g), len(l), {k: len(v) for k, v in tvres.items()})
