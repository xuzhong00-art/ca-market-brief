#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate daily brief page from data/YYYY-MM-DD.json and rebuild index.html.

Usage: python scripts/gen.py [date]   (default: newest json in data/)

JSON schema:
{
  "date": "2026-08-21", "weekday": "周五",
  "snapshot": "2026-08-21 16:00 ET 收盘",
  "market_state": "CLOSED",          # REGULAR / CLOSED / ...
  "note": "可选：页顶说明（如试跑说明）",
  "vr_note": "量比口径说明",
  "gainers": [[1,"OGN.V","Orogen Royalties","5.50","+15.79%","326M","贵金属权利金",3.5], ...],
  "losers":  [[...], ...],           # rank, sym, name, price, chg, cap, sector, vr
  "table_notes": ["*INTC 市值为美股母公司总市值"],
  "sectors_html": "<ul><li>...</li></ul>",   # 板块总结（HTML 片段）
  "anomalies_html": "<ul><li>...</li></ul>", # 异常量比（HTML 片段）
  "digest": "index 目录页一句话摘要"
}
"""
import json, sys, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA, BRIEFS = ROOT / "data", ROOT / "briefs"
BRIEFS.mkdir(exist_ok=True)

def vr_cell(vr):
    try: v = float(vr)
    except (TypeError, ValueError): return '<td class="vr">–</td>'
    cls, tag = "", ""
    if v >= 8: cls, tag = " fire", "🔥"
    elif v >= 3: cls, tag = " warn", "⚠️"
    return f'<td class="vr{cls}">{v:g}{tag}</td>'

def render_table(rows):
    out = ['<div class="tablebox"><table><thead><tr>'
           '<th>#</th><th>代码</th><th>公司</th><th>现价</th><th>涨跌</th>'
           '<th>市值</th><th>板块</th><th>量比</th></tr></thead><tbody>']
    for r in rows:
        rank, sym, name, price, chg, cap, sector, vr = r[:8]
        cls = "up" if str(chg).startswith("+") else "down"
        out.append(
            f'<tr><td>{rank}</td><td class="sym">{html.escape(str(sym))}</td>'
            f'<td>{html.escape(str(name))}</td><td>{price}</td>'
            f'<td class="chg {cls}">{chg}</td><td>{cap}</td>'
            f'<td>{html.escape(str(sector))}</td>{vr_cell(vr)}</tr>')
    out.append('</tbody></table></div>')
    return "".join(out)

def render_page(d):
    state = d.get("market_state", "")
    state_cls = "" if state == "REGULAR" else " closed"
    note = f'<div class="card" style="border-color:var(--warn)">{d["note"]}</div>' if d.get("note") else ""
    tnotes = "".join(f'<p class="note">{html.escape(n)}</p>' for n in d.get("table_notes", []))
    vrn = f'<p class="note">{html.escape(d["vr_note"])}</p>' if d.get("vr_note") else ""
    return f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>加股简报 {d["date"]}</title>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<header class="hero"><div class="wrap">
<h1>📊 加股涨跌幅日报</h1>
<div class="sub">{d["date"]}（{d.get("weekday","")}）</div>
<span class="pill">快照：{d.get("snapshot","")}</span><span class="pill{state_cls}">{state}</span>
<div class="sub" style="margin-top:8px"><a href="../index.html">← 历史简报目录</a></div>
</div></header>
<div class="wrap">
{note}
<h2 class="up">📈 涨幅 Top 30</h2>
{render_table(d["gainers"])}
<h2 class="down">📉 跌幅 Top 30</h2>
{render_table(d["losers"])}
{tnotes}{vrn}
<h2>🧭 板块表现总结</h2>
<div class="card">{d.get("sectors_html","")}</div>
<h2 class="warn">🚨 异常量比点名</h2>
<div class="card">{d.get("anomalies_html","")}</div>
<footer>数据源：Yahoo Finance + TradingView（交叉验证）· 自动生成</footer>
</div>
</body>
</html>"""

def rebuild_index(all_data):
    items = []
    for d in all_data:
        dg = html.escape(d.get("digest", ""))
        items.append(f'<li><a href="briefs/{d["date"]}.html">'
                     f'<div class="d">{d["date"]}（{d.get("weekday","")}）</div>'
                     f'<div class="m">{dg}</div></a></li>')
    page = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>加股涨跌幅日报</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="hero"><div class="wrap">
<h1>📊 加股涨跌幅日报</h1>
<div class="sub">TSX / TSXV / CSE / Cboe CA · 每交易日 7:00 PT 更新 · 涨跌 Top30 + 板块总结 + 异常量比</div>
</div></header>
<div class="wrap">
<ul class="arch">
{chr(10).join(items)}
</ul>
<footer>数据源：Yahoo Finance + TradingView（交叉验证）· 自动生成</footer>
</div>
</body>
</html>"""
    (ROOT / "index.html").write_text(page, encoding="utf-8")

def main():
    files = sorted(DATA.glob("*.json"), reverse=True)
    if not files:
        sys.exit("no data files")
    target = sys.argv[1] if len(sys.argv) > 1 else files[0].stem
    all_data = [json.loads(f.read_text(encoding="utf-8")) for f in files]
    for d in all_data:
        if d["date"] == target:
            (BRIEFS / f"{d['date']}.html").write_text(render_page(d), encoding="utf-8")
            print("wrote briefs/%s.html" % d["date"])
    rebuild_index(all_data)
    print("rebuilt index.html (%d entries)" % len(all_data))

if __name__ == "__main__":
    main()
