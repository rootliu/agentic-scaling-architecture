# v20 Enterprise Runtime Reframing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` to execute this plan task by task
> with independent specification and quality reviews.

**Goal:** Produce and release a v20 preprint that explains the enterprise
deployment problem, presents Skill, Harness, Scaffold, and the external data
substrate as explicit responsibility contracts, preserves the v19 falsifiable
scientific core, adds a Chinese Obsidian synthesis, and passes source, PDF, and
visual verification.

**Architecture:** `main.tex` remains the normative argument and
`latex_to_preprint.py` remains the rendering implementation. The Obsidian vault
stores Chinese research synthesis without rewriting archival notes. Work is
split into knowledge-base, paper, rendering, and release tasks so that each
artifact can be reviewed before the two repositories are pushed.

**Tech stack:** Markdown/Obsidian, LaTeX-like source, BibTeX, Python 3.12,
ReportLab, Poppler, Git.

## Global Constraints

- Preserve P1 as the `Testable Separability Conjecture` and preserve all six
  conditions: typed closure, complete mediation, effect non-interference,
  shared-state isolation, resource invariance, and scheduler independence.
- Preserve P15's fixed proposal bank, separate `(c)-(a)` and `(c)-(b)` margins,
  multi-seed online experiment, first-attempt grading, independent grader, and
  phantom-violation oracle.
- Preserve P16's token-matched direct-reading, metadata-only, field-ablation,
  shuffled-summary, strict held-out, and joint-contrast controls.
- Preserve P17's preregistered dependency graph, artifact-change oracle, and
  expected-versus-unanticipated propagation distinction.
- Preserve existing estimands, margins, falsification criteria, controls, and
  claim/evidence classifications unless the v20 framing makes wording changes
  necessary.
- Define Skill as a reusable, versioned business capability and workflow asset;
  Harness as runtime compiler/governor; Scaffold as execution/control boundary
  and NFR owner; and the data substrate as stack-external, independently
  CIO-governed semantic and telemetry infrastructure.
- Treat non-blocking scale from 0 to 100,000 admitted or active agents as a
  measurable design target, never as an achieved result.
- Separate business/use-case evidence from system/runtime evidence.
- Conway 1968 is the only historical reference. Every contemporary retained
  source must have a verified publication or release date on or after
  2026-06-01; a year alone is not evidence.
- Do not attribute the phrase "enterprise IT architecture is the enterprise
  communication protocol" to an external author. Present the shared-contract
  interpretation as this paper's narrower thesis.
- Keep original Obsidian notes unchanged. Add Chinese synthesis notes and index
  links.
- Preserve every PDF before v20.

## Task 1: Add the Chinese Obsidian Synthesis

**Files:**
- Create: `Agentic-Runtime-参考架构/13-v20-企业AI运行时架构-中文综合.md`
- Create: `Agentic-Runtime-参考架构/14-v20-图表与评估规范.md`
- Modify: `Agentic-Runtime-参考架构/00_Index.md`

- [ ] Synthesize the user's motivation, four responsibility objects, ownership
  and change cadence, semantic joins, Skill-as-Code, NFRs, and dual evaluation
  planes in Chinese.
- [ ] Translate and integrate only relevant eligible literature conclusions;
  retain source identifiers and verified exact dates.
- [ ] Record the v20 figure/table design vocabulary, ownership boundaries, and
  prohibited claims in a separate Chinese design note.
- [ ] Link both notes from the research-note section of `00_Index.md`.
- [ ] Verify archival notes are unchanged.

Run:

```bash
git -C "/Users/rootliu/Documents/Obsidian Vault" diff --check
git -C "/Users/rootliu/Documents/Obsidian Vault" diff --name-only
rg -n "Skill-as-Code|运行时编译器|执行与控制边界|CIO|语义连接|0 到 100,000|业务/use case|系统/运行时" \
  "/Users/rootliu/Documents/Obsidian Vault/Agentic-Runtime-参考架构/13-v20-企业AI运行时架构-中文综合.md" \
  "/Users/rootliu/Documents/Obsidian Vault/Agentic-Runtime-参考架构/14-v20-图表与评估规范.md"
```

## Task 2: Audit Literature and Rewrite the Enterprise Framing

**Files:**
- Modify: `academy/agentic-runtime-preprint/paper_source/main.tex`
- Modify: `academy/agentic-runtime-preprint/paper_source/references.bib`

- [ ] Inventory every citation key used by `main.tex` and map it to a verified
  date and source URL.
- [ ] Remove all ineligible pre-2026-06-01 contemporary citations and rewrite
  dependent prose as design motivation or support it with eligible sources.
- [ ] Add Conway's 1968 paper and eligible June/July 2026 academic and industry
  anchors with explicit `date` fields.
- [ ] Rewrite Abstract, Introduction, Origins, Related Work, Discussion,
  Limitations, and Conclusion around the cross-BU deployment problem and shared
  organizational contracts.
- [ ] Add the ownership/change-cadence table, responsibility-boundary table, and
  business/use-case versus system/runtime evaluation table.
- [ ] Preserve and update the claim/evidence table.
- [ ] Integrate Scaffold NFRs and measurable 0-to-100,000 metrics without
  claiming implementation evidence.
