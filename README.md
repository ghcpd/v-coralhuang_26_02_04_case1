# sqlglot (local fork)

## Bug fix: ClickHouse tuple alias & positional access parsing ✅

Summary
- Fixed a parsing bug in the ClickHouse dialect that made SQL like

  SELECT CAST(tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`).2 AS Nullable(String))

  fail to parse. The ClickHouse `tuple()` function allows aliased elements, and positional access (e.g. `.2`) should work with such tuples. This change allows `tuple()` arguments to include aliases and preserves positional access and CAST behavior.

How to run tests (Windows)
1. Install Python 3.11 and create or activate your environment.
2. Install project test requirements (if any). In most environments, the project only needs `pytest` to run tests:

   python -m pip install -U pytest

3. From the repository root run:

   python run_tests.py

The script will run the test suite using `pytest` and exit with a non-zero code if any test fails.

Prerequisites
- Python 3.11 (the repository is developed against 3.11 in CI)
- `pytest` for running tests

Files added/modified
- `sqlglot/dialects/clickhouse.py` — parser adjusted to support aliased tuple arguments
- `tests/test_clickhouse_tuple.py` — unit tests covering positive and negative cases and round-trip parsing
- `run_tests.py` — one-click test runner
- `README.md` — this documentation
- `CODE_DIFF.md` — summary of code changes
