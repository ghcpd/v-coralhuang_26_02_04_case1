import sqlglot as sg
import pytest


def test_tuple_with_aliased_args_and_positional_cast_roundtrip():
    sql = "SELECT CAST(tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`).2 AS Nullable(String))"
    parsed = sg.parse_one(sql, read="clickhouse")
    out = parsed.sql(dialect="clickhouse")
    assert out
    # Round-trip: serialized SQL must parse again
    reparsed = sg.parse_one(out, read="clickhouse")
    assert reparsed is not None


def test_tuple_with_aliased_args():
    sql = "SELECT tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`)"
    parsed = sg.parse_one(sql, read="clickhouse")
    assert parsed is not None


def test_tuple_with_positional_access():
    sql = "SELECT tuple(1, 2, 3).2"
    parsed = sg.parse_one(sql, read="clickhouse")
    out = parsed.sql(dialect="clickhouse")
    reparsed = sg.parse_one(out, read="clickhouse")
    assert reparsed is not None


def test_malformed_tuple_syntax_fails():
    # Missing comma between elements should fail
    bad_sql = "SELECT tuple(1 AS a 2 AS b).1"
    with pytest.raises(Exception):
        sg.parse_one(bad_sql, read="clickhouse")
