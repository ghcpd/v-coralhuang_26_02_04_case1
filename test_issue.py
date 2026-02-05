#!/usr/bin/env python3
"""Test script to reproduce the tuple parsing issue"""

import sqlglot as sg

print("=" * 60)
print("Testing ClickHouse tuple parsing issue")
print("=" * 60)

test_sql = "SELECT CAST(tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`).2 AS Nullable(String))"
print(f"\nTest SQL:\n{test_sql}\n")

try:
    result = sg.parse_one(test_sql, read="clickhouse")
    print("✓ SUCCESS: Parsed successfully!")
    print(f"\nParsed AST:\n{result}")
    print(f"\nSerialized back:\n{result.sql(dialect='clickhouse')}")
except Exception as e:
    print(f"✗ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
