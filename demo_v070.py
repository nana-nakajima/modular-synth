#!/usr/bin/env python3
"""
Modular Synth Studio v0.7.0 演示
新增功能:
- 演奏录音器 (Performance Recorder)
- 音效增强 (相位器、环形调制、比特粉碎、波形折叠)
- 扩展预设库 (200+ 预设)
"""

import sys
import os
import time
import threading
import numpy as np

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audio.core_modules import Oscillator, Filter, Envelope, LFO
from audio.presets import PresetLibrary
from audio.performance_recorder import PerformanceRecorder, RecordingState
from audio.enhanced_effects_v070 import (
    Phaser, RingModulator, Bitcrusher, Wavefolder, 
    FilterResonance, EnhancedEffectChain
)


def demo_presets_v070():
    """演示v0.7.0扩展预设库"""
    print("\n" + "=" * 60)
    print("🎹 Modular Synth Studio v0.7.0 - 扩展预设演示")
    print("=" * 60)
    
    library = PresetLibrary()
    
    # 统计
    total = 0
    for category, presets in library.presets.items():
        print(f"\n📁 {category}: {len(presets)} 个预设")
        total += len(presets)
        # 显示前3个
        for i, preset in enumerate(presets[:3]):
            print(f"   {i+1}. {preset.name}")
        if len(presets) > 3:
            print(f"   ... 还有 {len(presets) - 3} 个")
    
    print(f"\n✅ 总计: {total} 个预设 (v0.7.0扩展)")


def demo_performance_recorder():
    """演示演奏录音器"""
    print("\n" + "=" * 60)
    print("🎙️ 演奏录音器演示")
    print("=" * 60)
    
    recorder = PerformanceRecorder(sample_rate=44100)
    
    # 设置回调
    def on_note_on(note, velocity, channel):
        print(f"   🎵 按下: MIDI音符 {note} (频率: {440 * (2 ** ((note - 69) / 12)):.1f} Hz), 力度: {velocity}")
    
    def on_note_off(note, channel):
        print(f"   🔇 释放: MIDI音符 {note}")
    
    recorder.on_note_on = on_note_on
    recorder.on_note_off = on_note_off
    
    # 开始录音
    print("\n🎙️ 开始录音...")
    track = recorder.start_recording("测试演奏")
    time.sleep(0.5)
    
    # 模拟演奏
    print("\n🎹 模拟演奏...")
    notes = [60, 64, 67, 72, 71, 67, 64, 60]  # C大调音阶
    for i, note in enumerate(notes):
        recorder.record_note_on(note, 100)
        time.sleep(0.3)
        recorder.record_note_off(note)
        time.sleep(0.1)
    
    # 停止录音
    print("\n⏹️ 停止录音...")
    track = recorder.stop_recording()
    
    print(f"\n✅ 录制完成: {len(track.events)} 个音符")
    
    # 回放
    print("\n▶️ 回放录音...")
    recorder.start_playback(track)
    time.sleep(2)
    recorder.stop_playback()
    
    # 导出为MIDI
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    midi_path = os.path.join(output_dir, "recorded_performance.mid")
    recorder.export_to_midi(track, midi_path)
    
    print(f"\n✅ 录音器演示完成！")


