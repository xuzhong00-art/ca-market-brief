# -*- coding: utf-8 -*-
"""Build data/2026-11-03.json from _proc.json (live 07:35 PT, ~35 min after open, FRAC=0.09)."""
import json, sys

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
proc = json.load(open(D + "_proc.json", encoding="utf-8"))
tv = json.load(open(D + "_tv_raw.json", encoding="utf-8"))
meta_all = json.load(open(D + "_meta_all.json", encoding="utf-8"))
FRAC = 0.09

COLS = ["name","description","close","change","market_cap_basic","sector","volume","avg90","type","exchange","update_mode","time"]
tvcap = {}
for blob in tv.values():
    if not blob: continue
    for it in blob["data"]:
        d = dict(zip(COLS, it["d"])); sym = it["s"].split(":")[1]
        if d["type"] == "dr" and d["market_cap_basic"]: tvcap[sym] = d["market_cap_basic"]

EXCLUDE = {"QTRH.TO"}  # vol 8.4K < 15K

META = {
 "ORAC.NE":("Oracle（CDR）","企业软件/云·CDR"),"PZA.TO":("Pizza Pizza Royalty","餐饮权利金"),
 "TA.TO":("TransAlta","电力/公用事业"),"ECU.V":("Element 29 Resources","铜矿勘探(秘鲁)"),
 "TIH.TO":("Toromont Industries","卡特彼勒经销"),"NVDA.TO":("NVIDIA（CDR）","AI芯片·CDR"),
 "ARE.TO":("Aecon Group","工程建筑"),"GEI.TO":("Gibson Energy","油气中游"),
 "WJX.TO":("Wajax","工业设备经销"),"TPZ.TO":("Topaz Energy","油气权利金"),
 "VZLA.TO":("Vizsla Silver","银矿开发(墨西哥)"),"TKO.TO":("Trekor Metals","铜金矿"),
 "KNT.TO":("K92 Mining","金矿(巴新)"),"OGC.TO":("OceanaGold","黄金生产"),
 "ASM.TO":("Avino Silver & Gold","银金矿(墨西哥)"),"CURA.TO":("Curaleaf","大麻(美国MSO)"),
 "BRVO.V":("Bravo Mining","铂族/铜矿勘探"),"CNL.TO":("Collective Mining","金铜勘探(哥伦比亚)"),
 "HPS-A.TO":("Hammond Power Solutions","电力设备"),"EDR.TO":("Endeavour Silver","银矿生产(墨西哥)"),"MG.TO":("Magna International","汽车零部件"),
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

NARR = json.load(open(D + "_narr_1103.json", encoding="utf-8"))
data = {
 "date": "2026-11-03", "weekday": "周二",
 "snapshot": "2026-11-03 10:05 ET 盘中（开盘约 35 分钟；本期因北美 11-01 已结束夏令时、排程未随之调整，抓数时间较平日晚 30 分钟）",
 "market_state": "REGULAR",
 "vr_note": "量比 = 当日成交量 ÷ (3个月日均量 × 0.09)，0.09 为快照时已开盘时长占比（~35min / 6.5h），早盘量比波动大，仅供参考。CDR 行用 Yahoo .TO/.NE 挂牌 3 个月均量，基数小易放大。⚠️≥3，🔥≥8。",
 "gainers": G, "losers": L,
 "table_notes": NARR["table_notes"],
 "sectors_html": NARR["sectors_html"],
 "anomalies_html": NARR["anomalies_html"],
 "digest": NARR["digest"],
}
json.dump(data, open(D + "2026-11-03.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in G: print(r)
print("---")
for r in L: print(r)
