# greedyQ Research Framing

[한국어](./research-framing(kor).md)

**Status:** working conceptual framing for a future white paper

## Proposed title

**greedyQ: A Specification-Driven AI-Native Application for Online Academic Research**

Proposed subtitle:

**Turning General-Purpose Generative AI into a Reproducible Research Agent**

## Central definition

> greedyQ is a specification-driven, AI-native application for online academic research.

> Rather than implementing the application itself in conventional source code, greedyQ specifies how a general-purpose generative AI agent should instantiate and operate the application.

The portable greedyQ Markdown, schemas, checkpoints, templates, and conformance fixtures collectively form an **agent-executable application specification**.

The term “AI-native application” is intentionally not presented as unique to greedyQ. The proposed contribution is the more specific architecture: distributing substantial application behavior as a portable normative specification that a capable general-purpose GenAI can execute while remaining accountable to deterministic artifacts and conformance tests.

## Architectural separation

```text
greedyQ
agent-executable application specification
                    |
                    v
       general-purpose host GenAI
         (GPT / Claude / Gemini / ...)
                    |
                    v
        instantiated greedyQ research agent
                    |
                    v
                researcher
                    |
                    v
       research-design artifacts
                    +
       executable survey application
```

greedyQ itself is not an agent. The relation is:

```text
greedyQ specification + host GenAI = greedyQ research agent
```

The research agent is an instantiated application process. It asks questions, applies research reasoning, records approvals, and produces artifacts. The respondent-facing survey is separate software produced by that process.

## Three-layer positioning

### Architecture

**Specification-driven AI-native application.** Executable application behavior is defined and distributed through an agent-executable specification rather than being exhausted by a conventional source-code implementation.

### Domain

**Online academic research.** The domain includes research questions, study design, measurement, consent, governance, experiments, randomization, respondent collectors, data plans, preregistration, survey execution, and fielding.

### Implementation

**greedyQ.** The concrete application of this architecture to reproducible online academic research.

## Central research question

> Can a research methodology and workflow be packaged into a portable specification that turns an arbitrary capable general-purpose AI into a domain-specific research application?

This question shifts evaluation away from whether a particular chatbot can act as a helpful collaborator. It asks whether a normative application specification can produce sufficiently consistent, auditable, and useful application behavior across heterogeneous host models.

## Portability and conformance hypothesis

greedyQ remains greedyQ when instantiated by different capable host models because identity is anchored in the normative specification, not in one model vendor or interface. Surface interaction may differ; required decisions, prohibited assumptions, artifact contracts, and deterministic validations should remain invariant.

A future validation study can independently provide the same tagged greedyQ specification and study brief to GPT, Claude, Gemini, and other capable systems, then evaluate:

- profile and module selection;
- question sequence and decision escalation;
- preservation of researcher authority;
- final artifact validity and semantic equivalence;
- handling of unresolved information;
- refusal to claim unverified external actions;
- participant-flow equivalence;
- reproducibility across repeated runs;
- host-specific interface differences;
- conformance failures that deterministic validators can detect.

The goal is not byte-for-byte identical prose or UI. The relevant invariants are research decisions, participant rights, study semantics, stored values, lifecycle behavior, and declared output contracts.

## Boundary of the claim

The specification does not eliminate conventional code. Exact preview, runtime, database, validation, and export templates may contain code. The architectural claim is that the application’s domain workflow, decision logic, normative behavior, and artifact-generation contract are primarily defined and distributed as an agent-executable specification. Empirical validation is required before making claims about cross-model equivalence, reliability, or superiority.
