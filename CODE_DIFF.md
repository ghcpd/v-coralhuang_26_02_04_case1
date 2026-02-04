Modified files:
- sqlglot/parser.py: Adjusted function argument parsing to allow aliased arguments for struct-like functions (TokenType.STRUCT). This enables parsing ClickHouse's tuple(...) where elements may be aliased.
- tests/test_clickhouse_tuple.py: Added unit tests covering aliased tuple args, positional access, and malformed tuple negative test.
- run_tests.ps1: One-click test runner for Windows.
- README.md: Documentation of bugfix and instructions.

Why:
- ClickHouse allows tuple elements to be aliased and accessed positionally. The parser previously used a lambda parser that didn't accept aliases for generic functions, while struct parsing used alias-aware lambda parsing. Aligning function arg parsing for struct token solves the issue without special-casing specific function names.

Trade-offs:
- We enable alias parsing for any function tokenized as STRUCT. This is intentional and aligns with how STRUCT/tuple semantics are handled. It should not affect other dialects since TokenType.STRUCT is specific to struct-like constructs.
