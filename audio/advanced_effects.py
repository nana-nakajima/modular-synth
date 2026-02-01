# 🎹 高级效果器模块 v0.5.0
# 合唱、压缩器、均衡器

import numpy as np
from typing import List, Optional, Dict, Any

# ============ 合唱效果器 (Chorus) ============

class Chorus:
    """
    合唱效果器 - 创造宽广、丰富的立体声效果
    通过轻微延迟和调制来模拟多个乐器同时演奏
    """
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.delay_seconds = 0.025  # 基础延迟 25ms
        self.depth = 0.003  # 调制深度 3ms
        self.rate = 0.5  # 调制速率 Hz
        self.mix = 0.5  # 干湿混合比例
        self.feedback = 0.0  # 反馈量
        
        # 左右声道延迟线
        self.delay_left = np.zeros(int(0.05 * sample_rate))  # 50ms 最大延迟
        self.delay_right = np.zeros(int(0.05 * sample_rate))
        self.write_pos = 0
        self.phase = 0.0
        
        # LFO
        self.lfo_phase = 0.0
        self.lfo_freq = 0.5  # Hz
    
    def set_rate(self, rate: float):
        """设置LFO调制速率 (0.1 - 2.0 Hz)"""
        self.rate = np.clip(rate, 0.1, 2.0)
        self.lfo_freq = self.rate
    
    def set_depth(self, depth: float):
        """设置调制深度 (0.0 - 0.01)"""
        self.depth = np.clip(depth, 0.0, 0.01)
    
    def set_mix(self, mix: float):
        """设置混合比例 (0.0 - 1.0)"""
        self.mix = np.clip(mix, 0.0, 1.0)
    
    def set_feedback(self, feedback: float):
        """设置反馈量 (0.0 - 0.9)"""
        self.feedback = np.clip(feedback, 0.0, 0.9)
    
    def process(self, dry_left: np.ndarray, dry_right: np.ndarray) -> tuple:
        """
        处理立体声信号
        返回: (wet_left, wet_right)
        """
        wet_left = np.zeros_like(dry_left)
        wet_right = np.zeros_like(dry_right)
        
        delay_samples_max = len(self.delay_left)
        
        for i in range(len(dry_left)):
            # 更新LFO相位
            self.lfo_phase += 2 * np.pi * self.lfo_freq / self.sample_rate
            if self.lfo_phase > 2 * np.pi:
                self.lfo_phase -= 2 * np.pi
            
            # 计算动态延迟
            lfo_value = np.sin(self.lfo_phase)  # -1 到 1
            delay_offset = int((self.delay_seconds + self.depth * lfo_value) * self.sample_rate)
            delay_offset = np.clip(delay_offset, 1, delay_samples_max - 1)
            
            # 读取延迟样本
            read_pos = (self.write_pos - delay_offset) % delay_samples_max
            read_pos_int = int(read_pos)
            
            delayed_left = self.delay_left[read_pos_int]
            delayed_right = self.delay_right[read_pos_int]
            
            # 写入新样本（带反馈）
            self.delay_left[self.write_pos] = dry_left[i] + delayed_right * self.feedback
            self.delay_right[self.write_pos] = dry_right[i] + delayed_left * self.feedback
            
            # 更新写入位置
            self.write_pos = (self.write_pos + 1) % delay_samples_max
            
            # 混合干湿信号
            wet_left[i] = dry_left[i] * (1 - self.mix) + delayed_left * self.mix
            wet_right[i] = dry_right[i] * (1 - self.mix) + delayed_right * self.mix
        
        return wet_left, wet_right
    
    def process_mono(self, dry: np.ndarray) -> np.ndarray:
        """处理单声道信号"""
        wet = np.zeros_like(dry)
        
        delay_samples_max = len(self.delay_left)
        
        for i in range(len(dry)):
            self.lfo_phase += 2 * np.pi * self.lfo_freq / self.sample_rate
            if self.lfo_phase > 2 * np.pi:
                self.lfo_phase -= 2 * np.pi
            
            lfo_value = np.sin(self.lfo_phase)
            delay_offset = int((self.delay_seconds + self.depth * lfo_value) * self.sample_rate)
            delay_offset = np.clip(delay_offset, 1, delay_samples_max - 1)
            
            read_pos = (self.write_pos - delay_offset) % delay_samples_max
            delayed = self.delay_left[int(read_pos)]
            
            self.delay_left[self.write_pos] = dry[i] + delayed * self.feedback
            self.write_pos = (self.write_pos + 1) % delay_samples_max
            
            wet[i] = dry[i] * (1 - self.mix) + delayed * self.mix
        
        return wet
    
    def get_params(self) -> Dict[str, Any]:
        """获取参数"""
        return {
            'delay_seconds': self.delay_seconds,
            'depth': self.depth,
            'rate': self.rate,
            'mix': self.mix,
            'feedback': self.feedback
        }
    
    def set_params(self, params: Dict[str, Any]):
        """设置参数"""
        if 'delay_seconds' in params:
            self.delay_seconds = params['delay_seconds']
        if 'depth' in params:
            self.depth = params['depth']
        if 'rate' in params:
            self.set_rate(params['rate'])
        if 'mix' in params:
            self.set_mix(params['mix'])
        if 'feedback' in params:
            self.set_feedback(params['feedback'])


