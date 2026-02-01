#!/usr/bin/env python3
# ✨ Visual Effects - 增强视觉效果模块
# 为Modular Synth Studio添加专业级视觉效果

import pygame
import numpy as np

# ============ 渐变色配置 ============
def create_gradient(start_color, end_color, width, height, vertical=True):
    """创建渐变表面"""
    gradient = pygame.Surface((width, height))
    
    for i in range(height if vertical else width):
        ratio = i / (height if vertical else width)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        
        if vertical:
            pygame.draw.line(gradient, (r, g, b), (0, i), (width, i))
        else:
            pygame.draw.line(gradient, (r, g, b), (i, 0), (i, height))
    
    return gradient


def create_panel_gradient(width, height):
    """创建面板渐变 (深色主题)"""
    start_color = (60, 60, 90)
    end_color = (40, 40, 70)
    return create_gradient(start_color, end_color, width, height)


def create_knob_gradient(radius):
    """创建旋钮渐变"""
    knob_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    
    # 径向渐变效果
    center = (radius, radius)
    for r in range(radius, 0, -2):
        ratio = r / radius
        color = (
            int(150 + (220 - 150) * ratio),
            int(150 + (220 - 150) * ratio), 
            int(180 + (255 - 180) * ratio)
        )
        pygame.draw.circle(knob_surf, (*color, 255), center, r)
    
    return knob_surf


# ============ 发光效果 ============
def create_glow(surface, glow_color, glow_radius=10, glow_intensity=0.5):
    """创建发光效果"""
    glow_surf = pygame.Surface(
        (surface.get_width() + glow_radius * 2, 
         surface.get_height() + glow_radius * 2), 
        pygame.SRCALPHA
    )
    
    # 绘制多层发光
    for i in range(glow_radius, 0, -1):
        alpha = int(50 * glow_intensity * (i / glow_radius))
        glow_surf.blit(surface, (glow_radius, glow_radius))
        # 创建发光层
        glow_layer = pygame.Surface(
            (surface.get_width() + i * 2, surface.get_height() + i * 2),
            pygame.SRCALPHA
        )
        pygame.draw.rect(glow_layer, (*glow_color, alpha), 
                        glow_layer.get_rect(), border_radius=i)
        glow_surf.blit(glow_layer, (glow_radius - i, glow_radius - i))
    
    return glow_surf


def draw_glow_circle(surface, center, radius, color, glow_radius=15, intensity=0.6):
    """绘制发光圆圈 (LED效果)"""
    # 外发光
    for i in range(glow_radius, 0, -3):
        alpha = int(80 * intensity * (i / glow_radius))
        pygame.draw.circle(surface, (*color[:3], alpha), center, radius + i)
    
    # 主体
    pygame.draw.circle(surface, color, center, radius)