- [ ] Explain the CIO-governed data substrate, semantic joins, telemetry
  integration, and slower change cadence.
- [ ] Confirm P1 and P15-P17 remain substantively intact.

Run:

```bash
rg -n "\\\\cite\\{[^}]+\\}" academy/agentic-runtime-preprint/paper_source/main.tex
rg -n "typed closure|complete mediation|effect non-interference|shared-state isolation|resource invariance|scheduler independence|fixed proposal bank|token-matched direct reading|metadata-only|field ablation|shuffled summaries|artifact-change oracle" academy/agentic-runtime-preprint/paper_source/main.tex
rg -n "CIO|semantic join|0 to 100\\{,\\}000|business/use-case|system/runtime|performance|reliability|availability|manageability|security|portability" academy/agentic-runtime-preprint/paper_source/main.tex
rg -n "2020|2023|2024|2025|2601\\.|2602\\.|2603\\.|2604\\.|2605\\." academy/agentic-runtime-preprint/paper_source/main.tex academy/agentic-runtime-preprint/paper_source/references.bib
git diff --check
```

## Task 3: Redesign and Synchronize All Figures and Tables

**Files:**
- Modify: `academy/agentic-runtime-preprint/latex_to_preprint.py`
- Verify: `academy/agentic-runtime-preprint/paper_source/main.tex`

- [ ] Audit all eight figures for terminology, ownership, direction of
  dependencies, stack-external data placement, and readable labels.
- [ ] Use the canonical labels: `Business capability: Skill-as-Code`,
  `Runtime governance: Harness`, `Execution and control boundary: Scaffold`,
  and `CIO-governed semantic and telemetry foundation: data substrate`.
- [ ] Redraw figures whose current geometry encodes obsolete layer ownership.
- [ ] Ensure Figure 8 distinguishes business/use-case evaluation from
  system/runtime evaluation while retaining the v19 protocol controls.
- [ ] Ensure generated tables fit the page and repeat headers where needed.
- [ ] Update builder metadata and output path to v20 without overwriting v19.

Run:

```bash
rg -n "Skill-as-Code|Runtime governance|Execution and control boundary|CIO-governed|v20|Scalable_Manageable_Agentic_Runtime_Preprint_v20" academy/agentic-runtime-preprint/latex_to_preprint.py
rg -n "v19|production agent and workflow systems|OpenAI Assistants|AutoGen|CrewAI|LangGraph|Temporal" academy/agentic-runtime-preprint/paper_source/main.tex academy/agentic-runtime-preprint/latex_to_preprint.py
git diff --check
```

## Task 4: Build and Verify the v20 Preprint

**Files:**
- Modify: `academy/agentic-runtime-preprint/CHANGELOG.md`
- Create:
  `academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf`

- [ ] Prepend a v20 changelog entry without modifying historical entries.
- [ ] Build v20 with the bundled Python 3.12 runtime.
- [ ] Confirm every earlier PDF still exists.
- [ ] Extract the complete PDF text and scan for required concepts, stale
  terminology, unresolved citations, raw LaTeX, placeholders, and prohibited
  attribution.
- [ ] Render every page at 150 dpi.
- [ ] Inspect every page for clipping, overlap, broken glyphs, tiny figure/table
  text, orphan headings, blank pages, headers, and page numbering.
- [ ] Correct and repeat build, extraction, rendering, and inspection until no
  issue remains.

Run:

```bash
/Users/rootliu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3.12 \
  academy/agentic-runtime-preprint/latex_to_preprint.py
test -s academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf
find academy/agentic-runtime-preprint/output/pdf -name 'Scalable_Manageable_Agentic_Runtime_Preprint_v*.pdf' -print | sort
pdftotext academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf /tmp/agentic-v20.txt
rg -n "enterprise|CIO|semantic join|100,000|business/use-case|system/runtime|Testable Separability Conjecture|fixed proposal bank|token-matched direct reading|artifact-change oracle" /tmp/agentic-v20.txt
rg -n "\\\\[A-Za-z]+|\\{[^}]+\\}|undefined|TBD|TODO|enterprise IT architecture is the enterprise communication protocol" /tmp/agentic-v20.txt
rm -rf /tmp/agentic-v20-pages
mkdir -p /tmp/agentic-v20-pages
/Users/rootliu/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm \
  -png -r 150 \
  academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf \
  /tmp/agentic-v20-pages/page
pdfinfo academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf
```

## Task 5: Independent Review and Release

- [ ] Run an independent specification-compliance review against the committed
  design and this plan.
- [ ] Run an independent quality review of prose, evidence boundaries, figures,
  tables, references, and rendered pages.
- [ ] Resolve every critical or major issue and rerun verification.
- [ ] Confirm both worktrees contain only intended changes.
- [ ] Commit and push the paper branch.
- [ ] Commit and push the Obsidian `main` branch.

Run:

```bash
git status --short
git diff --check
git -C "/Users/rootliu/Documents/Obsidian Vault" status --short
git -C "/Users/rootliu/Documents/Obsidian Vault" diff --check
git push origin codex/v19-separability-revision
git -C "/Users/rootliu/Documents/Obsidian Vault" push origin main
```
