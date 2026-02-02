#!/usr/bin/env python3
# 🎵 MIDI Import Demo - MIDI导入演示
# 演示MIDI导入功能的用法

import sys
import os

# 添加音频模块到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audio.melody_generator import MusicGenerator, ScaleType, NOTE_TO_NUM
from audio.midi_importer import MIDIImporter, MIDIExporter, MIDIMelodyAdapter


def test_midi_export_import():
    """测试MIDI导出和导入"""
    print("🎵 测试 MIDI 导出 → 导入 循环")
    print("=" * 50)
    
    # 1. 生成测试旋律
    print("\n1. 生成测试旋律...")
    gen = MusicGenerator(root_note='C', scale_type=ScaleType.MAJOR, tempo=120)
    song = gen.generate_song(bars=4, style='pop', include_arpeggio=True)
    
    print(f"   旋律长度: {len(song['melody'])} 音符")
    print(f"   和弦进行: {[c['symbol'] for c in song['chord_progression']]}")
    
    # 2. 导出为MIDI
    print("\n2. 导出为MIDI文件...")
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    exporter = MIDIExporter()
    export_result = exporter.export_song(song, f'{output_dir}/test_song.mid')
    print(f"   导出结果: {export_result}")
    
    # 3. 导入MIDI
    print("\n3. 导入MIDI文件...")
    importer = MIDIImporter()
    import_result = importer.import_file(f'{output_dir}/test_song.mid')
    
    if import_result['imported']:
        print(f"   ✅ 导入成功!")
        print(f"   - 音符数: {len(import_result['melody'])}")
        print(f"   - 时长: {import_result['duration']:.2f}秒")
        print(f"   - 节拍: {import_result['tempo']} BPM")
        
        # 4. 显示前几个音符
        print("\n4. 导入的音符预览:")
        for i, note in enumerate(import_result['melody'][:5]):
            print(f"   {i+1}. {note['note']} - {note['duration']:.2f}拍 - 力度:{note['velocity']}")
        if len(import_result['melody']) > 5:
            print(f"   ... 共 {len(import_result['melody'])} 音符")
        
        # 5. 转换为旋律生成器格式
        print("\n5. 转换为旋律生成器格式...")
        adapted = MIDIMelodyAdapter.midi_to_melody_generator(import_result)
        print(f"   适配后的旋律长度: {len(adapted)} 音符")
        
        return True
    else:
        print(f"   ❌ 导入失败: {import_result.get('error')}")
        return False


def test_simple_export():
    """测试简单旋律导出"""
    print("\n🎹 测试简单旋律导出")
    print("=" * 50)
    
    exporter = MIDIExporter()
    
    # 创建简单旋律
    melody = [
        {'note': 'C4', 'duration': 1.0, 'velocity': 80},
        {'note': 'D4', 'duration': 0.5, 'velocity': 80},
        {'note': 'E4', 'duration': 0.5, 'velocity': 80},
        {'note': 'F4', 'duration': 1.0, 'velocity': 80},
        {'note': 'G4', 'duration': 1.0, 'velocity': 100},
        {'note': 'A4', 'duration': 1.0, 'velocity': 100},
        {'note': 'B4', 'duration': 0.5, 'velocity': 100},
        {'note': 'C5', 'duration': 0.5, 'velocity': 100},
        {'note': 'B4', 'duration': 0.5, 'velocity': 90},
        {'note': 'A4', 'duration': 0.5, 'velocity': 90},
        {'note': 'G4', 'duration': 1.0, 'velocity': 80},
        {'note': 'F4', 'duration': 2.0, 'velocity': 80},
    ]
    
    result = exporter.export_melody(melody, 'output/simple_melody.mid', tempo=100)
    print(f"导出结果: {result}")
    
    return result.get('exported', False)


def create_sample_midi():
    """创建一个示例MIDI文件用于测试"""
    print("\n🎼 创建示例MIDI文件")
    print("=" * 50)
    
    # 创建一个简单的琶音MIDI
    exporter = MIDIExporter()
    
    arpeggio = []
    notes = ['C3', 'E3', 'G3', 'B3', 'C4', 'B3', 'G3', 'E3']
    
    for i, note in enumerate(notes):
        arpeggio.append({
            'note': note,
            'duration': 0.5,
            'velocity': 70 + (i % 2) * 20  # 交替力度
        })
    
    result = exporter.export_melody(arpeggio, 'output/arpeggio.mid', tempo=80)
    print(f"琶音MIDI: {result}")
    
    return result.get('exported', False)


def main():
    """主测试函数"""
    print("🎹 Modular Synth - MIDI功能测试")
    print("=" * 50)
    
    # 确保output目录存在
    os.makedirs('output', exist_ok=True)
    
    # 运行测试
    success = True
    
    # 测试1: 简单导出
    if not test_simple_export():
        success = False
    
    # 测试2: 创建示例
    if not create_sample_midi():
        success = False
    
    # 测试3: 完整循环
    if not test_midi_export_import():
        success = False
    
    # 总结
    print("\n" + "=" * 50)
    if success:
        print("🎉 所有测试通过!")
        print("\n生成的文件:")
        print("  - output/simple_melody.mid")
        print("  - output/arpeggio.mid")
        print("  - output/test_song.mid")
    else:
        print("❌ 部分测试失败")
    
    print("\n📖 使用方法:")
    print("  导入MIDI:")
    print("    from audio.midi_importer import MIDIImporter")
    print("    importer = MIDIImporter()")
    print("    result = importer.import_file('your_file.mid')")
    print()
    print("  导出旋律:")
    print("    from audio.midi_importer import MIDIExporter")
    print("    exporter = MIDIExporter()")
    print("    exporter.export_melody(melody, 'output.mid')")


if __name__ == "__main__":
    main()
