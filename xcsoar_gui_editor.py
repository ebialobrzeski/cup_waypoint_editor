"""
Legacy launcher for XCSoar CUP Editor.

This file is kept for backwards compatibility.
The main application has been refactored into a proper package structure in src/xcsoar_editor/.

To run the application:
    python -m xcsoar_editor
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from xcsoar_editor.__main__ import main

if __name__ == "__main__":
    main()
