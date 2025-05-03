"""
Documentation generation and management.

This module provides:
- Documentation generation
- API documentation
- Change history documentation
- Report generation
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import json

def generate_documentation(config: Dict[str, Any]) -> None:
    """
    Generate project documentation.
    
    Args:
        config: Configuration dictionary
    """
    docs_dir = Path(config["docs_dir"])
    source_dir = docs_dir / "source"
    build_dir = docs_dir / "build"
    
    # Create documentation directories
    source_dir.mkdir(parents=True, exist_ok=True)
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate main documentation files
    generate_index_rst(source_dir)
    generate_api_docs(source_dir)
    generate_change_history(source_dir, config)
    
    # Build documentation
    build_docs(docs_dir)

def generate_index_rst(source_dir: Path) -> None:
    """
    Generate main index.rst file.
    
    Args:
        source_dir: Path to source directory
    """
    content = """GTO Documentation
================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api
   changes
"""
    with open(source_dir / "index.rst", 'w') as f:
        f.write(content)

def generate_api_docs(source_dir: Path) -> None:
    """
    Generate API documentation.
    
    Args:
        source_dir: Path to source directory
    """
    content = """API Documentation
================

.. automodule:: gto.core
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: gto.translate
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: gto.benchmark
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: gto.boost
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: gto.track
   :members:
   :undoc-members:
   :show-inheritance:
"""
    with open(source_dir / "api.rst", 'w') as f:
        f.write(content)

def generate_change_history(source_dir: Path, config: Dict[str, Any]) -> None:
    """
    Generate change history documentation.
    
    Args:
        source_dir: Path to source directory
        config: Configuration dictionary
    """
    log_file = Path(config["log_dir"]) / "changes.log"
    if not log_file.exists():
        return
        
    content = """Change History
=============

.. csv-table::
   :header: "Timestamp", "File", "Change Type"
   :widths: 20, 50, 30
"""
    with open(log_file, 'r') as f:
        for line in f:
            change = json.loads(line)
            content += f"   {change['timestamp']}, {change['file_path']}, Modified\n"
            
    with open(source_dir / "changes.rst", 'w') as f:
        f.write(content)

def build_docs(docs_dir: Path) -> None:
    """
    Build documentation using Sphinx.
    
    Args:
        docs_dir: Path to documentation directory
    """
    os.chdir(docs_dir)
    os.system("make html") 