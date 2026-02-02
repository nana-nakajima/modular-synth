"""
🎹 Modular Synth Studio - v0.8.0 音频导出演示
音频导出功能演示脚本
"""

import numpy as np
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audio.audio_exporter import AudioExporter, SynthAudioExporter, AudioFormat, ExportSettings


def demo_basic_export():
    """基础导出演示"""
    print("=" * 60)
    print("🎹 v0.8.0 音频导出功能演示")
    print("=" * 60)
    
    exporter = AudioExporter()
    
    print("\n📁 支持的音频格式:")
    formats = exporter.list_formats()
    for fmt_id, fmt_info in formats.items():
        print(f"\n  [{fmt_id.upper()}] {fmt_info['name']}")
        print(f"    扩展名: {fmt_info['extension']}")
        print(f"    说明: {fmt_info['description']}")
    
    return exporter


def demo_generate_test_audio(sample_rate=44100):
    """生成测试音频"""
    print("\n" + "-" * 60)
    print("🎵 生成测试音频...")
    
    duration = 2.0  # 2秒
    frequency = 440.0  # A4
    
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    
    # 生成一个简单的旋律：C4 -> E4 -> G4 -> C5
    audio_data = np.zeros_like(t)
    
    # 定义音符
    notes = [
        (261.63, 0.0, 0.4),   # C4
        (329.63, 0.5, 0.4),   # E4
        (392.00, 1.0, 0.4),   # G4
        (523.25, 1.5, 0.6),   # C5
    ]
    
    # 生成每个音符
    for freq, start, duration_sec in notes:
        start_sample = int(start * sample_rate)
        end_sample = int((start + duration_sec) * sample_rate)
        
        for i in range(start_sample, min(end_sample, len(t))):
            current_time = (i - start_sample) / sample_rate
            envelope = np.exp(-current_time * 3)  # 简单的衰减包络
            audio_data[i] = np.sin(2 * np.pi * freq * current_time) * 0.3 * envelope
    
    print(f"  生成了 {len(audio_data)} 样本 ({duration}秒)")
    print(f"  采样率: {sample_rate} Hz")
    
    return audio_data, sample_rate


def demo_wav_export(exporter, audio_data, sample_rate):
    """WAV导出演示"""
    print("\n" + "-" * 60)
    print("💾 导出WAV格式...")
    
    settings = ExportSettings(
        format=AudioFormat.WAV,
        sample_rate=sample_rate,
        channels=2,  # 立体声
        bits_per_sample=16,
        normalize=True,
        fade_in_ms=10,
        fade_out_ms=100
    )
    
    result = exporter.export(audio_data, "output/demo_v080.wav", settings)
    
    if result["success"]:
        print(f"  ✅ {result['message']}")
        print(f"  📊 文件大小: {result['file_size_bytes'] / 1024:.1f} KB")
        print(f"  ⏱️ 时长: {result['duration_seconds']:.2f} 秒")
        print(f"  🎵 采样率: {result['sample_rate']} Hz")
        print(f"  🔊 声道数: {result['channels']}")
    else:
        print(f"  ❌ 导出失败: {result['error']}")
    
    return result


def demo_flac_export(exporter, audio_data, sample_rate):
    """FLAC导出演示"""
    print("\n" + "-" * 60)
    print("💾 导出FLAC格式...")
    
    settings = ExportSettings(
        format=AudioFormat.FLAC,
        sample_rate=sample_rate,
        channels=2,
        bits_per_sample=24,
        normalize=True
    )
    
    result = exporter.export(audio_data, "output/demo_v080.flac", settings)
    
    if result["success"]:
        print(f"  ✅ {result['message']}")
        print(f"  📊 文件大小: {result['file_size_bytes'] / 1024:.1f} KB")
        print(f"  ⏱️ 时长: {result['duration_seconds']:.2f} 秒")
        print(f"  🎵 采样率: {result['sample_rate']} Hz")
    else:
        print(f"  ⚠️ {result.get('error', '未知错误')}")
        if result.get('suggestion'):
            print(f"  💡 建议: {result['suggestion']}")
    
    return result


