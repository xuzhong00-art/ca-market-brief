# -*- coding: utf-8 -*-
"""Build data/2026-10-20.json from _proc.json + CDR additions + meta (live 7:00 PT, FRAC=0.077)."""
import json

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
proc = json.load(open(D + "_proc.json", encoding="utf-8"))
FRAC = 0.077

# .NE rows -> .TO fuller data (none this time)
TO_OVERRIDE = {}
# TV-only CDR additions (Yahoo v7 quote 07:00 PT): sym, name, price, chg, cap, vol, avg3m
TV_ADD = {
 "gainers": [
  ("NOC.TO", "Northrop Grumman（CDR）", 18.32, 6.51, 2.6e9, 20125, 5241),
  ("MMMM.TO", "3M（CDR）", 26.47, 4.54, 113.8e9, 42193, 3685),
  ("INTU.TO", "Intuit（CDR）", 20.63, 4.66, 5.5e9, 34822, 55809),
  ("LLY.TO", "Eli Lilly（CDR）", 46.20, 4.31, 1509.7e9, 38848, 70561),
  ("PFE.TO", "Pfizer（CDR）", 13.36, 2.14, 224.2e9, 35783, 127409),
  ("NOWS.TO", "ServiceNow（CDR）", 18.84, 2.11, 1001.1e9, 36356, 203233),
 ],
 "losers": [
  ("GE.TO", "GE Aerospace（CDR）", 38.59, -4.39, 414.0e9, 19124, 15279),
  ("CRWV.TO", "CoreWeave（CDR）", 11.05, -3.91, 6.1e9, 186531, 232793),
 ],
}
EXCLUDE = {"PALI.V"}  # 1,100 shares traded at open only, below 15K volume floor

