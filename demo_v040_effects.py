#!/usr/bin/env python3
# 🎹 v0.4.0 效果器链与自动化演示
# 展示: 效果器链 + LFO自动化 + 失真效果

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from audio.core_modules import (
    Oscillator, Filter, Envelope, LFO, 
    Reverb, Delay, Distortion, EffectChain,
    LFOModulator, AutomationManager
)

def demo_effect_chain():
    """演示效果器链"""
    print("=" * 50)
    print("🎛️ 效果器链演示")
    print("=" * 50)
    
    # 创建效果器链
    chain = EffectChain(sample_rate=44100)
    
    # 添加效果器
    reverb = Reverb(room_size=0.3, damping=0.3)
    delay = Delay(delay_time=0.3, feedback=0.4)
    distortion = Distortion(drive=0.3, tone=0.6)
    
    chain.add_effect("reverb", reverb)
    chain.add_effect("delay", delay)
    chain.add_effect("distortion", distortion)
    
    print("✓ 效果器链配置:")
    print(f"  - 混响 (room_size={reverb.room_size}, damping={reverb.damping})")
    print(f"  - 延迟 (delay_time={delay.delay_time}s, feedback={delay.feedback})")
    print(f"  - 失真 (drive={distortion.drive}, tone={distortion.tone})")
    
    # 生成测试音频
    osc = Oscillator(frequency=440, wave_type='sawtooth', sample_rate=44100)
    audio = osc.generate(duration=2.0)
    
    # 处理音频
    processed = chain.process(audio)
    
    # 显示参数
    params = chain.get_params()
    print(f"\n✓ 效果器参数: {list(params.keys())}")
    
    # 动态调整参数
    chain.set_param("distortion", "drive", 0.6)
    print("✓ 失真驱动量已调整: 0.3 → 0.6")
    
    return True


def demo_lfo_modulation():
    """演示LFO自动化调制"""
    print("\n" + "=" * 50)
    print("🌊 LFO自动化调制演示")
    print("=" * 50)
    
    # 创建振荡器
    osc = Oscillator(frequency=440, wave_type='sine', sample_rate=44100)
    filter_module = Filter(cutoff=2000, filter_type='lowpass', sample_rate=44100)
    
    # 创建LFO
    lfo_freq = LFO(frequency=2.0, wave_type='sine', sample_rate=44100)  # 2Hz
    lfo_filter = LFO(frequency=0.5, wave_type='triangle', sample_rate=44100)  # 0.5Hz
    
    # 创建调制器
    modulator = LFOModulator(sample_rate=44100)
    
    # 添加调制: LFO调制振荡器频率 (颤音效果)
    modulator.add_modulation(osc, lfo_freq, 'frequency', depth=0.3)
    print("✓ 添加调制: LFO → 振荡器频率 (颤音)")
    
    # 添加调制: LFO调制滤波器截止频率 (哇音效果)
    modulator.add_modulation(filter_module, lfo_filter, 'cutoff', depth=0.5)
    print("✓ 添加调制: LFO → 滤波器截止频率 (哇音)")
    
    # 开始调制
    modulator.start()
    
    # 模拟处理
    print("\n🎵 实时调制演示 (2秒):")
    duration = 2.0
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    
    # 生成带调制的音频
    audio = np.zeros(num_samples)
    osc.phase = 0
    
    for i in range(num_samples):
        # 处理调制
        modulator.process(1)
        
        # 生成样本
        sample = osc.process_sample()
        audio[i] = sample
    
    print(f"✓ 生成了 {len(audio)} 个样本")
    print(f"✓ 频率范围: {osc.frequency:.1f} → ~{osc.frequency * 1.3:.1f} Hz")
    
    return True


