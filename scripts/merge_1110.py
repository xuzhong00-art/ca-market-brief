# -*- coding: utf-8 -*-
"""Merge _proc.json kept rows + TV DR rows (Yahoo quote) + TV-only checks -> _merged.json"""
import json, sys, datetime, urllib.request, urllib.parse, http.cookiejar
D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
TODAY = "2026-11-10"; FRAC = 0.077
proc = json.load(open(D+"_proc.json", encoding="utf-8"))
tv = json.load(open(D+"_tv_raw.json", encoding="utf-8"))
COLS = ["name","description","close","change","market_cap_basic","sector","volume","avg90","type","exchange","update_mode","time"]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [("User-Agent", UA), ("Accept", "*/*")]
try: op.open("https://fc.yahoo.com", timeout=30)
except Exception: pass
crumb = op.open("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=30).read().decode()
def quotes(syms):
    out = []
    for i in range(0, len(syms), 60):
        url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%s&crumb=%s" % (urllib.parse.quote(",".join(syms[i:i+60])), urllib.parse.quote(crumb))
        out += json.load(op.open(url, timeout=60))["quoteResponse"]["result"]
    return out
def day(t): return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d") if t else None

rows = {}
for side in ("gainers","losers"):
    for r in proc[side]:
        if "drop" in r: continue
        rows[r["sym"]] = dict(r, cdr=r.get("is_dr", False), tvsector=r.get("tv_sector"))

# DR rows from TV
dr = {}
for k in ("desc_dr","asc_dr"):
    for it in tv[k]["data"]:
        ex, t = it["s"].split(":"); d = dict(zip(COLS, it["d"]))
        if t not in dr or ex == "TSX": dr[t] = (ex, d)
drsyms = [s for t in dr for s in (t+".TO", t+".NE")]
# TV-only stock names to verify
extra = sys.argv[1:]
yq = {q["symbol"]: q for q in quotes(drsyms + extra)}
for t, (ex, d) in dr.items():
    cands = [yq.get(t+".TO"), yq.get(t+".NE")]
    cands = [c for c in cands if c and day(c.get("regularMarketTime")) == TODAY]
    best = next((c for c in cands if c.get("averageDailyVolume3Month")), cands[0] if cands else None)
    if not best: print("no fresh yahoo for DR", t, d["change"], file=sys.stderr); continue
    sym = best["symbol"]
    for s in (t+".TO", t+".NE"): rows.pop(s, None)
    vol = best.get("regularMarketVolume") or 0; avg = best.get("averageDailyVolume3Month") or 0
    rows[sym] = {"sym": sym, "name": d["description"], "price": best["regularMarketPrice"], "chg": best["regularMarketChangePercent"],
                 "cap": d["market_cap_basic"], "vol": vol, "avg": avg, "cdr": True, "tv_chg": d["change"], "tvsector": d["sector"]}
for s in extra:
    q = yq.get(s)
    if not q: print("extra missing", s, file=sys.stderr); continue
    print("EXTRA", s, q.get("shortName"), q.get("regularMarketPrice"), round(q.get("regularMarketChangePercent") or 0,2), "vol", q.get("regularMarketVolume"), "avg", q.get("averageDailyVolume3Month"), "cap", q.get("marketCap"), day(q.get("regularMarketTime")), file=sys.stderr)
    if day(q.get("regularMarketTime")) == TODAY and (q.get("marketCap") or 0) >= 2e8 and (q.get("regularMarketPrice") or 0) >= 2 and (q.get("regularMarketVolume") or 0) > 15000 and s not in rows:
        rows[s] = {"sym": s, "name": q.get("longName") or q.get("shortName"), "price": q["regularMarketPrice"], "chg": q["regularMarketChangePercent"],
                   "cap": q["marketCap"], "vol": q["regularMarketVolume"], "avg": q.get("averageDailyVolume3Month"), "cdr": False, "tvsector": None, "src": "extra"}
allr = list(rows.values())
g = sorted(allr, key=lambda x: -x["chg"])[:30]
l = sorted(allr, key=lambda x: x["chg"])[:30]
for name, lst in (("GAINERS", g), ("LOSERS", l)):
    print("==", name)
    for i, v in enumerate(lst, 1):
        v["vr"] = round(v["vol"]/(v["avg"]*FRAC), 1) if v.get("avg") else None
        print(i, v["sym"], str(v["name"])[:30], v["price"], round(v["chg"],2), "tv=%s" % v.get("tv_chg"), "%.2fB" % (v["cap"]/1e9), v.get("tvsector"), v["vol"], v["avg"], v["vr"], "CDR" if v["cdr"] else "")
json.dump({"g": g, "l": l}, open(D+"_merged.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
