#!/usr/bin/env python3
# 🎹 Modular Synth Studio v0.5.0 演示脚本
# 高级效果器、预设保存/加载、MIDI导入

import sys
import os
import numpy as np

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audio.core_modules import Oscillator, Filter, Envelope, LFO, EffectChain, Reverb, Delay, Distortion
from audio.advanced_effects import Chorus, Compressor, ParametricEQ, AdvancedEffectChain
from audio.preset_manager import PresetLibrary, PresetManager, Preset

# 简单的Synthesizer类用于演示
class SimpleSynthesizer:
    """简化的合成器类用于预设演示"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.oscillators = []
        self.filter = Filter(sample_rate=sample_rate)
        self.envelope = Envelope(sample_rate=sample_rate)
        self.volume = 0.8
    
    def add_oscillator(self, frequency, wave_type, gain=0.5):
        osc = Oscillator(frequency, wave_type, self.sample_rate)
        osc.gain = gain
        self.oscillators.append(osc)
    
    def set_volume(self, volume):
        self.volume = volume

print("=" * 60)
print("🎹 Modular Synth Studio v0.5.0 演示")
print("=" * 60)
print()

# ============ 1. 高级效果器演示 ============

print("🎵 1. 高级效果器演示")
print("-" * 40)

# 创建Chorus效果器
print("\n🎤 Chorus (合唱) 效果器:")
chorus = Chorus(sample_rate=44100)
print(f"   预设参数: {chorus.get_params()}")

# 修改Chorus参数
chorus.set_rate(0.3)
chorus.set_depth(0.005)
chorus.set_mix(0.6)
chorus.set_feedback(0.2)
print(f"   修改后: {chorus.get_params()}")

# 创建Compressor效果器
print("\n🔊 Compressor (压缩器) 效果器:")
compressor = Compressor(sample_rate=44100)
print(f"   预设参数: {compressor.get_params()}")

# 修改压缩器参数
compressor.set_threshold(-15)
compressor.set_ratio(6)
compressor.set_attack(5)
compressor.set_release(80)
compressor.set_makeup_gain(3)
print(f"   修改后: {compressor.get_params()}")

# 创建EQ效果器
print("\n🎚️ Parametric EQ (参数均衡器) 效果器:")
eq = ParametricEQ(sample_rate=44100)
print(f"   频段数: {len(eq.bands)}")
for i, band in enumerate(eq.bands):
    print(f"   频段{i+1}: {band.band_type} - {band.frequency}Hz, Q={band.q}, Gain={band.gain_db}dB")

# 修改EQ
eq.bands[0].set_gain(3)  # 低频+3dB
eq.bands[1].set_gain(-2)  # 中频-2dB
eq.bands[2].set_gain(4)  # 高频+4dB
print("\n   调整后EQ参数:")
for i, band in enumerate(eq.bands):
    print(f"   频段{i+1}: {band.band_type} - {band.frequency}Hz, Q={band.q}, Gain={band.gain_db}dB")

# ============ 2. 预设系统演示 ============

print("\n" + "=" * 60)
print("💾 2. 预设系统演示")
print("-" * 40)

# 创建预设库
library = PresetLibrary()
stats = library.get_stats()
print(f"\n📚 预设库统计:")
print(f"   总预设数: {stats['total_presets']}")
for category, count in stats['categories'].items():
    print(f"   {category}: {count}个")

# 按类别列出预设
print(f"\n📋 按类别列出:")
for category in ['Lead', 'Bass', 'Pad', 'Keys', 'FX']:
    presets = library.get_presets_by_category(category)
    print(f"\n   {category} ({len(presets)}个):")
    for p in presets[:3]:  # 只显示前3个
        print(f"   - {p.name}")
    if len(presets) > 3:
        print(f"   ... 还有{len(presets)-3}个")

# 搜索预设
print("\n🔍 搜索预设 'Pad':")
results = library.search_presets('Pad')
for p in results[:3]:
    print(f"   - {p.name} ({p.category})")

# ============ 3. 预设创建和修改演示 ============

print("\n" + "=" * 60)
print("✏️ 3. 预设创建和修改演示")
print("-" * 40)

# 创建自定义预设
print("\n🎨 创建自定义预设:")
custom_preset = Preset("Custom Lead", category="User")
custom_preset.oscillators = [
    {'frequency': 440, 'wave_type': 'sawtooth', 'gain': 0.6},
    {'frequency': 880, 'wave_type': 'square', 'gain': 0.3}
]
custom_preset.filter = {
    'type': 'lowpass',
    'cutoff': 2500,
    'resonance': 3.0,
    'enabled': True
}
custom_preset.envelope = {
    'attack': 0.01,
    'decay': 0.15,
    'sustain': 0.8,
    'release': 0.4,
    'enabled': True
}
custom_preset.effects['distortion'] = {'enabled': True, 'drive': 8, 'mix': 0.3}
custom_preset.description = "我的自定义主音音色"
custom_preset.tags = ['custom', 'lead', 'distorted']

library.add_preset(custom_preset)
print(f"   名称: {custom_preset.name}")
print(f"   类别: {custom_preset.category}")
print(f"   振荡器: {len(custom_preset.oscillators)}个")
print(f"   描述: {custom_preset.description}")
print(f"   标签: {custom_preset.tags}")

# 复制预设
print("\n📋 复制预设:")
copied = library.duplicate_preset("Custom Lead", "Custom Lead V2")
if copied:
    print(f"   复制成功: {copied.name} -> {copied.name} V2")

# ============ 4. 预设保存/加载演示 ============

print("\n" + "=" * 60)
print("💾 4. 预设保存/加载演示")
print("-" * 40)

# 保存整个库
print("\n💾 保存预设库...")
save_path = library.save_library('/tmp/modular_synth_presets.json')
print(f"   已保存到: {save_path}")

# 加载预设库
print("\n📂 加载预设库...")
new_library = PresetLibrary('/tmp/modular_synth_presets.json')
print(f"   加载了 {len(new_library.presets)} 个预设")

# 导出单个预设
print("\n📤 导出单个预设...")
library.export_preset("Dreamy Pad", "/tmp/dreamy_pad.json")
print(f"   已导出: Dreamy Pad")

# 导入单个预设
print("\n📥 导入单个预设...")
imported = new_library.import_preset("/tmp/dreamy_pad.json")
if imported:
    print(f"   导入成功: {imported.name}")

# ============ 5. 完整效果链演示 ============

print("\n" + "=" * 60)
print("🔗 5. 完整效果链演示")
print("-" * 40)

# 创建完整效果链
print("\n🔧 创建完整高级效果链...")
effect_chain = AdvancedEffectChain(sample_rate=44100)

# 配置所有效果器
effect_chain.set_compressor(True, 
    threshold_db=-18, ratio=5, attack_ms=8, release_ms=100, makeup_gain_db=2)
effect_chain.set_chorus(True, rate=0.4, depth=0.004, mix=0.5, feedback=0.1)

# 配置EQ
eq_bands = [
    {'band_type': 'low_shelf', 'frequency': 120, 'gain_db': 3, 'q': 1},
    {'band_type': 'peak', 'frequency': 1000, 'gain_db': -1.5, 'q': 2},
    {'band_type': 'peak', 'frequency': 3000, 'gain_db': 2, 'q': 1.5},
    {'band_type': 'high_shelf', 'frequency': 8000, 'gain_db': 4, 'q': 1}
]
effect_chain.set_eq(True, eq_bands)

print("   已配置:")
print("   - Compressor: 启用 (threshold=-18dB, ratio=5:1)")
print("   - Chorus: 启用 (rate=0.4Hz, depth=4ms)")
print("   - EQ: 启用 (4段均衡器)")

# 获取所有参数
all_params = effect_chain.get_all_params()
print("\n📊 效果链参数:")
for name, data in all_params.items():
    print(f"   {name}: {'启用' if data['enabled'] else '禁用'}")

# ============ 6. 合成器集成演示 ============

print("\n" + "=" * 60)
print("🎹 6. 合成器集成演示")
print("-" * 40)

# 创建合成器
synth = SimpleSynthesizer(sample_rate=44100)

# 加载预设
print("\n🎵 加载预设到合成器...")
manager = PresetManager(library)
preset = manager.load_preset("Classic Saw Lead")
if preset:
    print(f"   加载预设: {preset.name}")
    print(f"   振荡器数: {len(preset.oscillators)}")
    print(f"   滤波器: {preset.filter['type']} @ {preset.filter['cutoff']}Hz")
    
    # 应用到合成器
    if manager.apply_preset_to_synth(synth):
        print("   ✓ 成功应用到合成器")

# 从合成器收集状态
print("\n📝 从合成器收集状态...")
current_preset = manager.collect_synth_state(synth)
current_preset.name = "Live Capture"
print(f"   捕获预设: {current_preset.name}")
print(f"   振荡器数: {len(current_preset.oscillators)}")

# 保存当前状态
print("\n💾 保存当前状态...")
manager.save_current_preset("Live Capture", category="User")
print(f"   保存成功: Live Capture")

# ============ 总结 ============

print("\n" + "=" * 60)
print("✅ v0.5.0 演示完成!")
print("=" * 60)
print()
print("🎉 新功能总结:")
print("   ✓ Chorus (合唱) 效果器 - 创造宽广立体声")
print("   ✓ Compressor (压缩器) - 控制动态范围")
print("   ✓ Parametric EQ (参数均衡器) - 精确频段调整")
print("   ✓ PresetLibrary (预设库) - 101+预设管理")
print("   ✓ JSON保存/加载 - 便携式预设分享")
print("   ✓ 预设搜索/分类 - 快速找到想要的声音")
print()
print("📁 生成的文件:")
print("   - /tmp/modular_synth_presets.json (预设库)")
print("   - /tmp/dreamy_pad.json (单个预设)")
print()
print("🔜 v0.6.0 预告:")
print("   - GUI大升级 (更美观界面)")
print("   - MIDI导入功能")
print("   - 预设云同步")
print("   - 社区分享功能")
print()
