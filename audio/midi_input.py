"""
MIDI Input Handler - 实时MIDI键盘输入支持
"""

import mido
import threading
import time
from typing import Callable, Optional, List
from enum import Enum


class MIDIDeviceType(Enum):
    """MIDI设备类型"""
    KEYBOARD = "keyboard"
    PAD = "pad"
    CONTROLLER = "controller"
    UNKNOWN = "unknown"


class MIDIInputHandler:
    """MIDI输入处理器"""
    
    def __init__(self):
        self.port: Optional[mido.PortIO] = None
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self callbacks: List[Callable] = []
        self.current_note = None
        self.notes_pressed: set = set()
        
    def get_input_ports(self) -> List[str]:
        """获取可用的MIDI输入端口"""
        return mido.get_input_names()
    
    def get_output_ports(self) -> List[str]:
        """获取可用的MIDI输出端口"""
        return mido.get_output_names()
    
    def open_input(self, port_name: Optional[str] = None) -> bool:
        """打开MIDI输入端口"""
        try:
            if port_name is None:
                # 自动选择第一个可用端口
                ports = self.get_input_ports()
                if not ports:
                    print("❌ 没有找到MIDI输入设备")
                    return False
                port_name = ports[0]
                print(f"🎹 自动选择 MIDI 设备: {port_name}")
            
            self.port = mido.open_input(port_name)
            print(f"✅ 已连接到 MIDI 输入: {port_name}")
            return True
        except Exception as e:
            print(f"❌ MIDI连接失败: {e}")
            return False
    
    def close(self):
        """关闭MIDI输入端口"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)
        if self.port:
            self.port.close()
            self.port = None
        print("🔇 MIDI输入已关闭")
    
    def add_callback(self, callback: Callable[[dict], None]):
        """添加音符回调函数"""
        self.callbacks.append(callback)
    
    def _notify_callbacks(self, data: dict):
        """通知所有回调函数"""
        for callback in self.callbacks:
            try:
                callback(data)
            except Exception as e:
                print(f"⚠️ 回调错误: {e}")
    
    def _process_message(self, msg):
        """处理MIDI消息"""
        if msg.type == 'note_on':
            if msg.velocity > 0:
                # 按下音符
                self.notes_pressed.add(msg.note)
                self.current_note = msg.note
                self._notify_callbacks({
                    'type': 'note_on',
                    'note': msg.note,
                    'velocity': msg.velocity,
                    'channel': msg.channel
                })
            else:
                # 释放音符 (note_on with velocity 0 = note_off)
                self.notes_pressed.discard(msg.note)
                if msg.note == self.current_note:
                    self.current_note = None
                self._notify_callbacks({
                    'type': 'note_off',
                    'note': msg.note,
                    'velocity': 0,
                    'channel': msg.channel
                })
        
        elif msg.type == 'note_off':
            self.notes_pressed.discard(msg.note)
            if msg.note == self.current_note:
                self.current_note = None
            self._notify_callbacks({
                'type': 'note_off',
                'note': msg.note,
                'velocity': msg.velocity,
                'channel': msg.channel
            })
        
        elif msg.type == 'control_change':
            self._notify_callbacks({
                'type': 'control_change',
                'control': msg.control,
                'value': msg.value,
                'channel': msg.channel
            })
        
        elif msg.type == 'pitchwheel':
            self._notify_callbacks({
                'type': 'pitch_bend',
                'value': msg.pitch,
                'channel': msg.channel
            })
    
    def start_listening(self):
        """开始监听MIDI输入"""
        if self.running or not self.port:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        print("👂 开始监听MIDI输入...")
    
    def _listen_loop(self):
        """MIDI监听循环"""
        try:
            for msg in self.port:
                if not self.running:
                    break
                self._process_message(msg)
        except Exception as e:
            print(f"⚠️ MIDI监听错误: {e}")
    
    def get_pressed_notes(self) -> set:
        """获取当前按下的音符"""
        return self.notes_pressed.copy()
    
    def get_current_note(self) -> Optional[int]:
        """获取当前按下的音符(单音模式)"""
        return self.current_note
    
    def note_to_frequency(self, note: int) -> float:
        """将MIDI音符转换为频率"""
        return 440 * (2 ** ((note - 69) / 12))
    
    def note_to_name(self, note: int) -> str:
        """将MIDI音符转换为音符名称"""
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 
                      'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = note // 12 - 1
        name = note_names[note % 12]
        return f"{name}{octave}"


class MIDISynthBridge:
    """MIDI到合成器的桥接器"""
    
    def __init__(self, synth=None):
        self.midi = MIDIInputHandler()
        self.synth = synth
        self.active = False
        
        # 设置默认回调
        self.midi.add_callback(self._on_midi_message)
    
    def connect_synth(self, synth):
        """连接合成器"""
        self.synth = synth
    
    def _on_midi_message(self, data: dict):
        """处理MIDI消息并触发合成器"""
        if not self.synth:
            return
        
        msg_type = data['type']
        
        if msg_type == 'note_on':
            note = data['note']
            velocity = data['velocity']
            freq = self.midi.note_to_frequency(note)
            
            # 触发合成器
            if hasattr(self.synth, 'note_on'):
                self.synth.note_on(freq, velocity / 127)
            
            print(f"🎵 音符: {self.midi.note_to_name(note)} ({note}) | 频率: {freq:.1f}Hz | 力度: {velocity}")
        
        elif msg_type == 'note_off':
            if hasattr(self.synth, 'note_off'):
                self.synth.note_off()
        
        elif msg_type == 'control_change':
            control = data['control']
            value = data['value']
            # 可扩展: 处理旋钮、推子等
            print(f"🎛️ 控制: CC{control} = {value}")
        
        elif msg_type == 'pitch_bend':
            value = data['value']
            if hasattr(self.synth, 'set_pitch_bend'):
                # 映射到 -1 到 1
                bend = (value - 8192) / 8192
                self.synth.set_pitch_bend(bend)
    
    def start(self, port_name: Optional[str] = None) -> bool:
        """启动MIDI键盘支持"""
        if not self.midi.open_input(port_name):
            return False
        
        self.midi.start_listening()
        self.active = True
        return True
    
    def stop(self):
        """停止MIDI键盘支持"""
        self.active = False
        self.midi.close()
    
    def list_devices(self):
        """列出可用的MIDI设备"""
        inputs = self.midi.get_input_ports()
        outputs = self.midi.get_output_ports()
        
        print("\n🎹 可用的MIDI设备:")
        print(f"  输入设备 ({len(inputs)}):")
        for i, port in enumerate(inputs):
            print(f"    {i+1}. {port}")
        
        print(f"  输出设备 ({len(outputs)}):")
        for i, port in enumerate(outputs):
            print(f"    {i+1}. {port}")


# 简单的合成器示例
class SimpleSynth:
    """简单的合成器用于测试"""
    
    def __init__(self):
        self.amplitude = 0.5
        self.frequency = 440.0
        self.active = False
    
    def note_on(self, freq, vel):
        self.frequency = freq
        self.amplitude = vel * 0.8
        self.active = True
        print(f"🔊 声音开启: {freq:.1f}Hz, 音量: {self.amplitude:.2f}")
    
    def note_off(self):
        self.active = False
        print("🔇 声音关闭")
    
    def set_pitch_bend(self, bend):
        # 简单的弯音
        self.frequency *= (2 ** (bend / 12))


if __name__ == "__main__":
    # 测试 MIDI 输入
    print("🎹 MIDI 键盘测试程序")
    print("=" * 40)
    
    bridge = MIDISynthBridge(SimpleSynth())
    
    # 列出设备
    bridge.list_devices()
    
    print("\n🔌 尝试连接 MIDI 键盘...")
    if bridge.start():
        print("✅ MIDI 键盘已连接! 按下键盘上的音符来测试.")
        print("按 Ctrl+C 退出\n")
        
        try:
            # 保持运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 正在关闭...")
            bridge.stop()
    else:
        print("❌ 无法连接 MIDI 键盘")
        print("请确保:")
        print("  1. MIDI 键盘已连接到电脑")
        print("  2. 已安装必要的驱动")
        print("  3. 运行: pip install mido python-rtmidi")
