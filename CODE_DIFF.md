# Code changes for ClickHouse tuple parsing bug

Modified files:

1. `sqlglot/dialects/clickhouse.py`
   - Added `TUPLE` handling in the ClickHouse `Parser.FUNCTION_PARSERS` mapping to delegate parsing of `tuple(...)` calls to the existing `_parse_struct` implementation. This enables aliasing support within function arguments (e.g., `1 AS a`).
   - Added a generator transform mapping so that `exp.Struct` expressions serialize to the ClickHouse `tuple(...)` function using `rename_func("tuple")`.
   - Rationale: ClickHouse uses `tuple(...)` as a struct-like function. Reusing the `_parse_struct` parsing logic ensures aliased elements are parsed consistently with other struct-like constructs such as `STRUCT(...)` and avoids introducing ad-hoc special-casing. Mapping the expression back to `tuple(...)` in the generator ensures round-trip `parse -> sql -> parse` correctness.

2. `tests/test_clickhouse_tuple.py` (new)
   - Added unit tests exercising the following scenarios under the ClickHouse dialect:
     - tuple with aliased args + positional access inside CAST (roundtrip parse/serialize/parse)
     - tuple with aliased args without positional access
     - tuple without aliased args but with positional access (regression test)
     - a negative test ensuring malformed tuple syntax raises a `ParseError`

3. `run_tests.py` (new)
   - A one-click test runner that runs pytest (`python run_tests.py`) and exits with a non-zero exit code when tests fail. Works on Windows and other platforms.

4. `README.md` (new/updated)
   - Documents the bug fix, test running instructions on Windows, and prerequisites.

Design notes and tradeoffs:
- The solution extends ClickHouse dialect parsing by mapping the textual function name `TUPLE` to the existing `_parse_struct` parser. That parser already accepts aliased lambda-style arguments (via `alias=True`), so using it avoids duplicating parsing logic.
- We represent `tuple(...)` function calls in the AST as `exp.Struct` nodes. This keeps the AST consistent with other struct-like constructs.
- The ClickHouse generator maps `exp.Struct` back to the `tuple` function name so that serialization yields `tuple(...)` rather than `struct(...)`.
- This change is dialect-local (inside `dialects/clickhouse.py`) and does not alter parsing for other dialects.

Backward compatibility:
- Existing behavior for other dialects is unchanged. SQL that parsed prior to this change should continue to parse
- The fix only affects function name `tuple` in a ClickHouse context and how `exp.Struct` is serialized for ClickHouse dialect output.

Testing:
- Tests were implemented as pytest tests in `tests/test_clickhouse_tuple.py`.
- The tests perform round-trip checks for the positive cases and ensure errors for malformed input.

