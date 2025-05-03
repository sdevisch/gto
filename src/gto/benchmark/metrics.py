"""
Performance Metrics Module

This module provides tools for collecting and analyzing performance metrics
for different data processing frameworks.
"""

from typing import Dict, Any, List
import time
import psutil
import pandas as pd

class PerformanceMetrics:
    """Collects and analyzes performance metrics."""
    
    def __init__(self):
        """Initialize the performance metrics collector."""
        self.metrics = {
            "execution_time": 0.0,
            "memory_usage": 0.0,
            "cpu_usage": 0.0,
            "io_operations": 0
        }
    
    def start_timer(self) -> None:
        """Start the performance timer."""
        self.start_time = time.time()
    
    def stop_timer(self) -> None:
        """Stop the performance timer and record metrics."""
        self.metrics["execution_time"] = time.time() - self.start_time
        self.metrics["memory_usage"] = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        self.metrics["cpu_usage"] = psutil.Process().cpu_percent()
    
    def get_metrics(self) -> Dict[str, float]:
        """
        Get the collected performance metrics.
        
        Returns:
            Dict[str, float]: Dictionary of performance metrics
        """
        return self.metrics 