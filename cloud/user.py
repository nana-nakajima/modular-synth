"""
☁️ User Management - v0.9.0
用户账户系统 - 账户创建、登录、Token认证
"""

import hashlib
import secrets
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class User:
    """用户账户模型"""
    
    def __init__(
        self,
        user_id: str,
        username: str,
        email: str,
        password_hash: str,
        created_at: Optional[datetime] = None,
        last_login: Optional[datetime] = None,
        preset_count: int = 0,
        is_public: bool = True
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at or datetime.now()
        self.last_login = last_login
        self.preset_count = preset_count
        self.is_public = is_public
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'preset_count': self.preset_count,
            'is_public': self.is_public
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """从字典创建用户"""
        return cls(
            user_id=data['user_id'],
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            last_login=datetime.fromisoformat(data['last_login']) if data.get('last_login') else None,
            preset_count=data.get('preset_count', 0),
            is_public=data.get('is_public', True)
        )
    
    def verify_password(self, password: str) -> bool:
        """验证密码"""
        return self.password_hash == self.hash_password(password)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """哈希密码"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def generate_user_id() -> str:
        """生成唯一用户ID"""
        return f"user_{secrets.token_hex(8)}"


class UserManager:
    """用户管理服务"""
    
    def __init__(self, storage_path: str = './data/users'):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.users: Dict[str, User] = {}
        self.tokens: Dict[str, str] = {}  # token -> user_id
        self.token_expiry: Dict[str, datetime] = {}
        self._load_users()
    
    def _get_user_file(self, user_id: str) -> str:
        """获取用户文件路径"""
        return os.path.join(self.storage_path, f'{user_id}.json')
    
    def _load_users(self) -> None:
        """从磁盘加载所有用户"""
        if not os.path.exists(self.storage_path):
            return
        
        for filename in os.listdir(self.storage_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.storage_path, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        user = User.from_dict(data)
                        self.users[user.user_id] = user
                except Exception as e:
                    print(f"Error loading user {filename}: {e}")
    
    def _save_user(self, user: User) -> None:
        """保存用户到磁盘"""
        filepath = self._get_user_file(user.user_id)
        with open(filepath, 'w') as f:
            json.dump(user.to_dict(), f, indent=2)
    
    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        is_public: bool = True
    ) -> tuple[User, str]:
        """
        创建新用户
        
        Returns:
            tuple: (User实例, API Token)
        """
        # 检查用户名和邮箱是否已存在
        for user in self.users.values():
            if user.username == username:
                raise ValueError(f"用户名 '{username}' 已被使用")
            if user.email == email:
                raise ValueError(f"邮箱 '{email}' 已被注册")
        
        # 创建新用户
        user_id = User.generate_user_id()
        password_hash = User.hash_password(password)
        
        user = User(
            user_id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            is_public=is_public
        )
        
        # 生成token
        token = self._generate_token(user_id)
        
        # 保存
        self.users[user_id] = user
        self._save_user(user)
        
        return user, token
    
    def login(self, username: str, password: str) -> tuple[User, str]:
        """
        用户登录
        
        Returns:
            tuple: (User实例, API Token)
        """
        # 查找用户
        user = None
        for u in self.users.values():
            if u.username == username:
                user = u
                break
        
        if not user:
            raise ValueError("用户不存在")
        
        # 验证密码
        if not user.verify_password(password):
            raise ValueError("密码错误")
        
        # 更新最后登录时间
        user.last_login = datetime.now()
        self._save_user(user)
        
        # 生成新token
        token = self._generate_token(user.user_id)
        
        return user, token
    
    def _generate_token(self, user_id: str) -> str:
        """生成API token"""
        token = secrets.token_hex(32)
        self.tokens[token] = user_id
        self.token_expiry[token] = datetime.now() + timedelta(days=30)
        return token
    
    def verify_token(self, token: str) -> Optional[User]:
        """验证token并返回用户"""
        if token not in self.tokens:
            return None
        
        # 检查是否过期
        if token in self.token_expiry and self.token_expiry[token] < datetime.now():
            del self.tokens[token]
            del self.token_expiry[token]
            return None
        
        user_id = self.tokens[token]
        return self.users.get(user_id)
    
    def logout(self, token: str) -> bool:
        """注销/使token失效"""
        if token in self.tokens:
            del self.tokens[token]
            if token in self.token_expiry:
                del self.token_expiry[token]
            return True
        return False
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """通过ID获取用户"""
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """通过用户名获取用户"""
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def list_users(self, limit: int = 50) -> list[User]:
        """列出所有公开用户（用于社区浏览）"""
        return [u for u in self.users.values() if u.is_public][:limit]
    
    def update_user(self, user_id: str, **kwargs) -> Optional[User]:
        """更新用户信息"""
        user = self.users.get(user_id)
        if not user:
            return None
        
        allowed_fields = ['username', 'email', 'is_public']
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(user, field, value)
        
        self._save_user(user)
        return user


if __name__ == '__main__':
    # 演示
    manager = UserManager()
    
    # 创建用户
    user, token = manager.create_user(
        username='nana_test',
        email='nana@test.com',
        password='password123'
    )
    print(f"Created user: {user.username}")
    print(f"Token: {token[:20]}...")
    
    # 登录
    user2, token2 = manager.login('nana_test', 'password123')
    print(f"Login successful: {user2.username}")
    
    # 验证token
    verified = manager.verify_token(token2)
    print(f"Token valid: {verified is not None}")
