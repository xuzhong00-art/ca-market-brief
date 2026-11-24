# -*- coding: utf-8 -*-
"""Build data/2026-11-23.json from data/_merged.json with manual sector/narrative. Close backfill, FRAC=1.0."""
import json
M = json.load(open("data/_merged.json", encoding="utf-8"))
OUT = "data/2026-11-23.json"

def fmtcap(c, cdr=False):
    if not c: return "?"
    s = f"{c/1e9:.1f}B" if c >= 1e9 else f"{c/1e6:.0f}M"
    return s + ("*" if cdr else "")

SEC = {
 "NVDA.TO":"AI芯片 CDR","CRWV.TO":"AI云算力 CDR","DELL.TO":"AI服务器 CDR","NBIS.TO":"AI云算力 CDR","SGML.V":"锂",
 "OGN.V":"贵金属权利金","MRV.TO":"数据中心芯片 CDR","MU.TO":"存储芯片 CDR","CBRS.TO":"AI芯片 CDR","LUME.TO":"光通信 CDR",
 "BE.TO":"燃料电池 CDR","XNDU.TO":"量子计算","INTC.TO":"芯片 CDR","KEEL.TO":"AI数据中心/电力","COHR.TO":"光通信 CDR",
 "FISH.V":"贵金属权利金","KLAC.TO":"半导体设备 CDR","BMM.V":"黄金勘探(内华达)","VRNO.NE":"大麻(美国)","LRCX.TO":"半导体设备 CDR",
 "AMAT.TO":"半导体设备 CDR","WDC.TO":"存储 CDR","SMCI.TO":"AI服务器 CDR","XLY.TO":"大麻(加拿大)","MAU.TO":"黄金开发(科特迪瓦)",
 "ORAC.TO":"云/数据库 CDR","VRT.TO":"数据中心电力/散热 CDR","HUT.TO":"比特币矿机/AI数据中心","BZ.V":"黄金勘探(澳洲)","NG.TO":"黄金开发(阿拉斯加)",
 "SOIL.TO":"油气(萨省/阿省轻油)","CRWD.TO":"网络安全 CDR","DR.TO":"美国专科外科医院","SCR.TO":"油气/油砂","T.TO":"电信",
 "KEI.TO":"油气(俄克拉荷马)","PXT.TO":"油气(哥伦比亚)","KEL.TO":"油气(蒙尼)","VET.TO":"油气(国际)","BTE.TO":"油气(鹰滩/重油)",
 "STZ.TO":"酒类 CDR","IPCO.TO":"油气(国际)","RBY.TO":"重油(克利尔沃特)","TOU.TO":"天然气","VLE.TO":"油气(泰国)",
 "LCFS.TO":"可再生柴油","IPO.TO":"油气(卡迪姆)","SGY.TO":"油气(轻油)","GTE.TO":"油气(哥伦比亚/厄瓜多尔)","POU.TO":"油气(蒙尼)",
 "TNZ.TO":"油气(荷兰/加拿大)","PEY.TO":"天然气","ALA.TO":"燃气公用事业/中游","AIM.TO":"投资控股","CU.TO":"公用事业",
 "MX.TO":"甲醇","PSK.TO":"油气权利金","CVE.TO":"油砂/炼化","TPZ.TO":"油气权利金/基础设施","XOM.TO":"综合油气 CDR",
}
DROP_G = {"ZNVD.NE"}   # duplicate NVIDIA unsponsored Cboe line

def row(i, v):
    sym = v["sym"]; cdr = v.get("cdr", False)
    cap = v.get("cap")
    vr = round(v["vol"] / v["avg"], 1) if v.get("avg") else None
    name = v["name"]
    for cut in (" Shs", " SHS", " Inc.", " Inc", " Corp.", " Corporation", " Limited", " Ltd.", " Company", " N.V", ", "):
        if cut in name: name = name.split(cut)[0]
    name = name.rstrip(", ")
    if cdr: name += " CDR"
    chg = v["chg"]
    return [i, sym, name.strip(), f"{v['price']:.2f}", f"{chg:+.2f}%", fmtcap(cap, cdr), SEC.get(sym, v.get("tvsector") or "?"), vr]

g = [v for v in M["g"] if v["sym"] not in DROP_G][:30]
l = M["l"][:30]
G = [row(i, v) for i, v in enumerate(g, 1)]
L = [row(i, v) for i, v in enumerate(l, 1)]
for r in G + L:
    if r[6] == "?": print("NO SECTOR", r)

