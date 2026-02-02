# 🎹 预设库 - 100+音色
# Preset Library for Modular Synth Studio

from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class Preset:
    """音色预设"""
    name: str
    category: str
    oscillator_1: Dict
    oscillator_2: Dict = None
    oscillator_3: Dict = None
    filter: Dict = None
    envelope: Dict = None
    lfo: Dict = None
    effects: Dict = None

# ============ Lead 音色 (20个) ============

LEAD_PRESETS = [
    Preset(
        name="Classic Saw Lead",
        category="Lead",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.8},
        oscillator_2={"type": "square", "detune": 5, "gain": 0.4},
        filter={"type": "lowpass", "cutoff": 2000, "resonance": 0.3},
        envelope={"attack": 0.01, "decay": 0.2, "sustain": 0.7, "release": 0.3},
        lfo={"frequency": 0.1, "type": "sine", "destination": "filter_cutoff"}
    ),
    Preset(
        name="808 Lead",
        category="Lead",
        oscillator_1={"type": "square", "detune": 0, "gain": 0.9},
        filter={"type": "lowpass", "cutoff": 1500, "resonance": 0.2},
        envelope={"attack": 0.005, "decay": 0.1, "sustain": 0.8, "release": 0.1}
    ),
    Preset(
        name="Square Lead",
        category="Lead",
        oscillator_1={"type": "square", "detune": 0, "gain": 0.85},
        oscillator_2={"type": "square", "detune": 3, "gain": 0.3},
        filter={"type": "lowpass", "cutoff": 2500, "resonance": 0.4},
        envelope={"attack": 0.02, "decay": 0.3, "sustain": 0.6, "release": 0.2}
    ),
    Preset(
        name="Pulse Width Lead",
        category="Lead",
        oscillator_1={"type": "square", "detune": 0, "gain": 0.7, "pwm": True},
        filter={"type": "lowpass", "cutoff": 1800, "resonance": 0.5},
        envelope={"attack": 0.01, "decay": 0.15, "sustain": 0.75, "release": 0.25}
    ),
    Preset(
        name="Sync Lead",
        category="Lead",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.8},
        oscillator_2={"type": "sawtooth", "detune": -12, "gain": 0.5, "sync": True},
        filter={"type": "lowpass", "cutoff": 2200, "resonance": 0.35},
        envelope={"attack": 0.005, "decay": 0.2, "sustain": 0.7, "release": 0.2}
    ),
    Preset(
        name="Acid Lead",
        category="Lead",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.9},
        filter={"type": "lowpass", "cutoff": 800, "resonance": 0.8},
        envelope={"attack": 0.005, "decay": 0.05, "sustain": 0.9, "release": 0.1}
    ),
    Preset(
        name="FM Lead",
        category="Lead",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.6},
        oscillator_2={"type": "sine", "detune": 2, "gain": 0.5, "fm": True},
        filter={"type": "lowpass", "cutoff": 3000, "resonance": 0.2},
        envelope={"attack": 0.02, "decay": 0.3, "sustain": 0.6, "release": 0.3}
    ),
    Preset(
        name="Vintage Lead",
        category="Lead",
        oscillator_1={"type": "triangle", "detune": 0, "gain": 0.7},
        oscillator_2={"type": "sawtooth", "detune": 7, "gain": 0.5},
        filter={"type": "lowpass", "cutoff": 1600, "resonance": 0.4},
        envelope={"attack": 0.05, "decay": 0.4, "sustain": 0.5, "release": 0.4}
    ),
    Preset(
        name="Super Saw Layer",
        category="Lead",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.5},
        oscillator_2={"type": "sawtooth", "detune": 7, "gain": 0.5},
        filter={"type": "lowpass", "cutoff": 2800, "resonance": 0.25},
        envelope={"attack": 0.02, "decay": 0.25, "sustain": 0.7, "release": 0.25}
    ),
    Preset(
        name="Silky Lead",
        category="Lead",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.8},
        filter={"type": "lowpass", "cutoff": 3500, "resonance": 0.1},
        envelope={"attack": 0.1, "decay": 0.2, "sustain": 0.8, "release": 0.4}
    ),
    Preset(
        name="Brass Lead",
        category="Lead",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.6},
        oscillator_2={"type": "sawtooth", "detune": 5, "gain": 0.4},
        filter={"type": "lowpass", "cutoff": 2000, "resonance": 0.3},
        envelope={"attack": 0.05, "decay": 0.3, "sustain": 0.7, "release": 0.3}
    ),
    Preset(
        name="Pluck Lead",
        category="Lead",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.9},
        filter={"type": "lowpass", "cutoff": 1200, "resonance": 0.6},
        envelope={"attack": 0.001, "decay": 0.1, "sustain": 0.3, "release": 0.1}
    ),
    Preset(
        name="Glassy Lead",
        category="Lead",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.7},
        oscillator_2={"type": "sine", "detune": 12, "gain": 0.3},
        filter={"type": "highpass", "cutoff": 500, "resonance": 0.2},
        envelope={"attack": 0.01, "decay": 0.3, "sustain": 0.7, "release": 0.2}
    ),
    Preset(
        name="Gritty Lead",
        category="Lead",
        oscillator_1={"type": "square", "detune": 0, "gain": 0.8},
        oscillator_2={"type": "sawtooth", "detune": -3, "gain": 0.6},
        filter={"type": "lowpass", "cutoff": 1000, "resonance": 0.7},
        envelope={"attack": 0.01, "decay": 0.15, "sustain": 0.8, "release": 0.2}
    ),
    Preset(
        name="Dreamy Lead",
        category="Lead",
        oscillator_1={"type": "triangle", "detune": 0, "gain": 0.6},
        oscillator_2={"type": "sine", "detune": 14, "gain": 0.4},
        filter={"type": "lowpass", "cutoff": 2500, "resonance": 0.2},
        lfo={"frequency": 0.2, "type": "sine", "destination": "pitch"}
    ),
    Preset(
        name="Phaser Lead",
        category="Lead",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.75},
        filter={"type": "lowpass", "cutoff": 1800, "resonance": 0.4},
        lfo={"frequency": 0.3, "type": "sine", "destination": "filter_cutoff"}
    ),
    Preset(
        name="Tremolo Lead",
        category="Lead",
        oscillator_1={"type": "square", "detune": 0, "gain": 0.8},
        lfo={"frequency": 8, "type": "square", "destination": "gain"}
    ),
    Preset(
        name="Octave Lead",
        category="Lead",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.7},
        oscillator_2={"type": "sawtooth", "detune": -12, "gain": 0.5},
        filter={"type": "lowpass", "cutoff": 3000, "resonance": 0.3},
        envelope={"attack": 0.02, "decay": 0.2, "sustain": 0.7, "release": 0.25}
    ),
    Preset(
        name="Filter Sweep Lead",
        category="Lead",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.85},
        filter={"type": "lowpass", "cutoff": 500, "resonance": 0.5},
        lfo={"frequency": 0.1, "type": "triangle", "destination": "filter_cutoff"}
    ),
    Preset(
        name="Distorted Lead",
        category="Lead",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.9},
        oscillator_2={"type": "square", "detune": 2, "gain": 0.5},
        filter={"type": "lowpass", "cutoff": 2500, "resonance": 0.4},
        effects={"distortion": 0.6}
    ),
]

