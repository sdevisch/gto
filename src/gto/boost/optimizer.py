"""
Code Optimizer Module

This module provides tools for optimizing code performance.
"""

from typing import Dict, Any, List
import ast
import inspect
import time
import psutil

class CodeOptimizer:
    """Optimizes code for better performance."""
    
    def __init__(self):
        """Initialize the code optimizer."""
        self.optimizations = {}
    
    def optimize_function(self, func: callable) -> callable:
        """
        Optimize a function for better performance.
        
        Args:
            func: Function to optimize
            
        Returns:
            callable: Optimized function
        """
        # Create a wrapper that tracks performance
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss
            
            result = func(*args, **kwargs)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss
            
            # Record performance metrics
            self.optimizations[func.__name__] = {
                "execution_time": end_time - start_time,
                "memory_usage": end_memory - start_memory,
                "timestamp": time.time()
            }
            
            return result
        
        return wrapper
    
    def get_optimizations(self) -> Dict[str, Any]:
        """
        Get recorded optimization metrics.
        
        Returns:
            Dict[str, Any]: Optimization metrics
        """
        return self.optimizations
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """
        Analyze code for potential optimizations.
        
        Args:
            code: Code to analyze
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        try:
            tree = ast.parse(code)
            return {
                "complexity": self._calculate_complexity(tree),
                "optimization_suggestions": self._find_optimizations(tree)
            }
        except SyntaxError:
            return {"error": "Invalid code syntax"}
    
    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate code complexity."""
        return len(list(ast.walk(tree)))
    
    def _find_optimizations(self, tree: ast.AST) -> List[str]:
        """Find potential code optimizations."""
        suggestions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                suggestions.append("Consider using list comprehension")
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == "range" and len(node.args) == 1:
                    suggestions.append("Consider using xrange for large ranges")
        
        return suggestions 