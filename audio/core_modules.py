# 🎹 核心音频模块
# 振荡器、滤波器、包络等

import numpy as np

# ============ 振荡器模块 ============

class Oscillator:
    """基础振荡器 - 生成各种波形"""
    
    def __init__(self, frequency=440.0, wave_type='sine', sample_rate=44100):
        self.frequency = frequency  # 频率 (Hz)
        self.wave_type = wave_type  # 波形类型
        self.sample_rate = sample_rate  # 采样率
        self.phase = 0.0  # 相位
        self.phase_increment = 2 * np.pi * frequency / sample_rate
    
    def set_frequency(self, freq):
        """设置频率"""
        self.frequency = freq
        self.phase_increment = 2 * np.pi * freq / self.sample_rate
    
    def set_wave_type(self, wave_type):
        """设置波形类型: sine, square, sawtooth, triangle"""
        self.wave_type = wave_type
    
    def generate(self, duration=1.0):
        """生成音频样本"""
        num_samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, num_samples, False)
        
        if self.wave_type == 'sine':
            return np.sin(2 * np.pi * self.frequency * t)
        
        elif self.wave_type == 'square':
            return np.where(np.sin(2 * np.pi * self.frequency * t) >= 0, 1.0, -1.0)
        
        elif self.wave_type == 'sawtooth':
            return 2 * (self.frequency * t % 1) - 1
        
        elif self.wave_type == 'triangle':
            return 2 * np.abs(2 * (self.frequency * t % 1)) - 1
        
        else:
            return np.sin(2 * np.pi * self.frequency * t)
    
    def process_sample(self):
        """处理单个样本（用于实时播放）"""
        sample = 0.0
        
        if self.wave_type == 'sine':
            sample = np.sin(self.phase)
        elif self.wave_type == 'square':
            sample = 1.0 if np.sin(self.phase) >= 0 else -1.0
        elif self.wave_type == 'sawtooth':
            sample = 2 * (self.phase / (2 * np.pi)) - 1
        elif self.wave_type == 'triangle':
            sample = 2 * np.abs(self.phase / np.pi - 0.5) - 1
        
        self.phase += self.phase_increment
        if self.phase >= 2 * np.pi:
            self.phase -= 2 * np.pi
        
        return sample


