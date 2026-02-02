#!/usr/bin/env python3
# 🎹 Modular Synth Studio - Steam打包配置
# 用于创建可分发的应用程序包

import os
import sys
import subprocess
import shutil
from pathlib import Path

# 配置
APP_NAME = "Modular Synth Studio"
VERSION = "1.0.0"
AUTHOR = "Nana Nakajima"
DESCRIPTION = "A virtual modular synthesizer for music creation"

# 打包配置
PACKAGE_NAME = f"{APP_NAME.replace(' ', '-').lower()}-v{VERSION}"
DIST_DIR = Path(__file__).parent / "dist"
BUILD_DIR = Path(__file__).parent / "build"
SPEC_DIR = Path(__file__).parent / "packaging"

def clean_build():
    """清理之前的构建文件"""
    print("🧹 清理构建文件...")
    for dir_path in [DIST_DIR, BUILD_DIR]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  删除: {dir_path}")
    
    # 清理pycache
    for pycache in Path(__file__).parent.rglob("__pycache__"):
        shutil.rmtree(pycache)
    
    print("✓ 清理完成!\n")

def create_spec_file():
    """创建PyInstaller spec文件"""
    print("📦 创建打包配置...")
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
# 🎹 Modular Synth Studio v{VERSION} - PyInstaller配置

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('gui', 'gui'),
        ('audio', 'audio'),
        ('cloud', 'cloud'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'numpy',
        'pygame',
        'flask',
        'flask_cors',
        'requests',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{APP_NAME.replace(" ", "")}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='gui/icon.ico' if os.path.exists('gui/icon.ico') else None,
)
'''
    
    spec_path = SPEC_DIR / f"{APP_NAME.replace(' ', '')}.spec"
    spec_path.write_text(spec_content)
    print(f"  创建: {spec_path}")
    
    return spec_path

def build_package():
    """构建安装包"""
    print("🔨 开始打包...")
    
    # 确保目录存在
    SPEC_DIR.mkdir(exist_ok=True)
    
    # 创建spec文件
    spec_path = create_spec_file()
    
    # 运行PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "--distpath", str(DIST_DIR),
        "--workpath", str(BUILD_DIR),
        "--specpath", str(SPEC_DIR),
        str(spec_path)
    ]
    
    print(f"  运行: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    
    if result.returncode == 0:
        print("✓ 打包成功!")
        
        # 检查输出
        dist_path = DIST_DIR / APP_NAME.replace(" ", "")
        if sys.platform == "darwin":
            dist_path = DIST_DIR / f"{APP_NAME}.app"
        
        if dist_path.exists():
            print(f"  输出: {dist_path}")
            return True
    
    print("✗ 打包失败!")
    return False

def create_installer_script():
    """创建安装脚本"""
    print("\n📝 创建安装脚本...")
    
    # macOS脚本
    mac_script = '''#!/bin/bash
# 🎹 Modular Synth Studio - macOS安装脚本
# 用法: ./install_mac.sh

APP_NAME="Modular Synth Studio"
DMG_NAME="${APP_NAME}-v1.0.0.dmg"
VOLUME_NAME="${APP_NAME} Installer"

echo "🎹 ${APP_NAME} 安装程序"
echo "================================"

# 检查是否已安装
if [ -d "/Applications/${APP_NAME}.app" ]; then
    echo "⚠️  已安装 ${APP_NAME}"
    read -p "是否重新安装? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
    rm -rf "/Applications/${APP_NAME}.app"
fi

# 创建DMG
echo "📦 创建安装包..."
if [ -f "${DMG_NAME}" ]; then
    rm "${DMG_NAME}"
fi

# 创建临时DMG
hdiutil create -volname "${VOLUME_NAME}" \
    -srcfolder "dist/${APP_NAME}.app" \
    -ov -format UDZO \
    "${DMG_NAME}"

echo "✓ 安装包创建成功: ${DMG_NAME}"
echo ""
echo "📋 下一步:"
echo "  1. 打开 ${DMG_NAME}"
echo "  2. 将 ${APP_NAME}.app 拖到 Applications 文件夹"
echo "  3. 从 Applications 启动应用"
'''

    mac_script_path = PACKAGE_NAME / "install_mac.sh"
    mac_script_path.write_text(mac_script)
    os.chmod(mac_script_path, 0o755)
    print(f"  创建: {mac_script_path}")
    
    # Windows脚本
    win_script = '''@echo off
