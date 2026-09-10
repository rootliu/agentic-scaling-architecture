import unittest
from ir_contract import Registry, Rejected, fixture


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.source, self.contract = fixture()
        self.registry = Registry(self.source)

    def test_revocation_after_prepare_invalidates_ticket(self):
        ticket = self.registry.prepare(self.contract, 10)
        self.registry.update(owners=frozenset())
        with self.assertRaisesRegex(Rejected, "REVALIDATE"):
            self.registry.execute(ticket, 10)

    def test_same_version_content_replacement_is_detected(self):
        self.registry.update(content=b"revenue=900")
        with self.assertRaisesRegex(Rejected, "SOURCE_CHANGED"):
            self.registry.prepare(self.contract, 10)

    def test_expiry_between_prepare_and_read(self):
        ticket = self.registry.prepare(self.contract, 99)
        with self.assertRaisesRegex(Rejected, "STALE"):
            self.registry.execute(ticket, 100)

    def test_replay_of_read_is_stable(self):
        ticket = self.registry.prepare(self.contract, 10)
        self.assertEqual(self.registry.execute(ticket, 10), self.registry.execute(ticket, 10))

    def test_compatible_revalidation_retains_bytes(self):
        ticket = self.registry.prepare(self.contract, 10)
        before = self.registry.execute(ticket, 10)
        self.registry.update(expires=200)
        after = self.registry.execute(self.registry.prepare(self.contract, 10), 10)
        self.assertEqual(before["bytes"], after["bytes"])
        self.assertNotEqual(before["epoch"], after["epoch"])


if __name__ == "__main__":
    unittest.main()
