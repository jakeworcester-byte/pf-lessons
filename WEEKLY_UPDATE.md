# Weekly Update Procedure

This is the procedure the Saturday cloud routine follows. It runs unattended: nobody
answers questions mid-run. When something is ambiguous, take the conservative option,
say so in the week's entry or the final report, and keep going. Read `CLAUDE.md` first;
its ground rules and writing rules apply to everything below.

Scripts do the math. You do the research and the writing. Never compute a return by
hand when `tools/fetch_prices.py` can produce it.

## 0. Start clean

```bash
git checkout main && git pull --rebase origin main
python tools/verify.py --no-git      # last week's state should already pass
```

If the pre-check fails, last week's publish was incomplete. Fix that first (the log is
the source of truth for numbers, the dashboard follows it) and note the repair in this
week's entry.

## 1. Decide whether there is a new week

Get the current cumulative dividend total from `CUM_DIVIDENDS` in `index.html`, then:

```bash
python tools/fetch_prices.py --live --dividends <CUM_DIVIDENDS> --json /tmp/snap.json
```

`quote_dates` in the output is the trading day each price is from. Call the latest of
those dates the **close date**.

- If the close date is on or before the date of the latest `### Week N` entry in the
  log, there is nothing new. Stop: no edits, no commit, report "no new close."
- All seven symbols should share one close date. If one lags (a halt, a data hiccup),
  get that symbol's close for the close date from stockanalysis.com history or Google
  Finance, write all seven prices to `/tmp/prices.json`, and rerun with
  `--prices /tmp/prices.json` instead of `--live`. Say which source you used.
- If Finnhub is unreachable, do the same with all seven symbols. Never approximate a
  price and never carry one forward.
- If any position moved more than 25% in a week, check for a stock split before
  writing anything. A split changes `shares` and `entry` and needs Jake; record it as
  a flag, use split-adjusted math only if the split is confirmed, and say so plainly.

**Week number:** Week 1 closed Friday May 15, 2026. The new week number is
`1 + (weeks between May 15, 2026 and the Friday of the close date's week)`. Normally
that is the last week plus one. If a Saturday run was missed, the number skips (for
example W22 to W24); that is correct. Write one catch-up entry for the latest week,
never backfill skipped weeks, and say in the entry which week was skipped.

The week's date label is the close date (for example "October 9, 2026"). If Friday was
a market holiday, the close date is Thursday; note it in the entry.

## 2. Dividends

For each of the five positions, check whether an ex-dividend date fell after the
previous week's close date and on or before this close date. Start from the
"Upcoming / expected" list under the log's Dividend Ledger, then confirm the date and
per-share amount with a web search. A dividend counts when the ex-date is in the
window and the position is held.

If there is a new dividend: earned = per-share amount x shares. Add the new cumulative
total, and rerun step 1's command with the new `--dividends` value so the snapshot
includes it. Use full precision for `CUM_DIVIDENDS` (8 decimals), two decimals in the
log tables.

## 3. Research the week

For each position: the week's company news, analyst moves, and anything that bears on
its thesis. Earnings weeks get deeper treatment. Then the macro picture (rates, Fed,
data releases) only as far as it explains what the book did.

Load `thesis-criteria.md` only if a position is under real pressure (a bad report, a
sharp drawdown, a specific news event). Status changes come from company facts tested
against those criteria, never from price or rates alone (Lesson 14).

Prefer primary sources and reputable outlets. Get numbers right; if two sources
disagree on a figure that matters, say so rather than picking one silently.

## 4. Write the log (`Phase_2_Weekly_Review_Log.md`)

Append-only. Never rewrite a prior week. If you find an error in an old entry, correct
it with a note in this week's entry.

1. **Cumulative Performance Tracker:** add a row for the new week. Columns map to the
   snapshot: Portfolio Value = `price_value`, Price % = `price_return_pct`, Cum. Div.,
   Total Return % = `total_return_pct`, SPY %, QQQ %, vs. SPY = `vs_spy_pp`, vs. QQQ =
   `vs_qqq_pp`. Signs on every percentage, `pp` on the spreads.
