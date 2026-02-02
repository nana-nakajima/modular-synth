"""
音效增强模块 v0.7.0
添加相位器、滤波器共振、环形调制等效果
"""

import math
import numpy as np
from typing import Optional, List, Tuple
from dataclasses import dataclass


@dataclass
class PhaserParams:
    """相位器参数"""
    rate: float = 0.5  # LFO速率 (Hz)
    depth: float = 0.5  # 深度 (0-1)
    stages: int = 4  # 级数
    mix: float = 0.5  # 干湿比 (0-1)
    feedback: float = 0.3  # 反馈量 (0-1)


@dataclass
class RingModParams:
    """环形调制参数"""
    frequency: float = 440.0  # 调制频率 (Hz)
    mix: float = 0.5  # 干湿比 (0-1)


@dataclass
class BitcrusherParams:
    """比特粉碎参数"""
    bits: int = 8  # 比特深度 (4-16)
    mix: float = 0.5  # 干湿比 (0-1)


@dataclass
class WavefolderParams:
    """波形折叠参数"""
    drive: float = 1.0  # 驱动量 (1-4)
    mix: float = 0.5  # 干湿比 (0-1)


class Phaser:
    """相位器效果器"""
    
    def __init__(self, sample_rate: float = 44100.0):
        self.sample_rate = sample_rate
        self.params = PhaserParams()
        self.reset()
    
    def reset(self):
        """重置状态"""
        self.lfo_phase = 0.0
        self.delay_lines: List[List[float]] = []
        for _ in range(self.params.stages):
            self.delay_lines.append([0.0] * 1024)
        self.delay_index = 0
    
    def set_params(self, **kwargs):
        """设置参数"""
        for key, value in kwargs.items():
            if hasattr(self.params, key):
                setattr(self.params, key, value)
    
    def process(self, samples: np.ndarray) -> np.ndarray:
        """处理音频"""
        if len(samples) == 0:
            return samples
        
        # 更新LFO
        lfo_freq = self.params.rate / self.sample_rate
        self.lfo_phase = (self.lfo_phase + lfo_freq) % 1.0
        
        # 计算当前滤波器频率
        min_freq = 200.0
        max_freq = 4000.0
        lfo_value = (math.sin(2 * math.pi * self.lfo_phase) + 1) / 2
        current_freq = min_freq + lfo_value * (max_freq - min_freq)
        
        # 计算延迟样本数
        delay_samples = self.sample_rate / (2 * math.pi * current_freq)
        delay_samples = max(1, min(100, int(delay_samples)))
        
        output = np.zeros_like(samples)
        
        for i in range(len(samples)):
            sample = samples[i]
            
            # 多级相位处理
            for stage in range(self.params.stages):
                delay_line = self.delay_lines[stage]
                
                # 写入延迟线
                delay_line[self.delay_index] = sample
                
                # 读取延迟样本
                read_index = (self.delay_index - delay_samples + len(delay_line)) % len(delay_line)
                delayed = delay_line[read_index]
                
                # Allpass滤波
                alpha = (1 - current_freq / (self.sample_rate / 2)) / (1 + current_freq / (self.sample_rate / 2))
                sample = delayed + alpha * (sample - delayed)
                
                # 反馈
                if stage == self.params.stages - 1:
                    sample = sample * self.params.feedback + delayed * (1 - self.params.feedback)
            
            # 更新索引
            self.delay_index = (self.delay_index + 1) % len(self.delay_lines[0])
            
            # 混合
            output[i] = samples[i] * (1 - self.params.mix) + sample * self.params.mix
        
        return output


class RingModulator:
    """环形调制器"""
    
    def __init__(self, sample_rate: float = 44100.0):
        self.sample_rate = sample_rate
        self.params = RingModParams()
        self.reset()
    
    def reset(self):
        """重置状态"""
        self.phase = 0.0
        self.carrier_phase = 0.0
    
    def set_params(self, **kwargs):
        """设置参数"""
        for key, value in kwargs.items():
            if hasattr(self.params, key):
                setattr(self.params, key, value)
    
    def process(self, samples: np.ndarray) -> np.ndarray:
        """处理音频"""
        if len(samples) == 0:
            return samples
        
        # 更新载波相位
        carrier_freq = self.params.frequency / self.sample_rate
        self.carrier_phase = (self.carrier_phase + carrier_freq) % (2 * math.pi)
        
        # 生成载波
        carrier = np.sin(self.carrier_phase)
        
        # 环形调制
        modulated = samples * carrier
        
        # 混合
        output = samples * (1 - self.params.mix) + modulated * self.params.mix * 2
        
        return output


