#!/usr/bin/env python3
# 🎹 Modular Synth GUI - 图形界面 v1.0.0
# Nana的虚拟模块合成器 - 图形用户界面 (最终美化版)

import pygame
import json
import os
import sys

# 添加gui目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audio.core_modules import Oscillator, Filter, Envelope, LFO, MultiOscillator
from theme_system import ThemeManager, LayoutConfig
from loading_screen import LoadingScreen
from help_system import HelpSystem, AboutDialog

# 尝试导入实时音频模块
try:
    from audio.real_time_player import RealTimeSynth
    HAS_REALTIME_AUDIO = True
except ImportError:
    HAS_REALTIME_AUDIO = False
    print("⚠️ 实时音频模块不可用 (sounddevice未安装)")

# 使用主题系统
THEME = ThemeManager('DARK')
LAYOUT = LayoutConfig()

# 从主题获取颜色
COLOR_BG = THEME.get_color('bg_primary')
COLOR_PANEL = THEME.get_color('bg_panel')
COLOR_MODULE = THEME.get_color('bg_module')
COLOR_MODULE_BORDER = THEME.get_color('border')
COLOR_TEXT = THEME.get_color('text_primary')
COLOR_KNOB = THEME.get_color('knob')
COLOR_LED = THEME.get_color('led_on')
COLOR_WAVEFORM = THEME.get_color('waveform')

# 尺寸配置
SCREEN_WIDTH = LAYOUT.SCREEN_WIDTH
SCREEN_HEIGHT = LAYOUT.SCREEN_HEIGHT
MODULE_WIDTH = LAYOUT.MODULE_WIDTH
MODULE_HEIGHT = LAYOUT.MODULE_HEIGHT

