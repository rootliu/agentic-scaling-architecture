# v19 Separability Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a v19 preprint that recasts strict separability as a testable conjecture, states the experimental estimands precisely, strengthens P15-P17, and demonstrates the boundary with an AI4Science walkthrough.

**Architecture:** The paper source remains the normative argument, while the ReportLab builder remains the normative rendering implementation for custom figures. The revision is split into a prose/protocol task and a rendering/release task so that claim semantics can be reviewed before the figure and PDF are synchronized.

**Tech Stack:** LaTeX-like source consumed by the repository's Python/ReportLab builder, BibTeX source, Poppler PDF rendering and extraction, Git.

## Global Constraints

- Preserve the Skill-Harness-Scaffold architecture and the stack-external data subsystem; this revision narrows claims rather than replacing the architecture.
- Rename P1 to `Testable Separability Conjecture`; do not describe it as a theorem, proof, necessary condition, universal independence result, or strict sufficient condition.
- State the six causal separability conditions exactly as typed closure, complete mediation, effect non-interference, shared-state isolation, resource invariance, and scheduler independence.
- Treat deterministic gates and trace identity as observability, audit, and attribution requirements; do not list them as causal generators of separability.
- Define interface semantics in terms of admission decision, activated path, authorized effects, binding constraints, and postconditions.
- Split the main factorial evaluation into semantic invariance, capacity response, and capability-count by Scaffold-count interaction estimands.
- Add a claim-type table covering Proposition, Hypothesis, Design pattern, Open question, and Evidence status, and keep higher-order memory, locality, and Skill training as secondary hypotheses or future work.
- Add the AI4Science chain `intent -> contract compilation -> path gate -> binding -> trace -> typed failure -> recoupling`.
- Strengthen P15 with a fixed-proposal-bank offline gate comparison and a multi-seed online training experiment.
- Strengthen P16 with token-matched direct reading, metadata-only, field ablation, and shuffled-summary controls.
- Strengthen P17 with a preregistered dependency graph and artifact-change oracle.
- Keep all factual and empirical claims source-bounded; add no uncited empirical result and do not invent implementation evidence.
- Keep author identity, existing bibliography entries, v18 artifacts, and historical changelog entries unchanged.
- Build a new `Scalable_Manageable_Agentic_Runtime_Preprint_v19.pdf`; do not overwrite or remove earlier PDFs.
- Use ASCII in source edits except where an existing file already requires non-ASCII text.

---

### Task 1: Reframe the Claims and Evaluation Protocols

**Files:**
- Modify: `academy/agentic-runtime-preprint/paper_source/main.tex`
- Reference: `notes/附录-AI4Science实例化walkthrough.md`

**Interfaces:**
- Consumes: the v18 paper structure, proposition numbering P1-P17, existing citations, and the AI4Science example note.
- Produces: internally consistent v19 paper source whose claim vocabulary and protocol definitions can be rendered without builder changes.

- [ ] **Step 1: Record the v18 baseline claim vocabulary**

Run:

```bash
rg -n "Proposition|P1|P15|P16|P17|sufficient condition|deterministic gate|trace identity|factorial|AI4Science|higher-order|locality" academy/agentic-runtime-preprint/paper_source/main.tex
```

Expected: matches identify the abstract, contributions, central proposition, proposition summary, evaluation protocols, discussion, limitations, and conclusion that must remain synchronized.

- [ ] **Step 2: Rewrite the abstract, contributions, and central P1 statement**

Edit the abstract and contribution list so the paper's primary contribution is a bounded, falsifiable separability conjecture. Replace the current P1 heading and statement with `Testable Separability Conjecture`, enumerate the six causal conditions from Global Constraints, and state that they are hypotheses about when semantic behavior and capacity can vary independently inside a declared operating region.

Define the contract boundary using all five interface semantics: admission decision, activated path, authorized effects, binding constraints, and postconditions. Move deterministic gates and trace identity into a separate observability paragraph that says they make violations detectable, auditable, and attributable but do not themselves cause independence.

- [ ] **Step 3: Add the claim-type and evidence-status table**

Add a compact table near the proposition summary that classifies central and secondary claims using the exact claim types `Proposition`, `Hypothesis`, `Design pattern`, and `Open question`, plus an `Evidence status` column. Include at minimum P1, path-level safety/mediation, P15, P16, P17, dry-run/locality, higher-order memory, and Skill lifecycle/training. Use evidence labels that distinguish analytic argument, proposed experiment, cited external evidence, and future work; do not imply that this paper reports completed experiments.

