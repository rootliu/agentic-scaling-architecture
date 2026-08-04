# v22 Focused Thesis Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a visually polished v22 preprint whose sole central claim is bounded, cost-aware capability-capacity separability, while preserving the complete Skill-Harness-Scaffold architecture, external data substrate, and the v21 PDF byte-for-byte.

**Architecture:** Treat `main.tex` as the scientific source of truth and `latex_to_preprint.py` as a deterministic document and figure renderer. Contract tests exercise the generated PDF, not merely source strings: they check versioning, rendered terminology, figure labels, decision states, page layout, and preservation of the prior release. The revision keeps eight figures but redesigns Figures 1, 4, 5, 6, and 8 around the focused argument and moves former P15-P17 material to compact secondary protocols.

**Tech Stack:** Python 3, `unittest`, ReportLab, pypdf, pdfplumber, Poppler, LaTeX-like manuscript source, Git.

## Global Constraints

- Central thesis: bounded, cost-aware capability-capacity separability inside a declared operating region `Omega`.
- Canonical variables: activated capability configuration `c`, Scaffold capacity configuration `s`, runtime response `R(c,s)`, semantic outcome `Q(c,s)`, and enforcement overhead `E(c,s)`.
- Primary estimand: the capability-by-Scaffold interaction in `R(c,s)`; do not require a zero Scaffold main effect.
- Experimental unit: cluster-period or system epoch with randomized crossover, reset or washout, and cluster-aware uncertainty.
- Decision states: `supported within Omega`, `falsified within Omega`, and `inconclusive`.
- Capability growth means activated independently deployable behavior on admitted paths, not registry cardinality.
- Harness owns logical admission and control; Scaffold owns physical execution and isolation.
- Preserve all eight figures and make every caption state what is shown, why it matters, and whether it is architecture, protocol, or proposed measurement design.
- Preserve the v21 PDF byte-for-byte at SHA-256 `52DE73D7B3AF0CE20E632B929EB8BE4365C7CBC713805F949E5BE656F901969A`.
- Generate `academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf`.
- Do not claim a completed runtime implementation, experiment, dataset, or measurement artifact.

---

### Task 1: Encode the v22 PDF Contract

**Files:**
- Create: `academy/agentic-runtime-preprint/tests/test_v22_rendering.py`
- Preserve: `academy/agentic-runtime-preprint/tests/test_v21_rendering.py`
- Test: `academy/agentic-runtime-preprint/tests/test_v22_rendering.py`

**Interfaces:**
- Consumes: the command-line interface of `latex_to_preprint.py` and its generated PDF.
- Produces: executable acceptance checks for the v22 filename, metadata, thesis vocabulary, responsibility ownership, experimental design, figure labels, and v21 preservation.

- [ ] **Step 1: Record the release baseline**

Run:

```powershell
Get-FileHash academy\agentic-runtime-preprint\output\pdf\Scalable_Manageable_Agentic_Runtime_Preprint_v21.pdf -Algorithm SHA256
python -m unittest academy.agentic-runtime-preprint.tests.test_v21_rendering -v
```

Expected: SHA-256 equals the value in Global Constraints and all existing v21 tests pass.

- [ ] **Step 2: Write the failing v22 tests**

Create tests that build the real PDF and assert these independently derived outcomes:

```python
assert reader.metadata.subject.startswith("v22")
assert "supported within Omega" in rendered_text
assert "falsified within Omega" in rendered_text
assert "inconclusive" in rendered_text
assert "cluster-period" in rendered_text
assert "randomized crossover" in rendered_text
assert "activated behavior" in rendered_text
assert "Harness owns logical admission and control" in rendered_text
assert "Scaffold owns physical execution and isolation" in rendered_text
```

Add figure checks for:

```python
expected_by_figure = {
    1: ["Capability change", "Harness contract", "Scaffold capacity",
        "Governed data and evidence", "Measurement plane"],
    4: ["Main agent", "Bounded sub-agents", "Verifier / semantic join",
        "Termination gate"],
    5: ["Data authority", "Resolved contract", "Isolated fetch",
        "Evidence bundle"],
    6: ["Logical control", "Physical execution", "Evidence"],
    8: ["Hypothesis", "Intervention and control", "Evidence plane",
        "Falsification or inconclusive condition"],
}
```