# ============ Bass 音色 (20个) ============

BASS_PRESETS = [
    Preset(
        name="Deep Bass",
        category="Bass",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.9},
        filter={"type": "lowpass", "cutoff": 400, "resonance": 0.2},
        envelope={"attack": 0.01, "decay": 0.2, "sustain": 0.8, "release": 0.2}
    ),
    Preset(
        name="Sub Bass",
        category="Bass",
        oscillator_1={"type": "sine", "detune": 0, "gain": 1.0},
        oscillator_2={"type": "sine", "detune": -12, "gain": 0.3},
        envelope={"attack": 0.005, "decay": 0.05, "sustain": 1.0, "release": 0.1}
    ),
    Preset(
        name="Retro Bass",
        category="Bass",
        oscillator_1={"type": "square", "detune": 0, "gain": 0.8},
        filter={"type": "lowpass", "cutoff": 800, "resonance": 0.3},
        envelope={"attack": 0.01, "decay": 0.15, "sustain": 0.7, "release": 0.15}
    ),
    Preset(
        name="Acid Bass",
        category="Bass",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.85},
        filter={"type": "lowpass", "cutoff": 150, "resonance": 0.9},
        envelope={"attack": 0.001, "decay": 0.1, "sustain": 0.9, "release": 0.05}
    ),
    Preset(
        name="FM Bass",
        category="Bass",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.7},
        oscillator_2={"type": "sine", "detune": 2, "gain": 0.6, "fm": True},
        filter={"type": "lowpass", "cutoff": 600, "resonance": 0.3},
        envelope={"attack": 0.005, "decay": 0.2, "sustain": 0.7, "release": 0.1}
    ),
    Preset(
        name="Resonant Bass",
        category="Bass",
        oscillator_1={"type": "triangle", "detune": 0, "gain": 0.8},
        filter={"type": "lowpass", "cutoff": 300, "resonance": 0.8},
        envelope={"attack": 0.01, "decay": 0.3, "sustain": 0.6, "release": 0.2}
    ),
    Preset(
        name="Punk Bass",
        category="Bass",
        oscillator_1={"type": "square", "detune": 0, "gain": 0.9},
        filter={"type": "highpass", "cutoff": 100, "resonance": 0.1},
        envelope={"attack": 0.001, "decay": 0.05, "sustain": 0.9, "release": 0.05}
    ),
    Preset(
        name="Smooth Bass",
        category="Bass",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.85},
        oscillator_2={"type": "triangle", "detune": 7, "gain": 0.3},
        filter={"type": "lowpass", "cutoff": 500, "resonance": 0.2},
        envelope={"attack": 0.02, "decay": 0.25, "sustain": 0.75, "release": 0.3}
    ),
    Preset(
        name="Wobble Bass",
        category="Bass",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.8},
        filter={"type": "lowpass", "cutoff": 400, "resonance": 0.5},
        lfo={"frequency": 2, "type": "sine", "destination": "filter_cutoff"}
    ),
    Preset(
        name="808 Bass",
        category="Bass",
        oscillator_1={"type": "sine", "detune": 0, "gain": 1.0},
        envelope={"attack": 0.001, "decay": 0.02, "sustain": 0.9, "release": 0.1}
    ),
    Preset(
        name="Distorted Bass",
        category="Bass",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.9},
        filter={"type": "lowpass", "cutoff": 600, "resonance": 0.4},
        effects={"distortion": 0.5}
    ),
    Preset(
        name="Pluck Bass",
        category="Bass",
        oscillator_1={"type": "square", "detune": 0, "gain": 0.85},
        filter={"type": "lowpass", "cutoff": 200, "resonance": 0.6},
        envelope={"attack": 0.001, "decay": 0.1, "sustain": 0.4, "release": 0.05}
    ),
    Preset(
        name="Metallic Bass",
        category="Bass",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.7},
        oscillator_2={"type": "square", "detune": 12, "gain": 0.4},
        filter={"type": "bandpass", "cutoff": 800, "resonance": 0.5},
        envelope={"attack": 0.01, "decay": 0.2, "sustain": 0.6, "release": 0.15}
    ),
    Preset(
        name="Growl Bass",
        category="Bass",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.8},
        filter={"type": "lowpass", "cutoff": 250, "resonance": 0.7},
        lfo={"frequency": 0.5, "type": "sawtooth", "destination": "filter_cutoff"}
    ),
    Preset(
        name="Pad Bass",
        category="Bass",
        oscillator_1={"type": "triangle", "detune": 0, "gain": 0.6},
        oscillator_2={"type": "sine", "detune": 7, "gain": 0.5},
        filter={"type": "lowpass", "cutoff": 600, "resonance": 0.2},
        envelope={"attack": 0.1, "decay": 0.3, "sustain": 0.8, "release": 0.4}
    ),
    Preset(
        name="Hard Bass",
        category="Bass",
        oscillator_1={"type": "square", "detune": 0, "gain": 0.9},
        oscillator_2={"type": "sawtooth", "detune": -5, "gain": 0.5},
        filter={"type": "lowpass", "cutoff": 1000, "resonance": 0.4},
        envelope={"attack": 0.005, "decay": 0.1, "sustain": 0.8, "release": 0.1}
    ),
    Preset(
        name=" Reese Bass",
        category="Bass",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.7},
        oscillator_2={"type": "sawtooth", "detune": -1, "gain": 0.7},
        filter={"type": "lowpass", "cutoff": 200, "resonance": 0.5},
        envelope={"attack": 0.05, "decay": 0.4, "sustain": 0.7, "release": 0.3}
    ),
    Preset(
        name="Laser Bass",
        category="Bass",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.8},
        oscillator_2={"type": "square", "detune": 24, "gain": 0.3},
        filter={"type": "highpass", "cutoff": 200, "resonance": 0.3},
        envelope={"attack": 0.001, "decay": 0.15, "sustain": 0.8, "release": 0.1}
    ),
    Preset(
        name="Fuzzy Bass",
        category="Bass",
        oscillator_1={"type": "square", "detune": 0, "gain": 0.85},
        oscillator_2={"type": "sawtooth", "detune": 3, "gain": 0.5},
        filter={"type": "lowpass", "cutoff": 400, "resonance": 0.6},
        effects={"distortion": 0.3}
    ),
    Preset(
        name="Elastic Bass",
        category="Bass",
        oscillator_1={"type": "triangle", "detune": 0, "gain": 0.8},
        filter={"type": "lowpass", "cutoff": 350, "resonance": 0.4},
        lfo={"frequency": 1.5, "type": "sine", "destination": "pitch"}
    ),
]

