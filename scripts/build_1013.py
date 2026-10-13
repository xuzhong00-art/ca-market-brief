# -*- coding: utf-8 -*-
"""Build data/2026-10-13.json from _proc.json + TV-only CDR rows + manual meta (intraday 10:41 ET)."""
import json

D = "C:/Users/Elliott/Downloads/claude/ca-market-brief/data/"
proc = json.load(open(D + "_proc.json", encoding="utf-8"))
FRAC = 0.185  # 10:41 ET snapshot, ~72 min of 390

# .NE rows -> replace with fuller .TO data (TV lookup 10:42 ET): sym, price, chg, cap, vol, avg
TO_OVERRIDE = {
 "MU.NE": ("MU.TO", 41.41, -8.12, 1599.1e9, 1003066, 1802489),
}
# TV-only additions (absent from Yahoo screener): sym, name, price, chg, cap, vol, avg90
TV_ADD = {
 "gainers": [
  ("CRM.TO", "Salesforce（CDR）", 18.33, 5.28, 275.1e9, 63979, 131184),
  ("VZ.TO", "Verizon（CDR）", 18.00, 3.27, 254.0e9, 35459, 16111),
 ],
 "losers": [
  ("SNDK.TO", "SanDisk（CDR）", 35.24, -8.11, 307.2e9, 468486, 803392),
  ("WDC.TO", "Western Digital（CDR）", 22.48, -7.18, 207.0e9, 68281, 115737),
  ("ANET.TO", "Arista Networks（CDR）", 36.10, -7.03, 380.1e9, 15226, 31992),
  ("SMCI.TO", "Super Micro（CDR）", 12.57, -6.61, 37.5e9, 207741, 618502),
 ],
}
EXCLUDE = set()

