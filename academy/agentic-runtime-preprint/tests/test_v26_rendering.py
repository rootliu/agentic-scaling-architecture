"""Frozen v26 evidence-audited release checks."""
import hashlib
import unittest
from pathlib import Path

from pypdf import PdfReader


PREPRINT_DIR = Path(__file__).resolve().parents[1]
V26_RELEASE = (
    PREPRINT_DIR
    / "output"
    / "pdf"
    / "Scalable_Manageable_Agentic_Runtime_Preprint_v26.pdf"
)
V26_SHA256 = "E4211A9312E14FC801BC6F92C6CB612EF0375ABE60D0D4E161143766971F1D4A"


class V26RenderingTests(unittest.TestCase):
    def test_v26_release_artifact_stays_frozen(self):
        self.assertTrue(V26_RELEASE.is_file())
        self.assertEqual(
            hashlib.sha256(V26_RELEASE.read_bytes()).hexdigest().upper(),
            V26_SHA256,
        )
        self.assertTrue(PdfReader(str(V26_RELEASE)).metadata.subject.startswith("v26"))


if __name__ == "__main__":
    unittest.main()