- [ ] **Step 4: Add the AI4Science end-to-end walkthrough**

Using `notes/附录-AI4Science实例化walkthrough.md` as the source, add one concrete walkthrough for screening perovskite candidates with a target band gap near 1.3 eV from recent literature and producing a cited, reproducible report. Walk through exactly these stages:

1. intent: band-gap target, recency, citation, and reproducibility constraints;
2. contract compilation: literature, screening, and reporting Skills;
3. path gate: data authorization, HPC identity, network allowlist, and effect closure;
4. binding: databases, microVM, and GPU/HPC Scaffold;
5. trace: Skill/model/data-snapshot/binding/script/evidence identities;
6. typed failure: missing authorization, ungrounded citation, unit anomaly, or no compatible HPC;
7. recoupling: shared HPC quota, scheduler feedback, or resource-sensitive scientific output that breaks semantic invariance.

Use the example to expose where the conjecture can fail; do not present it as an implemented case study or empirical validation.

- [ ] **Step 5: Define three estimands for the shared factorial experiment**

Rewrite the Figure 8 lead-in and Protocols 9.1-9.2 so one shared capability-count by Scaffold-count randomized factorial design estimates:

- semantic invariance: equivalence or non-inferiority of preregistered semantic metrics across compatible Scaffold conditions;
- capacity response: the dose-response of throughput and latency to compatible Scaffold count/topology;
- recoupling: the capability-count by Scaffold-count interaction, with injected shared compute, locks, external quotas, authorization delay, scheduler feedback, and mutable policy as diagnostic arms.

Specify the unit of randomization, repeated seeds or runs, confidence intervals, equivalence/non-inferiority margins, and the declared operating region. Do not treat a non-significant interaction as proof of independence.

- [ ] **Step 6: Split P15 into offline and online experiments**

Rewrite Protocol 9.8 into two linked experiments:

- Offline gate comparison: evaluate scalar, output-vector, and output-plus-process gates on the same fixed proposal bank, with blinded oracle labels for Pareto validity, protected-component regression, and process-attribution truth.
- Online training: run each gate in otherwise matched training loops over multiple preregistered random seeds, comparing convergence, accepted edits, rollout cost, protected regressions, and attribution validity.

Keep first-attempt grading, executor/grader separation, preregistered criteria, and the counterfactual phantom-violation oracle. State separate falsification conditions for offline discrimination/attribution and online convergence/safety.

- [ ] **Step 7: Add P16 control arms and P17 artifact oracle**

For P16, compare the pinned summary against:

- token-matched direct reading of source content;
- metadata-only input;
- field ablations of the summary;
- shuffled summaries assigned to the wrong source or report family.

Keep strict train/validation/held-out separation and one-shot held-out inspection. Define what contrast establishes summary-specific sufficiency rather than generic context benefit.

For P17, preregister the expected dependency graph for each change class before intervention. Add an artifact-change oracle that records touched entries, schemas/modules, IR records, tests, and generated artifacts, then compares observed changes with necessary changes in the preregistered graph. Falsify independence when unanticipated cross-registry schema/module propagation occurs, while allowing expected entry and IR edits.

- [ ] **Step 8: Synchronize scope language throughout the paper**

Update the proposition summary, discussion, research questions, limitations, and conclusion to use the same causal/observability distinction and estimand vocabulary. Keep higher-order memory, locality, dry-run economics, and Skill training as secondary hypotheses, design patterns, or future work. Remove stale wording that still calls P1 a sufficient condition or treats deterministic gates/trace identity as causes of decoupling.

- [ ] **Step 9: Run source-level consistency checks**

Run:

```bash
rg -n "strict sufficient|sufficient conditions|bounded sufficient|Proposition~1|deterministic gates.*condition|trace identit.*condition" academy/agentic-runtime-preprint/paper_source/main.tex
rg -n "Testable Separability Conjecture|typed closure|complete mediation|effect non-interference|shared-state isolation|resource invariance|scheduler independence|semantic invariance|capacity response|fixed proposal bank|token-matched|artifact-change oracle|AI4Science" academy/agentic-runtime-preprint/paper_source/main.tex
git diff --check
```