META = {
 "ESI.TO":("Ensign Energy","陆上钻井服务"),"LMN.V":("Lumine Group","通信软件并购"),
 "TRI.TO":("Thomson Reuters","法律/税务信息服务"),"KITS.TO":("Kits Eyecare","眼镜电商"),
 "AIF.TO":("Altus Group","商业地产数据/软件"),"OTEX.TO":("Open Text","企业软件"),
 "CVO.TO":("Coveo Solutions","企业AI软件"),"ENGH.TO":("Enghouse Systems","企业软件"),
 "LSPD.TO":("Lightspeed Commerce","零售POS软件"),"GIB-A.TO":("CGI","IT服务"),
 "ATD.TO":("Couche-Tard","便利店零售"),"BBD-B.TO":("Bombardier","公务机制造"),
 "T.TO":("TELUS","电信"),"CSH-UN.TO":("Chartwell Retirement","养老地产REIT"),
 "RCI-B.TO":("Rogers Communications","电信"),"BHC.TO":("Bausch Health","制药"),
 "AP-UN.TO":("Allied Properties REIT","办公REIT"),"REI-UN.TO":("RioCan REIT","零售REIT"),
 "BAM.TO":("Brookfield Asset Mgmt","另类资产管理"),"CNL.TO":("Collective Mining","黄金勘探(哥伦比亚)"),
 "PD.TO":("Precision Drilling","陆上钻井服务"),"CAR-UN.TO":("CAPREIT","公寓REIT"),
 "DIR-UN.TO":("Dream Industrial REIT","工业REIT"),"DOL.TO":("Dollarama","折扣零售"),
 "EMP-A.TO":("Empire Company","食品零售"),"TCL-A.TO":("Transcontinental","印刷包装"),
 "NXR-UN.TO":("Nexus Industrial REIT","工业REIT"),"L.TO":("Loblaw","食品零售"),
 "SAP.TO":("Saputo","乳制品"),"CIA.TO":("Champion Iron","铁矿生产(魁北克)"),
 "PNG.V":("Kraken Robotics","海洋机器人/国防"),"SRU-UN.TO":("SmartCentres REIT","零售REIT"),
 "AQN.TO":("Algonquin Power","公用事业"),"SIA.TO":("Sienna Senior Living","养老服务"),
 "TCW.TO":("Trican Well Service","压裂油服"),"CURA.TO":("Curaleaf","大麻(美国)"),
 "VITL-UN.TO":("Vital Infrastructure","基建REIT"),"BN.TO":("Brookfield Corp","另类资产/保险"),
 "WSP.TO":("WSP Global","工程咨询"),"BCE.TO":("BCE","电信"),
 "NOC.TO":("Northrop Grumman（CDR）","国防·CDR"),"MMMM.TO":("3M（CDR）","工业集团·CDR"),
 "INTU.TO":("Intuit（CDR）","软件·CDR"),"LLY.TO":("Eli Lilly（CDR）","制药·CDR"),
 "PFE.TO":("Pfizer（CDR）","制药·CDR"),"NOWS.TO":("ServiceNow（CDR）","软件·CDR"),
 "BRK.TO":("Berkshire Hathaway（CDR）","综合控股·CDR"),"CP.TO":("CPKC","铁路"),
 "CHP-UN.TO":("Choice Properties REIT","零售REIT"),"GAU.TO":("Galiano Gold","黄金生产(加纳)"),
 "TSU.TO":("Trisura Group","专业保险"),"FTS.TO":("Fortis","公用事业"),
 "CRT-UN.TO":("CT REIT","零售REIT"),"X.TO":("TMX Group","交易所"),
 # losers
 "BZ.V":("Benz Mining","黄金勘探(西澳)"),"SLG.V":("San Lorenzo Gold","铜金勘探(智利)"),
 "SVM.TO":("Silvercorp Metals","银矿生产(中国)"),"RIO.TO":("Rio2","黄金开发(智利)"),
 "TMQ.TO":("Trilogy Metals","铜矿开发(阿拉斯加)"),"NCX.V":("NorthIsle Copper & Gold","铜金开发(BC)"),
 "META.TO":("Meta（CDR）","互联网·CDR"),"BDT.TO":("Bird Construction","建筑工程"),
 "FM.TO":("First Quantum","铜矿生产"),"XNDU.TO":("Xanadu Quantum","量子计算"),
 "PSI.TO":("Pason Systems","钻井数据技术"),"FTT.TO":("Finning","卡特彼勒经销"),
 "KEEL.TO":("Keel Infrastructure","AI数据中心基建"),"CS.TO":("Capstone Copper","铜矿生产"),
 "SDE.TO":("Spartan Delta","油气"),"IVN.TO":("Ivanhoe Mines","铜矿生产(刚果)"),
 "HBM.TO":("Hudbay Minerals","铜金生产"),"GTE.TO":("Gran Tierra Energy","油气(南美)"),
 "HIVE.TO":("HIVE Digital","加密挖矿/算力"),"MDI.TO":("Major Drilling","矿业钻探服务"),
 "JAG.TO":("Jaguar Mining","黄金生产(巴西)"),"MFG.V":("Mayfair Gold","黄金开发(安大略)"),
 "MACK.V":("Mackay Gold & Silver","金银勘探"),"ARG.TO":("Amerigo Resources","铜尾矿回收"),
 "USA.TO":("Americas Gold & Silver","银矿"),"VNP.TO":("5N Plus","特种半导体材料"),
 "FWZ.V":("Fireweed Metals","锌/钨开发"),"FDY.TO":("Faraday Copper","铜矿勘探(亚利桑那)"),
 "NICU.TO":("Magna Mining","镍铜开发(萨德伯里)"),"OBE.TO":("Obsidian Energy","油气生产"),
 "GMIN.TO":("G Mining Ventures","黄金生产(巴西)"),"BLDP.TO":("Ballard Power","氢燃料电池"),
 "EFR.TO":("Energy Fuels","铀/稀土"),"ERO.TO":("Ero Copper","铜矿生产(巴西)"),
 "GE.TO":("GE Aerospace（CDR）","航空发动机·CDR"),"CRWV.TO":("CoreWeave（CDR）","AI云算力·CDR"),
 "LUN.TO":("Lundin Mining","铜矿生产"),"DSV.TO":("Discovery Mining","银矿开发(墨西哥)"),
 "FDR.V":("Founders Metals","黄金勘探(苏里南)"),"LAC.TO":("Lithium Americas","锂矿开发"),
 "CVVY.TO":("Cavvy Energy","油气"),"HUT.TO":("Hut 8","加密挖矿/算力"),
 "CLS.TO":("Celestica","AI服务器/EMS"),"ASTL.TO":("Algoma Steel","钢铁"),
 "EFX.TO":("Enerflex","油气设备"),"OMG.V":("Omai Gold Mines","黄金勘探(圭亚那)"),
}

