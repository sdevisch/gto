"""
Resource Tracker Module

This module provides tools for tracking resource utilization during benchmarking.
"""

from typing import Dict, Any, List
import psutil
import time
from datetime import datetime

class ResourceTracker:
    """Tracks system resource utilization."""
    
    def __init__(self):
        """Initialize the resource tracker."""
        self.start_time = None
        self.end_time = None
        self.metrics = {
            "cpu_percent": [],
            "memory_percent": [],
            "disk_io": [],
            "network_io": []
        }
    
    def start(self) -> None:
        """Start tracking resources."""
        self.start_time = time.time()
        self._record_metrics()
    
    def stop(self) -> Dict[str, Any]:
        """
        Stop tracking resources and return summary.
        
        Returns:
            Dict[str, Any]: Resource utilization summary
        """
        self.end_time = time.time()
        self._record_metrics()
        
        return {
            "duration": self.end_time - self.start_time,
            "cpu_avg": sum(self.metrics["cpu_percent"]) / len(self.metrics["cpu_percent"]),
            "memory_avg": sum(self.metrics["memory_percent"]) / len(self.metrics["memory_percent"]),
            "disk_io_total": sum(io.read_bytes + io.write_bytes for io in self.metrics["disk_io"]),
            "network_io_total": sum(io.bytes_sent + io.bytes_recv for io in self.metrics["network_io"])
        }
    
    def _record_metrics(self) -> None:
        """Record current resource metrics."""
        process = psutil.Process()
        
        self.metrics["cpu_percent"].append(process.cpu_percent())
        self.metrics["memory_percent"].append(process.memory_percent())
        self.metrics["disk_io"].append(process.io_counters())
        self.metrics["network_io"].append(psutil.net_io_counters()) 