class MultiOscillator:
    """多振荡器组合 - 创造丰富音色"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.oscillators = []
        self.gains = []
    
    def add_oscillator(self, frequency, wave_type, gain=0.5):
        """添加一个振荡器"""
        osc = Oscillator(frequency, wave_type, self.sample_rate)
        self.oscillators.append(osc)
        self.gains.append(gain)
    
    def remove_oscillator(self, index):
        """移除振荡器"""
        if 0 <= index < len(self.oscillators):
            self.oscillators.pop(index)
            self.gains.pop(index)
    
    def set_frequency(self, index, freq):
        """设置某个振荡器的频率"""
        if 0 <= index < len(self.oscillators):
            self.oscillators[index].set_frequency(freq)
    
    def generate(self, duration=1.0):
        """生成混合音频"""
        if not self.oscillators:
            return np.zeros(int(duration * self.sample_rate))
        
        total = np.zeros(int(duration * self.sample_rate))
        for osc, gain in zip(self.oscillators, self.gains):
            total += osc.generate(duration) * gain
        
        # 归一化
        total = total / len(self.oscillators) if len(self.oscillators) > 0 else total
        return total


# ============ 滤波器模块 ============

class Filter:
    """滤波器 - 修改音色"""
    
    def __init__(self, cutoff=1000, filter_type='lowpass', sample_rate=44100):
        self.cutoff = cutoff  # 截止频率 (Hz)
        self.filter_type = filter_type  # 滤波器类型
        self.sample_rate = sample_rate
        self.prev_sample = 0.0
    
    def set_cutoff(self, cutoff):
        """设置截止频率"""
        self.cutoff = cutoff
    
    def set_filter_type(self, filter_type):
        """设置滤波器类型: lowpass, highpass, bandpass"""
        self.filter_type = filter_type
    
    def process(self, audio_data):
        """处理音频数据"""
        # 简单的IIR滤波器实现
        # 实际项目中应该用更复杂的算法
        
        # 计算滤波器系数（简化版）
        omega = 2 * np.pi * self.cutoff / self.sample_rate
        alpha = np.sin(omega) / 2
        cos_omega = np.cos(omega)
        
        if self.filter_type == 'lowpass':
            a0 = 1 + alpha
            b0 = (1 - cos_omega) / 2 / a0
            b1 = (1 - cos_omega) / a0
            b2 = (1 - cos_omega) / 2 / a0
            a1 = -2 * cos_omega / a0
            a2 = (1 - alpha) / a0
        
        elif self.filter_type == 'highpass':
            a0 = 1 + alpha
            b0 = (1 + cos_omega) / 2 / a0
            b1 = -(1 + cos_omega) / a0
            b2 = (1 + cos_omega) / 2 / a0
            a1 = -2 * cos_omega / a0
            a2 = (1 - alpha) / a0
        
        else:  # bandpass
            a0 = 1 + alpha
            b0 = alpha / a0
            b1 = 0 / a0
            b2 = -alpha / a0
            a1 = -2 * cos_omega / a0
            a2 = (1 - alpha) / a0
        
        # 应用滤波器
        filtered = np.zeros_like(audio_data)
        x1, x2 = 0, 0
        y1, y2 = 0, 0
        
        for n in range(len(audio_data)):
            x = audio_data[n]
            y = b0 * x + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
            filtered[n] = y
            x2, x1 = x1, x
            y2, y1 = y1, y
        
        return filtered


# ============ 包络模块 ============

class Envelope:
    """ADSR包络 - 控制声音的动态变化"""
    
    def __init__(self, attack=0.1, decay=0.2, sustain=0.7, release=0.3, sample_rate=44100):
        self.attack = attack    # attack时间（秒）
        self.decay = decay      # decay时间（秒）
        self.sustain = sustain  # sustain电平（0-1）
        self.release = release  # release时间（秒）
        self.sample_rate = sample_rate
        
        self.state = 'idle'  # idle, attack, decay, sustain, release
        self.current_level = 0.0
        self.elapsed = 0.0
    
    def set_parameters(self, attack=None, decay=None, sustain=None, release=None):
        """设置包络参数"""
        if attack is not None:
            self.attack = attack
        if decay is not None:
            self.decay = decay
        if sustain is not None:
            self.sustain = sustain
        if release is not None:
            self.release = release
    
    def trigger(self):
        """触发包络（按下按键）"""
        self.state = 'attack'
        self.elapsed = 0.0
        self.current_level = 0.0
    
    def release_envelope(self):
        """释放包络（松开按键）"""
        if self.state != 'idle':
            self.state = 'release'
            self.elapsed = 0.0
    
    def process(self, num_samples):
        """处理样本，返回增益值"""
        gain = np.zeros(num_samples)
        
        attack_samples = int(self.attack * self.sample_rate)
        decay_samples = int(self.decay * self.sample_rate)
        release_samples = int(self.release * self.sample_rate)
        
        for i in range(num_samples):
            if self.state == 'attack':
                progress = self.elapsed / self.attack if self.attack > 0 else 1
                self.current_level = progress
                
                if self.elapsed >= self.attack:
                    self.state = 'decay'
                    self.elapsed = 0
            
            elif self.state == 'decay':
                progress = self.elapsed / self.decay if self.decay > 0 else 1
                self.current_level = 1.0 - (1.0 - self.sustain) * progress
                
                if self.elapsed >= self.decay:
                    self.state = 'sustain'
                    self.elapsed = 0
            
            elif self.state == 'sustain':
                self.current_level = self.sustain
            
            elif self.state == 'release':
                progress = self.elapsed / self.release if self.release > 0 else 1
                self.current_level = self.sustain * (1.0 - progress)
                
                if self.elapsed >= self.release:
                    self.state = 'idle'
                    self.current_level = 0
            
            gain[i] = self.current_level
            self.elapsed += 1.0 / self.sample_rate
        
        return gain


# ============ LFO模块 ============

class LFO:
    """低频振荡器 - 调制其他参数"""
    
    def __init__(self, frequency=1.0, wave_type='sine', sample_rate=44100):
        self.frequency = frequency  # 频率 (Hz)
        self.wave_type = wave_type  # 波形类型
        self.sample_rate = sample_rate
        self.phase = 0.0
        self.phase_increment = 2 * np.pi * frequency / sample_rate
    
    def set_frequency(self, freq):
        """设置频率"""
        self.frequency = freq
        self.phase_increment = 2 * np.pi * freq / self.sample_rate
    
    def set_wave_type(self, wave_type):
        """设置波形: sine, square, sawtooth, triangle"""
        self.wave_type = wave_type
    
    def generate(self, duration=1.0):
        """生成LFO信号"""
        t = np.linspace(0, duration, int(duration * self.sample_rate), False)
        
        if self.wave_type == 'sine':
            return np.sin(2 * np.pi * self.frequency * t)
        
        elif self.wave_type == 'square':
            return np.where(np.sin(2 * np.pi * self.frequency * t) >= 0, 1.0, -1.0)
        
        elif self.wave_type == 'sawtooth':
            return 2 * (self.frequency * t % 1) - 1
        
        elif self.wave_type == 'triangle':
            return 2 * np.abs(2 * (self.frequency * t % 1)) - 1
        
        return np.sin(2 * np.pi * self.frequency * t)
    
    def get_value(self):
        """获取当前值（用于实时调制）"""
        value = 0.0
        
        if self.wave_type == 'sine':
            value = np.sin(self.phase)
        elif self.wave_type == 'square':
            value = 1.0 if np.sin(self.phase) >= 0 else -1.0
        elif self.wave_type == 'sawtooth':
            value = 2 * (self.phase / (2 * np.pi)) - 1
        elif self.wave_type == 'triangle':
            value = 2 * np.abs(self.phase / np.pi - 0.5) - 1
        
        self.phase += self.phase_increment
        if self.phase >= 2 * np.pi:
            self.phase -= 2 * np.pi
        
        return value


# ============ 效果器模块 ============

class Reverb:
    """混响效果"""
    
    def __init__(self, room_size=0.5, damping=0.5, sample_rate=44100):
        self.room_size = room_size  # 房间大小
        self.damping = damping      # 阻尼
        self.sample_rate = sample_rate
        self.delay_buffer = np.zeros(int(0.1 * sample_rate))  # 100ms延迟线
        self.write_index = 0
    
    def process(self, audio_data):
        """处理混响"""
        output = np.zeros_like(audio_data)
        
        for i in range(len(audio_data)):
            # 读延迟
            read_index = (self.write_index - int(self.room_size * 0.1 * self.sample_rate)) % len(self.delay_buffer)
            delayed = self.delay_buffer[read_index]
            
            # 混合
            output[i] = audio_data[i] * 0.5 + delayed * 0.5 * (1 - self.damping)
            
            # 写入延迟线
            self.delay_buffer[self.write_index] = audio[i] + delayed * self.room_size * 0.5
            self.write_index = (self.write_index + 1) % len(self.delay_buffer)
        
        return output


class Delay:
    """延迟效果"""
    
    def __init__(self, delay_time=0.5, feedback=0.4, sample_rate=44100):
        self.delay_time = delay_time  # 延迟时间（秒）
        self.feedback = feedback      # 反馈量
        self.sample_rate = sample_rate
        self.delay_buffer = np.zeros(int(delay_time * sample_rate))
        self.write_index = 0
    
    def process(self, audio_data):
        """处理延迟"""
        output = np.zeros_like(audio_data)
        delay_samples = int(self.delay_time * self.sample_rate)
        
        for i in range(len(audio_data)):
            # 读延迟
            read_index = (self.write_index - delay_samples) % len(self.delay_buffer)
            delayed = self.delay_buffer[read_index]
            
            # 混合
            output[i] = audio_data[i] + delayed * self.feedback
            
            # 写入
            self.delay_buffer[self.write_index] = output[i]
            self.write_index = (self.write_index + 1) % len(self.delay_buffer)
        
        return output


# ============ 工具函数 ============

def mix_signals(signals, volumes=None):
    """混合多个信号"""
    if volumes is None:
        volumes = [1.0] * len(signals)
    
    max_len = max(len(s) for s in signals)
    mixed = np.zeros(max_len)
    
    for signal, vol in zip(signals, volumes):
        if len(signal) < max_len:
            signal = np.pad(signal, (0, max_len - len(signal)))
        mixed += signal * vol
    
    # 归一化
    if np.max(np.abs(mixed)) > 0:
        mixed = mixed / np.max(np.abs(mixed))
    
    return mixed


def apply_gain(audio_data, gain):
    """应用增益"""
    return audio_data * gain


def normalize(audio_data):
    """归一化音频"""
    max_val = np.max(np.abs(audio_data))
    if max_val > 0:
        return audio_data / max_val
    return audio_data
