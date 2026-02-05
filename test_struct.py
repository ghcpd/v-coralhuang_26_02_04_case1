#!/usr/bin/env python3
"""Test to understand how STRUCT parsing works"""

import sqlglot as sg

# Test 1: Basic struct in standard SQL
print("Test 1: STRUCT in standard SQL")
try:
    result = sg.parse_one("SELECT STRUCT(1 AS a, 2 AS b)", read="")
    print(f"✓ SUCCESS: {result}")
except Exception as e:
    print(f"✗ ERROR: {e}")

# Test 2: TUPLE in ClickHouse without aliases
print("\nTest 2: TUPLE without aliases")
try:
    result = sg.parse_one("SELECT tuple(1, 2, 3)", read="clickhouse")
    print(f"✓ SUCCESS: {result}")
except Exception as e:
    print(f"✗ ERROR: {e}")

# Test 3: TUPLE in ClickHouse with aliases
print("\nTest 3: TUPLE with aliases")
try:
    result = sg.parse_one("SELECT tuple(1 AS a, 2 AS b)", read="clickhouse")
    print(f"✓ SUCCESS: {result}")
except Exception as e:
    print(f"✗ ERROR: {e}")

# Test 4: STRUCT in DuckDB with aliases
print("\nTest 4: STRUCT with aliases in DuckDB")
try:
    result = sg.parse_one("SELECT {'a': 1, 'b': 2}", read="duckdb")
    print(f"✓ SUCCESS: {result}")
except Exception as e:
    print(f"✗ ERROR: {e}")
