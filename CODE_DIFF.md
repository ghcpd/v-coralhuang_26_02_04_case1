# Code changes for ClickHouse tuple parsing fix

Modified files:

- `sqlglot/parser.py`
  - Added handling for numeric positional access after dotted expressions (e.g. `tuple(...).2`).
  - When a DOT is followed by a NUMBER token, the parser now constructs a `StructExtract` expression using the numeric literal as the key. This allows `tuple(1 AS a, ...).2` to parse correctly even when tuple elements are aliased.
  - The change is generic (not ClickHouse-specific) and applies wherever dot-number access appears. It preserves existing behavior for other dialects.

- `tests/test_clickhouse_tuple.py`
  - New pytest cases covering:
    - tuple with aliased args + positional access inside CAST (round-trip)
    - tuple with aliased args without positional access
    - tuple without aliased args but with positional access (round-trip)
    - malformed tuple syntax negative test

- `run_tests.ps1`
  - One-click test runner for Windows using `python -m pytest`.

- `README.md`
  - Notes about the bug fix and how to run tests.

Rationale and design notes:

- The parser already had `_parse_struct` which supports aliased elements (by delegating to `_parse_lambda(alias=True)`). The parsing failure was triggered when dot-number positional access followed a parsed struct/function call: the parser's generic DOT handling did not special-case numeric indices and could end up with an incomplete parse (field == None).

- Adding a small branch in `_parse_column` to detect `DOT NUMBER` and construct `StructExtract` preserves the parser's general architecture and keeps behavior consistent across dialects. This also covers ClickHouse because the tokenizer maps `TUPLE` to the `STRUCT` token and `_parse_struct` is used to parse tuple(...) calls.

- The solution avoids hard-coding for the specific reproduction SQL; it generalizes to other struct-like function calls and numeric dotted access.

Backward compatibility:

- This change is minimally invasive and only affects parsing when a DOT is followed immediately by a NUMBER. Existing behavior for other cases is unchanged.
