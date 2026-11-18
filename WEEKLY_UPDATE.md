# Weekly Update Procedure

This is the procedure the Saturday cloud routine follows. Each run updates **both**
experiments, Phase 2 and Phase 3, in one commit. Every step below applies to both
unless it names one. Where a step names a file, the Phase 3 equivalent is:

| Phase 2 | Phase 3 |
|---------|---------|
| `index.html` | `phase3.html` |
| `Phase_2_Weekly_Review_Log.md` | `Phase_3_Weekly_Review_Log.md` |
| `--phase 2` (default) | `--phase 3` |
| benchmarks SPY and QQQ | benchmark SPY, plus one sector ETF per position |

The Lessons Ledger (`Phase_2_Lessons_Ledger.md`) is shared.

The run is unattended: nobody
answers questions mid-run. When something is ambiguous, take the conservative option,
say so in the week's entry or the final report, and keep going. Read `CLAUDE.md` first;
its ground rules and writing rules apply to everything below.

Scripts do the math. You do the research and the writing. Never compute a return by
hand when `tools/fetch_prices.py` can produce it.

## 0. Start clean

```bash
git checkout main && git pull --rebase origin main
python tools/verify.py --no-git      # last week's state should already pass, for both phases
```

If the pre-check fails, last week's publish was incomplete. Fix that first (the log is
the source of truth for numbers, the dashboard follows it) and note the repair in this
week's entry.

## 1. Decide whether there is a new week

Get each phase's cumulative dividend total from `CUM_DIVIDENDS` in its dashboard, then:

```bash
python tools/fetch_prices.py --phase 2 --live --dividends <CUM_DIVIDENDS from index.html>  --json /tmp/snap2.json
python tools/fetch_prices.py --phase 3 --live --dividends <CUM_DIVIDENDS from phase3.html> --json /tmp/snap3.json
```

`quote_dates` in the output is the trading day each price is from. Call the latest of
those dates the **close date**.

- If the close date is on or before the date of the latest `### Week N` entry in a
  phase's log, there is nothing new for that phase. If neither phase has a new close,
  stop: no edits, no commit, report "no new close."
- All of a phase's symbols should share one close date (Phase 2: seven symbols;
  Phase 3: five positions, SPY, and the five sector ETFs). If one lags (a halt, a data
  hiccup), get that symbol's close for the close date from stockanalysis.com history or
  Google Finance, write all of that phase's prices to `/tmp/prices<phase>.json`, and
  rerun with `--prices /tmp/prices<phase>.json` instead of `--live`. Say which source you
  used.
- If Finnhub is unreachable, do the same with every symbol. Never approximate a price
  and never carry one forward.
- If any position moved more than 25% in a week, check for a stock split before
  writing anything. A split changes `shares` and `entry` and needs Jake; record it as
  a flag, use split-adjusted math only if the split is confirmed, and say so plainly.

**Week number:** each phase counts its own weeks. Phase 2's Week 1 closed Friday
May 15, 2026; Phase 3's Week 1 closes Friday November 20, 2026. The new week number is
`1 + (weeks between that phase's Week 1 Friday and the Friday of the close date's week)`. Normally
that is the last week plus one. If a Saturday run was missed, the number skips (for
example W22 to W24); that is correct. Write one catch-up entry for the latest week,
never backfill skipped weeks, and say in the entry which week was skipped.

The week's date label is the close date (for example "October 9, 2026"). If Friday was
a market holiday, the close date is Thursday; note it in the entry.

**Phase 3 sector baselines (one-time).** If any value in `PHASES[3]["sector_base"]` in
`tools/fetch_prices.py` is `None`, record it before anything else: get the November 18,
2026 close for that ETF (KIE, XRT, IHI, XLC, IGV) from
`https://stockanalysis.com/etf/<ticker>/history/`, confirm it against a second source,
and write the same value in three places: `PHASES[3]["sector_base"]`, `SECTOR_BASE` in
`phase3.html`, and the "Benchmark Baselines" table in the Phase 3 log (replace
"Pending" with the price and the source). Then rerun the Phase 3 snapshot. Say in the
week's entry that the baselines were recorded this run. If a close can't be confirmed,
leave it `None`; the scorecard shows "pending" for that position and `verify.py`
accepts it.

