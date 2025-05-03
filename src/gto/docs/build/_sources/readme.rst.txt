GTO Data Change Detection System
============================

A robust system for tracking and managing changes in data files, designed for data scientists and analysts who need to maintain data integrity and reproducibility.

Installation
------------

.. code-block:: bash

   pip install pandas gitpython sphinx sphinx-rtd-theme

Features
--------

Data Change Detection
~~~~~~~~~~~~~~~~~~~
The system automatically monitors data file operations and detects changes by:

* Creating fingerprints of data states
* Comparing current and previous states
* Generating detailed change reports

History Tracking
~~~~~~~~~~~~~~
All data changes are tracked and stored:

* Local history files for individual use
* Git-based distributed tracking for teams
* Timestamped records of all changes

Documentation Generation
~~~~~~~~~~~~~~~~~~~~~
Comprehensive documentation is automatically generated:

* API reference
* Usage examples
* Configuration guides
* Change history

Usage Examples
------------

Basic Usage
~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   
   # Read data - changes are automatically tracked
   df = pd.read_csv('data.csv')
   
   # Modify and save data
   df['new_column'] = df['value'] * 2
   df.to_csv('data.csv', index=False)
   
   # Read again - changes will be reported
   df = pd.read_csv('data.csv')

Configuration
~~~~~~~~~~~~

.. code-block:: python

   # Configure Git-based tracking
   config = {
       "use_git": True,
       "git_repo_url": "https://github.com/your_org/data_tracking.git"
   }
   
   with open('config.json', 'w') as f:
       json.dump(config, f, indent=2)

Contributing
-----------
Contributions are welcome! Please feel free to submit a Pull Request.

License
-------
This project is licensed under the MIT License. 