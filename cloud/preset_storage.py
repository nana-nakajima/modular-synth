"""
☁️ Cloud Preset Storage - v0.9.0
云端预设存储服务
"""

import hashlib
import secrets
import json
import os
import base64
import zlib
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict


@dataclass
class CloudPreset:
    """云端预设模型"""
    preset_id: str
    user_id: str
    name: str
    description: str
    category: str  # Lead, Bass, Pad, FX, Keys
    tags: List[str]
    preset_data: Dict[str, Any]  # 完整的预设参数
    is_public: bool = True
    is_featured: bool = False
    likes: int = 0
    downloads: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    author_name: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CloudPreset':
        """从字典创建"""
        return cls(**data)
    
    @property
    def compressed_data(self) -> str:
        """获取压缩后的数据（用于分享链接）"""
        json_str = json.dumps(self.preset_data)
        compressed = zlib.compress(json_str.encode(), level=9)
        return base64.urlsafe_b64encode(compressed).decode()
    
    @classmethod
    def from_compressed_data(cls, compressed: str) -> Dict[str, Any]:
        """从压缩数据解码"""
        compressed_bytes = base64.urlsafe_b64decode(compressed.encode())
        json_str = zlib.decompress(compressed_bytes).decode()
        return json.loads(json_str)
    
    def generate_share_link(self, base_url: str = "https://modular-synth.app/preset") -> str:
        """生成分享链接"""
        share_id = secrets.token_urlsafe(8)
        compressed = self.compressed_data
        return f"{base_url}/{share_id}?data={compressed[:100]}..."
    
    def to_preset_dict(self) -> Dict[str, Any]:
        """转换为合成器可用的预设格式"""
        return {
            'name': self.name,
            'category': self.category,
            'parameters': self.preset_data
        }


