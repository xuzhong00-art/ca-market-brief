# -*- coding: utf-8 -*-
"""Build data/2026-10-08.json from _proc.json + TV-only CDR rows + manual meta."""
import json

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
proc = json.load(open(D + "_proc.json", encoding="utf-8"))
FRAC = 1.0

# .NE rows that have a fuller .TO listing -> replace with TSX data (Yahoo v7 + TV lookup, 2026-10-08 close)
# sym, name, price, chg, cap, vol, avg
TO_OVERRIDE = {
 "CMGS.NE": ("CMGS.TO", 12.56, 5.81, 55.5e9, 96765, 7689),
 "HD.NE":   ("HD.TO", 18.23, 3.23, 406.7e9, 134528, 36252),
 "ORAC.NE": ("ORAC.TO", 6.68, -5.65, 619.2e9, 736950, 654385),
 "INTC.NE": ("INTC.TO", 59.90, -5.42, 853.0e9, 338297, 331018),
 "SMCI.NE": ("SMCI.TO", 13.75, -4.91, 42.1e9, 854308, 630576),
 "MU.NE":   ("MU.TO", 45.35, -4.73, 1752.9e9, 1750851, 1827179),
 "AVGO.NE": ("AVGO.TO", 13.69, -4.27, 2563.9e9, 1381159, 807646),
}
# TV-only additions (absent from Yahoo screener)
TV_ADD = {
 "gainers": [
  ("STZ.TO", "Constellation Brands CDR", 9.72, 4.29, 28.8e9, 24773, 6957),
  ("PEP.TO", "PepsiCo CDR", 18.98, 3.89, 240.9e9, 111251, 24425),
  ("ADBE.TO", "Adobe CDR", 9.18, 3.61, 129.2e9, 114942, 136367),
  ("OXY.TO", "Occidental Petroleum CDR", 25.05, 3.38, 83.0e9, 26267, 7201),
 ],
 "losers": [
  ("GLAS-A-U.NE", "Glass House Brands", 4.41, -11.80, 0.387e9, 71000, 34479),
  ("CRWV.TO", "CoreWeave CDR", 15.38, -7.74, 69.6e9, 467431, 150878),
  ("SNDK.TO", "SanDisk CDR", 39.05, -4.92, 353.5e9, 1001457, 796877),
  ("CEGS.TO", "Constellation Energy CDR", 19.40, -4.86, 151.4e9, 85409, 40526),
  ("SPCX.TO", "SpaceX CDR", 26.71, -4.23, 3244.7e9, 782168, 1653815),
 ],
}