def cap_s(c):
    if not c: return "–"
    return f"{c/1e9:.1f}B" if c >= 1e9 else f"{c/1e6:.0f}M"

def build(side, desc):
    rows = []
    for r in proc[side]:
        if "drop" in r or r["sym"] in EXCLUDE: continue
        if r["sym"] in TO_OVERRIDE:
            s, p, c, cap, vol, avg = TO_OVERRIDE[r["sym"]]
            r = dict(r, sym=s, price=p, chg=c, cap=cap, vol=vol, avg=avg, vr=round(vol/(avg*FRAC),1))
        rows.append(r)
    for s, n, p, c, cap, vol, avg in TV_ADD[side]:
        rows.append({"sym":s,"name":n,"price":p,"chg":c,"cap":cap,"vr":round(vol/(avg*FRAC),1),"tv_sector":"CDR"})
    rows.sort(key=lambda r: r["chg"], reverse=desc)
    out = []
    for i, r in enumerate(rows[:30], 1):
        name, sec = META.get(r["sym"], (str(r["name"])[:22], r.get("tv_sector") or "–"))
        if r["sym"] not in META: print("NO META:", r["sym"], r["name"])
        out.append([i, r["sym"], name, f"{r['price']:.2f}", f"{r['chg']:+.2f}%", cap_s(r["cap"]), sec, r["vr"]])
    return out

