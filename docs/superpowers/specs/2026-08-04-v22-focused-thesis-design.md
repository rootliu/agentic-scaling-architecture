# v22 Focused Thesis and Evidence Redesign

## Purpose

Version 22 will turn the current broad architecture manuscript into a focused
systems research preprint. The paper will preserve the complete
Skill-Harness-Scaffold architecture and its external data substrate, but it
will make one scientific claim central:

> Within a declared operating region, capability growth and capacity growth
> can remain empirically separable when logical control and admission are
> completely mediated by the Harness, physical execution and isolation are
> supplied by the Scaffold, and the cost of maintaining those conditions stays
> within a preregistered budget.

The responsibility contracts are the mechanism that makes this claim
observable and falsifiable. They are not additional independent scientific
theses.

## Research Question and Contribution

The primary research question is:

> Can a runtime add and activate independently deployable capabilities without
> materially changing capacity response, while scaling capacity without
> materially changing capability semantics, at an acceptable enforcement cost?

The paper will make three contributions:

1. A responsibility model that separates reusable capability, logical runtime
   governance, physical execution, and governed data access.
2. A cost-aware, falsifiable separability hypothesis with an explicit estimand,
   experimental unit, decision rule, and inconclusive outcome.
3. An evidence architecture that links admission decisions, execution facts,
   data provenance, semantic verification, and termination to the hypothesis.

Architecture mechanisms, empirical hypotheses, and measured results must remain
visibly distinct. The paper reports a research design and reference
architecture; it does not claim validation by a completed runtime experiment.

## Canonical Responsibility Contracts

### Skill

A Skill is a versioned capability contract. It owns bounded task semantics,
typed inputs and outputs, applicability conditions, permitted effects, tests,
and evidence requirements. Registry cardinality is not capability growth.
Capability growth requires activation of independently deployable behavior that
can affect an admitted execution path.

### Harness

The Harness is the logical control and admission boundary. It owns selective
activation, graph construction, path-level authorization, policy and budget
checks, evidence requirements, release gates, trace assembly, and binding of
accepted work to compatible capacity.

The Harness may request isolation and resources, but it does not supply their
physical enforcement.

### Scaffold

The Scaffold is the physical execution and isolation boundary. It owns resource
allocation, scheduling primitives, process or container isolation, locality,
identity binding, attestation, execution telemetry, and capacity behavior.

The Scaffold may expose enforceable facts, but it does not interpret
business-specific Skill semantics or decide logical admissibility.

### External Data Substrate

The data substrate is independently governed by a data governance authority,
typically a CIO or equivalent with domain data stewards. It owns semantic
access contracts, provenance, routing, lifecycle, and source-to-evidence
transformation. It is external to the three runtime layers.

This ownership model describes decision rights and evidence obligations, not a
mandatory organization chart.

## Primary Hypothesis

### P1: Cost-Aware Bounded Separability

P1 will be stated as an empirical hypothesis rather than a theorem-like
consequence of its assumptions.

Let:

- `c` denote an activated capability configuration;
- `s` denote a Scaffold capacity configuration;
- `R(c, s)` denote a preregistered vector of runtime responses;
- `Q(c, s)` denote capability-semantic outcomes;
- `E(c, s)` denote enforcement overhead;
- `Omega` denote the declared operating region.

`R` may include admission throughput, queueing delay, tail latency, saturation,
failure and retry rates, and cost per completed run. `Q` may include typed
postconditions, permitted-effect compliance, task-specific semantic invariants,
and evidence completeness. `E` includes control-plane latency, policy and
verification cost, trace volume, and reserved isolation capacity.

P1 asks whether, within `Omega`:

- capacity changes may have a Scaffold main effect on `R`;
- activated capability growth has no practically material interaction with the
  capacity response beyond preregistered margins;
- capacity growth has no practically material effect on `Q` beyond
  preregistered margins; and
- the required mediation, isolation, and evidence controls can be maintained
  within a preregistered enforcement budget.

The paper must not require a zero Scaffold main effect. The primary capacity
estimand is the capability-by-Scaffold interaction in `R(c, s)`, not an
undifferentiated difference between runs.

## Conditions and Their Status

The six existing conditions remain:

1. typed closure;
2. complete mediation;
3. effect non-interference;
4. shared-state isolation;
5. resource invariance;
6. scheduler independence.

They will be presented as maintained experimental conditions and measured
engineering obligations, not premises that logically prove P1. The experiment
must report:

