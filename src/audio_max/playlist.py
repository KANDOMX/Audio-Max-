"""
Playlist management for Audio Max
"""

import os
import json
from typing import List, Dict, Optional, Any
from pathlib import Path
from .utils import FileScanner


class PlaylistManager:
    """
    Manages playlists and track queues
    """
    
    def __init__(self, storage_path: str = "playlists.json"):
        """
        Initialize playlist manager
        
        Args:
            storage_path: Path to save playlists to
        """
        self.storage_path = storage_path
        self.playlists: Dict[str, List[str]] = {}
        self.current_playlist: Optional[str] = None
        self.current_index: int = 0
        self.queue: List[str] = []
        self.history: List[str] = []
        self.load_playlists()
    
    def load_playlists(self) -> None:
        """Load playlists from storage"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    self.playlists = json.load(f)
        except Exception as e:
            print(f"Error loading playlists: {e}")
            self.playlists = {}
    
    def save_playlists(self) -> None:
        """Save playlists to storage"""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.playlists, f, indent=2)
        except Exception as e:
            print(f"Error saving playlists: {e}")
    
    def create_playlist(self, name: str, tracks: List[str] = None) -> bool:
        """
        Create a new playlist
        
        Args:
            name: Playlist name
            tracks: Optional list of track paths
            
        Returns:
            True if created, False if already exists
        """
        if name in self.playlists:
            return False
        
        self.playlists[name] = tracks or []
        self.save_playlists()
        return True
    
    def delete_playlist(self, name: str) -> bool:
        """
        Delete a playlist
        
        Args:
            name: Playlist name
            
        Returns:
            True if deleted, False if not found
        """
        if name not in self.playlists:
            return False
        
        del self.playlists[name]
        if self.current_playlist == name:
            self.current_playlist = None
            self.current_index = 0
        self.save_playlists()
        return True
    
    def rename_playlist(self, old_name: str, new_name: str) -> bool:
        """
        Rename a playlist
        
        Args:
            old_name: Current playlist name
            new_name: New playlist name
            
        Returns:
            True if renamed, False if failed
        """
        if old_name not in self.playlists or new_name in self.playlists:
            return False
        
        self.playlists[new_name] = self.playlists.pop(old_name)
        if self.current_playlist == old_name:
            self.current_playlist = new_name
        self.save_playlists()
        return True
    
    def add_track_to_playlist(self, playlist_name: str, track_path: str) -> bool:
        """
        Add a track to a playlist
        
        Args:
            playlist_name: Name of the playlist
            track_path: Path to the audio file
            
        Returns:
            True if added, False if playlist not found
        """
        if playlist_name not in self.playlists:
            return False
        
        if track_path not in self.playlists[playlist_name]:
            self.playlists[playlist_name].append(track_path)
            self.save_playlists()
        return True
    
    def remove_track_from_playlist(self, playlist_name: str, track_path: str) -> bool:
        """
        Remove a track from a playlist
        
        Args:
            playlist_name: Name of the playlist
            track_path: Path to the audio file
            
        Returns:
            True if removed, False if not found
        """
        if playlist_name not in self.playlists:
            return False
        
        if track_path in self.playlists[playlist_name]:
            self.playlists[playlist_name].remove(track_path)
            self.save_playlists()
            return True
        return False
    
    def get_playlist(self, name: str) -> Optional[List[str]]:
        """
        Get tracks from a playlist
        
        Args:
            name: Playlist name
            
        Returns:
            List of track paths or None if not found
        """
        return self.playlists.get(name)
    
    def get_all_playlists(self) -> List[str]:
        """Get all playlist names"""
        return list(self.playlists.keys())
    
    def set_current_playlist(self, name: str) -> bool:
        """
        Set the current playlist
        
        Args:
            name: Playlist name
            
        Returns:
            True if set, False if not found
        """
        if name not in self.playlists:
            return False
        
        self.current_playlist = name
        self.current_index = 0
        return True
    
    def get_current_playlist(self) -> Optional[str]:
        """Get current playlist name"""
        return self.current_playlist
    
    def get_current_track(self) -> Optional[str]:
        """
        Get the current track from the current playlist
        
        Returns:
            Track path or None if no playlist or empty
        """
        if not self.current_playlist:
            return None
        
        playlist = self.playlists.get(self.current_playlist, [])
        if not playlist or self.current_index >= len(playlist):
            return None
        
        return playlist[self.current_index]
    
    def get_next_track(self) -> Optional[str]:
        """
        Get the next track from the current playlist
        
        Returns:
            Track path or None if no more tracks
        """
        if not self.current_playlist:
            return None
        
        playlist = self.playlists.get(self.current_playlist, [])
        if not playlist:
            return None
        
        next_index = self.current_index + 1
        if next_index >= len(playlist):
            # Loop to beginning
            next_index = 0
        
        self.current_index = next_index
        return playlist[next_index]
    
    def get_previous_track(self) -> Optional[str]:
        """
        Get the previous track from the current playlist
        
        Returns:
            Track path or None if no previous tracks
        """
        if not self.current_playlist:
            return None
        
        playlist = self.playlists.get(self.current_playlist, [])
        if not playlist:
            return None
        
        prev_index = self.current_index - 1
        if prev_index < 0:
            # Loop to end
            prev_index = len(playlist) - 1
        
        self.current_index = prev_index
        return playlist[prev_index]
    
    def add_to_queue(self, track_path: str) -> None:
        """Add a track to the play queue"""
        self.queue.append(track_path)
    
    def get_next_in_queue(self) -> Optional[str]:
        """
        Get the next track from the queue
        
        Returns:
            Track path or None if queue is empty
        """
        if self.queue:
            return self.queue.pop(0)
        return None
    
    def add_to_history(self, track_path: str) -> None:
        """Add a track to playback history"""
        self.history.append(track_path)
        # Keep history limited to 100 tracks
        if len(self.history) > 100:
            self.history = self.history[-100:]
    
    def get_history(self) -> List[str]:
        """Get playback history"""
        return self.history.copy()
    
    def scan_directory_to_playlist(self, directory: str, playlist_name: str) -> int:
        """
        Scan a directory for audio files and add to a playlist
        
        Args:
            directory: Directory to scan
            playlist_name: Name of the playlist to create/add to
            
        Returns:
            Number of tracks added
        """
        audio_files = FileScanner.scan_directory(directory)
        
        if playlist_name not in self.playlists:
            self.create_playlist(playlist_name)
        
        existing = set(self.playlists[playlist_name])
        added = 0
        
        for audio_file in audio_files:
            if audio_file not in existing:
                self.playlists[playlist_name].append(audio_file)
                existing.add(audio_file)
                added += 1
        
        if added > 0:
            self.save_playlists()
        
        return added
    
    def search_in_playlists(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for tracks across all playlists
        
        Args:
            query: Search query (case insensitive)
            
        Returns:
            List of matching tracks with playlist info
        """
        results = []
        query_lower = query.lower()
        
        for playlist_name, tracks in self.playlists.items():
            for track in tracks:
                track_name = os.path.basename(track).lower()
                if query_lower in track_name:
                    results.append({
                        'playlist': playlist_name,
                        'track': track,
                        'name': os.path.basename(track)
                    })
        
        return results
    
    def get_track_info(self, track_path: str) -> Dict[str, Any]:
        """
        Get information about a track
        
        Args:
            track_path: Path to the track
            
        Returns:
            Dictionary with track information
        """
        try:
            from mutagen import File
            audio = File(track_path)
            info = {
                'path': track_path,
                'name': os.path.basename(track_path),
                'size': os.path.getsize(track_path)
            }
            
            if audio:
                if 'title' in audio:
                    info['title'] = str(audio['title'][0])
                if 'artist' in audio:
                    info['artist'] = str(audio['artist'][0])
                if 'album' in audio:
                    info['album'] = str(audio['album'][0])
                if 'length' in audio:
                    info['duration'] = float(audio.info.length)
            
            return info
        except Exception as e:
            print(f"Error getting track info: {e}")
            return {
                'path': track_path,
                'name': os.path.basename(track_path),
                'size': os.path.getsize(track_path) if os.path.exists(track_path) else 0
            }
