#!/usr/bin/env python3
"""Check the actual expression types"""

import sqlglot as sg
from sqlglot import exp

# Test with positional access
sql = "SELECT tuple(1 AS a, 2 AS b, 3 AS c).2"
result = sg.parse_one(sql, read="clickhouse")
print(f"SQL: {sql}")
print(f"Result: {result}")
print(f"Expression type: {type(result.expressions[0])}")
print(f"Expression: {result.expressions[0]}")
print(f"Expression repr: {repr(result.expressions[0])}")
print()

# Let's explore the AST
expr = result.expressions[0]
print(f"Expr attributes: {dir(expr)}")
print()

if isinstance(expr, exp.Bracket):
    print(f"Is Bracket: True")
    print(f"  this: {expr.this}")
    print(f"  expression: {expr.expression}")
elif isinstance(expr, exp.Index):
    print(f"Is Index: True")
    print(f"  this: {expr.this}")
    print(f"  expression: {expr.expression}")
else:
    print(f"Type: {type(expr)}")
    for key, val in expr.args.items():
        print(f"  {key}: {val}")
