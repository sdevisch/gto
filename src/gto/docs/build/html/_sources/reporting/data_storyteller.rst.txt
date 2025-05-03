Data Storytelling
===============

.. automodule:: data_storyteller
   :members:
   :undoc-members:
   :show-inheritance:

The data_storyteller module provides functionality for creating comprehensive narratives about data changes:

* Change storytelling
* Trend analysis
* Impact assessment

Example Usage
------------

.. code-block:: python

   from data_storyteller import DataStoryteller
   
   # Create a storyteller instance
   storyteller = DataStoryteller()
   
   # Generate a story about data changes
   story = storyteller.tell_story('data.csv')
   
   # Print the story
   print(story) 