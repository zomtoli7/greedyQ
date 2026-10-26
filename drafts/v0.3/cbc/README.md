# v0.3 CBC planning package

[한국어](./README(kor).md)

**Status: import and local browser preview implemented (`0.3-preview.1`).** v0.2 remains the supported live runtime. The fixed Python and browser implementations now validate CSV/XLSX and provide independent computer/mobile previews. Server-backed consent, allocation, choice/exposure storage, protected results and archive CSV now exist in the dedicated [CBC collection package](../../../CBC-COLLECT.md), verified locally. Cloud CBC acceptance, paid CBC fielding, mixed QMD authoring and native export remain separate gates. See [the working instructions](../../../CBC.md).

Start with the [draft specification](./spec.md), [golden research design](./golden-reference/README.md), and [blank table instructions](./templates/README.md).

## Researcher entry choices

After learning the research topic, ask: “How would you like to prepare the combinations people will compare?” Offer three equally valid routes:

1. Work with the AI to propose attributes, levels and choice tasks, then review them.
2. Download a blank CSV or Excel workbook, fill it independently, and return it.
3. Bring an existing design table from another workflow; review column mapping and restrictions before import.

Never assume AI generation merely because the researcher requested conjoint. If the researcher chooses a blank file, deliver the file and a concise explanation, save the paused state, and wait. Do not fill missing cells or silently redesign the returned table.

The generic [blank workbook](./templates/cbc-design-template.xlsx) has `Attributes` and `Design` sheets. CSV users receive [attributes-blank.csv](./templates/attributes-blank.csv) and [design-blank.csv](./templates/design-blank.csv). After the attribute inventory is confirmed, the future agent should provide a study-specific Design sheet whose attribute headers match that inventory. Generic `attribute_1` headings are placeholders, not approved study attributes.

## Delivery sequence

Steps 1–5 now have local implementation and verification. Step 6 still includes cloud acceptance, mixed authoring and native export before public profile activation.

1. Confirm v0.3 contracts and the golden fixture; review unresolved study choices.
2. Implement an independently tested Python reference importer and validator.
3. Port deterministic import/validation to the browser core; handle XLSX in fixed bundled code without macros or formula execution.
4. Implement the shared CBC renderer, independent desktop/mobile preview, and structural summary.
5. Add server-persisted block/task/alternative orders, consent/withdrawal handling and long-format export.
6. Exercise new study, paused-table return, resume, modification/fork, deployment/results and negative cases before enabling `cbc` in the public registry.

The existing [reference checker](../../../tools/check_cbc_reference.py) checks only this draft's tables and expected synthetic export. It is not the production importer and makes no design-efficiency or statistical-estimation claim.

## Decisions to make before fielding

The fictional reference fixes software examples, not a real study's hypotheses, population, sample size, estimator, ethics or statistical adequacy. Keep these researcher decisions open until explicitly confirmed. Partial-profile, adaptive conjoint, best–worst, rating-based conjoint and built-in inference are outside the first CBC slice.

The [draft fixture schema](./design.schema.json) validates planning metadata only.
