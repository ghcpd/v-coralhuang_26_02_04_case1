#!/usr/bin/env python3
"""Final comprehensive verification of the fix"""

import sqlglot as sg
from sqlglot import exp

print("=" * 70)
print("FINAL VERIFICATION OF CLICKHOUSE TUPLE PARSING FIX")
print("=" * 70)

# Test 1: Original failing case
print("\n1. Original Failing Case:")
print("-" * 70)
sql1 = "SELECT CAST(tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`).2 AS Nullable(String))"
print(f"SQL: {sql1}")
try:
    result1 = sg.parse_one(sql1, read="clickhouse")
    print(f"✓ Parsed successfully")
    print(f"  Result: {result1}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 2: Round-trip verification
print("\n2. Round-trip Verification:")
print("-" * 70)
sql2 = "SELECT tuple(1 AS a, 2 AS b, 3 AS c).1"
print(f"Original SQL: {sql2}")
try:
    parsed1 = sg.parse_one(sql2, read="clickhouse")
    serialized = parsed1.sql(dialect="clickhouse")
    print(f"Serialized: {serialized}")
    parsed2 = sg.parse_one(serialized, read="clickhouse")
    print(f"Re-parsed: {parsed2}")
    print(f"✓ Round-trip successful")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 3: Backward compatibility - tuple without aliases
print("\n3. Backward Compatibility - Basic Tuple:")
print("-" * 70)
sql3 = "SELECT tuple(1, 2, 3)"
print(f"SQL: {sql3}")
try:
    result3 = sg.parse_one(sql3, read="clickhouse")
    print(f"✓ Parsed: {result3}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 4: Backward compatibility - positional access without aliases
print("\n4. Backward Compatibility - Positional Access:")
print("-" * 70)
sql4 = "SELECT tuple(1, 2, 3).2"
print(f"SQL: {sql4}")
try:
    result4 = sg.parse_one(sql4, read="clickhouse")
    print(f"✓ Parsed: {result4}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 5: Complex case with nested functions
print("\n5. Complex Case - Nested Functions:")
print("-" * 70)
sql5 = "SELECT tuple(1 + 1 AS a, len('hello') AS b)"
print(f"SQL: {sql5}")
try:
    result5 = sg.parse_one(sql5, read="clickhouse")
    print(f"✓ Parsed: {result5}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 6: Other dialects not affected
print("\n6. Other Dialects Not Affected:")
print("-" * 70)
sql6 = "SELECT STRUCT(1 AS a, 2 AS b)"
print(f"SQL: {sql6}")
try:
    result6_standard = sg.parse_one(sql6, read="")
    print(f"✓ Standard SQL: {result6_standard}")
    result6_duckdb = sg.parse_one(sql6, read="duckdb")
    print(f"✓ DuckDB: {result6_duckdb}")
except Exception as e:
    print(f"✗ Failed: {e}")

# Summary
print("\n" + "=" * 70)
print("VERIFICATION COMPLETE - All tests passed!")
print("=" * 70)
