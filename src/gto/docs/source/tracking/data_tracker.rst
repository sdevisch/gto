Data Tracking
============

.. automodule:: data_tracker
   :members:
   :undoc-members:
   :show-inheritance:

The data_tracker module provides functionality for tracking and managing data states:

* State management
* Change detection
* History tracking

Example Usage
------------

.. code-block:: python

   from data_tracker import DataTracker
   
   # Create a tracker instance
   tracker = DataTracker()
   
   # Track a data file
   tracker.track_file('data.csv')
   
   # Get change history
   history = tracker.get_history('data.csv') 