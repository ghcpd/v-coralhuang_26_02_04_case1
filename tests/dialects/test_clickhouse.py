import pytest

from sqlglot import parse_one


class TestClickHouse:
    def test_tuple_with_aliased_args_and_positional_access(self):
        sql = "SELECT CAST(tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`).2 AS Nullable(String))"
        parsed = parse_one(sql, read="clickhouse")
        assert parsed is not None
        # Round-trip
        serialized = parsed.sql(dialect="clickhouse")
        reparsed = parse_one(serialized, read="clickhouse")
        assert reparsed is not None

    def test_tuple_with_aliased_args(self):
        sql = "SELECT tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`)"
        parsed = parse_one(sql, read="clickhouse")
        assert parsed is not None

    def test_tuple_with_positional_access(self):
        sql = "SELECT tuple(1, 2, 3).2"
        parsed = parse_one(sql, read="clickhouse")
        assert parsed is not None
        # Round-trip
        serialized = parsed.sql(dialect="clickhouse")
        reparsed = parse_one(serialized, read="clickhouse")
        assert reparsed is not None

    def test_malformed_tuple_syntax_fails(self):
        # Missing comma
        sql = "SELECT tuple(1 AS `a` 2 AS `b`)"
        with pytest.raises(Exception):
            parse_one(sql, read="clickhouse")