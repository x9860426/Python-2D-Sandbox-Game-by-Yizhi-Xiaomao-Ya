import pygame
import time

# 现代深色主题配色方案（全面优化）
主背景色 = (23, 24, 26)       # 更深邃的深色背景，提升对比度
次级背景色 = (33, 34, 37)     # 调整后的次级背景色，层次感更强
边框颜色 = (60, 60, 63)       # 更柔和的边框颜色
文本颜色 = (245, 245, 245)    # 更明亮的文本，提升可读性
标题颜色 = (255, 255, 255)    # 纯白标题，更醒目
输入框背景色 = (45, 45, 48)   # 输入框背景色，与主背景区分
输入框激活色 = (55, 55, 60)   # 输入框激活状态颜色
按钮悬停色 = (75, 75, 80)     # 按钮悬停颜色
按钮点击色 = (90, 90, 95)     # 按钮点击状态颜色
强调色 = (72, 133, 237)       # 蓝色强调色，用于高亮和选中状态
高亮背景色 = (42, 47, 54)     # 选中项的高亮背景色

class DeveloperDebugPanel:
    """开发者调试页面"""
    
    def __init__(self, game):
        self.game = game
        self.屏幕 = game.屏幕  # 从game实例获取屏幕对象
        self.is_open = False
        
        # 获取屏幕尺寸
        self.屏幕宽度 = self.屏幕.get_width()
        self.屏幕高度 = self.屏幕.get_height()
        
        # 页面尺寸 - 严格保留原有大小
        self.底1宽度 = 200  # 左侧面板宽度（保持不变）
        self.底1高度 = 700  # 左侧面板高度（保持不变）
        self.底2宽度 = 850  # 右侧面板宽度（保持不变）
        self.底2高度 = 700  # 右侧面板高度（保持不变）
        self.间隔 = 20      # 面板间隔（保持不变）
        
        # 计算居中位置
        self.底1_x = (self.屏幕宽度 - self.底1宽度 - self.间隔 - self.底2宽度) // 2
        self.底2_x = self.底1_x + self.底1宽度 + self.间隔
        self.底_y = (self.屏幕高度 - max(self.底1高度, self.底2高度)) // 2
        
        # 圆角半径优化 - 更现代化的圆角
        self.圆角半径 = 12    # 主面板圆角
        self.元素圆角半径 = 6 # 按钮和输入框圆角
        self.小元素圆角半径 = 4 # 小型控件圆角
        
        # 字体设置优化
        self.标题字体 = pygame.font.SysFont("Microsoft YaHei", 24, True)
        self.文本字体 = pygame.font.SysFont("Microsoft YaHei", 16)
        self.输入框字体 = pygame.font.SysFont("Microsoft YaHei", 16, False)
        
        # 按钮设置优化
        self.button_height = 40  # 保持默认高度
        self.button_width = self.底1宽度 - 30
        self.button_spacing = 12  # 略微增加按钮间距，提升视觉舒适度
        
        # 调试选项分类
        self.categories = ["世界设置", "玩家设置", "玩家权限"]
        self.current_category = 0
        
        # 玩家权限设置
        self.is_instant_dig = False  # 秒挖掘（挖掘无时间限制）
        self.has_max_permission = False  # 最高权限（可挖掘基岩）
        self.enable_3x3_place = False  # 3*3放置（快捷栏物品只减少1个）
        self.enable_3x3_dig = False  # 3*3范围挖掘
        self.enable_fullscreen_click = False  # 全屏点击任意位置挖掘放置
        self.enable_fly_mode = False  # 开启飞行模式(按w上升,按s下降)
        
        # 世界时间设置
        self.world_time = "12:00"  # 默认时间
        self.is_input_active = False  # 输入框激活状态
        self.input_text = self.world_time  # 输入框文本
        self.last_update_time = time.time()  # 上次更新时间
        
        # 坐标设置
        self.x_input_text = "0"  # x坐标输入框文本
        self.y_input_text = "0"  # y坐标输入框文本
        self.active_input = None  # 当前激活的输入框 (None, 'x', 'y', 'health', 'speed', 'jump', 'damage', 'gravity')
        self.teleport_button_width = 120  # 传送按钮宽度
        self.teleport_button_height = 30  # 传送按钮高度
        
        # 玩家属性设置
        self.health_input_text = "100"  # 生命值输入框文本
        self.speed_input_text = "5"     # 移动速度输入框文本
        self.jump_input_text = "-10"     # 跳跃力输入框文本
        self.damage_input_text = "10"   # 基础攻击力输入框文本
        self.gravity_input_text = "1"   # 重力值输入框文本
        # Star相关设置 - 添加star百分比和数量设置
        self.star_percentage_input_text = "0"  # star百分比输入框文本
        self.star_count_input_text = "0"       # star数量输入框文本
        
        # 时间更新系数设置
        self.time_speed_input_text = "10"  # 时间更新系数输入框文本（控制游戏时间流逝速度）
        
        # 输入框激活状态
        self.active_input = None  # 当前激活的输入框类型（用于跟踪哪个输入框处于编辑状态）
        
        # 定义UI元素位置
        self._setup_ui_elements()
        
        # 初始化时获取当前游戏时间
        self.world_time = self.get_current_game_time()
        self.input_text = self.world_time
        # 保留初始默认坐标值，不再自动更新为0,0
    
    def _setup_ui_elements(self):
        """设置UI元素位置和尺寸 - 优化布局间距"""
        # 世界时间设置相关元素（优化布局）
        self.time_label_x = self.底2_x + 50
        self.time_label_y = self.底_y + 85  # 调整垂直居中
        
        self.input_box_x = self.底2_x + 150
        self.input_box_y = self.底_y + 80
        self.input_box_width = 100
        self.input_box_height = 30
        
        self.minus_button_x = self.底2_x + 270  # -1:00按钮在左边
        self.minus_button_y = self.底_y + 80
        # 使用独立的变量名，不覆盖分类按钮的尺寸设置
        self.time_button_width = 80
        self.time_button_height = 30
        
        self.plus_button_x = self.底2_x + 370  # +1:00按钮在右边
        self.plus_button_y = self.底_y + 80
        
        # 时间更新系数相关元素（在时间设置下方）
        self.time_speed_label_x = self.底2_x + 50
        self.time_speed_label_y = self.底_y + 130
        
        self.time_speed_input_box_x = self.底2_x + 150
        self.time_speed_input_box_y = self.底_y + 125
        self.time_speed_input_box_width = 100
        self.time_speed_input_box_height = 30
        
        self.time_speed_minus_button_x = self.底2_x + 270  # -1按钮在左边
        self.time_speed_minus_button_y = self.底_y + 125
        self.time_speed_minus_button_width = 50
        self.time_speed_minus_button_height = 30
        
        self.time_speed_plus_button_x = self.底2_x + 330  # +1按钮在右边
        self.time_speed_plus_button_y = self.底_y + 125
        self.time_speed_plus_button_width = 50
        self.time_speed_plus_button_height = 30
        
        # 确定修改和还原按钮位置和尺寸（在时间更新系数+1按钮右侧）
        self.action_button_width = 100  # 统一按钮宽度
        self.action_button_height = 30  # 调整按钮高度与其他按钮一致
        self.confirm_button_x = self.底2_x + 390  # 确定修改按钮X坐标（在+1按钮右侧）
        self.confirm_button_y = self.底_y + 125    # 确定修改按钮Y坐标（与+1按钮同高度）
        self.reset_button_x = self.底2_x + 500      # 还原按钮X坐标（在确定修改按钮右侧）
        self.reset_button_y = self.底_y + 125        # 还原按钮Y坐标（与确定修改按钮同高度）
        
        # 坐标设置相关元素（总共向上移动70像素）
        self.coordinate_label_x = self.底2_x + 50
        self.coordinate_label_y = self.底_y + 80
        
        self.x_label_x = self.底2_x + 200
        self.x_label_y = self.底_y + 80
        
        self.x_input_box_x = self.底2_x + 240
        self.x_input_box_y = self.底_y + 75
        
        self.y_label_x = self.底2_x + 360
        self.y_label_y = self.底_y + 80
        
        self.y_input_box_x = self.底2_x + 400
        self.y_input_box_y = self.底_y + 75
        
        self.teleport_button_x = self.底2_x + 520
        self.teleport_button_y = self.底_y + 75
        
        # 玩家属性设置相关元素位置（在坐标设置下方）
        # 第一行：生命值、移动速度、跳跃力
        # 生命值 - 左侧
        self.health_label_x = self.底2_x + 50  # 生命值标签X坐标
        self.health_label_y = self.底_y + 130  # 生命值标签Y坐标
        self.health_input_box_x = self.底2_x + 140  # 生命值输入框X坐标
        self.health_input_box_y = self.底_y + 125  # 生命值输入框Y坐标
        
        # 移动速度 - 中间（右移30像素）
        self.speed_label_x = self.底2_x + 260  # 移动速度标签X坐标（右移30像素）
        self.speed_label_y = self.底_y + 130  # 移动速度标签Y坐标
        self.speed_input_box_x = self.底2_x + 340  # 移动速度输入框X坐标（右移30像素）
        self.speed_input_box_y = self.底_y + 125  # 移动速度输入框Y坐标
        
        # 跳跃力 - 右侧（右移60像素）
        self.jump_label_x = self.底2_x + 450  # 跳跃力标签X坐标（右移60像素）
        self.jump_label_y = self.底_y + 130  # 跳跃力标签Y坐标
        self.jump_input_box_x = self.底2_x + 510  # 跳跃力输入框X坐标（右移60像素）
        self.jump_input_box_y = self.底_y + 125  # 跳跃力输入框Y坐标
        
        # 第二行：初始伤害、重力值和确定修改按钮
        # 初始伤害 - 左侧
        self.damage_label_x = self.底2_x + 50  # 初始伤害标签X坐标
        self.damage_label_y = self.底_y + 180  # 初始伤害标签Y坐标
        self.damage_input_box_x = self.底2_x + 140  # 初始伤害输入框X坐标
        self.damage_input_box_y = self.底_y + 175  # 初始伤害输入框Y坐标
        
        # 重力值 - 中间（右移30像素）
        self.gravity_label_x = self.底2_x + 260  # 重力值标签X坐标（右移30像素）
        self.gravity_label_y = self.底_y + 180  # 重力值标签Y坐标
        self.gravity_input_box_x = self.底2_x + 340  # 重力值输入框X坐标（右移30像素）
        self.gravity_input_box_y = self.底_y + 175  # 重力值输入框Y坐标
        
        # 重力值加减按钮（-0.1按钮在左边，+0.1按钮在右边）
        self.gravity_minus_button_x = self.底2_x + 450  # 重力值-0.1按钮X坐标（左移60像素）
        self.gravity_minus_button_y = self.底_y + 175  # 重力值-0.1按钮Y坐标
        self.gravity_minus_button_width = 50  # 重力值-0.1按钮宽度
        self.gravity_minus_button_height = 30  # 重力值-0.1按钮高度
        
        self.gravity_plus_button_x = self.底2_x + 510  # 重力值+0.1按钮X坐标（与-按钮间隔10像素，右移20像素）
        self.gravity_plus_button_y = self.底_y + 175  # 重力值+0.1按钮Y坐标
        self.gravity_plus_button_width = 50  # 重力值+0.1按钮宽度
        self.gravity_plus_button_height = 30  # 重力值+0.1按钮高度
        
        # Star相关UI元素位置 - 新增第三行设置
        # Star百分比 - 左侧
        self.star_percentage_label_x = self.底2_x + 50  # star百分比标签X坐标
        self.star_percentage_label_y = self.底_y + 230  # star百分比标签Y坐标（在重力值下方）
        self.star_percentage_input_box_x = self.底2_x + 140  # star百分比输入框X坐标
        self.star_percentage_input_box_y = self.底_y + 225  # star百分比输入框Y坐标
        
        # Star数量 - 中间
        self.star_count_label_x = self.底2_x + 260  # star数量标签X坐标
        self.star_count_label_y = self.底_y + 230  # star数量标签Y坐标
        self.star_count_input_box_x = self.底2_x + 340  # star数量输入框X坐标
        self.star_count_input_box_y = self.底_y + 225  # star数量输入框Y坐标
        
        # 确定修改按钮 - 右侧
        self.update_button_x = self.底2_x +  650 # 更新按钮X坐标
        self.update_button_y = self.底_y + 140  # 更新按钮Y坐标（与第二行对齐）
        self.update_button_width = 100  # 更新按钮宽度
        self.update_button_height = 50  # 更新按钮高度
        
        # 坐标设置区域底UI（包裹坐标修改元素）
        self.coordinate_settings_bg_x = self.底2_x + 30  # 坐标底UI X坐标
        self.coordinate_settings_bg_y = self.底_y + 70  # 坐标底UI Y坐标
        self.coordinate_settings_bg_width = 800  # 坐标底UI宽度
        self.coordinate_settings_bg_height = 40  # 坐标底UI高度
        
        # 玩家属性设置区域底UI（包裹所有元素）- 增加高度以容纳star设置
        self.player_settings_bg_x = self.底2_x + 30  # 底UI X坐标
        self.player_settings_bg_y = self.底_y + 120  # 底UI Y坐标
        self.player_settings_bg_width = 800  # 底UI宽度
        self.player_settings_bg_height = 150  # 增加底UI高度以容纳star设置
    
    def toggle(self):
        """切换页面显示状态"""
        self.is_open = not self.is_open
        if self.is_open:
            # 重置输入状态
            self.is_input_active = False
            self.world_time = self.get_current_game_time()
            self.input_text = self.world_time
            self.last_update_time = time.time()
            # 不再自动更新玩家坐标，保留上次设置的值
            # 更新玩家属性输入框显示
            if hasattr(self.game, '玩家'):
                player = self.game.玩家
                if hasattr(player, '生命值'):
                    self.health_input_text = str(int(player.生命值))
                if hasattr(player, '移动速度'):
                    self.speed_input_text = str(player.移动速度)
                if hasattr(player, '跳跃力度'):
                    self.jump_input_text = str(player.跳跃力度)
                if hasattr(player, 'base_attack'):
                    self.damage_input_text = str(int(player.base_attack))
                if hasattr(player, '重力值'):
                    self.gravity_input_text = str(player.重力值)
                
                # 初始化star相关设置
                if hasattr(player, 'star_progress'):
                    # 如果有star进度属性，直接使用
                    self.star_percentage_input_text = str(int(player.star_progress * 100))  # 转换为百分比
                elif hasattr(player, 'star_experience'):
                    # 如果有star经验属性，设置为当前值
                    self.star_percentage_input_text = str(int(player.star_experience))
                
                if hasattr(player, 'star_count'):
                    # 如果有star数量属性，直接使用
                    self.star_count_input_text = str(player.star_count)
                elif hasattr(player, 'stars'):
                    # 如果有stars属性，设置为当前值
                    self.star_count_input_text = str(player.stars)
        return self.is_open
        
    def get_current_game_time(self):
        """获取当前游戏时间"""
        # 优先使用传入的world对象
        if hasattr(self, 'world') and self.world is not None and hasattr(self.world, '时间_of_day'):
            # 从游戏世界对象获取实际时间 (100 = 1小时)
            hours = int(self.world.时间_of_day // 100)
            minutes = int((self.world.时间_of_day % 100) * 0.6)
            return f"{hours:02d}:{minutes:02d}"
        # 尝试从游戏实例获取
        elif hasattr(self.game, '世界') and hasattr(self.game.世界, '时间_of_day'):
            hours = int(self.game.世界.时间_of_day // 100)
            minutes = int((self.game.世界.时间_of_day % 100) * 0.6)
            return f"{hours:02d}:{minutes:02d}"
        # 默认返回系统当前时间
        return time.strftime("%H:%M")
    
    def draw(self, 屏幕):
        """绘制开发者调试页面"""
        if not self.is_open:
            return
        
        # 更新屏幕引用和尺寸
        self.屏幕 = 屏幕
        self.屏幕宽度 = self.屏幕.get_width()
        self.屏幕高度 = self.屏幕.get_height()
        
        # 重新计算居中位置，确保F4页面始终居中
        self.底1_x = (self.屏幕宽度 - self.底1宽度 - self.间隔 - self.底2宽度) // 2
        self.底2_x = self.底1_x + self.底1宽度 + self.间隔
        self.底_y = (self.屏幕高度 - max(self.底1高度, self.底2高度)) // 2
        
        # 同时更新UI元素位置
        self._setup_ui_elements()
        
        # 绘制背景遮罩
        overlay = pygame.Surface((self.屏幕宽度, self.屏幕高度), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # 半透明黑色
        self.屏幕.blit(overlay, (0, 0))
        
        # 绘制底1（左侧面板）带圆角 - 优化视觉效果
        # 绘制轻微发光效果
        pygame.draw.rect(self.屏幕, (40, 40, 45, 30), 
                        (self.底1_x - 2, self.底_y - 2, self.底1宽度 + 4, self.底1高度 + 4), 
                        border_radius=self.圆角半径 + 2)
        # 主面板
        pygame.draw.rect(self.屏幕, 主背景色, 
                        (self.底1_x, self.底_y, self.底1宽度, self.底1高度), 
                        border_radius=self.圆角半径)
        # 增强边框
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (self.底1_x, self.底_y, self.底1宽度, self.底1高度), 
                        2, border_radius=self.圆角半径)
        
        # 绘制底2（右侧面板）带圆角 - 优化视觉效果
        # 绘制轻微发光效果
        pygame.draw.rect(self.屏幕, (40, 40, 45, 30), 
                        (self.底2_x - 2, self.底_y - 2, self.底2宽度 + 4, self.底2高度 + 4), 
                        border_radius=self.圆角半径 + 2)
        # 主面板
        pygame.draw.rect(self.屏幕, 主背景色, 
                        (self.底2_x, self.底_y, self.底2宽度, self.底2高度), 
                        border_radius=self.圆角半径)
        # 增强边框
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (self.底2_x, self.底_y, self.底2宽度, self.底2高度), 
                        2, border_radius=self.圆角半径)
        
        # 绘制左侧面板标题 - 增强视觉效果
        左侧标题 = self.标题字体.render("设置选项", True, 标题颜色)
        左侧标题_rect = 左侧标题.get_rect(center=(self.底1_x + self.底1宽度//2, self.底_y + 30))
        # 增强标题阴影效果
        左侧标题阴影 = self.标题字体.render("设置选项", True, (0, 0, 0, 100))
        self.屏幕.blit(左侧标题阴影, (左侧标题_rect.x + 2, 左侧标题_rect.y + 2))
        # 添加轻微光晕效果
        pygame.draw.rect(self.屏幕, (50, 50, 50, 50), 
                        (左侧标题_rect.x - 5, 左侧标题_rect.y - 5, 
                        左侧标题_rect.width + 10, 左侧标题_rect.height + 10), 
                        border_radius=5)
        self.屏幕.blit(左侧标题, 左侧标题_rect)
        
        # 绘制右侧面板标题 - 增强视觉效果
        右侧标题 = self.标题字体.render(self.categories[self.current_category], True, 标题颜色)
        右侧标题_rect = 右侧标题.get_rect(center=(self.底2_x + self.底2宽度//2, self.底_y + 30))
        # 增强标题阴影效果
        右侧标题阴影 = self.标题字体.render(self.categories[self.current_category], True, (0, 0, 0, 100))
        self.屏幕.blit(右侧标题阴影, (右侧标题_rect.x + 2, 右侧标题_rect.y + 2))
        # 添加轻微光晕效果
        pygame.draw.rect(self.屏幕, (50, 50, 50, 50), 
                        (右侧标题_rect.x - 5, 右侧标题_rect.y - 5, 
                        右侧标题_rect.width + 10, 右侧标题_rect.height + 10), 
                        border_radius=5)
        self.屏幕.blit(右侧标题, 右侧标题_rect)
        
        # 绘制分类按钮
        self.draw_category_buttons()
        
        # 绘制内容区域
        self.draw_content()
        
        # 绘制关闭按钮
        self.draw_close_button()
    
    def draw_category_buttons(self):
        """绘制左侧分类按钮 - 优化视觉反馈和交互效果"""
        # 计算按钮起始位置（略微下移，与优化后的标题更协调）
        button_start_y = self.底_y + 80
        
        for i, category in enumerate(self.categories):
            button_y = button_start_y + i * (self.button_height + self.button_spacing)
            
            # 创建按钮矩形
            button_rect = pygame.Rect(
                self.底1_x + 15,
                button_y,
                self.button_width,
                self.button_height
            )
            
            # 检查鼠标是否悬停
            is_hovered = button_rect.collidepoint(pygame.mouse.get_pos())
            
            # 根据状态设置按钮样式
            if i == self.current_category:
                # 选中状态 - 使用强调色和高亮背景
                bg_color = 高亮背景色
                border_color = 强调色
                text_color = 标题颜色  # 选中时文字更亮
                border_width = 2
            elif is_hovered:
                # 悬停状态 - 更明显的视觉反馈
                bg_color = 次级背景色
                border_color = 按钮悬停色
                text_color = 文本颜色
                border_width = 1
            else:
                # 普通状态
                bg_color = 主背景色
                border_color = 边框颜色
                text_color = 文本颜色
                border_width = 1
            
            # 绘制按钮背景
            pygame.draw.rect(self.屏幕, bg_color, button_rect, border_radius=self.元素圆角半径)
            # 绘制边框
            pygame.draw.rect(self.屏幕, border_color, button_rect, border_width, border_radius=self.元素圆角半径)
            
            # 选中状态添加额外效果
            if i == self.current_category:
                # 内部发光效果
                inner_glow_rect = button_rect.inflate(-4, -4)
                pygame.draw.rect(self.屏幕, (100, 100, 120, 30), inner_glow_rect, border_radius=self.小元素圆角半径)
                # 添加强调色点缀
                pygame.draw.circle(self.屏幕, 强调色, 
                                  (button_rect.left + 10, button_rect.centery), 4)
            
            # 绘制按钮文字
            text = self.文本字体.render(category, True, text_color)
            text_rect = text.get_rect(center=button_rect.center)
            # 普通和悬停状态时文字居中，选中状态时文字略微右移
            if i == self.current_category:
                text_rect.x += 8
            # 添加轻微文字阴影提升质感
            shadow_text = self.文本字体.render(category, True, (0, 0, 0, 50))
            self.屏幕.blit(shadow_text, (text_rect.x + 1, text_rect.y + 1))
            self.屏幕.blit(text, text_rect)
    
    def update(self, world=None):
        """更新页面状态，每秒更新时间显示和玩家属性"""
        if not self.is_open or self.is_input_active:
            return
        
        # 如果提供了world参数，使用它来获取和更新时间
        self.world = world
        
        # 每秒更新一次时间
        current_time = time.time()
        if current_time - self.last_update_time >= 1.0:
            self.world_time = self.get_current_game_time()
            self.input_text = self.world_time
            self.last_update_time = current_time
        
        # 更新玩家坐标输入框
        # 只在坐标输入框未激活时更新，避免覆盖用户正在输入的内容
        if self.active_input not in ['x', 'y']:
            self._update_player_coordinates()
            
        # 每次更新都刷新玩家属性输入框（即使没有激活）
        if hasattr(self.game, '玩家'):
            player = self.game.玩家
            # 只在输入框未激活时更新，避免覆盖用户正在输入的内容
            if hasattr(player, 'current_health') and self.active_input != 'health':
                self.health_input_text = str(int(player.current_health))
            if hasattr(player, '移动速度') and self.active_input != 'speed':
                self.speed_input_text = str(player.移动速度)
            if hasattr(player, '跳跃力') and self.active_input != 'jump':
                self.jump_input_text = str(player.跳跃力)
            if hasattr(player, 'base_attack') and self.active_input != 'damage':
                self.damage_input_text = str(int(player.base_attack))
            if hasattr(player, '重力值') and self.active_input != 'gravity':
                self.gravity_input_text = str(player.重力值)
    
    def draw_content(self):
        """绘制右侧内容区域"""
        # 先更新时间（如果页面打开且输入框未激活）
        # 这里不传world参数，因为在主循环中会调用update
        
        if self.current_category == 0:  # 世界设置
            self.draw_world_settings()
        elif self.current_category == 1:  # 玩家设置
            self.draw_player_settings()
        elif self.current_category == 2:  # 玩家权限
            self.draw_player_permissions()
            
    def draw_player_permissions(self):
        """绘制玩家权限设置页面"""
        # 添加内容区域背景（内底，比外底更浅）
        content_bg_rect = pygame.Rect(self.底2_x + 20, self.底_y + 50, self.底2宽度 - 40, self.底2高度 - 100)
        内底颜色 = (45, 45, 48)  # 比外底主背景色更浅的灰色
        pygame.draw.rect(self.屏幕, (40, 40, 45, 30), content_bg_rect.inflate(4, 4), border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, 内底颜色, content_bg_rect, border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, content_bg_rect, 1, border_radius=self.元素圆角半径)
        
        # 移除重复的标题绘制，因为draw方法中已经绘制了右侧面板标题
        
        # 权限选项起始位置
        option_start_y = self.底_y + 80
        option_spacing = 40
        
        # 绘制秒挖掘选项
        self._draw_permission_option("秒挖掘（挖掘无时间限制）", self.is_instant_dig, option_start_y)
        
        # 绘制最高权限选项
        self._draw_permission_option("最高权限（可挖掘基岩）", self.has_max_permission, option_start_y + option_spacing)
        
        # 绘制3*3放置选项
        self._draw_permission_option("3*3放置（快捷栏物品只减少1个）", self.enable_3x3_place, option_start_y + option_spacing * 2)
        
        # 绘制3*3范围挖掘选项
        self._draw_permission_option("3*3范围挖掘", self.enable_3x3_dig, option_start_y + option_spacing * 3)
        
        # 绘制全屏点击任意位置挖掘放置选项
        self._draw_permission_option("全屏点击任意位置挖掘放置", self.enable_fullscreen_click, option_start_y + option_spacing * 4)
        
        # 绘制开启飞行模式选项
        self._draw_permission_option("开启飞行模式(按w上升,按s下降)", self.enable_fly_mode, option_start_y + option_spacing * 5)
        
        # 绘制应用按钮
        apply_button_rect = pygame.Rect(self.底2_x + self.底2宽度 // 2 - 100, self.底_y + self.底2高度 - 60, 200, 40)
        self._draw_button("应用权限设置", apply_button_rect)
        
        # 检查按钮点击
        mouse_pos = pygame.mouse.get_pos()
        if apply_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self._apply_permissions()
    
    def _draw_permission_option(self, label_text, is_enabled, y_position):
        """绘制单个权限选项（开关）"""
        # 计算位置
        label_x = self.底2_x + 40
        toggle_x = self.底2_x + self.底2宽度 - 100
        
        # 绘制标签
        label = self.文本字体.render(label_text, True, 文本颜色)
        self.屏幕.blit(label, (label_x, y_position))
        
        # 绘制开关背景
        toggle_bg_rect = pygame.Rect(toggle_x, y_position - 5, 80, 30)
        toggle_bg_color = 强调色 if is_enabled else 输入框背景色
        pygame.draw.rect(self.屏幕, toggle_bg_color, toggle_bg_rect, border_radius=self.小元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, toggle_bg_rect, 1, border_radius=self.小元素圆角半径)
        
        # 绘制开关滑块
        slider_x = toggle_x + 55 if is_enabled else toggle_x + 5
        slider_rect = pygame.Rect(slider_x, y_position - 1, 20, 22)
        pygame.draw.rect(self.屏幕, 标题颜色, slider_rect, border_radius=self.小元素圆角半径 - 1)
        
        # 注意：移除了直接检测鼠标状态的代码，现在点击处理逻辑移至handle_mouse_click方法
        # 这样可以避免开关过于敏感，确保每个点击事件只触发一次切换
    
    def _draw_button(self, text, rect):
        """绘制按钮"""
        # 检查鼠标是否悬停
        is_hovered = rect.collidepoint(pygame.mouse.get_pos())
        
        # 设置按钮颜色
        bg_color = 按钮悬停色 if is_hovered else 次级背景色
        
        # 绘制按钮背景
        pygame.draw.rect(self.屏幕, bg_color, rect, border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, rect, 1, border_radius=self.元素圆角半径)
        
        # 绘制按钮文本
        button_text = self.文本字体.render(text, True, 文本颜色)
        text_rect = button_text.get_rect(center=rect.center)
        self.屏幕.blit(button_text, text_rect)
    
    def _apply_permissions(self):
        """应用玩家权限设置到游戏中"""
        # 更新游戏实例中的权限状态
        print("应用玩家权限设置:")
        print(f"  秒挖掘: {self.is_instant_dig}")
        print(f"  最高权限: {self.has_max_permission}")
        print(f"  3*3放置: {self.enable_3x3_place}")
        print(f"  3*3范围挖掘: {self.enable_3x3_dig}")
        print(f"  全屏点击任意位置挖掘放置: {self.enable_fullscreen_click}")
        print(f"  开启飞行模式: {self.enable_fly_mode}")
        
        # 将秒挖掘状态应用到游戏实例
        self.game.is_instant_dig = self.is_instant_dig
        print(f"  应用到游戏实例 - 秒挖掘: {self.game.is_instant_dig}")
        
        # 将最高权限应用到游戏实例
        self.game.has_max_permission = self.has_max_permission
        print(f"  应用到游戏实例 - 最高权限: {self.game.has_max_permission}")
        
        # 将3*3放置应用到游戏实例
        self.game.enable_3x3_place = self.enable_3x3_place
        print(f"  应用到游戏实例 - 3*3放置: {self.game.enable_3x3_place}")
        
        # 将3*3范围挖掘应用到游戏实例
        self.game.enable_3x3_dig = self.enable_3x3_dig
        print(f"  应用到游戏实例 - 3*3范围挖掘: {self.game.enable_3x3_dig}")
        
        # 将全屏点击任意位置挖掘放置应用到游戏实例
        self.game.enable_fullscreen_click = self.enable_fullscreen_click
        print(f"  应用到游戏实例 - 全屏点击: {self.game.enable_fullscreen_click}")
        
        # 将飞行模式应用到玩家对象
        if hasattr(self.game, '玩家') and hasattr(self.game.玩家, 'fly_mode'):
            self.game.玩家.fly_mode = self.enable_fly_mode
            print(f"  飞行模式(按w上升,按s下降) 已切换为: {self.game.玩家.fly_mode}")
    
    def draw_world_settings(self):
        """绘制世界设置内容 - 优化UI元素视觉效果"""
        # 添加内容区域背景（内底，比外底更浅）
        content_bg_rect = pygame.Rect(self.底2_x + 20, self.底_y + 50, self.底2宽度 - 40, 120)
        内底颜色 = (45, 45, 48)  # 比外底主背景色更浅的灰色
        pygame.draw.rect(self.屏幕, (40, 40, 45, 30), content_bg_rect.inflate(4, 4), border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, 内底颜色, content_bg_rect, border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, content_bg_rect, 1, border_radius=self.元素圆角半径)
        
        # 绘制"时间："文字 - 使用标题颜色并添加阴影
        time_label = self.文本字体.render("时间：", True, 标题颜色)
        shadow_label = self.文本字体.render("时间：", True, (0, 0, 0, 50))
        self.屏幕.blit(shadow_label, (self.time_label_x + 1, self.time_label_y + 1))
        self.屏幕.blit(time_label, (self.time_label_x, self.time_label_y))
        
        # 绘制输入框 - 增强视觉效果和交互反馈
        input_box_rect = pygame.Rect(self.input_box_x, self.input_box_y, self.input_box_width, self.input_box_height)
        is_input_hovered = input_box_rect.collidepoint(pygame.mouse.get_pos())
        
        if self.is_input_active:
            # 激活状态
            input_box_color = 输入框激活色
            border_color = 强调色
            border_width = 2
        elif is_input_hovered:
            # 悬停状态
            input_box_color = 输入框背景色
            border_color = 按钮悬停色
            border_width = 1
        else:
            # 普通状态
            input_box_color = 输入框背景色
            border_color = 边框颜色
            border_width = 1
        
        pygame.draw.rect(self.屏幕, input_box_color, input_box_rect, border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, border_color, input_box_rect, border_width, border_radius=self.元素圆角半径)
        
        # 绘制输入框文本 - 添加阴影
        input_text = self.输入框字体.render(self.input_text, True, 文本颜色)
        shadow_text = self.输入框字体.render(self.input_text, True, (0, 0, 0, 50))
        text_rect = input_text.get_rect(center=input_box_rect.center)
        self.屏幕.blit(shadow_text, (text_rect.x + 1, text_rect.y + 1))
        self.屏幕.blit(input_text, text_rect)
        
        # 绘制-1:00按钮（现在在左边）- 增强视觉反馈
        minus_button_rect = pygame.Rect(self.minus_button_x, self.minus_button_y, self.time_button_width, self.time_button_height)
        is_minus_hovered = minus_button_rect.collidepoint(pygame.mouse.get_pos())
        
        if is_minus_hovered:
            pygame.draw.rect(self.屏幕, 按钮悬停色, minus_button_rect, border_radius=self.小元素圆角半径)
            pygame.draw.rect(self.屏幕, 强调色, minus_button_rect, 1, border_radius=self.小元素圆角半径)
        else:
            pygame.draw.rect(self.屏幕, 次级背景色, minus_button_rect, border_radius=self.小元素圆角半径)
            pygame.draw.rect(self.屏幕, 边框颜色, minus_button_rect, 1, border_radius=self.小元素圆角半径)
        
        minus_text = self.文本字体.render("-1：00", True, 标题颜色)
        shadow_text = self.文本字体.render("-1：00", True, (0, 0, 0, 50))
        minus_text_rect = minus_text.get_rect(center=minus_button_rect.center)
        self.屏幕.blit(shadow_text, (minus_text_rect.x + 1, minus_text_rect.y + 1))
        self.屏幕.blit(minus_text, minus_text_rect)
        
        # 绘制+1:00按钮（现在在右边）- 增强视觉反馈
        plus_button_rect = pygame.Rect(self.plus_button_x, self.plus_button_y, self.time_button_width, self.time_button_height)
        is_plus_hovered = plus_button_rect.collidepoint(pygame.mouse.get_pos())
        
        if is_plus_hovered:
            pygame.draw.rect(self.屏幕, 按钮悬停色, plus_button_rect, border_radius=self.小元素圆角半径)
            pygame.draw.rect(self.屏幕, 强调色, plus_button_rect, 1, border_radius=self.小元素圆角半径)
        else:
            pygame.draw.rect(self.屏幕, 次级背景色, plus_button_rect, border_radius=self.小元素圆角半径)
            pygame.draw.rect(self.屏幕, 边框颜色, plus_button_rect, 1, border_radius=self.小元素圆角半径)
        
        plus_text = self.文本字体.render("+1：00", True, 标题颜色)
        shadow_text = self.文本字体.render("+1：00", True, (0, 0, 0, 50))
        plus_text_rect = plus_text.get_rect(center=plus_button_rect.center)
        self.屏幕.blit(shadow_text, (plus_text_rect.x + 1, plus_text_rect.y + 1))
        self.屏幕.blit(plus_text, plus_text_rect)
        
        # 绘制时间更新系数设置（在时间设置下方）
        # 1. 绘制"时间更新系数："文字
        time_speed_label = self.文本字体.render("时间更新系数：", True, 文本颜色)
        self.屏幕.blit(time_speed_label, (self.time_speed_label_x, self.time_speed_label_y))
        
        # 2. 绘制时间更新系数输入框
        time_speed_input_box_rect = pygame.Rect(self.time_speed_input_box_x, self.time_speed_input_box_y, self.time_speed_input_box_width, self.time_speed_input_box_height)
        time_speed_input_box_color = 输入框背景色 if self.active_input != 'time_speed' else (60, 60, 60)
        pygame.draw.rect(self.屏幕, time_speed_input_box_color, time_speed_input_box_rect, border_radius=3)
        pygame.draw.rect(self.屏幕, 边框颜色, time_speed_input_box_rect, 1, border_radius=3)
        
        # 绘制时间更新系数输入框文本
        time_speed_input_text = self.输入框字体.render(self.time_speed_input_text, True, 文本颜色)
        time_speed_text_rect = time_speed_input_text.get_rect(center=time_speed_input_box_rect.center)
        self.屏幕.blit(time_speed_input_text, time_speed_text_rect)
        
        # 3. 绘制时间更新系数-1按钮（左边）
        time_speed_minus_rect = pygame.Rect(self.time_speed_minus_button_x, self.time_speed_minus_button_y, self.time_speed_minus_button_width, self.time_speed_minus_button_height)
        # 检查鼠标是否悬停
        if time_speed_minus_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.屏幕, 按钮悬停色, time_speed_minus_rect, border_radius=3)
        else:
            pygame.draw.rect(self.屏幕, 次级背景色, time_speed_minus_rect, border_radius=3)
        pygame.draw.rect(self.屏幕, 边框颜色, time_speed_minus_rect, 1, border_radius=3)
        
        time_speed_minus_text = self.文本字体.render("-1", True, 文本颜色)
        time_speed_minus_text_rect = time_speed_minus_text.get_rect(center=time_speed_minus_rect.center)
        self.屏幕.blit(time_speed_minus_text, time_speed_minus_text_rect)
        
        # 4. 绘制时间更新系数+1按钮（右边）
        time_speed_plus_rect = pygame.Rect(self.time_speed_plus_button_x, self.time_speed_plus_button_y, self.time_speed_plus_button_width, self.time_speed_plus_button_height)
        # 检查鼠标是否悬停
        if time_speed_plus_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.屏幕, 按钮悬停色, time_speed_plus_rect, border_radius=3)
        else:
            pygame.draw.rect(self.屏幕, 次级背景色, time_speed_plus_rect, border_radius=3)
        pygame.draw.rect(self.屏幕, 边框颜色, time_speed_plus_rect, 1, border_radius=3)
        
        time_speed_plus_text = self.文本字体.render("+1", True, 文本颜色)
        time_speed_plus_text_rect = time_speed_plus_text.get_rect(center=time_speed_plus_rect.center)
        self.屏幕.blit(time_speed_plus_text, time_speed_plus_text_rect)
        
        # 绘制确定修改按钮（在+1按钮右侧）
        confirm_button_rect = pygame.Rect(self.confirm_button_x, self.confirm_button_y, self.action_button_width, self.action_button_height)
        if confirm_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.屏幕, 按钮悬停色, confirm_button_rect, border_radius=3)
        else:
            pygame.draw.rect(self.屏幕, 次级背景色, confirm_button_rect, border_radius=3)
        pygame.draw.rect(self.屏幕, 边框颜色, confirm_button_rect, 1, border_radius=3)
        
        confirm_text = self.文本字体.render("确定修改", True, 文本颜色)
        confirm_text_rect = confirm_text.get_rect(center=confirm_button_rect.center)
        self.屏幕.blit(confirm_text, confirm_text_rect)
        
        # 绘制还原按钮（在确定修改按钮右侧）
        reset_button_rect = pygame.Rect(self.reset_button_x, self.reset_button_y, self.action_button_width, self.action_button_height)
        if reset_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.屏幕, 按钮悬停色, reset_button_rect, border_radius=3)
        else:
            pygame.draw.rect(self.屏幕, 次级背景色, reset_button_rect, border_radius=3)
        pygame.draw.rect(self.屏幕, 边框颜色, reset_button_rect, 1, border_radius=3)
        
        reset_text = self.文本字体.render("还原", True, 文本颜色)
        reset_text_rect = reset_text.get_rect(center=reset_button_rect.center)
        self.屏幕.blit(reset_text, reset_text_rect)
    
    def draw_player_settings(self):
        """绘制玩家设置内容，包括坐标修改功能，每次绘制时更新显示最新的玩家属性值"""
        # 每次绘制时实时更新玩家属性显示（如果输入框未激活），确保显示最新值
        if hasattr(self, 'game') and hasattr(self.game, '玩家'):
            player = self.game.玩家
            # 实时更新生命值显示 - 优先显示当前生命值，如果不存在则显示最大生命值（使用正确的属性名）
            if self.active_input != 'health':
                if hasattr(player, 'current_health'):
                    self.health_input_text = str(int(player.current_health))
                elif hasattr(player, 'max_health'):
                    self.health_input_text = str(int(player.max_health))
            # 实时更新移动速度显示
            if hasattr(player, '移动速度') and self.active_input != 'speed':
                self.speed_input_text = str(player.移动速度)
            # 实时更新跳跃力显示（使用正确的属性名'跳跃力度'）
            if hasattr(player, '跳跃力度') and self.active_input != 'jump':
                self.jump_input_text = str(player.跳跃力度)
            # 实时更新基础攻击力显示
            if hasattr(player, 'base_attack') and self.active_input != 'damage':
                self.damage_input_text = str(int(player.base_attack))
            # 实时更新重力值显示
            if hasattr(player, '重力值') and self.active_input != 'gravity':
                self.gravity_input_text = str(player.重力值)
            # 实时更新Star相关显示
            # Star百分比
            if self.active_input != 'star_percentage':
                if hasattr(player, 'star_progress'):
                    self.star_percentage_input_text = str(int(player.star_progress * 100))  # 转换为百分比
                elif hasattr(player, 'star_experience'):
                    self.star_percentage_input_text = str(int(player.star_experience))
            # Star数量
            if self.active_input != 'star_count':
                if hasattr(player, 'star_count'):
                    self.star_count_input_text = str(player.star_count)
                elif hasattr(player, 'stars'):
                    self.star_count_input_text = str(player.stars)
        
        # 对于坐标，仍然保持只在面板打开时更新，让用户可以自由输入修改坐标
        
        # 绘制坐标设置区域底UI背景（内底，比外底更浅）
        coordinate_bg_rect = pygame.Rect(self.coordinate_settings_bg_x, self.coordinate_settings_bg_y, self.coordinate_settings_bg_width, self.coordinate_settings_bg_height)
        内底颜色 = (45, 45, 48)  # 比外底主背景色更浅的灰色
        # 添加微妙发光效果
        pygame.draw.rect(self.屏幕, (40, 40, 45, 30), coordinate_bg_rect.inflate(4, 4), border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, 内底颜色, coordinate_bg_rect, border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, coordinate_bg_rect, 1, border_radius=self.元素圆角半径)
        
        # 绘制"修改坐标："文字 - 添加轻微阴影
        coordinate_label = self.文本字体.render("修改坐标：", True, 标题颜色)
        shadow_label = self.文本字体.render("修改坐标：", True, (0, 0, 0, 50))
        self.屏幕.blit(shadow_label, (self.coordinate_label_x + 1, self.coordinate_label_y + 1))
        self.屏幕.blit(coordinate_label, (self.coordinate_label_x, self.coordinate_label_y))
        
        # 绘制"x="文字
        x_label = self.文本字体.render("x=", True, 文本颜色)
        self.屏幕.blit(x_label, (self.x_label_x, self.x_label_y))
        
        # 绘制x坐标输入框 - 增强视觉效果和交互反馈
        x_input_box_rect = pygame.Rect(self.x_input_box_x, self.x_input_box_y, self.input_box_width, self.input_box_height)
        is_x_input_hovered = x_input_box_rect.collidepoint(pygame.mouse.get_pos())
        
        if self.active_input == 'x':
            # 激活状态
            x_input_box_color = 输入框激活色
            border_color = 强调色
            border_width = 2
        elif is_x_input_hovered:
            # 悬停状态
            x_input_box_color = 输入框背景色
            border_color = 按钮悬停色
            border_width = 1
        else:
            # 普通状态
            x_input_box_color = 输入框背景色
            border_color = 边框颜色
            border_width = 1
        
        pygame.draw.rect(self.屏幕, x_input_box_color, x_input_box_rect, border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, border_color, x_input_box_rect, border_width, border_radius=self.元素圆角半径)
        
        # 显示输入文本 - 添加轻微阴影
        x_input_text = self.输入框字体.render(self.x_input_text, True, 文本颜色)
        shadow_text = self.输入框字体.render(self.x_input_text, True, (0, 0, 0, 50))
        text_rect = x_input_text.get_rect(center=x_input_box_rect.center)
        self.屏幕.blit(shadow_text, (text_rect.x + 1, text_rect.y + 1))
        self.屏幕.blit(x_input_text, text_rect)
        
        # 绘制"y="文字
        y_label = self.文本字体.render("y=", True, 文本颜色)
        self.屏幕.blit(y_label, (self.y_label_x, self.y_label_y))
        
        # 绘制y坐标输入框 - 与x输入框相同的效果
        y_input_box_rect = pygame.Rect(self.y_input_box_x, self.y_input_box_y, self.input_box_width, self.input_box_height)
        is_y_input_hovered = y_input_box_rect.collidepoint(pygame.mouse.get_pos())
        
        if self.active_input == 'y':
            y_input_box_color = 输入框激活色
            border_color = 强调色
            border_width = 2
        elif is_y_input_hovered:
            y_input_box_color = 输入框背景色
            border_color = 按钮悬停色
            border_width = 1
        else:
            y_input_box_color = 输入框背景色
            border_color = 边框颜色
            border_width = 1
        
        pygame.draw.rect(self.屏幕, y_input_box_color, y_input_box_rect, border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, border_color, y_input_box_rect, border_width, border_radius=self.元素圆角半径)
        
        y_input_text = self.输入框字体.render(self.y_input_text, True, 文本颜色)
        shadow_text = self.输入框字体.render(self.y_input_text, True, (0, 0, 0, 50))
        text_rect = y_input_text.get_rect(center=y_input_box_rect.center)
        self.屏幕.blit(shadow_text, (text_rect.x + 1, text_rect.y + 1))
        self.屏幕.blit(y_input_text, text_rect)
        
        # 绘制"确定传送"按钮 - 增强视觉反馈
        teleport_button_rect = pygame.Rect(self.teleport_button_x, self.teleport_button_y, self.teleport_button_width, self.teleport_button_height)
        is_teleport_hovered = teleport_button_rect.collidepoint(pygame.mouse.get_pos())
        
        if is_teleport_hovered:
            pygame.draw.rect(self.屏幕, 按钮悬停色, teleport_button_rect, border_radius=self.元素圆角半径)
            pygame.draw.rect(self.屏幕, 强调色, teleport_button_rect, 1, border_radius=self.元素圆角半径)
        else:
            pygame.draw.rect(self.屏幕, 次级背景色, teleport_button_rect, border_radius=self.元素圆角半径)
            pygame.draw.rect(self.屏幕, 边框颜色, teleport_button_rect, 1, border_radius=self.元素圆角半径)
        
        teleport_text = self.文本字体.render("确定传送", True, 标题颜色)
        shadow_text = self.文本字体.render("确定传送", True, (0, 0, 0, 60))
        text_rect = teleport_text.get_rect(center=teleport_button_rect.center)
        self.屏幕.blit(shadow_text, (text_rect.x + 1, text_rect.y + 1))
        self.屏幕.blit(teleport_text, text_rect)
        
        # 绘制玩家属性设置（在坐标修改下方）
        # 绘制玩家属性设置区域底UI背景（内底，比外底更浅）
        settings_bg_rect = pygame.Rect(self.player_settings_bg_x, self.player_settings_bg_y, self.player_settings_bg_width, self.player_settings_bg_height)
        内底颜色 = (45, 45, 48)  # 比外底主背景色更浅的灰色
        pygame.draw.rect(self.屏幕, (40, 40, 45, 30), settings_bg_rect.inflate(4, 4), border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, 内底颜色, settings_bg_rect, border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, settings_bg_rect, 1, border_radius=self.元素圆角半径)
        
        # 绘制通用输入框的函数（减少重复代码）
        def draw_input_field(label_text, label_x, label_y, input_box_x, input_box_y, input_text, is_active):
            # 绘制标签
            label = self.文本字体.render(label_text, True, 文本颜色)
            self.屏幕.blit(label, (label_x, label_y))
            
            # 绘制输入框
            input_box_rect = pygame.Rect(input_box_x, input_box_y, self.input_box_width, self.input_box_height)
            is_hovered = input_box_rect.collidepoint(pygame.mouse.get_pos())
            
            if is_active:
                bg_color = 输入框激活色
                border_color = 强调色
                border_width = 2
            elif is_hovered:
                bg_color = 输入框背景色
                border_color = 按钮悬停色
                border_width = 1
            else:
                bg_color = 输入框背景色
                border_color = 边框颜色
                border_width = 1
            
            pygame.draw.rect(self.屏幕, bg_color, input_box_rect, border_radius=self.元素圆角半径)
            pygame.draw.rect(self.屏幕, border_color, input_box_rect, border_width, border_radius=self.元素圆角半径)
            
            # 绘制输入文本
            text = self.输入框字体.render(input_text, True, 文本颜色)
            shadow = self.输入框字体.render(input_text, True, (0, 0, 0, 50))
            text_rect = text.get_rect(center=input_box_rect.center)
            self.屏幕.blit(shadow, (text_rect.x + 1, text_rect.y + 1))
            self.屏幕.blit(text, text_rect)
        
        # 使用函数绘制各个输入框
        draw_input_field("生命值:", self.health_label_x, self.health_label_y, 
                        self.health_input_box_x, self.health_input_box_y, 
                        self.health_input_text, self.active_input == 'health')
        
        draw_input_field("移动速度:", self.speed_label_x, self.speed_label_y, 
                        self.speed_input_box_x, self.speed_input_box_y, 
                        self.speed_input_text, self.active_input == 'speed')
        
        draw_input_field("跳跃力:", self.jump_label_x, self.jump_label_y, 
                        self.jump_input_box_x, self.jump_input_box_y, 
                        self.jump_input_text, self.active_input == 'jump')
        
        draw_input_field("基础攻击力:", self.damage_label_x, self.damage_label_y, 
                        self.damage_input_box_x, self.damage_input_box_y, 
                        self.damage_input_text, self.active_input == 'damage')
        
        # 绘制Star相关输入框 - 新增功能
        draw_input_field("Star百分比:", self.star_percentage_label_x, self.star_percentage_label_y, 
                        self.star_percentage_input_box_x, self.star_percentage_input_box_y, 
                        self.star_percentage_input_text, self.active_input == 'star_percentage')
        
        draw_input_field("Star数量:", self.star_count_label_x, self.star_count_label_y, 
                        self.star_count_input_box_x, self.star_count_input_box_y, 
                        self.star_count_input_text, self.active_input == 'star_count')
        
        # 定义伤害输入框的矩形区域
        damage_input_box_rect = pygame.Rect(self.damage_input_box_x, self.damage_input_box_y, self.input_box_width, self.input_box_height)
        damage_input_text = self.输入框字体.render(self.damage_input_text, True, 文本颜色)
        text_rect = damage_input_text.get_rect(center=damage_input_box_rect.center)
        self.屏幕.blit(damage_input_text, text_rect)
        
        # 重力值
        gravity_label = self.文本字体.render("重力值:", True, 文本颜色)
        self.屏幕.blit(gravity_label, (self.gravity_label_x, self.gravity_label_y))
        
        gravity_input_box_rect = pygame.Rect(self.gravity_input_box_x, self.gravity_input_box_y, self.input_box_width, self.input_box_height)
        gravity_input_box_color = 输入框背景色 if self.active_input != 'gravity' else (60, 60, 60)
        pygame.draw.rect(self.屏幕, gravity_input_box_color, gravity_input_box_rect, border_radius=3)
        pygame.draw.rect(self.屏幕, 边框颜色, gravity_input_box_rect, 1, border_radius=3)
        
        gravity_input_text = self.输入框字体.render(self.gravity_input_text, True, 文本颜色)
        text_rect = gravity_input_text.get_rect(center=gravity_input_box_rect.center)
        self.屏幕.blit(gravity_input_text, text_rect)
        
        # 绘制重力值-0.1按钮（现在在左边）
        gravity_minus_rect = pygame.Rect(self.gravity_minus_button_x, self.gravity_minus_button_y, self.gravity_minus_button_width, self.gravity_minus_button_height)
        if gravity_minus_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.屏幕, 按钮悬停色, gravity_minus_rect, border_radius=3)
        else:
            pygame.draw.rect(self.屏幕, 次级背景色, gravity_minus_rect, border_radius=3)
        pygame.draw.rect(self.屏幕, 边框颜色, gravity_minus_rect, 1, border_radius=3)
        
        minus_text = self.文本字体.render("-0.1", True, 文本颜色)
        text_rect = minus_text.get_rect(center=gravity_minus_rect.center)
        self.屏幕.blit(minus_text, text_rect)
        
        # 绘制重力值+0.1按钮（现在在右边）
        gravity_plus_rect = pygame.Rect(self.gravity_plus_button_x, self.gravity_plus_button_y, self.gravity_plus_button_width, self.gravity_plus_button_height)
        if gravity_plus_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.屏幕, 按钮悬停色, gravity_plus_rect, border_radius=3)
        else:
            pygame.draw.rect(self.屏幕, 次级背景色, gravity_plus_rect, border_radius=3)
        pygame.draw.rect(self.屏幕, 边框颜色, gravity_plus_rect, 1, border_radius=3)
        
        plus_text = self.文本字体.render("+0.1", True, 文本颜色)
        text_rect = plus_text.get_rect(center=gravity_plus_rect.center)
        self.屏幕.blit(plus_text, text_rect)
        
        # 绘制"确定修改"按钮
        update_button_rect = pygame.Rect(self.update_button_x, self.update_button_y, self.update_button_width, self.update_button_height)
        
        # 检查鼠标是否悬停
        if update_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.屏幕, 按钮悬停色, update_button_rect, border_radius=3)
        else:
            pygame.draw.rect(self.屏幕, 次级背景色, update_button_rect, border_radius=3)
        
        pygame.draw.rect(self.屏幕, 边框颜色, update_button_rect, 1, border_radius=3)
        
        update_text = self.文本字体.render("确定修改", True, 文本颜色)
        text_rect = update_text.get_rect(center=update_button_rect.center)
        self.屏幕.blit(update_text, text_rect)
    
    def get_close_button_rect(self):
        """获取关闭按钮矩形区域"""
        button_width = 30
        button_height = 30
        button_x = self.底2_x + self.底2宽度 - 40
        button_y = self.底_y + 20
        return pygame.Rect(button_x, button_y, button_width, button_height)
    
    def draw_close_button(self):
        """绘制关闭按钮(X) - 优化视觉效果和交互反馈"""
        close_button_rect = self.get_close_button_rect()
        
        # 检查鼠标是否悬停
        is_hovered = close_button_rect.collidepoint(pygame.mouse.get_pos())
        
        # 根据悬停状态设置背景色和边框色
        if is_hovered:
            # 悬停状态 - 使用红色强调和发光效果
            pygame.draw.rect(self.屏幕, 强调色, close_button_rect, border_radius=self.元素圆角半径)
            pygame.draw.rect(self.屏幕, (255, 255, 255, 100), close_button_rect, 1, border_radius=self.元素圆角半径)
            line_color = 标题颜色
        else:
            # 普通状态 - 使用次级背景色
            pygame.draw.rect(self.屏幕, 次级背景色, close_button_rect, border_radius=self.元素圆角半径)
            pygame.draw.rect(self.屏幕, 边框颜色, close_button_rect, 1, border_radius=self.元素圆角半径)
            line_color = 文本颜色
        
        # 绘制关闭按钮的X符号
        x_center = close_button_rect.centerx
        y_center = close_button_rect.centery
        
        # 绘制两条斜线组成X，添加轻微的阴影效果
        pygame.draw.line(self.屏幕, (0, 0, 0, 100), 
                        (x_center - 6 + 1, y_center - 6 + 1), 
                        (x_center + 6 + 1, y_center + 6 + 1), 
                        2)
        pygame.draw.line(self.屏幕, (0, 0, 0, 100), 
                        (x_center + 6 + 1, y_center - 6 + 1), 
                        (x_center - 6 + 1, y_center + 6 + 1), 
                        2)
        
        # 绘制主要的X符号
        pygame.draw.line(self.屏幕, line_color, 
                        (x_center - 6, y_center - 6), 
                        (x_center + 6, y_center + 6), 
                        2)
        pygame.draw.line(self.屏幕, line_color, 
                        (x_center + 6, y_center - 6), 
                        (x_center - 6, y_center + 6), 
                        2)
    
    def handle_event(self, 事件):
        """处理事件"""
        if not self.is_open:
            return False
        
        # 处理鼠标点击事件
        if 事件.type == pygame.MOUSEBUTTONDOWN:
            return self.handle_mouse_click(事件)
        
        # 处理键盘输入事件（用于所有输入框）
        elif 事件.type == pygame.KEYDOWN and (self.is_input_active or self.active_input is not None):
            return self.handle_keyboard_input(事件)
        
        return False
    
    def _update_player_coordinates(self):
        """更新坐标输入框"""
        # 不再重置坐标值，保留当前设置的值
        pass  # 空操作，避免重置坐标
    
    def handle_mouse_click(self, 事件):
        """处理鼠标点击事件"""
        mx, my = 事件.pos
        
        # 检查关闭按钮点击
        close_button_rect = self.get_close_button_rect()
        if close_button_rect.collidepoint(mx, my):
            self.is_open = False
            self.active_input = None
            return True
        
        # 检查左侧分类按钮点击
        button_start_y = self.底_y + 70
        for i in range(len(self.categories)):
            button_y = button_start_y + i * (self.button_height + self.button_spacing)
            button_rect = pygame.Rect(
                self.底1_x + 15,
                button_y,
                self.button_width,
                self.button_height
            )
            if button_rect.collidepoint(mx, my):
                self.current_category = i
                # 切换分类时重置输入状态
                self.is_input_active = False
                self.input_text = self.world_time
                self.active_input = None
                return True
        
        # 如果当前是世界设置，处理时间设置相关点击
        if self.current_category == 0:
            # 检查输入框点击
            input_box_rect = pygame.Rect(self.input_box_x, self.input_box_y, self.input_box_width, self.input_box_height)
            if input_box_rect.collidepoint(mx, my):
                self.is_input_active = True
                self.active_input = None
                return True
            
            # 检查+1:00按钮点击
            plus_button_rect = pygame.Rect(self.plus_button_x, self.plus_button_y, self.time_button_width, self.time_button_height)
            if plus_button_rect.collidepoint(mx, my):
                self.adjust_time(1)
                return True
            
            # 检查-1:00按钮点击
            minus_button_rect = pygame.Rect(self.minus_button_x, self.minus_button_y, self.time_button_width, self.time_button_height)
            if minus_button_rect.collidepoint(mx, my):
                self.adjust_time(-1)
                return True
            
            # 检查时间更新系数输入框点击
            time_speed_input_box_rect = pygame.Rect(self.time_speed_input_box_x, self.time_speed_input_box_y, self.time_speed_input_box_width, self.time_speed_input_box_height)
            if time_speed_input_box_rect.collidepoint(mx, my):
                self.active_input = 'time_speed'
                return True
            
            # 检查时间更新系数-1按钮点击
            time_speed_minus_rect = pygame.Rect(self.time_speed_minus_button_x, self.time_speed_minus_button_y, self.time_speed_minus_button_width, self.time_speed_minus_button_height)
            if time_speed_minus_rect.collidepoint(mx, my):
                self.adjust_time_speed(-1)
                return True
            
            # 检查时间更新系数+1按钮点击
            time_speed_plus_rect = pygame.Rect(self.time_speed_plus_button_x, self.time_speed_plus_button_y, self.time_speed_plus_button_width, self.time_speed_plus_button_height)
            if time_speed_plus_rect.collidepoint(mx, my):
                self.adjust_time_speed(1)
                return True
            
            # 检查确定修改按钮点击
            confirm_button_rect = pygame.Rect(self.confirm_button_x, self.confirm_button_y, self.action_button_width, self.action_button_height)
            if confirm_button_rect.collidepoint(mx, my):
                self.confirm_changes()
                return True
            
            # 检查还原按钮点击
            reset_button_rect = pygame.Rect(self.reset_button_x, self.reset_button_y, self.action_button_width, self.action_button_height)
            if reset_button_rect.collidepoint(mx, my):
                self.reset_changes()
                return True
            
            # 点击其他地方，取消输入框激活
            self.is_input_active = False
            self.active_input = None
        # 如果当前是玩家设置，处理坐标设置相关点击
        elif self.current_category == 1:
            # 检查x坐标输入框点击
            x_input_box_rect = pygame.Rect(self.x_input_box_x, self.x_input_box_y, self.input_box_width, self.input_box_height)
            if x_input_box_rect.collidepoint(mx, my):
                self.active_input = 'x'
                return True
            
            # 检查y坐标输入框点击
            y_input_box_rect = pygame.Rect(self.y_input_box_x, self.y_input_box_y, self.input_box_width, self.input_box_height)
            if y_input_box_rect.collidepoint(mx, my):
                self.active_input = 'y'
                return True
            
            # 检查传送按钮点击
            teleport_button_rect = pygame.Rect(self.teleport_button_x, self.teleport_button_y, self.teleport_button_width, self.teleport_button_height)
            if teleport_button_rect.collidepoint(mx, my):
                self.teleport_player()
                return True
            
            # 检查生命值输入框点击
            health_input_box_rect = pygame.Rect(self.health_input_box_x, self.health_input_box_y, self.input_box_width, self.input_box_height)
            if health_input_box_rect.collidepoint(mx, my):
                self.active_input = 'health'
                return True
            
            # 检查移动速度输入框点击
            speed_input_box_rect = pygame.Rect(self.speed_input_box_x, self.speed_input_box_y, self.input_box_width, self.input_box_height)
            if speed_input_box_rect.collidepoint(mx, my):
                self.active_input = 'speed'
                return True
            
            # 检查跳跃力输入框点击
            jump_input_box_rect = pygame.Rect(self.jump_input_box_x, self.jump_input_box_y, self.input_box_width, self.input_box_height)
            if jump_input_box_rect.collidepoint(mx, my):
                self.active_input = 'jump'
                return True
            
            # 检查初始伤害输入框点击
            damage_input_box_rect = pygame.Rect(self.damage_input_box_x, self.damage_input_box_y, self.input_box_width, self.input_box_height)
            if damage_input_box_rect.collidepoint(mx, my):
                self.active_input = 'damage'
                return True
            
            # 检查重力值输入框点击
            gravity_input_box_rect = pygame.Rect(self.gravity_input_box_x, self.gravity_input_box_y, self.input_box_width, self.input_box_height)
            if gravity_input_box_rect.collidepoint(mx, my):
                self.active_input = 'gravity'
                return True
            
            # 检查Star百分比输入框点击 - 新增功能
            star_percentage_input_box_rect = pygame.Rect(self.star_percentage_input_box_x, self.star_percentage_input_box_y, self.input_box_width, self.input_box_height)
            if star_percentage_input_box_rect.collidepoint(mx, my):
                self.active_input = 'star_percentage'
                return True
            
            # 检查Star数量输入框点击 - 新增功能
            star_count_input_box_rect = pygame.Rect(self.star_count_input_box_x, self.star_count_input_box_y, self.input_box_width, self.input_box_height)
            if star_count_input_box_rect.collidepoint(mx, my):
                self.active_input = 'star_count'
                return True
            
            # 检查重力值-0.1按钮点击（现在在左边）
            gravity_minus_rect = pygame.Rect(self.gravity_minus_button_x, self.gravity_minus_button_y, self.gravity_minus_button_width, self.gravity_minus_button_height)
            if gravity_minus_rect.collidepoint(mx, my):
                try:
                    current_gravity = float(self.gravity_input_text)
                    new_gravity = max(0.0, round(current_gravity - 0.1, 1))  # 防止重力值小于0
                    self.gravity_input_text = str(new_gravity)
                    # 立即应用更改
                    if hasattr(self.game, '玩家') and hasattr(self.game.玩家, '重力值'):
                        self.game.玩家.重力值 = new_gravity
                        print(f"重力值已调整为: {new_gravity}")
                except:
                    self.gravity_input_text = "0.5"  # 默认值
                return True
            
            # 检查重力值+0.1按钮点击（现在在右边）
            gravity_plus_rect = pygame.Rect(self.gravity_plus_button_x, self.gravity_plus_button_y, self.gravity_plus_button_width, self.gravity_plus_button_height)
            if gravity_plus_rect.collidepoint(mx, my):
                try:
                    current_gravity = float(self.gravity_input_text)
                    new_gravity = round(current_gravity + 0.1, 1)
                    self.gravity_input_text = str(new_gravity)
                    # 立即应用更改
                    if hasattr(self.game, '玩家') and hasattr(self.game.玩家, '重力值'):
                        self.game.玩家.重力值 = new_gravity
                        print(f"重力值已调整为: {new_gravity}")
                except:
                    self.gravity_input_text = "0.5"  # 默认值
                return True
        
        # 如果当前是玩家权限，处理权限设置相关点击
        elif self.current_category == 2:
            # 权限选项起始位置
            option_start_y = self.底_y + 80
            option_spacing = 40
            
            # 权限选项列表
            permission_options = [
                ("秒挖掘（挖掘无时间限制）", "is_instant_dig"),
                ("最高权限（可挖掘基岩）", "has_max_permission"),
                ("3*3放置（快捷栏物品只减少1个）", "enable_3x3_place"),
                ("3*3范围挖掘", "enable_3x3_dig"),
                ("全屏点击任意位置挖掘放置", "enable_fullscreen_click"),
                ("开启飞行模式(按w上升,按s下降)", "enable_fly_mode")
            ]
            
            # 检查权限开关点击
            for i, (label, attr_name) in enumerate(permission_options):
                toggle_y = option_start_y + i * option_spacing - 5
                toggle_rect = pygame.Rect(self.底2_x + self.底2宽度 - 100, toggle_y, 80, 30)
                if toggle_rect.collidepoint(mx, my):
                    # 切换权限状态
                    current_value = getattr(self, attr_name)
                    new_value = not current_value
                    setattr(self, attr_name, new_value)
                    print(f"{label} 已切换为: {new_value}")
                    
                    # 立即将权限状态应用到游戏实例
                    if attr_name == 'enable_fly_mode' and hasattr(self.game, '玩家') and hasattr(self.game.玩家, 'fly_mode'):
                        setattr(self.game.玩家, 'fly_mode', new_value)
                    elif hasattr(self.game, attr_name):
                        setattr(self.game, attr_name, new_value)
                    return True
            
            # 检查应用按钮点击
            apply_button_rect = pygame.Rect(self.底2_x + self.底2宽度 // 2 - 100, self.底_y + self.底2高度 - 60, 200, 40)
            if apply_button_rect.collidepoint(mx, my):
                self._apply_permissions()
                return True
            
            # 检查确定修改按钮点击
            update_button_rect = pygame.Rect(self.update_button_x, self.update_button_y, self.update_button_width, self.update_button_height)
            if update_button_rect.collidepoint(mx, my):
                # 实现更新玩家属性的逻辑
                try:
                    if hasattr(self.game, '玩家'):
                        # 更新生命值 - 同时更新当前生命值和最大生命值
                        new_health = int(self.health_input_text)
                        # 先尝试更新当前生命值（使用正确的属性名）
                        if hasattr(self.game.玩家, 'current_health'):
                            self.game.玩家.current_health = new_health
                        # 更新本命生命值
                        if hasattr(self.game.玩家, 'base_max_health'):
                            self.game.玩家.base_max_health = new_health
                            # 重新计算总生命值
                            self.game.玩家.max_health = self.game.玩家.base_max_health + self.game.玩家.equipment_health + self.game.玩家.upgrade_health
                        elif hasattr(self.game.玩家, 'max_health'):
                            # 兼容旧版本，直接更新max_health
                            self.game.玩家.max_health = new_health
                        print(f"生命值已更新为: {new_health}")
                        # 更新移动速度
                        self.game.玩家.移动速度 = float(self.speed_input_text)
                        # 更新跳跃力（使用正确的属性名'跳跃力度'）
                        self.game.玩家.跳跃力度 = float(self.jump_input_text)
                        # 更新基础攻击力
                        self.game.玩家.base_attack = int(self.damage_input_text)
                        # 更新重力值
                        new_gravity = float(self.gravity_input_text)
                        new_gravity = max(0.1, new_gravity)  # 确保重力值不小于0.1
                        self.game.玩家.重力值 = new_gravity
                        print(f"重力值已更新为: {new_gravity}")
                        
                        # 更新Star百分比 - 新增功能
                        try:
                            new_star_percentage = float(self.star_percentage_input_text)
                            # 确保百分比在0-100之间
                            new_star_percentage = max(0, min(100, new_star_percentage))
                            # 根据玩家对象的属性设置正确的star进度
                            if hasattr(self.game.玩家, 'star_progress'):
                                self.game.玩家.star_progress = new_star_percentage / 100  # 转换为0-1范围
                                print(f"Star进度已更新为: {new_star_percentage}%")
                            elif hasattr(self.game.玩家, 'star_experience'):
                                self.game.玩家.star_experience = new_star_percentage
                                print(f"Star经验已更新为: {new_star_percentage}")
                        except:
                            print("Star百分比输入无效")
                        
                        # 更新Star数量 - 新增功能
                        try:
                            new_star_count = int(self.star_count_input_text)
                            # 确保数量非负
                            new_star_count = max(0, new_star_count)
                            # 根据玩家对象的属性设置正确的star数量
                            if hasattr(self.game.玩家, 'star_count'):
                                self.game.玩家.star_count = new_star_count
                                print(f"Star数量已更新为: {new_star_count}")
                            elif hasattr(self.game.玩家, 'stars'):
                                self.game.玩家.stars = new_star_count
                                print(f"Star数量已更新为: {new_star_count}")
                        except:
                            print("Star数量输入无效")
                        
                        print("玩家属性已更新")
                except Exception as e:
                    print(f"更新玩家属性时出错: {e}")
                return True
            
            # 点击其他地方，取消输入框激活
            self.active_input = None
        

        
        # 移除点击页面外部关闭页面的逻辑，玩家需要通过关闭按钮或ESC键关闭页面
        
        return False
    
    def teleport_player(self):
        """将玩家传送到指定坐标"""
        try:
            # 解析输入的坐标（用户输入的是方块坐标）
            block_x = int(self.x_input_text)
            block_y = int(self.y_input_text)
            
            # 将方块坐标转换为像素坐标
            block_size = 32
            target_x = block_x * block_size
            target_y = block_y * block_size
            
            # 检查是否有玩家对象（使用正确的中文属性名）
            if hasattr(self.game, '玩家'):
                # 设置玩家坐标
                self.game.玩家.坐标_x = target_x
                self.game.玩家.坐标_y = target_y
                
                # 如果游戏有相机，更新相机位置
                if hasattr(self.game, 'camera_x') and hasattr(self.game, 'camera_y'):
                    # 将相机中心对准玩家
                    self.game.camera_x = target_x - self.屏幕宽度 // 2
                    self.game.camera_y = target_y - self.屏幕高度 // 2
                
                print(f"玩家已传送到方块坐标: ({block_x}, {block_y})，像素坐标: ({target_x}, {target_y})")
        except ValueError:
            # 输入无效，不执行传送
            print("坐标输入无效，无法传送")
    
    def handle_keyboard_input(self, 事件):
        """处理键盘输入"""
        # 处理时间输入
        if self.is_input_active:
            if 事件.key == pygame.K_RETURN:
                # 确认输入
                if self.validate_time_input(self.input_text):
                    self.world_time = self.input_text
                else:
                    # 输入无效，恢复原时间
                    self.input_text = self.world_time
                self.is_input_active = False
            elif 事件.key == pygame.K_ESCAPE:
                # 取消输入
                self.input_text = self.world_time
                self.is_input_active = False
            elif 事件.key == pygame.K_BACKSPACE:
                # 删除字符
                self.input_text = self.input_text[:-1]
            else:
                # 只允许输入数字和冒号
                if 事件.unicode.isdigit() or 事件.unicode == ':' :
                    # 限制输入长度
                    if len(self.input_text) < 5:
                        self.input_text += 事件.unicode
                        # 自动添加冒号（在第二个字符后）
                        if len(self.input_text) == 2 and ':' not in self.input_text:
                            self.input_text += ':'
        # 处理坐标输入
        elif self.active_input == 'x':
            if 事件.key == pygame.K_RETURN or 事件.key == pygame.K_TAB:
                # 确认输入或切换到y输入框 - 参考生命值输入框的处理方式，完全保留用户输入值
                # 不执行任何重置操作，直接切换输入框状态
                self.active_input = None if 事件.key == pygame.K_RETURN else 'y'
            elif 事件.key == pygame.K_ESCAPE:
                # 取消输入
                # 不再调用_update_player_coordinates，避免重置为0
                self.active_input = None
            elif 事件.key == pygame.K_BACKSPACE:
                # 删除字符，如果删除后为空则设为0
                self.x_input_text = self.x_input_text[:-1]
                if not self.x_input_text:
                    self.x_input_text = '0'
            # 处理负号输入
            elif 事件.key == pygame.K_MINUS and self.x_input_text == '0':
                self.x_input_text = '-'  
            # 处理数字输入（参考设置.py的方式）
            elif pygame.K_0 <= 事件.key <= pygame.K_9:
                数字 = 事件.key - pygame.K_0
                # 如果当前是0，输入数字时替换0
                if self.x_input_text == '0':
                    self.x_input_text = str(数字)
                else:
                    self.x_input_text += str(数字)
                # 移除开头的0（除非是单独的0）
                if len(self.x_input_text) > 1 and self.x_input_text[0] == '0' and self.x_input_text[1] != '-':
                    self.x_input_text = self.x_input_text.lstrip('0')
                    if not self.x_input_text:
                        self.x_input_text = '0'
        elif self.active_input == 'y':
            if 事件.key == pygame.K_RETURN or 事件.key == pygame.K_TAB:
                # 确认输入或切换到x输入框 - 参考生命值输入框的处理方式，完全保留用户输入值
                # 不执行任何重置操作，直接切换输入框状态
                self.active_input = None if 事件.key == pygame.K_RETURN else 'x'
            elif 事件.key == pygame.K_ESCAPE:
                # 取消输入
                # 不再调用_update_player_coordinates，避免重置为0
                self.active_input = None
            elif 事件.key == pygame.K_BACKSPACE:
                # 删除字符，如果删除后为空则设为0
                self.y_input_text = self.y_input_text[:-1]
                if not self.y_input_text:
                    self.y_input_text = '0'
            # 处理负号输入
            elif 事件.key == pygame.K_MINUS and self.y_input_text == '0':
                self.y_input_text = '-'
            # 处理数字输入（参考设置.py的方式）
            elif pygame.K_0 <= 事件.key <= pygame.K_9:
                数字 = 事件.key - pygame.K_0
                # 如果当前是0，输入数字时替换0
                if self.y_input_text == '0':
                    self.y_input_text = str(数字)
                else:
                    self.y_input_text += str(数字)
                # 移除开头的0（除非是单独的0）
                if len(self.y_input_text) > 1 and self.y_input_text[0] == '0' and self.y_input_text[1] != '-':
                    self.y_input_text = self.y_input_text.lstrip('0')
                    if not self.y_input_text:
                        self.y_input_text = '0'
        # 处理玩家属性输入框
        elif self.active_input == 'health':
            if 事件.key == pygame.K_RETURN:
                # 自动应用生命值修改 - 同时更新当前生命值和最大生命值
                try:
                    if hasattr(self.game, '玩家'):
                        new_health = int(self.health_input_text)
                        # 先尝试更新当前生命值（使用正确的属性名）
                        if hasattr(self.game.玩家, 'current_health'):
                            self.game.玩家.current_health = new_health
                        # 如果存在单独的最大生命值属性也更新（使用正确的属性名）
                        if hasattr(self.game.玩家, 'max_health'):
                            self.game.玩家.max_health = new_health
                    print(f"生命值已更新为: {new_health}")
                except Exception as e:
                    print(f"更新生命值时出错: {e}")
                self.active_input = None
            elif 事件.key == pygame.K_ESCAPE:
                self.active_input = None
            elif 事件.key == pygame.K_BACKSPACE:
                self.health_input_text = self.health_input_text[:-1]
                if not self.health_input_text:
                    self.health_input_text = '0'
            elif pygame.K_0 <= 事件.key <= pygame.K_9:
                数字 = 事件.key - pygame.K_0
                if self.health_input_text == '0':
                    self.health_input_text = str(数字)
                else:
                    self.health_input_text += str(数字)
        elif self.active_input == 'speed':
            if 事件.key == pygame.K_RETURN:
                # 自动应用移动速度修改
                try:
                    if hasattr(self.game, '玩家'):
                        self.game.玩家.移动速度 = float(self.speed_input_text)
                        print(f"移动速度已更新为: {self.speed_input_text}")
                except Exception as e:
                    print(f"更新移动速度时出错: {e}")
                self.active_input = None
            elif 事件.key == pygame.K_ESCAPE:
                self.active_input = None
            elif 事件.key == pygame.K_BACKSPACE:
                self.speed_input_text = self.speed_input_text[:-1]
                if not self.speed_input_text:
                    self.speed_input_text = '0'
            elif 事件.key == pygame.K_PERIOD and '.' not in self.speed_input_text:
                self.speed_input_text += '.'
            elif pygame.K_0 <= 事件.key <= pygame.K_9:
                数字 = 事件.key - pygame.K_0
                if self.speed_input_text == '0':
                    self.speed_input_text = str(数字)
                else:
                    self.speed_input_text += str(数字)
        elif self.active_input == 'jump':
            if 事件.key == pygame.K_RETURN:
                # 自动应用跳跃力修改
                try:
                    if hasattr(self.game, '玩家'):
                        self.game.玩家.跳跃力度 = float(self.jump_input_text)
                        print(f"跳跃力度已更新为: {self.jump_input_text}")
                except Exception as e:
                    print(f"更新跳跃力时出错: {e}")
                self.active_input = None
            elif 事件.key == pygame.K_ESCAPE:
                self.active_input = None
            elif 事件.key == pygame.K_BACKSPACE:
                self.jump_input_text = self.jump_input_text[:-1]
                if not self.jump_input_text:
                    self.jump_input_text = '0'
            elif 事件.key == pygame.K_PERIOD and '.' not in self.jump_input_text:
                self.jump_input_text += '.'
            elif pygame.K_0 <= 事件.key <= pygame.K_9:
                数字 = 事件.key - pygame.K_0
                if self.jump_input_text == '0':
                    self.jump_input_text = str(数字)
                else:
                    self.jump_input_text += str(数字)
        elif self.active_input == 'damage':
            if 事件.key == pygame.K_RETURN:
                # 自动应用基础攻击力修改
                try:
                    if hasattr(self.game, '玩家'):
                        self.game.玩家.base_attack = int(self.damage_input_text)
                        print(f"基础攻击力已更新为: {self.damage_input_text}")
                except Exception as e:
                    print(f"更新基础攻击力时出错: {e}")
                self.active_input = None
            elif 事件.key == pygame.K_ESCAPE:
                self.active_input = None
            elif 事件.key == pygame.K_BACKSPACE:
                self.damage_input_text = self.damage_input_text[:-1]
                if not self.damage_input_text:
                    self.damage_input_text = '0'
            elif pygame.K_0 <= 事件.key <= pygame.K_9:
                数字 = 事件.key - pygame.K_0
                if self.damage_input_text == '0':
                    self.damage_input_text = str(数字)
                else:
                    self.damage_input_text += str(数字)
        elif self.active_input == 'gravity':
            if 事件.key == pygame.K_RETURN:
                # 自动应用重力值修改
                try:
                    if hasattr(self.game, '玩家'):
                        new_gravity = float(self.gravity_input_text)
                        new_gravity = max(0.1, new_gravity)  # 确保重力值不小于0.1
                        self.game.玩家.重力值 = new_gravity
                        print(f"重力值已更新为: {new_gravity}")
                except Exception as e:
                    print(f"更新重力值时出错: {e}")
                self.active_input = None
            elif 事件.key == pygame.K_ESCAPE:
                self.active_input = None
            elif 事件.key == pygame.K_BACKSPACE:
                self.gravity_input_text = self.gravity_input_text[:-1]
                if not self.gravity_input_text:
                    self.gravity_input_text = '0'
            elif 事件.key == pygame.K_MINUS and self.gravity_input_text == '0':
                self.gravity_input_text = '-'
            elif 事件.key == pygame.K_PERIOD and '.' not in self.gravity_input_text:
                self.gravity_input_text += '.'
            elif pygame.K_0 <= 事件.key <= pygame.K_9:
                数字 = 事件.key - pygame.K_0
                if self.gravity_input_text == '0':
                    self.gravity_input_text = str(数字)
                else:
                    self.gravity_input_text += str(数字)
        # 处理Star百分比输入 - 新增功能
        elif self.active_input == 'star_percentage':
            if 事件.key == pygame.K_RETURN:
                # 自动应用Star百分比修改
                try:
                    new_star_percentage = float(self.star_percentage_input_text)
                    # 确保百分比在0-100之间
                    new_star_percentage = max(0, min(100, new_star_percentage))
                    # 根据玩家对象的属性设置正确的star进度
                    if hasattr(self.game, '玩家'):
                        if hasattr(self.game.玩家, 'star_progress'):
                            self.game.玩家.star_progress = new_star_percentage / 100  # 转换为0-1范围
                            print(f"Star进度已更新为: {new_star_percentage}%")
                        elif hasattr(self.game.玩家, 'star_experience'):
                            self.game.玩家.star_experience = new_star_percentage
                            print(f"Star经验已更新为: {new_star_percentage}")
                except Exception as e:
                    print(f"更新Star百分比时出错: {e}")
                self.active_input = None
            elif 事件.key == pygame.K_ESCAPE:
                self.active_input = None
            elif 事件.key == pygame.K_BACKSPACE:
                self.star_percentage_input_text = self.star_percentage_input_text[:-1]
                if not self.star_percentage_input_text:
                    self.star_percentage_input_text = '0'
            elif 事件.key == pygame.K_PERIOD and '.' not in self.star_percentage_input_text:
                self.star_percentage_input_text += '.'
            elif pygame.K_0 <= 事件.key <= pygame.K_9:
                数字 = 事件.key - pygame.K_0
                if self.star_percentage_input_text == '0':
                    self.star_percentage_input_text = str(数字)
                else:
                    self.star_percentage_input_text += str(数字)
        # 处理Star数量输入 - 新增功能
        elif self.active_input == 'star_count':
            if 事件.key == pygame.K_RETURN:
                # 自动应用Star数量修改
                try:
                    if hasattr(self.game, '玩家'):
                        new_star_count = int(self.star_count_input_text)
                        # 确保数量非负
                        new_star_count = max(0, new_star_count)
                        # 根据玩家对象的属性设置正确的star数量
                        if hasattr(self.game.玩家, 'star_count'):
                            self.game.玩家.star_count = new_star_count
                            print(f"Star数量已更新为: {new_star_count}")
                        elif hasattr(self.game.玩家, 'stars'):
                            self.game.玩家.stars = new_star_count
                            print(f"Star数量已更新为: {new_star_count}")
                except Exception as e:
                    print(f"更新Star数量时出错: {e}")
                self.active_input = None
            elif 事件.key == pygame.K_ESCAPE:
                self.active_input = None
            elif 事件.key == pygame.K_BACKSPACE:
                self.star_count_input_text = self.star_count_input_text[:-1]
                if not self.star_count_input_text:
                    self.star_count_input_text = '0'
            elif pygame.K_0 <= 事件.key <= pygame.K_9:
                数字 = 事件.key - pygame.K_0
                if self.star_count_input_text == '0':
                    self.star_count_input_text = str(数字)
                else:
                    self.star_count_input_text += str(数字)
        # 处理时间更新系数输入
        elif self.active_input == 'time_speed':
            if 事件.key == pygame.K_RETURN:
                # 自动应用时间更新系数修改
                try:
                    new_speed = int(self.time_speed_input_text)
                    # 确保最小为1
                    new_speed = max(1, new_speed)
                    self.time_speed_input_text = str(new_speed)
                    self.apply_time_speed_change(new_speed)
                except Exception as e:
                    print(f"更新时间更新系数时出错: {e}")
                self.active_input = None
            elif 事件.key == pygame.K_ESCAPE:
                self.active_input = None
            elif 事件.key == pygame.K_BACKSPACE:
                self.time_speed_input_text = self.time_speed_input_text[:-1]
                if not self.time_speed_input_text:
                    self.time_speed_input_text = '1'
            elif pygame.K_0 <= 事件.key <= pygame.K_9:
                数字 = 事件.key - pygame.K_0
                if self.time_speed_input_text == '1':
                    self.time_speed_input_text = str(数字)
                else:
                    self.time_speed_input_text += str(数字)
        
        return True
    
    def validate_time_input(self, time_str):
        """验证时间输入格式是否正确"""
        # 简单验证：格式为HH:MM，小时00-23，分钟00-59
        if len(time_str) != 5 or time_str[2] != ':':
            return False
        
        try:
            hours = int(time_str[:2])
            minutes = int(time_str[3:])
            return 0 <= hours <= 23 and 0 <= minutes <= 59
        except ValueError:
            return False
    
    def adjust_time(self, hours_delta):
        """调整时间（增加或减少指定小时数）"""
        # 解析当前时间
        hours, minutes = map(int, self.world_time.split(':'))
        
        # 调整小时数
        hours += hours_delta
        
        # 确保时间在0-23小时范围内
        hours %= 24
        
        # 格式化新时间
        self.world_time = f"{hours:02d}:{minutes:02d}"
        self.input_text = self.world_time
        
        # 实际设置游戏世界时间
        # 优先使用传入的world对象
        if hasattr(self, 'world') and self.world is not None and hasattr(self.world, '时间_of_day'):
            # 转换为游戏内部时间格式 (100 = 1小时)
            self.world.时间_of_day = hours * 100 + (minutes * 100 / 60)
            print(f"世界时间已调整为: {self.world_time}")
        # 尝试从游戏实例获取
        elif hasattr(self.game, '世界') and hasattr(self.game.世界, '时间_of_day'):
            self.game.世界.时间_of_day = hours * 100 + (minutes * 100 / 60)
            print(f"世界时间已调整为: {self.world_time}")
    
    def adjust_time_speed(self, delta):
        """调整时间更新系数（增加或减少指定值）"""
        try:
            # 获取当前时间更新系数
            current_speed = int(self.time_speed_input_text)
            # 调整系数，确保最小为1
            new_speed = max(1, current_speed + delta)
            self.time_speed_input_text = str(new_speed)
            # 应用更改
            self.apply_time_speed_change(new_speed)
        except:
            # 如果出错，设置默认值
            self.time_speed_input_text = "10"
            self.apply_time_speed_change(10)
    
    def apply_time_speed_change(self, new_speed):
        """应用时间更新系数更改到游戏中"""
        # 尝试更新游玩.py中的时间更新系数
        if hasattr(self.game, '世界') and hasattr(self.game.世界, '时间更新系数'):
            self.game.世界.时间更新系数 = new_speed
            print(f"时间更新系数已调整为: {new_speed}")
        elif hasattr(self, 'world') and self.world is not None and hasattr(self.world, '时间更新系数'):
            self.world.时间更新系数 = new_speed
            print(f"时间更新系数已调整为: {new_speed}")
        else:
            print(f"无法应用时间更新系数 {new_speed}，游戏对象中未找到相关属性")
    
    def confirm_changes(self):
        """确认所有修改并应用到游戏中"""
        print("确认所有修改...")
        
        # 应用时间更新系数
        try:
            new_speed = int(self.time_speed_input_text)
            new_speed = max(1, new_speed)  # 确保最小为1
            self.apply_time_speed_change(new_speed)
        except Exception as e:
            print(f"确认时间更新系数时出错: {e}")
        
        # 应用时间设置
        try:
            if self.validate_time_input(self.input_text):
                # 解析时间
                hours, minutes = map(int, self.input_text.split(':'))
                # 更新世界时间
                if hasattr(self, 'world') and self.world is not None and hasattr(self.world, '时间_of_day'):
                    self.world.时间_of_day = hours * 100 + (minutes * 100 / 60)
                    print(f"确认世界时间设置为: {self.input_text}")
                elif hasattr(self.game, '世界') and hasattr(self.game.世界, '时间_of_day'):
                    self.game.世界.时间_of_day = hours * 100 + (minutes * 100 / 60)
                    print(f"确认世界时间设置为: {self.input_text}")
        except Exception as e:
            print(f"确认时间设置时出错: {e}")
        
        # 应用玩家属性修改
        try:
            if hasattr(self.game, '玩家'):
                player = self.game.玩家
                
                # 应用重力值修改
                try:
                    new_gravity = float(self.gravity_input_text)
                    new_gravity = max(0.1, new_gravity)  # 确保最小为0.1
                    player.重力值 = new_gravity
                    print(f"重力值已更新为: {new_gravity}")
                except Exception as e:
                    print(f"更新重力值时出错: {e}")
                
                # 应用生命值修改
                try:
                    new_health = int(self.health_input_text)
                    new_health = max(1, new_health)  # 确保至少为1
                    if hasattr(player, 'current_health'):
                        player.current_health = new_health
                    elif hasattr(player, 'max_health'):
                        player.max_health = new_health
                    print(f"生命值已更新为: {new_health}")
                except Exception as e:
                    print(f"更新生命值时出错: {e}")
                
                # 应用移动速度修改
                try:
                    new_speed = float(self.speed_input_text)
                    new_speed = max(0.1, new_speed)  # 确保最小为0.1
                    if hasattr(player, '移动速度'):
                        player.移动速度 = new_speed
                        print(f"移动速度已更新为: {new_speed}")
                except Exception as e:
                    print(f"更新移动速度时出错: {e}")
                
                # 应用跳跃力修改
                try:
                    new_jump = float(self.jump_input_text)
                    new_jump = max(0.1, new_jump)  # 确保最小为0.1
                    if hasattr(player, '跳跃力度'):
                        player.跳跃力度 = new_jump
                        print(f"跳跃力度已更新为: {new_jump}")
                except Exception as e:
                    print(f"更新跳跃力时出错: {e}")
                
                # 应用初始伤害修改
                try:
                    new_damage = int(self.damage_input_text)
                    new_damage = max(1, new_damage)  # 确保至少为1
                    if hasattr(player, '初始伤害'):
                        player.初始伤害 = new_damage
                        print(f"初始伤害已更新为: {new_damage}")
                except Exception as e:
                    print(f"更新初始伤害时出错: {e}")
        except Exception as e:
            print(f"应用玩家属性修改时出错: {e}")
        
        print("所有修改已确认并应用")
    
    def reset_changes(self):
        """还原所有设置为当前游戏值"""
        print("还原所有设置...")
        
        # 重置时间更新系数为默认值10
        self.time_speed_input_text = "10"
        
        # 重置时间为当前游戏时间
        if hasattr(self, 'world') and self.world is not None and hasattr(self.world, '时间_of_day'):
            current_time = self.world.时间_of_day
        elif hasattr(self.game, '世界') and hasattr(self.game.世界, '时间_of_day'):
            current_time = self.game.世界.时间_of_day
        else:
            current_time = 0
        
        # 转换游戏时间格式为显示格式
        hours = int(current_time // 100)
        minutes = int((current_time % 100) * 0.6)  # 100个单位 = 60分钟
        self.world_time = f"{hours:02d}:{minutes:02d}"
        self.input_text = self.world_time
        
        print("所有设置已还原为当前游戏值")