"""Frozen v27 formal-foundations release checks.

v28 added three verified citations and the Intermediate-Relation abbreviation
disambiguation, so paper_source/ no longer renders v27. Following the treatment
v27 gave v26, this file pins the shipped v27 artifact instead of rebuilding it.
"""
import hashlib
import unittest
from pathlib import Path

from pypdf import PdfReader


PREPRINT_DIR = Path(__file__).resolve().parents[1]
V27_RELEASE = (
    PREPRINT_DIR
    / "output"
    / "pdf"
    / "Scalable_Manageable_Agentic_Runtime_Preprint_v27.pdf"
)
V27_SHA256 = "69101CC292745DA8C9FA710EDC6BF59E49E86A26BF151C018C1CA35CE5761671"


class V27RenderingTests(unittest.TestCase):
    def test_v27_release_artifact_stays_frozen(self):
        self.assertTrue(V27_RELEASE.is_file())
        self.assertEqual(
            hashlib.sha256(V27_RELEASE.read_bytes()).hexdigest().upper(),
            V27_SHA256,
        )
        self.assertTrue(PdfReader(str(V27_RELEASE)).metadata.subject.startswith("v27"))


if __name__ == "__main__":
    unittest.main()
