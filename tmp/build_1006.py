# -*- coding: utf-8 -*-
import json
ws=r"C:\Users\Elliott\AppData\Local\hermes\cache\browser-use\workspace\06e2dfa6-d208-48ab-96b1-a485d91f3c66"
y=json.load(open(ws+r"\yahoo.json")); tv2=json.load(open(ws+r"\tv2.json"))
Y={}
for s in ('DESC','ASC'):
    for r in y[s]: Y[r['symbol']]=r
T={(x['exch'],x['name']):x for x in tv2}
F=0.10  # 10:11 ET snapshot, ~0.68h of 6.5h

def cap(v):
    return f"{v/1e9:.1f}B" if v>=1e9 else f"{v/1e6:.0f}M"

def yrow(sym,name,sector):
    r=Y[sym]; vr=r['regularMarketVolume']/(r['averageDailyVolume3Month']*F) if r['averageDailyVolume3Month'] else None
    p=r['regularMarketPrice']; chg=r['regularMarketChangePercent']
    return [sym,name,f"{p:.2f}",f"{chg:+.2f}%",cap(r['marketCap']),sector,round(vr,1) if vr else None]

def trow(exch,name,disp,cn,sector):
    x=T[(exch,name)]; vr=x['vol']/(x['avg30']*F)
    return [disp,cn,f"{x['close']:.2f}",f"{x['change']:+.2f}%",cap(x['cap']*1e6) if x['cap']<1e7 else cap(x['cap']),sector,round(vr,1)]

G=[
 trow('TSX','CEGS','CEGS.TO','Constellation Energy (CDR)','美股CDR·核电/电力'),
 yrow('KLD.V','Kenorland Minerals','黄金勘探/项目生成'),
 yrow('ACO-X.TO','ATCO','公用事业控股'),
 trow('TSX','MRV','MRV.TO','Marvell Technology (CDR)','美股CDR·半导体'),
 yrow('XNDU.TO','Xanadu Quantum','量子计算'),
 yrow('ISO.TO','IsoEnergy','铀矿'),
 yrow('ZVST.NE','Vistra (CDR)','美股CDR·电力'),
 yrow('ALDE.V','Aldebaran Resources','铜金勘探(阿根廷)'),
 yrow('NXE.TO','NexGen Energy','铀矿'),
 yrow('DML.TO','Denison Mines','铀矿'),
 yrow('BTQ.NE','BTQ Technologies','后量子加密'),
 trow('TSX','GEV','GEV.TO','GE Vernova (CDR)','美股CDR·电力设备'),
 yrow('BB.TO','BlackBerry','软件/QNX'),
 yrow('EFR.TO','Energy Fuels','铀/稀土'),
 trow('TSX','CRWD','CRWD.TO','CrowdStrike (CDR)','美股CDR·网络安全'),
 trow('TSX','CRWV','CRWV.TO','CoreWeave (CDR)','美股CDR·AI算力云'),
 yrow('CCO.TO','Cameco','铀矿龙头'),
 yrow('PRL.TO','Propel Holdings','金融科技/消费信贷'),
 yrow('CURA.TO','Curaleaf','大麻'),
 trow('TSX','FISV','FISV.TO','Fiserv (CDR)','美股CDR·支付'),
 yrow('TA.TO','TransAlta','独立发电'),
 yrow('ELVA.TO','Electrovaya','锂电池'),
 yrow('EPRX.TO','Eupraxia Pharmaceuticals','生物科技'),
 yrow('WJX.TO','Wajax','工业设备分销'),
 yrow('MACK.V','Mackay Gold & Silver','金银勘探(内华达)'),
 yrow('QBR-B.TO','Quebecor','电信'),
 trow('TSX','NOWS','NOWS.TO','ServiceNow (CDR)','美股CDR·企业软件'),
 trow('TSX','ABT','ABT.TO','Abbott Labs (CDR)','美股CDR·医疗器械'),
 yrow('MDA.TO','MDA Space','航天'),
 yrow('SMCI.NE','Super Micro Computer (CDR)','美股CDR·AI服务器'),
]
L=[
 trow('TSX','WDC','WDC.TO','Western Digital (CDR)','美股CDR·存储'),
 trow('TSX','CMGS','CMGS.TO','Chipotle (CDR)','美股CDR·餐饮'),
 yrow('MAXX.CN','Max Power Mining','天然氢勘探'),
 yrow('HG.CN','HydroGraph Clean Power','石墨烯材料'),
 yrow('BZ.V','Benz Mining','黄金勘探(澳洲)'),
 yrow('DPM.TO','DPM Metals','黄金生产'),
 yrow('TLO.TO','Talon Metals','镍铜勘探'),
 yrow('PHOS.CN','First Phosphate','磷矿/LFP'),
 yrow('SCZ.TO','Santacruz Silver','白银生产'),
 yrow('CS.TO','Capstone Copper','铜矿'),
 yrow('FDY.TO','Faraday Copper','铜勘探'),
 yrow('ERO.TO','Ero Copper','铜矿'),
 yrow('EFX.TO','Enerflex','油气设备服务'),
 yrow('CVO.TO','Coveo Solutions','AI企业搜索软件'),
 yrow('IPCO.TO','International Petroleum','油气生产'),
 yrow('CEU.TO','CES Energy Solutions','油田化学品'),
 yrow('CADY.TO','Cadillac Mines','黄金勘探'),
 yrow('ABRA.TO','AbraSilver Resource','白银勘探'),
 yrow('TCW.TO','Trican Well Service','油服'),
 trow('TSX','KLAC','KLAC.TO','KLA Corp (CDR)','美股CDR·半导体设备'),
 yrow('GIB-A.TO','CGI','IT服务'),
 yrow('WDO.TO','Wesdome Gold Mines','黄金生产'),
 yrow('TALA.TO','Talamore Mining','铜金勘探'),
 yrow('EXE.TO','Extendicare','养老护理'),
 yrow('CERT.V','Cerrado Gold','黄金生产'),
 yrow('TKO.TO','Trekor Metals','铜金矿业'),
 yrow('HBM.TO','Hudbay Minerals','铜矿'),
 yrow('HMMC.TO','Hemlo Mining','黄金生产'),
 yrow('IVN.TO','Ivanhoe Mines','铜矿(非洲)'),
 yrow('ARG.TO','Amerigo Resources','铜尾矿回收'),
]
G=[[i+1]+r for i,r in enumerate(G)]
L=[[i+1]+r for i,r in enumerate(L)]
for r in G+L: print(r)

