"""Keep the shipped v28 PDF frozen while v29 evolves."""
import hashlib
import unittest
from pathlib import Path

class V28FrozenTests(unittest.TestCase):
    def test_v28_release_stays_frozen(self):
        p = Path(__file__).resolve().parents[1] / "output/pdf/Scalable_Manageable_Agentic_Runtime_Preprint_v28.pdf"
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), "6e5d3e12e226311219f12189577f88c3bcd757c2b7b6b0ef8140b61c2340f19b")
