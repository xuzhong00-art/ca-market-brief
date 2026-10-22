# -*- coding: utf-8 -*-
"""Build data/2026-10-21.json from _proc.json + CDR additions + meta (post-close backfill, FRAC=1.0)."""
import json

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
proc = json.load(open(D + "_proc.json", encoding="utf-8"))
FRAC = 1.0

# .NE rows -> .TO fuller data (Yahoo v7 quote, post-close): sym, price, chg, cap, vol, avg3m
TO_OVERRIDE = {
 "SMCI.NE": ("SMCI.TO", 11.43, 9.59, 29.3e9, 1291333, 687522),
 "CRWD.NE": ("CRWD.TO", 14.82, 5.18, 69.1e9, 359581, 190432),
 "IBM.NE":  ("IBM.TO", 36.93, 3.85, 309.8e9, 123833, 74385),
 "NFLX.NE": ("NFLX.TO", 24.33, -5.22, 3536.5e9, 960041, 215351),
 "LULU.NE": ("LULU.TO", 4.17, -3.47, 14.6e9, 309203, 507716),
 "LUME.TO": ("LUME.TO", 18.17, 3.53, 1.65e9, 62105, 36450),
}
# TV-only additions (Yahoo v7 quote): sym, name, price, chg, cap, vol, avg3m
TV_ADD = {
 "gainers": [
  ("HFPC-U.TO", "Helios Fairfax Partners", 2.18, 7.92, 236e6, 15100, 6140),
  ("SPCX.TO", "SpaceX（CDR）", 26.45, 7.61, 2903.8e9, 3836661, 1681545),
  ("MSTR.TO", "Strategy（CDR）", 10.42, 7.64, 88.5e9, 786985, 444043),
  ("BE.TO", "Bloom Energy（CDR）", 18.66, 6.93, 92.3e9, 15359, None),
  ("PLTR.TO", "Palantir（CDR）", 15.18, 4.83, 663.2e9, 323871, 402422),
  ("CEGS.TO", "Constellation Energy（CDR）", 18.40, 4.72, 130.8e9, 48496, 52072),
  ("VRT.TO", "Vertiv（CDR）", 15.77, 4.58, 110.3e9, 100724, 103764),
  ("GEV.TO", "GE Vernova（CDR）", 61.98, 4.20, 329.9e9, 60658, 41398),
  ("LVMH.TO", "LVMH（CDR）", 16.41, 4.39, 301.1e9, 18151, 17111),
  ("WDC.TO", "Western Digital（CDR）", 22.98, 3.93, 191.9e9, 153904, 124612),
  ("HOOD.TO", "Robinhood（CDR）", 16.60, 3.75, 124.8e9, 138667, 170506),
 ],
 "losers": [
  ("CMGS.TO", "Chipotle（CDR）", 10.84, -5.00, 48.6e9, 18561, 10070),
  ("BKNG.TO", "Booking（CDR）", 25.61, -3.43, 168.7e9, 78821, 27217),
 ],
}
EXCLUDE = set()

