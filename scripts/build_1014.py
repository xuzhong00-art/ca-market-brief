# -*- coding: utf-8 -*-
"""Build data/2026-10-14.json from _proc.json + TV-only CDR rows + manual meta (post-close catch-up, FRAC=1.0)."""
import json

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
proc = json.load(open(D + "_proc.json", encoding="utf-8"))
FRAC = 1.0

# .NE rows -> replace with fuller .TO data (TV lookup post-close): sym, price, chg, cap, vol, avg90
TO_OVERRIDE = {
 "UNH.NE": ("UNH.TO", 18.06, 4.45, 482.3e9, 177882, 89052),
 "PFE.NE": ("PFE.TO", 12.96, 2.69, 230.0e9, 230832, 123983),
 "ABBV.NE": ("ABBV.TO", 39.41, 3.33, 689.7e9, 40033, 5028),
 "ORAC.NE": ("ORAC.TO", 6.43, -9.05, 615.9e9, 1726185, 678430),
 "SMCI.NE": ("SMCI.TO", 11.52, -8.35, 36.5e9, 621258, 622796),
}
# TV-only additions (absent from Yahoo screener): sym, name, price, chg, cap, vol, avg90
TV_ADD = {
 "gainers": [
  ("LLY.TO", "Eli Lilly（CDR）", 43.22, 3.82, 1562.0e9, 148912, 72522),
  ("LMT.TO", "Lockheed Martin（CDR）", 29.52, 3.54, 165.5e9, 16754, 17184),
  ("WMT.TO", "Walmart（CDR）", 48.35, 3.38, 1267.1e9, 158008, 96788),
  ("INTU.TO", "Intuit（CDR）", 18.81, 3.07, 114.6e9, 175009, 49450),
  ("PG.TO", "Procter & Gamble（CDR）", 25.71, 2.39, 505.6e9, 19106, 10638),
  ("TMUS.TO", "T-Mobile US（CDR）", 19.08, 2.25, 234.6e9, 26840, 6421),
  ("VZ.TO", "Verizon（CDR）", 18.60, 2.14, 257.3e9, 50609, 17114),
  ("BKNG.TO", "Booking Holdings（CDR）", 25.99, 2.00, 168.3e9, 28211, 23178),
  ("ADBE.TO", "Adobe（CDR）", 9.17, 1.89, 130.8e9, 56018, 138203),
  ("JNJ.TO", "Johnson & Johnson（CDR）", 32.31, 1.86, 852.2e9, 29258, 13898),
 ],
 "losers": [
  ("CRWV.TO", "CoreWeave（CDR）", 12.42, -15.34, 61.0e9, 994102, 163825),
  ("MRV.TO", "Marvell（CDR）", 39.62, -8.79, 335.2e9, 185703, 145352),
  ("HOOD.TO", "Robinhood（CDR）", 16.45, -8.66, 141.3e9, 233453, 176654),
 ],
}
EXCLUDE = set()

