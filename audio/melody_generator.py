#!/usr/bin/env python3
# 🎵 Melody Generator - 旋律生成器
# 基于规则的智能旋律生成系统

import random
import numpy as np
from enum import Enum


# ============ 音乐理论基础 ============
class ScaleType(Enum):
    """音阶类型"""
    MAJOR = "major"
    MINOR = "minor"
    PENTATONIC_MAJOR = "pentatonic_major"
    PENTATONIC_MINOR = "pentatonic_minor"
    DORIAN = "dorian"
    MIXOLYDIAN = "mixolydian"
    BLUES = "blues"


class ChordType(Enum):
    """和弦类型"""
    MAJOR = "major"
    MINOR = "minor"
    SEVENTH = "seventh"
    MINOR_SEVENTH = "minor_seventh"
    MAJOR_SEVENTH = "major_seventh"
    DIMINISHED = "diminished"
    SUS4 = "sus4"


# ============ 音符和音阶 ============
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_TO_NUM = {note: i for i, note in enumerate(NOTES)}
NUM_TO_NOTE = {i: note for i, note in enumerate(NOTES)}


def get_scale_intervals(scale_type):
    """获取音阶音程"""
    scales = {
        ScaleType.MAJOR: [0, 2, 4, 5, 7, 9, 11],
        ScaleType.MINOR: [0, 2, 3, 5, 7, 8, 10],
        ScaleType.PENTATONIC_MAJOR: [0, 2, 4, 7, 9],
        ScaleType.PENTATONIC_MINOR: [0, 3, 5, 7, 10],
        ScaleType.DORIAN: [0, 2, 3, 5, 7, 9, 10],
        ScaleType.MIXOLYDIAN: [0, 2, 4, 5, 7, 9, 10],
        ScaleType.BLUES: [0, 3, 5, 6, 7, 10],
    }
    return scales.get(scale_type, scales[ScaleType.MAJOR])


def get_scale_notes(root_note, scale_type):
    """获取指定根音的音阶所有音符"""
    root_idx = NOTE_TO_NUM[root_note]
    intervals = get_scale_intervals(scale_type)
    return [NUM_TO_NOTE[(root_idx + interval) % 12] for interval in intervals]


def note_to_frequency(note, octave=4):
    """将音符转换为频率"""
    note_name = note[:-1] if len(note) > 1 else note
    octave_offset = int(note[-1]) if len(note) > 1 else octave
    semitone = NOTE_TO_NUM[note_name]
    return 440 * (2 ** ((semitone + (octave_offset - 4) * 12 - 9) / 12))


