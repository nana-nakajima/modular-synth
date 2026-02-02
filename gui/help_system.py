#!/usr/bin/env python3
# 📖 Modular Synth 帮助文档 - v1.0.0
# Nana的虚拟模块合成器 - 帮助系统

import pygame


class HelpSystem:
    """帮助系统"""
    
    def __init__(self, screen_width, screen_height, theme_colors=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 颜色配置
        if theme_colors:
            self.colors = theme_colors
        else:
            self.colors = {
                'bg': (15, 15, 25),
                'panel': (35, 35, 55),
                'border': (70, 70, 100),
                'text_primary': (240, 240, 255),
                'text_secondary': (160, 160, 190),
                'text_accent': (120, 200, 255),
                'accent': (80, 150, 220),
            }
        
        # 字体
        self.title_font = pygame.font.Font(None, 36)
        self.header_font = pygame.font.Font(None, 26)
        self.normal_font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 16)
        
        # 帮助页面内容
        self.pages = {
            'main': self._get_main_content(),
            'keyboard': self._get_keyboard_content(),
            'modules': self._get_modules_content(),
            'presets': self._get_presets_content(),
            'shortcuts': self._get_shortcuts_content(),
        }
        
        self.current_page = 'main'
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # 页面切换按钮
        self.page_buttons = []
        self._create_page_buttons()
    
    def _create_page_buttons(self):
        """创建页面切换按钮"""
        page_names = ['main', 'keyboard', 'modules', 'presets', 'shortcuts']
        page_labels = ['概览', '键盘', '模块', '预设', '快捷键']
        
        button_width = 100
        button_height = 30
        button_y = 60
        start_x = self.screen_width // 2 - (len(page_names) * button_width + (len(page_names) - 1) * 10) // 2
        
        for i, (name, label) in enumerate(zip(page_names, page_labels)):
            rect = pygame.Rect(start_x + i * (button_width + 10), button_y, button_width, button_height)
            self.page_buttons.append({
                'rect': rect,
                'page': name,
                'label': label,
            })
    
    def _get_main_content(self):
        """获取主页面内容"""
        return [
            ("🎹 Modular Synth Studio", "title"),
            ("", "spacer"),
            ("欢迎使用 Nana 的虚拟模块合成器！", "normal"),
            ("", "spacer"),
            ("这是一个功能完整的虚拟模拟合成器，提供:", "normal"),
            ("• 4种波形振荡器 (正弦波、锯齿波、方波、三角波)", "bullet"),
            ("• 多模式滤波器 (低通、高通、带通)", "bullet"),
            ("• ADSR包络发生器", "bullet"),
            ("• LFO低频振荡器", "bullet"),
            ("• 实时音频播放", "bullet"),
            ("• 预设音色库", "bullet"),
            ("• 主题切换 (暗色/复古/赛博朋克)", "bullet"),
            ("", "spacer"),
            ("快速开始:", "header"),
            ("1. 按 A-S-D-F-G-H-J-K 键演奏音符", "normal"),
            ("2. 使用鼠标拖动旋钮调节参数", "normal"),
            ("3. 按 1-4 切换波形类型", "normal"),
            ("4. 按 +/- 调节音量", "normal"),
            ("", "spacer"),
            ("按 H 键打开/关闭帮助", "accent"),
        ]
    
    def _get_keyboard_content(self):
        """获取键盘演奏页面内容"""
        return [
            ("⌨️ 键盘演奏", "title"),
            ("", "spacer"),
            ("合成器键盘映射:", "header"),
            ("", "spacer"),
            ("键位        音符        频率", "header"),
            ("A           C4          261.63 Hz", "mono"),
            ("S           D4          293.66 Hz", "mono"),
            ("D           E4          329.63 Hz", "mono"),
            ("F           F4          349.23 Hz", "mono"),
            ("G           G4          392.00 Hz", "mono"),
            ("H           A4          440.00 Hz", "mono"),
            ("J           B4          493.88 Hz", "mono"),
            ("K           C5          523.25 Hz", "mono"),
            ("", "spacer"),
            ("演奏技巧:", "header"),
            ("• 同时按下多个键可以演奏和弦", "bullet"),
            ("• 按住键的时间越长，音量变化受包络控制", "bullet"),
            ("• 配合LFO可以创造颤音效果", "bullet"),
            ("", "spacer"),
            ("扩展键盘 (数字键区):", "header"),
            ("Num 1-4     选择波形类型", "normal"),
            ("Num + / -   调节音量", "normal"),
        ]
    
    def _get_modules_content(self):
        """获取模块说明页面内容"""
        return [
            ("🔧 模块说明", "title"),
            ("", "spacer"),
            ("OSCILLATOR (振荡器)", "header"),
            ("产生合成器的基本声音波形:", "normal"),
            ("• Freq (频率) - 调节音高 (20-2000 Hz)", "bullet"),
            ("• Wave (波形) - 切换声音音色", "bullet"),
            ("  - Sine: 纯净的正弦波，柔和", "subbullet"),
            ("  - Sawtooth: 锯齿波，刺耳但丰富", "subbullet"),
            ("  - Square: 方波，复古游戏风格", "subbullet"),
            ("  - Triangle: 三角波，介于正弦和方波之间", "subbullet"),
            ("", "spacer"),
            ("FILTER (滤波器)", "header"),
            ("塑造声音的频率特性:", "normal"),
            ("• Cutoff (截止频率) - 决定声音的亮度", "bullet"),
            ("• Resonance (共振) - 强调截止频率附近的频段", "bullet"),
            ("• Type (类型) - 低通/高通/带通", "bullet"),
            ("", "spacer"),
            ("ENVELOPE (包络)", "header"),
            ("控制声音的音量变化过程 (ADSR):", "normal"),
            ("• Attack (起音) - 从无声到最大音量的时间", "bullet"),
            ("• Decay (衰减) - 从最大到持续音量的时间", "bullet"),
            ("• Sustain (持续) - 按住键时的保持音量", "bullet"),
            ("• Release (释音) - 释放键后声音消失的时间", "bullet"),
            ("", "spacer"),
            ("LFO (低频振荡器)", "header"),
            ("产生低于20Hz的低频信号用于调制:", "normal"),
            ("• Freq (频率) - 调制速度 (0.1-20 Hz)", "bullet"),
            ("• Wave (波形) - 调制信号形状", "bullet"),
        ]
    
    def _get_presets_content(self):
        """获取预设说明页面内容"""
        return [
            ("🎵 预设音色", "title"),
            ("", "spacer"),
            ("内置预设:", "header"),
            ("", "spacer"),
            ("Lead (主音音色)", "header"),
            ("明亮的锯齿波主音，适合独奏和旋律", "normal"),
            ("• 特征: 快速起音、适中衰减、高保持", "bullet"),
            ("• 适用: Synth Lead、旋律线", "bullet"),
            ("", "spacer"),
            ("Bass (贝斯音色)", "header"),
            ("厚重的方波贝斯，808风格", "normal"),
            ("• 特征: 极快起音、短促衰减、 punchy", "bullet"),
            ("• 适用: 节奏贝斯、底鼓填充", "bullet"),
            ("", "spacer"),
            ("Pad (氛围音色)", "header"),
            ("柔和的正弦波pad，适合背景和声", "normal"),
            ("• 特征: 慢起音、长释音、梦幻", "bullet"),
            ("• 适用: 背景和声、电影配乐", "bullet"),
            ("", "spacer"),
            ("预设快捷键:", "header"),
            ("5 - 加载 Lead 预设", "normal"),
            ("6 - 加载 Bass 预设", "normal"),
            ("7 - 加载 Pad 预设", "normal"),
        ]
    
    def _get_shortcuts_content(self):
        """获取快捷键页面内容"""
        return [
            ("⚡ 快捷键参考", "title"),
            ("", "spacer"),
            ("演奏控制:", "header"),
            ("A S D F G H J K   演奏音符 (C4-C5)", "mono"),
            ("1 2 3 4           切换波形类型", "mono"),
            ("+/-               调节音量", "mono"),
            ("ESC               退出程序", "mono"),
            ("", "spacer"),
            ("预设操作:", "header"),
            ("5 6 7             加载预设 (Lead/Bass/Pad)", "mono"),
            ("P                 进入预设选择模式", "mono"),
            ("S                 保存当前设置", "mono"),
            ("", "spacer"),
            ("界面操作:", "header"),
            ("H                 显示/隐藏帮助", "mono"),
            ("T                 切换主题", "mono"),
            ("M                 静音/取消静音", "mono"),
            ("", "spacer"),
            ("鼠标操作:", "header"),
            ("拖动旋钮         调节参数值", "mono"),
            ("点击旋钮         复位到默认值", "mono"),
            ("滚轮             快速调节音量", "mono"),
        ]
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键
                # 检查页面切换按钮
                for button in self.page_buttons:
                    if button['rect'].collidepoint(event.pos):
                        self.current_page = button['page']
                        self.scroll_offset = 0
                        return True
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # 滚轮上
                self.scroll_offset = max(0, self.scroll_offset - 30)
            elif event.button == 5:  # 滚轮下
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + 30)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h or event.key == pygame.K_ESCAPE:
                return 'toggle'
            elif event.key == pygame.K_LEFT:
                # 上一页
                pages = list(self.pages.keys())
                idx = pages.index(self.current_page)
                self.current_page = pages[max(0, idx - 1)]
                self.scroll_offset = 0
            elif event.key == pygame.K_RIGHT:
                # 下一页
                pages = list(self.pages.keys())
                idx = pages.index(self.current_page)
                self.current_page = pages[min(len(pages) - 1, idx + 1)]
                self.scroll_offset = 0
        
        return False
    
    def render(self, surface, x=None, y=None, width=None, height=None):
        """渲染帮助面板"""
        if x is None:
            x = 100
        if y is None:
            y = 50
        if width is None:
            width = self.screen_width - 200
        if height is None:
            height = self.screen_height - 100
        
        # 绘制背景
        panel_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, self.colors['bg'], panel_rect)
        pygame.draw.rect(surface, self.colors['border'], panel_rect, 2)
        
        # 绘制标题
        title_text = {
            'main': '📖 使用帮助',
            'keyboard': '⌨️ 键盘演奏',
            'modules': '🔧 模块说明',
            'presets': '🎵 预设音色',
            'shortcuts': '⚡ 快捷键',
        }.get(self.current_page, '帮助')
        
        title = self.title_font.render(title_text, True, self.colors['text_primary'])
        surface.blit(title, (x + 20, y + 20))
        
        # 绘制页面切换按钮
        for button in self.page_buttons:
            color = self.colors['accent'] if button['page'] == self.current_page else self.colors['panel']
            pygame.draw.rect(surface, color, button['rect'])
            pygame.draw.rect(surface, self.colors['border'], button['rect'], 1)
            
            label = self.normal_font.render(button['label'], True, self.colors['text_primary'])
            label_rect = label.get_rect(center=button['rect'].center)
            surface.blit(label, label_rect)
        
        # 绘制内容
        content = self.pages.get(self.current_page, [])
        content_y = y + 80 - self.scroll_offset
        
        for item in content:
            if len(item) == 2:
                text, style = item
            else:
                text, style = item[0], item[1]
            
            if style == 'title':
                continue  # 主标题已在上面绘制
            
            elif style == 'spacer':
                content_y += 20
            
            elif style == 'header':
                surf = self.header_font.render(text, True, self.colors['text_accent'])
                surface.blit(surf, (x + 30, content_y))
                content_y += 35
            
            elif style == 'normal':
                surf = self.normal_font.render(text, True, self.colors['text_primary'])
                surface.blit(surf, (x + 30, content_y))
                content_y += 28
            
            elif style == 'accent':
                surf = self.normal_font.render(text, True, self.colors['text_accent'])
                surface.blit(surf, (x + 30, content_y))
                content_y += 28
            
            elif style == 'bullet':
                surf = self.normal_font.render(f"• {text}", True, self.colors['text_secondary'])
                surface.blit(surf, (x + 30, content_y))
                content_y += 28
            
            elif style == 'subbullet':
                surf = self.small_font.render(f"  - {text}", True, self.colors['text_secondary'])
                surface.blit(surf, (x + 50, content_y))
                content_y += 22
            
            elif style == 'mono':
                surf = self.small_font.render(text, True, (150, 255, 200))
                surface.blit(surf, (x + 30, content_y))
                content_y += 24
        
        # 更新最大滚动距离
        self.max_scroll = max(0, content_y - (y + height - 40))
        
        # 绘制滚动条（如果需要）
        if self.max_scroll > 0:
            scroll_height = height - 120
            thumb_height = max(30, scroll_height * (height - 120) / (self.max_scroll + height - 120))
            thumb_y = y + 80 + (scroll_height - thumb_height) * (self.scroll_offset / self.max_scroll)
            
            # 轨道
            pygame.draw.rect(surface, self.colors['panel'], (x + width - 15, y + 80, 10, scroll_height))
            # 滑块
            pygame.draw.rect(surface, self.colors['accent'], (x + width - 15, thumb_y, 10, int(thumb_height)))
        
        # 底部提示
        hint = self.small_font.render("按 ← → 切换页面 | 滚轮滚动 | 按 H 关闭", True, self.colors['text_secondary'])
        surface.blit(hint, (x + 20, y + height - 25))
        
        return panel_rect


