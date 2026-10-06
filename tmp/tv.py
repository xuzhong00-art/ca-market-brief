import json, urllib.request
def scan(types, order):
    body={"filter":[{"left":"close","operation":"greater","right":2},{"left":"market_cap_basic","operation":"egreater","right":2e8},{"left":"volume","operation":"greater","right":15000},{"left":"type","operation":"in_range","right":types}],
      "options":{"lang":"en"},"markets":["canada"],
      "columns":["name","description","close","change","market_cap_basic","sector","industry","volume","average_volume_30d_calc","average_volume_90d_calc","type","exchange","update_mode","time"],
      "sort":{"sortBy":"change","sortOrder":order},"range":[0,70]}
    req=urllib.request.Request("https://scanner.tradingview.com/canada/scan",data=json.dumps(body).encode(),headers={"Content-Type":"application/json","User-Agent":"Mozilla/5.0","Origin":"https://www.tradingview.com","Referer":"https://www.tradingview.com/"})
    return json.load(urllib.request.urlopen(req,timeout=30))["data"]
out={}
for t in (["stock"],["dr"]):
    for o in ("desc","asc"):
        out[t[0]+"_"+o]=scan(t,o)
json.dump(out,open("tmp/tv.json","w"))
for k,v in out.items():
    print(k,len(v))
    for r in v[:3]: print("  ",r["s"],r["d"][:5],r["d"][7:10],r["d"][12:])