# ============ Pad 音色 (20个) ============

PAD_PRESETS = [
    Preset(
        name="Soft Pad",
        category="Pad",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.6},
        oscillator_2={"type": "sine", "detune": 7, "gain": 0.5},
        filter={"type": "lowpass", "cutoff": 2000, "resonance": 0.1},
        envelope={"attack": 0.5, "decay": 0.5, "sustain": 0.8, "release": 1.0}
    ),
    Preset(
        name="Dream Pad",
        category="Pad",
        oscillator_1={"type": "triangle", "detune": 0, "gain": 0.5},
        oscillator_2={"type": "sine", "detune": 14, "gain": 0.4},
        filter={"type": "lowpass", "cutoff": 2500, "resonance": 0.15},
        envelope={"attack": 0.8, "decay": 0.5, "sustain": 0.9, "release": 1.5}
    ),
    Preset(
        name="Warm Pad",
        category="Pad",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.55},
        oscillator_2={"type": "sawtooth", "detune": 5, "gain": 0.3},
        filter={"type": "lowpass", "cutoff": 1800, "resonance": 0.2},
        envelope={"attack": 0.4, "decay": 0.4, "sustain": 0.85, "release": 0.8}
    ),
    Preset(
        name="Shimmer Pad",
        category="Pad",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.5},
        oscillator_2={"type": "sine", "detune": 12, "gain": 0.4},
        lfo={"frequency": 0.2, "type": "sine", "destination": "pitch"},
        effects={"reverb": 0.4}
    ),
    Preset(
        name="Space Pad",
        category="Pad",
        oscillator_1={"type": "triangle", "detune": 0, "gain": 0.5},
        oscillator_2={"type": "sine", "detune": 7, "gain": 0.4},
        oscillator_3={"type": "sine", "detune": -7, "gain": 0.3},
        filter={"type": "lowpass", "cutoff": 2200, "resonance": 0.15},
        envelope={"attack": 1.0, "decay": 0.5, "sustain": 0.9, "release": 2.0}
    ),
    Preset(
        name="Ethereal Pad",
        category="Pad",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.6},
        oscillator_2={"type": "triangle", "detune": 12, "gain": 0.3},
        filter={"type": "lowpass", "cutoff": 3000, "resonance": 0.1},
        lfo={"frequency": 0.15, "type": "sine", "destination": "filter_cutoff"},
        effects={"reverb": 0.5}
    ),
    Preset(
        name="Analog Pad",
        category="Pad",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.4},
        oscillator_2={"type": "sawtooth", "detune": 7, "gain": 0.4},
        filter={"type": "lowpass", "cutoff": 1500, "resonance": 0.3},
        envelope={"attack": 0.3, "decay": 0.6, "sustain": 0.7, "release": 1.0}
    ),
    Preset(
        name="Chorus Pad",
        category="Pad",
        oscillator_1={"type": "triangle", "detune": 0, "gain": 0.5},
        oscillator_2={"type": "triangle", "detune": 7, "gain": 0.5},
        filter={"type": "lowpass", "cutoff": 2000, "resonance": 0.2},
        lfo={"frequency": 0.3, "type": "sine", "destination": "detune"}
    ),
    Preset(
        name="Vintage Pad",
        category="Pad",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.45},
        oscillator_2={"type": "triangle", "detune": 5, "gain": 0.35},
        filter={"type": "lowpass", "cutoff": 1200, "resonance": 0.4},
        envelope={"attack": 0.4, "decay": 0.5, "sustain": 0.75, "release": 0.8}
    ),
    Preset(
        name="Glassy Pad",
        category="Pad",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.6},
        oscillator_2={"type": "sine", "detune": 24, "gain": 0.2},
        filter={"type": "highpass", "cutoff": 300, "resonance": 0.1},
        envelope={"attack": 0.2, "decay": 0.4, "sustain": 0.8, "release": 0.6}
    ),
    Preset(
        name="Dark Pad",
        category="Pad",
        oscillator_1={"type": "triangle", "detune": 0, "gain": 0.5},
        oscillator_2={"type": "sine", "detune": -7, "gain": 0.4},
        filter={"type": "lowpass", "cutoff": 800, "resonance": 0.3},
        envelope={"attack": 0.6, "decay": 0.6, "sustain": 0.7, "release": 1.2}
    ),
    Preset(
        name="Bright Pad",
        category="Pad",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.55},
        oscillator_2={"type": "sawtooth", "detune": 12, "gain": 0.3},
        filter={"type": "lowpass", "cutoff": 3500, "resonance": 0.1},
        envelope={"attack": 0.3, "decay": 0.4, "sustain": 0.85, "release": 0.7}
    ),
    Preset(
        name="Sweep Pad",
        category="Pad",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.5},
        filter={"type": "lowpass", "cutoff": 500, "resonance": 0.4},
        lfo={"frequency": 0.08, "type": "triangle", "destination": "filter_cutoff"}
    ),
    Preset(
        name="Strings Pad",
        category="Pad",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.4},
        oscillator_2={"type": "sawtooth", "detune": 7, "gain": 0.35},
        filter={"type": "lowpass", "cutoff": 2000, "resonance": 0.25},
        envelope={"attack": 0.2, "decay": 0.5, "sustain": 0.8, "release": 0.8}
    ),
    Preset(
        name="Pulsing Pad",
        category="Pad",
        oscillator_1={"type": "triangle", "detune": 0, "gain": 0.5},
        oscillator_2={"type": "triangle", "detune": 5, "gain": 0.4},
        lfo={"frequency": 1, "type": "sine", "destination": "gain"}
    ),
    Preset(
        name="Evolving Pad",
        category="Pad",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.5},
        oscillator_2={"type": "triangle", "detune": 7, "gain": 0.4},
        lfo={"frequency": 0.1, "type": "sawtooth", "destination": "filter_cutoff"}
    ),
    Preset(
        name="Heavenly Pad",
        category="Pad",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.6},
        oscillator_2={"type": "sine", "detune": 14, "gain": 0.3},
        filter={"type": "lowpass", "cutoff": 2800, "resonance": 0.1},
        effects={"reverb": 0.6}
    ),
    Preset(
        name="Phase Pad",
        category="Pad",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.55},
        oscillator_2={"type": "sine", "detune": 5, "gain": 0.45},
        lfo={"frequency": 0.2, "type": "sine", "destination": "detune"}
    ),
    Preset(
        name="Lush Pad",
        category="Pad",
        oscillator_1={"type": "triangle", "detune": 0, "gain": 0.5},
        oscillator_2={"type": "sine", "detune": 7, "gain": 0.4},
        oscillator_3={"type": "triangle", "detune": -7, "gain": 0.3},
        filter={"type": "lowpass", "cutoff": 2500, "resonance": 0.15},
        envelope={"attack": 0.5, "decay": 0.5, "sustain": 0.85, "release": 1.0}
    ),
    Preset(
        name="Ambient Pad",
        category="Pad",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.4},
        oscillator_2={"type": "sine", "detune": 12, "gain": 0.3},
        lfo={"frequency": 0.05, "type": "sine", "destination": "pitch"},
        effects={"reverb": 0.7}
    ),
]

