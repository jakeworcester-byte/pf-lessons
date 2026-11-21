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
| KIE | PGR sector | $64.74 | November 18 close, stockanalysis.com, confirmed by Yahoo Finance (recorded in the Week 1 run) |
| XRT | TJX sector | $90.30 | November 18 close, stockanalysis.com, confirmed by Yahoo Finance (recorded in the Week 1 run) |
| IHI | ISRG sector | $56.89 | November 18 close, stockanalysis.com, confirmed by Yahoo Finance (recorded in the Week 1 run) |
| XLC | NFLX sector | $105.58 | November 18 close, stockanalysis.com, confirmed by Yahoo Finance (recorded in the Week 1 run) |
| IGV | MSFT sector | $96.94 | November 18 close, stockanalysis.com, confirmed by Yahoo Finance (recorded in the Week 1 run) |

*Sector baselines use the November 18 close because intraday ETF prices at the fill time were not captured. When recorded, the same values go in `tools/fetch_prices.py` (`PHASES[3]["sector_base"]`) and `phase3.html` (`SECTOR_BASE`).*

---

## Cumulative Performance Tracker

*Updated each week. All % changes measured from the November 18, 2026 fills.*

| Week | Date | Portfolio Value | Price % | Cum. Div. | Total Return % | SPY % | vs. SPY |
|------|------|----------------|---------|-----------|----------------|-------|---------|
| W1 | November 20, 2026 | $484.35 | -3.13% | $0.19 | -3.09% | -5.52% | +2.43pp |

---

## Position Performance by Week

| Week | Date | PGR | TJX | ISRG | NFLX | MSFT |
|------|------|-----|-----|------|------|------|
| W1 | November 20, 2026 | +2.12% | -2.50% | -6.28% | -4.96% | -4.04% |

---

## Sector Scorecard by Week

*Each cell is the position's return minus its sector ETF's return since November 18, in percentage points. "Beaten" counts positions ahead of their sector.*

| Week | Date | PGR vs KIE | TJX vs XRT | ISRG vs IHI | NFLX vs XLC | MSFT vs IGV | Beaten |
|------|------|------------|------------|-------------|-------------|-------------|--------|
| W1 | November 20, 2026 | +3.16pp | +1.72pp | -3.63pp | +0.30pp | +1.41pp | 4 of 5 |

---

## Dividend Ledger

*Append-only. A dividend counts when the ex-dividend date falls on or after entry (November 18, 2026) and the position is held.*

| Ex-Div Date | Ticker | $/Share | Shares | Dividend Earned | Status |
|-------------|--------|---------|--------|-----------------|--------|
| November 19, 2026 | MSFT | $0.98 | 0.19805 | $0.19 | Earned (bought November 18, held through ex-date). first Phase 3 dividend |
| **Total to date** | | | | **$0.19** | |

