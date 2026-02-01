#!/usr/bin/env python3
# 🎹 MIDI Export Demo - v0.4.0 MIDI 导出功能演示

import sys
import os

# 添加路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from audio.melody_generator import MusicGenerator, ScaleType


def demo_midi_export():
    """演示 MIDI 导出功能"""
    print("🎹 Modular Synth Studio - MIDI Export Demo")
    print("=" * 50)
    
    # 创建音乐生成器
    gen = MusicGenerator(root_note='C', scale_type=ScaleType.MAJOR, tempo=120)
    
    # 生成一首歌曲
    print("\n🎵 生成歌曲数据...")
    song = gen.generate_song(bars=8, style='pop', include_arpeggio=True)
    
    print(f"📊 歌曲信息:")
    print(f"   - 速度: {song['tempo']} BPM")
    print(f"   - 根音: {song['root_note']}")
    print(f"   - 音阶: {song['scale']}")
    print(f"   - 和弦进行: {[c['symbol'] for c in song['chord_progression']]}")
    print(f"   - 旋律长度: {len(song['melody'])} 音符")
    
    # 导出为 MIDI
    output_dir = os.path.join(SCRIPT_DIR, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "demo_song.mid")
    
    print(f"\n💾 导出 MIDI 文件...")
    result = gen.export_to_midi(song, output_file)
    
    if result.get('exported'):
        print(f"\n✅ MIDI 导出成功!")
        print(f"   文件: {result['filename']}")
        print(f"   速度: {result['tempo']} BPM")
        print(f"   时长: {result.get('duration_seconds', 'N/A')} 秒")
        
        # 验证文件
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"   大小: {file_size} bytes")
    else:
        print(f"\n❌ MIDI 导出失败: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 50)
    print("✨ MIDI 导出测试完成!")


if __name__ == "__main__":
    demo_midi_export()
