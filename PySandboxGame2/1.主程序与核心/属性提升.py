import pygame
import time

# 现代深色主题配色方案
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

class 属性提升页面:
    """属性提升页面，包含属性提升和属性查询功能"""
    
    def __init__(self, game):
        self.game = game
        self.屏幕 = game.屏幕  # 从game实例获取屏幕对象
        self.is_open = False
        
        # 获取屏幕尺寸
        self.屏幕宽度 = self.屏幕.get_width()
        self.屏幕高度 = self.屏幕.get_height()
        
        # 状态显示相关变量
        self.show_status = False  # 是否显示状态信息
        self.status_text = ""  # 状态文本内容
        self.status_type = ""  # 状态类型："success" 或 "error"
        self.status_start_time = 0  # 状态显示开始时间
        self.status_duration = 3  # 状态显示持续时间（秒）
        self.blink_timer = 0  # 闪烁计时器
        self.blink_interval = 0.3  # 闪烁间隔（秒）
        
        # 页面尺寸 - 参照F4页面的样式
        self.底1宽度 = 200  # 左侧面板宽度
        self.底1高度 = 700  # 左侧面板高度
        self.底2宽度 = 850  # 右侧面板宽度
        self.底2高度 = 700  # 右侧面板高度
        self.间隔 = 20      # 面板间隔
        
        # 计算居中位置
        self.底1_x = (self.屏幕宽度 - self.底1宽度 - self.间隔 - self.底2宽度) // 2
        self.底2_x = self.底1_x + self.底1宽度 + self.间隔
        self.底_y = (self.屏幕高度 - max(self.底1高度, self.底2高度)) // 2
        
        # 圆角半径优化
        self.圆角半径 = 12    # 主面板圆角
        self.元素圆角半径 = 6 # 按钮和输入框圆角
        self.小元素圆角半径 = 4 # 小型控件圆角
        
        # 字体设置优化
        self.标题字体 = pygame.font.SysFont("Microsoft YaHei", 24, True)
        self.文本字体 = pygame.font.SysFont("Microsoft YaHei", 16)
        self.输入框字体 = pygame.font.SysFont("Microsoft YaHei", 16, False)
        
        # 属性提升相关数据 - 生命值
        self.生命值升级次数 = 0  # 当前升级次数
        self.生命值最大升级次数 = 10  # 最大升级次数
        self.生命值每次提升量 = 10  # 每次提升的生命值上限
        self.当前生命值增加总量 = 0  # 当前总共增加的生命值
        
        # 属性提升相关数据 - 攻击力
        self.攻击力升级次数 = 0  # 当前升级次数
        self.攻击力最大升级次数 = 10  # 最大升级次数
        self.攻击力每次提升量 = 2  # 每次提升的攻击力
        self.当前攻击力增加总量 = 0  # 当前总共增加的攻击力
        
        # 属性提升相关数据 - 防御力
        self.防御力升级次数 = 0  # 当前升级次数
        self.防御力最大升级次数 = 10  # 最大升级次数
        self.防御力每次提升量 = 0.5  # 每次提升的防御力
        self.当前防御力增加总量 = 0  # 当前总共增加的防御力
        
        # 属性提升相关数据 - 移速
        self.移速升级次数 = 0  # 当前升级次数
        self.移速最大升级次数 = 10  # 最大升级次数
        self.移速每次提升量 = 0.3  # 每次提升的移速百分比
        self.当前移速增加总量 = 0  # 当前总共增加的移速百分比
        
        # 属性提升相关数据 - 跳跃力
        self.跳跃力升级次数 = 0  # 当前升级次数
        self.跳跃力最大升级次数 = 10  # 最大升级次数
        self.跳跃力每次提升量 = 0.18  # 每次提升的跳跃力数值
        self.当前跳跃力增加总量 = 0  # 当前总共增加的跳跃力数值
        
        # 属性提升相关数据 - 挖掘效率
        self.挖掘效率升级次数 = 0  # 当前升级次数
        self.挖掘效率最大升级次数 = 10  # 最大升级次数
        self.挖掘效率每次提升量 = 8  # 每次提升的挖掘效率百分比
        self.当前挖掘效率增加总量 = 0  # 当前总共增加的挖掘效率百分比
        

        
        # 初始化UI元素
        self._setup_ui_elements()
        self._setup_attribute_elements()
    
    def _setup_ui_elements(self):
        """设置UI元素，包括选项按钮等"""
        # 选项按钮设置
        self.选项按钮列表 = [
            {"text": "属性提升", "rect": pygame.Rect(0, 0, self.底1宽度 - 40, 40), "index": 0},
            {"text": "属性查询", "rect": pygame.Rect(0, 0, self.底1宽度 - 40, 40), "index": 1}
        ]
        
        # 设置按钮位置
        button_y_offset = 60  # 第一个按钮的Y轴偏移
        button_spacing = 10   # 按钮间距
        
        for i, button in enumerate(self.选项按钮列表):
            button["rect"].x = self.底1_x + 20
            button["rect"].y = self.底_y + button_y_offset + i * (button["rect"].height + button_spacing)
        
        # 当前选中的选项
        self.current_option = 0
    
    def _setup_attribute_elements(self):
        """设置属性提升相关的UI元素"""
        element_height = 60  # 元素高度
        element_spacing = 20  # 元素间距
        
        # 生命值提升元素的位置和尺寸
        element_y = self.底_y + 80  # 第一个元素Y位置
        
        # 主元素区域 - 宽度增加20像素
        self.生命值提升区域 = pygame.Rect(
            self.底2_x + 40,  # X位置
            element_y,  # Y位置
            self.底2宽度 - 60,  # 宽度（增加了20像素）
            element_height  # 高度
        )
        
        # 提升按钮
        self.生命值提升按钮 = pygame.Rect(
            self.底2_x + self.底2宽度 - 150,  # X位置
            element_y + 15,  # Y位置
            110,  # 宽度
            30  # 高度
        )
        
        # 攻击力提升元素的位置和尺寸
        element_y += element_height + element_spacing
        self.攻击力提升区域 = pygame.Rect(
            self.底2_x + 40,  # X位置
            element_y,  # Y位置
            self.底2宽度 - 60,  # 宽度
            element_height  # 高度
        )
        
        # 攻击力提升按钮
        self.攻击力提升按钮 = pygame.Rect(
            self.底2_x + self.底2宽度 - 150,  # X位置
            element_y + 15,  # Y位置
            110,  # 宽度
            30  # 高度
        )
        
        # 防御力提升元素的位置和尺寸
        element_y += element_height + element_spacing
        self.防御力提升区域 = pygame.Rect(
            self.底2_x + 40,  # X位置
            element_y,  # Y位置
            self.底2宽度 - 60,  # 宽度
            element_height  # 高度
        )
        
        # 防御力提升按钮
        self.防御力提升按钮 = pygame.Rect(
            self.底2_x + self.底2宽度 - 150,  # X位置
            element_y + 15,  # Y位置
            110,  # 宽度
            30  # 高度
        )
        
        # 移速提升元素的位置和尺寸
        element_y += element_height + element_spacing
        self.移速提升区域 = pygame.Rect(
            self.底2_x + 40,  # X位置
            element_y,  # Y位置
            self.底2宽度 - 60,  # 宽度
            element_height  # 高度
        )
        
        # 移速提升按钮
        self.移速提升按钮 = pygame.Rect(
            self.底2_x + self.底2宽度 - 150,  # X位置
            element_y + 15,  # Y位置
            110,  # 宽度
            30  # 高度
        )
        
        # 跳跃力提升元素的位置和尺寸
        element_y += element_height + element_spacing
        self.跳跃力提升区域 = pygame.Rect(
            self.底2_x + 40,  # X位置
            element_y,  # Y位置
            self.底2宽度 - 60,  # 宽度
            element_height  # 高度
        )
        
        # 跳跃力提升按钮
        self.跳跃力提升按钮 = pygame.Rect(
            self.底2_x + self.底2宽度 - 150,  # X位置
            element_y + 15,  # Y位置
            110,  # 宽度
            30  # 高度
        )
        
        # 挖掘效率提升元素的位置和尺寸
        element_y += element_height + element_spacing
        self.挖掘效率提升区域 = pygame.Rect(
            self.底2_x + 40,  # X位置
            element_y,  # Y位置
            self.底2宽度 - 60,  # 宽度
            element_height  # 高度
        )
        
        # 挖掘效率提升按钮
        self.挖掘效率提升按钮 = pygame.Rect(
            self.底2_x + self.底2宽度 - 150,  # X位置
            element_y + 15,  # Y位置
            110,  # 宽度
            30  # 高度
        )
        

    
    def _calculate_star_cost(self, upgrade_count, max_upgrades):
        """
        计算属性升级所需的Star数量
        规则：第一次10，第二次20，第三次30...每次递增10
        如果已达上限，返回"-"
        
        参数:
            upgrade_count: 当前升级次数
            max_upgrades: 最大升级次数
            
        返回:
            int: Star消耗数量，如果已达上限返回"-"
        """
        # 如果已达上限，返回"-"
        if upgrade_count >= max_upgrades:
            return "-"
        
        # 计算消耗：第一次10，第二次20，以此类推
        # 当前已升级upgrade_count次，下一次是第(upgrade_count + 1)次
        return (upgrade_count + 1) * 10

    def toggle(self):
        """切换页面的显示状态"""
        self.is_open = not self.is_open  # 修正变量名称

    def draw(self, 屏幕):
        """绘制属性提升页面"""
        if not self.is_open:
            return
        
        # 绘制左侧面板
        self._draw_panel(self.底1_x, self.底_y, self.底1宽度, self.底1高度)
        
        # 绘制右侧面板
        self._draw_panel(self.底2_x, self.底_y, self.底2宽度, self.底2高度)
        
        # 绘制标题
        self._draw_title()
        
        # 绘制选项按钮
        self._draw_option_buttons()
        
        # 绘制内容区域
        self._draw_content()
        
        # 绘制关闭按钮
        self._draw_close_button()
        
        # 绘制状态信息
        if self.show_status:
            self._draw_status_text()
    
    def _draw_panel(self, x, y, width, height):
        """绘制面板背景"""
        # 绘制主面板背景
        pygame.draw.rect(self.屏幕, 次级背景色, (x, y, width, height), border_radius=self.圆角半径)
        # 绘制边框
        pygame.draw.rect(self.屏幕, 边框颜色, (x, y, width, height), 2, border_radius=self.圆角半径)
    
    def _draw_title(self):
        """绘制页面标题"""
        # 左侧面板标题
        title_surf = self.标题字体.render("属性提升", True, 标题颜色)
        title_rect = title_surf.get_rect(center=(self.底1_x + self.底1宽度 // 2, self.底_y + 30))
        self.屏幕.blit(title_surf, title_rect)
    
    def _draw_option_buttons(self):
        """绘制选项按钮列表"""
        for button in self.选项按钮列表:
            # 确定按钮颜色
            if button["index"] == self.current_option:
                button_color = 高亮背景色
                text_color = 强调色
            else:
                button_color = 输入框背景色
                text_color = 文本颜色
            
            # 绘制按钮背景
            pygame.draw.rect(self.屏幕, button_color, button["rect"], border_radius=self.元素圆角半径)
            pygame.draw.rect(self.屏幕, 边框颜色, button["rect"], 1, border_radius=self.元素圆角半径)
            
            # 绘制按钮文本
            text_surf = self.文本字体.render(button["text"], True, text_color)
            text_rect = text_surf.get_rect(center=button["rect"].center)
            self.屏幕.blit(text_surf, text_rect)
    
    def _draw_content(self):
        """绘制主内容区域"""
        if self.current_option == 0:  # 属性提升选项
            # 当选中属性提升时，绘制所有属性提升元素
            self._draw_life_upgrade_element()
            self._draw_attack_upgrade_element()
            self._draw_defense_upgrade_element()
            self._draw_speed_upgrade_element()
            self._draw_jump_upgrade_element()
            self._draw_mining_upgrade_element()
            
            # 获取玩家对象中的Star数量，同时支持star_count和stars两种属性名
            player = getattr(self.game, '玩家', None)
            star_count = 0
            if player is not None:
                # 优先使用star_count属性，如果不存在则尝试使用stars属性
                if hasattr(player, 'star_count'):
                    star_count = player.star_count
                elif hasattr(player, 'stars'):
                    star_count = player.stars
            
            # 设置Star数量文本样式
            star_font = pygame.font.SysFont("Microsoft YaHei", 18, True)  # 18号加粗字体
            
            # 计算文本宽度和高度，以便添加内边距
            text_surface = star_font.render(f"star:{star_count}", True, 文本颜色)
            text_width = text_surface.get_width() + 20  # 添加左右各10像素内边距
            text_height = text_surface.get_height() + 10  # 添加上下各5像素内边距
            
            # 右下角位置
            star_x = self.底2_x + self.底2宽度 - text_width - 20  # 距离右侧20像素
            star_y = self.底_y + self.底2高度 - text_height - 20  # 距离底部20像素
            
            # 绘制背景矩形
            pygame.draw.rect(self.屏幕, 次级背景色, (star_x, star_y, text_width, text_height), border_radius=self.小元素圆角半径)
            # 添加边框
            pygame.draw.rect(self.屏幕, 边框颜色, (star_x, star_y, text_width, text_height), 2, border_radius=self.小元素圆角半径)
            
            # 绘制文本，居中显示
            text_x = star_x + (text_width - text_surface.get_width()) // 2
            text_y = star_y + (text_height - text_surface.get_height()) // 2
            self.屏幕.blit(text_surface, (text_x, text_y))
        else:  # 属性查询选项
            # 绘制属性查询内容
            self._draw_attribute_query()
    
    def _draw_attribute_query(self):
        """绘制属性查询内容，显示各项属性的详细来源"""
        # 获取玩家对象
        player = getattr(self.game, '玩家', None)
        if player is None:
            return
        
        # 获取背包管理器
        装备生命值 = 0
        装备攻击力 = 0
        装备防御力 = 0
        装备移速 = 0
        装备跳跃力 = 0
        
        if hasattr(self.game, '背包管理器'):
            背包管理器 = self.game.背包管理器
            # 计算装备总属性
            装备属性 = 背包管理器.计算装备总属性()
            装备生命值 = 装备属性.get('生命值', 0)
            装备攻击力 = 装备属性.get('攻击力', 0)
            装备防御力 = 装备属性.get('防御力', 0)
            装备移速 = 装备属性.get('移速', 0)
            装备跳跃力 = 装备属性.get('跳跃力', 0)
        
        # 初始化属性值
        # 生命值属性 - 直接从玩家对象获取
        total_health = getattr(player, 'max_health', 100)
        base_health = total_health - self.当前生命值增加总量 - 装备生命值
        upgrade_health = self.当前生命值增加总量
        equipment_health = 装备生命值
        
        # 攻击力属性 - 直接从玩家对象获取
        total_attack = 0
        if hasattr(player, 'base_attack'):
            total_attack = getattr(player, 'base_attack', 0)
        elif hasattr(player, 'attack'):
            total_attack = getattr(player, 'attack', 0)
        base_attack = total_attack - self.当前攻击力增加总量 - 装备攻击力
        upgrade_attack = self.当前攻击力增加总量
        equipment_attack = 装备攻击力
        
        # 防御力属性 - 直接从玩家对象获取
        total_defense = 0
        if hasattr(player, 'defense'):
            total_defense = getattr(player, 'defense', 0)
        elif hasattr(player, 'defense_value'):
            total_defense = getattr(player, 'defense_value', 0)
        base_defense = total_defense - self.当前防御力增加总量 - 装备防御力
        upgrade_defense = self.当前防御力增加总量
        equipment_defense = 装备防御力
        
        # 移速属性 - 直接从玩家对象获取
        base_speed = getattr(player, '移动速度', 5)
        total_speed = base_speed + self.当前移速增加总量 + 装备移速
        equipment_speed = 装备移速
        upgrade_speed = self.当前移速增加总量
        
        # 跳跃力属性 - 直接从玩家对象获取
        base_jump = getattr(player, '跳跃力度', -10)
        total_jump = base_jump + self.当前跳跃力增加总量 + 装备跳跃力
        equipment_jump = 装备跳跃力
        upgrade_jump = self.当前跳跃力增加总量
        
        # 挖掘效率属性
        base_mining = 100  # 默认基础挖掘效率为100%
        total_mining = base_mining + self.当前挖掘效率增加总量
        equipment_mining = 0  # 默认装备挖掘效率加成
        upgrade_mining = self.当前挖掘效率增加总量
        
        # 准备属性数据列表
        attribute_data = [
            {"name": "生命值", "total": total_health, "base": base_health, "equipment": equipment_health, "upgrade": upgrade_health, "unit": ""},
            {"name": "攻击力", "total": total_attack, "base": base_attack, "equipment": equipment_attack, "upgrade": upgrade_attack, "unit": ""},
            {"name": "防御力", "total": total_defense, "base": base_defense, "equipment": equipment_defense, "upgrade": upgrade_defense, "unit": ""},
            {"name": "移速", "total": total_speed, "base": base_speed, "equipment": equipment_speed, "upgrade": upgrade_speed, "unit": ""},
            {"name": "跳跃力", "total": total_jump, "base": base_jump, "equipment": equipment_jump, "upgrade": upgrade_jump, "unit": ""},
            {"name": "挖掘效率", "total": total_mining, "base": base_mining, "equipment": equipment_mining, "upgrade": upgrade_mining, "unit": "%"}
        ]
        
        # 绘制属性查询内容
        start_y = self.底_y + 80
        line_height = 60
        for i, attr in enumerate(attribute_data):
            # 计算当前行的Y坐标
            y = start_y + i * line_height
            
            # 绘制背景框
            attr_rect = pygame.Rect(self.底2_x + 40, y, self.底2宽度 - 60, 50)
            pygame.draw.rect(self.屏幕, 输入框背景色, attr_rect, border_radius=self.元素圆角半径)
            pygame.draw.rect(self.屏幕, 边框颜色, attr_rect, 1, border_radius=self.元素圆角半径)
            
            # 绘制属性名称
            name_text = self.文本字体.render(f"{attr['name']}: ", True, 标题颜色)
            name_x = attr_rect.x + 20
            name_y = attr_rect.y + (attr_rect.height - name_text.get_height()) // 2
            self.屏幕.blit(name_text, (name_x, name_y))
            
            # 绘制属性详细信息
            detail_text = f"总{attr['name']}: {attr['total']}{attr['unit']} | 本命{attr['name']}: {attr['base']}{attr['unit']} | 装备{attr['name']}: +{attr['equipment']}{attr['unit']} | 升级{attr['name']}: +{attr['upgrade']}{attr['unit']}"
            detail_surface = self.文本字体.render(detail_text, True, 文本颜色)
            detail_x = name_x + name_text.get_width() + 10
            detail_y = attr_rect.y + (attr_rect.height - detail_surface.get_height()) // 2
            self.屏幕.blit(detail_surface, (detail_x, detail_y))
    
    def _draw_life_upgrade_element(self):
        """绘制生命值提升元素（长方形包裹）"""
        # 绘制背景框
        pygame.draw.rect(self.屏幕, 输入框背景色, self.生命值提升区域, border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, self.生命值提升区域, 1, border_radius=self.元素圆角半径)
        
        # 计算各个元素的位置
        x_offset = self.生命值提升区域.x + 20
        y_center = self.生命值提升区域.y + self.生命值提升区域.height // 2
        
        # 1. 提升生命值标签
        label_surf = self.文本字体.render("提升生命值:", True, 文本颜色)
        label_rect = label_surf.get_rect(center=(x_offset + label_surf.get_width() // 2, y_center))
        self.屏幕.blit(label_surf, label_rect)
        
        # 2. 限制次数
        x_offset += label_surf.get_width() + 40
        times_text = f"限制次数({self.生命值升级次数}/{self.生命值最大升级次数})"
        times_surf = self.文本字体.render(times_text, True, 文本颜色)
        times_rect = times_surf.get_rect(center=(x_offset + times_surf.get_width() // 2, y_center))
        self.屏幕.blit(times_surf, times_rect)
        
        # 3. 消耗星星
        x_offset += times_surf.get_width() + 40
        # 使用问号代替星星，实际应用中可以替换为星星图像
        star_cost = self._calculate_star_cost(self.生命值升级次数, self.生命值最大升级次数)
        cost_text = f"消耗: {star_cost}"
        cost_surf = self.文本字体.render(cost_text, True, 文本颜色)
        cost_rect = cost_surf.get_rect(center=(x_offset + cost_surf.get_width() // 2, y_center))
        self.屏幕.blit(cost_surf, cost_rect)
        
        # 4. 提升效果
        x_offset += cost_surf.get_width() + 40
        effect_text = f"提升效果:+{self.生命值每次提升量}"
        effect_surf = self.文本字体.render(effect_text, True, 文本颜色)
        effect_rect = effect_surf.get_rect(center=(x_offset + effect_surf.get_width() // 2, y_center))
        self.屏幕.blit(effect_surf, effect_rect)
        
        # 5. 当前增加
        x_offset += effect_surf.get_width() + 40
        current_text = f"当前增加:{self.当前生命值增加总量}"
        current_surf = self.文本字体.render(current_text, True, 文本颜色)
        current_rect = current_surf.get_rect(center=(x_offset + current_surf.get_width() // 2, y_center))
        self.屏幕.blit(current_surf, current_rect)
        
        # 6. 提升按钮
        # 确定按钮状态和颜色
        can_upgrade = self.生命值升级次数 < self.生命值最大升级次数
        button_color = 按钮悬停色 if can_upgrade else 输入框背景色
        text_color = 文本颜色 if can_upgrade else (120, 120, 120)  # 灰色表示禁用
        
        # 绘制按钮
        pygame.draw.rect(self.屏幕, button_color, self.生命值提升按钮, border_radius=self.小元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, self.生命值提升按钮, 1, border_radius=self.小元素圆角半径)
        
        # 绘制按钮文本
        button_text = "提升" if can_upgrade else "已达上限"
        button_text_surf = self.文本字体.render(button_text, True, text_color)
        button_text_rect = button_text_surf.get_rect(center=self.生命值提升按钮.center)
        self.屏幕.blit(button_text_surf, button_text_rect)
    
    def _draw_attack_upgrade_element(self):
        """绘制攻击力提升元素（长方形包裹）"""
        # 绘制背景框
        pygame.draw.rect(self.屏幕, 输入框背景色, self.攻击力提升区域, border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, self.攻击力提升区域, 1, border_radius=self.元素圆角半径)
        
        # 计算各个元素的位置
        x_offset = self.攻击力提升区域.x + 20
        y_center = self.攻击力提升区域.y + self.攻击力提升区域.height // 2
        
        # 1. 提升攻击力标签
        label_surf = self.文本字体.render("提升攻击力:", True, 文本颜色)
        label_rect = label_surf.get_rect(center=(x_offset + label_surf.get_width() // 2, y_center))
        self.屏幕.blit(label_surf, label_rect)
        
        # 2. 限制次数
        x_offset += label_surf.get_width() + 40
        times_text = f"限制次数({self.攻击力升级次数}/{self.攻击力最大升级次数})"
        times_surf = self.文本字体.render(times_text, True, 文本颜色)
        times_rect = times_surf.get_rect(center=(x_offset + times_surf.get_width() // 2, y_center))
        self.屏幕.blit(times_surf, times_rect)
        
        # 3. 消耗星星
        x_offset += times_surf.get_width() + 40
        star_cost = self._calculate_star_cost(self.攻击力升级次数, self.攻击力最大升级次数)
        cost_text = f"消耗: {star_cost}"
        cost_surf = self.文本字体.render(cost_text, True, 文本颜色)
        cost_rect = cost_surf.get_rect(center=(x_offset + cost_surf.get_width() // 2, y_center))
        self.屏幕.blit(cost_surf, cost_rect)
        
        # 4. 提升效果
        x_offset += cost_surf.get_width() + 40
        effect_text = f"提升效果:+{self.攻击力每次提升量}"
        effect_surf = self.文本字体.render(effect_text, True, 文本颜色)
        effect_rect = effect_surf.get_rect(center=(x_offset + effect_surf.get_width() // 2, y_center))
        self.屏幕.blit(effect_surf, effect_rect)
        
        # 5. 当前增加
        x_offset += effect_surf.get_width() + 40
        current_text = f"当前增加:{self.当前攻击力增加总量}"
        current_surf = self.文本字体.render(current_text, True, 文本颜色)
        current_rect = current_surf.get_rect(center=(x_offset + current_surf.get_width() // 2, y_center))
        self.屏幕.blit(current_surf, current_rect)
        
        # 6. 提升按钮
        can_upgrade = self.攻击力升级次数 < self.攻击力最大升级次数
        button_color = 按钮悬停色 if can_upgrade else 输入框背景色
        text_color = 文本颜色 if can_upgrade else (120, 120, 120)
        
        pygame.draw.rect(self.屏幕, button_color, self.攻击力提升按钮, border_radius=self.小元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, self.攻击力提升按钮, 1, border_radius=self.小元素圆角半径)
        
        button_text = "提升" if can_upgrade else "已达上限"
        button_text_surf = self.文本字体.render(button_text, True, text_color)
        button_text_rect = button_text_surf.get_rect(center=self.攻击力提升按钮.center)
        self.屏幕.blit(button_text_surf, button_text_rect)
    
    def _draw_defense_upgrade_element(self):
        """绘制防御力提升元素（长方形包裹）"""
        # 绘制背景框
        pygame.draw.rect(self.屏幕, 输入框背景色, self.防御力提升区域, border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, self.防御力提升区域, 1, border_radius=self.元素圆角半径)
        
        # 计算各个元素的位置
        x_offset = self.防御力提升区域.x + 20
        y_center = self.防御力提升区域.y + self.防御力提升区域.height // 2
        
        # 1. 提升防御力标签
        label_surf = self.文本字体.render("提升防御力:", True, 文本颜色)
        label_rect = label_surf.get_rect(center=(x_offset + label_surf.get_width() // 2, y_center))
        self.屏幕.blit(label_surf, label_rect)
        
        # 2. 限制次数
        x_offset += label_surf.get_width() + 40
        times_text = f"限制次数({self.防御力升级次数}/{self.防御力最大升级次数})"
        times_surf = self.文本字体.render(times_text, True, 文本颜色)
        times_rect = times_surf.get_rect(center=(x_offset + times_surf.get_width() // 2, y_center))
        self.屏幕.blit(times_surf, times_rect)
        
        # 3. 消耗星星
        x_offset += times_surf.get_width() + 40
        star_cost = self._calculate_star_cost(self.防御力升级次数, self.防御力最大升级次数)
        cost_text = f"消耗: {star_cost}"
        cost_surf = self.文本字体.render(cost_text, True, 文本颜色)
        cost_rect = cost_surf.get_rect(center=(x_offset + cost_surf.get_width() // 2, y_center))
        self.屏幕.blit(cost_surf, cost_rect)
        
        # 4. 提升效果
        x_offset += cost_surf.get_width() + 40
        effect_text = f"提升效果:+{self.防御力每次提升量}"
        effect_surf = self.文本字体.render(effect_text, True, 文本颜色)
        effect_rect = effect_surf.get_rect(center=(x_offset + effect_surf.get_width() // 2, y_center))
        self.屏幕.blit(effect_surf, effect_rect)
        
        # 5. 当前增加
        x_offset += effect_surf.get_width() + 40
        current_text = f"当前增加:{self.当前防御力增加总量}"
        current_surf = self.文本字体.render(current_text, True, 文本颜色)
        current_rect = current_surf.get_rect(center=(x_offset + current_surf.get_width() // 2, y_center))
        self.屏幕.blit(current_surf, current_rect)
        
        # 6. 提升按钮
        can_upgrade = self.防御力升级次数 < self.防御力最大升级次数
        button_color = 按钮悬停色 if can_upgrade else 输入框背景色
        text_color = 文本颜色 if can_upgrade else (120, 120, 120)
        
        pygame.draw.rect(self.屏幕, button_color, self.防御力提升按钮, border_radius=self.小元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, self.防御力提升按钮, 1, border_radius=self.小元素圆角半径)
        
        button_text = "提升" if can_upgrade else "已达上限"
        button_text_surf = self.文本字体.render(button_text, True, text_color)
        button_text_rect = button_text_surf.get_rect(center=self.防御力提升按钮.center)
        self.屏幕.blit(button_text_surf, button_text_rect)
    
    def _draw_speed_upgrade_element(self):
        """绘制移速提升元素（长方形包裹）"""
        # 绘制背景框
        pygame.draw.rect(self.屏幕, 输入框背景色, self.移速提升区域, border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, self.移速提升区域, 1, border_radius=self.元素圆角半径)
        
        # 计算各个元素的位置
        x_offset = self.移速提升区域.x + 20
        y_center = self.移速提升区域.y + self.移速提升区域.height // 2
        
        # 1. 提升移速标签
        label_surf = self.文本字体.render("提升移速:", True, 文本颜色)
        label_rect = label_surf.get_rect(center=(x_offset + label_surf.get_width() // 2, y_center))
        self.屏幕.blit(label_surf, label_rect)
        
        # 2. 限制次数
        x_offset += label_surf.get_width() + 40
        times_text = f"限制次数({self.移速升级次数}/{self.移速最大升级次数})"
        times_surf = self.文本字体.render(times_text, True, 文本颜色)
        times_rect = times_surf.get_rect(center=(x_offset + times_surf.get_width() // 2, y_center))
        self.屏幕.blit(times_surf, times_rect)
        
        # 3. 消耗星星
        x_offset += times_surf.get_width() + 40
        star_cost = self._calculate_star_cost(self.移速升级次数, self.移速最大升级次数)
        cost_text = f"消耗: {star_cost}"
        cost_surf = self.文本字体.render(cost_text, True, 文本颜色)
        cost_rect = cost_surf.get_rect(center=(x_offset + cost_surf.get_width() // 2, y_center))
        self.屏幕.blit(cost_surf, cost_rect)
        
        # 4. 提升效果
        x_offset += cost_surf.get_width() + 40
        effect_text = f"提升效果:+{self.移速每次提升量}"
        effect_surf = self.文本字体.render(effect_text, True, 文本颜色)
        effect_rect = effect_surf.get_rect(center=(x_offset + effect_surf.get_width() // 2, y_center))
        self.屏幕.blit(effect_surf, effect_rect)
        
        # 5. 当前增加
        x_offset += effect_surf.get_width() + 40
        current_text = f"当前增加:{self.当前移速增加总量}"
        current_surf = self.文本字体.render(current_text, True, 文本颜色)
        current_rect = current_surf.get_rect(center=(x_offset + current_surf.get_width() // 2, y_center))
        self.屏幕.blit(current_surf, current_rect)
        
        # 6. 提升按钮
        can_upgrade = self.移速升级次数 < self.移速最大升级次数
        button_color = 按钮悬停色 if can_upgrade else 输入框背景色
        text_color = 文本颜色 if can_upgrade else (120, 120, 120)
        
        pygame.draw.rect(self.屏幕, button_color, self.移速提升按钮, border_radius=self.小元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, self.移速提升按钮, 1, border_radius=self.小元素圆角半径)
        
        button_text = "提升" if can_upgrade else "已达上限"
        button_text_surf = self.文本字体.render(button_text, True, text_color)
        button_text_rect = button_text_surf.get_rect(center=self.移速提升按钮.center)
        self.屏幕.blit(button_text_surf, button_text_rect)
    
    def _draw_jump_upgrade_element(self):
        """绘制跳跃力提升元素（长方形包裹）"""
        # 绘制背景框
        pygame.draw.rect(self.屏幕, 输入框背景色, self.跳跃力提升区域, border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, self.跳跃力提升区域, 1, border_radius=self.元素圆角半径)
        
        # 计算各个元素的位置
        x_offset = self.跳跃力提升区域.x + 20
        y_center = self.跳跃力提升区域.y + self.跳跃力提升区域.height // 2
        
        # 1. 提升跳跃力标签
        label_surf = self.文本字体.render("提升跳跃力:", True, 文本颜色)
        label_rect = label_surf.get_rect(center=(x_offset + label_surf.get_width() // 2, y_center))
        self.屏幕.blit(label_surf, label_rect)
        
        # 2. 限制次数
        x_offset += label_surf.get_width() + 40
        times_text = f"限制次数({self.跳跃力升级次数}/{self.跳跃力最大升级次数})"
        times_surf = self.文本字体.render(times_text, True, 文本颜色)
        times_rect = times_surf.get_rect(center=(x_offset + times_surf.get_width() // 2, y_center))
        self.屏幕.blit(times_surf, times_rect)
        
        # 3. 消耗星星
        x_offset += times_surf.get_width() + 40
        star_cost = self._calculate_star_cost(self.跳跃力升级次数, self.跳跃力最大升级次数)
        cost_text = f"消耗: {star_cost}"
        cost_surf = self.文本字体.render(cost_text, True, 文本颜色)
        cost_rect = cost_surf.get_rect(center=(x_offset + cost_surf.get_width() // 2, y_center))
        self.屏幕.blit(cost_surf, cost_rect)
        
        # 4. 提升效果
        x_offset += cost_surf.get_width() + 40
        effect_text = f"提升效果:+{self.跳跃力每次提升量}"
        effect_surf = self.文本字体.render(effect_text, True, 文本颜色)
        effect_rect = effect_surf.get_rect(center=(x_offset + effect_surf.get_width() // 2, y_center))
        self.屏幕.blit(effect_surf, effect_rect)
        
        # 5. 当前增加
        x_offset += effect_surf.get_width() + 40
        current_text = f"当前增加:{self.当前跳跃力增加总量}"
        current_surf = self.文本字体.render(current_text, True, 文本颜色)
        current_rect = current_surf.get_rect(center=(x_offset + current_surf.get_width() // 2, y_center))
        self.屏幕.blit(current_surf, current_rect)
        
        # 6. 提升按钮
        can_upgrade = self.跳跃力升级次数 < self.跳跃力最大升级次数
        button_color = 按钮悬停色 if can_upgrade else 输入框背景色
        text_color = 文本颜色 if can_upgrade else (120, 120, 120)
        
        pygame.draw.rect(self.屏幕, button_color, self.跳跃力提升按钮, border_radius=self.小元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, self.跳跃力提升按钮, 1, border_radius=self.小元素圆角半径)
        
        button_text = "提升" if can_upgrade else "已达上限"
        button_text_surf = self.文本字体.render(button_text, True, text_color)
        button_text_rect = button_text_surf.get_rect(center=self.跳跃力提升按钮.center)
        self.屏幕.blit(button_text_surf, button_text_rect)
    
    def _draw_mining_upgrade_element(self):
        """绘制挖掘效率提升元素（长方形包裹）"""
        # 绘制背景框
        pygame.draw.rect(self.屏幕, 输入框背景色, self.挖掘效率提升区域, border_radius=self.元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, self.挖掘效率提升区域, 1, border_radius=self.元素圆角半径)
        
        # 计算各个元素的位置
        x_offset = self.挖掘效率提升区域.x + 20
        y_center = self.挖掘效率提升区域.y + self.挖掘效率提升区域.height // 2
        
        # 1. 提升挖掘效率标签
        label_surf = self.文本字体.render("提升挖掘效率:", True, 文本颜色)
        label_rect = label_surf.get_rect(center=(x_offset + label_surf.get_width() // 2, y_center))
        self.屏幕.blit(label_surf, label_rect)
        
        # 2. 限制次数
        x_offset += label_surf.get_width() + 40
        times_text = f"限制次数({self.挖掘效率升级次数}/{self.挖掘效率最大升级次数})"
        times_surf = self.文本字体.render(times_text, True, 文本颜色)
        times_rect = times_surf.get_rect(center=(x_offset + times_surf.get_width() // 2, y_center))
        self.屏幕.blit(times_surf, times_rect)
        
        # 3. 消耗星星
        x_offset += times_surf.get_width() + 40
        star_cost = self._calculate_star_cost(self.挖掘效率升级次数, self.挖掘效率最大升级次数)
        cost_text = f"消耗: {star_cost}"
        cost_surf = self.文本字体.render(cost_text, True, 文本颜色)
        cost_rect = cost_surf.get_rect(center=(x_offset + cost_surf.get_width() // 2, y_center))
        self.屏幕.blit(cost_surf, cost_rect)
        
        # 4. 提升效果
        x_offset += cost_surf.get_width() + 40
        effect_text = f"提升效果:+{self.挖掘效率每次提升量}%"
        effect_surf = self.文本字体.render(effect_text, True, 文本颜色)
        effect_rect = effect_surf.get_rect(center=(x_offset + effect_surf.get_width() // 2, y_center))
        self.屏幕.blit(effect_surf, effect_rect)
        
        # 5. 当前增加
        x_offset += effect_surf.get_width() + 40
        current_text = f"当前增加:{self.当前挖掘效率增加总量}%"
        current_surf = self.文本字体.render(current_text, True, 文本颜色)
        current_rect = current_surf.get_rect(center=(x_offset + current_surf.get_width() // 2, y_center))
        self.屏幕.blit(current_surf, current_rect)
        
        # 6. 提升按钮
        can_upgrade = self.挖掘效率升级次数 < self.挖掘效率最大升级次数
        button_color = 按钮悬停色 if can_upgrade else 输入框背景色
        text_color = 文本颜色 if can_upgrade else (120, 120, 120)
        
        pygame.draw.rect(self.屏幕, button_color, self.挖掘效率提升按钮, border_radius=self.小元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, self.挖掘效率提升按钮, 1, border_radius=self.小元素圆角半径)
        
        button_text = "提升" if can_upgrade else "已达上限"
        button_text_surf = self.文本字体.render(button_text, True, text_color)
        button_text_rect = button_text_surf.get_rect(center=self.挖掘效率提升按钮.center)
        self.屏幕.blit(button_text_surf, button_text_rect)
    

    
    def _draw_close_button(self):
        """绘制关闭按钮"""
        # 关闭按钮位置（右上角）
        close_button_size = 30
        close_button_x = self.底2_x + self.底2宽度 - close_button_size - 20
        close_button_y = self.底_y + 20
        self.close_button_rect = pygame.Rect(close_button_x, close_button_y, close_button_size, close_button_size)
        
        # 绘制关闭按钮
        pygame.draw.rect(self.屏幕, 输入框背景色, self.close_button_rect, border_radius=self.小元素圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, self.close_button_rect, 1, border_radius=self.小元素圆角半径)
        
        # 绘制关闭按钮文本
        close_text = self.文本字体.render("X", True, 文本颜色)
        text_rect = close_text.get_rect(center=self.close_button_rect.center)
        self.屏幕.blit(close_text, text_rect)
    
    def handle_event(self, 事件):
        """处理事件"""
        if not self.is_open:
            return False
        
        # 处理鼠标点击事件
        if 事件.type == pygame.MOUSEBUTTONDOWN:
            # 检查是否点击了选项按钮
            for button in self.选项按钮列表:
                if button["rect"].collidepoint(事件.pos):
                    self.current_option = button["index"]
                    print(f"选中选项: {button['text']}")
                    return True
            
            # 检查是否点击了关闭按钮
            if hasattr(self, 'close_button_rect') and self.close_button_rect.collidepoint(事件.pos):
                self.toggle()
                return True
            
            # 检查是否点击了属性提升按钮（仅在属性提升选项下）
            if self.current_option == 0:
                # 生命值提升按钮
                if hasattr(self, '生命值提升按钮') and self.生命值提升按钮.collidepoint(事件.pos):
                    self._handle_life_upgrade()
                    return True
                
                # 攻击力提升按钮
                if hasattr(self, '攻击力提升按钮') and self.攻击力提升按钮.collidepoint(事件.pos):
                    self._handle_attack_upgrade()
                    return True
                
                # 防御力提升按钮
                if hasattr(self, '防御力提升按钮') and self.防御力提升按钮.collidepoint(事件.pos):
                    self._handle_defense_upgrade()
                    return True
                
                # 移速提升按钮
                if hasattr(self, '移速提升按钮') and self.移速提升按钮.collidepoint(事件.pos):
                    self._handle_speed_upgrade()
                    return True
                
                # 跳跃力提升按钮
                if hasattr(self, '跳跃力提升按钮') and self.跳跃力提升按钮.collidepoint(事件.pos):
                    self._handle_jump_upgrade()
                    return True
                
                # 挖掘效率提升按钮
                if hasattr(self, '挖掘效率提升按钮') and self.挖掘效率提升按钮.collidepoint(事件.pos):
                    self._handle_mining_upgrade()
                    return True
                

        
        # 处理键盘事件
        elif 事件.type == pygame.KEYDOWN:
            # ESC键关闭页面
            if 事件.key == pygame.K_ESCAPE:
                self.toggle()
                return True
        
        return False
    
    def _draw_status_text(self):
        """绘制状态信息文本"""
        # 红色文本颜色
        red_color = (255, 0, 0)
        
        # 闪烁效果 - 仅当状态类型为error时闪烁
        if self.status_type == "error" and self.blink_timer > self.blink_interval:
            return  # 跳过这次绘制以实现闪烁效果
        
        # 创建文本表面
        status_font = pygame.font.SysFont("Microsoft YaHei", 18, True)  # 18号加粗字体
        status_surf = status_font.render(self.status_text, True, red_color)
        
        # 计算文本位置 - 在页面中间偏下位置居中显示（向上移动，并向右移动30像素）
        text_x = (self.屏幕宽度 - status_surf.get_width()) // 2 + 90  
        text_y = self.底_y + self.底2高度 - 50  # 页面底部上方50像素
        
        # 绘制文本
        self.屏幕.blit(status_surf, (text_x, text_y))
    
    def _handle_life_upgrade(self):
        """处理生命值提升逻辑"""
        # 检查是否可以升级
        if self.生命值升级次数 < self.生命值最大升级次数:
            # 计算所需的星星数量
            required_stars = self._calculate_star_cost(self.生命值升级次数, self.生命值最大升级次数)
            
            # 获取玩家对象和星星数量，同时支持star_count和stars两种属性名
            player = getattr(self.game, '玩家', None)
            if player is not None:
                # 检查是否有star_count或stars属性
                has_star_count = hasattr(player, 'star_count')
                has_stars = hasattr(player, 'stars')
                
                if has_star_count or has_stars:
                    # 获取当前星星数量
                    current_stars = player.star_count if has_star_count else player.stars
                    
                    if current_stars >= required_stars:
                        # 执行升级操作
                        self.生命值升级次数 += 1
                        self.当前生命值增加总量 += self.生命值每次提升量
                        
                        # 扣除星星
                        if has_star_count:
                            player.star_count -= required_stars
                        else:
                            player.stars -= required_stars
                        
                        # 应用到玩家对象的生命值上限
                        if hasattr(player, 'upgrade_health'):
                            player.upgrade_health += self.生命值每次提升量
                            # 重新计算总生命值
                            player.max_health = player.base_max_health + player.equipment_health + player.upgrade_health
                            print(f"玩家生命值上限增加到: {player.max_health}")
                        elif hasattr(player, 'max_health'):
                            # 兼容旧版本，直接更新max_health
                            player.max_health += self.生命值每次提升量
                            print(f"玩家生命值上限增加到: {player.max_health}")
                        # 如果有当前生命值属性，也同步增加
                        if hasattr(player, 'current_health'):
                            player.current_health += self.生命值每次提升量
                            print(f"玩家当前生命值增加到: {player.current_health}")
                        
                        remaining_stars = player.star_count if has_star_count else player.stars
                        print(f"生命值上限提升! 当前升级次数: {self.生命值升级次数}/{self.生命值最大升级次数}")
                        print(f"当前总共增加生命值: {self.当前生命值增加总量}")
                        print(f"扣除星星: {required_stars}, 剩余星星: {remaining_stars}")
                        
                        # 设置成功状态
                        self.show_status = True
                        self.status_text = "(生命值)升级成功"
                        self.status_type = "success"
                        self.status_start_time = time.time()
                    else:
                        print(f"星星数量不足! 需要 {required_stars}, 当前仅有 {current_stars}")
                        
                        # 设置错误状态
                        self.show_status = True
                        self.status_text = "star不足"
                        self.status_type = "error"
                        self.status_start_time = time.time()
                else:
                    # 如果玩家对象没有星星相关属性，模拟扣除星星（用于测试）
                    print(f"警告: 无法获取玩家星星数量，继续升级但不扣除星星")
                    self.生命值升级次数 += 1
                    self.当前生命值增加总量 += self.生命值每次提升量
            else:
                # 如果玩家对象不存在，模拟扣除星星（用于测试）
                print(f"警告: 无法获取玩家对象，继续升级但不扣除星星")
                self.生命值升级次数 += 1
                self.当前生命值增加总量 += self.生命值每次提升量
        else:
            print("生命值提升已达上限")
    
    def _handle_attack_upgrade(self):
        """处理攻击力提升逻辑"""
        # 检查是否可以升级
        if self.攻击力升级次数 < self.攻击力最大升级次数:
            # 计算所需的星星数量
            required_stars = self._calculate_star_cost(self.攻击力升级次数, self.攻击力最大升级次数)
            
            # 获取玩家对象和星星数量，同时支持star_count和stars两种属性名
            player = getattr(self.game, '玩家', None)
            if player is not None:
                # 检查是否有star_count或stars属性
                has_star_count = hasattr(player, 'star_count')
                has_stars = hasattr(player, 'stars')
                
                if has_star_count or has_stars:
                    # 获取当前星星数量
                    current_stars = player.star_count if has_star_count else player.stars
                    
                    if current_stars >= required_stars:
                        # 执行升级操作
                        self.攻击力升级次数 += 1
                        self.当前攻击力增加总量 += self.攻击力每次提升量
                        
                        # 扣除星星
                        if has_star_count:
                            player.star_count -= required_stars
                        else:
                            player.stars -= required_stars
                        
                        # 应用到玩家对象的攻击力
                        if hasattr(player, 'base_attack'):
                            player.base_attack += self.攻击力每次提升量
                            print(f"玩家攻击力增加到: {player.base_attack}")
                        elif hasattr(player, 'attack'):
                            player.attack += self.攻击力每次提升量
                            print(f"玩家攻击力增加到: {player.attack}")
                        
                        remaining_stars = player.star_count if has_star_count else player.stars
                        print(f"攻击力提升! 当前升级次数: {self.攻击力升级次数}/{self.攻击力最大升级次数}")
                        print(f"当前总共增加攻击力: {self.当前攻击力增加总量}")
                        print(f"扣除星星: {required_stars}, 剩余星星: {remaining_stars}")
                        
                        # 设置成功状态
                        self.show_status = True
                        self.status_text = "(攻击力)升级成功"
                        self.status_type = "success"
                        self.status_start_time = time.time()
                    else:
                        print(f"星星数量不足! 需要 {required_stars}, 当前仅有 {current_stars}")
                        
                        # 设置错误状态
                        self.show_status = True
                        self.status_text = "star不足"
                        self.status_type = "error"
                        self.status_start_time = time.time()
                else:
                    # 如果玩家对象没有星星相关属性，模拟扣除星星（用于测试）
                    print(f"警告: 无法获取玩家星星数量，继续升级但不扣除星星")
                    self.攻击力升级次数 += 1
                    self.当前攻击力增加总量 += self.攻击力每次提升量
            else:
                # 如果玩家对象不存在，模拟扣除星星（用于测试）
                print(f"警告: 无法获取玩家对象，继续升级但不扣除星星")
                self.攻击力升级次数 += 1
                self.当前攻击力增加总量 += self.攻击力每次提升量
        else:
            print("攻击力提升已达上限")
    
    def _handle_defense_upgrade(self):
        """处理防御力提升逻辑"""
        # 检查是否可以升级
        if self.防御力升级次数 < self.防御力最大升级次数:
            # 计算所需的星星数量
            required_stars = self._calculate_star_cost(self.防御力升级次数, self.防御力最大升级次数)
            
            # 获取玩家对象和星星数量，同时支持star_count和stars两种属性名
            player = getattr(self.game, '玩家', None)
            if player is not None:
                # 检查是否有star_count或stars属性
                has_star_count = hasattr(player, 'star_count')
                has_stars = hasattr(player, 'stars')
                
                if has_star_count or has_stars:
                    # 获取当前星星数量
                    current_stars = player.star_count if has_star_count else player.stars
                    
                    if current_stars >= required_stars:
                        # 执行升级操作
                        self.防御力升级次数 += 1
                        self.当前防御力增加总量 += self.防御力每次提升量
                        
                        # 扣除星星
                        if has_star_count:
                            player.star_count -= required_stars
                        else:
                            player.stars -= required_stars
                        
                        # 应用到玩家对象的防御力
                        if hasattr(player, 'upgrade_defense'):
                            player.upgrade_defense += self.防御力每次提升量
                            print(f"玩家防御力增加到: {player.upgrade_defense}")
                        elif hasattr(player, 'defense'):
                            player.defense += self.防御力每次提升量
                            print(f"玩家防御力增加到: {player.defense}")
                        elif hasattr(player, 'defense_value'):
                            player.defense_value += self.防御力每次提升量
                            print(f"玩家防御力增加到: {player.defense_value}")
                        
                        remaining_stars = player.star_count if has_star_count else player.stars
                        print(f"防御力提升! 当前升级次数: {self.防御力升级次数}/{self.防御力最大升级次数}")
                        print(f"当前总共增加防御力: {self.当前防御力增加总量}")
                        print(f"扣除星星: {required_stars}, 剩余星星: {remaining_stars}")
                        
                        # 设置成功状态
                        self.show_status = True
                        self.status_text = "(防御力)升级成功"
                        self.status_type = "success"
                        self.status_start_time = time.time()
                    else:
                        print(f"星星数量不足! 需要 {required_stars}, 当前仅有 {current_stars}")
                        
                        # 设置错误状态
                        self.show_status = True
                        self.status_text = "star不足"
                        self.status_type = "error"
                        self.status_start_time = time.time()
                else:
                    # 如果玩家对象没有星星相关属性，模拟扣除星星（用于测试）
                    print(f"警告: 无法获取玩家星星数量，继续升级但不扣除星星")
                    self.防御力升级次数 += 1
                    self.当前防御力增加总量 += self.防御力每次提升量
            else:
                # 如果玩家对象不存在，模拟扣除星星（用于测试）
                print(f"警告: 无法获取玩家对象，继续升级但不扣除星星")
                self.防御力升级次数 += 1
                self.当前防御力增加总量 += self.防御力每次提升量
        else:
            print("防御力提升已达上限")
    
    def _handle_speed_upgrade(self):
        """处理移速提升逻辑"""
        # 检查是否可以升级
        if self.移速升级次数 < self.移速最大升级次数:
            # 计算所需的星星数量
            required_stars = self._calculate_star_cost(self.移速升级次数, self.移速最大升级次数)
            
            # 获取玩家对象和星星数量，同时支持star_count和stars两种属性名
            player = getattr(self.game, '玩家', None)
            if player is not None:
                # 检查是否有star_count或stars属性
                has_star_count = hasattr(player, 'star_count')
                has_stars = hasattr(player, 'stars')
                
                if has_star_count or has_stars:
                    # 获取当前星星数量
                    current_stars = player.star_count if has_star_count else player.stars
                    
                    if current_stars >= required_stars:
                        # 执行升级操作
                        self.移速升级次数 += 1
                        self.当前移速增加总量 += self.移速每次提升量
                        
                        # 扣除星星
                        if has_star_count:
                            player.star_count -= required_stars
                        else:
                            player.stars -= required_stars
                        
                        # 应用到玩家对象的移速
                        if hasattr(player, '移动速度'):
                            player.移动速度 += self.移速每次提升量
                            print(f"玩家移速增加到: {player.移动速度}")
                        elif hasattr(player, 'speed'):
                            player.speed += self.移速每次提升量
                            print(f"玩家移速增加到: {player.speed}")
                        
                        remaining_stars = player.star_count if has_star_count else player.stars
                        print(f"移速提升! 当前升级次数: {self.移速升级次数}/{self.移速最大升级次数}")
                        print(f"当前总共增加移速: {self.当前移速增加总量}%")
                        print(f"扣除星星: {required_stars}, 剩余星星: {remaining_stars}")
                        
                        # 设置成功状态
                        self.show_status = True
                        self.status_text = "(移速)升级成功"
                        self.status_type = "success"
                        self.status_start_time = time.time()
                    else:
                        print(f"星星数量不足! 需要 {required_stars}, 当前仅有 {current_stars}")
                        
                        # 设置错误状态
                        self.show_status = True
                        self.status_text = "star不足"
                        self.status_type = "error"
                        self.status_start_time = time.time()
                else:
                    # 如果玩家对象没有星星相关属性，模拟扣除星星（用于测试）
                    print(f"警告: 无法获取玩家星星数量，继续升级但不扣除星星")
                    self.移速升级次数 += 1
                    self.当前移速增加总量 += self.移速每次提升量
            else:
                # 如果玩家对象不存在，模拟扣除星星（用于测试）
                print(f"警告: 无法获取玩家对象，继续升级但不扣除星星")
                self.移速升级次数 += 1
                self.当前移速增加总量 += self.移速每次提升量
        else:
            print("移速提升已达上限")
    
    def _handle_jump_upgrade(self):
        """处理跳跃力提升逻辑"""
        # 检查是否可以升级
        if self.跳跃力升级次数 < self.跳跃力最大升级次数:
            # 计算所需的星星数量
            required_stars = self._calculate_star_cost(self.跳跃力升级次数, self.跳跃力最大升级次数)
            
            # 获取玩家对象和星星数量，同时支持star_count和stars两种属性名
            player = getattr(self.game, '玩家', None)
            if player is not None:
                # 检查是否有star_count或stars属性
                has_star_count = hasattr(player, 'star_count')
                has_stars = hasattr(player, 'stars')
                
                if has_star_count or has_stars:
                    # 获取当前星星数量
                    current_stars = player.star_count if has_star_count else player.stars
                    
                    if current_stars >= required_stars:
                        # 执行升级操作
                        self.跳跃力升级次数 += 1
                        self.当前跳跃力增加总量 += self.跳跃力每次提升量
                        
                        # 扣除星星
                        if has_star_count:
                            player.star_count -= required_stars
                        else:
                            player.stars -= required_stars
                        
                        # 应用到玩家对象的跳跃力
                        if hasattr(player, '跳跃力度'):
                            player.跳跃力度 -= self.跳跃力每次提升量  # 跳跃力是负值，所以减去提升量
                            print(f"玩家跳跃力增加到: {player.跳跃力度}")
                        elif hasattr(player, 'jump_strength'):
                            player.jump_strength -= self.跳跃力每次提升量
                            print(f"玩家跳跃力增加到: {player.jump_strength}")
                        
                        # 同时增加摔落安全格数（每升级跳跃力一次，摔落安全格数+0.3）
                        if hasattr(player, 'upgrade_fall_safety'):
                            player.upgrade_fall_safety += 0.3
                        
                        remaining_stars = player.star_count if has_star_count else player.stars
                        print(f"跳跃力提升! 当前升级次数: {self.跳跃力升级次数}/{self.跳跃力最大升级次数}")
                        print(f"当前总共增加跳跃力: {self.当前跳跃力增加总量}")
                        print(f"扣除星星: {required_stars}, 剩余星星: {remaining_stars}")
                        
                        # 设置成功状态
                        self.show_status = True
                        self.status_text = "(跳跃力)升级成功"
                        self.status_type = "success"
                        self.status_start_time = time.time()
                    else:
                        print(f"星星数量不足! 需要 {required_stars}, 当前仅有 {current_stars}")
                        
                        # 设置错误状态
                        self.show_status = True
                        self.status_text = "star不足"
                        self.status_type = "error"
                        self.status_start_time = time.time()
                else:
                    # 如果玩家对象没有星星相关属性，模拟扣除星星（用于测试）
                    print(f"警告: 无法获取玩家星星数量，继续升级但不扣除星星")
                    self.跳跃力升级次数 += 1
                    self.当前跳跃力增加总量 += self.跳跃力每次提升量
            else:
                # 如果玩家对象不存在，模拟扣除星星（用于测试）
                print(f"警告: 无法获取玩家对象，继续升级但不扣除星星")
                self.跳跃力升级次数 += 1
                self.当前跳跃力增加总量 += self.跳跃力每次提升量
        else:
            print("跳跃力提升已达上限")
    
    def _handle_mining_upgrade(self):
        """处理挖掘效率提升逻辑"""
        # 检查是否可以升级
        if self.挖掘效率升级次数 < self.挖掘效率最大升级次数:
            # 计算所需的星星数量
            required_stars = self._calculate_star_cost(self.挖掘效率升级次数, self.挖掘效率最大升级次数)
            
            # 获取玩家对象和星星数量，同时支持star_count和stars两种属性名
            player = getattr(self.game, '玩家', None)
            if player is not None:
                # 检查是否有star_count或stars属性
                has_star_count = hasattr(player, 'star_count')
                has_stars = hasattr(player, 'stars')
                
                if has_star_count or has_stars:
                    # 获取当前星星数量
                    current_stars = player.star_count if has_star_count else player.stars
                    
                    if current_stars >= required_stars:
                        # 执行升级操作
                        self.挖掘效率升级次数 += 1
                        self.当前挖掘效率增加总量 += self.挖掘效率每次提升量
                        
                        # 扣除星星
                        if has_star_count:
                            player.star_count -= required_stars
                        else:
                            player.stars -= required_stars
                        
                        # 应用到玩家对象的挖掘效率
                        if hasattr(player, 'mining_efficiency'):
                            player.mining_efficiency += self.挖掘效率每次提升量
                            print(f"玩家挖掘效率增加到: {player.mining_efficiency}%")
                        elif hasattr(player, 'dig_speed'):
                            player.dig_speed += self.挖掘效率每次提升量 * 0.01
                            print(f"玩家挖掘速度增加到: {player.dig_speed}")
                        
                        remaining_stars = player.star_count if has_star_count else player.stars
                        print(f"挖掘效率提升! 当前升级次数: {self.挖掘效率升级次数}/{self.挖掘效率最大升级次数}")
                        print(f"当前总共增加挖掘效率: {self.当前挖掘效率增加总量}%")
                        print(f"扣除星星: {required_stars}, 剩余星星: {remaining_stars}")
                        
                        # 设置成功状态
                        self.show_status = True
                        self.status_text = "(挖掘效率)升级成功"
                        self.status_type = "success"
                        self.status_start_time = time.time()
                    else:
                        print(f"星星数量不足! 需要 {required_stars}, 当前仅有 {current_stars}")
                        
                        # 设置错误状态
                        self.show_status = True
                        self.status_text = "star不足"
                        self.status_type = "error"
                        self.status_start_time = time.time()
                else:
                    # 如果玩家对象没有星星相关属性，模拟扣除星星（用于测试）
                    print(f"警告: 无法获取玩家星星数量，继续升级但不扣除星星")
                    self.挖掘效率升级次数 += 1
                    self.当前挖掘效率增加总量 += self.挖掘效率每次提升量
            else:
                # 如果玩家对象不存在，模拟扣除星星（用于测试）
                print(f"警告: 无法获取玩家对象，继续升级但不扣除星星")
                self.挖掘效率升级次数 += 1
                self.当前挖掘效率增加总量 += self.挖掘效率每次提升量
        else:
            print("挖掘效率提升已达上限")
    

    
    def update(self, world=None):
        """更新页面状态"""
        if not self.is_open:
            return
        
        # 检查屏幕尺寸是否变化，如果变化了重新计算位置
        当前屏幕宽度 = self.屏幕.get_width()
        当前屏幕高度 = self.屏幕.get_height()
        
        if 当前屏幕宽度 != self.屏幕宽度 or 当前屏幕高度 != self.屏幕高度:
            # 更新屏幕尺寸
            self.屏幕宽度 = 当前屏幕宽度
            self.屏幕高度 = 当前屏幕高度
            
            # 重新计算居中位置
            self.底1_x = (self.屏幕宽度 - self.底1宽度 - self.间隔 - self.底2宽度) // 2
            self.底2_x = self.底1_x + self.底1宽度 + self.间隔
            self.底_y = (self.屏幕高度 - max(self.底1高度, self.底2高度)) // 2
            
            # 重新设置所有UI元素的位置
            self._setup_ui_elements()
            self._setup_attribute_elements()
        
        # 更新状态显示
        if self.show_status:
            current_time = time.time()
            # 检查是否超过显示时间
            if current_time - self.status_start_time > self.status_duration:
                self.show_status = False
            # 更新闪烁计时器
            self.blink_timer = (self.blink_timer + 0.016) % (self.blink_interval * 2)  # 假设60fps