# ============ 压缩器 (Compressor) ============

class Compressor:
    """
    动态压缩器 - 控制音频动态范围
    用于平衡音量、添加冲击力
    """
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.threshold_db = -20.0  # 阈值 dB
        self.ratio = 4.0  # 压缩比
        self.attack_ms = 10.0  # 启动时间 ms
        self.release_ms = 100.0  # 释放时间 ms
        self.makeup_gain_db = 0.0  # 增益补偿 dB
        self.knee_db = 6.0  # 拐点宽度 dB
        
        # 内部状态
        self.envelope = 0.0
        self.envelope_prev = 0.0
        self.attack_coeff = 0.0
        self.release_coeff = 0.0
        self._calc_coefficients()
    
    def _calc_coefficients(self):
        """计算attack/release系数"""
        self.attack_coeff = np.exp(-1.0 / (self.attack_ms / 1000.0 * self.sample_rate))
        self.release_coeff = np.exp(-1.0 / (self.release_ms / 1000.0 * self.sample_rate))
    
    def set_threshold(self, threshold_db: float):
        """设置阈值 (-60 到 0 dB)"""
        self.threshold_db = np.clip(threshold_db, -60.0, 0.0)
    
    def set_ratio(self, ratio: float):
        """设置压缩比 (1:1 到 20:1)"""
        self.ratio = np.clip(ratio, 1.0, 20.0)
    
    def set_attack(self, attack_ms: float):
        """设置启动时间 (0.1 - 100 ms)"""
        self.attack_ms = np.clip(attack_ms, 0.1, 100.0)
        self._calc_coefficients()
    
    def set_release(self, release_ms: float):
        """设置释放时间 (10 - 1000 ms)"""
        self.release_ms = np.clip(release_ms, 10.0, 1000.0)
        self._calc_coefficients()
    
    def set_makeup_gain(self, gain_db: float):
        """设置增益补偿 (0 - 24 dB)"""
        self.makeup_gain_db = np.clip(gain_db, 0.0, 24.0)
    
    def _db_to_linear(self, db: float) -> float:
        """dB转线性"""
        return 10 ** (db / 20.0)
    
    def _linear_to_db(self, linear: float) -> float:
        """线性转dB"""
        if linear < 1e-10:
            return -100.0
        return 20 * np.log10(linear)
    
    def _calc_gain_reduction(self, input_db: float) -> float:
        """计算增益衰减量"""
        # 拐点处理
        knee_start = self.threshold_db - self.knee_db / 2
        knee_end = self.threshold_db + self.knee_db / 2
        
        if input_db < knee_start:
            return 0.0
        elif input_db > knee_end:
            # 超过阈值部分应用压缩比
            excess = input_db - self.threshold_db
            reduction = excess * (1 - 1 / self.ratio)
            return reduction
        else:
            # 在拐点范围内 - 线性过渡
            knee_position = (input_db - knee_start) / self.knee_db
            excess = (input_db - knee_start) - knee_position * self.knee_db * (1 - 1 / self.ratio)
            return excess * knee_position
    
    def process_sample(self, sample: float) -> float:
        """处理单个样本"""
        # 计算输入电平
        input_linear = abs(sample)
        input_db = self._linear_to_db(input_linear)
        
        # 包络检测
        if input_db > self.envelope:
            # 启动 - 使用attack系数
            self.envelope = self.attack_coeff * self.envelope + (1 - self.attack_coeff) * input_db
        else:
            # 释放 - 使用release系数
            self.envelope = self.release_coeff * self.envelope + (1 - self.release_coeff) * input_db
        
        # 计算增益衰减
        gain_reduction_db = self._calc_gain_reduction(self.envelope)
        
        # 应用压缩
        linear_gain = self._db_to_linear(-gain_reduction_db + self.makeup_gain_db)
        return sample * linear_gain
    
    def process(self, signal: np.ndarray) -> np.ndarray:
        """处理整个信号"""
        output = np.zeros_like(signal)
        self.envelope = 0.0
        
        for i in range(len(signal)):
            output[i] = self.process_sample(signal[i])
        
        return output
    
    def get_params(self) -> Dict[str, Any]:
        """获取参数"""
        return {
            'threshold_db': self.threshold_db,
            'ratio': self.ratio,
            'attack_ms': self.attack_ms,
            'release_ms': self.release_ms,
            'makeup_gain_db': self.makeup_gain_db,
            'knee_db': self.knee_db
        }
    
    def set_params(self, params: Dict[str, Any]):
        """设置参数"""
        if 'threshold_db' in params:
            self.set_threshold(params['threshold_db'])
        if 'ratio' in params:
            self.set_ratio(params['ratio'])
        if 'attack_ms' in params:
            self.set_attack(params['attack_ms'])
        if 'release_ms' in params:
            self.set_release(params['release_ms'])
        if 'makeup_gain_db' in params:
            self.set_makeup_gain(params['makeup_gain_db'])