Expected: no stale causal overclaim remains; every required v19 concept appears in the intended section; `git diff --check` exits 0.

- [ ] **Step 10: Commit Task 1**

```bash
git add academy/agentic-runtime-preprint/paper_source/main.tex
git commit -m "paper: reframe separability claims and protocols for v19"
```

### Task 2: Synchronize Figure 8 and Release the v19 PDF

**Files:**
- Modify: `academy/agentic-runtime-preprint/latex_to_preprint.py`
- Modify: `academy/agentic-runtime-preprint/CHANGELOG.md`
- Create: `academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v19.pdf`
- Verify: `academy/agentic-runtime-preprint/paper_source/main.tex`

**Interfaces:**
- Consumes: Task 1's final estimand names, P15/P16/P17 protocol arms, and unchanged figure dispatch API.
- Produces: a Figure 8 whose labels match the paper, a v19 changelog entry, and a visually verified v19 PDF.

- [ ] **Step 1: Locate the Figure 8 builder and build entrypoint**

Run:

```bash
rg -n "_draw_evaluation_matrix|evaluation-matrix|v18|OUTPUT|Scalable_Manageable" academy/agentic-runtime-preprint/latex_to_preprint.py
```

Expected: `_draw_evaluation_matrix()` contains hard-coded matrix text and the script exposes the output-version path used to build the PDF.

- [ ] **Step 2: Update Figure 8 to match the v19 protocols**

Revise `_draw_evaluation_matrix()` without changing its public dispatch contract. The P1 area must name semantic invariance, capacity response, and interaction/recoupling. P15 must distinguish fixed-bank offline comparison from multi-seed online training. P16 must show held-out reconstruction with direct-reading, metadata, ablation, and shuffle controls. P17 must show preregistered dependency graph plus artifact-change oracle. Keep labels concise enough for the existing page width and preserve legibility at 150 dpi.

- [ ] **Step 3: Add the v19 changelog entry**

Prepend `## v19 — 2026-08-02` to `CHANGELOG.md`. Summarize:

- P1 renamed and narrowed to a testable conjecture;
- six causal conditions separated from gate/trace observability requirements;
- interface semantics and three estimands made explicit;
- claim-type/evidence table and AI4Science walkthrough added;
- P15-P17 controls strengthened;
- Figure 8 synchronized and v19 PDF rebuilt.

Do not alter historical entries.

- [ ] **Step 4: Build the v19 PDF**

Run the repository's current builder with the output version set to v19, using the existing CLI or constants discovered in Step 1.

Expected: exit 0 and `academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v19.pdf` exists and is non-empty.

- [ ] **Step 5: Extract and scan the complete PDF text**

Run:

```bash
pdftotext academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v19.pdf /tmp/agentic-v19.txt
rg -n "\\\\[A-Za-z]+|\\{[^}]+\\}|Section[0-9]|sum_|frac|\\[\\?\\]|undefined|TBD|TODO" /tmp/agentic-v19.txt
rg -n "Testable Separability Conjecture|AI4Science|semantic invariance|capacity response|fixed proposal bank|token-matched|artifact-change oracle" /tmp/agentic-v19.txt
```

Expected: the defect scan has no unexplained matches and all required v19 concepts are present in extracted text.

- [ ] **Step 6: Render every page and inspect high-risk pages**

Run:

```bash
rm -rf /tmp/agentic-v19-pages
mkdir -p /tmp/agentic-v19-pages
pdftoppm -png -r 150 academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v19.pdf /tmp/agentic-v19-pages/page
```

Inspect the title/abstract page, P1 and its condition list, the claim-type table, AI4Science walkthrough, Figure 8, and references. Check all rendered pages for clipping, overlaps, blank pages, broken glyphs, orphaned headings, and unreadably small figure text. If a defect appears, revise the source or builder, rebuild, and repeat Steps 4-6.

- [ ] **Step 7: Run final repository checks**

Run:

```bash
pdfinfo academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v19.pdf
git diff --check
git status --short
```

Expected: PDF metadata is readable, `git diff --check` exits 0, and only the intended builder, changelog, source, and v19 PDF changes are present.

- [ ] **Step 8: Commit Task 2**

```bash
git add academy/agentic-runtime-preprint/latex_to_preprint.py academy/agentic-runtime-preprint/CHANGELOG.md academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v19.pdf
git commit -m "paper: build and document v19 preprint"
```
