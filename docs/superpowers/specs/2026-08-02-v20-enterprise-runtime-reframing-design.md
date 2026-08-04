# V20 Enterprise Runtime Reframing Design

## Purpose

Version 20 reframes the preprint around the enterprise deployment problem that
motivated the architecture:

Enterprise AI is usually assembled along existing organizational and technology
boundaries such as business units, application development, testing, deployment,
cloud and server-farm infrastructure, operations, and security. Use-case
benchmarks can measure whether one agent solves one task, but they do not supply
a shared deployment architecture that tells these groups how rapidly changing
models, agents, frameworks, enterprise systems, and data should fit together.

The paper will present the Skill-Harness-Scaffold architecture and the external
data substrate as a set of shared organizational contracts for closing that
gap. Its central scientific claim remains the bounded, falsifiable Testable
Separability Conjecture rather than a claim of universal independence.

## Intended Contribution

The paper makes three distinct contributions:

1. An enterprise architecture that separates reusable business capability,
   runtime governance, physical execution boundaries, and enterprise data
   governance according to ownership and change cadence.
2. A precise Harness contract that connects fast-changing Skills and agent
   behavior to slower-changing infrastructure without loading every capability,
   policy, and data source into every model context.
3. Falsifiable protocols for testing whether capability growth and capacity
   growth remain separable inside a declared operating region.

The paper must keep architecture, mechanism, and empirical claim classifications
separate. It must not imply that a proposed control automatically proves
separability, safety, or business value.

## Approved Architecture

### Skill

A Skill is a versioned, reusable business capability and workflow asset. It
encodes the goal, typed inputs and outputs, applicability conditions, permitted
effects, tests, evidence requirements, and validated version needed to perform a
bounded enterprise task.

Skill-as-Code is the enterprise asset strategy. It stabilizes reusable knowledge
outside transient model context, reduces the opportunity for context corruption
and hallucination amplification, supports review and rollback, and gives the
Harness an artifact it can admit, test, trace, and govern. It does not make
probabilistic behavior deterministic by itself.

### Harness

The Harness is the runtime compiler and governor between business capability and
physical execution. It owns:

- selective context and Skill activation;
- tool, data, and multimodal composition;
- typed graph construction and path-level authorization;
- deterministic policy, budget, evidence, and release gates;
- model and agent evaluation;
- trace, replay, and provenance capture;
- multi-agent and multi-process coordination;
- binding accepted work to compatible Scaffold capacity.

The Harness extends vertically as new modalities, agent patterns, evaluators,
and coordination mechanisms emerge. It prevents every Skill author from
reimplementing those cross-cutting concerns.

### Scaffold

The Scaffold is the execution and control boundary supplied by enterprise IT,
platform, SRE, cloud, security, and operations teams. It exposes resources,
isolation, locality, identity, attestation, scheduling, and execution primitives
without interpreting business-specific Skill semantics.

Its non-functional responsibilities include:

- performance and latency;
- reliability and availability;
- manageability and observability;
- security and isolation;
- portability across platforms, model providers, and model versions;
- elasticity and capacity evolution;
- non-blocking scale from 0 to 100,000 concurrently admitted or active agents.

The 0-to-100,000 statement is a design target to be measured, not an achieved
result. The paper must define metrics for admission throughput, active-agent
capacity, queueing delay, p50/p95/p99 latency, saturation, failure and retry
rates, isolation violations, control-plane availability, cost per completed run,
and external-service backpressure.

### Data Substrate

The data substrate is stack-external rather than a fourth runtime layer. It is
independently governed by the CIO or equivalent enterprise data authority
because its stewardship, semantic standards, provenance requirements, and
change cadence differ from those of Skills and runtime infrastructure.

It provides:

- semantic joins across distributed enterprise systems;
- governed access and policy-aware routing;
- provenance and lineage;
- model, agent, Harness, and business telemetry integration;
- versioned intermediate representations that decouple source registries from
  output-oriented registries;
- on-policy access paths and off-policy indexing or maintenance loops.

The data substrate typically changes more slowly than Skills. Skills depend on
its contracts, not on ad hoc source-specific context assembly.

## Enterprise Ownership and Change Cadence

The paper will add a table with these rows:

