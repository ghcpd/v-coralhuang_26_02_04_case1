# Sqlglot

## Bug Fix: ClickHouse Tuple Parsing with Aliased Elements

A parsing issue existed when using sqlglot to parse valid ClickHouse SQL involving tuple expressions with aliased elements and positional access.

The issue has been fixed by updating the ClickHouse dialect parser to allow aliases in function arguments for the TUPLE function.

## How to Run Tests

On Windows, run the `run_tests.bat` script:

```
run_tests.bat
```

This will run the test suite using pytest. Ensure Python 3.11 and pytest are installed.

Prerequisites:
- Python 3.11
- pytest (install with `pip install pytest`)

## Fixed SQL

The following SQL now parses correctly:

```sql
SELECT CAST(tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`).2 AS Nullable(String))
```