Add a SHA-256 assertion that the existing v21 release remains unchanged after a default v22 build.

- [ ] **Step 3: Run the new tests to verify RED**

Run:

```powershell
python -m unittest discover -s academy\agentic-runtime-preprint\tests -p "test_v22_rendering.py" -v
```

Expected: failures identify the still-v21 filename, metadata, prose, and old figure vocabulary.

- [ ] **Step 4: Commit the executable specification**

```powershell
git add academy/agentic-runtime-preprint/tests/test_v22_rendering.py docs/superpowers/plans/2026-08-04-v22-focused-thesis-revision.md
git commit -m "test: define v22 focused thesis contract"
```

### Task 2: Rewrite the Scientific Argument and Evidence Boundary

**Files:**
- Modify: `academy/agentic-runtime-preprint/paper_source/main.tex`
- Modify: `academy/agentic-runtime-preprint/paper_source/references.bib`
- Test: `academy/agentic-runtime-preprint/tests/test_v22_rendering.py`

**Interfaces:**
- Consumes: the v22 terminology and decision contract established in Task 1.
- Produces: a focused manuscript source with one research question, one primary hypothesis, explicit experimental design, narrow novelty, and secondary protocols.

- [ ] **Step 1: Replace the abstract and introduction**

Write an abstract that states, in order: the systems problem, P1, the Harness/Scaffold mechanism, the cluster-period crossover design, and the current evidence status. Make the introduction converge on:

```text
Can a runtime activate independently deployable capabilities without materially
changing capacity response, while scaling capacity without materially changing
capability semantics, at an acceptable enforcement cost?
```

- [ ] **Step 2: Define the responsibility model and P1 before architecture detail**

Define Skill, Harness, Scaffold, and external data substrate with unambiguous ownership. State `c`, `s`, `R(c,s)`, `Q(c,s)`, `E(c,s)`, `Omega`, the capability-by-Scaffold interaction estimand, enforcement budget, and the three-way decision rule.

- [ ] **Step 3: Recast six conditions as measured obligations**

For typed closure, complete mediation, effect non-interference, shared-state isolation, resource invariance, and scheduler independence, require instrumentation coverage, observed violations, uncertainty, enforcement cost, and operating-region exclusions. Insufficient coverage yields `inconclusive`.

- [ ] **Step 4: Replace request-level randomization with cluster-period crossover**

Specify period assignment, order balancing, reset or washout rules, fixed workload mix, repeated seeds and failure regimes, cluster-aware uncertainty, and pre-outcome exclusions. Define capability interventions as activated bundles that occur on admitted paths and capacity interventions as Scaffold resource changes under fixed logical policy and data snapshots.

- [ ] **Step 5: Compress secondary claims and defensive prose**

Reduce former P15-P17 material to secondary protocols or future work. Remove withdrawn-proposition history from the body, the artificial 2026 cutoff, unsupported `0-100,000 agents` scope language, and repeated meta-level disclaimers.

- [ ] **Step 6: Strengthen the novelty boundary**

Add traceable references for reference monitors and complete mediation, capability security and least authority, information hiding, policy-mechanism separation, control/data-plane separation, MAPE-K, ISO/IEC 25010, and queueing or resource interference. State that the contribution composes established mechanisms into an agentic-runtime responsibility model and makes separability plus enforcement cost falsifiable.

- [ ] **Step 7: Run the v22 prose tests**

Run:

```powershell
python -m unittest discover -s academy\agentic-runtime-preprint\tests -p "test_v22_rendering.py" -v
```

Expected: prose-level assertions pass; figure and renderer assertions remain red until Task 3.

- [ ] **Step 8: Commit the manuscript revision**

```powershell
git add academy/agentic-runtime-preprint/paper_source/main.tex academy/agentic-runtime-preprint/paper_source/references.bib
git commit -m "docs: focus v22 on cost-aware separability"
```

### Task 3: Redesign the Figures and Cut the v22 Release

**Files:**
- Modify: `academy/agentic-runtime-preprint/latex_to_preprint.py`
- Modify: `academy/agentic-runtime-preprint/CHANGELOG.md`
- Create: `academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf`
- Test: `academy/agentic-runtime-preprint/tests/test_v22_rendering.py`

