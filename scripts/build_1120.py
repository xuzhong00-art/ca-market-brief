# -*- coding: utf-8 -*-
"""Build data/2026-11-20.json from data/_merged.json (+ raw extras) with manual sector/narrative. Close backfill, FRAC=1.0."""
import json
M = json.load(open("data/_merged.json", encoding="utf-8"))
R = json.load(open("data/_raw.json", encoding="utf-8"))
OUT = "data/2026-11-20.json"

def fmtcap(c, cdr=False):
    if not c: return "?"
    s = f"{c/1e9:.1f}B" if c >= 1e9 else f"{c/1e6:.0f}M"
    return s + ("*" if cdr else "")

SEC = {
 "BIPC.TO":"基础设施(并入BIP Inc.前最后交易日)","TNZ.TO":"油气(荷兰/加拿大)","CDR.TO":"天然气(乌兹别克)","QBR-B.TO":"电信/媒体",
 "BIP-UN.TO":"基础设施","BYD.TO":"汽车碰撞维修","DRX.TO":"钢结构制造(魁北克)","RCI-A.TO":"电信(A类薄流通股)","CGO.TO":"电信控股",
 "CCA.TO":"有线电信","UNH.TO":"医疗保险 CDR","TLO.TO":"镍矿开发(明尼苏达)","BCE.TO":"电信","T.TO":"电信","GORO.V":"黄金生产(墨西哥)",
 "HMM-A.TO":"电气外壳制造","VREO.CN":"大麻(美国)","ATD.TO":"便利店零售","TF.TO":"商业地产贷款","MRU.TO":"食品零售",
 "DHI.TO":"住宅建筑 CDR","WMT.TO":"大型零售 CDR","VZ.TO":"电信 CDR","SNY.TO":"制药 CDR","PVF-UN.V":"投资控股(Brookfield系)",
 "LNF.TO":"家具零售","GRT-UN.TO":"工业地产REIT","BTB-UN.TO":"商业地产REIT","XTC.TO":"汽车零部件","WN.TO":"食品零售控股",
 "HUT.TO":"比特币矿机/AI数据中心","SNDK.TO":"存储芯片 CDR","CLS.TO":"AI服务器/电子制造","NBIS.TO":"AI云算力 CDR","BE.TO":"燃料电池 CDR",
 "HG.CN":"石墨烯","SGML.V":"锂","KRY.V":"铜开发(纳米比亚)","AUXX.V":"黄金生产(多米尼加)","LUME.TO":"光通信 CDR","NVDA.TO":"AI芯片 CDR",
 "MU.TO":"存储芯片 CDR","AMD.TO":"芯片 CDR","INTU.TO":"财税软件 CDR","COHR.TO":"光通信 CDR","CRWV.TO":"AI云算力 CDR","MRV.TO":"数据中心芯片 CDR",
 "ABXX.TO":"商品交易所/科技","AVGO.TO":"AI芯片 CDR","TMQ.TO":"铜开发(阿拉斯加)","WDC.TO":"存储 CDR","ANET.TO":"网络设备 CDR",
 "SICO.V":"白银勘探","DELL.TO":"AI服务器 CDR","ABRA.TO":"白银开发(阿根廷)","ELVA.TO":"锂电池","CAML.TO":"铜锌生产(哈萨克/马其顿)",
 "RKLB.TO":"航天 CDR","ZDC.V":"安防/移动监控塔","ASTL.TO":"钢铁",
}
CAP_OVR = {"PVF-UN.V": 10.7e9, "CAML.TO": 0.55e9}
DROP_L = {"ZNVD.NE", "ZAVG.NE"}   # duplicate NVIDIA / Broadcom CDRs (unsponsored Cboe lines)

def row(i, v):
    sym = v["sym"]; cdr = v.get("cdr", False)
    cap = CAP_OVR.get(sym, v.get("cap"))
    vr = round(v["vol"] / v["avg"], 1) if v.get("avg") else None
    name = v["name"]
    for cut in (" Shs", " SHS", " Inc.", " Inc", " Corp.", " Corporation", " Limited", " Ltd.", " Company", " N.V", ", "):
        if cut in name: name = name.split(cut)[0]
    name = name.rstrip(", ")
    if cdr: name += " CDR"
    chg = v["chg"]
    return [i, sym, name.strip(), f"{v['price']:.2f}", f"{chg:+.2f}%", fmtcap(cap, cdr), SEC.get(sym, v.get("tvsector") or "?"), vr]

