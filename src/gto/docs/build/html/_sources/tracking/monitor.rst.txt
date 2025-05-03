Data Monitoring
=============

.. automodule:: monitor
   :members:
   :undoc-members:
   :show-inheritance:

The monitor module provides functionality for tracking data file operations:

* Automatic monitoring of pandas operations
* Change detection
* State tracking

Example Usage
------------

.. code-block:: python

   import pandas as pd
   
   # The monitor module automatically hooks into pandas
   df = pd.read_csv('data.csv')  # Changes are tracked automatically 