# -*- coding: utf-8 -*-
"""Build data/2026-10-27.json from _proc.json + CDR additions + meta (live 07:53 PT snapshot, FRAC=0.21)."""
import json

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
proc = json.load(open(D + "_proc.json", encoding="utf-8"))
tv = json.load(open(D + "_tv_raw.json", encoding="utf-8"))
FRAC = 0.21  # 10:53 ET => ~1h23m of 6.5h session

COLS = ["name","description","close","change","market_cap_basic","sector","volume","avg90","type","exchange","update_mode","time"]
tvcap = {}
for blob in tv.values():
    if not blob: continue
    for it in blob["data"]:
        d = dict(zip(COLS, it["d"])); sym = it["s"].split(":")[1]
        if d["type"] == "dr" and d["market_cap_basic"]: tvcap[sym] = d["market_cap_basic"]

# .NE rows -> .TO fuller data (Yahoo v7 quote): sym, price, chg, cap, vol, avg3m
TO_OVERRIDE = {
 "BA.NE": ("BA.TO", 28.18, -9.18, None, 184922, 46791),
}
# TV-only / misplaced additions (Yahoo v7 quote): sym, name, price, chg, cap(None->TV), vol, avg3m
TV_ADD = {
 "gainers": [
  ("BE.TO", "Bloom Energy（CDR）", 17.38, 9.03, None, 25082, 49280),
  ("WDC.TO", "Western Digital（CDR）", 23.25, 7.44, None, 94843, 131564),
  ("SMCI.TO", "Super Micro（CDR）", 11.18, 6.49, None, 141012, 670148),
 ],
 "losers": [
  ("INTU.TO", "Intuit（CDR）", 20.07, -2.38, None, 27757, 60404),
  ("NOWS.TO", "ServiceNow（CDR）", 19.66, -2.14, None, 32330, 186975),
  ("CRM.TO", "Salesforce（CDR）", 18.39, -2.08, None, 23078, 148666),
 ],
}
EXCLUDE = {"BE.TO"}  # Yahoo screener put BE (+9.03%) in the losers list by error; re-added to gainers above

