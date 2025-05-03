Data Narration
=============

.. automodule:: data_narrator
   :members:
   :undoc-members:
   :show-inheritance:

The data_narrator module provides functionality for generating human-readable reports about data changes:

* Change reporting
* Data summarization
* Narrative generation

Example Usage
------------

.. code-block:: python

   from data_narrator import DataNarrator
   
   # Create a narrator instance
   narrator = DataNarrator()
   
   # Generate a report about changes
   report = narrator.generate_report('data.csv')
   
   # Print the report
   print(report) 