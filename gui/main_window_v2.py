#!/usr/bin/env python3
# 🎹 Modular Synth GUI v0.6.0 - 现代主题版
# Nana的虚拟模块合成器 - 现代化图形用户界面

import pygame
import json
import os
import numpy as np
from audio.core_modules import Oscillator, Filter, Envelope, LFO, MultiOscillator
from gui.theme_system import ThemeManager, LayoutConfig, draw_knob_with_theme, draw_rounded_rect

# 尝试导入实时音频模块
try:
    from audio.real_time_player import RealTimeSynth
    HAS_REALTIME_AUDIO = True
except ImportError:
    HAS_REALTIME_AUDIO = False
    print("⚠️ 实时音频模块不可用")


# ============ 旋钮控件 v0.6.0 ============
class ModernKnob:
    """现代化旋钮控件"""
    
    def __init__(self, x, y, label, min_val, max_val, default, callback=None, size=44):
        self.rect = pygame.Rect(x, y, size, size)
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        self.value = default
        self.callback = callback
        self.dragging = False
        self.drag_start_y = 0
        self.drag_start_value = 0
        self.theme = default_theme
        self.show_value = True
    
    def draw(self, surface, font):
        # 绘制标签
        label_surf = font.render(self.label, True, self.theme.get_color('text_secondary'))
        surface.blit(label_surf, (self.rect.centerx - label_surf.get_width()//2, self.rect.y - 18))
        
        # 绘制旋钮
        draw_knob_with_theme(surface, self.rect, (self.value - self.min_val) / (self.max_val - self.min_val), 
                            self.theme, self.label)
        
        # 显示数值
        if self.show_value:
            value_str = f"{self.value:.1f}" if self.max_val - self.min_val > 10 else f"{self.value:.2f}"
            value_surf = font.render(value_str, True, self.theme.get_color('text_accent'))
            surface.blit(value_surf, (self.rect.centerx - value_surf.get_width()//2, self.rect.bottom + 2))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.drag_start_y = event.pos[1]
                self.drag_start_value = self.value
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
                        self.callback(new_value)
                return True
        
        return False


# ============ 按钮控件 ============
class ModernButton:
    """现代化按钮"""
    
    def __init__(self, x, y, width, height, text, callback=None, theme_manager=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.theme = theme_manager or default_theme
        self.hovered = False
        self.pressed = False
    
    def draw(self, surface, font):
        # 按钮背景
        bg_color = self.theme.get_color('bg_panel')
        border_color = self.theme.get_color('border_highlight') if self.hovered else self.theme.get_color('border')
        
        # 绘制圆角按钮
        draw_rounded_rect(surface, bg_color, self.rect, radius=6)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=6)
        
        # 文字
        text_surf = font.render(self.text, True, self.theme.get_color('text_primary'))
        surface.blit(text_surf, (self.rect.centerx - text_surf.get_width()//2, 
                                  self.rect.centery - text_surf.get_height()//2))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
            self.pressed = False
        
        return False


# ============ LED指示灯 ============
class LEDIndicator:
    """LED指示灯"""
    
    def __init__(self, x, y, size=10, color_on=None, color_off=None, theme_manager=None):
        self.rect = pygame.Rect(x, y, size, size)
        self.theme = theme_manager or default_theme
        self.color_on = color_on or self.theme.get_color('led_on')
        self.color_off = color_off or self.theme.get_color('led_off')
        self.state = False
    
    def draw(self, surface, font):
        color = self.color_on if self.state else self.color_off
        pygame.draw.circle(surface, color, self.rect.center, self.rect.width//2)
        pygame.draw.circle(surface, self.theme.get_color('border'), self.rect.center, self.rect.width//2, 1)


# ============ 模块基类 v0.6.0 ============
class ModernModule:
    """现代化模块基类"""
    
    def __init__(self, x, y, width, height, title, theme_manager=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.knobs = []
        self.buttons = []
        self.leds = []
        self.theme = theme_manager or default_theme
    
    def draw(self, surface, font):
        # 模块背景
        bg_color = self.theme.get_color('bg_module')
        border_color = self.theme.get_color('border')
        highlight_color = self.theme.get_color('border_highlight')
        
        # 绘制圆角背景
        draw_rounded_rect(surface, bg_color, self.rect, radius=12)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=12)
        
        # 标题栏
        title_bg = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, 35)
        draw_rounded_rect(surface, self.theme.get_color('bg_panel'), title_bg, radius=10)
        
        # 标题文字
        title_surf = font.render(self.title.upper(), True, self.theme.get_color('text_accent'))
        surface.blit(title_surf, (self.rect.x + 15, self.rect.y + 12))
        
        # 分割线
        pygame.draw.line(surface, self.theme.get_color('border'), 
                        (self.rect.x + 10, self.rect.y + 40), 
                        (self.rect.right - 10, self.rect.y + 40), 1)
        
        # 绘制控件
        for knob in self.knobs:
            knob.draw(surface, font)
        
        for button in self.buttons:
            button.draw(surface, font)
        
        for led in self.leds:
            led.draw(surface, font)
    
    def handle_event(self, event):
        for knob in self.knobs:
            if knob.handle_event(event):
                return True
        
        for button in self.buttons:
            if button.handle_event(event):
                return True
        
        return False


# ============ 振荡器模块 v0.6.0 ============
class OscillatorModuleV2(ModernModule):
    """振荡器模块 v0.6.0"""
    
    def __init__(self, x, y, theme_manager=None):
        super().__init__(x, y, LayoutConfig.MODULE_WIDTH, LayoutConfig.MODULE_HEIGHT, "OSCILLATOR", theme_manager)
        
        self.osc = Oscillator(frequency=440, wave_type='sine')
        
        # 波形类型列表
        self.wave_types = ['sine', 'sawtooth', 'square', 'triangle']
        self.wave_names = ['SINE', 'SAW', 'SQR', 'TRI']
        self.wave_colors = [
            (100, 200, 255),  # Sine - 蓝色
            (255, 150, 100),  # Saw - 橙色
            (150, 255, 150),  # Square - 绿色
            (255, 200, 100),  # Triangle - 黄色
        ]
        self.current_wave = 0
        
        # 频率旋钮
        freq_knob = ModernKnob(x + 78, y + 80, "FREQUENCY", 20, 2000, 440, 
                               lambda v: self.osc.set_frequency(v), size=44)
        self.knobs.append(freq_knob)
        
        # 波形选择按钮
        for i, (wave_name, wave_color) in enumerate(zip(self.wave_names, self.wave_colors)):
            btn_x = x + 20 + i * 45
            btn_y = y + 150
            
            def make_callback(idx=i):
                return lambda: self.set_wave(idx)
            
            btn = ModernButton(btn_x, btn_y, 40, 30, wave_name, make_callback(), theme_manager)
            btn.wave_color = wave_color
            self.buttons.append(btn)
        
        # 波形LED指示
        for i in range(4):
            led_x = x + 20 + i * 45 + 15
            led_y = y + 185
            led = LEDIndicator(led_x, led_y, size=8, color_on=self.wave_colors[i], theme_manager=theme_manager)
            self.leds.append(led)
        self.leds[0].state = True
    
    def set_wave(self, index):
        self.current_wave = index
        wave_type = self.wave_types[index]
        self.osc.set_wave_type(wave_type)
        
        # 更新LED状态
        for i, led in enumerate(self.leds):
            led.state = (i == index)
        
        # 实时音频
        if hasattr(self, 'synth') and self.synth:
            self.synth.set_wave_type(wave_type)
    
    def draw(self, surface, font):
        super().draw(surface, font)
        
        # 绘制波形预览
        wave_preview = self.osc.generate(duration=0.05)
        wave_preview = wave_preview * 40 + self.rect.y + 250
        
        # 波形显示区域
        wave_rect = pygame.Rect(self.rect.x + 15, self.rect.y + 220, self.rect.width - 30, 100)
        pygame.draw.rect(surface, self.theme.get_color('bg_panel'), wave_rect, border_radius=6)
        
        # 绘制波形线
        points = []
        for i, y in enumerate(wave_preview):
            x = wave_rect.x + 10 + i * (wave_rect.width - 20) // len(wave_preview)
            if x <= wave_rect.right - 10:
                points.append((x, y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, self.wave_colors[self.current_wave], False, points, 2)


# ============ 滤波器模块 v0.6.0 ============
class FilterModuleV2(ModernModule):
    """滤波器模块 v0.6.0"""
    
    def __init__(self, x, y, theme_manager=None):
        super().__init__(x, y, LayoutConfig.MODULE_WIDTH, LayoutConfig.MODULE_HEIGHT, "FILTER", theme_manager)
        
        self.filter = Filter(cutoff=1000, filter_type='lowpass')
        self.filter_types = ['lowpass', 'highpass', 'bandpass']
        self.filter_names = ['LP', 'HP', 'BP']
        self.current_type = 0
        
        # 截止频率旋钮
        cutoff_knob = ModernKnob(x + 78, y + 80, "CUTOFF", 100, 5000, 1000,
                                  lambda v: self.filter.set_cutoff(v), size=44)
        self.knobs.append(cutoff_knob)
        
        # 共振旋钮
        res_knob = ModernKnob(x + 78, y + 160, "RESONANCE", 0, 20, 5,
                              lambda v: setattr(self.filter, 'resonance', v) if hasattr(self.filter, 'resonance') else None, 
                              size=44)
        self.knobs.append(res_knob)
        
        # 滤波器类型按钮
        for i, type_name in enumerate(self.filter_names):
            btn_x = x + 20 + i * 55
            btn_y = y + 240
            
            def make_callback(idx=i):
                return lambda: self.set_filter_type(idx)
            
            btn = ModernButton(btn_x, btn_y, 50, 25, type_name, make_callback(), theme_manager)
            self.buttons.append(btn)
    
    def set_filter_type(self, index):
        self.current_type = index
        self.filter.filter_type = self.filter_types[index]
    
    def draw(self, surface, font):
        super().draw(surface, font)
        
        # 绘制滤波器响应曲线
        center_y = self.rect.y + 320
        center_x = self.rect.centerx
        
        # 简化响应曲线
        if self.current_type == 0:  # Lowpass
            points = [
                (self.rect.x + 20, center_y + 60),
                (self.rect.x + 80, center_y + 60),
                (self.rect.x + 140, center_y - 50),
                (self.rect.right - 20, center_y - 55),
            ]
        elif self.current_type == 1:  # Highpass
            points = [
                (self.rect.x + 20, center_y - 55),
                (self.rect.x + 60, center_y - 50),
                (self.rect.x + 120, center_y + 60),
                (self.rect.right - 20, center_y + 60),
            ]
        else:  # Bandpass
            points = [
                (self.rect.x + 20, center_y + 50),
                (self.rect.x + 60, center_y - 40),
                (self.rect.x + 100, center_y - 45),
                (self.rect.x + 140, center_y + 55),
                (self.rect.right - 20, center_y + 55),
            ]
        
        pygame.draw.lines(surface, self.theme.get_color('waveform'), False, points, 2)


# ============ 包络模块 v0.6.0 ============
class EnvelopeModuleV2(ModernModule):
    """ADSR包络模块 v0.6.0"""
    
    def __init__(self, x, y, theme_manager=None):
        super().__init__(x, y, LayoutConfig.MODULE_WIDTH, LayoutConfig.MODULE_HEIGHT, "ENVELOPE", theme_manager)
        
        self.env = Envelope(attack=0.1, decay=0.2, sustain=0.7, release=0.3)
        
        # 四个ADSR旋钮
        knob_y = y + 80
        knob_spacing = 40
        
        attack_knob = ModernKnob(x + 20, knob_y, "A", 0.001, 2.0, 0.1,
                                 lambda v: setattr(self.env, 'attack', v), size=38)
        self.knobs.append(attack_knob)
        
        decay_knob = ModernKnob(x + 20 + knob_spacing, knob_y, "D", 0.01, 2.0, 0.2,
                                lambda v: setattr(self.env, 'decay', v), size=38)
        self.knobs.append(decay_knob)
        
        sustain_knob = ModernKnob(x + 20 + knob_spacing * 2, knob_y, "S", 0.0, 1.0, 0.7,
                                  lambda v: setattr(self.env, 'sustain', v), size=38)
        self.knobs.append(sustain_knob)
        
        release_knob = ModernKnob(x + 20 + knob_spacing * 3, knob_y, "R", 0.01, 3.0, 0.3,
                                  lambda v: setattr(self.env, 'release', v), size=38)
        self.knobs.append(release_knob)
        
        # 增益旋钮
        gain_knob = ModernKnob(x + 78, y + 180, "GAIN", 0.1, 2.0, 1.0,
                               lambda v: None, size=44)
        self.knobs.append(gain_knob)
    
    def draw(self, surface, font):
        super().draw(surface, font)
        
        # 绘制ADSR曲线
        center_y = self.rect.y + 280
        
        points = [
            (self.rect.x + 30, center_y + 70),
            (self.rect.x + 60, center_y - 40),
            (self.rect.x + 90, center_y),
            (self.rect.x + 130, center_y),
            (self.rect.x + 160, center_y + 70),
        ]
        
        pygame.draw.lines(surface, self.theme.get_color('waveform'), False, points, 3)


# ============ LFO模块 v0.6.0 ============
class LFOModuleV2(ModernModule):
    """LFO模块 v0.6.0"""
    
    def __init__(self, x, y, theme_manager=None):
        super().__init__(x, y, LayoutConfig.MODULE_WIDTH, 280, "LFO", theme_manager)
        
        self.lfo = LFO(frequency=2, wave_type='sine')
        
        # 频率旋钮
        freq_knob = ModernKnob(x + 78, y + 60, "FREQ", 0.1, 20, 2,
                               lambda v: self.lfo.set_frequency(v), size=44)
        self.knobs.append(freq_knob)
        
        # 波形类型
        self.wave_types = ['sine', 'sawtooth', 'square', 'triangle']
        self.current_wave = 0
        
        for i, wave_name in enumerate(['SIN', 'SAW', 'SQR', 'TRI']):
            btn_x = x + 20 + i * 42
            btn_y = y + 140
            
            def make_callback(idx=i):
                return lambda: self.set_wave(idx)
            
            btn = ModernButton(btn_x, btn_y, 38, 25, wave_name, make_callback(), theme_manager)
            self.buttons.append(btn)
    
    def set_wave(self, index):
        self.current_wave = index
        self.lfo.set_wave_type(self.wave_types[index])
    
    def draw(self, surface, font):
        super().draw(surface, font)
        
        # 绘制LFO波形
        wave = self.lfo.generate(duration=0.5)
        wave = wave * 30 + self.rect.y + 210
        
        points = []
        for i, y in enumerate(wave):
            x = self.rect.x + 20 + i * (self.rect.width - 40) // len(wave)
            if x <= self.rect.right - 20:
                points.append((x, y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, self.theme.get_color('waveform'), False, points, 2)


# ============ 波形显示器 v0.6.0 ============
class WaveformDisplayV2:
    """波形显示器 v0.6.0"""
    
    def __init__(self, x, y, width, height, theme_manager=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.theme = theme_manager or default_theme
        self.audio_data = None
        self.peak_level = 0
    
    def set_audio(self, audio):
        """设置音频数据"""
        self.audio_data = audio
        if audio is not None:
            self.peak_level = max(abs(audio.max()), abs(audio.min())) if len(audio) > 0 else 0
    
    def draw(self, surface, font):
        # 背景
        bg_color = self.theme.get_color('bg_secondary')
        border_color = self.theme.get_color('border')
        
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=8)
        
        # 标题栏
        title_bg = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, 30)
        pygame.draw.rect(surface, self.theme.get_color('bg_panel'), title_bg, border_radius=6)
        
        # 标题
        title = font.render("OUTPUT WAVEFORM", True, self.theme.get_color('text_accent'))
        surface.blit(title, (self.rect.x + 15, self.rect.y + 8))
        
        # 绘制中心线
        center_y = self.rect.centery
        pygame.draw.line(surface, self.theme.get_color('border'), 
                        (self.rect.x + 10, center_y),
                        (self.rect.right - 10, center_y), 1)
        
        # 绘制波形
        if self.audio_data is not None and len(self.audio_data) > 0:
            display_data = self.audio_data[:self.rect.width - 40]
            display_data = display_data * (self.rect.height - 80) / 2
            
            points = []
            for i, sample in enumerate(display_data):
                x = self.rect.x + 20 + i
                y = center_y - sample
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(surface, self.theme.get_color('waveform'), False, points, 2)
        
        # 绘制电平表
        level_width = 8
        level_height = self.rect.height - 60
        level_x = self.rect.right - 25
        level_y = self.rect.y + 40
        
        # 背景
        pygame.draw.rect(surface, self.theme.get_color('bg_panel'), 
                        (level_x, level_y, level_width, level_height), border_radius=4)
        
        # 电平指示
        if self.peak_level > 0:
            fill_height = min(self.peak_level * level_height, level_height)
            level_color = self.theme.get_color('led_on') if self.peak_level < 0.9 else (255, 100, 100)
            pygame.draw.rect(surface, level_color, 
                            (level_x, level_y + level_height - fill_height, level_width, fill_height),
                            border_radius=4)


# ============ 主界面 v0.6.0 ============
class SynthGUIV2:
    """合成器主界面 v0.6.0 - 现代主题"""
    
    def __init__(self):
        pygame.init()
        
        # 屏幕设置
        self.screen = pygame.display.set_mode((LayoutConfig.SCREEN_WIDTH, LayoutConfig.SCREEN_HEIGHT))
        pygame.display.set_caption("🎹 Modular Synth Studio v0.6.0 - Nana's Project")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, LayoutConfig.FONT_NORMAL)
        self.title_font = pygame.font.Font(None, LayoutConfig.FONT_TITLE)
        self.small_font = pygame.font.Font(None, LayoutConfig.FONT_SMALL)
        
        # 主题系统
        self.theme = ThemeManager('DARK')
        
        # 创建模块
        module_x = LayoutConfig.MODULE_MARGIN
        module_y = LayoutConfig.MODULE_TOP_MARGIN
        
        self.osc_module = OscillatorModuleV2(module_x, module_y, self.theme)
        self.filter_module = FilterModuleV2(module_x + LayoutConfig.MODULE_WIDTH + LayoutConfig.MODULE_MARGIN, 
                                            module_y, self.theme)
        self.env_module = EnvelopeModuleV2(module_x + (LayoutConfig.MODULE_WIDTH + LayoutConfig.MODULE_MARGIN) * 2, 
                                           module_y, self.theme)
        self.lfo_module = LFOModuleV2(module_x + (LayoutConfig.MODULE_WIDTH + LayoutConfig.MODULE_MARGIN) * 3, 
                                      module_y, self.theme)
        
        # 波形显示
        self.waveform = WaveformDisplayV2(
            LayoutConfig.MODULE_MARGIN, 
            LayoutConfig.SCREEN_HEIGHT - LayoutConfig.WAVE_DISPLAY_HEIGHT - 20,
            LayoutConfig.SCREEN_WIDTH - LayoutConfig.MODULE_MARGIN * 2,
            LayoutConfig.WAVE_DISPLAY_HEIGHT,
            self.theme
        )
        
        # 状态变量
        self.running = True
        self.audio_buffer = None
        
        # 键盘音阶
        self.key_notes = {
            pygame.K_a: 261.63, pygame.K_s: 293.66, pygame.K_d: 329.63,
            pygame.K_f: 349.23, pygame.K_g: 392.00, pygame.K_h: 440.00,
            pygame.K_j: 493.88, pygame.K_k: 523.25,
        }
        self.active_keys = set()
        
        # 实时音频
        if HAS_REALTIME_AUDIO:
            self.synth = RealTimeSynth(sample_rate=44100, buffer_size=1024)
            self.synth.start()
            self.osc_module.synth = self.synth
            print("✅ 实时音频引擎已启动！")
        else:
            self.synth = None
        
        # 预设
        self.current_preset = "Default"
        self.status_message = ""
        self.status_timer = 0
        
        # 主题切换按钮
        self.theme_btn = ModernButton(
            LayoutConfig.SCREEN_WIDTH - 120, 15, 100, 35,
            "THEME", self.cycle_theme, self.theme
        )
        
        # 预设按钮
        self.preset_buttons = []
        presets = ['Lead', 'Bass', 'Pad']
        for i, preset_name in enumerate(presets):
            btn = ModernButton(
                400 + i * 100, 15, 80, 35,
                preset_name, lambda p=preset_name: self.load_preset(p), self.theme
            )
            self.preset_buttons.append(btn)
    
    def cycle_theme(self):
        """切换主题"""
        theme_name = self.theme.cycle_theme()
        self.show_status(f"🎨 主题: {theme_name}")
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                elif event.key in self.key_notes:
                    freq = self.key_notes[event.key]
                    self.osc_module.osc.set_frequency(freq)
                    self.active_keys.add(event.key)
                    
                    if self.synth:
                        self.synth.note_on(chr(event.key))
                
                # 音量
                elif event.key in [pygame.K_EQUAL, pygame.K_PLUS]:
                    if self.synth:
                        self.synth.set_volume(min(1.0, self.synth.volume + 0.1))
                elif event.key == pygame.K_MINUS:
                    if self.synth:
                        self.synth.set_volume(max(0.0, self.synth.volume - 0.1))
            
            elif event.type == pygame.KEYUP:
                if event.key in self.active_keys:
                    self.active_keys.remove(event.key)
                    if self.synth:
                        self.synth.note_off()
            
            # 模块事件
            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                for module in [self.osc_module, self.filter_module, self.env_module, self.lfo_module]:
                    if module.handle_event(event):
                        break
                
                self.theme_btn.handle_event(event)
                for btn in self.preset_buttons:
                    btn.handle_event(event)
    
    def update_audio(self):
        """更新音频"""
        osc = self.osc_module.osc
        audio = osc.generate(duration=0.05)
        filtered = self.filter_module.filter.process(audio)
        self.audio_buffer = filtered
        self.waveform.set_audio(filtered)
    
    def draw(self):
        """绘制界面"""
        # 背景渐变（使用实色）
        bg_color = self.theme.get_color('bg_primary')
        self.screen.fill(bg_color)
        
        # 标题
        title = self.title_font.render("🎹 Modular Synth Studio v0.6.0", True, 
                                       self.theme.get_color('text_primary'))
        self.screen.blit(title, (20, 20))
        
        # 副标题
        subtitle = self.small_font.render("A-S-D-F-G-H-J-K: 演奏 | 鼠标: 调节参数 | +/-: 音量", 
                                         True, self.theme.get_color('text_secondary'))
        self.screen.blit(subtitle, (20, 55))
        
        # 绘制模块
        self.osc_module.draw(self.screen, self.font)
        self.filter_module.draw(self.screen, self.font)
        self.env_module.draw(self.screen, self.font)
        self.lfo_module.draw(self.screen, self.font)
        
        # 绘制波形
        self.waveform.draw(self.screen, self.font)
        
        # 绘制连接线
        self.draw_connections()
        
        # 绘制按钮
        self.theme_btn.draw(self.screen, self.small_font)
        for btn in self.preset_buttons:
            btn.draw(self.screen, self.small_font)
        
        # 状态栏
        status_bg = pygame.Rect(0, LayoutConfig.SCREEN_HEIGHT - 25, LayoutConfig.SCREEN_WIDTH, 25)
        pygame.draw.rect(self.screen, self.theme.get_color('bg_panel'), status_bg)
        
        status = f"FPS: {self.clock.get_fps():.1f} | Keys: {len(self.active_keys)} | Preset: {self.current_preset}"
        status_surf = self.small_font.render(status, True, self.theme.get_color('text_secondary'))
        self.screen.blit(status_surf, (10, LayoutConfig.SCREEN_HEIGHT - 20))
        
        # 状态消息
        if self.status_timer > 0 and self.status_message:
            msg_surf = self.font.render(self.status_message, True, self.theme.get_color('text_accent'))
            self.screen.blit(msg_surf, (LayoutConfig.SCREEN_WIDTH//2 - msg_surf.get_width()//2, 
                                        LayoutConfig.SCREEN_HEIGHT - 55))
            self.status_timer -= 1
        
        pygame.display.flip()
    
    def draw_connections(self):
        """绘制模块连接线"""
        cable_color = self.theme.get_color('cable')
        active_color = self.theme.get_color('cable_active')
        
        # OSC -> FILTER
        start = (self.osc_module.rect.right - 5, self.osc_module.rect.centery)
        end = (self.filter_module.rect.left + 5, self.filter_module.rect.centery)
        pygame.draw.line(self.screen, cable_color, start, end, 4)
        
        # FILTER -> ENV
        start = (self.filter_module.rect.right - 5, self.filter_module.rect.centery + 30)
        end = (self.env_module.rect.left + 5, self.env_module.rect.centery + 30)
        pygame.draw.line(self.screen, cable_color, start, end, 3)
    
    def load_preset(self, preset_name):
        """加载预设"""
        self.current_preset = preset_name
        self.show_status(f"🎵 加载预设: {preset_name}")
    
    def show_status(self, message):
        """显示状态"""
        self.status_message = message
        self.status_timer = 120
    
    def run(self):
        """主循环"""
        print("\n" + "="*60)
        print("🎹 Modular Synth Studio v0.6.0 已启动!")
        print("="*60)
        print("按键: A S D F G H J K")
        print("操作: 鼠标拖动旋钮")
        print("音量: +/-")
        print("主题: 点击右上角 THEME 按钮")
        print("退出: ESC")
        print("="*60 + "\n")
        
        while self.running:
            self.handle_events()
            self.update_audio()
            self.draw()
            self.clock.tick(60)
        
        if self.synth:
            self.synth.stop()
        
        pygame.quit()
        print("\n👋 再见！")


def main():
    """主函数"""
    gui = SynthGUIV2()
    gui.run()


if __name__ == '__main__':
    main()
