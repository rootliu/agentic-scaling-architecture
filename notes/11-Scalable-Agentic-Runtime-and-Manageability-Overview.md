# 11 — Scalable Agentic Runtime and Manageability Overview

> Synchronized from: `site/index.html` (Chinese presentation page) and `site/index-en.html` (English presentation page)  
> Purpose: an Obsidian entry note for presentation-style communication, kept aligned with the HTML landing page in claims, logic, terminology and cases.

## 1. Research Goal

This project studies a **scalable agentic runtime** and its **manageability** after scaling: as an agent system continuously adds skills, execution resources, external data sources and parallel sub-agents, how can the runtime remain auditable, governable, operable and evolvable?

The goal is not merely to draw a three-layer architecture. The research question is how logical scaling, physical scaling, data scaling and parallel scaling can be orthogonally decoupled under probabilistic LLM calls through explicit contracts, responsibility planes, offline subsystems and locality planning.

## 2. One-Sentence Claim

For each of the four orthogonal cuts, the first-order cost of “adding more” should land in a plane or subsystem decoupled from the main request path: logical growth lands in the control plane, physical growth in the data plane, data growth in an offline off-policy loop, and parallel growth in tool-closure and locality planning. The target is an agentic runtime that is both **scalable and manageable**.

## 3. How to Read the Architecture Map

Read the architecture map in the presentation page in this order:

1. Start from the three-layer runtime core `A = <S, H, X>`: Skills, Harness and Scaffold.
2. Then inspect Harness as the contract gate that translates upper-layer intent into lower-layer executable units.
3. Read the CP/DP split horizontally: probabilistic control decisions go to CP, while high-frequency online execution goes to DP.
4. The `𝒟` subsystem on the right sits outside the stack. It is not a fourth layer, and only controlled interfaces such as semantic join enter the main path.
5. P10-P13 at the bottom describe parallelism/locality mechanisms; N8/P14 hardens validated, operation-closed skills into code as the deterministic anchor of a probabilistic control plane.

## 3.1 Figure Guide

Every figure in the presentation and dry-run pages keeps a standalone caption; Figure 0 serves as the overview navigation map before the audience enters the detailed architecture.

- **Figure 0 · Overview map**: the first global map for presentation. It places the three-layer runtime, CP/DP split, out-of-stack data subsystem, parallelism/locality and the Skill-as-Code deterministic anchor on one reading path.
- **Figure 1 · Architecture overview**: expands the three-layer stack and the external data subsystem, emphasizing Harness as the contract gate between logical and physical scaling.
- **Figure 2 · Spec architecture**: explains how Skills use I/O schemas, call/termination/loop conditions and task material to organize LLM context.
- **Figure 3 · Agent loop**: shows the control/execution loop among Skills, Harness, Scaffold and the data subsystem during one run.
- **Figure 4 · Parallelism/locality walkthrough**: shows how dry-run partitions sub-agents by tool-set closure and controls parallel cost through seed affinity, frozen prefixes and summarized context.
- **Figures DR-1/DR-2 plus six detailed dry-run diagrams**: use the AI4Science and Kronos cases to show spec call order, probability-to-determinism hardening, and data-flow/write-back paths as runtime evidence for Figures 1-4.
- **Figures 7/8 · Skill training and lifecycle**: explain reward training, lifecycle management and how Skill-as-Code hardens validated capability into a deterministic asset.
- **Figures 9/10 · Data Wiki**: explain how automated sources and complex reports enter Data Wiki, and how Data Wiki × Theme Wiki × IR supports governable data use.

## 4. Four Orthogonal Cuts

| Cut | Problem | Decoupling Mechanism | Main Note |
| --- | --- | --- | --- |
| Extension axis: logical/physical | Adding skills and adding execution resources should not drag each other | Skills express logical capability, Scaffold carries execution/isolation/throughput, and Harness decouples them as the contract layer | [[01-C5-双扩展解耦形式化与命题]] |
| CP/DP | Once LLMs participate in control decisions, how can the system stay auditable and operable? | CP handles probabilistic planning, reflection, tool synthesis and governance; DP handles online execution, isolation, retrieval and serving | [[05-控制面与数据面正交切分]] |
| Out-of-stack data subsystem | As external data keeps growing, how can the main request path avoid overload? | D1 retrieval sits in DP; D2 semantic summarization is an independent off-policy loop; D3 governance and D4 lifetime sit in CP | [[06-数据平面四组成架构]] |
| Parallelism/locality | When sub-agents multiply, how do we avoid context dilution, tool conflicts and cache waste? | Planning-time dry-run probes tool closure and environment scope, partitions sub-agents by non-overlapping tools, freezes stable prefixes and derives execution through seed affinity | [[09-并行度与局部性协同设计]] |

## 5. Three Layers and Data Subsystem

- **Skills (Specification Plane)**: specs, I/O schemas, call conditions, termination conditions and loop conditions. It assembles task-relevant material and iteratively pushes it into LLM context. Task skills live here.
- **Harness (Capability / Contract Plane)**: contract translation, capability supply through tool synthesis, and the manageability subsystem `M`. It is the decoupling point between logical and physical scaling.
- **Scaffold (Execution / Isolation Plane)**: microVMs/sandboxes, isolation, compute and inference serving capacity. It characterizes system throughput `Θ`.
- **Data Subsystem `𝒟` (not a fourth layer)**: how agents understand, access, govern and maintain authorized external data. It splits along both online/offline and CP/DP, and only controlled query interfaces enter the main path.

