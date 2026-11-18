# Phase 3 Portfolio: Weekly Review Log

**Portfolio opened:** November 18, 2026 (fills about 10:04 AM CT)
**Total invested:** $500.00
**Structure:** 5 equal-weight positions ($100 each), buy-and-hold
**Experiment duration:** 6 months minimum (3-month review February 18, 2027; 6-month review May 18, 2027)
**Primary benchmark:** SPY baseline $730.13 (recorded at fill time). **Diagnostic benchmarks:** one sector ETF per position, locked at entry.
**Runs alongside Phase 2**, which keeps its own log (`Phase_2_Weekly_Review_Log.md`).

> This is an append-only log. One entry per weekly check-in. Corrections go in the current week's entry with a note, never as edits to an earlier one.

---

## Baseline and Rules

**The hypothesis.** Stocks chosen for company-specific earnings drivers, with no two sharing a main price driver and no single name dominating risk, can outperform SPY over 6 to 12 months, and will beat their own sector benchmarks more often than not.

- **Goal (portfolio level):** total return beats SPY over the evaluation period.
- **Diagnostic (position level):** at least 3 of 5 positions beat their locked sector benchmark, and each result can be explained by the company's own numbers.
- **Failure:** the portfolio trails SPY, or the result is explained by a shared factor (see "Known tilt") rather than by company results. If so, the honest conclusion is that company-specific picking adds nothing over indexing at this account size.
- **Who picked:** Claude, at Jake's choice. The result scores the selection method, not Jake's own picking.

**Lessons this phase was built on (from Phase 2).**
1. Equal dollars are not equal risk. In Phase 2, MU was 20% of the dollars and about 75% of the daily risk.
2. Labels hide shared drivers. CEG was labeled Energy but traded partly on AI sentiment (0.45 correlation with semiconductors before purchase).
3. Company-specific earnings drivers beat macro-sentiment names. LLY, LMT and MA beat their sectors; MU and CEG lagged.

**Pre-purchase risk check** (daily closes, March 2 to September 8, 2026; window misses the October AI selloff; no SPY daily data was available):

| | PGR | TJX | ISRG | NFLX | MSFT |
|---|---|---|---|---|---|
| Annualized volatility | 29% | 23% | 40% | 34% | 37% |
| Share of portfolio risk at $100 each | 12% | 11% | 30% | 24% | 24% |
| Correlation with SMH | -0.49 | -0.19 | -0.08 | -0.26 | 0.01 |

Average pairwise correlation 0.16 (Phase 2: -0.05). Volatility rule (half position above 2x the median): not triggered; ISRG is 1.4x.

**Known tilt.** The book leans against the AI trade: equal-weight correlation with SMH of -0.32. MSFT replaced WM to cut that from -0.47. If AI stocks rally hard, the book will likely trail SPY for factor reasons. Read the SPY result alongside the sector count before concluding anything about stock-picking.

**Entry note.** TJX was bought on its Q3 report day (November 18), after a rise, against Lesson 4 ("Check the earnings calendar before entry"). Recorded so the next entry checks the calendar first.

**Reporting rules for this phase.**
- Every weekly entry reports the SPY comparison and the sector scorecard, and says which one explains the week.
- Quarterly reviews report each position's share of portfolio risk and the book's correlation with SMH, from daily closes.
- Thesis-break criteria are in `thesis-criteria.md` (Phase 3 section). Status changes come from company facts only.

**Decision audit (passed on).** WM (most anti-AI name, redundant with PGR), ORLY (shares the auto-repair-cost driver with PGR; first alternate), COST (forward P/E about 46), BKNG (Q4 guide cut on Middle East disruption), VRTX (binary FDA date November 30, shrinking core franchise), GOOGL (search and YouTube missed, negative free cash flow; more moving parts than MSFT), chip and AI-power names (excluded by design).

---

## Holdings Reference