- whether each condition was instrumented;
- instrumentation coverage;
- observed violations and uncertainty;
- the cost of maintaining the condition; and
- any operating-region exclusions caused by failure to maintain it.

The result is `inconclusive`, rather than accepted or rejected, when coverage is
insufficient to distinguish no observed violation from an unobserved violation.

## Experimental Design

### Experimental Unit

The experimental unit will be a cluster-period or system epoch, not an
individual request. Capacity and capability interventions affect shared
schedulers, caches, queues, registries, and control-plane state, so
request-level randomization would create interference.

The proposed design is a randomized crossover across cluster-periods:

- assign capability configurations and Scaffold configurations by period;
- use washout or state-reset rules for caches, queues, and generated artifacts;
- balance order effects and time trends;
- repeat across seeds, workloads, and failure regimes;
- use cluster-aware uncertainty estimates; and
- record exclusions before outcome inspection.

### Capability Intervention

Capability growth must activate behavior, not merely register inactive Skills.
The intervention will use capability bundles that:

- are independently versioned and deployable;
- participate in sampled admitted paths;
- exercise distinct tools, data contracts, or typed transformations;
- preserve a fixed workload mix for comparison; and
- expose activation frequency and path composition in the trace.

An inactive-registry-cardinality stress test may remain as a secondary
control-plane robustness test, but it is not evidence for capability-capacity
separability.

### Capacity Intervention

Capacity interventions may vary worker pools, execution slots, accelerator
allocation, queue partitions, or equivalent Scaffold resources. The Harness
policy, activated capability distribution, workload, external-service limits,
and data snapshots must be held fixed or explicitly modeled.

### Decision Rule

The paper will distinguish:

1. the latent property of interest;
2. observable metrics;
3. instrumentation coverage;
4. practical equivalence or non-inferiority margins; and
5. the final decision.

Possible outcomes are `supported within Omega`, `falsified within Omega`, and
`inconclusive`. No result will be generalized outside the tested operating
region.

## Secondary Subsystem Hypotheses

The current data-intermediate-representation and proposal-selection hypotheses
will no longer compete with P1 for the paper's center.

- P15-P17 will be renumbered continuously if retained.
- Their strongest controls may be summarized as secondary subsystem protocols.
- Claims without adequate baselines or an executable artifact will move to
  future work.
- Withdrawal history for P2-P14 will be removed from the body. Version history
  belongs in the changelog or an appendix only when scientifically necessary.

The fixed proposal bank, direct-reading and metadata controls, preregistered
dependency graph, and artifact-change oracle may be preserved as reusable
protocol details, but the abstract and conclusion will not present them as
coequal main contributions.

## Evidence and Threat Model

The evidence model will separate:

- admission and policy decisions from execution enforcement;
- declared contracts from observed runtime facts;
- zero observed violations from evidence of absence;
- semantic outcomes from infrastructure outcomes; and
- measurement artifacts from implementation artifacts.

The artifact statement will say that the paper currently provides no runtime
implementation, experimental dataset, or measurement artifact. It will not say
that the repository contains no code, because the document builder and figure
generation code exist.

External content, retrieved data, tool output, and dynamically derived
sub-agent instructions are untrusted inputs. They may influence bounded task
content only after parsing and policy mediation; they cannot redefine
authority, permissions, release criteria, or the parent termination contract.
This resolves the current conflict between an external-content threat model and
dynamic sub-agent derivation.

## Novelty Boundary

The related-work section will remove the artificial `2026-06-01` inclusion
boundary. It will position the contribution against both classical systems
ideas and contemporary agent-runtime work.

Required classical boundaries include:

- reference monitors and complete mediation;
- capability security and least authority;
- information hiding and modular contracts;
- policy-mechanism separation;
- control-plane and data-plane separation;
- autonomic control and MAPE-K;
- software quality models such as ISO/IEC 25010; and
- queueing, interference, and resource-isolation literature.

The novelty claim must be narrow: the paper composes these established ideas
into an agentic-runtime responsibility model and makes capability-capacity
separability, including enforcement cost, an explicit falsifiable systems
hypothesis. It does not claim to invent isolation, mediation, modularity, or
runtime governance.

Contemporary sources will be selected for direct relevance and verifiability,
not recency alone. Framework comparisons will describe responsibility
boundaries and documented mechanisms, not assign unsupported completeness
scores.

## Prose and Structure

The revision will:

