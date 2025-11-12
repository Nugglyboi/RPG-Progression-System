"""Deprecated shim for the old `parser` module.

This module now delegates to `csvparser`. Existing imports of
``import parser`` will continue to work but new code should import
``csvparser`` directly.
"""

from csvparser import CSVRow, read_csv  # re-export for compatibility

__all__ = ["CSVRow", "read_csv"]
