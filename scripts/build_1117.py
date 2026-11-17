# -*- coding: utf-8 -*-
"""Build data/2026-11-17.json from ca_proc.json + manual sector/narrative."""
import json, os
TMP = os.environ.get("LOCALAPPDATA", ".") + "/Temp"
P = json.load(open(TMP + "/ca_proc.json", encoding="utf-8"))
R = P["results"]; FRAC = 0.21
D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/2026-11-17.json"

def fmtcap(c):
    if not c: return "?"
    return f"{c/1e9:.1f}B" if c >= 1e9 else f"{c/1e6:.0f}M"

SEC = {
 "TC.TO":"互联网域名/光纤(Ting出售)","SCZ.TO":"白银生产(玻利维亚)","NUAG.TO":"白银开发(玻利维亚)","JAG.TO":"黄金生产(巴西)",
 "CHE-UN.TO":"工业化学品","SEA.TO":"黄金开发(KSM)","VZLA.TO":"白银开发(墨西哥)","LMCU.TO":"铜银开发(波兰)","FM.TO":"铜矿",
 "MSA.TO":"黄金生产(哥伦比亚)","DC-A.TO":"矿业投资控股","FWZ.TO":"锌铅/钨开发(育空)","MAI.TO":"黄金生产(内华达)",
 "ARA.TO":"稀土开发","SLG.V":"黄金勘探(智利)","MAU.TO":"黄金开发(科特迪瓦)","FNV.TO":"贵金属权利金","PPTA.TO":"黄金/锑开发(爱达荷)",
 "HSTR.TO":"黄金生产(墨西哥)","LAR.TO":"锂","TWM.TO":"中游/炼化","OR.TO":"贵金属权利金","GMIN.TO":"黄金生产(巴西)",
 "TMQ.TO":"铜开发(阿拉斯加)","IMG.TO":"黄金生产","RDDT.TO":"社交媒体 CDR","RIO.TO":"黄金开发(智利)","DGX.NE":"AI数据中心/挖矿",
 "XLY.TO":"大麻","RGSI.TO":"天然气储运","III.TO":"铜矿(BC)",
 "GRGD.TO":"女装零售","CRM.TO":"企业软件 CDR","SNDK.TO":"存储芯片 CDR","BDT.TO":"工程建筑","BE.TO":"燃料电池 CDR",
 "NOWS.TO":"企业软件 CDR","BB.TO":"网络安全/车载软件","EPRX.TO":"生物科技","MU.TO":"存储芯片 CDR","SMCI.TO":"AI服务器 CDR",
 "ELVA.TO":"锂电池","INTU.TO":"财税软件 CDR","HOOD.TO":"互联网券商 CDR","APPS.TO":"广告科技 CDR","ARE.TO":"工程建筑",
 "NGEX.TO":"铜金开发(阿根廷)","QBR-B.TO":"电信/媒体","XNDU.TO":"量子计算","CMG.TO":"油藏模拟软件","ENGH.TO":"企业软件",
 "RUS.TO":"金属分销","HG.CN":"石墨烯","ASTL.TO":"钢铁","OTEX.TO":"企业软件","KNT.TO":"黄金生产(巴新)","FSZ.TO":"资产管理",
 "SBC.TO":"分级基金(银行)","KEL.TO":"天然气(蒙特尼)","SHOP.TO":"电商软件","SLS.TO":"铜金开发(厄瓜多尔)","KRY.V":"铜开发(纳米比亚)",
}
# overrides: [sym, name, price, chg, cap, vr]  (CDR rows from v7 quote / TV, DGX from TV)
OVR = {
 "CRM.TO": ("Salesforce CDR", 14.75, -9.40, "253B*", round(103607/(144914*FRAC),1)),
 "SNDK.TO": ("SanDisk CDR", 18.17, -7.28, "165B*", round(971886/(1220280*FRAC),1)),
 "BE.TO": ("Bloom Energy CDR", 12.80, -7.18, "75B*", round(38622/(70805*FRAC),1)),
 "NOWS.TO": ("ServiceNow CDR", 11.72, -7.06, "148B*", round(166584/(205874*FRAC),1)),
 "MU.TO": ("Micron CDR", 29.29, -6.81, "1164B*", round(1118112/(1748374*FRAC),1)),
 "SMCI.TO": ("Super Micro CDR", 7.50, -6.72, "24B*", round(435373/(722311*FRAC),1)),
 "INTU.TO": ("Intuit CDR", 19.53, -6.38, "132B*", round(57632/(75476*FRAC),1)),
 "HOOD.TO": ("Robinhood CDR", 10.98, -6.31, "93B*", round(56664/(171012*FRAC),1)),
 "APPS.TO": ("AppLovin CDR", 12.16, -6.25, "197B*", round(50532/(190446*FRAC),1)),
 "RDDT.TO": ("Reddit CDR", 9.11, 2.94, "26B*", round(41251/(130649*FRAC),1)),
 "DGX.NE": ("Digi Power X", 2.95, 2.79, "266M", round(48506/(20610*FRAC),1)),
}
NAME = {"TC.TO":"Tucows","SCZ.TO":"Santacruz Silver","NUAG.TO":"New Pacific Metals","JAG.TO":"Jaguar Mining","CHE-UN.TO":"Chemtrade Logistics",
 "SEA.TO":"Seabridge Gold","VZLA.TO":"Vizsla Silver","LMCU.TO":"Lumina Metals","FM.TO":"First Quantum","MSA.TO":"Mineros","DC-A.TO":"Dundee Corp",
 "FWZ.TO":"Fireweed Metals","MAI.TO":"Mining Americas","ARA.TO":"Aclara Resources","SLG.V":"San Lorenzo Gold","MAU.TO":"Montage Gold",
 "FNV.TO":"Franco-Nevada","PPTA.TO":"Perpetua Resources","HSTR.TO":"Heliostar Metals","LAR.TO":"Lithium Argentina","TWM.TO":"Tidewater Midstream",
 "OR.TO":"OR Royalties","GMIN.TO":"G Mining Ventures","TMQ.TO":"Trilogy Metals","IMG.TO":"IAMGOLD","RIO.TO":"Rio2","XLY.TO":"Auxly Cannabis",
 "RGSI.TO":"Rockpoint Gas Storage","III.TO":"Imperial Metals","GRGD.TO":"Groupe Dynamite","BDT.TO":"Bird Construction","BB.TO":"BlackBerry",
 "EPRX.TO":"Eupraxia Pharma","ELVA.TO":"Electrovaya","ARE.TO":"Aecon Group","NGEX.TO":"NGEx Minerals","QBR-B.TO":"Quebecor","XNDU.TO":"Xanadu Quantum",
 "CMG.TO":"Computer Modelling","ENGH.TO":"Enghouse Systems","RUS.TO":"Russel Metals","HG.CN":"HydroGraph","ASTL.TO":"Algoma Steel","OTEX.TO":"Open Text",
 "KNT.TO":"K92 Mining","FSZ.TO":"Fiera Capital","SBC.TO":"Brompton Split Banc","KEL.TO":"Kelt Exploration","SHOP.TO":"Shopify","SLS.TO":"Solaris Resources"}