# ============ 旋钮控件 ============
class Knob:
    """旋钮控件"""
    
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
    
    def draw(self, surface, font):
        # 绘制标签
        label_surf = font.render(self.label, True, COLOR_TEXT)
        surface.blit(label_surf, (self.rect.x + 25 - label_surf.get_width()//2, self.rect.y - 20))
        
        # 绘制旋钮背景
        pygame.draw.circle(surface, COLOR_MODULE, self.rect.center, 25)
        pygame.draw.circle(surface, COLOR_MODULE_BORDER, self.rect.center, 25, 2)
        
        # 绘制旋钮位置
        angle = (self.value - self.min_val) / (self.max_val - self.min_val) * 270 - 135
        angle_rad = np.radians(angle)
        knob_x = self.rect.centerx + 20 * np.cos(angle_rad)
        knob_y = self.rect.centery + 20 * np.sin(angle_rad)
        pygame.draw.line(surface, COLOR_KNOB, self.rect.center, (knob_x, knob_y), 3)
        
        # 绘制值
        value_str = f"{self.value:.2f}"
        value_surf = font.render(value_str, True, COLOR_TEXT)
        surface.blit(value_surf, (self.rect.x + 25 - value_surf.get_width()//2, self.rect.y + 30))
    
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
                        self.callback(self.value)
                return True
        
        return False


# ============ 模块基类 ============
class SynthModule:
    """合成器模块基类"""
    
    def __init__(self, x, y, width, height, title):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.knobs = []
    
    def draw(self, surface, font):
        # 绘制模块背景
        pygame.draw.rect(surface, COLOR_MODULE, self.rect)
        pygame.draw.rect(surface, COLOR_MODULE_BORDER, self.rect, 2)
        
        # 绘制标题
        title_surf = font.render(self.title, True, COLOR_TEXT)
        surface.blit(title_surf, (self.rect.x + 10, self.rect.y + 10))
        
        # 绘制分割线
        pygame.draw.line(surface, COLOR_MODULE_BORDER, 
                        (self.rect.x, self.rect.y + 35), 
                        (self.rect.right, self.rect.y + 35), 2)
        
        # 绘制所有旋钮
        for knob in self.knobs:
            knob.draw(surface, font)
    
    def handle_event(self, event):
        for knob in self.knobs:
            if knob.handle_event(event):
                return True
        return False


# ============ 振荡器模块 ============
class OscillatorModule(SynthModule):
    """振荡器模块"""
    
    def __init__(self, x, y):
        super().__init__(x, y, MODULE_WIDTH, MODULE_HEIGHT, "OSCILLATOR")
        
        self.osc = Oscillator(frequency=440, wave_type='sine')
        
        # 频率旋钮
        freq_knob = Knob(x + 65, y + 60, "Freq", 20, 2000, 440, 
                        lambda v: self.osc.set_frequency(v))
        self.knobs.append(freq_knob)
        
        # 波形选择（简化为两个位置）
        self.wave_index = 0
        self.wave_types = ['sine', 'sawtooth']
    
    def draw(self, surface, font):
        super().draw(surface, font)
        
        # 绘制波形预览
        wave_preview = self.osc.generate(duration=0.05)
        wave_preview = wave_preview * 20 + self.rect.centery + 80
        
        # 绘制波形线
        points = []
        for i, y in enumerate(wave_preview):
            x = self.rect.x + 20 + i * (MODULE_WIDTH - 40) // len(wave_preview)
            points.append((x, y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, COLOR_WAVEFORM, False, points, 2)
        
        # 绘制波形类型标签
        wave_label = font.render(f"Wave: {self.osc.wave_type}", True, COLOR_TEXT)
        surface.blit(wave_label, (self.rect.x + 10, self.rect.y + 300))


# ============ 滤波器模块 ============
class FilterModule(SynthModule):
    """滤波器模块"""
    
    def __init__(self, x, y):
        super().__init__(x, y, MODULE_WIDTH, MODULE_HEIGHT, "FILTER")
        
        self.filter = Filter(cutoff=1000, filter_type='lowpass')
        
        # 截止频率旋钮
        cutoff_knob = Knob(x + 65, y + 60, "Cutoff", 100, 5000, 1000,
                          lambda v: self.filter.set_cutoff(v))
        self.knobs.append(cutoff_knob)
    
    def draw(self, surface, font):
        super().draw(surface, font)
        
        # 绘制滤波器类型标签
        type_label = font.render(f"Type: {self.filter.filter_type}", True, COLOR_TEXT)
        surface.blit(type_label, (self.rect.x + 10, self.rect.y + 300))
        
        # 绘制响应曲线（简化）
        center_y = self.rect.centery + 120
        pygame.draw.line(surface, COLOR_WAVEFORM, 
                        (self.rect.x + 20, center_y + 50),
                        (self.rect.right - 20, center_y - 50), 2)


# ============ 包络模块 ============
class EnvelopeModule(SynthModule):
    """ADSR包络模块"""
    
    def __init__(self, x, y):
        super().__init__(x, y, MODULE_WIDTH, MODULE_HEIGHT, "ENVELOPE")
        
        self.env = Envelope(attack=0.1, decay=0.2, sustain=0.7, release=0.3)
        
        # Attack
        attack_knob = Knob(x + 20, y + 60, "A", 0.001, 1.0, 0.1,
                          lambda v: setattr(self.env, 'attack', v))
        self.knobs.append(attack_knob)
        
        # Decay
        decay_knob = Knob(x + 65, y + 60, "D", 0.01, 1.0, 0.2,
                         lambda v: setattr(self.env, 'decay', v))
        self.knobs.append(decay_knob)
        
        # Sustain
        sustain_knob = Knob(x + 110, y + 60, "S", 0.0, 1.0, 0.7,
                           lambda v: setattr(self.env, 'sustain', v))
        self.knobs.append(sustain_knob)
        
        # Release
        release_knob = Knob(x + 65, y + 150, "R", 0.01, 2.0, 0.3,
                           lambda v: setattr(self.env, 'release', v))
        self.knobs.append(release_knob)
    
    def draw(self, surface, font):
        super().draw(surface, font)
        
        # 绘制ADSR曲线（简化）
        center_y = self.rect.centery + 100
        
        # 绘制包络形状
        points = [
            (self.rect.x + 30, center_y + 80),
            (self.rect.x + 60, center_y - 40),   # Attack peak
            (self.rect.x + 90, center_y),        # Decay to sustain
            (self.rect.x + 130, center_y),       # Sustain
            (self.rect.x + 160, center_y + 80),  # Release
        ]
        
        pygame.draw.lines(surface, COLOR_WAVEFORM, False, points, 2)


# ============ LFO模块 ============
class LFOModule(SynthModule):
    """LFO模块"""
    
    def __init__(self, x, y):
        super().__init__(x, y, MODULE_WIDTH, 250, "LFO")
        
        self.lfo = LFO(frequency=2, wave_type='sine')
        
        # 频率旋钮
        freq_knob = Knob(x + 20, y + 60, "Freq", 0.1, 20, 2,
                        lambda v: self.lfo.set_frequency(v))
        self.knobs.append(freq_knob)
    
    def draw(self, surface, font):
        super().draw(surface, font)
        
        # 绘制LFO波形
        wave = self.lfo.generate(duration=0.5)
        wave = wave * 30 + self.rect.centery + 50
        
        points = []
        for i, y in enumerate(wave):
            x = self.rect.x + 20 + i * (MODULE_WIDTH - 40) // len(wave)
            if x <= self.rect.right - 20:
                points.append((x, y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, COLOR_WAVEFORM, False, points, 2)


# ============ 波形显示器 ============
class WaveformDisplay:
    """波形显示器"""
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.audio_data = None
    
    def set_audio(self, audio):
        """设置音频数据"""
        self.audio_data = audio
    
    def draw(self, surface, font):
        # 绘制背景
        pygame.draw.rect(surface, (20, 20, 30), self.rect)
        pygame.draw.rect(surface, COLOR_MODULE_BORDER, self.rect, 2)
        
        # 标题
        title = font.render("OUTPUT WAVEFORM", True, COLOR_TEXT)
        surface.blit(title, (self.rect.x + 10, self.rect.y + 10))
        
        # 绘制中心线
        center_y = self.rect.centery
        pygame.draw.line(surface, (50, 50, 60), 
                        (self.rect.x, center_y),
                        (self.rect.right, center_y), 1)
        
        # 绘制波形
        if self.audio_data is not None:
            # 缩放到显示区域
            display_data = self.audio_data[:self.rect.width - 40]
            display_data = display_data * (self.rect.height - 60) / 2
            
            points = []
            for i, sample in enumerate(display_data):
                x = self.rect.x + 20 + i
                y = center_y - sample
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(surface, COLOR_WAVEFORM, False, points, 2)


# ============ 主界面 ============
class SynthGUI:
    """合成器主界面 v1.0.0 - 最终美化版"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎹 Modular Synth Studio - Nana's Project")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # ===== 加载画面 =====
        self.show_loading = True
        self.loading_screen = LoadingScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # 设置加载任务
        self.loading_screen.add_task("加载音频引擎...")
        self.loading_screen.add_task("初始化振荡器...")
        self.loading_screen.add_task("创建滤波器...")
        self.loading_screen.add_task("加载效果器...")
        self.loading_screen.add_task("构建界面...")
        self.loading_screen.add_task("加载预设音色...")
        
        # ===== 帮助系统 =====
        self.show_help = False
        self.help_system = HelpSystem(SCREEN_WIDTH, SCREEN_HEIGHT, THEME.colors)
        
        # ===== 关于对话框 =====
        self.about_dialog = AboutDialog(SCREEN_WIDTH, SCREEN_HEIGHT, THEME.colors)
        
        # 创建模块
        self.osc_module = OscillatorModule(50, 100)
        self.filter_module = FilterModule(260, 100)
        self.env_module = EnvelopeModule(470, 100)
        self.lfo_module = LFOModule(680, 100)
        
        # 创建波形显示
        self.waveform = WaveformDisplay(50, 550, 1100, 150)
        
        # 状态变量
        self.running = True
        self.audio_buffer = None
        self.loading_complete = False
        
        # 键盘音阶（简单版）
        self.key_notes = {
            pygame.K_a: 261.63,  # C4
            pygame.K_s: 293.66,  # D4
            pygame.K_d: 329.63,  # E4
            pygame.K_f: 349.23,  # F4
            pygame.K_g: 392.00,  # G4
            pygame.K_h: 440.00,  # A4
            pygame.K_j: 493.88,  # B4
            pygame.K_k: 523.25,  # C5
        }
        
        self.active_keys = set()

        # 实时音频播放器
        if HAS_REALTIME_AUDIO:
            self.synth = RealTimeSynth(sample_rate=44100, buffer_size=1024)
            self.synth.start()
            self.loading_screen.next_task("实时音频引擎已启动")
        else:
            self.synth = None
            self.loading_screen.next_task("使用模拟音频模式")

        # 预设音色库
        self.presets_dir = os.path.join(os.path.dirname(__file__), 'presets')
        os.makedirs(self.presets_dir, exist_ok=True)
        self.load_presets_list()

        # 当前预设名称
        self.current_preset = "Default"

        # 保存/加载状态提示
        self.status_message = ""
        self.status_timer = 0
        
        # 主题系统
        self.theme = THEME
        
        # 完成加载
        self.loading_screen.complete_all("就绪！")
        self.loading_complete = True
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # 帮助系统事件
            if self.show_help:
                result = self.help_system.handle_event(event)
                if result == 'toggle':
                    self.show_help = False
                continue
            
            # 关于对话框事件
            if self.about_dialog.visible:
                if self.about_dialog.handle_event(event):
                    continue
            
            # 键盘按下
            if event.type == pygame.KEYDOWN:
                # 帮助
                if event.key == pygame.K_h:
                    self.show_help = not self.show_help
                    continue
                
                # 关于
                if event.key == pygame.K_F1:
                    self.about_dialog.toggle()
                    continue
                
                # 主题切换
                if event.key == pygame.K_t:
                    new_theme = self.theme.cycle_theme()
                    self.show_status(f"切换到 {new_theme} 主题")
                    continue
                
                if event.key in self.key_notes:
                    freq = self.key_notes[event.key]
                    self.osc_module.osc.set_frequency(freq)
                    self.active_keys.add(event.key)

                    # 实时音频播放
                    if self.synth:
                        self.synth.note_on(chr(event.key))
                        self.synth.set_wave_type(self.osc_module.osc.wave_type)

                # 音量控制
                elif event.key == pygame.K_EQUAL or event.key == pygame.K_PLUS:
                    if self.synth:
                        self.synth.set_volume(self.synth.volume + 0.1)
                elif event.key == pygame.K_MINUS:
                    if self.synth:
                        self.synth.set_volume(self.synth.volume - 0.1)

                # 波形切换
                elif event.key == pygame.K_1:
                    self.osc_module.osc.set_wave_type('sine')
                    if self.synth:
                        self.synth.set_wave_type('sine')
                elif event.key == pygame.K_2:
                    self.osc_module.osc.set_wave_type('sawtooth')
                    if self.synth:
                        self.synth.set_wave_type('sawtooth')
                elif event.key == pygame.K_3:
                    self.osc_module.osc.set_wave_type('square')
                    if self.synth:
                        self.synth.set_wave_type('square')
                elif event.key == pygame.K_4:
                    self.osc_module.osc.set_wave_type('triangle')
                    if self.synth:
                        self.synth.set_wave_type('triangle')

                # 预设快捷键
                elif event.key == pygame.K_5:
                    self.load_preset('Lead')
                elif event.key == pygame.K_6:
                    self.load_preset('Bass')
                elif event.key == pygame.K_7:
                    self.load_preset('Pad')

                # ESC - 退出
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
            
            # 键盘释放
            elif event.type == pygame.KEYUP:
                if event.key in self.active_keys:
                    self.active_keys.remove(event.key)
                    # 停止实时音频
                    if self.synth:
                        self.synth.note_off()
            
            # 模块事件处理
            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                for module in [self.osc_module, self.filter_module, self.env_module, self.lfo_module]:
                    if module.handle_event(event):
                        break
    
    def update_audio(self):
        """更新音频"""
        # 生成一些测试音频
        osc = self.osc_module.osc
        audio = osc.generate(duration=0.05)
        
        # 应用滤波器
        filtered = self.filter_module.filter.process(audio)
        
        self.audio_buffer = filtered
        self.waveform.set_audio(filtered)
    
    def draw(self):
        """绘制界面"""
        # 背景
        self.screen.fill(COLOR_BG)
        
        # 标题栏背景
        pygame.draw.rect(self.screen, COLOR_PANEL, (0, 0, SCREEN_WIDTH, 50))
        
        # 标题
        title = self.font.render("🎹 Modular Synth Studio", True, COLOR_TEXT)
        self.screen.blit(title, (20, 15))
        
        # 副标题
        subtitle = self.small_font.render("Nana's Project | 按 H 查看帮助 | T 切换主题", True, (150, 150, 180))
        self.screen.blit(subtitle, (SCREEN_WIDTH - 350, 18))
        
        # 绘制模块
        self.osc_module.draw(self.screen, self.font)
        self.filter_module.draw(self.screen, self.font)
        self.env_module.draw(self.screen, self.font)
        self.lfo_module.draw(self.screen, self.font)
        
        # 绘制波形显示
        self.waveform.draw(self.screen, self.font)
        
        # 绘制连接线（简化版）
        self.draw_connections()
        
        # 绘制状态栏
        self.draw_status_bar()
        
        # 绘制帮助系统
        if self.show_help:
            self.help_system.render(self.screen)
        
        # 绘制关于对话框
        if self.about_dialog.visible:
            self.about_dialog.render(self.screen)
        
        pygame.display.flip()
    
    def draw_status_bar(self):
        """绘制状态栏"""
        # 状态栏背景
        status_y = SCREEN_HEIGHT - 30
        pygame.draw.rect(self.screen, COLOR_PANEL, (0, status_y, SCREEN_WIDTH, 30))
        
        # FPS
        fps = self.clock.get_fps()
        fps_text = f"FPS: {fps:.1f}"
        fps_surf = self.small_font.render(fps_text, True, COLOR_TEXT)
        self.screen.blit(fps_surf, (10, status_y + 8))
        
        # 活动键
        keys_text = f"Keys: {','.join(chr(k) if k < 256 else '' for k in self.active_keys)}" if self.active_keys else "Keys: -"
        keys_surf = self.small_font.render(keys_text, True, COLOR_TEXT)
        self.screen.blit(keys_surf, (120, status_y + 8))
        
        # 主题
        theme_text = f"Theme: {self.theme.current_theme}"
        theme_surf = self.small_font.render(theme_text, True, THEME.get_color('text_accent'))
        self.screen.blit(theme_surf, (280, status_y + 8))
        
        # 预设
        preset_text = f"Preset: {self.current_preset}"
        preset_surf = self.small_font.render(preset_text, True, (150, 200, 255))
        self.screen.blit(preset_surf, (420, status_y + 8))
        
        # 状态消息
        if self.status_timer > 0 and self.status_message:
            msg_surf = self.small_font.render(self.status_message, True, COLOR_LED)
            self.screen.blit(msg_surf, (SCREEN_WIDTH // 2 - msg_surf.get_width() // 2, status_y + 8))
            self.status_timer -= 1
        
        # 音量指示
        if self.synth:
            vol = int(self.synth.volume * 10)
            vol_text = f"Vol: {'█' * vol}{'░' * (10 - vol)}"
            vol_surf = self.small_font.render(vol_text, True, (100, 255, 100))
            self.screen.blit(vol_surf, (SCREEN_WIDTH - 150, status_y + 8))
    
    def update_audio(self):
        """更新音频"""
        # 生成一些测试音频
        osc = self.osc_module.osc
        audio = osc.generate(duration=0.05)
        
        # 应用滤波器
        filtered = self.filter_module.filter.process(audio)
        
        self.audio_buffer = filtered
        self.waveform.set_audio(filtered)
    
    def draw(self):
        """绘制界面"""
        # 背景
        self.screen.fill(COLOR_BG)
        
        # 标题
        title = self.font.render("🎹 Modular Synth Studio - Nana's Project", True, COLOR_TEXT)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        
        # 副标题
        subtitle = self.small_font.render("按 A-S-D-F-G-H-J-K 键播放音符 | 用鼠标拖动旋钮调节参数", True, (150, 150, 180))
        self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 60))
        
        # 绘制模块
        self.osc_module.draw(self.screen, self.font)
        self.filter_module.draw(self.screen, self.font)
        self.env_module.draw(self.screen, self.font)
        self.lfo_module.draw(self.screen, self.font)
        
        # 绘制波形显示
        self.waveform.draw(self.screen, self.font)
        
        # 绘制连接线（简化版）
        self.draw_connections()
        
        # 绘制状态
        status = f"FPS: {self.clock.get_fps():.1f} | Active Keys: {len(self.active_keys)}"
        status_surf = self.small_font.render(status, True, COLOR_TEXT)
        self.screen.blit(status_surf, (10, SCREEN_HEIGHT - 25))

        # 绘制预设名称
        preset_text = f"Preset: {self.current_preset}"
        preset_surf = self.small_font.render(preset_text, True, (150, 200, 255))
        self.screen.blit(preset_surf, (200, SCREEN_HEIGHT - 25))

        # 绘制状态消息
        if self.status_timer > 0 and self.status_message:
            msg_surf = self.font.render(self.status_message, True, (100, 255, 100))
            self.screen.blit(msg_surf, (SCREEN_WIDTH//2 - msg_surf.get_width()//2, SCREEN_HEIGHT - 60))
            self.status_timer -= 1
        
        pygame.display.flip()
    
    def draw_connections(self):
        """绘制模块连接线（简化版）"""
        # OSC -> FILTER
        start = (self.osc_module.rect.right, self.osc_module.rect.centery)
        end = (self.filter_module.rect.left, self.filter_module.rect.centery)
        pygame.draw.line(self.screen, (100, 100, 150), start, end, 3)

        # FILTER -> ENV (概念上的)
        start = (self.filter_module.rect.right, self.filter_module.rect.centery + 50)
        end = (self.env_module.rect.left, self.env_module.rect.centery + 50)
        pygame.draw.line(self.screen, (100, 100, 150), start, end, 3)

    # ============ 预设管理 ============

    def load_presets_list(self):
        """加载预设列表"""
        self.presets = {}
        preset_files = [f for f in os.listdir(self.presets_dir) if f.endswith('.json')]
        for pf in preset_files:
            preset_name = pf[:-5]  # 移除.json
            self.presets[preset_name] = os.path.join(self.presets_dir, pf)

        # 默认预设
        default_presets = {
            'Lead': self.create_lead_preset(),
            'Bass': self.create_bass_preset(),
            'Pad': self.create_pad_preset(),
        }
        for name, data in default_presets.items():
            self.presets[name] = data

    def create_lead_preset(self):
        """创建Lead音色预设"""
        return {
            'osc_frequency': 440.0,
            'osc_wave_type': 'sawtooth',
            'filter_cutoff': 3000,
            'filter_resonance': 5,
            'env_attack': 0.01,
            'env_decay': 0.3,
            'env_sustain': 0.8,
            'env_release': 0.5,
            'lfo_frequency': 0,
            'lfo_wave_type': 'sine',
        }

    def create_bass_preset(self):
        """创建Bass音色预设"""
        return {
            'osc_frequency': 110.0,
            'osc_wave_type': 'square',
            'filter_cutoff': 800,
            'filter_resonance': 8,
            'env_attack': 0.005,
            'env_decay': 0.2,
            'env_sustain': 0.6,
            'env_release': 0.3,
            'lfo_frequency': 0,
            'lfo_wave_type': 'sine',
        }

    def create_pad_preset(self):
        """创建Pad音色预设"""
        return {
            'osc_frequency': 220.0,
            'osc_wave_type': 'sine',
            'filter_cutoff': 2000,
            'filter_resonance': 2,
            'env_attack': 0.5,
            'env_decay': 0.5,
            'env_sustain': 0.9,
            'env_release': 1.5,
            'lfo_frequency': 0.5,
            'lfo_wave_type': 'sine',
        }

    def save_preset(self, preset_name):
        """保存当前设置到预设"""
        preset_data = {
            'osc_frequency': self.osc_module.osc.frequency,
            'osc_wave_type': self.osc_module.osc.wave_type,
            'filter_cutoff': self.filter_module.filter.cutoff,
            'filter_resonance': getattr(self.filter_module.filter, 'resonance', 0),
            'env_attack': self.env_module.env.attack,
            'env_decay': self.env_module.env.decay,
            'env_sustain': self.env_module.env.sustain,
            'env_release': self.env_module.env.release,
            'lfo_frequency': self.lfo_module.lfo.frequency,
            'lfo_wave_type': self.lfo_module.lfo.wave_type,
        }

        if preset_name in self.presets and isinstance(self.presets[preset_name], dict):
            # 更新内存中的预设
            self.presets[preset_name] = preset_data
        else:
            # 保存到文件
            filepath = os.path.join(self.presets_dir, f'{preset_name}.json')
            with open(filepath, 'w') as f:
                json.dump(preset_data, f, indent=2)
            self.presets[preset_name] = filepath

        self.current_preset = preset_name
        self.show_status(f"💾 已保存预设: {preset_name}")

    def load_preset(self, preset_name):
        """加载预设"""
        if preset_name not in self.presets:
            self.show_status(f"❌ 预设不存在: {preset_name}")
            return

        preset_data = self.presets[preset_name]

        if isinstance(preset_data, dict):
            data = preset_data
        else:
            with open(preset_data, 'r') as f:
                data = json.load(f)

        # 应用设置
        self.osc_module.osc.set_frequency(data.get('osc_frequency', 440.0))
        self.osc_module.osc.set_wave_type(data.get('osc_wave_type', 'sine'))
        self.filter_module.filter.set_cutoff(data.get('filter_cutoff', 2000))
        if 'filter_resonance' in data and hasattr(self.filter_module.filter, 'set_resonance'):
            self.filter_module.filter.set_resonance(data.get('filter_resonance', 0))
        self.env_module.env.attack = data.get('env_attack', 0.1)
        self.env_module.env.decay = data.get('env_decay', 0.2)
        self.env_module.env.sustain = data.get('env_sustain', 0.7)
        self.env_module.env.release = data.get('env_release', 0.3)
        self.lfo_module.lfo.set_frequency(data.get('lfo_frequency', 2.0))
        self.lfo_module.lfo.set_wave_type(data.get('lfo_wave_type', 'sine'))

        self.current_preset = preset_name
        self.show_status(f"🎵 已加载预设: {preset_name}")

    def show_status(self, message):
        """显示状态消息"""
        self.status_message = message
        self.status_timer = 120  # 显示2秒 (60fps * 2)
    
    def run(self):
        """主循环"""
        print("\n" + "="*60)
        print("🎹 Modular Synth Studio v1.0.0 已启动!")
        print("="*60)
        print("🎮 操作指南:")
        print("  按键: A S D F G H J K")
        print("  操作: 鼠标拖动旋钮调节参数")
        print("  波形: 1-4 (Sine/Saw/Square/Triangle)")
        print("  预设: 5-7 (Lead/Bass/Pad)")
        print("  音量: +/-")
        print("  帮助: H 键")
        print("  主题: T 键")
        print("  退出: ESC")
        print("="*60 + "\n")
        
        # 显示加载画面
        print("📦 显示加载画面...")
        while True:
            # 处理加载画面事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            # 更新加载画面
            if not self.loading_screen.render():
                break
        
        # 主循环
        while self.running:
            self.handle_events()
            self.update_audio()
            self.draw()
            self.clock.tick(60)

        # 停止实时音频
        if self.synth:
            self.synth.stop()
            print("✅ 音频引擎已停止")

        pygame.quit()
        print("\n👋 再见！下次再见～")


def main():
    """主函数"""
    gui = SynthGUI()
    gui.run()


if __name__ == '__main__':
    main()
