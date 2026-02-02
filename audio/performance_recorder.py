"""
演奏录音器 v0.7.0
录制和回放MIDI演奏
"""

import time
import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class RecordingState(Enum):
    """录音状态"""
    IDLE = "idle"
    RECORDING = "recording"
    PLAYING = "playing"
    PAUSED = "paused"


@dataclass
class NoteEvent:
    """音符事件"""
    note: int  # MIDI音符 (0-127)
    velocity: int  # 力度 (0-127)
    start_time: float  # 开始时间（秒）
    duration: float = 0  # 持续时间（秒）
    channel: int = 0  # MIDI通道


@dataclass
class PerformanceTrack:
    """演奏轨道"""
    name: str
    events: List[NoteEvent] = field(default_factory=list)
    tempo: int = 120  # BPM
    time_signature: Tuple[int, int] = (4, 4)  # 拍号
    start_time: float = 0  # 整体开始时间


class PerformanceRecorder:
    """演奏录音器"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.state = RecordingState.IDLE
        self.current_track: Optional[PerformanceTrack] = None
        self.recorded_tracks: List[PerformanceTrack] = []
        
        # 录音状态
        self.recording_start_time: float = 0
        self.note_start_times: Dict[int, float] = {}  # 音符 -> 开始时间
        self.active_notes: Dict[int, int] = {}  # 音符 -> 力度
        
        # 回放状态
        self.playback_track: Optional[PerformanceTrack] = None
        self.playback_index: int = 0
        self.playback_start_time: float = 0
        self.pause_time: float = 0
        
        # 回调函数
        self.on_note_on: Optional[callable] = None
        self.on_note_off: Optional[callable] = None
        
        # 线程锁
        self.lock = threading.Lock()
    
    def start_recording(self, name: str = "新演奏") -> PerformanceTrack:
        """开始录音"""
        with self.lock:
            if self.state == RecordingState.RECORDING:
                return None
            
            self.current_track = PerformanceTrack(name=name)
            self.recording_start_time = time.time()
            self.note_start_times = {}
            self.active_notes = {}
            self.state = RecordingState.RECORDING
            
            print(f"🎙️ 开始录音: {name}")
            return self.current_track
    
    def stop_recording(self) -> Optional[PerformanceTrack]:
        """停止录音"""
        with self.lock:
            if self.state != RecordingState.RECORDING:
                return None
            
            # 完成所有未关闭的音符
            current_time = time.time() - self.recording_start_time
            for note, start_time in self.note_start_times.items():
                if note in self.active_notes:
                    duration = current_time - start_time
                    event = NoteEvent(
                        note=note,
                        velocity=self.active_notes[note],
                        start_time=start_time,
                        duration=duration
                    )
                    self.current_track.events.append(event)
            
            track = self.current_track
            self.recorded_tracks.append(track)
            self.current_track = None
            self.state = RecordingState.IDLE
            
            print(f"🎙️ 录音完成: {track.name} ({len(track.events)} 个音符)")
            return track
    
    def record_note_on(self, note: int, velocity: int, channel: int = 0):
        """记录音符按下"""
        with self.lock:
            if self.state == RecordingState.RECORDING:
                current_time = time.time() - self.recording_start_time
                self.note_start_times[note] = current_time
                self.active_notes[note] = velocity
                
                # 回调
                if self.on_note_on:
                    self.on_note_on(note, velocity, channel)
    
    def record_note_off(self, note: int, channel: int = 0):
        """记录音符释放"""
        with self.lock:
            if self.state == RecordingState.RECORDING:
                if note in self.note_start_times:
                    current_time = time.time() - self.recording_start_time
                    start_time = self.note_start_times[note]
                    duration = current_time - start_time
                    velocity = self.active_notes.get(note, 100)
                    
                    event = NoteEvent(
                        note=note,
                        velocity=velocity,
                        start_time=start_time,
                        duration=duration,
                        channel=channel
                    )
                    self.current_track.events.append(event)
                    
                    del self.note_start_times[note]
                    del self.active_notes[note]
                    
                    # 回调
                    if self.on_note_off:
                        self.on_note_off(note, channel)
    
    def start_playback(self, track: PerformanceTrack) -> bool:
        """开始回放"""
        with self.lock:
            if not track or self.state == RecordingState.RECORDING:
                return False
            
            self.playback_track = track
            self.playback_index = 0
            self.playback_start_time = time.time()
            self.state = RecordingState.PLAYING
            
            print(f"▶️ 开始回放: {track.name}")
            return True
    
    def pause_playback(self):
        """暂停回放"""
        with self.lock:
            if self.state == RecordingState.PLAYING:
                self.pause_time = time.time()
                self.state = RecordingState.PAUSED
                print("⏸️ 暂停回放")
    
    def resume_playback(self):
        """继续回放"""
        with self.lock:
            if self.state == RecordingState.PAUSED:
                # 调整开始时间以补偿暂停时间
                pause_duration = time.time() - self.pause_time
                self.playback_start_time += pause_duration
                self.state = RecordingState.PLAYING
                print("▶️ 继续回放")
    
    def stop_playback(self):
        """停止回放"""
        with self.lock:
            self.playback_track = None
            self.playback_index = 0
            self.state = RecordingState.IDLE
            print("⏹️ 停止回放")
    
    def update(self) -> List[Tuple[str, int, int]]:
        """更新回放状态，返回当前应该播放的音符事件
        返回: [(event_type, note, velocity), ...]
        """
        with self.lock:
            if self.state != RecordingState.PLAYING or not self.playback_track:
                return []
            
            current_time = time.time() - self.playback_start_time
            events = self.playback_track.events
            result = []
            
            # 查找当前时间点的事件
            while self.playback_index < len(events):
                event = events[self.playback_index]
                
                if event.start_time <= current_time:
                    # 音符按下
                    if event.velocity > 0:
                        result.append(("on", event.note, event.velocity))
                    
                    # 音符释放（如果有持续时间）
                    if event.duration > 0:
                        release_time = event.start_time + event.duration
                        if release_time <= current_time:
                            result.append(("off", event.note, 0))
                            self.playback_index += 1
                            continue
                    
                    self.playback_index += 1
                else:
                    break
            
            return result
    
    def get_recorded_tracks(self) -> List[PerformanceTrack]:
        """获取所有录音轨道"""
        return self.recorded_tracks
    
    def delete_track(self, index: int) -> bool:
        """删除录音轨道"""
        with self.lock:
            if 0 <= index < len(self.recorded_tracks):
                del self.recorded_tracks[index]
                return True
            return False
    
    def export_to_midi(self, track: PerformanceTrack, filename: str):
        """导出为MIDI文件"""
        try:
            from midiutil import MIDIFile
            
            # 创建MIDI文件（1个轨道）
            midi = MIDIFile(1)
            track_index = 0
            
            # 设置轨道信息
            midi.addTrackName(track_index, 0, track.name)
            midi.addTempo(track_index, 0, track.tempo)
            
            # 转换音符事件
            for event in track.events:
                # 转换时间（秒）到节拍
                time_in_beats = event.start_time * (track.tempo / 60)
                duration_in_beats = event.duration * (track.tempo / 60)
                
                # 添加音符
                if event.velocity > 0:
                    midi.addNote(
                        track_index, 
                        event.channel,
                        event.note,
                        time_in_beats,
                        duration_in_beats,
                        event.velocity
                    )
            
            # 写入文件
            with open(filename, 'wb') as f:
                midi.writeFile(f)
            
            print(f"💾 导出MIDI: {filename}")
            return True
            
        except ImportError:
            print("❌ 需要安装 midiutil: pip install midiutil")
            return False
        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return False
    
    def get_state(self) -> str:
        """获取当前状态"""
        return self.state.value
    
    def get_track_count(self) -> int:
        """获取录音数量"""
        return len(self.recorded_tracks)
