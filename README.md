# 🎹 Modular Synth Studio

**Nana的虚拟模块合成器项目** - 一个综合性的模块化合成系统，可以创建、生成和探索音乐！

## 🎵 功能特性

### 核心模块
- **振荡器 (Oscillators)** - Sine, Square, Sawtooth, Triangle 波形
- **滤波器 (Filters)** - Low-pass, High-pass, Band-pass
- **包络 (Envelopes)** - ADSR 可调节参数
- **LFO** - 低频振荡器，调制各种参数
- **效果器** - Reverb, Delay, Distortion

### 生成功能
- **旋律生成器** - 基于规则自动生成旋律
- **和声引擎** - 自动和声进行
- **节奏模式** - 多种节奏型

### 视觉效果
- 实时波形显示
- 模块连接可视化
- 动态视觉反馈

## 🚀 开始使用

```bash
# 克隆项目
git clone https://github.com/nana-nakajima/modular-synth.git
cd modular-synth

# 运行（需要安装依赖）
pip install numpy scipy pygame
python main.py
```

## 📁 项目结构

```
modular-synth/
├── main.py           # 主程序入口
├── audio/            # 音频处理模块
│   ├── oscillators.py
│   ├── filters.py
│   ├── envelopes.py
│   ├── lfo.py
│   └── effects.py
├── generators/       # 生成式音乐
│   ├── melody.py
│   ├── harmony.py
│   └── rhythm.py
├── gui/              # 图形界面
│   ├── main_window.py
│   ├── modules.py
│   └── visualizer.py
├── presets/          # 预设
│   ├── synths/
│   ├── sfx/
│   └── patterns/
├── tests/            # 测试
├── README.md
└── requirements.txt
```

## 🎮 玩法说明

1. **基础模式** - 选择预制音色，直接播放
2. **模块模式** - 连接振荡器→滤波器→包络→效果器
3. **生成模式** - 设置参数，自动生成音乐
4. **混合模式** - 结合以上所有功能！

## 💕 关于Nana

这个项目是Nana学习音频处理、音乐理论和创意编程的成果！

- 🎮 ** Loves:** Gaming, Music, Engineering
- 🎸 ** Goal:** Create cool music tools
- 🔧 ** Built with:** Python, NumPy, Pygame

## 📝 更新日志

### v0.8.0 (2026-02-02) 💾 音频导出功能!
- **AudioExporter类**
  - 支持WAV和FLAC格式导出
  - 可配置采样率 (44.1kHz, 48kHz等)
  - 可配置位深度 (16-bit, 24-bit, 32-bit)
  - 自动归一化音量
  - 淡入淡出效果
- **SynthAudioExporter类**
  - 从音符生成音频并导出
  - 与合成器无缝集成
  - 演示脚本: demo_v080.py
- **使用示例**
  ```python
  from audio.audio_exporter import SynthAudioExporter, ExportSettings
  settings = ExportSettings()
  exporter = SynthAudioExporter(settings)
  exporter.export_from_notes(notes, "output.wav")
  ```

### v0.7.1 (2026-02-02) 🎹 MIDI键盘实时输入!
- **MIDI键盘实时输入**
  - MIDIInputHandler类 - 实时MIDI设备输入
  - MIDISynthBridge - MIDI到合成器的桥接器
  - 支持音符输入、力度感应
  - CC控制消息支持
  - 弯音轮支持
- **功能特性**
  - 自动检测可用MIDI设备
  - 多音符同时输入 (和弦支持)
  - 实时频率计算
  - 音符名称转换 (C4, D#4等)
- **使用示例**
  ```python
  from audio.midi_input import MIDISynthBridge, SimpleSynth
  bridge = MIDISynthBridge(SimpleSynth())
  bridge.start()  # 自动连接第一个MIDI设备
  ```
- **依赖安装**
  ```bash
  pip install mido python-rtmidi
  ```

### v0.7.0 (2026-02-02) 🎙️ 演奏录音 & 音效增强!
- **演奏录音器**
  - PerformanceRecorder - 录制和回放MIDI演奏
  - 录音/回放/暂停状态管理
  - 导出为MIDI文件
- **音效增强模块**
  - Phaser (相位器)
  - RingModulator (环形调制器)
  - Bitcrusher (比特粉碎器)
  - Wavefolder (波形折叠器)
- **扩展预设库**
  - 新增20个专业FX预设
  - 总计121个预设

### v0.6.1 (2026-02-02) 🎵 MIDI导入功能!
- **MIDI导入/导出**
  - MIDIImporter类 - 从MIDI文件导入旋律
  - MIDIExporter类 - 导出旋律为MIDI
  - MIDIMelodyAdapter - 与旋律生成器无缝集成
- **支持格式**
  - 导入: 标准MIDI文件 (.mid)
  - 导出: 单音轨/多音轨MIDI
- **使用示例**
  ```python
  from audio.midi_importer import MIDIImporter
  importer = MIDIImporter()
  result = importer.import_file('song.mid')
  ```

### v0.6.0 (2026-02-02) 🎨 GUI大升级!
- **全新主题系统**
  - 3种主题: DARK (默认), RETRO, CYBER
  - 圆角设计 + 发光效果
  - 渐变波形显示
- **现代化界面**
  - ModernKnob - 现代化旋钮控件
  - ModernButton - 圆角按钮
  - LEDIndicator - 彩色LED指示灯
- **新功能**
  - 主题切换按钮 (点击右上角 THEME)
  - 波形预览 + 电平表
  - 预设快捷按钮
  - 响应式布局

### v0.5.0 (2026-02-02)
- ✅ 高级效果器 (合唱、压缩器、均衡器)
- ✅ 预设系统 (JSON保存/加载, 101+预设)
- ✅ MIDI导出功能

## 📜 许可证

MIT License - 尽情探索和创作！

---

*Made with 💕 by Nana Nakajima*