## 2. Dividends

For each position in each phase, check whether an ex-dividend date fell after the
previous week's close date and on or before this close date. Start from the
"Upcoming / expected" list under that phase's Dividend Ledger, then confirm the date and
per-share amount with a web search. A dividend counts when the ex-date is in the
window and the position is held.

If there is a new dividend: earned = per-share amount x shares. Add the new cumulative
total, and rerun step 1's command with the new `--dividends` value so the snapshot
includes it. Use full precision for `CUM_DIVIDENDS` (8 decimals), two decimals in the
log tables.

## 3. Research the week

This is the step that decides whether the entry is worth reading. Do it before writing
anything, and use the "extended" web search mode for it.

Research the macro picture (step b and d) once and use it for both phases. Research each
position separately.

**a. Start from the daily closes, not the weekly number.** Pull the week's daily closes
for all ten positions, SPY and QQQ, and the five Phase 3 sector ETFs (stockanalysis.com history pages,
`https://stockanalysis.com/stocks/<ticker>/history/`). For each position, note its
largest one-day move. Then line the five up by day: when two or more positions move
sharply on the same day, the cause is probably shared, so look for it there first.

**b. Get the market wrap for every session that mattered.** At minimum, the day of each
position's largest move and the Friday close. Find what the indexes, yields and oil did
and why. Last week's entry quoted only the Friday close and missed the day that
decided the week.

**c. Check each position against its peers and customers.** A stock that moves with its
group moved on sector news; one that moves alone moved on company news.

| Position | Peers and read-throughs to check |
|----------|----------------------------------|
| MU | SK hynix, Samsung, SanDisk, SMH or SOXX; hyperscaler capex (Microsoft, Alphabet, Amazon, Meta, Oracle); Nvidia; China memory (CXMT, YMTC) |
| LLY | Novo Nordisk, XLV; FDA and drug-pricing news; GLP-1 competitors |
| CEG | Vistra, Talen, GE Vernova, Vertiv, XLU; hyperscaler power deals and capex; PJM and FERC |
| LMT | RTX, Northrop, General Dynamics, ITA; Pentagon budget and appropriations; the Iran conflict and oil |
| MA | Visa, American Express, XLF; consumer spending data; interchange regulation; stablecoins |
| PGR (Phase 3) | Allstate, Travelers, KIE; Progressive's monthly results (mid-month); auto repair and medical claims inflation; rates |
| TJX (Phase 3) | Ross Stores, Burlington, XRT; consumer spending and retail sales; tariffs |
| ISRG (Phase 3) | Medtronic, Stryker, IHI; hospital procedure volumes; reimbursement and China policy |
| NFLX (Phase 3) | Disney, Roku, Spotify, XLC; streaming pricing and advertising market |
| MSFT (Phase 3) | Alphabet, Amazon, Oracle, IGV and SMH; hyperscaler capex and AI-spending sentiment |

**Phase 3 known tilt.** The Phase 3 book leans against the AI trade. On any day SMH
moved more than 2%, check whether the Phase 3 positions moved the other way, and say so
when that, rather than company news, explains the week.

**d. Check the calendar for the week just ended.** Macro releases (CPI, PPI, jobs, PCE,
retail sales), Fed meetings, minutes and speeches, and earnings from the peers above.
A peer's earnings often explain a position's move better than its own news does.

**e. Close out last week's open questions.** Re-read last week's entry. Anything it
called unexplained or unconfirmed (a cause, an earnings date, a dividend date) gets
another search now. If the answer changes what last week said, add a short
"Correction to Week N" section to this week's entry. Never edit last week's entry.