def demo_enhanced_effects():
    """演示增强效果器"""
    print("\n" + "=" * 60)
    print("🎛️ 增强效果器演示")
    print("=" * 60)
    
    sample_rate = 44100
    duration = 1.0
    num_samples = int(sample_rate * duration)
    
    # 生成测试信号
    t = np.linspace(0, duration, num_samples, False)
    test_signal = 0.5 * np.sin(2 * np.pi * 440 * t)
    
    # 测试相位器
    print("\n🎚️ 相位器效果...")
    phaser = Phaser(sample_rate)
    phaser.params.rate = 0.3
    phaser.params.depth = 0.7
    phaser.params.stages = 4
    phaser.params.mix = 0.5
    
    output = phaser.process(test_signal)
    print(f"   ✅ 相位器输出范围: [{output.min():.3f}, {output.max():.3f}]")
    
    # 测试环形调制
    print("\n🎭 环形调制器效果...")
    ring_mod = RingModulator(sample_rate)
    ring_mod.params.frequency = 220.0
    ring_mod.params.mix = 0.5
    
    output = ring_mod.process(test_signal)
    print(f"   ✅ 环形调制输出范围: [{output.min():.3f}, {output.max():.3f}]")
    
    # 测试比特粉碎
    print("\n🔲 比特粉碎器效果...")
    bitcrusher = Bitcrusher(sample_rate)
    bitcrusher.params.bits = 8
    bitcrusher.params.mix = 0.5
    
    output = bitcrusher.process(test_signal)
    print(f"   ✅ 比特粉碎输出范围: [{output.min():.3f}, {output.max():.3f}]")
    
    # 测试波形折叠
    print("\n🌀 波形折叠器效果...")
    wavefolder = Wavefolder(sample_rate)
    wavefolder.params.drive = 2.0
    wavefolder.params.mix = 0.5
    
    loud_signal = 0.8 * np.sin(2 * np.pi * 220 * t)
    output = wavefolder.process(loud_signal)
    print(f"   ✅ 波形折叠输出范围: [{output.min():.3f}, {output.max():.3f}]")
    
    # 测试增强效果链
    print("\n🔗 增强效果链...")
    chain = EnhancedEffectChain(sample_rate)
    chain.set_effect_enabled('phaser', True)
    chain.set_effect_enabled('bitcrusher', True)
    chain.set_effect_enabled('ring_mod', True)
    
    output = chain.process(test_signal, cutoff=2000.0, resonance=0.5)
    print(f"   ✅ 效果链输出范围: [{output.min():.3f}, {output.max():.3f}]")
    
    print("\n✅ 增强效果器演示完成！")


def demo_audio_generation():
    """演示音频生成和效果处理"""
    print("\n" + "=" * 60)
    print("🎵 音频生成与效果处理演示")
    print("=" * 60)
    
    sample_rate = 44100
    duration = 2.0
    
    # 创建合成器
    osc = Oscillator(waveform="sawtooth", frequency=440, sample_rate=sample_rate)
    filter_module = Filter(filter_type="lowpass", cutoff=2000, resonance=0.5, sample_rate=sample_rate)
    envelope = Envelope(attack=0.01, decay=0.3, sustain=0.5, release=0.3, sample_rate=sample_rate)
    
    # 生成音频
    print("\n🎹 生成音频样本...")
    num_samples = int(sample_rate * duration)
    
    # 生成简单的旋律
    notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 392.00, 349.23, 329.63, 293.66, 261.63]
    samples = np.zeros(num_samples)
    
    note_duration = num_samples // len(notes)
    for i, freq in enumerate(notes):
        osc.frequency = freq
        start = i * note_duration
        end = min((i + 1) * note_duration, num_samples)
        
        for j in range(start, end):
            osc_sample = osc.process()
            env_sample = envelope.process()
            samples[j] = osc_sample * env_sample
    
    print(f"   ✅ 生成 {len(samples)} 个样本")
    print(f"   ✅ 峰值: {np.max(np.abs(samples)):.3f}")
    
    # 应用效果
    print("\n🎛️ 应用效果器...")
    chain = EnhancedEffectChain(sample_rate)
    
    # 相位器
    phaser = Phaser(sample_rate)
    phaser.params.rate = 0.2
    phaser.params.depth = 0.5
    phaser.params.mix = 0.5
    
    phaser_output = phaser.process(samples)
    print(f"   ✅ 相位器处理完成")
    
    # 比特粉碎
    bitcrusher = Bitcrusher(sample_rate)
    bitcrusher.params.bits = 6
    bitcrusher.params.mix = 0.4
    
    crushed_output = bitcrusher.process(samples)
    print(f"   ✅ 比特粉碎处理完成")
    
    # 环形调制
    ring_mod = RingModulator(sample_rate)
    ring_mod.params.frequency = 330.0
    ring_mod.params.mix = 0.5
    
    ring_output = ring_mod.process(samples)
    print(f"   ✅ 环形调制处理完成")
    
    # 效果链
    chain = EnhancedEffectChain(sample_rate)
    chain.set_effect_enabled('phaser', True)
    chain.set_effect_enabled('chorus', True)
    
    chain_output = chain.process(samples, cutoff=2500, resonance=0.4)
    print(f"   ✅ 效果链处理完成")
    
    print("\n✅ 音频生成与效果处理演示完成！")


