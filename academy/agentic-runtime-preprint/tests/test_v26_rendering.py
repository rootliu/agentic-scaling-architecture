"""v26 evidence-audited manuscript rendering tests."""
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import importlib.util
from pathlib import Path

from pypdf import PdfReader


PREPRINT_DIR = Path(__file__).resolve().parents[1]
RENDERER = PREPRINT_DIR / "latex_to_preprint.py"
PAPER_SOURCE = PREPRINT_DIR / "paper_source"
PDF_DIR = PREPRINT_DIR / "output" / "pdf"


def release(version: str) -> Path:
    return PDF_DIR / f"Scalable_Manageable_Agentic_Runtime_Preprint_{version}.pdf"


FROZEN = {
    "v21": "52DE73D7B3AF0CE20E632B929EB8BE4365C7CBC713805F949E5BE656F901969A",
    "v22": "E01761D7CC20459FC15D70EC8A47ED68C90D7104426EAA240FBCFCB8998CDF1A",
    "v23": "545F1A8A6C9D825A7A02CC298D32707BF48C8AB7E75E60C32F3E4B5FDA427DC4",
    "v25": "DFD7A8F30FA5E70CABE1A34E2948EA94B791A870B2AC8C58B86FA73EF71A96B6",
}


def rendered_text(reader: PdfReader) -> str:
    return re.sub(r"\s+", " ", "\n".join(p.extract_text() or "" for p in reader.pages))


def figure_page_text(reader: PdfReader, figure_number: int) -> str:
    marker = f"Figure {figure_number}."
    for page in reader.pages:
        text = page.extract_text() or ""
        if marker in text:
            return re.sub(r"\s+", " ", text)
    raise AssertionError(f"{marker} is missing from the rendered PDF")


def figure_captions(reader: PdfReader) -> dict[int, str]:
    text = rendered_text(reader)
    matches = list(re.finditer(r"\bFigure\s+(\d+)\.\s+", text))
    captions: dict[int, str] = {}
    for match, nxt in zip(matches, matches[1:] + [None]):
        number = int(match.group(1))
        if number in captions:
            raise AssertionError(f"Figure {number} has more than one caption")
        end = nxt.start() if nxt else len(text)
        captions[number] = text[match.end() : end].strip()
    return captions


