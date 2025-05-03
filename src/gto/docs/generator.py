"""
Documentation generation utilities.

This module handles generating and maintaining the system's documentation.
"""

import os
import subprocess
import sys
import webbrowser
from typing import List

def setup_sphinx() -> None:
    """Set up initial Sphinx documentation structure."""
    if not os.path.exists("docs"):
        subprocess.run([
            sys.executable, "-m", "sphinx.cmd.quickstart",
            "docs",
            "-q",  # Quiet mode
            "-p", "GTO Data Change Detection",
            "-a", "Data Governance Team",
            "--sep",  # Separate source and build
            "--ext-autodoc",  # Enable autodoc extension
            "--ext-napoleon",  # Enable Napoleon extension
            "--makefile",  # Generate Makefile
        ], check=True)

def generate_api_docs() -> None:
    """Generate API documentation using sphinx-apidoc."""
    subprocess.run([
        sys.executable, "-m", "sphinx.ext.apidoc",
        "-o", "docs/source",
        "gto",  # Source code directory
        "--separate",  # Create a file for each module
        "--module-first",  # Put module docs before submodule docs
    ], check=True)

def build_docs() -> None:
    """Build HTML documentation."""
    subprocess.run([
        sys.executable, "-m", "sphinx.cmd.build",
        "docs/source",
        "docs/build/html",
        "-b", "html",  # Build format
        "-E",  # Force rebuild
    ], check=True)

def generate_documentation() -> None:
    """Generate complete system documentation."""
    setup_sphinx()
    generate_api_docs()
    build_docs()
    
    # Open in browser
    index_path = os.path.abspath("docs/build/html/index.html")
    webbrowser.open_new_tab(f"file://{index_path}") 