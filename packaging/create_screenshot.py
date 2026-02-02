#!/usr/bin/env python3
"""
Steam Store Screenshot Generator
生成Steam商店所需的截图 (1920x1080)
使用PIL而不是pygame，更加稳定
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# 颜色定义 (R, G, B)
COLORS = {
    'BACKGROUND': (25, 25, 35),
    'BACKGROUND_LIGHT': (35, 35, 50),
    'CARD_BG': (45, 45, 65),
    'BORDER': (80, 80, 110),
    'ACCENT': (100, 180, 255),
    'TEXT_PRIMARY': (240, 240, 250),
    'TEXT_SECONDARY': (180, 180, 200),
    'KNOB_BG': (70, 70, 100),
}

def create_store_screenshot():
    """创建Steam商店截图"""
    width, height = 1920, 1080
    
    # 创建背景
    img = Image.new('RGB', (width, height), COLORS['BACKGROUND'])
    draw = ImageDraw.Draw(img)
    
    # 尝试加载字体，如果失败使用默认字体
    try:
        # 尝试系统字体
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        tiny_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
            tiny_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            # 使用默认字体
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
            tiny_font = ImageFont.load_default()
    
    # 标题
    title_text = "Modular Synth Studio"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 80), title_text, fill=COLORS['TEXT_PRIMARY'], font=title_font)
    
    # 副标题
    subtitle_text = "Professional Modular Synthesizer - Create Your Music"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text(((width - subtitle_width) // 2, 150), subtitle_text, fill=COLORS['TEXT_SECONDARY'], font=subtitle_font)
    
    # 功能特性
    features = [
        ("Complete Module System", "Oscillators, Filters, Envelopes, LFO, Effects"),
        ("MIDI Keyboard Support", "Real-time performance with external controllers"),
        ("High-Quality Export", "WAV/FLAC format, up to 32-bit depth"),
        ("Cloud Sync", "Cross-device preset sharing and community"),
        ("Modern Interface", "3 Themes: Dark, Retro, Cyberpunk"),
        ("200+ Presets", "Lead, Bass, Pad, FX, Keys - all included"),
    ]
    
    feature_y = 240
    for title, desc in features:
        # 背景框
        draw.rounded_rectangle([200, feature_y, 1720, feature_y + 80], radius=10, fill=COLORS['CARD_BG'], outline=COLORS['BORDER'])
        
        # 标题
        draw.text((230, feature_y + 20), f"[✓] {title}", fill=COLORS['ACCENT'], font=small_font)
        
        # 描述
        draw.text((350, feature_y + 30), desc, fill=COLORS['TEXT_PRIMARY'], font=tiny_font)
        
        feature_y += 100
    
    # 合成器界面模拟
    synth_y = feature_y + 50
    
    # 左侧：合成器界面
    draw.rounded_rectangle([100, synth_y, 920, synth_y + 350], radius=10, fill=COLORS['BACKGROUND_LIGHT'], outline=COLORS['BORDER'])
    draw.text((100, synth_y - 35), "Real-time Synthesizer Interface", fill=COLORS['TEXT_PRIMARY'], font=subtitle_font)
    
    # 旋钮
    for i in range(4):
        knob_x = 150 + i * 180
        knob_y = synth_y + 100
        
        # 旋钮背景
        draw.ellipse([knob_x - 40, knob_y - 40, knob_x + 40, knob_y + 40], fill=COLORS['KNOB_BG'], outline=COLORS['ACCENT'], width=2)
        
        # 旋钮指示
        angle = -45 + i * 30
        indicator_x = knob_x + 30 * math.cos(math.radians(angle))
        indicator_y = knob_y + 30 * math.sin(math.radians(angle))
        draw.line([knob_x, knob_y, indicator_x, indicator_y], fill=COLORS['TEXT_PRIMARY'], width=3)
    
    # 波形显示
    wave_rect = [150, synth_y + 180, 870, synth_y + 300]
    draw.rectangle(wave_rect, fill=COLORS['BACKGROUND'])
    
    # 绘制波形
    points = []
    for x in range(720):
        y = synth_y + 240 + math.sin(x * 0.05) * 40 + math.sin(x * 0.02) * 20
        points.append((150 + x, y))
    
    for i in range(len(points) - 1):
        draw.line([points[i][0], points[i][1], points[i+1][0], points[i+1][1]], fill=COLORS['ACCENT'], width=2)
    
    # 右侧：系统要求
    req_x = 1050
    req_y = synth_y
    
    draw.text((req_x, req_y - 35), "System Requirements", fill=COLORS['TEXT_PRIMARY'], font=subtitle_font)
    
    req_items = [
        ("Minimum", "Recommended"),
        ("OS: macOS 10.15+ / Win 10+", "OS: macOS 12+ / Win 11"),
        ("Memory: 4GB RAM", "Memory: 8GB RAM"),
        ("Storage: 500MB", "Storage: 1GB SSD"),
        ("Graphics: Integrated", "Graphics: Dedicated"),
    ]
    
    for i, (label, value) in enumerate(req_items):
        if i == 0:
            draw.text((req_x, req_y), label, fill=COLORS['ACCENT'], font=small_font)
            draw.text((req_x + 300, req_y), value, fill=COLORS['ACCENT'], font=small_font)
            req_y += 35
        else:
            draw.text((req_x, req_y), label, fill=COLORS['TEXT_SECONDARY'], font=tiny_font)
            draw.text((req_x + 300, req_y), value, fill=COLORS['TEXT_PRIMARY'], font=tiny_font)
            req_y += 30
    
    # 底部标签
    tags_y = height - 90
    tags = ["Music Creation", "Audio Production", "Synthesizer", "MIDI", "Education", "Creative"]
    
    for i, tag in enumerate(tags):
        # 计算文本宽度
        tag_bbox = draw.textbbox((0, 0), tag, font=tiny_font)
        tag_width = tag_bbox[2] - tag_bbox[0]
        
        bg_x = 200 + i * 180
        bg_rect = [bg_x, tags_y, bg_x + 160, tags_y + 50]
        draw.rounded_rectangle(bg_rect, radius=25, fill=COLORS['CARD_BG'], outline=COLORS['BORDER'])
        
        # 居中文本
        text_x = bg_x + (160 - tag_width) // 2
        draw.text((text_x, tags_y + 12), tag, fill=COLORS['TEXT_SECONDARY'], font=tiny_font)
    
    # 保存
    output_path = os.path.join(os.path.dirname(__file__), '..', 'screenshot_store.png')
    img.save(output_path, 'PNG')
    print(f"Screenshot saved: {output_path}")
    
    return output_path

if __name__ == "__main__":
    create_store_screenshot()
