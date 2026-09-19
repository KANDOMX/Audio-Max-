# Audio Max

A **modern, powerful, and clean** music player application built with Python and PyQt6.

## Features

### Core Features
- **High-quality audio playback** using pygame mixer
- **Multi-format support**: MP3, WAV, FLAC, OGG, AAC, M4A, WMA
- **Playlist management** with persistent storage
- **10-band graphic equalizer** with customizable presets
- **Dark and light theme** support

### Modern UI
- Clean, minimalist design
- Responsive layout
- Smooth animations
- Custom styling with theming

### Playback Controls
- Play, pause, next, previous
- Seek slider with precise positioning
- Volume control
- Track progress display

### Playlist Management
- Create, delete, and rename playlists
- Add/remove tracks from playlists
- Import folders of music
- Search functionality
- Playback history

### Equalizer
- 10-band graphic equalizer
- Preamp control
- Multiple presets (Rock, Pop, Jazz, Classical, Bass Boost, Treble Boost, Vocal)
- Save custom presets
- Real-time frequency response visualization

## Screenshots

![Audio Max Main Window](assets/screenshot.png)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/KANDOMX/Audio-Max-.git
cd Audio-Max-

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Required Packages
- PyQt6 - GUI framework
- pygame - Audio playback
- mutagen - Audio metadata
- pydub - Audio processing
- numpy - Numerical operations

## Usage

### Running the Application

```bash
# From the project root
python main.py
```

Or run the module directly:

```bash
python -m src.audio_max.app
```

### Basic Controls
- **Play/Pause**: Click the play button or press Space
- **Next Track**: Click the next button or press Right Arrow
- **Previous Track**: Click the previous button or press Left Arrow
- **Volume**: Use the volume slider
- **Seek**: Drag the seek slider

### Keyboard Shortcuts
- **Space**: Play/Pause
- **Right Arrow**: Next track
- **Left Arrow**: Previous track
- **Up Arrow**: Volume up
- **Down Arrow**: Volume down

## Project Structure

```
Audio-Max-
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── README.md               # Documentation
└── src
    └── audio_max
        ├── __init__.py     # Package init
        ├── app.py          # Main application
        ├── player.py       # Audio playback engine
        ├── playlist.py     # Playlist management
        ├── equalizer.py    # Equalizer module
        └── utils.py        # Utility functions
```

## Configuration

### Theme
Toggle between dark and light themes using the theme button in the header.

### Equalizer Presets
Select from predefined presets or create your own custom equalizer settings.

## Development

### Adding New Features
1. Create a new module in `src/audio_max/`
2. Import and integrate with the main application
3. Update the UI as needed

### Customizing Styles
Edit the theme colors in `utils.py` to customize the application's appearance.

## Troubleshooting

### No Sound
- Ensure your system has audio output
- Check that the volume is not muted
- Verify that the audio file is not corrupted

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### PyQt6 Not Found
```bash
pip install PyQt6 PyQt6-Qt6
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

### Guidelines
- Follow PEP 8 style guide
- Add docstrings to functions and classes
- Include type hints where possible
- Write tests for new features

## License

This project is licensed under the MIT License.

## Credits

- **Developer**: KANDOMX
- **Icon Design**: Custom design
- **Inspiration**: Modern music players like Spotify, VLC

## Version History

- **v1.0.0** (2024) - Initial release
  - Basic playback functionality
  - Playlist management
  - 10-band equalizer
  - Dark/light theme support

## Future Features

- [ ] Audio visualization
- [ ] Crossfade between tracks
- [ ] Gapless playback
- [ ] Lyrics display
- [ ] Album art support
- [ ] Custom hotkeys
- [ ] Multiple language support
- [ ] Plugin system
- [ ] Streaming support

---

**Audio Max** - Your modern music player experience

*Made with ❤️ and Python*
