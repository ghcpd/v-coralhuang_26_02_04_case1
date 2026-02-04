"""
Test suite for ClickHouse tuple() parsing with aliased elements.

This module tests the fix for the parsing issue where tuple() expressions
with aliased elements (e.g., "1 AS `a`") were not being parsed correctly
in ClickHouse SQL, particularly when combined with positional access.
"""

import pytest
import sqlglot as sg
from sqlglot import exp, parse_one
from sqlglot.dialects.clickhouse import ClickHouse


class TestClickHouseTupleWithAliases:
    """Tests for tuple() parsing with aliased arguments in ClickHouse."""

    def test_tuple_with_aliased_args_and_positional_access_in_cast(self):
        """
        Test tuple with aliased args and positional access inside CAST.
        
        This is the main reproduction case from the bug report.
        Valid ClickHouse SQL: SELECT CAST(tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`).2 AS Nullable(String))
        """
        sql = "SELECT CAST(tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`).2 AS Nullable(String))"
        
        # Should parse without error
        result = parse_one(sql, read="clickhouse")
        
        # Verify the structure is correct
        assert isinstance(result, exp.Select)
        cast_expr = result.expressions[0]
        assert isinstance(cast_expr, exp.Cast)
        
        # The cast argument should be a Dot (positional access) of a struct
        dot_expr = cast_expr.this
        assert isinstance(dot_expr, exp.Dot)
        
        # The struct should have 3 elements with aliases
        struct = dot_expr.this
        assert isinstance(struct, exp.Struct)
        assert len(struct.expressions) == 3
        
        # Check that each element is an alias expression
        for i, expr in enumerate(struct.expressions):
            assert isinstance(expr, exp.Alias)
        
        # Verify alias names
        assert struct.expressions[0].alias == "a"
        assert struct.expressions[1].alias == "b"
        assert struct.expressions[2].alias == "c"

    def test_tuple_with_aliased_args_without_positional_access(self):
        """Test tuple with aliased args but without positional access."""
        sql = "SELECT tuple(1 AS `a`, 2 AS `b`, 3.0 AS `c`)"
        
        result = parse_one(sql, read="clickhouse")
        
        assert isinstance(result, exp.Select)
        tuple_expr = result.expressions[0]
        assert isinstance(tuple_expr, exp.Struct)
        assert len(tuple_expr.expressions) == 3
        
        # Verify aliases exist
        assert all(isinstance(expr, exp.Alias) for expr in tuple_expr.expressions)

    def test_tuple_without_aliased_args_but_with_positional_access_regression(self):
        """Test tuple without aliased args with positional access (regression test)."""
        sql = "SELECT tuple(1, 2, 3).2"
        
        result = parse_one(sql, read="clickhouse")
        
        assert isinstance(result, exp.Select)
        dot_expr = result.expressions[0]
        assert isinstance(dot_expr, exp.Dot)
        
        struct = dot_expr.this
        assert isinstance(struct, exp.Struct)
        assert len(struct.expressions) == 3

    def test_tuple_basic_without_aliases(self):
        """Test basic tuple without aliases."""
        sql = "SELECT tuple(1, 2, 3)"
        
        result = parse_one(sql, read="clickhouse")
        
        assert isinstance(result, exp.Select)
        struct = result.expressions[0]
        assert isinstance(struct, exp.Struct)
        assert len(struct.expressions) == 3

    def test_tuple_single_element_with_alias(self):
        """Test tuple with a single aliased element."""
        sql = "SELECT tuple(1 AS x)"
        
        result = parse_one(sql, read="clickhouse")
        
        assert isinstance(result, exp.Select)
        struct = result.expressions[0]
        assert isinstance(struct, exp.Struct)
        assert len(struct.expressions) == 1
        assert isinstance(struct.expressions[0], exp.Alias)
        assert struct.expressions[0].alias == "x"

    def test_tuple_mixed_aliased_and_non_aliased_args(self):
        """Test tuple with mixed aliased and non-aliased arguments."""
        sql = "SELECT tuple(1 AS a, 2, 3 AS c)"
        
        result = parse_one(sql, read="clickhouse")
        
        assert isinstance(result, exp.Select)
        struct = result.expressions[0]
        assert isinstance(struct, exp.Struct)
        assert len(struct.expressions) == 3
        
        # Check first is aliased
        assert isinstance(struct.expressions[0], exp.Alias)
        assert struct.expressions[0].alias == "a"
        
        # Check second is not aliased (should be a literal)
        assert not isinstance(struct.expressions[1], exp.Alias)
        
        # Check third is aliased
        assert isinstance(struct.expressions[2], exp.Alias)
        assert struct.expressions[2].alias == "c"

    def test_roundtrip_tuple_with_aliases_and_positional_access(self):
        """Test parse -> serialize -> parse round-trip for tuple with aliases and positional access."""
        original_sql = "SELECT tuple(1 AS a, 2 AS b, 3 AS c).1"
        
        parsed_1 = parse_one(original_sql, read="clickhouse")
        serialized = parsed_1.sql(dialect="clickhouse")
        parsed_2 = parse_one(serialized, read="clickhouse")
        
        # Both should parse successfully
        assert isinstance(parsed_1, exp.Select)
        assert isinstance(parsed_2, exp.Select)
        
        # Serialize again to ensure stability
        serialized_2 = parsed_2.sql(dialect="clickhouse")
        assert serialized == serialized_2

    def test_roundtrip_tuple_without_aliases_and_positional_access(self):
        """Test parse -> serialize -> parse round-trip for tuple without aliases but with positional access."""
        original_sql = "SELECT tuple(1, 2, 3).2"
        
        parsed_1 = parse_one(original_sql, read="clickhouse")
        serialized = parsed_1.sql(dialect="clickhouse")
        parsed_2 = parse_one(serialized, read="clickhouse")
        
        # Both should parse successfully
        assert isinstance(parsed_1, exp.Select)
        assert isinstance(parsed_2, exp.Select)
        
        # Serialize again to ensure stability
        serialized_2 = parsed_2.sql(dialect="clickhouse")
        assert serialized == serialized_2

    def test_nested_tuples_with_aliases(self):
        """Test nested tuples with aliases."""
        sql = "SELECT tuple(tuple(1 AS x, 2 AS y) AS inner, 3 AS z)"
        
        result = parse_one(sql, read="clickhouse")
        
        assert isinstance(result, exp.Select)
        outer_struct = result.expressions[0]
        assert isinstance(outer_struct, exp.Struct)
        assert len(outer_struct.expressions) == 2

    def test_tuple_in_select_with_cast_and_nullable_type(self):
        """Test tuple in a CAST expression with ClickHouse-specific Nullable type."""
        sql = "SELECT CAST(tuple(1 AS x, 2 AS y) AS Nullable(String))"
        
        result = parse_one(sql, read="clickhouse")
        
        assert isinstance(result, exp.Select)
        cast_expr = result.expressions[0]
        assert isinstance(cast_expr, exp.Cast)
        
        struct = cast_expr.this
        assert isinstance(struct, exp.Struct)

    def test_tuple_with_string_literals_and_aliases(self):
        """Test tuple with string literals and aliases."""
        sql = "SELECT tuple('a' AS str1, 'b' AS str2)"
        
        result = parse_one(sql, read="clickhouse")
        
        assert isinstance(result, exp.Select)
        struct = result.expressions[0]
        assert isinstance(struct, exp.Struct)
        assert len(struct.expressions) == 2

    def test_tuple_in_where_clause_with_positional_access(self):
        """Test tuple usage in WHERE clause with positional access."""
        sql = "SELECT * FROM t WHERE x = tuple(1 AS a, 2 AS b).1"
        
        result = parse_one(sql, read="clickhouse")
        
        assert isinstance(result, exp.Select)
        # The WHERE clause should be parseable
        assert result.args.get("where") is not None

    def test_malformed_tuple_missing_comma_fails(self):
        """Test that malformed tuple syntax (missing comma) still fails."""
        sql = "SELECT tuple(1 AS a 2 AS b)"  # Missing comma between arguments
        
        with pytest.raises(Exception):  # Should raise a ParseError
            parse_one(sql, read="clickhouse")

    def test_malformed_tuple_invalid_alias_syntax_fails(self):
        """Test that invalid alias syntax in tuple with keyword fails."""
        # The parser is fairly lenient with missing parts, so let's test with something
        # that actually causes a parse error
        sql = "SELECT tuple(AS 1, 2)"  # AS without preceding expression
        
        with pytest.raises(Exception):  # Should raise a ParseError
            parse_one(sql, read="clickhouse")

    def test_tuple_with_complex_expressions_and_aliases(self):
        """Test tuple with complex expressions and aliases."""
        sql = "SELECT tuple(1 + 1 AS a, x * y AS b) FROM t"
        
        result = parse_one(sql, read="clickhouse")
        
        assert isinstance(result, exp.Select)
        struct = result.expressions[0]
        assert isinstance(struct, exp.Struct)
        assert len(struct.expressions) == 2
        
        # Both should be aliases
        assert all(isinstance(expr, exp.Alias) for expr in struct.expressions)

    def test_tuple_with_backtick_quoted_aliases(self):
        """Test tuple with backtick-quoted aliases (ClickHouse identifier quoting)."""
        sql = "SELECT tuple(1 AS `col1`, 2 AS `col2 with spaces`)"
        
        result = parse_one(sql, read="clickhouse")
        
        assert isinstance(result, exp.Select)
        struct = result.expressions[0]
        assert isinstance(struct, exp.Struct)
        assert len(struct.expressions) == 2
        assert struct.expressions[0].alias == "col1"
        assert struct.expressions[1].alias == "col2 with spaces"

    def test_other_dialects_not_affected(self):
        """Test that other dialects are not affected by the ClickHouse tuple fix."""
        # Standard SQL with STRUCT should still work
        sql = "SELECT STRUCT(1 AS a, 2 AS b)"
        result = parse_one(sql, read="")
        assert isinstance(result.expressions[0], exp.Struct)
        
        # DuckDB should still work
        sql = "SELECT STRUCT_PACK(a := 1, b := 2)"
        # This might not parse in the default dialect, but we can test basic STRUCT parsing
        sql = "SELECT STRUCT(1 AS a, 2 AS b)"
        result = parse_one(sql, read="duckdb")
        assert isinstance(result.expressions[0], exp.Struct)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