class AboutDialog:
    """关于对话框"""
    
    def __init__(self, screen_width, screen_height, theme_colors=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 颜色配置
        if theme_colors:
            self.colors = theme_colors
        else:
            self.colors = {
                'bg': (20, 20, 35),
                'panel': (40, 40, 65),
                'border': (80, 80, 120),
                'text_primary': (240, 240, 255),
                'text_secondary': (160, 160, 190),
                'accent': (100, 200, 255),
            }
        
        # 字体
        self.title_font = pygame.font.Font(None, 36)
        self.normal_font = pygame.font.Font(None, 22)
        self.small_font = pygame.font.Font(None, 16)
        
        # 窗口尺寸
        self.width = 450
        self.height = 350
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2
        
        # 按钮
        self.close_button = pygame.Rect(self.x + self.width - 90, self.y + self.height - 45, 80, 30)
        
        self.visible = False
    
    def show(self):
        """显示对话框"""
        self.visible = True
    
    def hide(self):
        """隐藏对话框"""
        self.visible = False
    
    def toggle(self):
        """切换显示状态"""
        self.visible = not self.visible
    
    def handle_event(self, event):
        """处理事件"""
        if not self.visible:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.close_button.collidepoint(event.pos):
                    self.visible = False
                    return True
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.visible = False
                return True
        
        return False
    
    def render(self, surface):
        """渲染对话框"""
        if not self.visible:
            return
        
        # 背景遮罩
        mask = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 150))
        surface.blit(mask, (0, 0))
        
        # 对话框背景
        pygame.draw.rect(surface, self.colors['bg'], (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, self.colors['border'], (self.x, self.y, self.width, self.height), 2)
        
        # 标题
        title = self.title_font.render("🎹 Modular Synth Studio", True, self.colors['text_primary'])
        surface.blit(title, (self.x + 20, self.y + 20))
        
        # 版本
        version = self.normal_font.render("v1.0.0 - Steam Edition", True, self.colors['accent'])
        surface.blit(version, (self.x + 20, self.y + 60))
        
        # 分隔线
        pygame.draw.line(surface, self.colors['border'], (self.x + 20, self.y + 95), 
                        (self.x + self.width - 20, self.y + 95), 1)
        
        # 内容
        lines = [
            ("开发者: Nana Nakajima", self.colors['text_secondary']),
            ("", self.colors['text_secondary']),
            ("功能特性:", self.colors['text_primary']),
            ("• 模块化合成器架构", self.colors['text_secondary']),
            ("• 实时音频处理", self.colors['text_secondary']),
            ("• 多种波形和效果", self.colors['text_secondary']),
            ("• 预设音色系统", self.colors['text_secondary']),
            ("• 主题切换", self.colors['text_secondary']),
            ("", self.colors['text_secondary']),
            ("按 H 打开帮助文档", self.colors['accent']),
        ]
        
        y = self.y + 115
        for text, color in lines:
            surf = self.small_font.render(text, True, color)
            surface.blit(surf, (self.x + 30, y))
            y += 22
        
        # 关闭按钮
        pygame.draw.rect(surface, self.colors['panel'], self.close_button)
        pygame.draw.rect(surface, self.colors['border'], self.close_button, 1)
        close_text = self.normal_font.render("关闭", True, self.colors['text_primary'])
        close_rect = close_text.get_rect(center=self.close_button.center)
        surface.blit(close_text, close_rect)


# ============ 演示代码 ============
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("帮助系统演示")
    
    help_system = HelpSystem(1000, 700)
    clock = pygame.time.Clock()
    
    running = True
    show_help = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            result = help_system.handle_event(event)
            if result == 'toggle':
                show_help = not show_help
        
        screen.fill((15, 15, 25))
        
        if show_help:
            help_system.render(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
