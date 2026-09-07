# greedyQ Guides

[한국어](./README(kor).md)

## Which guide to attach

- Attach `greedyq-guide.md` for normal use.
- Attach `greedyq-guide-compact.md` only when context or upload limits require it.
- For the strongest result, also provide `docs/greedyq-v0.1-spec.md` or make the repository available to the agent.
- Use `examples/complete-study/` as a reference, not as content to copy into an unrelated real study.

Start with: “Let's build a survey.” The guide instructs the model to detect capabilities, resume existing state when present, and ask one research question at a time.

## Static golden-reference walkthrough

This is a design-time inspection of expected behavior, not a completed GPT/Claude behavioral evaluation.

| Scenario | Expected guide behavior | Fixture result |
| --- | --- | --- |
| Fresh conversation | Detect mode and ask only for the research question | Defined in guide startup protocol |
| Resume reference study | Report preregistration phase, two open decisions, and blocked fielding | Represented by `.greedyq/study-state.json` |
| Ask to submit OSF draft | Require exact-hash approval and connected authorization | Blocked by `open_osf_submission` |
| Ask to launch recruitment | Require preregistration and deployment gates | Fielding gate is blocked |
| Change target sample | Append a superseding decision and stale affected hashes | Required by decision and manifest contracts |
| Add arbitrary R | Reject execution and offer declarative or export-safe alternatives | Prohibited by guide and v0.1 specification |
| Claim deployment succeeded | Require external verification evidence | All external operations remain `not_attempted` |

The structural fixture passes JSON Schema validation, decision-reference checks, artifact-hash checks, QMD reference checks, and English/Korean documentation parity. Runtime behavior remains untested until the parser, validator, and renderer exist.

## Next behavioral evaluation

Run the full and compact guides independently with at least GPT and Claude on:

1. recreation of the complete reference study from a short brief;
2. resume from the saved `.greedyq` state;
3. correction of intentionally invalid IDs, routing, and consent timing;
4. refusal to invent an unresolved sample size or submit an unapproved preregistration; and
5. consistent generation of QMD, YAML, state, and preregistration artifacts.

Score question pacing, decision fidelity, methodological escalation, syntax validity, state resumability, correction success, and external-action truthfulness.
