# -*- coding: utf-8 -*-
import json, os
TMP = os.environ.get("LOCALAPPDATA", ".") + "/Temp"
T = json.load(open(TMP + "/ca_tables.json", encoding="utf-8"))
d = {
 "date": "2026-11-17", "weekday": "周二",
 "snapshot": "2026-11-17 10:51 ET 盘中（开盘约 80 分钟）",
 "market_state": "REGULAR",
 "vr_note": "量比 = 当日成交量 ÷（3个月日均量 × 0.21）；0.21 = 抓取时已开盘约 81 分钟 / 全日 390 分钟。⚠️≥3，🔥≥8。早盘口径下量比天然偏高，关注相对排序。",
 "gainers": T["g"], "losers": T["l"],
 "table_notes": [
  "带 * 的 CDR 行（Reddit；Salesforce/SanDisk/Bloom/ServiceNow/Micron/Super Micro/Intuit/Robinhood/AppLovin）市值为美股母公司总市值（TradingView 口径），非加拿大挂牌份额；CDR 现价/涨跌/量比取 Yahoo v7 quote 的 .TO 主挂牌数据。",
  "Yahoo 80+80 行中仅 VBNK.TO（VersaBank，regularMarketTime 为 11/16 收盘）为僵尸数据已剔除；NVDA.NE 按 .TO 主挂牌去重（NVDA CDR -3.46% 列第 35 位榜外）。剔除 2 行 Yahoo/TradingView 价格分歧 >2 个百分点的行：TSXV:BZ Benz Mining（Yahoo -5.5% vs TV -1.5%）、TSX:KEEL Keel Infrastructure（Yahoo -4.0% vs TV -1.2%），疑为薄流动性下打印时点差异。TV 独有行 NEO:QBR.A（+105%）为 NEO 旧打印、NEO:AMX/TSX:RFA 为 11/16 旧 bar，均不计。",
  "TradingView 交叉验证：60 只中 57 只方向与幅度一致（差异 <1.5pp）；TV 加股 type=stock 榜单独有的 TSX:HBM Hudbay（+2.2%，Yahoo +1.0%）未入前 30。"
 ],
 "sectors_html": (
  "<ul>"
  "<li><strong>大盘</strong>：TSX 综指早盘 -1.09% 报 35,334（10:54 ET），延续周一 -1.06% 的跌势，金融板块领跌（RBC -2.0%、TD -2.0%、BMO -2.5%，美国 JPMorgan 系统故障+美联储 12 月加息预期升温）。全球等待 Nvidia 今晚盘后财报——黄仁勋辞职后首份财报，叠加美国商务部新规限制中国远程访问先进 AI 芯片，周一纳指 -2.5%、费城半导体 -5.3%。商品：WTI +0.7% 至 $86.3，黄金 +0.9% 至 $3,887、白银 +2.0% 至 $47.8（自一年低点反弹），铜 -0.4% 至 $5.98。加元 ~69.9 美分。</li>"
  "<li><strong>涨幅榜主线一：贵金属超跌反弹，白银矿股领涨</strong>——周一金银矿股补跌后今日随金银价反弹集体修复：Santacruz Silver（+16.1%，量比 5.0 ⚠️）11/16 盘后 Q3 财报大超预期——营收 US$1.53 亿（同比 +92%，二季度玻利维亚封路积压的精矿三季度集中出货）、调整后 EBITDA US$6,110 万（+213%）、AISC $19.73/oz（-33%）、EPS $0.40 超预期 $0.11，现金 US$1.25 亿；New Pacific（+6.1%）、Vizsla（+5.0%）白银开发同涨；黄金：Jaguar（+5.4%，量比 3.2 ⚠️，两日 -23% 后反弹）、Seabridge（+5.1%）、Mineros（+4.7%）、Mining Americas（+4.2%，周一 -17.7% 后反弹）、Montage（+3.5%）、Perpetua（+3.3%）、Heliostar（+3.3%，量比 3.2 ⚠️）、G Mining（+3.2%）、IAMGOLD（+3.0%）、Rio2（+2.9%）；权利金：Franco-Nevada（+3.4%）、OR Royalties（+3.2%）。榜外 Kinross +1.8%、Agnico +1.3%、Equinox +1.6%。</li>"
  "<li><strong>涨幅榜主线二：事件驱动个股</strong>——Tucows（+21.7%，量比 25.2 🔥）：11/17 盘前宣布将 Ting 自有光纤市场出售给 GTCR/Berkshire Partners 支持的 Clearwave，证券化债务 US$3.015 亿随业务剥离出表（名义对价），结束光纤资本开支黑洞，剩余债务仅 US$1.84 亿银团贷款；Chemtrade（+5.1%，量比 6.8 ⚠️）：11/13 盘后 Q3 财报+收窄全年 EBITDA 指引至 $4.95-5.15 亿、11/16 电话会后机构重估，叠加信托转公司结构（扩大投资者基础）；Dundee Corp（+4.5%，量比 5.1 ⚠️）：矿业投资控股，持仓 Ausgold 被 OceanaGold 收购 12 月交割、Magna Mining 等随金价反弹；Fireweed（+4.4%，量比 3.1 ⚠️）：11/16 获加拿大自然资源部 Global Partnerships Initiative 最高 C$1,400 万资助推进 Mactung 钨矿 FID；Aclara（+4.1%，量比 4.7 ⚠️）：11/17 盘前宣布实现磁材级 NdPr 金属生产，稀土股受政策催化。</li>"
  "<li><strong>涨幅榜其他</strong>：铜矿反弹——First Quantum（+4.8%，周一 -7.6%）、Lumina Metals（+4.9%，量比 3.2 ⚠️，连续第二日放量）、Trilogy（+3.1%）、Imperial Metals（+2.6%，榜外）；Lithium Argentina（+3.2%）；中游：Tidewater（+3.2%）、Rockpoint Gas Storage（+2.6%）；Reddit CDR（+2.9%）为美股社交媒体少数逆势；Digi Power X（+2.8%，量比 11.2 🔥）AI 数据中心转型 Q3 财报后延续。</li>"
  "<li><strong>跌幅榜主线一：美股软件/AI 硬件 CDR 全线重挫</strong>——企业软件遭 AI 变现质疑+企业 IT 支出冻结双杀：Salesforce CDR（-9.4%，量比 3.4 ⚠️，美股 -7~10%）Agentforce 变现进度存疑、$57 亿收购 Braze 后并购负债/稀释担忧；ServiceNow CDR（-7.1%，量比 3.9 ⚠️）10/28 Q3 cRPO 指引不及预期后持续阴跌、今日再创新低；Intuit CDR（-6.4%，量比 3.6 ⚠️）、AppLovin CDR（-6.3%）同步；AI 硬件：SanDisk CDR（-7.3%，量比 3.8 ⚠️）、Micron CDR（-6.8%，量比 3.0 ⚠️）存储芯片连续第二日遭抛售（周一美股 -6%）、Super Micro CDR（-6.7%）、Bloom Energy CDR（-7.2%）；Robinhood CDR（-6.3%）。Nvidia CDR -3.5%（榜外第 35）、Microsoft CDR -3.4%、AMD CDR -3.8%。</li>"
  "<li><strong>跌幅榜主线二：加拿大软件/科技同步受压</strong>——BlackBerry（-7.0%，成交 141 万股）、Enghouse（-4.7%）、Open Text（-4.3%）、Computer Modelling（-5.0%）、Shopify（-4.1%）、Xanadu（-5.1%）量子、Coveo（-3.6%，榜外）、Descartes（-3.3%，榜外）、Kinaxis/Lightspeed/Topicus（-2~3%，榜外）；HydroGraph（-4.5%）、Electrovaya（-6.6%）锂电。</li>"
  "<li><strong>跌幅榜主线三：事件驱动个股</strong>——Groupe Dynamite（-9.0%，量比 4.7 ⚠️）：做空机构 Spruce Point 11/17 盘前发布 Strong Sell 报告，称 35%-70% 下行空间，指控孟加拉供应商 Tusuka 违反供应商准则、同店销售/毛利率口径与同业不可比、停止披露关键数据，并质疑特别股息与溢价回购；Bird Construction（-7.2%，量比 5.4 ⚠️）：11/16 盘后宣布 $2 亿收购 Kel-Gor（工业维护/检修）并同步 $2 亿 bought deal 增发（$70.70/股，较 $75.18 收盘折价 6%），股价向增发价靠拢；Aecon（-6.1%）工程建筑同业受增发压制（WSP -3.7%、Stantec -1.9% 榜外）；Quebecor（-5.2%，量比 10.4 🔥，成交 224 万股）：作为收购方连续第二日重挫（累计 -20%），RBC/Desjardins 称 TELUS 并购监管通过概率低，TELUS 持平 $13.74 仅反映一半溢价；Eupraxia（-7.0%）生物科技连跌；Kelt（-4.1%）回吐周一 +10.7% 涨幅；Brompton Split Banc（-4.2%，量比 3.4 ⚠️）分级基金 Class A 随六大行下跌杠杆放大（单位 NAV 离 $15 红线仍有距离）；K92（-4.3%）、NGEx（-5.4%）、Solaris（-3.9%）金铜开发逆势下跌；Russel Metals（-4.6%）、Algoma（-4.4%）钢铁走弱。</li>"
  "</ul>"),
 "anomalies_html": (
  "<ul>"
  "<li><strong>早盘口径（占比 0.21），🔥 级（≥8）3 只，⚠️ 级（≥3）16 只：</strong></li>"
  "<li>🔥 <strong>TC.TO Tucows</strong>（量比 25.2，+21.7%）：盘前宣布 Ting 自有光纤业务出售给 Clearwave，US$3.015 亿证券化债务出表——日均仅 6K 股的冷门股放量换手 3.3 万股，Nasdaq 母股 TCX +26%。</li>"
  "<li>🔥 <strong>DGX.NE Digi Power X</strong>（量比 11.2，+2.8%）：NEO 挂牌日均仅 2 万股，11/13 Q3 财报（营收 +85%、AI 收入占 46%、Cerebras $10.7 亿十年合同）后延续买盘，流动性稀薄导致量比虚高。</li>"
  "<li>🔥 <strong>QBR-B.TO Quebecor</strong>（量比 10.4，-5.2%）：$313 亿收购 TELUS 提议后第二日继续被抛售（两日 -20%），分析师普遍认为监管通过概率低，机构减持。</li>"
  "<li>⚠️ <strong>CHE-UN.TO Chemtrade</strong>（量比 6.8，+5.1%）：Q3 财报+指引收窄+信托转公司后的机构重估，成交 27 万股。</li>"
  "<li>⚠️ <strong>BDT.TO Bird Construction</strong>（量比 5.4，-7.2%）：$2 亿 bought deal 增发（$70.70）压价，成交 43 万股已超全日均量。</li>"
  "<li>⚠️ <strong>DC-A.TO Dundee Corp</strong>（量比 5.1，+4.5%）：矿业投资控股随金矿持仓反弹，成交 17 万股超日均。</li>"
  "<li>⚠️ <strong>SCZ.TO Santacruz Silver</strong>（量比 5.0，+16.1%）：Q3 营收 +92%、EBITDA +213%、AISC -33%，EPS 大幅超预期，叠加白银反弹。</li>"
  "<li>⚠️ <strong>GRGD.TO Groupe Dynamite</strong>（量比 4.7，-9.0%）：Spruce Point 做空报告（35-70% 下行、供应商合规、KPI 口径质疑）。</li>"
  "<li>⚠️ <strong>ARA.TO Aclara Resources</strong>（量比 4.7，+4.1%）：盘前宣布实现磁材级 NdPr 金属生产。</li>"
  "<li>⚠️ <strong>NOWS.TO ServiceNow CDR</strong>（量比 3.9，-7.1%）、<strong>SNDK.TO SanDisk CDR</strong>（量比 3.8，-7.3%）、<strong>INTU.TO Intuit CDR</strong>（量比 3.6，-6.4%）、<strong>CRM.TO Salesforce CDR</strong>（量比 3.4，-9.4%）、<strong>MU.TO Micron CDR</strong>（量比 3.0，-6.8%）：美股软件 AI 变现质疑+AI 芯片出口新规+Nvidia 财报前风险出清，CDR 随母股放量下跌。</li>"
  "<li>⚠️ <strong>SBC.TO Brompton Split Banc</strong>（量比 3.4，-4.2%）：六大行早盘 -2~2.5%，分级基金 Class A 杠杆放大跌幅，无公司层面消息。</li>"
  "<li>⚠️ <strong>JAG.TO Jaguar Mining</strong>（量比 3.2，+5.4%）：两日 -23% 后空头回补反弹。</li>"
  "<li>⚠️ <strong>LMCU.TO Lumina Metals</strong>（量比 3.2，+4.9%）：连续第二日放量上行，无公告，疑机构建仓延续。</li>"
  "<li>⚠️ <strong>HSTR.TO Heliostar</strong>（量比 3.2，+3.3%）：11/13 Q3 创纪录矿山经营利润后随金价反弹。</li>"
  "<li>⚠️ <strong>FWZ.TO Fireweed Metals</strong>（量比 3.1，+4.4%）：NRCan 最高 C$1,400 万 Mactung 钨矿资助。</li>"
  "<li>榜外提示：Koryx Copper KRY.V（量比 6.7，-3.8%）、Alvopetro ALV.V（量比 6.6，-3.0%）、Orogen OGN.V（量比 6.1，-2.4%）均为小盘薄流动性放量下跌，无公告。</li>"
  "</ul>"),
 "digest": "早盘 TSX -1.09% 报 35,334，金融领跌、等待 Nvidia 今晚财报。涨幅榜：贵金属反弹（银 +2%）——Santacruz Silver +16.1%（Q3 大超预期）、New Pacific/Vizsla/Jaguar/Seabridge +5~6%、First Quantum +4.8%；Tucows +21.7%（Ting 光纤出售剥离 US$3 亿债务，量比 25 🔥）、Chemtrade +5.1%、Aclara +4.1%。跌幅榜：美股软件/AI 硬件 CDR 重挫——Salesforce -9.4%、SanDisk -7.3%、ServiceNow -7.1%、Micron -6.8%；Groupe Dynamite -9.0%（Spruce Point 做空报告）、Bird -7.2%（$2 亿增发）、BlackBerry -7.0%、Quebecor -5.2%（量比 10.4 🔥）、Brompton Split Banc -4.2%。"
}
json.dump(d, open("C:/Users/Elliott/Downloads/claude/ca-market-brief/data/2026-11-17.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
