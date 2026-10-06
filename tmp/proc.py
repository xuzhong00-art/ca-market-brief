import json, re, datetime
ws=r"C:\Users\Elliott\AppData\Local\hermes\cache\browser-use\workspace\06e2dfa6-d208-48ab-96b1-a485d91f3c66"
y=json.load(open(ws+r"\yahoo.json")); tv=json.load(open(ws+r"\tv.json"))
today=datetime.date(2026,10,6)
pri={'.TO':0,'.V':1,'.CN':2,'.NE':3}
def norm(n): return re.sub(r'\b(INC|CORP|CORPORATION|LTD|LIMITED|AND|&|THE|CO|PLC|TRUST|CLASS A|CL A)\b|[.,]','',(n or '').upper()).split()[:2]
def proc(rows):
    fresh=[]; stale=[]
    for r in rows:
        t=datetime.datetime.fromtimestamp(r['regularMarketTime'], datetime.timezone(datetime.timedelta(hours=-4))).date()
        (fresh if t==today else stale).append(r)
    seen={}
    for r in fresh:
        base=r['symbol'].rsplit('.',1)[0].replace('-','.'); suf='.'+r['symbol'].rsplit('.',1)[1]
        key=' '.join(norm(r['longName'] or r['shortName']))
        k=key or base
        if k not in seen or pri.get(suf,9)<pri.get('.'+seen[k]['symbol'].rsplit('.',1)[1],9): seen[k]=r
    return list(seen.values()), stale
tvall={}
for k,v in tv.items():
    for x in v: tvall.setdefault(x['name'].replace('.','-'),x)
for side,sort in [('G','DESC'),('L','ASC')]:
    rows,stale=proc(y[sort])
    print('==',side,'stale:',[(s['symbol'],s['regularMarketTime']) for s in stale])
    for i,r in enumerate(rows[:40],1):
        base=r['symbol'].rsplit('.',1)[0]
        t=tvall.get(base) or tvall.get(base.replace('-UN','.UN').replace('-','.'))
        vr=r['regularMarketVolume']/(r['averageDailyVolume3Month']*0.077) if r['averageDailyVolume3Month'] else None
        print(f"{i:2} {r['symbol']:10} {(r['longName'] or r['shortName'])[:28]:28} {r['regularMarketPrice']:>8} {r['regularMarketChangePercent']:+6.2f}% cap={r['marketCap']/1e6:7.0f}M vol={r['regularMarketVolume']:>8} avg={r['averageDailyVolume3Month']:>8} VR={vr and round(vr,1)} | TV={t and (round(t['change'],2), t['sector'], t['industry'])}")
print('== TV-only DR gainers:',[(x['name'],round(x['change'],1),x['desc']) for x in tv['dr_desc'][:12]])
print('== TV-only DR losers:',[(x['name'],round(x['change'],1),x['desc']) for x in tv['dr_asc'][:10]])
print('== TV stock top gainers:',[(x['name'],round(x['change'],1)) for x in tv['stock_desc'][:35]])
print('== TV stock top losers:',[(x['name'],round(x['change'],1)) for x in tv['stock_asc'][:35]])
