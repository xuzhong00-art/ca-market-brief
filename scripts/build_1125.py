# -*- coding: utf-8 -*-
"""Build data/2026-11-25.json from data/_merged.json. Late run ~13:10 ET (opened ~3h40m), FRAC=0.56."""
import json
M = json.load(open("data/_merged.json", encoding="utf-8"))
OUT = "data/2026-11-25.json"
FRAC = 0.56

def fmtcap(c, cdr=False):
    if not c: return "?"
    s = f"{c/1e9:.1f}B" if c >= 1e9 else f"{c/1e6:.0f}M"
    return s + ("*" if cdr else "")

SEC = {
 "FDR.V":"黄金勘探(苏里南)","VRNO.NE":"美国大麻(MSO)","MARI.TO":"铜开发(智利)","ASTL.TO":"钢铁","IVN.TO":"铜(刚果金)",
 "KEL.TO":"油气(蒙尼)","MOON.V":"钨/铜锌(美国/挪威)","LUNR.TO":"矿业权利金","FDY.TO":"铜开发(亚利桑那)","GMIN.TO":"黄金生产(巴西/圭亚那)",
 "SCZ.TO":"银矿(玻利维亚)","VNP.TO":"特种半导体材料","ANTH.TO":"AI模型 CDR","APM.TO":"贵金属(玻利维亚/加州)","AMX.V":"黄金勘探(魁北克)",
 "LNR.TO":"汽车零部件","CNL.TO":"黄金勘探(哥伦比亚)","TOU.TO":"天然气(龙头)","IBM.TO":"IT服务 CDR","BIR.TO":"天然气",
 "VET.TO":"油气(国际)","AYA.TO":"银矿(摩洛哥)","TCL-A.TO":"印刷包装","GTII.CN":"美国大麻(MSO)","CADY.TO":"黄金勘探(魁北克)",
 "IE.TO":"铜矿开发(美国)","SDE.TO":"油气(蒙尼/杜弗奈)","VZLA.TO":"银矿开发(墨西哥)","ESI.TO":"油服(钻井)","NKE.TO":"运动服饰 CDR",
 "DSV.TO":"银矿开发(墨西哥)","HD.TO":"家居零售 CDR","CAD.V":"煤炭(BC省)","ADEN.TO":"建材分销","QBR-B.TO":"电信/媒体","HPS-A.TO":"电力变压器",
 "SNDK.TO":"存储 CDR","MU.TO":"存储芯片 CDR","LRCX.TO":"半导体设备 CDR","CLS.TO":"AI服务器/电子制造","AMAT.TO":"半导体设备 CDR",
 "NVDA.TO":"AI芯片 CDR","NBIS.TO":"AI云算力 CDR","LUME.TO":"光通信器件 CDR","ANET.TO":"网络设备 CDR","AMD.TO":"AI芯片 CDR",
 "WDC.TO":"存储 CDR","BE.TO":"燃料电池 CDR","INTC.TO":"芯片 CDR","CRWD.TO":"网络安全 CDR","TALA.TO":"黄金勘探",
 "MRV.TO":"数据中心芯片 CDR","ORAC.TO":"软件/云 CDR","GORO.V":"黄金(墨西哥)","ASML.TO":"光刻机 CDR","CRWV.TO":"AI云算力 CDR",
 "AVGO.TO":"半导体 CDR","ARA.TO":"稀土开发","EPRX.TO":"生物制药","COHR.TO":"光通信器件 CDR","ZDC.V":"安防监控塔租赁",
 "U-UN.TO":"实物铀信托","FTG.TO":"航空电子","MKO.V":"黄金(尼加拉瓜)","DELL.TO":"AI服务器 CDR","AMZN.TO":"电商/云 CDR",
 "TSLA.TO":"电动车 CDR","PDI.TO":"黄金(西非)","BDT.TO":"建筑工程","CEGS.TO":"核电/公用事业 CDR","GOOG.TO":"互联网/云 CDR",
}
NAME = {"ANTH.TO":"Anthropic CDR","IBM.TO":"IBM CDR","NKE.TO":"Nike CDR","HD.TO":"Home Depot CDR","SNDK.TO":"SanDisk CDR","MU.TO":"Micron CDR",
 "LRCX.TO":"Lam Research CDR","AMAT.TO":"Applied Materials CDR","NVDA.TO":"NVIDIA CDR","NBIS.TO":"Nebius CDR","LUME.TO":"Lumentum CDR",
 "ANET.TO":"Arista Networks CDR","AMD.TO":"AMD CDR","WDC.TO":"Western Digital CDR","BE.TO":"Bloom Energy CDR","INTC.TO":"Intel CDR",
 "CRWD.TO":"CrowdStrike CDR","MRV.TO":"Marvell CDR","ORAC.TO":"Oracle CDR","ASML.TO":"ASML CDR","CRWV.TO":"CoreWeave CDR","AVGO.TO":"Broadcom CDR",
 "COHR.TO":"Coherent CDR","DELL.TO":"Dell CDR","AMZN.TO":"Amazon CDR","TSLA.TO":"Tesla CDR","CEGS.TO":"Constellation Energy CDR","GOOG.TO":"Alphabet CDR",
 "LUNR.TO":"LunR Royalties","GMIN.TO":"G Mining Ventures","TCL-A.TO":"Transcontinental","QBR-B.TO":"Quebecor","HPS-A.TO":"Hammond Power","U-UN.TO":"Sprott Physical Uranium Trust"}

