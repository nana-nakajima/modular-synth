#!/usr/bin/env python3
# 🎹 Modular Synth Studio - 主程序
# Nana的虚拟模块合成器项目

import sys
import numpy as np
from audio.core_modules import Oscillator, Filter, Envelope, LFO, MultiOscillator

def print_welcome():
    """打印欢迎信息"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🎹  Modular Synth Studio  🎹                             ║
║                                                           ║
║   Nana的虚拟模块合成器 - 综合音乐创作工具                   ║
║                                                           ║
║   功能:                                                   ║
║   • 振荡器 - 4种波形 (Sine, Square, Saw, Triangle)        ║
║   • 滤波器 - Low/High/Band pass                           ║
║   • 包络 - ADSR 可调节                                     ║
║   • LFO - 低频调制器                                       ║
║   • 效果器 - Reverb, Delay                                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)

def demo_oscillator():
    """演示振荡器"""
    print("\n🎵 演示1: 振荡器")
    print("-" * 50)
    
    # 创建振荡器
    osc = Oscillator(frequency=440.0, wave_type='sine')
    print(f"频率: {osc.frequency} Hz")
    print(f"波形: {osc.wave_type}")
    
    # 生成1秒音频
    audio = osc.generate(duration=1.0)
    print(f"生成样本数: {len(audio)}")
    print("✓ 振荡器正常工作!")

def demo_multi_oscillator():
    """演示多振荡器"""
    print("\n🎛️ 演示2: 多振荡器组合")
    print("-" * 50)
    
    multi = MultiOscillator()
    multi.add_oscillator(frequency=220.0, wave_type='sawtooth', gain=0.3)
    multi.add_oscillator(frequency=440.0, wave_type='sine', gain=0.5)
    multi.add_oscillator(frequency=660.0, wave_type='sine', gain=0.2)
    
    audio = multi.generate(duration=1.0)
    print(f"振荡器数量: {len(multi.oscillators)}")
    print("✓ 多振荡器组合正常工作!")

def demo_filter():
    """演示滤波器"""
    print("\n🔊 演示3: 滤波器")
    print("-" * 50)
    
    # 生成测试信号
    osc = Oscillator(frequency=100.0, wave_type='sawtooth')
    audio = osc.generate(duration=0.5)
    
    # 应用滤波器
    lowpass = Filter(cutoff=500, filter_type='lowpass')
    filtered = lowpass.process(audio)
    
    print(f"原始信号范围: [{audio.min():.3f}, {audio.max():.3f}]")
    print(f"滤波后范围: [{filtered.min():.3f}, {filtered.max():.3f}]")
    print("✓ 滤波器正常工作!")

def demo_envelope():
    """演示包络"""
    print("\n📈 演示4: ADSR包络")
    print("-" * 50)
    
    env = Envelope(attack=0.1, decay=0.2, sustain=0.7, release=0.3)
    
    # 触发包络
    env.trigger()
    gain = env.process(int(1.0 * 44100))
    
    print(f"Attack: {env.attack}s")
    print(f"Decay: {env.decay}s")
    print(f"Sustain: {env.sustain}")
    print(f"Release: {env.release}s")
    print(f"包络样本数: {len(gain)}")
    print("✓ 包络发生器正常工作!")

def demo_lfo():
    """演示LFO"""
    print("\n🌊 演示5: LFO调制")
    print("-" * 50)
    
    lfo = LFO(frequency=2.0, wave_type='sine')  # 2Hz = 每秒2个周期
    lfo_wave = lfo.generate(duration=1.0)
    
    print(f"LFO频率: {lfo.frequency} Hz")
    print(f"波形类型: {lfo.wave_type}")
    print(f"LFO范围: [{lfo_wave.min():.3f}, {lfo_wave.max():.3f}]")
    print("✓ LFO正常工作!")

def demo_synth_patch():
    """演示完整合成器音色"""
    print("\n🎹 演示6: 完整合成器音色")
    print("-" * 50)
    print("创建一个简单的Lead音色:")
    
    # 振荡器组合
    multi = MultiOscillator()
    multi.add_oscillator(frequency=220.0, wave_type='sawtooth', gain=0.4)
    multi.add_oscillator(frequency=440.0, wave_type='square', gain=0.3)
    
    # 滤波器
    flt = Filter(cutoff=2000, filter_type='lowpass')
    
    # 包络
    env = Envelope(attack=0.05, decay=0.3, sustain=0.6, release=0.5)
    
    print("  • 振荡器: Saw + Square")
    print("  • 滤波器: Lowpass @ 2000Hz")
    print("  • 包络: Fast attack, medium decay")
    print("✓ Lead音色配置完成!")

def demo_bass_synth():
    """演示贝斯音色"""
    print("\n🎸 演示7: 贝斯合成器")
    print("-" * 50)
    print("创建一个808风格贝斯:")
    
    multi = MultiOscillator()
    multi.add_oscillator(frequency=55.0, wave_type='sine', gain=0.5)  # A1
    multi.add_oscillator(frequency=55.0, wave_type='square', gain=0.5)
    
    flt = Filter(cutoff=800, filter_type='lowpass')
    
    env = Envelope(attack=0.01, decay=0.2, sustain=0.8, release=0.3)
    
    print("  • 振荡器: Sine + Square @ 55Hz")
    print("  • 滤波器: Lowpass @ 800Hz")
    print("  • 包络: Quick attack, punchy")
    print("✓ Bass音色配置完成!")

def demo_pad_synth():
    """演示Pad音色"""
    print("\n🌟 演示8: 氛围Pad")
    print("-" * 50)
    print("创建一个梦幻Pad:")
    
    multi = MultiOscillator()
    multi.add_oscillator(frequency=220.0, wave_type='sine', gain=0.3)  # A3
    multi.add_oscillator(frequency=330.0, wave_type='sine', gain=0.3)  # E4
    multi.add_oscillator(frequency=440.0, wave_type='triangle', gain=0.2)  # A4
    multi.add_oscillator(frequency=550.0, wave_type='sine', gain=0.2)  # C#5
    
    flt = Filter(cutoff=3000, filter_type='lowpass')
    
    env = Envelope(attack=0.5, decay=0.5, sustain=0.8, release=1.5)
    
    print("  • 振荡器: 多正弦波和弦")
    print("  • 滤波器: Soft lowpass")
    print("  • 包络: Slow attack/release")
    print("✓ Pad音色配置完成!")

def print_help():
    """打印帮助信息"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                     使用说明                                ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  运行主程序:                                              ║
