import json,glob
m={}
for f in sorted(glob.glob("data/*.json")):
    d=json.load(open(f,encoding="utf-8"))
    for r in d["gainers"]+d["losers"]: m[r[1]]=(r[2],r[6])
m.update({
 "WTE.TO":("Westshore Terminals","煤炭/钾盐码头"),"AP-UN.TO":("Allied Properties REIT","办公 REIT"),
 "GG.V":("Golconda Gold","黄金生产(南非)"),"GUD.TO":("Knight Therapeutics","特种制药"),
 "HR-UN.TO":("H&R REIT","综合 REIT"),"CHR.TO":("Chorus Aviation","支线航空/租赁"),
 "SVI.TO":("StorageVault Canada","自助仓储"),"CURA.TO":("Curaleaf Holdings","美国大麻MSO"),
 "TSLA.TO":("Tesla CDR","电动车(CDR)"),"SMCI.NE":("Super Micro CDR","AI服务器(CDR)"),
 "NKE.NE":("Nike CDR","运动服饰(CDR)"),"NOWS.NE":("ServiceNow CDR","企业软件(CDR)"),
 "HELP.NE":("Cybin (Helus Pharma)","迷幻药生物科技"),"MACK.V":("MacKay Gold and Silver","金银勘探"),
})
res=json.load(open("tmp/merged.json",encoding="utf-8"))
def cap(x,cdr):
    s=f"{x/1e9:.1f}B" if x>=1e9 else f"{x/1e6:.0f}M"
    return s+("*" if cdr else "")
def rows(lst):
    out=[];i=0
    for x in lst:
        if x['sym']=="DGS.TO": continue
        i+=1
        if i>30: break
        cdr=x['sym'].endswith('.NE') or (x['tv'] and x['tv']['type']=='dr')
        name,sec=m[x['sym']]
        out.append([i,x['sym'],name,f"{x['price']:.2f}",f"{x['chg']:+.2f}%",cap(x['cap'],cdr),sec,x['vr']])
    return out
d={
 "date":"2026-10-02","weekday":"周五",
 "snapshot":"2026-10-02 16:00 ET 收盘（补跑：早盘排程未执行，本期按收盘数据生成）",
 "market_state":"CLOSED",
 "note":"⏰ 本期为补跑：早上 7:00 PT 的排程未能执行，数据取自 10 月 2 日收盘快照（Yahoo + TradingView 双源核验），量比按全天口径计算。",
 "vr_note":"量比 = 全天成交量 ÷ 3个月日均量（收盘口径，系数 1.0）。⚠️≥3，🔥≥8。",
 "gainers":rows(res["gainers"]),"losers":rows(res["losers"]),
 "table_notes":["*CDR 市值为美股母公司总市值，非加拿大挂牌市值。","Yahoo 筛选 80 行 → .TO>.V>.CN>.NE 去重 → regularMarketTime 当日校验（本期无停牌僵尸数据）→ TradingView 逐只交叉验证（含 type=dr 补查 CDR）。DGS（分级基金，非经营性公司）已剔除。"],
 "sectors_html":"<ul><li><strong>铜/基本金属全线领涨</strong>：Teck +5.3%、Lundin +5.2%、Capstone +4.7%、Hudbay +4.1%、Ivanhoe +4.0%、Ero +6.5%、Trekor +7.3%——铜价强势 + 战略金属板块周五集体反弹（VanEck 稀土/战略金属 ETF +5.5%）。</li><li><strong>战略金属/锂超跌反弹</strong>：Sigma Lithium +9.4%（10/1 因巴西环保禁令停产暴跌 13% 后抄底）、Colonial Coal +6.2%。</li><li><strong>黄金勘探个股活跃</strong>：Gladiator +10.6%、Founders +7.1%、Helius +6.8%、Liberty Gold +4.5%，但黄金生产商（DPM -3.1%、Hemlo -4.6%、Vizsla -2.8%）回落——资金从金矿生产商向勘探股/铜股轮动。</li><li><strong>个股事件</strong>：Talamore +12.2%（10/2 股东会表决债务融资安排）、Abaxx +10.8%、Firan +7.8%、Westshore +5.5%、Algoma Steel +5.8%。</li><li><strong>跌幅榜</strong>：生物医药（Cardiol -9.0%、Eupraxia -7.8%、Knight -3.0%）、航空（Exchange Income -4.6%、Air Canada -3.6%、Chorus -2.7%）、REIT（Allied -5.6%、H&R -3.0%）、量子概念（Quantum eMotion -5.3%、Xanadu -4.1%）集体走弱；CDR 跌幅股 Nike -3.3%、ServiceNow -3.0%。</li></ul>",
 "anomalies_html":"<ul><li><strong>FDR.V Founders Metals</strong> 量比 5.0⚠️（+7.1%）：未见当日公告，苏里南 Antino 金矿勘探股放量追涨，叠加黄金勘探板块轮动。</li><li><strong>GLAD.V Gladiator Metals</strong> 量比 3.3⚠️（+10.6%）：前一日 -5.5% 后反弹，育空铜矿勘探（Cowley/Cub East 钻探题材），无新公告。</li><li><strong>SGML.V Sigma Lithium</strong> 量比 3.1⚠️（+9.4%）：10/1 巴西法院环保禁令停产暴跌后技术性反弹，JPM/BMO 已下调评级，12 月 1.06 亿美元债务到期压力仍在。</li><li>无 🔥（≥8）级别异常。</li></ul>",
 "digest":"铜/基本金属全线领涨（Teck、Lundin、Capstone），锂股 Sigma 超跌反弹；生物医药、航空、REIT 走弱。异常量比：FDR 5.0、GLAD 3.3、SGML 3.1。"
}
json.dump(d,open("data/2026-10-02.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(len(d["gainers"]),len(d["losers"]))
for r in d["gainers"]+d["losers"]: print(r)
