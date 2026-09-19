"""
Audio Max Mobile - Kivy Version
Complete music player for Android/iOS
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.utils import platform

import os
import json
from pathlib import Path

# Import audio modules
try:
    from .player import AudioPlayer
    from .playlist import PlaylistManager
    from .equalizer import Equalizer
    from .utils import ThemeManager, TimeFormatter, FileScanner
except:
    # Fallback for mobile
    pass

# Set window size for desktop testing
Window.size = (400, 700)

# Kivy language string for UI
KV = '''
<AudioMaxApp>:
    manager: screen_manager
    
    ScreenManager:
        id: screen_manager
        
        MainScreen:
            id: main_screen
            name: 'main'
            manager: root.manager
            
        PlaylistScreen:
            id: playlist_screen
            name: 'playlists'
            manager: root.manager
            
        EqualizerScreen:
            id: eq_screen
            name: 'equalizer'
            manager: root.manager

<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        
        # Header
        BoxLayout:
            size_hint_y: None
            height: 50
            
            Label:
                text: 'Audio Max'
                font_size: 24
                color: 1, 0.3, 0.5, 1
                bold: True
            
            Label:
                text: ''
            
            Button:
                text: 'Menu'
                size_hint_x: None
                width: 100
                on_press: root.show_menu()
        
        # Now Playing
        BoxLayout:
            size_hint_y: None
            height: 100
            padding: 10
            
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.7
                
                Label:
                    id: track_title
                    text: 'No Track Selected'
                    font_size: 18
                    bold: True
                    color: 1, 1, 1, 1
                
                Label:
                    id: track_info
                    text: ''
                    font_size: 14
                    color: 0.8, 0.8, 0.8, 1
            
            BoxLayout:
                size_hint_x: 0.3
                
                Label:
                    id: track_time
                    text: '00:00 / 00:00'
                    font_size: 14
                    color: 1, 1, 1, 1
        
        # Progress Slider
        Slider:
            id: progress_slider
            size_hint_y: None
            height: 30
            
        # Player Controls
        BoxLayout:
            size_hint_y: None
            height: 80
            padding: 10
            spacing: 20
            
            Button:
                text: 'Prev'
                on_press: root.prev_track()
            
            Button:
                id: play_btn
                text: 'Play'
                font_size: 18
                on_press: root.toggle_play()
            
            Button:
                text: 'Next'
                on_press: root.next_track()
        
        # Volume Control
        BoxLayout:
            size_hint_y: None
            height: 40
            
            Label:
                text: 'Volume:'
                size_hint_x: None
                width: 80
            
            Slider:
                id: volume_slider
                value: 70
                on_value: root.set_volume(args[1])
        
        # Track List
        BoxLayout:
            orientation: 'vertical'
            
            Label:
                text: 'Tracks'
                font_size: 16
                color: 1, 0.3, 0.5, 1
                bold: True
            
            ScrollView:
                id: track_scroll
                
                GridLayout:
                    id: track_grid
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    padding: 5
                    spacing: 5
        
        # Bottom Bar
        BoxLayout:
            size_hint_y: None
            height: 40
            
            Button:
                text: 'Playlists'
                on_press: root.switch_to_playlists()
            
            Button:
                text: 'Equalizer'
                on_press: root.switch_to_equalizer()

<PlaylistScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        
        # Header
        BoxLayout:
            size_hint_y: None
            height: 50
            
            Button:
                text: 'Back'
                size_hint_x: None
                width: 100
                on_press: root.back_to_main()
            
            Label:
                text: 'Playlists'
                font_size: 20
                color: 1, 0.3, 0.5, 1
                bold: True
        
        # Playlist List
        ScrollView:
            
            GridLayout:
                id: playlist_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 5
                spacing: 5
        
        # Add Playlist Button
        Button:
            text: '+ Add Playlist'
            size_hint_y: None
            height: 50
            on_press: root.add_playlist()

<EqualizerScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        
        # Header
        BoxLayout:
            size_hint_y: None
            height: 50
            
            Button:
                text: 'Back'
                size_hint_x: None
                width: 100
                on_press: root.back_to_main()
            
            Label:
                text: 'Equalizer'
                font_size: 20
                color: 1, 0.3, 0.5, 1
                bold: True
        
        # Enable Toggle
        BoxLayout:
            size_hint_y: None
            height: 40
            
            Label:
                text: 'Enable EQ:'
            
            Button:
                id: eq_enabled
                text: 'ON'
                on_press: root.toggle_eq()
        
        # Presets
        BoxLayout:
            size_hint_y: None
            height: 40
            
            Label:
                text: 'Preset:'
            
            Spinner:
                id: eq_presets
                values: ['Flat', 'Rock', 'Pop', 'Jazz', 'Classical', 'Bass Boost', 'Treble Boost', 'Vocal']
                on_text: root.load_preset(args[1])
        
        # EQ Bands
        ScrollView:
            
            GridLayout:
                id: eq_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 5
                spacing: 10

<EQBand>:
    BoxLayout:
        size_hint_y: None
        height: 40
        
        Label:
            id: freq_label
            text: '60Hz'
            size_hint_x: None
            width: 80
        
        Slider:
            id: gain_slider
            min: -20
            max: 20
            value: 0
            on_value: root.update_gain(args[1])
        
        Label:
            id: gain_label
            text: '0dB'
            size_hint_x: None
            width: 50

<PopupInput>:
    size_hint: 0.8, 0.4
    
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        
        Label:
            id: popup_title
            text: 'Enter Playlist Name'
            font_size: 18
        
        TextInput:
            id: input_text
            hint_text: 'Playlist name'
            multiline: False
        
        BoxLayout:
            size_hint_y: None
            height: 40
            spacing: 10
            
            Button:
                text: 'Cancel'
                on_press: root.dismiss()
            
            Button:
                text: 'OK'
                on_press: root.submit()
'''


class EQBand(BoxLayout):
    """Equalizer band control"""
    band_index = NumericProperty(0)
    
    def __init__(self, band_index, frequency, **kwargs):
        super().__init__(**kwargs)
        self.band_index = band_index
        self.ids.freq_label.text = f"{int(frequency)}Hz"
    
    def update_gain(self, value):
        self.ids.gain_label.text = f"{int(value)}dB"


class PopupInput(Popup):
    """Input popup for playlist name"""
    callback = ObjectProperty(None)
    
    def submit(self):
        if self.callback:
            self.callback(self.ids.input_text.text)
        self.dismiss()


class MainScreen(Screen):
    """Main player screen"""
    manager = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = None
        self.playlist_manager = None
        self.current_playlist = None
        self.update_timer = None
    
    def on_enter(self):
        # Initialize player
        if not self.player:
            from .player import AudioPlayer
            from .playlist import PlaylistManager
            self.player = AudioPlayer()
            self.playlist_manager = PlaylistManager()
        
        # Start update timer
        if self.update_timer:
            self.update_timer.cancel()
        self.update_timer = Clock.schedule_interval(self.update_progress, 1.0)
    
    def on_leave(self):
        if self.update_timer:
            self.update_timer.cancel()
    
    def update_progress(self, dt):
        if self.player and self.player.has_track():
            position = self.player.get_position()
            duration = self.player.get_duration()
            
            self.ids.track_time.text = f"{self.player.get_position_formatted()} / {self.player.get_duration_formatted()}"
            
            if duration > 0:
                self.ids.progress_slider.value = (position / duration) * 100
    
    def show_menu(self):
        self.manager.current = 'playlists'
    
    def switch_to_playlists(self):
        self.manager.current = 'playlists'
    
    def switch_to_equalizer(self):
        self.manager.current = 'equalizer'
    
    def toggle_play(self):
        if self.player.is_playing():
            self.player.pause()
            self.ids.play_btn.text = 'Play'
        else:
            if not self.player.has_track():
                # Play first track
                track = self.playlist_manager.get_current_track()
                if track:
                    self.play_track(track)
            else:
                self.player.play()
                self.ids.play_btn.text = 'Pause'
    
    def play_track(self, track_path):
        if self.player.load(track_path):
            self.player.play()
            self.ids.play_btn.text = 'Pause'
            self.ids.track_title.text = os.path.basename(track_path)
    
    def prev_track(self):
        track = self.playlist_manager.get_previous_track()
        if track:
            self.play_track(track)
    
    def next_track(self):
        track = self.playlist_manager.get_next_track()
        if track:
            self.play_track(track)
    
    def set_volume(self, value):
        if self.player:
            self.player.set_volume(value / 100.0)
    
    def on_track_end(self):
        self.next_track()


class PlaylistScreen(Screen):
    """Playlist management screen"""
    manager = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.playlist_manager = None
    
    def on_enter(self):
        if not self.playlist_manager:
            from .playlist import PlaylistManager
            self.playlist_manager = PlaylistManager()
        self.refresh_playlists()
    
    def refresh_playlists(self):
        self.ids.playlist_grid.clear_widgets()
        
        playlists = self.playlist_manager.get_all_playlists()
        for playlist_name in playlists:
            btn = Button(
                text=playlist_name,
                size_hint_y=None,
                height=50
            )
            btn.bind(on_press=lambda btn: self.select_playlist(btn.text))
            self.ids.playlist_grid.add_widget(btn)
    
    def select_playlist(self, playlist_name):
        self.playlist_manager.set_current_playlist(playlist_name)
        # Switch back to main screen and refresh tracks
        self.manager.get_screen('main').current_playlist = playlist_name
        self.manager.current = 'main'
        self.refresh_tracks_in_main()
    
    def refresh_tracks_in_main(self):
        main_screen = self.manager.get_screen('main')
        main_screen.refresh_tracks()
    
    def add_playlist(self):
        popup = PopupInput(callback=self.create_playlist)
        popup.open()
    
    def create_playlist(self, name):
        if name:
            self.playlist_manager.create_playlist(name)
            self.refresh_playlists()
    
    def back_to_main(self):
        self.manager.current = 'main'


class EqualizerScreen(Screen):
    """Equalizer settings screen"""
    manager = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.equalizer = None
    
    def on_enter(self):
        if not self.equalizer:
            from .equalizer import Equalizer
            self.equalizer = Equalizer()
        self.setup_eq_bands()
    
    def setup_eq_bands(self):
        self.ids.eq_grid.clear_widgets()
        
        for i in range(self.equalizer.get_num_bands()):
            freq = self.equalizer.get_band_frequency(i)
            band = EQBand(i, freq)
            band.ids.gain_slider.bind(value=self.on_band_change)
            self.ids.eq_grid.add_widget(band)
    
    def on_band_change(self, instance, value):
        band_index = instance.parent.band_index
        self.equalizer.set_band_gain(band_index, float(value))
    
    def toggle_eq(self):
        enabled = self.equalizer.is_enabled()
        self.equalizer.set_enabled(not enabled)
        self.ids.eq_enabled.text = 'ON' if not enabled else 'OFF'
    
    def load_preset(self, preset_name):
        preset_map = {
            'Flat': 'flat',
            'Rock': 'rock',
            'Pop': 'pop',
            'Jazz': 'jazz',
            'Classical': 'classical',
            'Bass Boost': 'bass_boost',
            'Treble Boost': 'treble_boost',
            'Vocal': 'vocal'
        }
        preset_key = preset_map.get(preset_name, 'flat')
        self.equalizer.load_preset(preset_key)
        # Refresh sliders
        for child in self.ids.eq_grid.children:
            if isinstance(child, EQBand):
                gain = self.equalizer.get_band_gain(child.band_index)
                if gain is not None:
                    child.ids.gain_slider.value = gain
                    child.ids.gain_label.text = f"{int(gain)}dB"
    
    def back_to_main(self):
        self.manager.current = 'main'


class AudioMaxApp(App):
    """Main application"""
    manager = ObjectProperty(None)
    
    def build(self):
        Builder.load_string(KV)
        return self.manager
    
    def on_start(self):
        # Set dark theme colors
        Window.clearcolor = (0.1, 0.1, 0.18, 1)


if __name__ == '__main__':
    AudioMaxApp().run()
