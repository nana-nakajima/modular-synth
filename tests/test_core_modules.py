#!/usr/bin/env python3
# 🎹 Modular Synth - 测试用例

import sys
import numpy as np
import pytest
sys.path.insert(0, '..')

from audio.core_modules import Oscillator, Filter, Envelope, LFO, MultiOscillator

class TestOscillator:
    """振荡器测试"""
    
    def test_sine_wave(self):
        """测试正弦波生成"""
        osc = Oscillator(frequency=440.0, wave_type='sine')
        audio = osc.generate(duration=0.1)
        
        assert len(audio) == int(0.1 * 44100)
        assert audio.min() >= -1.0
        assert audio.max() <= 1.0
        print("✓ Sine wave test passed")
    
    def test_square_wave(self):
        """测试方波生成"""
        osc = Oscillator(frequency=440.0, wave_type='square')
        audio = osc.generate(duration=0.1)
        
        assert len(audio) == int(0.1 * 44100)
        assert set(np.unique(audio)) == {-1.0, 1.0}
        print("✓ Square wave test passed")
    
    def test_sawtooth_wave(self):
        """测试锯齿波生成"""
        osc = Oscillator(frequency=440.0, wave_type='sawtooth')
        audio = osc.generate(duration=0.1)
        
        assert len(audio) == int(0.1 * 44100)
        assert audio.min() >= -1.0
        assert audio.max() <= 1.0
        print("✓ Sawtooth wave test passed")
    
    def test_triangle_wave(self):
        """测试三角波生成"""
        osc = Oscillator(frequency=440.0, wave_type='triangle')
        audio = osc.generate(duration=0.1)
        
        assert len(audio) == int(0.1 * 44100)
        assert audio.min() >= -1.0
        assert audio.max() <= 1.0
        print("✓ Triangle wave test passed")
    
    def test_frequency_change(self):
        """测试频率改变"""
        osc = Oscillator(frequency=440.0)
        osc.set_frequency(880.0)
        
        assert osc.frequency == 880.0
        assert osc.phase_increment == 2 * np.pi * 880.0 / 44100
        print("✓ Frequency change test passed")


class TestFilter:
    """滤波器测试"""
    
    def test_lowpass_filter(self):
        """测试低通滤波器"""
        osc = Oscillator(frequency=1000.0, wave_type='sawtooth')
        audio = osc.generate(duration=0.1)
        
        filt = Filter(cutoff=500, filter_type='lowpass')
        filtered = filt.process(audio)
        
        assert len(filtered) == len(audio)
        print("✓ Lowpass filter test passed")
    
    def test_highpass_filter(self):
        """测试高通滤波器"""
        osc = Oscillator(frequency=100.0, wave_type='sine')
        audio = osc.generate(duration=0.1)
        
        filt = Filter(cutoff=200, filter_type='highpass')
        filtered = filt.process(audio)
        
        assert len(filtered) == len(audio)
        print("✓ Highpass filter test passed")


class TestEnvelope:
    """包络测试"""
    
    def test_adsr_envelope(self):
        """测试ADSR包络"""
        env = Envelope(attack=0.1, decay=0.2, sustain=0.7, release=0.3)
        
        # 触发包络
        env.trigger()
        gain = env.process(int(1.0 * 44100))
        
        assert len(gain) == 44100
        assert gain[0] == 0.0  # 开始时应该是0
        print("✓ ADSR envelope test passed")
    
    def test_envelope_release(self):
        """测试包络释放"""
        env = Envelope(attack=0.05, decay=0.1, sustain=0.8, release=0.2)
        
        env.trigger()
        # 触发后一部分
        gain1 = env.process(int(0.2 * 44100))
        
        env.release_envelope()
        # 释放
        gain2 = env.process(int(0.3 * 44100))
        
        assert len(gain1) + len(gain2) == int(0.5 * 44100)
        print("✓ Envelope release test passed")


class TestLFO:
    """LFO测试"""
    
    def test_lfo_generation(self):
        """测试LFO生成"""
        lfo = LFO(frequency=1.0, wave_type='sine')
        wave = lfo.generate(duration=1.0)
        
        assert len(wave) == 44100
        assert wave.min() >= -1.0
        assert wave.max() <= 1.0
        print("✓ LFO generation test passed")
    
    def test_lfo_types(self):
        """测试各种LFO波形"""
        for wave_type in ['sine', 'square', 'sawtooth', 'triangle']:
            lfo = LFO(frequency=2.0, wave_type=wave_type)
            wave = lfo.generate(duration=0.5)
            
            assert len(wave) == int(0.5 * 44100)
        
        print("✓ All LFO types test passed")


class TestMultiOscillator:
    """多振荡器测试"""
    
    def test_multi_oscillator(self):
        """测试多振荡器"""
        multi = MultiOscillator()
        multi.add_oscillator(220.0, 'sine', 0.5)
        multi.add_oscillator(440.0, 'square', 0.5)
        
        audio = multi.generate(duration=0.1)
        
        assert len(audio) == int(0.1 * 44100)
        assert len(multi.oscillators) == 2
        print("✓ Multi-oscillator test passed")
    
    def test_remove_oscillator(self):
        """测试移除振荡器"""
        multi = MultiOscillator()
        multi.add_oscillator(220.0, 'sine', 0.5)
        multi.add_oscillator(440.0, 'square', 0.5)
        multi.remove_oscillator(0)
        
        assert len(multi.oscillators) == 1
        print("✓ Remove oscillator test passed")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🎹 Running Modular Synth Tests")
    print("="*60 + "\n")
    
    pytest.main([__file__, '-v'])
    
    print("\n" + "="*60)
    print("✅ All tests passed!")
    print("="*60)


if __name__ == '__main__':
    run_all_tests()