class Bitcrusher:
    """比特粉碎器"""
    
    def __init__(self, sample_rate: float = 44100.0):
        self.sample_rate = sample_rate
        self.params = BitcrusherParams()
        self.reset()
    
    def reset(self):
        """重置状态"""
        self.last_sample = 0.0
    
    def set_params(self, **kwargs):
        """设置参数"""
        for key, value in kwargs.items():
            if hasattr(self.params, key):
                setattr(self.params, key, value)
    
    def process(self, samples: np.ndarray) -> np.ndarray:
        """处理音频"""
        if len(samples) == 0:
            return samples
        
        # 量化步长
        if self.params.bits >= 16:
            step = 1.0
        else:
            step = 2.0 / (2 ** self.params.bits)
        
        # 量化
        crushed = np.round(samples / step) * step
        
        # 限制范围
        crushed = np.clip(crushed, -1.0, 1.0)
        
        # 混合
        output = samples * (1 - self.params.mix) + crushed * self.params.mix
        
        return output


class Wavefolder:
    """波形折叠效果器"""
    
    def __init__(self, sample_rate: float = 44100.0):
        self.sample_rate = sample_rate
        self.params = WavefolderParams()
        self.reset()
    
    def reset(self):
        """重置状态"""
        self.last_sample = 0.0
    
    def set_params(self, **kwargs):
        """设置参数"""
        for key, value in kwargs.items():
            if hasattr(self.params, key):
                setattr(self.params, key, value)
    
    def fold(self, x: float) -> float:
        """波形折叠函数"""
        drive = self.params.drive
        x = x * drive
        
        # 多次折叠
        for _ in range(4):
            if x > 1:
                x = 2 - x
            elif x < -1:
                x = -2 - x
        
        return x / drive
    
    def process(self, samples: np.ndarray) -> np.ndarray:
        """处理音频"""
        if len(samples) == 0:
            return samples
        
        # 折叠处理
        folded = np.array([self.fold(s) for s in samples])
        
        # 混合
        output = samples * (1 - self.params.mix) + folded * self.params.mix
        
        return output


class FilterResonance:
    """滤波器共振增强器"""
    
    def __init__(self, sample_rate: float = 44100.0):
        self.sample_rate = sample_rate
        self.reset()
    
    def reset(self):
        """重置状态"""
        self.low_pass = 0.0
        self.high_pass = 0.0
        self.resonance_boost = 0.0
    
    def enhance(self, samples: np.ndarray, 
                cutoff: float, 
                resonance: float,
                filter_type: str = "lowpass") -> np.ndarray:
        """增强滤波器共振"""
        if len(samples) == 0:
            return samples
        
        # 计算滤波器系数
        omega = 2 * math.pi * cutoff / self.sample_rate
        alpha = math.sin(omega) / 2
        
        if filter_type == "lowpass":
            a0 = 1 + alpha
            b0 = (1 - math.cos(omega)) / 2 / a0
            b1 = (1 - math.cos(omega)) / a0
            b2 = (1 - math.cos(omega)) / 2 / a0
            a1 = -2 * math.cos(omega) / a0
            a2 = (1 + alpha) / a0
        elif filter_type == "highpass":
            a0 = 1 + alpha
            b0 = (1 + math.cos(omega)) / 2 / a0
            b1 = -(1 + math.cos(omega)) / a0
            b2 = (1 + math.cos(omega)) / 2 / a0
            a1 = -2 * math.cos(omega) / a0
            a2 = (1 + alpha) / a0
        else:
            return samples
        
        # 共振增强
        resonance_boost = 1 + resonance * 2
        
        # 应用滤波器
        output = np.zeros_like(samples)
        x1, x2 = 0, 0
        y1, y2 = 0, 0
        
        for i in range(len(samples)):
            x = samples[i]
            y = b0 * x + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
            
            # 应用共振增强
            y = y * resonance_boost
            
            x2, x1 = x1, x
            y2, y1 = y1, y
            output[i] = y
        
        return output