def row(i, v):
    sym = v["sym"]; cdr = v.get("cdr", False)
    vr = round(v["vol"] / (v["avg"] * FRAC), 1) if v.get("avg") else None
    name = v["name"]
    for cut in (" Shs", " SHS", " Inc.", " Inc", " Corp.", " Corporation", " Limited", " Ltd.", " Company", " N.V", ", "):
        if cut in name: name = name.split(cut)[0]
    name = name.rstrip(", ")
    if cdr and "CDR" not in name: name += " CDR"
    name = NAME.get(sym, name.strip())
    return [i, sym, name, f"{v['price']:.2f}", f"{v['chg']:+.2f}%", fmtcap(v.get("cap"), cdr), SEC.get(sym, v.get("tvsector") or "?"), vr]

DROP = {"ZNVD.NE"}  # BMO NVIDIA CDR, duplicate of NVDA.TO
g = [v for v in M["g"] if v["sym"] not in DROP][:30]
l = [v for v in M["l"] if v["sym"] not in DROP][:30]
G = [row(i, v) for i, v in enumerate(g, 1)]
L = [row(i, v) for i, v in enumerate(l, 1)]
for r in G + L:
    if r[6] == "?": print("NO SECTOR", r)

D = {
 "date": "2026-11-25", "weekday": "周三",
 "snapshot": "2026-11-25 13:10 ET 盘中（开盘约 3 小时 40 分；本期为补跑，排程未于 10:00 ET 执行）",
 "market_state": "REGULAR",
 "vr_note": "量比 = 当日成交量 ÷ (3个月日均量 × 0.56)，0.56 为截至快照时已开盘 3.67h/6.5h 的时长占比（补跑按实际时长调整）。⚠️≥3，🔥≥8。",
 "gainers": G, "losers": L,
 "table_notes": [
  "带 * 的 CDR 行市值为美股母公司总市值的加元换算（TradingView 口径），非加拿大挂牌份额；CDR 现价/涨跌/成交量取 .TO 主挂牌（Yahoo v7 quote）。",
  "Yahoo 80+80 行中 BIPC.TO / BIP-UN.TO（时间戳 11/20，Brookfield Infrastructure 重组后旧代码停牌，新 BIP 于 11/23 挂牌）为僵尸行已剔除；ZNVD.NE（BMO 版 NVIDIA CDR，-7.1%，仅 2.4 万股）与 NVDA.TO 同一标的，按去重规则只保留 .TO 行。其余时间戳均为 11/25 13:10 ET 前后。",
  "TradingView 交叉验证：涨幅榜前 30 全部在 TV 出现、涨跌幅一致（误差 <1.5pt，TV 稍滞后）。跌幅榜 TV 独有的 TSXV:MFG -13.8%（Mayfair Gold，隔夜包销增发致跌，市值 $176M 低于 $200M 门槛）、TSX:TBX -5.7%（Tributary Exploration，11/19 自 Headwater 分拆新挂牌，Yahoo 未进筛选）、PAIN -4.5%（市值 $13M）未入榜；NEO:RIO/DC.A/XNDU 为 Cboe 线滞后报价。",
  "Dell CDR（DELL.TO）.TO 行 3 个月日均量仅 5.4 万股，量比基数小易放大，连续第三日量比 >10。",
 ],
 "sectors_html": (
  "<ul>"
  "<li><strong>大盘：</strong>13:10 ET TSX 33,979（+0.05%）基本持平，资源股撑盘对冲科技下跌；美股继续走弱——纳指 -1.7%、标普 -0.9%，10 年美债收益率回落至 4.84%。商品：WTI +2.0% 至 ~$83.7、天然气 +0.8%、黄金 -1.1% 至 ~$3,551、白银 -2.4%、铜 -0.5% 至 $5.43/lb；比特币持平 ~$59.7K；加元 +0.5%。</li>"
  "<li><strong>涨幅榜主线一：矿业个股消息驱动。</strong>Founders Metals +9.9%（今晨 7:00 ET 公告 Upper Antino 深部钻孔 FR298 见矿 15.0m @ 23.97 g/t 金，地表下约 400m，Gold Fields 持股 19.9% 的苏里南项目持续加深）；Marimaca +6.7%（昨日公告获 Sprott 投委会批准 US$4.5 亿融资包：US$4.25 亿项目贷款 + US$2,500 万股权，无对冲/现金清扫要求，MOD 氧化铜项目 FID 推进）；Ivanhoe +4.9%（Kamoa-Kakula 三次下修指引后超跌，公司今日回应 Morgan Stanley 融资缺口担忧——否认出售 Western Forelands/Platreef 股权，称 $26 亿债务可滚动，股价月跌 33% 后技术反弹）；Blue Moon +4.6%（昨 -15.6% 后反弹，Nussir 出售予 ACG 预计 11/30 交割）、Faraday +4.0%、Collective +3.2%、Ivanhoe Electric +2.7% 铜开发类跟涨；贵金属尽管金银下跌仍有 G Mining +3.9%（RBC 11/23 维持买入 PT C$59）、Santacruz +3.8%、Andean +3.4%、Amex +3.3%、Aya +3.1%、Cadillac +2.8%、Vizsla +2.6% 补涨。</li>"
  "<li><strong>涨幅榜主线二：能源随油气价格反弹。</strong>WTI +2%、Henry Hub +0.8%：Kelt +4.8%、Tourmaline +3.2%、Birchcliff +3.2%、Vermilion +3.1%、Spartan Delta +2.7%、Ensign +2.5%、Colonial Coal +2.4%——天然气权重股集体上榜，为加股对冲科技下跌的主要力量。</li>"
  "<li><strong>涨幅榜主线三：零散个股。</strong>Verano +8.8%、Green Thumb +2.9% 美国大麻 MSO（12/11 联邦含THC大麻素 hemp 禁令生效预期 + Verano 11/20 开第 89 家佛州门店，板块连日走强）；Algoma Steel +6.7%（11/24 Seaspan 公告 $1.82 亿、2.4 万吨极地级钢板订单，为 6 艘海岸警卫队破冰船供钢，加上 Q3「转型最低点已过」）；Anthropic CDR +3.6%（美股 ANT +3.6% 至 $84.8，重回 $83 发行价上方，IPO 第五个交易日）、IBM CDR +3.2%、Nike +2.5%、Home Depot +2.4% 为 CDR 中少数上涨的防御/价值标的；Linamar +3.2%、Transcontinental +3.0%、5N Plus +3.6%（特种半导体材料，逆 AI 链反弹）；Quebecor +2.4%（量比 3.2，Telus 收购案 11/23 双方 CEO 会面「鼓舞」、CRTC 否决 TVA 削减魁北克城本地节目；列第 35 未入前 30）。</li>"
  "<li><strong>跌幅榜主线一：AI 硬件链连续第二日重挫，存储芯片领跌（CDR 占 30 席中 22 席）。</strong>TrendForce 今日下修 DRAM 展望（中国云厂商削减 2027 内存订单、合约价涨幅收窄）+ 新关税消息：SanDisk -9.4%、Micron -8.7%、Western Digital -5.0%；半导体设备 Lam -8.3%、Applied Materials -6.6%、ASML -4.5%；GPU/定制芯片 NVIDIA -5.8%、AMD -5.3%、Marvell -4.9%、Broadcom -4.2%、Intel -5.0%；光模块 Lumentum -5.5%、Coherent -3.9%、Arista -5.4%；AI 云 Nebius -5.6%、CoreWeave -4.5%、Oracle -4.8%、Alphabet -3.1%、Amazon -3.2%；电力 Bloom -5.0%、Constellation -3.1%。Dell CDR -3.2%（量比 13）：昨晚财报 Q3 营收 $549 亿（+103%）、调整 EPS $9.45 vs 预期 $6.59、全年营收指引上调 $100 亿至 $2,020 亿、AI 服务器积压订单创纪录 $1,323 亿、新增 $250 亿回购，盘后曾 +3~5%，但今日随板块转跌，Raymond James 下调 PT 至 $570。本土 Celestica -6.7%（AI 服务器代工，与 Dell/HPE 利润率担忧同源）。</li>"
  "<li><strong>跌幅榜主线二：非 AI 零散。</strong>Talamore -4.9%、Goldgroup -4.6%、Mako -3.3%、PDI Gold -3.1% 随金价 -1.1% 走弱；Sprott 实物铀信托 -3.4%（折价已 ~17%，铀现货承压）；Aclara 稀土 -4.1%；Eupraxia -4.1%；Zedcor -3.8%、Firan -3.4%、Bird Construction -3.1%（工业/服务获利了结）；CrowdStrike -4.9%（软件板块跟跌，12/2 财报前）；Tesla -3.1%。</li>"
  "</ul>"),
 "anomalies_html": (
  "<ul>"
  "<li>🔥 <strong>DELL.TO 量比 13</strong>（-3.2%，70.6 万股 vs .TO 日均 5.4 万）：Q3 大超预期 + 上调全年指引 + $250 亿回购，但 AI 硬件链整体抛售压过利好，高开后转跌；CDR 日均基数小，连续第三日量比 >10，属财报周持续换手。</li>"
  "<li>⚠️ <strong>ADEN.TO 量比 3.5</strong>（+2.4%，10.8 万股 vs 日均 5.5 万）：ADENTRA 收购 AccessSMT 后第二日延续放量上涨，列第 34。</li>"
  "<li>⚠️ <strong>SNDK.TO 量比 3.5</strong>（-9.4%，270 万股 vs 日均 136 万）：TrendForce 下修 DRAM/NAND 展望 + 关税；今日跌幅榜第一。</li>"
  "<li>⚠️ <strong>MU.TO 量比 3.3</strong>（-8.7%，359 万股 vs 日均 196 万）：同上，Micron 为 DRAM 定价最敏感标的。</li>"
  "<li>⚠️ <strong>QBR-B.TO 量比 3.2</strong>（+2.4%，210 万股 vs 日均 117 万）：Quebecor–Telus $310 亿收购案 CEO 会面后「愿意继续谈」，Telus 当日走势需对照；列第 35。</li>"
  "<li>⚠️ <strong>LUME.TO 量比 3.1</strong>（-5.5%，2.8 万股 vs 日均 1.6 万）：Lumentum CDR 流动性极低，随光模块板块回落。</li>"
  "<li>⚠️ <strong>LRCX.TO 量比 2.9 / NVDA.TO 2.8 / AMD.TO 2.5</strong>：AI 芯片 CDR 连续两日放量下跌，已接近 ⚠️ 门槛，整体为板块性抛售而非个股恐慌。</li>"
  "<li>涨幅榜量比普遍 ≤2（Founders 1.1、Marimaca 1.7、Ivanhoe 2.0、Algoma 0.6）：消息驱动但未见资金蜂拥，Founders 23.97 g/t 见矿为近月最佳钻孔之一却仅正常成交，市场对金价回落更敏感。</li>"
  "</ul>"),
 "digest": "13:10 ET 补跑：TSX 持平 33,979，纳指 -1.7%——TrendForce 下修 DRAM 展望，存储芯片领跌 AI 硬件链第二日：SanDisk -9.4%、Micron -8.7%、Lam -8.3%、Applied Materials -6.6%、NVIDIA -5.8%、AMD -5.3%，Dell 财报大超预期仍 -3.2%（量比 13🔥）、Celestica -6.7%；跌幅榜 30 席 CDR 占 22。涨幅榜矿业消息股：Founders Metals +9.9%（15m @ 23.97 g/t 金）、Marimaca +6.7%（Sprott US$4.5 亿融资）、Ivanhoe +4.9% 超跌反弹、Algoma Steel +6.7%（$1.82 亿破冰船钢板订单）；油气反弹 Kelt/Tourmaline/Birchcliff/Vermilion +3~5%；美国大麻 Verano +8.8%。",
}
json.dump(D, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, len(G), len(L))
for r in G + L: print(r)
