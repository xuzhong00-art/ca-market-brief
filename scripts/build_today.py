# -*- coding: utf-8 -*-
"""Build data/2026-08-24.json from _proc.json + manual meta."""
import json

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
proc = json.load(open(D + "_proc.json", encoding="utf-8"))

META = {
 "LGC.V":("Lavras Gold","黄金勘探"),"TTS.V":("Tintina Mines","矿业勘探"),
 "BZ.V":("Benz Mining","黄金勘探"),"BRVO.V":("Bravo Mining","铂族/黄金"),
 "MFG.V":("Mayfair Gold","黄金开发"),"GRGD.TO":("Groupe Dynamite","服装零售"),
 "IAU.TO":("i-80 Gold","黄金"),"NG.TO":("NovaGold Resources","黄金"),
 "SEA.TO":("Seabridge Gold","黄金"),"SGML.V":("Sigma Lithium","锂矿"),
 "GORO.V":("Goldgroup Mining","黄金"),"VGC.TO":("Valor Gold","黄金勘探"),
 "NFG.V":("New Found Gold","黄金勘探"),"PDN.TO":("Paladin Energy","铀矿"),
 "CADY.TO":("Cadillac Mines","黄金"),"TECT.V":("Tectonic Metals","黄金勘探"),
 "MSA.TO":("Mineros S.A.","黄金"),"MOON.V":("Blue Moon Metals","铜锌"),
 "DC-A.TO":("Dundee Corp A","金融控股"),"ORV.TO":("Orvana Minerals","黄金"),
 "FDY.TO":("Faraday Copper","铜矿"),"WGO.V":("White Gold","黄金勘探"),
 "BTO.TO":("B2Gold","黄金"),"BHC.TO":("Bausch Health","制药"),
 "VMET.TO":("Versamet Royalties","贵金属权利金"),"TRI.TO":("Thomson Reuters","信息服务"),
 "ELO.TO":("Eloro Resources","银锡勘探"),"IMG.TO":("IAMGOLD","黄金"),
 "TLO.TO":("Talon Metals","镍矿"),"ATZ.TO":("Aritzia","服装零售"),
 "RM.TO":("Roxmore Resources","金属勘探"),
 "MU.NE":("Micron（CDR）","半导体·CDR"),"ASTL.TO":("Algoma Steel","钢铁"),
 "FTG.TO":("Firan Technology","航空电子"),"MAL.TO":("Magellan Aerospace","航空防务"),
 "BBD-B.TO":("Bombardier B","商务喷气机"),"SLG.V":("San Lorenzo Gold","黄金勘探"),
 "JOY.TO":("Journey Energy","油气"),"HPS-A.TO":("Hammond Power A","电力设备"),
 "XNDU.TO":("Xanadu Quantum","量子计算"),"UCU.V":("Ucore Rare Metals","稀土"),
 "CRDL.TO":("Cardiol Therapeutics","生物科技"),"ELVA.TO":("Electrovaya","锂电池"),
 "BLDP.TO":("Ballard Power","氢燃料电池"),"BB.TO":("BlackBerry","软件"),
 "AMD.TO":("AMD（CDR）","半导体·CDR"),"GOOS.TO":("Canada Goose","奢侈服饰"),
 "DFN.TO":("Dividend 15 Split A","分级基金"),"VNP.TO":("5N Plus","特种材料"),
 "TLRY.TO":("Tilray Brands","大麻"),"DF.TO":("Dividend 15 Split II","分级基金"),
 "ACX.TO":("ACT Energy Tech","油服钻井"),"ESI.TO":("Ensign Energy","油服钻井"),
 "NEO.TO":("Neo Performance","稀土磁材"),"BK.TO":("Canadian Banc A","分级基金"),
 "MDA.TO":("MDA Space","航天"),"MRE.TO":("Martinrea","汽车零部件"),
 "MG.TO":("Magna Intl","汽车零部件"),"PNG.V":("Kraken Robotics","海洋机器人"),
 "TMQ.TO":("Trilogy Metals","铜矿"),"IVN.TO":("Ivanhoe Mines","铜矿"),
 "GRID.TO":("Tantalus Systems","智能电网"),"HIVE.TO":("HIVE Digital","加密挖矿/算力"),
}
EXCLUDE = {"CF-PA.TO"}  # 优先股，剔除

def cap_s(c):
    if not c: return "–"
    return f"{c/1e9:.1f}B" if c >= 1e9 else f"{c/1e6:.0f}M"

