# -*- coding: utf-8 -*-
"""Build data/2026-10-26.json from _proc.json + CDR additions + meta (post-close backfill, FRAC=1.0)."""
import json

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
proc = json.load(open(D + "_proc.json", encoding="utf-8"))
tv = json.load(open(D + "_tv_raw.json", encoding="utf-8"))
FRAC = 1.0

COLS = ["name","description","close","change","market_cap_basic","sector","volume","avg90","type","exchange","update_mode","time"]
tvcap = {}
for blob in tv.values():
    if not blob: continue
    for it in blob["data"]:
        d = dict(zip(COLS, it["d"])); sym = it["s"].split(":")[1]
        if d["type"] == "dr" and d["market_cap_basic"]: tvcap[sym] = d["market_cap_basic"]

# .NE rows -> .TO fuller data (Yahoo v7 quote, post-close): sym, price, chg, cap, vol, avg3m
TO_OVERRIDE = {
 "INTC.NE": ("INTC.TO", 50.63, 4.05, None, 245376, 313098),
 "LULU.NE": ("LULU.TO", 4.43, 3.75, None, 154955, 515374),
 "NFLX.NE": ("NFLX.TO", 23.89, -2.85, None, 348872, 228935),
}
# TV-only additions (Yahoo v7 quote): sym, name, price, chg, cap(None->TV), vol, avg3m
TV_ADD = {
 "gainers": [
  ("LMT.TO", "Lockheed Martin（CDR）", 35.86, 5.19, None, 32810, 19827),
  ("GEV.TO", "GE Vernova（CDR）", 57.35, 4.83, None, 33647, 42514),
  ("WDC.TO", "Western Digital（CDR）", 21.64, 3.64, None, 164687, 130914),
 ],
 "losers": [
  ("MSTR.TO", "Strategy（CDR）", 9.49, -4.24, None, 434515, 458670),
  ("RDDT.TO", "Reddit（CDR）", 13.21, -3.79, None, 237478, 120212),
  ("PYPL.TO", "PayPal（CDR）", 3.90, -3.70, None, 33458, 108066),
  ("MRK.TO", "Merck（CDR）", 31.07, -3.66, None, 16160, 14304),
  ("VZ.TO", "Verizon（CDR）", 18.03, -3.38, None, 75493, 16175),
  ("FISV.TO", "Fiserv（CDR）", 4.86, -3.19, None, 18694, 20246),
  ("HOOD.TO", "Robinhood（CDR）", 15.11, -2.52, None, 121930, 165802),
 ],
}
EXCLUDE = {"BE.TO"}  # Yahoo screener put BE (+5.91%) in the losers list by error

