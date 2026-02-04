Bugfix: ClickHouse tuple parsing

What was fixed:
- Parser now accepts aliased arguments inside struct-like functions (e.g., tuple/struct) in ClickHouse.
- Positional access on tuple expressions (e.g. `.2`) works with aliased elements.

Running tests (Windows):
- Prerequisites: Python 3.11, dependencies from project
- Run: powershell -File run_tests.ps1
