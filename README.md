# SQLGlot ClickHouse Tuple Fix

## Bug fixed

Fixed parsing of ClickHouse `tuple()` expressions when elements use aliases (e.g. `1 AS `a``) and are accessed positionally (e.g. `.2`). This previously failed to parse under the ClickHouse dialect.

## How to run tests (Windows)

Prerequisites:
- Python 3.11
- install dev dependencies (pytest)

Run tests:

powershell -File run_tests.ps1

Or:

python -m pytest
