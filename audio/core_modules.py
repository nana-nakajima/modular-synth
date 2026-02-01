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
            self.delay_buffer[self.write_index] = audio_data[i] + delayed * self.room_size * 0.5
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


# ============ 失真效果器 ============

class Distortion:
    """失真效果 - 饱和与过载"""
    
    def __init__(self, drive=0.5, tone=0.5, sample_rate=44100):
        self.drive = drive      # 驱动量 (0-1)
        self.tone = tone        # 音色控制
        self.sample_rate = sample_rate
    
    def set_drive(self, drive):
        """设置驱动量"""
        self.drive = max(0, min(1, drive))
    
    def set_tone(self, tone):
        """设置音色"""
        self.tone = max(0, min(1, tone))
    
    def process(self, audio_data):
        """处理失真 - 使用软clipping"""
        # 应用驱动增益
        gain = 1.0 + self.drive * 10
        processed = audio_data * gain
        
        # 软clipping曲线
        k = self.drive * 20  # 失真强度
        processed = np.tanh(processed * k) / np.tanh(k)
        
        # 简单的音色滤波
        if self.tone < 0.5:
            # 更亮
            pass  # 不做额外处理
        else:
            # 更暗 - 简单的低通
            alpha = 0.1
            filtered = np.zeros_like(processed)
            prev = 0
            for i in range(len(processed)):
                filtered[i] = alpha * processed[i] + (1 - alpha) * prev
                prev = filtered[i]
            processed = filtered
        
        return processed


# ============ 效果器链 ============

class EffectChain:
    """效果器链 - 串联多个效果器"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.effects = []  # [(effect_name, effect_instance), ...]
    
    def add_effect(self, effect_name, effect_instance):
        """添加效果器到链"""
        self.effects.append((effect_name, effect_instance))
    
    def remove_effect(self, effect_name):
        """从链中移除效果器"""
        self.effects = [(name, eff) for name, eff in self.effects if name != effect_name]
    
    def process(self, audio_data):
        """依次处理所有效果器"""
        processed = audio_data
        for name, effect in self.effects:
            if hasattr(effect, 'process'):
                processed = effect.process(processed)
        return processed
    
    def get_params(self):
        """获取所有效果器参数"""
        params = {}
        for name, effect in self.effects:
            if hasattr(effect, '__dict__'):
                params[name] = effect.__dict__.copy()
        return params
    
    def set_param(self, effect_name, param_name, value):
        """设置某个效果器的参数"""
        for name, effect in self.effects:
            if name == effect_name and hasattr(effect, param_name):
                setter = f'set_{param_name}'
                if hasattr(effect, setter):
                    getattr(effect, setter)(value)
                    return True
                elif hasattr(effect, param_name):
                    setattr(effect, param_name, value)
                    return True
        return False


# ============ LFO自动化控制 ============

class LFOModulator:
    """LFO自动化控制器 - 将LFO连接到参数调制"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.modulations = []  # [(target, lfo, param_name, depth), ...]
    
    def add_modulation(self, target_obj, lfo, param_name, depth=0.5):
        """
        添加调制连接
        
        Args:
            target_obj: 目标对象 (Oscillator, Filter等)
            lfo: LFO实例
            param_name: 要调制的参数名
            depth: 调制深度 (0-1)
        """
        self.modulations.append({
            'target': target_obj,
            'lfo': lfo,
            'param_name': param_name,
            'depth': depth,
            'base_value': None
        })
    
    def start(self):
        """开始调制 - 记录基础值"""
        for mod in self.modulations:
            if hasattr(mod['target'], mod['param_name']):
                mod['base_value'] = getattr(mod['target'], mod['param_name'])
    
    def process(self, num_samples):
        """处理调制"""
        if not self.modulations:
            return
        
        for mod in self.modulations:
            target = mod['target']
            lfo = mod['lfo']
            param = mod['param_name']
            depth = mod['depth']
            base = mod['base_value']
            
            if base is None:
                continue
            
            # 获取LFO值
            lfo_value = lfo.get_value()
            
            # 计算调制值
            if param == 'frequency':
                # 频率调制 (以base_value为基准)
                mod_amount = base * depth * 0.5 * lfo_value
                new_value = base + mod_amount
                if hasattr(target, 'set_frequency'):
                    target.set_frequency(max(20, min(20000, new_value)))
            
            elif param == 'cutoff':
                # 滤波器截止频率调制
                mod_amount = 5000 * depth * lfo_value
                new_value = base + mod_amount
                if hasattr(target, 'set_cutoff'):
                    target.set_cutoff(max(20, min(20000, new_value)))
            
            elif param == 'gain':
                # 增益调制
                mod_amount = 0.5 * depth * lfo_value
                new_value = base + mod_amount
                if hasattr(target, 'gain'):
                    target.gain = max(0, min(1, new_value))
    
    def remove_modulation(self, index):
        """移除调制连接"""
        if 0 <= index < len(self.modulations):
            self.modulations.pop(index)


class AutomationManager:
    """自动化管理器 - 高级自动化控制"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.lfo_modulator = LFOModulator(sample_rate)
        self.automation_lanes = []  # [(target, param, automation_data, loop), ...]
        self.recorded_events = []  # 录制的自动化事件
    
    def create_lfo_modulation(self, target, lfo, param, depth=0.5):
        """创建LFO调制"""
        self.lfo_modulator.add_modulation(target, lfo, param, depth)
        return len(self.lfo_modulator.modulations) - 1
    
    def record_parameter_change(self, target, param_name, time, value):
        """记录参数变化事件"""
        self.recorded_events.append({
            'target': target,
            'param': param_name,
            'time': time,
            'value': value
        })
    
    def create_automation_lane(self, target, param_name, data_points, loop=False):
        """
        创建自动化轨道
        
        Args:
            target: 目标对象
            param_name: 参数名
            data_points: [(time, value), ...]
            loop: 是否循环
        """
        self.automation_lanes.append({
            'target': target,
            'param': param_name,
            'data': sorted(data_points, key=lambda x: x[0]),
            'loop': loop,
            'current_index': 0
        })
    
    def process_automation(self, current_time, num_samples):
        """处理自动化"""
        # 处理录制的自动化
        for event in self.recorded_events:
            if event['time'] <= current_time:
                if hasattr(event['target'], event['param']):
                    setter = f'set_{event["param"]}'
                    if hasattr(event['target'], setter):
                        getattr(event['target'], setter)(event['value'])
                self.recorded_events.remove(event)
        
        # 处理自动化轨道
        for lane in self.automation_lanes:
            if not lane['data']:
                continue
            
            # 找到当前时间对应的值
            data = lane['data']
            target = lane['target']
            param = lane['param']
            
            # 简单插值
            for i in range(len(data) - 1):
                if data[i][0] <= current_time < data[i + 1][0]:
                    t0, v0 = data[i]
                    t1, v1 = data[i + 1]
                    progress = (current_time - t0) / (t1 - t0)
                    value = v0 + (v1 - v0) * progress
                    
                    if hasattr(target, f'set_{param}'):
                        getattr(target, f'set_{param}')(value)
                    break
