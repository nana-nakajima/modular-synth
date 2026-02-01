#!/bin/bash
# 🎹 Modular Synth Studio v0.6.0 启动脚本

echo "🎹 Modular Synth Studio v0.6.0"
echo "================================"

# 检查依赖
echo "📦 检查依赖..."
python3 -c "import pygame, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少依赖，安装中..."
    pip install pygame numpy scipy
fi

# 切换到项目目录
cd "$(dirname "$0")"

# 启动 v0.6.0 现代 GUI
echo "🚀 启动 v0.6.0 现代界面..."
python3 gui/main_window_v2.py

echo "👋 再见！"
