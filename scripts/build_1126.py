# -*- coding: utf-8 -*-
"""Build data/2026-11-26.json from data/_merged.json. Post-close catch-up run (fetched ~20:45 ET), FRAC=1.0."""
import json
M = json.load(open("data/_merged.json", encoding="utf-8"))
OUT = "data/2026-11-26.json"
FRAC = 1.0

def fmtcap(c, cdr=False):
    if not c: return "?"
    s = f"{c/1e9:.1f}B" if c >= 1e9 else f"{c/1e6:.0f}M"
    return s + ("*" if cdr else "")

SEC = {
 "ARA.TO":"稀土开发(巴西/智利)","DC-A.TO":"矿业投资控股","CDR.TO":"天然气(乌兹别克)","AUXX.V":"黄金勘探(安大略)","CAD.V":"煤炭(BC省)",
 "ABXX.TO":"商品交易所/金融科技","USA.TO":"银矿(美国/墨西哥)","MAL.TO":"航空零部件","MARI.TO":"铜开发(智利)","FTG.TO":"航空电子",
 "PNG.V":"水下机器人/防务","CADY.TO":"黄金勘探(魁北克)","TLO.TO":"镍铜开发(美国)","SICO.V":"银矿","FAR.TO":"矿业钻探服务",
 "ERD.TO":"黄金(蒙古)","ELVA.TO":"锂电池","JOY.TO":"油气(阿省)","PDN.TO":"铀(纳米比亚)","ISO.TO":"铀勘探(萨省)",
 "NBIS.TO":"AI云算力 CDR","JAG.TO":"黄金(巴西)","TALA.TO":"黄金勘探","LBS.TO":"分级基金(金融股)","NUAG.TO":"银矿开发(玻利维亚)",
 "AMX.V":"黄金勘探(魁北克)","QTRH.TO":"智能交通/专利","AYA.TO":"银矿(摩洛哥)","DELL.TO":"AI服务器 CDR","REG.V":"铜金勘探(秘鲁)",
 "EM.V":"镍铜勘探(萨德伯里)","LUNR.TO":"矿业权利金","VGZ.TO":"黄金开发(澳洲)","BBD-B.TO":"公务机","HMMC.TO":"黄金(安大略)","MDA.TO":"航天/卫星",
 "NEE.TO":"公用事业 CDR","DIV.TO":"特许权使用费","F.TO":"汽车 CDR","XNDU.TO":"量子计算","CURA.TO":"美国大麻(MSO)","ASTL.TO":"钢铁",
 "LNR.TO":"汽车零部件","CCL-B.TO":"标签包装","D-UN.TO":"办公 REIT","CAR-UN.TO":"公寓 REIT","CSU.TO":"垂直软件","ASML.TO":"光刻机 CDR",
 "ADEN.TO":"建材分销","GUD.TO":"制药","DXT.TO":"设施服务","BCE.TO":"电信","XLY.TO":"大麻","QBR-B.TO":"电信/媒体","RCI-B.TO":"电信",
 "MRG-UN.TO":"住宅 REIT","DRM.TO":"地产开发","CCA.TO":"有线/电信","RBA.TO":"资产拍卖平台","NPI.TO":"可再生电力","MRE.TO":"汽车零部件",
 "PBH.TO":"食品加工","FFH.TO":"保险","AC.TO":"航空","EXE.TO":"养老护理","CGX.TO":"影院","BEI-UN.TO":"公寓 REIT","NA.TO":"银行",
 "AIF.TO":"地产软件/咨询","FSZ.TO":"资产管理","WCN.TO":"废物处理",
}
NAME = {"NBIS.TO":"Nebius CDR","DELL.TO":"Dell CDR","NEE.TO":"NextEra Energy CDR","F.TO":"Ford CDR","ASML.TO":"ASML CDR",
 "DC-A.TO":"Dundee Corp","USA.TO":"Americas Gold & Silver","PNG.V":"Kraken Robotics","FAR.TO":"Foraco International",
 "LBS.TO":"Life & Banc Split","CCL-B.TO":"CCL Industries","D-UN.TO":"Dream Office REIT","CAR-UN.TO":"CAPREIT",
 "QBR-B.TO":"Quebecor","RCI-B.TO":"Rogers Communications","MRG-UN.TO":"Morguard NA Residential REIT","FFH.TO":"Fairfax Financial",
 "CSU.TO":"Constellation Software","XNDU.TO":"Xanadu Quantum","CURA.TO":"Curaleaf","QTRH.TO":"Quarterhill","ERD.TO":"Erdene Resource"}

