# -*- coding: utf-8 -*-
import json
m = json.load(open("data/_merged.json", encoding="utf-8"))
sec = {
 "ITH.TO": "金矿开发(阿拉斯加)", "UCU.V": "稀土精炼", "ACT.TO": "塑料化学回收", "PPTA.TO": "金/锑开发(美国)", "GAU.TO": "金矿(加纳)",
 "HG.CN": "石墨烯材料", "HUT.TO": "比特币矿机/AI数据中心", "RKLB.TO": "航天发射(CDR)", "BTQ.NE": "量子/区块链", "COHR.TO": "光通信器件(CDR)",
 "KEEL.TO": "比特币矿机/数据中心", "TSAT.TO": "卫星通信", "ABNB.TO": "民宿平台(CDR)", "MSCL.TO": "生物科技", "XNDU.TO": "量子计算",
 "SLG.V": "金矿勘探(智利)", "OGG.V": "金矿勘探/权利金", "ARA.TO": "稀土开发", "AMD.TO": "AI芯片(CDR)", "ZVST.NE": "电力/数据中心供电(CDR)",
 "APPS.TO": "AI广告平台(CDR)", "CBRS.TO": "AI芯片(CDR)", "VNP.TO": "特种材料/半导体材料", "HIVE.TO": "比特币矿机/AI算力", "MAXX.CN": "天然氢/锂勘探",
 "LNF.TO": "家具零售", "GTII.CN": "美国大麻(MSO)", "SPCX.TO": "航天(SpaceX CDR)", "ASTL.TO": "钢铁", "SGML.V": "锂矿",
 "TSU.TO": "特种保险", "PXT.TO": "油气(哥伦比亚)", "IFP.TO": "木材", "NFI.TO": "客车制造", "ZDC.V": "安防监控塔租赁",
 "ALC.TO": "航运(五大湖)", "RFA.TO": "住房抵押贷款", "BDGI.TO": "基建服务(水力挖掘)", "DLCG.TO": "抵押贷款经纪", "BKNG.TO": "在线旅游(CDR)",
 "CAS.TO": "纸业/包装", "WSP.TO": "工程咨询", "AP-UN.TO": "办公REIT", "CRM.TO": "企业软件(CDR)", "ADEN.TO": "建材分销",
 "ALDE.V": "铜金勘探", "OTEX.TO": "企业软件", "TRI.TO": "信息服务", "INTU.TO": "财务软件(CDR)", "DCBO.TO": "企业学习SaaS",
 "WRN.TO": "铜金开发(育空)", "FTT.TO": "重型设备经销", "ISRG.TO": "手术机器人(CDR)", "HPS-A.TO": "电力变压器", "NFLX.TO": "流媒体(CDR)",
 "ACX.TO": "油服(钻井)", "SYK.TO": "医疗器械(CDR)", "ADBE.TO": "软件(CDR)", "T.TO": "电信", "HMM-A.TO": "电子机箱制造",
}
name = {
 "ITH.TO": "International Tower Hill", "UCU.V": "Ucore Rare Metals", "ACT.TO": "Aduro Clean Tech", "PPTA.TO": "Perpetua Resources", "GAU.TO": "Galiano Gold",
 "HG.CN": "HydroGraph Clean Power", "HUT.TO": "Hut 8", "RKLB.TO": "Rocket Lab CDR", "BTQ.NE": "BTQ Technologies", "COHR.TO": "Coherent CDR",
 "KEEL.TO": "Keel Infrastructure", "TSAT.TO": "Telesat", "ABNB.TO": "Airbnb CDR", "MSCL.TO": "Satellos Bioscience", "XNDU.TO": "Xanadu Quantum",
 "SLG.V": "San Lorenzo Gold", "OGG.V": "Osisko Gold Group", "ARA.TO": "Aclara Resources", "AMD.TO": "AMD CDR", "ZVST.NE": "Vistra CDR",
 "APPS.TO": "AppLovin CDR", "CBRS.TO": "Cerebras CDR", "VNP.TO": "5N Plus", "HIVE.TO": "HIVE Digital", "MAXX.CN": "Max Power Mining",
 "LNF.TO": "Leon's Furniture", "GTII.CN": "Green Thumb Industries", "SPCX.TO": "SpaceX CDR", "ASTL.TO": "Algoma Steel", "SGML.V": "Sigma Lithium",
 "TSU.TO": "Trisura Group", "PXT.TO": "Parex Resources", "IFP.TO": "Interfor", "NFI.TO": "NFI Group", "ZDC.V": "Zedcor",
 "ALC.TO": "Algoma Central", "RFA.TO": "RFA Financial", "BDGI.TO": "Badger Infrastructure", "DLCG.TO": "Dominion Lending Centres", "BKNG.TO": "Booking CDR",
 "CAS.TO": "Cascades", "WSP.TO": "WSP Global", "AP-UN.TO": "Allied Properties REIT", "CRM.TO": "Salesforce CDR", "ADEN.TO": "ADENTRA",
 "ALDE.V": "Aldebaran Resources", "OTEX.TO": "Open Text", "TRI.TO": "Thomson Reuters", "INTU.TO": "Intuit CDR", "DCBO.TO": "Docebo",
 "WRN.TO": "Western Copper and Gold", "FTT.TO": "Finning", "ISRG.TO": "Intuitive Surgical CDR", "HPS-A.TO": "Hammond Power", "NFLX.TO": "Netflix CDR",
 "ACX.TO": "ACT Energy Technologies", "SYK.TO": "Stryker CDR", "ADBE.TO": "Adobe CDR", "T.TO": "TELUS", "HMM-A.TO": "Hammond Manufacturing",
}
def cap(c):
    return "%.1fB" % (c / 1e9) if c >= 1e9 else "%dM" % round(c / 1e6)