def build(side, desc):
    rows = [r for r in proc[side] if "drop" not in r and r["sym"] not in EXCLUDE]
    rows.sort(key=lambda r: r["chg"], reverse=desc)
    out = []
    for i, r in enumerate(rows[:30], 1):
        name, sec = META.get(r["sym"], (str(r["name"])[:22], r.get("tv_sector") or "–"))
        chg = f"{r['chg']:+.2f}%"
        price = f"{r['price']:.2f}"
        out.append([i, r["sym"], name, price, chg, cap_s(r["cap"]), sec, r["vr"]])
    return out

data = {
 "date":"2026-08-24","weekday":"周一",
 "snapshot":"2026-08-24 10:05 ET · 开盘约35分钟",
 "market_state":"REGULAR",
 "vr_note":"量比 = 当日成交量 ÷（3个月日均量 × 已开盘时长占比≈9.9%）。⚠️ ≥3，🔥 ≥8。早盘窗口短，低流动性股票的量比易被少数几笔交易放大，解读需结合绝对成交额。",
 "gainers":build("gainers",True),
 "losers":build("losers",False),
 "table_notes":["*MU/AMD 为美股 CDR（加元对冲存托凭证），市值为美股母公司总市值，非加拿大挂牌流通值。"],
 "sectors_html":"<ul><li><strong>涨幅榜再度被贵金属包场（30 只中约 24 只金/银/矿）</strong>：金价维持 $4,600/oz 附近历史高位区，9 月降息预期 + 霍尔木兹海峡危机避险双驱动，金矿勘探小盘股弹性最大（LGC/BZ/MFG/IAU/NFG +5~19%）。铀（PDN）、锂（SGML）跟随。零售双雄 GRGD/ATZ 逆市上涨。</li><li><strong>跌幅榜三条主线</strong>：<ul><li><strong>芯片 CDR 领跌</strong>（MU -7.7%、AMD -4.2%）：美股芯片抛售延续，MU 8/26 财报前获利了结，叠加周一大盘因伊朗局势『economic D-Day』避险开局</li><li><strong>航空航天/工业回调</strong>（BBD.B/MAL/FTG/MDA/HPS.A -3~-7%）：前期强势的防务航天板块集体获利回吐，MAL/FTG 放量</li><li><strong>事件驱动</strong>：ASTL 电弧炉停产（8/17 电厂涡轮故障，最长 21 天）持续发酵续跌；银行分级基金 DFN/DF/BK 放量齐跌，杠杆结构放大回撤</li></ul></li></ul>",
 "anomalies_html":"<ul><li>🔥 <strong>LGC.V（量比 14.3，+19.1%）</strong>：新钻孔高品位金矿化结果（33.72 g/t Au × 7 米）叠加金价历史高位，小盘勘探股放量急拉，今日加股涨幅王。</li><li>🔥 <strong>TECT.V（量比 14.5，+3.6%）</strong>：阿拉斯加 Flat 金矿 4 万米钻探计划推进 + 财报窗口，勘探情绪高热。</li><li>🔥 <strong>ORV.TO（量比 14.3，+3.2%）</strong>：未见当日公告，金价驱动的小盘金矿放量，早盘窗口下量比可能失真。</li><li>🔥 <strong>BZ.V（量比 9.5，+8.6%）</strong>：连续第二日强势（上周五 +10%），Eric Sprott 持仓的金矿勘探股动能延续。</li><li>🔥 <strong>BK.TO（12.1，-3.3%）/ DFN.TO（11.0，-4.0%）/ DF.TO（6.0，-3.9%）</strong>：加拿大银行股分级基金（杠杆封闭式）集体放量下跌，A 类份额杠杆放大标的回撤，留意是否有分红调整公告。</li><li>⚠️ <strong>MAL.TO（7.7，-6.3%）</strong>：航空防务板块获利回吐中放量最大，未见单一公告。</li><li>⚠️ <strong>GOOS.TO（7.3，-4.1%）</strong>：奢侈品逆风 + 关税压力，投行看空后创新低区间。</li><li>⚠️ <strong>ASTL.TO（6.9，-7.3%）</strong>：电弧炉停产事件（预计最长 21 天，IESO 备用供电方案审批中）继续压制。</li><li>⚠️ <strong>FTG.TO（6.4，-7.3%）</strong>：连续第二日放量下跌（上周五 -6.1%），航空电子，未见新公告。</li><li>⚠️ <strong>MFG.V（6.5，+7.6%）</strong>：Fenn-Gib 金矿项目持续去风险化推进，随板块放量上行。</li></ul>",
 "digest":"贵金属再度包场涨幅榜（金价 $4,600 高位+避险），芯片 CDR 与航空航天领跌；🔥LGC 钻探+19%，分级基金放量齐跌"
}

with open(D + "2026-08-24.json","w",encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("gainers", len(data["gainers"]), "losers", len(data["losers"]))
for r in data["gainers"][:5]: print(r)
for r in data["losers"][:5]: print(r)
