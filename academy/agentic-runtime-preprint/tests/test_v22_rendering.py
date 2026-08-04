import hashlib
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
from reportlab.platypus import Paragraph


PREPRINT_DIR = Path(__file__).resolve().parents[1]
RENDERER = PREPRINT_DIR / "latex_to_preprint.py"
PAPER_SOURCE = PREPRINT_DIR / "paper_source"
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


def render_pdf(output: Path) -> PdfReader:
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
    return PdfReader(str(output))


def rendered_text(reader: PdfReader) -> str:
    return re.sub(
        r"\s+",
        " ",
        "\n".join(page.extract_text() or "" for page in reader.pages),
    )


def figure_page_text(reader: PdfReader, figure_number: int) -> str:
    marker = f"Figure {figure_number}."
    for page in reader.pages:
        text = page.extract_text() or ""
        if marker in text:
            return re.sub(r"\s+", " ", text)
    raise AssertionError(f"{marker} is missing from the rendered PDF")


def rendered_figure_captions(reader: PdfReader) -> dict[int, str]:
    text = rendered_text(reader)
    matches = list(re.finditer(r"\bFigure\s+(\d+)\.\s+", text))
    captions = {}
    for match, next_match in zip(matches, matches[1:] + [None]):
        figure_number = int(match.group(1))
        if figure_number in captions:
            raise AssertionError(f"Figure {figure_number} has more than one caption")
        end = next_match.start() if next_match else len(text)
        captions[figure_number] = text[match.end() : end].strip()
    return captions


