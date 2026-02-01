#!/usr/bin/env python3
# 🎹 测试实时音频播放

import sys
import time

# 测试实时播放器
try:
    from audio.real_time_player import RealTimeSynth

    print("🎹 测试实时音频合成器")
    print("="*50)
    print("按键: A-S-D-F-G-H-J-K (演奏音符)")
    print("Q: 退出")
    print("+/-: 调节音量")
    print("1-4: 切换波形 (1=Sine, 2=Sawtooth, 3=Square, 4=Triangle)")
    print("W/↑: 提高滤波器频率")
    print("S/↓: 降低滤波器频率")
    print("="*50)

    synth = RealTimeSynth()
    synth.start()

    print("\n🎵 实时音频引擎已启动！按任意键演奏...")

    note_names = {
        'a': 'C4', 's': 'D4', 'd': 'E4', 'f': 'F4',
        'g': 'G4', 'h': 'A4', 'j': 'B4', 'k': 'C5'
    }

    wave_names = {
        'sine': '正弦波', 'sawtooth': '锯齿波',
        'square': '方波', 'triangle': '三角波'
    }

    try:
        while True:
            key = input("\n按键 > ").strip().lower()

            if key == 'q':
                print("\n👋 退出测试")
                break

            elif key == '+':
                synth.set_volume(synth.volume + 0.1)
                print(f"🔊 音量: {synth.volume:.1f}")

            elif key == '-':
                synth.set_volume(synth.volume - 0.1)
                print(f"🔉 音量: {synth.volume:.1f}")

            elif key in ['1', '2', '3', '4']:
                waves = ['sine', 'sawtooth', 'square', 'triangle']
                synth.set_wave_type(waves[int(key)-1])
                print(f"🌊 波形: {wave_names[waves[int(key)-1]]}")

            elif key in synth.note_frequencies:
                synth.note_on(key)
                print(f"🎵 按下: {key.upper()} = {note_names[key]}")

            else:
                synth.note_off()
                print("🔇 释放")

    except KeyboardInterrupt:
        print("\n\n⏹️ 测试中断")
    finally:
        synth.stop()
        print("✅ 测试完成")

except ImportError as e:
    print(f"❌ 无法导入实时音频模块: {e}")
    print("请安装 sounddevice: pip install sounddevice")
    sys.exit(1)