D = {
 "date": "2026-11-23", "weekday": "周一",
 "snapshot": "2026-11-23 16:00 ET 收盘（补跑：电脑早间未运行，数据为全日收盘值）",
 "market_state": "CLOSED",
 "vr_note": "量比 = 当日成交量 ÷ 3个月日均量（收盘后补跑，已开盘时长占比取 1.0）。⚠️≥3，🔥≥8。全日口径下 ≥3 即为实质放量。",
 "gainers": G, "losers": L,
 "table_notes": [
  "带 * 的 CDR 行市值为美股母公司总市值的加元换算（TradingView 口径），非加拿大挂牌份额；CDR 现价/涨跌/成交量取 .TO 主挂牌（Yahoo v7 quote）。NVIDIA 的 Cboe 非赞助线 ZNVD.NE（+28.7%）与 NVDA.TO 重复，已去重。",
  "Yahoo 80+80 行中 BIPC.TO（regularMarketTime 仍为 11/20，已并入 BIP Inc. 停止交易）为僵尸行已剔除；其余时间戳均为 11/23。TradingView 交叉验证涨跌幅一致（BTE.TO Yahoo -3.2% vs TV -3.0%、VET.TO -3.3% vs -3.1% 为收盘前延迟差异，取 Yahoo 收盘值）。",
  "美股 CDR 占涨幅榜 20/30 席，为本简报开栏以来最高；CDR 三个月日均量多为低基数，量比解读需结合绝对成交额。",
 ],
 "sectors_html": (
  "<ul>"
  "<li><strong>大盘：</strong>TSX +2.69% 收 34,081.44（+891.59 点），终结七连跌、创 2025-04-09 以来最大单日涨幅，基本收复上周五 -839 点的失地；TSX 创业板 +3.7% 收 712.63。美股更猛：纳指 +6.51%（历史第二大点数涨幅）、标普 +4.73%、道指 +1,448 点，均为 2025 年 4 月以来最佳单日。</li>"
  "<li><strong>涨幅榜主线一：Nvidia 复辟黄仁勋，AI 算力链全面报复性反弹。</strong>Nvidia 董事会周一早间宣布黄仁勋重新出任总裁兼 CEO（上周因私生活丑闻辞职引发 AI 板块崩塌），NVDA +31% 单日增加约 9,760 亿美元市值，费城半导体指数 +13%。加元渠道 CDR 跟涨：Nvidia +31.0%、CoreWeave +22.4%、Dell +21.0%、Nebius +20.1%、Marvell +19.2%、Micron +19.0%、Cerebras +18.6%、Lumentum +18.5%、Bloom +18.1%、Intel +16.2%、Coherent +15.1%、KLA +14.8%（新加坡新厂 + 47 亿美元指引）、Lam +14.0%、Applied Materials +13.9%、Western Digital +13.5%、SuperMicro +13.3%、Oracle +12.3%、Vertiv +12.1%、Amphenol +11.5%、Tesla +11.2%、Palantir +11.0%、SanDisk +10.7%。本土 AI 周边同步：Xanadu +16.7%、Keel Infrastructure +16.1%（纳斯达克 +19%）、Hut 8 +12.1%、Hammond Power +11.8%、Kraken +11.5%、Electrovaya +10.0%。</li>"
  "<li><strong>涨幅榜主线二：贵金属与矿业超跌反弹。</strong>金价自上周五 14 个月低点反弹 1.5% 至 ~$3,636、白银回到 $43 上方、铜反弹，TSX 材料板块领涨：Montage +12.5%、Seabridge +11.5%（量比 3.4）、Santacruz Silver +11.2%、AbraSilver +11.1%、G Mining +10.9%、Hudbay +10.9%、NovaGold +12.0%、Benz +12.1%、Skeena +9.9%、Amex +10.3%；权利金股 Orogen +19.2%、Sailfish +15.0%、Elemental +10.1%、Metalla +9.7%。Sigma Lithium +20.0%（上周 -14.7% 后反弹，11/16 完成 1.25 亿美元可转债再融资）。</li>"
  "<li><strong>跌幅榜主线：能源单边出清——30 席中 24 席为油气/能源基础设施。</strong>WTI 跌破 $80 至 ~$79.97（-3.4%，8 月以来最低）、Brent ~$92，三周连跌：资金从上周避险的能源/防御板块轮出，回流 AI 风险资产。Saturn -10.2%（11/18 IDEAS 大会后连跌，无公司新消息，本月第四次单日跌幅 >5%）、Strathcona -5.5%（Greenfire 收购联合通函刊发、特别会议定于 2027-01-12，股东稀释预期）、Kolibri -4.1%、Parex -3.9%、Kelt -3.5%、Vermilion -3.3%、Baytex -3.2%、IPC -2.9%、Tourmaline -2.9%、Valeura -2.9%、Paramount -2.5%、Peyto -2.4%、Cenovus -2.1%，公用事业 AltaGas -2.4%、Canadian Utilities -2.2%，权利金 PrairieSky -2.1%、Topaz -2.0%、Freehold -1.9%；CDR 仅 Exxon -2.0%。</li>"
  "<li><strong>跌幅榜个股：</strong>CrowdStrike CDR -9.0%（量比 4.1）：Q3 营收 +28.3% 超预期并上调全年指引，但同日宣布 439 亿美元全股票收购 Zscaler（溢价 34%），市场质疑稀释与整合，为当日纳指少数逆势下跌的科技股。TELUS -4.9%（885 万股）：Quebecor 与 TELUS CEO 周一在渥太华会面讨论收购提议，但分析师普遍认为按现条款达成并获批概率低，自提议公开以来 TELUS +24%、Quebecor -21%，溢价空间已收窄至 11%，获利盘回吐。Medical Facilities -5.5%（量比 6.5）：完成出售阿肯色外科医院 51% 权益（6,300 万美元），资产缩表引发抛售。Constellation Brands CDR -3.1%、Tidewater Renewables -2.7%、Methanex -2.2%、Aimia -2.3%。</li>"
  "</ul>"),
 "anomalies_html": (
  "<ul>"
  "<li>🔥 <strong>DELL.TO 量比 15.6</strong>（+21.0%，44.7 万股 vs 日均 2.9 万）、<strong>KLAC.TO 量比 12.9</strong>（+14.8%，47.3 万股 vs 日均 3.7 万）：AI 服务器/半导体设备 CDR 三个月日均量基数低，黄仁勋回归引发的加元渠道散户追买放大量比；Dell 为 Nvidia 最大服务器合作伙伴。</li>"
  "<li>⚠️ <strong>NVDA.TO 量比 6.3</strong>（+31.0%，1,399 万股，为日均 6.3 倍）、<strong>DR.TO 量比 6.5</strong>（-5.5%，16.2 万股 vs 日均 2.5 万，出售阿肯色医院后抛售）、<strong>XLY.TO 量比 5.7</strong>（+13.0%，71.5 万股，Q3 创纪录业绩后第二波拉升，无新消息）、<strong>CRWD.TO 量比 4.1</strong>（-9.0%，Zscaler 并购）、<strong>VRT.TO 3.7</strong>（+12.1%）、<strong>APH.TO 3.6</strong>（+11.5%）、<strong>SEA.TO 3.4</strong>（+11.5%，金价反弹 + 近期协议收购 Orogen 的 Slaughterhouse 铜金项目）、<strong>AMAT.TO 3.3</strong>（+13.9%）、<strong>XOM.TO 3.3</strong>（-2.0%，油价跌破 $80）。</li>"
  "<li>其余涨跌幅榜量比均 <3：Nvidia 复辟是情绪驱动的全面反弹而非个股消息，本土矿业/能源成交量基本在正常区间（Hudbay 360 万股为日均 1.7 倍、Baytex 732 万股 1.5 倍）。</li>"
  "</ul>"),
 "digest": "收盘补跑：TSX +2.69% 收 34,081 终结七连跌、创 2025-04 以来最大单日涨幅，纳指 +6.5%——Nvidia 复辟黄仁勋出任 CEO，NVDA +31%，AI 算力链报复性反弹，CDR 占涨幅榜 20/30 席（CoreWeave +22.4%、Dell +21.0%、Nebius +20.1%、Marvell +19.2%、Micron +19.0%）；金价自 14 个月低点反弹 1.5%，矿业跟涨（Montage +12.5%、Seabridge/Santacruz/AbraSilver/Hudbay +11%、Sigma Lithium +20%）。跌幅榜 24/30 为能源：WTI 跌破 $80，Saturn -10.2%、Strathcona -5.5%、Parex -3.9%、Baytex -3.2%；CrowdStrike CDR -9.0%（439 亿美元收购 Zscaler）、TELUS -4.9%（Quebecor 会谈但成交概率低）。",
}
json.dump(D, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, len(G), len(L))
for r in G + L: print(r)