META = {
 # gainers
 "CLS.TO":("Celestica","电子制造/AI服务器"),"HG.CN":("HydroGraph Clean Power","石墨烯材料"),
 "ABXX.TO":("Abaxx Technologies","大宗商品交易所/清算"),"LAC.TO":("Lithium Americas","锂矿开发(内华达)"),
 "CFW.TO":("Calfrac Well Services","压裂/油服"),"XNDU.TO":("Xanadu Quantum Technologies","量子计算"),
 "BE.TO":("Bloom Energy（CDR）","燃料电池·CDR"),"BZ.V":("Benz Mining","黄金勘探(澳洲)"),
 "BLDP.TO":("Ballard Power Systems","燃料电池"),"LAR.TO":("Lithium Argentina","锂矿生产(阿根廷)"),
 "ISO.TO":("IsoEnergy","铀矿开发"),"TMQ.TO":("Trilogy Metals","铜矿勘探(阿拉斯加)"),
 "WDC.TO":("Western Digital（CDR）","存储硬盘·CDR"),"TSAT.TO":("Telesat","卫星通信"),
 "KEEL.TO":("Keel Infrastructure","数据中心/算力基建"),"PDN.TO":("Paladin Energy","铀矿生产(纳米比亚)"),
 "MAXX.CN":("Max Power Mining","天然氢/矿业勘探"),"EFR.TO":("Energy Fuels","铀/稀土生产(美国)"),
 "PMET.TO":("PMET Resources","锂矿开发(魁北克)"),"HUT.TO":("Hut 8","比特币挖矿/AI算力"),
 "MOON.V":("Blue Moon Metals","铜锌勘探(挪威)"),"PPTA.TO":("Perpetua Resources","金锑开发(爱达荷)"),
 "SMCI.TO":("Super Micro（CDR）","AI服务器·CDR"),"DML.TO":("Denison Mines","铀矿开发"),
 "HIVE.TO":("HIVE Digital Technologies","比特币挖矿/AI算力"),"IE.TO":("Ivanhoe Electric","铜矿开发(亚利桑那)"),
 "UCU.V":("Ucore Rare Metals","稀土分离"),"LGD.TO":("Liberty Gold","黄金勘探(美国)"),
 "FDY.TO":("Faraday Copper","铜矿勘探(亚利桑那)"),"ARG.TO":("Amerigo Resources","铜尾矿处理(智利)"),
 "WGX.TO":("Westgold Resources","黄金生产(澳洲)"),"TLO.TO":("Talon Metals","镍矿勘探(明尼苏达)"),
 "CS.TO":("Capstone Copper","铜矿生产"),"FM.TO":("First Quantum Minerals","铜矿生产"),
 "MDI.TO":("Major Drilling","矿业钻探服务"),"LUNR.TO":("LunR Royalties","贵金属权利金"),
 "SLG.V":("San Lorenzo Gold","黄金勘探(智利)"),"DGX.NE":("Digi Power X","AI数据中心/比特币挖矿"),
 # losers
 "BA.TO":("Boeing（CDR）","航空制造·CDR"),"GRGD.TO":("Groupe Dynamite","女装零售"),
 "IFP.TO":("Interfor","木材"),"TRI.TO":("Thomson Reuters","信息服务/软件"),
 "DPM.TO":("DPM Metals","金铜生产(保加利亚)"),"LSPD.TO":("Lightspeed Commerce","零售POS软件"),
 "FTG.TO":("Firan Technology Group","航空电子/电路板"),"CFP.TO":("Canfor","木材"),
 "CAE.TO":("CAE","飞行模拟/培训"),"FSV.TO":("FirstService","物业服务"),
 "OBE.TO":("Obsidian Energy","油气勘探开发"),"VET.TO":("Vermilion Energy","油气勘探开发"),
 "GORO.V":("Goldgroup Mining","黄金生产(墨西哥)"),"DSG.TO":("Descartes Systems","物流软件"),
 "PXT.TO":("Parex Resources","油气(哥伦比亚)"),"ZDC.V":("Zedcor","移动安防监控塔"),
 "TWM.TO":("Tidewater Midstream","中游/炼化"),"GFR.TO":("Greenfire Resources","油砂"),
 "IMO.TO":("Imperial Oil","综合石油"),"SU.TO":("Suncor Energy","综合石油"),
 "GSY.TO":("goeasy","次级消费贷"),"WSP.TO":("WSP Global","工程咨询"),
 "GIB-A.TO":("CGI","IT服务"),"CVE.TO":("Cenovus Energy","综合石油"),
 "KEL.TO":("Kelt Exploration","油气勘探开发"),"SHOP.TO":("Shopify","电商软件"),
 "CVVY.TO":("Cavvy Energy","油气勘探开发"),"SDE.TO":("Spartan Delta","油气勘探开发"),
 "SBI.TO":("Serabi Gold","黄金生产(巴西)"),"OVV.TO":("Ovintiv","油气勘探开发"),
 "INTU.TO":("Intuit（CDR）","财务软件·CDR"),"NOWS.TO":("ServiceNow（CDR）","企业软件·CDR"),
 "CRM.TO":("Salesforce（CDR）","企业软件·CDR"),"WCN.TO":("Waste Connections","固废处理"),
 "ENGH.TO":("Enghouse Systems","企业软件"),"TOY.TO":("Spin Master","玩具/娱乐"),
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
            r = dict(r, cap=drcap(r["sym"], r["cap"]), vr=vr(r["vol"], r["avg"]))
        else:
            r = dict(r, vr=vr(r["vol"], r["avg"]))
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
 "date":"2026-10-27","weekday":"周二",
 "snapshot":"2026-10-27 10:53 ET 盘中（开盘约 1 小时 23 分钟）",
 "market_state":"REGULAR",
 "vr_note":"量比 = 当日成交量 ÷ (3个月日均量 × 0.21)，0.21 为快照时已开盘时长占比（1h23m / 6.5h）。CDR 行用 Yahoo .TO 挂牌 3 个月均量，基数小易放大。⚠️≥3，🔥≥8。",
 "gainers":G,"losers":L,
 "table_notes":[
  "*CDR（BE/WDC/SMCI；BA/INTU/NOWS/CRM）市值为 TradingView 美股母公司总市值（加元口径），非加拿大挂牌流通市值。",
  "*BA 以 TSX 挂牌数据替代 Yahoo 返回的 NEO 行；WDC/SMCI 及跌幅榜 INTU/NOWS/CRM 为 TradingView type=dr 补充（Yahoo screener 未返回），行情取 Yahoo v7 盘中快照。BE（Bloom Energy CDR，+9.03%）被 Yahoo 误排进跌幅榜，已移回涨幅榜。",
  "*剔除：AMD.NE/TSLA.NE 交叉挂牌去重。所有入榜行 regularMarketTime 均为 10-27 当日盘中，无停牌僵尸数据；TV 交叉验证涨跌幅方向全部一致（盘中逐分钟变动，幅度差 <2 个点；TSAT Yahoo +6.9% vs TV +4.7% 为快照时差）。PPTA/UCU/FTG/FSV/GORO/SBI 未出现在 TV 前 80 行（UCU 现价恰为 $2.00 被 TV close>2 过滤），单票时间戳均为当日。TV 跌幅榜 SCHN（NEO 行，最后成交 10-22）为陈旧数据，未采纳。",
 ],
 "sectors_html":(
  "<ul>"
  "<li><strong>大盘：TSX 开盘 +0.3% 至 36,056，快照时 +0.16% 报 36,001</strong>：矿业领涨、能源回落。金价 -0.6%、白银 -1.5%（美元走强），油价在前日近六个月高点后小幅回升（WTI ~US$102，德黑兰谈判预期 vs 胡塞袭击沙特）。加央行周三议息，LSEG 定价 78% 概率加息 25bp；美联储同日决议。美加据报正就钢铁/汽车关税减免磋商；BC 省保守党胜选承诺扩大 LNG 产量。美股标普 +0.3%、纳指 +0.45% 开盘，本周亚马逊/微软/谷歌财报。</li>"
  "<li><strong>涨幅榜主线一：Celestica 财报 + AI 基建链</strong>：Celestica +10.0% 领涨（C$381.7，成交 22.5 万股）——Q3 营收 US$58.3 亿（+83%）、调整后 EPS US$3.30（+109%）均超指引上限，调整后营业利润率 8.5% 创新高；上调 2026 全年营收至 US$210 亿、EPS US$11.55，首次给出 2027 展望营收 US$400 亿（+90%）、EPS US$21.50，并拟于 Q4 启动新一轮 NCIB。10/22 曾因 AI 资本开支疑虑单日 -12%，今日财报一举收复。AI/算力链同涨：Keel Infrastructure +6.8%（110 万股）、Hut 8 +6.7%、HIVE +6.0%、Super Micro CDR +6.5%、Western Digital CDR +7.4%（量比 3.4）、Bloom Energy CDR +9.0%（被 Yahoo 误排进跌幅榜，已修正）。</li>"
  "<li><strong>涨幅榜主线二：铀 + 锂 + 铜的能源金属反弹</strong>：铀矿集体上涨——IsoEnergy +7.1%、Paladin +7.0%、Energy Fuels +6.9%、Denison +6.2%（100 万股）；锂：Lithium Americas +8.7%、Lithium Argentina +7.1%、PMET +6.6%；铜镍：Trilogy Metals +7.4%、Ivanhoe Electric +6.1%（量比 4.5）、Faraday +4.9%、Amerigo +5.0%、Capstone +5.0%、First Quantum +4.7%（榜外第 31）、Talon +4.7%。金价回落日黄金股整体缺席，仅 Benz +8.3%、Westgold +5.0%（量比 6.3）、Liberty Gold +5.0% 入榜。个股事件：Calfrac +8.7%（量比 11.8🔥，连续第二日创 52 周新高）、Abaxx +9.4%、HydroGraph +9.5% 连续第三日上榜（10/29 特别股东会审议美国重新注册）、Xanadu +9.2%、Ballard +7.5%、Telesat +6.9%（连续三日）。</li>"
  "<li><strong>跌幅榜主线一：Boeing CDR 财报 + 能源股回落</strong>：Boeing CDR -9.2% 领跌（量比 18.8🔥）——Q3 核心 EPS -US$0.34 远差于预期 -0.21，商用飞机部门亏损 US$6.97 亿（预期 -3.6 亿）、利润率 -6.5%，CEO 称 737 月产 47 架目标推迟至明年初；营收 US$242 亿超预期、积压订单创纪录 US$7,450 亿、FCF US$4.6 亿为亮点，美股母公司开盘跌 2–3%，CDR 跌幅含前一日美股收盘后变动及加元对冲。能源股普跌：油气板块 Obsidian -2.6%、Vermilion -2.5%、Greenfire -2.5%、Imperial Oil -2.3%、Suncor -2.1%、Parex -2.1%、Cenovus -1.9%（164 万股）、Kelt -1.9%、Cavvy -1.9%、Spartan Delta -2.0%、Ovintiv -1.7%、Tidewater -2.2%——油价持稳但前日已自六个月高点回落，板块获利了结。</li>"
  "<li><strong>跌幅榜主线二：软件/服务业 + 木材 + 零售</strong>：Thomson Reuters -4.0%（13 万股，Jefferies 10/20 新覆盖目标价 C$182.7 后冲高回落，11/3 Q3 财报前；欧洲同业 HSBC 财报拖累欧股）；软件/IT：Lightspeed -3.1%、Descartes -2.3%、CGI -2.0%、Shopify -1.9%，CDR：Intuit -2.4%、ServiceNow -2.1%、Salesforce -2.1%；FirstService -2.6%、WSP -2.0%、CAE -2.5%（前日出售 Flightscape 业务后回吐）。木材：Interfor -4.3%、Canfor -2.9%。Groupe Dynamite -4.0%（三日反弹后回落）。矿业中 DPM Metals -3.4%（44 万股，10/28 财报前连续两日减仓）、Goldgroup -1.8%、Serabi -1.9%。金融：goeasy -2.0%（量比 3.9，今晨仅公告 Q3 电话会时间，汽车贷款损失阴影未散）。</li>"
  "</ul>"),
 "anomalies_html":(
  "<ul>"
  "<li>🔥 <strong>BA.TO Boeing（CDR）</strong> 量比 18.8（-9.2%）：Q3 财报盘前发布，核心 EPS -US$0.34 vs 预期 -0.21，商用飞机部门亏损 US$6.97 亿、利润率 -6.5%（交付组合不利 + 供应链成本上升），737 月产 47 架目标推迟到 2027 年初；营收 US$242 亿、积压 US$7,450 亿创纪录、FCF US$4.6 亿超预期。美股母公司开盘 -2~3%，CDR 跌幅更大含前日美股盘后变动；18.5 万份为均量 4.7 万份的 18.8 倍（CDR 基数小）。</li>"
  "<li>🔥 <strong>CFW.TO Calfrac Well Services</strong> 量比 12.3（+8.7%）：无新公告；昨日收 C$7.34 创 52 周新高（量比 6.4）后今日再冲 C$7.98，26.5 万股为均量 10.2 万股的 12.3 倍（开盘 1 小时 23 分钟已达 2.6 倍全日均量）。油服板块动能延续 + ATB Cormark 目标价 C$9.00，技术性突破吸引追涨资金；11 月上旬 Q3 财报。</li>"
  "<li>🔥 <strong>DGX.NE Digi Power X</strong> 量比 11.1（+5.1%）：NEO 挂牌流动性极低（3 个月均量仅 9,800 股），2.3 万股即触发 🔥，属薄流通盘放大，主要交易在纳斯达克（DGXX 同步 +4.5%）；无当日公告，10/13 获 US$2 亿债务融资承诺建设阿拉巴马 40 MW AI 数据中心，随 AI 基建链反弹；一个月累计 -49% 后的超跌反弹。</li>"
  "<li>⚠️ <strong>WGX.TO Westgold Resources</strong> 量比 6.6（+5.0%）：无当日公告；10/21 已发 Q1 FY27 季报（产金 98.4 koz、AISC A$2,912/oz 符合指引）。金价 -0.6% 日逆势上涨，16 万股为均量 11.7 万股的 6.3 倍，疑似澳洲盘后 ASX 走强带动 TSX 挂牌补涨。</li>"
  "<li>⚠️ <strong>IE.TO Ivanhoe Electric</strong> 量比 4.7（+6.1%）：无当日公告，铜价走强 + Santa Cruz 铜矿项目题材，3 万股为均量 3.1 万股的 4.7 倍（TSX 挂牌流动性低，主要交易在 NYSE）。</li>"
  "<li>⚠️ <strong>GSY.TO goeasy</strong> 量比 4.1（-2.0%）：今晨仅公告 Q3 财报电话会时间（11 月），6.5 万股为均量 7.6 万股的 4.1 倍；此前汽车贷款损失激增、获贷方让步后股价持续承压，财报前抛压。</li>"
  "<li>⚠️ <strong>ZDC.V Zedcor</strong> 量比 3.9（-2.2%）：昨晚公告 11/4 盘后发 Q3 财报、11/5 电话会，10/13 刚扩信贷额度至 C$1 亿；14 万股为均量 17 万股的 3.9 倍，无负面消息，财报前获利了结。</li>"
  "<li>⚠️ <strong>WDC.TO Western Digital（CDR）</strong> 量比 3.4（+7.4%）：美股母公司存储/AI 数据中心需求题材延续，昨日 +3.6% 后今日加速；9.5 万份为均量 13.2 万份的 3.4 倍。</li>"
  "<li>⚠️ <strong>HG.CN HydroGraph Clean Power</strong> 量比 3.3（+9.5%）：连续第三日领涨（10/23 +11%、10/26 +15.6%），44 万股为均量 64 万股的 3.3 倍；10/29 特别股东会审议美国重新注册，无其他新公告，题材资金接力。</li>"
  "<li>⚠️ <strong>MAXX.CN Max Power Mining</strong> 量比 3.1（+6.7%）：45 万股为均量 3.1 倍，无新公告，天然氢题材延续昨日 +5.5% 的动能。</li>"
  "<li>⚠️ <strong>PMET.TO PMET Resources</strong> 量比 3.0（+6.6%）：19 万股为均量 3.0 倍，无新公告，锂板块联动（LAC +8.7%、LAR +7.1%）。</li>"
  "<li>其余入榜股量比均 &lt;3：LAC.TO 2.9（+8.7%）、PDN.TO 2.6（+7.0%）、BE.TO 2.4（+9.0%）、DPM.TO 2.4（-3.4%）、CLS.TO 2.3（+10.0%，财报日量能温和属机构承接）、INTU.TO 2.2（-2.4%）、LAR.TO 2.0（+7.1%）、TSAT.TO 2.0（+6.9%）。铀/锂/铜板块普涨但量能温和，属商品价格驱动的板块性轮动；能源股回落量比普遍 &lt;1.5，无恐慌性抛售。</li>"
  "</ul>"),
 "digest":"TSX 开盘 +0.3% 至 36,056（快照 +0.16%）：矿业领涨、能源回落，加央行周三议息（78% 概率加息 25bp）。Celestica +10.0% 领涨（Q3 营收 +83%/EPS +109% 超指引上限，2027 展望营收 US$400 亿），AI 基建链 Keel +6.8%/Hut 8 +6.7%/SMCI CDR +6.5% 同涨；铀（IsoEnergy +7.1%、Paladin +7.0%、Energy Fuels +6.9%）、锂（LAC +8.7%）、铜（Trilogy +7.4%）反弹；Calfrac +8.7% 量比 11.8🔥 连续创新高。跌幅榜 Boeing CDR -9.2% 领跌（Q3 核心 EPS -0.34 远差预期、737 增产推迟，量比 18.8🔥），能源股普跌（Imperial -2.3%、Suncor -2.1%、Cenovus -1.9%），Thomson Reuters -4.0%、Interfor -4.3%、Groupe Dynamite -4.0%，软件 CDR（Intuit/ServiceNow/Salesforce）-2% 左右。",
}
json.dump(data, open(D + "2026-10-27.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in G: print(r)
print("---")
for r in L: print(r)
