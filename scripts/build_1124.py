# -*- coding: utf-8 -*-
"""Build data/2026-11-24.json from data/_merged.json. Live 10:00 ET snapshot, FRAC=0.077."""
import json
M = json.load(open("data/_merged.json", encoding="utf-8"))
OUT = "data/2026-11-24.json"
FRAC = 0.077

def fmtcap(c, cdr=False):
    if not c: return "?"
    s = f"{c/1e9:.1f}B" if c >= 1e9 else f"{c/1e6:.0f}M"
    return s + ("*" if cdr else "")

SEC = {
 "ADEN.TO":"建材分销","TLO.TO":"镍铜(明尼苏达/密歇根)","XNDU.TO":"量子计算","AIF.TO":"房地产软件/咨询","ADBE.NE":"软件 CDR",
 "NKE.TO":"运动服饰 CDR","RDDT.TO":"社交媒体 CDR","LSPD.TO":"零售SaaS","LLY.TO":"制药 CDR","INTU.TO":"财务软件 CDR",
 "MLP.V":"钾肥勘探(加蓬)","OTEX.TO":"企业软件","ENGH.TO":"企业软件","TRI.TO":"信息服务","APPS.TO":"广告科技 CDR",
 "LULU.TO":"运动服饰 CDR","IPCO.TO":"油气(国际)","NFLX.TO":"流媒体 CDR","WSP.TO":"工程咨询","ATZ.TO":"服饰零售",
 "ORE.TO":"黄金生产(布基纳法索)","XLY.TO":"大麻(加拿大)","SOIL.TO":"油气(萨省/阿省轻油)","LNR.TO":"汽车零部件","BHC.TO":"制药",
 "GIB-A.TO":"IT服务","T.TO":"电信","KEL.TO":"油气(蒙尼)","TVE.TO":"油气(克利尔沃特/查理湖)","VLE.TO":"油气(泰国)",
 "IFC.TO":"财产保险","COST.TO":"仓储零售 CDR","WN.TO":"食品零售控股","SDE.TO":"油气(蒙尼/杜弗奈)","MARI.TO":"铜开发(智利)","BIR.TO":"天然气",
 "PNG.V":"水下机器人/国防","DELL.TO":"AI服务器 CDR","MOON.V":"铜锌(挪威)","CRWV.TO":"AI云算力 CDR","NBIS.TO":"AI云算力 CDR",
 "SNDK.TO":"存储 CDR","HUT.TO":"比特币矿机/AI数据中心","KEEL.TO":"AI数据中心/电力","MU.TO":"存储芯片 CDR","AMD.TO":"AI芯片 CDR",
 "ANTH.TO":"AI模型 CDR","FM.TO":"铜(赞比亚/巴拿马)","IVN.TO":"铜(刚果金)","MRV.TO":"数据中心芯片 CDR","AMAT.TO":"半导体设备 CDR",
 "VRT.TO":"数据中心电力/散热 CDR","NVDA.TO":"AI芯片 CDR","LRCX.TO":"半导体设备 CDR","CS.TO":"铜(智利/美国)","SMCI.TO":"AI服务器 CDR",
 "ERO.TO":"铜(巴西)","EFR.TO":"铀/稀土","INTC.TO":"芯片 CDR","TKO.TO":"铜(BC省)","WDC.TO":"存储 CDR","BE.TO":"燃料电池 CDR",
 "FDY.TO":"铜开发(亚利桑那)","III.TO":"铜(BC省)","NCX.V":"铜金勘探(BC省)","HBM.TO":"铜(秘鲁/马尼托巴)","ARG.TO":"铜尾矿(智利)",
 "LUN.TO":"铜(智利/阿根廷)","SLS.TO":"铜开发(厄瓜多尔)","CLS.TO":"AI服务器/电子制造","TECK-B.TO":"铜锌","CNL.TO":"黄金勘探(哥伦比亚)",
}

def row(i, v):
    sym = v["sym"]; cdr = v.get("cdr", False)
    cap = v.get("cap")
    vr = round(v["vol"] / (v["avg"] * FRAC), 1) if v.get("avg") else None
    name = v["name"]
    for cut in (" Shs", " SHS", " Inc.", " Inc", " Corp.", " Corporation", " Limited", " Ltd.", " Company", " N.V", ", "):
        if cut in name: name = name.split(cut)[0]
    name = name.rstrip(", ")
    if cdr: name += " CDR"
    chg = v["chg"]
    return [i, sym, name.strip(), f"{v['price']:.2f}", f"{chg:+.2f}%", fmtcap(cap, cdr), SEC.get(sym, v.get("tvsector") or "?"), vr]

g = M["g"][:30]
l = M["l"][:30]
G = [row(i, v) for i, v in enumerate(g, 1)]
L = [row(i, v) for i, v in enumerate(l, 1)]
for r in G + L:
    if r[6] == "?": print("NO SECTOR", r)

