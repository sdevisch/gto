"""
Performance Analyzer Module

This module provides tools for analyzing performance metrics and comparing
different implementations.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from datetime import datetime

class PerformanceAnalyzer:
    """Analyzes and compares performance metrics."""
    
    def __init__(self):
        """Initialize the performance analyzer."""
        self.metrics = {}
    
    def add_metrics(self, name: str, metrics: Dict[str, Any]) -> None:
        """
        Add performance metrics for analysis.
        
        Args:
            name: Name of the implementation
            metrics: Dictionary of performance metrics
        """
        if name not in self.metrics:
            self.metrics[name] = []
        
        self.metrics[name].append({
            "timestamp": datetime.now().isoformat(),
            **metrics
        })
    
    def compare_implementations(self) -> Dict[str, Any]:
        """
        Compare performance across different implementations.
        
        Returns:
            Dict[str, Any]: Comparison results
        """
        if not self.metrics:
            return {"error": "No metrics available"}
        
        comparison = {
            "implementations": list(self.metrics.keys()),
            "metrics": {}
        }
        
        # Calculate average metrics for each implementation
        for impl, measurements in self.metrics.items():
            df = pd.DataFrame(measurements)
            comparison["metrics"][impl] = {
                "execution_time": {
                    "mean": df["execution_time"].mean(),
                    "std": df["execution_time"].std(),
                    "min": df["execution_time"].min(),
                    "max": df["execution_time"].max()
                },
                "memory_usage": {
                    "mean": df["memory_usage"].mean(),
                    "std": df["memory_usage"].std(),
                    "min": df["memory_usage"].min(),
                    "max": df["memory_usage"].max()
                }
            }
        
        # Calculate relative performance
        best_time = min(
            metrics["execution_time"]["mean"]
            for metrics in comparison["metrics"].values()
        )
        best_memory = min(
            metrics["memory_usage"]["mean"]
            for metrics in comparison["metrics"].values()
        )
        
        for impl, metrics in comparison["metrics"].items():
            metrics["relative_performance"] = {
                "execution_time": best_time / metrics["execution_time"]["mean"],
                "memory_usage": best_memory / metrics["memory_usage"]["mean"]
            }
        
        return comparison
    
    def get_recommendations(self) -> Dict[str, Any]:
        """
        Get optimization recommendations based on analysis.
        
        Returns:
            Dict[str, Any]: Recommendations
        """
        comparison = self.compare_implementations()
        if "error" in comparison:
            return comparison
        
        recommendations = {
            "best_performing": None,
            "improvements": {}
        }
        
        # Find best performing implementation
        best_score = 0
        for impl, metrics in comparison["metrics"].items():
            score = (
                metrics["relative_performance"]["execution_time"] +
                metrics["relative_performance"]["memory_usage"]
            ) / 2
            
            if score > best_score:
                best_score = score
                recommendations["best_performing"] = impl
        
        # Generate improvement suggestions
        for impl, metrics in comparison["metrics"].items():
            if impl == recommendations["best_performing"]:
                continue
            
            improvements = []
            if metrics["relative_performance"]["execution_time"] < 1:
                improvements.append("Consider optimizing execution time")
            if metrics["relative_performance"]["memory_usage"] < 1:
                improvements.append("Consider optimizing memory usage")
            
            if improvements:
                recommendations["improvements"][impl] = improvements
        
        return recommendations 