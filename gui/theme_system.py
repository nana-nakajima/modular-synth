#!/usr/bin/env python3
# 🎨 Modular Synth 主题系统 - v0.6.0
# Nana的虚拟模块合成器 - 现代化主题

import pygame

# ============ 主题配置 ============
class ThemeColors:
    """主题颜色配置"""
    
    # 默认主题 (暗色现代风)
    DARK = {
        # 背景
        'bg_primary': (15, 15, 25),      # 深蓝黑背景
        'bg_secondary': (25, 25, 40),    # 次要背景
        'bg_panel': (35, 35, 55),        # 面板背景
        'bg_module': (45, 45, 70),       # 模块背景
        
        # 边框和线条
        'border': (70, 70, 100),         # 边框颜色
        'border_highlight': (100, 120, 180),  # 高亮边框
        
        # 文字
        'text_primary': (240, 240, 255), # 主文字
        'text_secondary': (160, 160, 190), # 次要文字
        'text_accent': (120, 200, 255),  # 强调文字
        
        # UI元素
        'knob': (180, 180, 220),         # 旋钮
        'knob_indicator': (100, 220, 255),  # 旋钮指示器
        'slider': (80, 150, 220),        # 滑块
        
        # 指示灯和状态
        'led_on': (50, 255, 100),        # LED开
        'led_off': (60, 60, 80),         # LED关
        'waveform': (80, 200, 255),      # 波形颜色
        'spectrum': (150, 100, 255),     # 频谱颜色
        
        # 连接线
        'cable': (100, 100, 140),        # 连接线
        'cable_active': (120, 180, 255), # 激活的连接线
        
        # 特殊效果
        'glow': (80, 160, 255, 100),     # 发光效果
        'shadow': (0, 0, 0, 150),        # 阴影
    }
    
    # 复古主题
    RETRO = {
        'bg_primary': (0, 0, 0),
        'bg_secondary': (30, 30, 30),
        'bg_panel': (50, 50, 50),
        'bg_module': (70, 70, 70),
        'border': (100, 100, 100),
        'border_highlight': (150, 150, 150),
        'text_primary': (200, 200, 200),
        'text_secondary': (140, 140, 140),
        'text_accent': (255, 200, 100),
        'knob': (180, 180, 180),
        'knob_indicator': (255, 255, 100),
        'slider': (150, 150, 150),
        'led_on': (0, 255, 0),
        'led_off': (50, 50, 50),
        'waveform': (100, 255, 100),
        'spectrum': (100, 255, 100),
        'cable': (80, 80, 80),
        'cable_active': (100, 255, 100),
        'glow': (100, 255, 100, 80),
        'shadow': (0, 0, 0, 180),
    }
    
    # 赛博朋克主题
    CYBER = {
        'bg_primary': (10, 5, 20),
        'bg_secondary': (20, 10, 35),
        'bg_panel': (30, 15, 50),
        'bg_module': (40, 20, 65),
        'border': (200, 50, 150),
        'border_highlight': (255, 100, 200),
        'text_primary': (255, 240, 255),
        'text_secondary': (180, 150, 200),
        'text_accent': (255, 100, 200),
        'knob': (255, 150, 220),
        'knob_indicator': (255, 100, 200),
        'slider': (200, 50, 150),
        'led_on': (255, 50, 200),
        'led_off': (60, 20, 80),
        'waveform': (255, 100, 200),
        'spectrum': (100, 200, 255),
        'cable': (150, 50, 120),
        'cable_active': (255, 150, 220),
        'glow': (255, 100, 200, 100),
        'shadow': (0, 0, 0, 150),
    }


class ThemeManager:
    """主题管理器"""
    
    def __init__(self, theme_name='DARK'):
        self.current_theme = theme_name
        self.colors = ThemeColors.DARK.copy()
        self.available_themes = ['DARK', 'RETRO', 'CYBER']
        self.load_theme(theme_name)
    
    def load_theme(self, theme_name):
        """加载主题"""
        if theme_name == 'DARK':
            self.colors = ThemeColors.DARK.copy()
        elif theme_name == 'RETRO':
            self.colors = ThemeColors.RETRO.copy()
        elif theme_name == 'CYBER':
            self.colors = ThemeColors.CYBER.copy()
        else:
            self.colors = ThemeColors.DARK.copy()
        self.current_theme = theme_name
    
    def get_color(self, key):
        """获取颜色"""
        return self.colors.get(key, (255, 255, 255))
    
    def cycle_theme(self):
        """切换到下一个主题"""
        current_idx = self.available_themes.index(self.current_theme)
        next_idx = (current_idx + 1) % len(self.available_themes)
        self.load_theme(self.available_themes[next_idx])
        return self.current_theme