META = {
 "FTG.TO":("Firan Technology","航空电子"),"PRN.TO":("Profound Medical","医疗器械(iMRI)"),
 "RCH.TO":("Richelieu Hardware","五金分销"),"GAU.TO":("Galiano Gold","金矿生产(加纳)"),
 "ALC.TO":("Algoma Central","海运/五大湖航运"),"CMGS.TO":("Chipotle CDR","餐饮(CDR)"),
 "GO-U.TO":("GO Residential REIT","住宅REIT(美元)"),"AKT.TO":("AKITA Drilling","钻井服务"),
 "IPCO.TO":("International Petroleum","油气生产"),"FVI.TO":("Fortuna Mining","金银矿"),
 "CAD.V":("Colonial Coal","冶金煤"),"ITH.TO":("International Tower Hill","黄金开发(阿拉斯加)"),
 "DPM.TO":("DPM Metals","黄金生产"),"OBE.TO":("Obsidian Energy","油气生产"),
 "RBA.TO":("RB Global","工业拍卖/服务"),"SDE.TO":("Spartan Delta","油气"),
 "IAU.TO":("i-80 Gold","黄金(内华达)"),"SU.TO":("Suncor Energy","油砂"),
 "HR-UN.TO":("H&R REIT","多元REIT"),"BTE.TO":("Baytex Energy","油气"),
 "CEU.TO":("CES Energy Solutions","油田化学品"),"MFG.V":("Mayfair Gold","黄金开发(安大略)"),
 "RBY.TO":("Rubellite Energy","油气"),"MKO.V":("Mako Mining","黄金(尼加拉瓜)"),
 "KEY.TO":("Keyera","能源中游"),"SCOT.V":("Scottie Resources","黄金勘探(BC)"),
 "LGD.TO":("Liberty Gold","黄金开发(美国)"),"IPO.TO":("InPlay Oil","油气"),
 "CG.TO":("Centerra Gold","黄金"),"CNQ.TO":("Canadian Natural Resources","油气"),
 "TNZ.TO":("Tenaz Energy","油气(荷兰/加)"),"HD.TO":("Home Depot CDR","家居零售CDR"),
 "TVE.TO":("Tamarack Valley Energy","油气"),"CJ.TO":("Cardinal Energy","油气"),
 "STZ.TO":("Constellation Brands CDR","酒类CDR"),"PEP.TO":("PepsiCo CDR","饮料食品CDR"),
 "ADBE.TO":("Adobe CDR","创意软件CDR"),"OXY.TO":("Occidental CDR","油气CDR"),
 # losers
 "HUT.TO":("Hut 8","比特币矿/AI算力"),"BTQ.NE":("BTQ Technologies","后量子加密"),
 "ELVA.TO":("Electrovaya","锂电池"),"TI.TO":("Titan Mining","锌/石墨"),
 "XNDU.TO":("Xanadu Quantum","量子计算"),"NEO.TO":("Neo Performance Materials","稀土磁材"),
 "HG.CN":("HydroGraph Clean Power","石墨烯材料"),"KITS.TO":("Kits Eyecare","眼镜电商"),
 "DML.TO":("Denison Mines","铀矿"),"HIVE.TO":("HIVE Digital","比特币矿/AI算力"),
 "MSCL.TO":("Satellos Bioscience","生物医药"),"ZVST.NE":("Vistra CDR","电力(CDR)"),
 "MDA.TO":("MDA Space","航天"),"APTX.TO":("Apotex Health","仿制药"),
 "KEEL.TO":("Keel Infrastructure","数据中心/算力"),"ORAC.TO":("Oracle CDR","软件/AI云CDR"),
 "MLP.V":("Millennial Potash","钾肥(加蓬)"),"INTC.TO":("Intel CDR","半导体CDR"),
 "PNG.V":("Kraken Robotics","海洋机器人/国防"),"SMCI.TO":("Super Micro CDR","AI服务器CDR"),
 "ISO.TO":("IsoEnergy","铀矿"),"ABXX.TO":("Abaxx Technologies","大宗商品交易所"),
 "UCU.V":("Ucore Rare Metals","稀土分离"),"MU.TO":("Micron CDR","存储芯片CDR"),
 "CLS.TO":("Celestica","AI服务器/EMS"),"HITI.V":("High Tide","大麻零售"),
 "AVGO.TO":("Broadcom CDR","半导体CDR"),"TSAT.TO":("Telesat","卫星通信"),
 "VNP.TO":("5N Plus","特种半导体材料"),"TLRY.TO":("Tilray Brands","大麻/饮料"),
 "GLAS-A-U.NE":("Glass House Brands","大麻(加州,美元)"),"CRWV.TO":("CoreWeave CDR","AI云算力CDR"),
 "SNDK.TO":("SanDisk CDR","存储芯片CDR"),"CEGS.TO":("Constellation Energy CDR","核电(CDR)"),
 "SPCX.TO":("SpaceX CDR","航天(CDR)"),
}

def fmt_cap(c):
    if not c: return "–"
    return f"{c/1e9:.1f}B" if c >= 1e9 else f"{c/1e6:.0f}M"

def build(side, desc):
    rows = []
    for r in proc[side]:
        if "drop" in r: continue
        sym = r["sym"]
        price, chg, cap, vol, avg = r["price"], r["chg"], r["cap"], r["vol"], r["avg"]
        if sym in TO_OVERRIDE:
            sym, price, chg, cap, vol, avg = TO_OVERRIDE[sym]
        rows.append((sym, price, chg, cap, vol, avg))
    for sym, _, price, chg, cap, vol, avg in TV_ADD[side]:
        rows.append((sym, price, chg, cap, vol, avg))
    rows.sort(key=lambda x: x[2], reverse=desc)
    out = []
    for i, (sym, price, chg, cap, vol, avg) in enumerate(rows[:30], 1):
        name, sector = META.get(sym, (sym, "?"))
        if sector == "?": print("MISSING META", sym)
        vr = round(vol / (avg * FRAC), 1) if avg else None
        out.append([i, sym, name, f"{price:.2f}", f"{chg:+.2f}%", fmt_cap(cap), sector, vr])
    return out

g, l = build("gainers", True), build("losers", False)
json.dump({"gainers": g, "losers": l}, open(D + "_rows_1008.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in g + l: print(r)
