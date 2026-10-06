import json, urllib.request, http.cookiejar, time
cj=http.cookiejar.CookieJar(); op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36","Accept":"*/*"}
try: op.open(urllib.request.Request("https://fc.yahoo.com",headers=UA),timeout=20)
except Exception as e: pass
crumb=op.open(urllib.request.Request("https://query1.finance.yahoo.com/v1/test/getcrumb",headers=UA),timeout=20).read().decode()
print("crumb",crumb)
def scr(order):
    body={"size":80,"offset":0,"sortField":"percentchange","sortType":order,"quoteType":"EQUITY",
      "query":{"operator":"AND","operands":[{"operator":"eq","operands":["region","ca"]},{"operator":"gte","operands":["intradayprice",2]},{"operator":"gte","operands":["intradaymarketcap",2e8]},{"operator":"gt","operands":["dayvolume",15000]}]},"userId":"","userIdType":"guid"}
    req=urllib.request.Request("https://query1.finance.yahoo.com/v1/finance/screener?crumb="+crumb,data=json.dumps(body).encode(),headers={**UA,"Content-Type":"application/json"})
    return json.load(op.open(req,timeout=30))["finance"]["result"][0]["quotes"]
out={}
for o in ("DESC","ASC"):
    out[o]=[{k:x.get(k) for k in ['symbol','shortName','longName','regularMarketPrice','regularMarketChangePercent','regularMarketVolume','averageDailyVolume3Month','marketCap','regularMarketTime','exchange','marketState']} for x in scr(o)]
    print(o,len(out[o]))
json.dump(out,open("tmp/yh.json","w"))
for r in out["DESC"][:4]+out["ASC"][:4]: print(r)
