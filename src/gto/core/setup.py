"""
Dependency management for the GTO Data Change Detection System.

This module ensures all required packages are installed and properly configured.
"""

import subprocess
import sys
from typing import List

REQUIRED_PACKAGES = [
    "pandas",
    "gitpython",
    "sphinx",
    "sphinx-rtd-theme"
]

def install_dependencies() -> None:
    """Install all required packages using pip."""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install"] + REQUIRED_PACKAGES,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def verify_installation() -> List[str]:
    """Verify all required packages are installed correctly."""
    missing = []
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing.append(package)
    return missing 