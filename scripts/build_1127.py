# -*- coding: utf-8 -*-
"""Build data/2026-11-27.json from data/_merged.json. Post-close catch-up run (fetched ~21:00 ET), FRAC=1.0."""
import json
M = json.load(open("data/_merged.json", encoding="utf-8"))
META = json.load(open("data/_meta.json", encoding="utf-8"))
OUT = "data/2026-11-27.json"
FRAC = 1.0

def fmtcap(c, cdr=False):
    if not c: return "?"
    s = f"{c/1e9:.1f}B" if c >= 1e9 else f"{c/1e6:.0f}M"
    return s + ("*" if cdr else "")

SEC = dict(META["SEC"])
SEC.update({
 "BTQ.NE":"后量子安全/量子软件","SBI.TO":"黄金(巴西)","SKE.TO":"黄金开发(BC金三角)","EDR.TO":"银矿(墨西哥)","MDP.TO":"专科制药",
 "GSKR.V":"黄金勘探","CGG.TO":"黄金/铜(中国)","ELD.TO":"黄金(土耳其/加)","PRN.TO":"医疗器械(前列腺消融)","BTO.TO":"黄金(马里/菲律宾)",
 "SVM.TO":"银矿(中国)","CTGO.TO":"黄金(阿拉斯加)","GGD.TO":"银金(墨西哥)","SGD.TO":"黄金勘探(育空)","TXR.TO":"黄金(墨西哥)",
 "WSTR.V":"医疗信息化(EMR/计费)","RSI.TO":"糖业/枫糖","HITI.V":"大麻零售","AP-UN.TO":"办公 REIT","AFN.TO":"农业设备",
 "BA.TO":"航空航天 CDR","GO-U.TO":"住宅 REIT(美国)","EMP-A.TO":"食品零售","TOI.V":"垂直软件(欧洲)","GS.TO":"投行 CDR",
 "SFC.TO":"保险(加勒比)","TJX.TO":"折扣零售 CDR","L.TO":"食品零售/药房","NWC.TO":"北方零售","DIR-UN.TO":"工业 REIT","ACO-X.TO":"公用事业/物流",
 "SNDK.TO":"NAND闪存 CDR","COHR.TO":"光通信/激光 CDR","ANTH.TO":"AI大模型 CDR","CBRS.TO":"AI芯片 CDR","CEGS.TO":"核电公用 CDR",
 "DGX.NE":"数据中心/AI算力","NCX.V":"铜金开发(温哥华岛)","VRNO.NE":"美国大麻(MSO)","ABRA.TO":"银矿开发(阿根廷)","SCZ.TO":"银矿(玻利维亚)",
 "DSV.TO":"银矿开发(墨西哥)","GMIN.TO":"黄金(巴西/加)","PPTA.TO":"金锑开发(爱达荷)","MAU.TO":"黄金开发(科特迪瓦)","ERO.TO":"铜矿(巴西)",
 "ZDC.V":"移动安防塔租赁","TWM.TO":"中游/炼油","LCFS.TO":"可再生柴油","KEI.TO":"油气(俄克拉荷马)","VLE.TO":"油气(泰国)",
})
NAME = dict(META["NAME"])
NAME.update({"SNDK.TO":"SanDisk CDR","COHR.TO":"Coherent CDR","ANTH.TO":"Anthropic CDR","BA.TO":"Boeing CDR","CBRS.TO":"Cerebras CDR",
 "GS.TO":"Goldman Sachs CDR","TJX.TO":"TJX CDR","CEGS.TO":"Constellation Energy CDR","BTQ.NE":"BTQ Technologies","DGX.NE":"Digi Power X",
 "NCX.V":"Northisle Copper & Gold","USA.TO":"Americas Gold & Silver","VRNO.NE":"Verano Holdings","AP-UN.TO":"Allied Properties REIT",
 "GO-U.TO":"GO Residential REIT","EMP-A.TO":"Empire Co","TOI.V":"Topicus.com","DIR-UN.TO":"Dream Industrial REIT","ACO-X.TO":"ATCO",
 "CGG.TO":"China Gold International","WSTR.V":"WELLSTAR Technologies","TWM.TO":"Tidewater Midstream","NWC.TO":"North West Company"})