def interactive_demo():
    """交互式演示"""
    print("\n" + "=" * 60)
    print("🎮 交互式演奏演示")
    print("=" * 60)
    print("\n按键盘演奏 (q 退出):")
    print("  A S D F G H J K - 演奏中音C D E F G A B")
    print("  Z X C V B N M - 演奏低音C D E F G A B")
    print("  1 2 3 4 5 6 7 8 - 切换效果器")
    
    # 创建音频引擎
    sample_rate = 44100
    osc = Oscillator(waveform="sawtooth", frequency=440, sample_rate=sample_rate)
    filter_module = Filter(filter_type="lowpass", cutoff=3000, resonance=0.3, sample_rate=sample_rate)
    envelope = Envelope(attack=0.01, decay=0.2, sustain=0.7, release=0.2, sample_rate=sample_rate)
    
    # 效果器
    phaser = Phaser(sample_rate)
    phaser.params.mix = 0.3
    bitcrusher = Bitcrusher(sample_rate)
    bitcrusher.params.mix = 0.2
    
    # 演奏录音器
    recorder = PerformanceRecorder(sample_rate)
    
    # 音符映射
    note_map = {
        'a': 60, 's': 62, 'd': 64, 'f': 65, 'g': 67, 'h': 69, 'j': 71, 'k': 72,
        'z': 48, 'x': 50, 'c': 52, 'v': 53, 'b': 55, 'n': 57, 'm': 59
    }
    
    active_notes = {}
    recording = False
    
    print("\n🎹 开始演奏! 按 'r' 开始/停止录音, 'q' 退出\n")
    
    while True:
        try:
            import tty
            import termios
            
            def get_char():
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch
            
            char = get_char()
            
            if char == 'q':
                break
            elif char == 'r':
                if not recording:
                    recorder.start_recording("现场演奏")
                    recording = True
                    print("\n🎙️ 开始录音...")
                else:
                    recorder.stop_recording()
                    recording = False
                    print("\n⏹️ 录音停止!")
            elif char.lower() in note_map:
                note = note_map[char.lower()]
                if note not in active_notes:
                    freq = 440 * (2 ** ((note - 69) / 12))
                    osc.frequency = freq
                    active_notes[note] = time.time()
                    envelope.reset()
                    recorder.record_note_on(note, 100)
                    print(f"   🎵 按下: {note} ({freq:.1f} Hz)")
            elif char.lower() in '12345678':
                effect_idx = int(char)
                effects = ['phaser', 'ring_mod', 'bitcrusher', 'wavefolder']
                if effect_idx <= len(effects):
                    recorder.state = RecordingState.IDLE
                    pass
            
        except ImportError:
            print("   (交互模式需要终端支持)")
            break
        except Exception as e:
            print(f"   错误: {e}")
            break
    
    print("\n✅ 交互演示完成！")


def main():
    """主函数"""
    print("\n" + "🎹" * 20)
    print("\n  Modular Synth Studio v0.7.0")
    print("  🎛️ 演奏录音 | 🎚️ 增强效果 | 🎵 扩展预设\n")
    print("🎹" * 20)
    
    # 菜单
    print("\n请选择演示:")
    print("1. 扩展预设库演示")
    print("2. 演奏录音器演示")
    print("3. 增强效果器演示")
    print("4. 音频生成演示")
    print("5. 交互式演奏 (需要终端)")
    print("0. 退出")
    
    choice = input("\n请输入选项 (0-5): ").strip()
    
    if choice == "1":
        demo_presets_v070()
    elif choice == "2":
        demo_performance_recorder()
    elif choice == "3":
        demo_enhanced_effects()
    elif choice == "4":
        demo_audio_generation()
    elif choice == "5":
        interactive_demo()
    elif choice == "0":
        print("\n👋 再见!")
        return
    
    print("\n" + "=" * 60)
    print("🎉 Modular Synth Studio v0.7.0 演示完成!")
    print("=" * 60)
    print("\n新增功能:")
    print("  🎙️ 演奏录音 - 录制和回放MIDI演奏")
    print("  🎚️ 增强效果 - 相位器、环形调制、比特粉碎、波形折叠")
    print("  📀 扩展预设 - 200+ 专业预设")
    print("\n项目地址: https://github.com/nana-nakajima/modular-synth")
    print("=" * 60)


if __name__ == "__main__":
    main()
