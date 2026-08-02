# Task 3 Report: Unified Figure and Table Rendering

## STATUS

DONE_WITH_CONCERNS

## Changed Files

- `academy/agentic-runtime-preprint/latex_to_preprint.py`
- `academy/agentic-runtime-preprint/tests/test_v20_rendering.py`
- `.superpowers/sdd/2026-08-02-v20-enterprise-runtime-reframing/task-3-report.md`

`paper_source/main.tex` was not modified.

## RED Checks (before production changes)

Command:

```bash
/Users/rootliu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3.12 \
  -m unittest academy/agentic-runtime-preprint/tests/test_v20_rendering.py -v
```

Expected failure after the real ReportLab builder generated a temporary PDF:

```text
AssertionError: 'v20' not found in 'Scalable and manageable agentic runtime architecture'
```

The output-level test then exposed a rendered-table width defect:

```text
AssertionError: 'Enterprise-runtime responsibility architecture' not found
```

The minimal correction widened the first four-column table allocation from
`[70, 134, 146, 90]` to `[90, 124, 136, 90]`, preserving `repeatRows=1`.

## GREEN and Build Checks

Fresh regression run:

```bash
/Users/rootliu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3.12 \
  -m unittest academy/agentic-runtime-preprint/tests/test_v20_rendering.py -v
```

Result:

```text
Ran 4 tests in 1.551s
OK
```

Explicit v20 build:

```bash
/Users/rootliu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3.12 \
  academy/agentic-runtime-preprint/latex_to_preprint.py \
  --paper-dir academy/agentic-runtime-preprint/paper_source \
  --output /tmp/task3-v20-pdf-review/Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf
```

Output:

```text
/tmp/task3-v20-pdf-review/Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf
```

`pypdf` reported `pages=27` and
`subject=v20 enterprise agentic runtime responsibility architecture`;
`stat` reported `114217 bytes`.

Required brief checks:

```bash
rg -n "Skill-as-Code|Runtime governance|Execution and control boundary|CIO-governed|v20|Scalable_Manageable_Agentic_Runtime_Preprint_v20" academy/agentic-runtime-preprint/latex_to_preprint.py
rg -n "v19|production agent and workflow systems|OpenAI Assistants|AutoGen|CrewAI|LangGraph|Temporal" academy/agentic-runtime-preprint/paper_source/main.tex academy/agentic-runtime-preprint/latex_to_preprint.py
git diff --check
```

Outputs:

```text
30:PREPRINT_VERSION = "v20"
36:    "Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf",
138:            ("Business capability: Skill-as-Code", "#f0fdfa", "#2dd4bf", "#115e59"),
139:            ("Runtime governance: Harness", "#eff6ff", "#60a5fa", "#1d4ed8"),
140:            ("Execution and control boundary: Scaffold", "#fffbeb", "#f59e0b", "#92400e"),
158:            "CIO-governed semantic and telemetry foundation: data substrate",
480:        draw_wrapped(canvas, "Skill-as-Code: capability growth as a release lifecycle", 18, h - 12, w - 36,
prohibited-term check: exit 1, no output
git diff --check: exit 0, no output
```

Additional boundary checks:

```bash
rg -n "repeatRows\s*=\s*1|repeatRows" \
  academy/agentic-runtime-preprint/latex_to_preprint.py \
  academy/agentic-runtime-preprint/tests/test_v20_rendering.py
git diff --exit-code -- academy/agentic-runtime-preprint/paper_source/main.tex
shasum -a 256 \
  academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v19.pdf
stat -f '%z bytes %Sm' -t '%Y-%m-%dT%H:%M:%S%z' \
  academy/agentic-runtime-preprint/output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v19.pdf
```

Outputs:

```text
academy/agentic-runtime-preprint/latex_to_preprint.py:1054:    tbl = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
main.tex diff: exit 0, no output
d6c465089938d5bf49550df91f2f8865828bad41c9586d2b6e194f70dd440ba5
114172 bytes 2026-08-02T12:25:32+0800
```

## Eight-Figure Audit

| Figure | Rendering audit |
| --- | --- |
| 1 | Renders the common responsibility band with the four canonical labels. |
| 2 | Renders Skill-as-Code, Harness, and Scaffold responsibility labels. |
| 3 | Renders Harness and the CIO-governed data substrate label. |
| 4 | Renders Skill-as-Code and the CIO-governed data substrate label. |
| 5 | Separates the CIO data foundation from the Skill/Harness/Scaffold stack and uses a dashed governed-contract path to Harness. |
| 6 | Renders Harness and Scaffold responsibility labels. |
| 7 | Renders Skill-as-Code and Harness responsibility labels. |
| 8 | Separates `Business/use-case evaluation` from `System/runtime evaluation` and retains P15, P16, and P17 controls. |

The generated figure pages (2, 7, 10, 13, 14, 16, 17, and 19) and the revised
table page (9) were raster-reviewed. No clipping or label collisions were
observed. The responsibility band is common to all eight figures.

## Self-Check

- The data substrate remains outside the Skill/Harness/Scaffold stack and is
  explicitly CIO-governed.
- Figure 8 preserves P15-P17 and makes the business/use-case and
  system/runtime evaluation planes distinct.
- Generated tables retain `repeatRows=1`.
- PDF metadata and the default output path now identify v20.
- The v19 PDF was not overwritten: SHA-256 remains
  `d6c465089938d5bf49550df91f2f8865828bad41c9586d2b6e194f70dd440ba5`;
  size `114172` bytes; timestamp `2026-08-02T12:25:32+0800`.

## Concerns

Rasterizing the PDF for the visual review emitted Fontconfig cache warnings.
They did not occur in the builder or regression-test output and did not affect
the generated PDF. No rendering defects remain known.
