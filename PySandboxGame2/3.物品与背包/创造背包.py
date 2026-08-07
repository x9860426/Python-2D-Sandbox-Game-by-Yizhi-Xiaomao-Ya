import pygame
import sys
from 物品定义 import 物品, 获取物品图片
from 图片加载 import 图片管理器

# 深色主题配色方案
主背景色 = (26, 27, 29)      # 更深灰色主背景
次级背景色 = (39, 40, 40)    # 深灰色次级背景
边框颜色 = (70, 70, 70)      # 中灰色边框
标题颜色 = (220, 220, 220)   # 浅色标题
文本颜色 = (240, 240, 240)   # 浅色文本
阴影颜色 = (0, 0, 0, 80)     # 更明显的半透明黑色阴影

class CreativeBackpack:
    """创造模式背包页面"""
    

    
    def generate_item_list(self):
        """根据物品分类生成物品列表"""
        self.category_items = {}
        
        for category in self.categories:
            self.category_items[category] = []
        
        # 将物品分类到不同类别
        for item_id, item_info in 物品.items():
            item_type = item_info.get("类型", "其他")
            item_name = item_info.get("名称", "")
            
            # 排除无法获取的物品：子弹发射、木箭发射和火箭弹发射
            if item_name in ["子弹发射", "木箭发射", "火箭弹发射"]:
                continue
            
            # 植物分类 - 通过物品名称识别植物类物品
            plant_names = ["草", "树叶", "红花", "枯草", "仙人掌", "乔木", "乔木叶", "灌木", "乔木果", 
                          "土豆", "小麦", "水稻", "玉米", "甘蔗", "番薯", "白菜", "木头"]
            # 检查物品是否为植物类（名称包含植物相关词汇或名称在plant_names列表中）
            is_plant = False
            if item_type == "block":
                if item_name in plant_names:
                    is_plant = True
                # 检查植物生长阶段（名称中包含发芽、幼年、成年、成熟等关键词）
                elif any(keyword in item_name for keyword in ["发芽", "幼年", "成年", "成熟"]):
                    is_plant = True
            
            if is_plant:
                self.category_items["植物"].append(item_id)
            # 方块分类（不包括植物类方块）
            elif item_type == "block" and item_name not in plant_names:
                self.category_items["方块"].append(item_id)
            # 武器分类（包括武器、弹药和救世能源）
            elif item_type in ["weapon", "arrow", "bullet"] or item_name in ["救世能源"]:
                self.category_items["武器"].append(item_id)
            # 工具分类（不包括武器）
            elif item_type in ["tool", "helmet", "armor", "boots", "special", "equipment", "axe", "pickaxe", "shovel"]:
                self.category_items["工具"].append(item_id)
            # 生物分类（生物蛋）
            elif item_type == "生物蛋":
                self.category_items["生物"].append(item_id)
            # 食品分类（包括食物和药水）
            elif item_type in ["food", "potion"]:
                self.category_items["食品"].append(item_id)
            # 材料分类
            elif item_type == "material":
                self.category_items["材料"].append(item_id)
            # 其他分类
            else:
                self.category_items["其他"].append(item_id)
        
        # 确保每个分类都有物品列表，即使为空
        for category in self.categories:
            if category not in self.category_items:
                self.category_items[category] = []
    
    def toggle(self):
        """切换页面显示状态"""
        self.is_open = not self.is_open
        return self.is_open
    
    def draw(self, 屏幕):
        """绘制创造背包页面"""
        if not self.is_open:
            return
        
        # 更新屏幕引用和尺寸
        self.屏幕 = 屏幕
        self.屏幕宽度 = self.屏幕.get_width()
        self.屏幕高度 = self.屏幕.get_height()
        
        # 重新计算居中位置，确保F3页面始终居中
        self.底1_x = (self.屏幕宽度 - self.底1宽度 - self.间隔 - self.底2宽度) // 2
        self.底2_x = self.底1_x + self.底1宽度 + self.间隔
        self.底_y = (self.屏幕高度 - max(self.底1高度, self.底2高度)) // 2
        
        # 绘制背景遮罩
        overlay = pygame.Surface((self.屏幕宽度, self.屏幕高度), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # 半透明黑色
        self.屏幕.blit(overlay, (0, 0))
        
        # 绘制底1（左侧面板）带圆角
        pygame.draw.rect(self.屏幕, 主背景色, 
                        (self.底1_x, self.底_y, self.底1宽度, self.底1高度), 
                        border_radius=self.圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (self.底1_x, self.底_y, self.底1宽度, self.底1高度), 
                        2, border_radius=self.圆角半径)
        
        # 绘制底2（右侧面板）带圆角
        pygame.draw.rect(self.屏幕, 主背景色, 
                        (self.底2_x, self.底_y, self.底2宽度, self.底2高度), 
                        border_radius=self.圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (self.底2_x, self.底_y, self.底2宽度, self.底2高度), 
                        2, border_radius=self.圆角半径)
        
        # 绘制左侧面板标题
        左侧标题 = self.标题字体.render("物品分类", True, 标题颜色)
        左侧标题_rect = 左侧标题.get_rect(center=(self.底1_x + self.底1宽度//2, self.底_y + 30))
        # 标题阴影
        左侧标题阴影 = self.标题字体.render("物品分类", True, (0, 0, 0, 50))
        self.屏幕.blit(左侧标题阴影, (左侧标题_rect.x + 1, 左侧标题_rect.y + 1))
        self.屏幕.blit(左侧标题, 左侧标题_rect)
        
        # 绘制右侧面板标题
        右侧标题 = self.标题字体.render("物品列表", True, 标题颜色)
        右侧标题_rect = 右侧标题.get_rect(center=(self.底2_x + self.底2宽度//2, self.底_y + 30))
        # 标题阴影
        右侧标题阴影 = self.标题字体.render("物品列表", True, (0, 0, 0, 50))
        self.屏幕.blit(右侧标题阴影, (右侧标题_rect.x + 1, 右侧标题_rect.y + 1))
        self.屏幕.blit(右侧标题, 右侧标题_rect)
        
        # 绘制分类按钮
        self.draw_category_buttons()
        
        # 绘制物品列表
        self.draw_item_list()
        
        # 绘制物品数量控制区域（右下角）
        self.draw_item_count_control()
        
        # 绘制关闭按钮
        self.draw_close_button()
        
        # 绘制物品悬停信息
        self.draw_item_tooltip(屏幕)
        
        # 绘制红色状态文本
        self._draw_status_text()
        
        # 绘制漂浮文字（在所有UI元素之后绘制，确保显示在最上层）
        self._draw_notifications()
    
    def draw_item_tooltip(self, 屏幕):
        """绘制物品悬停提示信息"""
        if not self.当前悬停物品:
            return
        
        # 获取物品信息
        物品名称 = self.当前悬停物品.get("名称", "未知物品")
        物品介绍 = self.当前悬停物品.get("说明", "无说明")
        
        # 创建提示文本
        名称文本 = f"物品:{物品名称}"
        介绍文本前缀 = "介绍:"
        介绍文本内容 = 物品介绍
        
        # 渲染名称文本
        名称表面 = self.悬停字体.render(名称文本, True, 文本颜色)
        
        # 文本换行处理函数
        def wrap_text(text, font, max_width_chars=20):
            """将文本按指定字符数分行"""
            lines = []
            current_line = ""
            
            # 中文字符按字数拆分，英文按单词拆分
            i = 0
            while i < len(text):
                # 如果当前行已经达到最大字符数，添加到lines并重置
                if len(current_line) >= max_width_chars:
                    lines.append(current_line)
                    current_line = ""
                
                # 添加当前字符
                current_line += text[i]
                i += 1
            
            # 添加最后一行
            if current_line:
                lines.append(current_line)
            
            return lines
        
        # 处理名称文本的换行（如果名称过长）
        名称_lines = wrap_text(物品名称, self.悬停字体, 20)
        # 重新构建带前缀的名称文本行
        名称_full_lines = [f"物品:{line}" for line in 名称_lines]
        
        # 处理介绍文本的换行
        介绍_lines = wrap_text(介绍文本内容, self.悬停字体, 20)
        # 第一行需要加上前缀
        if 介绍_lines:
            介绍_lines[0] = 介绍文本前缀 + 介绍_lines[0]
        
        # 渲染所有文本行
        文本_surfaces = []
        # 渲染名称行
        for line in 名称_full_lines:
            文本_surfaces.append(self.悬停字体.render(line, True, 文本颜色))
        # 渲染介绍行
        for line in 介绍_lines:
            文本_surfaces.append(self.悬停字体.render(line, True, 文本颜色))
        
        # 计算提示框尺寸
        行高 = self.悬停字体.get_height()
        最大宽度 = max(surface.get_width() for surface in 文本_surfaces)
        提示框宽度 = 最大宽度 + 16
        提示框高度 = len(文本_surfaces) * 行高 + 12
        
        # 计算提示框位置（在物品格子上方）
        提示框_x = self.当前悬停物品_rect.x + self.当前悬停物品_rect.width // 2 - 提示框宽度 // 2
        提示框_y = self.当前悬停物品_rect.y - 提示框高度 - 10
        
        # 确保提示框不会超出屏幕边界
        if 提示框_x < 0:
            提示框_x = 0
        elif 提示框_x + 提示框宽度 > 屏幕.get_width():
            提示框_x = 屏幕.get_width() - 提示框宽度
        
        if 提示框_y < 0:
            提示框_y = self.当前悬停物品_rect.y + self.当前悬停物品_rect.height + 10
        
        # 绘制提示框背景
        提示框_rect = pygame.Rect(提示框_x, 提示框_y, 提示框宽度, 提示框高度)
        pygame.draw.rect(屏幕, 次级背景色, 提示框_rect, border_radius=5)
        pygame.draw.rect(屏幕, 边框颜色, 提示框_rect, 1, border_radius=5)
        
        # 绘制所有文本行
        current_y = 提示框_y + 6
        for surface in 文本_surfaces:
            屏幕.blit(surface, (提示框_x + 8, current_y))
            current_y += 行高
    
    def _draw_status_text(self):
        """绘制红色状态文本"""
        if not self.状态显示文本 or self.状态显示计时器 <= 0:
            return
        
        # 闪烁效果控制
        if self.状态文本闪烁 and self.状态显示计时器 % 10 < 5:
            return
        
        # 创建红色文本
        status_surf = self.文本字体.render(self.状态显示文本, True, (255, 0, 0))
        
        # 计算文本位置，按照要求设置x坐标：(屏幕宽度 - 文本宽度) // 2 + 90
        text_x = (self.屏幕宽度 - status_surf.get_width()) // 2 + 90
        text_y = (self.屏幕高度 - status_surf.get_height()) // 2  # 居中显示
        
        # 绘制文本阴影（可选，增强可读性）
        shadow_surf = self.文本字体.render(self.状态显示文本, True, (0, 0, 0))
        self.屏幕.blit(shadow_surf, (text_x + 1, text_y + 1))
        
        # 绘制红色文本
        self.屏幕.blit(status_surf, (text_x, text_y))
        
    def _show_notification(self, text):
        """显示漂浮文字通知"""
        # 添加新的漂浮文字到列表
        self.notifications.append({
            "text": text,
            "x": self.屏幕宽度 // 2,  # 屏幕中心
            "y": self.屏幕高度 // 2 - 250,  # 初始位置在屏幕中心上方120像素
            "alpha": 255,  # 完全不透明
            "start_time": self.当前时间,  # 开始显示时间
            "duration": self.提示显示时间  # 显示持续时间
        })
    
    def _draw_notifications(self):
        """绘制所有漂浮文字"""
        for notification in self.notifications:
            # 创建文字表面
            text_surface = self.提示字体.render(notification["text"], True, (255, 255, 255))
            # 设置透明度
            text_surface.set_alpha(notification["alpha"])
            # 计算文字居中位置
            text_rect = text_surface.get_rect(center=(notification["x"], notification["y"]))
            # 绘制文字
            self.屏幕.blit(text_surface, text_rect)
    
    def _update_notifications(self, delta_time):
        """更新漂浮文字的位置和透明度"""
        self.当前时间 += delta_time
        
        # 更新每个漂浮文字
        for notification in self.notifications[:]:
            # 计算已经显示的时间比例
            elapsed_time = self.当前时间 - notification["start_time"]
            time_ratio = elapsed_time / notification["duration"]
            
            # 更新位置（向上移动）
            notification["y"] -= self.提示移动速度 * delta_time
            
            # 更新透明度（淡入淡出效果）
            if time_ratio < 0.1:
                # 前10%时间淡入
                notification["alpha"] = int(255 * (time_ratio / 0.1))
            elif time_ratio > 0.9:
                # 后10%时间淡出
                notification["alpha"] = int(255 * (1 - (time_ratio - 0.9) / 0.1))
            
            # 移除已经显示完成的文字
            if elapsed_time > notification["duration"]:
                self.notifications.remove(notification)
    
    def update(self):
        """更新状态显示计时器和漂浮文字"""
        if self.状态显示计时器 > 0:
            self.状态显示计时器 -= 1
        
        # 更新漂浮文字（使用固定的delta_time，因为没有实际的游戏循环时间）
        self._update_notifications(0.02)
    
    def draw_item_count_control(self):
        """绘制物品数量控制区域，格式：最小按钮|-1按钮|滑动区域|+1按钮|最大按钮"""
        # 控制区域位置（右下角，向左移动40像素）
        控制区域宽度 = self.物品数量最小值.__str__().__len__() * 30 + self.加减按钮宽度 * 4 + self.滑动区域宽度 + 20
        控制区域高度 = 40
        控制区域_x = self.底2_x + self.底2宽度 - 控制区域宽度 - 60  # 再向左移动20像素
        控制区域_y = self.底_y + self.底2高度 - 控制区域高度 - 20
        
        # 计算各元素位置
        最小按钮_x = 控制区域_x
        减号按钮_x = 最小按钮_x + self.加减按钮宽度 + 5
        滑动区域_x = 减号按钮_x + self.加减按钮宽度 + 5
        加号按钮_x = 滑动区域_x + self.滑动区域宽度 + 5
        最大按钮_x = 加号按钮_x + self.加减按钮宽度 + 5
        垂直中心 = 控制区域_y + 控制区域高度 // 2
        
        # 绘制最小按钮
        pygame.draw.rect(self.屏幕, 次级背景色, 
                        (最小按钮_x, 垂直中心 - self.加减按钮高度 // 2, 
                         self.加减按钮宽度, self.加减按钮高度), 
                        border_radius=4)
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (最小按钮_x, 垂直中心 - self.加减按钮高度 // 2, 
                         self.加减按钮宽度, self.加减按钮高度), 
                        1, border_radius=4)
        最小文本 = self.数字字体.render(str(self.物品数量最小值), True, 文本颜色)
        最小_rect = 最小文本.get_rect(center=(最小按钮_x + self.加减按钮宽度 // 2, 垂直中心))
        self.屏幕.blit(最小文本, 最小_rect)
        
        # 绘制减号按钮
        pygame.draw.rect(self.屏幕, 次级背景色, 
                        (减号按钮_x, 垂直中心 - self.加减按钮高度 // 2, 
                         self.加减按钮宽度, self.加减按钮高度), 
                        border_radius=4)
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (减号按钮_x, 垂直中心 - self.加减按钮高度 // 2, 
                         self.加减按钮宽度, self.加减按钮高度), 
                        1, border_radius=4)
        减号文本 = self.数字字体.render("-1", True, 文本颜色)
        减号_rect = 减号文本.get_rect(center=(减号按钮_x + self.加减按钮宽度 // 2, 垂直中心))
        self.屏幕.blit(减号文本, 减号_rect)
        
        # 绘制滑动区域背景
        pygame.draw.rect(self.屏幕, 次级背景色, 
                        (滑动区域_x, 垂直中心 - self.滑动区域高度 // 2, 
                         self.滑动区域宽度, self.滑动区域高度), 
                        border_radius=4)
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (滑动区域_x, 垂直中心 - self.滑动区域高度 // 2, 
                         self.滑动区域宽度, self.滑动区域高度), 
                        1, border_radius=4)
        
        # 计算滑块位置
        滑块位置比例 = (self.当前物品数量 - self.物品数量最小值) / (self.物品数量最大值 - self.物品数量最小值)
        滑块_x = 滑动区域_x + 2 + 滑块位置比例 * (self.滑动区域宽度 - self.滑块宽度 - 4)
        滑块_y = 垂直中心 - self.滑块高度 // 2
        
        # 绘制滑块
        pygame.draw.rect(self.屏幕, (100, 100, 100), 
                        (滑块_x, 滑块_y, self.滑块宽度, self.滑块高度), 
                        border_radius=2)
        pygame.draw.rect(self.屏幕, (150, 150, 150), 
                        (滑块_x + 1, 滑块_y + 1, self.滑块宽度 - 2, self.滑块高度 - 2), 
                        border_radius=2)
        
        # 绘制当前数值
        当前数量文本 = self.数字字体.render(str(self.当前物品数量), True, 标题颜色)
        当前数量_rect = 当前数量文本.get_rect(center=(滑动区域_x + self.滑动区域宽度 // 2, 垂直中心))
        self.屏幕.blit(当前数量文本, 当前数量_rect)
        
        # 绘制加号按钮
        pygame.draw.rect(self.屏幕, 次级背景色, 
                        (加号按钮_x, 垂直中心 - self.加减按钮高度 // 2, 
                         self.加减按钮宽度, self.加减按钮高度), 
                        border_radius=4)
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (加号按钮_x, 垂直中心 - self.加减按钮高度 // 2, 
                         self.加减按钮宽度, self.加减按钮高度), 
                        1, border_radius=4)
        加号文本 = self.数字字体.render("+1", True, 文本颜色)
        加号_rect = 加号文本.get_rect(center=(加号按钮_x + self.加减按钮宽度 // 2, 垂直中心))
        self.屏幕.blit(加号文本, 加号_rect)
        
        # 绘制最大按钮
        pygame.draw.rect(self.屏幕, 次级背景色, 
                        (最大按钮_x, 垂直中心 - self.加减按钮高度 // 2, 
                         self.加减按钮宽度, self.加减按钮高度), 
                        border_radius=4)
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (最大按钮_x, 垂直中心 - self.加减按钮高度 // 2, 
                         self.加减按钮宽度, self.加减按钮高度), 
                        1, border_radius=4)
        最大文本 = self.数字字体.render(str(self.物品数量最大值), True, 文本颜色)
        最大_rect = 最大文本.get_rect(center=(最大按钮_x + self.加减按钮宽度 // 2, 垂直中心))
        self.屏幕.blit(最大文本, 最大_rect)
    
    def draw_category_buttons(self):
        """绘制左侧分类按钮"""
        button_start_y = self.底_y + 70
        
        for i, category in enumerate(self.categories):
            button_y = button_start_y + i * (self.button_height + self.button_spacing)
            button_rect = pygame.Rect(
                self.底1_x + 15,
                button_y,
                self.button_width,
                self.button_height
            )
            
            # 根据是否选中设置按钮颜色
            if i == self.current_category:
                button_color = (70, 70, 70)  # 选中状态颜色
            else:
                button_color = 次级背景色
            
            # 绘制按钮
            pygame.draw.rect(self.屏幕, button_color, button_rect, border_radius=5)
            pygame.draw.rect(self.屏幕, 边框颜色, button_rect, 1, border_radius=5)
            
            # 绘制按钮文本
            text = self.文本字体.render(category, True, 文本颜色)
            text_rect = text.get_rect(center=button_rect.center)
            self.屏幕.blit(text, text_rect)
    
    def __init__(self, game):
        self.game = game
        self.屏幕 = game.屏幕  # 从game实例获取屏幕对象
        self.is_open = False
        
        # 获取屏幕尺寸
        self.屏幕宽度 = self.屏幕.get_width()
        self.屏幕高度 = self.屏幕.get_height()
        
        # 状态显示相关变量
        self.状态显示文本 = ""  # 要显示的状态文本
        self.状态显示计时器 = 0  # 状态文本显示计时器
        self.状态文本闪烁 = False  # 文本闪烁状态
        
        # 页面尺寸（比设置页面大）
        self.底1宽度 = 200  # 比设置页面的160宽
        self.底1高度 = 700  # 比设置页面的600高
        self.底2宽度 = 850  # 比设置页面的700宽
        self.底2高度 = 700  # 比设置页面的600高
        self.间隔 = 20
        
        # 圆角半径和字体设置
        self.圆角半径 = 10
        self.标题字体 = pygame.font.SysFont("Microsoft YaHei", 24, True)
        self.文本字体 = pygame.font.SysFont("Microsoft YaHei", 16)
        self.数字字体 = pygame.font.SysFont("Microsoft YaHei", 18)
        # 悬停信息字体
        self.悬停字体 = pygame.font.SysFont("Microsoft YaHei", 14)
        
        # 当前悬停的物品信息
        self.当前悬停物品 = None
        self.当前悬停物品_rect = None
        
        # 物品分类
        self.categories = [
            "植物", "方块", "工具", "武器", "生物", "食品", "材料", "其他"
        ]
        self.current_category = 0
        
        # 物品格子设置
        self.slot_size = 48  # 比普通背包大
        self.slot_margin = 4
        self.slots_per_row = 15  # 每行15个格子
        
        # 按钮设置
        self.button_height = 40
        self.button_width = self.底1宽度 - 30
        self.button_spacing = 10
        
        # 物品数量控制设置
        self.物品数量最小值 = 1  # 最小拿取数量
        self.物品数量最大值 = 99  # 最大拿取数量
        self.当前物品数量 = 64  # 默认拿取数量
        
        # 滑动控制区域设置
        self.滑动区域宽度 = 120
        self.滑动区域高度 = 24
        self.滑块宽度 = 20
        self.滑块高度 = 20
        
        # 按钮尺寸
        self.加减按钮宽度 = 30
        self.加减按钮高度 = 30
        
        # 漂浮文字系统
        self.notifications = []  # 存储当前显示的漂浮文字列表
        self.提示移动速度 = 50  # 文字向上移动速度（像素/秒）
        self.提示显示时间 = 3.0  # 文字显示总时间（秒）
        self.当前时间 = 0  # 当前时间记录
        self.提示字体 = pygame.font.SysFont("Microsoft YaHei", 20, True)  # 漂浮文字字体
        
        # 生物分类选项按钮
        self.生物分类按钮 = []
        
        # 滑动相关属性
        self.生物分类滑动偏移 = 0  # 当前滑动偏移量
        self.生物分类最大滑动偏移 = 0  # 最大滑动偏移量
        self.生物分类总高度 = 0  # 生物分类选项的总高度
        self.生物分类是否正在滑动 = False  # 是否正在滑动
        self.生物分类鼠标按下位置 = (0, 0)  # 鼠标按下时的位置
        self.生物分类鼠标按下时的偏移 = 0  # 鼠标按下时的滑动偏移量
        
        # 生成物品列表
        self.generate_item_list()
    
    def draw_item_list(self):
        """绘制右侧物品列表"""
        # 获取当前分类的物品
        current_category = self.categories[self.current_category]
        items = self.category_items[current_category]
        
        # 计算物品显示区域
        display_area_x = self.底2_x + 20
        display_area_y = self.底_y + 70
        display_area_width = self.底2宽度 - 40
        display_area_height = self.底2高度 - 140  # 留出底部空间
        
        # 绘制物品格子背景（内底，比外底更浅）
        内底颜色 = (50, 50, 50)  # 比外底主背景色更浅的灰色
        pygame.draw.rect(self.屏幕, 内底颜色, 
                        (display_area_x, display_area_y, display_area_width, display_area_height), 
                        border_radius=8)
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (display_area_x, display_area_y, display_area_width, display_area_height), 
                        1, border_radius=8)
        
        # 设置裁剪区域，确保所有内容只显示在内底区域内
        self.屏幕.set_clip(pygame.Rect(display_area_x, display_area_y, display_area_width, display_area_height))
        
        # 清空之前的生物分类按钮
        self.生物分类按钮.clear()
        
        button_size = self.slot_size  # 和其他选项一样大小
        button_margin = self.slot_margin  # 和其他选项一样间距
        columns = self.slots_per_row  # 一行显示15个
        
        if current_category == "生物":
            # 生物分类字典
            生物分类 = {
                "boos": {
                    "name": "boos",
                    "items": [21051, 21016, 21061, 21062],  # 贝利亚蛋, 吸血鬼蛋, 肥胖蛋, 死神蛋
                    "display_names": ["贝利亚", "吸血鬼", "肥胖Boss", "死神"]
                },
                "怪物": {
                    "name": "怪物",
                    "items": [21008, 21010, 21024, 21027, 21032, 21046, 21049, 21050, 21052, 21053, 21054, 21055, 21056, 21029, 21030, 21031, 21057],
                    "display_names": ["丧尸", "僵尸", "岩浆怪", "异变者", "异形蜘蛛", "恶魔球", "红眼粘液怪", "蓝怪", "蚂蚁怪物", "超异变者", "邪恶粘液怪", "邪恶蜘蛛", "邪恶蝙蝠", "金怪", "异形眼", "异形球体", "异形蛇", "问灵"]
                },
                "魔物": {
                    "name": "魔物",
                    "items": [21000, 21002, 21004, 21005, 21006, 21013, 21014, 21015, 21017, 21018, 21020, 21025, 21028, 21034, 21039, 21041, 21045, 21059, 21012, 21038, 21019],
                    "display_names": ["史莱姆", "幽灵", "火焰精灵", "蘑菇怪", "岩石怪", "双角骷髅", "变形怪", "可爱幽灵", "夜魔", "大史莱姆", "小恶魔", "幽灵人", "异变骷髅", "普通骷髅", "独眼人", "狼人", "章鱼怪", "骷髅球", "刺球", "牧羊人", "奶龙"]
                },
                "生物": {
                    "name": "生物",
                    "items": [21001, 21003, 21042, 21044, 21058, 21060],
                    "display_names": ["土拨鼠", "蝙蝠", "猪", "章鱼", "霸王龙", "鸟"]
                },
                "动物": {
                    "name": "动物",
                    "items": [21009, 21021, 21022, 21035, 21037, 21043, 21047, 21007, 21011, 21023, 21036],
                    "display_names": ["企鹅", "小熊猫", "小霸王龙", "松鼠", "灰兔", "白兔", "老虎", "三角龙", "猴子", "小鸡", "母鸡"]
                },
                "其他": {
                    "name": "其他",
                    "items": [21048, 21063],
                    "display_names": ["萌刺", "死神祝福"]
                }
            }
            
            # 首先计算生物分类选项的总高度
            total_height = 0
            for category_info in 生物分类.values():
                total_height += 30  # 分类名称高度
                # 计算该分类需要的行数
                items_count = len(category_info["items"])
                rows = (items_count + columns - 1) // columns
                total_height += rows * (button_size + button_margin) + 20  # 分类选项高度 + 间距
            
            # 绘制分类文字和选项按钮，考虑滑动偏移
            current_y = display_area_y + 15 - self.生物分类滑动偏移
            
            for category_name, category_info in 生物分类.items():
                # 绘制分类名称
                category_text = category_info["name"]
                category_surface = self.文本字体.render(category_text, True, (255, 255, 255))
                # 只有当分类名称在显示区域内时才绘制
                if current_y > display_area_y - 30 and current_y < display_area_y + display_area_height:
                    self.屏幕.blit(category_surface, (display_area_x + 20, current_y))
                current_y += 30
                
                # 绘制分类选项按钮
                row = 0
                col = 0
                
                for i, (item_id, display_name) in enumerate(zip(category_info["items"], category_info["display_names"])):
                    # 计算按钮位置，和其他分类的物品格子位置一致
                    button_x = display_area_x + 15 + col * (button_size + button_margin)
                    button_y = current_y + row * (button_size + button_margin)
                    
                    # 检查是否需要换行
                    if button_x + button_size > display_area_x + display_area_width - 30:
                        row += 1
                        col = 0
                        button_x = display_area_x + 15
                        button_y = current_y + row * (button_size + button_margin)
                    
                    # 创建按钮矩形
                    button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
                    
                    # 只有当按钮在显示区域内时才绘制
                    if button_y > display_area_y - button_size and button_y < display_area_y + display_area_height:
                        # 检查鼠标是否悬停
                        mouse_pos = pygame.mouse.get_pos()
                        is_hover = button_rect.collidepoint(mouse_pos)
                        
                        # 设置按钮颜色
                        button_color = (70, 70, 70) if is_hover else (40, 40, 40)
                        
                        # 绘制按钮背景，和其他物品格子一样
                        pygame.draw.rect(self.屏幕, button_color, button_rect, border_radius=4)
                        pygame.draw.rect(self.屏幕, 边框颜色, button_rect, 1, border_radius=4)
                        
                        # 尝试加载并绘制生物图片
                        try:
                            item_image = 获取物品图片(item_id)
                            if item_image:
                                # 缩放图片以适应按钮大小，和其他物品格子一样
                                scaled_image = pygame.transform.scale(item_image, (button_size - 4, button_size - 4))
                                self.屏幕.blit(scaled_image, (button_x + 2, button_y + 2))
                        except Exception:
                            # 如果图片加载失败，绘制生物名称
                            button_text = self.文本字体.render(display_name[:2], True, (200, 200, 200))
                            text_rect = button_text.get_rect(center=button_rect.center)
                            self.屏幕.blit(button_text, text_rect)
                    
                    # 保存按钮信息，用于点击检测
                    self.生物分类按钮.append({
                        "rect": button_rect,
                        "item_id": item_id,
                        "item_name": display_name
                    })
                    
                    col += 1
                
                current_y += (row + 1) * (button_size + button_margin) + 20
        elif current_category == "植物":
            # 植物分类字典
            植物分类 = {
                "方块": {
                    "name": "方块",
                    "items": [],
                    "display_names": []
                },
                "植物": {
                    "name": "植物",
                    "items": [],
                    "display_names": []
                },
                "种子": {
                    "name": "种子",
                    "items": [],
                    "display_names": []
                },
                "生长状态": {
                    "name": "生长状态",
                    "items": [],
                    "display_names": []
                },
                "其他": {
                    "name": "其他",
                    "items": [],
                    "display_names": []
                }
            }
            
            # 根据物品ID添加到对应的子分类
            for item_id in items:
                item_info = 物品.get(item_id, {})
                item_name = item_info.get("名称", "")
                item_type = item_info.get("类型", "")
                
                # 根据物品名称和类型分类
                # 方块：乔木，乔木叶，树叶，木头
                if item_type == "block":
                    if item_name in ["乔木", "乔木叶", "树叶", "木头"]:
                        植物分类["方块"]["items"].append(item_id)
                        植物分类["方块"]["display_names"].append(item_name)
                    # 植物：红花，草，灌木，枯草，仙人掌
                    elif item_name in ["红花", "草", "灌木", "枯草", "仙人掌"]:
                        植物分类["植物"]["items"].append(item_id)
                        植物分类["植物"]["display_names"].append(item_name)
                    # 其他植物相关的生长状态
                    else:
                        植物分类["生长状态"]["items"].append(item_id)
                        植物分类["生长状态"]["display_names"].append(item_name)
                # 种子：各种种子
                elif "种子" in item_name:
                    植物分类["种子"]["items"].append(item_id)
                    植物分类["种子"]["display_names"].append(item_name)
                # 生长状态：各种植物的生长阶段
                elif any(keyword in item_name for keyword in ["发芽", "幼年", "成年", "成熟"]):
                    植物分类["生长状态"]["items"].append(item_id)
                    植物分类["生长状态"]["display_names"].append(item_name)
                # 其他植物相关物品
                else:
                    植物分类["其他"]["items"].append(item_id)
                    植物分类["其他"]["display_names"].append(item_name)
            
            # 首先计算植物分类选项的总高度
            total_height = 0
            for category_info in 植物分类.values():
                if len(category_info["items"]) > 0:
                    total_height += 30  # 分类名称高度
                    # 计算该分类需要的行数
                    items_count = len(category_info["items"])
                    rows = (items_count + columns - 1) // columns
                    total_height += rows * (button_size + button_margin) + 20  # 分类选项高度 + 间距
            
            # 绘制分类文字和选项按钮，考虑滑动偏移
            current_y = display_area_y + 15 - self.生物分类滑动偏移
            
            for category_name, category_info in 植物分类.items():
                if len(category_info["items"]) == 0:
                    continue
                    
                # 绘制分类名称
                category_text = category_info["name"]
                category_surface = self.文本字体.render(category_text, True, (255, 255, 255))
                # 只有当分类名称在显示区域内时才绘制
                if current_y > display_area_y - 30 and current_y < display_area_y + display_area_height:
                    self.屏幕.blit(category_surface, (display_area_x + 20, current_y))
                current_y += 30
                
                # 绘制分类选项按钮
                row = 0
                col = 0
                
                for i, (item_id, display_name) in enumerate(zip(category_info["items"], category_info["display_names"])):
                    # 计算按钮位置，和其他分类的物品格子位置一致
                    button_x = display_area_x + 15 + col * (button_size + button_margin)
                    button_y = current_y + row * (button_size + button_margin)
                    
                    # 检查是否需要换行
                    if button_x + button_size > display_area_x + display_area_width - 30:
                        row += 1
                        col = 0
                        button_x = display_area_x + 15
                        button_y = current_y + row * (button_size + button_margin)
                    
                    # 创建按钮矩形
                    button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
                    
                    # 只有当按钮在显示区域内时才绘制
                    if button_y > display_area_y - button_size and button_y < display_area_y + display_area_height:
                        # 检查鼠标是否悬停
                        mouse_pos = pygame.mouse.get_pos()
                        is_hover = button_rect.collidepoint(mouse_pos)
                        
                        # 设置按钮颜色
                        button_color = (70, 70, 70) if is_hover else (40, 40, 40)
                        
                        # 绘制按钮背景，和其他物品格子一样
                        pygame.draw.rect(self.屏幕, button_color, button_rect, border_radius=4)
                        pygame.draw.rect(self.屏幕, 边框颜色, button_rect, 1, border_radius=4)
                        
                        # 尝试加载并绘制植物图片
                        try:
                            item_image = 获取物品图片(item_id)
                            if item_image:
                                # 缩放图片以适应按钮大小，和其他物品格子一样
                                scaled_image = pygame.transform.scale(item_image, (button_size - 4, button_size - 4))
                                self.屏幕.blit(scaled_image, (button_x + 2, button_y + 2))
                        except Exception:
                            # 如果图片加载失败，绘制植物名称
                            button_text = self.文本字体.render(display_name[:2], True, (200, 200, 200))
                            text_rect = button_text.get_rect(center=button_rect.center)
                            self.屏幕.blit(button_text, text_rect)
                    
                    # 保存按钮信息，用于点击检测
                    self.生物分类按钮.append({
                        "rect": button_rect,
                        "item_id": item_id,
                        "item_name": display_name
                    })
                    
                    col += 1
                
                current_y += (row + 1) * (button_size + button_margin) + 20
        elif current_category == "方块":
            # 方块分类字典
            方块分类 = {
                "自然方块": {
                    "name": "自然方块",
                    "items": [],
                    "display_names": []
                },
                "方块": {
                    "name": "方块",
                    "items": [],
                    "display_names": []
                },
                "功能方块": {
                    "name": "功能方块",
                    "items": [],
                    "display_names": []
                },
                "建筑方块": {
                    "name": "建筑方块",
                    "items": [],
                    "display_names": []
                },
                "其他": {
                    "name": "其他",
                    "items": [],
                    "display_names": []
                }
            }
            
            # 根据物品ID添加到对应的子分类
            for item_id in items:
                item_info = 物品.get(item_id, {})
                item_name = item_info.get("名称", "")
                item_type = item_info.get("类型", "")
                
                # 根据物品名称和类型分类
                # 自然方块：土块，草块，黑土块，沙子，全面原矿石，岩石，岩石底
                if item_name in ["土块", "草方块", "黑土块", "沙子", "煤矿", "红矿石", "蓝矿石", "金矿石", "铁矿石", "铜矿石", "钻石矿石", "岩石", "岩石底"]:
                    方块分类["自然方块"]["items"].append(item_id)
                    方块分类["自然方块"]["display_names"].append(item_name)
                # 方块：木板，金块...
                elif item_name in ["木板", "金块", "铁块", "铜块", "钻石块", "蓝石", "红石", "小煤块", "木炭", "石子"]:
                    方块分类["方块"]["items"].append(item_id)
                    方块分类["方块"]["display_names"].append(item_name)
                # 功能方块：箱子，火把，工作台，熔炉，床
                elif item_name in ["箱子", "火把", "工作台", "熔炉", "床", "床左", "床右", "床整体", "床_整体", "床_完整"]:
                    方块分类["功能方块"]["items"].append(item_id)
                    方块分类["功能方块"]["display_names"].append(item_name)
                # 建筑方块：红方块，蓝方块，紫方块
                elif item_name in ["红方块", "蓝方块", "紫石块", "红石块", "玻璃"]:
                    方块分类["建筑方块"]["items"].append(item_id)
                    方块分类["建筑方块"]["display_names"].append(item_name)
                # 其他：水，岩浆，煤块
                elif item_name in ["水", "岩浆", "煤块"]:
                    方块分类["其他"]["items"].append(item_id)
                    方块分类["其他"]["display_names"].append(item_name)
                # 未分类的方块，添加到方块子分类
                else:
                    方块分类["方块"]["items"].append(item_id)
                    方块分类["方块"]["display_names"].append(item_name)
            
            # 首先计算方块分类选项的总高度
            total_height = 0
            for category_info in 方块分类.values():
                if len(category_info["items"]) > 0:
                    total_height += 30  # 分类名称高度
                    # 计算该分类需要的行数
                    items_count = len(category_info["items"])
                    rows = (items_count + columns - 1) // columns
                    total_height += rows * (button_size + button_margin) + 20  # 分类选项高度 + 间距
            
            # 绘制分类文字和选项按钮，考虑滑动偏移
            current_y = display_area_y + 15 - self.生物分类滑动偏移
            
            for category_name, category_info in 方块分类.items():
                if len(category_info["items"]) == 0:
                    continue
                    
                # 绘制分类名称
                category_text = category_info["name"]
                category_surface = self.文本字体.render(category_text, True, (255, 255, 255))
                # 只有当分类名称在显示区域内时才绘制
                if current_y > display_area_y - 30 and current_y < display_area_y + display_area_height:
                    self.屏幕.blit(category_surface, (display_area_x + 20, current_y))
                current_y += 30
                
                # 绘制分类选项按钮
                row = 0
                col = 0
                
                for i, (item_id, display_name) in enumerate(zip(category_info["items"], category_info["display_names"])):
                    # 计算按钮位置，和其他分类的物品格子位置一致
                    button_x = display_area_x + 15 + col * (button_size + button_margin)
                    button_y = current_y + row * (button_size + button_margin)
                    
                    # 检查是否需要换行
                    if button_x + button_size > display_area_x + display_area_width - 30:
                        row += 1
                        col = 0
                        button_x = display_area_x + 15
                        button_y = current_y + row * (button_size + button_margin)
                    
                    # 创建按钮矩形
                    button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
                    
                    # 只有当按钮在显示区域内时才绘制
                    if button_y > display_area_y - button_size and button_y < display_area_y + display_area_height:
                        # 检查鼠标是否悬停
                        mouse_pos = pygame.mouse.get_pos()
                        is_hover = button_rect.collidepoint(mouse_pos)
                        
                        # 设置按钮颜色
                        button_color = (70, 70, 70) if is_hover else (40, 40, 40)
                        
                        # 绘制按钮背景，和其他物品格子一样
                        pygame.draw.rect(self.屏幕, button_color, button_rect, border_radius=4)
                        pygame.draw.rect(self.屏幕, 边框颜色, button_rect, 1, border_radius=4)
                        
                        # 尝试加载并绘制物品图片
                        try:
                            item_image = 获取物品图片(item_id)
                            if item_image:
                                # 缩放图片以适应按钮大小，和其他物品格子一样
                                scaled_image = pygame.transform.scale(item_image, (button_size - 4, button_size - 4))
                                self.屏幕.blit(scaled_image, (button_x + 2, button_y + 2))
                        except Exception:
                            # 如果图片加载失败，绘制物品名称
                            button_text = self.文本字体.render(display_name[:2], True, (200, 200, 200))
                            text_rect = button_text.get_rect(center=button_rect.center)
                            self.屏幕.blit(button_text, text_rect)
                    
                    # 保存按钮信息，用于点击检测
                    self.生物分类按钮.append({
                        "rect": button_rect,
                        "item_id": item_id,
                        "item_name": display_name
                    })
                    
                    col += 1
                
                current_y += (row + 1) * (button_size + button_margin) + 20
        elif current_category == "工具":
            # 工具分类字典
            工具分类 = {
                "稿子": {
                    "name": "稿子",
                    "items": [],
                    "display_names": []
                },
                "斧头": {
                    "name": "斧头",
                    "items": [],
                    "display_names": []
                },
                "铲子": {
                    "name": "铲子",
                    "items": [],
                    "display_names": []
                },
                "装备": {
                    "name": "装备",
                    "items": [],
                    "display_names": []
                },
                "其他": {
                    "name": "其他",
                    "items": [],
                    "display_names": []
                }
            }
            
            # 根据物品ID添加到对应的子分类
            for item_id in items:
                item_info = 物品.get(item_id, {})
                item_name = item_info.get("名称", "")
                item_type = item_info.get("类型", "")
                
                # 根据物品名称和类型分类
                # 稿子：各种稿子
                if "镐" in item_name or item_type == "pickaxe":
                    工具分类["稿子"]["items"].append(item_id)
                    工具分类["稿子"]["display_names"].append(item_name)
                # 斧头：各种斧头
                elif "斧" in item_name or item_type == "axe":
                    工具分类["斧头"]["items"].append(item_id)
                    工具分类["斧头"]["display_names"].append(item_name)
                # 铲子：各种铲子
                elif "铲" in item_name or item_type == "shovel":
                    工具分类["铲子"]["items"].append(item_id)
                    工具分类["铲子"]["display_names"].append(item_name)
                # 装备：头盔，护甲，靴子等
                elif item_type in ["helmet", "armor", "boots", "special", "equipment"]:
                    工具分类["装备"]["items"].append(item_id)
                    工具分类["装备"]["display_names"].append(item_name)
                # 其他工具
                else:
                    工具分类["其他"]["items"].append(item_id)
                    工具分类["其他"]["display_names"].append(item_name)
            
            # 首先计算工具分类选项的总高度
            total_height = 0
            for category_info in 工具分类.values():
                if len(category_info["items"]) > 0:
                    total_height += 30  # 分类名称高度
                    # 计算该分类需要的行数
                    items_count = len(category_info["items"])
                    rows = (items_count + columns - 1) // columns
                    total_height += rows * (button_size + button_margin) + 20  # 分类选项高度 + 间距
            
            # 绘制分类文字和选项按钮，考虑滑动偏移
            current_y = display_area_y + 15 - self.生物分类滑动偏移
            
            for category_name, category_info in 工具分类.items():
                if len(category_info["items"]) == 0:
                    continue
                    
                # 绘制分类名称
                category_text = category_info["name"]
                category_surface = self.文本字体.render(category_text, True, (255, 255, 255))
                # 只有当分类名称在显示区域内时才绘制
                if current_y > display_area_y - 30 and current_y < display_area_y + display_area_height:
                    self.屏幕.blit(category_surface, (display_area_x + 20, current_y))
                current_y += 30
                
                # 绘制分类选项按钮
                row = 0
                col = 0
                
                for i, (item_id, display_name) in enumerate(zip(category_info["items"], category_info["display_names"])):
                    # 计算按钮位置，和其他分类的物品格子位置一致
                    button_x = display_area_x + 15 + col * (button_size + button_margin)
                    button_y = current_y + row * (button_size + button_margin)
                    
                    # 检查是否需要换行
                    if button_x + button_size > display_area_x + display_area_width - 30:
                        row += 1
                        col = 0
                        button_x = display_area_x + 15
                        button_y = current_y + row * (button_size + button_margin)
                    
                    # 创建按钮矩形
                    button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
                    
                    # 只有当按钮在显示区域内时才绘制
                    if button_y > display_area_y - button_size and button_y < display_area_y + display_area_height:
                        # 检查鼠标是否悬停
                        mouse_pos = pygame.mouse.get_pos()
                        is_hover = button_rect.collidepoint(mouse_pos)
                        
                        # 设置按钮颜色
                        button_color = (70, 70, 70) if is_hover else (40, 40, 40)
                        
                        # 绘制按钮背景，和其他物品格子一样
                        pygame.draw.rect(self.屏幕, button_color, button_rect, border_radius=4)
                        pygame.draw.rect(self.屏幕, 边框颜色, button_rect, 1, border_radius=4)
                        
                        # 尝试加载并绘制物品图片
                        try:
                            item_image = 获取物品图片(item_id)
                            if item_image:
                                # 缩放图片以适应按钮大小，和其他物品格子一样
                                scaled_image = pygame.transform.scale(item_image, (button_size - 4, button_size - 4))
                                self.屏幕.blit(scaled_image, (button_x + 2, button_y + 2))
                        except Exception:
                            # 如果图片加载失败，绘制物品名称
                            button_text = self.文本字体.render(display_name[:2], True, (200, 200, 200))
                            text_rect = button_text.get_rect(center=button_rect.center)
                            self.屏幕.blit(button_text, text_rect)
                    
                    # 保存按钮信息，用于点击检测
                    self.生物分类按钮.append({
                        "rect": button_rect,
                        "item_id": item_id,
                        "item_name": display_name
                    })
                    
                    col += 1
                
                current_y += (row + 1) * (button_size + button_margin) + 20
        elif current_category == "武器":
            # 武器分类字典
            武器分类 = {
                "投掷物": {
                    "name": "投掷物",
                    "items": [],
                    "display_names": []
                },
                "近战武器": {
                    "name": "近战武器",
                    "items": [],
                    "display_names": []
                },
                "远程武器": {
                    "name": "远程武器",
                    "items": [],
                    "display_names": []
                },
                "魔法武器": {
                    "name": "魔法武器",
                    "items": [],
                    "display_names": []
                },
                "黑暗系列": {
                    "name": "黑暗系列",
                    "items": [],
                    "display_names": []
                },
                "科幻机甲系列": {
                    "name": "科幻机甲系列",
                    "items": [],
                    "display_names": []
                },
                "西游系列": {
                    "name": "西游系列",
                    "items": [],
                    "display_names": []
                },
                "龙息系列": {
                    "name": "龙息系列",
                    "items": [],
                    "display_names": []
                },
                "救世主系列": {
                    "name": "救世主系列",
                    "items": [],
                    "display_names": []
                },
                "其他": {
                    "name": "其他",
                    "items": [],
                    "display_names": []
                }
            }
            
            # 根据物品ID添加到对应的子分类
            # 黑暗系列武器列表
            dark_weapons = ["骨弩", "死神的镰刀", "骨刀", "骨弯刀", "超暗黑刺刀", "精美骨刀", "亡灵斧头", "骨矛", "骨头狼牙棒", "尖锐骨头狼牙棒", "普通骨锤"]
            
            # 西游系列武器列表
            west_travel_weapons = ["齐天金箍棒", "齐天ak47", "齐天m4", "齐天短枪"]
            
            # 龙息系列武器列表
            dragon_breath_weapons = ["龙息暗雷", "龙息沧蓝", "龙息蓝核"]
            
            # 救世主系列武器列表
            savior_weapons = ["救世主ak47", "救世主m4", "救世主AWM", "救世主MP5", "救世主ump45", "救世主维克托", "救世主S686", "救世主喷子", "救世主手枪", "救世主RPG", "救世主加特林", "救世主榴弹炮", "救世主弩", "救世主短刀", "救世主短剑", "救世主长剑", "救世能源"]
            
            for item_id in items:
                item_info = 物品.get(item_id, {})
                item_name = item_info.get("名称", "")
                item_type = item_info.get("类型", "")
                
                # 根据物品名称和类型分类
                # 黑暗系列武器
                if item_name in dark_weapons:
                    武器分类["黑暗系列"]["items"].append(item_id)
                    武器分类["黑暗系列"]["display_names"].append(item_name)
                # 龙息系列武器
                elif item_name in dragon_breath_weapons:
                    武器分类["龙息系列"]["items"].append(item_id)
                    武器分类["龙息系列"]["display_names"].append(item_name)
                # 救世主系列武器
                elif item_name in savior_weapons:
                    武器分类["救世主系列"]["items"].append(item_id)
                    武器分类["救世主系列"]["display_names"].append(item_name)
                # 科幻机甲系列武器：未来弩，激光炮，机甲系列武器
                elif item_name in ["未来弩", "激光炮", "机甲弹", "机甲步枪", "机甲冲锋枪", "机甲短枪", "机甲狙击枪A型", "机甲狙击枪B型", "机甲手枪A型", "机甲手枪B型"]:
                    武器分类["科幻机甲系列"]["items"].append(item_id)
                    武器分类["科幻机甲系列"]["display_names"].append(item_name)
                # 西游系列武器：齐天金箍棒
                elif item_name in west_travel_weapons:
                    武器分类["西游系列"]["items"].append(item_id)
                    武器分类["西游系列"]["display_names"].append(item_name)
                # 投掷物：燃烧瓶，手榴弹等
                elif item_name in ["燃烧瓶", "骨头手榴弹"] or "投掷" in item_name or "手榴弹" in item_name:
                    武器分类["投掷物"]["items"].append(item_id)
                    武器分类["投掷物"]["display_names"].append(item_name)
                # 近战武器：各种剑，斧头，刀，狼牙棒等
                elif item_type == "weapon" and item_name not in ["木弓箭", "弩", "未来弩", "激光炮", "步枪", "手枪", "狙击枪", "喷子", "火箭筒", "冲锋枪"] and item_name not in west_travel_weapons:
                    if "剑" in item_name or "刀" in item_name or "斧" in item_name or "矛" in item_name or "戟" in item_name or "狼牙棒" in item_name or "锤" in item_name or "刺刀" in item_name:
                        武器分类["近战武器"]["items"].append(item_id)
                        武器分类["近战武器"]["display_names"].append(item_name)
                    # 魔法武器：各种法杖，电磁发射器等
                    elif "法杖" in item_name or "电磁" in item_name:
                        武器分类["魔法武器"]["items"].append(item_id)
                        武器分类["魔法武器"]["display_names"].append(item_name)
                    else:
                        武器分类["其他"]["items"].append(item_id)
                        武器分类["其他"]["display_names"].append(item_name)
                # 远程武器：弓箭，弩，枪，火箭筒等
                elif item_type in ["weapon", "arrow", "bullet"]:
                    if item_name in ["木弓箭", "弩", "步枪", "手枪", "狙击枪", "喷子", "火箭筒", "木箭", "子弹", "火箭弹"] or ("箭" in item_name or "弹" in item_name or "枪" in item_name or "炮" in item_name) and item_name not in west_travel_weapons:
                        武器分类["远程武器"]["items"].append(item_id)
                        武器分类["远程武器"]["display_names"].append(item_name)
                    else:
                        武器分类["其他"]["items"].append(item_id)
                        武器分类["其他"]["display_names"].append(item_name)
                # 魔法武器：法杖类
                elif "法杖" in item_name:
                    武器分类["魔法武器"]["items"].append(item_id)
                    武器分类["魔法武器"]["display_names"].append(item_name)
                # 其他武器
                else:
                    武器分类["其他"]["items"].append(item_id)
                    武器分类["其他"]["display_names"].append(item_name)
            
            # 首先计算武器分类选项的总高度
            total_height = 0
            for category_info in 武器分类.values():
                if len(category_info["items"]) > 0:
                    total_height += 30  # 分类名称高度
                    # 计算该分类需要的行数
                    items_count = len(category_info["items"])
                    rows = (items_count + columns - 1) // columns
                    total_height += rows * (button_size + button_margin) + 20  # 分类选项高度 + 间距
            
            # 绘制分类文字和选项按钮，考虑滑动偏移
            current_y = display_area_y + 15 - self.生物分类滑动偏移
            
            for category_name, category_info in 武器分类.items():
                if len(category_info["items"]) == 0:
                    continue
                    
                # 绘制分类名称
                category_text = category_info["name"]
                category_surface = self.文本字体.render(category_text, True, (255, 255, 255))
                # 只有当分类名称在显示区域内时才绘制
                if current_y > display_area_y - 30 and current_y < display_area_y + display_area_height:
                    self.屏幕.blit(category_surface, (display_area_x + 20, current_y))
                current_y += 30
                
                # 绘制分类选项按钮
                row = 0
                col = 0
                
                for i, (item_id, display_name) in enumerate(zip(category_info["items"], category_info["display_names"])):
                    # 计算按钮位置，和其他分类的物品格子位置一致
                    button_x = display_area_x + 15 + col * (button_size + button_margin)
                    button_y = current_y + row * (button_size + button_margin)
                    
                    # 检查是否需要换行
                    if button_x + button_size > display_area_x + display_area_width - 30:
                        row += 1
                        col = 0
                        button_x = display_area_x + 15
                        button_y = current_y + row * (button_size + button_margin)
                    
                    # 创建按钮矩形
                    button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
                    
                    # 只有当按钮在显示区域内时才绘制
                    if button_y > display_area_y - button_size and button_y < display_area_y + display_area_height:
                        # 检查鼠标是否悬停
                        mouse_pos = pygame.mouse.get_pos()
                        is_hover = button_rect.collidepoint(mouse_pos)
                        
                        # 设置按钮颜色
                        button_color = (70, 70, 70) if is_hover else (40, 40, 40)
                        
                        # 绘制按钮背景，和其他物品格子一样
                        pygame.draw.rect(self.屏幕, button_color, button_rect, border_radius=4)
                        pygame.draw.rect(self.屏幕, 边框颜色, button_rect, 1, border_radius=4)
                        
                        # 尝试加载并绘制物品图片
                        try:
                            item_image = 获取物品图片(item_id)
                            if item_image:
                                # 缩放图片以适应按钮大小，和其他物品格子一样
                                scaled_image = pygame.transform.scale(item_image, (button_size - 4, button_size - 4))
                                self.屏幕.blit(scaled_image, (button_x + 2, button_y + 2))
                        except Exception:
                            # 如果图片加载失败，绘制物品名称
                            button_text = self.文本字体.render(display_name[:2], True, (200, 200, 200))
                            text_rect = button_text.get_rect(center=button_rect.center)
                            self.屏幕.blit(button_text, text_rect)
                    
                    # 保存按钮信息，用于点击检测
                    self.生物分类按钮.append({
                        "rect": button_rect,
                        "item_id": item_id,
                        "item_name": display_name
                    })
                    
                    col += 1
                
                current_y += (row + 1) * (button_size + button_margin) + 20
        elif current_category == "食品":
            # 食品分类字典
            食品分类 = {
                "药水": {
                    "name": "药水",
                    "items": [],
                    "display_names": []
                },
                "水果": {
                    "name": "水果",
                    "items": [],
                    "display_names": []
                },
                "材料": {
                    "name": "材料",
                    "items": [],
                    "display_names": []
                },
                "美食": {
                    "name": "美食",
                    "items": [],
                    "display_names": []
                }
            }
            
            # 根据物品ID添加到对应的子分类
            for item_id in items:
                item_info = 物品.get(item_id, {})
                item_name = item_info.get("名称", "")
                item_type = item_info.get("类型", "")
                
                # 根据物品名称和类型分类
                # 药水：各种药水
                if "药水" in item_name or "瓶" in item_name or item_type == "potion":
                    食品分类["药水"]["items"].append(item_id)
                    食品分类["药水"]["display_names"].append(item_name)
                # 水果：各种水果
                elif item_name in ["苹果", "香蕉", "橙子", "草莓", "葡萄", "一片西瓜", "刺瓜", "哈密瓜", "大菠萝", "小草莓", "山竹", "杨桃", "柠檬", "桃子", "榴莲", "樱桃", "橘子", "火龙果", "牛油果", "猕猴桃", "芒果", "草莓吗", "荔枝", "菠萝", "蓝莓", "龙眼"] or any(keyword in item_name for keyword in ["果", "瓜", "莓", "桃", "橘", "橙", "樱", "李", "杏", "梨", "梅", "枣", "柿", "椰", "柠", "檬", "芒", "葡", "萄", "蕉", "荔", "枝", "榴", "莲", "龙", "眼", "山", "竹", "杨", "桃", "火", "龙", "果", "牛", "油", "果", "猕", "猴", "桃", "蓝", "莓", "菠", "萝", "杨", "梅", "枇", "杷", "枇", "杷", "石", "榴", "无", "花", "果", "木", "瓜", "西", "瓜", "香", "瓜", "哈", "密", "瓜", "黄", "瓜", "南", "瓜", "冬", "瓜", "甜", "瓜", "丝", "瓜", "苦", "瓜", "金", "瓜", "节", "瓜", "蛇", "瓜", "越", "南", "瓜", "西", "葫", "芦", "瓜", "北", "瓜", "南", "瓜", "冬", "瓜", "甜", "瓜", "丝", "瓜", "苦", "瓜", "金", "瓜", "节", "瓜", "蛇", "瓜", "越", "南", "瓜", "西", "葫", "芦", "瓜", "北", "瓜", "南", "瓜", "冬", "瓜", "甜", "瓜", "丝", "瓜", "苦", "瓜", "金", "瓜", "节", "瓜", "蛇", "瓜", "越", "南", "瓜", "西", "葫", "芦", "瓜", "北", "瓜"]) and item_name not in ["糖果", "果酱"]:
                    食品分类["水果"]["items"].append(item_id)
                    食品分类["水果"]["display_names"].append(item_name)
                # 材料：肉，鸡蛋，土豆，奶油，巧克力，牛奶，玉米，甘，生米番薯，白菜，糖，面粉，甘蔗，生肉
                elif item_name in ["肉", "鸡蛋", "土豆", "奶油", "巧克力", "牛奶", "玉米", "甘", "生米", "番薯", "白菜", "糖", "面粉", "猪肉", "牛肉", "鸡肉", "鱼", "虾", "胡萝卜", "番茄", "洋葱", "甘蔗", "生肉"]:
                    食品分类["材料"]["items"].append(item_id)
                    食品分类["材料"]["display_names"].append(item_name)
                # 美食：各种制作好的食物
                else:
                    食品分类["美食"]["items"].append(item_id)
                    食品分类["美食"]["display_names"].append(item_name)
            
            # 首先计算食品分类选项的总高度
            total_height = 0
            for category_info in 食品分类.values():
                if len(category_info["items"]) > 0:
                    total_height += 30  # 分类名称高度
                    # 计算该分类需要的行数
                    items_count = len(category_info["items"])
                    rows = (items_count + columns - 1) // columns
                    total_height += rows * (button_size + button_margin) + 20  # 分类选项高度 + 间距
            
            # 绘制分类文字和选项按钮，考虑滑动偏移
            current_y = display_area_y + 15 - self.生物分类滑动偏移
            
            for category_name, category_info in 食品分类.items():
                if len(category_info["items"]) == 0:
                    continue
                    
                # 绘制分类名称
                category_text = category_info["name"]
                category_surface = self.文本字体.render(category_text, True, (255, 255, 255))
                # 只有当分类名称在显示区域内时才绘制
                if current_y > display_area_y - 30 and current_y < display_area_y + display_area_height:
                    self.屏幕.blit(category_surface, (display_area_x + 20, current_y))
                current_y += 30
                
                # 绘制分类选项按钮
                row = 0
                col = 0
                
                for i, (item_id, display_name) in enumerate(zip(category_info["items"], category_info["display_names"])):
                    # 计算按钮位置，和其他分类的物品格子位置一致
                    button_x = display_area_x + 15 + col * (button_size + button_margin)
                    button_y = current_y + row * (button_size + button_margin)
                    
                    # 检查是否需要换行
                    if button_x + button_size > display_area_x + display_area_width - 30:
                        row += 1
                        col = 0
                        button_x = display_area_x + 15
                        button_y = current_y + row * (button_size + button_margin)
                    
                    # 创建按钮矩形
                    button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
                    
                    # 只有当按钮在显示区域内时才绘制
                    if button_y > display_area_y - button_size and button_y < display_area_y + display_area_height:
                        # 检查鼠标是否悬停
                        mouse_pos = pygame.mouse.get_pos()
                        is_hover = button_rect.collidepoint(mouse_pos)
                        
                        # 设置按钮颜色
                        button_color = (70, 70, 70) if is_hover else (40, 40, 40)
                        
                        # 绘制按钮背景，和其他物品格子一样
                        pygame.draw.rect(self.屏幕, button_color, button_rect, border_radius=4)
                        pygame.draw.rect(self.屏幕, 边框颜色, button_rect, 1, border_radius=4)
                        
                        # 尝试加载并绘制物品图片
                        try:
                            item_image = 获取物品图片(item_id)
                            if item_image:
                                # 缩放图片以适应按钮大小，和其他物品格子一样
                                scaled_image = pygame.transform.scale(item_image, (button_size - 4, button_size - 4))
                                self.屏幕.blit(scaled_image, (button_x + 2, button_y + 2))
                        except Exception:
                            # 如果图片加载失败，绘制物品名称
                            button_text = self.文本字体.render(display_name[:2], True, (200, 200, 200))
                            text_rect = button_text.get_rect(center=button_rect.center)
                            self.屏幕.blit(button_text, text_rect)
                    
                    # 保存按钮信息，用于点击检测
                    self.生物分类按钮.append({
                        "rect": button_rect,
                        "item_id": item_id,
                        "item_name": display_name
                    })
                    
                    col += 1
                
                current_y += (row + 1) * (button_size + button_margin) + 20

        else:
            # 其他分类，使用普通物品列表
            # 计算物品列表总高度
            items_count = len(items)
            rows = (items_count + columns - 1) // columns
            total_height = rows * (button_size + button_margin) + 20
            
            # 绘制物品格子，考虑滑动偏移
            current_y = display_area_y + 15 - self.生物分类滑动偏移
            
            for i, item_id in enumerate(items):
                row = i // columns
                col = i % columns
                
                # 计算格子位置
                slot_x = display_area_x + 15 + col * (button_size + button_margin)
                slot_y = current_y + row * (button_size + button_margin)
                
                # 创建格子矩形
                slot_rect = pygame.Rect(slot_x, slot_y, button_size, button_size)
                
                # 只有当格子在显示区域内时才绘制
                if slot_y > display_area_y - button_size and slot_y < display_area_y + display_area_height:
                    # 检查鼠标是否悬停
                    mouse_pos = pygame.mouse.get_pos()
                    is_hover = slot_rect.collidepoint(mouse_pos)
                    
                    # 设置格子颜色
                    slot_color = (70, 70, 70) if is_hover else (40, 40, 40)
                    
                    # 绘制格子背景
                    pygame.draw.rect(self.屏幕, slot_color, slot_rect, border_radius=4)
                    pygame.draw.rect(self.屏幕, 边框颜色, slot_rect, 1, border_radius=4)
                    
                    # 尝试加载并绘制物品图片
                    try:
                        item_image = 获取物品图片(item_id)
                        if item_image:
                            # 缩放图片以适应格子
                            scaled_image = pygame.transform.scale(item_image, (button_size - 4, button_size - 4))
                            self.屏幕.blit(scaled_image, (slot_x + 2, slot_y + 2))
                    except Exception:
                        # 如果图片加载失败，绘制物品ID作为文本
                        text = self.文本字体.render(str(item_id)[:2], True, (200, 200, 200))
                        text_rect = text.get_rect(center=(slot_x + button_size//2, slot_y + button_size//2))
                        self.屏幕.blit(text, text_rect)
                
                # 保存按钮信息，用于点击检测
                self.生物分类按钮.append({
                    "rect": slot_rect,
                    "item_id": item_id,
                    "item_name": ""
                })
        
        # 更新总高度和最大滑动偏移，适用于所有分类，增加100滑动距离
        self.生物分类总高度 = total_height
        self.生物分类最大滑动偏移 = max(0, total_height - display_area_height + 20 + 100)
        
        # 限制滑动偏移量
        self.生物分类滑动偏移 = max(0, min(self.生物分类滑动偏移, self.生物分类最大滑动偏移))
        
        # 绘制滚动条，只有当内容超出显示区域时才绘制
        if self.生物分类最大滑动偏移 > 0:
            # 滚动条参数
            scrollbar_width = 8
            scrollbar_x = display_area_x + display_area_width - scrollbar_width - 10
            scrollbar_height = display_area_height - 20
            scrollbar_y = display_area_y + 10
            
            # 滑块参数
            slider_height = max(20, int(scrollbar_height * (display_area_height / self.生物分类总高度)))
            slider_y = scrollbar_y + (self.生物分类滑动偏移 / self.生物分类最大滑动偏移) * (scrollbar_height - slider_height)
            
            # 绘制滚动条背景
            pygame.draw.rect(self.屏幕, (60, 60, 60), 
                            (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height), 
                            border_radius=4)
            # 绘制滑块
            pygame.draw.rect(self.屏幕, (100, 100, 100), 
                            (scrollbar_x, slider_y, scrollbar_width, slider_height), 
                            border_radius=4)
            pygame.draw.rect(self.屏幕, (150, 150, 150), 
                            (scrollbar_x + 1, slider_y + 1, scrollbar_width - 2, slider_height - 2), 
                            border_radius=3)
        
        # 恢复裁剪区域，允许绘制其他UI元素
        self.屏幕.set_clip(None)
    

    
    def get_close_button_rect(self):
        """获取关闭按钮的矩形区域"""
        # 计算关闭按钮的位置，放在左侧面板（底1）的最下方
        button_y = self.底_y + self.底1高度 - 60  # 底部留出一定间距
        return pygame.Rect(
            self.底1_x + 15,
            button_y,
            self.button_width,
            self.button_height
        )
    
    def draw_close_button(self):
        """绘制关闭按钮"""
        close_button_rect = self.get_close_button_rect()
        
        # 绘制按钮背景
        pygame.draw.rect(self.屏幕, 次级背景色, close_button_rect, border_radius=5)
        pygame.draw.rect(self.屏幕, 边框颜色, close_button_rect, 1, border_radius=5)
        
        # 绘制按钮文本
        text = self.文本字体.render("关闭", True, 文本颜色)
        text_rect = text.get_rect(center=close_button_rect.center)
        self.屏幕.blit(text, text_rect)
    
    def handle_event(self, 事件):
        """处理事件"""
        if not self.is_open:
            return False
        
        # 确保底1_x、底2_x和底_y属性已初始化
        if not hasattr(self, '底2_x') or not hasattr(self, '底_y'):
            # 如果属性不存在，先计算它们（与draw方法中的计算逻辑相同）
            self.底1_x = (self.屏幕宽度 - self.底1宽度 - self.间隔 - self.底2宽度) // 2
            self.底2_x = self.底1_x + self.底1宽度 + self.间隔
            self.底_y = (self.屏幕高度 - max(self.底1高度, self.底2高度)) // 2
        
        # 处理ESC键关闭
        if 事件.type == pygame.KEYDOWN:
            if 事件.key == pygame.K_ESCAPE:
                self.is_open = False
                return True
        
        # 计算显示区域，用于生物分类滑动检测
        display_area_x = self.底2_x + 20
        display_area_y = self.底_y + 70
        display_area_width = self.底2宽度 - 40
        display_area_height = self.底2高度 - 140
        
        if 事件.type == pygame.MOUSEBUTTONDOWN:
            # 只有左键点击才处理物品获取
            if 事件.button != 1:  # 1是左键
                return False
                
            mx, my = 事件.pos
            
            # 先处理数量控制区域的点击
            if self.handle_count_control_click(事件):
                return True
            
            # 检查分类按钮点击
            button_start_y = self.底_y + 70
            for i, category in enumerate(self.categories):
                button_y = button_start_y + i * (self.button_height + self.button_spacing)
                button_rect = pygame.Rect(
                    self.底1_x + 15,
                    button_y,
                    self.button_width,
                    self.button_height
                )
                if button_rect.collidepoint(mx, my):
                    self.current_category = i
                    self.生物分类滑动偏移 = 0  # 切换分类时重置滑动偏移
                    return True
            
            # 检查所有分类选项按钮点击（统一处理，包括生物和非生物分类）
            for button in self.生物分类按钮:
                if button["rect"].collidepoint(mx, my):
                    # 将物品添加到玩家快捷栏
                    if self.game and hasattr(self.game, '背包管理器'):
                        print(f"创造背包: 调用add_item_to_hotbar，物品ID: {button['item_id']}")
                        self.add_item_to_hotbar(button['item_id'])
                    else:
                        print(f"创造背包: 无法获取背包管理器，游戏对象: {self.game}, 可用属性: {dir(self.game) if self.game else 'None'}")
                    return True
            
            # 检查物品列表区域的鼠标按下，准备滑动（所有分类都支持滑动）
            if display_area_x <= mx <= display_area_x + display_area_width and \
               display_area_y <= my <= display_area_y + display_area_height:
                # 开始滑动
                self.生物分类是否正在滑动 = True
                self.生物分类鼠标按下位置 = (mx, my)
                self.生物分类鼠标按下时的偏移 = self.生物分类滑动偏移
            
            # 检查关闭按钮点击
            close_button_rect = self.get_close_button_rect()
            if close_button_rect.collidepoint(mx, my):
                self.is_open = False
                return True
        
        elif 事件.type == pygame.MOUSEMOTION:
            # 处理鼠标移动事件
            current_category = self.categories[self.current_category]
            
            # 首先处理物品悬停检测
            self.handle_mouse_motion(事件)
            
            # 处理滑块拖动
            if 事件.buttons[0] == 1:  # 左键按住
                if hasattr(self, 'is_dragging') and self.is_dragging:
                    self.handle_slider_drag(事件)
                
                # 处理物品列表区域的滑动（所有分类都支持滑动）
                elif self.生物分类是否正在滑动:
                    mx, my = 事件.pos
                    # 计算鼠标移动的垂直距离
                    delta_y = my - self.生物分类鼠标按下位置[1]
                    # 更新滑动偏移量
                    self.生物分类滑动偏移 = self.生物分类鼠标按下时的偏移 + delta_y
                    # 限制滑动范围
                    self.生物分类滑动偏移 = max(0, min(self.生物分类滑动偏移, self.生物分类最大滑动偏移))
            
            return True  # 返回True表示事件已处理
        
        elif 事件.type == pygame.MOUSEBUTTONUP:
            # 停止拖动滑块
            if hasattr(self, 'is_dragging'):
                self.is_dragging = False
            
            # 停止生物分类滑动
            self.生物分类是否正在滑动 = False
        
        elif 事件.type == pygame.MOUSEWHEEL:
            # 处理鼠标滚轮事件，实现物品列表上下滑动
            # 检查鼠标是否在显示区域内
            mx, my = pygame.mouse.get_pos()
            if display_area_x <= mx <= display_area_x + display_area_width and \
               display_area_y <= my <= display_area_y + display_area_height:
                # 滚轮滚动距离，正值向上，负值向下
                scroll_distance = 事件.y * 20  # 放大滚动效果，每次滚动20像素
                # 更新滑动偏移量
                self.生物分类滑动偏移 -= scroll_distance
                # 限制滑动范围
                self.生物分类滑动偏移 = max(0, min(self.生物分类滑动偏移, self.生物分类最大滑动偏移))
                return True
        
        return False
    
    def handle_mouse_click(self, 事件):
        """处理鼠标点击事件"""
        # 调用现有的handle_event方法处理鼠标点击
        return self.handle_event(事件)
    
    def handle_count_control_click(self, 事件):
        """处理数量控制区域的点击事件"""
        mx, my = 事件.pos
        
        # 计算控制区域元素位置（向左移动40像素）
        控制区域宽度 = self.物品数量最小值.__str__().__len__() * 30 + self.加减按钮宽度 * 4 + self.滑动区域宽度 + 20
        控制区域_y = self.底_y + self.底2高度 - 40 - 20
        垂直中心 = 控制区域_y + 40 // 2
        
        # 最小按钮位置和尺寸
        最小按钮_x = self.底2_x + self.底2宽度 - 控制区域宽度 - 60
        最小按钮_rect = pygame.Rect(最小按钮_x, 垂直中心 - self.加减按钮高度 // 2, 
                                   self.加减按钮宽度, self.加减按钮高度)
        
        # 减号按钮位置和尺寸
        减号按钮_x = 最小按钮_x + self.加减按钮宽度 + 5
        减号按钮_rect = pygame.Rect(减号按钮_x, 垂直中心 - self.加减按钮高度 // 2, 
                                   self.加减按钮宽度, self.加减按钮高度)
        
        # 滑动区域位置和尺寸
        滑动区域_x = 减号按钮_x + self.加减按钮宽度 + 5
        滑动区域_rect = pygame.Rect(滑动区域_x, 垂直中心 - self.滑动区域高度 // 2, 
                                   self.滑动区域宽度, self.滑动区域高度)
        
        # 加号按钮位置和尺寸
        加号按钮_x = 滑动区域_x + self.滑动区域宽度 + 5
        加号按钮_rect = pygame.Rect(加号按钮_x, 垂直中心 - self.加减按钮高度 // 2, 
                                   self.加减按钮宽度, self.加减按钮高度)
        
        # 最大按钮位置和尺寸
        最大按钮_x = 加号按钮_x + self.加减按钮宽度 + 5
        最大按钮_rect = pygame.Rect(最大按钮_x, 垂直中心 - self.加减按钮高度 // 2, 
                                   self.加减按钮宽度, self.加减按钮高度)
        
        # 处理最小按钮点击
        if 最小按钮_rect.collidepoint(mx, my):
            self.当前物品数量 = self.物品数量最小值
            return True
        
        # 处理减号按钮点击
        elif 减号按钮_rect.collidepoint(mx, my):
            self.当前物品数量 = max(self.物品数量最小值, self.当前物品数量 - 1)
            return True
        
        # 处理滑动区域点击（直接设置滑块位置）
        elif 滑动区域_rect.collidepoint(mx, my):
            self.is_dragging = True
            self.handle_slider_drag(事件)
            return True
        
        # 处理加号按钮点击
        elif 加号按钮_rect.collidepoint(mx, my):
            self.当前物品数量 = min(self.物品数量最大值, self.当前物品数量 + 1)
            return True
        
        # 处理最大按钮点击
        elif 最大按钮_rect.collidepoint(mx, my):
            self.当前物品数量 = self.物品数量最大值
            return True
        
        return False
    
    def handle_slider_drag(self, 事件):
        """处理滑块拖动事件"""
        mx = 事件.pos[0]
        
        # 计算滑动区域位置（向左移动40像素）
        控制区域宽度 = self.物品数量最小值.__str__().__len__() * 30 + self.加减按钮宽度 * 4 + self.滑动区域宽度 + 20
        最小按钮_x = self.底2_x + self.底2宽度 - 控制区域宽度 - 60
        减号按钮_x = 最小按钮_x + self.加减按钮宽度 + 5
        滑动区域_x = 减号按钮_x + self.加减按钮宽度 + 5
        
        # 计算滑块位置比例
        相对位置 = mx - (滑动区域_x + 2)
        最大移动范围 = self.滑动区域宽度 - self.滑块宽度 - 4
        
        if 相对位置 < 0:
            比例 = 0
        elif 相对位置 > 最大移动范围:
            比例 = 1
        else:
            比例 = 相对位置 / 最大移动范围
        
        # 计算当前数量
        self.当前物品数量 = int(self.物品数量最小值 + 比例 * (self.物品数量最大值 - self.物品数量最小值))
        self.当前物品数量 = max(self.物品数量最小值, min(self.物品数量最大值, self.当前物品数量))
    
    def handle_mouse_motion(self, 事件):
        """处理鼠标移动事件，检测物品悬停"""
        if not self.is_open:
            return False
        
        # 确保底2_x和底_y属性已初始化
        if not hasattr(self, '底2_x') or not hasattr(self, '底_y'):
            # 如果属性不存在，先计算它们（与draw方法中的计算逻辑相同）
            self.底1_x = (self.屏幕宽度 - self.底1宽度 - self.间隔 - self.底2宽度) // 2
            self.底2_x = self.底1_x + self.底1宽度 + self.间隔
            self.底_y = (self.屏幕高度 - max(self.底1高度, self.底2高度)) // 2
        
        mx, my = 事件.pos
        
        # 检查是否悬停在物品格子上
        display_area_x = self.底2_x + 20
        display_area_y = self.底_y + 70
        display_area_width = self.底2宽度 - 40
        display_area_height = self.底2高度 - 140
        
        button_size = self.slot_size
        button_margin = self.slot_margin
        columns = self.slots_per_row
        
        # 检查是否悬停在显示区域内
        if not (display_area_x <= mx <= display_area_x + display_area_width and \
                display_area_y <= my <= display_area_y + display_area_height):
            # 鼠标不在显示区域内，清空悬停信息
            self.当前悬停物品 = None
            self.当前悬停物品_rect = None
            return True
        
        # 检查是否悬停在生物或植物分类的按钮上
        current_category = self.categories[self.current_category]
        if current_category == "生物":
            # 生物分类字典
            生物分类 = {
                "boos": {
                    "name": "boos",
                    "items": [21051, 21016, 21061, 21062],  # 贝利亚蛋, 吸血鬼蛋, 肥胖蛋, 死神蛋
                    "display_names": ["贝利亚", "吸血鬼", "肥胖Boss", "死神"]
                },
                "怪物": {
                    "name": "怪物",
                    "items": [21008, 21010, 21024, 21027, 21032, 21046, 21049, 21050, 21052, 21053, 21054, 21055, 21056, 21029, 21030, 21031, 21057],
                    "display_names": ["丧尸", "僵尸", "岩浆怪", "异变者", "异形蜘蛛", "恶魔球", "红眼粘液怪", "蓝怪", "蚂蚁怪物", "超异变者", "邪恶粘液怪", "邪恶蜘蛛", "邪恶蝙蝠", "金怪", "异形眼", "异形球体", "异形蛇", "问灵"]
                },
                "魔物": {
                    "name": "魔物",
                    "items": [21000, 21002, 21004, 21005, 21006, 21013, 21014, 21015, 21017, 21018, 21020, 21025, 21028, 21034, 21039, 21041, 21045, 21059, 21012, 21038, 21019],
                    "display_names": ["史莱姆", "幽灵", "火焰精灵", "蘑菇怪", "岩石怪", "双角骷髅", "变形怪", "可爱幽灵", "夜魔", "大史莱姆", "小恶魔", "幽灵人", "异变骷髅", "普通骷髅", "独眼人", "狼人", "章鱼怪", "骷髅球", "刺球", "牧羊人", "奶龙"]
                },
                "生物": {
                    "name": "生物",
                    "items": [21001, 21003, 21042, 21044, 21058, 21060],
                    "display_names": ["土拨鼠", "蝙蝠", "猪", "章鱼", "霸王龙", "鸟"]
                },
                "动物": {
                    "name": "动物",
                    "items": [21009, 21021, 21022, 21035, 21037, 21043, 21047, 21007, 21011, 21023, 21036],
                    "display_names": ["企鹅", "小熊猫", "小霸王龙", "松鼠", "灰兔", "白兔", "老虎", "三角龙", "猴子", "小鸡", "母鸡"]
                },
                "其他": {
                    "name": "其他",
                    "items": [21048, 21063],
                    "display_names": ["萌刺", "死神祝福"]
                }
            }
            
            # 计算当前滑动偏移后的起始Y坐标
            current_y = display_area_y + 15 - self.生物分类滑动偏移
            
            # 遍历所有生物分类和物品，检查鼠标是否悬停
            for category_name, category_info in 生物分类.items():
                # 跳过分类名称行
                current_y += 30
                
                row = 0
                col = 0
                
                for i, (item_id, display_name) in enumerate(zip(category_info["items"], category_info["display_names"])):
                    # 计算按钮位置
                    button_x = display_area_x + 15 + col * (button_size + button_margin)
                    button_y = current_y + row * (button_size + button_margin)
                    
                    # 检查是否需要换行
                    if button_x + button_size > display_area_x + display_area_width - 30:
                        row += 1
                        col = 0
                        button_x = display_area_x + 15
                        button_y = current_y + row * (button_size + button_margin)
                    
                    # 创建按钮矩形
                    button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
                    
                    # 检查鼠标是否悬停
                    if button_rect.collidepoint(mx, my):
                        # 使用正确的物品定义获取物品信息
                        item_info = 物品.get(item_id, {})
                        # 记录悬停的物品信息和位置
                        self.当前悬停物品 = item_info
                        self.当前悬停物品_rect = button_rect
                        return True
                    
                    col += 1
                
                # 跳过分类间的间距
                current_y += (row + 1) * (button_size + button_margin) + 20
        elif current_category == "植物":
            # 植物分类字典
            植物分类 = {
                "方块": {
                    "name": "方块",
                    "items": [],
                    "display_names": []
                },
                "植物": {
                    "name": "植物",
                    "items": [],
                    "display_names": []
                },
                "种子": {
                    "name": "种子",
                    "items": [],
                    "display_names": []
                },
                "生长状态": {
                    "name": "生长状态",
                    "items": [],
                    "display_names": []
                },
                "其他": {
                    "name": "其他",
                    "items": [],
                    "display_names": []
                }
            }
            
            # 获取当前分类的物品
            items = self.category_items[current_category]
            
            # 根据物品ID添加到对应的子分类
            for item_id in items:
                item_info = 物品.get(item_id, {})
                item_name = item_info.get("名称", "")
                item_type = item_info.get("类型", "")
                
                # 根据物品名称和类型分类
                # 方块：乔木，乔木叶，树叶，木头
                if item_type == "block":
                    if item_name in ["乔木", "乔木叶", "树叶", "木头"]:
                        植物分类["方块"]["items"].append(item_id)
                        植物分类["方块"]["display_names"].append(item_name)
                    # 植物：红花，草，灌木，枯草，仙人掌
                    elif item_name in ["红花", "草", "灌木", "枯草", "仙人掌"]:
                        植物分类["植物"]["items"].append(item_id)
                        植物分类["植物"]["display_names"].append(item_name)
                    # 其他植物相关的生长状态
                    else:
                        植物分类["生长状态"]["items"].append(item_id)
                        植物分类["生长状态"]["display_names"].append(item_name)
                # 种子：各种种子
                elif "种子" in item_name:
                    植物分类["种子"]["items"].append(item_id)
                    植物分类["种子"]["display_names"].append(item_name)
                # 生长状态：各种植物的生长阶段
                elif any(keyword in item_name for keyword in ["发芽", "幼年", "成年", "成熟"]):
                    植物分类["生长状态"]["items"].append(item_id)
                    植物分类["生长状态"]["display_names"].append(item_name)
                # 其他植物相关物品
                else:
                    植物分类["其他"]["items"].append(item_id)
                    植物分类["其他"]["display_names"].append(item_name)
            
            # 计算当前滑动偏移后的起始Y坐标
            current_y = display_area_y + 15 - self.生物分类滑动偏移
            
            # 遍历所有植物分类和物品，检查鼠标是否悬停
            for category_name, category_info in 植物分类.items():
                if len(category_info["items"]) == 0:
                    continue
                    
                # 跳过分类名称行
                current_y += 30
                
                row = 0
                col = 0
                
                for i, (item_id, display_name) in enumerate(zip(category_info["items"], category_info["display_names"])):
                    # 计算按钮位置
                    button_x = display_area_x + 15 + col * (button_size + button_margin)
                    button_y = current_y + row * (button_size + button_margin)
                    
                    # 检查是否需要换行
                    if button_x + button_size > display_area_x + display_area_width - 30:
                        row += 1
                        col = 0
                        button_x = display_area_x + 15
                        button_y = current_y + row * (button_size + button_margin)
                    
                    # 创建按钮矩形
                    button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
                    
                    # 检查鼠标是否悬停
                    if button_rect.collidepoint(mx, my):
                        # 使用正确的物品定义获取物品信息
                        item_info = 物品.get(item_id, {})
                        # 记录悬停的物品信息和位置
                        self.当前悬停物品 = item_info
                        self.当前悬停物品_rect = button_rect
                        return True
                    
                    col += 1
                
                # 跳过分类间的间距
                current_y += (row + 1) * (button_size + button_margin) + 20
        elif current_category == "方块":
            # 方块分类字典
            方块分类 = {
                "自然方块": {
                    "name": "自然方块",
                    "items": [],
                    "display_names": []
                },
                "方块": {
                    "name": "方块",
                    "items": [],
                    "display_names": []
                },
                "功能方块": {
                    "name": "功能方块",
                    "items": [],
                    "display_names": []
                },
                "建筑方块": {
                    "name": "建筑方块",
                    "items": [],
                    "display_names": []
                },
                "其他": {
                    "name": "其他",
                    "items": [],
                    "display_names": []
                }
            }
            
            # 获取当前分类的物品
            items = self.category_items[current_category]
            
            # 根据物品ID添加到对应的子分类
            for item_id in items:
                item_info = 物品.get(item_id, {})
                item_name = item_info.get("名称", "")
                item_type = item_info.get("类型", "")
                
                # 根据物品名称和类型分类
                # 自然方块：土块，草块，黑土块，沙子，全面原矿石，岩石，岩石底
                if item_name in ["土块", "草方块", "黑土块", "沙子", "煤矿", "红矿石", "蓝矿石", "金矿石", "铁矿石", "铜矿石", "钻石矿石", "岩石", "岩石底"]:
                    方块分类["自然方块"]["items"].append(item_id)
                    方块分类["自然方块"]["display_names"].append(item_name)
                # 方块：木板，金块...
                elif item_name in ["木板", "金块", "铁块", "铜块", "钻石块", "蓝石", "红石", "小煤块", "木炭", "石子"]:
                    方块分类["方块"]["items"].append(item_id)
                    方块分类["方块"]["display_names"].append(item_name)
                # 功能方块：箱子，火把，工作台，熔炉，床
                elif item_name in ["箱子", "火把", "工作台", "熔炉", "床", "床左", "床右", "床整体", "床_整体", "床_完整"]:
                    方块分类["功能方块"]["items"].append(item_id)
                    方块分类["功能方块"]["display_names"].append(item_name)
                # 建筑方块：红方块，蓝方块，紫方块
                elif item_name in ["红方块", "蓝方块", "紫石块", "红石块", "玻璃"]:
                    方块分类["建筑方块"]["items"].append(item_id)
                    方块分类["建筑方块"]["display_names"].append(item_name)
                # 其他：水，岩浆，煤块
                elif item_name in ["水", "岩浆", "煤块"]:
                    方块分类["其他"]["items"].append(item_id)
                    方块分类["其他"]["display_names"].append(item_name)
                # 未分类的方块，添加到方块子分类
                else:
                    方块分类["方块"]["items"].append(item_id)
                    方块分类["方块"]["display_names"].append(item_name)
            
            # 计算当前滑动偏移后的起始Y坐标
            current_y = display_area_y + 15 - self.生物分类滑动偏移
            
            # 遍历所有方块分类和物品，检查鼠标是否悬停
            for category_name, category_info in 方块分类.items():
                if len(category_info["items"]) == 0:
                    continue
                    
                # 跳过分类名称行
                current_y += 30
                
                row = 0
                col = 0
                
                for i, (item_id, display_name) in enumerate(zip(category_info["items"], category_info["display_names"])):
                    # 计算按钮位置
                    button_x = display_area_x + 15 + col * (button_size + button_margin)
                    button_y = current_y + row * (button_size + button_margin)
                    
                    # 检查是否需要换行
                    if button_x + button_size > display_area_x + display_area_width - 30:
                        row += 1
                        col = 0
                        button_x = display_area_x + 15
                        button_y = current_y + row * (button_size + button_margin)
                    
                    # 创建按钮矩形
                    button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
                    
                    # 检查鼠标是否悬停
                    if button_rect.collidepoint(mx, my):
                        # 使用正确的物品定义获取物品信息
                        item_info = 物品.get(item_id, {})
                        # 记录悬停的物品信息和位置
                        self.当前悬停物品 = item_info
                        self.当前悬停物品_rect = button_rect
                        return True
                    
                    col += 1
                
                # 跳过分类间的间距
                current_y += (row + 1) * (button_size + button_margin) + 20
        elif current_category == "工具":
            # 工具分类字典
            工具分类 = {
                "稿子": {
                    "name": "稿子",
                    "items": [],
                    "display_names": []
                },
                "斧头": {
                    "name": "斧头",
                    "items": [],
                    "display_names": []
                },
                "铲子": {
                    "name": "铲子",
                    "items": [],
                    "display_names": []
                },
                "装备": {
                    "name": "装备",
                    "items": [],
                    "display_names": []
                },
                "其他": {
                    "name": "其他",
                    "items": [],
                    "display_names": []
                }
            }
            
            # 获取当前分类的物品
            items = self.category_items[current_category]
            
            # 根据物品ID添加到对应的子分类
            for item_id in items:
                item_info = 物品.get(item_id, {})
                item_name = item_info.get("名称", "")
                item_type = item_info.get("类型", "")
                
                # 根据物品名称和类型分类
                # 稿子：各种稿子
                if "镐" in item_name or item_type == "pickaxe":
                    工具分类["稿子"]["items"].append(item_id)
                    工具分类["稿子"]["display_names"].append(item_name)
                # 斧头：各种斧头
                elif "斧" in item_name or item_type == "axe":
                    工具分类["斧头"]["items"].append(item_id)
                    工具分类["斧头"]["display_names"].append(item_name)
                # 铲子：各种铲子
                elif "铲" in item_name or item_type == "shovel":
                    工具分类["铲子"]["items"].append(item_id)
                    工具分类["铲子"]["display_names"].append(item_name)
                # 装备：头盔，护甲，靴子等
                elif item_type in ["helmet", "armor", "boots", "special", "equipment"]:
                    工具分类["装备"]["items"].append(item_id)
                    工具分类["装备"]["display_names"].append(item_name)
                # 其他工具
                else:
                    工具分类["其他"]["items"].append(item_id)
                    工具分类["其他"]["display_names"].append(item_name)
            
            # 计算当前滑动偏移后的起始Y坐标
            current_y = display_area_y + 15 - self.生物分类滑动偏移
            
            # 遍历所有工具分类和物品，检查鼠标是否悬停
            for category_name, category_info in 工具分类.items():
                if len(category_info["items"]) == 0:
                    continue
                    
                # 跳过分类名称行
                current_y += 30
                
                row = 0
                col = 0
                
                for i, (item_id, display_name) in enumerate(zip(category_info["items"], category_info["display_names"])):
                    # 计算按钮位置
                    button_x = display_area_x + 15 + col * (button_size + button_margin)
                    button_y = current_y + row * (button_size + button_margin)
                    
                    # 检查是否需要换行
                    if button_x + button_size > display_area_x + display_area_width - 30:
                        row += 1
                        col = 0
                        button_x = display_area_x + 15
                        button_y = current_y + row * (button_size + button_margin)
                    
                    # 创建按钮矩形
                    button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
                    
                    # 检查鼠标是否悬停
                    if button_rect.collidepoint(mx, my):
                        # 使用正确的物品定义获取物品信息
                        item_info = 物品.get(item_id, {})
                        # 记录悬停的物品信息和位置
                        self.当前悬停物品 = item_info
                        self.当前悬停物品_rect = button_rect
                        return True
                    
                    col += 1
                
                # 跳过分类间的间距
                current_y += (row + 1) * (button_size + button_margin) + 20
        elif current_category == "武器":
            # 武器分类字典 - 与draw_item_list方法完全一致
            武器分类 = {
                "投掷物": {
                    "name": "投掷物",
                    "items": [],
                    "display_names": []
                },
                "近战武器": {
                    "name": "近战武器",
                    "items": [],
                    "display_names": []
                },
                "远程武器": {
                    "name": "远程武器",
                    "items": [],
                    "display_names": []
                },
                "魔法武器": {
                    "name": "魔法武器",
                    "items": [],
                    "display_names": []
                },
                "黑暗系列": {
                    "name": "黑暗系列",
                    "items": [],
                    "display_names": []
                },
                "科幻机甲系列": {
                    "name": "科幻机甲系列",
                    "items": [],
                    "display_names": []
                },
                "西游系列": {
                    "name": "西游系列",
                    "items": [],
                    "display_names": []
                },
                "其他": {
                    "name": "其他",
                    "items": [],
                    "display_names": []
                }
            }
            
            # 获取当前分类的物品
            items = self.category_items[current_category]
            
            # 根据物品ID添加到对应的子分类 - 与draw_item_list方法完全一致
            for item_id in items:
                item_info = 物品.get(item_id, {})
                item_name = item_info.get("名称", "")
                item_type = item_info.get("类型", "")
                
                # 黑暗系列武器列表
                dark_weapons = ["骨弩", "死神的镰刀", "骨刀", "骨弯刀", "超暗黑刺刀", "精美骨刀", "亡灵斧头", "骨矛", "骨头狼牙棒", "尖锐骨头狼牙棒", "普通骨锤"]
                
                # 西游系列武器列表
                west_travel_weapons = ["齐天金箍棒"]
                
                # 根据物品名称和类型分类
                # 黑暗系列武器
                if item_name in dark_weapons:
                    武器分类["黑暗系列"]["items"].append(item_id)
                    武器分类["黑暗系列"]["display_names"].append(item_name)
                # 科幻机甲系列武器：未来弩，激光炮，机甲系列武器
                elif item_name in ["未来弩", "激光炮", "机甲弹", "机甲步枪", "机甲冲锋枪", "机甲短枪", "机甲狙击枪A型", "机甲狙击枪B型", "机甲手枪A型", "机甲手枪B型"]:
                    武器分类["科幻机甲系列"]["items"].append(item_id)
                    武器分类["科幻机甲系列"]["display_names"].append(item_name)
                # 西游系列武器：齐天金箍棒
                elif item_name in west_travel_weapons:
                    武器分类["西游系列"]["items"].append(item_id)
                    武器分类["西游系列"]["display_names"].append(item_name)
                # 投掷物：燃烧瓶，手榴弹等
                elif item_name in ["燃烧瓶", "骨头手榴弹"] or "投掷" in item_name or "手榴弹" in item_name:
                    武器分类["投掷物"]["items"].append(item_id)
                    武器分类["投掷物"]["display_names"].append(item_name)
                # 近战武器：各种剑，斧头，刀，狼牙棒等
                elif item_type == "weapon" and item_name not in ["木弓箭", "弩", "未来弩", "激光炮", "步枪", "手枪", "狙击枪", "喷子", "火箭筒", "冲锋枪"]:
                    if "剑" in item_name or "刀" in item_name or "斧" in item_name or "矛" in item_name or "戟" in item_name or "狼牙棒" in item_name or "锤" in item_name or "刺刀" in item_name:
                        武器分类["近战武器"]["items"].append(item_id)
                        武器分类["近战武器"]["display_names"].append(item_name)
                    # 魔法武器：各种法杖，电磁发射器等
                    elif "法杖" in item_name or "电磁" in item_name:
                        武器分类["魔法武器"]["items"].append(item_id)
                        武器分类["魔法武器"]["display_names"].append(item_name)
                    else:
                        武器分类["其他"]["items"].append(item_id)
                        武器分类["其他"]["display_names"].append(item_name)
                # 远程武器：弓箭，弩，枪，火箭筒等
                elif item_type in ["weapon", "arrow", "bullet"]:
                    if item_name in ["木弓箭", "弩", "未来弩", "激光炮", "步枪", "手枪", "狙击枪", "喷子", "火箭筒", "木箭", "子弹", "火箭弹"] or "箭" in item_name or "弹" in item_name or "枪" in item_name or "炮" in item_name:
                        武器分类["远程武器"]["items"].append(item_id)
                        武器分类["远程武器"]["display_names"].append(item_name)
                    else:
                        武器分类["其他"]["items"].append(item_id)
                        武器分类["其他"]["display_names"].append(item_name)
                # 魔法武器：各种法杖，电磁发射器等
                elif "法杖" in item_name or "电磁" in item_name:
                    武器分类["魔法武器"]["items"].append(item_id)
                    武器分类["魔法武器"]["display_names"].append(item_name)
                # 其他武器
                else:
                    武器分类["其他"]["items"].append(item_id)
                    武器分类["其他"]["display_names"].append(item_name)
            
            # 计算当前滑动偏移后的起始Y坐标
            current_y = display_area_y + 15 - self.生物分类滑动偏移
            
            # 遍历所有武器分类和物品，检查鼠标是否悬停
            for category_name, category_info in 武器分类.items():
                if len(category_info["items"]) == 0:
                    continue
                    
                # 跳过分类名称行
                current_y += 30
                
                row = 0
                col = 0
                
                for i, (item_id, display_name) in enumerate(zip(category_info["items"], category_info["display_names"])):
                    # 计算按钮位置
                    button_x = display_area_x + 15 + col * (button_size + button_margin)
                    button_y = current_y + row * (button_size + button_margin)
                    
                    # 检查是否需要换行
                    if button_x + button_size > display_area_x + display_area_width - 30:
                        row += 1
                        col = 0
                        button_x = display_area_x + 15
                        button_y = current_y + row * (button_size + button_margin)
                    
                    # 创建按钮矩形
                    button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
                    
                    # 检查鼠标是否悬停
                    if button_rect.collidepoint(mx, my):
                        # 使用正确的物品定义获取物品信息
                        item_info = 物品.get(item_id, {})
                        # 记录悬停的物品信息和位置
                        self.当前悬停物品 = item_info
                        self.当前悬停物品_rect = button_rect
                        return True
                    
                    col += 1
                
                # 跳过分类间的间距
                current_y += (row + 1) * (button_size + button_margin) + 20
        elif current_category == "食品":
            # 食品分类字典
            食品分类 = {
                "药水": {
                    "name": "药水",
                    "items": [],
                    "display_names": []
                },
                "水果": {
                    "name": "水果",
                    "items": [],
                    "display_names": []
                },
                "材料": {
                    "name": "材料",
                    "items": [],
                    "display_names": []
                },
                "美食": {
                    "name": "美食",
                    "items": [],
                    "display_names": []
                }
            }
            
            # 获取当前分类的物品
            items = self.category_items[current_category]
            
            # 根据物品ID添加到对应的子分类
            for item_id in items:
                item_info = 物品.get(item_id, {})
                item_name = item_info.get("名称", "")
                item_type = item_info.get("类型", "")
                
                # 根据物品名称和类型分类
                # 药水：各种药水
                if "药水" in item_name or "瓶" in item_name or item_type == "potion":
                    食品分类["药水"]["items"].append(item_id)
                    食品分类["药水"]["display_names"].append(item_name)
                # 水果：各种水果
                elif item_name in ["苹果", "香蕉", "橙子", "草莓", "葡萄", "一片西瓜", "刺瓜", "哈密瓜", "大菠萝", "小草莓", "山竹", "杨桃", "柠檬", "桃子", "榴莲", "樱桃", "橘子", "火龙果", "牛油果", "猕猴桃", "芒果", "草莓吗", "荔枝", "菠萝", "蓝莓", "龙眼"] or any(keyword in item_name for keyword in ["果", "瓜", "莓", "桃", "橘", "橙", "樱", "李", "杏", "梨", "梅", "枣", "柿", "椰", "柠", "檬", "芒", "葡", "萄", "蕉", "荔", "枝", "榴", "莲", "龙", "眼", "山", "竹", "杨", "桃", "火", "龙", "果", "牛", "油", "果", "猕", "猴", "桃", "蓝", "莓", "菠", "萝", "杨", "梅", "枇", "杷", "枇", "杷", "石", "榴", "无", "花", "果", "木", "瓜", "西", "瓜", "香", "瓜", "哈", "密", "瓜", "黄", "瓜", "南", "瓜", "冬", "瓜", "甜", "瓜", "丝", "瓜", "苦", "瓜", "金", "瓜", "节", "瓜", "蛇", "瓜", "越", "南", "瓜", "西", "葫", "芦", "瓜", "北", "瓜", "南", "瓜", "冬", "瓜", "甜", "瓜", "丝", "瓜", "苦", "瓜", "金", "瓜", "节", "瓜", "蛇", "瓜", "越", "南", "瓜", "西", "葫", "芦", "瓜", "北", "瓜", "南", "瓜", "冬", "瓜", "甜", "瓜", "丝", "瓜", "苦", "瓜", "金", "瓜", "节", "瓜", "蛇", "瓜", "越", "南", "瓜", "西", "葫", "芦", "瓜", "北", "瓜"]) and item_name not in ["糖果", "果酱"]:
                    食品分类["水果"]["items"].append(item_id)
                    食品分类["水果"]["display_names"].append(item_name)
                # 材料：肉，鸡蛋，土豆，奶油，巧克力，牛奶，玉米，甘，生米番薯，白菜，糖，面粉，甘蔗，生肉
                elif item_name in ["肉", "鸡蛋", "土豆", "奶油", "巧克力", "牛奶", "玉米", "甘", "生米", "番薯", "白菜", "糖", "面粉", "猪肉", "牛肉", "鸡肉", "鱼", "虾", "胡萝卜", "番茄", "洋葱", "甘蔗", "生肉"]:
                    食品分类["材料"]["items"].append(item_id)
                    食品分类["材料"]["display_names"].append(item_name)
                # 美食：各种制作好的食物
                else:
                    食品分类["美食"]["items"].append(item_id)
                    食品分类["美食"]["display_names"].append(item_name)
            
            # 计算当前滑动偏移后的起始Y坐标
            current_y = display_area_y + 15 - self.生物分类滑动偏移
            
            # 遍历所有食品分类和物品，检查鼠标是否悬停
            for category_name, category_info in 食品分类.items():
                if len(category_info["items"]) == 0:
                    continue
                    
                # 跳过分类名称行
                current_y += 30
                
                row = 0
                col = 0
                
                for i, (item_id, display_name) in enumerate(zip(category_info["items"], category_info["display_names"])):
                    # 计算按钮位置
                    button_x = display_area_x + 15 + col * (button_size + button_margin)
                    button_y = current_y + row * (button_size + button_margin)
                    
                    # 检查是否需要换行
                    if button_x + button_size > display_area_x + display_area_width - 30:
                        row += 1
                        col = 0
                        button_x = display_area_x + 15
                        button_y = current_y + row * (button_size + button_margin)
                    
                    # 创建按钮矩形
                    button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
                    
                    # 检查鼠标是否悬停
                    if button_rect.collidepoint(mx, my):
                        # 使用正确的物品定义获取物品信息
                        item_info = 物品.get(item_id, {})
                        # 记录悬停的物品信息和位置
                        self.当前悬停物品 = item_info
                        self.当前悬停物品_rect = button_rect
                        return True
                    
                    col += 1
                
                # 跳过分类间的间距
                current_y += (row + 1) * (button_size + button_margin) + 20
        else:
            # 普通分类，计算点击的格子索引
            col = (mx - display_area_x - 15) // (self.slot_size + self.slot_margin)
            row = (my - display_area_y - 15) // (self.slot_size + self.slot_margin)
            
            # 计算实际的物品索引，考虑滑动偏移
            items = self.category_items[current_category]
            
            # 根据滑动偏移计算起始行
            scroll_offset = self.生物分类滑动偏移
            start_row = scroll_offset // (self.slot_size + self.slot_margin)
            actual_row = start_row + row
            
            slot_index = actual_row * self.slots_per_row + col
            
            if 0 <= slot_index < len(items):
                item_id = items[slot_index]
                # 修复：使用正确的物品定义获取物品信息
                item_info = 物品.get(item_id, {})
                # 记录悬停的物品信息和位置
                self.当前悬停物品 = item_info
                self.当前悬停物品_rect = pygame.Rect(
                    display_area_x + 15 + col * (self.slot_size + self.slot_margin),
                    display_area_y + 15 + row * (self.slot_size + self.slot_margin),
                    self.slot_size,
                    self.slot_size
                )
                return True
        
        # 鼠标不在物品格子上，清空悬停信息
        self.当前悬停物品 = None
        self.当前悬停物品_rect = None
        
        return True
    
    def add_item_to_hotbar(self, item_id):
        """将物品添加到玩家快捷栏或主背包（当快捷栏满时）"""
        # 导入背包物品类和物品定义
        from 背包 import 物品 as 背包物品
        from 物品定义 import 物品 as 物品定义
        
        # 检查物品是否为工具类物品（工具类物品只能拿1个）
        物品信息 = 物品定义.get(item_id, {})
        物品类型 = 物品信息.get("类型", "其他")
        物品名称 = 物品信息.get("名称", "未知物品")
        是工具类 = 物品类型 in ["weapon", "tool", "helmet", "armor", "boots", "special", "equipment", "axe", "pickaxe", "shovel"]
        
        # 特殊处理救世能源，只能拿1个
        if 物品名称 == "救世能源":
            添加数量 = 1
        else:
            # 根据物品类型确定添加数量
            添加数量 = 1 if 是工具类 else self.当前物品数量
        
        # 终端提示 - 按照用户要求的格式
        print(f"获取{物品名称}*{添加数量}")
        
        # 显示漂浮文字
        self._show_notification(f"拿取{物品名称}*{添加数量}")
        
        # 获取背包管理器
        if self.game and hasattr(self.game, '背包管理器'):
            背包管理器 = self.game.背包管理器
            
            # 尝试添加到快捷栏
            成功 = 背包管理器.添加物品到快捷栏(item_id, 添加数量)
            
            if not 成功:
                # 尝试添加到主背包
                成功 = 背包管理器.添加物品到背包(item_id, 添加数量)
                
                if not 成功:
                    print(f"背包已满，无法添加 {物品名称}")
                    # 显示背包满了的漂浮文字提示
                    self._show_notification("背包已满")
                    # 播放警告音效
                    if hasattr(self.game, '音频管理器'):
                        self.game.音频管理器.播放音效("警告.mp3")
        # else:
        #     print(f"无法获取背包管理器，添加物品失败")