META = {
 "HG.CN":("HydroGraph Clean Power","石墨烯材料"),"ABRA.TO":("AbraSilver Resource","银金开发(阿根廷)"),
 "SMCI.TO":("Super Micro（CDR）","AI服务器·CDR"),"ASTL.TO":("Algoma Steel","钢铁"),
 "VRNO.NE":("Verano Holdings","大麻(美国)"),"ZDC.V":("Zedcor","移动安防监控"),
 "UCU.V":("Ucore Rare Metals","稀土分离"),"BB.TO":("BlackBerry","车载软件/网安"),
 "GTII.CN":("Green Thumb Industries","大麻(美国)"),"MTL.TO":("Mullen Group","物流运输"),
 "CRWD.TO":("CrowdStrike（CDR）","网络安全·CDR"),"SLG.V":("San Lorenzo Gold","铜金勘探(智利)"),
 "PNG.V":("Kraken Robotics","海洋机器人/国防"),"FTG.TO":("Firan Technology","航空电子"),
 "ZVST.NE":("Vistra（CDR）","电力·CDR"),"HPS-A.TO":("Hammond Power","变压器"),
 "CVVY.TO":("Cavvy Energy","油气"),"MDA.TO":("MDA Space","航天卫星"),
 "GRID.TO":("Tantalus Systems","智能电网"),"GORO.V":("Goldgroup Mining","黄金生产(墨西哥)"),
 "WGX.TO":("Westgold Resources","黄金生产(西澳)"),"IFP.TO":("Interfor","木材"),
 "ETG.TO":("Entrée Resources","铜金权益(蒙古)"),"IBM.TO":("IBM（CDR）","IT服务·CDR"),
 "NGEX.TO":("NGEx Minerals","铜金勘探(阿根廷)"),"AMD.TO":("AMD（CDR）","半导体·CDR"),
 "HUT.TO":("Hut 8","加密挖矿/算力"),"KRY.V":("Koryx Copper","铜矿勘探(纳米比亚)"),
 "IFOS.V":("Itafos","磷肥"),"LUME.TO":("Lumentum（CDR）","光通信·CDR"),
 "SJ.TO":("Stella-Jones","木材制品"),"TSLA.TO":("Tesla（CDR）","电动车·CDR"),
 "VNP.TO":("5N Plus","特种半导体材料"),"TSAT.TO":("Telesat","卫星通信"),
 "WSP.TO":("WSP Global","工程咨询"),"ISO.TO":("IsoEnergy","铀矿"),
 "SDE.TO":("Spartan Delta","油气"),"BEP-UN.TO":("Brookfield Renewable","可再生能源"),
 "MAL.TO":("Magellan Aerospace","航空零部件"),
 "HFPC-U.TO":("Helios Fairfax Partners","非洲投资控股"),"SPCX.TO":("SpaceX（CDR）","航天/AI·CDR"),
 "MSTR.TO":("Strategy（CDR）","比特币金库·CDR"),"BE.TO":("Bloom Energy（CDR）","燃料电池·CDR"),
 "PLTR.TO":("Palantir（CDR）","AI软件·CDR"),"CEGS.TO":("Constellation Energy（CDR）","核电·CDR"),
 "VRT.TO":("Vertiv（CDR）","数据中心电力/散热·CDR"),"GEV.TO":("GE Vernova（CDR）","电力设备·CDR"),
 "LVMH.TO":("LVMH（CDR）","奢侈品·CDR"),"WDC.TO":("Western Digital（CDR）","存储·CDR"),
 "HOOD.TO":("Robinhood（CDR）","零售经纪·CDR"),
 # losers
 "SBI.TO":("Serabi Gold","黄金生产(巴西)"),"TTS.V":("Tintina Mines","矿业勘探"),
 "IVN.TO":("Ivanhoe Mines","铜矿生产(刚果)"),"PDI.TO":("PDI Gold","黄金勘探"),
 "NFLX.TO":("Netflix（CDR）","流媒体·CDR"),"AGMR.TO":("Silver Mountain Resources","银矿(秘鲁)"),
 "OMG.V":("Omai Gold Mines","黄金勘探(圭亚那)"),"CAS.TO":("Cascades","纸业包装"),
 "TLRY.TO":("Tilray Brands","大麻"),"MG.TO":("Magna International","汽车零部件"),
 "LCFS.TO":("Tidewater Renewables","可再生柴油"),"FSZ.TO":("Fiera Capital","资产管理"),
 "OGG.V":("Osisko Gold Group","黄金勘探"),"LULU.TO":("Lululemon（CDR）","运动服饰·CDR"),
 "RFA.TO":("RFA Financial","房贷金融"),"MNO.TO":("Meridian Mining","铜金开发(巴西)"),
 "RHM.NE":("Rheinmetall（CDR）","国防·CDR"),"CGG.TO":("China Gold International","黄金/铜生产(中国)"),
 "CS.TO":("Capstone Copper","铜矿生产"),"GG.V":("Golconda Gold","黄金生产(南非)"),
 "AUXX.V":("Gold X2 Mining","黄金开发"),"LUN.TO":("Lundin Mining","铜矿生产"),
 "LNR.TO":("Linamar","汽车零部件"),"ERO.TO":("Ero Copper","铜矿生产(巴西)"),
 "TECK-B.TO":("Teck Resources","铜/煤"),"ARG.TO":("Amerigo Resources","铜尾矿回收"),
 "GO-U.TO":("GO Residential REIT","公寓REIT(纽约)"),"MLP.V":("Millennial Potash","钾肥勘探"),
 "TI.TO":("Titan Mining","锌/石墨(纽约州)"),"ATD.TO":("Couche-Tard","便利店零售"),
 "AP-UN.TO":("Allied Properties REIT","办公REIT"),"PMET.TO":("PMET Resources","锂矿开发"),
 "GFL.TO":("GFL Environmental","环保服务"),"CAD.V":("Colonial Coal","焦煤勘探"),
 "CMGS.TO":("Chipotle（CDR）","快餐·CDR"),"BKNG.TO":("Booking（CDR）","在线旅游·CDR"),
 "TALA.TO":("Talamore Mining","矿业"),"LSPD.TO":("Lightspeed Commerce","零售POS软件"),
}

