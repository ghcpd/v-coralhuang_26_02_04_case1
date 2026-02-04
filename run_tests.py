#!/usr/bin/env python
"""
One-click test runner for Windows (and other platforms).
Usage: python run_tests.py
"""
import sys
import pytest

if __name__ == "__main__":
    # Use -q for concise output
    errno = pytest.main(["-q", "tests"])
    sys.exit(errno)
