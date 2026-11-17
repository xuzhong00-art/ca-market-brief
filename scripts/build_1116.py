# -*- coding: utf-8 -*-
"""Build data/2026-11-16.json from _merged.json + _proc.json (makeup run, close basis FRAC=1.0)."""
import json
D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
m = json.load(open(D + "_merged.json", encoding="utf-8"))
proc = json.load(open(D + "_proc.json", encoding="utf-8"))
META = json.load(open(D + "_meta_all.json", encoding="utf-8"))
META.update({
 "MRT-UN.TO": ["Morguard REIT", "商业地产REIT"], "MHC-U.TO": ["Flagship Communities REIT (US$)", "活动房屋社区REIT"],
 "ATS.TO": ["ATS", "自动化设备"], "ONEX.TO": ["Onex", "私募/资管"], "PBH.TO": ["Premium Brands", "食品加工"],
 "AGF-B.TO": ["AGF Management", "资产管理"], "WSTR.V": ["WellStar Technologies", "科技服务"],
 "HELP.NE": ["Helus Pharma (ex-Cybin)", "致幻剂药物研发"], "CDR.TO": ["Condor Energies", "油气(中亚)"],
 "NWC.TO": ["North West Company", "北方零售"], "AAV.TO": ["Advantage Energy", "天然气(蒙特尼)"],
 "T.TO": ["TELUS", "电信"], "QBR-B.TO": ["Quebecor", "电信/媒体"], "MAI.TO": ["Mining Americas", "黄金生产(内华达)"],
 "PG.TO": ["Procter & Gamble CDR", "日用消费品(CDR)"], "DELL.TO": ["Dell CDR", "服务器/PC(CDR)"],
})
RATIO = 1.0
# NTLX.V: Yahoo intradaymarketcap 339.6M is a data error (TMX market cap $48.7M, 13.7M shs x $4) -> fails $200M filter, drop.
g = [r for r in m["g"] if r["sym"] != "NTLX.V"]
nwc = next(r for r in proc["gainers"] if r["sym"] == "NWC.TO")
nwc = dict(nwc, cdr=False, tvsector=nwc.get("tv_sector"))
g.append(nwc)
g = sorted(g, key=lambda x: -x["chg"])[:30]
l = m["l"][:30]

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
G, L = rows(g), rows(l)
print("missing:", [r[1] for r in G + L if r[1] not in META])
for r in G + L:
    if r[7] and r[7] >= 3: print(r[1], r[4], r[7])