REM 🎹 Modular Synth Studio - Windows安装脚本
REM 用法: install_win.bat

set APP_NAME=Modular-Synth-Studio
set ZIP_NAME=%APP_NAME%-v1.0.0-windows.zip

echo 🎹 %APP_NAME% 安装程序
echo ================================
echo.

REM 检查是否已安装
if exist "%APPDATA%\\%APP_NAME%" (
    echo ⚠️  已安装 %APP_NAME%
    set /p REINSTALL="是否重新安装? (y/n) "
    if not "!REINSTALL!"=="y" (
        exit /b 0
    )
    rmdir /s /q "%APPDATA%\\%APP_NAME%"
)

echo 📦 创建安装包...
powershell -Command "Compress-Archive -Path 'dist\\ModularSynthStudio' -DestinationPath '%ZIP_NAME%' -Force"

echo ✓ 安装包创建成功: %ZIP_NAME%
echo.
echo 📋 下一步:
echo   1. 解压 %ZIP_NAME%
echo   2. 运行 ModularSynthStudio.exe
'''
    
    win_script_path = PACKAGE_NAME / "install_win.bat"
    win_script_path.write_text(win_script)
    print(f"  创建: {win_script_path}")
    
    return True

def create_readme():
    """创建安装说明"""
    print("\n📖 创建安装说明...")
    
    readme_content = f'''# 🎹 Modular Synth Studio v{VERSION}

**Nana的虚拟模块合成器** - 综合音乐创作工具

## 📦 安装说明

### macOS
```bash
./install_mac.sh
```

### Windows
```batch
install_win.bat
```

## 🎮 功能特性

### 核心音频模块
- **振荡器** - 4种波形 (Sine, Square, Sawtooth, Triangle)
- **滤波器** - Lowpass, Highpass, Bandpass
- **包络** - ADSR可调节
- **LFO** - 低频调制器
- **效果器** - Reverb, Delay, Phaser, RingModulator, Bitcrusher

### GUI界面
- PyGame框架 - 完整窗口系统
- 实时波形显示
- 旋钮控件
- 键盘演奏

### 云功能
- 用户账户系统
- 云端预设存储
- 预设分享

## 🎹 使用说明

1. **启动应用**
   ```bash
   # macOS
   open "Modular Synth Studio.app"
   
   # Windows
   ./ModularSynthStudio.exe
   ```

2. **演奏**
   - 使用A-S-D-F-G-H-J-K键演奏
   - 或连接MIDI键盘
   - 使用鼠标调节旋钮

3. **导出音频**
   - 点击菜单: File → Export Audio
   - 选择WAV或FLAC格式

## 📋 系统要求

- **macOS**: 10.15+
- **Windows**: 10+
- **内存**: 4GB+
- **磁盘空间**: 500MB

## 🔧 开发信息

- **GitHub**: https://github.com/nana-nakajima/modular-synth
- **作者**: Nana Nakajima
- **版本**: {VERSION}

## 📝 许可证

MIT License

---

*Made with ❤️ by Nana Nakajima*
*🎮🎸🔧 Always building, always learning*
'''
    
    readme_path = PACKAGE_NAME / "INSTALL.md"
    readme_path.write_text(readme_content)
    print(f"  创建: {readme_path}")
    
    return True

def main():
    """主函数"""
    print(f"🎹 Modular Synth Studio v{VERSION} - Steam发布准备")
    print("=" * 60)
    print()
    
    # 清理
    clean_build()
    
    # 打包
    if build_package():
        # 创建安装脚本
        create_installer_script()
        
        # 创建说明文档
        create_readme()
        
        print("\n" + "=" * 60)
        print("✅ Steam发布准备完成!")
        print("=" * 60)
        print(f"\n📁 输出目录: {PACKAGE_NAME}/")
        print("  • install_mac.sh - macOS安装脚本")
        print("  • install_win.bat - Windows安装脚本")
        print("  • INSTALL.md - 安装说明")
        print()
        print("📦 下一步:")
        print("  1. 测试打包的应用")
        print("  2. 创建Steam商店页面")
        print("  3. 配置Steamworks")

if __name__ == '__main__':
    main()
'''

    file_path: /Users/n3kjm/clawd/modular-synth/packaging/build_package.py
