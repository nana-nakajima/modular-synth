#!/usr/bin/env python3
# ⏳ Modular Synth 加载动画 - v1.0.0
# Nana的虚拟模块合成器 - 启动加载画面

import pygame
import sys
import time


class LoadingScreen:
    """启动加载画面"""
    
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("🎹 Modular Synth Studio")
        
        # 颜色配置
        self.bg_color = (15, 15, 25)
        self.accent_color = (100, 200, 255)
        self.text_color = (220, 220, 240)
        self.progress_color = (80, 150, 220)
        
        # 字体
        self.title_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 24)
        
        # 动画状态
        self.clock = pygame.time.Clock()
        self.progress = 0
        self.message = "初始化..."
        self.done = False
        self.fade_in = 0
        self.pulse_phase = 0
        
        # 加载任务列表
        self.tasks = []
        self.current_task = 0
        
    def add_task(self, task_name):
        """添加加载任务"""
        self.tasks.append({
            'name': task_name,
            'completed': False,
            'start_time': None
        })
    
    def set_progress(self, progress, message=""):
        """设置进度"""
        self.progress = progress
        if message:
            self.message = message
    
    def next_task(self, message=""):
        """完成当前任务，进入下一个"""
        if self.current_task < len(self.tasks):
            self.tasks[self.current_task]['completed'] = True
            self.current_task += 1
            self.progress = self.current_task / len(self.tasks) if self.tasks else 1.0
            if message:
                self.message = message
            else:
                if self.current_task < len(self.tasks):
                    self.message = f"加载中: {self.tasks[self.current_task]['name']}"
    
    def complete_all(self, message="就绪！"):
        """完成所有任务"""
        self.progress = 1.0
        self.message = message
        self.done = True
    
    def _draw_progress_bar(self, x, y, width, height, progress, color):
        """绘制进度条"""
        # 背景
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (40, 40, 60), bg_rect)
        
        # 进度
        if progress > 0:
            progress_width = int(width * progress)
            progress_rect = pygame.Rect(x, y, progress_width, height)
            pygame.draw.rect(self.screen, color, progress_rect)
        
        # 边框
        pygame.draw.rect(self.screen, (80, 80, 120), bg_rect, 2)
        
        # 发光效果
        if progress > 0:
            glow_rect = pygame.Rect(x, y, int(width * progress), height // 3)
            pygame.draw.rect(self.screen, (150, 200, 255, 100), glow_rect)
    
    def _draw_knob_animation(self, center_x, center_y, time_val):
        """绘制旋钮动画"""
        # 多个旋钮旋转动画
        for i in range(4):
            angle = time_val * 2 + i * (360 // 4)
            angle_rad = pygame.math.radians(angle)
            
            radius = 35
            knob_x = center_x + 60 * pygame.math.cos(angle_rad)
            knob_y = center_y + 60 * pygame.math.sin(angle_rad)
            
            # 旋钮主体
            pygame.draw.circle(self.screen, (60, 60, 90), (int(knob_x), int(knob_y)), 20)
            pygame.draw.circle(self.screen, self.accent_color, (int(knob_x), int(knob_y)), 20, 2)
            
            # 指示器
            indicator_x = knob_x + 12 * pygame.math.cos(angle_rad - 90)
            indicator_y = knob_y + 12 * pygame.math.sin(angle_rad - 90)
            pygame.draw.circle(self.screen, self.accent_color, (int(indicator_x), int(indicator_y)), 4)
    
    def _draw_waveform_animation(self, x, y, width, height, time_val):
        """绘制波形动画"""
        center_y = y + height // 2
        
        # 绘制多条波形
        for wave_idx in range(3):
            offset_y = (wave_idx - 1) * 20
            amplitude = 20 + wave_idx * 10
            color = [
                (80, 200, 255),
                (150, 100, 255),
                (255, 100, 200)
            ][wave_idx]
            
            points = []
            for i in range(width):
                t = i / 50 + time_val * 3 + wave_idx
                y_offset = pygame.math.sin(t) * amplitude
                points.append((x + i, center_y + y_offset + offset_y))
            
            pygame.draw.lines(self.screen, color, False, points, 2)
    
    def render(self):
        """渲染加载画面"""
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # 更新淡入效果
        if self.fade_in < 255:
            self.fade_in += 15
        
        # 更新脉冲相位
        self.pulse_phase += 0.1
        
        # 背景
        self.screen.fill(self.bg_color)
        
        # 标题
        title = self.title_font.render("🎹 Modular Synth Studio", True, self.text_color)
        title_rect = title.get_rect(center=(self.width // 2, 100))
        
        # 标题发光效果
        glow_surf = pygame.Surface((title.get_width() + 20, title.get_height() + 10), pygame.SRCALPHA)
        glow_color = (100, 200, 255, 50 + int(pygame.math.sin(self.pulse_phase) * 20))
        pygame.draw.rect(glow_surf, glow_color, (0, 0, title.get_width() + 20, title.get_height() + 10), 
                        border_radius=10)
        self.screen.blit(glow_surf, (title_rect.x - 10, title_rect.y - 5))
        self.screen.blit(title, title_rect)
        
        # 副标题
        subtitle = self.text_font.render("Nana's Virtual Modular Synthesizer", True, (150, 150, 180))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 150))
        self.screen.blit(subtitle, subtitle_rect)
        
        # 绘制旋钮动画
        self._draw_knob_animation(self.width // 2, 280, self.pulse_phase)
        
        # 绘制波形动画
        self._draw_waveform_animation(self.width // 2 - 150, 360, 300, 60, self.pulse_phase)
        
        # 进度条背景
        bar_x = self.width // 2 - 200
        bar_y = 480
        bar_width = 400
        bar_height = 20
        
        self._draw_progress_bar(bar_x, bar_y, bar_width, bar_height, self.progress, self.progress_color)
        
        # 进度百分比
        percent_text = f"{int(self.progress * 100)}%"
        percent_surf = self.text_font.render(percent_text, True, self.text_color)
        percent_rect = percent_surf.get_rect(center=(self.width // 2, bar_y - 25))
        self.screen.blit(percent_surf, percent_rect)
        
        # 状态消息
        message_surf = self.text_font.render(self.message, True, self.accent_color)
        message_rect = message_surf.get_rect(center=(self.width // 2, bar_y + 45))
        self.screen.blit(message_surf, message_rect)
        
        # 任务列表
        if self.tasks:
            task_y = 560
            task_font = pygame.font.Font(None, 18)
            
            for i, task in enumerate(self.tasks):
                if i >= 5:  # 只显示前5个
                    break
                    
                task_text = f"{'✓' if task['completed'] else '○'} {task['name']}"
                task_color = (100, 255, 100) if task['completed'] else (150, 150, 180)
                task_surf = task_font.render(task_text, True, task_color)
                self.screen.blit(task_surf, (self.width // 2 - 150, task_y + i * 22))
        
        # 版本信息
        version_text = "v1.0.0 - Steam Edition"
        version_surf = self.text_font.render(version_text, True, (100, 100, 130))
        version_rect = version_surf.get_rect(center=(self.width // 2, self.height - 40))
        self.screen.blit(version_surf, version_rect)
        
        # 更新显示
        pygame.display.flip()
        self.clock.tick(60)
        
        return not self.done
    
    def run(self):
        """运行加载画面"""
        # 模拟加载过程（实际使用中会被外部控制）
        while self.render():
            if self.done:
                pygame.time.wait(500)  # 完成后再显示一会儿
                break
        return self.done


class SplashScreen:
    """启动闪屏（更简洁的版本）"""
    
    def __init__(self, duration=2000):
        pygame.init()
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        
        # 全屏显示
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        
        # 颜色
        self.bg_color = (15, 15, 25)
        self.accent_color = (100, 200, 255)
        self.text_color = (220, 220, 240)
        
        # 字体
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_font = pygame.font.Font(None, 28)
        
        self.pulse_phase = 0
        
    def render(self):
        """渲染闪屏"""
        # 计算进度
        elapsed = pygame.time.get_ticks() - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        
        # 处理事件（允许提前退出）
        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                return False  # 用户交互，提前退出
        
        # 背景
        self.screen.fill(self.bg_color)
        
        # 脉冲效果
        self.pulse_phase += 0.05
        pulse = 0.8 + pygame.math.sin(self.pulse_phase) * 0.2
        
        # 标题
        title = self.title_font.render("🎹 Modular Synth Studio", True, self.text_color)
        title_alpha = int(255 * min(progress * 2, 1.0))
        
        # 创建带透明度标题
        title_surf = pygame.Surface(title.get_size(), pygame.SRCALPHA)
        title_surf.blit(title, (0, 0))
        title_surf.set_alpha(title_alpha)
        
        title_rect = title_surf.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(title_surf, title_rect)
        
        # 副标题
        subtitle = self.subtitle_font.render("Nana's Virtual Modular Synthesizer", True, self.accent_color)
        subtitle_alpha = int(255 * min((progress - 0.3) * 2, 1.0))
        
        subtitle_surf = pygame.Surface(subtitle.get_size(), pygame.SRCALPHA)
        subtitle_surf.blit(subtitle, (0, 0))
        subtitle_surf.set_alpha(subtitle_alpha)
        
        subtitle_rect = subtitle_surf.get_rect(center=(self.width // 2, self.height // 2 + 20))
        self.screen.blit(subtitle_surf, subtitle_rect)
        
        # 简单的脉冲圆圈
        if progress > 0.5:
            circle_radius = 30 + pygame.math.sin(self.pulse_phase * 2) * 5
            circle_alpha = int(200 * (1 - (progress - 0.5) * 2))
            
            pygame.draw.circle(self.screen, (*self.accent_color, circle_alpha), 
                             (self.width // 2, self.height // 2 + 100), int(circle_radius), 3)
        
        pygame.display.flip()
        self.clock.tick(60)
        
        return progress < 1.0
    
    def run(self):
        """运行闪屏"""
        while self.render():
            pass
        return True


# ============ 演示代码 ============
if __name__ == '__main__':
    # 创建加载画面
    loading = LoadingScreen()
    
    # 添加加载任务
    loading.add_task("加载音频引擎...")
    loading.add_task("初始化振荡器...")
    loading.add_task("创建滤波器...")
    loading.add_task("加载效果器...")
    loading.add_task("构建界面...")
    loading.add_task("加载预设音色...")
    
    # 模拟加载过程
    for i in range(len(loading.tasks) + 1):
        loading.render()
        pygame.time.wait(500)
        loading.next_task()
    
    print("✅ 加载动画演示完成！")
    pygame.quit()
