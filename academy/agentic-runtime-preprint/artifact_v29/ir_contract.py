"""Executable specification of a 5W1H+Which data-use contract.

Standard-library, in-process reference model, NOT a security sandbox or LLM
runtime. Authoritative records and policy are trusted inputs; a real adapter
must implement the same check-and-read boundary with appropriate isolation.
"""
from dataclasses import dataclass, replace
from hashlib import sha256
from threading import RLock


def digest(value: bytes) -> str:
    return sha256(value).hexdigest()


@dataclass(frozen=True)
class Source:
    source_id: str
    version: str
    content: bytes
    unit: str
    period: str
    domain: str
    owners: frozenset[str]
    expires: int
    relation: str


@dataclass(frozen=True)
class Contract:
    source_id: str
    version: str
    source_digest: str
    theme_version: str
    principal: str
    domain: str
    unit: str
    period: str
    rationale_id: str
    relation: str
    operation: str
    max_bytes: int


@dataclass(frozen=True)
class Ticket:
    contract: Contract
    epoch: int


class Rejected(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


class Registry:
    def __init__(self, source: Source):
        self.source = source
        self.epoch = 0
        self.theme_version = "theme-v1"
        self.rationales = frozenset({"revenue-reconciliation"})
        self.lock = RLock()

    def update(self, **changes):
        with self.lock:
            self.source = replace(self.source, **changes)
            self.epoch += 1

    def check(self, c: Contract, now: int):
        s = self.source
        checks = (
            (c.source_id == s.source_id and c.version == s.version
             and c.source_digest == digest(s.content), "SOURCE_CHANGED"),
            (c.theme_version == self.theme_version, "THEME_CHANGED"),
            (c.principal in s.owners, "UNAUTHORIZED"),
            (c.domain == s.domain, "WRONG_DOMAIN"),
            (now < s.expires and c.period == s.period, "STALE"),
            (c.unit == s.unit, "SEMANTIC_MISMATCH"),
            (c.rationale_id in self.rationales, "UNAPPROVED_RATIONALE"),
            (c.relation == s.relation, "RELATION_MISMATCH"),
            (c.operation == "read", "OPERATION_DENIED"),
            (0 < len(s.content) <= c.max_bytes, "BUDGET_EXCEEDED"),
        )
        for passed, code in checks:
            if not passed:
                raise Rejected(code)

    def prepare(self, c: Contract, now: int) -> Ticket:
        with self.lock:
            self.check(c, now)
            return Ticket(c, self.epoch)

    def execute(self, ticket: Ticket, now: int) -> dict:
        with self.lock:
            if ticket.epoch != self.epoch:
                raise Rejected("REVALIDATE")
            self.check(ticket.contract, now)
            s = self.source
            return {"bytes": s.content.decode("utf-8"), "source": s.source_id,
                    "version": s.version, "digest": digest(s.content),
                    "epoch": self.epoch, "unit": s.unit, "period": s.period,
                    "operation": "read"}


def fixture():
    s = Source("sales", "snapshot-v1", b"revenue=120", "USD", "2026Q2",
               "internal", frozenset({"analyst"}), 100, "product-id")
    c = Contract(s.source_id, s.version, digest(s.content), "theme-v1", "analyst",
                 "internal", "USD", "2026Q2", "revenue-reconciliation",
                 "product-id", "read", 64)
    return s, c
