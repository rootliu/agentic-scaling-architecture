import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pdfplumber
from pypdf import PdfReader
from reportlab.platypus import SimpleDocTemplate


PREPRINT_DIR = Path(__file__).resolve().parents[1]
RENDERER = PREPRINT_DIR / "latex_to_preprint.py"
PAPER_SOURCE = PREPRINT_DIR / "paper_source"


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
    def test_default_output_is_a_v20_pdf_beside_the_renderer(self):
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v20-default-") as tmp:
            isolated_preprint = Path(tmp) / "agentic-runtime-preprint"
            isolated_preprint.mkdir()
            isolated_renderer = isolated_preprint / RENDERER.name
            isolated_source = isolated_preprint / "paper_source"
            shutil.copy2(RENDERER, isolated_renderer)
            shutil.copytree(PAPER_SOURCE, isolated_source)

            result = subprocess.run(
                [
                    sys.executable,
                    str(isolated_renderer),
                    "--paper-dir",
                    str(isolated_source),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            expected = (
                isolated_preprint
                / "output"
                / "pdf"
                / "Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf"
            )

            self.assertTrue(expected.is_file())
            self.assertEqual(result.stdout.strip(), str(expected))

    def test_v20_pdf_encodes_the_enterprise_responsibility_model(self):
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v20-test-") as tmp:
            output = Path(tmp) / "Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf"
            subprocess.run(
                [
                    sys.executable,
                    str(RENDERER),
                    "--paper-dir",
                    str(PAPER_SOURCE),
                    "--output",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            reader = PdfReader(str(output))

        self.assertIn("v20", reader.metadata.subject)
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

    def test_v20_tables_keep_enterprise_labels_intact(self):
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v20-test-") as tmp:
            output = Path(tmp) / "Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf"
            subprocess.run(
                [
                    sys.executable,
                    str(RENDERER),
                    "--paper-dir",
                    str(PAPER_SOURCE),
                    "--output",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            reader = PdfReader(str(output))

        rendered_text = re.sub(
            r"\s+",
            " ",
            "\n".join(page.extract_text() or "" for page in reader.pages),
        )
        self.assertIn("Enterprise-runtime responsibility architecture", rendered_text)
        self.assertIn("Business/use-case", rendered_text)
        self.assertIn("System/runtime", rendered_text)

    def test_v20_responsibility_table_does_not_split_boundary_header(self):
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v20-test-") as tmp:
            output = Path(tmp) / "Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf"
            subprocess.run(
                [
                    sys.executable,
                    str(RENDERER),
                    "--paper-dir",
                    str(PAPER_SOURCE),
                    "--output",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            with pdfplumber.open(output) as pdf:
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

    def test_v20_conclusion_does_not_orphan_its_final_clause(self):
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v20-test-") as tmp:
            output = Path(tmp) / "Scalable_Manageable_Agentic_Runtime_Preprint_v20.pdf"
            subprocess.run(
                [
                    sys.executable,
                    str(RENDERER),
                    "--paper-dir",
                    str(PAPER_SOURCE),
                    "--output",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            reader = PdfReader(str(output))

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
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v20-table-") as tmp:
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
