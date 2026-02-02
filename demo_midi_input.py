#!/usr/bin/env python3
"""
MIDI Keyboard Input Demo - MIDI键盘输入演示
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from audio.midi_input import MIDIInputHandler, MIDISynthBridge, SimpleSynth
import time


def main():
    print("🎹 Modular Synth Studio - MIDI键盘输入演示")
    print("=" * 50)
    
    # 创建MIDI处理器和合成器
    handler = MIDIInputHandler()
    synth = SimpleSynth()
    bridge = MIDISynthBridge(synth)
    
    # 列出可用的MIDI设备
    bridge.list_devices()
    
    print("\n🔌 正在尝试连接MIDI键盘...")
    
    # 尝试连接 (自动选择第一个设备)
    if bridge.start():
        print("\n✅ MIDI键盘连接成功!")
        print("-" * 50)
        print("操作说明:")
        print("  • 按下音符键 → 触发声音")
               print("  • 释放音符键 → 停止声音")
        print("  • 移动旋钮/推子 → 显示CC值")
        print("  • 弯音轮 → 改变音高")
        print("-" * 50)
        print("按 Ctrl+C 退出")
        print()
        
        try:
            while True:
                time.sleep(0.1)
                # 可选: 显示当前按下的音符
                notes = handler.get_pressed_notes()
                if notes:
                    note = list(notes)[-1]  # 最后一个按下的音符
                    print(f"📝 当前音符: {handler.note_to_name(note)} ({note}) | 频率: {handler.note_to_frequency(note):.1f}Hz")
        except KeyboardInterrupt:
            print("\n\n🛑 正在关闭...")
    
    else:
        print("\n❌ 无法连接MIDI键盘")
        print("\n可能的原因:")
        print("  1. 没有连接MIDI设备")
        print("  2. 设备正被其他程序占用")
        print("  3. 需要安装驱动")
        print("\n安装依赖:")
        print("  pip install mido python-rtmidi")
        
        # 列出所有可用的端口名称
        print("\n可用的MIDI端口:")
        print(f"  输入: {handler.get_input_ports()}")
        print(f"  输出: {handler.get_output_ports()}")


def test_with_virtual_port():
    """测试虚拟MIDI端口"""
    print("\n🔧 测试模式: 虚拟MIDI端口")
    print("=" * 50)
    
    handler = MIDIInputHandler()
    inputs = handler.get_input_ports()
    
    if not inputs:
        print("❌ 没有可用的MIDI输入端口")
        print("\n在macOS上创建虚拟端口:")
        print("  1. 安装: brew install coreutils")
        print("  2. 使用: https://github.com/cvacker/macMIDI/releases")
        return
    
    print(f"找到 {len(inputs)} 个MIDI输入端口:")
    for i, port in enumerate(inputs):
        print(f"  {i+1}. {port}")
    
    # 选择端口
    if len(inputs) == 1:
        port_name = inputs[0]
    else:
        try:
            choice = int(input(f"选择端口 (1-{len(inputs)}): ")) - 1
            port_name = inputs[choice]
        except:
            port_name = inputs[0]
    
    print(f"\n连接到: {port_name}")
    
    # 创建简单的测试回调
    def test_callback(data):
        if data['type'] == 'note_on':
            print(f"🎵 收到音符: {data['note']} (力度: {data['velocity']})")
    
    handler.add_callback(test_callback)
    
    if handler.open_input(port_name):
        print("✅ 端口已打开，开始监听...")
        handler.start_listening()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            handler.close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_with_virtual_port()
    else:
        main()
