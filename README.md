# ClickHouse Tuple Parsing Fix

## Overview

This fix addresses a parsing issue in sqlglot when parsing valid ClickHouse SQL involving tuple expressions with aliased elements and positional access.

### Problem
The ClickHouse dialect in sqlglot was unable to parse `tuple()` expressions where arguments used aliases (e.g., `1 AS a`). This is valid ClickHouse SQL and executes successfully in ClickHouse, but sqlglot would fail with a `ParseError`.

**Example of failing SQL:**
```sql
SELECT CAST(tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`).2 AS Nullable(String))
```

Error message:
```
ParseError: Expecting ). Line 1, Col: 22.
```

### Root Cause
The ClickHouse dialect tokenizes the keyword `TUPLE` as `TokenType.STRUCT`, but there was no function parser registered for the "TUPLE" function name. When the parser encountered `tuple(...)`, it would attempt to parse the arguments using the default function argument parser, which does not support aliases.

### Solution
Added a function parser for "TUPLE" in the ClickHouse dialect that uses the same parsing logic as "STRUCT" (which supports aliases through `_parse_lambda(alias=True)`).

**Change Made:**
- File: `sqlglot/dialects/clickhouse.py`
- Added `"TUPLE": lambda self: self._parse_struct()` to the `FUNCTION_PARSERS` dictionary in the ClickHouse `Parser` class

This allows tuple arguments to be parsed with aliases, making the behavior consistent with how STRUCT is parsed in other dialects.

## Features
- ✅ Parse tuple expressions with aliased arguments
- ✅ Support positional tuple access (e.g., `.2`)
- ✅ Work with CAST and ClickHouse-specific types (e.g., `Nullable(String)`)
- ✅ Maintain backward compatibility with existing tuple parsing
- ✅ No breaking changes to other dialects

## Usage

### Running Tests

#### Windows (Command Prompt or PowerShell)
```bash
run_tests.bat
```

#### Windows with Python
```bash
python -m pytest tests/test_clickhouse_tuple_fix.py -v
```

#### Other Platforms
```bash
python -m pytest tests/test_clickhouse_tuple_fix.py -v
```

### Example: Using the Fix

Before the fix, this would fail:
```python
import sqlglot as sg

result = sg.parse_one(
    "SELECT CAST(tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`).2 AS Nullable(String))",
    read="clickhouse"
)
print(result)
# Now works successfully!
```

## Test Coverage

The fix includes 17 comprehensive tests covering:

1. **Tuple with aliased args and positional access inside CAST** - The main reproduction case
2. **Tuple with aliased args without positional access** - Basic alias support
3. **Tuple without aliased args but with positional access** - Regression test for existing functionality
4. **Basic tuple without aliases** - Backward compatibility
5. **Single aliased element** - Edge case
6. **Mixed aliased and non-aliased arguments** - Real-world scenarios
7. **Round-trip parsing** - Parse → serialize → parse consistency
8. **Nested tuples** - Complex expressions
9. **CAST with Nullable type** - ClickHouse-specific types
10. **String literals with aliases** - Different data types
11. **Tuple in WHERE clause** - Different SQL contexts
12. **Malformed syntax detection** - Error handling
13. **Complex expressions with aliases** - Real-world usage
14. **Backtick-quoted aliases** - ClickHouse identifier quoting
15. **Other dialects not affected** - Backward compatibility

Run all tests with:
```bash
run_tests.bat
```

Or run specific tests with:
```bash
python -m pytest tests/test_clickhouse_tuple_fix.py::TestClickHouseTupleWithAliases::test_tuple_with_aliased_args_and_positional_access_in_cast -v
```

## Prerequisites

- **Python**: 3.11 or compatible version
- **Dependencies**: sqlglot (included in repository)
- **Testing**: pytest

## Implementation Details

### What Changed
1. **`sqlglot/dialects/clickhouse.py`**: Added TUPLE function parser

### Why This Works
- The existing `_parse_struct()` method in the base `Parser` class already supports parsing arguments with aliases via `_parse_lambda(alias=True)`
- By registering a FUNCTION_PARSERS entry for "TUPLE" that calls `_parse_struct()`, ClickHouse tuple expressions now support the same aliased argument syntax as other SQL dialects
- This change is minimal and leverages existing, well-tested parsing infrastructure

### Backward Compatibility
- ✅ All existing tuple parsing without aliases continues to work
- ✅ Other dialects (DuckDB, PostgreSQL, etc.) are unaffected
- ✅ No changes to expression types or AST structure
- ✅ No breaking changes to the API

## Verification

The fix has been verified to:
1. Parse the exact SQL from the bug report without errors
2. Generate correct AST structures
3. Support round-trip parsing (parse → serialize → parse)
4. Maintain backward compatibility with existing code
5. Not affect other SQL dialects

Example verification:
```python
import sqlglot as sg

# Original failing SQL
sql = "SELECT CAST(tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`).2 AS Nullable(String))"
parsed = sg.parse_one(sql, read="clickhouse")
print(parsed)  # Works!

# Round-trip verification
serialized = parsed.sql(dialect="clickhouse")
reparsed = sg.parse_one(serialized, read="clickhouse")
print(reparsed)  # Works again!
```

## References

- ClickHouse Tuple documentation: https://clickhouse.com/docs/en/sql-reference/data-types/tuple
- sqlglot Parser implementation: `sqlglot/parser.py`
- ClickHouse Dialect: `sqlglot/dialects/clickhouse.py`

## Questions or Issues?

For issues with this fix, please refer to the test suite in `tests/test_clickhouse_tuple_fix.py` and the code diff in `CODE_DIFF.md`.
