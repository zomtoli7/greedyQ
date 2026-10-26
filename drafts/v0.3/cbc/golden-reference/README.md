# Golden reference design: online course subscriptions

[한국어](./README(kor).md)

**Design fixture only; no live study, approved sample or implemented CBC runtime.** This independently authored fictional example tests the future `greedyQCBC` contract. It is not a D-efficient design or a validated instrument.

## Scenario

Compare hypothetical online course subscriptions. The demonstration population is adults familiar with online courses; eligibility wording, geography, language, sample size, consent, retention, incentives and estimator remain decisions for an actual researcher. Do not invent an institution or ethics approval. No personal or sensitive attributes are needed in the fixture.

| Attribute | Levels |
| --- | --- |
| Monthly fee | GBP 10, GBP 20, GBP 30 per month |
| Course format | Recorded video, written lessons, live online class |
| Tutor support | No tutor support, email support, live chat support |
| Access after subscription | 1 month, 3 months, 12 months |

Each task offers two full-profile unlabeled alternatives and “I would choose neither plan”. Two blocks contain four tasks each: eight task definitions and sixteen ordinary profile rows in total. A respondent is proposed to receive one block with equal allocation probabilities, four tasks, randomized task order and once-per-task randomized ordinary alternative order. None stays last. These are software fixture choices, not recommendations for statistical precision or respondent burden.

## Proposed participant journey

1. Welcome, approved participation information and consent.
2. Confirm relevant course experience; use a separately reviewed ending if ineligible.
3. Explain the four attributes, prices and what none means; include a non-scored practice example if the researcher confirms it.
4. Assign one block after consent, then present its four choice tasks with stable recorded orders.
5. Optional usability feedback, completion, or voluntary withdrawal.
6. Review protected results and export observed alternatives/choices with their design version.

The demonstration has no live collector credentials or completion codes. Existing direct/Prolific core contracts must be reused when implemented; no new payment or recruitment is authorized.

## Files and expected data

- `study.design.json`: proposed decisions, explicit `fielding_approval=false`, design-only status, block/order/none rules and open estimator.
- `design/attributes.csv`: twelve level rows with stable IDs and display labels.
- `design/design.csv`: sixteen ordinary profile rows, keyed by block/task/alternative.
- `design.manifest.json`: original-file hashes and expected dimensions. Statistical efficiency is not established.
- `expected/choice-data-long.csv`: twenty-four **synthetic** rows for two fictional respondents, one per block. Each has four tasks and three alternatives per task. Exactly one alternative is selected; none rows have blank attribute cells. This expected fixture uses source order deliberately to make joins inspectable; it is not an observed random draw or real respondent data.
- `expected/scenarios.json`: future acceptance plan and explicit implementation gaps.
- `survey.qmd.draft`: proposed authoring sketch, not accepted by v0.2.

The two blank CSVs and blank workbook are in [templates](../templates/README.md). The draft checker validates structure, code references, hashes and synthetic chosen-row joins; it does not generate a design or estimate preferences.

## Required future simulations

Both blocks; AI-assisted and independently filled design routes; saved conversation → download → return in another host; malformed/partial/duplicate rows; Unicode and string ID preservation; reviewed prohibited combinations; fresh/resumed task and alternative orders; keyboard/mobile selection; none versus unanswered; previous/reload; interrupted save and retry; simultaneous submissions; consent refusal; withdrawal erasure of choices/exposures; real/test isolation; protected results/long CSV; approved design revision requiring a new version; fork without copying respondent data; explicit native-export limitations.

No automatic sample-size or model choice is frozen. A future preregistration draft must describe the approved choice design, block assignment, ordering, exclusions, missing data, estimand and analysis while visibly retaining unresolved commitments.

## Next implementation checkpoint

Implement the Python reference import/normalized design schema against this fixture and invalid examples. Then implement the same fixed browser contract and renderer; do not declare this planning package a functioning conjoint survey.
