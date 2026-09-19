"""
Audio Player module for Audio Max
Handles audio playback using pygame
"""

import pygame
import os
from typing import Optional, Callable, Any
from pathlib import Path
from .utils import TimeFormatter


class AudioPlayer:
    """
    Audio playback engine using pygame mixer
    Supports MP3, WAV, OGG, and other formats supported by pygame
    """
    
    def __init__(self):
        """Initialize the audio player"""
        pygame.mixer.init()
        self._current_track: Optional[str] = None
        self._is_playing: bool = False
        self._is_paused: bool = False
        self._volume: float = 0.7
        self._position: float = 0.0
        self._duration: float = 0.0
        self._on_track_end: Optional[Callable] = None
        self._on_position_change: Optional[Callable] = None
        
        pygame.mixer.music.set_volume(self._volume)
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
    
    def load(self, file_path: str) -> bool:
        """
        Load an audio file
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                return False
            
            self._current_track = file_path
            self._is_playing = False
            self._is_paused = False
            self._position = 0.0
            
            # Try to get duration using pygame
            try:
                sound = pygame.mixer.Sound(file_path)
                self._duration = sound.get_length()
            except:
                # Fallback for formats that pygame can't get length for
                self._duration = 0.0
            
            pygame.mixer.music.load(file_path)
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def play(self) -> bool:
        """
        Start or resume playback
        
        Returns:
            True if playback started, False otherwise
        """
        if not self._current_track:
            return False
        
        if self._is_paused:
            pygame.mixer.music.unpause()
            self._is_paused = False
            self._is_playing = True
        else:
            pygame.mixer.music.play(start=self._position)
            self._is_playing = True
            self._is_paused = False
        
        return True
    
    def pause(self) -> bool:
        """
        Pause playback
        
        Returns:
            True if paused, False otherwise
        """
        if not self._is_playing:
            return False
        
        pygame.mixer.music.pause()
        self._is_paused = True
        self._is_playing = False
        return True
    
    def stop(self) -> bool:
        """
        Stop playback and reset position
        
        Returns:
            True if stopped, False otherwise
        """
        pygame.mixer.music.stop()
        self._is_playing = False
        self._is_paused = False
        self._position = 0.0
        return True
    
    def next_track(self) -> bool:
        """Signal that the current track should end"""
        if self._on_track_end:
            self._on_track_end()
        return True
    
    def previous_track(self) -> bool:
        """Signal to go to previous track"""
        if self._on_track_end:
            # For previous, we might want a different callback
            pass
        return True
    
    def seek(self, position: float) -> bool:
        """
        Seek to a specific position in the current track
        
        Args:
            position: Position in seconds
            
        Returns:
            True if seek succeeded, False otherwise
        """
        if not self._current_track:
            return False
        
        try:
            self._position = max(0, min(position, self._duration))
            pygame.mixer.music.set_pos(self._position)
            return True
        except:
            # Some formats don't support seeking
            # We'll handle this by stopping and replaying
            self.stop()
            pygame.mixer.music.play(start=self._position)
            self._is_playing = True
            return True
    
    def set_volume(self, volume: float) -> bool:
        """
        Set the playback volume
        
        Args:
            volume: Volume level (0.0 to 1.0)
            
        Returns:
            True if volume set, False otherwise
        """
        self._volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self._volume)
        return True
    
    def get_volume(self) -> float:
        """Get current volume level"""
        return self._volume
    
    def get_position(self) -> float:
        """Get current playback position in seconds"""
        if not self._is_playing:
            return self._position
        
        try:
            pos = pygame.mixer.music.get_pos() / 1000.0
            if pos >= 0:
                self._position = pos
            return self._position
        except:
            return self._position
    
    def get_duration(self) -> float:
        """Get current track duration in seconds"""
        return self._duration
    
    def get_position_formatted(self) -> str:
        """Get formatted current position"""
        return TimeFormatter.seconds_to_time(self.get_position())
    
    def get_duration_formatted(self) -> str:
        """Get formatted track duration"""
        return TimeFormatter.seconds_to_time(self._duration)
    
    def get_current_track(self) -> Optional[str]:
        """Get current track path"""
        return self._current_track
    
    def get_current_track_name(self) -> str:
        """Get current track filename"""
        if self._current_track:
            return os.path.basename(self._current_track)
        return "No track loaded"
    
    def is_playing(self) -> bool:
        """Check if currently playing"""
        return self._is_playing
    
    def is_paused(self) -> bool:
        """Check if currently paused"""
        return self._is_paused
    
    def has_track(self) -> bool:
        """Check if a track is loaded"""
        return self._current_track is not None
    
    def set_on_track_end(self, callback: Callable) -> None:
        """Set callback for when track ends"""
        self._on_track_end = callback
    
    def set_on_position_change(self, callback: Callable) -> None:
        """Set callback for position changes"""
        self._on_position_change = callback
    
    def update(self) -> None:
        """
        Update player state - should be called regularly
        Checks for track end events
        """
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                # Track ended
                if self._on_track_end:
                    self._on_track_end()
                self._is_playing = False
                self._position = 0.0
    
    def cleanup(self) -> None:
        """Clean up resources"""
        self.stop()
        pygame.mixer.quit()
