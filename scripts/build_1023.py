# -*- coding: utf-8 -*-
"""Build data/2026-10-23.json from _proc.json + CDR additions + meta (post-close backfill, FRAC=1.0)."""
import json

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
proc = json.load(open(D + "_proc.json", encoding="utf-8"))
tv = json.load(open(D + "_tv_raw.json", encoding="utf-8"))
FRAC = 1.0

COLS = ["name","description","close","change","market_cap_basic","sector","volume","avg90","type","exchange","update_mode","time"]
tvcap = {}
for blob in tv.values():
    if not blob: continue
    for it in blob["data"]:
        d = dict(zip(COLS, it["d"])); sym = it["s"].split(":")[1]
        if d["type"] == "dr" and d["market_cap_basic"]: tvcap[sym] = d["market_cap_basic"]

# .NE rows -> .TO fuller data (Yahoo v7 quote, post-close): sym, price, chg, cap, vol, avg3m
TO_OVERRIDE = {
 "LULU.NE": ("LULU.TO", 4.27, -4.69, None, 302334, 513454),
 "CRWD.NE": ("CRWD.TO", 15.93, 8.07, None, 170062, 193541),
}
# TV-only additions (Yahoo v7 quote): sym, name, price, chg, cap(None->TV), vol, avg3m
TV_ADD = {
 "gainers": [
  ("PANW.TO", "Palo Alto Networks（CDR）", 44.51, 7.28, None, 48024, 35666),
 ],
 "losers": [
  ("TMUS.TO", "T-Mobile US（CDR）", 17.75, -7.74, None, 22036, 7411),
  ("RDDT.TO", "Reddit（CDR）", 13.73, -4.12, None, 85657, 119606),
  ("AXP.TO", "American Express（CDR）", 26.40, -3.54, None, 38821, 10930),
  ("GSKR.NE", "Goldsky Resources", 2.45, -3.54, 683435862, 35510, 5681),
 ],
}
EXCLUDE = set()

