import pytest
import sqlglot as sg
from sqlglot.errors import ParseError


def test_tuple_with_aliased_args_and_positional_cast():
    sql = "SELECT CAST(tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`).2 AS Nullable(String))"
    parsed = sg.parse_one(sql, read="clickhouse")
    out = parsed.sql(dialect="clickhouse")
    assert sg.parse_one(out, read="clickhouse")


def test_tuple_with_aliased_args():
    sql = "SELECT tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`)"
    parsed = sg.parse_one(sql, read="clickhouse")
    assert parsed


def test_tuple_with_positional_access():
    sql = "SELECT tuple(1, 2, 3).2"
    parsed = sg.parse_one(sql, read="clickhouse")
    out = parsed.sql(dialect="clickhouse")
    assert sg.parse_one(out, read="clickhouse")


def test_malformed_tuple_fails():
    bad = "SELECT tuple(1 AS `a` 2 AS `b`)"
    with pytest.raises(ParseError):
        sg.parse_one(bad, read="clickhouse")
