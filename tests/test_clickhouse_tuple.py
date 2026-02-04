import pytest

import sqlglot as sg
from sqlglot.errors import ParseError


def test_tuple_with_aliased_args_and_positional_in_cast():
    sql = "SELECT CAST(tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`).2 AS Nullable(String))"

    parsed = sg.parse_one(sql, read="clickhouse")
    assert parsed is not None

    rendered = parsed.sql(dialect="clickhouse")
    # Ensure the rendered SQL can be parsed back under clickhouse
    parsed_round = sg.parse_one(rendered, read="clickhouse")
    assert parsed_round is not None


def test_tuple_with_aliased_args_without_positional():
    sql = "SELECT tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`)"

    parsed = sg.parse_one(sql, read="clickhouse")
    assert parsed is not None

    rendered = parsed.sql(dialect="clickhouse")
    # Ensure it round-trips
    parsed_round = sg.parse_one(rendered, read="clickhouse")
    assert parsed_round is not None


def test_tuple_without_aliased_args_with_positional():
    sql = "SELECT tuple(1, 2, 3).2"

    parsed = sg.parse_one(sql, read="clickhouse")
    assert parsed is not None

    rendered = parsed.sql(dialect="clickhouse")
    parsed_round = sg.parse_one(rendered, read="clickhouse")
    assert parsed_round is not None


def test_malformed_tuple_syntax_fails():
    # Missing comma between elements should fail to parse
    sql = "SELECT tuple(1 AS `a` 2 AS `b`)"
    with pytest.raises(ParseError):
        sg.parse_one(sql, read="clickhouse")
