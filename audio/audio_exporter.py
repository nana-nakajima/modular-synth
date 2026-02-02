"""
🎹 音频导出模块 v0.8.0
支持导出音频为WAV和FLAC格式
"""

import numpy as np
import os
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import json


class AudioFormat(Enum):
    """支持的音频格式"""
    WAV = "wav"
    FLAC = "flac"


@dataclass
class ExportSettings:
    """导出设置"""
    format: AudioFormat = AudioFormat.WAV
    sample_rate: int = 44100
    channels: int = 2  # 1=单声道, 2=立体声
    bits_per_sample: int = 16  # 16, 24, 32
    normalize: bool = True  # 自动归一化音量
    fade_in_ms: int = 10  # 淡入毫秒
    fade_out_ms: int = 100  # 淡出毫秒


class AudioExporter:
    """音频导出器"""
    
    # 格式对应文件扩展名
    FORMAT_EXTENSIONS = {
        AudioFormat.WAV: ".wav",
        AudioFormat.FLAC: ".flac",
    }
    
    def __init__(self, settings: Optional[ExportSettings] = None):
        """初始化导出器
        
        Args:
            settings: 导出设置，如果不提供则使用默认设置
        """
        self.settings = settings or ExportSettings()
        self.supported_formats = [fmt.value for fmt in AudioFormat]
    
    def export(
        self,
        audio_data: np.ndarray,
        filepath: str,
        settings: Optional[ExportSettings] = None,
    ) -> Dict[str, Any]:
        """导出音频文件
        
        Args:
            audio_data: 音频数据 (numpy数组，float32，范围-1到1)
            filepath: 输出文件路径
            settings: 覆盖设置
            
        Returns:
            导出结果信息
        """
        effective_settings = settings or self.settings
        
        # 验证音频数据
        if audio_data is None or len(audio_data) == 0:
            return {"success": False, "error": "音频数据为空"}
        
        # 确保是float32
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32)
        
        # 应用设置
        export_data = self._apply_settings(audio_data, effective_settings)
        
        # 确保输出目录存在
        output_dir = Path(filepath).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 根据格式导出
        format_type = effective_settings.format
        
        try:
            if format_type == AudioFormat.WAV:
                return self._export_wav(export_data, filepath, effective_settings)
            elif format_type == AudioFormat.FLAC:
                return self._export_flac(export_data, filepath, effective_settings)
            else:
                return {"success": False, "error": f"不支持的格式: {format_type}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _apply_settings(
        self,
        audio_data: np.ndarray,
        settings: ExportSettings
    ) -> np.ndarray:
        """应用导出设置"""
        processed = audio_data.copy()
        
        # 归一化
        if settings.normalize:
            max_val = np.max(np.abs(processed))
            if max_val > 0:
                processed = processed / max_val * 0.95  # 留出3dB余量
        
        # 转换为指定声道数
        if settings.channels == 2 and len(processed.shape) == 1:
            # 单声道转立体声
            processed = np.column_stack([processed, processed])
        elif settings.channels == 1 and len(processed.shape) == 2:
            # 立体声转单声道
            processed = np.mean(processed, axis=1)
        
        # 淡入淡出
        if settings.fade_in_ms > 0:
            fade_samples = int(settings.fade_in_ms * settings.sample_rate / 1000)
            fade_in = np.linspace(0, 1, fade_samples)
            # 确保fade_in可以广播到所有通道
            fade_in = fade_in.reshape(-1, 1) if len(processed.shape) > 1 else fade_in
            processed[:fade_samples] *= fade_in
        
        if settings.fade_out_ms > 0:
            fade_samples = int(settings.fade_out_ms * settings.sample_rate / 1000)
            fade_out = np.linspace(1, 0, fade_samples)
            # 确保fade_out可以广播到所有通道
            fade_out = fade_out.reshape(-1, 1) if len(processed.shape) > 1 else fade_out
            processed[-fade_samples:] *= fade_out
        
        return processed
    
    def _export_wav(
        self,
        audio_data: np.ndarray,
        filepath: str,
        settings: ExportSettings
    ) -> Dict[str, Any]:
        """导出WAV文件"""
        try:
            from scipy.io import wavfile
            
            # 根据位深度转换数据类型
            if settings.bits_per_sample == 16:
                audio_int = (audio_data * 32767).astype(np.int16)
            elif settings.bits_per_sample == 24:
                # 24位需要特殊处理
                audio_int = (audio_data * 8388607).astype(np.int32)
            elif settings.bits_per_sample == 32:
                audio_int = (audio_data * 2147483647).astype(np.int32)
            else:
                audio_int = (audio_data * 32767).astype(np.int16)
            
            # 写入WAV文件
            wavfile.write(
                filepath,
                settings.sample_rate,
                audio_int
            )
            
            file_size = os.path.getsize(filepath)
            duration = len(audio_data) / settings.sample_rate
            
            return {
                "success": True,
                "format": "WAV",
                "filepath": filepath,
                "file_size_bytes": file_size,
                "duration_seconds": duration,
                "sample_rate": settings.sample_rate,
                "channels": settings.channels,
                "bits_per_sample": settings.bits_per_sample,
                "message": f"✅ 导出成功: {filepath}"
            }
            
        except ImportError:
            # 如果scipy不可用，尝试使用wave模块
            return self._export_wav_native(audio_data, filepath, settings)
    
    def _export_wav_native(
        self,
        audio_data: np.ndarray,
        filepath: str,
        settings: ExportSettings
    ) -> Dict[str, Any]:
        """使用标准库导出WAV"""
        import wave
        import struct
        
        # 转换为16位整数
        audio_int = (audio_data * 32767).astype(np.int16)
        
        # 获取文件大小
        num_samples = len(audio_int.flatten())
        byte_rate = settings.sample_rate * settings.channels * 2  # 16 bits = 2 bytes
        data_size = num_samples * settings.channels * 2
        file_size = 36 + data_size  # RIFF header size + data size
        
        # 写入WAV
        with wave.open(filepath, 'wb') as wav_file:
            wav_file.setnchannels(settings.channels)
            wav_file.setsampwidth(2)  # 2 bytes = 16 bits
            wav_file.setframerate(settings.sample_rate)
            
            # 转换为字节
            audio_bytes = b''.join(
                struct.pack('<h', sample) for sample in audio_int.flatten()
            )
            wav_file.writeframes(audio_bytes)
        
        duration = num_samples / (settings.sample_rate * settings.channels)
        
        return {
            "success": True,
            "format": "WAV",
            "filepath": filepath,
            "file_size_bytes": file_size,
            "duration_seconds": duration,
            "sample_rate": settings.sample_rate,
            "channels": settings.channels,
            "bits_per_sample": 16,
            "message": f"✅ 导出成功: {filepath}"
        }
    
    def _export_flac(
        self,
        audio_data: np.ndarray,
        filepath: str,
        settings: ExportSettings
    ) -> Dict[str, Any]:
        """导出FLAC文件"""
        try:
            import soundfile as sf
            
            # FLAC支持多种格式
            if settings.bits_per_sample == 24:
                subtype = 'PCM_24'
            elif settings.bits_per_sample == 16:
                subtype = 'PCM_16'
            else:
                subtype = 'PCM_16'
            
            sf.write(
                filepath,
                audio_data,
                settings.sample_rate,
                subtype=subtype
            )
            
            file_size = os.path.getsize(filepath)
            duration = len(audio_data) / settings.sample_rate
            
            return {
                "success": True,
                "format": "FLAC",
                "filepath": filepath,
                "file_size_bytes": file_size,
                "duration_seconds": duration,
                "sample_rate": settings.sample_rate,
                "channels": settings.channels,
                "bits_per_sample": settings.bits_per_sample,
                "message": f"✅ FLAC导出成功: {filepath}"
            }
            
        except ImportError:
            return {
                "success": False,
                "error": "需要安装 soundfile: pip install soundfile",
                "suggestion": "或者使用WAV格式导出"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def export_performance(
        self,
        audio_data: np.ndarray,
        filename: str,
        directory: str = "output",
        settings: Optional[ExportSettings] = None
    ) -> Dict[str, Any]:
        """便捷方法：导出演奏录音
        
        Args:
            audio_data: 音频数据
            filename: 文件名（不含扩展名）
            directory: 输出目录
            settings: 导出设置
            
        Returns:
            导出结果
        """
        effective_settings = settings or self.settings
        
        # 构建完整路径
        ext = self.FORMAT_EXTENSIONS[effective_settings.format]
        filepath = os.path.join(directory, f"{filename}{ext}")
        
        # 导出
        return self.export(audio_data, filepath, effective_settings)
    
    def get_format_info(self, format_type: AudioFormat) -> Dict[str, Any]:
        """获取格式信息"""
        info = {
            AudioFormat.WAV: {
                "name": "WAV (Waveform Audio File Format)",
                "extension": ".wav",
                "description": "无损音频格式，Windows标准",
                " Pros": ["兼容性最好", "无需额外依赖"],
                "cons": ["文件较大"],
            },
            AudioFormat.FLAC: {
                "name": "FLAC (Free Lossless Audio Codec)",
                "extension": ".flac",
                "description": "开源无损压缩格式",
                "pros": ["文件小", "无损质量", "开源"],
                "cons": ["需要soundfile库"],
            },
        }
        return info.get(format_type, {})
    
    def list_formats(self) -> Dict[str, Dict[str, Any]]:
        """列出所有支持的格式"""
        return {
            fmt.value: self.get_format_info(fmt) 
            for fmt in AudioFormat
        }


# ============ 导出演示器 ============

class SynthAudioExporter:
    """合成器音频导出器 - 从演奏生成音频"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.exporter = AudioExporter()
    
    def generate_audio_from_notes(
        self,
        notes: list,
        duration_seconds: float = 5.0,
        wave_type: str = "sawtooth"
    ) -> np.ndarray:
        """从音符列表生成音频数据
        
        Args:
            notes: [(frequency, start_time, duration, velocity), ...]
            duration_seconds: 总时长
            wave_type: 波形类型
            
        Returns:
            音频数据数组
        """
        # 创建振荡器
        from .core_modules import Oscillator, Envelope
        
        oscillator = Oscillator(wave_type=wave_type, sample_rate=self.sample_rate)
        envelope = Envelope(attack=0.01, decay=0.2, sustain=0.5, release=0.3, sample_rate=self.sample_rate)
        
        # 生成音频
        num_samples = int(duration_seconds * self.sample_rate)
        audio_data = np.zeros(num_samples, dtype=np.float32)
        
        # 跟踪当前活动的音符
        active_note = None
        
        for i in range(num_samples):
            current_time = i / self.sample_rate
            
            # 检查当前时间点应该播放哪个音符
            new_active = None
            for freq, start, dur, vel in notes:
                if start <= current_time < start + dur:
                    new_active = (freq, vel)
                    break
            
            # 如果音符改变
            if new_active != active_note:
                if new_active is None:
                    # 释放当前音符
                    envelope.release_envelope()
                else:
                    # 触发新音符
                    oscillator.set_frequency(new_active[0])
                    envelope.trigger()
                active_note = new_active
            
            # 生成样本
            if active_note:
                freq, vel = active_note
                oscillator.set_frequency(freq)
                sample = oscillator.process_sample()
                env = envelope.process(1)[0]  # 处理1个样本
                audio_data[i] = sample * env * (vel / 127.0)
            else:
                audio_data[i] = 0.0
        
        return audio_data
    
    def export_synth_performance(
        self,
        notes: list,
        filename: str,
        directory: str = "output",
        format_type: AudioFormat = AudioFormat.WAV,
        duration_seconds: float = 5.0
    ) -> Dict[str, Any]:
        """导出合成器演奏
        
        Args:
            notes: 音符列表
            filename: 文件名
            directory: 输出目录
            format_type: 音频格式
            duration_seconds: 时长
            
        Returns:
            导出结果
        """
        # 生成音频
        audio_data = self.generate_audio_from_notes(notes, duration_seconds)
        
        # 设置导出格式
        settings = ExportSettings(
            format=format_type,
            sample_rate=self.sample_rate,
            channels=2,
            bits_per_sample=16,
            normalize=True,
            fade_in_ms=10,
            fade_out_ms=100
        )
        
        # 导出
        return self.exporter.export_performance(
            audio_data, filename, directory, settings
        )


# ============ 测试代码 ============

if __name__ == "__main__":
    print("🎹 音频导出器测试")
    print("=" * 50)
    
    # 创建导出器
    exporter = AudioExporter()
    
    # 显示支持的格式
    print("📁 支持的音频格式:")
    formats = exporter.list_formats()
    for fmt_id, fmt_info in formats.items():
        print(f"  [{fmt_id.upper()}] {fmt_info['name']}")
        print(f"      {fmt_info['description']}")
    
    print("\n🎵 测试音频生成...")
    
    # 生成测试音频 (1秒的正弦波)
    sample_rate = 44100
    duration = 1.0
    frequency = 440.0  # A4
    
    t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
    test_audio = np.sin(2 * np.pi * frequency * t) * 0.5
    
    print(f"  生成 {duration}秒 的 {frequency}Hz 正弦波")
    print(f"  音频数据: {len(test_audio)} 样本")
    
    # 测试WAV导出
    print("\n💾 测试WAV导出...")
    settings = ExportSettings(
        format=AudioFormat.WAV,
        sample_rate=sample_rate,
        channels=1,
        bits_per_sample=16,
        normalize=True
    )
    
    result = exporter.export(test_audio, "output/test_output.wav", settings)
    print(f"  结果: {result.get('message', result.get('error', '未知'))}")
    
    # 测试FLAC导出 (需要soundfile)
    print("\n💾 测试FLAC导出...")
    result_flac = exporter.export(test_audio, "output/test_output.flac", settings)
    print(f"  结果: {result_flac.get('message', result_flac.get('error', '未知'))}")
    
    # 测试合成器导出器
    print("\n🎹 测试合成器音频导出...")
    synth_exporter = SynthAudioExporter(sample_rate=sample_rate)
    
    # 定义一些音符
    notes = [
        (261.63, 0.0, 0.5, 100),   # C4, 从0秒开始, 持续0.5秒
        (329.63, 0.5, 0.5, 100),   # E4, 从0.5秒开始
        (392.00, 1.0, 0.5, 100),   # G4, 从1.0秒开始
        (523.25, 1.5, 1.0, 100),   # C5, 从1.5秒开始
    ]
    
    result_synth = synth_exporter.export_synth_performance(
        notes, "test_synth", "output", AudioFormat.WAV, duration_seconds=3.0
    )
    print(f"  结果: {result_synth.get('message', result_synth.get('error', '未知'))}")
    
    print("\n" + "=" * 50)
    print("✅ 测试完成!")
    print(f"📁 输出文件保存在: output/")