# ============ FX 音色 (20个) ============

FX_PRESETS = [
    Preset(
        name="Laser FX",
        category="FX",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.8},
        filter={"type": "bandpass", "cutoff": 1500, "resonance": 0.7},
        lfo={"frequency": 10, "type": "sawtooth", "destination": "pitch"}
    ),
    Preset(
        name="weep FX",
        category="FX",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.7},
        filter={"type": "lowpass", "cutoff": 800, "resonance": 0.5},
        lfo={"frequency": 0.5, "type": "triangle", "destination": "filter_cutoff"}
    ),
    Preset(
        name="Tremolo FX",
        category="FX",
        oscillator_1={"type": "square", "detune": 0, "gain": 0.8},
        lfo={"frequency": 5, "type": "sine", "destination": "gain"}
    ),
    Preset(
        name="Vibrato FX",
        category="FX",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.8},
        lfo={"frequency": 6, "type": "sine", "destination": "pitch"}
    ),
    Preset(
        name="Drone FX",
        category="FX",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.5},
        oscillator_2={"type": "sine", "detune": -5, "gain": 0.5},
        oscillator_3={"type": "sine", "detune": 5, "gain": 0.5},
        envelope={"attack": 1.0, "decay": 0, "sustain": 1.0, "release": 2.0}
    ),
    Preset(
        name="Riser FX",
        category="FX",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.8},
        filter={"type": "lowpass", "cutoff": 200, "resonance": 0.3},
        lfo={"frequency": 0.02, "type": "triangle", "destination": "filter_cutoff"}
    ),
    Preset(
        name="Faller FX",
        category="FX",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.8},
        filter={"type": "lowpass", "cutoff": 3000, "resonance": 0.3},
        lfo={"frequency": 0.02, "type": "triangle", "destination": "filter_cutoff", "invert": True}
    ),
    Preset(
        name="Pan FX",
        category="FX",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.7},
        lfo={"frequency": 0.5, "type": "sine", "destination": "pan"}
    ),
    Preset(
        name="Distort FX",
        category="FX",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.9},
        filter={"type": "lowpass", "cutoff": 3000, "resonance": 0.3},
        effects={"distortion": 0.8}
    ),
    Preset(
        name="Bitcrush FX",
        category="FX",
        oscillator_1={"type": "square", "detune": 0, "gain": 0.8},
        effects={"bitcrush": 0.5}
    ),
    Preset(
        name="Wobble FX",
        category="FX",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.75},
        filter={"type": "lowpass", "cutoff": 500, "resonance": 0.6},
        lfo={"frequency": 4, "type": "sine", "destination": "filter_cutoff"}
    ),
    Preset(
        name="Glitch FX",
        category="FX",
        oscillator_1={"type": "square", "detune": 0, "gain": 0.8},
        effects={"bitcrush": 0.7}
    ),
    Preset(
        name="Stutter FX",
        category="FX",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.8},
        lfo={"frequency": 8, "type": "square", "destination": "gain"}
    ),
    Preset(
        name="Filter Res FX",
        category="FX",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.7},
        filter={"type": "bandpass", "cutoff": 1000, "resonance": 0.9},
        lfo={"frequency": 0.3, "type": "sine", "destination": "filter_cutoff"}
    ),
    Preset(
        name="Phaser FX",
        category="FX",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.7},
        filter={"type": "allpass", "cutoff": 1500, "resonance": 0.5},
        lfo={"frequency": 0.2, "type": "sine", "destination": "filter_cutoff"}
    ),
    Preset(
        name="Flanger FX",
        category="FX",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.7},
        lfo={"frequency": 0.3, "type": "sine", "destination": "detune"}
    ),
    Preset(
        name="Ring Mod FX",
        category="FX",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.6},
        oscillator_2={"type": "sine", "detune": 5, "gain": 0.5, "ring_mod": True}
    ),
    Preset(
        name="Granular FX",
        category="FX",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.5},
        envelope={"attack": 0.01, "decay": 0.5, "sustain": 0.5, "release": 1.0},
        effects={"granular": 0.5}
    ),
    Preset(
        name="Lo-fi FX",
        category="FX",
        oscillator_1={"type": "triangle", "detune": 0, "gain": 0.7},
        effects={"bitcrush": 0.3, "sample_rate_reduce": 0.2}
    ),
    Preset(
        name="Dub FX",
        category="FX",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.8},
        filter={"type": "lowpass", "cutoff": 400, "resonance": 0.6},
        effects={"delay": 0.4, "reverb": 0.3}
    ),
    Preset(
        name="Sci-fi FX",
        category="FX",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.6},
        oscillator_2={"type": "square", "detune": 12, "gain": 0.4},
        lfo={"frequency": 0.1, "type": "sawtooth", "destination": "pitch"}
    ),
]