META = {
 "MLP.V":("Millennial Potash","钾肥开发(加蓬)"),"BMM.V":("Black Mammoth Metals","金银勘探(内华达)"),
 "RFA.TO":("RFA Financial","银行/地产金融"),"UNH.TO":("UnitedHealth（CDR）","医疗保险·CDR"),
 "LIF.TO":("Labrador Iron Ore","铁矿权利金"),"LLY.TO":("Eli Lilly（CDR）","制药·CDR"),
 "FEC.TO":("Frontera Energy","油气(哥伦比亚)"),"LMT.TO":("Lockheed Martin（CDR）","国防·CDR"),
 "WMT.TO":("Walmart（CDR）","零售·CDR"),"ABBV.TO":("AbbVie（CDR）","制药·CDR"),
 "CU.TO":("Canadian Utilities","公用事业"),"INTU.TO":("Intuit（CDR）","软件·CDR"),
 "EMA.TO":("Emera","公用事业"),"ATD.TO":("Couche-Tard","便利店零售"),
 "COST.TO":("Costco（CDR）","零售·CDR"),"L.TO":("Loblaw","食品零售"),
 "PFE.TO":("Pfizer（CDR）","制药·CDR"),"QTRH.TO":("Quarterhill","智能交通"),
 "DOL.TO":("Dollarama","折扣零售"),"PG.TO":("Procter & Gamble（CDR）","日用消费·CDR"),
 "WN.TO":("George Weston","食品零售控股"),"DTOL.TO":("D2L","教育软件"),
 "TMUS.TO":("T-Mobile US（CDR）","电信·CDR"),"ACO-X.TO":("ATCO","公用事业"),
 "WCN.TO":("Waste Connections","环保服务"),"VZ.TO":("Verizon（CDR）","电信·CDR"),
 "SAP.TO":("Saputo","乳制品"),"HLF.TO":("High Liner Foods","冷冻食品"),
 "BKNG.TO":("Booking Holdings（CDR）","在线旅游·CDR"),"ELF.TO":("E-L Financial","保险控股"),
 "ADBE.TO":("Adobe（CDR）","软件·CDR"),"JNJ.TO":("Johnson & Johnson（CDR）","制药·CDR"),
 "FTG.TO":("Firan Technology","航空电子"),"RBY.TO":("Rubellite Energy","油气生产"),
 "QSR.TO":("Restaurant Brands","快餐连锁"),"VET.TO":("Vermilion Energy","油气生产"),
 "MRU.TO":("Metro","食品零售"),"T.TO":("TELUS","电信"),"BTE.TO":("Baytex Energy","油气生产"),
 "FTS.TO":("Fortis","公用事业"),"H.TO":("Hydro One","输电公用"),
 "HG.CN":("HydroGraph Clean Power","石墨烯材料"),"CRWV.TO":("CoreWeave（CDR）","AI云算力·CDR"),
 "PDN.TO":("Paladin Energy","铀矿生产"),"ITH.TO":("Intl Tower Hill","黄金开发(阿拉斯加)"),
 "KEEL.TO":("Keel Infrastructure","AI数据中心基建"),"IE.TO":("Ivanhoe Electric","铜矿开发"),
 "UCU.V":("Ucore Rare Metals","稀土加工"),"AUXX.V":("Gold X2 Mining","黄金勘探"),
 "PDI.TO":("PDI Gold","黄金开发(西非)"),"HUT.TO":("Hut 8","比特币挖矿/算力"),
 "PPTA.TO":("Perpetua Resources","金锑开发(爱达荷)"),"EFR.TO":("Energy Fuels","铀/稀土"),
 "ARA.TO":("Aclara Resources","稀土开发"),"CLS.TO":("Celestica","AI服务器/EMS"),
 "ORAC.TO":("Oracle（CDR）","软件/云·CDR"),"TALA.TO":("Talamore Mining","黄金勘探"),
 "MRV.TO":("Marvell（CDR）","半导体·CDR"),"MAXX.CN":("MaxPower Mining","天然氢/矿业"),
 "HOOD.TO":("Robinhood（CDR）","互联网券商·CDR"),"PALI.V":("Palisades Goldcorp","矿业投资公司"),
 "SMCI.TO":("Super Micro（CDR）","AI服务器·CDR"),"KRY.V":("Koryx Copper","铜矿开发(纳米比亚)"),
 "TMQ.TO":("Trilogy Metals","铜矿开发(阿拉斯加)"),"NCX.V":("NorthIsle Copper & Gold","铜金开发"),
 "FDR.V":("Founders Metals","黄金勘探(苏里南)"),"ITR.V":("Integra Resources","黄金生产"),
 "LMCU.TO":("Lumina Metals","铜矿开发"),"CDE.TO":("Coeur Mining","金银生产"),
 "PNG.V":("Kraken Robotics","海洋机器人/国防"),"CTGO.TO":("Contango Silver & Gold","金银生产"),
 "FWZ.V":("Fireweed Metals","锌/钨开发"),"USA.TO":("Americas Gold & Silver","银矿"),
 "III.TO":("Imperial Metals","铜矿生产"),"SGD.TO":("Snowline Gold","黄金勘探(育空)"),
 "MNO.TO":("Meridian Mining","铜金开发(巴西)"),"BZ.V":("Benz Mining","黄金勘探"),
 "DSV.TO":("Discovery Mining","银矿开发"),
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
 "date":"2026-10-14","weekday":"周三",
 "snapshot":"2026-10-14 16:00 ET 收盘（补跑快照，18:50 PT 执行）",
 "market_state":"CLOSED",
 "note":"本期为收盘后补跑：早盘定时任务未执行，于 18:50 PT 以当日收盘数据补发。量比按全天成交量（系数 1.0）计算。",
 "vr_note":"量比 = 当日全天成交量 ÷ 3个月日均量（收盘后补跑，系数 1.0）。CDR 行用 TradingView 90 日均量。⚠️≥3，🔥≥8。",
 "gainers":G,"losers":L,
 "table_notes":[
  "*CDR（UNH/LLY/LMT/WMT/ABBV/INTU/COST/PFE/PG/TMUS/VZ/BKNG/CRWV/ORAC/MRV/HOOD/SMCI）市值为美股母公司总市值，非加拿大挂牌流通市值。",
  "*UNH/PFE/ABBV/ORAC/SMCI 以 TSX 挂牌数据替代 Yahoo 返回的 NEO 行；LLY/LMT/WMT/INTU/PG/TMUS/VZ/BKNG/CRWV/MRV/HOOD 为 TradingView 补充（Yahoo screener 未返回）。",
  "*剔除：COST.NE/BRK.NE 交叉挂牌去重。所有入榜行 regularMarketTime 均为 10-14 当日，无停牌僵尸数据；TV 交叉验证涨跌幅全部一致。",
  "*BMM.V 未进入 TV 筛选（市值 2.0 亿处于门槛边缘），以 TV 单票查询核实 +11.11% 一致。",
 ],
 "sectors_html":(
  "<ul>"
  "<li><strong>大盘：美国 9 月 CPI 超预期，TSX 从三周高点回落 -1.11%（35,584）</strong>：加息预期升温（10/28 加息概率升至 ~46%），材料板块 -4.3% 为最大拖累，金价连跌第三日至 ~US$4,120/oz，银价同跌。涨幅榜 30 只中仅 2 只涨幅超 10%，整体是「防御板块抗跌」而非普涨。</li>"
  "<li><strong>涨幅榜主线一：防御性板块集体走强</strong>：公用事业 CU +3.2%、EMA +3.1%、ACO-X +2.2%、FTS/H +1.5%；必需消费 ATD +3.0%、L +2.8%、DOL +2.5%、WN +2.3%、SAP +2.1%、MRU +1.7%、QSR +1.8%；美股 CDR 中医药/消费龙头 UNH +4.5%、LLY +3.8%、WMT +3.4%、ABBV +3.3%、COST +2.9%、PFE +2.7%、PG +2.4%、JNJ +1.9%——资金在加息阴影下轮动至低 beta 现金流资产。</li>"
  "<li><strong>涨幅榜主线二：个股催化</strong>：Millennial Potash（MLP）+15.8% 领涨——Banio 钾肥项目（加蓬）DFS 年底完成、目标 2029 投产、美国 DFC 已注资并表态愿参与建设融资，钾肥题材连日活跃；Black Mammoth（BMM）+11.1% 获准纳斯达克挂牌（10/14 公告）；RFA Financial +6.4% 延续资产处置/银行转型行情（年内 +186%）；Labrador Iron Ore（LIF）+4.3% 铁矿石权利金逆势上涨。</li>"
  "<li><strong>跌幅榜主线一：贵金属/铜矿全面重挫</strong>：跌幅榜 30 只中 19 只为矿业——金矿 ITH -11.6%、AUXX -10.9%、PDI -10.8%、PPTA -10.2%、TALA -9.0%、FDR -8.0%、ITR -7.8%、CDE/CTGO -7.7%；铜矿 IE -11.2%、KRY -8.3%、TMQ -8.2%、NCX -8.1%、LMCU -7.8%；稀土/铀 UCU -10.9%、EFR -10.1%、ARA -9.5%。金银连跌三日叠加加息预期，矿业成为抛售重灾区。</li>"
  "<li><strong>跌幅榜主线二：AI 算力/债务担忧蔓延</strong>：CoreWeave CDR（CRWV）-15.3% 创榜首之一——其债券收益率飙至近 15%、Gartner 预测 80% 的 neocloud 将在 2030 年前消失，引发 AI 借贷泡沫担忧；连带 Oracle CDR（ORAC）-9.1%、Celestica（CLS）-9.2%、Keel Infrastructure（KEEL）-11.3%、Hut 8（HUT）-10.4%、Super Micro（SMCI）-8.4%、Marvell（MRV）-8.8%，AI 基建链整体回撤。HydroGraph（HG）-15.5% 石墨烯概念高位回落（8 月 C$6.80 融资价已被腰斩）。</li>"
  "<li><strong>铀矿：Paladin 季报拖累</strong>：PDN -12.7%（量比 5.0）——9 月季度报告显示 Langer Heinrich 产量环比偏弱，公司称「预计 FY2027 下半年产量回升、维持全年指引」，市场对上半年出货不满；同板块 EFR -10.1% 跟跌。</li>"
  "</ul>"),
 "anomalies_html":(
  "<ul>"
  "<li>🔥 <strong>ABBV.TO AbbVie（CDR）</strong> 量比 8.0（+3.3%）：全天成交仅 4.0 万份、90 日均量 5 千份，CDR 基数极小导致倍数放大，医药防御性买盘，参考价值有限。</li>"
  "<li>⚠️ <strong>CRWV.TO CoreWeave（CDR）</strong> 量比 6.1（-15.3%）：母公司美股暴跌 15.5%（成交 1.07 亿股），债券收益率近 15% + Gartner neocloud 淘汰预警，AI 债务担忧集中爆发，CDR 成交 99 万份为均量 6 倍。</li>"
  "<li>⚠️ <strong>BMM.V Black Mammoth Metals</strong> 量比 5.7（+11.1%）：获准纳斯达克 Capital Market 挂牌，美国投资者可及性提升预期推动放量。</li>"
  "<li>⚠️ <strong>PDN.TO Paladin Energy</strong> 量比 5.0（-12.7%）：9 月季度报告出货/产量不及预期（ASX 同步大跌），TSX 挂牌成交 47 万股为均量 5 倍。</li>"
  "<li>⚠️ <strong>PDI.TO PDI Gold</strong> 量比 4.4（-10.8%）：无公司公告，金价三连跌下的西非金矿抛压；绝对成交仅 14.5 万股，薄量放大跌幅。</li>"
  "<li>⚠️ <strong>TMUS.TO T-Mobile（CDR）</strong> 量比 4.2（+2.3%）、<strong>INTU.TO Intuit（CDR）</strong> 量比 3.5（+3.1%）、<strong>VZ.TO Verizon（CDR）</strong> 量比 3.0（+2.1%）：CDR 小基数效应，防御/软件轮动。</li>"
  "<li>⚠️ <strong>EMA.TO Emera</strong> 量比 3.6（+3.1%）：全天 492 万股，公用事业板块资金流入最集中的一只，无公司公告，属防御性配置买盘。</li>"
  "<li>⚠️ <strong>ARA.TO Aclara Resources</strong> 量比 3.3（-9.5%）、<strong>KRY.V Koryx Copper</strong> 量比 3.2（-8.3%）：稀土/铜小盘开发股随板块放量下跌。</li>"
  "<li>⚠️ <strong>MLP.V Millennial Potash</strong> 量比 3.0（+15.8%）：钾肥项目融资/DFS 进展题材，83 万股为均量 3 倍。</li>"
  "</ul>"),
 "digest":"美 CPI 超预期、TSX -1.1%：防御板块（公用/必需消费/医药 CDR）抗跌领涨，Millennial Potash +15.8%；金价三连跌致矿业重挫（18 只矿股上跌幅榜），CoreWeave CDR -15.3% 引爆 AI 债务担忧，Paladin 季报 -12.7%。",
}
json.dump(data, open(D + "2026-10-14.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in G: print(r)
print("---")
for r in L: print(r)