# ============ 动态波形显示 ============
class WaveformDisplay:
    """动态波形显示器"""
    
    def __init__(self, x, y, width, height, max_points=512):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_points = max_points
        self.data = np.zeros(max_points)
        self.color = (100, 200, 255)
        self.glow_color = (100, 200, 255)
        self.amplitude = 1.0
        self.animation_offset = 0
    
    def update(self, new_data):
        """更新波形数据"""
        if len(new_data) > 0:
            # 归一化并添加到缓冲区
            normalized = np.array(new_data) / np.max(np.abs(new_data)) if np.max(np.abs(new_data)) > 0 else new_data
            self.data = np.roll(self.data, -len(normalized))
            self.data[-len(normalized):] = normalized
    
    def draw(self, surface, show_glow=True):
        """绘制波形"""
        # 绘制背景
        bg_rect = self.rect.inflate(4, 4)
        pygame.draw.rect(surface, (30, 30, 45), bg_rect, border_radius=8)
        pygame.draw.rect(surface, (80, 80, 120), self.rect, 2, border_radius=4)
        
        if show_glow:
            # 绘制发光效果
            glow_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            
            points = []
            for i, val in enumerate(self.data):
                x = self.rect.x + (i / self.max_points) * self.rect.width
                y = self.rect.centery - val * (self.rect.height // 2 - 10) * self.amplitude
                points.append((x, y))
            
            if len(points) > 1:
                # 绘制填充区域
                polygon_points = [points[0]] + points + [points[-1]]
                polygon_points.append((self.rect.right, self.rect.bottom))
                polygon_points.append((self.rect.left, self.rect.bottom))
                
                pygame.draw.polygon(glow_surf, (*self.glow_color, 40), polygon_points)
                surface.blit(glow_surf, (0, 0))
            
            # 绘制主线
            if len(points) > 1:
                pygame.draw.lines(surface, self.color, False, points, 2)
        else:
            # 简单绘制
            points = []
            for i, val in enumerate(self.data):
                x = self.rect.x + (i / self.max_points) * self.rect.width
                y = self.rect.centery - val * (self.rect.height // 2 - 10) * self.amplitude
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(surface, self.color, False, points, 2)


# ============ 动态LED指示灯 ============
class DynamicLED:
    """动态LED指示灯"""
    
    def __init__(self, x, y, radius=8, color=(100, 255, 100), blink_rate=0):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.base_color = color
        self.current_color = color
        self.radius = radius
        self.blink_rate = blink_rate  # 0-1, 0=常亮, 1=快闪
        self.pulse_phase = 0
        self.active = True
    
    def update(self, dt):
        """更新LED状态"""
        if self.blink_rate > 0:
            self.pulse_phase += dt * self.blink_rate * 10
            pulse = (np.sin(self.pulse_phase) + 1) / 2
            
            # 闪烁时颜色变暗
            self.current_color = (
                int(self.base_color[0] * (0.5 + 0.5 * pulse)),
                int(self.base_color[1] * (0.5 + 0.5 * pulse)),
                int(self.base_color[2] * (0.5 + 0.5 * pulse))
            )
        else:
            self.current_color = self.base_color
    
    def draw(self, surface, show_glow=True):
        """绘制LED"""
        if show_glow:
            draw_glow_circle(
                surface, 
                self.rect.center, 
                self.radius, 
                self.current_color,
                glow_radius=12,
                intensity=0.7
            )
        else:
            pygame.draw.circle(surface, self.current_color, self.rect.center, self.radius)


# ============ 旋钮增强 ============
class EnhancedKnob:
    """增强版旋钮 (带视觉效果)"""
    
    def __init__(self, x, y, label, min_val, max_val, default, callback=None):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        self.value = default
        self.callback = callback
        self.dragging = False
        self.drag_start_y = 0
        self.drag_start_value = 0
        
        # 视觉效果
        self.gradient_surf = create_knob_gradient(25)
        self.hovered = False
        self.press_animation = 0
    
    def draw(self, surface, font):
        # 绘制标签
        label_surf = font.render(self.label, True, (220, 220, 240))
        surface.blit(label_surf, (self.rect.x + 25 - label_surf.get_width()//2, self.rect.y - 20))
        
        # 绘制旋钮背景阴影
        shadow_rect = self.rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.circle(surface, (20, 20, 30), self.rect.center, 27)
        
        # 绘制旋钮渐变
        surface.blit(self.gradient_surf, (self.rect.x, self.rect.y))
        
        # 绘制边框
        border_color = (150, 150, 200) if self.hovered else (100, 100, 140)
        pygame.draw.circle(surface, border_color, self.rect.center, 25, 2)
        
        # 绘制旋钮位置指示线
        angle = (self.value - self.min_val) / (self.max_val - self.min_val) * 270 - 135
        angle_rad = np.radians(angle)
        knob_x = self.rect.centerx + 18 * np.cos(angle_rad)
        knob_y = self.rect.centery + 18 * np.sin(angle_rad)
        
        # 指示线颜色
        line_color = (255, 255, 255) if self.hovered else (200, 200, 220)
        pygame.draw.line(surface, line_color, self.rect.center, (knob_x, knob_y), 4)
        
        # 中心点
        pygame.draw.circle(surface, (255, 255, 255), self.rect.center, 3)
        
        # 绘制值
        value_str = f"{self.value:.2f}"
        value_surf = font.render(value_str, True, (200, 200, 220))
        surface.blit(value_surf, (self.rect.x + 25 - value_surf.get_width()//2, self.rect.y + 32))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.drag_start_y = event.pos[1]
                self.drag_start_value = self.value
                self.press_animation = 1.0
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                delta = (self.drag_start_y - event.pos[1]) / 100
                new_value = self.drag_start_value + delta
                new_value = max(self.min_val, min(self.max_val, new_value))
                
                if new_value != self.value:
                    self.value = new_value
                    if self.callback:
                        self.callback(self.value)
                return True
        
        return False


# ============ 模块背景增强 ============
def draw_module_background(surface, rect, title, font, is_active=False):
    """绘制增强版模块背景"""
    # 渐变背景
    gradient = create_panel_gradient(rect.width, rect.height)
    surface.blit(gradient, (rect.x, rect.y))
    
    # 边框
    border_color = (120, 120, 160) if is_active else (100, 100, 140)
    pygame.draw.rect(surface, border_color, rect, 2, border_radius=6)
    
    # 标题栏背景
    title_bg = pygame.Rect(rect.x + 2, rect.y + 2, rect.width - 4, 30)
    title_gradient = create_gradient((70, 70, 100), (50, 50, 80), title_bg.width, title_bg.height)
    surface.blit(title_gradient, (title_bg.x, title_bg.y))
    
    # 标题
    title_surf = font.render(title, True, (255, 255, 255))
    surface.blit(title_surf, (rect.x + 15, rect.y + 8))
    
    # 装饰线
    pygame.draw.line(surface, border_color,
                    (rect.x + 10, rect.y + 35),
                    (rect.right - 10, rect.y + 35), 1)


# ============ 频谱分析器 ============
class SpectrumAnalyzer:
    """实时频谱分析器"""
    
    def __init__(self, x, y, width, height, bins=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.bins = bins
        self.levels = np.zeros(bins)
        self.colors = self._generate_colors()
        self.animation_speed = 0.15
    
    def _generate_colors(self):
        """生成彩虹色谱"""
        colors = []
        for i in range(self.bins):
            hue = i / self.bins
            rgb = self._hsv_to_rgb(hue, 0.8, 1.0)
            colors.append(rgb)
        return colors
    
    def _hsv_to_rgb(self, h, s, v):
        """HSV转RGB"""
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))
    
    def update(self, audio_data):
        """更新频谱数据"""
        if len(audio_data) > 0:
            # 简单的FFT近似
            spectrum = np.abs(np.fft.fft(audio_data))[:len(audio_data)//2]
            spectrum = spectrum / (np.max(spectrum) + 1e-6)
            
            # 分桶
            bin_size = max(1, len(spectrum) // self.bins)
            new_levels = []
            for i in range(self.bins):
                start = i * bin_size
                end = start + bin_size
                level = np.mean(spectrum[start:end]) if end <= len(spectrum) else 0
                new_levels.append(level)
            
            # 平滑过渡
            self.levels = self.levels * (1 - self.animation_speed) + np.array(new_levels) * self.animation_speed
    
    def draw(self, surface):
        """绘制频谱"""
        # 背景
        pygame.draw.rect(surface, (25, 25, 40), self.rect, border_radius=4)
        pygame.draw.rect(surface, (80, 80, 120), self.rect, 1, border_radius=4)
        
        bar_width = (self.rect.width - 10) // self.bins
        bar_max_height = self.rect.height - 10
        
        for i, level in enumerate(self.levels):
            bar_height = level * bar_max_height
            x = self.rect.x + 5 + i * bar_width
            y = self.rect.bottom - 5 - bar_height
            
            # 绘制条形
            color = self.colors[i]
            rect = pygame.Rect(x, y, bar_width - 2, bar_height)
            pygame.draw.rect(surface, color, rect)
            
            # 顶部高光
            pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width - 2, 2))


# ============ 键盘灯光效果 ============
class KeyLight:
    """键盘按键灯光效果"""
    
    def __init__(self, rect, note_name, color=(100, 200, 255)):
        self.rect = rect
        self.note_name = note_name
        self.base_color = color
        self.current_color = color
        self.pressed = False
        self.press_animation = 0.0
        self.glow_radius = 8
    
    def update(self, dt):
        """更新灯光状态"""
        if self.pressed:
            self.press_animation = min(1.0, self.press_animation + dt * 8)
        else:
            self.press_animation = max(0.0, self.press_animation - dt * 12)
        
        # 颜色根据按压状态变化
        ratio = self.press_animation
        self.current_color = (
            int(self.base_color[0] * (0.5 + 0.5 * ratio)),
            int(self.base_color[1] * (0.5 + 0.5 * ratio)),
            int(self.base_color[2] * (0.5 + 0.5 * ratio))
        )
    
    def draw(self, surface):
        """绘制按键灯光"""
        # 基础按键
        color = self.current_color if self.pressed else (60, 60, 80)
        pygame.draw.rect(surface, color, self.rect, border_radius=4)
        
        # 边框
        border_color = self.current_color if self.pressed else (100, 100, 140)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=4)
        
        # 发光效果（按下时）
        if self.press_animation > 0.3:
            glow_intensity = (self.press_animation - 0.3) / 0.7
            for i in range(self.glow_radius, 0, -2):
                alpha = int(60 * glow_intensity * (i / self.glow_radius))
                glow_rect = self.rect.inflate(i * 2, i * 2)
                pygame.draw.rect(surface, (*self.current_color[:3], alpha), 
                                glow_rect, border_radius=6)
        
        # 音符标签
        font = pygame.font.Font(None, 24)
        text = font.render(self.note_name, True, (255, 255, 255))
        surface.blit(text, (
            self.rect.centerx - text.get_width() // 2,
            self.rect.bottom - 20
        ))
