"""
Main application for Audio Max
Modern music player with PyQt6
"""

import sys
import os
from typing import Optional, List
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSlider, QLabel, QListWidget, QListWidgetItem,
    QStackedWidget, QFrame, QLineEdit, QComboBox, QFileDialog,
    QMessageBox, QToolButton, QInputDialog
)
from PyQt6.QtCore import (
    Qt, QSize, QTimer, pyqtSignal, QObject, QStyle
)
from PyQt6.QtGui import (
    QIcon, QPixmap, QFont, QPalette, QColor
)

from .player import AudioPlayer
from .playlist import PlaylistManager
from .equalizer import Equalizer
from .utils import ThemeManager, TimeFormatter, FileScanner


class SignalEmitter(QObject):
    """Custom signal emitter for thread-safe updates"""
    track_changed = pyqtSignal(str, str)
    playback_state_changed = pyqtSignal(bool)
    position_updated = pyqtSignal(float, float)
    playlist_updated = pyqtSignal()


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        """Initialize the main window"""
        super().__init__()
        
        # Initialize components
        self.player = AudioPlayer()
        self.playlist_manager = PlaylistManager()
        self.equalizer = Equalizer()
        self.signal_emitter = SignalEmitter()
        self.is_dark_theme = True
        
        # Window setup
        self.setWindowTitle("Audio Max")
        self.setMinimumSize(900, 600)
        self.setWindowIcon(self._create_icon())
        
        # Setup UI
        self.setup_ui()
        self.apply_theme()
        self.setup_connections()
        
        # Timer for position updates
        self.position_timer = QTimer()
        self.position_timer.timeout.connect(self.update_position)
        self.position_timer.start(1000)  # Update every second
        
        # Set track end callback
        self.player.set_on_track_end(self.on_track_end)
    
    def _create_icon(self) -> QIcon:
        """Create application icon"""
        icon = QIcon()
        # Create a simple music note icon
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        # This would be replaced with actual icon in production
        return icon
    
    def setup_ui(self) -> None:
        """Setup the user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create header
        self.header = self.create_header()
        main_layout.addWidget(self.header)
        
        # Create main content area
        content_widget = QFrame()
        content_widget.setFrameShape(QFrame.Shape.NoFrame)
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)
        
        # Left panel - Playlists
        self.left_panel = self.create_left_panel()
        content_layout.addWidget(self.left_panel, stretch=1)
        
        # Center panel - Current playlist/tracks
        self.center_panel = self.create_center_panel()
        content_layout.addWidget(self.center_panel, stretch=2)
        
        # Right panel - Equalizer/Info
        self.right_panel = self.create_right_panel()
        content_layout.addWidget(self.right_panel, stretch=1)
        
        main_layout.addWidget(content_widget, stretch=1)
        
        # Create player controls
        self.player_controls = self.create_player_controls()
        main_layout.addWidget(self.player_controls)
        
        # Status bar
        self.status_bar = QLabel()
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_bar.setStyleSheet("padding: 8px; font-size: 12px;")
        main_layout.addWidget(self.status_bar)
    
    def create_header(self) -> QWidget:
        """Create header with title and controls"""
        header = QFrame()
        header.setFrameShape(QFrame.Shape.NoFrame)
        header.setStyleSheet("background-color: #16213e; padding: 10px;")
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(10, 0, 10, 0)
        
        # Title
        title = QLabel("Audio Max")
        title.setStyleSheet("color: #e94560; font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        # Spacer
        layout.addStretch()
        
        # Theme toggle
        self.theme_btn = QToolButton()
        self.theme_btn.setIcon(self.style().standardIcon(
            getattr(QStyle, 'SP_TitleBarContextHelpButton', 0)
        ))
        self.theme_btn.setToolTip("Toggle Theme")
        self.theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_btn)
        
        # Minimize, Maximize, Close buttons would be handled by window manager
        
        return header
    
    def create_left_panel(self) -> QWidget:
        """Create left panel with playlists"""
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.NoFrame)
        panel.setStyleSheet("background-color: #1a1a2e; border-radius: 5px;")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Panel title
        title = QLabel("Playlists")
        title.setStyleSheet("color: #e94560; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Add playlist button
        add_btn = QPushButton("+")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #e94560;
                color: white;
                border: none;
                border-radius: 15px;
                width: 30px;
                height: 30px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #ff6b81;
            }
        """)
        add_btn.clicked.connect(self.add_playlist)
        layout.addWidget(add_btn)
        
        # Playlist list
        self.playlist_list = QListWidget()
        self.playlist_list.setStyleSheet("""
            QListWidget {
                background-color: #16213e;
                border: 1px solid #2a2a4a;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #2a2a4a;
            }
            QListWidget::item:selected {
                background-color: #e94560;
                color: white;
            }
        """)
        self.playlist_list.itemClicked.connect(self.on_playlist_selected)
        layout.addWidget(self.playlist_list, stretch=1)
        
        # Load playlists
        self.refresh_playlists()
        
        return panel
    
    def create_center_panel(self) -> QWidget:
        """Create center panel with track list"""
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.NoFrame)
        panel.setStyleSheet("background-color: #1a1a2e; border-radius: 5px;")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Panel title
        self.track_list_title = QLabel("Tracks")
        self.track_list_title.setStyleSheet("color: #e94560; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.track_list_title)
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search tracks...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                background-color: #16213e;
                color: #eaeaea;
                border: 1px solid #2a2a4a;
                border-radius: 4px;
                padding: 6px;
            }
        """)
        self.search_box.textChanged.connect(self.filter_tracks)
        layout.addWidget(self.search_box)
        
        # Track list
        self.track_list = QListWidget()
        self.track_list.setStyleSheet("""
            QListWidget {
                background-color: #16213e;
                border: 1px solid #2a2a4a;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #2a2a4a;
            }
            QListWidget::item:selected {
                background-color: #e94560;
                color: white;
            }
        """)
        self.track_list.itemDoubleClicked.connect(self.on_track_double_clicked)
        layout.addWidget(self.track_list, stretch=1)
        
        # Track info display
        self.track_info = QLabel("No track selected")
        self.track_info.setStyleSheet("color: #b8b8b8; font-size: 12px;")
        layout.addWidget(self.track_info)
        
        return panel
    
    def create_right_panel(self) -> QWidget:
        """Create right panel with equalizer and info"""
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.NoFrame)
        panel.setStyleSheet("background-color: #1a1a2e; border-radius: 5px;")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Tabs for different views
        self.right_tabs = QStackedWidget()
        
        # Equalizer tab
        self.eq_tab = self.create_equalizer_tab()
        self.right_tabs.addWidget(self.eq_tab)
        
        # Track info tab
        self.info_tab = self.create_info_tab()
        self.right_tabs.addWidget(self.info_tab)
        
        # Tab selector
        tab_selector = QHBoxLayout()
        self.eq_tab_btn = QPushButton("Equalizer")
        self.eq_tab_btn.setCheckable(True)
        self.eq_tab_btn.setChecked(True)
        self.eq_tab_btn.clicked.connect(lambda: self.right_tabs.setCurrentIndex(0))
        
        self.info_tab_btn = QPushButton("Info")
        self.info_tab_btn.setCheckable(True)
        self.info_tab_btn.clicked.connect(lambda: self.right_tabs.setCurrentIndex(1))
        
        tab_selector.addWidget(self.eq_tab_btn)
        tab_selector.addWidget(self.info_tab_btn)
        
        layout.addLayout(tab_selector)
        layout.addWidget(self.right_tabs)
        
        return panel
    
    def create_equalizer_tab(self) -> QWidget:
        """Create equalizer controls"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Equalizer title
        title = QLabel("Equalizer")
        title.setStyleSheet("color: #e94560; font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        
        # Enable toggle
        self.eq_enabled = QPushButton("Enable EQ")
        self.eq_enabled.setCheckable(True)
        self.eq_enabled.setChecked(True)
        self.eq_enabled.clicked.connect(self.toggle_eq)
        layout.addWidget(self.eq_enabled)
        
        # Presets combobox
        self.eq_presets = QComboBox()
        self.eq_presets.addItems(self.equalizer.get_preset_names())
        self.eq_presets.currentTextChanged.connect(self.load_eq_preset)
        layout.addWidget(self.eq_presets)
        
        # Band sliders
        self.eq_sliders = []
        for i in range(self.equalizer.get_num_bands()):
            freq = self.equalizer.get_band_frequency(i)
            
            band_layout = QHBoxLayout()
            
            # Frequency label
            freq_label = QLabel(f"{int(freq)}Hz")
            freq_label.setStyleSheet("color: #b8b8b8; font-size: 10px;")
            freq_label.setFixedWidth(50)
            band_layout.addWidget(freq_label)
            
            # Slider
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(-20, 20)
            slider.setValue(0)
            slider.setFixedHeight(20)
            slider.valueChanged.connect(lambda v, idx=i: self.on_eq_slider_changed(idx, v))
            band_layout.addWidget(slider, stretch=1)
            
            # Value label
            value_label = QLabel("0dB")
            value_label.setStyleSheet("color: #b8b8b8; font-size: 10px;")
            value_label.setFixedWidth(40)
            band_layout.addWidget(value_label)
            
            layout.addLayout(band_layout)
            self.eq_sliders.append((slider, value_label))
        
        # Preamp control
        preamp_layout = QHBoxLayout()
        preamp_label = QLabel("Preamp")
        preamp_label.setStyleSheet("color: #b8b8b8; font-size: 10px;")
        preamp_layout.addWidget(preamp_label)
        
        self.preamp_slider = QSlider(Qt.Orientation.Horizontal)
        self.preamp_slider.setRange(-20, 20)
        self.preamp_slider.setValue(0)
        self.preamp_slider.valueChanged.connect(self.on_preamp_changed)
        preamp_layout.addWidget(self.preamp_slider, stretch=1)
        
        self.preamp_label = QLabel("0dB")
        self.preamp_label.setStyleSheet("color: #b8b8b8; font-size: 10px;")
        preamp_layout.addWidget(self.preamp_label)
        
        layout.addLayout(preamp_layout)
        
        # Reset button
        reset_btn = QPushButton("Reset EQ")
        reset_btn.clicked.connect(self.reset_eq)
        layout.addWidget(reset_btn)
        
        # Initialize sliders
        self.update_eq_sliders()
        
        return tab
    
    def create_info_tab(self) -> QWidget:
        """Create track info display"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Info title
        title = QLabel("Track Info")
        title.setStyleSheet("color: #e94560; font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        
        # Info display
        self.track_info_display = QLabel("No track info available")
        self.track_info_display.setStyleSheet("color: #b8b8b8; font-size: 12px;")
        self.track_info_display.setWordWrap(True)
        layout.addWidget(self.track_info_display, stretch=1)
        
        return tab
    
    def create_player_controls(self) -> QWidget:
        """Create player control panel"""
        controls = QFrame()
        controls.setFrameShape(QFrame.Shape.NoFrame)
        controls.setStyleSheet("background-color: #0f3460; padding: 15px;")
        
        layout = QHBoxLayout(controls)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(15)
        
        # Previous button
        prev_btn = QPushButton()
        prev_btn.setIcon(self.style().standardIcon(
            getattr(QStyle, 'SP_MediaSkipBackward', 0)
        ))
        prev_btn.setFixedSize(40, 40)
        prev_btn.setStyleSheet("border-radius: 20px;")
        prev_btn.clicked.connect(self.previous_track)
        layout.addWidget(prev_btn)
        
        # Play/Pause button
        self.play_btn = QPushButton()
        self.play_btn.setIcon(self.style().standardIcon(
            getattr(QStyle, 'SP_MediaPlay', 0)
        ))
        self.play_btn.setFixedSize(50, 50)
        self.play_btn.setStyleSheet("border-radius: 25px;")
        self.play_btn.clicked.connect(self.toggle_playback)
        layout.addWidget(self.play_btn)
        
        # Next button
        next_btn = QPushButton()
        next_btn.setIcon(self.style().standardIcon(
            getattr(QStyle, 'SP_MediaSkipForward', 0)
        ))
        next_btn.setFixedSize(40, 40)
        next_btn.setStyleSheet("border-radius: 20px;")
        next_btn.clicked.connect(self.next_track)
        layout.addWidget(next_btn)
        
        # Spacer
        layout.addStretch()
        
        # Progress display
        self.progress_label = QLabel("00:00 / 00:00")
        self.progress_label.setStyleSheet("color: #eaeaea; font-size: 14px;")
        layout.addWidget(self.progress_label)
        
        # Spacer
        layout.addStretch()
        
        # Volume control
        volume_layout = QHBoxLayout()
        volume_icon = QLabel()
        volume_icon.setPixmap(QPixmap(":/icons/volume").scaled(20, 20)) if False else None
        volume_layout.addWidget(volume_icon)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(int(self.player.get_volume() * 100))
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        volume_layout.addWidget(self.volume_slider)
        
        layout.addLayout(volume_layout)
        
        # Seek slider
        self.seek_slider = QSlider(Qt.Orientation.Horizontal)
        self.seek_slider.setRange(0, 1000)
        self.seek_slider.setValue(0)
        self.seek_slider.sliderMoved.connect(self.on_seek)
        layout.addWidget(self.seek_slider)
        
        return controls
    
    def apply_theme(self) -> None:
        """Apply the current theme to the UI"""
        theme = ThemeManager.get_theme(self.is_dark_theme)
        stylesheet = ThemeManager.get_stylesheet(self.is_dark_theme)
        
        self.setStyleSheet(stylesheet)
        
        # Update button styles
        for btn in self.findChildren(QPushButton):
            btn.setStyleSheet(f"""
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
            """)
    
    def toggle_theme(self) -> None:
        """Toggle between dark and light themes"""
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()
    
    def setup_connections(self) -> None:
        """Setup signal connections"""
        self.signal_emitter.track_changed.connect(self.on_track_changed)
        self.signal_emitter.playback_state_changed.connect(self.on_playback_state_changed)
        self.signal_emitter.position_updated.connect(self.on_position_updated)
        self.signal_emitter.playlist_updated.connect(self.refresh_playlists)
    
    def refresh_playlists(self) -> None:
        """Refresh the playlist list"""
        self.playlist_list.clear()
        playlists = self.playlist_manager.get_all_playlists()
        
        for playlist_name in playlists:
            item = QListWidgetItem(playlist_name)
            item.setData(Qt.ItemDataRole.UserRole, playlist_name)
            self.playlist_list.addItem(item)
        
        # Refresh current playlist tracks
        if self.playlist_manager.get_current_playlist():
            self.refresh_tracks()
    
    def refresh_tracks(self) -> None:
        """Refresh the track list for current playlist"""
        self.track_list.clear()
        
        current_playlist = self.playlist_manager.get_current_playlist()
        if not current_playlist:
            self.track_list_title.setText("Tracks (No playlist selected)")
            return
        
        self.track_list_title.setText(f"Tracks - {current_playlist}")
        
        tracks = self.playlist_manager.get_playlist(current_playlist)
        if not tracks:
            return
        
        for track in tracks:
            item = QListWidgetItem(os.path.basename(track))
            item.setData(Qt.ItemDataRole.UserRole, track)
            self.track_list.addItem(item)
    
    def add_playlist(self) -> None:
        """Add a new playlist"""
        name, ok = QInputDialog.getText(
            self, "New Playlist", "Enter playlist name:"
        )
        if ok and name:
            self.playlist_manager.create_playlist(name)
            self.refresh_playlists()
    
    def on_playlist_selected(self, item: QListWidgetItem) -> None:
        """Handle playlist selection"""
        playlist_name = item.data(Qt.ItemDataRole.UserRole)
        self.playlist_manager.set_current_playlist(playlist_name)
        self.refresh_tracks()
    
    def on_track_double_clicked(self, item: QListWidgetItem) -> None:
        """Handle track double click - play the track"""
        track_path = item.data(Qt.ItemDataRole.UserRole)
        self.play_track(track_path)
    
    def play_track(self, track_path: str) -> None:
        """Play a specific track"""
        if self.player.load(track_path):
            self.player.play()
            self.signal_emitter.playback_state_changed.emit(True)
            
            # Update track info
            track_name = os.path.basename(track_path)
            info = self.playlist_manager.get_track_info(track_path)
            
            self.track_info.setText(f"Now Playing: {track_name}")
            self.signal_emitter.track_changed.emit(track_path, track_name)
            
            # Update seek slider range
            duration = self.player.get_duration()
            self.seek_slider.setRange(0, max(1, int(duration * 1000)))
    
    def on_track_changed(self, path: str, name: str) -> None:
        """Handle track change signal"""
        self.track_info.setText(f"Now Playing: {name}")
    
    def on_track_end(self) -> None:
        """Handle track end"""
        # Get next track from current playlist
        next_track = self.playlist_manager.get_next_track()
        if next_track:
            self.play_track(next_track)
        else:
            # Playlist ended
            self.player.stop()
            self.signal_emitter.playback_state_changed.emit(False)
    
    def toggle_playback(self) -> None:
        """Toggle play/pause"""
        if self.player.is_playing():
            self.player.pause()
            self.signal_emitter.playback_state_changed.emit(False)
        else:
            if not self.player.has_track():
                # Try to play first track from current playlist
                current_track = self.playlist_manager.get_current_track()
                if current_track:
                    self.play_track(current_track)
            else:
                self.player.play()
                self.signal_emitter.playback_state_changed.emit(True)
    
    def on_playback_state_changed(self, is_playing: bool) -> None:
        """Handle playback state change"""
        if is_playing:
            self.play_btn.setIcon(self.style().standardIcon(
                getattr(QStyle, 'SP_MediaPause', 0)
            ))
        else:
            self.play_btn.setIcon(self.style().standardIcon(
                getattr(QStyle, 'SP_MediaPlay', 0)
            ))
    
    def next_track(self) -> None:
        """Play next track"""
        next_track = self.playlist_manager.get_next_track()
        if next_track:
            self.play_track(next_track)
    
    def previous_track(self) -> None:
        """Play previous track"""
        prev_track = self.playlist_manager.get_previous_track()
        if prev_track:
            self.play_track(prev_track)
    
    def update_position(self) -> None:
        """Update playback position"""
        if self.player.has_track():
            position = self.player.get_position()
            duration = self.player.get_duration()
            
            self.progress_label.setText(
                f"{self.player.get_position_formatted()} / {self.player.get_duration_formatted()}"
            )
            
            if duration > 0:
                self.seek_slider.setValue(int(position * 1000))
    
    def on_seek(self, value: int) -> None:
        """Handle seek slider movement"""
        if self.player.has_track():
            duration = self.player.get_duration()
            if duration > 0:
                position = value / 1000.0
                self.player.seek(position)
    
    def on_volume_changed(self, value: int) -> None:
        """Handle volume slider change"""
        volume = value / 100.0
        self.player.set_volume(volume)
    
    def on_eq_slider_changed(self, band_index: int, value: int) -> None:
        """Handle equalizer slider change"""
        self.equalizer.set_band_gain(band_index, float(value))
        self.eq_sliders[band_index][1].setText(f"{value}dB")
    
    def on_preamp_changed(self, value: int) -> None:
        """Handle preamp slider change"""
        self.equalizer.set_preamp(float(value))
        self.preamp_label.setText(f"{value}dB")
    
    def update_eq_sliders(self) -> None:
        """Update equalizer sliders to match current settings"""
        for i in range(self.equalizer.get_num_bands()):
            gain = self.equalizer.get_band_gain(i)
            if gain is not None:
                self.eq_sliders[i][0].setValue(int(gain))
                self.eq_sliders[i][1].setText(f"{int(gain)}dB")
        
        preamp = self.equalizer.get_preamp()
        self.preamp_slider.setValue(int(preamp))
        self.preamp_label.setText(f"{int(preamp)}dB")
    
    def toggle_eq(self, enabled: bool) -> None:
        """Toggle equalizer on/off"""
        self.equalizer.set_enabled(enabled)
    
    def load_eq_preset(self, preset_name: str) -> None:
        """Load an equalizer preset"""
        self.equalizer.load_preset(preset_name)
        self.update_eq_sliders()
    
    def reset_eq(self) -> None:
        """Reset equalizer to flat"""
        self.equalizer.reset()
        self.update_eq_sliders()
    
    def filter_tracks(self, query: str) -> None:
        """Filter tracks based on search query"""
        # This would implement track filtering
        # For now, we'll just refresh the list
        self.refresh_tracks()
    
    def closeEvent(self, event) -> None:
        """Handle window close"""
        self.player.cleanup()
        event.accept()


class AudioMaxApp:
    """Main application class"""
    
    def __init__(self):
        """Initialize the application"""
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
    
    def run(self) -> int:
        """Run the application"""
        self.window.show()
        return self.app.exec()


def main():
    """Entry point for the application"""
    app = AudioMaxApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
