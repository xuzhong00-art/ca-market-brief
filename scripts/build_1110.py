# -*- coding: utf-8 -*-
import json
m = json.load(open("data/_merged.json", encoding="utf-8"))
RATIO = 0.077
META = {
 "PET.TO": ("Pet Valu", "宠物零售"), "HG.CN": ("HydroGraph Clean Power", "石墨烯材料"), "CLS.TO": ("Celestica", "AI服务器/EMS"),
 "AMD.TO": ("AMD CDR", "AI芯片(CDR)"), "PEY.TO": ("Peyto Exploration", "天然气"), "AVGO.TO": ("Broadcom CDR", "AI芯片(CDR)"),
 "IAG.TO": ("iA Financial", "寿险/财富管理"), "BIR.TO": ("Birchcliff Energy", "天然气"), "CRWV.TO": ("CoreWeave CDR", "AI云算力(CDR)"),
 "VNP.TO": ("5N Plus", "特种材料/半导体"), "KEEL.TO": ("Keel Infrastructure", "基础设施软件"), "CHR.TO": ("Chorus Aviation", "区域航空/租赁"),
 "KRY.V": ("Koryx Copper", "铜矿开发(纳米比亚)"), "LBS.TO": ("Life & Banc Split", "分级基金"), "GWO.TO": ("Great-West Lifeco", "寿险"),
 "MRV.TO": ("Marvell CDR", "AI芯片(CDR)"), "AAV.TO": ("Advantage Energy", "天然气"), "DCBO.TO": ("Docebo", "企业学习SaaS"),
 "XNDU.TO": ("Xanadu Quantum", "量子计算"), "ANET.TO": ("Arista Networks CDR", "数据中心网络(CDR)"), "SOIL.TO": ("Saturn Oil & Gas", "油气"),
 "SNDK.TO": ("SanDisk CDR", "存储(CDR)"), "POW.TO": ("Power Corp", "金融控股"), "INTC.TO": ("Intel CDR", "半导体(CDR)"),
 "CEU.TO": ("CES Energy Solutions", "油服化学品"), "NFI.TO": ("NFI Group", "客车制造"), "TOU.TO": ("Tourmaline Oil", "天然气"),
 "HIVE.TO": ("HIVE Digital", "加密挖矿/算力"), "SPCX.TO": ("SpaceX CDR", "航天(CDR)"), "FSZ.TO": ("Fiera Capital", "资产管理"),
 "MUX.TO": ("McEwen Inc", "金矿/铜"), "WELL.TO": ("WELL Health", "数字医疗/诊所"), "QTRH.TO": ("Quarterhill", "智能交通系统"),
 "GFL.TO": ("GFL Environmental", "环保/垃圾处理"), "LGD.TO": ("Liberty Gold", "金矿开发"), "GAU.TO": ("Galiano Gold", "金矿(加纳)"),
 "TAU.V": ("Thesis Gold & Silver", "金银勘探"), "GEV.TO": ("GE Vernova CDR", "电力设备/燃气轮机(CDR)"), "ITR.V": ("Integra Resources", "金矿"),
 "VHI.TO": ("VitalHub", "医疗软件"), "HMMC.TO": ("Hemlo Mining", "金矿"), "SBI.TO": ("Serabi Gold", "金矿(巴西)"),
 "TALA.TO": ("Talamore Mining", "金属矿业"), "FDR.V": ("Founders Metals", "金矿勘探(苏里南)"), "NG.TO": ("NovaGold Resources", "金矿开发"),
 "OR.TO": ("OR Royalties", "贵金属权利金"), "APM.TO": ("Andean Precious Metals", "金银"), "ALDE.V": ("Aldebaran Resources", "铜矿勘探"),
 "BTO.TO": ("B2Gold", "金矿"), "SGD.TO": ("Snowline Gold", "金矿开发(育空)"), "USA.TO": ("Americas Gold & Silver", "银矿"),
 "ABRA.TO": ("AbraSilver Resource", "银矿开发(阿根廷)"), "GMIN.TO": ("G Mining Ventures", "金矿"), "KNT.TO": ("K92 Mining", "金矿(巴新)"),
 "DPM.TO": ("DPM Metals", "金矿/铜"), "SCZ.TO": ("Santacruz Silver", "银矿"), "MAI.TO": ("Mining Americas", "金银"),
 "FTT.TO": ("Finning International", "重型设备经销"), "SKE.TO": ("Skeena Resources", "金矿开发"), "PAAS.TO": ("Pan American Silver", "银矿"),
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
d = {
 "date": "2026-11-10", "weekday": "周二",
 "snapshot": "2026-11-10 10:00 ET · 开盘约30分钟",
 "market_state": "REGULAR",
 "vr_note": "量比 = 当日成交量 ÷（3个月日均量 × 已开盘时长占比≈7.7%）。⚠️≥3，🔥≥8。早盘窗口极短，低流动性股票/CDR 的量比易被少数几笔交易放大，解读需结合绝对成交额。",
 "gainers": g, "losers": l,
 "table_notes": [
  "CDR 行（AMD/Broadcom/CoreWeave/Marvell/Arista/SanDisk/Intel/SpaceX/GE Vernova）市值为美股母公司总市值（TradingView 口径），非加拿大挂牌份额；由 TradingView type=dr 查询补入，量比用 Yahoo v7 quote 补算。CDR 早盘涨跌幅以加拿大前收为基准，对美股当日走势的映射有滞后（如 AMD/AVGO CDR +4~6% 而美股盘前约 -1%），TradingView 延迟口径明显更低，解读需打折。",
  "Yahoo 80+80 行中剔除 2 只僵尸数据：TXG.TO（最后成交 11-02）、FWZ.V（最后成交 11-04）。TradingView 交叉验证：涨跌幅方向一致（TV 延迟 15 分钟，早盘波动大故幅度有差异）；NEO:QBR.A（+105%）/NEO:GFR（+38%）等 NEO 挂牌为旧打印，不计入；TV 独有的 ADEN/CTGO/MDA/KEY/DSV/NEO/SSRM/NXE/FVI 经 Yahoo 核对为当日小幅波动，不足以进榜。",
 ],
 "sectors_html": (
  "<ul>"
  "<li><strong>大盘</strong>：TSX 昨日大涨 657 点（+1.8%）创两个月新高后，今早低开 -0.7%（36,190）——美国 10 月 CPI 总体与核心均高于预期，市场已基本定价 12 月美联储加息并开始计入明年多次加息，美债收益率反弹；Brent 跌破 $90、黄金 -1.5% 至 ~$4,075，材料与能源板块承压；美股期货 S&P -0.6%、纳指 -1.2%，SoftBank 数据中心减记拖累 AI 基建链，Nvidia 因黄仁勋丑闻续跌。</li>"
  "<li><strong>涨幅榜主线一：财报驱动</strong>——Pet Valu（+6.5%）Q3 同店销售 +1.5%、净利润 +6%，防御性消费获追捧；Chorus Aviation（+3.3%）Q3 净利 $15.6M 同比 +46% 并上调指引、完成 SkyCare 收购；Peyto（+4.6%）Q3 业绩 + 2027 资本计划，月度股息上周已提至 $0.13；Docebo（+2.5%，量比 6.0）上周财报后宣布 $60M 特别股息延续反弹；iA Financial（+3.8%）/Great-West（+2.6%）/Power Corp（+2.3%）寿险三巨头在收益率反弹下走强。</li>"
  "<li><strong>涨幅榜主线二：天然气与油服</strong>——油价回落但天然气股逆势：Peyto、Birchcliff（+3.6%）、Advantage（+2.5%）、Tourmaline（+2.0%）、Saturn（+2.3%）、CES Energy（+2.1%）集体上榜，冬季取暖需求 + 加息预期下的现金流防御属性。</li>"
  "<li><strong>涨幅榜主线三：AI 链 CDR「惯性」上榜（9 席）</strong>——AMD（+5.8%）、Broadcom（+4.5%）、CoreWeave（+3.4%）、Marvell（+2.6%）、Arista（+2.3%）、SanDisk（+2.3%）、Intel（+2.1%）、SpaceX（+1.9%）均为 CDR，涨幅主要反映昨日美股收盘相对加拿大前收的补涨；美股盘前 AMD/AVGO 已回落约 1%、Micron/Marvell/SanDisk -3%，TradingView 延迟口径 AMD 仅 +2.1%、Marvell/SanDisk 已转负，本土 Celestica（+5.9%）昨日领涨科技反弹后续涨。谨慎看待。</li>"
  "<li><strong>跌幅榜主线一：财报暴雷</strong>——McEwen（-17.3%）Q3 每股亏 $0.60 vs 预期盈利 $0.19，营收 $43.6M 低于预期 16%，产量同比 -23%、成本超支；WELL Health（-11.1%）营收创纪录 $407M 但净亏 $135.5M（商誉减值 $67.5M + WELLSTAR 上市费用），2026 营收指引下修至 ~$15.8 亿；Quarterhill（-9.3%）营收 +9% 但净亏扩大至 $16.5M、经营现金流 -$8.6M；GFL（-8.7%）董事会一致拒绝私有化要约（曾要求 $58+/股未果），套利盘出逃。</li>"
  "<li><strong>跌幅榜主线二：贵金属全线回吐（跌幅榜 23 席）</strong>——CPI 过热推升加息预期与美元，黄金 -1.5%、白银同步走弱，昨日领涨的金银矿集体回吐：Liberty Gold（-6.0%）、Galiano（-5.9%）、Thesis（-5.5%）、Integra（-5.4%）、Hemlo（-5.3%）、Serabi（-5.1%）、NovaGold/OR Royalties（-4.8%）、B2Gold（-4.6%）、Snowline（-4.5%）、Americas G&S/AbraSilver/G Mining/K92/DPM/Santacruz/Skeena/Pan American（-4%~-4.5%）；TV 榜上 SSR Mining/Fortuna/Discovery 同步下跌。</li>"
  "<li><strong>跌幅榜其他</strong>：GE Vernova CDR（-5.5%，美股盘前 -9%）因 SoftBank 大额数据中心减记引发 AI 电力基建链抛售；Finning（-4.0%）重型设备经销随矿业回落；VitalHub（-5.4%）财报（11/12）前获利了结。</li>"
  "</ul>"
 ),
 "anomalies_html": (
  "<ul>"
  "<li>🔥 <strong>GEV.TO</strong> 量比 34.3（-5.5%）：GE Vernova CDR 早盘 15.2 万股（日均 5.7 万）放量杀跌，美股盘前 -9%——SoftBank 公布数据中心相关大额减记引发 AI 电力/基建链恐慌，叠加 CPI 过热推高收益率打压高负债 AI 基建股；CDR 跌幅尚未完全反映美股盘前幅度。</li>"
  "<li>🔥 <strong>QTRH.TO</strong> 量比 26.0（-9.3%）：Quarterhill Q3 营收 $43.2M（+9%，2022 年以来最高）、调整 EBITDA $3.9M，但净亏扩大至 $16.5M（每股 -$0.13 vs 预期 -$0.03）、经营现金流 -$8.6M；年初至今涨近 200% 后高位放量兑现，早盘 39 万股为日均 2 倍。</li>"
  "<li>🔥 <strong>WELL.TO</strong> 量比 24.0（-11.1%）：WELL Health Q3 营收 $407.4M 创纪录（+12%）、加拿大患者服务 EBITDA +82%，但净亏 $135.5M（HEALWELL 商誉减值 $67.5M + WELLSTAR 反向上市费 $24.4M + 可转债提前赎回损失），2026 营收指引下修至 ~$15.8 亿（美国业务疲软）；早盘 196 万股已达日均 1.9 倍。</li>"
  "<li>🔥 <strong>MUX.TO</strong> 量比 21.2（-17.3%）：McEwen Q3 每股亏 $0.60（预期 +$0.19），营收 $43.6M 低于预期 $51.9M，产量 22,852 GEO 同比 -23%——Gold Bar 管理失误 + 圣何塞矿创纪录降雪致处理低品位矿；AISC 高达 $3,414-3,725/oz。今日加股跌幅王。</li>"
  "<li>🔥 <strong>PET.TO</strong> 量比 16.4（+6.5%）：Pet Valu Q3 同店销售 +1.5%、净利润 +6%、调整后每股收益增长，防御性消费在加息预期下受追捧，早盘 21 万股超日均 1.3 倍。今日加股涨幅王。</li>"
  "<li>🔥 <strong>GFL.TO</strong> 量比 15.7（-8.7%）：GFL 董事会一致拒绝多方私有化要约、选择维持独立上市（此前要求 $58+/股，PE 财团拒绝加价），美股盘前 -14~15%，并购套利盘集中出逃，早盘 108 万股已超日均。</li>"
  "<li>🔥 <strong>SBI.TO</strong> 量比 14.0（-5.1%）：Serabi Gold 昨日 +5.9%（量比 23）今日随金价回吐，日均仅 4.3 万股的小盘金矿连续两日放量，无公司公告。</li>"
  "<li>🔥 <strong>CHR.TO</strong> 量比 11.1（+3.3%）：Chorus Aviation Q3 净利 $15.6M（+46%）、调整每股 $0.68 vs 去年 $0.60，上调指引（2027 零部件/合约飞行/MRO 收入 $265-300M，约为 2025 两倍），完成 $40M SkyCare 空中救护收购，昨日 +5.1% 后今日再放量。</li>"
  "<li>🔥 <strong>ANET.TO</strong> 量比 10.9（+2.3%）：Arista CDR 日均仅 3.4 万股，早盘 2.8 万股即放量，涨幅为昨日美股补涨，TV 口径仅 +0.5%。</li>"
  "<li>🔥 <strong>KRY.V</strong> 量比 9.2（+2.9%）：Koryx Copper 海布铜矿 PFS 预计 11 月内发布，赞比亚钻探进行中，无当日公告，小盘铜矿开发股 PFS 前放量。</li>"
  "<li>⚠️ <strong>AMD.TO</strong> 7.8（+5.8%）/ <strong>AVGO.TO</strong> 5.3（+4.5%）/ <strong>SNDK.TO</strong> 5.0（+2.3%）/ <strong>MRV.TO</strong> 3.0（+2.6%）/ <strong>SPCX.TO</strong> 3.1（+1.9%）：AI 链 CDR 昨日美股补涨 + 今日美股盘前回落交织，早盘放量换手，方向不稳。</li>"
  "<li>⚠️ <strong>VHI.TO</strong> 6.3（-5.4%）：VitalHub 11/12 盘后财报前放量下跌，无公告，软件股在收益率反弹下承压；<strong>DCBO.TO</strong> 6.0（+2.5%）：Docebo 上周财报 + $60M 特别股息（$2.42/股）后延续放量上行。</li>"
  "<li>⚠️ <strong>PEY.TO</strong> 5.3（+4.6%）：Peyto Q3 财报 + 2027 初步资本预算，电话会 10:00 ET 进行中，天然气板块领涨；<strong>BTO.TO</strong> 3.9（-4.6%）：B2Gold 早盘 125 万股随金价回落放量下跌；<strong>HIVE.TO</strong> 3.3（+2.0%）：比特币矿企随算力叙事波动；<strong>GAU.TO</strong> 3.1（-5.9%）/ <strong>OR.TO</strong> 3.0（-4.8%）：金矿/权利金随板块放量回吐。</li>"
  "</ul>"
 ),
 "digest": "CPI 过热→加息预期升温，TSX 低开 -0.7%，黄金 -1.5% 致贵金属占跌幅榜 23 席；财报暴雷：McEwen -17%🔥（每股亏 $0.60 vs 预期盈利）、WELL Health -11%🔥（减值致净亏 $135M + 指引下修）、Quarterhill -9%🔥；GFL -8.7%🔥 拒绝私有化要约；GE Vernova CDR -5.5% 量比 34🔥（SoftBank 数据中心减记）；涨幅榜 Pet Valu +6.5%🔥/Chorus +3.3%🔥 财报驱动，天然气股逆势，AI 链 CDR 补涨 9 席但美股盘前已回落。",
}
json.dump(d, open("data/2026-11-10.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(g), len(l))
