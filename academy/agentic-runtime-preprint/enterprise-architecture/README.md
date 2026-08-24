# Enterprise Architecture

> **FROZEN as of 2026-08-22.** v25 merged this series back into a single manuscript at
> `../paper_source/main.tex`; the v21/v22 split is retired because it produced four
> inconsistencies between the two documents (identical titles, divergent contract tuple,
> contradictory units of randomization, no cross-reference). This subproject and its v23
> PDF are kept for the record and are no longer updated. See `../CHANGELOG.md` (v25).

Full architecture whitepaper: enterprise responsibility model, four responsibility objects, six conditional decoupling assumptions, context partitioning, data subsystem (Intermediate Relation), Skill-as-Code lifecycle, dual-subgoal reward, and nine falsifiable evaluation protocols.

- **Current version**: v24 (37 pages, 2026-08-18)
- **Source**: `paper_source/main.tex`
- **Builder**: `latex_to_preprint.py --paper-dir paper_source --output output/pdf/Enterprise_Architecture_vXX.pdf`
- **Split from**: v20 enterprise reframe; v22 focused thesis was extracted from this on 2026-08-05
- **Scope**: Full enterprise responsibility architecture + Testable Separability Conjecture + all secondary propositions + context partitioning + data subsystem + training lifecycle.

## Version History
- v24: Scaffold functional decomposition into three modules (sandbox / API routing dual-track / governance); tool taxonomy grounded in 2608.00101 production traces (775M calls, read/mutate/execute/meta classes, failure-amplification evidence); Intermediate Relation schema extended from 5W1H to 5W1H+Which (relational seventh dimension); new Agent-Side Memory subsection (explicit/implicit dual track, archive offload, SQLite dedup, hash-indexed overflow, compression model as built-in API); first enterprise release with embedded figures (7 PNG architecture diagrams). Version number aligns with the repo release counter: v23 was consumed by the focused-paper release of 2026-08-08, so this release is v24.
- v22: Round-3 revision. Classical foundations citations added (reference monitors, non-interference, capability security, MAPE-K, ISO 25010, queueing), NFR/CIO first-use expansions, capability-count vs activated-behavior reconciliation, Intermediate Relation schema + end-to-end join example, Dispute and Escalation subsection, notation-vs-formal-model statement, earlier design-motivation registration of 2605.27744/2605.28000.
- v21: Current version (second revision pass of v20). Threat model added, power rules qualified, minimal study specified.
- v20: Enterprise reframe (27 pages). Four responsibility objects, six assumptions, data substrate as fourth object.
