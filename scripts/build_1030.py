# -*- coding: utf-8 -*-
"""Build data/2026-10-30.json from _proc.json + CDR additions + meta (live 7:00 PT, FRAC=0.077)."""
import json, sys

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
proc = json.load(open(D + "_proc.json", encoding="utf-8"))
tv = json.load(open(D + "_tv_raw.json", encoding="utf-8"))
FRAC = 0.077

COLS = ["name","description","close","change","market_cap_basic","sector","volume","avg90","type","exchange","update_mode","time"]
tvcap = {}
for blob in tv.values():
    if not blob: continue
    for it in blob["data"]:
        d = dict(zip(COLS, it["d"])); sym = it["s"].split(":")[1]
        if d["type"] == "dr" and d["market_cap_basic"]: tvcap[sym] = d["market_cap_basic"]

TO_OVERRIDE = {}
# TV-only additions (Yahoo v7 quote 07:00 PT): sym, name, price, chg, cap(None->TV), vol, avg3m
TV_ADD = {
 "gainers": [
  ("LLY.TO", "Eli Lilly（CDR）", 50.79, 3.88, None, 65524, 76712),
  ("INTU.TO", "Intuit（CDR）", 20.78, 3.75, None, 42502, 62059),
  ("ADBE.TO", "Adobe（CDR）", 9.72, 2.97, None, 43498, 102322),
  ("XOM.TO", "Exxon Mobil（CDR）", 33.67, 2.75, None, 16351, 27545),
  ("WMT.TO", "Walmart（CDR）", 51.40, 1.98, None, 25265, 120488),
  ("NKE.TO", "NIKE（CDR）", 6.94, 1.46, None, 37200, 262516),
  ("PFE.TO", "Pfizer（CDR）", 13.48, 1.43, None, 19792, 119159),
 ],
 "losers": [
  ("INTC.TO", "Intel（CDR）", 36.60, -28.93, None, 611121, 310296),
  ("RDDT.TO", "Reddit（CDR）", 9.40, -24.01, None, 269255, 129103),
  ("MSTR.TO", "Strategy（CDR）", 8.76, -8.84, None, 383838, 470669),
  ("QCOM.TO", "Qualcomm（CDR）", 22.01, -8.02, None, 34985, 84461),
  ("HOOD.TO", "Robinhood（CDR）", 13.73, -7.91, None, 60539, 172651),
  ("SNDK.TO", "SanDisk（CDR）", 29.71, -7.76, None, 441770, 1015238),
  ("CRWV.TO", "CoreWeave（CDR）", 10.58, -7.19, None, 219665, 300758),
  ("ANET.TO", "Arista Networks（CDR）", 30.75, -6.68, None, 21974, 27161),
  ("APPS.TO", "AppLovin（CDR）", 7.51, -6.24, None, 45907, 141301),
  ("MRV.TO", "Marvell（CDR）", 33.08, -6.22, None, 449523, 170401),
 ],
}
EXCLUDE = {"CBRS.TO", "BE.TO"}  # CBRS 成交 4.9K 不足 15K 且为负涨幅混入涨幅榜; BE -3.87% 未入榜

