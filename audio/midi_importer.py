#!/usr/bin/env python3
# 🎹 MIDI Importer - MIDI文件导入器
# 从MIDI文件导入旋律到合成器

import os
from collections import defaultdict


# ============ 音符转换 ============
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NUM_TO_NOTE = {i: note for i, note in enumerate(NOTES)}


def midi_note_to_name(midi_note):
    """将MIDI音符编号转换为音符名称"""
    octave = (midi_note // 12) - 1
    note_name = NUM_TO_NOTE[midi_note % 12]
    return f"{note_name}{octave}"


def note_name_to_midi(note_name):
    """将音符名称转换为MIDI编号"""
    note = note_name[:-1]
    octave = int(note_name[-1])
    NOTE_TO_NUM = {note: i for i, note in enumerate(NOTES)}
    return NOTE_TO_NUM[note] + (octave + 1) * 12


# ============ MIDI导入器 ============
class MIDIImporter:
    """MIDI文件导入器"""
    
    def __init__(self):
        self.note_events = []
        self.tempo = 120
        self.ticks_per_beat = 480  # 默认值
    
    def _guess_tempo(self, header):
        """从MIDI头猜测节拍"""
        if hasattr(header, 'ticks_per_beat'):
            self.ticks_per_beat = header.ticks_per_beat
        return 120  # 默认B importPM
    
    def import_file(self, filepath, channel_filter=None):
        """
        导入MIDI文件
        
        Args:
            filepath: MIDI文件路径
            channel_filter: 可选，只导入指定通道
        
        Returns:
            dict: 包含melody, tempo, time_signature等信息
        """
        try:
            import mido
        except ImportError:
            print("⚠️ 需要安装 mido 库: pip install mido")
            return {
                'imported': False,
                'error': 'mido not installed',
                'suggestion': 'pip install mido'
            }
        
        if not os.path.exists(filepath):
            return {
                'imported': False,
                'error': f'文件不存在: {filepath}'
            }
        
        try:
            # 打开MIDI文件
            mid = mido.MidiFile(filepath)
            self.ticks_per_beat = mid.ticks_per_beat
            
            # 解析音轨
            tracks_data = self._parse_tracks(mid.tracks, channel_filter)
            
            if not tracks_data['melody']:
                return {
                    'imported': False,
                    'error': '未找到有效的音符数据',
                    'filepath': filepath
                }
            
            print(f"✅ MIDI导入成功: {filepath}")
            print(f"   音符数: {len(tracks_data['melody'])}")
            print(f"   时长: {tracks_data['duration']:.2f}秒")
            
            return {
                'imported': True,
                'melody': tracks_data['melody'],
                'duration': tracks_data['duration'],
                'tempo': tracks_data.get('tempo', 120),
                'time_signature': tracks_data.get('time_signature', (4, 4)),
                'filepath': filepath
            }
            
        except Exception as e:
            return {
                'imported': False,
                'error': str(e),
                'filepath': filepath
            }
    
    def _parse_tracks(self, tracks, channel_filter=None):
        """解析所有音轨"""
        all_notes = []
        tempo = 120
        time_signature = (4, 4)
        
        # 收集所有音轨的音符
        for track in tracks:
            notes = self._parse_track_notes(track, channel_filter)
            all_notes.extend(notes)
        
        # 按时间排序
        all_notes.sort(key=lambda x: x['start_time'])
        
        # 合并重叠音符（保留最长的）
        merged_notes = self._merge_overlapping_notes(all_notes)
        
        # 计算时长
        duration = 0
        if merged_notes:
            max_end = max(n['end_time'] for n in merged_notes)
            duration = max_end
        
        return {
            'melody': merged_notes,
            'duration': duration,
            'tempo': tempo,
            'time_signature': time_signature
        }
    
    def _parse_track_notes(self, track, channel_filter=None):
        """解析单个音轨的音符"""
        notes = []
        current_time = 0
        active_notes = {}  # note_on但没有note_off的音符
        tempo = 120
        
        for msg in track:
            current_time += msg.time
            
            # 解析元消息
            if msg.type == 'set_tempo':
                tempo = int(60000000 / msg.tempo)
            
            # 解析音符消息
            if msg.type in ('note_on', 'note_off'):
                # 检查通道过滤
                if channel_filter is not None and hasattr(msg, 'channel'):
                    if msg.channel != channel_filter:
                        continue
                
                # note_off 或 velocity为0的note_on
                if msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    if msg.note in active_notes:
                        note_info = active_notes.pop(msg.note)
                        note_info['end_time'] = current_time
                        note_info['duration'] = current_time - note_info['start_time']
                        notes.append(note_info)
                # note_on 且 velocity > 0
                elif msg.type == 'note_on' and msg.velocity > 0:
                    # 如果已经有相同的音符在播放，先关闭旧的
                    if msg.note in active_notes:
                        old_note = active_notes.pop(msg.note)
                        old_note['end_time'] = current_time
                        old_note['duration'] = current_time - old_note['start_time']
                        notes.append(old_note)
                    
                    active_notes[msg.note] = {
                        'midi_note': msg.note,
                        'note': midi_note_to_name(msg.note),
                        'start_time': current_time,
                        'velocity': msg.velocity,
                        'channel': getattr(msg, 'channel', 0)
                    }
        
        # 处理还在播放的音符
        for note_info in active_notes.values():
            note_info['end_time'] = current_time
            note_info['duration'] = current_time - note_info['start_time']
            notes.append(note_info)
        
        return notes
    
    def _merge_overlapping_notes(self, notes):
        """合并重叠音符"""
        if not notes:
            return []
        
        # 按开始时间排序
        notes.sort(key=lambda x: x['start_time'])
        
        merged = []
        current_group = []
        
        for note in notes:
            if not current_group:
                current_group = [note]
            else:
                # 检查是否与当前组重叠
                last_note = current_group[-1]
                if note['start_time'] < last_note.get('end_time', float('inf')):
                    current_group.append(note)
                else:
                    # 不重叠，将当前组添加到结果并开始新组
                    merged.extend(self._select_longest(current_group))
                    current_group = [note]
        
        # 处理最后一组
        if current_group:
            merged.extend(self._select_longest(current_group))
        
        return merged
    
    def _select_longest(self, notes):
        """从重叠组中选择最长的音符"""
        if not notes:
            return []
        
        # 按音符分组
        note_groups = defaultdict(list)
        for note in notes:
            note_groups[note['midi_note']].append(note)
        
        # 选择每个音高的最长音符
        result = []
        for midi_note, group in note_groups.items():
            longest = max(group, key=lambda x: x.get('duration', 0))
            result.append(longest)
        
        return result


# ============ MIDI导出器（补充） ============
class MIDIExporter:
    """MIDI文件导出器"""
    
    def __init__(self):
        self.ticks_per_beat = 480
    
    def export_melody(self, melody, filename, tempo=120):
        """
        导出旋律为MIDI文件
        
        Args:
            melody: 旋律列表 [{'note': 'C4', 'duration': 1.0, 'velocity': 80}]
            filename: 输出文件名
            tempo: 节拍速度 (BPM)
        """
        try:
            import mido
            from mido import Message, MidiTrack, MidiFile
        except ImportError:
            print("⚠️ 需要安装 mido 库: pip install mido")
            return {
                'exported': False,
                'error': 'mido not installed'
            }
        
        mid = MidiFile()
        mid.ticks_per_beat = self.ticks_per_beat
        
        # 创建音轨
        track = MidiTrack()
        mid.tracks.append(track)
        
        # 设置速度
        track.append(mido.MetaMessage('set_tempo', tempo=int(60000000 / tempo)))
        
        # 导出音符
        current_time = 0
        for note_data in melody:
            note_str = note_data['note']
            duration = note_data.get('duration', 1.0)
            velocity = note_data.get('velocity', 80)
            
            midi_note = note_name_to_midi(note_str)
            
            # 计算ticks
            duration_ticks = int(duration * self.ticks_per_beat)
            
            # 添加音符
            track.append(Message('note_on', note=midi_note, velocity=velocity, time=0))
            track.append(Message('note_off', note=midi_note, velocity=0, time=duration_ticks))
        
        # 保存文件
        mid.save(filename)
        
        print(f"✅ MIDI导出成功: {filename}")
        return {
            'exported': True,
            'filename': filename
        }
    
    def export_song(self, song_data, filename):
        """
        导出完整歌曲为MIDI文件
        
        Args:
            song_data: 歌曲数据 {'melody': [...], 'chord_progression': [...], 'tempo': 120}
            filename: 输出文件名
        """
        try:
            import mido
            from mido import Message, MidiTrack, MidiFile
        except ImportError:
            return {
                'exported': False,
                'error': 'mido not installed'
            }
        
        mid = MidiFile()
        mid.ticks_per_beat = self.ticks_per_beat
        tempo = song_data.get('tempo', 120)
        
        # 音轨1: 旋律
        melody_track = MidiTrack()
        mid.tracks.append(melody_track)
        melody_track.append(mido.MetaMessage('set_tempo', tempo=int(60000000 / tempo)))
        melody_track.append(mido.MetaMessage('track_name', name='Melody'))
        
        if 'melody' in song_data:
            current_time = 0
            for note_data in song_data['melody']:
                note_str = note_data['note']
                duration = note_data.get('duration', 1.0)
                velocity = note_data.get('velocity', 80)
                
                midi_note = note_name_to_midi(note_str)
                duration_ticks = int(duration * self.ticks_per_beat * 0.8)  # 留一点间隙
                
                melody_track.append(Message('note_on', note=midi_note, velocity=velocity, time=0))
                melody_track.append(Message('note_off', note=midi_note, velocity=0, time=duration_ticks))
                current_time += duration_ticks
        
        # 音轨2: 和弦
        chord_track = MidiTrack()
        mid.tracks.append(chord_track)
        chord_track.append(mido.MetaMessage('set_tempo', tempo=int(60000000 / tempo)))
        chord_track.append(mido.MetaMessage('track_name', name='Chords'))
        
        if 'chord_progression' in song_data:
            current_time = 0
            for chord in song_data['chord_progression']:
                duration = chord.get('duration', 2.0)
                for i, note_str in enumerate(chord['notes']):
                    midi_note = note_name_to_midi(note_str)
                    duration_ticks = int(duration * self.ticks_per_beat * 0.7)
                    # 错开每个音符
                    offset_ticks = int(i * self.ticks_per_beat * 0.05)
                    
                    chord_track.append(Message('note_on', note=midi_note, velocity=60, time=offset_ticks))
                    chord_track.append(Message('note_off', note=midi_note, velocity=0, time=duration_ticks))
                current_time += duration_ticks
        
        # 保存
        mid.save(filename)
        
        print(f"✅ 歌曲MIDI导出成功: {filename}")
        return {
            'exported': True,
            'filename': filename,
            'tracks': 2
        }


# ============ 与旋律生成器集成 ============
class MIDIMelodyAdapter:
    """MIDI与旋律生成器之间的适配器"""
    
    @staticmethod
    def midi_to_melody_generator(midi_data):
        """
        将导入的MIDI数据转换为旋律生成器格式
        
        Args:
            midi_data: MIDI导入结果 {'melody': [...], 'tempo': 120}
        
        Returns:
            list: 适合MelodyGenerator的melody格式
        """
        if not midi_data.get('imported', False):
            return []
        
        melody = []
        for note in midi_data['melody']:
            melody.append({
                'note': note['note'],
                'duration': note.get('duration', 1.0),
                'velocity': note.get('velocity', 80)
            })
        
        return melody
    
    @staticmethod
    def melody_generator_to_midi(melody, filename, tempo=120):
        """
        将旋律生成器的melody导出为MIDI
        
        Args:
            melody: MelodyGenerator生成的melody格式
            filename: 输出文件
            tempo: 节拍速度
        
        Returns:
            dict: 导出结果
        """
        exporter = MIDIExporter()
        return exporter.export_melody(melody, filename, tempo)


# ============ 测试 ============
if __name__ == "__main__":
    print("🎹 MIDI Importer/Exporter 测试")
    print("=" * 40)
    
    # 测试导出
    exporter = MIDIExporter()
    test_melody = [
        {'note': 'C4', 'duration': 1.0, 'velocity': 80},
        {'note': 'E4', 'duration': 1.0, 'velocity': 80},
        {'note': 'G4', 'duration': 1.0, 'velocity': 80},
        {'note': 'B4', 'duration': 1.0, 'velocity': 80},
        {'note': 'C5', 'duration': 2.0, 'velocity': 100},
    ]
    
    result = exporter.export_melody(test_melody, '/tmp/test_export.mid', tempo=120)
    print(f"导出结果: {result}")
    
    # 测试导入
    importer = MIDIImporter()
    import_result = importer.import_file('/tmp/test_export.mid')
    print(f"导入结果: {import_result}")
    
    print("\n✅ MIDI工具测试完成!")
