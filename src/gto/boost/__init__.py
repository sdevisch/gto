"""
GTO Boost Module

Provides tools for automatic code optimization and enhancement:
- Code analysis and transformation
- Performance optimization
- Resource optimization
- Automatic framework selection
- Runtime code replacement

Key Features:
- Transparent code optimization:
  * Analyzes data characteristics
  * Monitors performance metrics
  * Identifies optimization opportunities
  * Automatically selects best framework
  * Replaces code at runtime
- Framework-specific optimizations:
  * Pandas optimizations
  * PySpark optimizations
  * Dask optimizations
  * Ray optimizations
  * NumPy optimizations
- Resource management:
  * Memory optimization
  * CPU utilization
  * I/O optimization
  * Network optimization
- Automatic scaling:
  * Horizontal scaling
  * Vertical scaling
  * Load balancing
  * Resource allocation
"""

from .code import *
from .quality import *
from .features import *
from .optimizer import *

__all__ = ['code', 'quality', 'features', 'optimizer']
