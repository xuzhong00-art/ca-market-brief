import json, re, datetime
yh=json.load(open("tmp/yh.json")); tv=json.load(open("tmp/tv.json"))
today=datetime.date(2026,10,2)
def norm(n): return re.sub(r'\b(INC|CORP|CORPORATION|LTD|LIMITED|AND|&|CLASS A|THE|CO)\b|[.,]','',(n or '').upper()).split()
def key(n): return " ".join(norm(n)[:2])
pri={'.TO':0,'.V':1,'.CN':2,'.NE':3}
# TV lookup: by base ticker -> best row (prefer TSX, dedupe)
tvmap={}
for k,rows in tv.items():
    for r in rows:
        ex,t=r['s'].split(':'); d=r['d']
        rec=dict(ex=ex,t=t,name=d[1],close=d[2],chg=d[3],cap=d[4],sector=d[5],ind=d[6],vol=d[7],avg30=d[8],avg90=d[9],type=d[10],time=d[13])
        if t not in tvmap or (ex in('TSX',) and tvmap[t]['ex']!='TSX'): tvmap[t]=rec
def proc(rows):
    seen={}; out=[]
    rows=sorted(rows,key=lambda r:pri.get(re.search(r'\.\w+$',r['symbol']).group(),9))
    for r in rows:
        ts=datetime.datetime.fromtimestamp(r['regularMarketTime'],datetime.timezone(datetime.timedelta(hours=-4))).date()
        if ts!=today: print("STALE",r['symbol'],ts); continue
        k=key(r['longName'] or r['shortName'])
        if k in seen: continue
        seen[k]=1; out.append(r)
    out.sort(key=lambda r:-r['regularMarketChangePercent'])
    return out
res={}
for o,name in (("DESC","gainers"),("ASC","losers")):
    rows=proc(yh[o]); rows=rows if o=="DESC" else rows[::-1]
    lst=[]
    for r in rows[:36]:
        base=r['symbol'].rsplit('.',1)[0].replace('-','.')
        t=tvmap.get(base) or tvmap.get(base.replace('.','-'))
        vr=r['regularMarketVolume']/r['averageDailyVolume3Month'] if r['averageDailyVolume3Month'] else None
        lst.append(dict(sym=r['symbol'],name=r['longName'] or r['shortName'],price=r['regularMarketPrice'],chg=round(r['regularMarketChangePercent'],2),cap=r['marketCap'],vol=r['regularMarketVolume'],avg=r['averageDailyVolume3Month'],vr=round(vr,1) if vr else None,
                        tv=(dict(chg=round(t['chg'],2),sector=t['sector'],ind=t['ind'],type=t['type'],cap=t['cap'],vol=t['vol'],avg90=t['avg90']) if t else None)))
    res[name]=lst
json.dump(res,open("tmp/merged.json","w"),ensure_ascii=False,indent=0)
for name in res:
    print("==",name)
    for i,x in enumerate(res[name],1):
        t=x['tv']; print(i,x['sym'],x['name'][:28],x['price'],x['chg'],t and t['chg'],x['cap']//1e6 if x['cap'] else None,'M','vr',x['vr'],t and t['type'],t and t['ind'],sep='|')