def row(i, v):
    sym = v["sym"]; cdr = v.get("cdr", False)
    vr = round(v["vol"] / (v["avg"] * FRAC), 1) if v.get("avg") else None
    name = v["name"]
    for cut in (" Shs", " SHS", " Inc.", " Inc", " Corp.", " Corporation", " Limited", " Ltd.", " Ltd", " Company", " N.V", ", ", " SA"):
        if cut in name: name = name.split(cut)[0]
    name = name.rstrip(", ")
    if cdr and "CDR" not in name: name += " CDR"
    name = NAME.get(sym, name.strip())
    return [i, sym, name, f"{v['price']:.2f}", f"{v['chg']:+.2f}%", fmtcap(v.get("cap"), cdr), SEC.get(sym, v.get("tvsector") or "?"), vr]

DROP = {"SLF-PC.TO"}  # Sun Life preferred share, not common equity
g = [v for v in M["g"] if v["sym"] not in DROP][:30]
l = [v for v in M["l"] if v["sym"] not in DROP][:30]
G = [row(i, v) for i, v in enumerate(g, 1)]
L = [row(i, v) for i, v in enumerate(l, 1)]
for r in G + L:
    if r[6] == "?": print("NO SECTOR", r)

D = {
 "date": "2026-11-26", "weekday": "周四",
 "snapshot": "2026-11-26 16:00 ET 收盘（本期为补跑，排程未于 10:00 ET 执行，数据为全日收盘值）",
 "market_state": "CLOSED",
 "vr_note": "量比 = 当日成交量 ÷ 3个月日均量（收盘后补跑，开盘时长占比取 1.0）。⚠️≥3，🔥≥8。",
 "gainers": G, "losers": L,
 "table_notes": [
  "带 * 的 CDR 行市值为美股母公司总市值的加元换算（TradingView 口径），非加拿大挂牌份额；CDR 现价/涨跌/成交量取 .TO 主挂牌（Yahoo v7 quote）。",
  "今日为美国感恩节、美股休市，CDR 无美股母公司参考价，全日仅靠多伦多本地撮合，成交极薄（Nebius CDR 全天仅 7,418 股、Ford CDR 16,650 股），其涨跌幅更多反映 CDR 自身供需与汇率对冲，不代表美股方向，参考价值有限。",
  "Yahoo 80+80 行中剔除僵尸行：BIPC.TO / BIP-UN.TO（时间戳 11/20，Brookfield Infrastructure 重组旧代码停牌）、HWX.TO（Headwater，时间戳 11/20）、AMAT.NE / BRK.NE（Cboe 线 11/25 旧价、0%）。SLF-PC.TO（Sun Life 优先股 -1.07%，量比 3.2）为优先股非普通股，已从跌幅榜剔除。其余时间戳均为 11/26 收盘。",
  "TradingView 交叉验证：涨幅榜 30 只全部在 TV 加股涨幅榜出现且涨跌幅一致（误差 <0.1pt）；FAR/LBS/EM 在 TV 60 行外，用 symbol lookup 单独核对一致。跌幅榜 TV 独有的 NEO 线行（NEO:DIV/XNDU/BCE）为 Cboe 滞后报价、同一标的，按 .TO 保留。NEO:TXN -7.7%（TI CDR）时间戳为 11/25，Yahoo 无今日成交，未入榜。",
 ],
 "sectors_html": (
  "<ul>"
  "<li><strong>大盘：</strong>TSX 收 34,426.88（+0.72%，+246.89 点），连涨第二日，收于 11/18 以来最高；美股感恩节休市，多伦多独自交易、整体量能偏淡。能源板块 +1.9%（胡塞武装称打击沙特最大炼厂、伊朗称霍尔木兹海峡有船只触雷，WTI +1.5~1.9% 至 ~$85）；材料板块 +1.7%（铜 +0.6% 至 $5.45/lb 反弹、白银 +3.1% 至 $41.8、黄金 +0.8% 至 ~$3,594）；科技板块在前一日全球抛售后反弹。加元 70.2 美分（-0.03%）；天然气 -1.7%；比特币 ~$60.6K 持平。12 个子板块中 9 个上涨，材料、能源、黄金领涨。</li>"
  "<li><strong>涨幅榜主线一：矿业/资源全面反弹（30 席中 19 席）。</strong>贵金属随银价 +3% 领涨——Americas Gold & Silver +6.7%（11/13 Q3 后跌至 52 周低点，今日银价反弹 + 11/25 Crux 报道锑副产品收入线，超跌反弹；量比 0.5）、Aya +4.4%、New Pacific +4.5%、Silverco +5.1%、Cadillac +5.5%、Jaguar +4.6%、Amex +4.5%、Talamore +4.6%、Erdene +5.0%、Gold X2 +9.0%（从 $3.06 52 周低点反弹，Moss 项目；量比 0.3）；铜/镍：Marimaca +6.3%（Sprott US$4.5 亿融资后连续第二日上涨）、Talon Metals +5.5%、Regulus +4.3%（量比 2.4）；铀：Paladin +4.9%、IsoEnergy +4.8%；稀土龙头 Aclara +13.4% 居首（11/24 聘美国国务院前执行秘书 Lisa Kenna 任 EVP 政府关系，11/26 智利媒体热议其华府背景，叠加 11/17 磁体级 NdPr 金属产出、美国进出口银行 $7.5 亿意向函——但仅 5.9 万股、量比 0.5，属低量拉升）。</li>"
  "<li><strong>涨幅榜主线二：能源随油价。</strong>Condor Energies +9.3%（乌兹别克斯坦天然气，11 月产量创纪录 18,631 boe/d、Q3 销售 +24% QoQ、11/16 新版 PPT 公布 North Syuzma 碎屑岩新层系 54m 净产层）、Colonial Coal +8.9%（昨日 +2.4% 后续涨，BC 煤矿资产出售预期）、Journey Energy +4.9%。</li>"
  "<li><strong>涨幅榜主线三：加拿大防务/航空与个股消息。</strong>Dundee Corp +10.1%（11/24 Ventum 买入评级、目标价 C$4.80 较前收盘有 49% 上行空间；矿业投资组合随金银反弹，Shovelnose 项目；量比 0.8）；Abaxx +8.6%（11/16 推出人民币计价新加坡黄金期货和 LNG 期货新合约，11/24 宣布 12/11 迈阿密年终投资者论坛；量比 1.2）；Magellan Aerospace +6.5%（11/11 Q3 后一度 $38.67，回落后反弹）、Firan +6.0%（11/13 创纪录季报 + 11/4 $1,500 万加拿大反干扰系统订单）、Bombardier +4.2%、MDA Space +4.1% 列 31–36；Kraken Robotics +5.6%（11/24 Q3 下修 2026 指引后暴跌，ATB Cormark 目标价砍半至 $2.50，今日技术反弹，量比 1.2）；Electrovaya +5.0%（Janus Electric $2,600 万电池订单交付推进）；Quarterhill +4.4%。CDR 中 Nebius +4.6%、Dell +4.3% 上榜，但见上方「美股休市」注——仅数千至数万股薄量。</li>"
  "<li><strong>跌幅榜主线：无主线，普跌幅度极小（第 30 名仅 -0.5%）。</strong>美股休市 + TSX 普涨，跌幅榜由利率敏感/防御板块的小幅回吐填满：电信四家（BCE -0.8%、Quebecor -0.7%、Rogers -0.7%、Cogeco -0.7%）、REIT 五家（Dream Office -1.0%、CAPREIT -0.9%、Morguard -0.7%、Boardwalk -0.5%）、Northland Power -0.7%、Fairfax -0.6%、National Bank -0.5%——加拿大央行行长 11/25 暗示 12 月可能再加息，利率敏感板块承压。个股：Diversified Royalty -3.4%（11/25 完成 $5,000 万 6% 可转债发行、转股价 $4.66，用以赎回 2027 年到期旧债；成交 76.7 万股、量比 1.5，为跌幅榜本土第一）；Xanadu Quantum -2.1%（量子计算概念回落）；Curaleaf -1.7%（前日 MSO 板块大涨后回吐）；Algoma Steel -1.6%、Linamar -1.3%、Martinrea -0.6%（昨日汽车/钢铁涨后回落）；Constellation Software -0.9%。CDR：NextEra -4.9%（量比 7.9 ⚠️）、Ford -3.3%、ASML -0.9%（量比 4.4 ⚠️）——均为美股休市日薄量 CDR 错价，见异常量比。</li>"
  "</ul>"),
 "anomalies_html": (
  "<ul>"
  "<li>⚠️ <strong>NEE.TO 量比 7.9</strong>（-4.9%，7.9 万股 vs .TO 日均 1.0 万）：NextEra Energy CDR。美股休市、母公司无报价（美股 11/25 收 +1.0%），CDR 在无参考价下被卖单砸出 -4.9%，为典型的休市日 CDR 流动性错价，不代表 NextEra 基本面；明日美股开盘后大概率回归。</li>"
  "<li>⚠️ <strong>ASML.TO 量比 4.4</strong>（-0.9%，20.2 万股 vs 日均 4.6 万）：ASML CDR 单日 20 万股为近月最大，疑为机构大宗换手（11/25 美股 ASML -2.5%，CDR 今日仅跟跌 0.9%）；价格平稳、量大，属持仓调整而非恐慌。</li>"
  "<li>⚠️ <strong>SLF-PC.TO 量比 3.2</strong>（-1.1%，2.3 万股 vs 日均 7 千）：Sun Life 优先股（已从主表剔除），BoC 加息预期下浮息/固息优先股换手放大，与普通股无关。</li>"
  "<li><strong>REG.V 量比 2.4 / EM.V 量比 2.8</strong>（+4.3% / +4.3%）：Regulus（AntaKori 铜金，秘鲁）与 Errington Metals（萨德伯里镍铜，11/9 提交资源量技术报告）均为小盘勘探股，放量上涨接近 ⚠️ 门槛，EM 列第 31 未入前 30。</li>"
  "<li>涨幅榜前 10 量比全部 ≤1.2（Aclara 0.5、Dundee 0.8、Condor 1.1、Gold X2 0.3、Colonial 0.7、Abaxx 1.2、Americas 0.5）：美股休市日整体量能偏低，今日榜单是「低量反弹」而非资金涌入，持续性需看明日美股半日市与下周表现。</li>"
  "</ul>"),
 "digest": "收盘补跑：TSX +0.72% 收 34,427（八日新高），美股感恩节休市、多伦多独自交易量能偏淡。油价受中东袭击消息 +1.5~1.9%、白银 +3%、铜反弹，能源 +1.9%、材料 +1.7% 领涨——涨幅榜 30 席矿业/资源占 19：Aclara 稀土 +13.4%（聘前美国务院高官）、Dundee +10.1%（Ventum 目标价 $4.80）、Condor Energies +9.3%（乌兹别克产量创纪录）、Gold X2 +9.0%、Colonial Coal +8.9%、Abaxx +8.6%、Americas Gold & Silver +6.7%、Magellan +6.5%、Marimaca +6.3%、Firan +6.0%。跌幅榜无主线、第 30 名仅 -0.5%，电信/REIT 小幅回吐（BoC 暗示 12 月加息）；本土最大跌幅 Diversified Royalty -3.4%（$5,000 万可转债完成发行）。CDR 薄量错价：NextEra -4.9%（量比 7.9⚠️）、Ford -3.3%、ASML 量比 4.4⚠️。",
}
json.dump(D, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, len(G), len(L))
for r in G + L: print(r)