**f. Pass this test before writing.** For each position, write down the cause of its
largest one-day move and the source. "Unexplained" is allowed only after steps a to d,
and the entry must then name what was checked (for example: "no company news; peers
flat; the market wrap names no cause"). Never write "unexplained" when the stock moved
with its peer group on the same day.

**g. Handling sources.** Prefer primary sources (company releases, SEC filings, the Fed,
BLS) and reputable outlets. Some outlets (CNBC, Benzinga, Reuters) block page fetches;
use their search snippets, or the same story from another outlet. Treat AI-generated
"market mover" pages as leads, not sources. When two sources disagree on a number
that matters, use stockanalysis.com closes to settle price moves, and say so in the
entry when the conflict can't be settled.

Load `thesis-criteria.md` only if a position is under real pressure (a bad report, a
sharp drawdown, a specific news event). Status changes come from company facts tested
against those criteria, never from price or rates alone (Lesson 14).

## 4. Write the logs

Append-only. Never rewrite a prior week. If you find an error in an old entry, correct
it with a note in this week's entry.

1. **Cumulative Performance Tracker:** add a row for the new week. Columns map to the
   snapshot: Portfolio Value = `price_value`, Price % = `price_return_pct`, Cum. Div.,
   Total Return % = `total_return_pct`, SPY %, QQQ %, vs. SPY = `vs_spy_pp`, vs. QQQ =
   `vs_qqq_pp`. Signs on every percentage, `pp` on the spreads. Phase 3 has no QQQ
   columns.
2. **Position Performance by Week:** add a row of each position's `return_pct`.
   **Phase 3 also:** add a row to **Sector Scorecard by Week**, one cell per position
   from its `vs_sector_pp` (for example `+1.19pp`), or `pending` when it is `null`, and
   a "Beaten" cell of `<sectors_beaten> of <sectors_scored>` (or `pending` when
   `sectors_scored` is 0).
3. **Dividend Ledger:** add any new dividend rows above "Total to date", update the
   total, and update the "Upcoming / expected" bullets.
4. **The week's entry:** insert `### Week N: <Month D, YYYY>` (colon, not a dash)
   just above the `---` that precedes `## Quarterly Reviews`. Match the structure of
   the latest entries:
   - an italic line on the portfolio's age and the price source
   - `#### Prices Used` table and the italic summary line under it
   - `**Benchmarks:**` bullets and the italic note on which side moved
   - `#### The Week's One Fact`
   - `#### What Moved and Why` (one paragraph per position, 80 words max each)
   - `#### Macro Context`
   - `#### Lesson: ...` or `#### Lesson: None This Week` with one line on why
   - `#### Thesis Status Check` table (40 words max per note)
   - `#### Things to Watch Next Week`
   - an italic "Next check-in" line with the dates that matter
   Read the last two entries before writing so the voice and format stay consistent.
   **Phase 3 entries** follow the same structure without QQQ. Add two columns to the
   Prices Used table, "Sector ETF %" and "vs. Sector", and under the Benchmarks bullets
   one italic line saying which result explains the week: the SPY comparison, the sector
   scorecard, or the known AI tilt. Until Phase 3 has its own entries to copy, model the
   first one on the latest Phase 2 entry.
5. **Concepts Learned Index:** add a row only if the week introduced a new concept.
6. **Earnings Calendar:** when a company reports, update its row with the result and
   the next expected date.

## 5. Lessons Ledger (`Phase_2_Lessons_Ledger.md`)

The ledger is shared by both phases. Default to no lesson. Add one only when it clears
every writing rule in `CLAUDE.md` (instruction-style title, 150 words max, not about a
previous entry, not a third entry on the same holding and mechanism). Number it after
the last entry, format the heading `**N. Title.** *(Week N: Month D, YYYY)*` for Phase 2
or `**N. Title.** *(Phase 3, Week N: Month D, YYYY)*` for Phase 3. One run adds at most
one lesson across both phases. An update to an earlier lesson is a
short `> **Amendment (Week N, date).**` block under that lesson, not a new number.

## 6. Dashboards (`index.html` and `phase3.html`)

Only the static data block and the week labels change. Do not touch the layout,
styles, or render code.

- `FALLBACK`: this week's closes for every symbol of that phase (Phase 3: the five
  positions, SPY, and each sector ETF whose baseline is set).