║    python main.py                                         ║
║                                                           ║
║  运行测试:                                                ║
║    python -m pytest tests/                               ║
║                                                           ║
║  安装依赖:                                                ║
║    pip install -r requirements.txt                        ║
║                                                           ║
║  未来功能:                                                ║
║    • GUI图形界面                                          ║
║    • 实时音频播放                                         ║
║    • 模块连接可视化                                       ║
║    • 预设音色库                                           ║
║    • 旋律/和声生成                                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)

def main():
    """主函数"""
    print_welcome()
    
    # 检查是否有命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help', 'help']:
            print_help()
            return
        elif sys.argv[1] == '--demo':
            # 运行所有演示
            demo_oscillator()
            demo_multi_oscillator()
            demo_filter()
            demo_envelope()
            demo_lfo()
            demo_synth_patch()
            demo_bass_synth()
            demo_pad_synth()
            
            print("\n" + "="*60)
            print("🎉 所有演示完成!")
            print("="*60)
            print("\n下一步:")
            print("  • 安装依赖: pip install -r requirements.txt")
            print("  • 创建GUI界面")
            print("  • 添加实时音频播放")
            return
    
    # 默认运行基本演示
    demo_oscillator()
    demo_filter()
    demo_envelope()
    
    print("\n" + "="*60)
    print("🎹 Modular Synth Studio 已就绪!")
    print("="*60)
    print("\n使用 --demo 运行完整演示:")
    print("  python main.py --demo")
    print("\n或者运行帮助:")
    print("  python main.py --help")

if __name__ == '__main__':
    main()
