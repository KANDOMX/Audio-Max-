"""
Utility functions for Audio Max
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import timedelta


class TimeFormatter:
    """Format time in various ways for display"""
    
    @staticmethod
    def seconds_to_time(seconds: float) -> str:
        """Convert seconds to MM:SS format"""
        if seconds < 0:
            seconds = 0
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def milliseconds_to_time(ms: float) -> str:
        """Convert milliseconds to MM:SS format"""
        return TimeFormatter.seconds_to_time(ms / 1000)
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration with hours if needed"""
        if seconds < 3600:
            return TimeFormatter.seconds_to_time(seconds)
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"


class FileScanner:
    """Scan directories for audio files"""
    
    AUDIO_EXTENSIONS = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma']
    
    @staticmethod
    def is_audio_file(path: str) -> bool:
        """Check if a file is an audio file"""
        return Path(path).suffix.lower() in FileScanner.AUDIO_EXTENSIONS
    
    @staticmethod
    def scan_directory(directory: str) -> List[str]:
        """Scan a directory for audio files recursively"""
        audio_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if FileScanner.is_audio_file(file):
                    audio_files.append(os.path.join(root, file))
        return audio_files
    
    @staticmethod
    def get_file_info(path: str) -> Dict:
        """Get basic file information"""
        try:
            stat = os.stat(path)
            return {
                'path': path,
                'name': os.path.basename(path),
                'size': stat.st_size,
                'modified': stat.st_mtime
            }
        except OSError:
            return {'path': path, 'name': os.path.basename(path)}


class ThemeManager:
    """Manage application themes"""
    
    DARK_THEME = {
        'bg_primary': '#1a1a2e',
        'bg_secondary': '#16213e',
        'bg_tertiary': '#0f3460',
        'text_primary': '#eaeaea',
        'text_secondary': '#b8b8b8',
        'accent': '#e94560',
        'accent_hover': '#ff6b81',
        'border': '#2a2a4a',
        'success': '#4ecca3',
        'warning': '#ffc107',
        'error': '#ff4757'
    }
    
    LIGHT_THEME = {
        'bg_primary': '#f5f6fa',
        'bg_secondary': '#ffffff',
        'bg_tertiary': '#e8e8e8',
        'text_primary': '#2d3436',
        'text_secondary': '#636e72',
        'accent': '#e94560',
        'accent_hover': '#ff6b81',
        'border': '#dfe6e9',
        'success': '#4ecca3',
        'warning': '#ffc107',
        'error': '#ff4757'
    }
    
    @staticmethod
    def get_theme(is_dark: bool = True) -> Dict:
        """Get theme colors"""
        return ThemeManager.DARK_THEME if is_dark else ThemeManager.LIGHT_THEME
    
    @staticmethod
    def get_stylesheet(is_dark: bool = True) -> str:
        """Generate stylesheet for the theme"""
        theme = ThemeManager.get_theme(is_dark)
        return f"""
        QMainWindow {{
            background-color: {theme['bg_primary']};
        }}
        QWidget {{
            background-color: {theme['bg_primary']};
            color: {theme['text_primary']};
        }}
        QPushButton {{
            background-color: {theme['accent']};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {theme['accent_hover']};
        }}
        QPushButton:pressed {{
            background-color: {theme['bg_tertiary']};
        }}
        QSlider::groove:horizontal {{
            height: 4px;
            background: {theme['border']};
            border-radius: 2px;
        }}
        QSlider::handle:horizontal {{
            width: 16px;
            height: 16px;
            border-radius: 8px;
            background: {theme['accent']};
        }}
        QListWidget {{
            background-color: {theme['bg_secondary']};
            border: 1px solid {theme['border']};
            border-radius: 4px;
        }}
        QListWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {theme['border']};
        }}
        QListWidget::item:selected {{
            background-color: {theme['accent']};
            color: white;
        }}
        QLabel {{
            color: {theme['text_primary']};
        }}
        QLineEdit {{
            background-color: {theme['bg_secondary']};
            color: {theme['text_primary']};
            border: 1px solid {theme['border']};
            border-radius: 4px;
            padding: 6px;
        }}
        QProgressBar {{
            text-align: center;
            border: 1px solid {theme['border']};
            border-radius: 4px;
            background-color: {theme['bg_secondary']};
        }}
        QProgressBar::chunk {{
            background-color: {theme['accent']};
            border-radius: 4px;
        }}
        """
