import pygame

class DeathPage:
    """死亡页面类，显示玩家死亡信息和复活选项"""
    def __init__(self, game):
        self.game = game
        self.is_open = True
        
        # 初始化字体
        try:
            self.title_font = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 60, bold=True)
            self.button_font = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 24, bold=True)
            self.tip_font = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 20, bold=True)
        except:
            self.title_font = pygame.font.Font(None, 60)
            self.button_font = pygame.font.Font(None, 24)
            self.tip_font = pygame.font.Font(None, 20)
        
        # 按钮配置
        self.button_width = 200
        self.button_height = 50
        self.button_spacing = 10  # 按钮间隔改为10像素
        
        # 按钮颜色配置
        self.base_buttons = [
            {"text": "原地复活", "color": (0, 255, 0), "hover_color": (0, 200, 0)},  # 绿色
            {"text": "返回复活点", "color": (0, 191, 255), "hover_color": (0, 150, 200)},  # 蓝色
            {"text": "清空背包复活", "color": (255, 165, 0), "hover_color": (200, 130, 0)}  # 橙色
        ]
        
        # 创建模式复活按钮，只在创造模式下显示
        self.creative_button = {"text": "创造模式复活", "color": (255, 0, 255), "hover_color": (200, 0, 200)}   # 紫色
        
        # 根据游戏模式动态生成按钮列表
        self.buttons = self.base_buttons.copy()
        if hasattr(self.game, '创造模式') and self.game.创造模式:
            self.buttons.append(self.creative_button)
        
        # 悬停状态
        self.hovered_button = None
        
    def draw(self, screen):
        """绘制死亡页面"""
        # 填充半透明黑色背景
        screen_width, screen_height = screen.get_size()
        background = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        background.fill((0, 0, 0, 200))  # 半透明黑色
        screen.blit(background, (0, 0))
        
        # 绘制标题"你已死亡"
        title_text = self.title_font.render("你已死亡", True, (255, 0, 0))  # 红色文字
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 150))
        screen.blit(title_text, title_rect)
        
        # 计算按钮总高度
        total_buttons_height = len(self.buttons) * self.button_height + (len(self.buttons) - 1) * self.button_spacing
        
        # 绘制按钮
        for i, button_info in enumerate(self.buttons):
            button_y = (screen_height // 2) - (total_buttons_height // 2) + i * (self.button_height + self.button_spacing)
            button_rect = pygame.Rect(
                (screen_width // 2) - (self.button_width // 2),
                button_y,
                self.button_width,
                self.button_height
            )
            
            # 选择按钮颜色
            if self.hovered_button == i:
                color = button_info["hover_color"]
            else:
                color = button_info["color"]
            
            # 绘制按钮
            pygame.draw.rect(screen, color, button_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), button_rect, 3, border_radius=10)  # 白色边框
            
            # 绘制按钮文字
            button_text = self.button_font.render(button_info["text"], True, (255, 255, 255))
            text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, text_rect)
        
        # 绘制star不足提示
        if hasattr(self, 'star_not_enough') and self.star_not_enough:
            star_tip_text = self.tip_font.render("star不足", True, (255, 0, 0))  # 红色文字
            star_tip_rect = star_tip_text.get_rect(center=(screen_width // 2, screen_height // 2 + total_buttons_height // 2 + 50))
            screen.blit(star_tip_text, star_tip_rect)
    
    def handle_mouse_motion(self, event):
        """处理鼠标移动事件，更新悬停状态"""
        screen_width, screen_height = self.game.屏幕.get_size()
        mouse_x, mouse_y = event.pos
        
        # 计算按钮总高度
        total_buttons_height = len(self.buttons) * self.button_height + (len(self.buttons) - 1) * self.button_spacing
        
        # 检查鼠标是否悬停在按钮上
        self.hovered_button = None
        for i, button_info in enumerate(self.buttons):
            button_y = (screen_height // 2) - (total_buttons_height // 2) + i * (self.button_height + self.button_spacing)
            button_rect = pygame.Rect(
                (screen_width // 2) - (self.button_width // 2),
                button_y,
                self.button_width,
                self.button_height
            )
            
            if button_rect.collidepoint(mouse_x, mouse_y):
                self.hovered_button = i
                break
    
    def handle_mouse_click(self, event):
        """处理鼠标点击事件，执行复活逻辑"""
        if event.button == 1:  # 左键点击
            if self.hovered_button is not None:
                self._handle_resurrection(self.hovered_button)
    
    def _handle_resurrection(self, button_index):
        """处理复活逻辑"""
        # 获取按钮文本
        button_text = self.buttons[button_index]['text']
        print(f"选择了复活方式: {button_text}")
        
        # 检查是否需要消耗star
        need_star = button_text in ["原地复活", "返回复活点"]
        if need_star:
            # 检查玩家star数量是否足够
            if not hasattr(self.game.玩家, 'star_count') or self.game.玩家.star_count < 1:
                # star不足，显示提示
                self.star_not_enough = True
                return
        
        # 恢复玩家生命值
        self.game.玩家.current_health = self.game.玩家.max_health
        self.game.玩家.current_hunger = self.game.玩家.max_hunger
        
        # 设置玩家复活后的无敌时间 - 使用状态管理器
        from 状态管理 import 状态管理器实例
        状态管理器实例.激活无敌状态(30)  # 30秒无敌时间
        # 关闭火焰状态
        状态管理器实例.关闭燃烧状态()
        
        # 根据不同按钮执行不同复活逻辑
        if button_index == 0:  # 原地复活
            # 消耗1个star
            self.game.玩家.star_count -= 1
            # 原地复活，不移动玩家位置
            pass
        elif button_index == 1 or button_index == 2:  # 返回复活点或清空背包复活
            if button_index == 1:  # 返回复活点
                # 消耗1个star
                self.game.玩家.star_count -= 1
            else:  # 清空背包复活
                # 清空背包
                if hasattr(self.game, '背包管理器'):
                    self.game.背包管理器.清空背包()
            
            # 返回出生点 - 使用游戏中已有的出生点信息
            # 从游戏对象中获取方块大小和出生点
            方块大小 = getattr(self.game.世界, '方块大小', 32)  # 默认32像素
            
            # 使用游戏参数中的出生点或默认值
            出生点_x = getattr(self.game.世界参数, '出生点_x', 500) if hasattr(self.game, '世界参数') else 500
            出生点_y = getattr(self.game.世界参数, '出生点_y', 0) if hasattr(self.game, '世界参数') else 0
            
            # 游戏中1个方块 = 方块大小（32像素），所以需要将方块坐标转换为像素坐标
            self.game.玩家.坐标_x = 出生点_x * 方块大小
            self.game.玩家.坐标_y = 出生点_y * 方块大小
        elif button_index == 3:  # 创造模式复活
            # 开启创造模式
            self.game.创造模式 = True
        
        # 关闭死亡页面
        self.game.death_page_open = False
        # 移除死亡页面属性，以便下次死亡时重新创建
        delattr(self.game, 'death_page_open')
        delattr(self.game, 'death_page')
        print(f"玩家已复活，剩余star: {self.game.玩家.star_count}")