class V22RenderingTests(unittest.TestCase):
    def test_default_v22_build_uses_new_filename_and_preserves_v21_release(self):
        before = hashlib.sha256(V21_RELEASE.read_bytes()).hexdigest().upper()
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v22-default-") as tmp:
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
                / "Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf"
            )

            self.assertTrue(expected.is_file())
            self.assertEqual(result.stdout.strip(), str(expected))

        after = hashlib.sha256(V21_RELEASE.read_bytes()).hexdigest().upper()
        self.assertEqual(before, V21_SHA256)
        self.assertEqual(after, V21_SHA256)

    def test_v22_pdf_encodes_focused_thesis_and_responsibility_contract(self):
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v22-test-") as tmp:
            reader = render_pdf(
                Path(tmp) / "Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf"
            )

        self.assertTrue(reader.metadata.subject.startswith("v22"))
        text = rendered_text(reader)
        for expected_term in (
            "supported within Omega",
            "falsified within Omega",
            "inconclusive",
            "cluster-period",
            "randomized crossover",
            "activated capability configuration c",
            "Scaffold capacity configuration s",
            "runtime response R(c,s)",
            "semantic outcome Q(c,s)",
            "enforcement overhead E(c,s)",
            "declared operating region Omega",
            "capability-by-Scaffold interaction estimand",
            "reset or washout",
            "cluster-aware uncertainty",
            "activated independently deployable behavior on admitted paths",
            "activated behavior",
            "Harness owns logical admission and control",
            "Scaffold owns physical execution and isolation",
        ):
            self.assertIn(expected_term, text)

    def test_v22_pdf_defines_all_eight_captions_with_semantic_classification(self):
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v22-captions-") as tmp:
            reader = render_pdf(
                Path(tmp) / "Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf"
            )

        captions = rendered_figure_captions(reader)
        self.assertEqual(
            set(captions),
            set(range(1, 9)),
            "The rendered PDF must contain exactly one caption for each Figure 1 through Figure 8",
        )
        for figure_number, caption in captions.items():
            self.assertRegex(
                caption,
                r"\bShown:\s+\S.+?\bWhy it matters:\s+\S.+?"
                r"\bClass:\s+(?:architecture|protocol|proposed measurement design)\b",
                f"Figure {figure_number} caption must state shown, significance, and class",
            )

    def test_v22_figures_encode_focused_contract_labels(self):
        expected_by_figure = {
            1: [
                "Capability change",
                "Harness contract",
                "Scaffold capacity",
                "Governed data and evidence",
                "Measurement plane",
            ],
            4: [
                "Main agent",
                "Bounded sub-agents",
                "Verifier / semantic join",
                "Termination gate",
            ],
            5: [
                "Data authority",
                "Resolved contract",
                "Isolated fetch",
                "Evidence bundle",
            ],
            6: ["Logical control", "Physical execution", "Evidence"],
            8: [
                "Hypothesis",
                "Intervention and control",
                "Evidence plane",
                "Falsification or inconclusive condition",
            ],
        }

        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v22-figures-") as tmp:
            reader = render_pdf(
                Path(tmp) / "Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf"
            )

        for figure_number, expected_terms in expected_by_figure.items():
            text = figure_page_text(reader, figure_number)
            for expected_term in expected_terms:
                self.assertIn(
                    expected_term,
                    text,
                    f"Figure {figure_number} must render {expected_term!r}",
                )

    def test_figure_two_uses_the_canonical_harness_contract_fields(self):
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v22-contract-") as tmp:
            output = Path(tmp) / "Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf"
            render_pdf(output)
            with pdfplumber.open(output) as pdf:
                page = next(
                    page
                    for page in pdf.pages
                    if "Figure 2." in (page.extract_text() or "")
                )
                words = page.extract_words(use_text_flow=True, keep_blank_chars=False)
                title_top = next(
                    word["top"]
                    for word in words
                    if word["text"] == "From"
                )
                caption_top = next(
                    current["top"]
                    for current, following in zip(words, words[1:])
                    if current["text"] == "Figure" and following["text"] == "2."
                )
                figure_text = re.sub(
                    r"\s+",
                    " ",
                    page.crop((0, title_top - 2, page.width, caption_top)).extract_text()
                    or "",
                )

        for expected_row in (
            "I / O typed inputs and outputs",
            "G activated Skill graph",
            "A authority, effects + evidence duties",
            "B time, cost, token, concurrency budgets",
            "V policy, model, data, capability, verifier + trace versions",
        ):
            self.assertIn(expected_row, figure_text)

    def test_v22_pdf_repairs_formula_typography_and_first_use_acronyms(self):
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v22-typography-") as tmp:
            reader = render_pdf(
                Path(tmp) / "Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf"
            )

        text = rendered_text(reader)
        for forbidden in (
            "Delta_R",
            "Q_req",
            "K_min",
            "gamma_j",
            "nu_j",
            "eta_j",
            "widehatE_k",
        ):
            self.assertNotIn(
                forbidden,
                text,
                f"source-like formula token {forbidden!r} must not appear in the rendered PDF",
            )
        self.assertIn(
            "Monitor, Analyze, Plan, Execute over a shared Knowledge base (MAPE-K)",
            text,
        )
        self.assertIn(
            "Chief Information Officer",
            figure_page_text(reader, 1),
        )

    def test_clean_math_formats_simple_compound_signed_and_hat_subscripts(self):
        renderer = load_renderer()
        expected = {
            "x_i": "x<sub>i</sub>",
            "B_{E,k}": "B<sub>E,k</sub>",
            "x_{i,j}": "x<sub>i,j</sub>",
            "x_{-1}": "x<sub>-1</sub>",
            r"\widehat{E}_k(c,s)": "E-hat<sub>k</sub>(c,s)",
        }

        for source, rendered in expected.items():
            with self.subTest(source=source):
                self.assertEqual(renderer.escape(renderer.clean_math(source)), rendered)

    def test_escape_treats_literal_rich_text_tags_as_text_and_paragraph_parses(self):
        renderer = load_renderer()
        sources = (
            "literal <sub>balanced</sub> text",
            "literal <sub>unmatched text",
            "literal <sub>crossed</super> text",
        )

        for source in sources:
            with self.subTest(source=source):
                escaped = renderer.escape(source)
                self.assertNotIn("<sub>", escaped)
                self.assertNotIn("</sub>", escaped)
                self.assertNotIn("<super>", escaped)
                self.assertNotIn("</super>", escaped)
                self.assertIn("&lt;", escaped)
                self.assertIn("&gt;", escaped)
                Paragraph(escaped).wrap(300, 100)

    def test_v22_pdf_keeps_compound_subscript_on_one_lowered_baseline(self):
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v22-geometry-") as tmp:
            output = Path(tmp) / "Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf"
            render_pdf(output)
            with pdfplumber.open(output) as pdf:
                page = next(
                    page
                    for page in pdf.pages
                    if "component budget" in (page.extract_text() or "")
                )
                words = page.extract_words(use_text_flow=True, keep_blank_chars=False)

            phrase_index = next(
                index
                for index, (current, following) in enumerate(zip(words, words[1:]))
                if current["text"] == "component" and following["text"] == "budget"
            )
            formula_words = words[phrase_index + 2 : phrase_index + 7]
            self.assertGreaterEqual(len(formula_words), 3)
            self.assertEqual(formula_words[0]["text"], "B")

            base_top = formula_words[0]["top"]
            next_word = formula_words[3]
            operand_chars = [
                char
                for char in page.chars
                if formula_words[0]["x1"] <= char["x0"] <= next_word["x0"]
                and char["text"] in "E,k"
                and base_top <= char["top"] <= base_top + 10
            ]
            self.assertEqual("".join(char["text"] for char in operand_chars), "E,k")
            subscript_tops = [char["top"] for char in operand_chars]
            self.assertGreater(min(subscript_tops) - base_top, 3.0)
            self.assertLess(max(subscript_tops) - min(subscript_tops), 0.5)


if __name__ == "__main__":
    unittest.main()