class PresetCloudStorage:
    """云端预设存储服务"""
    
    def __init__(self, storage_path: str = './data/presets'):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        os.makedirs(os.path.join(storage_path, 'public'), exist_ok=True)
        os.makedirs(os.path.join(storage_path, 'private'), exist_ok=True)
        os.makedirs(os.path.join(storage_path, 'meta'), exist_ok=True)
        
        self.presets: Dict[str, CloudPreset] = {}
        self.user_presets: Dict[str, List[str]] = {}  # user_id -> [preset_ids]
        self._load_presets()
    
    def _get_preset_file(self, preset_id: str) -> str:
        """获取预设文件路径"""
        return os.path.join(self.storage_path, 'public' if self.presets.get(preset_id, CloudPreset("", "", "", "", "", [])).is_public else 'private', f'{preset_id}.json')
    
    def _get_meta_file(self, preset_id: str) -> str:
        """获取元数据文件路径"""
        return os.path.join(self.storage_path, 'meta', f'{preset_id}.json')
    
    def _load_presets(self) -> None:
        """从磁盘加载所有预设"""
        for folder in ['public', 'private']:
            folder_path = os.path.join(self.storage_path, folder)
            if not os.path.exists(folder_path):
                continue
            
            for filename in os.listdir(folder_path):
                if filename.endswith('.json'):
                    preset_id = filename.replace('.json', '')
                    filepath = os.path.join(folder_path, filename)
                    try:
                        with open(filepath, 'r') as f:
                            data = json.load(f)
                            preset = CloudPreset.from_dict(data)
                            self.presets[preset_id] = preset
                            
                            # 记录用户预设
                            if preset.user_id not in self.user_presets:
                                self.user_presets[preset.user_id] = []
                            if preset_id not in self.user_presets[preset.user_id]:
                                self.user_presets[preset.user_id].append(preset_id)
                    except Exception as e:
                        print(f"Error loading preset {filename}: {e}")
    
    def _save_preset(self, preset: CloudPreset) -> None:
        """保存预设到磁盘"""
        # 保存数据文件
        folder = 'public' if preset.is_public else 'private'
        filepath = os.path.join(self.storage_path, folder, f'{preset.preset_id}.json')
        with open(filepath, 'w') as f:
            json.dump(preset.to_dict(), f, indent=2)
        
        # 保存元数据（用于搜索）
        meta = {
            'preset_id': preset.preset_id,
            'user_id': preset.user_id,
            'name': preset.name,
            'description': preset.description,
            'category': preset.category,
            'tags': preset.tags,
            'is_public': preset.is_public,
            'likes': preset.likes,
            'downloads': preset.downloads,
            'created_at': preset.created_at,
            'author_name': preset.author_name
        }
        meta_path = self._get_meta_file(preset.preset_id)
        with open(meta_path, 'w') as f:
            json.dump(meta, f, indent=2)
    
    def create_preset(
        self,
        user_id: str,
        name: str,
        description: str,
        category: str,
        tags: List[str],
        preset_data: Dict[str, Any],
        is_public: bool = True,
        author_name: str = ""
    ) -> CloudPreset:
        """创建新预设"""
        preset_id = f"preset_{secrets.token_hex(8)}"
        
        preset = CloudPreset(
            preset_id=preset_id,
            user_id=user_id,
            name=name,
            description=description,
            category=category,
            tags=tags,
            preset_data=preset_data,
            is_public=is_public,
            author_name=author_name
        )
        
        # 保存
        self.presets[preset_id] = preset
        if user_id not in self.user_presets:
            self.user_presets[user_id] = []
        self.user_presets[user_id].append(preset_id)
        self._save_preset(preset)
        
        return preset
    
    def get_preset(self, preset_id: str) -> Optional[CloudPreset]:
        """获取预设"""
        return self.presets.get(preset_id)
    
    def get_user_presets(self, user_id: str, include_private: bool = True) -> List[CloudPreset]:
        """获取用户的所有预设"""
        preset_ids = self.user_presets.get(user_id, [])
        presets = []
        for pid in preset_ids:
            preset = self.presets.get(pid)
            if preset and (include_private or preset.is_public):
                presets.append(preset)
        return presets
    
    def list_public_presets(
        self,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50,
        sort_by: str = "created_at"
    ) -> List[CloudPreset]:
        """列出公开预设（支持过滤和排序）"""
        presets = [p for p in self.presets.values() if p.is_public]
        
        # 分类过滤
        if category:
            presets = [p for p in presets if p.category.lower() == category.lower()]
        
        # 标签过滤
        if tags:
            presets = [p for p in presets if any(t in p.tags for t in tags)]
        
        # 排序
        if sort_by == "likes":
            presets.sort(key=lambda p: p.likes, reverse=True)
        elif sort_by == "downloads":
            presets.sort(key=lambda p: p.downloads, reverse=True)
        else:  # created_at
            presets.sort(key=lambda p: p.created_at, reverse=True)
        
        return presets[:limit]
    
    def search_presets(
        self,
        query: str,
        limit: int = 20
    ) -> List[CloudPreset]:
        """搜索预设"""
        query = query.lower()
        results = []
        
        for preset in self.presets.values():
            if not preset.is_public:
                continue
            
            # 搜索名称、描述、标签
            if (query in preset.name.lower() or
                query in preset.description.lower() or
                query in preset.category.lower() or
                any(query in tag.lower() for tag in preset.tags)):
                results.append(preset)
        
        return results[:limit]
    
    def update_preset(
        self,
        preset_id: str,
        user_id: str,
        **kwargs
    ) -> Optional[CloudPreset]:
        """更新预设（只能更新自己的预设）"""
        preset = self.presets.get(preset_id)
        if not preset or preset.user_id != user_id:
            return None
        
        allowed_fields = ['name', 'description', 'tags', 'is_public', 'preset_data']
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(preset, field, value)
        
        preset.updated_at = datetime.now().isoformat()
        self._save_preset(preset)
        
        return preset
    
    def delete_preset(self, preset_id: str, user_id: str) -> bool:
        """删除预设（只能删除自己的预设）"""
        preset = self.presets.get(preset_id)
        if not preset or preset.user_id != user_id:
            return False
        
        # 删除文件
        folder = 'public' if preset.is_public else 'private'
        filepath = os.path.join(self.storage_path, folder, f'{preset_id}.json')
        meta_path = self._get_meta_file(preset_id)
        
        if os.path.exists(filepath):
            os.remove(filepath)
        if os.path.exists(meta_path):
            os.remove(meta_path)
        
        # 从内存中移除
        del self.presets[preset_id]
        if user_id in self.user_presets and preset_id in self.user_presets[user_id]:
            self.user_presets[user_id].remove(preset_id)
        
        return True
    
    def like_preset(self, preset_id: str) -> bool:
        """点赞预设"""
        preset = self.presets.get(preset_id)
        if preset:
            preset.likes += 1
            self._save_preset(preset)
            return True
        return False
    
    def download_preset(self, preset_id: str) -> bool:
        """下载预设"""
        preset = self.presets.get(preset_id)
        if preset:
            preset.downloads += 1
            self._save_preset(preset)
            return True
        return False
    
    def get_featured_presets(self, limit: int = 10) -> List[CloudPreset]:
        """获取精选预设"""
        presets = [p for p in self.presets.values() if p.is_featured]
        presets.sort(key=lambda p: p.likes, reverse=True)
        return presets[:limit]
    
    def get_popular_presets(self, limit: int = 10) -> List[CloudPreset]:
        """获取最热门的预设"""
        presets = [p for p in self.presets.values() if p.is_public]
        presets.sort(key=lambda p: (p.likes + p.downloads * 2), reverse=True)
        return presets[:limit]


if __name__ == '__main__':
    # 演示
    storage = PresetCloudStorage()
    
    # 创建预设
    preset_data = {
        'oscillator': {'type': 'sawtooth', 'detune': 0},
        'filter': {'type': 'lowpass', 'cutoff': 1000},
        'envelope': {'attack': 0.1, 'decay': 0.3, 'sustain': 0.5, 'release': 0.5}
    }
    
    preset = storage.create_preset(
        user_id='user_test123',
        name='Test Lead',
        description='A test lead sound',
        category='Lead',
        tags=['synth', 'lead', 'bright'],
        preset_data=preset_data,
        author_name='Nana'
    )
    print(f"Created preset: {preset.name} (ID: {preset.preset_id})")
    
    # 列出公开预设
    public = storage.list_public_presets()
    print(f"Public presets: {len(public)}")
    
    # 搜索
    results = storage.search_presets('lead')
    print(f"Search results: {len(results)}")
    
    # 生成分享链接
    share_link = preset.generate_share_link()
    print(f"Share link: {share_link[:60]}...")