META = {
 # gainers
 "HLF.TO":("High Liner Foods","冷冻海鲜食品"),"HG.CN":("HydroGraph Clean Power","石墨烯材料"),
 "PDI.TO":("PDI Gold","黄金勘探(澳洲)"),"ISO.TO":("IsoEnergy","铀矿开发"),
 "HPS-A.TO":("Hammond Power Solutions","变压器/电力设备"),"OGG.V":("Osisko Gold Group","黄金勘探"),
 "BZ.V":("Benz Mining","黄金勘探(澳洲)"),"SEA.TO":("Seabridge Gold","黄金开发(BC KSM)"),
 "TSLA.TO":("Tesla（CDR）","电动车·CDR"),"LMT.TO":("Lockheed Martin（CDR）","军工·CDR"),
 "PD.TO":("Precision Drilling","钻井服务"),"TSAT.TO":("Telesat","卫星通信"),
 "MAXX.CN":("Max Power Mining","天然氢/矿业勘探"),"GEV.TO":("GE Vernova（CDR）","电力设备·CDR"),
 "FWZ.V":("Fireweed Metals","锌铅钨勘探(育空)"),"PMET.TO":("PMET Resources","锂矿开发(魁北克)"),
 "CAE.TO":("CAE","飞行模拟/培训"),"NOA.TO":("North American Construction","油砂/矿山工程承包"),
 "GSKR.V":("Goldsky Resources","黄金勘探"),"CNL.TO":("Collective Mining","金铜勘探(哥伦比亚)"),
 "INTC.TO":("Intel（CDR）","半导体·CDR"),"NICU.TO":("Magna Mining","镍铜矿(安大略)"),
 "ERO.TO":("Ero Copper","铜矿生产(巴西)"),"SGML.V":("Sigma Lithium","锂矿生产(巴西)"),
 "IFP.TO":("Interfor","木材"),"BDT.TO":("Bird Construction","建筑工程"),
 "TCW.TO":("Trican Well Service","压裂/油服"),"LULU.TO":("Lululemon（CDR）","运动服饰·CDR"),
 "PSI.TO":("Pason Systems","钻井数据技术"),"WDC.TO":("Western Digital（CDR）","存储硬盘·CDR"),
 "BB.TO":("BlackBerry","车载软件/网安"),"CFW.TO":("Calfrac Well Services","压裂/油服"),
 "MAL.TO":("Magellan Aerospace","航空零部件"),"MTL.TO":("Mullen Group","物流运输"),
 # losers
 "TTS.V":("Tintina Mines","矿业勘探"),"HSLV.TO":("Highlander Silver","银矿勘探(秘鲁)"),
 "VITL-UN.TO":("Vital Infrastructure Property Trust","医疗地产REIT"),"FISH.V":("Sailfish Royalty","贵金属权利金"),
 "DPM.TO":("DPM Metals","金铜生产(保加利亚)"),"GORO.V":("Goldgroup Mining","黄金生产(墨西哥)"),
 "FDR.V":("Founders Metals","黄金勘探(苏里南)"),"CLS.TO":("Celestica","电子制造/AI服务器"),
 "MSTR.TO":("Strategy（CDR）","比特币财库·CDR"),"SBI.TO":("Serabi Gold","黄金生产(巴西)"),
 "LMCU.TO":("Lumina Metals","铜矿勘探"),"RDDT.TO":("Reddit（CDR）","社交媒体·CDR"),
 "PLZ-UN.TO":("Plaza Retail REIT","零售地产REIT"),"PYPL.TO":("PayPal（CDR）","支付·CDR"),
 "MRK.TO":("Merck（CDR）","制药·CDR"),"VZ.TO":("Verizon（CDR）","电信·CDR"),
 "ABRA.TO":("AbraSilver Resource","银矿开发(阿根廷)"),"FISV.TO":("Fiserv（CDR）","支付科技·CDR"),
 "TLRY.TO":("Tilray Brands","大麻/饮料"),"BLDP.TO":("Ballard Power Systems","燃料电池"),
 "NFLX.TO":("Netflix（CDR）","流媒体·CDR"),"SGD.TO":("Snowline Gold","黄金勘探(育空)"),
 "ALS.TO":("Altius Minerals","矿业权利金"),"LAC.TO":("Lithium Americas","锂矿开发(内华达)"),
 "XNDU.TO":("Xanadu Quantum Technologies","量子计算"),"MFG.V":("Mayfair Gold","黄金勘探(安大略)"),
 "VREO.CN":("Vireo Growth","大麻(美国)"),"NUAG.TO":("New Pacific Metals","银矿开发(玻利维亚)"),
 "HHH.V":("Helius Minerals","矿业勘探"),"HOOD.TO":("Robinhood（CDR）","券商·CDR"),
 "TSU.TO":("Trisura Group","专业保险"),"ATZ.TO":("Aritzia","服饰零售"),"ETG.TO":("Entrée Resources","铜金(蒙古)"),
 "EXE.TO":("Extendicare","养老护理"),"ARA.TO":("Aclara Resources","稀土开发(智利/巴西)"),"SVI.TO":("StorageVault Canada","自助仓储"),
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
            r = dict(r, cap=drcap(r["sym"], r["cap"]))
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
data = {
 "date":"2026-10-26","weekday":"周一",
 "snapshot":"2026-10-26 16:00 ET 收盘（补跑快照，当日 18:15 PT 执行）",
 "market_state":"CLOSED",
 "vr_note":"量比 = 当日全天成交量 ÷ 3个月日均量（收盘后补跑，系数 1.0）。CDR 行用 Yahoo .TO 挂牌 3 个月均量，基数小易放大。⚠️≥3，🔥≥8。",
 "gainers":G,"losers":L,
 "table_notes":[
  "*CDR（TSLA/LMT/GEV/INTC/LULU/WDC；MSTR/RDDT/PYPL/MRK/VZ/FISV/NFLX/HOOD）市值为 TradingView 美股母公司总市值（加元口径），非加拿大挂牌流通市值。",
  "*INTC/LULU/NFLX 以 TSX 挂牌数据替代 Yahoo 返回的 NEO 行；LMT/GEV/WDC 及跌幅榜 MSTR/RDDT/PYPL/MRK/VZ/FISV/HOOD 为 TradingView type=dr 补充（Yahoo screener 未返回），行情取 Yahoo v7 收盘快照。",
  "*剔除：TSLA.NE/AMD.NE/NVDA.NE/META.NE/GOOG.NE 交叉挂牌去重；BE.TO（Yahoo 误把 +5.91% 的 Bloom Energy 放进跌幅榜）。所有入榜行 regularMarketTime 均为 10-26 当日，无停牌僵尸数据；TV 交叉验证涨跌幅全部一致（TTS.V 不在 TV 扫描榜但单票查询确认 -7.83%）。TV 跌幅榜 DLCG（NEO 行，最后成交 10-13）/SCHN（NEO 行，10-22）为陈旧数据，未采纳。",
 ],
 "sectors_html":(
  "<ul>"
  "<li><strong>大盘：TSX +0.44% 收 35,944（+156 点），周一反弹</strong>：黄金 +1%、金融 +0.8%、材料 +0.7% 领涨，金价回升 US$19 至 4,027；消费 -0.6%、科技/医疗各 -0.5% 拖累。加央行周三议息，Reuters 调查预期加息 25bp 至 2.50%；特朗普周日称美加贸易争端「很快」解决。美股方面 Anthropic 递交 IPO 申请点燃 AI 情绪，半导体反弹，标普 +0.7%、纳指 +0.8%；WTI 回落至 US$101。</li>"
  "<li><strong>涨幅榜主线一：并购事件 + 金矿反弹</strong>：High Liner Foods +77.5% 领涨——日本水产巨头 Umios 以每股 C$27 现金收购（股权估值 C$8.04 亿，企业价值 C$12.5 亿，溢价 80%，预计 2027 年 Q1 交割），成交 229 万股为均量 2.1 万股的 109 倍。黄金/贵金属随金价反弹占 11 席：PDI Gold +8.0%（上周五 -4.9% 后反弹）、Osisko Gold Group +5.8%、Benz +5.6%、Seabridge +5.4%、Goldsky +4.4%、Collective +4.3%；铜镍锂同涨：Ero Copper +4.0%、Magna Mining +4.0%、Sigma Lithium +4.0%、PMET +4.6%、Fireweed +4.8%；铀矿 IsoEnergy +6.3%。</li>"
  "<li><strong>涨幅榜主线二：油服 + 美股 CDR + 个股事件</strong>：油服板块继续走强——Precision Drilling +5.1%、Trican +3.8%、Pason +3.7%，榜外第 32 Calfrac +3.4% 创 52 周新高（量比 6.4）、Total Energy +3.2%；北美建筑承包 NOA +4.5%。CAE +4.6%（以 5 亿美元含债务向 SITA 出售航空运营软件业务 Flightscape）；Hammond Power +5.8%（AI 数据中心变压器需求）；Telesat +5.0% 连续两日上榜；HydroGraph +15.6% 连续第二日领涨（10/29 特别股东会审议美国重新注册）。CDR：Tesla +5.3%（Barclays 上调至增持、目标价 370→450，SpaceX 合并预期）、Lockheed Martin +5.2%（上调全年指引后延续）、GE Vernova +4.8%、Intel +4.1%（Anthropic IPO 带动半导体）、Lululemon +3.8%、Western Digital +3.6%。</li>"
  "<li><strong>跌幅榜主线一：矿业分化 + 财报前减仓</strong>：虽然金价反弹，部分银矿/小金矿逆势下跌——Highlander Silver -6.9%（77 万股）、Sailfish -5.5%、DPM Metals -5.1%（142 万股，10/28 财报前减仓）、Goldgroup -5.0%、Founders -4.9%、Serabi -4.2%（量比 3.2）、Lumina -4.2%、AbraSilver -3.2%、Snowline -2.9%、Altius -2.8%、Mayfair -2.7%、New Pacific -2.5%；白银 -0.6% 弱于黄金。Celestica -4.8%（盘后 Q3 财报，10/22 -12% 后 AI 资本开支疑虑未消）；Lithium Americas -2.8%、Xanadu -2.7%、Ballard -2.9%。Vital Infrastructure -5.8%（498 万股，量比 7.0，H 系列可转债 10/26 提前赎回完成，转股套利盘抛售）。</li>"
  "<li><strong>跌幅榜主线二：美股 CDR 跌幅集中于金融/电信/支付</strong>：Strategy CDR -4.2%（比特币回落）、Reddit -3.8%（连续第二日）、PayPal -3.7%（10/27 财报前）、Merck -3.7%（10/28 财报前）、Verizon -3.4%（SpaceX 入局无线担忧延续，量比 4.7）、Fiserv -3.2%、Netflix -2.9%、Robinhood -2.5%。加股消费/地产：Plaza Retail REIT -3.8%、Tilray -3.1%、Trisura -2.4%，榜外 Aritzia -2.3%、Extendicare -2.2%、Aclara -2.2%（量比 3.5，周五 +5.3% 后回吐）。</li>"
  "</ul>"),
 "anomalies_html":(
  "<ul>"
  "<li>🔥 <strong>HLF.TO High Liner Foods</strong> 量比 108.9（+77.5%）：日本 Umios Corporation（东证 1333）宣布以每股 C$27.00 现金收购全部股份，股权估值约 C$8.04 亿、企业价值 C$12.5 亿，较周五收盘 C$15 溢价 80%；总部留在新斯科舍，作为 Umios 北美核心平台。需股东、法院及加美反垄断批准，预计 2027 年 Q1 交割。收盘 C$26.76 与要约价差 0.9%，套利空间基本收窄；229 万股为均量 2.1 万股的 109 倍。</li>"
  "<li>⚠️ <strong>VITL-UN.TO Vital Infrastructure Property Trust</strong> 量比 7.0（-5.8%）：此前宣布的 H 系列可转换债券提前赎回于 10/26 完成，债券持有人转股后集中抛售，498 万单位为均量 71 万的 7 倍；无其他公告，11/11 盘后 Q3 财报。</li>"
  "<li>⚠️ <strong>CFW.TO Calfrac Well Services</strong> 量比 6.4（+3.4%，榜外第 32）：收 C$7.34 创 52 周新高，60 万股为均量 9.3 万股的 6.4 倍；油服板块集体走强（Precision +5.1%、Trican +3.8%、Pason +3.7%），油价维持 US$100 上方带动压裂服务需求预期。</li>"
  "<li>⚠️ <strong>VZ.TO Verizon（CDR）</strong> 量比 4.7（-3.4%）：SpaceX 据报谈判接入 8 万基站进军美国无线市场的担忧延续，电信三巨头连续两个交易日下跌；CDR 7.5 万份为均量 1.6 万份的 4.7 倍（基数小）。</li>"
  "<li>⚠️ <strong>ARA.TO Aclara Resources</strong> 量比 3.5（-2.2%，榜外第 35）：32 万股为均量 3.5 倍，周五 +5.3% 后回吐，无公司公告，稀土题材短线资金进出。</li>"
  "<li>⚠️ <strong>SBI.TO Serabi Gold</strong> 量比 3.2（-4.2%）：13.4 万股为均量 3.2 倍，无公告；小市值（2.5 亿）巴西金矿，在金价反弹日逆势下跌，疑似个别机构减仓。</li>"
  "<li>其余入榜股量比均 &lt;3：MTL.TO 2.2（+3.3%，榜外）、PD.TO 2.1（+5.1%）、VREO.CN 2.0（-2.5%）、TSAT.TO 1.8（+5.0%）、FISH.V 1.8（-5.5%）、PLZ-UN.TO 1.8（-3.8%）、PDI.TO 1.7（+8.0%）、DPM.TO 1.6（-5.1%）、SEA.TO 1.6（+5.4%）、NOA.TO 1.6（+4.5%）、CLS.TO 1.5（-4.8%）、NFLX.TO 1.5（-2.9%）。金矿反弹普遍量能温和，属金价驱动的板块性修复；Tesla CDR +5.3% 量比 1.4。</li>"
  "</ul>"),
 "digest":"TSX +0.44% 收 35,944（+156 点）：黄金 +1%/金融 +0.8% 领涨，加央行周三议息预期加息 25bp。High Liner Foods +77.5% 领涨（日本 Umios 每股 C$27 现金收购，量比 109🔥），HydroGraph +15.6%、PDI Gold +8.0%、IsoEnergy +6.3%，金矿/油服/CDR（Tesla +5.3% Barclays 上调、Lockheed +5.2%）齐涨；跌幅榜 Tintina -7.8%、Highlander Silver -6.9%、Vital REIT -5.8%（可转债赎回转股抛压，量比 7.0）、DPM -5.1%、Celestica -4.8%（盘后财报），美股 CDR 金融/电信/支付偏弱（Strategy -4.2%、Verizon -3.4% 量比 4.7）。",
}
json.dump(data, open(D + "2026-10-26.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in G: print(r)
print("---")
for r in L: print(r)
