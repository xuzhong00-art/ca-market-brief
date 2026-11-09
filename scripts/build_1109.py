# -*- coding: utf-8 -*-
import json
m = json.load(open("data/_merged.json", encoding="utf-8"))
RATIO = 0.077  # ~30 min open / 6.5h
META = {
 "GFR.TO": ("Greenfire Resources", "油砂(SAGD)"), "BE.TO": ("Bloom Energy CDR", "燃料电池/数据中心供电(CDR)"),
 "UCU.V": ("Ucore Rare Metals", "稀土精炼"), "AMD.TO": ("AMD CDR", "AI芯片(CDR)"), "HG.CN": ("HydroGraph Clean Power", "石墨烯材料"),
 "PDN.TO": ("Paladin Energy", "铀矿"), "VRT.TO": ("Vertiv CDR", "数据中心散热/电源(CDR)"), "ANET.TO": ("Arista Networks CDR", "数据中心网络(CDR)"),
 "WDC.TO": ("Western Digital CDR", "存储(CDR)"), "MRV.TO": ("Marvell CDR", "AI芯片(CDR)"), "AVGO.TO": ("Broadcom CDR", "AI芯片(CDR)"),
 "MOON.V": ("Blue Moon Metals", "铜锌"), "HBM.TO": ("Hudbay Minerals", "铜矿"), "LRCX.TO": ("Lam Research CDR", "半导体设备(CDR)"),
 "GEV.TO": ("GE Vernova CDR", "电力设备/燃气轮机(CDR)"), "SGD.TO": ("Snowline Gold", "金矿开发(育空)"), "BDT.TO": ("Bird Construction", "建筑工程"),
 "ABRA.TO": ("AbraSilver Resource", "银矿开发(阿根廷)"), "FDY.TO": ("Faraday Copper", "铜矿开发"), "VBNK.TO": ("VersaBank", "数字银行"),
 "SPCX.TO": ("SpaceX CDR", "航天(CDR)"), "CLS.TO": ("Celestica", "AI服务器/EMS"), "SBI.TO": ("Serabi Gold", "金矿(巴西)"),
 "FWZ.TO": ("Fireweed Metals", "锌/钨开发"), "TALA.TO": ("Talamore Mining", "金属矿业"), "LUNR.TO": ("LunR Royalties", "矿业权利金"),
 "NICU.TO": ("Magna Mining", "镍铜(萨德伯里)"), "SNDK.TO": ("SanDisk CDR", "存储(CDR)"), "TKO.TO": ("Trekor Metals", "铜矿"),
 "HSLV.TO": ("Highlander Silver", "银矿勘探"),
 "PBL.TO": ("Pollard Banknote", "彩票印刷/iLottery"), "RBY.TO": ("Rubellite Energy", "油气(重油)"), "NVDA.TO": ("NVIDIA CDR", "AI芯片(CDR)"),
 "CURA.TO": ("Curaleaf", "美国大麻(MSO)"), "LMN.V": ("Lumine Group", "垂直软件(通信)"), "MSTR.TO": ("Strategy CDR", "比特币财库(CDR)"),
 "TLRY.TO": ("Tilray Brands", "大麻"), "OBE.TO": ("Obsidian Energy", "油气"), "DIV.TO": ("Diversified Royalty", "品牌权利金"),
 "CSH-UN.TO": ("Chartwell Retirement", "养老地产REIT"), "IFP.TO": ("Interfor", "木材"), "TRI.TO": ("Thomson Reuters", "信息服务"),
 "VET.TO": ("Vermilion Energy", "油气"), "BTE.TO": ("Baytex Energy", "油气"), "CGG.TO": ("China Gold Intl", "金/铜矿(中国)"),
 "MFI.TO": ("Maple Leaf Foods", "食品加工"), "SCR.TO": ("Strathcona Resources", "油砂/重油"), "SU.TO": ("Suncor Energy", "综合油气"),
 "GTII.CN": ("Green Thumb Industries", "美国大麻(MSO)"), "CCL-B.TO": ("CCL Industries", "标签/包装"), "ENGH.TO": ("Enghouse Systems", "企业软件"),
 "CJ.TO": ("Cardinal Energy", "油气"), "DSG.TO": ("Descartes Systems", "物流软件"), "GIB-A.TO": ("CGI Inc", "IT服务"),
 "CAS.TO": ("Cascades", "纸业/包装"), "KEL.TO": ("Kelt Exploration", "油气"), "CCA.TO": ("Cogeco Communications", "有线电信"),
 "BCE.TO": ("BCE", "电信"), "CAR-UN.TO": ("CAPREIT", "公寓REIT"), "T.TO": ("TELUS", "电信"),
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
 "date": "2026-11-09", "weekday": "周一",
 "snapshot": "2026-11-09 10:00 ET · 开盘约30分钟",
 "market_state": "REGULAR",
 "vr_note": "量比 = 当日成交量 ÷（3个月日均量 × 已开盘时长占比≈7.7%）。⚠️≥3，🔥≥8。早盘窗口极短，低流动性股票/CDR 的量比易被少数几笔交易放大，解读需结合绝对成交额。",
 "gainers": g, "losers": l,
 "table_notes": [
  "CDR 行（Bloom/AMD/Vertiv/Arista/WDC/Marvell/Broadcom/Lam/GE Vernova/SpaceX/SanDisk/NVIDIA/Strategy）市值为美股母公司总市值（TradingView 口径），非加拿大挂牌份额；由 TradingView type=dr 查询补入，量比用 Yahoo v7 quote 补算。",
  "Yahoo 80+80 行中剔除 2 只僵尸数据：GWO-PN.TO（优先股，最后成交 11-06）、LB.TO（最后成交 11-03）。TradingView 交叉验证：涨跌幅方向与幅度一致（TV 延迟 15 分钟略有差异）；NEO:QBR.A（+105%）/NEO:UCU（+18%）等 NEO 挂牌为 11-06 旧打印，不计入。",
 ],
 "sectors_html": (
  "<ul>"
  "<li><strong>大盘</strong>：TSX 期货高开——油价回落（WTI ~$90.7、Brent ~$97）缓和通胀担忧，黄金小幅反弹至 $4,075-4,110；美股方面 Nvidia 因董事会调查 CEO 黄仁勋与涉嫌中国间谍关系而独跌 5-6%，但上周被「民主党控制国会→数据中心监管」叙事砸出的 AI 链其余环节继续技术反弹。本周关注美国 CPI。</li>"
  "<li><strong>涨幅榜主线一：并购套利</strong>——Greenfire Resources（+37.9%）周日被 Strathcona 以 C$11 现金或 0.25 股 SCR 收购（含债务估值 C$27-29 亿，现金对价较周五收盘溢价 39%），Waterous 基金同时控股双方（72%/57%）已承诺投票赞成，股价直接贴到 $10.94 套利区间；收购方 Strathcona（-1.3%）出现在跌幅榜。</li>"
  "<li><strong>涨幅榜主线二：AI/算力链 CDR 反弹（13 席）</strong>——上周四 AMD -17%/NVDA -9% 的恐慌性抛售后连续第二日修复：Bloom Energy（+12.0%）、AMD（+8.4%）、Vertiv（+7.8%）、Arista（+7.7%）、Western Digital（+7.7%）、Marvell（+7.2%）、Broadcom（+7.2%）、Lam Research（+6.3%）、GE Vernova（+6.3%）、SpaceX（+5.9%）、SanDisk（+5.7%）；本土 Celestica（+5.9%）跟涨。唯一例外是 NVIDIA CDR（-4.4%）因黄仁勋丑闻领跌跌幅榜。</li>"
  "<li><strong>涨幅榜主线三：基本金属/铀/贵金属</strong>——铜价维持高位带动 Hudbay（+6.8%）、Blue Moon（+7.0%）、Faraday（+6.1%）、Trekor（+5.7%）、Magna Mining（+5.7%）；TV 榜上 Teck.B（+5.3%）、Ero（+5.6%）、Lundin（+5.1%）、Coeur（+5.6%）同步上行；铀矿 Paladin（+8.1%）；金银 Snowline（+6.3%）、AbraSilver（+6.2%）、Serabi（+5.9%）、Highlander（+5.6%）随金价反弹；Ucore（+9.4%）稀土延续上周。</li>"
  "<li><strong>跌幅榜主线：早盘跌幅普遍温和（除 PBL/NVDA 外均 <5%）</strong>——Pollard Banknote（-8.6%）周五盘后 Q3 调整 EBITDA $28.3M 同比 -$4.0M、Michigan iLottery 合同 7 月到期拖累，周一首个交易日放量杀跌；油价回落压制能源股 Rubellite（-4.8%）、Obsidian（-2.5%）、Vermilion/Baytex/Suncor/Cardinal/Kelt（-1~-2%）；大麻股 Curaleaf（-4.2%）、Tilray（-2.7%）、Green Thumb（-1.3%）回吐；比特币财库 Strategy CDR（-2.7%）；电信 BCE/TELUS/Cogeco 与 REIT（Chartwell/CAPREIT）在利率担忧下小幅走弱；软件 Lumine/Enghouse/Descartes/CGI 延续上周防御性科技回吐。</li>"
  "</ul>"
 ),
 "anomalies_html": (
  "<ul>"
  "<li>🔥 <strong>GFR.TO</strong> 量比 64.5（+37.9%）：Strathcona 周日宣布以 C$11 现金 / 0.25 股 SCR 收购 Greenfire，含债务估值 C$27-29 亿，现金对价溢价 39%；Waterous 基金控股双方已锁定投票，股价一步到位贴近套利价，开盘 30 分钟成交 128 万股（日均 26 万）。</li>"
  "<li>🔥 <strong>PBL.TO</strong> 量比 39.7（-8.6%）：Pollard Q3 营收 $158.9M（+1.7%）但调整 EBITDA $28.3M 同比 -12%，Michigan iLottery 合同 7/17 到期损失 $2.1M EBITDA、即开型彩票均价下降；平日日均仅 1.4 万股，4.4 万股即放量 40 倍。</li>"
  "<li>🔥 <strong>SBI.TO</strong> 量比 23.0（+5.9%）：Serabi Gold 无当日公告，巴西金矿随金价反弹，日均 4.2 万股的小盘股早盘 7.4 万股放量。</li>"
  "<li>🔥 <strong>NVDA.TO</strong> 量比 20.7（-4.4%）：Nvidia 董事会周日就 CEO 黄仁勋与被指为中国间谍的 MegaSpeed 高管 Alice Huang 的关系启动独立调查，黄仁勋致员工信承认婚外情；美股 -5~6%，CDR 159 万股为日均 1.6 倍（全天口径）。11/17 财报前领导层不确定性成最大风险。</li>"
  "<li>🔥 <strong>ANET.TO</strong> 量比 14.4（+7.7%）：Arista CDR 随 AI 网络链反弹，上周财报后超跌。</li>"
  "<li>🔥 <strong>GEV.TO</strong> 量比 10.0（+6.3%）/ <strong>LRCX.TO</strong> 9.6（+6.3%）/ <strong>AMD.TO</strong> 9.4（+8.4%）/ <strong>VRT.TO</strong> 8.2（+7.8%）/ <strong>SNDK.TO</strong> 8.4（+5.7%）：AI 数据中心链 CDR 集体放量反弹，AMD 上周四 -17% 后连续两日修复（累计 ~+19%），Vertiv/GE Vernova 为数据中心电力/散热「铲子股」。</li>"
  "<li>🔥 <strong>VBNK.TO</strong> 量比 8.7（+6.0%）：VersaBank 无当日公告，数字银行小盘股（日均 3.5 万股）早盘 2.3 万股即放量，留意是否有财报预告/美国业务消息。</li>"
  "<li>🔥 <strong>DIV.TO</strong> 量比 8.6（-2.0%）：Diversified Royalty 早盘 37.7 万股（日均 57 万），TV 口径仅 -0.25%，Yahoo -2.0% 疑为单笔大宗压价，解读保留。</li>"
  "<li>⚠️ <strong>GFR 收购方 SCR.TO</strong> 量比 4.6（-1.3%）：Strathcona 将发行 4,300-6,000 万新股（占合并后 17-22%）并支付最多 C$7.4 亿现金，市场对稀释小幅定价。</li>"
  "<li>⚠️ <strong>BE.TO</strong> 6.5（+12.0%）/ <strong>WDC.TO</strong> 6.2（+7.7%）/ <strong>AVGO.TO</strong> 6.0（+7.2%）/ <strong>CSH-UN.TO</strong> 6.6（-1.9%）/ <strong>SPCX.TO</strong> 5.2（+5.9%）/ <strong>BTE.TO</strong> 3.3（-1.6%）/ <strong>CJ.TO</strong> 3.4（-1.1%）等：早盘窗口放量，其中 Bloom Energy 为数据中心燃料电池概念 + 民主党胜选后清洁能源政策预期双重驱动；Chartwell 无公告。</li>"
  "<li>⚠️ <strong>HG.CN</strong> 5.8（+8.2%）：HydroGraph 石墨烯材料延续上周财报后反弹；<strong>PDN.TO</strong> 4.9（+8.1%）：Paladin 铀矿随铀价/澳洲盘走强；<strong>RBY.TO</strong> 4.2（-4.8%）：Rubellite 重油小盘股随油价回落放量下跌；<strong>MSTR.TO</strong> 4.1（-2.7%）：Strategy CDR 随比特币走弱。</li>"
  "</ul>"
 ),
 "digest": "Greenfire +38% 被 Strathcona 溢价 39% 收购（量比 65🔥）；AI 链 CDR 连续第二日反弹占涨幅榜 13 席（Bloom +12%、AMD +8%、Vertiv/Arista/WDC/Marvell/Broadcom +7%），唯 NVIDIA CDR -4.4% 因黄仁勋间谍丑闻调查领跌；铜/铀/金银矿跟涨；Pollard Banknote -8.6% 财报 EBITDA 下滑放量 40 倍🔥；油价回落压能源股。",
}
json.dump(d, open("data/2026-11-09.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(g), len(l))