def cap_s(c):
    if not c: return "–"
    return f"{c/1e9:.1f}B" if c >= 1e9 else f"{c/1e6:.0f}M"

def vr(vol, avg):
    return round(vol/(avg*FRAC), 1) if avg else None

def build(side, desc):
    rows = []
    for r in proc[side]:
        if "drop" in r or r["sym"] in EXCLUDE: continue
        if r["sym"] in TO_OVERRIDE:
            s, p, c, cap, vol, avg = TO_OVERRIDE[r["sym"]]
            r = dict(r, sym=s, price=p, chg=c, cap=cap, vol=vol, avg=avg, vr=vr(vol, avg))
        rows.append(r)
    for s, n, p, c, cap, vol, avg in TV_ADD[side]:
        rows.append({"sym":s,"name":n,"price":p,"chg":c,"cap":cap,"vr":vr(vol, avg),"tv_sector":"CDR"})
    rows.sort(key=lambda r: r["chg"], reverse=desc)
    out = []
    for i, r in enumerate(rows[:30], 1):
        name, sec = META.get(r["sym"], (str(r["name"])[:22], r.get("tv_sector") or "–"))
        if r["sym"] not in META: print("NO META:", r["sym"], r["name"])
        out.append([i, r["sym"], name, f"{r['price']:.2f}", f"{r['chg']:+.2f}%", cap_s(r["cap"]), sec, r["vr"]])
    return out