2. **Position Performance by Week:** add a row of each position's `return_pct`.
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
5. **Concepts Learned Index:** add a row only if the week introduced a new concept.
6. **Earnings Calendar:** when a company reports, update its row with the result and
   the next expected date.

## 5. Lessons Ledger (`Phase_2_Lessons_Ledger.md`)

Default to no lesson. Add one only when it clears every writing rule in `CLAUDE.md`
(instruction-style title, 150 words max, not about a previous entry, not a third
entry on the same holding and mechanism). Number it after the last entry, format the
heading `**N. Title.** *(Week N: Month D, YYYY)*`. An update to an earlier lesson is a
short `> **Amendment (Week N, date).**` block under that lesson, not a new number.

## 6. Dashboard (`index.html`)

Only the static data block and the week labels change. Do not touch the layout,
styles, or render code.

- `FALLBACK`: this week's seven closes.
- `CUM_DIVIDENDS`: the new total, and refresh its comment (what changed, what is next).
- `PUBLISHED`: today's date in Central time, `YYYY-MM-DD`.
- `WEEKS`, `WK_DATES` ("Oct 9" style), and `HIST.port` / `HIST.spy` / `HIST.qqq`:
  append this week, using the values just written to the Cumulative Performance
  Tracker.
- `THESIS`: overwrite with this week's five statuses and condensed notes, keeping
  the existing row order.
- `LESSONS`: append a card only if step 5 added a ledger entry (or an amendment card,
  following the W18 example).
- Week labels: replace every `W<last>, <date>` string (thesis heading, footer, status
  line, the two `showErr` messages, the fallback comment). `verify.py` fails on any
  label that still names the old week.

## 7. Verify (the publish gate)

```bash
python tools/verify.py
```

It must print `VERIFY OK`. It checks that the dashboard and log agree to the cent and
the hundredth of a point, that every label names the current week, that the thesis
grid is complete, that the page script parses, and that nothing added this run
contains an em dash. Fix whatever it reports and rerun. If you cannot get it to pass,
do not commit: run `git checkout -- . && git clean -fd`, and report exactly what
failed. The live site keeps last week's data, and after nine days it shows a stale
warning on its own.

## 8. Publish

```bash
git add -A
git commit -m "Week N update: <Month D, YYYY>"
git pull --rebase origin main
git push origin main
```

Push to `main`, not a `claude/` branch: GitHub Pages deploys from `main`. Then confirm
the deploy: within about three minutes,
`https://jakeworcester-byte.github.io/pf-lessons/index.html` should contain the new
`PUBLISHED` date. If it does not after five minutes, say so in the report.

## 9. Report

End with a short plain-language summary: the week number and close date, total return
and the spread to SPY and QQQ, one line per position, any thesis status change, the
lesson (or "no lesson"), any new dividend, and anything flagged (price source
fallback, split, verification repair, skipped week, unanswered question for Jake).

## Milestones and phase changes

- **6-month review.** On the first run whose close date is on or after November 11,
  2026, also write a `## 6-Month Review: Phase 2` section after the 3-Month Review,
  modeled on its structure: bottom line first, scorecard against the success and
  failure criteria in `CLAUDE.md`, where the outperformance came from, what the
  experiment proved and did not. Update the review index line under
  `## Quarterly Reviews`. The site lists it automatically.
- **After the review, keep tracking.** Phase 2 positions are real holdings. Keep
  running the weekly update on them until Jake changes the holdings. Never invent,
  buy, sell, or propose trades in the files.
- **Phase 3 starts only when Jake sets it up** in an interactive session: new
  positions in `CLAUDE.md`, `tools/fetch_prices.py` (`POSITIONS`, entries, baselines),
  and the dashboard's `POS` block. Until then, from the 6-month review on, add one line
  to each weekly report noting that Phase 3 is waiting on Jake.