d = {
 "date": "2026-11-16", "weekday": "周一",
 "snapshot": "2026-11-16 16:00 ET 收盘（补跑：本机 19:10 PT 执行，数据为全日收盘口径）",
 "market_state": "CLOSED",
 "note": "本期为补跑：电脑在排程时段未唤醒，数据于收盘后抓取，表中现价/涨跌/成交量均为 11/16 全日收盘数据，量比口径=全日成交量 ÷ 3个月日均量（开盘占比 1.0）。",
 "vr_note": "量比 = 当日全日成交量 ÷ 3个月日均量（补跑收盘口径，占比 1.0）。⚠️≥3，🔥≥8。全日口径下量比天然低于早盘 7.7% 口径，阈值相同故触发更少。",
 "gainers": G, "losers": L,
 "table_notes": [
  "CDR 行（P&G；Dell/SanDisk/Strategy）市值为美股母公司总市值（TradingView 口径），非加拿大挂牌份额；由 TradingView type=dr 查询补入，量比用 Yahoo v7 quote 补算。",
  "Yahoo 80+80 行全部为 11/16 当日新鲜数据（无僵尸停牌行）；AMD.NE 已按 .TO 主挂牌去重。剔除 1 行数据错误：TSXV:NTLX NeuroThera（+12.7%，Yahoo 市值 $340M 为错误值，TMX 实为 $49M，不满足 ≥$200M）。TradingView 交叉验证：60 行方向与幅度全部一致；TV 独有行 NEO:QBR.A（+105%）为 NEO 旧打印不计，TSXV:PAIN 市值为 TV 数据错误（Yahoo 实为 $17M）、TSX:BNKR Bunker Hill 市值 $197M 略低于门槛，均剔除。",
 ],
 "sectors_html": (
  "<ul>"
  "<li><strong>大盘</strong>：TSX 综指大跌 383.77 点（-1.06%）收 35,722.13，成交 3.83 亿股放量；能源、基本金属领跌，美股 AI 板块在周三 Nvidia 财报前再度抛售（标普 -1.92%、纳指 -2.49%、道指 -1.41%，VIX +18% 至 22.9）。WTI -3.96% 至 $83.83，黄金持平 $3,861，加元 69.88 美分。权重股：Cameco -6.35%、Agnico -3.97%、First Quantum -7.57%、Canadian Natural -2.75%（收购方）、Suncor -2.41%、RBC -0.93%；Shopify 逆市 +0.81%。</li>"
  "<li><strong>涨幅榜主线一：并购日——两单大交易引爆榜首</strong>——Advantage Energy（+23.7%，量比 23.5 🔥，成交 1,756 万股为日均 23 倍）：Canadian Natural 全现金收购，交易总值 $25.3 亿（含债务），蒙特尼天然气资产整合；TELUS（+12.9%，量比 4.5 ⚠️，成交 3,587 万股）：Quebecor 11/16 公开非约束性收购提议，现金+股票约 $19.45/股、总值 $313 亿，较周五收盘溢价 ~60%，TELUS 特别委员会称提案存在重大监管与执行风险、正评估其他战略选项，股价仅反映约一半溢价（市场对 CRTC/竞争局审批存疑）。并购外溢：Rogers（+4.6%，量比 3.1 ⚠️）、BCE（+3.4%，成交 1,038 万股）、Cogeco（+1.8%）电信板块整体重估；Kelt（+10.7%，量比 3.7 ⚠️，创 52 周新高）、Birchcliff（+2.2%）作为蒙特尼气田同业受 AAV 收购估值读穿，叠加 Kelt 周五 Q3 超预期后的延续买盘。</li>"
  "<li><strong>涨幅榜主线二：风险厌恶下的防御轮动</strong>——食品/必需消费：Metro（+1.9%）、Saputo（+1.9%，成交 1.7 倍日均）、Maple Leaf（+2.4%）、Premium Brands（+2.3%）、North West（+1.9%）；公用事业：ATCO（+1.9%）、Algonquin（+1.9%）、Northland（+1.8%，成交 2.4 倍日均）；废弃物处理：GFL（+2.5%）、Waste Connections（+2.1%）；养老：Sienna（+2.7%）；REIT 受益收益率回落：Morguard REIT（+3.8%，量比 10.4 🔥）、Flagship Communities 美元单位（+3.0%，量比 9.3 🔥）、Colliers（+3.4%）、Altus（+2.0%）；P&amp;G CDR（+2.0%）为美股防御性代表。</li>"
  "<li><strong>涨幅榜其他</strong>：Martinrea（+2.7%，量比 3.4 ⚠️）周五 Q3 超预期 +13.4% 后继续放量上行；Lumina Metals（+4.2%，量比 3.0 ⚠️）波兰铜银开发商，无新公告，疑为 11 月投资者路演后的机构建仓；Apotex（+2.1%）、Topicus（+2.9%）、VersaBank（+2.7%）、Onex（+2.4%）、AGF（+2.1%）、ATS（+3.0%）、Curaleaf（+3.2%）、Benz Mining（+3.9%，量比仅 0.3）零散走强。</li>"
  "<li><strong>跌幅榜主线一：财报/事件驱动个股重挫</strong>——Mining Americas（-17.7%，量比 3.1 ⚠️，成交 136 万股）：Q3 AISC $2,121/oz 高于全年指引上限 $2,000（剥采与柴油成本上升），调整后净利仅 $160 万（$0.01/股），Pan 矿单季产量 7,915 oz；Quebecor（-15.3%，量比 4.7 ⚠️，成交 463 万股）：作为收购方被抛售——$313 亿现金+股票对价、巨额融资与稀释担忧，且监管审批前景不明，收购要约价值随其股价同步缩水；Helus Pharma（ex-Cybin，-13.6%，量比 3.4 ⚠️）：HLP003 三期 APPROACH 试验达主要终点（MADRS 较安慰剂改善 7.6 分、第 2 天即显效），但披露 3 例治疗相关严重不良事件（含 1 例非应答者在第二次给药后 55 天自杀未遂），美股 -21%，利好出尽+安全性疑虑；Jaguar Mining（-14.4%，量比 3.7 ⚠️）周五 Q3 后 -10.2% 再跌，创 52 周新低；Sigma Lithium（-14.1%，量比 3.2 ⚠️）11/16 宣布 US$1.25 亿可转债完成（7% 票息、转股价 US$6.51、上调 25%），虽置换 11.45% 浮息抵押债，但潜在稀释约 1,920 万股（~17%）引发抛售；Palisades Goldcorp（-11.1%，量比 3.5 ⚠️）矿业投资控股随初级金矿股普跌。</li>"
  "<li><strong>跌幅榜主线二：金属矿业全线下挫</strong>——铜：Hudbay（-8.3%，成交 382 万股）、First Quantum（-7.6%）、Capstone（-7.3%，成交 672 万股）、Solaris（-7.9%）随基本金属与风险偏好回落；黄金/白银（金价持平但矿股补跌）：Orezone（-10.3%）、Highlander Silver（-9.1%）、New Pacific（-9.3%）、Americas Gold &amp; Silver（-8.2%，成交 269 万股）、Gold X2（-9.1%）、Contango（-11.4%）、Titan（-12.0%）、McEwen（-7.3%）；权利金：LunR（-9.3%）、Metalla（-8.1%）；铀/核电（AI 电力交易同步回吐）：IsoEnergy（-8.5%）、Energy Fuels（-8.2%）、Cameco -6.4%；稀土 Aclara（-8.3%）、锂电 Electrovaya（-8.7%）。</li>"
  "<li><strong>跌幅榜主线三：AI/科技链与油气</strong>——美股 AI 硬件 CDR 随纳指 -2.5%：Dell CDR（-8.6%）、SanDisk CDR（-8.5%，成交 199 万股 1.6 倍日均）、Micron CDR（-7.7%，榜外 31）、Strategy CDR（-7.9%，比特币 ~$6.46 万）；加拿大科技：Xanadu（-11.0%，成交 159 万股）量子高波动、Digi Power X（-12.8%）AI 数据中心/挖矿、Docebo（-7.9%）、Quarterhill（-8.4%）、WellStar（-13.6%）；油气（WTI -4%）：Condor Energies（-12.2%）、Tenaz（-8.1%，成交 2.6 倍日均）；生物科技 Eupraxia（-9.4%）。</li>"
  "</ul>"
 ),
 "anomalies_html": (
  "<ul>"
  "<li><strong>本期为收盘口径补跑（占比 1.0），🔥 级（≥8）3 只，⚠️ 级（≥3）10 只：</strong></li>"
  "<li>🔥 <strong>AAV.TO Advantage Energy</strong>（量比 23.5，+23.7%）：Canadian Natural 全现金收购，交易总值 $25.3 亿（含债务），成交 1,756 万股为日均 23 倍——并购套利盘大举换手。</li>"
  "<li>🔥 <strong>MRT-UN.TO Morguard REIT</strong>（量比 10.4，+3.8%）：成交仅 4.7 万股但日均 4.5K 极薄；11/16 宣布 11 月每单位 2 分派息，叠加 REIT 板块随收益率回落走强——流动性稀薄导致量比虚高，无实质性利好。</li>"
  "<li>🔥 <strong>MHC-U.TO Flagship Communities REIT（美元单位）</strong>（量比 9.3，+3.0%）：美元挂牌单位日均仅 1 万股；11/11 Q3 FFO/单位 +6.8%、派息上调 5.9%、启动 NCIB，11/16 宣布 11 月派息 US$0.0577——基本面催化叠加薄流动性。</li>"
  "<li>⚠️ <strong>QBR-B.TO Quebecor</strong>（量比 4.7，-15.3%）：公开 $313 亿收购 TELUS 提议后作为买方被重挫——融资/稀释与监管审批疑虑。</li>"
  "<li>⚠️ <strong>T.TO TELUS</strong>（量比 4.5，+12.9%）：Quebecor 收购提议 ~$19.45/股（溢价 ~60%），成交 3,587 万股；股价仅反映一半溢价，市场对成交概率打折。</li>"
  "<li>⚠️ <strong>KEL.TO Kelt Exploration</strong>（量比 3.7，+10.7%）：周五 Q3 超预期后延续 + AAV 被 CNQ 收购的蒙特尼同业估值读穿，创 52 周新高。</li>"
  "<li>⚠️ <strong>JAG.TO Jaguar Mining</strong>（量比 3.7，-14.4%）：Q3 后连续第二日重挫（累计 -23%），创 52 周新低，叠加金矿股普跌。</li>"
  "<li>⚠️ <strong>PALI.V Palisades Goldcorp</strong>（量比 3.5，-11.1%）：矿业投资控股公司，随初级金银矿股集体下跌，持仓净值预期缩水。</li>"
  "<li>⚠️ <strong>HELP.NE Helus Pharma</strong>（量比 3.4，-13.6%）：三期 HLP003 抑郁症试验达主要终点，但 3 例严重不良事件（含 1 例自杀未遂）引发安全性疑虑，美股 -21%。</li>"
  "<li>⚠️ <strong>MRE.TO Martinrea</strong>（量比 3.4，+2.7%）：周五 Q3 超预期 +13.4% 后继续放量上行，低估值汽配股空头回补延续。</li>"
  "<li>⚠️ <strong>SGML.V Sigma Lithium</strong>（量比 3.2，-14.1%）：US$1.25 亿 7% 可转债完成（转股价 US$6.51），置换高息抵押债但潜在稀释 ~17%。</li>"
  "<li>⚠️ <strong>MAI.TO Mining Americas</strong>（量比 3.1，-17.7%）：Q3 AISC $2,121/oz 超指引上限、调整后净利仅 $160 万，成本失控担忧。</li>"
  "<li>⚠️ <strong>RCI-B.TO Rogers</strong>（量比 3.1，+4.6%）：Quebecor-TELUS 并购提议带动电信板块整体重估，成交 736 万股。</li>"
  "<li>⚠️ <strong>LMCU.TO Lumina Metals</strong>（量比 3.0，+4.2%）：波兰铜银开发商，无新公告，疑为 11 月投资者路演后机构建仓；铜矿股普跌中逆势走强。</li>"
  "</ul>"
 ),
 "digest": "补跑收盘口径：TSX -1.06%（-384 点）收 35,722，能源/基本金属领跌、美股 AI 抛售。并购日：Advantage Energy +23.7%（CNQ $25.3 亿全现金收购，量比 23.5 🔥）、TELUS +12.9%（Quebecor $313 亿收购提议，溢价 60%），Rogers +4.6%/BCE +3.4% 电信板块重估，Kelt +10.7% 蒙特尼同业读穿；防御轮动（食品/公用事业/REIT）。跌幅榜：Mining Americas -17.7%（Q3 AISC 超指引）、Quebecor -15.3%（收购方）、Jaguar -14.4%、Sigma Lithium -14.1%（可转债稀释）、Helus -13.6%（三期达标但 SAE 疑虑）；铜矿（Hudbay/FM/Capstone -7~8%）、金银矿、铀、AI 硬件 CDR（Dell/SanDisk -8.5%）全线下挫。",
}
json.dump(d, open(D + "2026-11-16.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written", len(G), len(L))