META = {
 # gainers
 "BDI.TO":("Black Diamond Group","模块化空间租赁"),"MX.TO":("Methanex","甲醇化工"),
 "X.TO":("TMX Group","交易所运营"),"LLY.TO":("Eli Lilly（CDR）","制药/GLP-1·CDR"),
 "INTU.TO":("Intuit（CDR）","财税软件·CDR"),"TRI.TO":("Thomson Reuters","信息服务"),
 "ADBE.TO":("Adobe（CDR）","创意软件·CDR"),"XOM.TO":("Exxon Mobil（CDR）","综合油气·CDR"),
 "CVO.TO":("Coveo Solutions","AI搜索软件"),"SDE.TO":("Spartan Delta","油气勘探开发"),
 "RCI-B.TO":("Rogers Communications","电信"),"WMT.TO":("Walmart（CDR）","零售·CDR"),
 "COST.TO":("Costco（CDR）","仓储零售·CDR"),"SCR.TO":("Strathcona Resources","油气勘探开发"),
 "SU.TO":("Suncor Energy","综合油气/油砂"),"VET.TO":("Vermilion Energy","国际油气"),
 "T.TO":("TELUS","电信"),"NKE.TO":("NIKE（CDR）","运动服饰·CDR"),
 "PFE.TO":("Pfizer（CDR）","制药·CDR"),"CVE.TO":("Cenovus Energy","综合油气/油砂"),
 "MKP.TO":("MCAN Mortgage","按揭投资公司"),"MFI.TO":("Maple Leaf Foods","食品加工"),
 "CNQ.TO":("Canadian Natural Resources","综合油气/油砂"),"QBR-B.TO":("Quebecor","电信/媒体"),
 "DXT.TO":("Dexterra Group","设施管理/营地服务"),"PEY.TO":("Peyto Exploration","天然气"),
 "KEY.TO":("Keyera","中游管道/NGL"),"SAP.TO":("Saputo","乳制品"),
 "AAV.TO":("Advantage Energy","天然气"),"KEL.TO":("Kelt Exploration","油气勘探开发"),
 "ACO-X.TO":("ATCO","公用事业/结构物流"),"OVV.TO":("Ovintiv","油气勘探开发"),
 "GIB-A.TO":("CGI","IT服务"),"IMO.TO":("Imperial Oil","综合油气"),
 "APTX.TO":("Apotex Health","仿制药"),"BCE.TO":("BCE","电信"),"L.TO":("Loblaw","食品零售"),
 "FSZ.TO":("Fiera Capital","资产管理"),"CP.TO":("CPKC","铁路"),
 # losers
 "INTC.TO":("Intel（CDR）","半导体·CDR"),"RDDT.TO":("Reddit（CDR）","社交媒体·CDR"),
 "TFII.TO":("TFI International","货运物流"),"CCO.TO":("Cameco","铀矿"),
 "ECOR.TO":("Ecora Resources","矿业权利金"),"MSTR.TO":("Strategy（CDR）","比特币财库·CDR"),
 "AMD.TO":("AMD（CDR）","半导体·CDR"),"HUT.TO":("Hut 8","比特币矿机/算力"),
 "ABRA.TO":("AbraSilver Resource","银矿勘探"),"QCOM.TO":("Qualcomm（CDR）","半导体·CDR"),
 "HOOD.TO":("Robinhood（CDR）","在线券商·CDR"),"SNDK.TO":("SanDisk（CDR）","存储芯片·CDR"),
 "TMQ.TO":("Trilogy Metals","铜矿勘探"),"KEEL.TO":("Keel Infrastructure","数据中心基础设施"),
 "LAR.TO":("Lithium Argentina","锂矿"),"NUAG.TO":("New Pacific Metals","银矿勘探"),
 "EFR.TO":("Energy Fuels","铀/稀土"),"SLG.V":("San Lorenzo Gold","金矿勘探"),
 "CRWV.TO":("CoreWeave（CDR）","AI算力云·CDR"),"USA.TO":("Americas Gold and Silver","金银矿"),
 "NGEX.TO":("NGEx Minerals","铜金勘探"),"HSTR.TO":("Heliostar Metals","金矿"),
 "AP-UN.TO":("Allied Properties REIT","办公REIT"),"MAI.TO":("Mining Americas","金矿"),
 "ARA.TO":("Aclara Resources","稀土"),"ANET.TO":("Arista Networks（CDR）","网络设备·CDR"),
 "HBM.TO":("Hudbay Minerals","铜金矿"),"HIVE.TO":("HIVE Digital","比特币矿机/算力"),
 "AAUC.TO":("Allied Gold","金矿"),"HSLV.TO":("Highlander Silver","银矿勘探"),
 "ARIS.TO":("Aris Mining","金矿"),"CDE.TO":("Coeur Mining","金银矿"),
 "IMG.TO":("IAMGOLD","金矿"),"ISO.TO":("IsoEnergy","铀矿勘探"),"APPS.TO":("AppLovin（CDR）","广告科技·CDR"),
 "MRV.TO":("Marvell（CDR）","半导体·CDR"),"TLO.TO":("Talon Metals","镍矿勘探"),"DML.TO":("Denison Mines","铀矿"),
 "K.TO":("Kinross Gold","金矿"),"TSAT.TO":("Telesat","卫星通信"),
}

def cap_s(c):
    if not c: return "–"
    return f"{c/1e9:.1f}B" if c >= 1e9 else f"{c/1e6:.0f}M"

def vr(vol, avg):
    return round(vol/(avg*FRAC), 1) if avg else None

def drcap(sym, fallback):
    return tvcap.get(sym.split(".")[0], fallback)

def build(side, desc):
    rows = []
    for r in proc[side]:
        if "drop" in r or r["sym"] in EXCLUDE: continue
        if r.get("is_dr"):
            r = dict(r, cap=drcap(r["sym"], r["cap"]), vr=vr(r["vol"], r["avg"]))
        else:
            r = dict(r, vr=vr(r["vol"], r["avg"]))
        rows.append(r)
    for s, n, p, c, cap, vol, avg in TV_ADD[side]:
        rows.append({"sym":s,"name":n,"price":p,"chg":c,"cap":cap or drcap(s, None),"vr":vr(vol, avg),"tv_sector":"CDR"})
    rows.sort(key=lambda r: r["chg"], reverse=desc)
    out = []
    for i, r in enumerate(rows[:30], 1):
        name, sec = META.get(r["sym"], (str(r["name"])[:22], r.get("tv_sector") or "–"))
        if r["sym"] not in META: print("NO META:", r["sym"], r["name"])
        out.append([i, r["sym"], name, f"{r['price']:.2f}", f"{r['chg']:+.2f}%", cap_s(r["cap"]), sec, r["vr"]])
    print(side, "31-36:", [(r["sym"], r["chg"], r["vr"]) for r in rows[30:36]])
    return out

G, L = build("gainers", True), build("losers", False)
if len(sys.argv) > 1 and sys.argv[1] == "preview":
    for r in G: print(r)
    print("---")
    for r in L: print(r)
    sys.exit()

NARR = json.load(open(D + "_narr_1030.json", encoding="utf-8"))
data = {
 "date": "2026-10-30", "weekday": "周五",
 "snapshot": "2026-10-30 10:00 ET 盘中（开盘约 30 分钟）",
 "market_state": "REGULAR",
 "vr_note": "量比 = 当日成交量 ÷ (3个月日均量 × 0.077)，0.077 为快照时已开盘时长占比（0.5h / 6.5h），早盘量比波动大，仅供参考。CDR 行用 Yahoo .TO 挂牌 3 个月均量，基数小易放大。⚠️≥3，🔥≥8。",
 "gainers": G, "losers": L,
 "table_notes": NARR["table_notes"],
 "sectors_html": NARR["sectors_html"],
 "anomalies_html": NARR["anomalies_html"],
 "digest": NARR["digest"],
}
json.dump(data, open(D + "2026-10-30.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in G: print(r)
print("---")
for r in L: print(r)
