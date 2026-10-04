#!/usr/bin/env python3
"""
fetch_prices.py  —  Phase 2 weekly price + return snapshot

Pulls Friday-close prices for the 7 tracked tickers from Finnhub and computes
every number the weekly review needs, using the EXACT same math as the
dashboard (index.html compute()). The point: the log, the dashboard, and the
standalone review all agree because they come from one place.

Usage:
  python fetch_prices.py --key YOUR_FINNHUB_KEY            # live
  python fetch_prices.py --prices quotes.json              # pre-fetched prices (sandboxed envs)
  python fetch_prices.py --mock                            # offline self-test (W6 fallback)
  python fetch_prices.py --key KEY --dividends 1.00 --json out.json

Output: a JSON snapshot to stdout (and optionally a file). No reasoning here —
just deterministic arithmetic so the cloud-Claude run never has to do math.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import re
import os
from datetime import datetime, timezone

# ---- Static experiment config (mirrors index.html POS / entries) ----
POSITIONS = [
    {"t": "MU",  "theme": "AI / Semi — memory",          "shares": 0.12617, "entry": 792.53},
    {"t": "LLY", "theme": "Healthcare / GLP-1",           "shares": 0.10583, "entry": 944.90},
    {"t": "CEG", "theme": "Energy / AI power (nuclear)",  "shares": 0.31744, "entry": 315.02},
    {"t": "LMT", "theme": "Defense / quality value",      "shares": 0.19849, "entry": 503.78},
    {"t": "MA",  "theme": "Fintech / payments",           "shares": 0.20202, "entry": 495.00},
]
SPY_ENTRY = 739.30
QQQ_ENTRY = 713.29
TOTAL_INVESTED = 499.99
ENTRY_DATE = "May 11, 2026"

# Offline self-test prices = the W6 (June 19) fallback snapshot from index.html.
# With dividends=1.00 this should reproduce the logged W6 total return of +10.00%.
MOCK_PRICES = {
    "MU": 1151.80, "LLY": 1098.78, "CEG": 274.06, "LMT": 511.05,
    "MA": 489.79, "SPY": 746.93, "QQQ": 740.62,
}

FINNHUB_QUOTE = "https://finnhub.io/api/v1/quote?symbol={sym}&token={key}"


QUOTE_DATES = {}  # ticker -> UTC date of the quote, filled by fetch_finnhub


def key_from_html(path):
    """Read the FINNHUB_KEY constant from the dashboard so the key lives in one place."""
    with open(path, encoding="utf-8") as f:
        m = re.search(r'const FINNHUB_KEY\s*=\s*"([^"]+)"', f.read())
    if not m:
        raise SystemExit(f"ERROR: no FINNHUB_KEY found in {path}")
    return m.group(1)


def fetch_finnhub(key):
    """Return {ticker: last_price} from Finnhub /quote (.c field) for all symbols."""
    symbols = [p["t"] for p in POSITIONS] + ["SPY", "QQQ"]
    prices = {}
    for sym in symbols:
        url = FINNHUB_QUOTE.format(sym=sym, key=key)
        req = urllib.request.Request(url, headers={"User-Agent": "pf-lessons-weekly"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            j = json.loads(resp.read().decode())
        c = j.get("c")
        if not c:  # 0 or missing = bad/empty quote
            raise ValueError(f"{sym}: no price returned (got {j!r})")
        prices[sym] = float(c)
        if j.get("t"):
            QUOTE_DATES[sym] = datetime.fromtimestamp(j["t"], tz=timezone.utc).strftime("%Y-%m-%d")
    return prices


def compute(prices, cum_dividends):
    """Same logic as the dashboard's compute(). Returns a structured snapshot."""
    rows = []
    value = 0.0
    for p in POSITIONS:
        px = prices[p["t"]]
        ret = (px / p["entry"] - 1) * 100
        val = px * p["shares"]
        value += val
        rows.append({
            "ticker": p["t"], "theme": p["theme"], "shares": p["shares"],
            "entry": p["entry"], "price": round(px, 2),
            "return_pct": round(ret, 2), "value": round(val, 2),
        })
    price_val = value
    total_val = value + cum_dividends
    price_ret = (price_val / TOTAL_INVESTED - 1) * 100
    total_ret = (total_val / TOTAL_INVESTED - 1) * 100
    spy_ret = (prices["SPY"] / SPY_ENTRY - 1) * 100
    qqq_ret = (prices["QQQ"] / QQQ_ENTRY - 1) * 100
    return {
        "entry_date": ENTRY_DATE,
        "total_invested": TOTAL_INVESTED,
        "cum_dividends": round(cum_dividends, 2),
        "positions": rows,
        "price_value": round(price_val, 2),          # price-only sum = log's "Portfolio Value" column
        "portfolio_value": round(total_val, 2),       # price + dividends = dashboard's value tile
        "price_return_pct": round(price_ret, 2),
        "total_return_pct": round(total_ret, 2),
        "pl_dollars": round(total_val - TOTAL_INVESTED, 2),
        "benchmarks": {
            "SPY": {"price": round(prices["SPY"], 2), "return_pct": round(spy_ret, 2)},
            "QQQ": {"price": round(prices["QQQ"], 2), "return_pct": round(qqq_ret, 2)},
        },
        "vs_spy_pp": round(total_ret - spy_ret, 2),
        "vs_qqq_pp": round(total_ret - qqq_ret, 2),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", help="Finnhub API key (live mode)")
    ap.add_argument("--live", action="store_true",
                    help="live mode, reading the key from FINNHUB_KEY in ../index.html")
    ap.add_argument("--prices", help="path to a JSON file of {ticker: close_price} for all 7 symbols "
                                     "(use when this environment can't reach Finnhub directly — fetch the "
                                     "quotes via another tool, save them, and let this script do the math)")
    ap.add_argument("--mock", action="store_true", help="offline self-test with W6 fallback prices")
    ap.add_argument("--dividends", type=float, default=1.00,
                    help="cumulative dividends earned to date (from the Dividend Ledger)")
    ap.add_argument("--json", help="also write the snapshot to this file path")
    args = ap.parse_args()

    if args.mock:
        prices = MOCK_PRICES
    elif args.prices:
        with open(args.prices) as f:
            prices = {k: float(v) for k, v in json.load(f).items()}
        expected = {p["t"] for p in POSITIONS} | {"SPY", "QQQ"}
        missing = expected - set(prices)
        if missing:
            print(f"ERROR: --prices file missing symbols: {sorted(missing)}", file=sys.stderr)
            sys.exit(1)
        bad = [s for s in expected if prices[s] <= 0]
        if bad:
            print(f"ERROR: non-positive price for: {bad}", file=sys.stderr)
            sys.exit(1)
    elif args.key or args.live:
        key = args.key or key_from_html(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html"))
        try:
            prices = fetch_finnhub(key)
        except (urllib.error.URLError, ValueError, urllib.error.HTTPError) as e:
            print(f"ERROR fetching prices: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        ap.error("provide --key or --live for live prices, --prices FILE for pre-fetched quotes, or --mock for the offline self-test")

    snapshot = compute(prices, args.dividends)
    if QUOTE_DATES:
        snapshot["quote_dates"] = QUOTE_DATES
    out = json.dumps(snapshot, indent=2)
    print(out)
    if args.json:
        with open(args.json, "w") as f:
            f.write(out)


if __name__ == "__main__":
    main()