D = {
 "date": "2026-11-24", "weekday": "周二",
 "snapshot": "2026-11-24 10:03 ET 盘中（开盘约 33 分钟）",
 "market_state": "REGULAR",
 "vr_note": "量比 = 当日成交量 ÷ (3个月日均量 × 0.077)，0.077 为开盘 0.5h/6.5h 的时长占比。⚠️≥3，🔥≥8。早盘量比天然偏高（开盘集合竞价+首半小时放量），≥8 才算实质异常。",
 "gainers": G, "losers": L,
 "table_notes": [
  "带 * 的 CDR 行市值为美股母公司总市值的加元换算（TradingView 口径），非加拿大挂牌份额；CDR 现价/涨跌/成交量取 .TO 主挂牌（Yahoo v7 quote），Adobe 以 .NE 行入榜（.TO 行 +4.1%，成交更少）。",
  "Yahoo 80+80 行中 BIPC.TO / BIP-UN.TO（时间戳 11/20，Brookfield Infrastructure 重组后停牌）、VBNK.TO（11/16）为僵尸行已剔除；其余时间戳均为 11/24 10:00 ET 前后。TradingView 交叉验证：涨幅榜 TV 独有的 BMM.V +14.6%、CGG.TO +9.2%、AMX.NE +6.4% 均为 TV 延迟报价（Yahoo 实时分别为 -1.8%/-4.4%/-2.5%，成交仅数百至数千股），未采信；NEO:INTC +16.5%、NEO:META +6.6%、BLK/VLO/STZ 为 Cboe 线昨日残值，已按 .TO 实时行处理。COST.TO Yahoo +1.97% 与 TV -1.6% 不一致，取 Yahoo 实时（前收 47.28）。",
  "早盘涨幅榜整体幅度小（第 1 名仅 +8.6%，第 4 名起 <4.3%），跌幅榜 30 席中 CDR 15 席 + 铜矿 13 席。",
 ],
 "sectors_html": (
  "<ul>"
  "<li><strong>大盘：</strong>TSX 开盘半小时基本持平（34,069，-0.04%），昨日 +2.69% 的报复性反弹暂歇；美股回吐：纳指 -1.15%、标普 -0.34%，道指小跌。WTI 反弹至 ~$81.5（+1.6%，昨跌破 $80 后技术回补）；黄金 -0.7% 至 ~$3,625；<strong>铜 -3.1% 至 $5.54/lb</strong>，为今日板块主线。</li>"
  "<li><strong>涨幅榜主线：缺乏统一主题，个股消息驱动 + 防御/软件补涨。</strong>ADENTRA +8.6%（量比 18）：昨日收盘后宣布以 2.3 亿加元现金收购 AccessSMT（加拿大商用门/五金/门禁分销商，15 个网点、年销售约 2.4 亿加元），预计增厚调整后 EPS 10-15%，全部用现有循环信贷支付、杠杆率升至 ~3.0x，市场看好。Talon Metals +8.4%（量比 8.2）：Tamarack 镍铜项目钻探结果持续发布（11/13 之后又一批 138 区高品位）；今日为铜矿普跌中少见的逆势上涨，属镍为主标的且美国国内关键矿物叙事。Xanadu 量子 +8.0%（量比 5.9），延续昨日 +16.7%，量子股与 AI 板块脱钩。Altus Group +4.2%、Lightspeed +3.2%、Open Text +3.0%、Enghouse +2.9%、Thomson Reuters +2.9%、CGI +2.0%：加拿大软件/信息服务板块在美股科技回吐时逆势补涨，属上周超跌后的轮动。CDR 涨幅榜仅剩防御/消费：Nike +3.5%、Lilly +3.1%、Intuit +3.1%、Adobe +3.5%、AppLovin +2.8%、lululemon +2.7%、Netflix +2.5%、Reddit +3.2%（Costco +2.0% 列第 32）——资金从 AI 硬件切向软件/消费。能源小幅反弹：IPC +2.6%、Saturn +2.3%（昨 -10.2%）、Kelt +1.8%、Tamarack +1.8%、Valeura +1.8%、Spartan Delta +1.7%、Birchcliff +1.7%。</li>"
  "<li><strong>跌幅榜主线一：AI 硬件链回吐昨日涨幅，HPE 利润率警告是导火索。</strong>HPE 昨晚财报营收/EPS 双超预期但 CFO 预警未来半年 AI 服务器毛利率下行，股价 -13.7%；Dell 今晚盘后发财报，受连带 -10%（CDR DELL.TO -10.4%，量比 16.5，昨 +21%）。整条链条跟跌：CoreWeave -8.3%、Nebius -8.1%、SanDisk -8.0%、Micron -7.7%、AMD -7.7%、Anthropic -7.5%、Marvell -5.9%、Applied Materials -5.6%、Vertiv -5.5%、Nvidia -5.5%（美股 -6.0%）、Lam -5.3%、SuperMicro -5.2%、Intel -5.2%（昨 +16%）、Western Digital -4.7%、Bloom -4.7%。本土 AI 周边同步：Hut 8 -7.8%、Keel -7.8%、Celestica -4.1%。</li>"
  "<li><strong>跌幅榜主线二：铜价 -3.1%，铜矿全线下挫（13 席）。</strong>First Quantum -6.7%、Ivanhoe -6.2%、Capstone -5.3%、Ero -5.2%、Trekor -5.1%、Faraday -4.6%、Imperial -4.6%、NorthIsle -4.5%、Hudbay -4.5%、Amerigo -4.3%、Lundin -4.3%、Solaris -4.3%、Teck -3.9%。铜期货回落至 $5.54，叠加昨日反弹后获利了结；TSX 铜板块近一月已 -24%。Blue Moon Metals -8.7%（挪威铜锌，成交仅 3 万股，TV 无报价，疑为薄盘跳价）。</li>"
  "<li><strong>跌幅榜个股：</strong>Kraken Robotics -20.8%（量比 22，225 万股，TSXV 跌幅第一）：Q3 营收 1.02 亿加元 vs 预期 1.156 亿、调整后 EPS $0.03 vs $0.04，国防项目授标延迟 + 海上风电活动疲软，并下调全年指引，收购 Covelya 的重组成本致净亏 1,800 万加元；股价创 52 周新低（2.26）。Energy Fuels -5.2%（铀，跟随风险资产回吐）、Collective Mining -3.9%。</li>"
  "</ul>"),
 "anomalies_html": (
  "<ul>"
  "<li>🔥 <strong>PNG.V 量比 22</strong>（-20.8%，225 万股 vs 日均 133 万，开盘半小时即超全日均量 1.7 倍）：Q3 不及预期 + 下调指引，见上。</li>"
  "<li>🔥 <strong>ADEN.TO 量比 18</strong>（+8.6%，7.1 万股 vs 日均 5.1 万，已超全日均量）：2.3 亿加元收购 AccessSMT，EPS 增厚 10-15%。</li>"
  "<li>🔥 <strong>DELL.TO 量比 16.5</strong>（-10.4%，5.8 万股 vs 日均 4.5 万）：HPE 利润率警告连带 + 今晚财报前获利了结；连续第二日量比 >15，CDR 日均量基数低。</li>"
  "<li>🔥 <strong>BE.TO 量比 11</strong>（-4.7%，7.6 万股 vs 日均 8.9 万）：Bloom Energy CDR，昨 +18% 后回吐，无公司消息，属 AI 电力链情绪交易。</li>"
  "<li>🔥 <strong>TLO.TO 量比 8.2</strong>（+8.4%，44.9 万股 vs 日均 71 万）：Tamarack 钻探结果 + 铜矿普跌中逆势，关注是否有新公告。</li>"
  "<li>⚠️ 量比 3–8（早盘口径下多为正常开盘放量）：LRCX.TO 7.4（-5.3%）、NVDA.TO 7.2（-5.5%）、CRWV.TO 6.6（-8.3%）、MU.TO 6.5（-7.7%）、AMAT.TO 6.1（-5.6%）、XLY.TO 6.0（+2.3%，Auxly 连续第三日放量）、XNDU.TO 5.9（+8.0%）、SNDK.TO 5.3（-8.0%）、LLY.TO 5.2（+3.1%）、INTU.TO 5.0（+3.1%）、ADBE.NE 4.5（+3.5%）、ORE.TO 3.9（+2.3%）、AMD.TO 3.9（-7.7%）、WDC.TO 3.8（-4.7%）、AIF.TO 3.7（+4.2%）、IPCO.TO 3.6（+2.6%）、NKE.TO 3.3（+3.5%）、MLP.V 3.1（+3.1%）、INTC.TO 3.1（-5.2%）、MRV.TO 3.0（-5.9%）。</li>"
  "<li>铜矿跌幅榜量比普遍 <3（First Quantum 2.2、Ivanhoe 2.5、Capstone 1.9、Hudbay 1.6）：铜价驱动的板块性回落，非个股恐慌抛售。</li>"
  "</ul>"),
 "digest": "早盘 10:03 ET：TSX 持平 34,069，纳指 -1.2%——HPE 预警 AI 服务器利润率（-13.7%）引发 AI 硬件链回吐昨日涨幅，Dell CDR -10.4%（今晚财报）、CoreWeave -8.3%、Nebius -8.1%、SanDisk -8.0%、Micron/AMD -7.7%、Nvidia -5.5%；铜价 -3.1% 带崩铜矿 13 席（First Quantum -6.7%、Ivanhoe -6.2%、Capstone -5.3%）。Kraken Robotics Q3 不及预期 -20.8%（量比 22）。涨幅榜无主线：ADENTRA +8.6% 收购 AccessSMT（量比 18）、Talon Metals +8.4%、Xanadu +8.0%，加国软件股（Open Text/Enghouse/Thomson Reuters/CGI）与消费 CDR（Nike/Lilly/Costco）逆势补涨。",
}
json.dump(D, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, len(G), len(L))
for r in G + L: print(r)
