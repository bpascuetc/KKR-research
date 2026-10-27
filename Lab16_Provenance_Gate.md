# Lab 16 — Provenance Gate

Bernat Pascuet Cuesta · FIN 43900 · October 27, 2026

## Question and result

On the day I would have traded, what did this data actually say—and how much of what I see now came later?

For the fictional training table, my decision date is March 31, 2026. The filter reproduces every supplied known answer. A separate April 15 run makes the as-of signals equal the naive signals for all three tickers. These are training-index changes, not stock returns or evidence of a profitable trading strategy. Code and this write-up were AI-enhanced; executions below were performed by Codex.

## Reproduce

Keep these files together, open a terminal in this folder, and run:

```bash
python3 asof.py
```

Only the Python standard library is required. The table and decision date are editable at the top of the file. All printed results are computed from those inputs. Saved runs are [March 31](output_2026-03-31.txt) and [April 15](output_2026-04-15.txt); [validation](VALIDATION.txt) records the executed checks.

To repeat the date experiment, change `DECISION_DATE` to `"2026-04-15"`, run again, then restore `"2026-03-31"`. The saved code retains March 31. The assistant ran both dates; this does not establish that a partner's separate file was run.

## Ordered row funnel

| Step | Count removed | Row numbers | Remaining |
|---|---:|---|---:|
| Input | — | — | 12 |
| No ticker: quarantine | 1 | 11 | 11 |
| Exact duplicate | 1 | 7 | 10 |
| Published after March 31 | 3 | 3, 8, 10 | 7 |
| Older publication replaced | 1 | 2 | 6 |

Exact duplication compares ticker, measured month, publication date and index; the row identifier is excluded. Otherwise rows 6 and 7 would incorrectly count as different observations.

## Retained as-of panel

| Row | Ticker | Month measured | Published on | Index |
|---:|---|---|---|---:|
| 1 | AAA | 2026-01 | 2026-02-10 | 101.0 |
| 4 | AAA | 2026-02 | 2026-03-25 | 103.0 |
| 5 | BBB | 2026-01 | 2026-02-10 | 98.0 |
| 6 | BBB | 2026-02 | 2026-03-10 | 97.0 |
| 9 | CCC | 2026-01 | 2026-02-10 | 110.0 |
| 12 | CCC | 2026-02 | 2026-03-10 | 111.0 |

## Signal proof

Signal = `(latest index / previous month's index - 1) * 100`.

| Ticker | As-of March 31 | Naive: latest publication without date cutoff |
|---|---|---|
| AAA | +1.98% (February): 103/101 − 1 | +5.83% (March): 109/103 − 1 |
| BBB | −1.02% (February): 97/98 − 1 | −5.15% (March): 92/97 − 1 |
| CCC | +0.91% (February): 111/110 − 1 | +1.82% (February, revised): 112/110 − 1 |

The naive comparison still removes the blank ticker and duplicate and selects the latest vintage per ticker/month. It deliberately omits the publication-date cutoff. By April 15 all publications in this table are available, so both approaches retain rows 1, 3, 4, 5, 6, 8, 9, 10 and give the same signals. The latest measured month is March for AAA/BBB and February for CCC.

## How rule 4 works

`filter_asof` first removes publications after the cutoff. Then `latest_vintages` groups observations with `key = (row[1], row[2])`, meaning ticker and measured month. `previous = latest.get(key)` retrieves the vintage already saved for that pair. If none exists, or the new row has a later publication date, `latest[key] = row` saves it. ISO dates in YYYY-MM-DD form sort chronologically.

For AAA February, row 2 is first saved, then row 4 replaces it because March 25 is later than March 10 and both are eligible. Keeping row 2 would produce +2.97%, which fails the known answer. For CCC February, row 10 has already been removed because April 5 is after March 31, so row 12 survives. Selecting the newest revision before filtering availability would incorrectly lose CCC's eligible February observation.

Dates on the cutoff are included. Conflicting values for the same ticker/month/publication date cause an explicit error rather than an arbitrary choice. Signals require adjacent measured months and a nonzero previous index; otherwise they print unavailable.

## Point-in-time explanation and reflection

The month measured is event time: February spending describes February activity. Publication time is when that observation becomes available. A revision is a later publication changing an already measured month. February CCC therefore has two vintages: 111 available March 10, and 112 available April 5. On March 31 only 111 is knowable.

Look-ahead bias occurs when a historical decision uses information published after its decision date. AAA's naive +5.83% incorporates March's 109, published April 10. It appears stronger than the +1.98% latest knowable change on March 31. It describes a different, later interval and cannot be used as a March 31 signal.

For AAA, rule 3 has the largest effect on the comparison because it excludes the not-yet-published March observation. Rule 4 also matters: it corrects February from 104 to the already available revision of 103. Which row matters most depends on the ticker and decision rule; future information does not always increase a signal, as BBB demonstrates.

A backtest using the naive column could claim it selected stronger AAA growth, avoided BBB's deterioration, or observed CCC's revised improvement at the decision date. Those observations were unavailable then. The table alone does not define trades, thresholds, execution prices or investment returns, so it cannot establish a performance gain. Applying the publication gate is necessary before evaluating such a strategy.

## Personal completion and GitHub checkout

Technical proof is complete. Bernat confirms that he answered the AI quiz and completed the no-AI code explanation to his partner, including the partner question activity. These are student-confirmed activities; the exact quiz answers and partner question/response were not supplied here.

Bernat confirms sending his own file to his partner. The partner's actual `Downloads/asof.py` was supplied and checked by Codex: March 31 matches the known answer, and April 15 makes as-of and naive signals equal. The original partner file was unchanged. See [partner-file execution evidence](partner_file_verification.txt). Its extra bond-yield interpretation is inappropriate for the fictional card-spend index and should be removed.

Bernat reports that his partner reviewed the work and said everything looked good. The [partner review and response](PARTNER_DISCUSSION.md) records that actual reported feedback and expands Bernat's response with the verified publication-timing explanation, rule-4 logic, AAA example and reflection. The expanded technical explanation is AI-enhanced writing; it is not attributed to the partner as additional feedback. Bernat subsequently confirms personally running his partner's file and completing the oral reflection. His quiz, no-AI code explanation, file exchange, personal partner-file run and oral reflection are now student-confirmed. The exact dates/results of his personal run were not separately supplied; the saved two-date numerical verification records Codex execution.

Thursday's ALFRED series is a preview and is outside this fictional-table exercise.

Upload this folder's files to GitHub, then use the real GitHub links to `Lab16_Provenance_Gate.md` and `asof.py` for the individual checkout, with the saved output files as supporting evidence. Bernat handles upload and submission; neither has been performed here.

I am a student, not a financial professional. This document was prepared for FIN 43900 (AI Finance Applications, Purdue) as a class learning exercise. It is not professional investment research or financial advice. I used OpenAI Codex to help with research, analysis, calculations, and drafting. Any remaining errors are my own.