class V26RenderingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory(prefix="agentic-runtime-v26-")
        out = Path(cls._tmp.name) / "v26.pdf"
        subprocess.run(
            [
                sys.executable,
                str(RENDERER),
                "--paper-dir",
                str(PAPER_SOURCE),
                "--output",
                str(out),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.reader = PdfReader(str(out))
        cls.text = rendered_text(cls.reader)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_default_build_writes_v26_and_preserves_frozen_releases(self):
        before = {
            version: hashlib.sha256(release(version).read_bytes()).hexdigest().upper()
            for version in FROZEN
        }
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v26-default-") as tmp:
            isolated = Path(tmp) / "agentic-runtime-preprint"
            isolated.mkdir()
            shutil.copy2(RENDERER, isolated / RENDERER.name)
            shutil.copytree(PAPER_SOURCE, isolated / "paper_source")
            result = subprocess.run(
                [
                    sys.executable,
                    str(isolated / RENDERER.name),
                    "--paper-dir",
                    str(isolated / "paper_source"),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            expected = (
                isolated
                / "output"
                / "pdf"
                / "Scalable_Manageable_Agentic_Runtime_Preprint_v26.pdf"
            )
            self.assertTrue(expected.is_file())
            self.assertEqual(result.stdout.strip(), str(expected))
        after = {
            version: hashlib.sha256(release(version).read_bytes()).hexdigest().upper()
            for version in FROZEN
        }
        self.assertEqual(before, FROZEN)
        self.assertEqual(after, FROZEN)

    def test_contributions_are_reduced_to_three_auditable_claims(self):
        for term in (
            "contract-bounded runtime architecture",
            "source-preserving data substrate",
            "falsifiable measurement protocol",
        ):
            self.assertIn(term, self.text)

    def test_canonical_sources_remain_authoritative(self):
        for term in (
            "canonical raw or source-native records",
            "auditable derivatives rather than the sole authority",
            "ranked discovery",
            "versioned source evidence",
        ):
            self.assertIn(term, self.text)

    def test_p16_and_p17_are_narrowly_falsifiable(self):
        for term in (
            "task-family evidence-path sufficiency",
            "bounded policy-contract decoupling",
            "metadata-only input",
            "shuffled indexes",
            "artifact-change oracle",
        ):
            self.assertIn(term, self.text)

    def test_memory_records_observable_evidence_not_private_reasoning(self):
        self.assertIn("rather than private chain-of-thought", self.text)
        self.assertIn("retention", self.text)
        self.assertIn("deletion", self.text)

    def test_three_new_sources_resolve_to_official_arxiv_records(self):
        bib = (PAPER_SOURCE / "references.bib").read_text(encoding="utf-8")
        for identifier in ("2606.29251", "2607.26497", "2608.06305"):
            self.assertIn(f"https://arxiv.org/abs/{identifier}", bib)

    def test_eight_captions_state_shown_significance_and_class(self):
        captions = figure_captions(self.reader)
        self.assertEqual(set(captions), set(range(1, 9)))
        for number, caption in captions.items():
            self.assertRegex(
                caption,
                r"\bShown:\s+\S.+?\bWhy it matters:\s+\S.+?"
                r"\bClass:\s+(?:architecture|protocol|proposed measurement design)\b",
                f"Figure {number} caption must state shown, significance, and class",
            )

    def test_vector_figure_uses_v26_hypothesis_labels(self):
        text = figure_page_text(self.reader, 8)
        for term in (
            "Evidence-path sufficiency",
            "Policy-contract decoupling",
            "Intervention and control",
            "Falsification or inconclusive condition",
        ):
            self.assertIn(term, text, f"Figure 8 must render {term!r}")
        self.assertNotIn("Summary reconstruction", text)
        self.assertNotIn("Registry change control", text)

    def test_all_seven_figure_images_are_embedded(self):
        images = 0
        for page in self.reader.pages:
            resources = page.get("/Resources", {})
            xobjects = resources.get("/XObject", {}) if resources else {}
            for name in (xobjects or {}):
                if xobjects[name].get("/Subtype") == "/Image":
                    images += 1
        self.assertEqual(images, 7, "figures 1-7 must each embed their PNG")

    def test_png_figures_do_not_duplicate_the_responsibility_band(self):
        spec = importlib.util.spec_from_file_location("v26_renderer", RENDERER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        figure = module.FigureGraphic(
            "dual_scaling",
            height=176,
            paper_dir=str(PAPER_SOURCE),
        )
        self.assertIsNotNone(figure.image_path)
        self.assertEqual(figure.height, figure.content_height)

    def test_every_citation_resolves_and_no_entry_is_unused(self):
        tex = (PAPER_SOURCE / "main.tex").read_text(encoding="utf-8")
        bib = (PAPER_SOURCE / "references.bib").read_text(encoding="utf-8")
        used = {
            key.strip()
            for match in re.finditer(r"\\cite\{([^}]*)\}", tex)
            for key in match.group(1).split(",")
        }
        have = {
            match.group(1).strip()
            for match in re.finditer(r"@\w+\{([^,]+),", bib)
        }
        self.assertEqual(used - have, set(), "citation without a bib entry")
        self.assertEqual(have - used, set(), "bib entry never cited")

    def test_standing_risks_are_not_softened(self):
        for term in (
            "no completed runtime implementation",
            "would not mean that independence has been proven",
            "least evidenced part of this work",
        ):
            self.assertIn(term, self.text)


if __name__ == "__main__":
    unittest.main()