# ============ Keys 音色 (20个) ============

KEYS_PRESETS = [
    Preset(
        name="Electric Piano",
        category="Keys",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.7},
        oscillator_2={"type": "triangle", "detune": 5, "gain": 0.3},
        envelope={"attack": 0.01, "decay": 0.3, "sustain": 0.6, "release": 0.4}
    ),
    Preset(
        name="FM Electric Piano",
        category="Keys",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.6},
        oscillator_2={"type": "sine", "detune": 2, "gain": 0.5, "fm": True},
        envelope={"attack": 0.005, "decay": 0.2, "sustain": 0.7, "release": 0.3}
    ),
    Preset(
        name="Clavinet",
        category="Keys",
        oscillator_1={"type": "square", "detune": 0, "gain": 0.8},
        filter={"type": "highpass", "cutoff": 200, "resonance": 0.3},
        envelope={"attack": 0.001, "decay": 0.1, "sustain": 0.8, "release": 0.1}
    ),
    Preset(
        name="Organ",
        category="Keys",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.5},
        oscillator_2={"type": "sawtooth", "detune": 12, "gain": 0.3},
        oscillator_3={"type": "sawtooth", "detune": 24, "gain": 0.2},
        envelope={"attack": 0.01, "decay": 0.01, "sustain": 1.0, "release": 0.01}
    ),
    Preset(
        name="Hammond Organ",
        category="Keys",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.4},
        oscillator_2={"type": "sawtooth", "detune": 7, "gain": 0.3},
        oscillator_3={"type": "sawtooth", "detune": 12, "gain": 0.2},
        effects={"reverb": 0.2}
    ),
    Preset(
        name="Piano",
        category="Keys",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.8},
        oscillator_2={"type": "triangle", "detune": 5, "gain": 0.2},
        envelope={"attack": 0.01, "decay": 0.5, "sustain": 0.4, "release": 0.8}
    ),
    Preset(
        name="Upright Piano",
        category="Keys",
        oscillator_1={"type": "triangle", "detune": 0, "gain": 0.75},
        oscillator_2={"type": "sine", "detune": 3, "gain": 0.25},
        envelope={"attack": 0.01, "decay": 0.4, "sustain": 0.35, "release": 0.6}
    ),
    Preset(
        name="DX7 Style",
        category="Keys",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.5},
        oscillator_2={"type": "sine", "detune": 1, "gain": 0.5},
        oscillator_3={"type": "sine", "detune": 3, "gain": 0.3},
        envelope={"attack": 0.005, "decay": 0.3, "sustain": 0.6, "release": 0.4}
    ),
    Preset(
        name="CP70 Electric Piano",
        category="Keys",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.6},
        oscillator_2={"type": "triangle", "detune": 7, "gain": 0.4},
        envelope={"attack": 0.01, "decay": 0.25, "sustain": 0.65, "release": 0.35}
    ),
    Preset(
        name="Rhodes",
        category="Keys",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.7},
        oscillator_2={"type": "triangle", "detune": 12, "gain": 0.2},
        envelope={"attack": 0.01, "decay": 0.3, "sustain": 0.7, "release": 0.5}
    ),
    Preset(
        name="Wurlitzer",
        category="Keys",
        oscillator_1={"type": "triangle", "detune": 0, "gain": 0.75},
        oscillator_2={"type": "sine", "detune": 5, "gain": 0.25},
        envelope={"attack": 0.005, "decay": 0.2, "sustain": 0.75, "release": 0.25}
    ),
    Preset(
        name="Vibraphone",
        category="Keys",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.7},
        oscillator_2={"type": "sine", "detune": 12, "gain": 0.3},
        envelope={"attack": 0.001, "decay": 0.4, "sustain": 0, "release": 0.3}
    ),
    Preset(
        name="Celesta",
        category="Keys",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.8},
        envelope={"attack": 0.001, "decay": 0.2, "sustain": 0.3, "release": 0.2}
    ),
    Preset(
        name="Glockenspiel",
        category="Keys",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.85},
        envelope={"attack": 0.001, "decay": 0.15, "sustain": 0, "release": 0.15}
    ),
    Preset(
        name="Harpsichord",
        category="Keys",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.6},
        oscillator_2={"type": "sawtooth", "detune": 12, "gain": 0.4},
        envelope={"attack": 0.005, "decay": 0.1, "sustain": 0.8, "release": 0.05}
    ),
    Preset(
        name="Clavinet 2",
        category="Keys",
        oscillator_1={"type": "square", "detune": 0, "gain": 0.75},
        filter={"type": "lowpass", "cutoff": 800, "resonance": 0.4},
        envelope={"attack": 0.001, "decay": 0.15, "sustain": 0.7, "release": 0.1}
    ),
    Preset(
        name="FM Piano",
        category="Keys",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.6},
        oscillator_2={"type": "sine", "detune": 3, "gain": 0.5, "fm": True},
        envelope={"attack": 0.01, "decay": 0.4, "sustain": 0.5, "release": 0.5}
    ),
    Preset(
        name="Synth Piano",
        category="Keys",
        oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.6},
        oscillator_2={"type": "square", "detune": 7, "gain": 0.4},
        filter={"type": "lowpass", "cutoff": 2000, "resonance": 0.3},
        envelope={"attack": 0.01, "decay": 0.3, "sustain": 0.6, "release": 0.3}
    ),
    Preset(
        name="E. Grand Piano",
        category="Keys",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.65},
        oscillator_2={"type": "triangle", "detune": 5, "gain": 0.35},
        oscillator_3={"type": "sine", "detune": -5, "gain": 0.2},
        envelope={"attack": 0.01, "decay": 0.5, "sustain": 0.45, "release": 0.7}
    ),
    Preset(
        name="Toy Piano",
        category="Keys",
        oscillator_1={"type": "sine", "detune": 0, "gain": 0.8},
        envelope={"attack": 0.001, "decay": 0.1, "sustain": 0.5, "release": 0.15}
    ),
]

