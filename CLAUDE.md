# Phase 2 Portfolio Experiment

This repo is the home of Jake Worcester's small stock-picking experiment and its
public dashboard (GitHub Pages: https://jakeworcester-byte.github.io/pf-lessons/).
A Claude Code cloud routine updates it every Saturday morning by following
`WEEKLY_UPDATE.md`. Jake reads the results on the site; he does not review the
work before it publishes, so the files have to be right on their own.

**This repo is the source of truth.** Interactive sessions on Jake's PC work in a
clone at `OneDrive/Documents/Claude/Projects/Investing/portfolio-site/` and must
`git pull` before reading or changing anything.

## The experiment

- **Opened:** May 11, 2026 · **Invested:** $499.99 · 5 equal-weight positions, buy-and-hold
- **Review date:** November 11, 2026 (6 months). A Phase 3 is expected after it.
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

**Phase 1 (ended):** ASML, AMD, IONQ, NVDA, SNOW from Sept 29, 2025. Its lessons are
the first entries in the Lessons Ledger.

## Files

| File | What it is |
|------|------------|
| `WEEKLY_UPDATE.md` | The weekly procedure. Follow it exactly. |
| `Phase_2_Weekly_Review_Log.md` | Append-only log: summary tables, one entry per week, quarterly reviews. The source of truth for every weekly number. |
| `Phase_2_Lessons_Ledger.md` | Append-only ledger of durable, transferable lessons. |
| `index.html` | The dashboard. Live prices load from Finnhub in the browser; the thesis grid, chart history, lessons, fallback prices, and `PUBLISHED` date are a static block updated each week. |
| `review.html` | Renders the log and ledger as readable pages (latest week, all weeks, reviews, ledger). It reads the markdown files directly and never needs editing for a weekly update. |
| `thesis-criteria.md` | Per-ticker thesis-break criteria. Load only when a position is under real pressure. |
| `tools/fetch_prices.py` | Pulls closes from Finnhub and computes every figure with the dashboard's exact math. `--live` reads the key from `index.html`. |
| `tools/verify.py` | The publish gate. Must print `VERIFY OK` before any commit. |

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

Nothing here is financial advice. This is a $500 learning experiment.
