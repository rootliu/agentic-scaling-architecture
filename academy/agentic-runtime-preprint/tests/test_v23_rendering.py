import hashlib
import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

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
V22_RELEASE = (
    PREPRINT_DIR
    / "output"
    / "pdf"
    / "Scalable_Manageable_Agentic_Runtime_Preprint_v22.pdf"
)
V21_SHA256 = "52DE73D7B3AF0CE20E632B929EB8BE4365C7CBC713805F949E5BE656F901969A"
V22_SHA256 = "E01761D7CC20459FC15D70EC8A47ED68C90D7104426EAA240FBCFCB8998CDF1A"


def load_renderer():
    spec = importlib.util.spec_from_file_location("latex_to_preprint", RENDERER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def unpack_preprint(tmp: Path) -> Path:
    isolated_preprint = tmp / "agentic-runtime-preprint"
    isolated_preprint.mkdir()
    shutil.copy2(RENDERER, isolated_preprint / RENDERER.name)
    shutil.copytree(PAPER_SOURCE, isolated_preprint / "paper_source")
    return isolated_preprint


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


class V23RenderingTests(unittest.TestCase):
    def test_default_v23_build_uses_new_filename_and_preserves_prior_releases(self):
        before = [
            hashlib.sha256(V21_RELEASE.read_bytes()).hexdigest().upper(),
            hashlib.sha256(V22_RELEASE.read_bytes()).hexdigest().upper(),
        ]
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v23-default-") as tmp:
            isolated_preprint = unpack_preprint(Path(tmp))
            result = subprocess.run(
                [
                    sys.executable,
                    str(isolated_preprint / RENDERER.name),
                    "--paper-dir",
                    str(isolated_preprint / "paper_source"),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            expected = (
                isolated_preprint
                / "output"
                / "pdf"
                / "Scalable_Manageable_Agentic_Runtime_Preprint_v23.pdf"
            )
            self.assertTrue(expected.is_file())
            self.assertEqual(result.stdout.strip(), str(expected))

        after = [
            hashlib.sha256(V21_RELEASE.read_bytes()).hexdigest().upper(),
            hashlib.sha256(V22_RELEASE.read_bytes()).hexdigest().upper(),
        ]
        self.assertEqual(before, [V21_SHA256, V22_SHA256])
        self.assertEqual(after, [V21_SHA256, V22_SHA256])

    def test_v23_pdf_encodes_focused_thesis_and_responsibility_contract(self):
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v23-test-") as tmp:
            reader = render_pdf(
                Path(tmp) / "Scalable_Manageable_Agentic_Runtime_Preprint_v23.pdf"
            )

        self.assertTrue(reader.metadata.subject.startswith("v23"))
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

    def test_v23_pdf_adds_threat_model_and_methodological_repairs(self):
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v23-threat-") as tmp:
            reader = render_pdf(
                Path(tmp) / "Scalable_Manageable_Agentic_Runtime_Preprint_v23.pdf"
            )

        text = rendered_text(reader)
        for expected_term in (
            "Trusted computing base",
            "Untrusted model output",
            "Semi-trusted Skills",
            "Untrusted external content",
            "Adversary capabilities",
            "contract resolution, rather than instruction filtering",
            "two one sided tests (TOST) rule at level 0.05",
            "a 10% multiplicative change in p95 tail latency",
            "family-wise error rule",
            "minimum detectable interaction at 80% power",
            "41 clusters per treatment order",
            "per-cell timeout rate",
            "non-interference",
            "Reference monitors and least authority",
            "Control loops, quality models, and queueing",
            "Contemporary agentic-runtime work",
            "Novelty boundary",
        ):
            self.assertIn(expected_term, text)

    def test_v23_pdf_defines_all_eight_captions_with_semantic_classification(self):
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v23-captions-") as tmp:
            reader = render_pdf(
                Path(tmp) / "Scalable_Manageable_Agentic_Runtime_Preprint_v23.pdf"
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

    def test_v23_figures_encode_focused_contract_labels(self):
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
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v23-figures-") as tmp:
            reader = render_pdf(
                Path(tmp) / "Scalable_Manageable_Agentic_Runtime_Preprint_v23.pdf"
            )

        for figure_number, expected_terms in expected_by_figure.items():
            text = figure_page_text(reader, figure_number)
            for expected_term in expected_terms:
                self.assertIn(
                    expected_term,
                    text,
                    f"Figure {figure_number} must render {expected_term!r}",
                )

    def test_v23_pdf_keeps_formula_typography_clean(self):
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v23-typography-") as tmp:
            reader = render_pdf(
                Path(tmp) / "Scalable_Manageable_Agentic_Runtime_Preprint_v23.pdf"
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
            "\\Omega",
            "{",
            "}",
            "??",
        ):
            self.assertNotIn(
                forbidden,
                text,
                f"source-like token {forbidden!r} must not appear in the rendered PDF",
            )
        self.assertIn(
            "Monitor, Analyze, Plan, Execute over a shared Knowledge base (MAPE-K)",
            text,
        )
        self.assertIn("Chief Information Officer", figure_page_text(reader, 1))

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


if __name__ == "__main__":
    unittest.main()