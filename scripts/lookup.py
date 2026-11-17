# -*- coding: utf-8 -*-
import json, subprocess, os, sys
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
TMP = os.environ.get("LOCALAPPDATA", ".") + "/Temp"
raw = json.load(open(TMP + "/ca_raw.json", encoding="utf-8")); crumb = raw["crumb"]
tvt = sys.argv[1].split(",")
ysyms = sys.argv[2].split(",") if len(sys.argv) > 2 else []
body = {"symbols": {"tickers": tvt}, "columns": ["name","description","close","change","market_cap_basic","volume","average_volume_30d_calc","type","sector","industry","time","Perf.1M"]}
r = subprocess.run(["curl","-s","-X","POST","-H","Content-Type: application/json","-A",UA,"-d",json.dumps(body),"https://scanner.tradingview.com/canada/scan"],capture_output=True,text=True,encoding="utf-8")
for it in json.loads(r.stdout)["data"]:
    print("TV", it["s"], it["d"])
if ysyms:
    r = subprocess.run(["curl","-s","-c",TMP+"/yj.txt","-b",TMP+"/yj.txt","-A",UA,"https://query1.finance.yahoo.com/v7/finance/quote?symbols="+",".join(ysyms)+"&crumb="+crumb],capture_output=True,text=True,encoding="utf-8")
    import datetime
    for q in json.loads(r.stdout)["quoteResponse"]["result"]:
        t=q.get("regularMarketTime"); print("YH", q["symbol"], q.get("longName"), q.get("regularMarketPrice"), round(q.get("regularMarketChangePercent") or 0,2), "vol",q.get("regularMarketVolume"),"avg",q.get("averageDailyVolume3Month"),"cap",q.get("marketCap"), datetime.datetime.fromtimestamp(t).strftime("%m-%d %H:%M") if t else None)