G, L = build("gainers", True), build("losers", False)
data = {
 "date":"2026-10-21","weekday":"周三",
 "snapshot":"2026-10-21 16:00 ET 收盘（补跑快照，次日 01:40 PT 执行）",
 "market_state":"CLOSED",
 "vr_note":"量比 = 当日全天成交量 ÷ 3个月日均量（收盘后补跑，系数 1.0）。CDR 行用 Yahoo .TO 挂牌 3 个月均量，基数小易放大。⚠️≥3，🔥≥8。",
 "gainers":G,"losers":L,
 "table_notes":[
  "*CDR（SPCX/MSTR/SMCI/BE/CRWD/PLTR/CEGS/VRT/LVMH/GEV/WDC/IBM/HOOD/AMD/ZVST；NFLX/CMGS/LULU/BKNG/RHM）市值为美股母公司总市值（加元口径），非加拿大挂牌流通市值；BE 市值按 TradingView 母公司口径修正，其 TSX 挂牌为新上市无 3 个月均量，量比留空。",
  "*SMCI/CRWD/IBM/NFLX/LULU 以 TSX 挂牌数据替代 Yahoo 返回的 NEO 行；HFPC-U/SPCX/MSTR/BE/PLTR/CEGS/VRT/GEV/LVMH/WDC/HOOD 及跌幅榜 CMGS/BKNG 为 TradingView type=dr/stock 补充（Yahoo screener 未返回），行情取 Yahoo .TO 挂牌收盘快照。",
  "*剔除：AMD.NE/TSLA.NE/NVDA.NE/GOOG.NE/BEPC.TO 交叉挂牌去重。所有入榜行 regularMarketTime 均为 10-21 当日，无停牌僵尸数据；TV 交叉验证涨跌幅全部一致（OMG.V TV 无记录，Yahoo 当日成交 226 万股有效，保留）。TV 跌幅榜 DLCG/VCM（NEO 行）最后成交为 10-13/10-08，陈旧数据未采纳。",
 ],
 "sectors_html":(
  "<ul>"
  "<li><strong>大盘：TSX +0.60% 收 36,325（+217 点），科技与金融领涨</strong>：SpaceX Q3 营收 146 亿美元（+161%）、净利 44 亿大幅超预期，重燃 AI 交易——纳指 +1.3%、标普 +0.5%、道指 +360 点；比特币反弹至 US$84.8K（10/7 以来新高）。12 月黄金 +7.4 至 US$4,150/oz，银约 US$57.5；WTI -0.67 至 US$97.15。加元 71.14 美分持平。</li>"
  "<li><strong>涨幅榜主线一：AI/航天/加密 CDR 集体爆发</strong>：SpaceX CDR +7.6%（366 万份成交为均量 2.3 倍，JPMorgan 目标价 240→500）、Strategy +7.6%（比特币反弹 + 回购额度提至 30 亿、Clear Street/Cantor 上调目标价）、Super Micro +9.6%（AI 服务器需求回暖，129 万份为均量 1.9 倍）、Bloom Energy +6.9%、CrowdStrike +5.2%、Palantir +4.8%、Constellation Energy +4.7%、Vertiv +4.6%、GE Vernova +4.2%、Western Digital +3.9%、IBM +3.9%（财报前）、Robinhood +3.8%、AMD +3.6%、Lumentum +3.5%、Tesla +3.4%（盘后财报）、Vistra +4.6%——AI 算力/电力链全线反弹。</li>"
  "<li><strong>涨幅榜主线二：本土个股题材</strong>：HydroGraph +26.7% 领跑全榜——Austin 总部取得使用许可（3 台 Hyperion 反应堆、年产 30 吨石墨烯）、多个客户进入商业谈判、新设国防事业部，10/29 特别股东会表决迁册美国；AbraSilver +12.5%（Diablillos 项目 Oculto East 钻获 228 m @ 1.79 g/t 金，为该矿床史上最佳金矿段）；Algoma Steel +9.2%（10/28 财报前钢价反弹、空头回补）；BlackBerry +6.2%（QNX 积压订单创纪录，年内累涨 149%，美股 BB +6.1%）；Zedcor +6.9%、Mullen +5.7%、Kraken Robotics +5.1%、Firan +4.8%、Hammond Power +4.5%、MDA Space +4.3%——国防/航天/电力设备链随 SpaceX 情绪同涨。大麻股 Verano +8.3%、Green Thumb +6.1% 反弹。</li>"
  "<li><strong>涨幅榜主线三：矿业分化，勘探/黄金部分走强</strong>：Ucore 稀土 +6.3%、San Lorenzo +5.1%、Goldgroup +4.0%、Westgold +4.0%、Entrée +3.7%、NGEx +3.7%、Koryx +3.6%；木材 Interfor +3.8%、Stella-Jones +3.4%；能源 Cavvy +4.3%、Spartan Delta +3.3%（榜外）。</li>"
  "<li><strong>跌幅榜主线一：金矿/铜矿个股利空与获利了结</strong>：Serabi Gold -13.4% 领跌（Q3 产量 11,008 oz 同比 -9%，Palito 品位不及预期；伦敦 AIM 同日 -11%～-16%，并因许可延迟下调 2026 产量指引至与 2025 持平约 4.4 万 oz，原指引 5.3 万+）；Ivanhoe Mines -6.2%（连续第二日下跌，10/8 已因全年产量指引低端承压，11/3 财报前继续去风险，768 万股为均量 1.9 倍）；Tintina -7.5%、PDI Gold -5.4%、Silver Mountain -4.9%、Omai -4.3%、Osisko Gold Group -3.9%、Meridian -3.4%、China Gold Intl -3.2%、Capstone -3.2%、Golconda/Gold X2 -2.9%、Lundin -2.9%、Ero -2.8%、Teck -2.6%、Amerigo -2.5%、Titan/Millennial -2.4%——铜矿在金价微涨下仍集体回吐（铜价承压 + Ivanhoe 拖累）。</li>"
  "<li><strong>跌幅榜主线二：消费/汽车/CDR 财报反应</strong>：Netflix CDR -5.2%（Q3 EPS 超预期但 Q4 营收指引低于预期、2026 广告收入指引 30 亿→27 亿，美股跌至两年新低，CDR 96 万份为均量 4.5 倍）；Chipotle -5.0%、Booking -3.4%（财报前消费服务类走弱）、Lululemon -3.5%、Rheinmetall -3.2%（欧洲国防回调）。汽车链 Magna -4.1%、Linamar -2.8%（Mobileye/Aptiv 美股走低拖累零部件板块，Magna 10/30 财报）。其他：Cascades -4.3%、Tilray -4.2%、Tidewater Renewables -4.0%、Fiera Capital -4.0%（AUM 流出后持续走弱）、RFA Financial -3.5%、Couche-Tard -2.3%、Allied Properties -2.3%（量比 2.1）、GFL -2.1%。</li>"
  "</ul>"),
 "anomalies_html":(
  "<ul>"
  "<li>⚠️ <strong>NFLX.TO Netflix（CDR）</strong> 量比 4.5（-5.2%）：Q3 EPS 超预期但 Q4 营收指引低于华尔街预期（连续第四季增速放缓）、2026 广告收入指引从 30 亿美元下调至 27 亿，美股跌至两年新低、年内 -25%，CDR 全天 96 万份为均量 21.5 万份的 4.5 倍。</li>"
  "<li>⚠️ <strong>SBI.TO Serabi Gold</strong> 量比 4.4（-13.4%）：Q3 产量 11,008 oz 同比 -9%（Palito 品位不及预期），并因许可延迟将 2026 全年产量指引下调至与 2025 持平（约 4.4 万 oz，原 5.3 万+）；伦敦主挂牌 AIM 成交 152 万股为均量 4.2 倍，多伦多 17.2 万股同步放量。</li>"
  "<li>⚠️ <strong>HG.CN HydroGraph Clean Power</strong> 量比 3.2（+26.7%）：10/21 盘前发布 2026 进展更新——Austin 总部取得使用许可（3 台 Hyperion 反应堆，年产 30 吨）、Bellville 二厂 2027 上半年投产（60 吨）、多个客户从评估转入商业谈判、新设国防事业部，10/29 特别股东会表决迁册特拉华；8 月 7,040 万加元 bought deal（@6.80）后股价回落至 2.7 区间，今日一日拉升 27%，190 万股为均量 3.2 倍。</li>"
  "<li>其余入榜股量比均 &lt;3：BKNG.TO 2.9（-3.4%，财报前）、SPCX.TO 2.3（+7.6%，SpaceX Q3 超预期）、SGML.V 2.4（-1.7%，榜外）、AP-UN.TO 2.1（-2.3%）、ERO.TO 2.1（-2.8%）、ABRA.TO 1.9（+12.5%，钻探利好）、IVN.TO 1.9（-6.2%）、SMCI.TO 1.9（+9.6%）、CRWD.TO 1.9（+5.2%）、MSTR.TO 1.8（+7.6%）、ASTL.TO 1.8（+9.2%）。板块性涨跌为主，个股放量集中在 Netflix/Serabi/HydroGraph 三只有明确公告的标的。</li>"
  "</ul>"),
 "digest":"TSX +0.60% 收 36,325：SpaceX Q3 大超预期重燃 AI 交易，SpaceX/Strategy/Super Micro 等 AI·加密 CDR 领涨，HydroGraph 石墨烯进展 +26.7%、AbraSilver 钻探 +12.5%、Algoma +9.2%、BlackBerry +6.2%；Serabi Gold 下调产量指引 -13.4%、Ivanhoe -6.2% 拖累铜矿，Netflix CDR 财报指引不及预期 -5.2% 量比 4.5，Magna/Linamar 汽车链走弱。",
}
json.dump(data, open(D + "2026-10-21.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in G: print(r)
print("---")
for r in L: print(r)
