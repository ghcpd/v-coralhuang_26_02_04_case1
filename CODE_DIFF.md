# CODE_DIFF

This document lists the changes made to support parsing ClickHouse `tuple()` with aliased elements and positional access.

Modified files:

1. `sqlglot/dialects/clickhouse.py`
   - What changed: The `_parse_function` method was extended to special-case the `TUPLE` function. When `tuple` is parsed, its arguments are parsed using `self._parse_lambda(alias=True)`, which allows each tuple element to include an alias (e.g., `1 AS a` or backtick-quoted aliases). The parsed function is then handled like any other function expression.
   - Why: ClickHouse supports aliased tuple elements and positional access (e.g., `tuple(1 AS a, 2 AS b).2`). The base parser did not allow aliases inside function arguments, causing valid ClickHouse SQL to fail parsing. Handling `tuple` specially confines the permissive alias parsing to only the desired function and avoids making the base parser too permissive for all functions.
   - Backward compatibility: The change only affects the ClickHouse dialect and only when the function name is `tuple`. Other dialects and functions keep their previous parsing behavior.

2. `tests/test_clickhouse_tuple.py` (new)
   - What changed: Added unit tests covering:
     - `SELECT CAST(tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`).2 AS Nullable(String))` (parsing + round-trip)
     - `SELECT tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`)` (parsing)
     - `SELECT tuple(1, 2, 3).2` (parsing + round-trip)
     - A negative test ensuring malformed tuple syntax fails to parse (missing comma example)
   - Why: These tests ensure the fix works and prevents regressions.

3. `run_tests.py` (new)
   - What changed: Added a small script that runs `pytest` using the current Python interpreter: `python run_tests.py`.
   - Why: Provides a single-command test runner that works on Windows and exits with non-zero on test failures.

4. `README.md` (new/updated)
   - What changed: Documented the bug fix, how to run tests on Windows, and prerequisites.

Notes on implementation
- The fix avoids modifying the base parser behavior globally. Instead, it targets ClickHouse and only the `tuple` function. This keeps the parsing logic conservative and limits the surface area for potential regressions.
- The chosen approach generalizes to other struct-like functions if needed by adding additional entries in the ClickHouse parser (e.g., checking other function names and parsing their args with `alias=True`).

Trade-offs
- A small amount of duplicated logic from the base `_parse_function` is introduced to handle `tuple` specially. This is deliberate to keep the change local to the ClickHouse dialect and avoid changing the parser's semantics for all dialects.

Testing
- Run `python run_tests.py` to execute the tests. Ensure `pytest` is installed.