**Interfaces:**
- Consumes: figure labels and captions from `main.tex`.
- Produces: the v22 PDF with eight legible figures and stable v21 preservation.

- [ ] **Step 1: Set the release version to v22**

Change:

```python
PREPRINT_VERSION = "v22"
```

Keep the default output derived from the version so the builder cannot overwrite v21.

- [ ] **Step 2: Redraw Figure 1**

Render the causal argument left to right:

```text
Capability change -> Harness contract -> Scaffold capacity
```

Add an external governed-data/evidence lane and a measurement plane for `Q(c,s)`, `R(c,s)`, condition coverage, and `E(c,s)`.

- [ ] **Step 3: Redraw Figures 4, 5, and 6**

Render Figure 4 as main agent to bounded sub-agents to verifier/semantic join to termination gate. Render Figure 5 as data authority to resolved contract to isolated fetch to evidence bundle. Render Figure 6 as parallel logical-control, physical-execution, and evidence lanes with orthogonal connectors and no crossed lines.

- [ ] **Step 4: Replace Figure 8 with the falsification matrix**

Use exactly these columns:

```text
Hypothesis | Intervention and control | Evidence plane |
Falsification or inconclusive condition
```

Give P1 the dominant row and visually subordinate secondary protocols.

- [ ] **Step 5: Append the v22 changelog entry**

Record the focused thesis, experimental unit, estimand, responsibility correction, three-way decision rule, classical novelty boundary, figure redesign, and v21 preservation. Do not rewrite historical entries.

- [ ] **Step 6: Build and run all rendering tests**

Run:

```powershell
python academy\agentic-runtime-preprint\latex_to_preprint.py --paper-dir academy\agentic-runtime-preprint\paper_source
python -m unittest discover -s academy\agentic-runtime-preprint\tests -p "test_*.py" -v
```

Expected: v22 is generated, all v21 and v22 tests pass, and v21's SHA-256 is unchanged.

- [ ] **Step 7: Commit the release implementation**

```powershell
git add academy/agentic-runtime-preprint/latex_to_preprint.py academy/agentic-runtime-preprint/CHANGELOG.md academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf
git commit -m "release: generate focused v22 preprint"
```

### Task 4: Verify, Synchronize, and Publish

**Files:**
- Modify in Obsidian repository: `00_Index.md`
- Modify in Obsidian repository: the current architecture synthesis note
- Modify in Obsidian repository: the latest paper review note
- Modify in Obsidian repository: the figure and evaluation specification note

**Interfaces:**
- Consumes: final v22 manuscript, PDF, and design vocabulary.
- Produces: visually verified release plus synchronized, independently committed source and Obsidian repositories.

- [ ] **Step 1: Run structural and text QA**

Extract all PDF text and reject unresolved LaTeX controls, placeholders, broken references, raw formula-control words, and unexplained abbreviations. Check citation keys in `main.tex` against `references.bib`, run `git diff --check`, and confirm exactly eight figure captions.

- [ ] **Step 2: Render every page to PNG**

Run:

```powershell
pdftoppm -png -r 144 academy\agentic-runtime-preprint\output\pdf\Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf tmp\pdfs\v22-page
```

Inspect every page for clipping, overlap, broken glyphs, unreadable labels, orphan headings, poor whitespace balance, URL wrapping, and inconsistent typography. Correct the source or renderer and repeat the build and inspection after any defect.

- [ ] **Step 3: Synchronize Obsidian notes**

Record the v22 thesis, ownership boundaries, cluster-period unit, interaction estimand, three evidence outcomes, figure vocabulary, and final PDF path in the authoritative active notes. Preserve archival conclusions and ignore empty notes as evidence.

- [ ] **Step 4: Run final verification in both repositories**

Run the complete test suite, PDF hash check, text scan, image render, `git diff --check`, and `git status --short` in the source worktree. In the Obsidian repository run `git diff --check` and inspect the exact staged note diff.

- [ ] **Step 5: Commit and push the source repository**

```powershell
git add academy docs
git commit -m "docs: finalize v22 focused thesis"
git push origin HEAD:main
```

- [ ] **Step 6: Commit and push the Obsidian repository**

```powershell
git add <the four verified active notes>
git commit -m "docs: synchronize v22 agentic runtime research"
git push origin HEAD:main
```

