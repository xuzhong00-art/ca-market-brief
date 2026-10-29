# -*- coding: utf-8 -*-
"""Build data/2026-10-29.json from _proc.json + CDR additions + meta (catch-up run 15:35 ET, FRAC=0.94)."""
import json, sys

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
proc = json.load(open(D + "_proc.json", encoding="utf-8"))
tv = json.load(open(D + "_tv_raw.json", encoding="utf-8"))
FRAC = 0.94  # 15:35 ET => 6h05m of 6.5h session

COLS = ["name","description","close","change","market_cap_basic","sector","volume","avg90","type","exchange","update_mode","time"]
tvcap = {}
for blob in tv.values():
    if not blob: continue
    for it in blob["data"]:
        d = dict(zip(COLS, it["d"])); sym = it["s"].split(":")[1]
        if d["type"] == "dr" and d["market_cap_basic"]: tvcap[sym] = d["market_cap_basic"]

# .NE rows -> .TO fuller data (Yahoo v7 quote): sym, price, chg, cap, vol, avg3m
TO_OVERRIDE = {
 "LLY.NE": ("LLY.TO", 48.82, 6.22, None, 292512, 72316),
 "LULU.NE": ("LULU.TO", 4.74, 4.41, None, 407626, 514998),
 "NKE.NE": ("NKE.TO", 6.86, 3.63, None, 153439, 262927),
 "NOWS.NE": ("NOWS.TO", 13.87, -27.12, None, 739700, 179561),
 "CATR.NE": ("CATR.TO", 45.74, -9.48, None, 100225, 39859),
 "MU.NE": ("MU.TO", 40.71, -5.28, None, 904448, 1513725),
}
# TV-only additions (Yahoo v7 quote): sym, name, price, chg, cap(None->TV), vol, avg3m
TV_ADD = {
 "gainers": [
  ("CMGS.TO", "Chipotle（CDR）", 12.11, 9.39, None, 48946, 11240),
  ("KLAC.TO", "KLA（CDR）", 22.55, 5.52, None, 34276, 27901),
  ("MA.TO", "Mastercard（CDR）", 38.25, 4.11, None, 21965, 13967),
  ("MRK.TO", "Merck（CDR）", 32.63, 4.05, None, 39559, 14543),
  ("F.TO", "Ford（CDR）", 10.34, 3.40, None, 90814, 30687),
  ("BA.TO", "Boeing（CDR）", 28.50, 3.00, None, 110998, 54040),
  ("HD.TO", "Home Depot（CDR）", 20.11, 2.92, None, 42290, 39248),
  ("MCD.TO", "McDonald's（CDR）", 21.56, 2.72, None, 189922, 103514),
  ("VISA.TO", "Visa（CDR）", 37.25, 2.42, None, 24059, 30838),
  ("LMT.TO", "Lockheed Martin（CDR）", 36.46, 2.39, None, 23263, 22430),
  ("CEGS.TO", "Constellation Energy（CDR）", 17.97, 2.33, None, 46470, 56998),
  ("WMT.TO", "Walmart（CDR）", 50.47, 2.10, None, 52919, 120645),
  ("HG.CN", "HydroGraph Clean Power", 4.40, 3.04, 1594622976, 1345054, 663580),
 ],
 "losers": [
  ("FTNT.TO", "Fortinet（CDR）", 17.37, -21.97, None, 52363, 6150),
  ("MRV.TO", "Marvell（CDR）", 34.87, -14.22, None, 339175, 165261),
  ("CRM.TO", "Salesforce（CDR）", 17.41, -5.28, None, 73504, 145498),
  ("SNDK.TO", "SanDisk（CDR）", 32.24, -5.26, None, 518029, 1030832),
  ("RDDT.TO", "Reddit（CDR）", 12.19, -4.91, None, 285360, 125601),
  ("CRWV.TO", "CoreWeave（CDR）", 11.47, -4.50, None, 438618, 296380),
 ],
}
EXCLUDE = set()

