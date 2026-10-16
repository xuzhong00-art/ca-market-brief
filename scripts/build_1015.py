# -*- coding: utf-8 -*-
"""Build data/2026-10-15.json from _proc.json + TV-only CDR rows + manual meta (post-close catch-up, FRAC=1.0)."""
import json

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
proc = json.load(open(D + "_proc.json", encoding="utf-8"))
FRAC = 1.0

# .NE rows -> replace with fuller .TO data (TV lookup post-close): sym, price, chg, cap, vol, avg90
TO_OVERRIDE = {
 "NKE.NE": ("NKE.TO", 6.64, 5.48, 74.7e9, 426353, 226358),
 "NOWS.NE": ("NOWS.TO", 18.86, 6.07, 206.2e9, 207711, 201779),
 "INTC.NE": ("INTC.TO", 53.39, -2.93, 738.8e9, 467521, 332340),
}
# TV-only additions (absent from Yahoo screener): sym, name, price, chg, cap, vol, avg90
TV_ADD = {
 "gainers": [
  ("RDDT.TO", "Reddit（CDR）", 15.17, 6.98, 40.7e9, 85892, 105979),
  ("APPS.TO", "AppLovin（CDR）", 8.73, 6.46, 125.0e9, 183762, 108822),
  ("INTU.TO", "Intuit（CDR）", 19.98, 6.22, 118.2e9, 228424, 51032),
 ],
 "losers": [
  ("ANET.TO", "Arista Networks（CDR）", 33.18, -4.96, 351.1e9, 57274, 33459),
  ("VRT.TO", "Vertiv（CDR）", 15.96, -3.68, 122.2e9, 167201, 81856),
  ("AMAT.TO", "Applied Materials（CDR）", 47.53, -3.63, 504.9e9, 158244, 64701),
  ("CSCO.TO", "Cisco（CDR）", 52.32, -3.31, 638.2e9, 23073, 22390),
  ("LRCX.TO", "Lam Research（CDR）", 24.33, -3.14, 511.5e9, 77720, 65620),
  ("KLAC.TO", "KLA（CDR）", 23.53, -2.61, 332.4e9, 29542, 35630),
  ("SCHW.TO", "Charles Schwab（CDR）", 27.82, -2.49, 238.5e9, 16304, 2535),
  ("SPCX.TO", "SpaceX（CDR）", 24.70, -2.49, 2941.6e9, 2378142, 1541670),
  ("WDC.TO", "Western Digital（CDR）", 21.68, -2.30, 194.1e9, 343031, 120348),
 ],
}
EXCLUDE = set()