## 6. Novelty Map

| ID | Novelty | Summary | Proposition |
| --- | --- | --- | --- |
| C5 | Orthogonal logical/physical scaling | Logical and physical scaling are orthogonal, with the Harness contract layer as the decoupling point | P1-P3 |
| N0 | Probabilistic control plane | LLM-driven contract translation, reflection and tool synthesis require audit logs and invariant constraints | P4-P6 |
| N1 | Off-policy semantic summarization | A schema-on-read background loop summarizes into an untruncated lake, while semantic joins inject only what is needed | P8 |
| N2 | Data governance as skill | Governance moves from boundary control to per-use-case data-usage skills as accumulated experience | P9 |
| N3 | Architectural consistency of the data subsystem | The data subsystem naturally splits along CP/DP and reuses the same plane invariant | - |
| N4 | Independent out-of-stack off-policy loop | Semantic summarization is an offline subsystem with its own loop, sub-agents and model, not an online step | - |
| N5 | Skill triad | Task, system and data-usage skills share one skill form | - |
| N6 | Tool-set partitioned sub-agents | Tool-set closure defines parallel independence, Skills locality and Scaffold seed boundaries | P10-P12 |
| N7 | Dry Run probes parallelizability | Before execution, dry-run probes tool-set closure and environment scope, then partitions sub-agents | P13 |
| N8 | Skill-as-Code deterministic anchor | Validated and operation-closed skills can be hardened into code to reduce model-version drift | P14 |

See [[07-创新点总结]] and [[10-Skill-as-Code与确定性固化]].

## 7. Dry Run Instantiation

The presentation page uses two cases to ground the abstract architecture in a concrete run:

- **Perovskite band-gap screening (~1.3 eV)**: papers feed D2 temporal summaries, property databases feed D1 retrieval, simulations trigger code generation plus Scaffold cloud/HPC, multi-signal validation gates the result, and reports/write-back update D2/Ω/D3. Sub-goals `{literature → candidates → properties → screening → analysis → report}` are partitioned into parallel sub-agents through dry-run.
- **Kronos foundation model for stock prediction**: D1 performs retrieval, Scaffold hosts the GPU pretrained model, probabilistic sampling enters the loop, multi-signal validation uses backtest/leakage/calibration, and predictions are written back as expiring records. Multiple tickers and horizons are parallelized by tool-set partition.

Together, the two cases show that one spec invocation sequence leaves observable first-order traces along the extension axis, CP/DP split, data subsystem and parallel-locality dimension.

Related notes: [[附录-AI4Science实例化walkthrough]], [[09-并行度与局部性协同设计]].

## 8. Abbreviation Glossary

| Abbreviation | Meaning |
| --- | --- |
| `S/H/X` | Skills / Harness / Scaffold |
| `CP` | Control Plane |
| `DP` | Data Plane |
| `D` / `𝒟` | Data Subsystem, the out-of-stack data subsystem |
| `D1-D4` | Four data-subsystem parts: retrieval API, semantic summary, governance memory and lifetime budget |
| `M1-M4` | Locality mechanisms: stable prefix, context shard, seed affinity and summarized context |
| `T1-T8` | Tool capsule categories that describe routable Harness capabilities |
| `O1-O8` | Runtime choices in Harness, such as tool, shot, schema, plan, code generation, reflection, model and token |
| `LLM` | Large Language Model |
| `I/O` | Input / Output |
| `API` | Application Programming Interface |
| `IR` | Intermediate Relation |
| `5W1H` | When / Where / Who / What / Why / How, used for fact extraction and report organization |
| `NFR` | Non-Functional Requirement |
| `SLA/SLO` | Service-Level Agreement / Objective |
| `QPS` | Queries Per Second |
| `SDN` | Software-Defined Networking |
| `K8s` | Kubernetes |
| `MCP` | Model Context Protocol |
| `BI` | Business Intelligence |
| `JSON` | JavaScript Object Notation |
| `PPT/PDF/HTML` | Presentation, document and web output formats |
| `microVM` | micro virtual machine |
| `GPU` | Graphics Processing Unit |
| `HPC` | High Performance Computing |
| `SSO` | Single Sign-On |
| `OIDC` | OpenID Connect |
| `SAML` | Security Assertion Markup Language |
| `SCIM` | System for Cross-domain Identity Management |
| `RBAC` | Role-Based Access Control |
| `KMS` | Key Management Service |
| `S3` | Simple Storage Service |
| `PrivateLink` | Private cloud connectivity service |
| `DFT` | Density Functional Theory |
| `OHLCV` | Open / High / Low / Close / Volume |
| `KV-cache` | attention key-value cache |
| `vLLM` | high-throughput LLM serving engine |
| `SOTA` | State of the Art |
| `DB` | Database |
| `MP` / `OQMD` | Materials Project / Open Quantum Materials Database |
| `HF` | Hugging Face |
| `EOD` | End of Day |
| `maxDD` | Maximum Drawdown |
| `RQ` | Research Question |
| `P/N/C` or `N/P/C` | Proposition / Novelty / Contribution |

## 9. Presentation Entry Points

- Chinese presentation page: `site/index.html`
- English presentation page: `site/index-en.html`
- Detailed architecture page: `site/architecture.html`
- Dry Run walkthrough: `site/dry-run.html`
- Research brief: `site/research-brief.md`