# ============ 均衡器 (EQ) ============

class EQBand:
    """EQ频段"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.band_type = 'peak'  # low_shelf, high_shelf, peak, low_pass, high_pass
        self.frequency = 1000.0
        self.gain_db = 0.0
        self.q = 1.0
        
        # biquad滤波器系数
        self.b0, self.b1, self.b2, self.a0, self.a1, self.a2 = 1, 0, 0, 1, 0, 0
        self.x1, self.x2 = 0, 0
        self.y1, self.y2 = 0, 0
    
    def _calc_coefficients(self):
        """计算biquad系数"""
        w0 = 2 * np.pi * self.frequency / self.sample_rate
        cos_w0 = np.cos(w0)
        sin_w0 = np.sin(w0)
        alpha = sin_w0 / (2 * self.q)
        
        A = 10 ** (self.gain_db / 40)  # 增益因子
        
        if self.band_type == 'low_shelf':
            sqrt_A = np.sqrt(A)
            self.b0 = A * ((A + 1) - (A - 1) * cos_w0 + 2 * sqrt_A * alpha)
            self.b1 = 2 * A * ((A - 1) - (A + 1) * cos_w0)
            self.b2 = A * ((A + 1) - (A - 1) * cos_w0 - 2 * sqrt_A * alpha)
            self.a0 = (A + 1) + (A - 1) * cos_w0 + 2 * sqrt_A * alpha
            self.a1 = -2 * ((A - 1) + (A + 1) * cos_w0)
            self.a2 = (A + 1) + (A - 1) * cos_w0 - 2 * sqrt_A * alpha
            
        elif self.band_type == 'high_shelf':
            sqrt_A = np.sqrt(A)
            self.b0 = A * ((A + 1) + (A - 1) * cos_w0 + 2 * sqrt_A * alpha)
            self.b1 = -2 * A * ((A - 1) + (A + 1) * cos_w0)
            self.b2 = A * ((A + 1) + (A - 1) * cos_w0 - 2 * sqrt_A * alpha)
            self.a0 = (A + 1) - (A - 1) * cos_w0 + 2 * sqrt_A * alpha
            self.a1 = 2 * ((A - 1) - (A + 1) * cos_w0)
            self.a2 = (A + 1) - (A - 1) * cos_w0 - 2 * sqrt_A * alpha
            
        elif self.band_type == 'peak':
            self.b0 = 1 + alpha * A
            self.b1 = -2 * cos_w0
            self.b2 = 1 - alpha * A
            self.a0 = 1 + alpha / A
            self.a1 = -2 * cos_w0
            self.a2 = 1 - alpha / A
        
        # 归一化
        self.b0 /= self.a0
        self.b1 /= self.a0
        self.b2 /= self.a0
        self.a1 /= self.a0
        self.a2 /= self.a0
    
    def set_frequency(self, freq: float):
        """设置中心频率 (20 - 20000 Hz)"""
        self.frequency = np.clip(freq, 20.0, 20000.0)
        self._calc_coefficients()
    
    def set_gain(self, gain_db: float):
        """设置增益 (-12 到 12 dB)"""
        self.gain_db = np.clip(gain_db, -12.0, 12.0)
        self._calc_coefficients()
    
    def set_q(self, q: float):
        """设置Q值 (0.1 - 20)"""
        self.q = np.clip(q, 0.1, 20.0)
        self._calc_coefficients()
    
    def set_band_type(self, band_type: str):
        """设置频段类型"""
        valid_types = ['low_shelf', 'high_shelf', 'peak', 'low_pass', 'high_pass']
        if band_type in valid_types:
            self.band_type = band_type
            self._calc_coefficients()
    
    def process(self, sample: float) -> float:
        """处理单个样本"""
        result = self.b0 * sample + self.b1 * self.x1 + self.b2 * self.x2 - self.a1 * self.y1 - self.a2 * self.y2
        
        self.x2, self.x1 = self.x1, sample
        self.y2, self.y1 = self.y1, result
        
        return result
    
    def reset(self):
        """重置状态"""
        self.x1, self.x2 = 0, 0
        self.y1, self.y2 = 0, 0


class ParametricEQ:
    """参数均衡器 - 多频段均衡"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.bands: List[EQBand] = []
        self._init_default_bands()
    
    def _init_default_bands(self):
        """初始化默认频段"""
        # 低频-shelf
        low = EQBand(self.sample_rate)
        low.set_band_type('low_shelf')
        low.set_frequency(100)
        low.set_gain(0)
        self.bands.append(low)
        
        # 中频-peak
        mid = EQBand(self.sample_rate)
        mid.set_band_type('peak')
        mid.set_frequency(1000)
        mid.set_gain(0)
        mid.set_q(1)
        self.bands.append(mid)
        
        # 高频-shelf
        high = EQBand(self.sample_rate)
        high.set_band_type('high_shelf')
        high.set_frequency(8000)
        high.set_gain(0)
        self.bands.append(high)
    
    def add_band(self, band_type: str = 'peak', frequency: float = 2000, 
                 gain_db: float = 0, q: float = 1.0) -> EQBand:
        """添加频段"""
        band = EQBand(self.sample_rate)
        band.set_band_type(band_type)
        band.set_frequency(frequency)
        band.set_gain(gain_db)
        band.set_q(q)
        self.bands.append(band)
        return band
    
    def remove_band(self, index: int):
        """移除频段"""
        if 0 <= index < len(self.bands):
            self.bands.pop(index)
    
    def process(self, sample: float) -> float:
        """处理单个样本 - 串联所有频段"""
        result = sample
        for band in self.bands:
            result = band.process(result)
        return result
    
    def process_block(self, signal: np.ndarray) -> np.ndarray:
        """处理信号块"""
        output = np.zeros_like(signal)
        # 重置所有频段状态
        for band in self.bands:
            band.reset()
        
        for i in range(len(signal)):
            output[i] = self.process(signal[i])
        
        return output
    
    def get_params(self) -> List[Dict[str, Any]]:
        """获取所有频段参数"""
        return [{
            'band_type': band.band_type,
            'frequency': band.frequency,
            'gain_db': band.gain_db,
            'q': band.q
        } for band in self.bands]
    
    def set_params(self, params: List[Dict[str, Any]]):
        """设置所有频段参数"""
        for i, param in enumerate(params):
            if i < len(self.bands):
                band = self.bands[i]
                if 'band_type' in param:
                    band.set_band_type(param['band_type'])
                if 'frequency' in param:
                    band.set_frequency(param['frequency'])
                if 'gain_db' in param:
                    band.set_gain(param['gain_db'])
                if 'q' in param:
                    band.set_q(param['q'])


