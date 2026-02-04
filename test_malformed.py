#!/usr/bin/env python3
"""Test malformed tuple"""

import sqlglot as sg

sql = "SELECT tuple(1 AS, 2)"
try:
    result = sg.parse_one(sql, read="clickhouse")
    print(f"Parsed: {result}")
except Exception as e:
    print(f"Error: {e}")