# ============ 尺寸配置 ============
class LayoutConfig:
    """布局配置"""
    
    # 屏幕尺寸
    SCREEN_WIDTH = 1400
    SCREEN_HEIGHT = 900
    
    # 模块尺寸
    MODULE_WIDTH = 200
    MODULE_HEIGHT = 450
    
    # 模块间距
    MODULE_MARGIN = 20
    MODULE_TOP_MARGIN = 80
    
    # 旋钮尺寸
    KNOB_SIZE = 44
    KNOB_INDICATOR_LENGTH = 16
    
    # 波形显示
    WAVE_DISPLAY_HEIGHT = 180
    
    # 字体大小
    FONT_TITLE = 28
    FONT_HEADER = 22
    FONT_NORMAL = 18
    FONT_SMALL = 14


# ============ 视觉增强函数 ============
def draw_glow_surface(surface, color, rect, radius=10, intensity=0.5):
    """绘制发光效果"""
    # 创建发光表面
    glow_surf = pygame.Surface((rect.width + radius*4, rect.height + radius*4), pygame.SRCALPHA)
    
    # 绘制发光
    glow_color = (*color[:3], int(255 * intensity))
    pygame.draw.rect(glow_surf, glow_color, 
                    (radius, radius, rect.width + radius*2, rect.height + radius*2), 
                    border_radius=radius)
    
    # 应用高斯模糊（模拟）
    surface.blit(glow_surf, (rect.x - radius*2, rect.y - radius*2))


def draw_rounded_rect(surface, color, rect, radius=8, width=0):
    """绘制圆角矩形"""
    x, y, w, h = rect
    
    # 绘制圆角矩形
    pygame.draw.rect(surface, color, (x + radius, y, w - radius*2, h), width=width)
    pygame.draw.rect(surface, color, (x, y + radius, w, h - radius*2), width=width)
    
    # 绘制角落
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius, width=width)
    pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius, width=width)
    pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius, width=width)
    pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius, width=width)


def draw_knob_with_theme(surface, rect, value, theme, label="", show_value=True):
    """绘制旋钮（带主题）"""
    center_x, center_y = rect.centerx, rect.centery
    radius = rect.width // 2
    
    # 旋钮背景
    pygame.draw.circle(surface, theme.get_color('bg_module'), (center_x, center_y), radius)
    pygame.draw.circle(surface, theme.get_color('border'), (center_x, center_y), radius, 2)
    
    # 旋钮指示器
    angle = (value - 0.5) * 270  # -135 到 135 度
    angle_rad = pygame.math.radians(angle + 90)  # 调整为顶部为0
    
    indicator_x = center_x + (radius - 8) * pygame.math.cos(angle_rad)
    indicator_y = center_y + (radius - 8) * pygame.math.sin(angle_rad)
    
    pygame.draw.line(surface, theme.get_color('knob_indicator'), 
                    (center_x, center_y), (indicator_x, indicator_y), 3)
    
    # 中心点
    pygame.draw.circle(surface, theme.get_color('knob'), (center_x, center_y), 4)


def draw_waveform_with_gradient(surface, rect, data, theme, gradient_colors=None):
    """绘制波形（带渐变效果）"""
    if gradient_colors is None:
        gradient_colors = [
            theme.get_color('waveform'),
            theme.get_color('spectrum')
        ]
    
    # 绘制中心线
    center_y = rect.centery
    pygame.draw.line(surface, theme.get_color('bg_panel'), 
                    (rect.x, center_y), (rect.right, center_y), 1)
    
    # 绘制波形
    if data is not None and len(data) > 0:
        # 缩放到显示区域
        display_data = data[:rect.width - 40]
        display_data = display_data * (rect.height - 60) / 2
        
        points = []
        for i, sample in enumerate(display_data):
            x = rect.x + 20 + i
            y = center_y - sample
            points.append((x, y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, theme.get_color('waveform'), False, points, 2)


# ============ 预设主题实例 ============
default_theme = ThemeManager('DARK')
