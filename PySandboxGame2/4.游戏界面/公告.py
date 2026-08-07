import pygame
import sys
import os
from pygame.locals import *
# 导入图片加载器
from 图片加载 import 图片管理器

# 初始化pygame
pygame.init()

class AnnouncementSystem:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        # 使用更清晰的字体
        self.font = pygame.font.SysFont("Microsoft YaHei", 28, True)  # 加粗标题
        self.small_font = pygame.font.SysFont("Microsoft YaHei", 20)
        self.is_open = False
        
        # 深色主题配色方案
        self.large_bg_color = (39, 40, 40)    # 深灰色外底
        self.small_bg_color = (26, 27, 29)    # 更深灰色内底
        self.border_color = (70, 70, 70)      # 中灰色边框
        self.title_color = (220, 220, 220)    # 浅色标题
        self.text_color = (180, 180, 180)     # 中灰色文本
        self.close_text_color = (140, 140, 140) # 浅灰色关闭提示
        self.shadow_color = (0, 0, 0, 80)     # 更明显的半透明黑色阴影
        self.corner_radius = 10                # 圆角半径
        
        # 使用图片加载器获取背景图片
        self.background_image = None
        
        # 公告内容（重置为更合理的中文内容）
        self.announcements = [
            "暂无新公告",
            "",
            "",
            ""
        ]
    
    def toggle_announcement(self):
        """切换公告页面显示状态"""
        self.is_open = not self.is_open
    
    def draw_gradient_background(self):
        """绘制渐变背景"""
        # 从深蓝到浅蓝的垂直渐变
        start_color = (100, 100, 255)
        end_color = (150, 150, 255)
        
        for y in range(self.height):
            # 计算当前行的颜色插值
            ratio = y / self.height
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            # 绘制一行像素
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))
    
    def draw(self):
        """绘制公告页面"""
        if not self.is_open:
            return
        
        # 每次绘制前更新屏幕尺寸，确保窗口调整大小时公告界面始终居中
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        # 绘制背景：尝试使用图片加载器获取背景图1，失败则使用渐变
        背景图片 = 图片管理器.获取图片("背景图1")
        if 背景图片 is not None:
            # 计算缩放比例，保持图片的原始宽高比
            图片宽度 = 背景图片.get_width()
            图片高度 = 背景图片.get_height()
            
            # 计算缩放后的尺寸，保持原始宽高比
            缩放比例 = max(self.width / 图片宽度, self.height / 图片高度)
            新宽度 = int(图片宽度 * 缩放比例)
            新高度 = int(图片高度 * 缩放比例)
            
            # 缩放图片
            缩放背景图 = pygame.transform.scale(背景图片, (新宽度, 新高度))
            
            # 计算居中位置
            x = (self.width - 新宽度) // 2
            y = (self.height - 新高度) // 2
            
            # 绘制背景图
            self.screen.blit(缩放背景图, (x, y))
        else:
            # 使用渐变背景
            self.draw_gradient_background()
        
        # 绘制大底（外部背景）带阴影
        large_rect = pygame.Rect(
            self.width // 2 - 450,
            self.height // 2 - 350,
            900,
            700
        )
        
        # 绘制阴影
        shadow_surface = pygame.Surface((large_rect.width + 10, large_rect.height + 10), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, self.shadow_color, (
            5, 5, large_rect.width, large_rect.height), border_radius=self.corner_radius)
        self.screen.blit(shadow_surface, (large_rect.x - 5, large_rect.y - 5))
        
        # 绘制圆角矩形背景
        pygame.draw.rect(self.screen, self.large_bg_color, large_rect, border_radius=self.corner_radius)
        pygame.draw.rect(self.screen, self.border_color, large_rect, 2, border_radius=self.corner_radius)
        
        # 绘制小底（内部内容区域）
        small_rect = pygame.Rect(
            self.width // 2 - 400,
            self.height // 2 - 300,
            800,
            600
        )
        pygame.draw.rect(self.screen, self.small_bg_color, small_rect, border_radius=self.corner_radius - 2)
        pygame.draw.rect(self.screen, self.border_color, small_rect, 1, border_radius=self.corner_radius - 2)
        
        # 绘制标题（带阴影效果）
        title = self.font.render("游戏公告", True, self.title_color)
        # 标题阴影
        title_shadow = self.font.render("游戏公告", True, (0, 0, 0, 80))
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 320))
        self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title, title_rect)
        
        # 绘制公告内容
        y_offset = self.height // 2 - 250
        for announcement in self.announcements:
            text = self.small_font.render(announcement, True, self.text_color)
            text_rect = text.get_rect(center=(self.width // 2, y_offset))
            # 添加轻微的文本阴影
            text_shadow = self.small_font.render(announcement, True, (0, 0, 0, 30))
            self.screen.blit(text_shadow, (text_rect.x + 1, text_rect.y + 1))
            self.screen.blit(text, text_rect)
            y_offset += 40
        
        # 绘制关闭按钮文本
        close_text = self.small_font.render("按ESC键关闭", True, self.close_text_color)
        close_rect = close_text.get_rect(center=(self.width // 2, self.height // 2 + 320))
        self.screen.blit(close_text, close_rect)
    
    def handle_event(self, event):
        """处理公告页面相关事件"""
        if not self.is_open:
            return False
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.is_open = False
                return False
        
        return True

# 示例使用方法
def 主函数():
    屏幕 = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("游戏公告")
    时钟 = pygame.time.Clock()
    
    公告系统 = AnnouncementSystem(屏幕)
    公告系统.is_open = True  # 默认打开公告页面便于测试
    
    运行中 = True
    while 运行中:
        for 事件 in pygame.event.get():
            if 事件.type == QUIT:
                运行中 = False
            公告系统.handle_event(事件)
        
        屏幕.fill((150, 150, 150))  # 灰色游戏背景色
        公告系统.draw()
        
        pygame.display.flip()
        时钟.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    主函数()