G, L = build("gainers", True), build("losers", False)
data = {
 "date":"2026-10-20","weekday":"周二",
 "snapshot":"2026-10-20 10:00 ET 早盘（开盘约 30 分钟）",
 "market_state":"REGULAR",
 "vr_note":"量比 = 当日成交量 ÷ (3个月日均量 × 0.077)，0.077 为开盘 30 分钟占全日 6.5 小时的比例。CDR 行用 Yahoo .TO 挂牌 3 个月均量，基数小易放大。⚠️≥3，🔥≥8。",
 "gainers":G,"losers":L,
 "table_notes":[
  "*CDR（NOC/MMMM/INTU/LLY/PFE/NOWS/META/GE/CRWV）市值为美股母公司总市值（加元口径），非加拿大挂牌流通市值；NOC/INTU/CRWV 的 Yahoo 市值字段异常偏小，已按母公司口径修正。",
  "*NOC/MMMM/INTU/LLY/PFE/NOWS 及跌幅榜 GE/CRWV 为 TradingView type=dr 补充（Yahoo screener 未返回），行情取 Yahoo .TO 挂牌 10:00 ET 快照。",
  "*剔除：AMD.NE 交叉挂牌去重；PALI.V 开盘仅成交 1,100 股（低于 1.5 万股门槛）。所有入榜行 regularMarketTime 均为 10-20 当日；TV 交叉验证涨跌幅方向一致，差异仅为快照时间差（Yahoo 10:00 vs TV 延迟约 2–3 分钟）。TV 跌幅榜 DLCG/VCM（NEO 行）最后成交为 10-13/10-08，陈旧数据未采纳。",
  "*早盘开盘 30 分钟，涨跌幅整体偏小（涨幅榜第 30 名仅 +1.2%），榜单稳定性低于收盘榜，收盘后排序可能明显变化。",
 ],
 "sectors_html":(
  "<ul>"
  "<li><strong>大盘：TSX 开盘小幅走低，防御/科技轮动</strong>：隔夜中东局势推高油价、加剧通胀担忧，金价回落 0.5% 至 US$4,120/oz（银 +0.2% 至 US$57.2），TSX 期货开盘前 -0.13%；美股受 GM/GE 财报拖累分化。开盘半小时资金从昨日领涨的矿业撤出，转入软件/电信/REIT/必需消费等防御与利率敏感板块，整体涨跌幅都很温和（涨幅榜第 30 名仅 +1.2%）。</li>"
  "<li><strong>涨幅榜主线一：美股财报季 CDR 领涨</strong>：Northrop Grumman +6.5%（Q3 EPS US$7.89 大幅超预期 7.18，上调全年 EPS 指引至 29.35–29.75，积压订单 1,100 亿）、3M +4.5%（调整后 EPS 2.50 vs 预期 2.38）、Intuit +4.7%、Eli Lilly +4.3%（制药连续走强）、Pfizer +2.1%、ServiceNow +2.1%。</li>"
  "<li><strong>涨幅榜主线二：油服与加拿大软件</strong>：Ensign Energy +4.6% 居本土股首位——TD Cowen 今晨上调至 Buy、目标价 C$3.50→4.75，称加美两地钻机活动强于预期并上调 2027 EBITDA 至 5.1 亿；Precision Drilling +1.9% 跟涨；WTI 高企继续利好钻井商。软件板块：Lumine +3.5%、Thomson Reuters +3.1%、Open Text +2.7%、Coveo +2.7%、Enghouse +2.7%、Lightspeed +2.4%、CGI +2.2%，随美股科技隔夜反弹集体修复。</li>"
  "<li><strong>涨幅榜主线三：防御与利率敏感板块</strong>：电信 TELUS +2.1%、Rogers +1.8%；REIT Chartwell +1.9%、Allied +1.7%、RioCan +1.7%、CAPREIT +1.6%、Dream Industrial +1.4%；必需消费 Couche-Tard +2.1%、Dollarama +1.5%、Loblaw +1.4%、Empire +1.3%、Saputo +1.2%；Brookfield AM +1.6%。Altus Group +2.8%（量比 6.4）、Kits Eyecare +3.5%（量比 4.2）为个股放量，暂无公告。</li>"
  "<li><strong>跌幅榜主线一：金银铜矿集体回吐</strong>：金价回落叠加昨日大涨后获利了结，跌幅榜 30 只中 17 只为矿业——Benz Mining -10.2% 领跌（A$1.5 亿配售刚完成，Simply Wall St 周末点名估值过高）、San Lorenzo -4.9%、Silvercorp -5.1%（昨晚公布 Q2 FY27 产销数据，银品位 159 g/t 同比降 25%）、Rio2 -3.6%、Trilogy -3.3%、NorthIsle -3.1%、First Quantum -3.1%、Capstone -3.0%、Ivanhoe -2.9%、Hudbay -2.9%、Americas G&S -2.6%、Mayfair/Mackay/Faraday/Fireweed/5N Plus/Jaguar -2.3%～-2.6%；榜外铀 Energy Fuels -2.2%（量比 3.5）、Amerigo -2.3%（量比 3.4）、Ero Copper -2.2%。</li>"
  "<li><strong>跌幅榜主线二：AI 算力/科技硬件 CDR 与国内算力股</strong>：GE Aerospace -4.4%（Q3 自由现金流 20.4 亿低于预期 22 亿，虽上调全年指引仍遭抛售）、CoreWeave -3.9%（500 亿美元债务担忧延续，上周五美股 -11.9% 后继续走低）、Meta -3.0%；国内算力链 Xanadu Quantum -2.8%（量比 5.9）、HIVE Digital -2.7%（量比 3.7）、Keel Infrastructure -2.4%、Pason -3.0%、Celestica -1.7%（榜外）同步承压。工业：Bird Construction -2.7%、Finning -2.5%、Major Drilling -2.8%；能源 Spartan Delta -2.9%、Gran Tierra -2.8%、Obsidian -2.3%。</li>"
  "</ul>"),
 "anomalies_html":(
  "<ul>"
  "<li>🔥 <strong>MMMM.TO 3M（CDR）</strong> 量比 148（+4.5%）：3M Q3 调整后 EPS US$2.50 超预期 2.38，美股盘前 +1%；该 CDR 日均量仅 3,685 份，开盘半小时 4.2 万份属极小基数放大，关注度信号而非资金信号。</li>"
  "<li>🔥 <strong>NOC.TO Northrop Grumman（CDR）</strong> 量比 50（+6.5%）：Q3 EPS 7.89 vs 预期 7.18，上调 2026 EPS 指引、book-to-bill 1.5x、积压订单创 1,100 亿新高，美股盘前大涨；CDR 日均量仅 5,241 份，同样小基数。</li>"
  "<li>🔥 <strong>ESI.TO Ensign Energy</strong> 量比 17.5（+4.6%）：TD Cowen 今晨上调评级 Hold→Buy、目标价 C$4.75（隐含 20% 空间），称自由现金流收益率为覆盖范围内最高，开盘半小时 36 万股已超全日均量 26.8 万股。</li>"
  "<li>🔥 <strong>GE.TO GE Aerospace（CDR）</strong> 量比 16（-4.4%）：Q3 EPS 超预期并上调全年指引，但自由现金流 20.4 亿美元不及预期 22 亿，39x 前瞻 PE 下高预期兑现即卖；CDR 日均量 1.5 万份小基数。</li>"
  "<li>🔥 <strong>CRWV.TO CoreWeave（CDR）</strong> 量比 10.4（-3.9%）：上周五美股因 500 亿美元债务/债券收益率飙至 15% 暴跌 11.9%，Cantor 称回调是买点，但今日开盘半小时 18.7 万份已达全日均量 80%，CDR 持有者继续去风险。</li>"
  "<li>🔥 <strong>INTU.TO Intuit（CDR）</strong> 量比 8.1（+4.7%）：10/15–16 连续放量上涨后今日再度放量，无公司公告，软件 CDR 轮动买盘延续。</li>"
  "<li>⚠️ <strong>AIF.TO Altus Group</strong> 量比 6.4（+2.8%）：无当日公告，Q3 业绩定于 11/5；近期有 AI 治理认证、美国二次上市计划题材，疑为机构建仓。</li>"
  "<li>⚠️ <strong>XNDU.TO Xanadu Quantum</strong> 量比 5.9（-2.8%）：量子/AI 概念随美股算力链去风险放量下跌，无公司公告。</li>"
  "<li>⚠️ <strong>KITS.TO Kits Eyecare</strong> 量比 4.2（+3.5%）：无公告，小盘股开盘集中成交。</li>"
  "<li>⚠️ <strong>BZ.V Benz Mining</strong> 量比 4.1（-10.2%）：10/19 公告 A$1.5 亿配售完成，稀释落地 + 周末估值质疑文章（P/B 23x），放量下跌。</li>"
  "<li>⚠️ <strong>SLG.V San Lorenzo Gold</strong> 量比 4.1（-4.9%）、<strong>MACK.V Mackay Gold & Silver</strong> 量比 4.2（-2.4%）：TSXV 勘探股随金价回落放量回吐，无公告。</li>"
  "<li>⚠️ <strong>SVM.TO Silvercorp</strong> 量比 3.8（-5.1%）：Q2 FY27 产销数据——银品位 159 g/t（去年同期 213），财报 11 月初发布，品位下滑引发抛售。</li>"
  "<li>⚠️ <strong>HIVE.TO HIVE Digital</strong> 量比 3.7（-2.7%）、<strong>EFR.TO Energy Fuels</strong> 量比 3.5（-2.2%）、<strong>ARG.TO Amerigo</strong> 量比 3.4（-2.3%）、<strong>LMN.V Lumine</strong> 量比 3.4（+3.5%）、<strong>PD.TO Precision Drilling</strong> 量比 3.7（+1.9%）：板块性放量，无个股公告（PD 受 Ensign 上调带动）。</li>"
  "</ul>"),
 "digest":"TSX 开盘小幅走低、涨跌幅温和：金价回落致金银铜矿集体回吐（Benz -10.2%、Silvercorp -5.1%），美股财报季 CDR 领涨（Northrop +6.5%、3M +4.5%），Ensign 获 TD Cowen 上调 +4.6% 量比 17.5，软件/电信/REIT 防御轮动；GE/CoreWeave/Meta CDR 与国内算力股走弱。",
}
json.dump(data, open(D + "2026-10-20.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in G: print(r)
print("---")
for r in L: print(r)