- `CUM_DIVIDENDS`: the new total, and refresh its comment (what changed, what is next).
- `PUBLISHED`: today's date in Central time, `YYYY-MM-DD`.
- `WEEKS`, `WK_DATES` ("Oct 9" style), and `HIST.port` / `HIST.spy` / `HIST.qqq`:
  append this week, using the values just written to the Cumulative Performance
  Tracker. Phase 3 has `HIST.port` and `HIST.spy` only.
- `THESIS`: overwrite with this week's five statuses and condensed notes, keeping
  the existing row order.
- `LESSONS`: append a card only if step 5 added a ledger entry (or an amendment card,
  following the W18 example), on the dashboard of the phase it came from.
- `SECTOR_BASE` (Phase 3): changes only in the one-time baseline step in step 1.
- Week labels: replace every `W<last>, <date>` string (thesis heading, footer, status
  line, the two `showErr` messages, the fallback comment). `verify.py` fails on any
  label that still names the old week.

## 7. Verify (the publish gate)

```bash
python tools/verify.py
```

It must print `VERIFY OK` for both Phase 2 and Phase 3. For each phase it checks that
the dashboard and log agree to the cent and
the hundredth of a point, that every label names the current week, that the thesis
grid is complete, that the Phase 3 sector scorecard and baselines match the script,
that the page scripts parse, and that nothing added this run
contains an em dash. Fix whatever it reports and rerun. If you cannot get it to pass,
do not commit: run `git checkout -- . && git clean -fd`, and report exactly what
failed. The live site keeps last week's data, and after nine days it shows a stale
warning on its own.

## 8. Publish

```bash
git add -A
git commit -m "Weekly update: <Month D, YYYY> (Phase 2 W<n>, Phase 3 W<m>)"
git pull --rebase origin main
git push origin main
```

Push to `main`, not a `claude/` branch: GitHub Pages deploys from `main`. Then confirm
the deploy: within about three minutes,
`https://jakeworcester-byte.github.io/pf-lessons/index.html` and
`https://jakeworcester-byte.github.io/pf-lessons/phase3.html` should contain the new
`PUBLISHED` date. If it does not after five minutes, say so in the report.

## 9. Report

End with a short plain-language summary, one block per phase: the week number and close
date, total return and the spread to SPY (and QQQ for Phase 2), for Phase 3 the sector
count ("2 of 5 beating their sector"), one line per position, any thesis status change, the
lesson (or "no lesson"), any new dividend, and anything flagged (price source
fallback, split, verification repair, skipped week, unanswered question for Jake). Name
any move still unexplained after step 3, and any correction made to last week.

## Milestones and phase changes

- **Phase 2 6-month review:** done (written November 14, 2026, in the Week 27 run).
- **Phase 2 keeps running.** Its positions are real holdings. Keep the weekly update
  going on them until Jake changes the holdings. Its 12-month mark is May 11, 2027: on
  the first run with a close on or after that date, add one line to the report asking
  Jake whether Phase 2 ends there. Do not write a 12-month review unless he asks.
- **Phase 3 3-month review.** On the first run whose close date is on or after
  February 18, 2027, write a `## 3-Month Review: Phase 3` section under
  `## Quarterly Reviews` in the Phase 3 log, modeled on Phase 2's 3-Month Review:
  bottom line first, scorecard against the goal and diagnostic in `CLAUDE.md`, where the
  result came from (theme versus stock selection against the sector ETFs), each
  position's share of portfolio risk and the book's correlation with SMH computed from
  daily closes since entry, and what it proves and does not. Update the review index
  line. The site lists it automatically. The 6-month review follows the same pattern on
  the first run on or after May 18, 2027.
- **Never invent, buy, sell, or propose trades in the files.** New positions or a new
  phase come only from Jake in an interactive session: positions in `CLAUDE.md`,
  `tools/fetch_prices.py` (`PHASES`), and the dashboard's `POS` block.