**Upcoming / expected** (confirm dates and amounts before booking):
- TJX, MSFT and PGR pay quarterly dividends; PGR also pays an annual variable dividend, usually declared in December. ISRG and NFLX pay none.
- MSFT: **Nov 19, 2026 ex-div earned** ($0.98, record Nov 19, pay Dec 10, per stockanalysis.com and Microsoft's September 15 release), added in W1: +$0.1941, cumulative $0.00 to $0.1941. Next quarterly ex-div ~Feb 2027.
- TJX: last ex-div was November 12, 2026 ($0.48), before entry, so not earned. Next ~Feb 2027.
- PGR: last quarterly ex-div October 1, 2026 ($0.10); next quarterly ~early January 2027. Watch for the annual variable dividend declaration in December.

---

## Weekly Entries

### Week 1: November 20, 2026

*Portfolio is 2 days old (fills November 18 at about 10:04 AM CT, then two full sessions). All prices are Finnhub quotes stamped November 20, 2026, on all eleven symbols, and match the stockanalysis.com closes to the cent. Sector ETF baselines were recorded this run: November 18 closes from stockanalysis.com, each confirmed against Yahoo Finance.*

#### Prices Used

| Ticker | Entry Price | Current Price | Current Value | Price P&L | Dividend | Total P&L | Total Return % | Sector ETF % | vs. Sector |
|--------|-------------|---------------|---------------|-----------|----------|-----------|----------------|--------------|------------|
| PGR | $226.58 | $231.39 | $102.12 | +$2.12 | +$0.00 | +$2.12 | +2.12% | KIE -1.03% | +3.16pp |
| TJX | $143.20 | $139.62 | $97.50 | -$2.50 | +$0.00 | -$2.50 | -2.50% | XRT -4.22% | +1.72pp |
| ISRG | $425.80 | $399.05 | $93.72 | -$6.28 | +$0.00 | -$6.28 | -6.28% | IHI -2.65% | -3.63pp |
| NFLX | $59.69 | $56.73 | $95.04 | -$4.96 | +$0.00 | -$4.96 | -4.96% | XLC -5.26% | +0.30pp |
| MSFT | $504.90 | $484.52 | $95.96 | -$4.04 | +$0.19 | -$3.85 | -3.85% | IGV -5.45% | +1.41pp |
| **Total** | | | **$484.35** | **-$15.65** | **+$0.19** | **-$15.46** | **-3.09%** | | **4 of 5** |

*Price-only return -3.13%; total return **-3.09%**. "vs. Sector" compares price returns, matching the dashboard. First ex-dividend: MSFT $0.98 on November 19, +$0.1941 on 0.19805 shares (bought November 18, so held on the ex-date). Cumulative dividends $0.1941.*

**Benchmarks:**
- SPY: $730.13 to $689.81 = **-5.52%**
- Portfolio (total return) vs. SPY: **+2.43 pp ahead**
- Sector scorecard: **4 of 5** positions ahead of their sector ETF; ISRG is the miss.

*The known AI tilt explains the week. SMH fell 12.94% from the November 18 close, and on November 20, when it fell 10.60%, the book lost 1.38% against SPY's 3.64%. Two sessions say nothing yet about stock picking.*

#### The Week's One Fact

**On November 20, when SMH fell 10.60% and SPY 3.64%, the book lost only $6.77 (1.38%), and PGR and TJX rose.** That one day supplies about 2.3 of the book's 2.43-point lead over SPY. Daily closes per stockanalysis.com, valued at the book's share counts.

#### What Moved and Why

**PGR (+2.12% since entry).** Largest move: +0.83% from the fill to the November 18 close. That morning Progressive reported October: net premiums written +1%, combined ratio 91.2 against 89.7 a year earlier, policies in force +6% (SEC 8-K). The stock closed down 2.64% on the day but above our fill. It then rose 0.65% and 0.62% while KIE fell, so this was company-specific, not the sector.

**TJX (-2.50% since entry).** Largest move: -2.03% from the fill to the November 18 close. Bought on its Q3 report day after the open jump: comps +4%, adjusted EPS $1.34 in line, full-year comp guide raised to 4%, Q4 EPS guide lowered on tariff-refund compensation accruals (company release). Ross rose 3.3% and Burlington 5.5% that day (Trefis). TJX then held flat while XRT fell 4.2%. The entry-note risk cost 2.03 points.

**ISRG (-6.28% since entry).** Largest move: -3.26% on November 19, when IHI fell 1.51%. Reports cite a break below the 200-day moving average, valuation, and small planned insider sales (TradingKey, MarketBeat); no company news found. It fell 1.92% on November 20 with IHI down 1.16%. It fell more than twice as far as its sector without news, the one scorecard miss; two sessions is noise, not a thesis question.

**NFLX (-4.96% since entry).** Largest move: -2.96% on November 20, with XLC down 2.66%. It set multi-year lows this week, still weighed by the Q3 cut of the ad-revenue outlook to $2.7B and a Wells Fargo downgrade to Underweight (FX Leaders, Benzinga; downgrade date not confirmed). It moved with XLC on both days and finished 0.30 points ahead of it. No new company news.

**MSFT (-4.04% price since entry).** Largest move: -2.77% on November 20, when IGV fell 4.62% and SMH 10.60%. Reports tie it to the broad AI unwind and to Microsoft's warning that a proposed FCC ban on new Chinese optical transceiver models could slow data-center buildout (IBTimes, Traders Union). It fell with software, less than IGV. First dividend earned: $0.98 per share, ex-date November 19.

#### Macro Context

Shared with Phase 2's Week 28 entry. The book's two sessions were the end of a five-day AI selloff. Nvidia beat on November 17 but closed down about 3% on November 18 (Investing.com). On November 19 the S&P 500 fell 2.02% as an early rally on Anthropic's first trading day faded (CNBC). On November 20 Reuters reported an SEC probe of Nvidia's accounting; the Nasdaq fell 5.28%, the S&P 500 3.7%, and the S&P 500 and Dow closed in correction (UPI). The 10-year yield fell to about 4.92%, and markets price about a 92% chance of a December hike (CNBC). SMH moved more than 2% on both days. On November 19 PGR rose against it; on November 20 PGR and TJX did.

#### Lesson: None This Week

The book is two sessions old, and its first move was the AI tilt it was built with. Nothing new.

#### Thesis Status Check

| Position | Thesis Status | Notes |
|----------|--------------|-------|
| PGR | ✅ Intact | October: policies in force +6%, combined ratio 91.2, still profitable underwriting. Premium growth slow at +1%. Rose while KIE fell. |
| TJX | ✅ Intact | Q3 comps +4%, full-year comp guide raised to 4%; Q4 EPS guide lowered on tariff-refund accruals. Held while XRT fell 4.2%. |
| ISRG | ✅ Intact | Fell 3.63 points behind IHI with no company news. No procedure, pricing or reimbursement change reported. Q4 report around January 28. |
| NFLX | ✅ Intact | Multi-year low on the ad-outlook cut and a downgrade, no new company news. Moved with XLC. |
| MSFT | ✅ Intact | Fell with software in the AI selloff, less than IGV. Azure facts unchanged since Q1 (+48%). First dividend earned. |

#### Things to Watch Next Week
- **AI tilt.** If chips rebound, expect the book to give back some of its SPY lead for factor reasons, not company ones.
- **ISRG.** Whether the gap to IHI keeps widening without company news.
- **MSFT.** Any FCC action on Chinese optical transceivers, and Nvidia SEC probe news that changes hyperscaler capex.
- **PGR.** November results in mid-December, and the annual variable dividend, usually declared in December.
- **Fed meeting December 8 and 9.** A hike is about 92% priced; higher rates help PGR's investment income.
- **Thanksgiving.** Markets close November 26 and close early November 27, so W2 uses the November 27 close.

---

*Next check-in: ~November 27, 2026 (Week 2). Thanksgiving November 26, Fed meeting December 8 and 9, PGR November results mid-December.*

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
| PGR | Monthly results mid-month; Q4 around January 27, 2027 | Q3 reported November 5, 2026: EPS $4.37 vs $4.42 expected, net premiums written +4%. October (W1): reported November 18, net premiums written +1%, combined ratio 91.2 vs 89.7, net income $828M (-2%), policies in force 40.53M (+6%). November results expected mid-December. |
| NFLX | Mid-to-late January 2027 (Q4) | Q3 reported October 20, 2026: EPS $0.87 vs $0.82, revenue $12.87B in line, 2026 ad outlook cut to $2.7B. |
| MSFT | Late January 2027 (FY Q2) | FY Q1 reported October 28, 2026: revenue $92.3B (+19%), Azure +48%, EPS $4.89 vs $4.72. |
| ISRG | Around January 28, 2027 (Q4) | Q3 reported October 20, 2026: procedures +15%, adjusted EPS $3.00 vs $2.65. |
| TJX | Late February 2027 (Q4 FY27) | Q3 FY27 reported November 18, 2026 (entry day): comps +4%, above plan. W1 detail: sales $16.0B (+6%), adjusted EPS $1.34 (+5%), full-year comp guide raised to +4%, Q4 comps planned +2% to +3%, Q4 EPS guide lowered on tariff-refund compensation accruals (company release). Stock +8.05% that session. |
