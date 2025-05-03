#!/usr/bin/env python3
"""
GTO Trust Demo Runner

This script provides a simple way to run GTO trust demonstrations.
Just run: python run_trust_demo.py

It will:
1. Set up GTO monitoring
2. Create example data
3. Show data changes
4. Generate documentation
"""

import pandas as pd
import os
from datetime import datetime

def main():
    print("=== GTO Data Trust Demo ===\n")
    
    # Import GTO (this sets up monitoring automatically)
    print("Setting up GTO...")
    import src.gto
    
    # Create example data directory
    os.makedirs("examples/data", exist_ok=True)
    
    # Create and monitor initial data
    print("\nCreating initial data...")
    df = pd.DataFrame({
        'id': range(1, 4),
        'value': [100, 200, 300]
    })
    df.to_csv("examples/data/sample.csv", index=False)
    print("\nReading initial data:")
    df = pd.read_csv("examples/data/sample.csv")
    print(df)
    
    # Modify data to demonstrate change detection
    print("\nModifying data...")
    df['value'] = df['value'] + 10
    df.to_csv("examples/data/sample.csv", index=False)
    print("\nReading modified data:")
    df = pd.read_csv("examples/data/sample.csv")
    print(df)
    
    print("\nDemo complete! Check docs/build/html/index.html for documentation.")

if __name__ == "__main__":
    main() 