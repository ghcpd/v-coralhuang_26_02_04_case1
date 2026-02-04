# sqlglot (local workspace)

## Bug fix: ClickHouse tuple(...) with aliased elements and positional access

What was fixed:
- The ClickHouse dialect parser now correctly accepts function calls written as `tuple(...)` where the tuple arguments include aliased elements (e.g., `1 AS `a``), and supports positional access like `.2` after the tuple (e.g., `tuple(...).2`).
- Casts targeting ClickHouse-specific types (e.g., `CAST(... AS Nullable(String))`) continue to work with these tuple expressions.

How to run tests (Windows):

Prerequisites:
- Python 3.11
- Install dev/test dependencies: `pip install -r requirements-dev.txt` (if applicable)

One-command run:
- From the repository root, run:

    python run_tests.py

This runs the pytest test-suite and exits with non-zero status if tests fail.

Notes:
- Tests are implemented using pytest and placed under the `tests/` directory.
- The ClickHouse-specific parser changes are in `sqlglot/dialects/clickhouse.py` and new tests are in `tests/test_clickhouse_tuple.py`.
