# -*- coding: utf-8 -*-
"""Build data/2026-11-04.json from _proc.json (backfill run after close, FRAC=1.0)."""
import json, sys

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
proc = json.load(open(D + "_proc.json", encoding="utf-8"))
tv = json.load(open(D + "_tv_raw.json", encoding="utf-8"))
meta_all = json.load(open(D + "_meta_all.json", encoding="utf-8"))
FRAC = 1.0

COLS = ["name","description","close","change","market_cap_basic","sector","volume","avg90","type","exchange","update_mode","time"]
tvcap = {}
for blob in tv.values():
    if not blob: continue
    for it in blob["data"]:
        d = dict(zip(COLS, it["d"])); sym = it["s"].split(":")[1]
        if d["type"] == "dr" and d["market_cap_basic"]: tvcap[sym] = d["market_cap_basic"]

EXCLUDE = {"CVS.NE", "GEV.NE"}  # replaced by .TO listings below (fuller data)

# TV-only / .TO CDR rows from Yahoo v7 quote (sym, name, price, chg, vol, avg3m, is_dr)
INJECT_LOSERS = [
 ("VRT.TO", "Vertiv Holdings Co", 15.23, -12.82, 386679, 113409),
 ("CRWV.TO", "CoreWeave, Inc.", 9.11, -9.89, 671333, 310722),
 ("DELL.TO", "Dell Technologies Inc.", 15.80, -9.09, 17419, 9281),
 ("CVS.TO", "CVS Health Corporation", 19.09, -12.39, 96815, 14342),
 ("GEV.TO", "GE Vernova Inc.", 55.83, -9.10, 196420, 44303),
]

META = {
 "MTA.V":("Metalla Royalty","贵金属权利金"),"DB.V":("Decibel Cannabis","大麻"),
 "SICO.V":("Silverco Mining","银矿勘探"),"FFH.TO":("Fairfax Financial","财险/保险投资"),
 "PHX.TO":("PHX Energy Services","油服定向钻井"),"ALDE.V":("Aldebaran Resources","铜金勘探(阿根廷)"),
 "CVS.TO":("CVS Health（CDR）","药房/医保·CDR"),"SPB.TO":("Superior Plus","丙烷分销"),
 "GEV.TO":("GE Vernova（CDR）","燃气轮机/电网·CDR"),"VLE.TO":("Valeura Energy","油气生产(泰国)"),
 "DELL.TO":("Dell（CDR）","服务器/PC·CDR"),"HSTR.TO":("Heliostar Metals","金矿(墨西哥)"),
 "BZ.V":("Benz Mining","黄金勘探(澳洲)"),"HHH.V":("Helius Minerals","矿业勘探"),
 "HMM-A.TO":("Hammond Manufacturing","电气外壳制造"),"PRL.TO":("Propel Holdings","金融科技消费贷"),
 "GRGD.TO":("Groupe Dynamite","服装零售"),"ARA.TO":("Aclara Resources","稀土"),
 "UCU.V":("Ucore Rare Metals","稀土"),"EFX.TO":("Enerflex","油气设备"),
 "MOON.V":("Blue Moon Metals","铜锌矿"),"EFN.TO":("Element Fleet Management","车队管理"),
 "HPS-A.TO":("Hammond Power Solutions","电力设备/变压器"),"CLS.TO":("Celestica","电子制造/AI服务器"),
 "ZVST.NE":("Vistra（CDR）","电力·CDR"),"HUT.TO":("Hut 8","比特币矿机/算力"),
 "FTG.TO":("Firan Technology","航空电子"),"VRT.TO":("Vertiv（CDR）","数据中心电力/散热·CDR"),
 "CRWV.TO":("CoreWeave（CDR）","AI算力云·CDR"),
 "WPM.TO":("Wheaton Precious Metals","贵金属流媒体"),"ASM.TO":("Avino Silver & Gold","银金矿(墨西哥)"),
 "ARTG.V":("Artemis Gold","黄金生产(BC Blackwater)"),"EDR.TO":("Endeavour Silver","银矿生产(墨西哥)"),
}
META = {**meta_all, **META}

def cap_s(c):
    if not c: return "–"
    return f"{c/1e9:.1f}B" if c >= 1e9 else f"{c/1e6:.0f}M"

def vr(vol, avg):
    return round(vol/(avg*FRAC), 1) if avg else None

def build(side, desc):
    rows = []
    for r in proc[side]:
        if "drop" in r or r["sym"] in EXCLUDE or r["vol"] < 15000: continue
        cap = tvcap.get(r["sym"].split(".")[0], r["cap"]) if r.get("is_dr") else r["cap"]
        rows.append(dict(r, cap=cap, vr=vr(r["vol"], r["avg"])))
    if side == "losers":
        for sym, name, price, chg, vol, avg in INJECT_LOSERS:
            rows.append({"sym":sym,"name":name,"price":price,"chg":chg,"cap":tvcap.get(sym.split(".")[0]),
                         "vol":vol,"avg":avg,"vr":vr(vol,avg),"tv_sector":None})
    rows.sort(key=lambda r: r["chg"], reverse=desc)
    out = []
    for i, r in enumerate(rows[:30], 1):
        name, sec = META.get(r["sym"], (str(r["name"])[:22], r.get("tv_sector") or "–"))
        if r["sym"] not in META: print("NO META:", r["sym"], r["name"])
        out.append([i, r["sym"], name, f"{r['price']:.2f}", f"{r['chg']:+.2f}%", cap_s(r["cap"]), sec, r["vr"]])
    print(side, "31-34:", [(r["sym"], r["chg"], r["vr"]) for r in rows[30:34]])
    return out

G, L = build("gainers", True), build("losers", False)
if len(sys.argv) > 1 and sys.argv[1] == "preview":
    for r in G: print(r)
    print("---")
    for r in L: print(r)
    sys.exit()

NARR = json.load(open(D + "_narr_1104.json", encoding="utf-8"))
data = {
 "date": "2026-11-04", "weekday": "周三",
 "snapshot": "2026-11-04 16:00 ET 收盘（本期为补跑：早上排程未执行，于当日晚间按收盘数据补生成）",
 "market_state": "CLOSED",
 "vr_note": "量比 = 当日全天成交量 ÷ 3个月日均量（收盘后补跑，开盘时长占比取 1.0）。CDR 行用 Yahoo .TO 挂牌 3 个月均量，基数小易放大。⚠️≥3，🔥≥8。",
 "gainers": G, "losers": L,
 "table_notes": NARR["table_notes"],
 "sectors_html": NARR["sectors_html"],
 "anomalies_html": NARR["anomalies_html"],
 "digest": NARR["digest"],
}
json.dump(data, open(D + "2026-11-04.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in G: print(r)
print("---")
for r in L: print(r)
