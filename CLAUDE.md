# Portfolio Experiments: Phase 2 and Phase 3

This repo is the home of Jake Worcester's two small stock-picking experiments and their
public dashboards (GitHub Pages: https://jakeworcester-byte.github.io/pf-lessons/ for
Phase 2, `phase3.html` for Phase 3). Both run at the same time.
A Claude Code cloud routine updates it every Saturday morning by following
`WEEKLY_UPDATE.md`. Jake reads the results on the site; he does not review the
work before it publishes, so the files have to be right on their own.

**This repo is the source of truth.** Interactive sessions on Jake's PC work in a
clone at `OneDrive/Documents/Claude/Projects/Investing/portfolio-site/` and must
`git pull` before reading or changing anything.

## Phase 2 (continuing)

- **Opened:** May 11, 2026 · **Invested:** $499.99 · 5 equal-weight positions, buy-and-hold
- **6-month review:** done November 14, 2026 (in the log). The positions are still
  held, so the weekly update keeps tracking them until Jake changes the holdings. Its
  12-month mark is May 11, 2027; whether it ends there is Jake's call.
- **Benchmarks:** SPY baseline $739.30 · QQQ baseline $713.29

| Ticker | Theme | Shares | Entry Price | Cost Basis |
|--------|-------|--------|-------------|------------|
| MU | AI/Semi (memory) | 0.12617 | $792.53 | $99.99 |
| LLY | Healthcare / GLP-1 | 0.10583 | $944.90 | $100.00 |
| CEG | Energy / AI power (nuclear) | 0.31744 | $315.02 | $100.00 |
| LMT | Defense / quality value | 0.19849 | $503.78 | $100.00 |
| MA | Fintech / payments | 0.20202 | $495.00 | $100.00 |

**Hypothesis:** thematic stock-picking across five uncorrelated themes with
disciplined equal-weight sizing can outperform a broad index over 6 to 12 months,
and the pattern of which themes work will show whether there is edge or luck.

- **Success:** at least 3 of 5 themes beat their sector benchmark, and we can say
  clearly why each worked or didn't.
- **Failure:** returns concentrated in one or two themes (a Phase 1 repeat), or a
  random distribution with no pattern. Then the honest conclusion is that fun money
  should be indexed.

## Phase 3 (opened November 18, 2026)

- **Invested:** $500.00 · 5 equal-weight positions, buy-and-hold, fills about 10:04 AM CT
- **Reviews:** 3-month February 18, 2027 · 6-month May 18, 2027
- **Primary benchmark:** SPY baseline $730.13 (recorded at fill time)
- **Diagnostic benchmarks:** one sector ETF per position, locked at entry, baselines are
  the November 18 closes (`PHASES[3]["sector_base"]` in `tools/fetch_prices.py`, mirrored
  in `SECTOR_BASE` in `phase3.html`)

| Ticker | Price driver | Shares | Entry Price | Cost Basis | Sector ETF |
|--------|--------------|--------|-------------|------------|------------|
| PGR | Auto insurance pricing vs. claims | 0.44135 | $226.58 | $100.00 | KIE |
| TJX | Off-price retail, trade-down | 0.69834 | $143.20 | $100.00 | XRT |
| ISRG | Surgical procedure volumes | 0.23485 | $425.80 | $100.00 | IHI |
| NFLX | Subscriptions, pricing, ads | 1.67538 | $59.69 | $100.00 | XLC |
| MSFT | Azure cloud growth | 0.19805 | $504.90 | $100.00 | IGV |

**Hypothesis:** stocks chosen for company-specific earnings drivers, with no two sharing
a main price driver and no single name dominating risk, can outperform SPY over 6 to 12
months, and will beat their own sector benchmarks more often than not.

- **Goal:** total return beats SPY.
- **Diagnostic:** at least 3 of 5 positions beat their sector ETF, each explained by the
  company's own numbers.
- **Failure:** the book trails SPY, or the result is explained by a shared factor rather
  than company results. Then fun money should be indexed.
- **Known tilt:** the book leans against the AI trade (equal-weight correlation with SMH
  of -0.32 at entry). If AI rallies hard, it will likely trail SPY for factor reasons. Say
  so whenever it explains a week.

The full baseline (risk check, decision audit, entry note) is the "Baseline and Rules"
section of `Phase_3_Weekly_Review_Log.md`.