# ============ 旋律生成器 ============
class MelodyGenerator:
    """智能旋律生成器"""
    
    def __init__(self, root_note='C', scale_type=ScaleType.MAJOR, octave_range=(3, 5)):
        self.root_note = root_note
        self.scale_type = scale_type
        self.octave_range = octave_range
        self.scale_notes = get_scale_notes(root_note, scale_type)
        
        # 生成参数
        self.tempo = 120  # BPM
        self.note_lengths = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]  # 拍数
        
        # 旋律模式库
        self.melodic_patterns = [
            # 上下行
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            # 波浪
            [1, 2, 3, 2, 1, 2, 3, 4],
            # 跳跃
            [1, 3, 5, 3, 1],
            # 重复
            [1, 2, 1, 2, 3, 4],
        ]
        
        # 节奏模式库
        self.rhythm_patterns = [
            [1, 0.5, 0.5, 1, 1],      # 标准
            [0.5, 0.5, 0.5, 0.5, 1, 1],  # 快速
            [1, 1, 0.5, 0.5, 1],      # 推进
            [0.25] * 8,               # 碎拍
            [1.5, 0.5, 1, 1],         # 切分
        ]
    
    def set_scale(self, root_note, scale_type):
        """设置音阶"""
        self.root_note = root_note
        self.scale_type = scale_type
        self.scale_notes = get_scale_notes(root_note, scale_type)
    
    def scale_degree_to_note(self, degree, octave=None):
        """将音阶级数转换为音符"""
        degree = degree % len(self.scale_notes)
        if octave is None:
            octave = random.randint(*self.octave_range)
        
        # 计算实际音符
        note_idx = degree % len(self.scale_notes)
        octave_offset = degree // len(self.scale_notes)
        actual_octave = octave + octave_offset
        
        return f"{self.scale_notes[note_idx]}{actual_octave}"
    
    def generate_melody(self, length=8, use_pattern=True, vary_rhythm=True):
        """生成旋律"""
        melody = []
        
        if use_pattern:
            pattern = random.choice(self.melodic_patterns)
            rhythm = random.choice(self.rhythm_patterns)
            
            for i in range(min(length, len(pattern))):
                note = self.scale_degree_to_note(pattern[i])
                duration = rhythm[i % len(rhythm)] if vary_rhythm else random.choice(self.note_lengths)
                melody.append({
                    'note': note,
                    'duration': duration,
                    'velocity': random.randint(60, 100)
                })
        else:
            for i in range(length):
                degree = random.randint(0, len(self.scale_notes) * 2 - 1)
                note = self.scale_degree_to_note(degree)
                duration = random.choice(self.note_lengths)
                melody.append({
                    'note': note,
                    'duration': duration,
                    'velocity': random.randint(60, 100)
                })
        
        return melody
    
    def generate_melody_with_rules(self, length=8):
        """基于音乐规则生成旋律"""
        melody = []
        current_degree = random.randint(0, len(self.scale_notes) - 1)
        
        for i in range(length):
            # 根据位置选择移动方向
            if i == 0:
                # 开头：从主音或属音开始
                current_degree = random.choice([0, 4])
            elif i == length - 1:
                # 结尾：回到主音
                target_degree = 0
            else:
                # 中间：基于规则选择
                rule = random.random()
                
                if rule < 0.3:
                    # 级进 (30%)
                    direction = random.choice([-1, 1])
                    current_degree = (current_degree + direction) % len(self.scale_notes)
                elif rule < 0.5:
                    # 跳进 (20%)
                    jump = random.choice([-3, -2, 2, 3])
                    current_degree = (current_degree + jump) % len(self.scale_notes)
                elif rule < 0.7:
                    # 重复 (20%)
                    pass  # 保持当前音
                else:
                    # 回到主音方向 (30%)
                    if current_degree > 3:
                        current_degree = max(0, current_degree - 1)
                    elif current_degree < 3:
                        current_degree = min(len(self.scale_notes) - 1, current_degree + 1)
            
            note = self.scale_degree_to_note(current_degree)
            duration = self._get_rhythm_for_position(i, length)
            
            melody.append({
                'note': note,
                'duration': duration,
                'velocity': random.randint(70, 100)
            })
        
        return melody
    
    def _get_rhythm_for_position(self, position, total_length):
        """根据位置生成节奏"""
        if position == 0:
            return random.choice([1.0, 1.5, 2.0])  # 开头：长音符
        elif position == total_length - 1:
            return random.choice([1.0, 2.0, 4.0])  # 结尾：长音符
        else:
            return random.choice([0.25, 0.5, 0.75, 1.0])  # 中间：灵活
    
    def generate_arpeggio(self, chord_notes, pattern='up', octaves=1):
        """生成琶音"""
        arpeggio = []
        notes_with_octave = []
        
        for octave in range(octaves):
            for i, note in enumerate(chord_notes):
                note_name = note[:-1] if len(note) > 1 else note
                note_octave = int(note[-1]) if len(note) > 1 else 4
                full_note = f"{note_name}{note_octave + octave}"
                notes_with_octave.append(full_note)
        
        if pattern == 'up':
            pass  # 保持原序
        elif pattern == 'down':
            notes_with_octave.reverse()
        elif pattern == 'up-down':
            notes_with_octave = notes_with_octave + notes_with_octave[-2:0:-1]
        elif pattern == 'random':
            random.shuffle(notes_with_octave)
        
        for note in notes_with_octave:
            arpeggio.append({
                'note': note,
                'duration': 0.25,
                'velocity': 80
            })
        
        return arpeggio


