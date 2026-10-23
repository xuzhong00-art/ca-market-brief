# -*- coding: utf-8 -*-
"""Build data/2026-10-22.json from _proc.json + CDR additions + meta (post-close backfill, FRAC=1.0)."""
import json

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
proc = json.load(open(D + "_proc.json", encoding="utf-8"))
tv = json.load(open(D + "_tv_raw.json", encoding="utf-8"))
FRAC = 1.0

# TV parent market cap for DR rows (CAD)
COLS = ["name","description","close","change","market_cap_basic","sector","volume","avg90","type","exchange","update_mode","time"]
tvcap = {}
for blob in tv.values():
    if not blob: continue
    for it in blob["data"]:
        d = dict(zip(COLS, it["d"])); sym = it["s"].split(":")[1]
        if d["type"] == "dr" and d["market_cap_basic"]: tvcap[sym] = d["market_cap_basic"]

# .NE rows -> .TO fuller data (Yahoo v7 quote, post-close): sym, price, chg, cap, vol, avg3m
TO_OVERRIDE = {
 "LULU.NE": ("LULU.TO", 4.48, 7.43, None, 720488, 508358),
 "PEP.NE":  ("PEP.TO", 20.50, 3.07, None, 281262, 33541),
 "NFLX.NE": ("NFLX.TO", 25.06, 3.00, None, 272656, 226301),
 "GEV.NE":  ("GEV.TO", 55.39, -10.63, None, 152637, 42296),
}
# TV-only additions (Yahoo v7 quote .TO): sym, name, price, chg, cap(None->TV), vol, avg3m
TV_ADD = {
 "gainers": [
  ("BX.TO", "Blackstone（CDR）", 14.77, 8.21, None, 94136, 27441),
  ("LMT.TO", "Lockheed Martin（CDR）", 33.27, 6.87, None, 79270, 21530),
  ("ADBE.TO", "Adobe（CDR）", 10.29, 5.97, None, 264381, 108824),
  ("INTU.TO", "Intuit（CDR）", 21.47, 5.71, None, 139025, 57453),
  ("PG.TO", "Procter & Gamble（CDR）", 27.25, 5.70, None, 34322, 14055),
  ("FISV.TO", "Fiserv（CDR）", 5.10, 4.94, None, 90590, 20012),
  ("HD.TO", "Home Depot（CDR）", 20.17, 4.29, None, 73403, 34228),
  ("JNJ.TO", "Johnson & Johnson（CDR）", 34.11, 3.80, None, 39540, 16261),
  ("ISRG.TO", "Intuitive Surgical（CDR）", 22.96, 3.56, None, 41192, 20146),
 ],
 "losers": [
  ("LRCX.TO", "Lam Research（CDR）", 20.16, -11.89, None, 151616, 61938),
  ("CRWV.TO", "CoreWeave（CDR）", 10.45, -10.07, None, 733027, 256922),
  ("KLAC.TO", "KLA（CDR）", 19.96, -9.56, None, 63022, 28331),
  ("SPCX.TO", "SpaceX（CDR）", 24.11, -8.85, None, 2541482, 1730901),
 ],
}
EXCLUDE = set()

