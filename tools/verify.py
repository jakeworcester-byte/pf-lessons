#!/usr/bin/env python3
"""
verify.py  -  the publish gate for the weekly update (Phase 2 and Phase 3)

For each phase, checks that its dashboard and its log describe the same week with
the same numbers, using the same math as the dashboards:

  Phase 2: index.html   <->  Phase_2_Weekly_Review_Log.md
  Phase 3: phase3.html  <->  Phase_3_Weekly_Review_Log.md

Run from anywhere; exits 1 with a list of failures if anything disagrees.

Usage:
  python tools/verify.py            # full check
  python tools/verify.py --no-git   # skip the em-dash check on uncommitted additions
"""

import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_prices import compute, PHASES, required_symbols  # noqa: E402  (same math as the dashboards)

TOL = 0.015  # percentage points; values are logged to 2 decimals
EM_DASH = "\u2014"
failures = []

PAGES = {
    2: {"html": "index.html", "log": "Phase_2_Weekly_Review_Log.md"},
    3: {"html": "phase3.html", "log": "Phase_3_Weekly_Review_Log.md"},
}


def fail(msg):
    failures.append(msg)


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


def js_const(html, name, where):
    m = re.search(r"const %s\s*=\s*(.+?);\s*\n" % name, html, re.S)
    if not m:
        fail(f"{where}: const {name} not found")
        return None
    return m.group(1)


def js_to_json(html, name, default, where):
    # {MU:1074.89, ...} or {port:[...], ...} -> JSON, tolerating trailing commas
    src = js_const(html, name, where)
    if src is None:
        return default
    src = re.sub(r"([{,]\s*)([A-Za-z_]\w*)\s*:", r'\1"\2":', src)
    src = re.sub(r",\s*([}\]])", r"\1", src)
    try:
        return json.loads(src)
    except json.JSONDecodeError as e:
        fail(f"{where}: could not parse {name}: {e}")
        return default


def pct(s):
    return float(s.replace("%", "").replace("pp", "").replace("+", "").replace("*", "").strip())


def table_row(log, section_title, week_label, where):
    sec = log.split(section_title, 1)
    if len(sec) < 2:
        fail(f"{where}: section '{section_title}' not found")
        return None
    for line in sec[1].split("\n## ", 1)[0].splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == week_label:
            return cells
    fail(f"{where}: no {week_label} row in '{section_title}'")
    return None