META = {
 # gainers
 "HG.CN":("HydroGraph Clean Power","石墨烯材料"),"CRWD.TO":("CrowdStrike（CDR）","网络安全·CDR"),
 "PANW.TO":("Palo Alto Networks（CDR）","网络安全·CDR"),"BNE.TO":("Bonterra Energy","油气生产(阿省)"),
 "TSAT.TO":("Telesat","卫星通信"),"ARA.TO":("Aclara Resources","稀土开发(智利/巴西)"),
 "KEI.TO":("Kolibri Global Energy","油气生产(俄克拉荷马)"),"SGY.TO":("Surge Energy","油气生产"),
 "TNZ.TO":("Tenaz Energy","油气生产(荷兰/加)"),"OVV.TO":("Ovintiv","油气生产(北美)"),
 "SOIL.TO":("Saturn Oil & Gas","油气生产"),"OBE.TO":("Obsidian Energy","油气生产"),
 "GFR.TO":("Greenfire Resources","油砂生产"),"MX.TO":("Methanex","甲醇化工"),
 "HMMC.TO":("Hemlo Mining","黄金生产(安大略)"),"ACQ.TO":("AutoCanada","汽车经销"),
 "DLCG.TO":("Dominion Lending Centres","房贷经纪"),"BB.TO":("BlackBerry","车载软件/网安"),
 "PD.TO":("Precision Drilling","钻井服务"),"IPO.TO":("InPlay Oil","油气生产"),
 "ACX.TO":("ACT Energy Technologies","钻井技术服务"),"ALV.V":("Alvopetro Energy","天然气(巴西)"),
 "VET.TO":("Vermilion Energy","油气生产(国际)"),"ASTL.TO":("Algoma Steel","钢铁"),
 "PXT.TO":("Parex Resources","油气生产(哥伦比亚)"),"GFL.TO":("GFL Environmental","固废处理"),
 "CKG.V":("Chesapeake Gold","黄金开发(墨西哥)"),"BTE.TO":("Baytex Energy","油气生产"),
 "ATZ.TO":("Aritzia","服饰零售"),"GTE.TO":("Gran Tierra Energy","油气生产(南美)"),
 "HWX.TO":("Headwater Exploration","油气生产"),"SCR.TO":("Strathcona Resources","油气生产"),
 "LMCU.TO":("Lumina Metals","铜矿勘探"),"MDA.TO":("MDA Space","航天/卫星"),"RBY.TO":("Rubellite Energy","油气生产"),
 # losers
 "MTL.TO":("Mullen Group","物流运输"),"BE.TO":("Bloom Energy（CDR）","燃料电池·CDR"),
 "EPRX.TO":("Eupraxia Pharmaceuticals","生物制药"),"SXGC.TO":("Southern Cross Gold","金锑勘探(澳洲)"),
 "TMUS.TO":("T-Mobile US（CDR）","电信·CDR"),"BRVO.V":("Bravo Mining","铂钯镍勘探(巴西)"),
 "CIA.TO":("Champion Iron","铁矿(魁北克)"),"BZ.V":("Benz Mining","黄金勘探(澳洲)"),
 "APM.TO":("Andean Precious Metals","银金生产(玻利维亚/美国)"),"LULU.TO":("Lululemon（CDR）","运动服饰·CDR"),
 "PDI.TO":("PDI Gold","黄金勘探(澳洲)"),"PPTA.TO":("Perpetua Resources","金锑开发(爱达荷)"),
 "AC.TO":("Air Canada","航空"),"DRM.TO":("Dream Unlimited","地产开发"),
 "MAXX.CN":("Max Power Mining","天然氢/矿业勘探"),"TAU.V":("Thesis Gold & Silver","金银勘探(BC)"),
 "HUT.TO":("Hut 8","加密挖矿/算力"),"TLRY.TO":("Tilray Brands","大麻/饮料"),
 "HMM-A.TO":("Hammond Manufacturing","电气外壳制造"),"SLG.V":("San Lorenzo Gold","铜金勘探(智利)"),
 "XTC.TO":("Exco Technologies","汽车零部件/模具"),"IGM.TO":("IGM Financial","财富管理"),
 "ELD.TO":("Eldorado Gold","黄金生产"),"KEEL.TO":("Keel Infrastructure","算力基础设施"),
 "USA.TO":("Americas Gold & Silver","银矿(爱达荷)"),"WGX.TO":("Westgold Resources","黄金生产(澳洲)"),
 "NG.TO":("NovaGold Resources","黄金开发(阿拉斯加)"),"FVI.TO":("Fortuna Mining","金银生产"),
 "PRN.TO":("Profound Medical","医疗设备"),"KRY.V":("Koryx Copper","铜矿勘探(纳米比亚)"),
 "GOOS.TO":("Canada Goose","服饰"),"WN.TO":("George Weston","食品零售控股"),
 "CIGI.TO":("Colliers","商业地产服务"),"III.TO":("Imperial Metals","铜金矿(BC)"),
 "TNGD.V":("Tiernan Gold","黄金勘探"),"RDDT.TO":("Reddit（CDR）","社交媒体·CDR"),
 "AXP.TO":("American Express（CDR）","信用卡/支付·CDR"),"GSKR.NE":("Goldsky Resources","黄金勘探"),
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
 "date":"2026-10-23","weekday":"周五",
 "snapshot":"2026-10-23 16:00 ET 收盘（补跑快照，当日 18:05 PT 执行）",
 "market_state":"CLOSED",
 "vr_note":"量比 = 当日全天成交量 ÷ 3个月日均量（收盘后补跑，系数 1.0）。CDR 行用 Yahoo .TO 挂牌 3 个月均量，基数小易放大。⚠️≥3，🔥≥8。",
 "gainers":G,"losers":L,
 "table_notes":[
  "*CDR（CRWD/PANW；BE/TMUS/LULU/RDDT）市值为 TradingView 美股母公司总市值（加元口径），非加拿大挂牌流通市值。",
  "*CRWD/LULU 以 TSX 挂牌数据替代 Yahoo 返回的 NEO 行；PANW 及跌幅榜 TMUS/RDDT 为 TradingView type=dr 补充（Yahoo screener 未返回；AXP CDR -3.5%/GSKR.NE -3.5% 亦为 TV 补充但位列榜外 32/33），行情取 Yahoo v7 收盘快照。GSKR 3 个月均量取 TV 90 日均量。",
  "*剔除：AMD.NE/U-UN.TO 交叉挂牌去重。所有入榜行 regularMarketTime 均为 10-23 当日，无停牌僵尸数据；TV 交叉验证涨跌幅全部一致。TV 跌幅榜 SCHN（NEO 行）最后成交 10-22、DPRO.CN/GG.V 市值 <2 亿，未采纳。",
 ],
 "sectors_html":(
  "<ul>"
  "<li><strong>大盘：TSX -0.52% 收 35,788（-185 点），10/14 以来最低，全周 -1.1%</strong>：胡塞武装袭击沙特设施推升 WTI +3.8% 至 US$103.27、布伦特盘中破 US$116（5 月以来首次），能源板块 +2.1% 成为 TSX 十大板块中唯一上涨者；金融 -0.9%（宏利 -2.9%）、必需消费 -2.2%（Loblaw -2.8%）、材料 -1.2%（黄金三个月新低）拖累指数。下周加央行议息，多数经济学家预期加息 25bp 至 2.50%——利率敏感的银行/保险/消费股承压。美股纳指小幅收跌，标普科技板块 +0.35% 企稳，网络安全股成为唯一亮点。</li>"
  "<li><strong>涨幅榜主线一：油气股集体走强（榜单 30 席中 17 席为油气/油服，另有甲醇 Methanex）</strong>：Bonterra +5.7%、Kolibri +5.2%、Surge +4.5%、Tenaz +4.5%、Ovintiv +4.4%、Saturn +4.3%、Obsidian +4.1%、Greenfire +4.1%、InPlay +3.6%、Alvopetro +3.4%、Vermilion +3.3%（263 万股，量比 2.5）、Parex +3.3%、Baytex +3.2%（594 万股）、Gran Tierra +3.0%（榜外：Headwater +3.0%、Strathcona +3.0%、Rubellite +2.9%）；油服 Precision Drilling +3.6%、ACT Energy +3.4%（美股 SLB 财报超预期 +7%）；甲醇 Methanex +3.9% 随能源价格走高。中小型加拿大生产商对油价弹性最大，中东供应风险溢价持续抬升。</li>"
  "<li><strong>涨幅榜主线二：网络安全 CDR 与少数个股事件</strong>：CrowdStrike CDR +8.1%、Palo Alto Networks CDR +7.3%——Evercore ISI 渠道调查显示企业安全预算走强，叠加 PHP2Shell 高危漏洞披露与 CrowdStrike/Nvidia 芯片级安全合作，美股 CRWD +8.4%、PANW +6.8%；BlackBerry +3.7% 跟涨网安。HydroGraph +10.1% 领涨（10/22 -12.9% 后反弹，10/29 特别股东会审议美国重新注册，加籍股东换股截止延至 11/15）；Telesat +5.4%（Lightspeed 低轨卫星预期，榜外 MDA Space +2.9% 同涨）；Aclara +5.3%（稀土）；Algoma Steel +3.3%；GFL +3.3%、Aritzia +3.1%、AutoCanada +3.7% 为少数非能源蓝筹。</li>"
  "<li><strong>跌幅榜主线一：财报后获利了结与 AI 电力链</strong>：Mullen Group -10.9% 领跌，前一日因创纪录 Q3 +11.5% 后全数回吐（75 万股，量比 2.1，Scotia 目标价仅 C$30，估值已满）；Bloom Energy CDR -10.8%（Q3 EPS 0.94 vs 0.69 预期、上调指引，但自由现金流 -1.81 亿美元引发恐慌，JPMorgan 目标价 314→292，美股 -11.2%、成交 2.2 倍，量比 6.3）；Hut 8 -4.3%、Keel Infrastructure -3.8% 延续 AI 算力链去风险。Eupraxia -10.1%（无公告，Nasdaq 同跌 9.5%，10/20 以来 +9% 后回落，11/3 财报）。</li>"
  "<li><strong>跌幅榜主线二：金银矿延续抛售 + 美股电信/金融 CDR</strong>：黄金三个月新低，跌幅榜 30 席中 15 席为金银铜矿——Southern Cross Gold -7.9%（ASX 母股 -9.1%，连续两日 -8%）、Bravo -6.3%、Champion Iron -5.3%、Benz -5.3%、Andean -5.0%、PDI Gold -4.9%、Perpetua -4.7%（52 周新低 C$22.99，锑价年内 -22%、Zacks 10/15 降至强卖，量比 3.5）、Thesis -4.3%、San Lorenzo -4.1%、Eldorado -3.9%（117 万股）、Americas Gold & Silver -3.8%、Westgold -3.7%、NovaGold -3.7%、Fortuna -3.7%（榜外 Koryx -3.6%、Imperial -3.5%）。CDR：T-Mobile -7.7%（SpaceX 据报与基站公司谈判 8 万站点进军无线市场，美股 TMUS -7.7%、AT&T -7.3%，量比 3.0）、Lululemon -4.7%（10/22 +7.4% 后回吐）、Reddit -4.1%；榜外 American Express CDR -3.5%（上调全年盈利预期但宣布裁员 5%，美股 -3.7%，量比 3.6）。利率敏感：IGM -4.0%、Dream Unlimited -4.4%（榜外 Colliers -3.5%、George Weston -3.5%、Loblaw -2.8%）；Air Canada -4.7%（油价破 US$100 推升燃油成本，275 万股）。</li>"
  "</ul>"),
 "anomalies_html":(
  "<ul>"
  "<li>⚠️ <strong>BE.TO Bloom Energy（CDR）</strong> 量比 6.3（-10.8%）：Q3 营收 12.4 亿美元 +138%、EPS 0.94 大超 0.69 预期并第三次上调全年指引，但季度自由现金流 -1.81 亿美元、扩产资本开支加重，叠加 Meta 财报引发的 AI 资本开支融资疑虑，美股 -11.2%（3,470 万股为均量 2.2 倍）、距高点 -44%；JPMorgan 目标价 314→292 维持增持。CDR 12.3 万份为均量 1.95 万份的 6.3 倍，连续两日上榜。</li>"
  "<li>⚠️ <strong>GSKR.NE Goldsky Resources</strong> 量比 6.3（-3.5%，榜外第 33）：NEO 挂牌 3.55 万股 vs TV 90 日均量 5,681 股，基数极小易放大；10/22 -9.6% 后延续下跌，无公司公告，随黄金三个月新低的板块性抛售。</li>"
  "<li>⚠️ <strong>AXP.TO American Express（CDR）</strong> 量比 3.6（-3.5%，榜外第 32）：Q3 财报上调全年 EPS 预期但宣布裁员约 5%，市场解读为消费放缓/成本压力，美股 AXP -3.7% 拖累道指；CDR 3.88 万份为均量 1.09 万份的 3.6 倍。</li>"
  "<li>⚠️ <strong>PPTA.TO Perpetua Resources</strong> 量比 3.5（-4.7%）：创 52 周新低 C$22.99（美股 US$16.38），40.3 万股为均量 3.5 倍——锑价年内 -22%、黄金三个月新低双重打击，Zacks 10/15 降至「强卖」，股价已从 US$37 高点腰斩，70% 机构持仓加剧抛压。</li>"
  "<li>⚠️ <strong>TMUS.TO T-Mobile US（CDR）</strong> 量比 3.0（-7.7%）：媒体报道 SpaceX 正与基站运营商谈判接入至少 8 万个站点以进军美国无线市场，AT&T -7.3%、Verizon 同跌，T-Mobile 10/28 财报前承压；CDR 2.2 万份为均量 7,411 份的 3.0 倍（基数小）。</li>"
  "<li>其余入榜股量比均 &lt;3：SXGC.TO 2.5（-7.9%，117 万股）、VET.TO 2.5（+3.3%，263 万股）、ALV.V 2.5（+3.4%）、TNGD.V 2.2（-3.4%）、MTL.TO 2.1（-10.9%，财报后回吐）、GFL.TO 2.1（+3.3%，175 万股）、APM.TO 2.0（-5.0%）、BNE.TO 1.9（+5.7%）、TNZ.TO 1.9（+4.5%）、OVV.TO 1.9（+4.4%）、ACX.TO 1.9（+3.4%）。能源股普涨但量比多在 1–2，属油价驱动的板块性上涨而非个股事件；CRWD.TO +8.1% 量比仅 0.9、PANW.TO +7.3% 量比 1.3。</li>"
  "</ul>"),
 "digest":"TSX -0.52% 收 35,788（周 -1.1%）：胡塞袭沙特推升 WTI +3.8% 至 US$103，能源成唯一上涨板块（+2.1%），涨幅榜 17 席为油气/油服股（Bonterra +5.7%、Ovintiv +4.4%、Baytex +3.2%），网安 CDR CrowdStrike +8.1%/Palo Alto +7.3%；跌幅榜 Mullen -10.9% 回吐财报涨幅、Bloom Energy CDR -10.8%（现金流疑虑，量比 6.3）、T-Mobile CDR -7.7%（SpaceX 入局无线），黄金三个月新低压制矿业 15 席，Perpetua 创 52 周新低。",
}
json.dump(data, open(D + "2026-10-23.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in G: print(r)
print("---")
for r in L: print(r)