| Object | Primary enterprise owner | Typical change cadence | Stable contract |
|---|---|---|---|
| Skill | Business product owner with AI/automation developers | Hours to weeks | Goal, typed I/O, effects, tests, evidence, version |
| Harness | AI platform/runtime and governance teams | Days to months | Admission, activated path, effects, binding constraints, postconditions, trace |
| Scaffold | Enterprise platform, cloud/server-farm, SRE, security, and operations | Weeks to years | Resource, isolation, locality, identity, attestation, execution |
| Data substrate | CIO/data authority with domain data stewards | Weeks to years | Semantic access, provenance, routing, lifecycle, intermediate representation |

Ownership is a responsibility model rather than a mandatory organization chart.
One team may implement multiple objects, but the contracts and decision rights
must remain distinguishable.

## Business and System Evaluation

The paper will explicitly separate two evaluation planes:

| Evaluation plane | Core question | Example measures | Primary evidence owner |
|---|---|---|---|
| Business/use-case | Does the Skill improve the intended work? | task success, requirement completion, quality, cycle time, human correction, business risk, unit economics | business owner and independent evaluator |
| System/runtime | Can the capability be admitted and operated predictably at enterprise scale? | contract validity, policy decisions, semantic invariance, throughput, tail latency, availability, isolation, replay, provenance, cost | Harness, Scaffold, security, SRE, and audit owners |

Neither plane substitutes for the other. A strong use-case benchmark does not
establish deployability, and a reliable runtime does not establish business
value.

## Responsibility-Boundary Comparison

The production-framework scorecard will be removed. Its replacement will compare
responsibility boundaries rather than assign completeness ratings to named
frameworks:

| Boundary | Business semantics | Runtime governance | Physical execution | Enterprise data |
|---|---|---|---|---|
| Skill | owns | declares requirements | does not own | consumes governed contracts |
| Harness | compiles activated capability | owns | binds but does not supply | mediates access and evidence |
| Scaffold | does not interpret | exposes enforceable facts | owns | enforces locality and network boundary |
| Data substrate | preserves domain meaning | supplies policy/provenance facts | does not schedule | owns semantic integration and routing |

The table's purpose is to make handoffs and non-ownership explicit. It must not
claim that existing products lack undocumented capabilities.

## Organizational Framing

Conway's 1968 observation that system structures reflect the communication
structures of the organizations that design them will be used only as historical
grounding. The paper will make a narrower interpretation of its own:

> For enterprise AI, architecture can serve as a shared organizational contract
> that makes communication, ownership, change cadence, and evidence obligations
> explicit across business and technology groups.

This interpretation must be attributed to this paper. The unverified quotation
"enterprise IT architecture is the enterprise communication protocol" must not
be presented as a quotation or attributed to another author.

## Scientific Core to Preserve

The following content must remain substantively and textually unchanged except
for cross-reference renumbering or grammar required by surrounding prose:

- P1 and all six conditions: typed closure, complete mediation, effect
  non-interference, shared-state isolation, resource invariance, and scheduler
  independence.
- P15's fixed proposal bank and multi-seed online experiment.
- P16's direct-reading, metadata, ablation, and shuffle controls.
- P17's preregistered dependency graph and artifact-change oracle.
- Existing estimands, falsification criteria, comparator-specific margins,
  controls, and evidence classifications.

The enterprise reframing may explain why these tests matter, but it must not
weaken their causal or statistical requirements.

## Literature Policy

### Historical exception

- Melvin E. Conway, "How Do Committees Invent?" (1968).

### Contemporary inclusion boundary

All contemporary references retained in v20 must have a verifiable publication
or release date on or after 2026-06-01. A 2026 year alone is insufficient.

Eligible academic anchors include, with the date taken from the arXiv API
`<published>` field rather than from a year or a local filename:

- arXiv:2606.12320, Five-Plane Reference Architecture, 2026-06-10;
- arXiv:2606.15242, composition risks, 2026-06-13;
- arXiv:2607.09175, GRACE, 2026-07-10;
- arXiv:2607.13070, falsifiable release gates, 2026-07-11;
- arXiv:2607.10534, Skill misalignment, 2026-07-12;
- arXiv:2607.13083, phantom guardrails, 2026-07-13;
- arXiv:2607.13285, Harness Handbook, 2026-07-14;
- arXiv:2607.13683, gated semantic quality-diversity, 2026-07-15;
- arXiv:2607.14004, continual optimizer evaluation, 2026-07-15;
- arXiv:2607.16345, AEVAL, 2026-07-16;
- arXiv:2607.15557, SkillCorpus, 2026-07-17;
- arXiv:2607.17598, progressive disclosure, 2026-07-20;
- arXiv:2607.17937, Skill failure under long contexts, 2026-07-20;
- arXiv:2607.18970, Skillware, 2026-07-21;
- arXiv:2607.20999, workflow-localized mechanism learning, 2026-07-23.

