# -*- coding: utf-8 -*-
"""Pull Yahoo screener gainers/losers + TV cross-check; dump raw JSON to tmp."""
import json, subprocess, sys, os, time
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
TMP = os.environ.get("LOCALAPPDATA", ".") + "/Temp"
JAR = TMP + "/yj.txt"
if os.path.exists(JAR): os.remove(JAR)

def curl(args):
    r = subprocess.run(["curl", "-s", "-c", JAR, "-b", JAR, "-A", UA] + args, capture_output=True, text=True, encoding="utf-8")
    return r.stdout

curl(["-L", "https://fc.yahoo.com", "-o", os.devnull])
crumb = curl(["https://query1.finance.yahoo.com/v1/test/getcrumb"]).strip()
print("crumb:", crumb, file=sys.stderr)

def screener(sort, size=80):
    body = {"size": size, "offset": 0, "sortField": "percentchange", "sortType": sort, "quoteType": "EQUITY",
            "query": {"operator": "AND", "operands": [
                {"operator": "eq", "operands": ["region", "ca"]},
                {"operator": "gte", "operands": ["intradayprice", 2]},
                {"operator": "gte", "operands": ["intradaymarketcap", 2e8]},
                {"operator": "gt", "operands": ["dayvolume", 15000]}]},
            "userId": "", "userIdType": "guid"}
    out = curl(["-X", "POST", "-H", "Content-Type: application/json", "-d", json.dumps(body),
                "https://query1.finance.yahoo.com/v1/finance/screener?crumb=" + crumb])
    j = json.loads(out)
    return j["finance"]["result"][0]["quotes"]

fields = ["symbol", "shortName", "longName", "regularMarketPrice", "regularMarketChangePercent", "regularMarketVolume",
          "averageDailyVolume3Month", "marketCap", "regularMarketTime", "exchange", "fullExchangeName", "sector", "industry", "marketState", "quoteType"]
def slim(q): return {k: q.get(k) for k in fields}
g = [slim(q) for q in screener("DESC")]
l = [slim(q) for q in screener("ASC")]

def tv(body, market="canada"):
    r = subprocess.run(["curl", "-s", "-X", "POST", "-H", "Content-Type: application/json", "-A", UA,
                        "-d", json.dumps(body), f"https://scanner.tradingview.com/{market}/scan"], capture_output=True, text=True, encoding="utf-8")
    return json.loads(r.stdout)["data"]

cols = ["name", "description", "close", "change", "market_cap_basic", "sector", "industry", "volume", "average_volume_30d_calc", "type", "exchange", "time"]
def tvbody(order, types, n=60):
    return {"filter": [{"left": "close", "operation": "greater", "right": 2},
                       {"left": "market_cap_basic", "operation": "egreater", "right": 2e8},
                       {"left": "volume", "operation": "greater", "right": 15000},
                       {"left": "type", "operation": "in_range", "right": types}],
            "options": {"lang": "en"}, "markets": ["canada"], "columns": cols,
            "sort": {"sortBy": "change", "sortOrder": order}, "range": [0, n]}
tvg = tv(tvbody("desc", ["stock"]))
tvl = tv(tvbody("asc", ["stock"]))
tvgd = tv(tvbody("desc", ["dr"], 30))
tvld = tv(tvbody("asc", ["dr"], 30))
def tvslim(rows): return [dict(zip(["ticker"] + cols, [r["s"]] + r["d"])) for r in rows]
json.dump({"crumb": crumb, "yg": g, "yl": l, "tvg": tvslim(tvg), "tvl": tvslim(tvl), "tvgd": tvslim(tvgd), "tvld": tvslim(tvld), "fetched": time.time()},
          open(TMP + "/ca_raw.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("yahoo", len(g), len(l), "tv", len(tvg), len(tvl), len(tvgd), len(tvld))
