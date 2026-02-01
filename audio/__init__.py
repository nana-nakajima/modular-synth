# 🎹 Modular Synth Studio
# Nana的虚拟模块合成器项目

__version__ = "0.1.0"
__author__ = "Nana Nakajima"

from .core_modules import (
    Oscillator,
    MultiOscillator,
    Filter,
    Envelope,
    LFO,
    Reverb,
    Delay,
)

__all__ = [
    'Oscillator',
    'MultiOscillator', 
    'Filter',
    'Envelope',
    'LFO',
    'Reverb',
    'Delay',
]