EXCLUDE = {"BZ.V","KEEL.TO"}  # Yahoo/TV price discrepancy >2pp, see table_notes

def rows(side, extra_syms):
    out = []
    for r in R[side]:
        if r["drop"] or r["sym"] in EXCLUDE: continue
        out.append(r)
    byname = {r["sym"]: r for r in out}
    lst = []
    for r in out:
        s = r["sym"]
        if s.endswith(".NE") and s[:-3] + ".TO" in OVR: s = s[:-3] + ".TO"
        if s in OVR:
            n, p, c, cap, vr = OVR[s]
        else:
            n, p, c, cap, vr = NAME.get(s, r["name"]), r["price"], r["chg"], fmtcap(r["cap"]), r["vr"]
        lst.append([s, n, p, c, cap, SEC.get(s, r["tv_ind"] or "?"), vr])
    for s in extra_syms:
        n, p, c, cap, vr = OVR[s]
        lst.append([s, n, p, c, cap, SEC[s], vr])
    lst.sort(key=lambda x: -x[3] if side == "gainers" else x[3])
    lst = lst[:30]
    res = []
    for i, (s, n, p, c, cap, sec, vr) in enumerate(lst, 1):
        res.append([i, s, n, f"{p:.2f}" if p < 100 else f"{p:.2f}", f"{c:+.2f}%", cap, sec, vr])
    return res

g = rows("gainers", ["DGX.NE", "RDDT.TO"])
l = rows("losers", ["CRM.TO", "SNDK.TO", "BE.TO", "INTU.TO", "HOOD.TO", "APPS.TO"])
for r in g: print(r)
print("---")
for r in l: print(r)
json.dump({"g": g, "l": l}, open(TMP + "/ca_tables.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