def verify_phase(phase):
    cfg = PHASES[phase]
    page, logname = PAGES[phase]["html"], PAGES[phase]["log"]
    tickers = [p["t"] for p in cfg["positions"]]
    bench = list(cfg["benchmarks"])
    html = read(page)

    # ---------------- dashboard ----------------
    fallback = js_to_json(html, "FALLBACK", {}, page)
    cum_div = float(js_const(html, "CUM_DIVIDENDS", page) or 0)
    weeks = js_to_json(html, "WEEKS", [], page)
    wk_dates = js_to_json(html, "WK_DATES", [], page)
    hist = js_to_json(html, "HIST", {}, page)
    published = js_to_json(html, "PUBLISHED", "", page)

    n = int(weeks[-1][1:]) if weeks else -1
    label = f"W{n}"
    hist_keys = ["port"] + [b.lower() for b in bench]
    for k in hist_keys:
        if len(hist.get(k, [])) != len(weeks):
            fail(f"{page}: HIST.{k} has {len(hist.get(k, []))} points, WEEKS has {len(weeks)}")
    if len(wk_dates) != len(weeks):
        fail(f"{page}: WK_DATES has {len(wk_dates)} entries, WEEKS has {len(weeks)}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", published or ""):
        fail(f"{page}: PUBLISHED must be a YYYY-MM-DD date")

    # every "W<number>, <Month>" label in the page text must be the current week
    stale_labels = sorted({m for m in re.findall(r"\b(W\d+),\s+[A-Z][a-z]{2}", html) if m != label})
    if stale_labels:
        fail(f"{page}: stale week labels still present: {stale_labels} (current is {label})")

    thesis = re.findall(r'\{t:"(\w+)",\s*s:"(\w+)"', js_const(html, "THESIS", page) or "")
    if sorted(t for t, _ in thesis) != sorted(tickers):
        fail(f"{page}: THESIS must have one row per position, found {[t for t, _ in thesis]}")
    for t, s in thesis:
        if s not in ("Intact", "Pressured", "Broken"):
            fail(f"{page}: THESIS {t} has invalid status {s!r}")

    # Phase 3: the page's sector baselines must match the script's
    if cfg.get("sector_base"):
        page_base = js_to_json(html, "SECTOR_BASE", {}, page)
        for etf, base in cfg["sector_base"].items():
            if page_base.get(etf) != base:
                fail(f"{page}: SECTOR_BASE.{etf} is {page_base.get(etf)}, tools/fetch_prices.py has {base}")

    need = set(required_symbols(phase))
    missing = need - set(fallback)
    snap = compute(fallback, cum_div, phase) if not missing else None
    if not snap:
        fail(f"{page}: FALLBACK is missing {sorted(missing)}")
    else:
        pairs = [("port", snap["total_return_pct"])] + \
                [(b.lower(), snap["benchmarks"][b]["return_pct"]) for b in bench]
        for k, v in pairs:
            if hist.get(k) and abs(hist[k][-1] - v) > TOL:
                fail(f"{page}: HIST.{k} last point {hist[k][-1]} != {v} computed from FALLBACK")

    # ---------------- log ----------------
    log = read(logname)
    headings = re.findall(r"^### Week (\d+)\b", log, re.M)
    latest = int(headings[-1]) if headings else 0   # W0 = baseline, no weekly entry yet
    if latest != n:
        fail(f"{logname}: latest '### Week' heading is {headings[-1] if headings else 'none (W0)'}, "
             f"{page} is {label}")

    if n > 0 and snap:
        cum = table_row(log, "## Cumulative Performance Tracker", label, logname)
        if cum:
            # Phase 2: Week | Date | Value | Price % | Cum Div | Total % | SPY % | QQQ % | vs SPY | vs QQQ
            # Phase 3: Week | Date | Value | Price % | Cum Div | Total % | SPY % | vs SPY
            checks = [("Price %", cum[3], snap["price_return_pct"]),
                      ("Total Return %", cum[5], snap["total_return_pct"])]
            for i, b in enumerate(bench):
                checks.append((f"{b} %", cum[6 + i], snap["benchmarks"][b]["return_pct"]))
            for i, b in enumerate(bench):
                checks.append((f"vs. {b}", cum[6 + len(bench) + i], snap[f"vs_{b.lower()}_pp"]))
            for name, logged, computed in checks:
                if abs(pct(logged) - computed) > TOL:
                    fail(f"{logname}: {label} {name} is {logged}, dashboard math gives {computed}")
            if abs(pct(cum[2].replace("$", "").replace(",", "")) - snap["price_value"]) > 0.015:
                fail(f"{logname}: {label} Portfolio Value {cum[2]} != {snap['price_value']}")
            if abs(pct(cum[4].replace("$", "").replace("†", "")) - round(cum_div, 2)) > 0.015:
                fail(f"{logname}: {label} Cum. Div. {cum[4]} != CUM_DIVIDENDS {cum_div:.2f}")

        pos = table_row(log, "## Position Performance by Week", label, logname)
        if pos:
            for i, row in enumerate(snap["positions"]):
                if abs(pct(pos[2 + i]) - row["return_pct"]) > TOL:
                    fail(f"{logname}: {label} {row['ticker']} is {pos[2 + i]}, dashboard math gives {row['return_pct']}")

        if cfg.get("sectors"):
            sec = table_row(log, "## Sector Scorecard by Week", label, logname)
            if sec:
                for i, row in enumerate(snap["positions"]):
                    cell = sec[2 + i]
                    if row.get("vs_sector_pp") is None:
                        if not cell.lower().startswith("pending"):
                            fail(f"{logname}: {label} {row['ticker']} sector cell is {cell!r}, baseline not set (write 'pending')")
                    elif cell.lower().startswith("pending") or abs(pct(cell) - row["vs_sector_pp"]) > TOL:
                        fail(f"{logname}: {label} {row['ticker']} vs {row['sector']} is {cell}, dashboard math gives {row['vs_sector_pp']}")
                beaten = sec[2 + len(tickers)]
                want = f"{snap['sectors_beaten']} of {snap['sectors_scored']}" if snap["sectors_scored"] else "pending"
                if beaten.lower() != want.lower():
                    fail(f"{logname}: {label} Beaten is {beaten!r}, dashboard math gives {want!r}")

    # ---------------- dashboard script parses ----------------
    script = re.search(r"<script>\s*(.*?)</script>", html, re.S)
    tmp = os.path.join(ROOT, ".verify_tmp.js")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(script.group(1) if script else "")
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        if r.returncode != 0:
            fail(f"{page}: inline script does not parse:\n" + r.stderr[-500:])
    except FileNotFoundError:
        print("note: node not installed, skipped the script syntax check")
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

    return label, (wk_dates[-1] if wk_dates else "?"), snap, published


results = {p: verify_phase(p) for p in PAGES}

# ---------------- no em dashes in anything added this run ----------------
if "--no-git" not in sys.argv:
    try:
        diff = subprocess.run(["git", "diff", "HEAD", "-U0", "--", "."], cwd=ROOT,
                              capture_output=True, text=True, encoding="utf-8", check=True).stdout
        untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT,
                                   capture_output=True, text=True, encoding="utf-8", check=True).stdout.split()
        added = [l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]
        for name in untracked:
            try:
                added += read(name).splitlines()
            except (OSError, UnicodeDecodeError):
                pass
        bad = [l[:90] for l in added if EM_DASH in l]
        if bad:
            fail("em dashes in new or changed lines:\n    " + "\n    ".join(bad[:10]))
    except (OSError, subprocess.CalledProcessError) as e:
        fail(f"could not run git diff for the em-dash check: {e}")

if failures:
    print(f"VERIFY FAILED ({len(failures)}):")
    for f_ in failures:
        print(" - " + f_)
    sys.exit(1)

for phase, (label, date, snap, published) in results.items():
    spreads = ", ".join(f"vs {b} {snap[f'vs_{b.lower()}_pp']:+.2f}pp" for b in PHASES[phase]["benchmarks"])
    extra = ""
    if PHASES[phase].get("sectors"):
        extra = (f", sectors beaten {snap['sectors_beaten']} of {snap['sectors_scored']}"
                 if snap["sectors_scored"] else ", sector baselines pending")
    print(f"VERIFY OK: Phase {phase} {label} ({date}), total return {snap['total_return_pct']:+.2f}%, "
          f"{spreads}{extra}, published {published}")
