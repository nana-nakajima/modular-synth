"""
☁️ REST API - v0.9.0
Flask API端点 - 用户认证、预设管理、分享
"""

from flask import Flask, request, jsonify, g
from functools import wraps
from typing import Callable
import os
import sys

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloud.user import UserManager
from cloud.preset_storage import PresetCloudStorage


def create_app(
    user_storage_path: str = './data/users',
    preset_storage_path: str = './data/presets'
) -> Flask:
    """创建并配置Flask应用"""
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # 初始化管理器
    user_manager = UserManager(user_storage_path)
    preset_storage = PresetCloudStorage(preset_storage_path)
    
    # 将管理器保存到app配置
    app.config['USER_MANAGER'] = user_manager
    app.config['PRESET_STORAGE'] = preset_storage
    
    # ===== 认证装饰器 =====
    
    def require_auth(f: Callable) -> Callable:
        """需要认证的装饰器"""
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Missing or invalid Authorization header'}), 401
            
            token = auth_header.split(' ')[1]
            user = user_manager.verify_token(token)
            
            if not user:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            g.current_user = user
            return f(*args, **kwargs)
        return decorated
    
    # ===== 用户端点 =====
    
    @app.route('/api/v1/users/register', methods=['POST'])
    def register():
        """用户注册"""
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required = ['username', 'email', 'password']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        try:
            user, token = user_manager.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                is_public=data.get('is_public', True)
            )
            return jsonify({
                'message': 'User created successfully',
                'user': {
                    'user_id': user.user_id,
                    'username': user.username,
                    'email': user.email
                },
                'token': token
            }), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/v1/users/login', methods=['POST'])
    def login():
        """用户登录"""
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        try:
            user, token = user_manager.login(username, password)
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'user_id': user.user_id,
                    'username': user.username,
                    'email': user.email
                },
                'token': token
            })
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
    
    @app.route('/api/v1/users/logout', methods=['POST'])
    @require_auth
    def logout():
        """用户登出"""
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        user_manager.logout(token)
        return jsonify({'message': 'Logged out successfully'})
    
    @app.route('/api/v1/users/me', methods=['GET'])
    @require_auth
    def get_current_user():
        """获取当前用户信息"""
        return jsonify({
            'user_id': g.current_user.user_id,
            'username': g.current_user.username,
            'email': g.current_user.email,
            'preset_count': g.current_user.preset_count,
            'created_at': g.current_user.created_at,
            'last_login': g.current_user.last_login
        })
    
    @app.route('/api/v1/users/<user_id>', methods=['GET'])
    def get_user(user_id: str):
        """获取用户公开信息"""
        user = user_manager.get_user_by_id(user_id)
        if not user or not user.is_public:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user_id': user.user_id,
            'username': user.username,
            'preset_count': user.preset_count,
            'created_at': user.created_at
        })
    
    # ===== 预设端点 =====
    
    @app.route('/api/v1/presets', methods=['POST'])
    @require_auth
    def create_preset():
        """创建新预设"""
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required = ['name', 'category', 'preset_data']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        preset = preset_storage.create_preset(
            user_id=g.current_user.user_id,
            name=data['name'],
            description=data.get('description', ''),
            category=data['category'],
            tags=data.get('tags', []),
            preset_data=data['preset_data'],
            is_public=data.get('is_public', True),
            author_name=g.current_user.username
        )
        
        return jsonify({
            'message': 'Preset created successfully',
            'preset': {
                'preset_id': preset.preset_id,
                'name': preset.name,
                'category': preset.category,
                'is_public': preset.is_public
            }
        }), 201
    
    @app.route('/api/v1/presets', methods=['GET'])
    def list_presets():
        """列出公开预设"""
        category = request.args.get('category')
        tags = request.args.getlist('tags')
        limit = min(int(request.args.get('limit', 50)), 100)
        sort_by = request.args.get('sort_by', 'created_at')
        
        presets = preset_storage.list_public_presets(
            category=category,
            tags=tags if tags else None,
            limit=limit,
            sort_by=sort_by
        )
        
        return jsonify({
            'presets': [
                {
                    'preset_id': p.preset_id,
                    'name': p.name,
                    'description': p.description,
                    'category': p.category,
                    'tags': p.tags,
                    'likes': p.likes,
                    'downloads': p.downloads,
                    'author_name': p.author_name,
                    'created_at': p.created_at
                }
                for p in presets
            ],
            'count': len(presets)
        })
    
    @app.route('/api/v1/presets/search', methods=['GET'])
    def search_presets():
        """搜索预设"""
        query = request.args.get('q', '')
        limit = min(int(request.args.get('limit', 20)), 100)
        
        if not query:
            return jsonify({'error': 'Search query required'}), 400
        
        presets = preset_storage.search_presets(query, limit)
        
        return jsonify({
            'presets': [
                {
                    'preset_id': p.preset_id,
                    'name': p.name,
                    'description': p.description,
                    'category': p.category,
                    'tags': p.tags,
                    'likes': p.likes,
                    'author_name': p.author_name
                }
                for p in presets
            ],
            'count': len(presets)
        })
    
    @app.route('/api/v1/presets/<preset_id>', methods=['GET'])
    def get_preset(preset_id: str):
        """获取预设详情"""
        preset = preset_storage.get_preset(preset_id)
        
        if not preset:
            return jsonify({'error': 'Preset not found'}), 404
        
        # 检查访问权限
        if not preset.is_public:
            # 需要认证
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Private preset - authentication required'}), 403
            
            token = auth_header.split(' ')[1]
            user = user_manager.verify_token(token)
            if not user or user.user_id != preset.user_id:
                return jsonify({'error': 'Access denied'}), 403
        
        # 增加下载计数
        preset_storage.download_preset(preset_id)
        
        return jsonify({
            'preset': {
                'preset_id': preset.preset_id,
                'name': preset.name,
                'description': preset.description,
                'category': preset.category,
                'tags': preset.tags,
                'preset_data': preset.preset_data,
                'likes': preset.likes,
                'downloads': preset.downloads,
                'author_name': preset.author_name,
                'created_at': preset.created_at
            }
        })
    
    @app.route('/api/v1/presets/<preset_id>', methods=['PUT'])
    @require_auth
    def update_preset(preset_id: str):
        """更新预设"""
        preset = preset_storage.get_preset(preset_id)
        
        if not preset:
            return jsonify({'error': 'Preset not found'}), 404
        
        if preset.user_id != g.current_user.user_id:
            return jsonify({'error': 'Can only update your own presets'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        updated = preset_storage.update_preset(
            preset_id=preset_id,
            user_id=g.current_user.user_id,
            **{k: v for k, v in data.items() if k in ['name', 'description', 'tags', 'is_public', 'preset_data']}
        )
        
        return jsonify({
            'message': 'Preset updated successfully',
            'preset': {
                'preset_id': updated.preset_id,
                'name': updated.name
            }
        })
    
    @app.route('/api/v1/presets/<preset_id>', methods=['DELETE'])
    @require_auth
    def delete_preset(preset_id: str):
        """删除预设"""
        preset = preset_storage.get_preset(preset_id)
        
        if not preset:
            return jsonify({'error': 'Preset not found'}), 404
        
        if preset.user_id != g.current_user.user_id:
            return jsonify({'error': 'Can only delete your own presets'}), 403
        
        success = preset_storage.delete_preset(preset_id, g.current_user.user_id)
        
        if success:
            return jsonify({'message': 'Preset deleted successfully'})
        else:
            return jsonify({'error': 'Failed to delete preset'}), 500
    
    @app.route('/api/v1/presets/<preset_id>/like', methods=['POST'])
    def like_preset(preset_id: str):
        """点赞预设"""
        success = preset_storage.like_preset(preset_id)
        if success:
            preset = preset_storage.get_preset(preset_id)
            return jsonify({'message': 'Liked!', 'likes': preset.likes})
        else:
            return jsonify({'error': 'Preset not found'}), 404
    
    @app.route('/api/v1/presets/<preset_id>/share', methods=['GET'])
    def share_preset(preset_id: str):
        """生成分享链接"""
        preset = preset_storage.get_preset(preset_id)
        
        if not preset:
            return jsonify({'error': 'Preset not found'}), 404
        
        share_link = preset.generate_share_link()
        
        return jsonify({
            'share_link': share_link,
            'preset_id': preset.preset_id,
            'name': preset.name
        })
    
    @app.route('/api/v1/presets/user/<user_id>', methods=['GET'])
    def get_user_presets(user_id: str):
        """获取用户的预设列表"""
        include_private = False
        
        # 检查是否是当前用户
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            user = user_manager.verify_token(token)
            if user and user.user_id == user_id:
                include_private = True
        
        presets = preset_storage.get_user_presets(user_id, include_private)
        
        return jsonify({
            'presets': [
                {
                    'preset_id': p.preset_id,
                    'name': p.name,
                    'category': p.category,
                    'is_public': p.is_public,
                    'likes': p.likes,
                    'created_at': p.created_at
                }
                for p in presets
            ],
            'count': len(presets)
        })
    
    @app.route('/api/v1/presets/featured', methods=['GET'])
    def get_featured():
        """获取精选预设"""
        limit = min(int(request.args.get('limit', 10)), 50)
        presets = preset_storage.get_featured_presets(limit)
        
        return jsonify({
            'presets': [
                {
                    'preset_id': p.preset_id,
                    'name': p.name,
                    'author_name': p.author_name,
                    'likes': p.likes,
                    'category': p.category
                }
                for p in presets
            ]
        })
    
    @app.route('/api/v1/presets/popular', methods=['GET'])
    def get_popular():
        """获取热门预设"""
        limit = min(int(request.args.get('limit', 10)), 50)
        presets = preset_storage.get_popular_presets(limit)
        
        return jsonify({
            'presets': [
                {
                    'preset_id': p.preset_id,
                    'name': p.name,
                    'author_name': p.author_name,
                    'likes': p.likes,
                    'downloads': p.downloads,
                    'category': p.category
                }
                for p in presets
            ]
        })
    
    # ===== 健康检查 =====
    
    @app.route('/api/v1/health', methods=['GET'])
    def health():
        """健康检查"""
        return jsonify({
            'status': 'ok',
            'version': '0.9.0',
            'service': 'modular-synth-cloud'
        })
    
    return app


# 运行API服务器
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
