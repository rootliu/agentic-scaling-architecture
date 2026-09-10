# Executable data-use contract reference model

This artifact checks a small portion of the v29 proposal. It is a trusted,
single-process executable specification, not a production security boundary.

Run from this directory with Python 3.10 or newer, using only the standard library:

```sh
python3 evaluate.py
python3 -m unittest -v test_contract.py
```

`results/fault-cases.csv` contains all 1,024 combinations of ten binary fault
dimensions, including the one valid fixture. `results/summary.json` records
the interpreter version and source hashes. The independent oracle accepts
exactly the unmutated fixture, because every declared mutation breaks one
specified requirement. This is finite specification conformance, not a random
sample or a production failure-rate estimate. Multiple faults return the first
failed predicate; diagnostic completeness is not measured.

Five lifecycle tests cover revocation, unchanged-name content replacement,
expiry during queuing, stable read replay, and compatible revalidation.
No LLM or paid API is called. No throughput, retrieval-quality, cross-tenant,
adversarial, or distributed-consistency experiment is performed. P1 is not
evaluated. The test domain and implementation were designed together in this
revision; there is no claim of preregistered or independent external validation.

The reference registry uses a conservative global epoch. Fine-grained dependency
invalidation is specified in the paper but not implemented. The read returns
source identity and bytes; semantic entailment and publication validation are
outside this implementation. Any real adapter must implement atomic revalidation
and reading, and must obtain principal, policy and source descriptors from trusted
authorities. Direct access to registry internals is trusted in this model.