META = {
 # gainers
 "MTL.TO":("Mullen Group","物流运输"),"WCN.TO":("Waste Connections","固废处理"),
 "BX.TO":("Blackstone（CDR）","另类资管·CDR"),"LULU.TO":("Lululemon（CDR）","运动服饰·CDR"),
 "FSV.TO":("FirstService","物业服务"),"LMT.TO":("Lockheed Martin（CDR）","国防·CDR"),
 "TRI.TO":("Thomson Reuters","法律/税务信息服务"),"ADBE.TO":("Adobe（CDR）","软件·CDR"),
 "TOI.V":("Topicus.com","垂直软件(欧洲)"),"INTU.TO":("Intuit（CDR）","财税软件·CDR"),
 "PG.TO":("Procter & Gamble（CDR）","日用消费品·CDR"),"AP-UN.TO":("Allied Properties REIT","办公REIT"),
 "CSU.TO":("Constellation Software","垂直软件"),"T.TO":("TELUS","电信"),
 "FISV.TO":("Fiserv（CDR）","支付科技·CDR"),"WSP.TO":("WSP Global","工程咨询"),
 "DOO.TO":("BRP","动力运动车"),"HD.TO":("Home Depot（CDR）","家居零售·CDR"),
 "OTEX.TO":("Open Text","企业软件"),"RCI-B.TO":("Rogers Communications","电信"),
 "AIF.TO":("Altus Group","房地产数据/软件"),"EMA.TO":("Emera","公用事业"),
 "REAL.TO":("Real Matters","房贷评估/产权服务"),"JNJ.TO":("Johnson & Johnson（CDR）","医药·CDR"),
 "BYD.TO":("Boyd Group","汽车碰撞维修"),"CPKR.TO":("Canada Packers","肉类加工"),
 "BCE.TO":("BCE","电信"),"STN.TO":("Stantec","工程咨询"),"WFG.TO":("West Fraser Timber","木材"),
 "DRX.TO":("ADF Group","钢结构"),"BBUC.TO":("Brookfield Business","工业投资控股"),
 "ISRG.TO":("Intuitive Surgical（CDR）","手术机器人·CDR"),"PEP.TO":("PepsiCo（CDR）","饮料食品·CDR"),
 "CIGI.TO":("Colliers","商业地产服务"),"L.TO":("Loblaw","食品零售"),"EMP-A.TO":("Empire","食品零售"),
 "BAM.TO":("Brookfield Asset Mgmt","资产管理"),"QBR-B.TO":("Quebecor","电信/媒体"),"CCA.TO":("Cogeco","有线/电信"),
 "NFLX.TO":("Netflix（CDR）","流媒体·CDR"),
 # losers
 "COHR.TO":("Coherent（CDR）","光通信·CDR"),"SCZ.TO":("Santacruz Silver","银锌矿(玻利维亚/墨西哥)"),
 "HG.CN":("HydroGraph Clean Power","石墨烯材料"),"CLS.TO":("Celestica","电子制造/AI服务器"),
 "LRCX.TO":("Lam Research（CDR）","半导体设备·CDR"),"CADY.TO":("Cadillac Mines","黄金勘探(魁北克)"),
 "HMMC.TO":("Hemlo Mining","黄金生产(安大略)"),"USA.TO":("Americas Gold & Silver","银矿(爱达荷)"),
 "HUT.TO":("Hut 8","加密挖矿/算力"),"GEV.TO":("GE Vernova（CDR）","电力设备·CDR"),
 "RIO.TO":("Rio2","黄金开发(智利)"),"NUAG.TO":("New Pacific Metals","银矿开发(玻利维亚)"),
 "SGML.V":("Sigma Lithium","锂矿(巴西)"),"AYA.TO":("Aya Gold & Silver","银矿生产(摩洛哥)"),
 "MAU.TO":("Montage Gold","黄金开发(科特迪瓦)"),"ZVST.NE":("Vistra（CDR）","电力·CDR"),
 "CRWV.TO":("CoreWeave（CDR）","AI云算力·CDR"),"MAI.TO":("Mining Americas","矿业勘探"),
 "JAG.TO":("Jaguar Mining","黄金生产(巴西)"),"SKE.TO":("Skeena Resources","金银开发(BC)"),
 "FDR.V":("Founders Metals","黄金勘探(苏里南)"),"BE.TO":("Bloom Energy（CDR）","燃料电池·CDR"),
 "KLAC.TO":("KLA（CDR）","半导体设备·CDR"),"GSKR.V":("Goldsky Resources","黄金勘探"),
 "APM.TO":("Andean Precious Metals","银金生产(玻利维亚/美国)"),"HHH.V":("Helius Minerals","矿业勘探"),
 "HSTR.TO":("Heliostar Metals","黄金生产(墨西哥)"),"BTQ.NE":("BTQ Technologies","量子安全/区块链"),
 "SLG.V":("San Lorenzo Gold","铜金勘探(智利)"),"BB.TO":("BlackBerry","车载软件/网安"),
 "HBM.TO":("Hudbay Minerals","铜矿生产"),"NEO.TO":("Neo Performance","稀土磁材"),
 "CNL.TO":("Collective Mining","黄金勘探(哥伦比亚)"),"ORE.TO":("Orezone Gold","黄金生产(布基纳法索)"),
 "SPCX.TO":("SpaceX（CDR）","航天/AI·CDR"),
}

def cap_s(c):
    if not c: return "–"
    return f"{c/1e9:.1f}B" if c >= 1e9 else f"{c/1e6:.0f}M"

def vr(vol, avg):
    return round(vol/(avg*FRAC), 1) if avg else None

def drcap(sym, fallback):
    return tvcap.get(sym.split(".")[0], fallback)

