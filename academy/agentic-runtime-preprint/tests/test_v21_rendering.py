import importlib.util
import hashlib
import re
import tempfile
import unittest
from pathlib import Path

import pdfplumber
from pypdf import PdfReader
from reportlab.platypus import SimpleDocTemplate


PREPRINT_DIR = Path(__file__).resolve().parents[1]
RENDERER = PREPRINT_DIR / "latex_to_preprint.py"
V21_RELEASE = (
    PREPRINT_DIR
    / "output"
    / "pdf"
    / "Scalable_Manageable_Agentic_Runtime_Preprint_v21.pdf"
)
V21_SHA256 = "52DE73D7B3AF0CE20E632B929EB8BE4365C7CBC713805F949E5BE656F901969A"


def load_renderer():
    spec = importlib.util.spec_from_file_location("latex_to_preprint", RENDERER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def figure_page_text(reader: PdfReader, figure_number: int) -> str:
    return re.sub(r"\s+", " ", figure_page(reader, figure_number).extract_text() or "")


def figure_page(reader: PdfReader, figure_number: int):
    marker = f"Figure {figure_number}."
    for page in reader.pages:
        text = page.extract_text() or ""
        if marker in text:
            return page
    raise AssertionError(f"{marker} is missing from the rendered PDF")


def rendered_text_baseline(page, prefix: str) -> float:
    baselines = []

    def capture(text, cm, tm, _font, _size):
        if text.strip().startswith(prefix):
            baselines.append(cm[5] + tm[5])

    page.extract_text(visitor_text=capture)
    if len(baselines) != 1:
        raise AssertionError(
            f"Expected one rendered text item beginning {prefix!r}, got {baselines!r}"
        )
    return baselines[0]


class V20RenderingTests(unittest.TestCase):
    def test_archived_v21_release_is_preserved_byte_for_byte(self):
        self.assertTrue(V21_RELEASE.is_file())
        actual = hashlib.sha256(V21_RELEASE.read_bytes()).hexdigest().upper()
        self.assertEqual(actual, V21_SHA256)

    def test_v21_pdf_encodes_the_enterprise_responsibility_model(self):
        reader = PdfReader(str(V21_RELEASE))

        self.assertIn("v21", reader.metadata.subject)
        expected_by_figure = {
            1: [
                "Business capability: Skill-as-Code",
                "Runtime governance: Harness",
                "Execution and control boundary: Scaffold",
                "CIO-governed semantic and telemetry foundation: data substrate",
            ],
            2: [
                "Business capability: Skill-as-Code",
                "Runtime governance: Harness",
                "Execution and control boundary: Scaffold",
            ],
            3: [
                "Runtime governance: Harness",
                "CIO-governed semantic and telemetry foundation: data substrate",
            ],
            4: [
                "Business capability: Skill-as-Code",
                "CIO-governed semantic and telemetry foundation: data substrate",
            ],
            5: [
                "Runtime governance: Harness",
                "Execution and control boundary: Scaffold",
                "CIO-governed semantic and telemetry foundation: data substrate",
            ],
            6: [
                "Runtime governance: Harness",
                "Execution and control boundary: Scaffold",
            ],
            7: [
                "Business capability: Skill-as-Code",
                "Runtime governance: Harness",
            ],
            8: [
                "Business/use-case evaluation",
                "System/runtime evaluation",
                "P15",
                "fixed proposal bank",
                "separate (c)-(a) and (c)-(b) margins",
                "multi-seed online",
                "first-attempt grading",
                "independent grader",
                "phantom-violation oracle",
                "P16",
                "strict held-out",
                "token-matched direct reading",
                "metadata-only",
                "field ablation",
                "shuffled summaries",
                "joint contrast",
                "P17",
                "preregistered dependency graph",
                "artifact-change oracle",
                "expected versus unanticipated propagation",
            ],
        }
        for figure_number, expected_terms in expected_by_figure.items():
            text = figure_page_text(reader, figure_number)
            for expected_term in expected_terms:
                self.assertIn(
                    expected_term,
                    text,
                    f"Figure {figure_number} must render {expected_term!r}",
                )

        all_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        self.assertEqual(
            all_text.count("Evidence plane"),
            1,
            "The compact evidence-plane table must render its visible header",
        )

        figure_five = figure_page(reader, 5)
        catalog_baseline = rendered_text_baseline(
            figure_five, "semantic catalog"
        )
        governance_baseline = rendered_text_baseline(
            figure_five, "independent data governance; no task"
        )
        self.assertGreaterEqual(
            abs(catalog_baseline - governance_baseline),
            14,
            "Figure 5's CIO data-foundation annotations must not overlap",
        )

    def test_v21_tables_keep_enterprise_labels_intact(self):
        reader = PdfReader(str(V21_RELEASE))

        rendered_text = re.sub(
            r"\s+",
            " ",
            "\n".join(page.extract_text() or "" for page in reader.pages),
        )
        self.assertIn("Enterprise-runtime responsibility architecture", rendered_text)
        self.assertIn("Business/use-case", rendered_text)
        self.assertIn("System/runtime", rendered_text)

    def test_v21_tables_have_sequential_captions_and_accurate_references(self):
        reader = PdfReader(str(V21_RELEASE))

        rendered_text = re.sub(
            r"\s+",
            " ",
            "\n".join(page.extract_text() or "" for page in reader.pages),
        )
        expected_captions = [
            "Table 1. Enterprise ownership, typical change cadence, and stable contract.",
            "Table 2. Responsibility boundaries in the proposed architecture.",
            "Table 3. Claim types and evidence status.",
            "Table 4. Two required evidence planes for enterprise adoption.",
        ]
        for caption in expected_captions:
            self.assertIn(caption, rendered_text)
        expected_references = [
            "Table 1 is a responsibility model",
            "Table 2 instead states the ownership",
            "Table 3 separates claim type",
            "both planes in Table 4",
        ]
        for reference in expected_references:
            self.assertIn(reference, rendered_text)

    def test_v21_pdf_has_no_raw_math_control_leaks(self):
        reader = PdfReader(str(V21_RELEASE))

        rendered_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        for raw_leak in ("lambda", "sigma_out", "AND over", ">="):
            self.assertNotIn(raw_leak, rendered_text)

    def test_rendered_references_preserve_traceability_fields(self):
        renderer = load_renderer()
        tex = r"""
        \documentclass{article}
        Traceable source \cite{traceable}.
        \begin{document}
        \end{document}
        """
        bib = r"""
        @article{traceable,
          title={Traceable Runtime Evidence},
          author={Example, Ada},
          journal={Systems Journal},
          year={2026},
          date={2026-06-01},
          volume={14},
          number={4},
          pages={28--31},
          doi={10.1234/example.2026.1},
          url={https://example.org/release}
        }
        """
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v21-reference-") as tmp:
            output = Path(tmp) / "references.pdf"
            story = renderer.build_story(tex, bib, renderer.make_styles())
            SimpleDocTemplate(str(output)).build(story)
            reader = PdfReader(str(output))

        rendered_text = re.sub(
            r"\s+",
            " ",
            "\n".join(page.extract_text() or "" for page in reader.pages),
        )
        self.assertIn("2026-06-01.", rendered_text)
        self.assertIn("Volume 14, issue 4, pages 28-31.", rendered_text)
        self.assertIn("DOI: 10.1234/example.2026.1.", rendered_text)
        self.assertIn("URL: https://example.org/release.", rendered_text)

    def test_figure_eight_shows_directed_runtime_contracts(self):
        reader = PdfReader(str(V21_RELEASE))

        figure_eight = figure_page_text(reader, 8)
        expected_relationships = [
            "Skill -> Harness: versioned capability contract",
            "Harness -> Scaffold: admission + compatible capacity binding",
            "Harness <-> data substrate: semantic join + governed evidence",
            "Scaffold -> Harness: enforceable execution facts",
        ]
        for relationship in expected_relationships:
            self.assertIn(relationship, figure_eight)

    def test_v21_responsibility_table_does_not_split_boundary_header(self):
        with pdfplumber.open(V21_RELEASE) as pdf:
            responsibility_page = next(
                page
                for page in pdf.pages
                if "Responsibility boundaries in the proposed architecture."
                in (page.extract_text() or "")
            )
            words = responsibility_page.extract_words()

        boundary_words = [word for word in words if word["text"] == "Boundary"]
        self.assertEqual(
            len(boundary_words),
            1,
            "Boundary must render as exactly one PDF word box",
        )
        boundary = boundary_words[0]
        for label in ("Business", "Runtime", "Physical", "Enterprise"):
            candidates = [
                word
                for word in words
                if word["text"] == label and word["x0"] > boundary["x0"]
            ]
            self.assertTrue(candidates, f"Missing responsibility-table header {label!r}")
            header_word = min(
                candidates,
                key=lambda word: abs(word["top"] - boundary["top"]),
            )
            self.assertAlmostEqual(
                header_word["top"],
                boundary["top"],
                delta=0.5,
                msg=f"Boundary must share the header line with {label}",
            )
            self.assertAlmostEqual(
                header_word["bottom"],
                boundary["bottom"],
                delta=0.5,
                msg=f"Boundary must share the header line with {label}",
            )

    def test_v21_conclusion_does_not_orphan_its_final_clause(self):
        reader = PdfReader(str(V21_RELEASE))

        conclusion_page = next(
            page
            for page in reader.pages
            if "12. Conclusion" in (page.extract_text() or "")
        )
        conclusion_text = re.sub(r"\s+", " ", conclusion_page.extract_text() or "")
        self.assertIn(
            "organizational, or economic conditions under which they do not.",
            conclusion_text,
            "The Conclusion must not leave its final clause on a continuation page",
        )

    def test_split_tables_repeat_the_header_on_every_page(self):
        renderer = load_renderer()
        rows = "\n".join(
            f"row {number} & detail {number} \\\\" for number in range(1, 41)
        )
        block = rf"""
        \begin{{table}}
        \begin{{tabular}}{{ll}}
        Repeated header A & Repeated header B \\
        {rows}
        \end{{tabular}}
        \end{{table}}
        """
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v21-table-") as tmp:
            output = Path(tmp) / "split-table.pdf"
            story = renderer.table_from_latex(block, renderer.make_styles(), {})
            SimpleDocTemplate(
                str(output),
                pagesize=(360, 220),
                leftMargin=18,
                rightMargin=18,
                topMargin=18,
                bottomMargin=18,
            ).build(story)
            reader = PdfReader(str(output))

        table_pages = [
            (page_number, re.sub(r"\s+", " ", page.extract_text() or ""))
            for page_number, page in enumerate(reader.pages, start=1)
            if "row " in (page.extract_text() or "")
        ]
        self.assertGreater(len(table_pages), 1)
        for page_number, text in table_pages:
            self.assertIn(
                "Repeated header A",
                text,
                f"Split table page {page_number} must repeat its header",
            )


if __name__ == "__main__":
    unittest.main()