def demo_synth_exporter(sample_rate):
    """合成器导出器演示"""
    print("\n" + "-" * 60)
    print("🎹 合成器音频导出器演示...")
    
    synth_exporter = SynthAudioExporter(sample_rate=sample_rate)
    
    # 定义一个简单的旋律
    melody_notes = [
        (261.63, 0.0, 0.3, 100),   # C4, start, duration, velocity
        (329.63, 0.4, 0.3, 100),   # E4
        (392.00, 0.8, 0.3, 100),   # G4
        (523.25, 1.2, 0.6, 100),   # C5 (长一点)
        (493.88, 2.0, 0.3, 80),    # B4
        (440.00, 2.4, 0.3, 80),    # A4
        (392.00, 2.8, 0.5, 100),   # G4
    ]
    
    print("  旋律音符:")
    for freq, start, dur, vel in melody_notes:
        note_names = {261.63: "C4", 329.63: "E4", 392.00: "G4", 
                      523.25: "C5", 493.88: "B4", 440.00: "A4"}
        note_name = note_names.get(freq, f"{freq:.1f}Hz")
        print(f"    {note_name}: {start}s - {start+dur}s")
    
    result = synth_exporter.export_synth_performance(
        melody_notes,
        "melody_demo",
        "output",
        AudioFormat.WAV,
        duration_seconds=4.0
    )
    
    if result["success"]:
        print(f"\n  ✅ {result['message']}")
    else:
        print(f"\n  ❌ {result.get('error', '未知错误')}")
    
    return result


def demo_batch_export(exporter, sample_rate):
    """批量导出演示"""
    print("\n" + "-" * 60)
    print("📦 批量导出演示...")
    
    # 生成一个简单的正弦波
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    audio_data = np.sin(2 * np.pi * 440 * t) * 0.5
    
    results = []
    
    # 导出不同格式
    for format_type in [AudioFormat.WAV]:
        settings = ExportSettings(
            format=format_type,
            sample_rate=sample_rate,
            channels=1,
            bits_per_sample=16
        )
        
        filename = f"batch_test_{format_type.value}"
        result = exporter.export_performance(
            audio_data, filename, "output", settings
        )
        results.append(result)
        
        if result["success"]:
            print(f"  ✅ {filename}: {result['file_size_bytes'] / 1024:.1f} KB")
    
    return results


def show_usage_info():
    """显示使用信息"""
    print("\n" + "=" * 60)
    print("📖 使用方法")
    print("=" * 60)
    print("""
# 在你的代码中使用音频导出器

from audio.audio_exporter import AudioExporter, AudioFormat, ExportSettings

# 创建导出器
exporter = AudioExporter()

# 导出音频
result = exporter.export(
    audio_data,  # numpy数组，float32，范围-1到1
    "output/my_sound.wav",
    ExportSettings(
        format=AudioFormat.WAV,
        sample_rate=44100,
        channels=2,
        bits_per_sample=16
    )
)

if result["success"]:
    print(result["message"])
""")
    
    print("""
# 使用合成器导出器直接生成和导出

from audio.audio_exporter import SynthAudioExporter, AudioFormat

synth_exporter = SynthAudioExporter()

# 定义音符: (频率, 开始时间, 持续时间, 力度)
notes = [
    (261.63, 0.0, 0.5, 100),  # C4
    (329.63, 0.5, 0.5, 100),  # E4
    (392.00, 1.0, 0.5, 100),  # G4
]

result = synth_exporter.export_synth_performance(
    notes, "my_melody", "output", AudioFormat.WAV
)
""")


def main():
    """主函数"""
    # 确保输出目录存在
    os.makedirs("output", exist_ok=True)
    
    # 运行演示
    exporter = demo_basic_export()
    audio_data, sample_rate = demo_generate_test_audio()
    demo_wav_export(exporter, audio_data, sample_rate)
    demo_flac_export(exporter, audio_data, sample_rate)
    demo_synth_exporter(sample_rate)
    demo_batch_export(exporter, sample_rate)
    show_usage_info()
    
    print("\n" + "=" * 60)
    print("✅ v0.8.0 音频导出演示完成!")
    print("=" * 60)
    
    # 列出输出文件
    print("\n📁 生成的文件:")
    for f in os.listdir("output"):
        if f.startswith("demo_v080") or f.startswith("melody_demo") or f.startswith("batch_test"):
            filepath = os.path.join("output", f)
            size = os.path.getsize(filepath)
            print(f"  📄 {f} ({size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