g = M["g"][:30]
l = [v for v in M["l"] if v["sym"] not in DROP_L]
extra = {q["symbol"]: q for q in R["yl"]}
for s in ("ZDC.V", "ASTL.TO"):
    q = extra[s]
    l.append({"sym": s, "name": q["longName"], "price": q["regularMarketPrice"], "chg": q["regularMarketChangePercent"],
              "cap": q["marketCap"], "vol": q["regularMarketVolume"], "avg": q["averageDailyVolume3Month"], "cdr": False})
l = sorted(l, key=lambda x: x["chg"])[:30]
G = [row(i, v) for i, v in enumerate(g, 1)]
L = [row(i, v) for i, v in enumerate(l, 1)]
for r in G + L:
    if r[6] == "?": print("NO SECTOR", r)

D = {
 "date": "2026-11-20", "weekday": "周五",
 "snapshot": "2026-11-20 16:00 ET 收盘（补跑：电脑早间未运行，数据为全日收盘值）",
 "market_state": "CLOSED",
 "vr_note": "量比 = 当日成交量 ÷ 3个月日均量（收盘后补跑，已开盘时长占比取 1.0）。⚠️≥3，🔥≥8。全日口径下 ≥3 即为实质放量。",
 "gainers": G, "losers": L,
 "table_notes": [
  "带 * 的 CDR 行市值为美股母公司总市值的加元换算（TradingView 口径），非加拿大挂牌份额；CDR 现价/涨跌/成交量取 .TO 主挂牌（Yahoo v7 quote）。NVIDIA/Broadcom 的 Cboe 非赞助线 ZNVD.NE/ZAVG.NE 与 NVDA.TO/AVGO.TO 重复，已去重。",
  "BIPC.TO +10.6%：11/19 Brookfield Infrastructure 完成公司简化，BIPC 与 BIP.UN 1:1 换成 BIP Inc. A 股，11/23 起以 BIP 代码交易——11/20 为 BIPC 最后交易日，收盘集合竞价 4,030 万股换仓（量比 103）把收盘价推到 $65.40（午间仍为 $59.37），属结构性换仓价差而非基本面行情，BIP.UN 同日 +4.6% 收 $61.66。",
  "RCI-A.TO（Rogers A 类）、DHI.TO、SNY.TO 为薄流通线（3 个月日均量仅 1.5K–3.4K 股），量比 14–18 为小基数效应，无独立消息；Rogers 主流通 B 类 RCI-B +3.3%。Partners Value（PVF-UN.V）Yahoo 无市值，取 TradingView 10.7B。",
  "Yahoo 80+80 行中 VBNK.TO（VersaBank 旧代码，regularMarketTime 仍为 11/16，已更名 VRSA.TO）为僵尸行已剔除；其余时间戳均为 11/20。TradingView 交叉验证涨跌幅一致（KRY.V Yahoo -14.3% vs TV -11.7%、HG.CN -14.8% vs -14.3% 为延迟报价差异，取 Yahoo 收盘值）。",
 ],
 "sectors_html": (
  "<ul>"
  "<li><strong>大盘：</strong>TSX -2.47% 收 33,189.85（-838.88 点），连跌七日、自 11/11 累跌 8.8%，较 8 月底历史高点回撤逾 10% 进入技术性调整；周跌 8.1% 为年内最惨一周。纳指 -5.28%、标普 -3.70%，VIX 跳升至 35.9。TSX 创业板 -3.9% 收 688。</li>"
  "<li><strong>跌幅榜主线一：AI 算力链崩塌。</strong>Nvidia 财报后次日 AI 交易全面出清，Celestica -16.4%（TSX 科技板块 -6%，权重最大拖累）、Hut 8 -17.7%（比特币四个月低点 + AI 数据中心叙事双杀，无公司消息）。CDR 跌幅榜 17 只：SanDisk -16.8%、Nebius -16.3%、Bloom -15.4%、Lumentum -13.9%、Nvidia -13.9%、Micron -13.8%、AMD -13.2%、Intuit -12.9%、Coherent -12.9%、CoreWeave -12.5%、Marvell -12.3%、Broadcom -12.2%、Western Digital -12.0%、Arista -11.9%、Dell -11.5%、Rocket Lab -11.1%。本土 AI 周边 Abaxx -12.3%、Electrovaya -11.4%、HydroGraph -14.8%。</li>"
  "<li><strong>跌幅榜主线二：金属全线重挫。</strong>美元指数 19 个月新高 + 美联储 12 月加息预期 + 中国数据疲弱，黄金 -3.7%（12 月合约 -$170 至 $3,515，14 个月低点）、白银 -7%、铜 -2.5%，TSX 黄金分项 -5%、材料 -4.8%：Sigma Lithium -14.7%、Koryx -14.3%（Haib PFS 后利好出尽）、Gold X2 -14.0%、Trilogy -12.0%、Silverco -11.7%、AbraSilver -11.5%（量比 7.4，全日 623 万股）、Central Asia Metals -11.1%，榜外 Vizsla -10.6%、Skeena -9.3%、Ero -8.3% 等批量 -8~-10%。</li>"
  "<li><strong>涨幅榜主线：防御性板块抱团。</strong>全市场仅 185 涨 / 830 跌，TSX 仅 5 个分项收涨——电信 +3.2%（Quebecor +5.7%、Rogers +3.3~3.5%、Cogeco +3.0~3.5%、BCE +2.5%、TELUS +2.3%，BCE 入局 TELUS 传闻延续、估值洼地资金避险）、必需消费 +1.3%（Metro +1.8%、Couche-Tard +2.0%、George Weston +1.4%、Leon's +1.5%）、公用事业 +0.4%（BIP.UN +4.6%，BIPC +10.6% 为换仓价差）。个股：Tenaz +7.1%（油价 WTI ~$91 高位，Q3 后反弹）、Condor +5.9%（乌兹别克产量创纪录延续）、Boyd +4.4%、ADF +4.3%（史上最大合同后第二日续涨）。CDR 涨幅榜仅防御性 4 只：UnitedHealth +2.9%、D.R. Horton +1.7%、Walmart +1.7%、Verizon +1.7%。</li>"
  "</ul>"),
 "anomalies_html": (
  "<ul>"
  "<li>🔥 <strong>BIPC.TO 量比 103</strong>（+10.6%）：最后交易日换仓，收盘集合竞价 4,030 万股（日均 39 万），非基本面行情，11/23 起并入 BIP。</li>"
  "<li>🔥 <strong>RCI-A.TO 量比 17.3</strong>（+3.5%）、<strong>DHI.TO 量比 18.5</strong>（+1.7%）、<strong>SNY.TO 量比 14.2</strong>（+1.7%）：薄流通线小基数效应，无独立消息。</li>"
  "<li>🔥 <strong>LUME.TO 量比 12.8</strong>（-13.9%）、<strong>NBIS.TO 量比 10.9</strong>（-16.3%）、<strong>ZAVG.NE 量比 8.9</strong>（已去重）、<strong>DELL.TO 量比 8.0</strong>（-11.5%）：AI 光通信/云算力/服务器 CDR 恐慌抛售，散户加元渠道集中出逃。</li>"
  "<li>⚠️ <strong>ABRA.TO 量比 7.4</strong>（-11.5%）：白银 -7% 单日暴跌下的高贝塔白银开发股，623 万股为 7 月以来最大量。</li>"
  "<li>⚠️ <strong>NVDA.TO 量比 7.3</strong>（-13.9%，1,458 万股）、<strong>KRY.V 量比 6.9</strong>（-14.3%，PFS 后第三日放量回吐）、<strong>BIP-UN.TO 量比 6.8</strong>（+4.6%，同为换仓最后日）、<strong>BE.TO 量比 6.0</strong>、<strong>RKLB.TO 量比 5.2</strong>、<strong>INTU.TO 3.9</strong>、<strong>COHR.TO 3.9</strong>、<strong>ANET.TO 3.8</strong>、<strong>WMT.TO 3.5</strong>（+1.7%，财报后避险买盘）、<strong>AVGO.TO 3.2</strong>、<strong>MU.TO 3.1</strong>、<strong>TNZ.TO 3.0</strong>。</li>"
  "</ul>"),
 "digest": "收盘补跑：TSX -2.47% 收 33,190 连跌七日进入技术性调整（周跌 8.1%，年内最惨一周），纳指 -5.3%——AI 算力链崩塌：Hut 8 -17.7%、Celestica -16.4%，CDR 跌幅榜 17 只（SanDisk -16.8%、Nebius -16.3%、Nvidia -13.9%、Micron -13.8%、AMD -13.2%）；金属全线重挫（金 -3.7% 14 个月低、银 -7%）：Sigma -14.7%、Koryx -14.3%、AbraSilver -11.5%。涨幅榜仅剩防御抱团：电信 +3.2%（Quebecor +5.7%、Rogers +3.3%、BCE/TELUS +2.3~2.5%）、必需消费 +1.3%；BIPC +10.6% 为并入 BIP Inc. 最后交易日的换仓价差（量比 103）。",
}
json.dump(D, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, len(G), len(L))
for r in G + L: print(r)
