"""
Feature Engineering Module

This module provides tools for feature engineering and data transformation.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np

class FeatureEngineer:
    """Engineers features from raw data."""
    
    def __init__(self):
        """Initialize the feature engineer."""
        self.features = {}
    
    def create_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Create new features from the input data.
        
        Args:
            data: Input DataFrame
            
        Returns:
            pd.DataFrame: DataFrame with new features
        """
        df = data.copy()
        
        # Add basic statistical features
        for col in df.select_dtypes(include=[np.number]).columns:
            df[f'{col}_mean'] = df[col].mean()
            df[f'{col}_std'] = df[col].std()
            df[f'{col}_min'] = df[col].min()
            df[f'{col}_max'] = df[col].max()
        
        return df
    
    def transform_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform features using various techniques.
        
        Args:
            data: Input DataFrame
            
        Returns:
            pd.DataFrame: Transformed DataFrame
        """
        df = data.copy()
        
        # Apply transformations
        for col in df.select_dtypes(include=[np.number]).columns:
            df[f'{col}_log'] = np.log1p(df[col])
            df[f'{col}_sqrt'] = np.sqrt(df[col])
            df[f'{col}_square'] = df[col] ** 2
        
        return df 