META = {
 "RM.TO":("Roxmore Resources","黄金开发(内华达)"),"EFX.TO":("Enerflex","油气设备/发电"),
 "META.TO":("Meta（CDR）","互联网·CDR"),"MAXX.CN":("MaxPower Mining","天然氢/矿业"),
 "TOI.V":("Topicus.com","垂直软件"),"OTEX.TO":("Open Text","企业软件"),
 "DCBO.TO":("Docebo","企业学习软件"),"PXT.TO":("Parex Resources","油气(哥伦比亚)"),
 "TNZ.TO":("Tenaz Energy","油气(欧洲)"),"POU.TO":("Paramount Resources","油气生产"),
 "SHOP.TO":("Shopify","电商软件"),"JOY.TO":("Journey Energy","油气生产"),
 "BCE.TO":("BCE","电信"),"OBE.TO":("Obsidian Energy","油气生产"),
 "T.TO":("TELUS","电信"),"CNQ.TO":("Canadian Natural","油气综合"),
 "CVE.TO":("Cenovus Energy","油气综合"),"SU.TO":("Suncor Energy","油气综合"),
 "DXT.TO":("Dexterra Group","设施服务"),"CKG.V":("Chesapeake Gold","黄金开发"),
 "AAPL.TO":("Apple（CDR）","消费电子·CDR"),"OVV.TO":("Ovintiv","油气生产"),
 "TWM.TO":("Tidewater Midstream","中游/炼化"),"BTE.TO":("Baytex Energy","油气生产"),
 "GFR.TO":("Greenfire Resources","油砂"),"CAS.TO":("Cascades","纸业包装"),
 "IMO.TO":("Imperial Oil","油气综合"),"CVO.TO":("Coveo Solutions","企业AI软件"),
 "MSFT.TO":("Microsoft（CDR）","软件·CDR"),"RBA.TO":("RB Global","工业拍卖"),
 "DSG.TO":("Descartes Systems","物流软件"),"TCL-A.TO":("Transcontinental","印刷包装"),
 "SCR.TO":("Strathcona Resources","油气生产"),"GIB-A.TO":("CGI","IT服务"),
 "XNDU.TO":("Xanadu Quantum","量子计算"),"ELVA.TO":("Electrovaya","锂电池"),
 "BTQ.NE":("BTQ Technologies","后量子加密"),"WDO.TO":("Wesdome Gold","黄金生产"),
 "MAI.TO":("Mining Americas","黄金生产(内华达)"),"DPRO.CN":("Draganfly","无人机"),
 "MU.TO":("Micron（CDR）","半导体·CDR"),"EPRX.TO":("Eupraxia Pharma","生物制药"),
 "SLI.V":("Standard Lithium","锂矿"),"PMET.TO":("PMET Resources","锂矿"),
 "KEEL.TO":("Keel Infrastructure","数字基建"),"USA.TO":("Americas Gold & Silver","银矿"),
 "HPS-A.TO":("Hammond Power","电力变压器"),"BLDP.TO":("Ballard Power","氢燃料电池"),
 "SGML.V":("Sigma Lithium","锂矿"),"EFR.TO":("Energy Fuels","铀/稀土"),
 "GMG.V":("Graphene Mfg Group","石墨烯电池"),"LAR.TO":("Lithium Argentina","锂矿"),
 "CLS.TO":("Celestica","AI服务器/EMS"),"SCZ.TO":("Santacruz Silver","银矿"),
 "SSRM.TO":("SSR Mining","黄金生产"),"TLRY.TO":("Tilray Brands","大麻"),
 "LAC.TO":("Lithium Americas","锂矿"),"HIVE.TO":("HIVE Digital","加密挖矿/算力"),
 "LIF.TO":("Labrador Iron Ore","铁矿权利金"),"TAU.V":("Thesis Gold","金银勘探"),
 "WRN.TO":("Western Copper & Gold","铜金开发"),"FTG.TO":("Firan Technology","航空电子"),
 "PHOS.CN":("First Phosphate","磷矿(LFP)"),"GSKR.V":("Goldsky Resources","黄金勘探"),
 "HSTR.TO":("Heliostar Metals","金矿(墨西哥)"),"ITR.V":("Integra Resources","黄金生产"),
 "QNC.V":("Quantum eMotion","量子安全"),"CDE.TO":("Coeur Mining","金银生产"),
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
        if r["sym"] not in META and "CDR" in str(r["name"]): sec = "CDR"
        out.append([i, r["sym"], name, f"{r['price']:.2f}", f"{r['chg']:+.2f}%", cap_s(r["cap"]), sec, r["vr"]])
    return out

G, L = build("gainers", True), build("losers", False)
data = {
 "date":"2026-10-13","weekday":"周二",
 "snapshot":"2026-10-13 10:41 ET 盘中（开盘约 70 分钟，手动补跑快照）",
 "market_state":"REGULAR",
 "note":"本期为手动补跑：早盘定时任务未执行，于 07:41 PT（10:41 ET）以盘中数据补发。量比按已开盘约 72 分钟折算。",
 "vr_note":"量比 = 当日成交量 ÷ (3个月日均量 × 0.185)，0.185 为开盘 72 分钟占 6.5 小时交易日的比例。CDR 行用 TradingView 90 日均量。⚠️≥3，🔥≥8。",
 "gainers":G,"losers":L,
 "table_notes":[
  "*CDR（META/AAPL/MSFT/CRM/VZ/MU/SNDK/WDC/ANET/SMCI）市值为美股母公司总市值，非加拿大挂牌流通市值。",
  "*MU 以 TSX 挂牌（MU.TO）数据替代 Yahoo 返回的 NEO 行；SNDK/WDC/ANET/SMCI/CRM/VZ 为 TradingView 补充（Yahoo screener 未返回）。",
  "*剔除：HSTR.V（Yahoo 返回 10-06 僵尸数据，TSX 主挂牌 HSTR.TO 实为 -5.5% 在跌幅榜）；META.NE/MSFT.NE/BEPC.TO 交叉挂牌去重。",
  "*CKG.V Yahoo +2.99% 与 TV +5.65% 不一致（成交仅 1.7 万股，薄量跳价），取 Yahoo 口径保守列示。",
 ],
 "sectors_html":(
  "<ul>"
  "<li><strong>并购驱动的黄金股成为榜首</strong>：Roxmore（RM）+30.5% 领跑——SSR Mining 以每股 C$6.75 现金 + 0.33 股勘探 SpinCo（合计约 C$7.25，溢价 36%）收购，总对价约 C$7.12 亿；买方 SSRM 自身 -6.3% 落入跌幅榜，典型的「买家折价、卖家溢价」。</li>"
  "<li><strong>油气板块整体走强</strong>：涨幅榜 30 只中 15 只为油气（CNQ/CVE/SU/IMO 四大综合油企齐涨 +2.4~3.2%，PXT/TNZ/POU/JOY/OBE/BTE/OVV/GFR/SCR 等生产商 +2.5~4.3%），油价回升带动加股能源权重股普涨。Enerflex（EFX）+13.3% 则是独立催化剂：拿下 >1GW 数据中心配套燃气发电设备订单，表计后发电积压突破 1.75GW。</li>"
  "<li><strong>软件/电信防御性反弹</strong>：OTEX/TOI/DCBO/SHOP/CVO/DSG/GIB-A 等软件股 +2.3~5%，BCE/T 电信双雄 +3.3~3.6%；美股 CDR 中 META +7.1%、CRM +5.3%、AAPL/MSFT +2.5~2.9%，大型科技（非半导体）获资金回流。</li>"
  "<li><strong>跌幅榜：存储/半导体 CDR 集体重挫</strong>：MU -8.1%、SNDK -8.1%、WDC -7.2%、ANET -7.0%、SMCI -6.6%——美股内存板块因中国 CXMT 宣布进军服务器 DDR5 内存引发供给担忧而暴跌，Celestica（CLS）-6.7% 作为 AI 服务器代工受连带拖累。</li>"
  "<li><strong>贵金属生产商回调</strong>：WDO -9.5%（Q3 产量同比 -18%，Eagle River 品位骤降，全年指引下调至区间下半段）、MAI -7.8%（Q3 产量 7,915 盎司，仅「符合预算」）、USA/SCZ/SSRM/CDE/HSTR/ITR 跟跌 -4~7%，金银股在连涨后获利了结。</li>"
  "<li><strong>锂矿与量子/新能源成长股普跌</strong>：SLI/PMET/SGML/LAR/LAC 五只锂矿 -6~7.6%；XNDU -10.8%、QNC -5.4% 量子板块退潮；ELVA/BLDP/GMG 电池/氢能 -6.8~10.6%，高 beta 主题股被集中抛售。</li>"
  "</ul>"),
 "anomalies_html":(
  "<ul>"
  "<li>🔥 <strong>RM.TO Roxmore Resources</strong> 量比 71.1（+30.5%）：被 SSR Mining 收购，现价 6.945 已接近 C$7.25 的隐含总对价，剩余为 SpinCo 估值博弈，套利盘涌入推高成交。</li>"
  "<li>🔥 <strong>XNDU.TO Xanadu Quantum</strong> 量比 8.4（-10.8%）：量子板块集体回调，XNDU 自上市后波动极大，无公司层面公告，属主题资金撤退。</li>"
  "<li>🔥 <strong>VZ.TO Verizon（CDR）</strong> 量比 11.9（+3.3%）：绝对成交仅 3.5 万份，CDR 均量基数小导致倍数放大，参考价值有限。</li>"
  "<li>⚠️ <strong>DPRO.CN Draganfly</strong> 量比 6.7（-7.7%）：昨晚宣布成立美国国防子公司（前海军部代理部长 Modly 任主席）、今晨又宣布投资乌克兰无人机自主导航公司 DoD Solution，利好出尽转跌。</li>"
  "<li>⚠️ <strong>GMG.V Graphene Mfg Group</strong> 量比 5.9（-6.8%）：发布石墨烯快充电池循环测试新数据后高开低走。</li>"
  "<li>⚠️ <strong>CVO.TO Coveo</strong> 量比 5.8（+2.5%）：延续上周 Metcash（澳洲）扩大 AI 合作的利好，软件板块反弹叠加。</li>"
  "<li>⚠️ <strong>MAXX.CN MaxPower Mining</strong> 量比 5.5（+6.2%）：天然氢概念持续活跃，连续多日上榜。</li>"
  "<li>⚠️ <strong>MAI.TO Mining Americas</strong> 量比 4.9（-7.8%）：Q3 产量公告后抛压。</li>"
  "<li>⚠️ <strong>QNC.V Quantum eMotion</strong> 量比 4.4（-5.4%）：随量子板块回落。</li>"
  "<li>⚠️ <strong>HIVE.TO HIVE Digital</strong> 量比 3.4（-5.9%）、<strong>SSRM.TO SSR Mining</strong> 量比 3.1（-6.3%，收购 Roxmore 买方折价）、<strong>AAPL.TO / OVV.TO</strong> 量比 3.0。</li>"
  "</ul>"),
 "digest":"Roxmore 被 SSR Mining 溢价收购 +30%；油气权重普涨、Enerflex 数据中心发电订单 +13%；存储/半导体 CDR（MU/SNDK/WDC）重挫 -7~8%，Wesdome 产量不达预期 -9.5%。",
}
json.dump(data, open(D + "2026-10-13.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in G: print(r)
print("---")
for r in L: print(r)
