# -*- coding: utf-8 -*-
import json
m = json.load(open("data/_merged.json", encoding="utf-8"))
RATIO = 0.077
META = {
 "CRWV.TO": ("CoreWeave CDR", "AI云算力(CDR)"), "MAL.TO": ("Magellan Aerospace", "航空零部件"), "SNDK.TO": ("SanDisk CDR", "存储(CDR)"),
 "BE.TO": ("Bloom Energy CDR", "燃料电池/数据中心电力(CDR)"), "MU.TO": ("Micron CDR", "存储(CDR)"), "KEEL.TO": ("Keel Infrastructure", "基础设施软件"),
 "EPRX.TO": ("Eupraxia Pharmaceuticals", "生物科技"), "RAY.TO": ("Stingray Group", "流媒体/广播"), "SMCI.TO": ("Super Micro CDR", "AI服务器(CDR)"),
 "MRV.TO": ("Marvell CDR", "AI芯片(CDR)"), "INTC.TO": ("Intel CDR", "半导体(CDR)"), "RKLB.TO": ("Rocket Lab CDR", "航天发射(CDR)"),
 "AVGO.TO": ("Broadcom CDR", "AI芯片(CDR)"), "ORAC.TO": ("Oracle CDR", "云计算(CDR)"), "WDC.TO": ("Western Digital CDR", "存储(CDR)"),
 "HUT.TO": ("Hut 8", "加密挖矿/算力"), "VRT.TO": ("Vertiv CDR", "数据中心电力/散热(CDR)"), "ANET.TO": ("Arista Networks CDR", "数据中心网络(CDR)"),
 "CLS.TO": ("Celestica", "AI服务器/EMS"), "BB.TO": ("BlackBerry", "网络安全/车载软件"), "SOIL.TO": ("Saturn Oil & Gas", "油气"),
 "LRCX.TO": ("Lam Research CDR", "半导体设备(CDR)"), "ARG.TO": ("Amerigo Resources", "铜尾矿"), "PDN.TO": ("Paladin Energy", "铀矿"),
 "CCL-B.TO": ("CCL Industries", "标签/包装"), "BDT.TO": ("Bird Construction", "建筑工程"), "AMD.TO": ("AMD CDR", "AI芯片(CDR)"),
 "FRU.TO": ("Freehold Royalties", "油气权利金"), "HIVE.TO": ("HIVE Digital", "加密挖矿/算力"), "MATR.TO": ("Mattr", "管材/复合材料"),
 "GSY.TO": ("goeasy", "次级消费贷"), "BYD.TO": ("Boyd Group Services", "汽车碰撞维修"), "CFW.TO": ("Calfrac Well Services", "油服压裂"),
 "AIM.TO": ("Aimia", "投资控股"), "LAC.TO": ("Lithium Americas", "锂矿开发"), "ALS.TO": ("Altius Minerals", "矿业权利金"),
 "SPB.TO": ("Superior Plus", "丙烷/CNG分销"), "TOT.TO": ("Total Energy Services", "油服/压缩设备"), "TLRY.TO": ("Tilray Brands", "大麻"),
 "MUX.TO": ("McEwen Inc", "金矿/铜"), "BTB-UN.TO": ("BTB REIT", "商业地产REIT"), "EQX.TO": ("Equinox Gold", "金矿"),
 "SLI.V": ("Standard Lithium", "锂提取"), "LULU.TO": ("Lululemon CDR", "运动服饰(CDR)"), "GMIN.TO": ("G Mining Ventures", "金矿"),
 "NCX.V": ("NorthIsle Copper & Gold", "铜金勘探"), "HSTR.TO": ("Heliostar Metals", "金矿(墨西哥)"), "CAD.V": ("Colonial Coal", "冶金煤"),
 "SPCX.TO": ("SpaceX CDR", "航天(CDR)"), "CSH-UN.TO": ("Chartwell Retirement", "养老地产REIT"), "SXGC.TO": ("Southern Cross Gold", "金矿勘探(澳)"),
 "IFP.TO": ("Interfor", "木材"), "CIA.TO": ("Champion Iron", "铁矿"), "MCD.TO": ("McDonald's CDR", "快餐(CDR)"),
 "NFI.TO": ("NFI Group", "客车制造"), "QTRH.TO": ("Quarterhill", "智能交通系统"), "KNT.TO": ("K92 Mining", "金矿(巴新)"),
 "UBER.TO": ("Uber CDR", "网约车(CDR)"), "ABRA.TO": ("AbraSilver Resource", "银矿开发(阿根廷)"), "CRON.TO": ("Cronos Group", "大麻"),
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
 "date": "2026-11-11", "weekday": "周三",
 "snapshot": "2026-11-11 10:00 ET · 开盘约30分钟",
 "market_state": "REGULAR",
 "vr_note": "量比 = 当日成交量 ÷（3个月日均量 × 已开盘时长占比≈7.7%）。⚠️≥3，🔥≥8。早盘窗口极短，低流动性股票/CDR 的量比易被少数几笔交易放大，解读需结合绝对成交额。",
 "gainers": g, "losers": l,
 "table_notes": [
  "今日为加拿大国殇纪念日（Remembrance Day），TSX 正常交易；美股开市、美债休市。",
  "CDR 行（CoreWeave/SanDisk/Bloom/Micron/Super Micro/Marvell/Intel/Rocket Lab/Broadcom/Oracle/WD/Vertiv/Arista/Lam/AMD；Lululemon/SpaceX/McDonald's/Uber）市值为美股母公司总市值（TradingView 口径），非加拿大挂牌份额；由 TradingView type=dr 查询补入，量比用 Yahoo v7 quote 补算。SYK（Stryker CDR，-1.7%）因成交仅 393 股未达 15K 门槛剔除。",
  "Yahoo 80+80 行均为当日新鲜数据（无僵尸停牌行）；AMD.NE/NVDA.NE 为 .TO 的交叉挂牌重复已去重。TradingView 交叉验证：方向一致（TV 延迟 15 分钟，幅度有差）；TV 独有的 AIM（-10%）经 Yahoo 核实为当日有效补入；NEO:QBR.A（+105%）等 NEO 旧打印不计；TV 的 WELL/RIO/VZLA/PET 经 Yahoo 核对为小幅波动不足以进榜。",
 ],
 "sectors_html": (
  "<ul>"
  "<li><strong>大盘</strong>：昨日 TSX 在美国 10 月 CPI 过热（加息预期升温、10 年美债逼近 5%）下回落，Nvidia 因 CEO 丑闻连跌两日（-5.5%）拖累 AI 链；今早风向反转——CoreWeave 财报大超预期并上调全年指引、TSMC 10 月营收同比近 6 倍、Nvidia 盘前反弹，纳指期货 +1.5~1.9%，AI 交易重新点火。美股开市但美债休市（退伍军人节），加拿大国殇纪念日 TSX 照常交易。</li>"
  "<li><strong>涨幅榜主线一：AI 链 CDR 集体冲榜（15 席）</strong>——CoreWeave（+18.1%，量比 16.8）Q3 营收 +168% 至 $37 亿、积压订单 $1,325 亿、全年营收指引上调至 $130~133 亿；带动存储三杰 SanDisk（+11.7%）/Micron（+8.4%）/WD（+5.9%）、Bloom Energy（+10.3%）、Super Micro（+6.5%）、Marvell（+6.4%）、Intel（+6.2%）、Broadcom（+6.0%）、Oracle（+6.0%）、Vertiv（+5.3%）、Arista（+5.2%，量比 18.1）、Lam（+4.4%，量比 11.9）、AMD（+3.8%）；Rocket Lab（+6.2%）Q3 营收 +73% 创纪录、积压 $35.7 亿，昨日因亏损扩大下跌后今日反弹。CDR 早盘涨幅含对昨日美股收盘的补跌/补涨，解读需打折。本土 AI 链同步：Celestica（+4.9%）、Hut 8（+5.7%）、HIVE（+3.7%）、BlackBerry（+4.9%）。</li>"
  "<li><strong>涨幅榜主线二：本土财报驱动</strong>——Magellan Aerospace（+14.0%，量比 11.7）Q3 营收 $3.006 亿同比 +18%、净利 $2,000 万同比 +57%、经营现金流 $3,640 万（去年同期 $450 万），毛利率升至 14.7%；Stingray（+7.1%，量比 20.4）FY27 Q2 营收 +51% 至 $1.714 亿、调整后 EBITDA +47.5%、自由现金流 $3,900 万，TuneIn 整合超预期；Freehold（+3.8%，量比 4.8）Q3 FFO +37%、派息率 55%，并宣布收购 West Duvernay 3% 总收益权利金；Eupraxia（+7.4%，量比 10.4）Q3 财报确认 RESOLVE 2b 期 12 月出中期数据、现金跑道至 2028 下半年，同日设 $1.25 亿 ATM。</li>"
  "<li><strong>涨幅榜其他</strong>：油气板块延续走强（Saturn +4.5%、Kelt/Strathcona/Vermilion 榜外小涨），Paladin（+3.8%，量比 3.7）铀矿随核电主题反弹，Amerigo（+4.1%）铜价企稳，CCL（+3.8%）财报后续涨，Keel（+8.1%）低价股高波动。</li>"
  "<li><strong>跌幅榜主线一：财报暴雷（量比最高集中区）</strong>——goeasy（-14.4%，量比 35.2 🔥）Q3 每股亏损 $1.03（Q2 为盈利 $0.96）、贷款余额环比 -2%、总收益率下滑，年内已跌 66% 后再创新低；Boyd Group（-12.6%，量比 13.3 🔥）Q3 调整后 EPS $0.68 远低于预期 $0.85、净利仅 $0.1 万（折旧与财务费用吞噬 28% 的营收增长）；Calfrac（-10.6%，量比 5.8）Q3 净利 $1,630 万、EPS $0.16 略低于预期 $0.17，且警示 Q4 客户排程调整致利用率下滑超预期；Superior Plus（-5.6%，量比 9.4 🔥）将 2026 调整后 EBITDA 指引从 +2% 下修至 -2%，丙烷业务拖累抵消 CNG 创纪录季度；Total Energy（-4.5%，量比 5.6）虽创纪录经营现金流 $1.126 亿但 $1,590 万股权激励费用压利润，年内大涨后获利了结；BTB REIT（-2.8%，量比 12.8 🔥）Q3 FFO 每单位 9.3¢ 同比 -19%、派息率升至 80.6%；McEwen（-3.3%，量比 6.3）昨日暴雷后续跌。</li>"
  "<li><strong>跌幅榜主线二：资本开支与项目风险</strong>——Lithium Americas（-7.8%，量比 13.0 🔥）Thacker Pass 一期确定性资本估算从 $29.3 亿上修至 $38.3 亿（+31%），需与 DOE/GM 重新敲定合资股比，潜在稀释压力；Standard Lithium（-2.3%）锂板块联动走弱。Aimia（-10.0%，量比 22.4 🔥）无当日新闻，11/6 Q3 亏损（Clear Media 公允价值损失 $830 万）后低流动性股放量下跌，TV 独有行经 Yahoo 核实补入。</li>"
  "<li><strong>跌幅榜主线三：贵金属小幅回吐 + 防御股</strong>——金价在加息预期下继续承压，Equinox（-2.6%）、G Mining（-2.1%）、Heliostar/Southern Cross/K92/AbraSilver（-1~-2%）温和下跌；Altius（-5.7%）矿业权利金随贵金属与铁矿回落；消费防御型 CDR（Lululemon -2.1%、McDonald's -1.5%、Uber -1.1%）与养老地产 Chartwell（-1.7%）在风险偏好回升时被轮出；大麻股 Tilray（-4.0%）/Cronos（-1.0%）延续弱势。</li>"
  "</ul>"
 ),
 "anomalies_html": (
  "<ul>"
  "<li>🔥 <strong>GSY.TO goeasy</strong>（量比 35.2，-14.4%）：Q3 转亏每股 -$1.03、贷款余额收缩，次级消费贷信用周期恶化，放量破位。</li>"
  "<li>🔥 <strong>AIM.TO Aimia</strong>（量比 22.4，-10.0%）：无当日公告，Q3 亏损（11/6）后低流动性放量下跌，绝对成交仅 6.7 万股，解读需打折。</li>"
  "<li>🔥 <strong>RAY.TO Stingray</strong>（量比 20.4，+7.1%）：FY27 Q2 营收 +51%、EBITDA +47.5%，TuneIn 整合超预期。</li>"
  "<li>🔥 <strong>ANET.TO Arista CDR</strong>（量比 18.1，+5.2%）：AI 网络需求随 CoreWeave 财报重燃，CDR 日均量小易放大。</li>"
  "<li>🔥 <strong>CRWV.TO CoreWeave CDR</strong>（量比 16.8，+18.1%）：Q3 营收 +168%、全年指引上调，美股盘前 +15~17%。</li>"
  "<li>🔥 <strong>BYD.TO Boyd Group</strong>（量比 13.3，-12.6%）：Q3 调整后 EPS $0.68 vs 预期 $0.85，折旧与利息费用吞噬增长。</li>"
  "<li>🔥 <strong>LAC.TO Lithium Americas</strong>（量比 13.0，-7.8%）：Thacker Pass 资本估算上修 31% 至 $38.3 亿，合资股比待重谈。</li>"
  "<li>🔥 <strong>BTB-UN.TO BTB REIT</strong>（量比 12.8，-2.8%）：Q3 FFO/单位 -19%，派息率升至 80.6%。</li>"
  "<li>🔥 <strong>LRCX.TO Lam Research CDR</strong>（量比 11.9，+4.4%）：半导体设备随 AI 链反弹，CDR 小盘量易放大。</li>"
  "<li>🔥 <strong>MAL.TO Magellan Aerospace</strong>（量比 11.7，+14.0%）：Q3 净利 +57%、经营现金流 $3,640 万，航空零部件需求强劲。</li>"
  "<li>🔥 <strong>RKLB.TO Rocket Lab CDR</strong>（量比 11.6，+6.2%）：Q3 营收 +73% 创纪录、积压 $35.7 亿，昨日下跌后反弹。</li>"
  "<li>🔥 <strong>EPRX.TO Eupraxia</strong>（量比 10.4，+7.4%）：Q3 财报 + RESOLVE 2b 期 12 月中期数据预期，同日设 $1.25 亿 ATM。</li>"
  "<li>🔥 <strong>AMD.TO AMD CDR</strong>（量比 9.9，+3.8%）：AI 芯片反弹，CDR 加币对冲成交活跃。</li>"
  "<li>🔥 <strong>SPB.TO Superior Plus</strong>（量比 9.4，-5.6%）：2026 EBITDA 指引由 +2% 下修至 -2%，丙烷拖累。</li>"
  "<li>🔥 <strong>SNDK.TO SanDisk CDR</strong>（量比 8.9，+11.7%）：存储板块随 AI 链反弹，昨日美股 SanDisk +6%。</li>"
  "<li>🔥 <strong>AVGO.TO Broadcom CDR</strong>（量比 8.3，+6.0%）：AI 芯片龙头随 CoreWeave 财报反弹。</li>"
  "<li>⚠️ MU.TO（7.6，+8.4%）、VRT.TO（6.4，+5.3%）、MUX.TO（6.3，-3.3%）、CFW.TO（5.8，-10.6%）、MRV.TO（5.7，+6.4%）、TOT.TO（5.6，-4.5%）、ORAC.TO（5.4，+6.0%）、INTC.TO（4.9，+6.2%）、FRU.TO（4.8，+3.8%）、LULU.TO（4.8，-2.1%）、CRON.TO（4.8，-1.0%）、SPCX.TO（4.7，-1.7%）、BE.TO（4.6，+10.3%）、SMCI.TO（4.5，+6.5%）、QTRH.TO（4.4，-1.2%）、BB.TO（4.3，+4.9%）、TLRY.TO（4.2，-4.0%）、CAD.V（4.0，-1.7%）、PDN.TO（3.7，+3.8%）、MSFT.TO（3.4，-1.1%）、CLS.TO（3.2，+4.9%）、WDC.TO（3.1，+5.9%）：多为 AI 链 CDR 跟随美股反弹的早盘放量，以及本土财报后的持续换手（Calfrac/Total Energy/McEwen/Quarterhill）。</li>"
  "</ul>"
 ),
 "digest": "AI 交易重燃：CoreWeave 财报超预期带动 15 只 AI 链 CDR 冲榜（CRWV +18%、SNDK +12%、MU +8%）；本土 Magellan +14%/Stingray +7% 财报大超预期；跌幅榜财报暴雷集中——goeasy -14%（Q3 转亏，量比 35）、Boyd -13%（EPS 大幅不及）、Calfrac -11%、Lithium Americas -8%（Thacker Pass 资本上修 31%）。",
}
json.dump(d, open("data/2026-11-11.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written")