def build(side, desc):
    rows = []
    for r in proc[side]:
        if "drop" in r or r["sym"] in EXCLUDE: continue
        if r["sym"] in TO_OVERRIDE:
            s, p, c, cap, vol, avg = TO_OVERRIDE[r["sym"]]
            r = dict(r, sym=s, price=p, chg=c, cap=cap or drcap(s, r["cap"]), vol=vol, avg=avg, vr=vr(vol, avg))
        elif r.get("is_dr"):
            r = dict(r, cap=drcap(r["sym"], r["cap"]))
        rows.append(r)
    for s, n, p, c, cap, vol, avg in TV_ADD[side]:
        rows.append({"sym":s,"name":n,"price":p,"chg":c,"cap":cap or drcap(s, None),"vr":vr(vol, avg),"tv_sector":"CDR"})
    rows.sort(key=lambda r: r["chg"], reverse=desc)
    out = []
    for i, r in enumerate(rows[:30], 1):
        name, sec = META.get(r["sym"], (str(r["name"])[:22], r.get("tv_sector") or "–"))
        if r["sym"] not in META: print("NO META:", r["sym"], r["name"])
        out.append([i, r["sym"], name, f"{r['price']:.2f}", f"{r['chg']:+.2f}%", cap_s(r["cap"]), sec, r["vr"]])
    print(side, "31-36:", [(r["sym"], r["chg"], r["vr"]) for r in rows[30:36]])
    return out

