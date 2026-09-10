## 01. Contract-Centered Agentic Runtimes

Allow 25 minutes plus discussion. Internal v29 revises the existing arXiv manuscript. The new contribution is an executable data boundary with finite validation, not a completed production system or a conference acceptance.

- [Existing arXiv / 已发表前版](https://arxiv.org/abs/2608.27086)

## 02. Task success does not establish system manageability

Introduce a quarterly report. A plausible final number can still rely on the wrong period, unauthorized evidence or a stale artifact. Ask both whether the task was completed and whether its execution met the contract.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 03. v29 makes the data boundary executable

The three contributions have different evidence levels. The architecture is a design; the data reference model executes; P1 remains an empirical hypothesis. Do not call the complete architecture validated.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 04. Four responsibility objects; three runtime layers

Skill declares business capability. Harness admits and binds it. Scaffold supplies execution boundaries and resources. The external substrate governs data semantics. This is a responsibility model, not a mandatory four-team organization chart.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 05. P1: can capability and capacity be separated?

Explain the 2×2 experiment. A capacity main effect is expected and does not establish P1. Test whether the capability effect changes across capacity, while semantics remain non-inferior and control cost stays within budget. Margins must be decision-derived.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 06. A minimal counterexample: same columns, different meaning

This is not merely an SQL type error. Schemas and field names can agree while units, entity scope and periods differ. The proposal makes those constraints explicit rather than relying on model inference at query time.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 07. Data Wiki, Theme Wiki and IR answer different questions

Data Wiki describes sources. Theme Wiki specifies outputs. IR declares how a task may connect them. Summaries aid discovery, but canonical sources remain authoritative. IR means Intermediate Relation; the execution ticket is a separate resolved object.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 08. Turn 5W1H+Which into checkable conditions

The seven question words are not seven inventions. The technical work links them to trusted inputs, runtime checks and explicit failures. Why is an approved rationale, not a model-generated causal proof. The reference model implements simplified checks, not multi-source joins.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 09. From candidates to execution tickets to evidence

Discovery is not authorization. Search returns candidates; it cannot grant tools or source privileges. Recheck versions and policy immediately before execution, then bind returned evidence. Fallback can only use already permitted paths.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 10. Revocation during queuing: is admission enough?

Time order matters: admission at t0, revocation at t1, read at t2. The old ticket must not authorize a later read. Revalidation and reading need a shared linearization point relative to updates. Bytes released before revocation cannot be retracted; publication is a separate check.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 11. Change impact follows explicit dependencies

Dependency traversal is a standard algorithm. The research question is whether semantic, policy, operator, theme and artifact dependencies can be captured completely and reduce real revalidation work. The current model uses a conservative global epoch, not fine-grained optimization.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 12. An existing file is not a verified deliverable

Teams often equate file generation with completion. Examples include a same-named old deck, an unexecuted script, or a valid citation that does not support the claim. These cases retain unresolved obligations instead of being marked complete.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 13. Executed evidence: finite contract conformance

Numbers are loaded from the committed result JSON. Only the no-fault configuration should pass; the other 1,023 should be rejected. Zero disagreement establishes conformance in this finite domain. It is not a statistical sample or a production failure-rate bound.

- [Raw cases / 逐例结果](../agentic-runtime-preprint/artifact_v29/results/fault-cases.csv)
- [Summary / 汇总](../agentic-runtime-preprint/artifact_v29/results/summary.json)

## 14. Evidence boundary: what can we say today?

Separate implementation scope from future commitments. There are no natural retrieval, load, cross-tenant attack or complete P1 results. The model assumes trusted descriptors and mediation; it is not a security sandbox.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 15. Recent work: execution, research and delivery

These are external studies, not our results. Prime Agent operationalizes persistent state and accounting. AutoResearch separates artifacts from evidence. Apodex separates generation from controlled delivery. Those broad capabilities are not our unique novelty.

- [Prime Agent](https://arxiv.org/html/2608.23552v1)
- [AutoResearch](https://arxiv.org/html/2608.17906v1)
- [Apodex 1.1](https://arxiv.org/html/2608.23283v1)

## 16. Recent work: indexing, routing and source access

VoiceMem motivates separate index and routing ablations. NeoHorse separates demand from actual route, exposing capacity-driven model changes. Beyond Top-K motivates strong BM25 controls and conversion-error accounting. The last paper is a recheck of an existing citation.

- [VoiceMem](https://arxiv.org/html/2608.26005v1)
- [NeoHorse-1](https://arxiv.org/html/2609.08183v1)
- [Beyond Top-K](https://arxiv.org/html/2608.06305v1)

## 17. Methodological repairs in v29

The four-state verdicts no longer overlap. Establish measurement adequacy, then obligation eligibility, then classify P1. Remove the invalid p95 power calculation. Pilot simulation determines replication; it must not widen acceptable degradation.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 18. Next experiment: isolate contract enforcement

Hold candidates, tools, model and budget fixed; vary whether the boundary enforces the described constraints. Include natural errors and injections, with source/time holdouts. Report false refusal alongside violations; rejecting everything is not useful.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 19. Internal pilot: start with one bounded workflow

Choose a quarterly report or internal research brief with human-verifiable fields and a controlled source. Business owns tolerances; data owners define sources and policy; platform engineers enforce the boundary. Use evidence gates rather than arbitrary schedule promises.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 20. Venue choice follows the contribution and evidence

Prioritize SIGMOD for data contracts, OSDI for an implemented P1 runtime study, and ICSE/FSE for evolution and maintainability. The October SIGMOD window is tight. Synthetic checks cannot replace empirical work. ICSE 2027 is closed; FSE 2027 deadlines were not verified.

- [SIGMOD 2027 CFP](https://2027.sigmod.org/calls_papers_sigmod_research.shtml)
- [OSDI 2027 CFP](https://www.usenix.org/conference/osdi27/call-for-papers)
- [ICSE 2027 CFP](https://conf.researchr.org/track/icse-2027/icse-2027-research-track)

## 21. Three decisions for the internal discussion

Do not close by implying that all validation is complete. The team must choose the primary question, accessible real data and decision-derived tolerances. The next output is an owned pilot protocol, not another architecture name.

- [v29 manuscript / 论文源码](../agentic-runtime-preprint/paper_source/main.tex)

## 22. Reading and reproduction

Paper links on this slide are clickable. Speaker notes preserve reading guidance. The code and case CSV are in artifact_v29 in the same repository. The existing arXiv link points to the earlier public manuscript; v29 has not been submitted as a replacement.

- [Existing arXiv](https://arxiv.org/abs/2608.27086)
- [v29 evidence record](../agentic-runtime-preprint/V29_REVIEW.md)
