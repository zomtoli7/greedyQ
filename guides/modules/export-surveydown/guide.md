# surveydown Export Module

[한국어](./guide(kor).md)

Generate a native surveydown-compatible project, including `survey.qmd` and `app.R`, as a first-class secondary output. The greedyQ Vercel/Supabase runtime remains primary. Use only public surveydown behavior and documentation; do not copy its source, tests, or internal fixtures.

Classify each feature as directly portable, generated, greedyQ-only, or unsupported. Validate displayed labels and stored values exactly. Tell the researcher in ordinary language about any behavior that changes or cannot be exported, and obtain approval for material differences. Recommend native surveydown for advanced customization beyond greedyQ’s supported runtime.

For every greedyQ-only control (`audio`, `video`, `rank_order`, `side_by_side`, `nps`, `timing`, `constant_sum`, `pick_group_rank`, `drill_down`, and confirmed `custom` controls), the exporter MUST replace the greedyQ `sd_question()` block with Surveydown's public `sd_question_custom()` interface. It MUST generate the matching Shiny output and reactive value binding in `app.R`; it MUST NOT leave an unknown greedyQ type in the exported QMD. Mark these conversions `generated_custom` and `generated_unverified` until the exported project has been reviewed in its native Surveydown runtime. Never claim exact behavioral equivalence merely because code was generated.

The compatibility report MUST list every converted question, every behavior that remains greedyQ-only, and every material mismatch. The generated project is a secondary output; the deterministic browser runtime remains the primary greedyQ runtime.
