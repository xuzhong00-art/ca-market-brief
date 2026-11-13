# -*- coding: utf-8 -*-
import json
m = json.load(open("data/_merged.json", encoding="utf-8"))
RATIO = 1.0
META = {
 "LCFS.TO": ("Tidewater Renewables", "可再生柴油"), "TWM.TO": ("Tidewater Midstream", "中游/炼油"), "CJT.TO": ("Cargojet", "航空货运"),
 "GRZ.V": ("Gold Reserve", "仲裁索偿/Citgo"), "DRM.TO": ("Dream Unlimited", "地产开发/资管"), "DR.TO": ("Medical Facilities", "专科医院"),
 "FDR.V": ("Founders Metals", "金矿勘探(苏里南)"), "FEC.TO": ("Frontera Energy", "油气(哥伦比亚)"), "HHH.V": ("Helius Minerals", "铜金勘探(内华达)"),
 "CTC-A.TO": ("Canadian Tire", "综合零售"), "APTX.TO": ("Apotex Health", "仿制药"), "AMD.TO": ("AMD CDR", "AI芯片(CDR)"),
 "AVGO.TO": ("Broadcom CDR", "AI芯片(CDR)"), "ANET.TO": ("Arista Networks CDR", "数据中心网络(CDR)"), "ESI.TO": ("Ensign Energy Services", "钻井服务"),
 "GRID.TO": ("Tantalus Systems", "智能电网软件"), "CLS.TO": ("Celestica", "AI服务器/EMS"), "SCOT.V": ("Scottie Resources", "金矿勘探(BC)"),
 "AP-UN.TO": ("Allied Properties REIT", "办公REIT"), "GG.V": ("Golconda Gold", "金矿(南非)"), "TOT.TO": ("Total Energy Services", "油服/压缩设备"),
 "TNZ.TO": ("Tenaz Energy", "油气(荷兰/加)"), "CAE.TO": ("CAE", "航空模拟训练"), "CEGS.TO": ("Constellation Energy CDR", "核电公用事业(CDR)"),
 "AVTS.V": ("Aventus Capital", "金融控股"), "ACX.TO": ("ACT Energy Technologies", "定向钻井技术"), "GSY.TO": ("goeasy", "次级消费贷"),
 "PRV-UN.TO": ("PRO REIT", "商业地产REIT"), "KEI.TO": ("Kolibri Global Energy", "油气(俄克拉荷马)"), "DB.V": ("Decibel Cannabis", "大麻"),
 "FSZ.TO": ("Fiera Capital", "资产管理"), "TF.TO": ("Timbercreek Financial", "商业地产抵押贷"), "ITR.V": ("Integra Resources", "金矿(内华达/爱达荷)"),
 "BTQ.NE": ("BTQ Technologies", "后量子加密"), "TLO.TO": ("Talon Metals", "镍铜勘探(明尼苏达)"), "SMCI.TO": ("Super Micro CDR", "AI服务器(CDR)"),
 "VRNO.NE": ("Verano Holdings", "美国大麻MSO"), "PDI.TO": ("PDI Gold", "金矿(澳)"), "MOON.V": ("Blue Moon Metals", "铜锌开发(挪威)"),
 "XNDU.TO": ("Xanadu Quantum", "量子计算"), "NFGC.TO": ("New Found Gold", "金矿勘探(纽芬兰)"), "ABXX.TO": ("Abaxx Technologies", "商品交易所/清算"),
 "EDV.TO": ("Endeavour Mining", "金矿(西非)"), "IE.TO": ("Ivanhoe Electric", "铜矿开发(亚利桑那)"), "MAXX.CN": ("Max Power Mining", "天然氢/铀勘探"),
 "SCRI.NE": ("Silver Crown Royalties", "白银权利金"), "PMET.TO": ("PMET Resources", "锂矿开发(魁北克)"), "AYA.TO": ("Aya Gold & Silver", "银矿(摩洛哥)"),
 "CRWV.TO": ("CoreWeave CDR", "AI云算力(CDR)"), "GAU.TO": ("Galiano Gold", "金矿(加纳)"), "LMCU.TO": ("Lumina Metals", "铜金勘探(阿根廷)"),
 "ISO.TO": ("IsoEnergy", "铀矿开发"), "CURA.TO": ("Curaleaf", "美国大麻MSO"), "DSV.TO": ("Discovery Mining", "银矿开发(墨西哥)"),
 "TSAT.TO": ("Telesat", "卫星通信"), "CS.TO": ("Capstone Copper", "铜矿"), "MSTR.TO": ("Strategy CDR", "比特币财库(CDR)"),
 "GMIN.TO": ("G Mining Ventures", "金矿(巴西)"), "HIVE.TO": ("HIVE Digital", "加密挖矿/算力"), "MAL.TO": ("Magellan Aerospace", "航空零部件"),
}
def cap(c):
    return "%.1fB" % (c / 1e9) if c >= 1e9 else "%dM" % round(c / 1e6)
def rows(lst):
    out = []
    for i, v in enumerate(lst, 1):
        s = v["sym"]
        nm, sc = META.get(s, (v["name"][:24], v.get("tvsector", "")))
        vr = round(v["vol"] / (v["avg"] * RATIO), 1) if v.get("avg") else None
        out.append([i, s, nm, "%.2f" % v["price"], "%+.2f%%" % v["chg"], cap(v["cap"]), sc, vr])
    return out
g, l = rows(m["g"]), rows(m["l"])
print("missing:", [r[1] for r in g + l if r[1] not in META])
for r in g + l:
    if r[7] and r[7] >= 3: print(r[1], r[4], r[7])
json.dump({"g": g, "l": l}, open("data/_rows.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
