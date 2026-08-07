# 这个文件包含了完整的新箱子页面功能代码

import pygame

# 新箱子页面功能类
class NewChestPageManager:
    def __init__(self, game, ITEMS_global):
        self.game = game
        self.ITEMS = ITEMS_global  # 存储全局ITEMS引用
        self.is_open = False
        self.items = []  # 存储物品 [(item_id, count), ...]
        self.chest_x = 0  # 箱子x坐标
        self.chest_y = 0  # 箱子y坐标
        
    def open_page(self, chest_x=0, chest_y=0):
        """打开新箱子页面"""
        self.is_open = True
        self.chest_x = chest_x  # 存储箱子坐标
        self.chest_y = chest_y
        # 检查是否为玩家放置的箱子
        is_player_placed = hasattr(self.game.world, 'player_placed_chests') and (chest_x, chest_y) in self.game.world.player_placed_chests
        # 从World类获取该坐标箱子的物品数据，传递是否为玩家放置的箱子参数
        self.items = self.game.world.get_chest_items(chest_x, chest_y, is_player_placed).copy()
        # 关闭其他界面
        self.game.player.is_inventory_open = False
        self.game.player.is_crafting_open = False
        self.game.player.is_chest_open = False
        self.game.player.current_chest = None
        
    def close_page(self):
        """关闭新箱子页面"""
        # 保存当前箱子的物品数据回World类
        if self.chest_x != 0 or self.chest_y != 0:
            self.game.world.set_chest_items(self.chest_x, self.chest_y, self.items)
        self.is_open = False
        # 记录关闭页面日志
        import time
        print(f"[{time.strftime('%H:%M:%S')}] 玩家关闭新箱子页面")
        
    def handle_click(self, mx, my, button=1):
        """处理新箱子页面的点击事件，button=1表示左键，button=3表示右键"""
        if not self.is_open:
            return
            
        # 如果正在拖动物品，则只允许左键点击（防止物品消失）
        if self.game.player.dragging_item and button == 3:
            return
            
        # 界面参数 - 调整宽度以更紧凑地容纳16列箱子格
        inv_width = 800
        inv_height = 600
        # Get screen dimensions directly from Pygame
        screen_width, screen_height = pygame.display.get_surface().get_size()
        inv_x = (screen_width - inv_width) // 2
        inv_y = (screen_height - inv_height) // 2
        
        # 检查是否点击了关闭按钮
        close_button_rect = pygame.Rect(inv_x + inv_width - 35, inv_y + 5, 30, 30)
        if close_button_rect.collidepoint(mx, my):
            self.close_page()
            return
            
        # 检查是否点击了页面外部区域关闭
        page_rect = pygame.Rect(inv_x, inv_y, inv_width, inv_height)
        if not page_rect.collidepoint(mx, my):
            self.close_page()
            return
        
        # 新箱子格子参数
        chest_rows = 5
        chest_cols = 16
        slot_size = 40
        slot_margin = 5
        chest_start_x = inv_x + 50
        chest_start_y = inv_y + 80
        
        # 检查是否点击了新箱子格子
        chest_rect = pygame.Rect(chest_start_x, chest_start_y,
                               chest_cols * (slot_size + slot_margin), 
                               chest_rows * (slot_size + slot_margin))
        
        if chest_rect.collidepoint(mx, my):
            # 计算点击的箱子槽位索引
            col = (mx - chest_start_x) // (slot_size + slot_margin)
            row = (my - chest_start_y) // (slot_size + slot_margin)
            slot_idx = row * chest_cols + col
            
            if 0 <= slot_idx < chest_rows * chest_cols:
                if self.game.player.dragging_item:
                    # 放置物品到新箱子
                    self._place_item_in_slot(slot_idx)
                else:
                    if button == 3:  # 右键点击
                        # 右键点击拿取一半物品
                        # 确保items列表有足够的空间
                        while len(self.items) <= slot_idx:
                            self.items.append([0, 0])
                        
                        if self.items[slot_idx][0] != 0:
                            item_id, count = self.items[slot_idx]
                            
                            # 如果物品数量大于1，允许右键拿取一半
                            if count > 1:
                                # 计算要拿取的数量（向下取整）
                                half_count = count // 2
                                
                                # 从原槽位中减去拿取的数量
                                self.items[slot_idx] = [item_id, count - half_count]
                                
                                # 开始拖动拿取的物品
                                self.game.player.dragging_item = {"item_id": item_id, "quantity": half_count}
                                self.game.player.dragging_source = "new_chest"
                                self.game.player.dragging_slot = slot_idx
                                self.game.player.is_split_dragging = True  # 标记为右键拆分的物品拖动
                    else:  # 左键点击
                        # 从新箱子取出物品
                        self._take_item_from_slot(slot_idx)
        
        # 检查是否点击了背包格子
        backpack_rows = 3
        backpack_cols = 9
        backpack_start_x = inv_x + 50
        backpack_start_y = inv_y + 330
        backpack_rect = pygame.Rect(backpack_start_x, backpack_start_y,
                                  backpack_cols * (slot_size + slot_margin),
                                  backpack_rows * (slot_size + slot_margin))
        
        if backpack_rect.collidepoint(mx, my):
            # 计算点击的背包槽位索引
            col = (mx - backpack_start_x) // (slot_size + slot_margin)
            row = (my - backpack_start_y) // (slot_size + slot_margin)
            backpack_slot_idx = row * backpack_cols + col
            
            if 0 <= backpack_slot_idx < 27:  # 27个背包格子
                if self.game.player.dragging_item:
                    # 放置物品到背包
                    self._place_item_in_backpack(backpack_slot_idx)
                else:
                    if button == 3:  # 右键点击
                        # 右键点击背包物品拿取一半
                        if hasattr(self.game.player, 'inventory') and backpack_slot_idx < len(self.game.player.inventory):
                            item = self.game.player.inventory[backpack_slot_idx]
                            if item:
                                item_id, count = item
                                
                                # 如果物品数量大于1，允许右键拿取一半
                                if count > 1:
                                    # 计算要拿取的数量（向下取整）
                                    half_count = count // 2
                                    
                                    # 从原槽位中减去拿取的数量
                                    self.game.player.inventory[backpack_slot_idx] = (item_id, count - half_count)
                                    
                                    # 开始拖动拿取的物品
                                    self.game.player.dragging_item = {"item_id": item_id, "quantity": half_count}
                                    self.game.player.dragging_source = "backpack"
                                    self.game.player.dragging_slot = backpack_slot_idx
                                    self.game.player.is_split_dragging = True  # 标记为右键拆分的物品拖动
                    else:  # 左键点击
                        # 从背包取出物品
                        self._take_item_from_backpack(backpack_slot_idx)
        
        # 检查是否点击了快捷栏格子
        hotbar_cols = 9
        hotbar_start_x = inv_x + 50
        hotbar_start_y = inv_y + 510
        hotbar_rect = pygame.Rect(hotbar_start_x, hotbar_start_y,
                                hotbar_cols * (slot_size + slot_margin),
                                slot_size + slot_margin)
        
        if hotbar_rect.collidepoint(mx, my):
            # 计算点击的快捷栏槽位索引
            col = (mx - hotbar_start_x) // (slot_size + slot_margin)
            hotbar_slot_idx = col
            
            if 0 <= hotbar_slot_idx < 9:  # 9个快捷栏格子
                if self.game.player.dragging_item:
                    # 放置物品到快捷栏
                    self._place_item_in_hotbar(hotbar_slot_idx)
                else:
                    if button == 3:  # 右键点击
                        # 右键点击快捷栏物品拿取一半
                        if hasattr(self.game.player, 'hotbar') and hotbar_slot_idx < len(self.game.player.hotbar):
                            item = self.game.player.hotbar[hotbar_slot_idx]
                            if item:
                                item_id, count = item
                                
                                # 如果物品数量大于1，允许右键拿取一半
                                if count > 1:
                                    # 计算要拿取的数量（向下取整）
                                    half_count = count // 2
                                    
                                    # 从原槽位中减去拿取的数量
                                    self.game.player.hotbar[hotbar_slot_idx] = (item_id, count - half_count)
                                    
                                    # 开始拖动拿取的物品
                                    self.game.player.dragging_item = {"item_id": item_id, "quantity": half_count}
                                    self.game.player.dragging_source = "hotbar"
                                    self.game.player.dragging_slot = hotbar_slot_idx
                                    self.game.player.is_split_dragging = True  # 标记为右键拆分的物品拖动
                    else:  # 左键点击
                        # 从快捷栏取出物品
                        self._take_item_from_hotbar(hotbar_slot_idx)
    
    def _is_tool_or_equipment(self, item_id):
        """判断物品是否为工具或装备类型"""
        item_info = self.ITEMS.get(item_id)
        if item_info:
            # 检查物品类型是否为工具或装备（包括所有需要堆叠上限为1的物品类型）
            return item_info.get("type") in ["weapon", "pickaxe", "axe", "shovel", "helmet", "armor", "boots", "special"]
        return False
        
    def _place_item_in_slot(self, slot_idx):
        """将拖动的物品放置到指定槽位，实现物品堆叠上限功能"""
        item_id = self.game.player.dragging_item["item_id"]
        quantity = self.game.player.dragging_item["quantity"]
        source = self.game.player.dragging_source
        source_slot = self.game.player.dragging_slot
        
        # 确保items列表有足够的空间
        while len(self.items) <= slot_idx:
            self.items.append([0, 0])
        
        # 获取物品堆叠上限
        is_tool_or_equipment = self._is_tool_or_equipment(item_id)
        max_stack = 1 if is_tool_or_equipment else 99
        
        # 目标槽位现有物品
        existing_id, existing_count = self.items[slot_idx]
        
        if existing_id == 0:
            # 如果槽位为空，放置物品（不超过堆叠上限）
            placed_quantity = min(quantity, max_stack)
            self.items[slot_idx] = [item_id, placed_quantity]
            
            # 计算剩余数量
            remaining_quantity = quantity - placed_quantity
            
            if remaining_quantity > 0:
                # 如果有剩余物品，放回原位置
                if source == "new_chest":
                    self.items[source_slot] = [item_id, remaining_quantity]
                elif source == "backpack" and hasattr(self.game.player, 'inventory') and source_slot < len(self.game.player.inventory):
                    self.game.player.inventory[source_slot] = [item_id, remaining_quantity]
                elif source == "hotbar" and hasattr(self.game.player, 'hotbar') and source_slot < len(self.game.player.hotbar):
                    self.game.player.hotbar[source_slot] = [item_id, remaining_quantity]
                else:
                    # 如果源位置不存在或无效，保留拖动状态
                    self.game.player.dragging_item = {"item_id": item_id, "quantity": remaining_quantity}
                    return
                
            # 清除拖动状态
            self.game.player.dragging_item = None
            self.game.player.dragging_source = None
            self.game.player.dragging_slot = None
        elif existing_id == item_id:
            # 如果槽位有相同物品，尝试合并
            total_count = existing_count + quantity
            
            if total_count <= max_stack:
                # 如果合并后不超过上限，直接合并
                self.items[slot_idx] = [item_id, total_count]
                # 清除拖动状态
                self.game.player.dragging_item = None
                self.game.player.dragging_source = None
                self.game.player.dragging_slot = None
            else:
                # 如果合并后超过上限，只放置部分物品
                placed_quantity = max_stack - existing_count
                self.items[slot_idx] = [item_id, max_stack]
                remaining_quantity = quantity - placed_quantity
                
                # 将剩余物品放回原位置
                if source == "new_chest":
                    self.items[source_slot] = [item_id, remaining_quantity]
                elif source == "backpack" and hasattr(self.game.player, 'inventory') and source_slot < len(self.game.player.inventory):
                    self.game.player.inventory[source_slot] = [item_id, remaining_quantity]
                elif source == "hotbar" and hasattr(self.game.player, 'hotbar') and source_slot < len(self.game.player.hotbar):
                    self.game.player.hotbar[source_slot] = [item_id, remaining_quantity]
                else:
                    # 如果源位置不存在或无效，保留拖动状态
                    self.game.player.dragging_item = {"item_id": item_id, "quantity": remaining_quantity}
                    return
                
                # 清除拖动状态
                self.game.player.dragging_item = None
                self.game.player.dragging_source = None
                self.game.player.dragging_slot = None
    
    def _take_item_from_slot(self, slot_idx):
        """从指定槽位取出物品"""
        if slot_idx < len(self.items) and self.items[slot_idx][0] != 0:
            item_id, quantity = self.items[slot_idx]
            self.game.player.dragging_item = {"item_id": item_id, "quantity": quantity}
            self.game.player.dragging_source = "new_chest"
            self.game.player.dragging_slot = slot_idx
            self.items[slot_idx] = [0, 0]
    
    def _place_item_in_backpack(self, slot_idx):
        """将拖动的物品放置到背包槽位，实现物品堆叠上限功能"""
        item_id = self.game.player.dragging_item["item_id"]
        quantity = self.game.player.dragging_item["quantity"]
        source = self.game.player.dragging_source
        source_slot = self.game.player.dragging_slot
        
        # 确保背包有足够的空间
        if not hasattr(self.game.player, 'inventory'):
            self.game.player.inventory = []
        while len(self.game.player.inventory) <= slot_idx:
            self.game.player.inventory.append([0, 0])
        
        # 获取物品堆叠上限
        is_tool_or_equipment = self._is_tool_or_equipment(item_id)
        max_stack = 1 if is_tool_or_equipment else 99
        
        # 目标槽位现有物品
        existing_id, existing_count = self.game.player.inventory[slot_idx]
        
        if existing_id == 0:
            # 如果槽位为空，放置物品（不超过堆叠上限）
            placed_quantity = min(quantity, max_stack)
            self.game.player.inventory[slot_idx] = [item_id, placed_quantity]
            
            # 计算剩余数量
            remaining_quantity = quantity - placed_quantity
            
            if remaining_quantity > 0:
                # 如果有剩余物品，放回原位置
                if source == "new_chest" and source_slot < len(self.items):
                    self.items[source_slot] = [item_id, remaining_quantity]
                elif source == "backpack" and source_slot < len(self.game.player.inventory):
                    self.game.player.inventory[source_slot] = [item_id, remaining_quantity]
                elif source == "hotbar" and hasattr(self.game.player, 'hotbar') and source_slot < len(self.game.player.hotbar):
                    self.game.player.hotbar[source_slot] = [item_id, remaining_quantity]
                else:
                    # 如果源位置不存在或无效，保留拖动状态
                    self.game.player.dragging_item = {"item_id": item_id, "quantity": remaining_quantity}
                    return
                
            # 清除拖动状态
            self.game.player.dragging_item = None
            self.game.player.dragging_source = None
            self.game.player.dragging_slot = None
        elif existing_id == item_id:
            # 如果槽位有相同物品，尝试合并
            total_count = existing_count + quantity
            
            if total_count <= max_stack:
                # 如果合并后不超过上限，直接合并
                self.game.player.inventory[slot_idx] = [item_id, total_count]
                # 清除拖动状态
                self.game.player.dragging_item = None
                self.game.player.dragging_source = None
                self.game.player.dragging_slot = None
            else:
                # 如果合并后超过上限，只放置部分物品
                placed_quantity = max_stack - existing_count
                self.game.player.inventory[slot_idx] = [item_id, max_stack]
                remaining_quantity = quantity - placed_quantity
                
                # 将剩余物品放回原位置
                if source == "new_chest" and source_slot < len(self.items):
                    self.items[source_slot] = [item_id, remaining_quantity]
                elif source == "backpack" and source_slot < len(self.game.player.inventory):
                    self.game.player.inventory[source_slot] = [item_id, remaining_quantity]
                elif source == "hotbar" and hasattr(self.game.player, 'hotbar') and source_slot < len(self.game.player.hotbar):
                    self.game.player.hotbar[source_slot] = [item_id, remaining_quantity]
                else:
                    # 如果源位置不存在或无效，保留拖动状态
                    self.game.player.dragging_item = {"item_id": item_id, "quantity": remaining_quantity}
                    return
                
                # 清除拖动状态
                self.game.player.dragging_item = None
                self.game.player.dragging_source = None
                self.game.player.dragging_slot = None
    
    def _take_item_from_backpack(self, slot_idx):
        """从背包槽位取出物品"""
        if hasattr(self.game.player, 'inventory') and slot_idx < len(self.game.player.inventory):
            item = self.game.player.inventory[slot_idx]
            if item[0] != 0 and item[1] > 0:
                item_id, quantity = item
                self.game.player.dragging_item = {"item_id": item_id, "quantity": quantity}
                self.game.player.dragging_source = "backpack"
                self.game.player.dragging_slot = slot_idx
                self.game.player.inventory[slot_idx] = [0, 0]
    
    def _place_item_in_hotbar(self, slot_idx):
        """将拖动的物品放置到快捷栏槽位，实现物品堆叠上限功能"""
        item_id = self.game.player.dragging_item["item_id"]
        quantity = self.game.player.dragging_item["quantity"]
        source = self.game.player.dragging_source
        source_slot = self.game.player.dragging_slot
        
        # 确保快捷栏有足够的空间
        if not hasattr(self.game.player, 'hotbar'):
            self.game.player.hotbar = []
        while len(self.game.player.hotbar) <= slot_idx:
            self.game.player.hotbar.append([0, 0])
        
        # 获取物品堆叠上限
        is_tool_or_equipment = self._is_tool_or_equipment(item_id)
        max_stack = 1 if is_tool_or_equipment else 99
        
        # 目标槽位现有物品
        existing_id, existing_count = self.game.player.hotbar[slot_idx]
        
        if existing_id == 0:
            # 如果槽位为空，放置物品（不超过堆叠上限）
            placed_quantity = min(quantity, max_stack)
            self.game.player.hotbar[slot_idx] = [item_id, placed_quantity]
            
            # 计算剩余数量
            remaining_quantity = quantity - placed_quantity
            
            if remaining_quantity > 0:
                # 如果有剩余物品，放回原位置
                if source == "new_chest" and source_slot < len(self.items):
                    self.items[source_slot] = [item_id, remaining_quantity]
                elif source == "backpack" and hasattr(self.game.player, 'inventory') and source_slot < len(self.game.player.inventory):
                    self.game.player.inventory[source_slot] = [item_id, remaining_quantity]
                elif source == "hotbar" and source_slot < len(self.game.player.hotbar):
                    self.game.player.hotbar[source_slot] = [item_id, remaining_quantity]
                else:
                    # 如果源位置不存在或无效，保留拖动状态
                    self.game.player.dragging_item = {"item_id": item_id, "quantity": remaining_quantity}
                    return
                
            # 清除拖动状态
            self.game.player.dragging_item = None
            self.game.player.dragging_source = None
            self.game.player.dragging_slot = None
        elif existing_id == item_id:
            # 如果槽位有相同物品，尝试合并
            total_count = existing_count + quantity
            
            if total_count <= max_stack:
                # 如果合并后不超过上限，直接合并
                self.game.player.hotbar[slot_idx] = [item_id, total_count]
                # 清除拖动状态
                self.game.player.dragging_item = None
                self.game.player.dragging_source = None
                self.game.player.dragging_slot = None
            else:
                # 如果合并后超过上限，只放置部分物品
                placed_quantity = max_stack - existing_count
                self.game.player.hotbar[slot_idx] = [item_id, max_stack]
                remaining_quantity = quantity - placed_quantity
                
                # 将剩余物品放回原位置
                if source == "new_chest" and source_slot < len(self.items):
                    self.items[source_slot] = [item_id, remaining_quantity]
                elif source == "backpack" and hasattr(self.game.player, 'inventory') and source_slot < len(self.game.player.inventory):
                    self.game.player.inventory[source_slot] = [item_id, remaining_quantity]
                elif source == "hotbar" and source_slot < len(self.game.player.hotbar):
                    self.game.player.hotbar[source_slot] = [item_id, remaining_quantity]
                else:
                    # 如果源位置不存在或无效，保留拖动状态
                    self.game.player.dragging_item = {"item_id": item_id, "quantity": remaining_quantity}
                    return
                
                # 清除拖动状态
                self.game.player.dragging_item = None
                self.game.player.dragging_source = None
                self.game.player.dragging_slot = None
    
    def _take_item_from_hotbar(self, slot_idx):
        """从快捷栏槽位取出物品"""
        if hasattr(self.game.player, 'hotbar') and slot_idx < len(self.game.player.hotbar):
            item = self.game.player.hotbar[slot_idx]
            if item[0] != 0 and item[1] > 0:
                item_id, quantity = item
                self.game.player.dragging_item = {"item_id": item_id, "quantity": quantity}
                self.game.player.dragging_source = "hotbar"
                self.game.player.dragging_slot = slot_idx
                self.game.player.hotbar[slot_idx] = [0, 0]
    
    def draw(self, screen):
        """绘制新箱子页面"""
        if not self.is_open:
            return None
        
        # 获取屏幕尺寸
        WIDTH, HEIGHT = screen.get_size()
        
        # 创建必要的字体
        chinese_fonts = ["SimHei", "Microsoft YaHei", "NSimSun", "SimSun"]
        
        # 尝试加载中文字体，加载失败则使用默认字体
        def load_font(size=16, bold=False):
            for font_name in chinese_fonts:
                try:
                    font = pygame.font.SysFont(font_name, size, bold=bold)
                    # 测试是否能正常渲染中文
                    test_text = font.render("测试", True, (255, 255, 255))
                    return font
                except:
                    continue
            # 如果都失败了，使用默认字体
            return pygame.font.SysFont(None, size, bold=bold)
            
        # 创建不同大小的字体
        font_small = load_font(16)
        font_medium = load_font(20)
        font_large = load_font(24, bold=True)
        
        # 界面参数 - 调整宽度以更紧凑地容纳16列箱子格
        inv_width = 800
        inv_height = 600
        inv_x = (WIDTH - inv_width) // 2
        inv_y = (HEIGHT - inv_height) // 2
        
        # 绘制半透明背景
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # 绘制主界面背景
        main_bg = pygame.Surface((inv_width, inv_height), pygame.SRCALPHA)
        main_bg.fill((60, 60, 60, 240))
        pygame.draw.rect(main_bg, (80, 80, 80), (0, 0, inv_width, inv_height), 3, 10)
        screen.blit(main_bg, (inv_x, inv_y))
        
        # 绘制标题 - 显示箱子坐标
        title_text = font_large.render(f"箱子（x={self.chest_x}, y={self.chest_y}）", True, (255, 255, 255))
        title_x = inv_x + (inv_width - title_text.get_width()) // 2
        screen.blit(title_text, (title_x, inv_y + 15))
        
        # 绘制关闭按钮
        close_button_rect = pygame.Rect(inv_x + inv_width - 35, inv_y + 5, 30, 30)
        mouse_pos = pygame.mouse.get_pos()
        is_close_hovered = close_button_rect.collidepoint(mouse_pos)
        
        close_color = (200, 60, 60) if is_close_hovered else (150, 50, 50)
        pygame.draw.rect(screen, close_color, close_button_rect, 0, 5)
        pygame.draw.rect(screen, (255, 255, 255), close_button_rect, 2, 5)
        
        close_text = font_medium.render("×", True, (255, 255, 255))
        close_text_x = close_button_rect.x + (close_button_rect.width - close_text.get_width()) // 2
        close_text_y = close_button_rect.y + (close_button_rect.height - close_text.get_height()) // 2
        screen.blit(close_text, (close_text_x, close_text_y))
        
        # 新箱子格子参数
        chest_rows = 5
        chest_cols = 16
        slot_size = 40
        slot_margin = 5
        chest_start_x = inv_x + 40
        chest_start_y = inv_y + 80
        
        # 绘制箱子格子背景
        chest_bg_width = chest_cols * (slot_size + slot_margin) + 20
        chest_bg_height = chest_rows * (slot_size + slot_margin) + 20
        chest_bg_rect = pygame.Rect(chest_start_x - 10, chest_start_y - 10, chest_bg_width, chest_bg_height)
        pygame.draw.rect(screen, (40, 40, 40), chest_bg_rect, 0, 5)
        pygame.draw.rect(screen, (80, 80, 80), chest_bg_rect, 2, 5)
        
        # 绘制箱子格子
        for row in range(chest_rows):
            for col in range(chest_cols):
                slot_idx = row * chest_cols + col
                x = chest_start_x + col * (slot_size + slot_margin)
                y = chest_start_y + row * (slot_size + slot_margin)
                slot_rect = pygame.Rect(x, y, slot_size, slot_size)
                
                # 格子背景
                is_slot_hovered = slot_rect.collidepoint(mouse_pos)
                slot_color = (70, 70, 70) if is_slot_hovered else (50, 50, 50)
                pygame.draw.rect(screen, slot_color, slot_rect, 0, 3)
                pygame.draw.rect(screen, (100, 100, 100), slot_rect, 1, 3)
                
                # 绘制物品
                if slot_idx < len(self.items) and self.items[slot_idx][0] != 0:
                    item_id, count = self.items[slot_idx]
                    item_info = self.ITEMS.get(item_id)
                    
                    if item_info:
                        # 绘制物品图标或颜色块
                        if item_info["texture"] in self.game.image_loader.images:
                            item_image = pygame.transform.scale(
                                self.game.image_loader.images[item_info["texture"]], 
                                (slot_size - 6, slot_size - 6)
                            )
                            screen.blit(item_image, (x + 3, y + 3))
                        else:
                            pygame.draw.rect(screen, item_info["color"], 
                                           (x + 3, y + 3, slot_size - 6, slot_size - 6))
                        
                        # 绘制数量
                        if count > 1:
                            count_text = font_small.render(str(count), True, (255, 255, 255))
                            count_bg = pygame.Surface((count_text.get_width() + 4, count_text.get_height() + 2), pygame.SRCALPHA)
                            count_bg.fill((0, 0, 0, 180))
                            screen.blit(count_bg, (x + slot_size - count_text.get_width() - 6, y + slot_size - count_text.get_height() - 4))
                            screen.blit(count_text, (x + slot_size - count_text.get_width() - 4, y + slot_size - count_text.get_height() - 2))
                
        # 绘制背包格
        backpack_title = font_medium.render("背包", True, (255, 255, 255))
        backpack_title_x = inv_x + 50
        backpack_title_y = inv_y + 300
        screen.blit(backpack_title, (backpack_title_x, backpack_title_y))
        
        # 背包格子参数
        backpack_rows = 3
        backpack_cols = 9
        backpack_start_x = inv_x + 50
        backpack_start_y = inv_y + 330
        
        # 绘制背包格子背景
        backpack_bg_width = backpack_cols * (slot_size + slot_margin) + 20
        backpack_bg_height = backpack_rows * (slot_size + slot_margin) + 20
        backpack_bg_rect = pygame.Rect(backpack_start_x - 10, backpack_start_y - 10, backpack_bg_width, backpack_bg_height)
        pygame.draw.rect(screen, (40, 40, 40), backpack_bg_rect, 0, 5)
        pygame.draw.rect(screen, (80, 80, 80), backpack_bg_rect, 2, 5)
        
        # 绘制背包格子
        for row in range(backpack_rows):
            for col in range(backpack_cols):
                x = backpack_start_x + col * (slot_size + slot_margin)
                y = backpack_start_y + row * (slot_size + slot_margin)
                slot_rect = pygame.Rect(x, y, slot_size, slot_size)
                
                # 格子背景
                is_slot_hovered = slot_rect.collidepoint(mouse_pos)
                slot_color = (70, 70, 70) if is_slot_hovered else (50, 50, 50)
                pygame.draw.rect(screen, slot_color, slot_rect, 0, 3)
                pygame.draw.rect(screen, (100, 100, 100), slot_rect, 1, 3)
                
                # 尝试获取玩家背包物品并绘制
                player_inventory_slot = row * backpack_cols + col
                if hasattr(self.game.player, 'inventory') and player_inventory_slot < len(self.game.player.inventory):
                    item = self.game.player.inventory[player_inventory_slot]
                    if item:
                        item_id, count = item
                        item_info = self.ITEMS.get(item_id)
                        
                        if item_info:
                            # 绘制物品图标或颜色块
                            if item_info["texture"] in self.game.image_loader.images:
                                item_image = pygame.transform.scale(
                                    self.game.image_loader.images[item_info["texture"]], 
                                    (slot_size - 6, slot_size - 6)
                                )
                                screen.blit(item_image, (x + 3, y + 3))
                            else:
                                pygame.draw.rect(screen, item_info["color"], 
                                               (x + 3, y + 3, slot_size - 6, slot_size - 6))
                            
                            # 绘制数量
                            if count > 1:
                                count_text = font_small.render(str(count), True, (255, 255, 255))
                                count_bg = pygame.Surface((count_text.get_width() + 4, count_text.get_height() + 2), pygame.SRCALPHA)
                                count_bg.fill((0, 0, 0, 180))
                                screen.blit(count_bg, (x + slot_size - count_text.get_width() - 6, y + slot_size - count_text.get_height() - 4))
                                screen.blit(count_text, (x + slot_size - count_text.get_width() - 4, y + slot_size - count_text.get_height() - 2))
        
        # 绘制快捷栏格
        hotbar_title = font_medium.render("快捷栏", True, (255, 255, 255))
        hotbar_title_x = inv_x + 50
        hotbar_title_y = inv_y + 480
        screen.blit(hotbar_title, (hotbar_title_x, hotbar_title_y))
        
        # 快捷栏格子参数
        hotbar_cols = 9
        hotbar_start_x = inv_x + 50
        hotbar_start_y = inv_y + 510
        
        # 绘制快捷栏格子背景
        hotbar_bg_width = hotbar_cols * (slot_size + slot_margin) + 20
        hotbar_bg_height = slot_size + slot_margin + 20
        hotbar_bg_rect = pygame.Rect(hotbar_start_x - 10, hotbar_start_y - 10, hotbar_bg_width, hotbar_bg_height)
        pygame.draw.rect(screen, (40, 40, 40), hotbar_bg_rect, 0, 5)
        pygame.draw.rect(screen, (80, 80, 80), hotbar_bg_rect, 2, 5)
        
        # 绘制快捷栏格子
        for col in range(hotbar_cols):
            x = hotbar_start_x + col * (slot_size + slot_margin)
            y = hotbar_start_y
            slot_rect = pygame.Rect(x, y, slot_size, slot_size)
            
            # 格子背景
            is_slot_hovered = slot_rect.collidepoint(mouse_pos)
            slot_color = (70, 70, 70) if is_slot_hovered else (50, 50, 50)
            pygame.draw.rect(screen, slot_color, slot_rect, 0, 3)
            pygame.draw.rect(screen, (100, 100, 100), slot_rect, 1, 3)
            
            # 尝试获取玩家快捷栏物品并绘制
            hotbar_slot = col
            if hasattr(self.game.player, 'hotbar') and hotbar_slot < len(self.game.player.hotbar):
                item = self.game.player.hotbar[hotbar_slot]
                if item:
                    item_id, count = item
                    item_info = self.ITEMS.get(item_id)
                    
                    if item_info:
                        # 绘制物品图标或颜色块
                        if item_info["texture"] in self.game.image_loader.images:
                            item_image = pygame.transform.scale(
                                self.game.image_loader.images[item_info["texture"]], 
                                (slot_size - 6, slot_size - 6)
                            )
                            screen.blit(item_image, (x + 3, y + 3))
                        else:
                            pygame.draw.rect(screen, item_info["color"], 
                                           (x + 3, y + 3, slot_size - 6, slot_size - 6))
                        
                        # 绘制数量
                        if count > 1:
                            count_text = font_small.render(str(count), True, (255, 255, 255))
                            count_bg = pygame.Surface((count_text.get_width() + 4, count_text.get_height() + 2), pygame.SRCALPHA)
                            count_bg.fill((0, 0, 0, 180))
                            screen.blit(count_bg, (x + slot_size - count_text.get_width() - 6, y + slot_size - count_text.get_height() - 4))
                            screen.blit(count_text, (x + slot_size - count_text.get_width() - 4, y + slot_size - count_text.get_height() - 2))
        
        # 绘制说明文字
        help_text = font_small.render("拖拽物品进行存储和取出", True, (200, 200, 200))
        help_x = inv_x + (inv_width - help_text.get_width()) // 2
        screen.blit(help_text, (help_x, inv_y + inv_height - 30))
        
        # 绘制拖动的物品
        if self.game.player.dragging_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            item_id = self.game.player.dragging_item["item_id"]
            item_info = self.ITEMS.get(item_id)
            
            if item_info:
                if item_info["texture"] in self.game.image_loader.images:
                    screen.blit(
                        pygame.transform.scale(self.game.image_loader.images[item_info["texture"]], (48, 48)),
                        (mouse_x - 24, mouse_y - 24)
                    )
                else:
                    pygame.draw.rect(screen, item_info["color"], (mouse_x - 24, mouse_y - 24, 48, 48))
                
                # 绘制数量
                count = self.game.player.dragging_item["quantity"]
                if count > 1:
                    count_text = font_small.render(str(count), True, (255, 255, 255))
                    count_bg = pygame.Surface((count_text.get_width() + 4, count_text.get_height() + 2), pygame.SRCALPHA)
                    count_bg.fill((0, 0, 0, 180))
                    screen.blit(count_bg, (mouse_x + 8, mouse_y + 8))
                    screen.blit(count_text, (mouse_x + 12, mouse_y + 10))
        
        return close_button_rect