# Browser Preview

[한국어](./browser-preview(kor).md)

The v0.2 reference pipeline turns the study's source files into a safe, self-contained browser preview:

```text
survey.qmd + greedyq.yml
            ↓
       QMD/YAML parser
            ↓
 normalized-survey.json
            ↓
         validator
            ↓
 preview-model.json + preview.html
```

## Start a preview

From the greedyQ repository root:

```bash
python3 -m greedyq preview examples/complete-study
```

The command validates and rebuilds the study before serving it at `http://localhost:4173/preview.html`. Stop the server with Control-C. Use `--port 4174` when the default port is occupied, and `--no-open` when you do not want greedyQ to open a browser automatically.

## What to test

Complete the questionnaire as a respondent, then use the researcher controls to test:

- every experimental condition;
- consent refusal and screening paths;
- required-field messages and numeric limits;
- conditional questions and hidden-answer clearing;
- Previous navigation and saved local preview state;
- completion, withdrawal, and technical-error endings;
- displayed labels and stored values in the debug panel;
- narrow/mobile browser widths.

The preview deliberately blocks network connections, form submission, and production redirects through its Content Security Policy. Answers are retained only in browser `localStorage` for preview resume testing and can be removed with Reset.

## Commands

```bash
# Check only; do not write generated files
python3 -m greedyq validate PATH_TO_STUDY

# Validate and create generated preview files
python3 -m greedyq build PATH_TO_STUDY

# Validate, build, serve, and open the preview
python3 -m greedyq preview PATH_TO_STUDY
```

A successful build writes `preview-model.json`, `preview.html`, `.greedyq/normalized-survey.json`, and `.greedyq/validation-report.runtime.json`. The source of truth remains `survey.qmd` plus `greedyq.yml`; do not hand-edit the generated preview files.

## Current boundary

This is a researcher preview, not a production respondent runtime. It does not create server sessions, write to Supabase, perform concurrency-safe randomization, validate Prolific participants, send completion redirects, or collect deployable responses. Those operations remain blocked even when the preview passes.
