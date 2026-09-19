"""
Audio Max Mobile - Entry Point for Kivy Version
Run this to test on desktop or build for mobile
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from audio_max.kivy_app import AudioMaxApp

if __name__ == '__main__':
    AudioMaxApp().run()
