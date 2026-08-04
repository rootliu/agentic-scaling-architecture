# Task 4a Fix Round 1 Report

Date: 2026-08-05
Worktree: `C:\Users\liuya\Documents\Deep Research\agentic-v22-worktree`
Branch: `codex/v22-focused-thesis`
Review base: `84e56e7437dfd186b63a8d883de4100bffc82342`

## Status

DONE_WITH_CONCERNS

The fix round is implemented, rebuilt, visually inspected, verified, and
ready for the commit recorded after this report is staged.

## Root Cause

`clean_math()` removed braces before applying a subscript regex that accepted
only a single alphanumeric operand. The real source formula is at
`academy/agentic-runtime-preprint/paper_source/main.tex:242` and contains
`B_{E,k}`. Before the fix, that became `B<sub>E</sub>,k`, leaving `,k` at the
normal text baseline. Signed and other compound forms were similarly
malformed.

The global `escape()` helper also preserved every literal exact `<sub>` and
`<super>` tag in source text. Balanced, unmatched, or crossed literal tags
could therefore become ReportLab markup or cause XML parsing failures.

## TDD Evidence

The smallest regression tests were added before the production fix and run
against the pre-fix behavior. The captured RED evidence was:

- `B_{E,k}` rendered as `B<sub>E</sub>,k`.
- `x_{i,j}` rendered as `x<sub>i</sub>,j`.
- `x_{-1}` remained `x_-1`.
- Literal rich-text tags were preserved instead of being XML-escaped, and
  the parser regression test failed on the unsafe markup path.
- PDF character geometry showed `E` lowered while `,k` remained at the normal
  baseline.

## Implementation

- Added renderer-owned ASCII sentinels for subscript and superscript markup.
- Changed `escape()` to XML-escape all text and restore only those sentinels.
- Converted braced compound subscripts before brace removal.
- Extended simple subscript handling to signed operands while retaining the
  repaired simple forms.
- Added unit coverage for simple, compound, signed, and hat forms.
- Added real ReportLab parsing coverage for balanced, unmatched, and crossed
  literal tags.
- Added a generated-PDF character-geometry assertion for the real compound
  subscript behavior.
- Scoped the `Chief Information Officer` assertion to Figure 1.

## Verification

Focused tests, final tree:

```text
Ran 4 tests in 1.327s
OK
```

The final complete preprint suite was run with:

```text
C:\Users\liuya\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest discover -s academy\agentic-runtime-preprint\tests -p test_*.py -v
```

Result:

```text
Ran 18 tests in 5.970s
OK
```

The v22 PDF was rebuilt with:

```text
C:\Users\liuya\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe academy\agentic-runtime-preprint\latex_to_preprint.py --paper-dir academy\agentic-runtime-preprint\paper_source
```

The final output is
`academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf`.

The final PDF has 16 pages and exactly one caption for each Figure 1 through
Figure 8. The repaired formula geometry reports:

```text
formula_words=['B', 'E,k', 'in', 'every', 'required']
operand_chars=[('E', 317.176), (',', 317.176), ('k', 317.176)]
baseline_delta=6.566
top_spread=0.0
```

The v21 release remains byte-for-byte unchanged:

```text
52DE73D7B3AF0CE20E632B929EB8BE4365C7CBC713805F949E5BE656F901969A
```

`git diff --check` passed. The only accompanying messages were existing
environment warnings about the global Git ignore path and LF-to-CRLF
normalization; no whitespace errors were reported.

## Visual Inspection

Pages 10 and 13 were the only pages with detected geometry changes between
the pre-fix and rebuilt v22 PDFs. Both were rendered at 220 DPI and inspected.
Page 10 retained the figure, formula text, margins, and page flow without
clipping or overlap. Page 13 showed the `B` subscript `E,k` on one lowered
baseline, with the surrounding paragraph and page transition intact.

## Concerns

The bundled Poppler rasterizer emitted non-fatal warnings that display fonts
`Symbol` and `ArialUnicode` were unavailable. It still rendered both affected
pages successfully and the images were readable; the PDF tests, extracted
geometry, and final artifact checks all passed.

## Changed Files

- `academy/agentic-runtime-preprint/latex_to_preprint.py`
- `academy/agentic-runtime-preprint/tests/test_v22_rendering.py`
- `academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf`
- `.superpowers/sdd/2026-08-04-v22-focused-thesis-revision/2026-08-04-task-4a-fix-1-report.md`

The Obsidian repository and prior release PDFs were not modified.

Commit SHA: recorded in the final Git commit metadata reported with this task.
