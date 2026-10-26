# CBC capability module — v0.3

[한국어](./guide(kor).md) · [简体中文](./guide(zh-CN).md)

CBC is an insertable module in an ordinary greedyQ survey, not a separate kind of survey. Keep existing ordinary questions in survey.qmd. When the researcher says “put CBC tasks here,” add one module page at that position. Ordinary questions before and after it continue to use the fixed question parser and renderer. Do not require the researcher to prepare separate pre/post questionnaires or learn internal before/after arrays.

Ask whether to collaborate with the AI on design, fill a blank CSV/XLSX table, or import an existing design. Persist that choice and wait for confirmation of attributes, levels, alternatives, tasks, blocks, neither and ordering. Never invent methodological approvals. For blank-table handoff, record expected files and the next question; preserve the pinned version when the researcher returns.

The first mixed-module contract supports one CBC sequence in a linear survey. Put the module on its own page; split a page at the insertion point if necessary. Do not silently approximate multiple CBC sequences, page branching across the module or a separate experimental randomization plan; explain these boundaries before changing a design. Question-level conditional visibility and ordinary supported controls remain available.

```r
sd_cbc(name = "course_choices", design = "study.design.json")
```

Use greedyq/cbc_authoring.py for source-only authoring handoffs, resume, fork and explicit version upgrades; use greedyq/cbc_flow.py to compile ordinary QMD pages around the module. collection.json records consent and explicit deployment/fielding approvals separately. It is not a second questionnaire. The canonical collection renderer, additive 010_cbc_module.sql and guarded CBC RPCs handle sequencing, acknowledged saves, completion and withdrawal. Do not write replacement control HTML or call the generic v0.2 writer for module sessions.

A normal build detects sd_cbc and produces the integrated dual preview and private preparation package. Native surveydown CBC export remains explicitly unsupported; never remove the module and export an apparently complete questionnaire. Actual recruitment still requires approved participant information, research-team contact, data plan and fielding decisions. Local and cloud synthetic tests do not provide these approvals.
