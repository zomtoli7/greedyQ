# Fill a CBC design table

[한국어](./README(kor).md)

These are blank **v0.3 planning templates**, not a working v0.2 questionnaire. You can stop after downloading them and return to the AI when ready. Ask for help with any field rather than guessing a code.

## Choose a file

- Excel: download [cbc-design-template.xlsx](./cbc-design-template.xlsx). Fill both `Attributes` and `Design`.
- CSV: download [attributes-blank.csv](./attributes-blank.csv) and [design-blank.csv](./design-blank.csv). Return both files.

Blue-tinted cells are empty input space, not generated study content. The workbook has no macros or formulas. Add rows as needed; twenty formatted blank rows are not a study-size limit. Keep the sheet names and first-row headings. Do not insert instructions, extra tables or merged cells into the input tables.

## 1. Describe attributes and levels

An **attribute** is a feature people compare, such as monthly fee. A **level** is one possible value, such as “GBP 10 per month”. One row describes one level:

| attribute_id | attribute_label | level_id | level_label |
| --- | --- | --- | --- |
| monthly_price | Monthly fee | p10 | GBP 10 per month |
| monthly_price | Monthly fee | p20 | GBP 20 per month |

This is an illustration only; no example rows were inserted into your blank file. Use short stable codes in `_id` columns. Labels are the words participants will see and can be in the survey language. Do not reuse the same level code twice within one attribute.

## 2. Describe the comparisons

The AI should replace `attribute_1`…`attribute_4` with your confirmed attribute IDs before you fill the Design table. If you need another number of attributes, ask for a matching blank file. Do not leave spare placeholder columns.

- `block_id`: which set of questions a person receives. If everyone receives the same set, use one block such as `main`.
- `task_id`: which comparison within that block. Two rows sharing a block and task are two alternatives in one comparison.
- `alternative_id`: the stable name of an alternative, such as `a` or `b`. It is not necessarily its final left/right position.
- Each attribute column: the corresponding **level code**, not an unreviewed display phrase.

For two alternatives, write two ordinary rows for each task. Repeat attribute values where needed; do not merge cells. “I would choose neither” is configured with the AI separately and should not be entered as a made-up profile row. Missing cells do not mean “none”.

## 3. Return the file and review it

Send the completed files to the AI and say:

> I filled the CBC design table. Read it without changing it. Show the attributes, levels, number of blocks and comparisons, and one example comparison. Point out incomplete or ambiguous cells one issue at a time. Ask before changing anything.

You can also ask the AI to propose a table first. It must still explain its choices and obtain your confirmation. A table that passes file checks is not automatically an efficient or statistically adequate design. Review the design method, sample and analysis separately before collecting data.

The provided files and the [filled reference tables](../golden-reference/design/design.csv) are prepared now. Browser import, CBC display and real collection remain future v0.3 work.
