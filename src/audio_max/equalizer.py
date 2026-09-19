"""
Equalizer module for Audio Max
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class EQBand:
    """Represents an equalizer band"""
    frequency: float  # Center frequency in Hz
    gain: float = 0.0  # Gain in dB (-20 to +20)
    q_factor: float = 1.0  # Quality factor
    
    def __post_init__(self):
        self.gain = max(-20.0, min(20.0, self.gain))


@dataclass
class EqualizerSettings:
    """Equalizer settings with presets"""
    bands: List[EQBand] = field(default_factory=list)
    enabled: bool = True
    preamp: float = 0.0  # Global preamp gain in dB
    
    # Presets
    PRESETS = {
        'flat': [
            EQBand(60, 0), EQBand(170, 0), EQBand(310, 0), EQBand(600, 0),
            EQBand(1000, 0), EQBand(3000, 0), EQBand(6000, 0), EQBand(12000, 0),
            EQBand(14000, 0), EQBand(16000, 0)
        ],
        'rock': [
            EQBand(60, 4), EQBand(170, 3), EQBand(310, 2), EQBand(600, 1),
            EQBand(1000, 0), EQBand(3000, 2), EQBand(6000, 3), EQBand(12000, 4),
            EQBand(14000, 4), EQBand(16000, 3)
        ],
        'pop': [
            EQBand(60, 2), EQBand(170, 3), EQBand(310, 1), EQBand(600, 0),
            EQBand(1000, -1), EQBand(3000, 2), EQBand(6000, 3), EQBand(12000, 2),
            EQBand(14000, 1), EQBand(16000, 0)
        ],
        'jazz': [
            EQBand(60, 3), EQBand(170, 2), EQBand(310, 0), EQBand(600, -1),
            EQBand(1000, 0), EQBand(3000, 1), EQBand(6000, 2), EQBand(12000, 1),
            EQBand(14000, 0), EQBand(16000, -1)
        ],
        'classical': [
            EQBand(60, 2), EQBand(170, 1), EQBand(310, 0), EQBand(600, 0),
            EQBand(1000, 0), EQBand(3000, 0), EQBand(6000, -1), EQBand(12000, -1),
            EQBand(14000, -2), EQBand(16000, -2)
        ],
        'bass_boost': [
            EQBand(60, 6), EQBand(170, 4), EQBand(310, 2), EQBand(600, 0),
            EQBand(1000, -2), EQBand(3000, -1), EQBand(6000, 0), EQBand(12000, 0),
            EQBand(14000, 0), EQBand(16000, 0)
        ],
        'treble_boost': [
            EQBand(60, 0), EQBand(170, 0), EQBand(310, 0), EQBand(600, 0),
            EQBand(1000, 1), EQBand(3000, 2), EQBand(6000, 4), EQBand(12000, 5),
            EQBand(14000, 5), EQBand(16000, 4)
        ],
        'vocal': [
            EQBand(60, -2), EQBand(170, -1), EQBand(310, 0), EQBand(600, 1),
            EQBand(1000, 2), EQBand(3000, 3), EQBand(6000, 2), EQBand(12000, 1),
            EQBand(14000, 0), EQBand(16000, -1)
        ]
    }


class Equalizer:
    """
    Software equalizer for audio processing
    Uses numpy for FFT-based equalization
    """
    
    # Standard 10-band equalizer frequencies (ISO standard)
    STANDARD_FREQUENCIES = [
        60, 170, 310, 600, 1000, 3000, 6000, 12000, 14000, 16000
    ]
    
    def __init__(self, sample_rate: int = 44100, num_bands: int = 10):
        """
        Initialize the equalizer
        
        Args:
            sample_rate: Audio sample rate in Hz
            num_bands: Number of equalizer bands
        """
        self.sample_rate = sample_rate
        self.num_bands = num_bands
        self.settings = EqualizerSettings()
        self._initialize_bands()
        self._filters = []
        self._create_filters()
    
    def _initialize_bands(self) -> None:
        """Initialize equalizer bands with standard frequencies"""
        frequencies = self.STANDARD_FREQUENCIES[:self.num_bands]
        self.settings.bands = [EQBand(freq) for freq in frequencies]
    
    def _create_filters(self) -> None:
        """Create filter coefficients for each band"""
        # This would be implemented with actual filter design
        # For now, we'll use a simplified approach
        self._filters = [self._design_band_filter(band) for band in self.settings.bands]
    
    def _design_band_filter(self, band: EQBand) -> Dict:
        """
        Design a peaking filter for a band
        
        Args:
            band: The EQBand to design filter for
            
        Returns:
            Filter coefficients
        """
        # Simplified filter design
        # In a real implementation, this would use proper IIR filter design
        # For now, we'll just store the band parameters
        return {
            'frequency': band.frequency,
            'gain': band.gain,
            'q_factor': band.q_factor
        }
    
    def set_band_gain(self, band_index: int, gain: float) -> bool:
        """
        Set gain for a specific band
        
        Args:
            band_index: Index of the band (0 to num_bands-1)
            gain: Gain in dB (-20 to +20)
            
        Returns:
            True if set successfully
        """
        if 0 <= band_index < len(self.settings.bands):
            self.settings.bands[band_index].gain = max(-20.0, min(20.0, gain))
            self._filters[band_index] = self._design_band_filter(
                self.settings.bands[band_index]
            )
            return True
        return False
    
    def get_band_gain(self, band_index: int) -> Optional[float]:
        """
        Get gain for a specific band
        
        Args:
            band_index: Index of the band
            
        Returns:
            Gain in dB or None if invalid index
        """
        if 0 <= band_index < len(self.settings.bands):
            return self.settings.bands[band_index].gain
        return None
    
    def get_band_frequency(self, band_index: int) -> Optional[float]:
        """
        Get frequency for a specific band
        
        Args:
            band_index: Index of the band
            
        Returns:
            Frequency in Hz or None if invalid index
        """
        if 0 <= band_index < len(self.settings.bands):
            return self.settings.bands[band_index].frequency
        return None
    
    def get_num_bands(self) -> int:
        """Get number of equalizer bands"""
        return len(self.settings.bands)
    
    def set_preamp(self, gain: float) -> None:
        """
        Set preamp gain
        
        Args:
            gain: Preamp gain in dB (-20 to +20)
        """
        self.settings.preamp = max(-20.0, min(20.0, gain))
    
    def get_preamp(self) -> float:
        """Get preamp gain"""
        return self.settings.preamp
    
    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the equalizer"""
        self.settings.enabled = enabled
    
    def is_enabled(self) -> bool:
        """Check if equalizer is enabled"""
        return self.settings.enabled
    
    def load_preset(self, preset_name: str) -> bool:
        """
        Load an equalizer preset
        
        Args:
            preset_name: Name of the preset
            
        Returns:
            True if loaded successfully
        """
        if preset_name not in EqualizerSettings.PRESETS:
            return False
        
        preset_bands = EqualizerSettings.PRESETS[preset_name]
        for i, band in enumerate(preset_bands[:self.num_bands]):
            if i < len(self.settings.bands):
                self.settings.bands[i].gain = band.gain
        
        self._create_filters()
        return True
    
    def save_preset(self, preset_name: str) -> bool:
        """
        Save current settings as a preset
        
        Args:
            preset_name: Name for the preset
            
        Returns:
            True if saved successfully
        """
        EqualizerSettings.PRESETS[preset_name] = [
            EQBand(band.frequency, band.gain, band.q_factor) 
            for band in self.settings.bands
        ]
        return True
    
    def get_preset_names(self) -> List[str]:
        """Get all preset names"""
        return list(EqualizerSettings.PRESETS.keys())
    
    def apply(self, audio_data: np.ndarray) -> np.ndarray:
        """
        Apply equalizer to audio data
        
        Args:
            audio_data: Input audio data as numpy array
            
        Returns:
            Processed audio data
        """
        if not self.settings.enabled:
            return audio_data
        
        # Apply preamp
        if self.settings.preamp != 0:
            linear_gain = 10 ** (self.settings.preamp / 20.0)
            audio_data = audio_data * linear_gain
        
        # Apply each band's filter
        # In a real implementation, this would apply the actual filters
        # For now, we'll just apply a simple gain based on the bands
        for band, filter_coeffs in zip(self.settings.bands, self._filters):
            if band.gain != 0:
                # Simplified: apply gain directly (not frequency-specific)
                linear_gain = 10 ** (band.gain / 20.0)
                audio_data = audio_data * linear_gain
        
        # Clip to prevent distortion
        audio_data = np.clip(audio_data, -1.0, 1.0)
        
        return audio_data
    
    def get_settings(self) -> EqualizerSettings:
        """Get current equalizer settings"""
        return self.settings
    
    def set_settings(self, settings: EqualizerSettings) -> None:
        """Set equalizer settings"""
        self.settings = settings
        self._create_filters()
    
    def reset(self) -> None:
        """Reset all bands to 0 gain"""
        for band in self.settings.bands:
            band.gain = 0.0
        self.settings.preamp = 0.0
        self._create_filters()
    
    def get_frequency_response(self, frequencies: List[float]) -> List[float]:
        """
        Get the frequency response of the equalizer
        
        Args:
            frequencies: List of frequencies to evaluate at
            
        Returns:
            List of gain values in dB at each frequency
        """
        # Simplified frequency response calculation
        gains = np.zeros(len(frequencies))
        
        for band in self.settings.bands:
            for i, freq in enumerate(frequencies):
                # Simple approximation: gain at frequency is proportional
                # to how close it is to the band's center frequency
                distance = abs(freq - band.frequency)
                influence = max(0, 1 - distance / (band.frequency * 2))
                gains[i] += band.gain * influence
        
        gains += self.settings.preamp
        return gains.tolist()
