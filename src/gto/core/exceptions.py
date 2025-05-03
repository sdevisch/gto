"""
Custom exceptions for the GTO package.

This module defines all custom exceptions used throughout the package
to provide more specific error handling and better error messages.
"""

class GTOError(Exception):
    """Base exception for all GTO-specific errors."""
    pass

class ConfigError(GTOError):
    """Raised when there are issues with configuration."""
    pass

class DataReadError(GTOError):
    """Raised when there are issues reading data files."""
    pass

class ValidationError(GTOError):
    """Raised when data validation fails."""
    pass

class TrackingError(GTOError):
    """Raised when there are issues tracking data changes."""
    pass

class ReportingError(GTOError):
    """Raised when there are issues generating reports."""
    pass 