# 🎹 实时音频播放器模块

import numpy as np
import sounddevice as sd
import threading
from .core_modules import Oscillator, Filter, Envelope, MultiOscillator

class RealTimeSynth:
    """实时音频合成器 - 支持键盘演奏"""

    def __init__(self, sample_rate=44100, buffer_size=1024):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size

        # 音频模块
        self.oscillator = Oscillator(frequency=440.0, wave_type='sawtooth', sample_rate=sample_rate)
        self.filter = Filter(cutoff=2000, filter_type='lowpass', sample_rate=sample_rate)
        self.envelope = Envelope(attack=0.01, decay=0.2, sustain=0.7, release=0.3, sample_rate=sample_rate)

        # 状态
        self.is_playing = False
        self.current_note = None
        self.note_frequencies = {
            'a': 261.63,  # C4
            's': 293.66,  # D4
            'd': 329.63,  # E4
            'f': 349.23,  # F4
            'g': 392.00,  # G4
            'h': 440.00,  # A4
            'j': 493.88,  # B4
            'k': 523.25,  # C5
        }

        # 音量控制
        self.volume = 0.5

        # 音频流
        self.stream = None

    def start(self):
        """启动音频流"""
        if self.stream is None:
            self.stream = sd.OutputStream(
                samplerate=self.sample_rate,
                channels=1,
                callback=self._audio_callback,
                blocksize=self.buffer_size
            )
        self.stream.start()
        self.is_playing = True

    def stop(self):
        """停止音频流"""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.is_playing = False
        self.current_note = None

    def _audio_callback(self, outdata, frames, time, status):
        """音频回调函数"""
        # 生成静音
        audio_data = np.zeros(frames, dtype=np.float32)

        if self.current_note and self.is_playing:
            # 设置振荡器频率
            self.oscillator.set_frequency(self.current_note)

            # 生成音频
            for i in range(frames):
                # 处理包络
                env_value = self.envelope.process_sample()

                # 生成波形
                sample = self.oscillator.process_sample()

                # 应用滤波器
                filtered = self.filter.process_sample(sample)

                # 应用包络和音量
                audio_data[i] = filtered * env_value * self.volume

        outdata[:, 0] = audio_data

    def note_on(self, note_key):
        """按下音符"""
        if note_key.lower() in self.note_frequencies:
            self.current_note = self.note_frequencies[note_key.lower()]
            self.envelope.note_on()

    def note_off(self):
        """释放音符"""
        self.envelope.note_off()
        self.current_note = None

    def set_volume(self, volume):
        """设置音量 (0.0 - 1.0)"""
        self.volume = max(0.0, min(1.0, volume))

    def set_wave_type(self, wave_type):
        """设置波形类型"""
        self.oscillator.set_wave_type(wave_type)

    def set_filter(self, cutoff, resonance=None):
        """设置滤波器参数"""
        self.filter.set_cutoff(cutoff)
        if resonance:
            self.filter.set_resonance(resonance)


# ============ 测试代码 ============

if __name__ == "__main__":
    print("🎹 测试实时音频合成器")
    print("按键: A-S-D-F-G-H-J-K (演奏音符)")
    print("Q: 退出")
    print("+/-: 调节音量")
    print("W/S: 切换波形")
    print()

    synth = RealTimeSynth()
    synth.start()

    try:
        while True:
            key = input("按键: ").strip().lower()

            if key == 'q':
                break
            elif key == '+':
                synth.set_volume(synth.volume + 0.1)
                print(f"音量: {synth.volume:.1f}")
            elif key == '-':
                synth.set_volume(synth.volume - 0.1)
                print(f"音量: {synth.volume:.1f}")
            elif key == 'w':
                synth.set_wave_type('sawtooth')
                print("波形: Sawtooth")
            elif key == 's':
                synth.set_wave_type('sine')
                print("波形: Sine")
            elif key in synth.note_frequencies:
                synth.note_on(key)
                print(f"按下: {key.upper()} ({synth.note_frequencies[key]} Hz)")
            else:
                synth.note_off()
                print("释放")

    except KeyboardInterrupt:
        pass
    finally:
        synth.stop()
        print("\n👋 测试完成")