- lead the abstract with the research problem, hypothesis, mechanism, and
  evidence status;
- make the introduction converge on one research question;
- move architecture detail after the hypothesis and responsibility model;
- compress defensive and meta-level prose by approximately 15-20 percent;
- replace repeated "does not prove" formulations with one explicit evidence
  taxonomy and localized limitations;
- remove unsupported `0-100,000 agents` scope claims, retaining any such value
  only as a labeled experimental setting;
- use "independent data governance authority, typically CIO or equivalent"
  instead of organization-specific `CIO-governed`; and
- give each abbreviation in the abstract, body, figures, and tables an
  expansion at first use or in a local legend.

The conclusion will state what a future implementation and experiment must
show, without presenting architectural plausibility as empirical evidence.

## Figure Redesign

All figures will have self-contained captions that state what is shown, why it
matters, and whether the figure is architecture, protocol, or proposed
measurement design.

### Overview Figure

The opening overview will show the paper's single argument:

`Capability change -> Harness contract -> Scaffold capacity`

with the external data substrate supplying governed evidence and a measurement
plane observing semantic outcomes, capacity response, condition coverage, and
enforcement cost. It will distinguish claims from mechanisms visually.

### Figure 4: Bounded Multi-Agent Execution

Redraw as:

`Main agent -> Bounded sub-agents -> Verifier / semantic join -> Termination gate`

Show inherited authority, bounded contracts, evidence return, and parent-owned
termination without dense bidirectional arrows.

### Figure 5: Governed Data Evidence

Redraw as:

`Data authority -> Resolved contract -> Isolated fetch -> Evidence bundle`

Place policy/provenance annotations in aligned lanes. Avoid prose-heavy boxes.

### Figure 6: Control and Execution Lanes

Use parallel logical-control, physical-execution, and evidence lanes with
straight orthogonal connectors. Remove crossed connections.

### Figure 8: Falsification Matrix

Replace the crowded flow diagram with a matrix whose columns are:

`Hypothesis | Intervention and control | Evidence plane | Falsification or
inconclusive condition`

P1 receives the dominant row; secondary protocols are visually subordinate.

Tables and formulas will be rebuilt so that no raw textual operators such as
`sum over`, `bigwedge`, or `at least` leak into the PDF. Dense tables may split
across pages with repeated headers.

## Versioning and Build

- Set the renderer version to `v22`.
- Generate
  `academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf`.
- Preserve the v21 PDF byte-for-byte and verify its checksum before and after.
- Update version-specific rendering tests for v22 while retaining a regression
  assertion that v21 is not overwritten.
- Add a v22 changelog entry without rewriting historical entries.
- Fix the orphaned subsection heading, excessive whitespace, broken URL wraps,
  formula rendering, and any page overflow revealed by the new layout.

## Obsidian Synchronization

The authoritative vault notes will be updated after the paper stabilizes:

- `00_Index.md`;
- `16-评审与精读总入口.md`;
- the latest paper review note; and
- the figure/evaluation specification note.

The synchronization will record the v22 thesis, responsibility corrections,
experimental unit, estimand, evidence states, figure vocabulary, and final PDF
path. Empty notes will not be treated as evidence. Existing archival notes will
not be silently rewritten to match the new conclusion.

## Verification

The revision is acceptable only when:

1. v22 builds and all rendering tests pass.
2. The v21 PDF checksum is unchanged.
3. Extracted text contains no unresolved LaTeX commands, placeholders, broken
   references, raw formula-control words, or unexplained abbreviations.
4. P1 states the operating region, response functions, interaction estimand,
   experimental unit, enforcement budget, and three-way decision rule.
5. Capability growth is operationalized by activated behavior.
6. Harness and Scaffold ownership is consistent in prose, figures, and tables.
7. The related-work section contains the required classical boundaries and
   makes a narrow novelty claim.
8. Every figure has a self-contained caption and all rendered labels fit.
9. Every PDF page is rendered to an image and inspected for clipping, overlap,
   whitespace imbalance, broken glyphs, orphan headings, and unreadable text.
10. The paper and Obsidian worktrees contain only intended changes, pass
    `git diff --check`, and are committed and pushed independently.

## Deliverables

- this approved design;
- a task-level v22 implementation plan;
- revised paper source and references;
- revised renderer and rendering tests;
- a new v22 PDF with v21 preserved;
- synchronized Obsidian review and index notes; and
- pushed commits for both repositories.