| Ticker | Company | Price driver | Shares | Entry Price | Cost Basis | Sector ETF |
|--------|---------|--------------|--------|-------------|------------|------------|
| PGR | Progressive | Auto insurance pricing vs. claims | 0.44135 | $226.58 | $100.00 | KIE |
| TJX | TJX Companies | Off-price retail, trade-down | 0.69834 | $143.20 | $100.00 | XRT |
| ISRG | Intuitive Surgical | Surgical procedure volumes | 0.23485 | $425.80 | $100.00 | IHI |
| NFLX | Netflix | Subscriptions, pricing, ads | 1.67538 | $59.69 | $100.00 | XLC |
| MSFT | Microsoft | Azure cloud growth | 0.19805 | $504.90 | $100.00 | IGV |

---

## Benchmark Baselines

| Benchmark | Role | Baseline | Source |
|-----------|------|----------|--------|
| SPY | Primary | $730.13 | Recorded by Jake at fill time, November 18 |
| KIE | PGR sector | Pending | November 18 close |
| XRT | TJX sector | Pending | November 18 close |
| IHI | ISRG sector | Pending | November 18 close |
| XLC | NFLX sector | Pending | November 18 close |
| IGV | MSFT sector | Pending | November 18 close |

*Sector baselines use the November 18 close because intraday ETF prices at the fill time were not captured. When recorded, the same values go in `tools/fetch_prices.py` (`PHASES[3]["sector_base"]`) and `phase3.html` (`SECTOR_BASE`).*

---

## Cumulative Performance Tracker

*Updated each week. All % changes measured from the November 18, 2026 fills.*

| Week | Date | Portfolio Value | Price % | Cum. Div. | Total Return % | SPY % | vs. SPY |
|------|------|----------------|---------|-----------|----------------|-------|---------|

---

## Position Performance by Week

| Week | Date | PGR | TJX | ISRG | NFLX | MSFT |
|------|------|-----|-----|------|------|------|

---

## Sector Scorecard by Week

*Each cell is the position's return minus its sector ETF's return since November 18, in percentage points. "Beaten" counts positions ahead of their sector.*

| Week | Date | PGR vs KIE | TJX vs XRT | ISRG vs IHI | NFLX vs XLC | MSFT vs IGV | Beaten |
|------|------|------------|------------|-------------|-------------|-------------|--------|

---

## Dividend Ledger

*Append-only. A dividend counts when the ex-dividend date falls on or after entry (November 18, 2026) and the position is held.*

| Ex-Div Date | Ticker | $/Share | Shares | Dividend Earned | Status |
|-------------|--------|---------|--------|-----------------|--------|
| **Total to date** | | | | **$0.00** | |

**Upcoming / expected** (confirm dates and amounts before booking):
- TJX, MSFT and PGR pay quarterly dividends; PGR also pays an annual variable dividend, usually declared in December. ISRG and NFLX pay none.

---

## Weekly Entries

---

## Quarterly Reviews

- **3-Month Review:** February 18, 2027 (written on the first run with a close on or after that date)
- **6-Month Review:** May 18, 2027

---

## Concepts Learned Index

| Week | Concept | One-Line Summary |
|------|---------|-----------------|

---

## Earnings Calendar (Phase 3)

| Company | Expected Report | Status |
|---------|----------------|--------|
| PGR | Monthly results mid-month; Q4 around January 27, 2027 | Q3 reported November 5, 2026: EPS $4.37 vs $4.42 expected, net premiums written +4%. |
| NFLX | Mid-to-late January 2027 (Q4) | Q3 reported October 20, 2026: EPS $0.87 vs $0.82, revenue $12.87B in line, 2026 ad outlook cut to $2.7B. |
| MSFT | Late January 2027 (FY Q2) | FY Q1 reported October 28, 2026: revenue $92.3B (+19%), Azure +48%, EPS $4.89 vs $4.72. |
| ISRG | Around January 28, 2027 (Q4) | Q3 reported October 20, 2026: procedures +15%, adjusted EPS $3.00 vs $2.65. |
| TJX | Late February 2027 (Q4 FY27) | Q3 FY27 reported November 18, 2026 (entry day): comps +4%, above plan. |