# ============ 和弦进行生成器 ============
class ChordProgressionGenerator:
    """和弦进行生成器"""
    
    def __init__(self, root_note='C', scale_type=ScaleType.MAJOR):
        self.root_note = root_note
        self.scale_type = scale_type
        self.scale_notes = get_scale_notes(root_note, scale_type)
        
        # 经典和弦进行
        self.classic_progressions = {
            'pop': [
                ['I', 'V', 'vi', 'IV'],
                ['I', 'IV', 'V', 'IV'],
                ['vi', 'IV', 'I', 'V'],
                ['I', 'vi', 'IV', 'V'],
            ],
            'jazz': [
                ['ii', 'V', 'I'],
                ['ii', 'V', 'I', 'vi'],
                ['I', 'vi', 'ii', 'V'],
            ],
            'rock': [
                ['I', 'IV', 'V'],
                ['I', 'IV', 'I', 'V'],
                ['I', 'bVII', 'IV'],
            ],
            'minor': [
                ['i', 'VI', 'III', 'VII'],
                ['i', 'iv', 'VII', 'VI'],
                ['i', 'VII', 'VI', 'V'],
            ]
        }
    
    def get_chord_from_degree(self, degree_symbol):
        """从级数获取和弦"""
        degree_map = {
            'I': 0, 'II': 1, 'III': 2, 'IV': 3, 'V': 4, 'VI': 5, 'VII': 6,
            'i': 0, 'ii': 1, 'iii': 2, 'iv': 3, 'v': 4, 'vi': 5, 'vii': 6,
            'bIII': 2, 'bVI': 5, 'bVII': 6,
        }
        
        roman = degree_symbol.upper().replace('B', 'b')
        degree = degree_map.get(roman, 0)
        
        # 确定大小调
        is_minor = roman.islower() or 'b' in roman
        
        # 构建和弦音符
        intervals = [0, 4, 7] if not is_minor else [0, 3, 7]
        if '7' in roman:
            intervals.append(11) if not is_minor else intervals.append(10)
        
        chord_notes = []
        for interval in intervals:
            note_idx = (NOTE_TO_NUM[self.root_note] + degree + interval) % 12
            chord_notes.append(f"{NUM_TO_NOTE[note_idx]}{4}")
        
        return chord_notes
    
    def generate_progression(self, style='pop', length=4):
        """生成和弦进行"""
        progressions = self.classic_progressions.get(style, self.classic_progressions['pop'])
        pattern = random.choice(progressions)
        
        progression = []
        for i, chord_symbol in enumerate(pattern[:length]):
            chord_notes = self.get_chord_from_degree(chord_symbol)
            progression.append({
                'symbol': chord_symbol,
                'notes': chord_notes,
                'duration': 2.0 if i < length - 1 else 4.0,
                'type': 'minor' if chord_symbol.islower() or 'b' in chord_symbol else 'major'
            })
        
        return progression


