#!/usr/bin/env python3
"""Run the test suite (cross-platform).

Usage: python run_tests.py
"""
import sys
import subprocess

def main():
    cmd = [sys.executable, "-m", "pytest", "-q"]
    proc = subprocess.run(cmd)
    sys.exit(proc.returncode)

if __name__ == "__main__":
    main()
