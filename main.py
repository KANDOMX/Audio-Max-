"""
Audio Max - Main Entry Point
Modern, powerful music player application
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from audio_max.app import main

if __name__ == "__main__":
    main()