# ============ 节奏模式生成器 ============
class RhythmPatternGenerator:
    """节奏模式生成器"""
    
    def __init__(self, tempo=120):
        self.tempo = tempo
        self.beat_duration = 60 / tempo
        
        # 预设节奏模式
        self.patterns = {
            'basic': [1, 0, 1, 0, 1, 0, 1, 0],
            'syncopated': [1, 0, 0.5, 0.5, 1, 0, 1, 0],
            'shuffle': [1, 0, 1, 0, 1, 0, 1, 0],
            'halftime': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            'double': [0.5, 0, 0.5, 0, 0.5, 0, 0.5, 0],
        }
    
    def generate_pattern(self, length=8, style='basic'):
        """生成节奏模式"""
        pattern = self.patterns.get(style, self.patterns['basic'])
        
        # 填充或截断到指定长度
        if len(pattern) < length:
            pattern = pattern * (length // len(pattern) + 1)
        pattern = pattern[:length]
        
        return pattern
    
    def pattern_to_timestamps(self, pattern):
        """将模式转换为时间戳"""
        timestamps = []
        current_time = 0
        
        for beat in pattern:
            if beat > 0:
                timestamps.append(current_time)
            current_time += beat * self.beat_duration
        
        return timestamps


# ============ 综合音乐生成器 ============
class MusicGenerator:
    """综合音乐生成器"""
    
    def __init__(self, root_note='C', scale_type=ScaleType.MAJOR, tempo=120):
        self.melody_gen = MelodyGenerator(root_note, scale_type)
        self.chord_gen = ChordProgressionGenerator(root_note, scale_type)
        self.rhythm_gen = RhythmPatternGenerator(tempo)
        self.tempo = tempo
    
    def generate_song(self, bars=8, style='pop', include_arpeggio=True):
        """生成完整歌曲"""
        song = {
            'tempo': self.tempo,
            'root_note': self.melody_gen.root_note,
            'scale': self.melody_gen.scale_type.value,
            'chord_progression': [],
            'melody': [],
            'arpeggios': [],
            'rhythm': [],
        }
        
        # 生成和弦进行
        num_chords = min(bars // 2 + 1, 8)
        song['chord_progression'] = self.chord_gen.generate_progression(style, num_chords)
        
        # 生成旋律
        song['melody'] = self.melody_gen.generate_melody_with_rules(bars * 2)
        
        # 生成节奏
        song['rhythm'] = self.rhythm_gen.generate_pattern(bars * 4, style)
        
        # 生成琶音（如果需要）
        if include_arpeggio and song['chord_progression']:
            for chord in song['chord_progression']:
                arpeggio = self.melody_gen.generate_arpeggio(
                    chord['notes'], 
                    pattern='up-down'
                )
                song['arpeggios'].append({
                    'chord': chord['symbol'],
                    'pattern': arpeggio
                })
        
        return song
    
    def generate_melody_data(self, length=16):
        """生成旋律数据（适合音频引擎使用）"""
        melody = self.melody_gen.generate_melody_with_rules(length)
        
        # 转换为频率序列
        frequencies = []
        durations = []
        
        for note_data in melody:
            freq = note_to_frequency(note_data['note'])
            frequencies.append(freq)
            durations.append(note_data['duration'])
        
        return {
            'frequencies': frequencies,
            'durations': durations,
            'velocities': [n['velocity'] for n in melody],
        }
    
    def export_to_midi(self, song_data, filename):
        """导出为MIDI文件"""
        try:
            from midiutil import MIDIFile
        except ImportError:
            # 如果没有安装 midiutil，返回占位
            print("⚠️ midiutil 未安装，跳过 MIDI 导出")
            return {
                'exported': False,
                'error': 'midiutil not installed',
                'filename': filename
            }
        
        # 创建 MIDI 文件 (2个音轨: 1=旋律, 2=和弦)
        midi = MIDIFile(2)
        
        tempo = song_data.get('tempo', 120)
        
        # 音轨1: 旋律
        track1 = 0
        midi.addTempo(track1, 0, tempo)
        midi.addProgramChange(track1, 0, 0, 0)  # 钢琴
        
        if 'melody' in song_data:
            current_time = 0
            for note_data in song_data['melody']:
                note_str = note_data['note']
                duration = note_data['duration']
                velocity = note_data.get('velocity', 80)
                
                note_name = note_str[:-1]
                octave = int(note_str[-1])
                midi_note = NOTE_TO_NUM[note_name] + (octave + 1) * 12
                midi.addNote(track1, 0, midi_note, current_time, duration * 0.8, velocity)
                current_time += duration
        
        # 音轨2: 和弦
        track2 = 1
        midi.addTempo(track2, 0, tempo)
        midi.addProgramChange(track2, 0, 0, 40)  # 弦乐
        
        if 'chord_progression' in song_data:
            current_time = 0
            for chord in song_data['chord_progression']:
                duration = chord.get('duration', 2.0)
                for i, note_str in enumerate(chord['notes']):
                    note_name = note_str[:-1]
                    octave = int(note_str[-1])
                    midi_note = NOTE_TO_NUM[note_name] + (octave + 1) * 12
                    # 稍微错开每个音符的起始时间，避免重叠
                    midi.addNote(track2, 0, midi_note, current_time + i * 0.05, duration * 0.7, 60)
                current_time += duration
        
        # 写入文件
        with open(filename, 'wb') as f:
            midi.writeFile(f)
        
        print(f"✅ MIDI 文件已保存: {filename}")
        return {
            'exported': True,
            'filename': filename,
            'tempo': tempo
        }


# ============ 测试 ============
if __name__ == "__main__":
    # 测试旋律生成器
    print("🎵 测试旋律生成器")
    print("=" * 40)
    
    gen = MusicGenerator(root_note='C', scale_type=ScaleType.MINOR, tempo=120)
    
    # 生成旋律
    melody_data = gen.generate_melody_data(8)
    print("\n旋律数据:")
    print(f"频率: {melody_data['frequencies']}")
    print(f"时长: {melody_data['durations']}")
    
    # 生成完整歌曲
    song = gen.generate_song(bars=4, style='pop')
    print("\n歌曲结构:")
    print(f"和弦进行: {[c['symbol'] for c in song['chord_progression']]}")
    print(f"旋律长度: {len(song['melody'])} 小节")
    
    print("\n✅ 旋律生成器测试完成!")