def rows(lst):
    out = []
    for i, v in enumerate(lst, 1):
        s = v["sym"]
        out.append([i, s, name.get(s, v["name"]), "%.2f" % v["price"], "%+.2f%%" % v["chg"], cap(v["cap"]), sec.get(s, v.get("tvsector", "")), v["vr"]])
    return out
g, l = rows(m["g"]), rows(m["l"])
missing = [r[1] for r in g + l if r[1] not in sec]
print("missing sector:", missing)
d = {
 "date": "2026-11-06", "weekday": "周五",
 "snapshot": "2026-11-06 16:00 ET 收盘（本期为补跑：早上排程未执行，于当日晚间按收盘数据补生成）",
 "market_state": "CLOSED",
 "vr_note": "量比 = 当日全天成交量 ÷ 3个月日均量（收盘后补跑，开盘时长占比取 1.0）。CDR 行用 Yahoo .TO/.NE 挂牌 3 个月均量，基数小易放大。⚠️≥3，🔥≥8。",
 "gainers": g, "losers": l,
 "table_notes": [
  "CDR 行市值为美股母公司总市值（TradingView 口径），非加拿大挂牌份额。Yahoo 筛选器漏掉的 RKLB/COHR/ABNB/APPS/CBRS/SPCX/BKNG/CRM/INTU/ISRG/NFLX/SYK/ADBE 由 TradingView type=dr 查询补入，量比用 Yahoo v7 quote 补算。",
  "本期为收盘后补跑，涨跌幅与成交量为 11-06 全天数据。Yahoo 80+80 行全部 regularMarketTime=11-06，无停牌僵尸数据需剔除；TradingView 交叉验证涨跌幅全部一致。",
  "NEO:QBR.A（Quebecor A 类，+105%）为无流动性挂牌的异常打印，不计入榜单。",
 ],
 "sectors_html": (
  "<ul>"
  "<li><strong>大盘</strong>：TSX 综合指数收涨 0.52%（+184 点至 35,789），周线仍跌约 0.03%；美股技术性反弹——纳指 +1.1%、标普 +0.3%、道指 -0.5%，费城半导体指数 +4.2% 收复前日 -11% 的一小部分。10 月非农远超预期（失业率回落）压低降息预期，黄金回落 1% 至 $4,074，金矿股本日没有继续领涨。</li>"
  "<li><strong>涨幅榜主线一：AI/算力链超跌反弹（含 CDR 共 12 席）</strong>——Hut 8（+15.7%，前两日财报后累跌 ~28%，B. Riley 维持买入）、Keel（+12.9%）、HIVE（+9.1%）比特币矿机转 AI 数据中心三兄弟集体反弹；CDR 方面 Rocket Lab（+14.7%，11/9 财报前空头回补）、Coherent（+13.5%，市场重估 $200 亿 PhotonLink AI 光互连订单）、AMD（+10.6%）、Vistra（+10.4%）、AppLovin（+9.9%）、Cerebras（+9.9%）、SpaceX（+8.6%）全线修复；本土 Xanadu 量子（+11.9%）、BTQ（+13.9%）、5N Plus（+9.4%）跟涨。</li>"
  "<li><strong>涨幅榜主线二：美国本土关键矿产/金矿开发</strong>——International Tower Hill（+29.2%，阿拉斯加 Livengood 1,360 万盎司金矿，无公司公告、放量 3 倍）领涨；Perpetua（+17.5%）延续 11/4 Stibnite 新金锑矿体发现（109.7m @ 3.2g/t Au + 1.1% Sb）的追捧；Ucore（+19.6%）、Aclara（+10.7%）稀土概念反弹；Galiano（+17.1%）Q3 产金 40,922 盎司环比 +19%、经营现金流 $57M、AISC 降至 $2,346。</li>"
  "<li><strong>涨幅榜主线三：财报</strong>——Leon's Furniture（+8.9%）Q3 调整 EPS $0.74 同比 +14%（含 Edmonton 物业出售 $12.5M 收益）、维持 $0.24 派息，连续三季床垫品类增长；Green Thumb（+8.8%）美国大麻 MSO 财报后走强；Aduro（+18.0%）、HydroGraph（+16.8%）前一日财报/技术更新遭抛售后反弹。</li>"
  "<li><strong>跌幅榜主线一：财报暴雷</strong>——Trisura（-29.9%，创三年新低）Q3 净利 -32%、美国 Programs 业务意外赔付恶化致综合成本率升至 87.5%、多家券商下调目标价；Parex（-16.6%）Q3 虽产量跃升至 83,264 boe/d，但因价差扩大/能源成本/汇率下调 FFO 指引并上调资本开支，五日累跌 29%；NFI（-6.9%）Q3 营收 +14.5%、EBITDA +34% 但经营现金流 -$48M、电池召回相关减值，高开 $26.72 后反转杀跌；Interfor（-8.2%）Q3 净亏 $45.6M（含 $53.2M 减值），且 Q4 还要计 US$63M 反倾销税追溯费用，10 月木材价格回落 6-11%；Algoma Central（-6.7%）Q3 创纪录后「利好出尽」；Zedcor（-6.7%）EPS 低预期；Dominion Lending（-5.2%）Q3 调整 EPS $0.13 不及预期；Docebo（-3.7%）Q3 超预期但 $60M 特别股息靠举债引发争议。</li>"
  "<li><strong>跌幅榜主线二：高利率再定价</strong>——强劲非农推高美债收益率，利率敏感板块走弱：Allied Properties（-4.2%）、CAPREIT（-2.8%）REIT；RFA Financial（-6.3%）、Dominion Lending 房贷链；TELUS（-2.9%）电信；Thomson Reuters（-3.9%）、Open Text（-3.9%）等前日「防御性」科技回吐；WSP（-4.2%）、Finning（-3.6%）、Badger（-6.2%）工业服务获利了结。CDR 跌幅榜只有 Booking/Salesforce/Intuit/ISRG/Netflix/Stryker/Adobe 等防御型美股小幅走弱（-3~-5%），与前日 AI 链集体 -15% 的格局完全反转。</li>"
  "</ul>"),
 "anomalies_html": (
  "<ul>"
  "<li>🔥 <strong>TSU.TO</strong> 量比 16.4（-29.9%）：Trisura Q3 净利 $26.2M 同比 -32%、EPS $0.54 vs 去年 $0.79，美国 Programs 伤亡险（含清盘中项目）赔付恶化，损失率 36.4%（+2.1pt）；成交 140 万股 vs 日均 8.5 万，机构集中出逃至三年新低 $29.58。</li>"
  "<li>⚠️ <strong>ABNB.TO</strong> 量比 7.9（+12.6%）：Airbnb CDR 随美股财报后反弹（Q3 预订量超预期），.TO 挂牌日均仅 5.7K 股，基数小放大。</li>"
  "<li>⚠️ <strong>NFI.TO</strong> 量比 7.1（-6.9%）：Q3 收入 $1.0B（+14.5%）、调整 EBITDA $108.7M（+34%）、上调全年 EBITDA 下限至 $395M，但经营现金流 -$48M、电池电芯减值、杠杆率 2.79x，日内 $27.37→$23.52 大幅反转，196 万股为日均 7 倍。</li>"
  "<li>⚠️ <strong>LNF.TO</strong> 量比 6.9（+8.9%）：Leon's Q3 调整 EPS $0.74（+13.8%），物业出售 $12.5M 一次性收益，Luke Leon 升任 COO；平日流动性极低（日均 2 万股），财报日放量。</li>"
  "<li>⚠️ <strong>DLCG.TO</strong> 量比 5.6（-5.2%）：Q3 营收 +14%、调整 EBITDA +26% 至 $17.8M，但调整 EPS $0.13 低于预期、Filogix 并购后杠杆升至 1.86x，放量 5.6 倍下跌。</li>"
  "<li>⚠️ <strong>APPS.TO</strong> 量比 4.5（+9.9%）：AppLovin CDR 延续前日 +31% 财报行情，连续两日放量。</li>"
  "<li>⚠️ <strong>WRN.TO</strong> 量比 4.3（-3.7%）：Western Copper 11/2 提交 Casino 项目环评后连日放量，本日 151 万股为日均 4.3 倍，无新公告，疑获利盘/融资预期压制。</li>"
  "<li>⚠️ <strong>PXT.TO</strong> 量比 4.1（-16.6%）：Parex Q3 FFO $196M、净利 $75M 但下调 2026 财务指引（价差/能源成本/汇率）并上调资本开支，维持 C$0.385 季度股息；312 万股为日均 4 倍，五日累跌 29%。</li>"
  "<li>⚠️ <strong>DCBO.TO</strong> 量比 3.8（-3.7%）：Docebo Q3 调整 EPS $0.55 超预期、ARR +11%，但宣布举债 $60M 派特别股息 $2.42/股，市场对「借钱分红」分歧。</li>"
  "<li>⚠️ <strong>ITH.TO</strong> 量比 3.1（+29.2%）：International Tower Hill 无公司公告，Livengood 金矿可研/许可推进预期 + 美国本土关键矿产热度（Perpetua 新发现外溢），27 万股为日均 3 倍。</li>"
  "<li>⚠️ <strong>ALC.TO</strong> 量比 3.1（-6.7%）：Algoma Central Q3 营收 $287.8M、EBITDA +6%、自由现金流 +37%，10 月已预告创纪录业绩并派特别股息，财报日「利好出尽」；流动性极低（日均 9.5K 股）。</li>"
  "<li>⚠️ <strong>ZDC.V</strong> 量比 3.0（-6.7%）：Zedcor Q3 营收 $26.7M（+67%）、EBITDA $10.3M 均超预期，但净亏 $3.3M、EPS -$0.03 低于预期 +$0.012，11/5 电话会后次日放量回调。</li>"
  "</ul>"),
 "digest": "AI 链超跌反弹：Hut 8/Keel/HIVE、Rocket Lab/Coherent/AMD 等 CDR 占涨幅榜 12 席；ITH +29%、Perpetua +17% 美国本土金/锑矿热；跌幅榜财报暴雷——Trisura -30% 创三年新低（量比 16🔥）、Parex -17% 下调指引、NFI/Interfor/Algoma Central 高开低走；强非农压降息预期，REIT/房贷/电信走弱。",
}
json.dump(d, open("data/2026-11-06.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(g), len(l))
