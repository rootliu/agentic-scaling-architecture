"""Frozen v25 merged-manuscript release checks."""
import hashlib
import unittest
from pathlib import Path

from pypdf import PdfReader


PREPRINT_DIR = Path(__file__).resolve().parents[1]
V25_RELEASE = (
    PREPRINT_DIR
    / "output"
    / "pdf"
    / "Scalable_Manageable_Agentic_Runtime_Preprint_v25.pdf"
)
V25_SHA256 = "DFD7A8F30FA5E70CABE1A34E2948EA94B791A870B2AC8C58B86FA73EF71A96B6"


class V25RenderingTests(unittest.TestCase):
    def test_v25_release_artifact_stays_frozen(self):
        self.assertTrue(V25_RELEASE.is_file())
        self.assertEqual(
            hashlib.sha256(V25_RELEASE.read_bytes()).hexdigest().upper(),
            V25_SHA256,
        )
        self.assertTrue(PdfReader(str(V25_RELEASE)).metadata.subject.startswith("v25"))


if __name__ == "__main__":
    unittest.main()
