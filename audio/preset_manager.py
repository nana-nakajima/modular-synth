# 🎹 预设管理系统 v0.5.0
# JSON格式保存/加载音色预设

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

# ============ 预设库 ============

class Preset:
    """音色预设"""
    
    def __init__(self, name: str, category: str = 'User'):
        self.name = name
        self.category = category
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        
        # 振荡器设置
        self.oscillators: List[Dict[str, Any]] = []
        
        # 滤波器设置
        self.filter = {
            'type': 'lowpass',
            'cutoff': 2000,
            'resonance': 1.0,
            'enabled': True
        }
        
        # 包络设置
        self.envelope = {
            'attack': 0.01,
            'decay': 0.2,
            'sustain': 0.7,
            'release': 0.3,
            'enabled': True
        }
        
        # LFO设置
        self.lfo = {
            'wave_type': 'sine',
            'frequency': 5.0,
            'enabled': False,
            'modulates': []  # ['filter', 'pitch', 'amplitude']
        }
        
        # 效果器设置
        self.effects = {
            'distortion': {'enabled': False, 'drive': 5, 'mix': 0.5},
            'reverb': {'enabled': False, 'room_size': 0.5, 'damping': 0.5, 'mix': 0.3},
            'delay': {'enabled': False, 'time': 0.3, 'feedback': 0.3, 'mix': 0.3},
            'chorus': {'enabled': False, 'rate': 0.5, 'depth': 0.003, 'mix': 0.5},
            'compressor': {'enabled': False, 'threshold_db': -20, 'ratio': 4, 'makeup_gain_db': 0},
            'eq': {'enabled': False, 'bands': []}
        }
        
        # 其他设置
        self.master_volume = 0.8
        self.transpose = 0
        self.description = ""
        self.tags: List[str] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'category': self.category,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'oscillators': self.oscillators,
            'filter': self.filter,
            'envelope': self.envelope,
            'lfo': self.lfo,
            'effects': self.effects,
            'master_volume': self.master_volume,
            'transpose': self.transpose,
            'description': self.description,
            'tags': self.tags,
            'version': '0.5.0'
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Preset':
        """从字典创建"""
        preset = cls(name=data['name'], category=data.get('category', 'User'))
        preset.created_at = data.get('created_at', datetime.now().isoformat())
        preset.updated_at = data.get('updated_at', datetime.now().isoformat())
        preset.oscillators = data.get('oscillators', [])
        preset.filter = data.get('filter', preset.filter)
        preset.envelope = data.get('envelope', preset.envelope)
        preset.lfo = data.get('lfo', preset.lfo)
        preset.effects = data.get('effects', preset.effects)
        preset.master_volume = data.get('master_volume', 0.8)
        preset.transpose = data.get('transpose', 0)
        preset.description = data.get('description', '')
        preset.tags = data.get('tags', [])
        return preset


