"""v28 citation-completion release tests.

v28 closes three gaps found by auditing the local PDF library against the
bibliography: each of the three added sources backs a claim that previously had
no external support. It also disambiguates the Intermediate Relation from the
compiler sense of "IR". These tests pin that the citations are present *with*
their delineation, so a later edit cannot quietly turn a bounded citation into
an unqualified endorsement.
"""
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
    "v26": "E4211A9312E14FC801BC6F92C6CB612EF0375ABE60D0D4E161143766971F1D4A",
    "v27": "69101CC292745DA8C9FA710EDC6BF59E49E86A26BF151C018C1CA35CE5761671",
}


class V28RenderingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory(prefix="agentic-runtime-v28-")
        out = Path(cls._tmp.name) / "v28.pdf"
        subprocess.run(
            [sys.executable, str(RENDERER), "--paper-dir", str(PAPER_SOURCE),
             "--output", str(out)],
            check=True, capture_output=True, text=True,
        )
        cls.reader = PdfReader(str(out))
        cls.text = re.sub(r"\s+", " ",
                          "\n".join(p.extract_text() or "" for p in cls.reader.pages))

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_default_build_writes_v28_and_preserves_frozen_releases(self):
        before = {v: hashlib.sha256(release(v).read_bytes()).hexdigest().upper()
                  for v in FROZEN}
        with tempfile.TemporaryDirectory(prefix="agentic-runtime-v28-default-") as tmp:
            isolated = Path(tmp) / "agentic-runtime-preprint"
            isolated.mkdir()
            shutil.copy2(RENDERER, isolated / RENDERER.name)
            shutil.copytree(PAPER_SOURCE, isolated / "paper_source")
            result = subprocess.run(
                [sys.executable, str(isolated / RENDERER.name),
                 "--paper-dir", str(isolated / "paper_source")],
                check=True, capture_output=True, text=True,
            )
            expected = (isolated / "output" / "pdf"
                        / "Scalable_Manageable_Agentic_Runtime_Preprint_v28.pdf")
            self.assertTrue(expected.is_file())
            self.assertEqual(result.stdout.strip(), str(expected))
        after = {v: hashlib.sha256(release(v).read_bytes()).hexdigest().upper()
                 for v in FROZEN}
        self.assertEqual(before, FROZEN)
        self.assertEqual(after, FROZEN)

    def test_memoharness_is_cited_as_asset_not_as_safe_policy(self):
        self.assertIn("MemoHarness", self.text)
        self.assertIn("harness state is a governed asset", self.text)
        self.assertIn("not as evidence that any particular accumulation policy is safe",
                      self.text)

    def test_coagent_justifies_the_interface_not_a_mechanism(self):
        self.assertIn("CoAgent", self.text)
        self.assertIn("ordering contract as a declared interface", self.text)
        self.assertIn("rather than to adopt any specific mechanism", self.text)
        self.assertIn("we make no throughput or contention claim of our own", self.text)

    def test_agentforesight_is_delineated_from_coverage(self):
        self.assertIn("AgentForesight", self.text)
        self.assertIn("predicting that a run is likely to fail is a different problem",
                      self.text)
        self.assertIn("demand an independent event inventory", self.text)

    def test_intermediate_relation_is_disambiguated_from_intermediate_representation(self):
        self.assertIn("IR more often denotes an intermediate representation", self.text)
        self.assertIn("Our IR is not that", self.text)

    def test_every_citation_resolves_and_no_entry_is_unused(self):
        tex = (PAPER_SOURCE / "main.tex").read_text(encoding="utf-8")
        bib = (PAPER_SOURCE / "references.bib").read_text(encoding="utf-8")
        used = {k.strip() for m in re.finditer(r"\\cite\{([^}]*)\}", tex)
                for k in m.group(1).split(",")}
        have = {m.group(1).strip() for m in re.finditer(r"@\w+\{([^,]+),", bib)}
        self.assertEqual(used - have, set(), "citation without a bib entry")
        self.assertEqual(have - used, set(), "bib entry never cited")

    def test_three_new_keys_carry_verified_metadata(self):
        """Titles and author lists were read from each PDF's /Title and /Author,
        not transcribed from the local filename, which this audit proved unreliable."""
        bib = (PAPER_SOURCE / "references.bib").read_text(encoding="utf-8")
        for key, title, first_author in (
            ("huang2026memoharness",
             "MemoHarness: Agent Harnesses That Learn from Experience", "Huang, Yue"),
            ("lyu2026coagent",
             "CoAgent: Concurrency Control for Multi-Agent Systems", "Lyu, Hongtao"),
            ("zhang2026agentforesight",
             "AgentForesight: Online Auditing for Early Failure Prediction",
             "Zhang, Boxuan"),
        ):
            self.assertIn(key, bib)
            self.assertIn(title, bib)
            self.assertIn(first_author, bib)

    def test_latex_source_stays_ascii(self):
        """A stray CJK character slipped into an English sentence while drafting
        the IR disambiguation; this guards the class of defect."""
        tex = (PAPER_SOURCE / "main.tex").read_text(encoding="utf-8")
        offenders = [(i + 1, line) for i, line in enumerate(tex.split("\n"))
                     if any(ord(c) > 127 for c in line)]
        self.assertEqual(offenders, [], f"non-ASCII in main.tex: {offenders[:3]}")

    def test_all_seven_figure_images_are_embedded(self):
        images = 0
        for page in self.reader.pages:
            resources = page.get("/Resources", {})
            xobjects = resources.get("/XObject", {}) if resources else {}
            for name in (xobjects or {}):
                if xobjects[name].get("/Subtype") == "/Image":
                    images += 1
        self.assertEqual(images, 7)

    def test_renderer_still_exposes_title_override(self):
        result = subprocess.run([sys.executable, str(RENDERER), "--help"],
                                check=True, capture_output=True, text=True)
        self.assertIn("--title", result.stdout)


if __name__ == "__main__":
    unittest.main()
