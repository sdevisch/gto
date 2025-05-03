"""
Data Story Tracking System

This module tells the story of your data's journey by:
1. Recording each chapter of your data's life
2. Capturing the essence of your data at each moment
3. Maintaining a chronicle of changes
4. Sharing the story with your team

The goal is to make data changes as readable as a story,
helping everyone understand how data evolves over time.
"""

import hashlib
import json
import os
from datetime import datetime
import pandas as pd
from git import Repo
from typing import Dict, Any, List

# The books where we write our data stories
CHRONICLE_PATH = "gto_reproducibility_state_log.json"
SHARED_STORIES_PATH = "simulated_shared_repo.json"

def begin_new_story():
    """
    Start a new data story by creating the initial settings.
    
    Like any good story, we need to decide if it's a solo adventure
    or a collaborative tale.
    """
    CONFIG_FILE = "config.json"
    
    if not os.path.exists(CONFIG_FILE):
        story_settings = {
            "is_collaborative": False,  # Solo adventure by default
            "collaboration_hub": "https://github.com/your_org/shared_stories.git"
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(story_settings, f, indent=2)
    
    with open(CONFIG_FILE) as f:
        return json.load(f)

def read_previous_chapters():
    """
    Recall what happened in previous chapters of our data story.
    Returns an empty book if this is where the story begins.
    """
    if os.path.exists(CHRONICLE_PATH):
        with open(CHRONICLE_PATH, "r") as f:
            return json.load(f)
    return {}

def write_new_chapter(chronicle):
    """
    Add a new chapter to our data's story.
    """
    with open(CHRONICLE_PATH, "w") as f:
        json.dump(chronicle, f, indent=2)

def capture_data_essence(df):
    """
    Distill the essence of our data into a memorable summary.
    
    Like a book summary, we capture:
    - How many characters (rows) are in our story
    - The key themes (numeric patterns) that emerge
    """
    return {
        "characters": len(df),
        "themes": df.select_dtypes('number').sum().to_dict()
    }

def create_memory_imprint(essence):
    """
    Create an unforgettable impression of this moment in data's story.
    
    Like a book's ISBN, this unique identifier helps us:
    - Remember exactly how the data looked
    - Spot when the story changes
    - Keep track of different editions
    """
    serialized = json.dumps(essence, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()

def share_story(filepath, memory, settings):
    """
    Share our data's story with other readers.
    
    In collaborative mode: The story goes to a shared library
    In solo mode: We keep the story in our personal collection
    """
    if settings["is_collaborative"]:
        _share_in_library(filepath, memory, settings)
    else:
        _keep_personal_copy(filepath, memory)

def _share_in_library(filepath, memory, settings):
    """Share our story in the collaborative library."""
    LIBRARY_PATH = os.path.expanduser("~/.gto_shared_stories")
    
    # Set up or access the library
    if not os.path.exists(LIBRARY_PATH):
        Repo.clone_from(settings["collaboration_hub"], LIBRARY_PATH)
    library = Repo(LIBRARY_PATH)
    
    # Update the collection
    stories_catalog = os.path.join(LIBRARY_PATH, "shared_stories.json")
    collection = {}
    if os.path.exists(stories_catalog):
        with open(stories_catalog) as f:
            collection = json.load(f)
    
    # Add this edition to the collection
    collection[filepath] = {
        "memory": memory,
        "publication_date": datetime.now().isoformat()
    }
    
    # Catalog the new edition
    with open(stories_catalog, "w") as f:
        json.dump(collection, f, indent=2)
    
    library.index.add(["shared_stories.json"])
    library.index.commit(f"Add new chapter for {filepath}")
    library.remote().push()

def _keep_personal_copy(filepath, memory):
    """Keep this story in our personal collection."""
    if not os.path.exists(SHARED_STORIES_PATH):
        with open(SHARED_STORIES_PATH, "w") as f:
            json.dump({}, f)
    
    with open(SHARED_STORIES_PATH, "r+") as f:
        try:
            collection = json.load(f)
        except json.JSONDecodeError:
            collection = {}
        
        collection[filepath] = {
            "memory": memory,
            "publication_date": datetime.now().isoformat()
        }
        
        f.seek(0)
        json.dump(collection, f, indent=2)
        f.truncate()

def tell_story_of_changes(filepath, previous_edition, new_essence):
    """
    Narrate how our data's story has evolved.
    
    Tells the tale of:
    - Which part of our data changed
    - How the numbers shifted
    - When this new chapter began
    """
    print(f"\n📚 [Data Story Update] A new chapter unfolds in '{filepath}':")
    previous_essence = previous_edition["essence"]
    
    for key in previous_essence:
        if previous_essence[key] != new_essence[key]:
            print(f"📖 {key}: {previous_essence[key]} ➡️ {new_essence[key]}")
    
    print(f"⏰ Chapter written at: {datetime.now().isoformat()}\n")

class DataStoryteller:
    """Generates narrative reports about data changes."""
    
    def __init__(self):
        """Initialize the data storyteller."""
        self.templates = {
            "change": "The data in {file} was {change_type} on {timestamp}.",
            "insight": "Key insight: {insight}",
            "summary": "Summary: {summary}"
        }
    
    def generate_report(self, changes: List[Dict[str, Any]]) -> str:
        """
        Generate a narrative report from changes.
        
        Args:
            changes: List of changes to report
            
        Returns:
            str: Narrative report
        """
        report = []
        for change in changes:
            report.append(self._format_change(change))
        
        if report:
            return "\n".join(report)
        return "No changes detected."
    
    def _format_change(self, change: Dict[str, Any]) -> str:
        """
        Format a single change into narrative.
        
        Args:
            change: Change details
            
        Returns:
            str: Formatted narrative
        """
        return self.templates["change"].format(
            file=change.get("file", "unknown"),
            change_type=change.get("type", "modified"),
            timestamp=change.get("timestamp", datetime.now().isoformat())
        ) 