class EnhancedEffectChain:
    """增强版效果链 v0.7.0"""
    
    def __init__(self, sample_rate: float = 44100.0):
        self.sample_rate = sample_rate
        
        # 效果器实例
        self.phaser = Phaser(sample_rate)
        self.ring_mod = RingModulator(sample_rate)
        self.bitcrusher = Bitcrusher(sample_rate)
        self.wavefolder = Wavefolder(sample_rate)
        self.filter_resonance = FilterResonance(sample_rate)
        
        # 效果器启用状态
        self.enabled = {
            'phaser': False,
            'ring_mod': False,
            'bitcrusher': False,
            'wavefolder': False,
            'filter_resonance': False
        }
    
    def set_effect_enabled(self, effect_name: str, enabled: bool):
        """设置效果器启用状态"""
        if effect_name in self.enabled:
            self.enabled[effect_name] = enabled
    
    def process(self, samples: np.ndarray, 
                cutoff: float = 1000.0,
                resonance: float = 0.0,
                filter_type: str = "lowpass") -> np.ndarray:
        """处理音频"""
        output = samples.copy()
        
        # 依次应用效果
        if self.enabled.get('phaser', False):
            output = self.phaser.process(output)
        
        if self.enabled.get('ring_mod', False):
            output = self.ring_mod.process(output)
        
        if self.enabled.get('bitcrusher', False):
            output = self.bitcrusher.process(output)
        
        if self.enabled.get('wavefolder', False):
            output = self.wavefolder.process(output)
        
        if self.enabled.get('filter_resonance', False):
            output = self.filter_resonance.enhance(
                output, cutoff, resonance, filter_type
            )
        
        return output
    
    def get_effect_params(self, effect_name: str):
        """获取效果器参数"""
        if effect_name == 'phaser':
            return self.phaser.params
        elif effect_name == 'ring_mod':
            return self.ring_mod.params
        elif effect_name == 'bitcrusher':
            return self.bitcrusher.params
        elif effect_name == 'wavefolder':
            return self.wavefolder.params
        return None
    
    def set_effect_params(self, effect_name: str, **kwargs):
        """设置效果器参数"""
        if effect_name == 'phaser':
            self.phaser.set_params(**kwargs)
        elif effect_name == 'ring_mod':
            self.ring_mod.set_params(**kwargs)
        elif effect_name == 'bitcrusher':
            self.bitcrusher.set_params(**kwargs)
        elif effect_name == 'wavefolder':
            self.wavefolder.set_params(**kwargs)
    
    def reset(self):
        """重置所有效果器"""
        self.phaser.reset()
        self.ring_mod.reset()
        self.bitcrusher.reset()
        self.wavefolder.reset()


# 演示脚本
if __name__ == "__main__":
    print("🎛️ 音效增强模块 v0.7.0")
    print("=" * 40)
    
    # 测试参数
    sample_rate = 44100
    duration = 2.0
    num_samples = int(sample_rate * duration)
    
    # 生成测试信号（正弦波）
    t = np.linspace(0, duration, num_samples, False)
    test_signal = 0.5 * np.sin(2 * np.pi * 440 * t)
    
    # 测试相位器
    print("\n🎚️ 测试相位器...")
    phaser = Phaser(sample_rate)
    phaser.params.rate = 0.3
    phaser.params.depth = 0.7
    phaser.params.stages = 4
    phaser.params.mix = 0.5
    
    output = phaser.process(test_signal)
    print(f"✅ 相位器输出范围: [{output.min():.3f}, {output.max():.3f}]")
    
    # 测试环形调制
    print("\n🎭 测试环形调制器...")
    ring_mod = RingModulator(sample_rate)
    ring_mod.params.frequency = 220.0
    ring_mod.params.mix = 0.5
    
    output = ring_mod.process(test_signal)
    print(f"✅ 环形调制输出范围: [{output.min():.3f}, {output.max():.3f}]")
    
    # 测试比特粉碎
    print("\n🔲 测试比特粉碎器...")
    bitcrusher = Bitcrusher(sample_rate)
    bitcrusher.params.bits = 8
    bitcrusher.params.mix = 0.5
    
    output = bitcrusher.process(test_signal)
    print(f"✅ 比特粉碎输出范围: [{output.min():.3f}, {output.max():.3f}]")
    
    # 测试波形折叠
    print("\n🌀 测试波形折叠器...")
    wavefolder = Wavefolder(sample_rate)
    wavefolder.params.drive = 2.0
    wavefolder.params.mix = 0.5
    
    # 使用更高振幅的信号测试
    loud_signal = 0.8 * np.sin(2 * np.pi * 220 * t)
    output = wavefolder.process(loud_signal)
    print(f"✅ 波形折叠输出范围: [{output.min():.3f}, {output.max():.3f}]")
    
    # 测试增强效果链
    print("\n🔗 测试增强效果链...")
    chain = EnhancedEffectChain(sample_rate)
    chain.set_effect_enabled('phaser', True)
    chain.set_effect_enabled('bitcrusher', True)
    
    output = chain.process(test_signal, cutoff=2000.0, resonance=0.5)
    print(f"✅ 效果链输出范围: [{output.min():.3f}, {output.max():.3f}]")
    
    print("\n🎉 所有效果器测试完成！")