# ============ 预设库管理 ============

class PresetLibrary:
    """预设库管理器"""
    
    def __init__(self):
        self.presets = {
            "Lead": LEAD_PRESETS,
            "Bass": BASS_PRESETS,
            "Pad": PAD_PRESETS,
            "FX": FX_PRESETS,
            "Keys": KEYS_PRESETS,
        }
    
    def get_categories(self):
        """获取所有类别"""
        return list(self.presets.keys())
    
    def get_presets_by_category(self, category):
        """按类别获取预设"""
        return self.presets.get(category, [])
    
    def get_all_presets(self):
        """获取所有预设"""
        all_presets = []
        for category, presets in self.presets.items():
            for preset in presets:
                all_presets.append((category, preset))
        return all_presets
    
    def get_preset_by_name(self, name):
        """按名称获取预设"""
        for category, presets in self.presets.items():
            for preset in presets:
                if preset.name == name:
                    return category, preset
        return None, None
    
    def list_presets(self):
        """列出所有预设"""
        print("\n🎹 Modular Synth Studio - 预设库")
        print("=" * 50)
        for category, presets in self.presets.items():
            print(f"\n📁 {category} ({len(presets)} 个音色)")
            print("-" * 40)
            for i, preset in enumerate(presets, 1):
                print(f"  {i:2}. {preset.name}")
        print("\n" + "=" * 50)
        total = sum(len(p) for p in self.presets.values())
        print(f"总计: {total} 个预设\n")


