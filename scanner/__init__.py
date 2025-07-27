"""
OWASP ZAP Scanner Integration

This module provides an interface to the OWASP ZAP API for performing security scans.
"""

__version__ = "0.1.0"

# Import the main scanner class to make it available when importing the package
from .engine import OWASPScanner  # noqa: F401

# This makes the package importable and allows for future expansion