def row(i, v):
    sym = v["sym"]; cdr = v.get("cdr", False)
    vr = round(v["vol"] / (v["avg"] * FRAC), 1) if v.get("avg") else None
    name = v["name"]
    for cut in (" Shs", " SHS", " Inc.", " Inc", " Corp.", " Corporation", " Limited", " Ltd.", " Ltd", " Company", " N.V", ", ", " SA", " plc"):
        if cut in name: name = name.split(cut)[0]
    name = name.rstrip(", ")
    if cdr and "CDR" not in name: name += " CDR"
    name = NAME.get(sym, name.strip())
    return [i, sym, name, f"{v['price']:.2f}", f"{v['chg']:+.2f}%", fmtcap(v.get("cap"), cdr), SEC.get(sym, v.get("tvsector") or "?"), vr]

DROP = set()
g = [v for v in M["g"] if v["sym"] not in DROP][:30]
l = [v for v in M["l"] if v["sym"] not in DROP][:30]
G = [row(i, v) for i, v in enumerate(g, 1)]
L = [row(i, v) for i, v in enumerate(l, 1)]
for r in G + L:
    if r[6] == "?": print("NO SECTOR", r)

D = {
 "date": "2026-11-27", "weekday": "周五",
 "snapshot": "2026-11-27 16:00 ET 收盘（本期为补跑，排程未于 10:00 ET 执行，数据为全日收盘值）",
 "market_state": "CLOSED",
 "vr_note": "量比 = 当日成交量 ÷ 3个月日均量（收盘后补跑，开盘时长占比取 1.0）。⚠️≥3，🔥≥8。",
 "gainers": G, "losers": L,
 "table_notes": [
  "带 * 的 CDR 行市值为美股母公司总市值的加元换算（TradingView 口径），非加拿大挂牌份额；CDR 现价/涨跌/成交量取 .TO 主挂牌（Yahoo v7 quote）。美股今日感恩节次日半日市（13:00 ET 收盘），CDR 下午在多伦多继续交易、无美股参考价。",
  "Yahoo 80+80 行中剔除僵尸行：BIPC.TO（时间戳 11/20，Brookfield Infrastructure 重组旧代码停牌，+10.6% 为旧数据）。其余时间戳均为 11/27 收盘。BTQ.NE / DGX.NE / VRNO.NE 为 Cboe 主挂牌（BTQ、Digi Power X 为纳斯达克主上市、加拿大仅 Cboe 线），已用 Yahoo v7 + TV symbol lookup 核对为当日真实成交。",
  "TradingView 交叉验证：涨幅榜 30 只中 28 只在 TV 加股涨幅榜前 60 行出现且涨跌幅一致（误差 <0.1pt）；BTQ.NE（TV 无加拿大线数据，以 Cboe 当日 17.8 万股成交 + 纳斯达克母股 +22% 为旁证保留）、MDP.TO（TV 60 行外，lookup 核对一致）。跌幅榜 30 只全部与 TV 一致；TJX CDR Yahoo -1.22% vs TV -0.79%（Cboe/TSX 收盘价差），按 .TO 主挂牌保留。",
 ],
 "sectors_html": (
  "<ul>"
  "<li><strong>大盘：</strong>TSX 收 34,839.87（+1.20%，+412.99 点），本周累涨 1,650 点（+4.97%），创 2026 年以来最强单周之一；TSXV +2.3% 至 737.25。12 个子板块 11 个上涨：黄金 +5.4%、材料 +4.6%、信息科技 +2.5%，仅消费必需品 -1.0%。驱动：美元回落 + 周三 15 个月低点后的空头回补——黄金期货 +3.2% 至 $3,650、白银 +7.8% 至 $43.7（金银比从 86.7 压至 83）、铜 +3.3% 至 $5.60/lb；美股黑五半日市普涨（标普 +1.6%、纳指 +2.3%、费半 +4.7%），内存/光通信板块领涨。加元 70.19 美分持平；WTI -0.7% 至 $83。TSX 涨跌家数 718:235。</li>"
  "<li><strong>涨幅榜主线一：贵金属全线暴涨（30 席中 20 席为金银股）。</strong>白银 +7.8% 带动银矿领跑：Americas Gold & Silver +9.8%（连续第二日，量比 1.0）、Aya +9.5%（124 万股，量比 1.3）、AbraSilver +9.3%、Endeavour Silver +9.0%、Santacruz +8.1%、Silvercorp +7.4%、Discovery +7.9%；黄金股：Seabridge +10.3%（TSX 综指第一，KSM 铜金项目对金铜双敏感）、Serabi +10.0%、Skeena +9.5%（Eskay Creek 建设中、高 beta）、Jaguar +8.5%、Heliostar +8.2%、G Mining +7.8%、China Gold +7.8%、Eldorado +7.7%、B2Gold +7.6%、Perpetua +7.6%、Montage +7.5%。整体量比 0.5–1.4，属价格驱动的板块性反弹，无单只异常放量——市场在周三金价 15 个月低点后集体回补。</li>"
  "<li><strong>涨幅榜主线二：铜/铜金开发商随铜价 +3.3%。</strong>Northisle Copper & Gold +15.2%（北温哥华岛 North Island 铜金项目，11/3 启动环评、11/25 Vancouver Sun 报道 Wheaton 参与其 $1.15 亿融资并称「优质铜资源+黄金 kicker」，PFS 定于 2027Q1；82.7 万股、量比 1.3）；Amerigo +7.1%（铜尾矿）。反面是 Ero Copper -3.0%（见跌幅榜）。</li>"
  "<li><strong>涨幅榜主线三：美股科技反弹经 CDR 传导 + 加拿大科技/生物个股。</strong>SanDisk CDR +11.5%（美股 SNDK +16%，Kioxia-Nvidia 合作提振 NAND 情绪，自 6 月高点跌 75% 后超跌反弹；CDR 201 万股、量比 1.5）、Coherent CDR +11.0%（美股 +14%，光通信板块随 Marvell/Lumentum 反弹）、Anthropic CDR +8.5%（美股 ANT +11% 至 $91.88 重回 $83 发行价上方，上市首周最佳单日；CDR 53 万股）。本土：BTQ Technologies +25.8% 居首（Cboe 线、后量子安全，纳斯达克母股 +22%、210 万股——11/17 Q3 更新后连跌至 $1.00 附近，今日随 IonQ/Rigetti 等量子股反弹 + 低价股超跌回补；Cboe 17.8 万股、量比 1.4）、Digi Power X +17.5%（Cboe 线仅 1.5 万股薄量，纳斯达克母股 DGXX 仅 +3.7%——加拿大线为补涨/错价，参考价值低）、Abaxx +8.8%（连续第二日，11/26 +8.6%）、Medexus +8.4%（11/11 Q2 创纪录季报、GRAFAPEX 放量，11/26 刷 52 周新高 $6.30 后今日续创 $6.89 新高；14.3 万股、量比 3.3 ⚠️）、Profound Medical +7.7%（量比 2.0）、Verano +9.2%、Green Thumb +7.0%（美国 MSO 板块）、Algoma Steel +7.8%（昨日 -1.6% 后反弹）。</li>"
  "<li><strong>跌幅榜主线：普涨日跌幅榜极浅（第 30 名 -1.15%），由个股利空和防御板块回吐组成。</strong>个股利空：Rogers Sugar -4.8%（11/26 Q4 EPS $0.11 不及预期 $0.13、LEAP 项目 $480 万减值，11/27 Desjardins 下调至 Hold、Scotia 目标价降至 $6.25「行业跑输」；75.4 万股、量比 3.8 ⚠️）；Ero Copper -3.0%（11/26 盘后公告巴西 Tucumã 矿因暴雨溢流、州环保局 SEMAS 要求全面停产停工，罚款 $290 万、无复产时间表——Tucumã 占 2026 产量指引 48%、NAV 21%；117 万股、量比 2.3，铜价 +3.3% 的逆势大跌）；Tidewater Midstream -4.2% / Tidewater Renewables -4.1%（合并案 12/14 投票前双双回落，LCFS 量比 1.4）；Allied Properties REIT -3.6%（TSX 综指跌幅第一，97 万股）；Zedcor -5.1%（11/4 Q3 创纪录后持续回落，净债务 $6,700 万引担忧）；WELLSTAR -5.4%（10/1 新上市，11/26 公告 CFO 更换 12/1 生效；4.8 万股、量比 1.1）；Leon's Furniture -2.7%（量比 2.1，近月 +69% 后回吐）；High Tide -3.6%、Martinrea -3.1%、Ag Growth -3.1%、Kolibri -2.5%。防御/消费必需品回吐（唯一下跌子板块）：Couche-Tard -1.7%（202 万股、量比 1.4）、Empire -1.6%、Loblaw -1.2%、Metro -1.0%、North West -1.1%；Air Canada -1.6%、Birchcliff -1.3%（天然气）、Topicus -1.3%。昨日涨幅榜回吐：Aclara -1.7%、Colonial Coal -1.7%、Erdene -1.7%（量比 2.2）。CDR：Boeing -2.2%、Cerebras -1.9%、Goldman -1.2%、TJX -1.2%（美股 TJX -1.6%）、Constellation Energy -1.0%。</li>"
  "</ul>"),
 "anomalies_html": (
  "<ul>"
  "<li>⚠️ <strong>RSI.TO 量比 3.8</strong>（-4.8%，75.4 万股 vs 日均 20 万；TMX 综合成交 146 万股）：Rogers Sugar 11/26 Q4 EPS 不及预期 + LEAP 减值，11/27 Desjardins 下调评级、Scotia 降目标价至 $6.25 并称 F27 面临竞争加剧/贸易风险，机构换手放大。跌破 50 日/200 日均线（$6.66/$6.72），为本日跌幅榜唯一真正的基本面驱动放量。</li>"
  "<li>⚠️ <strong>MDP.TO 量比 3.3</strong>（+8.4%，14.3 万股 vs 日均 4.3 万）：Medexus 连续第二日创 52 周新高（$6.89），11/11 Q2 季报后 GRAFAPEX 放量叙事获认可，小盘药股被动跟随动量资金；市值仅 $2.1 亿，流动性薄。</li>"
  "<li><strong>ERO.TO 量比 2.3</strong>（-3.0%，117 万股 vs 日均 52 万）：Ero Copper Tucumã 全面停产，铜价 +3.3% 的日子逆势放量下跌，接近 ⚠️ 门槛。Jefferies 称若快速提交整改方案「两周内可能复产」，TD 估一周停产影响 Q4 EBITDA ~3%——下周复产进展是关键。</li>"
  "<li><strong>GSKR.V 量比 2.2 / CTGO.TO 量比 2.6 / ERD.TO 量比 2.2 / LNF.TO 量比 2.1 / PRN.TO 量比 2.0</strong>：Goldsky（+8.0%）、Contango（+7.3%，仅 4 万股）、Erdene（-1.7%）、Leon's（-2.7%）、Profound（+7.7%）均为薄量小盘股的 2 倍放量，无 ⚠️ 级异常。</li>"
  "<li><strong>BTQ.NE +25.8%、DGX.NE +17.5%：</strong>两只纳斯达克主上市股的 Cboe 加拿大线。BTQ 加拿大线 17.8 万股与母股 +22% 方向一致（量比 1.4）；Digi Power X 加拿大线仅 1.5 万股、母股仅 +3.7%，+17.5% 为薄量错价，勿作为信号。</li>"
  "<li>涨幅榜 20 只金银股量比全部在 0.5–1.4：今日是金价 +3%/银价 +8% 驱动的板块性 beta 反弹，而非资金选择性涌入某只个股。贵金属自周三 15 个月低点两日反弹（金 +3.5%、银 +8%），下周能否守住 $3,600/$43 决定这波是否只是空头回补。</li>"
  "</ul>"),
 "digest": "收盘补跑：TSX +1.20% 收 34,840，周涨 4.97%；美元回落 + 空头回补推金 +3.2%、银 +7.8%、铜 +3.3%，黄金板块 +5.4%、材料 +4.6%，涨幅榜 30 席中 20 席为金银股（Seabridge +10.3%、Serabi +10.0%、Americas Gold & Silver +9.8%、Skeena +9.5%、Aya +9.5%、AbraSilver +9.3%、Endeavour Silver +9.0%）+ 铜金开发 Northisle +15.2%；美股黑五半日市内存/光通信反弹经 CDR 传导：SanDisk CDR +11.5%、Coherent CDR +11.0%、Anthropic CDR +8.5%（母股重回发行价上方）；榜首 BTQ +25.8%（量子股反弹）。跌幅榜浅（第 30 名 -1.15%）：Rogers Sugar -4.8%（季报不及预期+两家下调，量比 3.8⚠️）、Ero Copper -3.0%（Tucumã 矿被勒令停产，逆势放量）、Tidewater 双股 -4%、消费必需品为唯一下跌板块（Couche-Tard -1.7%、Empire -1.6%、Loblaw -1.2%）。Medexus +8.4% 量比 3.3⚠️ 连创新高。",
}
json.dump(D, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, len(G), len(L))
for r in G + L: print(r)