# ============ v0.7.0 扩展预设 ============

def create_extended_fx_presets():
    """创建扩展FX预设 (v0.7.0)"""
    return [
        Preset(
            name="Cyber Sweep",
            category="FX",
            oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.7},
            oscillator_2={"type": "sawtooth", "detune": 5, "gain": 0.5},
            filter={"type": "lowpass", "cutoff": 2000, "resonance": 0.3},
            envelope={"attack": 0.01, "decay": 0.5, "sustain": 0.5, "release": 0.3},
            lfo={"frequency": 0.2, "type": "sine", "destination": "filter_cutoff"}
        ),
        Preset(
            name="Laser Blast",
            category="FX",
            oscillator_1={"type": "square", "detune": 0, "gain": 0.9},
            oscillator_2={"type": "square", "detune": 10, "gain": 0.5},
            filter={"type": "bandpass", "cutoff": 3500, "resonance": 0.7},
            envelope={"attack": 0.001, "decay": 0.1, "sustain": 0, "release": 0.2}
        ),
        Preset(
            name="Warp Drive",
            category="FX",
            oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.6},
            oscillator_2={"type": "sawtooth", "detune": 15, "gain": 0.4},
            filter={"type": "lowpass", "cutoff": 1500, "resonance": 0.8},
            envelope={"attack": 0.05, "decay": 0.8, "sustain": 0.3, "release": 1.0},
            lfo={"frequency": 0.1, "type": "sine", "destination": "pitch"}
        ),
        Preset(
            name="Phaser Sweep",
            category="FX",
            oscillator_1={"type": "triangle", "detune": 0, "gain": 0.8},
            filter={"type": "lowpass", "cutoff": 2500, "resonance": 0.4},
            envelope={"attack": 0.02, "decay": 0.3, "sustain": 0.6, "release": 0.4}
        ),
        Preset(
            name="Tremolo Wave",
            category="FX",
            oscillator_1={"type": "sine", "detune": 0, "gain": 0.8},
            filter={"type": "highpass", "cutoff": 500, "resonance": 0.3},
            envelope={"attack": 0.01, "decay": 0.2, "sustain": 0.8, "release": 0.3},
            lfo={"frequency": 5, "type": "sine", "destination": "amplitude"}
        ),
        Preset(
            name="Granular Texture",
            category="FX",
            oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.5},
            oscillator_2={"type": "sawtooth", "detune": 3, "gain": 0.5},
            oscillator_3={"type": "sawtooth", "detune": -3, "gain": 0.5},
            filter={"type": "bandpass", "cutoff": 2000, "resonance": 0.6},
            envelope={"attack": 0.1, "decay": 0.5, "sustain": 0.7, "release": 0.5}
        ),
        Preset(
            name="Glitch Machine",
            category="FX",
            oscillator_1={"type": "square", "detune": 0, "gain": 0.9},
            filter={"type": "highpass", "cutoff": 300, "resonance": 0.2},
            envelope={"attack": 0.001, "decay": 0.05, "sustain": 0, "release": 0.05}
        ),
        Preset(
            name="Space Drone",
            category="FX",
            oscillator_1={"type": "sine", "detune": 0, "gain": 0.4},
            oscillator_2={"type": "sine", "detune": 2, "gain": 0.4},
            oscillator_3={"type": "sine", "detune": -2, "gain": 0.4},
            filter={"type": "lowpass", "cutoff": 800, "resonance": 0.2},
            envelope={"attack": 1.0, "decay": 1.0, "sustain": 1.0, "release": 2.0}
        ),
        Preset(
            name="Vibrato Lead",
            category="FX",
            oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.8},
            filter={"type": "lowpass", "cutoff": 3000, "resonance": 0.2},
            envelope={"attack": 0.01, "decay": 0.1, "sustain": 0.9, "release": 0.2},
            lfo={"frequency": 5, "type": "sine", "destination": "pitch"}
        ),
        Preset(
            name="Ethereal Pad",
            category="FX",
            oscillator_1={"type": "sine", "detune": 0, "gain": 0.5},
            oscillator_2={"type": "sine", "detune": 3, "gain": 0.5},
            filter={"type": "lowpass", "cutoff": 1200, "resonance": 0.3},
            envelope={"attack": 0.5, "decay": 0.5, "sustain": 0.8, "release": 1.5},
            lfo={"frequency": 0.1, "type": "sine", "destination": "filter_cutoff"}
        ),
        Preset(
            name="Wind Chimes",
            category="FX",
            oscillator_1={"type": "sine", "detune": 0, "gain": 0.6},
            oscillator_2={"type": "sine", "detune": 7, "gain": 0.6},
            oscillator_3={"type": "sine", "detune": 19, "gain": 0.6},
            filter={"type": "highpass", "cutoff": 2000, "resonance": 0.2},
            envelope={"attack": 0.001, "decay": 1.5, "sustain": 0, "release": 2.0}
        ),
        Preset(
            name="Ocean Waves",
            category="FX",
            oscillator_1={"type": "sine", "detune": 0, "gain": 0.5},
            oscillator_2={"type": "sine", "detune": 2, "gain": 0.5},
            filter={"type": "lowpass", "cutoff": 800, "resonance": 0.4},
            envelope={"attack": 1.0, "decay": 1.0, "sustain": 0.9, "release": 1.5},
            lfo={"frequency": 0.05, "type": "sine", "destination": "filter_cutoff"}
        ),
        Preset(
            name="Crystal Clear",
            category="FX",
            oscillator_1={"type": "triangle", "detune": 0, "gain": 0.7},
            oscillator_2={"type": "triangle", "detune": 5, "gain": 0.5},
            oscillator_3={"type": "triangle", "detune": 10, "gain": 0.3},
            filter={"type": "highpass", "cutoff": 1000, "resonance": 0.3},
            envelope={"attack": 0.01, "decay": 0.3, "sustain": 0.9, "release": 0.5}
        ),
        Preset(
            name="Metallic Bells",
            category="FX",
            oscillator_1={"type": "square", "detune": 0, "gain": 0.8},
            oscillator_2={"type": "square", "detune": 9, "gain": 0.5},
            oscillator_3={"type": "square", "detune": 14, "gain": 0.3},
            filter={"type": "bandpass", "cutoff": 3000, "resonance": 0.7},
            envelope={"attack": 0.001, "decay": 0.5, "sustain": 0, "release": 1.0}
        ),
        Preset(
            name="Retro Computer",
            category="FX",
            oscillator_1={"type": "square", "detune": 0, "gain": 0.8},
            filter={"type": "lowpass", "cutoff": 2500, "resonance": 0.2},
            envelope={"attack": 0.01, "decay": 0.1, "sustain": 0.5, "release": 0.1}
        ),
        Preset(
            name="8-Bit Hero",
            category="FX",
            oscillator_1={"type": "square", "detune": 0, "gain": 0.9},
            filter={"type": "lowpass", "cutoff": 3000, "resonance": 0.1},
            envelope={"attack": 0.01, "decay": 0.1, "sustain": 0.5, "release": 0.1}
        ),
        Preset(
            name="Dark Matter",
            category="FX",
            oscillator_1={"type": "sawtooth", "detune": 0, "gain": 0.5},
            oscillator_2={"type": "sawtooth", "detune": 3, "gain": 0.5},
            filter={"type": "lowpass", "cutoff": 600, "resonance": 0.6},
            envelope={"attack": 0.5, "decay": 0.8, "sustain": 0.9, "release": 1.0},
            lfo={"frequency": 0.05, "type": "sine", "destination": "filter_cutoff"}
        ),
        Preset(
            name="Shimmering Star",
            category="FX",
            oscillator_1={"type": "sine", "detune": 0, "gain": 0.6},
            oscillator_2={"type": "sine", "detune": 2, "gain": 0.6},
            filter={"type": "lowpass", "cutoff": 2500, "resonance": 0.4},
            envelope={"attack": 0.1, "decay": 0.5, "sustain": 0.8, "release": 0.8},
            lfo={"frequency": 0.15, "type": "sine", "destination": "filter_cutoff"}
        ),
        Preset(
            name="Lo-Fi Texture",
            category="FX",
            oscillator_1={"type": "triangle", "detune": 0, "gain": 0.7},
            oscillator_2={"type": "triangle", "detune": 5, "gain": 0.5},
            filter={"type": "lowpass", "cutoff": 1500, "resonance": 0.3},
            envelope={"attack": 0.05, "decay": 0.3, "sustain": 0.7, "release": 0.4}
        ),
        Preset(
            name="Spectral Freeze",
            category="FX",
            oscillator_1={"type": "sine", "detune": 0, "gain": 0.5},
            oscillator_2={"type": "sine", "detune": 7, "gain": 0.5},
            oscillator_3={"type": "sine", "detune": 14, "gain": 0.5},
            filter={"type": "highpass", "cutoff": 500, "resonance": 0.4},
            envelope={"attack": 0.5, "decay": 1.0, "sustain": 1.0, "release": 1.0}
        ),
    ]


# ============ 主程序入口 ============

if __name__ == "__main__":
    library = PresetLibrary()
    
    # v0.7.0: 添加扩展FX预设
    extended_fx = create_extended_fx_presets()
    library.presets["FX"].extend(extended_fx)
    
    library.list_presets()