Tightening the date rule is not a licence to drop an eligible source. A source
whose verified date is on or after 2026-06-01 must be retained if any claim
depends on it; the five 2607 anchors above were dropped in the first v20 pass
and had to be restored because their removal left four claims — a phantom
oracle with no definition, two unmotivated §9.1 control conditions, a
first-person attribution, and a deleted novelty-narrowing disclosure —
stranded without support.

Ineligible by verified date, and therefore usable only as recorded design
motivation with no result of theirs asserted:

- arXiv:2605.23904, SkillOpt, 2026-05-22.

Eligible industry anchors include:

- AWS AgentOps, 2026-06-01;
- AWS SAP agentic ERP case, 2026-06-04;
- AWS hybrid-cloud agentic architecture, 2026-06-22;
- Anthropic managed-agent sessions, 2026-06-30.

Every retained citation must be audited against this boundary. Claims that
currently rely only on older work must be removed, rewritten as design
motivation, or supported by an eligible source.

## Paper Changes

The following sections will be rewritten:

- Abstract: lead with the missing enterprise deployment architecture, then give
  the four-object response and bounded research claim.
- Introduction: establish the cross-BU coordination problem, limits of
  use-case-only benchmarks, fast model/agent change, and shared-contract thesis.
- Origins: replace weak product analogy with enterprise architecture,
  organizational communication, and control/data/capacity motivations.
- Related Work: use only eligible contemporary sources plus Conway, and state
  novelty through responsibility boundaries rather than framework ratings.
- Discussion: develop adoption path, ownership tension, change cadence,
  non-functional requirements, and the business/system evidence split.
- Limitations: state that ownership assignments, 100,000-agent scale, semantic
  join effectiveness, and portability remain proposals requiring implementation
  and evidence.
- Conclusion: return to the enterprise communication and deployment problem,
  then state the testable next step without claiming completed experiments.

The Model, design mechanisms, protocols, and proposition classifications will be
edited only where needed to connect them to the enterprise framing or remove
ineligible citations.

## Figure and Builder Synchronization

Figure 8 and the document builder must use the same labels and responsibility
boundaries as the paper:

- Business capability: Skill-as-Code;
- Runtime governance: Harness;
- Execution and control boundary: Scaffold;
- CIO-governed semantic and telemetry foundation: data substrate.

The builder must create a new v20 PDF path and must not overwrite v19 or any
earlier artifact.

## Verification

The v20 work is acceptable only when all of the following pass:

1. The PDF exists at
   `academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf`.
2. V19 and all earlier PDFs retain their existing paths.
3. Every contemporary bibliography entry has a verified date on or after
   2026-06-01; Conway 1968 is the only historical exception.
4. Extracted text contains the enterprise problem statement, CIO ownership,
   business/system evaluation split, NFRs, and the 0-to-100,000 target.
5. P1 lists all six required conditions.
6. P15, P16, and P17 retain all named controls and falsification logic.
7. Figure labels, captions, section references, bibliography numbering, and
   builder metadata are synchronized.
8. Text scans find no unresolved citation keys, LaTeX artifacts, placeholders,
   or prohibited quotation attribution.
9. Every rendered PDF page is inspected for clipping, overlap, broken glyphs,
   unreadable tables, and inconsistent headers or page numbering.
10. An independent review finds no unresolved critical or major issue.

## Deliverables

- `docs/superpowers/specs/2026-08-02-v20-enterprise-runtime-reframing-design.md`
- `docs/superpowers/plans/2026-08-02-v20-enterprise-runtime-reframing.md`
- revised `academy/agentic-runtime-preprint/paper_source/main.tex`
- revised `academy/agentic-runtime-preprint/paper_source/references.bib`
- revised `academy/agentic-runtime-preprint/latex_to_preprint.py`
- revised `academy/agentic-runtime-preprint/CHANGELOG.md`
- new
  `academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf`
