import pygame
import sys
import math

class 加载窗口:
    def __init__(self, screen=None, width=1200, height=800):
        # 初始化pygame
        pygame.init()
        
        # 设置窗口大小
        self.width, self.height = width, height
        
        # 如果传入了screen，则使用传入的screen，否则创建新screen（兼容旧代码）
        if screen is None:
            # 兼容旧代码，创建新窗口，可调节大小
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
            pygame.display.set_caption("加载资源")
        else:
            # 使用传入的screen，实现统一窗口
            self.screen = screen
        
        # 设置字体
        self.font_large = pygame.font.SysFont("SimHei", 36)
        self.font_medium = pygame.font.SysFont("SimHei", 24)
        self.font_small = pygame.font.SysFont("SimHei", 18)
        
        # 初始化进度值
        self.progress = 0
        self.loading_text = "准备加载资源..."
        
        # 初始化猫猫图片相关
        self.cat_images = []
        self._load_cat_images()
        self.current_cat_image = None
        self.cat_x = 0
        self.cat_y = 0
        
        # 颜色定义
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 128, 255)
        
        # 加载背景图片
        self.background_image = None
        self._load_background_image()
        
        # 设置窗口居中
        self._center_window()
        
        # 绘制初始界面
        self._draw()
        
    def _load_background_image(self):
        """加载背景图片"""
        try:
            import os
            import random
            # 获取当前脚本所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 获取项目根目录（向上一级，因为加载窗口.py在4.游戏界面文件夹中）
            project_root = os.path.dirname(current_dir)
            # 随机选择背景图3到背景图6
            background_index = random.randint(3, 6)
            # 构建背景图片路径
            background_path = os.path.join(project_root, "资源", "图片", "背景-ui", f"背景图{background_index}.png")
            # 检查文件是否存在
            if not os.path.exists(background_path):
                print(f"背景图片文件不存在: {background_path}")
                # 尝试列出目录内容
                bg_ui_dir = os.path.join(project_root, "资源", "图片", "背景-ui")
                if os.path.exists(bg_ui_dir):
                    print(f"背景-ui目录内容: {os.listdir(bg_ui_dir)}")
                else:
                    print(f"背景-ui目录不存在: {bg_ui_dir}")
                self.background_image = None
                return
            # 加载背景图片
            print(f"尝试加载背景图片: {background_path}")
            self.background_image = pygame.image.load(background_path)
            print(f"成功加载背景图片: {background_path}")
            print(f"背景图片尺寸: {self.background_image.get_size()}")
        except Exception as e:
            print(f"加载背景图片失败: {str(e)}")
            import traceback
            traceback.print_exc()
            self.background_image = None
    
    def _center_window(self):
        """将窗口设置在屏幕中央"""
        # 获取屏幕信息
        info = pygame.display.Info()
        screen_width, screen_height = info.current_w, info.current_h
        
        # 计算窗口位置
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        
        # 在Windows系统中，pygame没有直接设置窗口位置的方法
        # 这里仅计算位置信息，不重新创建窗口
    
    def _draw(self):
        """绘制加载界面"""
        # 绘制背景图片
        if self.background_image:
            # 缩放背景图片以适应窗口大小，保持纵横比
            scaled_background = pygame.transform.scale(self.background_image, (self.width, self.height))
            self.screen.blit(scaled_background, (0, 0))
        else:
            # 背景图片加载失败时，使用渐变背景
            self._draw_gradient_background()
        
        # 添加半透明遮罩层，增强文字可读性
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 30))  # 半透明黑色遮罩
        self.screen.blit(overlay, (0, 0))
        
        # 绘制标题 - 使用白色文字，添加文字阴影
        title_text = self.font_large.render("加载资源", True, self.WHITE)
        title_shadow = self.font_large.render("加载资源", True, self.BLACK)
        title_rect = title_text.get_rect(center=(self.width // 2, 80))
        # 绘制文字阴影
        self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title_text, title_rect)
        

        
        # 绘制进度条背景 - 位置调整到窗口下方
        progress_bar_width = int(self.width * 0.7)
        progress_bar_height = 25
        progress_bar_x = (self.width - progress_bar_width) // 2
        # 进度条Y坐标：距离底部80像素
        progress_bar_y = self.height - 120
        
        # 绘制进度条背景 - 带圆角
        pygame.draw.rect(self.screen, (100, 100, 100, 200), (
            progress_bar_x, progress_bar_y, 
            progress_bar_width, progress_bar_height
        ), border_radius=12)
        
        # 绘制进度条填充 - 带圆角和发光效果
        progress_width = int(progress_bar_width * (self.progress / 100))
        if progress_width > 0:
            # 绘制发光效果
            glow_surface = pygame.Surface((progress_width, progress_bar_height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (0, 150, 255, 100), (
                0, 0, progress_width, progress_bar_height
            ), border_radius=12)
            # 绘制放大的发光效果
            scaled_glow = pygame.transform.scale(glow_surface, (progress_width + 8, progress_bar_height + 8))
            self.screen.blit(scaled_glow, (progress_bar_x - 4, progress_bar_y - 4))
            
            # 绘制主进度条
            pygame.draw.rect(self.screen, self.BLUE, (
                progress_bar_x, progress_bar_y, 
                progress_width, progress_bar_height
            ), border_radius=12)
            
            # 绘制进度条高亮
            highlight_rect = pygame.Rect(
                progress_bar_x, progress_bar_y, 
                progress_width, progress_bar_height // 2
            )
            pygame.draw.rect(self.screen, (100, 200, 255), highlight_rect, border_radius=12)
        
        # 绘制进度百分比文本 - 使用白色文字，带阴影
        progress_text = self.font_medium.render(f"{self.progress}%", True, self.WHITE)
        progress_shadow = self.font_medium.render(f"{self.progress}%", True, self.BLACK)
        progress_text_rect = progress_text.get_rect(center=(
            progress_bar_x + progress_bar_width // 2, 
            progress_bar_y + progress_bar_height // 2
        ))
        # 绘制文字阴影
        self.screen.blit(progress_shadow, (progress_text_rect.x + 1, progress_text_rect.y + 1))
        self.screen.blit(progress_text, progress_text_rect)
        
        # 绘制猫猫图片 - 跟随进度
        self._draw_cat()
        
        # 绘制加载状态指示器 - 旋转的圆点
        self._draw_loading_indicator()
        
        # 绘制加载资源信息 - 位置调整到进度条下方，使用白色文字，带阴影
        loading_info = self.font_small.render(self.loading_text, True, self.WHITE)
        loading_shadow = self.font_small.render(self.loading_text, True, self.BLACK)
        loading_info_rect = loading_info.get_rect(center=(
            self.width // 2, 
            progress_bar_y + progress_bar_height + 30
        ))
        # 绘制文字阴影
        self.screen.blit(loading_shadow, (loading_info_rect.x + 1, loading_info_rect.y + 1))
        self.screen.blit(loading_info, loading_info_rect)
        
        # 更新显示
        pygame.display.flip()
    
    def _draw_gradient_background(self):
        """绘制渐变背景"""
        # 垂直渐变背景
        for y in range(self.height):
            # 从深蓝到浅蓝的渐变
            r = 0
            g = 50 + int(y * 150 / self.height)
            b = 100 + int(y * 155 / self.height)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))
    
    def _load_cat_images(self):
        """加载猫猫图片"""
        import os
        try:
            # 获取当前脚本所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 获取项目根目录（向上一级，因为加载窗口.py在4.游戏界面文件夹中）
            project_root = os.path.dirname(current_dir)
            # 构建图片路径
            cat_image_paths = [
                os.path.join(project_root, "资源", "图片", "生物", "小灰猫.png"),
                os.path.join(project_root, "资源", "图片", "生物", "小黑猫.png")
            ]
            
            # 加载所有可用的猫猫图片
            for path in cat_image_paths:
                if os.path.exists(path):
                    image = pygame.image.load(path)
                    # 调整图片大小
                    scaled_image = pygame.transform.scale(image, (50, 50))
                    self.cat_images.append(scaled_image)
                    print(f"成功加载猫猫图片: {path}")
            
            # 如果没有找到猫猫图片，使用默认图片
            if not self.cat_images:
                print("未找到猫猫图片，将使用默认图片")
        except Exception as e:
            print(f"加载猫猫图片失败: {str(e)}")
    
    def _draw_loading_indicator(self):
        """绘制旋转的加载指示器"""
        import time
        indicator_radius = 8
        indicator_x = self.width // 2
        indicator_y = self.height // 2
        
        # 绘制5个旋转的圆点
        for i in range(5):
            angle = time.time() * 6 + i * 1.256  # 1.256是2π/5，速度提高300%
            x = indicator_x + 30 * math.cos(angle)
            y = indicator_y + 30 * math.sin(angle)
            
            # 计算透明度，根据旋转位置变化
            alpha = 50 + 205 * (1 + math.cos(angle)) / 2
            circle_surface = pygame.Surface((indicator_radius * 2, indicator_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (self.WHITE[0], self.WHITE[1], self.WHITE[2], int(alpha)), 
                             (indicator_radius, indicator_radius), indicator_radius)
            self.screen.blit(circle_surface, (x - indicator_radius, y - indicator_radius))
    
    def _draw_cat(self):
        """绘制跟随进度的猫猫图片"""
        if not self.cat_images:
            return
        
        import random
        # 随机选择一张猫猫图片
        if self.current_cat_image is None:
            self.current_cat_image = random.choice(self.cat_images)
        
        # 计算猫猫位置：随进度变化，在进度条上方
        progress_bar_width = int(self.width * 0.7)
        progress_bar_x = (self.width - progress_bar_width) // 2
        progress_bar_y = self.height - 120
        
        # 猫猫X坐标：从进度条左端到进度条当前进度位置
        self.cat_x = progress_bar_x + int(progress_bar_width * (self.progress / 100)) - 25
        # 猫猫Y坐标：在进度条上方50像素
        self.cat_y = progress_bar_y - 60
        
        # 绘制猫猫图片
        self.screen.blit(self.current_cat_image, (self.cat_x, self.cat_y))
    
    def update_progress(self, progress, text):
        """更新进度条和加载信息
        
        Args:
            progress: 进度值(0-100)
            text: 当前加载的资源信息文本
        """
        self.progress = max(0, min(100, progress))  # 限制进度在0-100之间
        self.loading_text = text
        
        # 处理窗口事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 处理窗口大小变化事件
            elif event.type == pygame.VIDEORESIZE:
                self.width, self.height = event.w, event.h
        
        # 重新绘制界面
        self._draw()
    
    def close(self):
        """关闭加载窗口，但不退出pygame"""
        # 不调用pygame.quit()，因为这会导致主游戏无法运行
        # 只需确保加载窗口不再显示
        pass

# 示例使用代码
if __name__ == "__main__":
    import time
    
    # 创建加载窗口实例
    loading_window = 加载窗口()
    
    # 模拟加载过程
    loading_steps = [
        (10, "加载游戏设置..."),
        (30, "加载图片资源..."),
        (50, "加载音频文件..."),
        (70, "初始化游戏系统..."),
        (90, "加载完成，准备启动游戏..."),
        (100, "所有资源加载完成！")
    ]
    
    for progress, text in loading_steps:
        loading_window.update_progress(progress, text)
        time.sleep(1)  # 模拟加载延迟
    
    # 关闭加载窗口
    loading_window.close()