class PresetLibrary:
    """预设库管理器"""
    
    def __init__(self, library_path: str = None):
        """初始化预设库
        
        Args:
            library_path: 预设库路径，默认使用内置预设
        """
        self.presets: Dict[str, Preset] = {}
        self.library_path = library_path
        self.current_category = 'All'
        
        # 加载预设
        if library_path and os.path.exists(library_path):
            self.load_library(library_path)
        else:
            self._create_default_presets()
    
    def _create_default_presets(self):
        """创建默认预设库"""
        # Lead 预设
        lead_presets = [
            ('Classic Saw Lead', 'Lead', '经典锯齿波主音', ['classic', 'synth', 'lead']),
            ('Super Saw Stack', 'Lead', '超级锯齿堆叠', ['supersaw', 'chord', 'rich']),
            ('80s Synth Lead', 'Lead', '80年代合成主音', ['retro', '80s', 'vintage']),
            ('Square Pulse', 'Lead', '方波脉冲', ['square', 'digital', 'retro']),
            ('Acid Lead', 'Lead', 'Acid风格主音', ['acid', 'tb-303', ' distortion']),
            ('Soft Pad Lead', 'Lead', '柔软垫式主音', ['soft', 'pad', 'warm']),
            ('Bright Lead', 'Lead', '明亮主音', ['bright', 'clean', 'modern']),
            ('Aggressive Lead', 'Lead', '激进主音', ['aggressive', 'hard', 'distorted']),
            ('Ethereal Lead', 'Lead', '空灵主音', ['ethereal', 'dreamy', 'ambient']),
            ('Pulsing Lead', 'Lead', '脉冲主音', ['pulsing', 'rhythmic', 'electronic'])
        ]
        
        for name, category, desc, tags in lead_presets:
            preset = Preset(name, category)
            preset.oscillators = [
                {'frequency': 440, 'wave_type': 'sawtooth', 'gain': 0.6},
                {'frequency': 445, 'wave_type': 'sawtooth', 'gain': 0.4}
            ]
            preset.filter = {'type': 'lowpass', 'cutoff': 3000, 'resonance': 2.0, 'enabled': True}
            preset.envelope = {'attack': 0.01, 'decay': 0.1, 'sustain': 0.8, 'release': 0.5, 'enabled': True}
            preset.description = desc
            preset.tags = tags
            self.add_preset(preset)
        
        # Bass 预设
        bass_presets = [
            ('808 Style Bass', 'Bass', '经典808贝斯', ['808', 'kick', 'sub']),
            ('Deep Sub Bass', 'Bass', '深沉低音', ['sub', 'deep', 'cinematic']),
            ('Acid Bass', 'Bass', 'Acid贝斯', ['acid', 'tb-303', 'resonant']),
            ('Retro Bass', 'Bass', '复古贝斯', ['retro', '8-bit', 'nes']),
            ('Wobble Bass', 'Bass', '摆动贝斯', ['wobble', 'dubstep', ' modulation']),
            ('Fat Bass', 'Bass', '肥厚贝斯', ['fat', 'rich', 'distorted']),
            ('Pluck Bass', 'Bass', '弹拨贝斯', ['pluck', 'picked', 'acoustic']),
            (' Reese Bass', 'Bass', 'Reese风格贝斯', ['reese', 'dnb', 'heavy']),
            ('FM Bass', 'Bass', 'FM合成贝斯', ['fm', 'digital', 'metallic']),
            ('Clean Bass', 'Bass', '干净贝斯', ['clean', 'studio', 'pristine'])
        ]
        
        for name, category, desc, tags in bass_presets:
            preset = Preset(name, category)
            preset.oscillators = [
                {'frequency': 55, 'wave_type': 'sine', 'gain': 0.8},
                {'frequency': 110, 'wave_type': 'square', 'gain': 0.2}
            ]
            preset.filter = {'type': 'lowpass', 'cutoff': 800, 'resonance': 1.0, 'enabled': True}
            preset.envelope = {'attack': 0.001, 'decay': 0.1, 'sustain': 0.9, 'release': 0.2, 'enabled': True}
            preset.description = desc
            preset.tags = tags
            self.add_preset(preset)
        
        # Pad 预设
        pad_presets = [
            ('Dreamy Pad', 'Pad', '梦幻垫音', ['dreamy', 'ambient', 'soft']),
            ('Warm Pad', 'Pad', '温暖垫音', ['warm', 'cozy', 'comforting']),
            ('Space Pad', 'Pad', '太空垫音', ['space', 'cosmic', 'wide']),
            ('Ethereal Pad', 'Pad', '空灵垫音', ['ethereal', 'heavenly', 'angelic']),
            ('Evolving Pad', 'Pad', '演变垫音', ['evolving', 'dynamic', 'cinematic']),
            ('Retro Pad', 'Pad', '复古垫音', ['retro', 'vintage', 'classic']),
            ('Chorus Pad', 'Pad', '合唱垫音', ['chorus', 'wide', 'rich']),
            ('Reverb Pad', 'Pad', '混响垫音', ['reverb', 'huge', 'spacious']),
            ('Analog Pad', 'Pad', '模拟垫音', ['analog', 'warm', 'vintage']),
            ('Digital Pad', 'Pad', '数字垫音', ['digital', 'clean', 'modern'])
        ]
        
        for name, category, desc, tags in pad_presets:
            preset = Preset(name, category)
            preset.oscillators = [
                {'frequency': 220, 'wave_type': 'sine', 'gain': 0.4},
                {'frequency': 220, 'wave_type': 'triangle', 'gain': 0.3},
                {'frequency': 330, 'wave_type': 'sine', 'gain': 0.3}
            ]
            preset.filter = {'type': 'lowpass', 'cutoff': 4000, 'resonance': 0.5, 'enabled': True}
            preset.envelope = {'attack': 0.5, 'decay': 0.5, 'sustain': 0.9, 'release': 1.5, 'enabled': True}
            preset.lfo = {
                'wave_type': 'sine',
                'frequency': 0.2,
                'enabled': True,
                'modulates': ['filter', 'amplitude']
            }
            preset.effects['chorus'] = {'enabled': True, 'rate': 0.3, 'depth': 0.002, 'mix': 0.4}
            preset.effects['reverb'] = {'enabled': True, 'room_size': 0.8, 'damping': 0.3, 'mix': 0.4}
            preset.description = desc
            preset.tags = tags
            self.add_preset(preset)
        
        # Keys 预设
        keys_presets = [
            ('Electric Piano', 'Keys', '电钢琴', ['electric', 'piano', ' Rhodes']),
            ('Grand Piano', 'Keys', '三角钢琴', ['piano', 'acoustic', 'classic']),
            ('Clavinet', 'Keys', '克莱维inet', ['clav', 'funk', 'gospel']),
            ('Hammond B3', 'Keys', 'Hammond风琴', ['hammond', 'organ', 'church']),
            ('Synth Clav', 'Keys', '合成克莱维', ['synth', 'clav', 'digital']),
            ('Digital Keys', 'Keys', '数字键盘', ['digital', 'clean', 'modern']),
            ('Retro Keys', 'Keys', '复古键盘', ['retro', 'vintage', '80s']),
            ('Wurli', 'Keys', 'Wurlitzer', ['wurlitzer', 'electric', 'tine']),
            ('Celesta', 'Keys', '钢片琴', ['celesta', 'bell', '童话']),
            ('Glockenspiel', 'Keys', '铝板琴', ['glockenspiel', 'bell', 'sparkle'])
        ]
        
        for name, category, desc, tags in keys_presets:
            preset = Preset(name, category)
            preset.oscillators = [
                {'frequency': 261.63, 'wave_type': 'triangle', 'gain': 0.6},
                {'frequency': 523.25, 'wave_type': 'triangle', 'gain': 0.2}
            ]
            preset.filter = {'type': 'lowpass', 'cutoff': 6000, 'resonance': 0.5, 'enabled': True}
            preset.envelope = {'attack': 0.005, 'decay': 0.1, 'sustain': 0.7, 'release': 0.3, 'enabled': True}
            preset.description = desc
            preset.tags = tags
            self.add_preset(preset)
        
        # FX 预设
        fx_presets = [
            ('Laser Zap', 'FX', '激光音效', ['laser', 'zap', 'sci-fi']),
            ('Riser', 'FX', '上升音效', ['riser', 'build', 'tension']),
            ('Downlifter', 'FX', '下降音效', ['downlifter', 'release', 'calm']),
            ('Impact', 'FX', '冲击音效', ['impact', 'hit', 'boom']),
            ('Sweep', 'FX', '扫频音效', ['sweep', 'whoosh', 'transition']),
            ('Glitch', 'FX', '故障音效', ['glitch', 'digital', 'broken']),
            ('Sci-Fi', 'FX', '科幻音效', ['sci-fi', 'alien', 'space']),
            ('Metallic', 'FX', '金属音效', ['metallic', 'bell', 'chine']),
            ('Wind', 'FX', '风声音效', ['wind', 'air', 'ambient']),
            ('Drone', 'FX', '无人机音效', ['drone', 'ambient', 'texture'])
        ]
        
        for name, category, desc, tags in fx_presets:
            preset = Preset(name, category)
            preset.oscillators = [
                {'frequency': 110, 'wave_type': 'sawtooth', 'gain': 0.5},
                {'frequency': 55, 'wave_type': 'sine', 'gain': 0.5}
            ]
            preset.filter = {'type': 'bandpass', 'cutoff': 2000, 'resonance': 5.0, 'enabled': True}
            preset.envelope = {'attack': 0.01, 'decay': 0.5, 'sustain': 0.5, 'release': 1.0, 'enabled': True}
            preset.lfo = {
                'wave_type': 'sawtooth',
                'frequency': 0.5,
                'enabled': True,
                'modulates': ['filter', 'pitch']
            }
            preset.description = desc
            preset.tags = tags
            self.add_preset(preset)
    
    def add_preset(self, preset: Preset):
        """添加预设"""
        self.presets[preset.name] = preset
    
    def remove_preset(self, name: str):
        """移除预设"""
        if name in self.presets:
            del self.presets[name]
    
    def get_preset(self, name: str) -> Optional[Preset]:
        """获取预设"""
        return self.presets.get(name)
    
    def get_presets_by_category(self, category: str) -> List[Preset]:
        """按类别获取预设"""
        if category == 'All':
            return list(self.presets.values())
        return [p for p in self.presets.values() if p.category == category]
    
    def get_categories(self) -> List[str]:
        """获取所有类别"""
        categories = set(p.category for p in self.presets.values())
        return ['All'] + sorted(categories)
    
    def search_presets(self, query: str) -> List[Preset]:
        """搜索预设（按名称、描述、标签）"""
        query = query.lower()
        results = []
        for preset in self.presets.values():
            if (query in preset.name.lower() or 
                query in preset.description.lower() or
                any(query in tag.lower() for tag in preset.tags)):
                results.append(preset)
        return results
    
    def save_library(self, path: str = None):
        """保存预设库到JSON文件"""
        save_path = path or self.library_path
        if not save_path:
            save_path = os.path.join(os.path.dirname(__file__), '..', 'presets.json')
        
        data = {
            'version': '0.5.0',
            'saved_at': datetime.now().isoformat(),
            'presets': {name: preset.to_dict() for name, preset in self.presets.items()}
        }
        
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return save_path
    
    def load_library(self, path: str):
        """从JSON文件加载预设库"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for name, preset_data in data.get('presets', {}).items():
            preset = Preset.from_dict(preset_data)
            self.add_preset(preset)
    
    def export_preset(self, name: str, path: str):
        """导出单个预设到JSON文件"""
        preset = self.get_preset(name)
        if preset:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(preset.to_dict(), f, ensure_ascii=False, indent=2)
    
    def import_preset(self, path: str) -> Optional[Preset]:
        """从JSON文件导入单个预设"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        preset = Preset.from_dict(data)
        self.add_preset(preset)
        return preset
    
    def duplicate_preset(self, name: str, new_name: str) -> Optional[Preset]:
        """复制预设"""
        preset = self.get_preset(name)
        if preset:
            new_preset = Preset.from_dict(preset.to_dict())
            new_preset.name = new_name
            new_preset.category = 'User'
            self.add_preset(new_preset)
            return new_preset
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """获取库统计信息"""
        categories = {}
        for preset in self.presets.values():
            categories[preset.category] = categories.get(preset.category, 0) + 1
        
        return {
            'total_presets': len(self.presets),
            'categories': categories,
            'user_presets': len([p for p in self.presets.values() if p.category == 'User'])
        }