# ============ 高级效果器链 ============

class AdvancedEffectChain:
    """
    高级效果器链 - 整合所有效果器
    顺序: Compressor -> Chorus -> EQ -> Distortion -> Reverb -> Delay
    """
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        
        # 效果器
        self.compressor = Compressor(sample_rate)
        self.chorus = Chorus(sample_rate)
        self.eq = ParametricEQ(sample_rate)
        self.distortion = None  # 从core_modules导入
        self.reverb = None  # 从core_modules导入
        self.delay = None  # 从core_modules导入
        
        # 效果器启用状态
        self.enabled = {
            'compressor': False,
            'chorus': False,
            'eq': False,
            'distortion': False,
            'reverb': False,
            'delay': False
        }
    
    def set_compressor(self, enabled: bool, **params):
        """配置压缩器"""
        self.enabled['compressor'] = enabled
        if params:
            self.compressor.set_params(params)
    
    def set_chorus(self, enabled: bool, **params):
        """配置合唱"""
        self.enabled['chorus'] = enabled
        if params:
            self.chorus.set_params(params)
    
    def set_eq(self, enabled: bool, bands: List[Dict[str, Any]] = None):
        """配置均衡器"""
        self.enabled['eq'] = enabled
        if bands:
            self.eq.set_params(bands)
    
    def set_reverb(self, enabled: bool, **params):
        """配置混响"""
        self.enabled['reverb'] = enabled
        if params and self.reverb:
            self.reverb.set_params(params)
    
    def set_delay(self, enabled: bool, **params):
        """配置延迟"""
        self.enabled['delay'] = enabled
        if params and self.delay:
            self.delay.set_params(params)
    
    def set_distortion(self, enabled: bool, **params):
        """配置失真"""
        self.enabled['distortion'] = enabled
        if params and self.distortion:
            self.distortion.set_params(params)
    
    def process_stereo(self, left: np.ndarray, right: np.ndarray) -> tuple:
        """处理立体声信号"""
        out_left, out_right = left.copy(), right.copy()
        
        # 压缩器
        if self.enabled['compressor']:
            out_left = self.compressor.process(out_left)
            out_right = self.compressor.process(out_right)
        
        # 合唱
        if self.enabled['chorus']:
            out_left, out_right = self.chorus.process(out_left, out_right)
        
        # 均衡器
        if self.enabled['eq']:
            out_left = self.eq.process_block(out_left)
            out_right = self.eq.process_block(out_right)
        
        return out_left, out_right
    
    def process_mono(self, signal: np.ndarray) -> np.ndarray:
        """处理单声道信号"""
        output = signal.copy()
        
        if self.enabled['compressor']:
            output = self.compressor.process(output)
        
        if self.enabled['chorus']:
            output = self.chorus.process_mono(output)
        
        if self.enabled['eq']:
            output = self.eq.process_block(output)
        
        return output
    
    def get_all_params(self) -> Dict[str, Any]:
        """获取所有效果器参数"""
        return {
            'compressor': {
                'enabled': self.enabled['compressor'],
                'params': self.compressor.get_params()
            },
            'chorus': {
                'enabled': self.enabled['chorus'],
                'params': self.chorus.get_params()
            },
            'eq': {
                'enabled': self.enabled['eq'],
                'params': self.eq.get_params()
            }
        }
    
    def reset(self):
        """重置所有效果器"""
        self.compressor = Compressor(self.sample_rate)
        self.chorus = Chorus(self.sample_rate)
        self.eq = ParametricEQ(self.sample_rate)
        for key in self.enabled:
            self.enabled[key] = False