**Phase 1 (ended):** ASML, AMD, IONQ, NVDA, SNOW from Sept 29, 2025. Its lessons are
the first entries in the Lessons Ledger.

## Files

| File | What it is |
|------|------------|
| `WEEKLY_UPDATE.md` | The weekly procedure. Follow it exactly. |
| `Phase_2_Weekly_Review_Log.md` | Phase 2 append-only log: summary tables, one entry per week, quarterly reviews. The source of truth for every Phase 2 weekly number. |
| `Phase_3_Weekly_Review_Log.md` | Phase 3 append-only log, same structure plus a Sector Scorecard table and a Baseline and Rules section. The source of truth for every Phase 3 number. |
| `Phase_2_Lessons_Ledger.md` | Append-only ledger of durable, transferable lessons, shared by both phases (the file name is historical). |
| `index.html` | The Phase 2 dashboard. Live prices load from Finnhub in the browser; the thesis grid, chart history, lessons, fallback prices, and `PUBLISHED` date are a static block updated each week. |
| `phase3.html` | The Phase 3 dashboard. Same pattern as `index.html`: live Finnhub prices, and a static block (`FALLBACK`, `CUM_DIVIDENDS`, `PUBLISHED`, `WEEKS`, `WK_DATES`, `HIST`, `THESIS`, `LESSONS`, `SECTOR_BASE`) updated each week. |
| `review.html` | Renders a log and the ledger as readable pages (latest week, all weeks, reviews, ledger). `review.html` is Phase 2; `review.html?phase=3` is Phase 3. It reads the markdown files directly and never needs editing for a weekly update. |
| `thesis-criteria.md` | Per-ticker thesis-break criteria for both phases. Load only when a position is under real pressure. |
| `tools/fetch_prices.py` | Pulls closes from Finnhub and computes every figure with the dashboards' exact math. `--phase 2` (default) or `--phase 3`; `--live` reads the key from `index.html`. |
| `tools/verify.py` | The publish gate for both phases. Must print `VERIFY OK` for Phase 2 and Phase 3 before any commit. |

## Ground rules

- **No trading.** This is buy-and-hold. Nothing in these files recommends or records
  a trade Jake has not made. An urge to sell is a lesson to discuss, not a signal.
- **Thesis-break criteria are the only legitimate exit trigger.** Volatility is not a
  thesis break. A bad report triggers a thesis re-check, not a sale.
- **Status changes come from company facts.** Never move a thesis status because
  rates or the market moved the price (Lesson 14).
- **The log and ledger are append-only.** Corrections go in the current week's entry
  with a note. The dashboard's static block is overwritten each week by design.
- **Separate facts, interpretation, and opinion.** Name sources for numbers that
  matter. Never approximate a price.
- **Stay in the repo.** Never send email or messages, never touch other repos, never
  push anywhere but `origin main`.

## Writing rules for lessons, concepts, and narrative

These govern the Lessons Ledger, the log's lesson section, the thesis notes, and the
dashboard lesson cards. They exist because W13, W14 and W15 produced three ledger
entries that were all the same lesson, at 1,800 words, each mostly a critique of the
one before.

1. **Default to no lesson.** Most weeks teach nothing durable. If nothing new
   surfaced, write "No lesson this week" plus one line on why, and move on.
2. **The title is an instruction, not an observation.** It must tell Jake what to do,
   in plain words, and work on its own. "Don't change a thesis rating when rates moved
   and the business didn't" passes. "A Macro Catalyst Is Symmetric" fails.
3. **150 words maximum per lesson,** in three parts: what happened (one sentence, with
   the number in it), what it means (two sentences), what to do differently next time
   (one imperative sentence).
4. **No entry may be primarily about a previous entry.** That is a two-line amendment
   under the earlier lesson, not a new numbered one.
5. **Same holding plus same mechanism twice means stop.** Don't write a third;
   consolidate or skip.
6. **No coined terms, no aphorisms, no abstraction as a device.** Name the company, the
   number, and the decision.

Section caps: "What Moved and Why" 80 words per position, thesis notes 40 words,
concept or lesson section 200 words. Price and benchmark tables are data and stay as
they are.

**No em dashes anywhere** in new text. Use commas, colons, or a period. Older entries
contain some; leave them, since the log is append-only. `verify.py` checks new lines.

Voice: direct, specific numbers, plain language for a smart reader who is not a
finance professional. Call out sector noise versus a real thesis concern.

## Standard reminder

Nothing here is financial advice. These are two $500 learning experiments.
