#!/usr/bin/env python3
"""
verify.py  -  the publish gate for the weekly update

Checks that the dashboard (index.html) and the log (Phase_2_Weekly_Review_Log.md)
describe the same week with the same numbers, using the same math as the dashboard.
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
from fetch_prices import compute  # noqa: E402  (same math as the dashboard)

TOL = 0.015  # percentage points; values are logged to 2 decimals
EM_DASH = "\u2014"
failures = []


def fail(msg):
    failures.append(msg)


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


def js_const(html, name):
    m = re.search(r"const %s\s*=\s*(.+?);\s*\n" % name, html, re.S)
    if not m:
        fail(f"index.html: const {name} not found")
        return None
    return m.group(1)


def js_to_json(name, default):
    # {MU:1074.89, ...} or {port:[...], ...} -> JSON, tolerating trailing commas
    src = js_const(html, name)
    if src is None:
        return default
    src = re.sub(r"([{,]\s*)([A-Za-z_]\w*)\s*:", r'\1"\2":', src)
    src = re.sub(r",\s*([}\]])", r"\1", src)
    try:
        return json.loads(src)
    except json.JSONDecodeError as e:
        fail(f"index.html: could not parse {name}: {e}")
        return default


def pct(s):
    return float(s.replace("%", "").replace("pp", "").replace("+", "").replace("*", "").strip())


# ---------------- dashboard ----------------
html = read("index.html")
fallback = js_to_json("FALLBACK", {})
cum_div = float(js_const(html, "CUM_DIVIDENDS") or 0)
weeks = js_to_json("WEEKS", [])
wk_dates = js_to_json("WK_DATES", [])
hist = js_to_json("HIST", {})
published = js_to_json("PUBLISHED", "")

n = int(weeks[-1][1:]) if weeks else -1
label = f"W{n}"
for k in ("port", "spy", "qqq"):
    if len(hist.get(k, [])) != len(weeks):
        fail(f"index.html: HIST.{k} has {len(hist.get(k, []))} points, WEEKS has {len(weeks)}")
if len(wk_dates) != len(weeks):
    fail(f"index.html: WK_DATES has {len(wk_dates)} entries, WEEKS has {len(weeks)}")
if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", published or ""):
    fail("index.html: PUBLISHED must be a YYYY-MM-DD date")

# every "W<number>, <Month>" label in the page text must be the current week
stale_labels = sorted({m for m in re.findall(r"\b(W\d+),\s+[A-Z][a-z]{2}", html) if m != label})
if stale_labels:
    fail(f"index.html: stale week labels still present: {stale_labels} (current is {label})")

thesis = re.findall(r'\{t:"(\w+)",\s*s:"(\w+)"', js_const(html, "THESIS") or "")
if sorted(t for t, _ in thesis) != sorted(["MU", "LLY", "CEG", "LMT", "MA"]):
    fail(f"index.html: THESIS must have one row per position, found {[t for t, _ in thesis]}")
for t, s in thesis:
    if s not in ("Intact", "Pressured", "Broken"):
        fail(f"index.html: THESIS {t} has invalid status {s!r}")

snap = compute(fallback, cum_div) if len(fallback) == 7 else None
if not snap:
    fail("index.html: FALLBACK must have all 7 symbols")
else:
    for k, v in (("port", snap["total_return_pct"]),
                 ("spy", snap["benchmarks"]["SPY"]["return_pct"]),
                 ("qqq", snap["benchmarks"]["QQQ"]["return_pct"])):
        if hist.get(k) and abs(hist[k][-1] - v) > TOL:
            fail(f"index.html: HIST.{k} last point {hist[k][-1]} != {v} computed from FALLBACK")

# ---------------- log ----------------
log = read("Phase_2_Weekly_Review_Log.md")
headings = re.findall(r"^### Week (\d+)\b", log, re.M)
if not headings or int(headings[-1]) != n:
    fail(f"log: latest '### Week' heading is {headings[-1] if headings else None}, dashboard is {label}")


def table_row(section_title, week_label):
    sec = log.split(section_title, 1)
    if len(sec) < 2:
        fail(f"log: section '{section_title}' not found")
        return None
    for line in sec[1].split("\n## ", 1)[0].splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == week_label:
            return cells
    fail(f"log: no {week_label} row in '{section_title}'")
    return None


cum = table_row("## Cumulative Performance Tracker", label)
if cum and snap:
    # Week | Date | Value | Price % | Cum Div | Total % | SPY % | QQQ % | vs SPY | vs QQQ
    checks = [("Price %", cum[3], snap["price_return_pct"]),
              ("Total Return %", cum[5], snap["total_return_pct"]),
              ("SPY %", cum[6], snap["benchmarks"]["SPY"]["return_pct"]),
              ("QQQ %", cum[7], snap["benchmarks"]["QQQ"]["return_pct"]),
              ("vs. SPY", cum[8], snap["vs_spy_pp"]),
              ("vs. QQQ", cum[9], snap["vs_qqq_pp"])]
    for name, logged, computed in checks:
        if abs(pct(logged) - computed) > TOL:
            fail(f"log: {label} {name} is {logged}, dashboard math gives {computed}")
    if abs(pct(cum[2].replace("$", "").replace(",", "")) - snap["price_value"]) > 0.015:
        fail(f"log: {label} Portfolio Value {cum[2]} != {snap['price_value']}")
    if abs(pct(cum[4].replace("$", "").replace("†", "")) - round(cum_div, 2)) > 0.015:
        fail(f"log: {label} Cum. Div. {cum[4]} != CUM_DIVIDENDS {cum_div:.2f}")

pos = table_row("## Position Performance by Week", label)
if pos and snap:
    for i, row in enumerate(snap["positions"]):
        if abs(pct(pos[2 + i]) - row["return_pct"]) > TOL:
            fail(f"log: {label} {row['ticker']} is {pos[2 + i]}, dashboard math gives {row['return_pct']}")

# ---------------- no em dashes in anything added this run ----------------
if "--no-git" not in sys.argv:
    try:
        diff = subprocess.run(["git", "diff", "HEAD", "-U0", "--", "."], cwd=ROOT,
                              capture_output=True, text=True, encoding="utf-8", check=True).stdout
        added = [l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]
        bad = [l[:90] for l in added if EM_DASH in l]
        if bad:
            fail("em dashes in new or changed lines:\n    " + "\n    ".join(bad[:10]))
    except (OSError, subprocess.CalledProcessError) as e:
        fail(f"could not run git diff for the em-dash check: {e}")

# ---------------- dashboard script parses ----------------
script = re.search(r"<script>\s*(.*?)</script>", html, re.S)
try:
    tmp = os.path.join(ROOT, ".verify_tmp.js")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(script.group(1) if script else "")
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    if r.returncode != 0:
        fail("index.html: inline script does not parse:\n" + r.stderr[-500:])
except FileNotFoundError:
    print("note: node not installed, skipped the script syntax check")
finally:
    if os.path.exists(tmp):
        os.remove(tmp)

if failures:
    print(f"VERIFY FAILED ({len(failures)}):")
    for f_ in failures:
        print(" - " + f_)
    sys.exit(1)
print(f"VERIFY OK: {label} ({wk_dates[-1]}), total return {snap['total_return_pct']:+.2f}%, "
      f"vs SPY {snap['vs_spy_pp']:+.2f}pp, vs QQQ {snap['vs_qqq_pp']:+.2f}pp, published {published}")