META = {
 "BMM.V":("Black Mammoth Metals","金银勘探(内华达)"),"ITH.TO":("Intl Tower Hill","黄金开发(阿拉斯加)"),
 "HMMC.TO":("Hemlo Mining","黄金生产(安省)"),"NFGC.TO":("New Found Gold","黄金勘探(纽芬兰)"),
 "IE.TO":("Ivanhoe Electric","铜矿开发"),"DML.TO":("Denison Mines","铀矿开发"),
 "DRX.TO":("ADF Group","钢结构工程"),"EQX.TO":("Equinox Gold","黄金生产"),
 "BBD-B.TO":("Bombardier","公务机制造"),"LAC.TO":("Lithium Americas","锂矿开发"),
 "MAXX.CN":("MaxPower Mining","天然氢/矿业"),"BHC.TO":("Bausch Health","制药"),
 "K.TO":("Kinross Gold","黄金生产"),"SGD.TO":("Snowline Gold","黄金勘探(育空)"),
 "ARIS.TO":("Aris Mining","黄金生产(哥伦比亚)"),"GAU.TO":("Galiano Gold","黄金生产(加纳)"),
 "ORE.TO":("Orezone Gold","黄金生产(西非)"),"ELE.TO":("Elemental Royalty","贵金属权利金"),
 "PPTA.TO":("Perpetua Resources","金锑开发(爱达荷)"),"VGZ.TO":("Vista Gold","黄金开发(澳洲)"),
 "FIH-U.TO":("Fairfax India","印度投资控股"),"NUAG.TO":("New Pacific Metals","银矿开发(玻利维亚)"),
 "NKE.TO":("Nike（CDR）","运动服饰·CDR"),"LMN.V":("Lumine Group","通信软件并购"),
 "DOO.TO":("BRP","动力运动产品"),"WDO.TO":("Wesdome Gold","黄金生产"),
 "SKE.TO":("Skeena Resources","金银开发(BC)"),"NOWS.TO":("ServiceNow（CDR）","软件·CDR"),
 "AAUC.TO":("Allied Gold","黄金生产(非洲)"),"ENGH.TO":("Enghouse Systems","企业软件"),
 "AEM.TO":("Agnico Eagle","黄金生产"),"CAPT.V":("Capitan Silver","银矿勘探"),
 "HSLV.TO":("Highlander Silver","银矿勘探"),"EDV.TO":("Endeavour Mining","黄金生产(西非)"),
 "RDDT.TO":("Reddit（CDR）","社交媒体·CDR"),"APPS.TO":("AppLovin（CDR）","广告科技·CDR"),
 "INTU.TO":("Intuit（CDR）","软件·CDR"),
 "FSZ.TO":("Fiera Capital","资产管理"),"CIA.TO":("Champion Iron","铁矿生产(魁北克)"),
 "MLP.V":("Millennial Potash","钾肥开发(加蓬)"),"DXT.TO":("Dexterra Group","设施服务"),
 "TTS.V":("Tintina Mines","矽/工业矿物"),"EFX.TO":("Enerflex","油气设备/数据中心电力"),
 "TWM.TO":("Tidewater Midstream","中游/炼化"),"ALS.TO":("Altius Minerals","矿业权利金"),
 "LCFS.TO":("Tidewater Renewables","可再生燃料"),"ASTL.TO":("Algoma Steel","钢铁"),
 "BDT.TO":("Bird Construction","建筑工程"),"VNP.TO":("5N Plus","特种半导体材料"),
 "HHH.V":("Helius Minerals","矿业勘探"),"TNZ.TO":("Tenaz Energy","油气(欧洲)"),
 "HG.CN":("HydroGraph Clean Power","石墨烯材料"),"HPS-A.TO":("Hammond Power","变压器"),
 "TOT.TO":("Total Energy Services","油服"),"NGEX.TO":("NGEx Minerals","铜矿勘探(阿根廷)"),
 "CLS.TO":("Celestica","AI服务器/EMS"),"PNG.V":("Kraken Robotics","海洋机器人/国防"),
 "TRP.TO":("TC Energy","天然气管道"),"BK.TO":("Canadian Banc Corp","银行分级基金"),
 "RGSI.TO":("Rockpoint Gas Storage","天然气储存"),"INTC.TO":("Intel（CDR）","半导体·CDR"),
 "KEY.TO":("Keyera","中游"),"NOA.TO":("North American Construction","油砂重型施工"),
 "ZDC.V":("Zedcor","安防监控"),"CURA.TO":("Curaleaf","大麻(美国)"),
 "MNO.TO":("Meridian Mining","铜金开发(巴西)"),"CVE.TO":("Cenovus Energy","油砂/炼化"),
 "UCU.V":("Ucore Rare Metals","稀土加工"),"ARG.TO":("Amerigo Resources","铜尾矿回收"),
 "GFR.TO":("Greenfire Resources","油砂生产"),"ACB.TO":("Aurora Cannabis","大麻"),
 "ANET.TO":("Arista Networks（CDR）","网络设备·CDR"),"VRT.TO":("Vertiv（CDR）","数据中心电力·CDR"),
 "AMAT.TO":("Applied Materials（CDR）","半导体设备·CDR"),"CSCO.TO":("Cisco（CDR）","网络设备·CDR"),
 "LRCX.TO":("Lam Research（CDR）","半导体设备·CDR"),"KLAC.TO":("KLA（CDR）","半导体设备·CDR"),
 "SCHW.TO":("Charles Schwab（CDR）","券商·CDR"),"SPCX.TO":("SpaceX（CDR）","航天·CDR"),
 "WDC.TO":("Western Digital（CDR）","存储·CDR"),
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
 "date":"2026-10-15","weekday":"周四",
 "snapshot":"2026-10-15 16:00 ET 收盘（补跑快照，18:55 PT 执行）",
 "market_state":"CLOSED",
 "note":"本期为收盘后补跑：早盘定时任务未执行，于 18:55 PT 以当日收盘数据补发。量比按全天成交量（系数 1.0）计算。",
 "vr_note":"量比 = 当日全天成交量 ÷ 3个月日均量（收盘后补跑，系数 1.0）。CDR 行用 TradingView 90 日均量。⚠️≥3，🔥≥8。",
 "gainers":G,"losers":L,
 "table_notes":[
  "*CDR（NKE/NOWS/RDDT/APPS/INTU/INTC/ANET/VRT/AMAT/CSCO/LRCX/KLAC）市值为美股母公司总市值（TradingView 加元口径），非加拿大挂牌流通市值。",
  "*NKE/NOWS/INTC 以 TSX 挂牌数据替代 Yahoo 返回的 NEO 行；RDDT/APPS/INTU 及跌幅榜 ANET/VRT/AMAT/CSCO/LRCX/KLAC 为 TradingView 补充（Yahoo screener 未返回）。",
  "*剔除：NVDA.NE/AMD.NE/TSLA.NE 交叉挂牌去重。所有入榜行 regularMarketTime 均为 10-15 当日，无停牌僵尸数据；TV 交叉验证涨跌幅全部一致。TV 跌幅榜中 DLCG/VCM（NEO 行）最后成交为 10-13/10-08，属陈旧数据，未采纳。",
  "*BK.TO 为分级基金（Class A），TradingView 归类 fund 不在其股票榜，Yahoo 当日数据有效，保留。",
 ],
 "sectors_html":(
  "<ul>"
  "<li><strong>大盘：TSX +1.55% 收 36,137，六周最大单日涨幅、三周新高</strong>：美国初请失业金高于预期压低实际收益率，金价 +2.1% 至 US$4,194/oz（收盘新高）、银价 +3.7% 至 US$57.60，材料板块 +3.3% 领涨，昨日 CPI 冲击下的抛售一日反转。美股同日仅微涨（S&P +0.33%），TSX 显著跑赢。</li>"
  "<li><strong>涨幅榜主线一：贵金属全线反弹，昨日跌幅榜今日集体回榜</strong>：涨幅榜 30 只中 21 只为矿业——ITH +9.9%（昨 -11.6%）、Hemlo +9.6%、NFGC +9.4%、Equinox +7.3%、Kinross +6.9%、Snowline +6.8%、Aris +6.6%、Galiano/Orezone +6.6%、Perpetua +6.4%（昨 -10.2%）、Vista Gold +6.4%、Wesdome +6.1%、Skeena +6.1%、Allied Gold +6.0%、Agnico +5.7%、Endeavour +5.6%；银矿 New Pacific +6.3%、Highlander +5.7%、Capitan +5.7%。铜矿 Ivanhoe Electric +9.1%（昨 -11.2%）、铀矿 Denison +8.8%（昨 -7.2%）、锂矿 LAC +7.1% 同步修复，典型的超跌反弹而非新驱动。</li>"
  "<li><strong>涨幅榜主线二：个股催化</strong>：Black Mammoth（BMM）+11.5% 连续第二日领涨——10/15 正式登陆纳斯达克（BMMX），两日累涨 24%；Bombardier +7.1% 刷新历史新高（欧洲盘同步 +4.6%，公务机需求/回购题材延续）；美股 CDR 科技反弹 Reddit +7.0%、AppLovin +6.5%、Intuit +6.2%（昨 +3.1% 后再度放量）、ServiceNow +6.1%、Nike +5.5%；Lumine +6.2%、Enghouse +5.9% 加拿大软件跟涨。</li>"
  "<li><strong>跌幅榜主线一：财务数据/融资利空个股</strong>：Fiera Capital（FSZ）-13.0% 居榜首——Q3 初步 AUM 从 1,635 亿降至 1,514 亿（-7%），净流出 83 亿（含分销顾问账户 52 亿）叠加利率上行市值缩水 38 亿，多家券商此前已下调目标价至 C$5；Champion Iron（CIA）-9.1%——FY2027 Q2 初步业绩：实现售价 US$89.9/dmt、营收 4.04 亿，近一月累跌 21%、一年腰斩；Canadian Banc（BK）-2.8%、量比 5.9——隔夜增发 Class A（$15.40）与优先股（$10.35）共 6,000 万，折价发行压制股价；Millennial Potash（MLP）-7.7% 昨日 +15.8% 后获利回吐。</li>"
  "<li><strong>跌幅榜主线二：能源/中游与基建承压</strong>：WTI +1.2% 但中游与油服走弱——Enerflex -5.1%、Tidewater Midstream -4.9%、Tidewater Renewables -4.7%、Total Energy -3.3%、TC Energy -2.9%（成交 798 万股）、Keyera -2.6%、Rockpoint -2.8%、Cenovus -2.3%；建筑/工业 Bird Construction -4.1%、Dexterra -5.5%、NOA -2.5%（量比 3.7，榜外）、Algoma Steel -4.5%、Hammond Power -3.4%、5N Plus -4.1%。市场风险偏好回归金矿与科技，昨日抗跌的现金流资产遭轮出。</li>"
  "<li><strong>跌幅榜主线三：半导体/AI 硬件 CDR 回落</strong>：Arista -5.0%、Vertiv -3.7%、Applied Materials -3.6%、Cisco -3.3%、Lam Research -3.1%、Intel -2.9%、KLA -2.6%（WDC/SpaceX -2.3%/-2.5% 榜外），Celestica -3.1% 同步，AI 硬件链在昨日 CoreWeave 债务担忧后继续去风险，而软件/互联网 CDR 走强形成分化。</li>"
  "</ul>"),
 "anomalies_html":(
  "<ul>"
  "<li>⚠️ <strong>BK.TO Canadian Banc Corp</strong> 量比 5.9（-2.8%）：10/14 15:16 停牌待公告，10/15 恢复交易后公告隔夜增发完成——Class A $15.40、优先股 $10.35，总额约 6,000 万，10/22 交割。全天 132 万股为均量 5.6 倍，折价发行引发套利卖压（Class A 收 $15.15 已低于发行价）。</li>"
  "<li>⚠️ <strong>BMM.V Black Mammoth Metals</strong> 量比 5.3（+11.5%）：纳斯达克 BMMX 首日交易，TSXV 端 5.6 万股为均量 4.5 倍（基数仅 1.26 万股/日），两日累涨 24%。</li>"
  "<li>⚠️ <strong>INTU.TO Intuit（CDR）</strong> 量比 4.5（+6.2%）：连续第二日放量上涨（昨量比 3.5），22.8 万份为均量 4.5 倍，软件 CDR 轮动买盘。</li>"
  "<li>⚠️ <strong>FSZ.TO Fiera Capital</strong> 量比 4.3（-13.0%）：Q3 初步 AUM -7%、净流出 83 亿，全天 197 万股为均量 4.3 倍（公司 IR 口径 347 万股），资管费收入前景恶化引发估值重估。</li>"
  "<li>⚠️ <strong>CIA.TO Champion Iron</strong> 量比 4.0（-9.1%）：FY2027 Q2 初步业绩售价/营收不及预期，ASX 同步 -9.7%，TSX 214 万股为均量 4 倍。</li>"
  "<li>⚠️ <strong>VGZ.TO Vista Gold</strong> 量比 3.2（+6.4%）：无公司公告，Mt Todd 金矿开发股随金价新高放量，34 万股为均量 3.2 倍。</li>"
  "</ul>"),
 "digest":"TSX +1.55% 三周新高：金价新高 US$4,194 带动矿业全线反弹（21 只矿股上涨幅榜，ITH/Hemlo/NFGC +9%+），Black Mammoth 纳斯达克首日 +11.5%，Bombardier 新高；Fiera Capital AUM 流出 -13.0%、Champion Iron 季报 -9.1%，中游/AI 硬件 CDR 走弱。",
}
json.dump(data, open(D + "2026-10-15.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in G: print(r)
print("---")
for r in L: print(r)