# ============ 预设管理器 - 用于与Synthesizer集成 ============

class PresetManager:
    """预设管理器 - 包装PresetLibrary，提供与Synthesizer的接口"""
    
    def __init__(self, library: PresetLibrary = None):
        self.library = library or PresetLibrary()
        self.current_preset: Optional[Preset] = None
    
    def load_preset(self, name: str) -> Optional[Preset]:
        """加载预设"""
        self.current_preset = self.library.get_preset(name)
        return self.current_preset
    
    def save_current_preset(self, name: str, category: str = 'User'):
        """保存当前设置为新预设"""
        if self.current_preset:
            new_preset = Preset.from_dict(self.current_preset.to_dict())
            new_preset.name = name
            new_preset.category = category
            self.library.add_preset(new_preset)
            self.current_preset = new_preset
            return new_preset
        return None
    
    def apply_preset_to_synth(self, synth) -> bool:
        """应用当前预设到合成器实例
        
        Args:
            synth: Synthesizer实例
            
        Returns:
            bool: 是否成功应用
        """
        if not self.current_preset:
            return False
        
        preset = self.current_preset
        
        # 应用振荡器设置
        if hasattr(synth, 'oscillators'):
            synth.oscillators = []
            for osc_data in preset.oscillators:
                synth.add_oscillator(osc_data.get('frequency', 440), 
                                   osc_data.get('wave_type', 'sine'),
                                   osc_data.get('gain', 0.5))
        
        # 应用滤波器设置
        if hasattr(synth, 'filter') and preset.filter.get('enabled', True):
            synth.filter.set_filter_type(preset.filter.get('type', 'lowpass'))
            synth.filter.set_cutoff(preset.filter.get('cutoff', 2000))
            # Note: Filter类没有resonance属性，跳过
        
        # 应用包络设置
        if hasattr(synth, 'envelope') and preset.envelope.get('enabled', True):
            synth.envelope.set_parameters(
                attack=preset.envelope.get('attack', 0.01),
                decay=preset.envelope.get('decay', 0.2),
                sustain=preset.envelope.get('sustain', 0.7),
                release=preset.envelope.get('release', 0.3)
            )
        
        # 应用主音量
        if hasattr(synth, 'set_volume'):
            synth.set_volume(preset.master_volume)
        
        return True
    
    def collect_synth_state(self, synth) -> Preset:
        """从合成器收集当前状态创建预设
        
        Args:
            synth: Synthesizer实例
            
        Returns:
            Preset: 新创建的预设
        """
        preset = Preset(name='Current State', category='User')
        
        # 收集振荡器状态
        if hasattr(synth, 'oscillators'):
            for osc in synth.oscillators:
                preset.oscillators.append({
                    'frequency': osc.frequency,
                    'wave_type': osc.wave_type,
                    'gain': osc.gain
                })
        
        # 收集滤波器状态
        if hasattr(synth, 'filter'):
            preset.filter = {
                'type': synth.filter.filter_type if hasattr(synth.filter, 'filter_type') else 'lowpass',
                'cutoff': synth.filter.cutoff if hasattr(synth.filter, 'cutoff') else 2000,
                'resonance': synth.filter.resonance if hasattr(synth.filter, 'resonance') else 1.0,
                'enabled': True
            }
        
        # 收集包络状态
        if hasattr(synth, 'envelope'):
            preset.envelope = {
                'attack': synth.envelope.attack if hasattr(synth.envelope, 'attack') else 0.01,
                'decay': synth.envelope.decay if hasattr(synth.envelope, 'decay') else 0.2,
                'sustain': synth.envelope.sustain if hasattr(synth.envelope, 'sustain') else 0.7,
                'release': synth.envelope.release if hasattr(synth.envelope, 'release') else 0.3,
                'enabled': True
            }
        
        return preset