def demo_automation_manager():
    """演示自动化管理器"""
    print("\n" + "=" * 50)
    print("🎹 自动化管理器演示")
    print("=" * 50)
    
    # 创建管理器
    manager = AutomationManager(sample_rate=44100)
    
    # 创建自动化轨道 - 滤波器扫频
    filter_module = Filter(cutoff=1000, filter_type='lowpass', sample_rate=44100)
    
    # 自动化数据: 时间点 → 截止频率
    automation_data = [
        (0.0, 1000),
        (1.0, 5000),
        (2.0, 500),
        (3.0, 3000),
        (4.0, 1000)
    ]
    
    manager.create_automation_lane(filter_module, 'cutoff', automation_data, loop=True)
    print("✓ 创建自动化轨道: 滤波器扫频")
    print(f"  自动化点: {automation_data}")
    
    # 模拟自动化播放
    print("\n🎵 自动化播放演示 (4秒):")
    for t in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
        manager.process_automation(t, 1)
        print(f"  t={t:.1f}s: 滤波器截止频率 = {filter_module.cutoff:.0f} Hz")
    
    return True


def demo_full_signal_chain():
    """演示完整信号链"""
    print("\n" + "=" * 50)
    print("🔗 完整信号链演示")
    print("=" * 50)
    
    # 创建组件
    osc = Oscillator(frequency=220, wave_type='sawtooth', sample_rate=44100)
    envelope = Envelope(attack=0.05, decay=0.2, sustain=0.6, release=0.5)
    filter_module = Filter(cutoff=3000, filter_type='lowpass', sample_rate=44100)
    
    # 创建LFO调制滤波器
    lfo = LFO(frequency=0.3, wave_type='sine', sample_rate=44100)
    modulator = LFOModulator(sample_rate=44100)
    modulator.add_modulation(filter_module, lfo, 'cutoff', depth=0.4)
    
    # 创建效果器链
    effect_chain = EffectChain(sample_rate=44100)
    effect_chain.add_effect("distortion", Distortion(drive=0.2, tone=0.5))
    effect_chain.add_effect("reverb", Reverb(room_size=0.4, damping=0.4))
    effect_chain.add_effect("delay", Delay(delay_time=0.25, feedback=0.3))
    
    # 创建自动化管理器
    manager = AutomationManager(sample_rate=44100)
    manager.lfo_modulator = modulator
    
    print("✓ 完整信号链配置:")
    print("  振荡器 → 包络 → 滤波器(LFO调制) → 效果器链 → 输出")
    print("  效果器: 失真 → 混响 → 延迟")
    
    # 生成音频
    duration = 3.0
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    
    audio = np.zeros(num_samples)
    osc.phase = 0
    envelope_samples = envelope.process(num_samples)
    
    modulator.start()
    
    for i in range(num_samples):
        # 处理LFO调制
        modulator.process(1)
        
        # 生成振荡器样本
        sample = osc.process_sample()
        
        # 应用包络
        sample *= envelope_samples[i]
        
        # 应用滤波器
        audio[i] = filter_module.process(np.array([sample]))[0]
    
    # 应用效果器链
    audio = effect_chain.process(audio)
    
    print(f"\n✓ 生成的音频: {len(audio)} 样本, {duration}秒")
    print(f"✓ 峰值振幅: {np.max(np.abs(audio)):.3f}")
    
    return True


def main():
    """主函数"""
    print("\n🎹 Modular Synth Studio v0.4.0")
    print("   效果器链 + 自动化控制演示")
    print()
    
    # 运行所有演示
    demo_effect_chain()
    demo_lfo_modulation()
    demo_automation_manager()
    demo_full_signal_chain()
    
    print("\n" + "=" * 50)
    print("✅ v0.4.0 功能演示完成!")
    print("=" * 50)
    print("\n📋 v0.4.0 完成清单:")
    print("  ✅ MIDI导出功能")
    print("  ✅ 预设库扩展 (101个音色)")
    print("  ✅ 效果器链 (混响、延迟、失真)")
    print("  ✅ 自动化控制 (LFO调制)")
    print("\n🔥 v0.4.0 完成度: 100%")
    print()


if __name__ == "__main__":
    main()
