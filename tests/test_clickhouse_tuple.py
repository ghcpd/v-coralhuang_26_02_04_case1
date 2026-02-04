import pytest
from sqlglot import parse_one
from sqlglot.errors import ParseError


def test_tuple_with_aliased_args_and_positional_cast():
    sql = "SELECT CAST(tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`).2 AS Nullable(String))"
    # Should parse under ClickHouse dialect
    expr = parse_one(sql, read="clickhouse")
    assert expr is not None

    # Round-trip: generated SQL should parse again
    sql2 = expr.sql(dialect="clickhouse")
    assert parse_one(sql2, read="clickhouse") is not None


def test_tuple_with_aliased_args():
    sql = "SELECT tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`)"
    expr = parse_one(sql, read="clickhouse")
    assert expr is not None


def test_tuple_positional_access():
    sql = "SELECT tuple(1, 2, 3).2"
    expr = parse_one(sql, read="clickhouse")
    assert expr is not None

    sql2 = expr.sql(dialect="clickhouse")
    assert parse_one(sql2, read="clickhouse") is not None


def test_malformed_tuple_syntax_fails():
    # Missing comma between arguments should fail
    bad_sql = "SELECT tuple(1 AS `a` 2 AS `b`).2"
    with pytest.raises(ParseError):
        parse_one(bad_sql, read="clickhouse")
