#!/usr/bin/env python3
"""
☁️ Modular Synth Studio v0.9.0 - Cloud Demo
云同步功能演示 - 用户账户、预设存储、分享
"""

import os
import sys
import json

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cloud.user import UserManager
from cloud.preset_storage import PresetCloudStorage, CloudPreset
from cloud.api import create_app


def demo_user_management():
    """演示用户管理功能"""
    print("\n" + "="*60)
    print("👤 用户管理演示")
    print("="*60)
    
    # 初始化用户管理器
    manager = UserManager('./demo_data/users')
    
    # 创建测试用户
    print("\n1. 创建新用户...")
    user1, token1 = manager.create_user(
        username='nana_synth',
        email='nana@icloud.com',
        password='synth123',
        is_public=True
    )
    print(f"   ✅ 用户创建成功: {user1.username}")
    print(f"   📝 User ID: {user1.user_id}")
    print(f"   🔑 Token: {token1[:20]}...")
    
    # 创建第二个用户
    print("\n2. 创建第二个用户...")
    user2, token2 = manager.create_user(
        username='eli_music',
        email='eli@example.com',
        password='music456',
        is_public=True
    )
    print(f"   ✅ 用户创建成功: {user2.username}")
    
    # 登录演示
    print("\n3. 用户登录...")
    user_login, token_login = manager.login('nana_synth', 'synth123')
    print(f"   ✅ 登录成功: {user_login.username}")
    
    # Token验证
    print("\n4. Token验证...")
    verified = manager.verify_token(token_login)
    print(f"   ✅ Token有效: {verified.username}")
    
    # 列出用户
    print("\n5. 用户列表...")
    users = manager.list_users()
    print(f"   📋 总用户数: {len(users)}")
    
    # 清理
    import shutil
    if os.path.exists('./demo_data'):
        shutil.rmtree('./demo_data')
    
    print("\n✅ 用户管理演示完成!\n")


def demo_preset_storage():
    """演示预设存储功能"""
    print("\n" + "="*60)
    print("🎹 预设存储演示")
    print("="*60)
    
    # 初始化预设存储
    storage = PresetCloudStorage('./demo_data/presets')
    
    # 示例预设数据
    lead_preset = {
        'oscillators': [
            {'type': 'sawtooth', 'detune': 0, 'mix': 0.7},
            {'type': 'square', 'detune': 5, 'mix': 0.3}
        ],
        'filter': {'type': 'lowpass', 'cutoff': 2000, 'resonance': 0.3},
        'envelope': {'attack': 0.01, 'decay': 0.2, 'sustain': 0.7, 'release': 0.5},
        'lfo': {'waveform': 'sine', 'frequency': 4, 'depth': 0.2}
    }
    
    bass_preset = {
        'oscillators': [
            {'type': 'square', 'detune': 0, 'mix': 1.0}
        ],
        'filter': {'type': 'lowpass', 'cutoff': 500, 'resonance': 0.5},
        'envelope': {'attack': 0.01, 'decay': 0.1, 'sustain': 0.9, 'release': 0.2}
    }
    
    # 创建预设
    print("\n1. 创建Lead预设...")
    preset1 = storage.create_preset(
        user_id='user_nana',
        name='Cyber Lead',
        description='A bright cyberpunk lead sound',
        category='Lead',
        tags=['synth', 'lead', 'bright', 'cyberpunk'],
        preset_data=lead_preset,
        author_name='Nana'
    )
    print(f"   ✅ 创建成功: {preset1.name} (ID: {preset1.preset_id})")
    
    print("\n2. 创建Bass预设...")
    preset2 = storage.create_preset(
        user_id='user_eli',
        name='Deep Bass',
        description='Deep 808-style bass',
        category='Bass',
        tags=['bass', '808', 'deep'],
        preset_data=bass_preset,
        author_name='Eli'
    )
    print(f"   ✅ 创建成功: {preset2.name}")
    
    # 列出公开预设
    print("\n3. 列出公开预设...")
    presets = storage.list_public_presets()
    print(f"   📋 公开预设数: {len(presets)}")
    for p in presets:
        print(f"      - {p.name} ({p.category}) by {p.author_name}")
    
    # 搜索
    print("\n4. 搜索 'lead'...")
    results = storage.search_presets('lead')
    print(f"   🔍 找到 {len(results)} 个结果")
    
    # 点赞和下载
    print("\n5. 点赞和下载...")
    storage.like_preset(preset1.preset_id)
    storage.like_preset(preset1.preset_id)
    storage.download_preset(preset1.preset_id)
    preset = storage.get_preset(preset1.preset_id)
    print(f"   ❤️ Likes: {preset.likes}, ⬇️ Downloads: {preset.downloads}")
    
    # 生成分享链接
    print("\n6. 生成分享链接...")
    share_link = preset.generate_share_link()
    print(f"   🔗 {share_link[:70]}...")
    
    # 热门和精选
    print("\n7. 热门预设...")
    popular = storage.get_popular_presets()
    if popular:
        print(f"   🔥 {popular[0].name} - {popular[0].likes + popular[0].downloads * 2} points")
    
    # 清理
    import shutil
    if os.path.exists('./demo_data'):
        shutil.rmtree('./demo_data')
    
    print("\n✅ 预设存储演示完成!\n")