META = {
 # gainers
 "BHC.TO":("Bausch Health","制药"),"CMGS.TO":("Chipotle（CDR）","餐饮·CDR"),
 "LLY.TO":("Eli Lilly（CDR）","制药/GLP-1·CDR"),"KLAC.TO":("KLA（CDR）","半导体设备·CDR"),
 "HFPC-U.TO":("Helios Fairfax Partners","非洲投资控股(美元计价)"),"LULU.TO":("lululemon（CDR）","运动服饰·CDR"),
 "RBA.TO":("RB Global","工业资产拍卖"),"MA.TO":("Mastercard（CDR）","支付网络·CDR"),
 "ACQ.TO":("AutoCanada","汽车经销"),"MRK.TO":("Merck（CDR）","制药·CDR"),
 "FSV.TO":("FirstService","物业服务"),"NKE.TO":("NIKE（CDR）","运动服饰·CDR"),
 "F.TO":("Ford（CDR）","汽车制造·CDR"),"HG.CN":("HydroGraph Clean Power","石墨烯材料"),
 "BA.TO":("Boeing（CDR）","航空制造·CDR"),"PRL.TO":("Propel Holdings","金融科技消费贷"),
 "HD.TO":("Home Depot（CDR）","家装零售·CDR"),"KITS.TO":("Kits Eyecare","眼镜电商"),
 "GFL.TO":("GFL Environmental","固废处理"),"MCD.TO":("McDonald's（CDR）","餐饮·CDR"),
 "APTX.TO":("Apotex Health","仿制药"),"DFY.TO":("Definity Financial","财产保险"),
 "QTRH.TO":("Quarterhill","智能交通/收费系统"),"GSY.TO":("goeasy","次级消费贷"),
 "VISA.TO":("Visa（CDR）","支付网络·CDR"),"AIF.TO":("Altus Group","地产数据/软件"),
 "GOOS.TO":("Canada Goose","高端服饰"),"LMT.TO":("Lockheed Martin（CDR）","国防·CDR"),
 "CEGS.TO":("Constellation Energy（CDR）","核电/电力·CDR"),"META.TO":("Meta Platforms（CDR）","互联网广告·CDR"),
 "ATZ.TO":("Aritzia","女装零售"),"APR-UN.TO":("Automotive Properties REIT","汽车经销地产REIT"),
 "BN.TO":("Brookfield Corp","另类资产管理"),"BAM.TO":("Brookfield Asset Mgmt","另类资产管理"),
 "WMT.TO":("Walmart（CDR）","零售·CDR"),"CIGI.TO":("Colliers","商业地产服务"),
 "MFI.TO":("Maple Leaf Foods","食品加工"),"ATRL.TO":("AtkinsRéalis","工程咨询/核电"),
 "DIV.TO":("Diversified Royalty","特许权利金"),"XLY.TO":("Auxly Cannabis","大麻"),
 "VHI.TO":("Vitalhub","医疗软件"),"DRX.TO":("ADF Group","钢结构制造"),
 "BIP-UN.TO":("Brookfield Infrastructure","基础设施"),"DOL.TO":("Dollarama","折扣零售"),
 "WSP.TO":("WSP Global","工程咨询"),"AAPL.TO":("Apple（CDR）","消费电子·CDR"),
 # losers
 "NOWS.TO":("ServiceNow（CDR）","企业软件·CDR"),"AP-UN.TO":("Allied Properties REIT","写字楼REIT"),
 "FTNT.TO":("Fortinet（CDR）","网络安全·CDR"),"MRV.TO":("Marvell（CDR）","半导体·CDR"),
 "GOOG.TO":("Alphabet（CDR）","互联网/云·CDR"),"CATR.TO":("Caterpillar（CDR）","工程机械·CDR"),
 "AGI.TO":("Alamos Gold","黄金生产"),"TSAT.TO":("Telesat","卫星通信"),
 "MOON.V":("Blue Moon Metals","铜锌勘探(挪威)"),"K.TO":("Kinross Gold","黄金生产"),
 "MAI.TO":("Mining Americas","黄金勘探"),"DGX.NE":("Digi Power X","AI数据中心/比特币挖矿"),
 "SXGC.TO":("Southern Cross Gold","黄金勘探(澳洲)"),"CADY.TO":("Cadillac Mines","黄金勘探"),
 "CLS.TO":("Celestica","电子制造/AI服务器"),"HMMC.TO":("Hemlo Mining","黄金生产"),
 "ELD.TO":("Eldorado Gold","黄金生产"),"SKE.TO":("Skeena Resources","金银开发(BC)"),
 "WDO.TO":("Wesdome Gold Mines","黄金生产"),"EFN.TO":("Element Fleet Management","车队管理"),
 "GSKR.V":("Goldsky Resources","黄金勘探"),"KEEL.TO":("Keel Infrastructure","数据中心/算力基建"),
 "ARA.TO":("Aclara Resources","稀土开发"),"NUAG.TO":("New Pacific Metals","白银开发(玻利维亚)"),
 "ELE.TO":("Elemental Royalty","贵金属权利金"),"MU.TO":("Micron（CDR）","存储芯片·CDR"),
 "CRM.TO":("Salesforce（CDR）","企业软件·CDR"),"SNDK.TO":("SanDisk（CDR）","存储闪存·CDR"),
 "JAG.TO":("Jaguar Mining","黄金生产(巴西)"),"TALA.TO":("Talamore Mining","黄金勘探"),
 "RDDT.TO":("Reddit（CDR）","社交媒体·CDR"),"FM.TO":("First Quantum Minerals","铜矿生产"),
 "AMX.V":("Amex Gold Mining","黄金勘探(魁北克)"),"GGD.TO":("GoGold Resources","银金开发(墨西哥)"),
 "CGG.TO":("China Gold International","黄金/铜生产"),"HUT.TO":("Hut 8","比特币挖矿/AI算力"),
 "SSRM.TO":("SSR Mining","贵金属生产"),"ORE.TO":("Orezone Gold","黄金生产(布基纳法索)"),
 "CRWV.TO":("CoreWeave（CDR）","AI云算力·CDR"),"BE.TO":("Bloom Energy（CDR）","燃料电池·CDR"),
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
        if r["sym"] in TO_OVERRIDE:
            s, p, c, cap, vol, avg = TO_OVERRIDE[r["sym"]]
            r = dict(r, sym=s, price=p, chg=c, cap=cap or drcap(s, r["cap"]), vol=vol, avg=avg, vr=vr(vol, avg))
        elif r.get("is_dr"):
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

NARR = json.load(open(D + "_narr_1029.json", encoding="utf-8"))
data = {
 "date":"2026-10-29","weekday":"周四",
 "snapshot":"2026-10-29 15:35 ET 盘中（补跑，开盘约 6 小时 05 分钟，收盘前 25 分钟）",
 "market_state":"REGULAR",
 "note":"本期为补跑：电脑未在 7:00 PT 按时执行，快照取自 15:35 ET（收盘前 25 分钟），数据接近全日。",
 "vr_note":"量比 = 当日成交量 ÷ (3个月日均量 × 0.94)，0.94 为快照时已开盘时长占比（6h05m / 6.5h），接近全日量比。CDR 行用 Yahoo .TO 挂牌 3 个月均量，基数小易放大。⚠️≥3，🔥≥8。",
 "gainers":G,"losers":L,
 "table_notes":NARR["table_notes"],
 "sectors_html":NARR["sectors_html"],
 "anomalies_html":NARR["anomalies_html"],
 "digest":NARR["digest"],
}
json.dump(data, open(D + "2026-10-29.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in G: print(r)
print("---")
for r in L: print(r)
