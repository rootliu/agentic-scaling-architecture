# Task 3 Report: Redesign the Figures and Cut the v22 Release

## Implementation Summary

- Set `PREPRINT_VERSION` to `v22`, retaining version-derived default output so
  the renderer cannot overwrite the archived v21 release.
- Added a reusable orthogonal-arrow primitive with segment validation.
- Redesigned Figure 1 around the capability-to-Harness-to-Scaffold causal
  contract, governed data/evidence lane, and measurement plane.
- Redesigned Figures 4, 5, and 6 as legible contract paths with orthogonal,
  non-crossing connectors.
- Replaced Figure 8 with the required four-column falsification matrix. P1 is
  the dominant row; P15-P17 are visually subordinate diagnostics.
- Added the v22 changelog entry covering the focused thesis, experimental unit,
  estimand, responsibility correction, three-way decision rule, classical
  novelty boundary, figure redesign, and v21 preservation.
- Generated the 16-page v22 release PDF with subject metadata
  `v22 enterprise agentic runtime responsibility architecture`.

## Test-Contract Correction

The original v21 release-specific tests rebuilt current `main.tex` with the
current renderer while merely assigning a v21 output filename. Once the
renderer correctly became v22, those tests no longer examined v21 at all; they
examined current v22 content under a stale name. This was a test defect, not a
release regression.

Per the explicit conflict resolution, the v21 content and layout assertions
now inspect the frozen `V21_RELEASE` artifact directly, and a dedicated test
requires its fixed SHA-256. Generic renderer-unit tests continue to load and
exercise the current renderer. `test_v22_rendering.py` and `main.tex` were not
edited.

## Files Changed

- `academy/agentic-runtime-preprint/latex_to_preprint.py`
- `academy/agentic-runtime-preprint/CHANGELOG.md`
- `academy/agentic-runtime-preprint/tests/test_v21_rendering.py`
- `academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf`
- `.superpowers/sdd/2026-08-04-v22-focused-thesis-revision/task-3-report.md`

## RED Evidence

The fresh pre-implementation RED state had already been verified with:

```powershell
& 'C:\Users\liuya\Documents\code\stock-prediction\.venv\Scripts\python.exe' -m unittest discover -s academy\agentic-runtime-preprint\tests -p 'test_v22_rendering.py' -v
```

Observed result:

```text
test_default_v22_build_uses_new_filename_and_preserves_v21_release ... FAIL
test_v22_figures_encode_focused_contract_labels ... FAIL
test_v22_pdf_defines_all_eight_captions_with_semantic_classification ... ok
test_v22_pdf_encodes_focused_thesis_and_responsibility_contract ... FAIL

Ran 4 tests
FAILED (failures=3)
```

The failures were the expected production gaps: absent v22 default output,
v21 metadata, and missing focused-contract labels in the figures. The semantic
caption contract already passed after Task 2.

## Build and GREEN Evidence

Release build:

```powershell
& 'C:\Users\liuya\Documents\code\stock-prediction\.venv\Scripts\python.exe' academy\agentic-runtime-preprint\latex_to_preprint.py --paper-dir academy\agentic-runtime-preprint\paper_source
```

Output:

```text
C:\Users\liuya\Documents\Deep Research\agentic-v22-worktree\academy\agentic-runtime-preprint\output\pdf\Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf
```

Focused GREEN:

```powershell
& 'C:\Users\liuya\Documents\code\stock-prediction\.venv\Scripts\python.exe' -m unittest discover -s academy\agentic-runtime-preprint\tests -p 'test_v22_rendering.py' -v
```

```text
Ran 4 tests in 2.211s
OK
```

Full-suite GREEN:

```powershell
& 'C:\Users\liuya\Documents\code\stock-prediction\.venv\Scripts\python.exe' -m unittest discover -s academy\agentic-runtime-preprint\tests -p 'test_*.py' -v
```

```text
Ran 14 tests in 4.983s
OK
```

`git diff --check` completed with exit code 0. A protected-file diff check also
confirmed that `paper_source/main.tex` and `tests/test_v22_rendering.py` are
unchanged.

## v21 Preservation Evidence

Command:

```powershell
Get-FileHash academy\agentic-runtime-preprint\output\pdf\Scalable_Manageable_Agentic_Runtime_Preprint_v21.pdf -Algorithm SHA256
```

Observed SHA-256:

```text
52DE73D7B3AF0CE20E632B929EB8BE4365C7CBC713805F949E5BE656F901969A
```

This exactly matches the frozen v21 baseline and the literal enforced by both
release suites.

## Visual Self-Review

Rendered and inspected pages 2, 7, 8, 9, and 14, which contain Figures 1, 4,
5, 6, and 8 respectively.

- Figure 1: causal sequence, governed-data lane, and measurement plane are
  legible; connectors do not cross; no text is clipped.
- Figure 4: the main-agent loop, semantic join, and termination gate are clear;
  the return path is orthogonal and does not intersect labels.
- Figure 5: authority-to-evidence path is linear and aligned; duty labels fit.
- Figure 6: all three lanes remain independently readable; vertical mappings
  align without crossings.
- Figure 8: the four required headers fit; P1 is explicitly labeled and
  visually dominant; secondary protocols are subordinate; no text clips.

Poppler reported missing display-font mappings for `Symbol` and `ArialUnicode`
while producing the PNGs. The rendered pages and extracted PDF text were
complete, so this is an environment warning rather than an artifact defect.
