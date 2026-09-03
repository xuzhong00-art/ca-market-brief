#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fetch TSX/TSXV/CSE/NEO movers from TradingView scanner (stock + dr types)."""
import json, sys, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

def tv_scan(sort_order, types, nrows=80):
    body = {
        "filter": [
            {"left": "close", "operation": "greater", "right": 2},
            {"left": "market_cap_basic", "operation": "egreater", "right": 2e8},
            {"left": "volume", "operation": "greater", "right": 15000},
            {"left": "type", "operation": "in_range", "right": types},
        ],
        "options": {"lang": "en"},
        "markets": ["canada"],
        "columns": ["name", "description", "close", "change", "market_cap_basic",
                    "sector", "volume", "average_volume_90d_calc", "type",
                    "exchange", "update_mode", "time"],
        "sort": {"sortBy": "change", "sortOrder": sort_order},
        "range": [0, nrows],
    }
    req = urllib.request.Request(
        "https://scanner.tradingview.com/canada/scan",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "User-Agent": UA,
                 "Origin": "https://www.tradingview.com",
                 "Referer": "https://www.tradingview.com/"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

out = {}
for order in ("desc", "asc"):
    for types in (["stock"], ["dr"]):
        key = f"{order}_{types[0]}"
        try:
            res = tv_scan(order, types)
            out[key] = res
            print(key, "count", res.get("totalCount"), "rows", len(res.get("data", [])), file=sys.stderr)
        except Exception as e:
            print(key, "FAIL", type(e).__name__, e, file=sys.stderr)
            out[key] = None

with open(sys.argv[1] if len(sys.argv) > 1 else "tv_raw.json", "w", encoding="utf-8") as f:
    json.dump(out, f)
print("done")