def demo_api():
    """演示REST API"""
    print("\n" + "="*60)
    print("🌐 REST API 演示")
    print("="*60)
    
    # 创建Flask应用
    app = create_app('./demo_data/users', './demo_data/presets')
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        # 用户注册
        print("\n1. 用户注册...")
        resp = client.post('/api/v1/users/register', json={
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'test123'
        })
        print(f"   📊 状态码: {resp.status_code}")
        data = json.loads(resp.data)
        if resp.status_code == 201:
            token = data['token']
            print(f"   ✅ 注册成功! Token: {token[:20]}...")
        else:
            print(f"   ❌ 错误: {data.get('error')}")
            # 尝试登录
            resp = client.post('/api/v1/users/login', json={
                'username': 'test_user',
                'password': 'test123'
            })
            if resp.status_code == 200:
                data = json.loads(resp.data)
                token = data['token']
                print(f"   ✅ 登录成功! Token: {token[:20]}...")
        
        # 创建预设
        print("\n2. 创建预设...")
        resp = client.post('/api/v1/presets', json={
            'name': 'API Test Preset',
            'category': 'Lead',
            'description': 'Created via REST API',
            'tags': ['api', 'test'],
            'preset_data': {
                'oscillator': {'type': 'sine'},
                'filter': {'cutoff': 1000}
            },
            'is_public': True
        }, headers={'Authorization': f'Bearer {token}'})
        print(f"   📊 状态码: {resp.status_code}")
        
        # 获取预设列表
        print("\n3. 获取预设列表...")
        resp = client.get('/api/v1/presets')
        data = json.loads(resp.data)
        print(f"   📋 预设数: {data['count']}")
        
        # 搜索预设
        print("\n4. 搜索预设...")
        resp = client.get('/api/v1/presets/search?q=test')
        data = json.loads(resp.data)
        print(f"   🔍 找到: {data['count']} 个")
        
        # 健康检查
        print("\n5. 健康检查...")
        resp = client.get('/api/v1/health')
        data = json.loads(resp.data)
        print(f"   💚 Status: {data['status']} (v{data['version']})")
    
    # 清理
    import shutil
    if os.path.exists('./demo_data'):
        shutil.rmtree('./demo_data')
    
    print("\n✅ REST API 演示完成!\n")


def main():
    """主函数"""
    print("\n" + "🎹"*30)
    print("\n   Modular Synth Studio v0.9.0 - Cloud Demo")
    print("   ☁️ 云同步功能演示\n")
    print("🎹"*30)
    
    # 运行演示
    demo_user_management()
    demo_preset_storage()
    demo_api()
    
    print("="*60)
    print("🎉 所有演示完成!")
    print("="*60)
    print("\n下一步:")
    print("  1. 安装依赖: pip install flask")
    print("  2. 启动API服务器: python -m cloud.api")
    print("  3. 在浏览器打开: http://localhost:5000/api/v1/health")
    print()


if __name__ == '__main__':
    main()
