#!/usr/bin/env python3
"""
fetch_prices.py: weekly price and return snapshot for Phase 2 and Phase 3

Pulls Friday-close prices for each phase's tickers from Finnhub and computes
every number the weekly review needs, using the EXACT same math as the
dashboards (index.html and phase3.html compute()). The point: the log, the dashboard, and the
standalone review all agree because they come from one place.

Usage:
  python fetch_prices.py --key YOUR_FINNHUB_KEY            # live
  python fetch_prices.py --prices quotes.json              # pre-fetched prices (sandboxed envs)
  python fetch_prices.py --mock                            # offline self-test (W6 fallback)
  python fetch_prices.py --key KEY --dividends 1.00 --json out.json
  python fetch_prices.py --phase 3 --live --dividends 0 --json p3.json   # Phase 3

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

# ---- Static experiment config (mirrors the dashboards' POS / entries) ----
# Phase 2 lives in index.html; Phase 3 lives in phase3.html. Keep both in sync.
PHASES = {
    2: {
        "positions": [
            {"t": "MU",  "theme": "AI / Semi, memory",            "shares": 0.12617, "entry": 792.53},
            {"t": "LLY", "theme": "Healthcare / GLP-1",           "shares": 0.10583, "entry": 944.90},
            {"t": "CEG", "theme": "Energy / AI power (nuclear)",  "shares": 0.31744, "entry": 315.02},
            {"t": "LMT", "theme": "Defense / quality value",      "shares": 0.19849, "entry": 503.78},
            {"t": "MA",  "theme": "Fintech / payments",           "shares": 0.20202, "entry": 495.00},
        ],
        "benchmarks": {"SPY": 739.30, "QQQ": 713.29},
        "sectors": {},
        "total_invested": 499.99,
        "entry_date": "May 11, 2026",
        # Offline self-test = the W6 (June 19) fallback; with dividends=1.00 it
        # should reproduce the logged W6 total return of +10.00%.
        "mock": {"MU": 1151.80, "LLY": 1098.78, "CEG": 274.06, "LMT": 511.05,
                 "MA": 489.79, "SPY": 746.93, "QQQ": 740.62},
    },
    3: {
        "positions": [
            {"t": "PGR",  "theme": "Auto insurance pricing vs. claims",  "shares": 0.44135, "entry": 226.58},
            {"t": "TJX",  "theme": "Off-price retail, trade-down",       "shares": 0.69834, "entry": 143.20},
            {"t": "ISRG", "theme": "Surgical procedure volumes",         "shares": 0.23485, "entry": 425.80},
            {"t": "NFLX", "theme": "Subscriptions, pricing, ads",        "shares": 1.67538, "entry": 59.69},
            {"t": "MSFT", "theme": "Azure cloud growth",                 "shares": 0.19805, "entry": 504.90},
        ],
        "benchmarks": {"SPY": 730.13},
        # Sector benchmark per position, locked at entry. Baselines are the
        # November 18, 2026 closes. None = not yet recorded (see WEEKLY_UPDATE.md).
        "sectors": {"PGR": "KIE", "TJX": "XRT", "ISRG": "IHI", "NFLX": "XLC", "MSFT": "IGV"},
        "sector_base": {"KIE": 64.74, "XRT": 90.30, "IHI": 56.89, "XLC": 105.58, "IGV": 96.94},
        "total_invested": 500.00,
        "entry_date": "November 18, 2026",
        # Offline self-test = entry prices; total return should be +0.00%.
        "mock": {"PGR": 226.58, "TJX": 143.20, "ISRG": 425.80, "NFLX": 59.69,
                 "MSFT": 504.90, "SPY": 730.13},
    },
}

# Back-compat names (Phase 2), used by older callers.
POSITIONS = PHASES[2]["positions"]
SPY_ENTRY = PHASES[2]["benchmarks"]["SPY"]
QQQ_ENTRY = PHASES[2]["benchmarks"]["QQQ"]
TOTAL_INVESTED = PHASES[2]["total_invested"]
ENTRY_DATE = PHASES[2]["entry_date"]
MOCK_PRICES = PHASES[2]["mock"]


def symbols(phase, include_sectors=True):
    cfg = PHASES[phase]
    syms = [p["t"] for p in cfg["positions"]] + list(cfg["benchmarks"])
    if include_sectors:
        syms += list(cfg.get("sector_base", {}))
    return syms


def required_symbols(phase):
    """Symbols that must have a price. Sector ETFs are required once their baseline is set."""
    cfg = PHASES[phase]
    req = [p["t"] for p in cfg["positions"]] + list(cfg["benchmarks"])
    req += [s for s, b in cfg.get("sector_base", {}).items() if b]
    return req


FINNHUB_QUOTE = "https://finnhub.io/api/v1/quote?symbol={sym}&token={key}"


QUOTE_DATES = {}  # ticker -> UTC date of the quote, filled by fetch_finnhub


def key_from_html(path):
    """Read the FINNHUB_KEY constant from the dashboard so the key lives in one place."""
    with open(path, encoding="utf-8") as f:
        m = re.search(r'const FINNHUB_KEY\s*=\s*"([^"]+)"', f.read())
    if not m:
        raise SystemExit(f"ERROR: no FINNHUB_KEY found in {path}")
    return m.group(1)


def fetch_finnhub(key, syms):
    """Return {ticker: last_price} from Finnhub /quote (.c field) for the given symbols."""
    prices = {}
    for sym in syms:
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


def compute(prices, cum_dividends, phase=2):
    """Same logic as the dashboards' compute(). Returns a structured snapshot."""
    cfg = PHASES[phase]
    invested = cfg["total_invested"]
    rows = []
    value = 0.0
    sectors_scored = sectors_beaten = 0
    for p in cfg["positions"]:
        px = prices[p["t"]]
        ret = (px / p["entry"] - 1) * 100
        val = px * p["shares"]
        value += val
        row = {
            "ticker": p["t"], "theme": p["theme"], "shares": p["shares"],
            "entry": p["entry"], "price": round(px, 2),
            "return_pct": round(ret, 2), "value": round(val, 2),
        }
        etf = cfg["sectors"].get(p["t"])
        if etf:
            base = cfg["sector_base"].get(etf)
            row["sector"] = etf
            if base and etf in prices:
                sret = (prices[etf] / base - 1) * 100
                row["sector_price"] = round(prices[etf], 2)
                row["sector_return_pct"] = round(sret, 2)
                row["vs_sector_pp"] = round(ret - sret, 2)
                sectors_scored += 1
                sectors_beaten += ret > sret
            else:
                row["sector_return_pct"] = None
                row["vs_sector_pp"] = None
        rows.append(row)
    price_val = value
    total_val = value + cum_dividends
    price_ret = (price_val / invested - 1) * 100
    total_ret = (total_val / invested - 1) * 100
    snap = {
        "phase": phase,
        "entry_date": cfg["entry_date"],
        "total_invested": invested,
        "cum_dividends": round(cum_dividends, 2),
        "positions": rows,
        "price_value": round(price_val, 2),          # price-only sum = log's "Portfolio Value" column
        "portfolio_value": round(total_val, 2),       # price + dividends = dashboard's value tile
        "price_return_pct": round(price_ret, 2),
        "total_return_pct": round(total_ret, 2),
        "pl_dollars": round(total_val - invested, 2),
        "benchmarks": {},
    }
    for b, entry in cfg["benchmarks"].items():
        bret = (prices[b] / entry - 1) * 100
        snap["benchmarks"][b] = {"price": round(prices[b], 2), "return_pct": round(bret, 2)}
        snap[f"vs_{b.lower()}_pp"] = round(total_ret - bret, 2)
    if cfg["sectors"]:
        snap["sectors_scored"] = sectors_scored
        snap["sectors_beaten"] = sectors_beaten
    return snap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", type=int, choices=sorted(PHASES), default=2,
                    help="which experiment to snapshot (default 2)")
    ap.add_argument("--key", help="Finnhub API key (live mode)")
    ap.add_argument("--live", action="store_true",
                    help="live mode, reading the key from FINNHUB_KEY in ../index.html")
    ap.add_argument("--prices", help="path to a JSON file of {ticker: close_price} for every symbol of the phase "
                                     "(use when this environment can't reach Finnhub directly: fetch the "
                                     "quotes via another tool, save them, and let this script do the math)")
    ap.add_argument("--mock", action="store_true", help="offline self-test with the phase's mock prices")
    ap.add_argument("--dividends", type=float, default=None,
                    help="cumulative dividends earned to date (from the phase's Dividend Ledger)")
    ap.add_argument("--json", help="also write the snapshot to this file path")
    args = ap.parse_args()
    phase = args.phase
    if args.dividends is None:
        args.dividends = 1.00 if (args.mock and phase == 2) else 0.0

    if args.mock:
        prices = PHASES[phase]["mock"]
    elif args.prices:
        with open(args.prices) as f:
            prices = {k: float(v) for k, v in json.load(f).items()}
        expected = set(required_symbols(phase))
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
            prices = fetch_finnhub(key, symbols(phase))
        except (urllib.error.URLError, ValueError, urllib.error.HTTPError) as e:
            print(f"ERROR fetching prices: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        ap.error("provide --key or --live for live prices, --prices FILE for pre-fetched quotes, or --mock for the offline self-test")

    snapshot = compute(prices, args.dividends, phase)
    if QUOTE_DATES:
        snapshot["quote_dates"] = QUOTE_DATES
    out = json.dumps(snapshot, indent=2)
    print(out)
    if args.json:
        with open(args.json, "w") as f:
            f.write(out)


if __name__ == "__main__":
    main()