d={
 "date":"2026-10-06","weekday":"周二",
 "snapshot":"2026-10-06 10:11 ET 早盘（开盘约40分钟）",
 "market_state":"REGULAR",
 "vr_note":"量比 = 当日成交量 ÷ (3个月日均量 × 0.10)，0.10 为快照时已开盘约 0.68 小时占全日 6.5 小时的比例。CDR 行（由 TradingView 补入）用 30 日均量。⚠️≥3，🔥≥8。早盘量比对开盘集合竞价敏感，数值偏高属正常，请结合全天观察。",
 "gainers":G,"losers":L,
 "table_notes":["*CDR 市值为美股母公司总市值，非加拿大挂牌市值。",
   "Yahoo 筛选 80 行 → .TO>.V>.CN>.NE 去重 → regularMarketTime 当日校验（本期无停牌僵尸数据）→ TradingView 逐只交叉验证（含 type=dr 补查 CDR：CEGS/MRV/GEV/CRWD/CRWV/FISV/NOWS/ABT/WDC/CMGS/KLAC 由 TV 补入）。DGS（分级基金）与 U.UN（实物铀信托）为非经营性基金，已剔除。"],
 "sectors_html":"<ul>"
  "<li><strong>公用事业世纪并购</strong>：Emera 宣布以全股票方式合并 Canadian Utilities 并收购 ATCO（CU 的 A 股换 0.755 股 EMA，ATCO 每股换 0.865 股 EMA + 1 股 New ATCO），合并后企业价值约 720 亿加元。ATCO +12.8%（量比 17🔥），收购方 Emera -1.8%（量比 5.0⚠️，未进前 30）。</li>"
  "<li><strong>铀矿板块集体走强</strong>：IsoEnergy +7.7%、NexGen +6.3%、Denison +6.2%、Energy Fuels +5.4%、Cameco +4.5%，实物铀信托 U.UN +2.4%——核电需求题材延续（美股 Constellation 同日大涨）。</li>"
  "<li><strong>美股 CDR 映射 AI 电力/芯片主线</strong>：Constellation Energy +14.0%（Amazon 20 年核电购电协议刺激）、Marvell +9.9%（Investor Day 当日）、Vistra +7.3%、GE Vernova +5.8%、CoreWeave +4.6%、CrowdStrike +4.7%；存储股回落 Western Digital -5.6%，Chipotle -5.0%，KLA -2.2%。</li>"
  "<li><strong>勘探与科技个股</strong>：Kenorland +13.0%（Franco-Nevada 以 $2.22/股私下购入 12.42% 股权成为大股东）、Xanadu +7.8%（量子计算热度延续，量比 11.7🔥）、Aldebaran +6.3%（昨日 Altar 超长铜金钻孔后续涨，量比 9.9🔥）、BlackBerry +5.7%、BTQ +6.0%、Mackay +2.8%（量比 11.6🔥）。</li>"
  "<li><strong>跌幅榜</strong>：铜矿股普跌（Capstone -2.9%、Ero -2.8%、Faraday -2.8%、Hudbay -2.1%、Ivanhoe -1.9%、Amerigo -1.8%、Talon -3.6%），金银生产/勘探回调（DPM -3.7%、Benz -3.8%、Santacruz -2.9%、Cadillac -2.4%、AbraSilver -2.3%、Wesdome -2.2%、Hemlo -2.0%）；油服与油气（Enerflex -2.8%、IPCO -2.6%、CES -2.6%、Trican -2.2%）；HydroGraph -4.3%（量比 6.2⚠️）、Max Power -4.9% 等小盘题材股退潮。</li></ul>",
 "anomalies_html":"<ul>"
  "<li><strong>ZVST.NE Vistra (CDR)</strong> 量比 48.6🔥（+7.3%）：NEO 挂牌 CDR 日均量仅 1.3 万，早盘 6.3 万股即放大 50 倍，母公司 Vistra 随 AI 电力题材走强，小基数效应为主。</li>"
  "<li><strong>ACO-X.TO ATCO</strong> 量比 17.3🔥（+12.8%）：Emera 全股票收购 ATCO/Canadian Utilities，每股 ATCO 换 0.865 股 Emera 外加 New ATCO 分拆股，套利盘涌入。</li>"
  "<li><strong>CEGS.TO Constellation Energy (CDR)</strong> 量比 13.3🔥（+14.0%）：母公司与 Amazon 签订 20 年核电购电协议，美股盘前大涨。</li>"
  "<li><strong>MRV.TO Marvell (CDR)</strong> 量比 12.9🔥（+9.9%）：10/6 Investor Day，AI 定制芯片预期升温。</li>"
  "<li><strong>XNDU.TO Xanadu Quantum</strong> 量比 11.7🔥（+7.8%）：无新公告，延续上周 Bluefors 合作+RBC 覆盖后的量子题材追涨。</li>"
  "<li><strong>MACK.V Mackay Gold & Silver</strong> 量比 11.6🔥（+2.8%）：早盘 5.6 万股 vs 日均 4.8 万股，未见当日公告，Comstock 2 万米钻探结果陆续披露中。</li>"
  "<li><strong>ALDE.V Aldebaran Resources</strong> 量比 9.9🔥（+6.3%）：10/5 Altar 项目 1,728.9 米 0.45% CuEq 钻孔后第二日续涨放量。</li>"
  "<li><strong>FISV.TO Fiserv (CDR)</strong> 量比 14.0🔥（+3.6%）、<strong>KLAC.TO KLA (CDR)</strong> 量比 11.3🔥（-2.2%）、<strong>CMGS.TO Chipotle (CDR)</strong> 量比 19.0🔥（-5.0%）、<strong>GEV.TO GE Vernova (CDR)</strong> 8.0🔥（+5.8%）、<strong>ABT.TO Abbott (CDR)</strong> 7.5⚠️、<strong>WDC.TO Western Digital (CDR)</strong> 6.9⚠️（-5.6%，上周五 -10% 后继续回落）、<strong>CRWD.TO</strong> 5.2⚠️、<strong>CRWV.TO</strong> 4.0⚠️、<strong>NOWS.TO</strong> 3.3⚠️：CDR 日均量小（数千至十几万股），早盘单笔成交即触发高量比，参考意义有限。</li>"
  "<li><strong>WJX.TO Wajax</strong> 量比 6.5⚠️（+3.1%）：无当日公告，连续第二日放量上涨。</li>"
  "<li><strong>DML.TO Denison Mines</strong> 量比 6.1⚠️（+6.2%）、<strong>ISO.TO IsoEnergy</strong> 4.8⚠️、<strong>BB.TO BlackBerry</strong> 4.3⚠️、<strong>KLD.V Kenorland</strong> 4.0⚠️、<strong>NXE.TO NexGen</strong> 3.6⚠️、<strong>EPRX.TO Eupraxia</strong> 3.3⚠️：板块/事件驱动放量。</li>"
  "<li><strong>HG.CN HydroGraph</strong> 量比 6.2⚠️（-4.3%）：延续 10/2 以来回调，无新公告。</li>"
  "<li><strong>BZ.V Benz Mining</strong> 量比 4.0⚠️（-3.8%）、<strong>IPCO.TO International Petroleum</strong> 3.1⚠️（-2.6%）。</li></ul>",
 "digest":"Emera 720 亿企业价值合并 Canadian Utilities/ATCO，ATCO +12.8%（量比 17🔥）；铀矿板块集体走强（ISO +7.7%、NXE +6.3%、DML +6.2%、CCO +4.5%）；Kenorland +13.0%（Franco-Nevada 入股）；CDR 端 Constellation +14.0%（Amazon 核电协议）、Marvell +9.9%。铜矿、金银股与油服回调，Western Digital CDR -5.6%。"
}
json.dump(d,open("data/2026-10-06.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("written")