G, L = build("gainers", True), build("losers", False)
data = {
 "date":"2026-10-22","weekday":"周四",
 "snapshot":"2026-10-22 16:00 ET 收盘（补跑快照，次日 01:45 PT 执行）",
 "market_state":"CLOSED",
 "vr_note":"量比 = 当日全天成交量 ÷ 3个月日均量（收盘后补跑，系数 1.0）。CDR 行用 Yahoo .TO 挂牌 3 个月均量，基数小易放大。⚠️≥3，🔥≥8。",
 "gainers":G,"losers":L,
 "table_notes":[
  "*CDR（BX/LMT/ADBE/INTU/PG/FISV/HD/JNJ/ISRG/LULU；COHR/LRCX/GEV/CRWV/KLAC/BE/ZVST）市值为 TradingView 美股母公司总市值（加元口径），非加拿大挂牌流通市值。",
  "*LULU/GEV/PEP/NFLX 以 TSX 挂牌数据替代 Yahoo 返回的 NEO 行；BX/LMT/ADBE/INTU/PG/FISV/HD/JNJ/ISRG 及跌幅榜 LRCX/CRWV/KLAC/SPCX 为 TradingView type=dr 补充（Yahoo screener 未返回），行情取 Yahoo .TO 挂牌收盘快照。",
  "*剔除：BIP-UN/AMD.NE/META.NE 交叉挂牌去重。所有入榜行 regularMarketTime 均为 10-22 当日，无停牌僵尸数据；TV 交叉验证涨跌幅全部一致（BTQ.NE TV 无记录，Yahoo 当日成交 33 万股有效，保留）。TV 跌幅榜 DLCG（NEO 行）最后成交 10-13，陈旧数据未采纳。PEP.TO +3.07% 量比 8.4 位列榜外第 34。",
 ],
 "sectors_html":(
  "<ul>"
  "<li><strong>大盘：TSX -0.97% 收 35,973（-352 点），从四周高点回落；创业板 -3.13%</strong>：Meta/Tesla 财报未能化解 AI 资本开支融资疑虑（Meta 自由现金流转负、新设无投票权股融资），叠加沙特 Aramco 油田遇袭推升布伦特至 ~US$112、加息预期回升——纳指 -2.6%、标普 -1.2%（7 月以来最差单日）、英伟达 -4.4%。12 月黄金 -89.6 至 US$4,060（两个半月新低），银 -5.9% 至 US$55.3（年内收盘新低），铜 -2.8%；WTI +2.32 至 US$99.47；加元 71.32 美分。TSX 材料板块 -5.6%（8/4 以来最低）、科技 -1.6%；通讯 +3.9%、地产 +2.8%、工业 +2.3%、必需消费 +2.1%、公用 +1.2% 逆势上涨——典型「卖 AI/矿业、买防御/利率敏感」轮动。</li>"
  "<li><strong>涨幅榜主线一：财报驱动的本土蓝筹</strong>：Mullen Group +11.5% 领跑（Q3 营收 6.53 亿 +16%、净利 5,150 万 +55% 创纪录，内生增长驱动，986 万股为均量 2.9 倍）；Waste Connections +9.5%（Q3 EPS 1.52 超预期 4%、上调全年指引）；FirstService +7.4%（Q3 营收 15.3 亿美元 +6%、调整后 EPS 1.89 +7%，美股成交 3.1 倍）；Thomson Reuters +6.5%（AI 法律/税务产品需求，10/22 美股同涨 6.5%）；Topicus +5.9%、Constellation Software +5.3%、Open Text +4.1%——加拿大软件股与美股 AI 硬件背离，受益「软件受益者 vs 算力卖铲人」切换。</li>"
  "<li><strong>涨幅榜主线二：电信/地产/公用防御股集体走强</strong>：TELUS +5.0%（1,060 万股）、Rogers +4.1%（周五盘前财报）、BCE +3.6%、Quebecor +3.1%、Cogeco +3.1%——通讯板块 +3.9% 为 TSX 当日最强；Allied Properties +5.7%（10/22 盘后 Q3 财报前买入，165 万股）、Altus +4.0%、Colliers +3.3%、Brookfield Asset Mgmt +3.1%；Emera +3.9%、Fortis +3.0%（榜外）；美债 10 年期收益率 -11bp 至 5.02%（两年来最大单日降幅）利好利率敏感板块。工程/工业：WSP +4.9%、Stantec +3.6%、BRP +4.6%、Boyd +3.7%、ADF +3.6%；木材 West Fraser +3.6%；食品零售 Loblaw +3.2%、Empire +3.2%、Canada Packers +3.6%。</li>"
  "<li><strong>涨幅榜主线三：美股财报超预期 CDR</strong>：Blackstone +8.2%（Q3 可分配收益 1.32 美元超预期、季度流入 630 亿、量比 3.4）；Lockheed Martin +6.9%（850 架 F-35 十年期协议 ≥780 亿美元、上调全年指引、积压订单 2,920 亿创纪录，量比 3.7）；Procter & Gamble +5.7%（FQ1 EPS 2.00 vs 1.88 预期）；Fiserv +4.9%（超跌反弹 + VikingCloud 网安合作、11/3 财报前，量比 4.5）；Adobe +6.0%、Intuit +5.7%（软件 vs 硬件切换）；Home Depot +4.3%、J&J +3.8%、Intuitive Surgical +3.6%、Lululemon +7.4%（LULU 10/21 反弹延续）；PepsiCo +3.1%（Taco Bell 续约至 2036，CDR 量比 8.4，榜外第 34）。</li>"
  "<li><strong>跌幅榜主线一：金银铜矿全线重挫（材料板块 -5.6%）</strong>：金 -2.2%/银 -5.9%/铜 -2.8% 同日下跌，TSX 跌幅榜 30 席中 18 席为金银铜矿——Santacruz Silver -13.1%（Q3 白银产量 150 万 oz 环比 -5%，叠加银价暴跌）、Cadillac Mines -11.6%、Hemlo -11.4%、Americas Gold & Silver -11.3%、Rio2 -10.7%、New Pacific -10.6%、Aya -10.5%、Montage -10.5%、Mining Americas -10.0%、Jaguar -9.9%、Skeena -9.7%、Founders -9.7%、Goldsky -9.6%、Andean -9.5%、Helius -9.5%、Heliostar -9.2%、San Lorenzo -9.1%；Sigma Lithium -10.6%；榜外 Hudbay -9.0%（370 万股）、Neo Performance -9.0%、Collective -8.9%、Orezone -8.8%。银矿跌幅系统性大于金矿，与银 -5.9% 的 beta 一致。</li>"
  "<li><strong>跌幅榜主线二：AI 算力/电力链 CDR 与本土 AI 硬件</strong>：Coherent -13.1%（Susquehanna 目标价 425→350、Morningstar 新覆盖称估值过高，光通信板块 Lumentum -9%/AAOI -10%）；Celestica -12.0%（无公司消息，纯 AI 资本开支担忧，10/26 盘后财报）；Lam Research -11.9%（FQ1 创纪录 40% 营业利润率但指引仅符合预期、供应受限）；Hut 8 -10.9%（比特币 -3% 至 US$82K + neocloud 融资担忧）；GE Vernova -10.6%（Meta 资本开支融资疑虑冲击电力设备链，10/28 财报）；Vistra -10.4%、CoreWeave -10.1%、KLA -9.6%、Bloom Energy -9.6%、SpaceX -8.9%（榜外第 34）、BlackBerry -9.1%（美股 BB -8.7%，无公司消息）；HydroGraph -12.9%（昨日 +26.7% 后回吐）。</li>"
  "</ul>"),
 "anomalies_html":(
  "<ul>"
  "<li>🔥 <strong>PEP.TO PepsiCo（CDR）</strong> 量比 8.4（+3.1%，榜外第 34）：PepsiCo 与 Taco Bell 续签 11 年独家饮料协议至 2036（弥补 10/15 失去 KFC 给可口可乐的打击），美股 PEP +3.1%、成交 +15%；CDR 全天 28.1 万份为均量 3.35 万份的 8.4 倍——加拿大投资者在防御股轮动日集中买入消费必需品 CDR。</li>"
  "<li>⚠️ <strong>REAL.TO Real Matters</strong> 量比 5.8（+3.9%）：10/21 National Bank 将目标价 6.50→5.00（维持 sector perform）后股价探至 52 周低点 3.00，10/22 反弹 3.9%、59.6 万股为均量 5.8 倍，无公司公告；美债收益率单日 -11bp 利好房贷评估业务预期，叠加低位空头回补。11/19 发 Q4 财报。</li>"
  "<li>⚠️ <strong>FISV.TO Fiserv（CDR）</strong> 量比 4.5（+4.9%）：美股 FISV +5.4%，无单一催化——10/20 与 VikingCloud 签多年网安合作、激进投资者 Jana 施压成本削减，11/3 财报前超跌反弹（52 周 128.78→43.87 低点）。</li>"
  "<li>⚠️ <strong>LMT.TO Lockheed Martin（CDR）</strong> 量比 3.7（+6.9%）：五角大楼 850 架 F-35 十年期协议（≥780 亿美元）、Q3 营收 207 亿 +11%、上调全年 EPS 指引至 30.35–30.75、积压订单 2,920 亿创纪录，美股盘中最高 +10%。</li>"
  "<li>⚠️ <strong>ZVST.NE Vistra（CDR）</strong> 量比 3.7（-10.4%）：美股 VST -10%+，AI 电力股集体抛售（Quanta -8%、Talen -8.3%、Eaton -7%），Meta 资本开支融资疑虑外溢至独立发电商；NEO 挂牌基数小（均量 1.9 万份）易放大。</li>"
  "<li>⚠️ <strong>GEV.TO GE Vernova（CDR）</strong> 量比 3.6（-10.6%）：美股 GEV -10.9%、成交为均量 2.2 倍，Meta 财报暴露 AI 基础设施融资缺口，JPMorgan/Susquehanna 近期下调目标价，10/28 盘前 Q3 财报前机构去风险；一周累跌 ~20%。</li>"
  "<li>⚠️ <strong>BX.TO Blackstone（CDR）</strong> 量比 3.4（+8.2%）：Q3 可分配收益 1.32 美元 vs 1.26 预期，季度流入 633 亿、过去 12 个月 2,716 亿为四年最高，管理层预计 Q4 变现大幅回升、2027 基础管理费重回双位数增长，美股 +6%。</li>"
  "<li>其余入榜股量比均 &lt;3：MTL.TO 2.9（+11.5%，创纪录 Q3）、CRWV.TO 2.9（-10.1%）、BE.TO 2.7（-9.6%）、ADBE.TO 2.4（+6.0%）、INTU.TO 2.4（+5.7%）、PG.TO 2.4（+5.7%，财报超预期）、JNJ.TO 2.4（+3.8%）、LRCX.TO 2.4（-11.9%，财报）、HMMC.TO 2.2（-11.4%）、KLAC.TO 2.2（-9.6%）、SCZ.TO 2.1（-13.1%）、HD.TO 2.1（+4.3%）、BYD.TO 2.1（+3.7%）。矿业跌幅虽大但多数量比 1–2，属板块性抛售而非个股事件。</li>"
  "</ul>"),
 "digest":"TSX -0.97% 收 35,973：金 -2.2%/银 -5.9% 重挫矿业（材料 -5.6%，跌幅榜 18 席为金银铜矿，Santacruz -13.1%），Meta 财报引爆 AI 资本开支融资疑虑——Coherent/Celestica/Lam Research -12%+、Hut 8/GE Vernova/Vistra/CoreWeave -10%+；资金转向防御与财报超预期蓝筹：Mullen +11.5%、Waste Connections +9.5%、Blackstone CDR +8.2%、FirstService +7.4%、Lockheed +6.9%、Thomson Reuters +6.5%，电信板块 +3.9%（TELUS +5.0%）；PepsiCo CDR 量比 8.4。",
}
json.dump(data, open(D + "2026-10-22.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in G: print(r)
print("---")
for r in L: print(r)
