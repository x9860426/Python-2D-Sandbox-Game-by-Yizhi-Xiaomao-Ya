# 这个文件包含了熔炉页面UI代码（暂不包含功能实现）

import pygame

# 熔炉页面UI类
class FurnaceManager:
    def __init__(self, game, ITEMS_global):
        self.game = game
        self.ITEMS = ITEMS_global  # 存储全局ITEMS引用
        self.是否打开 = False
        self.items = []  # 当前打开页面的物品
        self.furnace_x = 0  # 当前打开页面的熔炉x坐标
        self.furnace_y = 0  # 当前打开页面的熔炉y坐标
        
        # 存储每个熔炉的独立状态，键为(furnace_x, furnace_y)坐标元组
        self.furnaces_data = {}
        
        # === 动画控制变量 ===
        # 动画开关 - 一个变量控制是否循环播放
        self.enable_animations = True
        # 动画开始时间记录
        self.animation_start_time = pygame.time.get_ticks()
        
        # 动画状态跟踪 - 存储每个熔炉的动画状态
        self.animation_states = {}
        
        # 物品悬停相关变量
        self.当前悬停物品 = None
        self.当前悬停物品_rect = None
        self.当前悬停位置 = None
        
        # 拖拽相关变量
        self.拖拽中的物品 = None  # (物品, 来源类型, 来源位置) 来源类型: '背包'、'快捷栏'、'燃料槽'、'燃烧槽'、'输出槽'
        self.右键拆分的物品 = None  # (物品, 来源类型, 来源位置) 用于处理右键拆分跟随鼠标的物品
        
    def calculate_animation_progress(self, furnace_id):
        """基于实际冶炼进度计算横向进度条显示"""
        # 获取当前熔炉数据
        furnace_key = (self.furnace_x, self.furnace_y)
        furnace_data = self.furnaces_data.get(furnace_key, {})
        
        # 获取冶炼进度和输入物品
        smelting_progress = furnace_data.get('smelting_progress', 0)
        input_slot_item = furnace_data.get('input_slot_item')
        
        # 烧制配置 - 不同物品的烧制时间
        烧制配置 = {
            '乔木': {'烧制时间': 10},
            '木头': {'烧制时间': 9},
            '铁矿石': {'烧制时间': 15},
            '金矿石': {'烧制时间': 15},
            '钻石矿石': {'烧制时间': 20},
            '铜矿石': {'烧制时间': 15},
            '红矿石': {'烧制时间': 10},
            '蓝矿石': {'烧制时间': 10}
        }
        
        if input_slot_item:
            # 获取输入物品名称
            输入物品名称 = input_slot_item.物品信息.get('名称', '')
            
            # 检查物品是否有烧制配置
            if 输入物品名称 in 烧制配置:
                # 获取该物品的烧制时间
                烧制时间 = 烧制配置[输入物品名称]['烧制时间']
                
                if 烧制时间 > 0:
                    # 计算进度百分比
                    progress = min(100, (smelting_progress / 烧制时间) * 100)
                else:
                    progress = 0
            else:
                # 物品没有烧制配置，显示0%
                progress = 0
        else:
            # 没有输入物品，显示0%
            progress = 0
        
        return progress
    
    def calculate_fuel_animation_progress(self, furnace_id):
        """计算燃料消耗动画：基于剩余燃烧时间计算"""
        # 获取当前熔炉数据
        furnace_key = (self.furnace_x, self.furnace_y)
        furnace_data = self.furnaces_data.get(furnace_key, {})
        remaining_burn_time = furnace_data.get('remaining_burn_time', 0)
        
        # 计算燃烧进度百分比
        if remaining_burn_time > 0:
            burn_progress = min(100, remaining_burn_time)
        else:
            burn_progress = 0
        
        return burn_progress
    
    def update(self, delta_time):
        """更新熔炉状态 - 处理燃烧时间和冶炼进度"""
        # 燃料物品燃烧时间配置（1% = 1秒）
        燃料燃烧时间配置 = {
            '煤块': 100,    # +100%
            '小煤块': 10,    # +10%
            '木炭': 9,      # +9%
            '木板': 4,      # +4%
            '枯草': 2,      # +2%
            '树叶': 3,      # +3%
            '乔木叶': 3,     # +3%
            '乔木': 7,      # +7%
            '木头': 6       # +6%
        }
        
        # 遍历所有熔炉
        for furnace_key in list(self.furnaces_data.keys()):
            furnace_data = self.furnaces_data[furnace_key]
            
            # 获取熔炉的燃烧时间和燃料物品
            remaining_burn_time = furnace_data.get('remaining_burn_time', 0)
            fuel_slot_item = furnace_data.get('fuel_slot_item')
            input_slot_item = furnace_data.get('input_slot_item')
            
            # 检测燃烧格物品变化
            current_input_item_id = input_slot_item.物品_id if input_slot_item else None
            last_input_item_id = furnace_data.get('last_input_item_id')
            
            if current_input_item_id != last_input_item_id:
                # 燃烧格物品发生变化，重置冶炼进度
                furnace_data['smelting_progress'] = 0
                furnace_data['last_input_item_id'] = current_input_item_id
            
            # 更新燃烧时间
            if remaining_burn_time > 0:
                # 燃烧时间减少（1秒 = 1%）
                remaining_burn_time -= delta_time
                furnace_data['remaining_burn_time'] = max(0, remaining_burn_time)
            
            # 检查是否需要添加燃料
            if remaining_burn_time < 1:  # 进度条低于1%
                # 只有当燃烧槽有物品时，才触发减少物品增加燃烧时间的机制
                input_slot_item = furnace_data.get('input_slot_item')
                if input_slot_item and fuel_slot_item:  # 燃烧槽有物品且燃料槽有物品
                    # 获取燃料物品名称
                    物品名称 = fuel_slot_item.物品信息.get('名称', '')
                    if 物品名称 in 燃料燃烧时间配置:
                        # 获取该燃料的燃烧时间
                        燃烧时间增量 = 燃料燃烧时间配置[物品名称]
                        
                        # 减少燃料物品数量
                        fuel_slot_item.数量 -= 1
                        if fuel_slot_item.数量 <= 0:
                            # 物品已用完，移除
                            furnace_data['fuel_slot_item'] = None
                        
                        # 增加燃烧时间
                        remaining_burn_time += 燃烧时间增量
                        furnace_data['remaining_burn_time'] = remaining_burn_time
            # 燃烧时间正常减少，不需要额外条件
            # 进度条大于30%时自动停止消耗物品，因为只有在remaining_burn_time < 1时才会消耗燃料
            
            # 更新冶炼进度
            if remaining_burn_time > 0:
                # 有燃烧时间，冶炼进度增加
                smelting_progress = furnace_data.get('smelting_progress', 0)
                smelting_progress += delta_time
                furnace_data['smelting_progress'] = smelting_progress
                
                # 检查是否完成冶炼
                input_slot_item = furnace_data.get('input_slot_item')
                if input_slot_item:
                    # 获取输入物品名称
                    输入物品名称 = input_slot_item.物品信息.get('名称', '')
                    
                    # 烧制配置 - 不同物品的烧制时间
                    烧制配置 = {
                        '乔木': {'烧制时间': 10},
                        '木头': {'烧制时间': 9},
                        '铁矿石': {'烧制时间': 15},
                        '金矿石': {'烧制时间': 15},
                        '钻石矿石': {'烧制时间': 20},
                        '铜矿石': {'烧制时间': 15},
                        '红矿石': {'烧制时间': 10},
                        '蓝矿石': {'烧制时间': 10}
                    }
                    
                    # 检查物品是否有烧制配置
                    if 输入物品名称 in 烧制配置:
                        # 获取该物品的烧制时间
                        烧制时间 = 烧制配置[输入物品名称]['烧制时间']
                        
                        # 检查是否完成冶炼
                        if smelting_progress >= 烧制时间:
                            # 完成冶炼，重置进度
                            furnace_data['smelting_progress'] = 0
                            
                            # 1. 减少燃烧槽物品数量
                            input_slot_item.数量 -= 1
                            if input_slot_item.数量 <= 0:
                                # 物品已用完，移除
                                furnace_data['input_slot_item'] = None
                            
                            # 2. 生成冶炼产物
                            import random
                            from 物品定义 import 物品
                            
                            # 冶炼产物配置（使用物品ID）
                            冶炼产物配置 = {
                                '乔木': {'产物ID': 15008, '数量': 2},  # 木炭
                                '木头': {'产物ID': 15008, '数量': 2},  # 木炭
                                '铁矿石': {'产物ID': 15004, '数量': random.randint(1, 2)},  # 铁锭
                                '金矿石': {'产物ID': 15001, '数量': random.randint(1, 2)},  # 金锭
                                '钻石矿石': {'产物ID': 15007, '数量': 1},  # 钻石
                                '铜矿石': {'产物ID': 15005, '数量': random.randint(1, 3)},  # 铜锭
                                '红矿石': {'产物ID': 15000, '数量': random.randint(1, 3)},  # 红石
                                '蓝矿石': {'产物ID': 15002, '数量': random.randint(1, 3)}   # 蓝石
                            }
                            
                            # 获取冶炼产物
                            if 输入物品名称 in 冶炼产物配置:
                                产物配置 = 冶炼产物配置[输入物品名称]
                                产物ID = 产物配置['产物ID']
                                产物数量 = 产物配置['数量']
                                
                                # 3. 将产物添加到输出槽
                                output_items = furnace_data.get('output_slots', [])
                                
                                # 确保输出槽列表有6个位置
                                while len(output_items) < 6:
                                    output_items.append(None)
                                
                                # 尝试堆叠到现有产物槽
                                产物已添加 = False
                                for i in range(6):
                                    slot_item = output_items[i]
                                    if slot_item and slot_item.物品_id == 产物ID:
                                        # 可以堆叠，尝试堆叠
                                        已添加数量 = slot_item.增加数量(产物数量)
                                        产物数量 -= 已添加数量
                                        if 产物数量 <= 0:
                                            产物已添加 = True
                                            break
                                
                                # 如果还有剩余产物，尝试放入空槽
                                if not 产物已添加 and 产物数量 > 0:
                                    for i in range(6):
                                        if output_items[i] is None:
                                            # 创建新的产物物品实例
                                            # 从物品定义中获取物品信息
                                            产物信息 = 物品.get(产物ID, {})
                                            if 产物信息:
                                                # 假设物品类有一个创建方法
                                                from 背包 import 物品 as 物品类
                                                new_item = 物品类(产物ID)
                                                new_item.数量 = 产物数量
                                                output_items[i] = new_item
                                                产物已添加 = True
                                                break
                                
                                # 获取产物名称用于打印
                                产物名称 = 物品.get(产物ID, {}).get('名称', '未知物品')
                                print(f"烧制完成: {输入物品名称} → {产物名称} x{产物配置['数量']}")
            else:
                # 没有燃烧时间，重置冶炼进度为0%
                furnace_data['smelting_progress'] = 0
        
    def open_page(self, furnace_x=0, furnace_y=0):
        """打开熔炉页面"""
        self.是否打开 = True
        self.furnace_x = furnace_x  # 存储熔炉坐标
        self.furnace_y = furnace_y
        
        # 初始化或加载该熔炉的状态
        furnace_key = (furnace_x, furnace_y)
        if furnace_key not in self.furnaces_data:
            # 如果是第一次打开该熔炉，初始化其状态
            self.furnaces_data[furnace_key] = {
                'remaining_burn_time': 0,
                'smelting_progress': 0,
                'smelting_total_time': 0,
                'output_slots': [],
                'fuel_slot_item': None,
                'input_slot_item': None,
                'last_input_item_id': None  # 存储上一次的燃烧格物品ID，用于检测物品变化
            }
        
        # 尝试关闭其他界面（使用try-except避免属性错误）
        try:
            # 检查是否有player属性并尝试关闭其他界面
            if hasattr(self.game, 'player'):
                player = self.game.player
                if hasattr(player, 'is_inventory_open'):
                    player.is_inventory_open = False
                if hasattr(player, 'is_crafting_open'):
                    player.is_crafting_open = False
                if hasattr(player, 'is_chest_open'):
                    player.is_chest_open = False
                if hasattr(player, 'current_chest'):
                    player.current_chest = None
        except:
            # 忽略错误，继续执行
            pass
        
    def close_page(self):
        """关闭熔炉页面"""
        self.是否打开 = False
    
    def handle_keyboard(self, event):
        """处理熔炉页面的键盘事件"""
        if not self.是否打开:
            return False
        
        # 处理ESC键关闭页面
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close_page()
                return True
        
        return False
    
    def 处理点击(self, mx, my, button=1):
        """处理熔炉页面的点击事件"""
        if not self.是否打开:
            return
            
        # 界面参数 - 与draw方法保持一致 (长680,宽450)
        page_width = 680
        page_height = 450
        # 获取屏幕尺寸
        screen_width, screen_height = pygame.display.get_surface().get_size()
        page_x = (screen_width - page_width) // 2
        page_y = (screen_height - page_height) // 2
        
        # 检查是否点击了关闭按钮（X按钮）
        # 关闭按钮位置与draw方法中保持一致
        close_button_size = 28
        title_bar_height = 45  # 与draw方法中的标题栏高度保持一致
        close_button_rect = pygame.Rect(page_x + page_width - close_button_size - 10, 
                                       page_y + (title_bar_height - close_button_size) // 2, 
                                       close_button_size, close_button_size)
        if close_button_rect.collidepoint(mx, my):
            self.close_page()
            return
            
        # 移除点击页面外部关闭页面的逻辑，玩家需要通过关闭按钮或ESC键关闭页面
        
        # 格子尺寸
        slot_size = 44
        slot_margin = 5
        
        # 背包格子参数 - 与draw方法保持一致
        backpack_rows = 5
        backpack_cols = 6
        backpack_x = page_x + 340
        backpack_y = page_y + title_bar_height + 20
        backpack_start_x = backpack_x + 15
        backpack_start_y = backpack_y + 50
        
        # 快捷栏参数 - 与draw方法保持一致
        hotbar_y = page_y + page_height - 70
        hotbar_width = 660
        hotbar_x = page_x + 20
        total_hotbar_slots_width = 8 * slot_size + 7 * slot_margin
        hotbar_slot_start_x = hotbar_x + (hotbar_width - total_hotbar_slots_width) // 2
        hotbar_slot_y = hotbar_y + 7
        
        # 熔炉核心区域参数 - 与draw方法保持一致
        furnace_core_y = page_y + title_bar_height + 20
        furnace_core_width = 320
        furnace_core_height = 300
        furnace_core_x = page_x + 20
        
        # 左侧系统区域参数 - 与draw方法保持一致
        格子宽度 = 48
        格子高度 = 48
        元素间距 = 8
        区域间距 = 15
        左侧系统宽度 = 格子宽度 + 元素间距 + 70
        左侧区域_x = furnace_core_x + (furnace_core_width - 左侧系统宽度 - 区域间距 - (格子宽度 * 3 + 元素间距 * 2)) // 2
        左侧区域_y = furnace_core_y + (furnace_core_height - (格子高度 * 2 + 元素间距 * 3)) // 2
        
        # 燃烧槽和燃料槽位置 - 与draw方法保持一致
        燃烧格_x = 左侧区域_x
        燃烧格_y = 左侧区域_y
        燃料格_x = 燃烧格_x
        燃料格_y = 燃烧格_y + 格子高度 + 元素间距 * 2
        
        # 输出槽位置 - 与draw方法保持一致
        存储区域_x = 左侧区域_x + 左侧系统宽度 + 区域间距
        存储区域_y = 左侧区域_y
        存储格行数 = 2
        存储格列数 = 3
        存储格间距 = 6
        存储格坐标 = []
        for 行 in range(存储格行数):
            for 列 in range(存储格列数):
                当前格_x = 存储区域_x + 列 * (格子宽度 + 存储格间距)
                当前格_y = 存储区域_y + 行 * (格子高度 + 存储格间距)
                存储格坐标.append({
                    'x': 当前格_x,
                    'y': 当前格_y,
                    'width': 格子宽度,
                    'height': 格子高度
                })
        
        # 查找点击位置对应的格子
        def 查找点击位置对应的格子(mx, my):
            """查找指定位置对应的格子"""
            # 检查背包格子
            for row in range(backpack_rows):
                for col in range(backpack_cols):
                    x = backpack_start_x + col * (slot_size + slot_margin)
                    y = backpack_start_y + row * (slot_size + slot_margin)
                    rect = pygame.Rect(x, y, slot_size, slot_size)
                    if rect.collidepoint(mx, my):
                        return ('背包', (row, col))
            
            # 检查快捷栏格子
            for i in range(8):
                x = hotbar_slot_start_x + i * (slot_size + slot_margin)
                y = hotbar_slot_y
                rect = pygame.Rect(x, y, slot_size, slot_size)
                if rect.collidepoint(mx, my):
                    return ('快捷栏', (i,))
            
            # 检查燃烧槽
            燃烧槽_rect = pygame.Rect(燃烧格_x, 燃烧格_y, 格子宽度, 格子高度)
            if 燃烧槽_rect.collidepoint(mx, my):
                return ('燃烧槽', ())
            
            # 检查燃料槽
            燃料槽_rect = pygame.Rect(燃料格_x, 燃料格_y, 格子宽度, 格子高度)
            if 燃料槽_rect.collidepoint(mx, my):
                return ('燃料槽', ())
            
            # 检查输出槽
            for i, 存储格 in enumerate(存储格坐标):
                输出槽_rect = pygame.Rect(存储格['x'], 存储格['y'], 存储格['width'], 存储格['height'])
                if 输出槽_rect.collidepoint(mx, my):
                    return ('输出槽', (i,))
            
            return None
        
        # 处理左键点击（叠加和更换位置）
        def 处理左键点击(位置):
            """处理鼠标左键点击（叠加和更换位置）"""
            # 如果有右键拆分的物品，先处理放置
            if self.右键拆分的物品:
                拆分物品, 来源类型, 来源位置 = self.右键拆分的物品
                格子信息 = 查找点击位置对应的格子(mx, my)
                
                if 格子信息:
                    目标类型, 目标位置 = 格子信息
                    # 处理放置逻辑
                    self._放置拆分物品(拆分物品, 来源类型, 来源位置, 目标类型, 目标位置)
                else:
                    # 点击空白处，将拆分物品放回原格子
                    self._放回拆分物品(拆分物品, 来源类型, 来源位置)
                return
                
            格子信息 = 查找点击位置对应的格子(mx, my)
            if not 格子信息:
                # 如果点击了格子外，取消拖拽并将物品放回原位置
                if self.拖拽中的物品:
                    物品, 来源类型, 来源位置 = self.拖拽中的物品
                    self._放回拖拽物品(物品, 来源类型, 来源位置)
                return
                
            目标类型, 目标位置 = 格子信息
            
            if self.拖拽中的物品:
                # 正在拖拽物品，尝试放置
                被拖拽物品, 来源类型, 来源位置 = self.拖拽中的物品
                
                # 如果是同一个格子，将物品放回并取消拖拽
                if 目标类型 == 来源类型 and 目标位置 == 来源位置:
                    self._放回拖拽物品(被拖拽物品, 来源类型, 来源位置)
                    return
                    
                # 尝试放置物品
                self._放置拖拽物品(被拖拽物品, 来源类型, 来源位置, 目标类型, 目标位置)
            else:
                # 没有拖拽物品，尝试拿起物品
                self._拿起物品(目标类型, 目标位置)
        
        # 处理右键点击（对半拆分物品）
        def 处理右键点击(位置):
            """处理鼠标右键点击（对半拆分物品）"""
            # 如果有拖拽中的物品，不执行右键操作
            if self.拖拽中的物品:
                return
                
            格子信息 = 查找点击位置对应的格子(mx, my)
            if not 格子信息:
                # 如果右键点击空白处，将拆分的物品放回原格子
                if self.右键拆分的物品:
                    拆分物品, 来源类型, 来源位置 = self.右键拆分的物品
                    self._放回拆分物品(拆分物品, 来源类型, 来源位置)
                return
                
            目标类型, 目标位置 = 格子信息
            
            # 如果已经有拆分中的物品，尝试放置到当前位置
            if self.右键拆分的物品:
                拆分物品, 来源类型, 来源位置 = self.右键拆分的物品
                self._放置拆分物品(拆分物品, 来源类型, 来源位置, 目标类型, 目标位置)
            else:
                # 尝试拆分当前物品
                self._拆分物品(目标类型, 目标位置)
        
        # 根据按钮类型处理点击
        if button == 1:  # 左键点击
            处理左键点击((mx, my))
        elif button == 3:  # 右键点击
            处理右键点击((mx, my))
    
    def _拿起物品(self, 物品类型, 位置):
        """从指定位置拿起物品"""
        # 获取当前熔炉数据
        furnace_key = (self.furnace_x, self.furnace_y)
        furnace_data = self.furnaces_data.get(furnace_key, {})
        
        if 物品类型 == '背包':
            # 从背包拿起物品
            row, col = 位置
            if hasattr(self.game, '背包管理器'):
                current_item = self.game.背包管理器.背包物品[row][col]
                if current_item:
                    self.拖拽中的物品 = (current_item, '背包', (row, col))
                    self.game.背包管理器.背包物品[row][col] = None
        elif 物品类型 == '快捷栏':
            # 从快捷栏拿起物品
            index, = 位置
            if hasattr(self.game, '背包管理器'):
                current_item = self.game.背包管理器.快捷栏物品[index]
                if current_item:
                    self.拖拽中的物品 = (current_item, '快捷栏', (index,))
                    self.game.背包管理器.快捷栏物品[index] = None
        elif 物品类型 == '燃烧槽':
            # 从燃烧槽拿起物品
            input_item = furnace_data.get('input_slot_item')
            if input_item:
                self.拖拽中的物品 = (input_item, '燃烧槽', ())
                furnace_data['input_slot_item'] = None
        elif 物品类型 == '燃料槽':
            # 从燃料槽拿起物品
            fuel_item = furnace_data.get('fuel_slot_item')
            if fuel_item:
                self.拖拽中的物品 = (fuel_item, '燃料槽', ())
                furnace_data['fuel_slot_item'] = None
        elif 物品类型 == '输出槽':
            # 从输出槽拿起物品
            index, = 位置
            output_items = furnace_data.get('output_slots', [])
            if index < len(output_items) and output_items[index]:
                self.拖拽中的物品 = (output_items[index], '输出槽', (index,))
                output_items[index] = None
    
    def _放置拖拽物品(self, 物品, 来源类型, 来源位置, 目标类型, 目标位置):
        """将拖拽中的物品放置到目标位置"""
        # 获取当前熔炉数据
        furnace_key = (self.furnace_x, self.furnace_y)
        furnace_data = self.furnaces_data.get(furnace_key, {})
        
        # 燃料槽允许的物品列表
        允许的燃料物品 = ['煤块', '小煤块', '木炭', '木板', '枯草', '树叶', '乔木叶', '乔木', '木头']
        
        # 检查是否是放置到燃料槽
        if 目标类型 == '燃料槽':
            # 获取物品名称
            物品名称 = 物品.物品信息.get('名称', '')
            # 检查物品是否在允许的燃料列表中
            if 物品名称 not in 允许的燃料物品:
                # 不允许放置，将物品放回原位置
                self._放回拖拽物品(物品, 来源类型, 来源位置)
                return
        
        # 获取目标位置的物品
        目标物品 = None
        if 目标类型 == '背包':
            # 背包目标
            row, col = 目标位置
            if hasattr(self.game, '背包管理器'):
                目标物品 = self.game.背包管理器.背包物品[row][col]
        elif 目标类型 == '快捷栏':
            # 快捷栏目标
            index, = 目标位置
            if hasattr(self.game, '背包管理器'):
                目标物品 = self.game.背包管理器.快捷栏物品[index]
        elif 目标类型 == '燃烧槽':
            # 燃烧槽目标
            目标物品 = furnace_data.get('input_slot_item')
        elif 目标类型 == '燃料槽':
            # 燃料槽目标
            目标物品 = furnace_data.get('fuel_slot_item')
        elif 目标类型 == '输出槽':
            # 输出槽目标
            index, = 目标位置
            output_items = furnace_data.get('output_slots', [])
            if index < len(output_items):
                目标物品 = output_items[index]
        
        if 目标物品:
            # 目标位置有物品
            if 目标物品.可以堆叠(物品):
                # 可以堆叠，尝试堆叠
                已添加 = 目标物品.增加数量(物品.数量)
                物品.数量 -= 已添加
                if 物品.数量 <= 0:
                    # 物品已完全堆叠，清空拖拽状态
                    self.拖拽中的物品 = None
                else:
                    # 还有剩余物品，继续拖拽
                    self.拖拽中的物品 = (物品, 来源类型, 来源位置)
            else:
                # 不能堆叠，交换物品
                self._交换物品(物品, 来源类型, 来源位置, 目标物品, 目标类型, 目标位置)
        else:
            # 目标位置为空，直接放置
            self._直接放置物品(物品, 目标类型, 目标位置)
            self.拖拽中的物品 = None
    
    def _放回拖拽物品(self, 物品, 来源类型, 来源位置):
        """将拖拽中的物品放回原位置"""
        # 获取当前熔炉数据
        furnace_key = (self.furnace_x, self.furnace_y)
        furnace_data = self.furnaces_data.get(furnace_key, {})
        
        if 来源类型 == '背包':
            # 放回背包
            row, col = 来源位置
            if hasattr(self.game, '背包管理器'):
                self.game.背包管理器.背包物品[row][col] = 物品
        elif 来源类型 == '快捷栏':
            # 放回快捷栏
            index, = 来源位置
            if hasattr(self.game, '背包管理器'):
                self.game.背包管理器.快捷栏物品[index] = 物品
        elif 来源类型 == '燃烧槽':
            # 放回燃烧槽
            furnace_data['input_slot_item'] = 物品
        elif 来源类型 == '燃料槽':
            # 放回燃料槽
            furnace_data['fuel_slot_item'] = 物品
        elif 来源类型 == '输出槽':
            # 放回输出槽
            index, = 来源位置
            output_items = furnace_data.get('output_slots', [])
            if index < len(output_items):
                output_items[index] = 物品
        
        # 清空拖拽状态
        self.拖拽中的物品 = None
    
    def _交换物品(self, 物品1, 类型1, 位置1, 物品2, 类型2, 位置2):
        """交换两个物品的位置"""
        # 获取当前熔炉数据
        furnace_key = (self.furnace_x, self.furnace_y)
        furnace_data = self.furnaces_data.get(furnace_key, {})
        
        # 放置物品2到位置1
        if 类型1 == '背包':
            row, col = 位置1
            if hasattr(self.game, '背包管理器'):
                self.game.背包管理器.背包物品[row][col] = 物品2
        elif 类型1 == '快捷栏':
            index, = 位置1
            if hasattr(self.game, '背包管理器'):
                self.game.背包管理器.快捷栏物品[index] = 物品2
        elif 类型1 == '燃烧槽':
            furnace_data['input_slot_item'] = 物品2
        elif 类型1 == '燃料槽':
            furnace_data['fuel_slot_item'] = 物品2
        elif 类型1 == '输出槽':
            index, = 位置1
            output_items = furnace_data.get('output_slots', [])
            if index < len(output_items):
                output_items[index] = 物品2
        
        # 放置物品1到位置2
        if 类型2 == '背包':
            row, col = 位置2
            if hasattr(self.game, '背包管理器'):
                self.game.背包管理器.背包物品[row][col] = 物品1
        elif 类型2 == '快捷栏':
            index, = 位置2
            if hasattr(self.game, '背包管理器'):
                self.game.背包管理器.快捷栏物品[index] = 物品1
        elif 类型2 == '燃烧槽':
            furnace_data['input_slot_item'] = 物品1
        elif 类型2 == '燃料槽':
            furnace_data['fuel_slot_item'] = 物品1
        elif 类型2 == '输出槽':
            index, = 位置2
            output_items = furnace_data.get('output_slots', [])
            if index < len(output_items):
                output_items[index] = 物品1
        
        # 交换完成后，清空拖拽中的物品状态
        self.拖拽中的物品 = None
    
    def _直接放置物品(self, 物品, 目标类型, 目标位置):
        """将物品直接放置到目标位置"""
        # 获取当前熔炉数据
        furnace_key = (self.furnace_x, self.furnace_y)
        furnace_data = self.furnaces_data.get(furnace_key, {})
        
        if 目标类型 == '背包':
            # 放置到背包
            row, col = 目标位置
            if hasattr(self.game, '背包管理器'):
                self.game.背包管理器.背包物品[row][col] = 物品
        elif 目标类型 == '快捷栏':
            # 放置到快捷栏
            index, = 目标位置
            if hasattr(self.game, '背包管理器'):
                self.game.背包管理器.快捷栏物品[index] = 物品
        elif 目标类型 == '燃烧槽':
            # 放置到燃烧槽
            furnace_data['input_slot_item'] = 物品
        elif 目标类型 == '燃料槽':
            # 放置到燃料槽
            furnace_data['fuel_slot_item'] = 物品
        elif 目标类型 == '输出槽':
            # 放置到输出槽
            index, = 目标位置
            output_items = furnace_data.get('output_slots', [])
            # 确保输出槽列表足够长
            while len(output_items) <= index:
                output_items.append(None)
            output_items[index] = 物品
    
    def _拆分物品(self, 物品类型, 位置):
        """右键拆分物品"""
        # 获取当前熔炉数据
        furnace_key = (self.furnace_x, self.furnace_y)
        furnace_data = self.furnaces_data.get(furnace_key, {})
        
        物品 = None
        if 物品类型 == '背包':
            # 从背包拆分物品
            row, col = 位置
            if hasattr(self.game, '背包管理器'):
                物品 = self.game.背包管理器.背包物品[row][col]
        elif 物品类型 == '快捷栏':
            # 从快捷栏拆分物品
            index, = 位置
            if hasattr(self.game, '背包管理器'):
                物品 = self.game.背包管理器.快捷栏物品[index]
        elif 物品类型 == '燃烧槽':
            # 从燃烧槽拆分物品
            物品 = furnace_data.get('input_slot_item')
        elif 物品类型 == '燃料槽':
            # 从燃料槽拆分物品
            物品 = furnace_data.get('fuel_slot_item')
        elif 物品类型 == '输出槽':
            # 从输出槽拆分物品
            index, = 位置
            output_items = furnace_data.get('output_slots', [])
            if index < len(output_items):
                物品 = output_items[index]
        
        if 物品:
            # 尝试拆分一半物品
            拆分物品 = 物品.拆分一半()
            if 拆分物品:
                self.右键拆分的物品 = (拆分物品, 物品类型, 位置)
    
    def _放置拆分物品(self, 拆分物品, 来源类型, 来源位置, 目标类型, 目标位置):
        """将拆分的物品放置到目标位置"""
        # 获取当前熔炉数据
        furnace_key = (self.furnace_x, self.furnace_y)
        furnace_data = self.furnaces_data.get(furnace_key, {})
        
        # 燃料槽允许的物品列表
        允许的燃料物品 = ['煤块', '小煤块', '木炭', '木板', '枯草', '树叶', '乔木叶', '乔木', '木头']
        
        # 检查是否是放置到燃料槽
        if 目标类型 == '燃料槽':
            # 获取物品名称
            物品名称 = 拆分物品.物品信息.get('名称', '')
            # 检查物品是否在允许的燃料列表中
            if 物品名称 not in 允许的燃料物品:
                # 不允许放置，将物品放回原位置
                self._放回拆分物品(拆分物品, 来源类型, 来源位置)
                return
        
        # 获取目标位置的物品
        目标物品 = None
        if 目标类型 == '背包':
            # 背包目标
            row, col = 目标位置
            if hasattr(self.game, '背包管理器'):
                目标物品 = self.game.背包管理器.背包物品[row][col]
        elif 目标类型 == '快捷栏':
            # 快捷栏目标
            index, = 目标位置
            if hasattr(self.game, '背包管理器'):
                目标物品 = self.game.背包管理器.快捷栏物品[index]
        elif 目标类型 == '燃烧槽':
            # 燃烧槽目标
            目标物品 = furnace_data.get('input_slot_item')
        elif 目标类型 == '燃料槽':
            # 燃料槽目标
            目标物品 = furnace_data.get('fuel_slot_item')
        elif 目标类型 == '输出槽':
            # 输出槽目标
            index, = 目标位置
            output_items = furnace_data.get('output_slots', [])
            if index < len(output_items):
                目标物品 = output_items[index]
        
        if 目标物品:
            # 目标位置有物品
            if 目标物品.可以堆叠(拆分物品):
                # 可以堆叠，尝试堆叠
                已添加 = 目标物品.增加数量(拆分物品.数量)
                拆分物品.数量 -= 已添加
                if 拆分物品.数量 <= 0:
                    # 物品已完全堆叠，清空拆分状态
                    self.右键拆分的物品 = None
                else:
                    # 还有剩余物品，将剩余物品放回原位置
                    self._放回拆分物品(拆分物品, 来源类型, 来源位置)
            else:
                # 不能堆叠，将拆分物品放回原位置
                self._放回拆分物品(拆分物品, 来源类型, 来源位置)
        else:
            # 目标位置为空，放置拆分的物品
            self._直接放置物品(拆分物品, 目标类型, 目标位置)
            self.右键拆分的物品 = None
    
    def _放回拆分物品(self, 拆分物品, 来源类型, 来源位置):
        """将拆分的物品放回原位置"""
        # 获取当前熔炉数据
        furnace_key = (self.furnace_x, self.furnace_y)
        furnace_data = self.furnaces_data.get(furnace_key, {})
        
        if 来源类型 == '背包':
            # 放回背包
            row, col = 来源位置
            if hasattr(self.game, '背包管理器'):
                原物品 = self.game.背包管理器.背包物品[row][col]
                if 原物品:
                    原物品.数量 += 拆分物品.数量
                else:
                    self.game.背包管理器.背包物品[row][col] = 拆分物品
        elif 来源类型 == '快捷栏':
            # 放回快捷栏
            index, = 来源位置
            if hasattr(self.game, '背包管理器'):
                原物品 = self.game.背包管理器.快捷栏物品[index]
                if 原物品:
                    原物品.数量 += 拆分物品.数量
                else:
                    self.game.背包管理器.快捷栏物品[index] = 拆分物品
        elif 来源类型 == '燃烧槽':
            # 放回燃烧槽
            原物品 = furnace_data.get('input_slot_item')
            if 原物品:
                原物品.数量 += 拆分物品.数量
            else:
                furnace_data['input_slot_item'] = 拆分物品
        elif 来源类型 == '燃料槽':
            # 放回燃料槽
            原物品 = furnace_data.get('fuel_slot_item')
            if 原物品:
                原物品.数量 += 拆分物品.数量
            else:
                furnace_data['fuel_slot_item'] = 拆分物品
        elif 来源类型 == '输出槽':
            # 放回输出槽
            index, = 来源位置
            output_items = furnace_data.get('output_slots', [])
            if index < len(output_items):
                原物品 = output_items[index]
                if 原物品:
                    原物品.数量 += 拆分物品.数量
                else:
                    output_items[index] = 拆分物品
        
        # 清空拆分状态
        self.右键拆分的物品 = None
    
    def draw(self, screen):
        """绘制熔炉页面（重新设计版）"""
        if not self.是否打开:
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
        font_small = load_font(14)
        font_medium = load_font(18, bold=True)
        font_large = load_font(24, bold=True)
        
        # 获取鼠标位置
        mouse_pos = pygame.mouse.get_pos()
        
        # 定义更好的颜色方案
        COLORS = {
            'bg_dark': (30, 30, 30),
            'bg_medium': (50, 50, 50),
            'bg_light': (70, 70, 70),
            'border_dark': (80, 80, 80),
            'border_medium': (120, 120, 120),
            'border_light': (160, 160, 160),
            'text_primary': (255, 255, 255),
            'text_secondary': (200, 200, 200),
            'text_hint': (150, 150, 150),
            'slot_normal': (60, 60, 60),
            'slot_hover': (85, 85, 85),
            'slot_equipped': (100, 120, 80),
            'furnace_brown': (101, 67, 33),
            'furnace_light_brown': (139, 69, 19),
            'fire_orange': (255, 165, 0),
            'fire_red': (220, 50, 50),
            'progress_blue': (65, 105, 225),
            'close_button': (150, 50, 50),
            'close_button_hover': (200, 60, 60)
        }
        
        # 界面参数 - 修改后的熔炉页面尺寸 (长680,宽450)
        page_width = 680
        page_height = 450
        page_x = (WIDTH - page_width) // 2
        page_y = (HEIGHT - page_height) // 2
        
        # 格子尺寸
        slot_size = 44
        slot_margin = 5
        
        # 绘制半透明背景覆盖层
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # 更暗的背景，增强对比度
        screen.blit(overlay, (0, 0))
        
        # 绘制主界面背景 - 多层边框效果
        # 底层阴影
        pygame.draw.rect(screen, (0, 0, 0, 100), 
                         (page_x + 3, page_y + 3, page_width, page_height), 0, 8)
        # 主背景
        pygame.draw.rect(screen, COLORS['bg_dark'], 
                         (page_x, page_y, page_width, page_height), 0, 8)
        # 三层边框效果
        pygame.draw.rect(screen, COLORS['border_dark'], 
                         (page_x, page_y, page_width, page_height), 3, 8)
        pygame.draw.rect(screen, COLORS['border_medium'], 
                         (page_x + 3, page_y + 3, page_width - 6, page_height - 6), 1, 6)
        
        # 绘制标题栏
        title_bar_height = 45
        pygame.draw.rect(screen, COLORS['bg_medium'], 
                         (page_x, page_y, page_width, title_bar_height), 0, 8)
        pygame.draw.rect(screen, COLORS['border_medium'], 
                         (page_x, page_y, page_width, title_bar_height), 1, 8)
        pygame.draw.rect(screen, COLORS['border_dark'], 
                         (page_x, page_y + title_bar_height - 2, page_width, 2))
        
        # 绘制标题 - 熔炉图标和文字
        title_text = font_large.render("熔炉", True, COLORS['text_primary'])
        title_x = page_x + 20
        screen.blit(title_text, (title_x, page_y + 10))

        # 显示熔炉坐标 - 右上角
        coordinate_text = font_medium.render(f"(x={self.furnace_x}, y={self.furnace_y})", True, COLORS['text_secondary'])
        coordinate_x = page_x + page_width - 150  # 距离右侧150像素，为关闭按钮留出空间
        coordinate_y = page_y + 10
        screen.blit(coordinate_text, (coordinate_x, coordinate_y))
        
        # 美化关闭按钮
        close_button_size = 28
        close_button_rect = pygame.Rect(page_x + page_width - close_button_size - 10, 
                                       page_y + (title_bar_height - close_button_size) // 2, 
                                       close_button_size, close_button_size)
        is_close_hovered = close_button_rect.collidepoint(mouse_pos)
        
        # 关闭按钮多层效果
        pygame.draw.rect(screen, COLORS['close_button_hover'] if is_close_hovered else COLORS['close_button'], 
                         close_button_rect, 0, 5)
        pygame.draw.rect(screen, COLORS['border_light'], close_button_rect, 2, 5)
        pygame.draw.rect(screen, (0, 0, 0, 50), 
                         (close_button_rect.x + 1, close_button_rect.y + 1, 
                          close_button_rect.width - 2, close_button_rect.height - 2), 0, 4)
        
        # 绘制关闭符号
        close_text = font_medium.render("×", True, COLORS['text_primary'])
        close_text_x = close_button_rect.x + (close_button_rect.width - close_text.get_width()) // 2
        close_text_y = close_button_rect.y + (close_button_rect.height - close_text.get_height()) // 2 - 2
        screen.blit(close_text, (close_text_x, close_text_y))
        
        # === 上部熔炉核心区域 ===
        # 熔炉核心区域Y坐标 - 与背包区域保持一致
        furnace_core_y = page_y + title_bar_height + 20  # 移除额外的40像素偏移，与背包区域对齐
        furnace_core_width = 320  # 修改宽度为320像素
        furnace_core_height = 300  # 修改高度为300像素
        furnace_core_x = page_x + 20
        
        # 绘制熔炉核心区域背景
        pygame.draw.rect(screen, COLORS['bg_medium'], 
                         (furnace_core_x, furnace_core_y, furnace_core_width, furnace_core_height), 0, 6)
        pygame.draw.rect(screen, COLORS['border_medium'], 
                         (furnace_core_x, furnace_core_y, furnace_core_width, furnace_core_height), 2, 6)
        
        # 移除熔炉图标以消除左上角的橙色显示
        # 原本的图标绘制代码已删除
        
        # 获取当前熔炉数据
        furnace_key = (self.furnace_x, self.furnace_y)
        furnace_data = self.furnaces_data.get(furnace_key, {
            'remaining_burn_time': 0,
            'smelting_progress': 0
        })
        
        # === 统一的格子尺寸设置 ===
        格子宽度 = 48  # 稍微增大格子尺寸，提高可用性
        格子高度 = 48
        元素间距 = 8  # 调整元素间距，使布局更紧凑
        区域间距 = 15  # 区域之间的间距
        
        # === 重新设计的布局：左侧为燃料/燃烧系统，右侧为存储区域 ===
        
        # 计算左侧系统区域的居中位置
        左侧系统宽度 = 格子宽度 + 元素间距 + 70  # 格子 + 进度条 + 间距
        左侧区域_x = furnace_core_x + (furnace_core_width - 左侧系统宽度 - 区域间距 - (格子宽度 * 3 + 元素间距 * 2)) // 2
        左侧区域_y = furnace_core_y + (furnace_core_height - (格子高度 * 2 + 元素间距 * 3)) // 2
        
        # === 1. 燃烧格（输入槽）=== 位于左侧上方
        燃烧格_x = 左侧区域_x
        燃烧格_y = 左侧区域_y
        
        # 绘制燃烧格（输入槽）
        pygame.draw.rect(screen, (70, 60, 40), (燃烧格_x, 燃烧格_y, 格子宽度, 格子高度), 0, 4)
        pygame.draw.rect(screen, (160, 140, 100), (燃烧格_x, 燃烧格_y, 格子宽度, 格子高度), 2, 4)
        
        # === 2. 熔炼进度条 === 位于燃烧格右侧，精确对齐
        熔炼进度条_x = 燃烧格_x + 格子宽度 + 元素间距
        熔炼进度条_y = 燃烧格_y + (格子高度 - 12) // 2  # 垂直居中
        熔炼进度条宽度 = 70
        熔炼进度条高度 = 12
        
        # 确保进度条与燃烧格垂直居中对齐
        熔炼进度条_y = 燃烧格_y + (格子高度 - 熔炼进度条高度) // 2
        
        # 绘制熔炼进度条背景（增强视觉效果）
        # 添加外阴影
        shadow_offset = 2
        pygame.draw.rect(screen, (20, 20, 20), 
                         (熔炼进度条_x + shadow_offset, 熔炼进度条_y + shadow_offset, 熔炼进度条宽度, 熔炼进度条高度), 0, 2)
        # 主背景
        pygame.draw.rect(screen, (40, 40, 40), (熔炼进度条_x, 熔炼进度条_y, 熔炼进度条宽度, 熔炼进度条高度), 0, 2)
        # 内边框
        pygame.draw.rect(screen, (80, 80, 80), (熔炼进度条_x + 1, 熔炼进度条_y + 1, 熔炼进度条宽度 - 2, 熔炼进度条高度 - 2), 1, 2)
        
        # 计算冶炼进度动画
        furnace_id = (self.furnace_x, self.furnace_y)  # 创建熔炉唯一标识符
        animated_progress = self.calculate_animation_progress(furnace_id)
        
        # 使用动画进度替代原有静态进度
        smelting_progress = animated_progress / 100  # 转换为0-1范围
        
        # 熔炼进度条宽度
        progress_width = int(熔炼进度条宽度 * smelting_progress)
        
        # 绘制熔炼进度条（增强视觉效果）
        if smelting_progress > 0:
            # 基础蓝色进度（更深的蓝色）
            pygame.draw.rect(screen, (50, 120, 200), 
                             (熔炼进度条_x + 2, 熔炼进度条_y + 2, progress_width - 4, 熔炼进度条高度 - 4), 0, 1)
            
            # 添加渐变高光效果
            if progress_width > 6:  # 确保有足够空间绘制高光
                # 顶部亮边
                highlight_height = max(1, (熔炼进度条高度 - 4) // 3)
                pygame.draw.rect(screen, (120, 200, 255), 
                                (熔炼进度条_x + 3, 熔炼进度条_y + 3, progress_width - 6, highlight_height), 0, 1)
                
                # 添加动画时的脉冲效果
                if self.enable_animations and animated_progress > 0 and animated_progress < 100:
                    pulse_intensity = int((pygame.time.get_ticks() % 300) / 300 * 40)  # 脉冲强度
                    if pulse_intensity > 20:
                        # 在进度条右端添加脉冲光效
                        pulse_x = 熔炼进度条_x + progress_width - 4
                        pulse_y = 熔炼进度条_y + 熔炼进度条高度 // 2
                        pygame.draw.circle(screen, (255, 255, 200), (pulse_x, pulse_y), 1)
        
        # 在冶炼进度条上方添加百分比显示
        if smelting_progress > 0:
            percentage_text = font_small.render(f"{int(smelting_progress * 100)}%", True, (255, 255, 255))
            percentage_x = 熔炼进度条_x + (熔炼进度条宽度 - percentage_text.get_width()) // 2
            percentage_y = 熔炼进度条_y - 18  # 在进度条上方显示
            # 添加文字背景以提高可读性
            text_bg_rect = pygame.Rect(percentage_x - 2, percentage_y - 1, percentage_text.get_width() + 4, percentage_text.get_height() + 2)
            pygame.draw.rect(screen, (0, 0, 0), text_bg_rect, 0, 2)
            pygame.draw.rect(screen, (80, 80, 80), text_bg_rect, 1, 2)
            screen.blit(percentage_text, (percentage_x, percentage_y))
        
        # === 3. 燃料格（燃料槽）=== 位于燃烧格正下方，精确间距
        燃料格_x = 燃烧格_x  # 与燃烧格X坐标对齐
        燃料格_y = 燃烧格_y + 格子高度 + 元素间距 * 2  # 保持一致的间距
        
        # 绘制燃料格（燃料槽）
        pygame.draw.rect(screen, (70, 40, 40), (燃料格_x, 燃料格_y, 格子宽度, 格子高度), 0, 4)
        pygame.draw.rect(screen, (160, 100, 100), (燃料格_x, 燃料格_y, 格子宽度, 格子高度), 2, 4)
        
        # === 4. 燃烧进度条 === 位于燃料格右侧，确保与熔炼进度条在水平方向对齐
        燃烧进度条_x = 燃料格_x + 格子宽度 + 元素间距
        燃烧进度条_y = 燃料格_y  # 与燃料格顶部对齐
        燃烧进度条宽度 = 12  # 适中的宽度，提高可视性
        燃烧进度条_height = 格子高度
        
        # 确保燃烧进度条与熔炼进度条X坐标对齐
        燃烧进度条_x = 熔炼进度条_x
        
        # 绘制燃烧进度条背景（增强视觉效果）
        # 添加外阴影
        shadow_offset = 2
        pygame.draw.rect(screen, (20, 20, 20), 
                         (燃烧进度条_x + shadow_offset, 燃烧进度条_y + shadow_offset, 燃烧进度条宽度, 燃烧进度条_height), 0, 2)
        # 主背景
        pygame.draw.rect(screen, (40, 40, 40), (燃烧进度条_x, 燃烧进度条_y, 燃烧进度条宽度, 燃烧进度条_height), 0, 2)
        # 内边框
        pygame.draw.rect(screen, (80, 80, 80), (燃烧进度条_x + 1, 燃烧进度条_y + 1, 燃烧进度条宽度 - 2, 燃烧进度条_height - 2), 1, 2)
        
        # 计算燃料消耗动画
        animated_burn_progress = self.calculate_fuel_animation_progress(furnace_id)
        burn_progress = animated_burn_progress / 100  # 转换为0-1范围
        
        # 燃烧进度条高度
        progress_height = int(燃烧进度条_height * burn_progress)
        progress_y = 燃烧进度条_y + (燃烧进度条_height - progress_height)  # 从底部开始绘制
        
        # 绘制火焰进度条（增强视觉效果）
        if burn_progress > 0:
            # 上部分使用橙色（更亮的火焰）
            upper_height = max(1, int(progress_height * 0.6))
            upper_y = progress_y
            pygame.draw.rect(screen, (255, 140, 0), 
                             (燃烧进度条_x + 2, upper_y, 燃烧进度条宽度 - 4, upper_height), 0, 1)
            
            # 下部分使用红色（较暗的火焰）
            lower_height = progress_height - upper_height
            lower_y = upper_y + upper_height
            if lower_height > 0:
                pygame.draw.rect(screen, (200, 40, 0), 
                                 (燃烧进度条_x + 2, lower_y, 燃烧进度条宽度 - 4, lower_height), 0, 1)
            
            # 添加脉冲高光效果（动画进行时）
            if self.enable_animations and animated_burn_progress > 0 and animated_burn_progress < 100:
                pulse_intensity = int((pygame.time.get_ticks() % 400) / 400 * 60)  # 0-60的脉冲强度
                if pulse_intensity > 30:
                    # 在进度条顶部添加脉冲光效
                    pulse_y = 燃烧进度条_y + 燃烧进度条_height - 3
                    pygame.draw.circle(screen, (255, 200, 100), 
                                     (燃烧进度条_x + 燃烧进度条宽度 // 2, pulse_y), 2)
            
            # 添加火焰跳动效果
            if self.enable_animations and animated_burn_progress > 10:
                # 添加白色高光点，模拟火焰跳动
                flicker_intensity = int((pygame.time.get_ticks() % 150) / 150 * 50)  # 0-50的闪烁强度
                if flicker_intensity > 25:  # 只有在较亮时才显示
                    # 在进度条中上部分添加闪烁点
                    flicker_y = upper_y + upper_height // 2
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (燃烧进度条_x + 燃烧进度条宽度 // 2, flicker_y), 2)
        
        # 在燃料进度条右侧添加百分比显示
        if burn_progress > 0:
            burn_percentage_text = font_small.render(f"{int(burn_progress * 100)}%", True, (255, 255, 255))
            burn_percentage_x = 燃烧进度条_x + 燃烧进度条宽度 + 10  # 在进度条右侧显示
            burn_percentage_y = 燃烧进度条_y + (燃烧进度条_height - burn_percentage_text.get_height()) // 2  # 垂直居中
            # 添加文字背景以提高可读性
            burn_text_bg_rect = pygame.Rect(burn_percentage_x - 2, burn_percentage_y - 1, burn_percentage_text.get_width() + 4, burn_percentage_text.get_height() + 2)
            pygame.draw.rect(screen, (0, 0, 0), burn_text_bg_rect, 0, 2)
            pygame.draw.rect(screen, (80, 80, 80), burn_text_bg_rect, 1, 2)
            screen.blit(burn_percentage_text, (burn_percentage_x, burn_percentage_y))
        
        # === 5. 输出槽（存储格）绘制 - 2*3布局 === 位于右侧，与左侧系统对齐
        存储区域_x = 左侧区域_x + 左侧系统宽度 + 区域间距
        存储区域_y = 左侧区域_y  # 与左侧系统垂直对齐
        
        # 存储格行列数 (2行3列)
        存储格行数 = 2
        存储格列数 = 3
        存储格间距 = 6  # 略微增大存储格间距，使布局更清晰
        
        # 存储每个存储格的坐标，方便未来修改和引用
        存储格坐标 = []
        
        # 绘制2*3的存储格，排列整齐
        for 行 in range(存储格行数):
            for 列 in range(存储格列数):
                # 计算当前存储格的位置
                当前格_x = 存储区域_x + 列 * (格子宽度 + 存储格间距)
                当前格_y = 存储区域_y + 行 * (格子高度 + 存储格间距)
                
                # 存储坐标信息
                存储格坐标.append({
                    'x': 当前格_x,
                    'y': 当前格_y,
                    'width': 格子宽度,
                    'height': 格子高度
                })
                
                # 绘制存储格背景和边框
                pygame.draw.rect(screen, (40, 70, 50), 
                                 (当前格_x, 当前格_y, 格子宽度, 格子高度), 0, 4)
                pygame.draw.rect(screen, (100, 160, 120), 
                                 (当前格_x, 当前格_y, 格子宽度, 格子高度), 2, 4)
        
        # === 绘制左侧槽位中的物品图标和数量 ===
        # 获取当前熔炉数据
        furnace_key = (self.furnace_x, self.furnace_y)
        furnace_data = self.furnaces_data.get(furnace_key, {})
        
        # 1. 绘制燃烧槽（输入槽）中的物品
        input_item = furnace_data.get('input_slot_item')
        if input_item:
            # 计算物品绘制位置（居中）
            item_x = 燃烧格_x + 5
            item_y = 燃烧格_y + 5
            item_size = 格子宽度 - 10
            
            # 获取物品图像
            item_image = input_item.获取图像((item_size, item_size))
            if item_image:
                screen.blit(item_image, (item_x, item_y))
            else:
                # 没有图像时，绘制物品颜色块
                pygame.draw.rect(screen, input_item.获取颜色(), 
                               (item_x, item_y, item_size, item_size), 
                               border_radius=3)
            
            # 绘制物品数量（如果大于1）
            if input_item.数量 > 1:
                count_text = font_small.render(str(input_item.数量), True, (255, 255, 255))
                # 数量文本位置（右下角）
                count_x = 燃烧格_x + 格子宽度 - count_text.get_width() - 3
                count_y = 燃烧格_y + 格子高度 - count_text.get_height() - 3
                # 绘制数量背景
                bg_rect = pygame.Rect(count_x - 2, count_y - 2, 
                                    count_text.get_width() + 4, count_text.get_height() + 4)
                pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect, border_radius=3)
                # 绘制数量文本
                screen.blit(count_text, (count_x, count_y))
            
            # 绘制耐久度进度条
            max_durability = input_item.获取属性("耐久度", 0)
            if max_durability > 0:
                current_durability = input_item.获取属性("当前耐久度", max_durability)
                durability_percent = (current_durability / max_durability) * 100
                
                # 满95%+不显示耐久进度条
                if durability_percent < 95:
                    # 计算耐久度颜色（从红到绿渐变）
                    if durability_percent <= 50:
                        # 红到黄渐变 (0-50%)
                        ratio = durability_percent / 50
                        red = 255
                        green = int(255 * ratio)
                        blue = 0
                    else:
                        # 黄到绿渐变 (50-100%)
                        ratio = (durability_percent - 50) / 50
                        red = int(255 * (1 - ratio))
                        green = 255
                        blue = 0
                    
                    # 熔炉燃烧格显示3像素高度耐久进度条
                    progress_bar_height = 3
                    progress_bar_width = (格子宽度 - 10) * (durability_percent / 100)
                    
                    # 绘制背景条（灰色）
                    pygame.draw.rect(screen, (60, 60, 60), 
                                    (燃烧格_x + 5, 燃烧格_y + 格子高度 - progress_bar_height - 5, 
                                    格子宽度 - 10, progress_bar_height))
                    # 绘制耐久度条（彩色）
                    pygame.draw.rect(screen, (red, green, blue), 
                                    (燃烧格_x + 5, 燃烧格_y + 格子高度 - progress_bar_height - 5, 
                                    progress_bar_width, progress_bar_height))
        
        # 2. 绘制燃料槽中的物品
        fuel_item = furnace_data.get('fuel_slot_item')
        if fuel_item:
            # 计算物品绘制位置（居中）
            item_x = 燃料格_x + 5
            item_y = 燃料格_y + 5
            item_size = 格子宽度 - 10
            
            # 获取物品图像
            item_image = fuel_item.获取图像((item_size, item_size))
            if item_image:
                screen.blit(item_image, (item_x, item_y))
            else:
                # 没有图像时，绘制物品颜色块
                pygame.draw.rect(screen, fuel_item.获取颜色(), 
                               (item_x, item_y, item_size, item_size), 
                               border_radius=3)
            
            # 绘制物品数量（如果大于1）
            if fuel_item.数量 > 1:
                count_text = font_small.render(str(fuel_item.数量), True, (255, 255, 255))
                # 数量文本位置（右下角）
                count_x = 燃料格_x + 格子宽度 - count_text.get_width() - 3
                count_y = 燃料格_y + 格子高度 - count_text.get_height() - 3
                # 绘制数量背景
                bg_rect = pygame.Rect(count_x - 2, count_y - 2, 
                                    count_text.get_width() + 4, count_text.get_height() + 4)
                pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect, border_radius=3)
                # 绘制数量文本
                screen.blit(count_text, (count_x, count_y))
            
            # 绘制耐久度进度条
            max_durability = fuel_item.获取属性("耐久度", 0)
            if max_durability > 0:
                current_durability = fuel_item.获取属性("当前耐久度", max_durability)
                durability_percent = (current_durability / max_durability) * 100
                
                # 满95%+不显示耐久进度条
                if durability_percent < 95:
                    # 计算耐久度颜色（从红到绿渐变）
                    if durability_percent <= 50:
                        # 红到黄渐变 (0-50%)
                        ratio = durability_percent / 50
                        red = 255
                        green = int(255 * ratio)
                        blue = 0
                    else:
                        # 黄到绿渐变 (50-100%)
                        ratio = (durability_percent - 50) / 50
                        red = int(255 * (1 - ratio))
                        green = 255
                        blue = 0
                    
                    # 熔炉燃料格显示3像素高度耐久进度条
                    progress_bar_height = 3
                    progress_bar_width = (格子宽度 - 10) * (durability_percent / 100)
                    
                    # 绘制背景条（灰色）
                    pygame.draw.rect(screen, (60, 60, 60), 
                                    (燃料格_x + 5, 燃料格_y + 格子高度 - progress_bar_height - 5, 
                                    格子宽度 - 10, progress_bar_height))
                    # 绘制耐久度条（彩色）
                    pygame.draw.rect(screen, (red, green, blue), 
                                    (燃料格_x + 5, 燃料格_y + 格子高度 - progress_bar_height - 5, 
                                    progress_bar_width, progress_bar_height))
        
        # 3. 绘制输出槽中的物品
        output_items = furnace_data.get('output_slots', [])
        for i, 存储格 in enumerate(存储格坐标):
            if i < len(output_items):
                output_item = output_items[i]
                if output_item:
                    # 计算物品绘制位置（居中）
                    item_x = 存储格['x'] + 5
                    item_y = 存储格['y'] + 5
                    item_size = 格子宽度 - 10
                    
                    # 获取物品图像
                    item_image = output_item.获取图像((item_size, item_size))
                    if item_image:
                        screen.blit(item_image, (item_x, item_y))
                    else:
                        # 没有图像时，绘制物品颜色块
                        pygame.draw.rect(screen, output_item.获取颜色(), 
                                       (item_x, item_y, item_size, item_size), 
                                       border_radius=3)
                    
                    # 绘制物品数量（如果大于1）
                    if output_item.数量 > 1:
                        count_text = font_small.render(str(output_item.数量), True, (255, 255, 255))
                        # 数量文本位置（右下角）
                        count_x = 存储格['x'] + 格子宽度 - count_text.get_width() - 3
                        count_y = 存储格['y'] + 格子高度 - count_text.get_height() - 3
                        # 绘制数量背景
                        bg_rect = pygame.Rect(count_x - 2, count_y - 2, 
                                            count_text.get_width() + 4, count_text.get_height() + 4)
                        pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect, border_radius=3)
                        # 绘制数量文本
                        screen.blit(count_text, (count_x, count_y))
                    
                    # 绘制耐久度进度条
                    max_durability = output_item.获取属性("耐久度", 0)
                    if max_durability > 0:
                        current_durability = output_item.获取属性("当前耐久度", max_durability)
                        durability_percent = (current_durability / max_durability) * 100
                        
                        # 满95%+不显示耐久进度条
                        if durability_percent < 95:
                            # 计算耐久度颜色（从红到绿渐变）
                            if durability_percent <= 50:
                                # 红到黄渐变 (0-50%)
                                ratio = durability_percent / 50
                                red = 255
                                green = int(255 * ratio)
                                blue = 0
                            else:
                                # 黄到绿渐变 (50-100%)
                                ratio = (durability_percent - 50) / 50
                                red = int(255 * (1 - ratio))
                                green = 255
                                blue = 0
                            
                            # 熔炉输出槽显示3像素高度耐久进度条
                            progress_bar_height = 3
                            progress_bar_width = (格子宽度 - 10) * (durability_percent / 100)
                            
                            # 绘制背景条（灰色）
                            pygame.draw.rect(screen, (60, 60, 60), 
                                            (存储格['x'] + 5, 存储格['y'] + 格子高度 - progress_bar_height - 5, 
                                            格子宽度 - 10, progress_bar_height))
                            # 绘制耐久度条（彩色）
                            pygame.draw.rect(screen, (red, green, blue), 
                                            (存储格['x'] + 5, 存储格['y'] + 格子高度 - progress_bar_height - 5, 
                                            progress_bar_width, progress_bar_height))
        
        # === 槽位绘制函数 ===
        def draw_slot(x, y, is_hovered=False, slot_type="normal"):
            """绘制单个槽位，支持不同类型和悬停效果"""
            # 槽位背景颜色
            if slot_type == "input":
                slot_bg = (70, 60, 40)
                slot_border = (160, 140, 100)
            elif slot_type == "fuel":
                slot_bg = (70, 40, 40)
                slot_border = (160, 100, 100)
            elif slot_type == "output":
                slot_bg = (40, 70, 50)
                slot_border = (100, 160, 120)
            else:
                slot_bg = COLORS['slot_hover'] if is_hovered else COLORS['slot_normal']
                slot_border = COLORS['border_light'] if is_hovered else COLORS['border_medium']
            
            # 绘制槽位背景
            pygame.draw.rect(screen, slot_bg, (x, y, slot_size, slot_size), 0, 4)
            # 外边框
            pygame.draw.rect(screen, slot_border, (x, y, slot_size, slot_size), 2, 4)
            # 内边框阴影
            pygame.draw.rect(screen, (0, 0, 0, 30), 
                             (x + 2, y + 2, slot_size - 4, slot_size - 4), 1, 3)
            
            return pygame.Rect(x, y, slot_size, slot_size)
        
        
        # === 右侧背包区域 - 适配新的页面尺寸 ===
        backpack_x = page_x + 340  # 向左移动40像素以调整布局（底部左侧增加10像素）
        backpack_y = page_y + title_bar_height + 20
        # 增加背包区域宽度以容纳6列格子并增加额外空间
        backpack_width = 320  # 增加50像素宽度（底部右侧增加10像素）
        backpack_height = 300
        
        # 绘制背包区域背景
        pygame.draw.rect(screen, COLORS['bg_medium'], 
                         (backpack_x, backpack_y, backpack_width, backpack_height), 0, 6)
        pygame.draw.rect(screen, COLORS['border_medium'], 
                         (backpack_x, backpack_y, backpack_width, backpack_height), 2, 6)
        
        # 背包标题
        backpack_title = font_medium.render("物品栏", True, COLORS['text_primary'])
        title_bg_rect = pygame.Rect(backpack_x + 10, backpack_y + 10, 
                                   backpack_width - 20, 25)
        pygame.draw.rect(screen, COLORS['bg_dark'], title_bg_rect, 0, 3)
        pygame.draw.rect(screen, COLORS['border_dark'], title_bg_rect, 1, 3)
        title_x = backpack_x + 20
        screen.blit(backpack_title, (title_x, backpack_y + 12))
        
        # 背包格子参数 - 改为5*6布局
        backpack_rows = 5
        backpack_cols = 6
        backpack_start_x = backpack_x + 15
        backpack_start_y = backpack_y + 50
        
        # 重置悬停状态
        self.当前悬停物品 = None
        self.当前悬停物品_rect = None
        self.当前悬停位置 = None
        
        # 检测鼠标悬停位置
        hover_detected = False
        
        # 绘制背包格子和物品
        for row in range(backpack_rows):
            for col in range(backpack_cols):
                x = backpack_start_x + col * (slot_size + slot_margin)
                y = backpack_start_y + row * (slot_size + slot_margin)
                
                # 检查是否悬停
                is_hovered = x <= mouse_pos[0] <= x + slot_size and \
                            y <= mouse_pos[1] <= y + slot_size
                
                # 绘制格子
                draw_slot(x, y, is_hovered)
                
                # 绘制背包物品
                if hasattr(self.game, '背包管理器'):
                    current_item = self.game.背包管理器.背包物品[row][col]
                    if current_item:
                        # 计算物品绘制位置（居中）
                        item_x = x + 5
                        item_y = y + 5
                        item_size = slot_size - 10
                        
                        # 获取物品图像
                        item_image = current_item.获取图像((item_size, item_size))
                        if item_image:
                            screen.blit(item_image, (item_x, item_y))
                        else:
                            # 没有图像时，绘制物品颜色块
                            pygame.draw.rect(screen, current_item.获取颜色(), 
                                           (item_x, item_y, item_size, item_size), 
                                           border_radius=3)
                        
                        # 绘制物品数量（如果大于1）
                        if current_item.数量 > 1:
                            count_text = font_small.render(str(current_item.数量), True, (255, 255, 255))
                            # 数量文本位置（右下角）
                            count_x = x + slot_size - count_text.get_width() - 3
                            count_y = y + slot_size - count_text.get_height() - 3
                            # 绘制数量背景
                            bg_rect = pygame.Rect(count_x - 2, count_y - 2, 
                                                count_text.get_width() + 4, count_text.get_height() + 4)
                            pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect, border_radius=3)
                            # 绘制数量文本
                            screen.blit(count_text, (count_x, count_y))
                        
                        # 绘制耐久度进度条
                        max_durability = current_item.获取属性("耐久度", 0)
                        if max_durability > 0:
                            current_durability = current_item.获取属性("当前耐久度", max_durability)
                            durability_percent = (current_durability / max_durability) * 100
                            
                            # 满95%+不显示耐久进度条
                            if durability_percent < 95:
                                # 计算耐久度颜色（从红到绿渐变）
                                if durability_percent <= 50:
                                    # 红到黄渐变 (0-50%)
                                    ratio = durability_percent / 50
                                    red = 255
                                    green = int(255 * ratio)
                                    blue = 0
                                else:
                                    # 黄到绿渐变 (50-100%)
                                    ratio = (durability_percent - 50) / 50
                                    red = int(255 * (1 - ratio))
                                    green = 255
                                    blue = 0
                                
                                # 熔炉背包显示3像素高度耐久进度条
                                progress_bar_height = 3
                                progress_bar_width = (slot_size - 10) * (durability_percent / 100)
                                
                                # 绘制背景条（灰色）
                                pygame.draw.rect(screen, (60, 60, 60), 
                                                (x + 5, y + slot_size - progress_bar_height - 5, 
                                                slot_size - 10, progress_bar_height))
                                # 绘制耐久度条（彩色）
                                pygame.draw.rect(screen, (red, green, blue), 
                                                (x + 5, y + slot_size - progress_bar_height - 5, 
                                                progress_bar_width, progress_bar_height))
                    
                    # 检测鼠标悬停
                    if is_hovered and not hover_detected:
                        hover_detected = True
                        self.当前悬停位置 = f"背包 {row+1}*{col+1}"
                        if current_item:
                            self.当前悬停物品 = current_item.物品信息
                            self.当前悬停物品_rect = pygame.Rect(x, y, slot_size, slot_size)
                        print(f"停留位置: {self.当前悬停位置}")
        
        # === 底部快捷栏 - 适配新的页面尺寸 ===
        hotbar_y = page_y + page_height - 70
        hotbar_width = 660  # 增加宽度以适配新页面
        hotbar_height = 50
        hotbar_x = page_x + 20
        
        # 绘制8个快捷栏格子 - 居中显示
        # 计算8个格子的总宽度（8个格子 + 7个间距）
        total_hotbar_slots_width = 8 * slot_size + 7 * slot_margin
        # 计算居中的起始X坐标
        hotbar_slot_start_x = hotbar_x + (hotbar_width - total_hotbar_slots_width) // 2
        hotbar_slot_y = hotbar_y + 7
        
        for i in range(8):
            x = hotbar_slot_start_x + i * (slot_size + slot_margin)
            y = hotbar_slot_y
            
            # 检查是否悬停
            is_hovered = x <= mouse_pos[0] <= x + slot_size and \
                        y <= mouse_pos[1] <= y + slot_size
            
            # 绘制格子
            draw_slot(x, y, is_hovered)
            
            # 绘制快捷栏物品
            if hasattr(self.game, '背包管理器'):
                current_item = self.game.背包管理器.快捷栏物品[i]
                if current_item:
                    # 计算物品绘制位置（居中）
                    item_x = x + 5
                    item_y = y + 5
                    item_size = slot_size - 10
                    
                    # 获取物品图像
                    item_image = current_item.获取图像((item_size, item_size))
                    if item_image:
                        screen.blit(item_image, (item_x, item_y))
                    else:
                        # 没有图像时，绘制物品颜色块
                        pygame.draw.rect(screen, current_item.获取颜色(), 
                                       (item_x, item_y, item_size, item_size), 
                                       border_radius=3)
                    
                    # 绘制物品数量（如果大于1）
                    if current_item.数量 > 1:
                        count_text = font_small.render(str(current_item.数量), True, (255, 255, 255))
                        # 数量文本位置（右下角）
                        count_x = x + slot_size - count_text.get_width() - 3
                        count_y = y + slot_size - count_text.get_height() - 3
                        # 绘制数量背景
                        bg_rect = pygame.Rect(count_x - 2, count_y - 2, 
                                            count_text.get_width() + 4, count_text.get_height() + 4)
                        pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect, border_radius=3)
                        # 绘制数量文本
                        screen.blit(count_text, (count_x, count_y))
                    
                    # 绘制耐久度进度条
                    max_durability = current_item.获取属性("耐久度", 0)
                    if max_durability > 0:
                        current_durability = current_item.获取属性("当前耐久度", max_durability)
                        durability_percent = (current_durability / max_durability) * 100
                        
                        # 满95%+不显示耐久进度条
                        if durability_percent < 95:
                            # 计算耐久度颜色（从红到绿渐变）
                            if durability_percent <= 50:
                                # 红到黄渐变 (0-50%)
                                ratio = durability_percent / 50
                                red = 255
                                green = int(255 * ratio)
                                blue = 0
                            else:
                                # 黄到绿渐变 (50-100%)
                                ratio = (durability_percent - 50) / 50
                                red = int(255 * (1 - ratio))
                                green = 255
                                blue = 0
                            
                            # 熔炉快捷栏显示3像素高度耐久进度条
                            progress_bar_height = 3
                            progress_bar_width = (slot_size - 10) * (durability_percent / 100)
                            
                            # 绘制背景条（灰色）
                            pygame.draw.rect(screen, (60, 60, 60), 
                                            (x + 5, y + slot_size - progress_bar_height - 5, 
                                            slot_size - 10, progress_bar_height))
                            # 绘制耐久度条（彩色）
                            pygame.draw.rect(screen, (red, green, blue), 
                                            (x + 5, y + slot_size - progress_bar_height - 5, 
                                            progress_bar_width, progress_bar_height))
                    
                    # 检测鼠标悬停
                    if is_hovered and not hover_detected:
                        hover_detected = True
                        self.当前悬停位置 = f"快捷栏 {i+1}"
                        if current_item:
                            self.当前悬停物品 = current_item.物品信息
                            self.当前悬停物品_rect = pygame.Rect(x, y, slot_size, slot_size)
                        print(f"停留位置: {self.当前悬停位置}")
        
        # 检测燃料槽悬停
        燃料槽_rect = pygame.Rect(燃料格_x, 燃料格_y, 格子宽度, 格子高度)
        if 燃料槽_rect.collidepoint(mouse_pos) and not hover_detected:
            hover_detected = True
            self.当前悬停位置 = "燃料槽"
            furnace_key = (self.furnace_x, self.furnace_y)
            furnace_data = self.furnaces_data.get(furnace_key, {})
            fuel_item = furnace_data.get('fuel_slot_item')
            if fuel_item:
                self.当前悬停物品 = fuel_item.物品信息
                self.当前悬停物品_rect = 燃料槽_rect
            print(f"停留位置: {self.当前悬停位置}")
        
        # 检测燃烧槽悬停
        燃烧槽_rect = pygame.Rect(燃烧格_x, 燃烧格_y, 格子宽度, 格子高度)
        if 燃烧槽_rect.collidepoint(mouse_pos) and not hover_detected:
            hover_detected = True
            self.当前悬停位置 = "燃烧槽"
            furnace_key = (self.furnace_x, self.furnace_y)
            furnace_data = self.furnaces_data.get(furnace_key, {})
            input_item = furnace_data.get('input_slot_item')
            if input_item:
                self.当前悬停物品 = input_item.物品信息
                self.当前悬停物品_rect = 燃烧槽_rect
            print(f"停留位置: {self.当前悬停位置}")
        
        # 检测输出槽悬停
        for i, 存储格 in enumerate(存储格坐标):
            输出槽_rect = pygame.Rect(存储格['x'], 存储格['y'], 存储格['width'], 存储格['height'])
            if 输出槽_rect.collidepoint(mouse_pos) and not hover_detected:
                hover_detected = True
                self.当前悬停位置 = f"输出槽 {i+1}"
                furnace_key = (self.furnace_x, self.furnace_y)
                furnace_data = self.furnaces_data.get(furnace_key, {})
                output_items = furnace_data.get('output_slots', [])
                if i < len(output_items) and output_items[i]:
                    self.当前悬停物品 = output_items[i].物品信息
                    self.当前悬停物品_rect = 输出槽_rect
                print(f"停留位置: {self.当前悬停位置}")
                break
        
        # 绘制物品提示
        if self.当前悬停物品 and self.当前悬停物品_rect:
            # 获取物品信息
            物品名称 = self.当前悬停物品.get("名称", "未知物品")
            物品介绍 = self.当前悬停物品.get("说明", "无说明")
            
            # 创建提示文本
            名称文本 = f"物品:{物品名称}"
            介绍文本前缀 = "介绍:"
            介绍文本内容 = 物品介绍
            
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
            名称_lines = wrap_text(物品名称, font_small, 20)
            # 重新构建带前缀的名称文本行
            名称_full_lines = [f"物品:{line}" for line in 名称_lines]
            
            # 处理介绍文本的换行
            介绍_lines = wrap_text(介绍文本内容, font_small, 20)
            # 第一行需要加上前缀
            if 介绍_lines:
                介绍_lines[0] = 介绍文本前缀 + 介绍_lines[0]
            
            # 渲染所有文本行
            文本_surfaces = []
            # 渲染名称行
            for line in 名称_full_lines:
                文本_surfaces.append(font_small.render(line, True, COLORS['text_primary']))
            # 渲染介绍行
            for line in 介绍_lines:
                文本_surfaces.append(font_small.render(line, True, COLORS['text_secondary']))
            
            # 计算提示框尺寸
            行高 = font_small.get_height()
            最大宽度 = max(surface.get_width() for surface in 文本_surfaces)
            提示框宽度 = 最大宽度 + 16
            提示框高度 = len(文本_surfaces) * 行高 + 12
            
            # 计算提示框位置（在物品格子上方）
            提示框_x = self.当前悬停物品_rect.x + self.当前悬停物品_rect.width // 2 - 提示框宽度 // 2
            提示框_y = self.当前悬停物品_rect.y - 提示框高度 - 10
            
            # 确保提示框不会超出屏幕边界
            if 提示框_x < 0:
                提示框_x = 0
            elif 提示框_x + 提示框宽度 > WIDTH:
                提示框_x = WIDTH - 提示框宽度
            
            if 提示框_y < 0:
                提示框_y = self.当前悬停物品_rect.y + self.当前悬停物品_rect.height + 10
            
            # 绘制提示框背景
            提示框_rect = pygame.Rect(提示框_x, 提示框_y, 提示框宽度, 提示框高度)
            pygame.draw.rect(screen, COLORS['bg_medium'], 提示框_rect, border_radius=5)
            pygame.draw.rect(screen, COLORS['border_medium'], 提示框_rect, 1, border_radius=5)
            
            # 绘制所有文本行
            current_y = 提示框_y + 6
            for surface in 文本_surfaces:
                screen.blit(surface, (提示框_x + 8, current_y))
                current_y += 行高
        
        # 绘制拖拽中的物品
        鼠标位置 = pygame.mouse.get_pos()
        if self.拖拽中的物品:
            # 绘制左键拖拽的物品
            物品, _, _ = self.拖拽中的物品
            self._绘制拖拽物品(screen, 物品, 鼠标位置, 是拆分物品=False)
        
        if self.右键拆分的物品:
            # 绘制右键拆分的物品
            物品, _, _ = self.右键拆分的物品
            self._绘制拖拽物品(screen, 物品, 鼠标位置, 是拆分物品=True)
        
        # 删除底部提示文字
        
        return close_button_rect
    
    def _绘制拖拽物品(self, screen, 物品, 鼠标位置, 是拆分物品=False):
        """绘制拖拽中的物品"""
        # 格子尺寸
        slot_size = 44
        
        # 计算物品绘制尺寸
        物品_size = slot_size - 10
        
        # 创建物品表面
        物品表面 = pygame.Surface((物品_size, 物品_size), pygame.SRCALPHA)
        
        # 拆分物品添加半透明效果区分
        透明度 = 150 if 是拆分物品 else 200
        
        # 获取物品图像
        物品图像 = 物品.获取图像((物品_size, 物品_size))
        if 物品图像:
            # 拆分物品添加半透明效果
            if 是拆分物品:
                # 创建半透明表面
                半透明表面 = pygame.Surface((物品_size, 物品_size), pygame.SRCALPHA)
                半透明表面.fill((255, 255, 255, 透明度))
                # 绘制物品图像
                物品表面.blit(物品图像, (0, 0))
                # 应用半透明效果
                物品表面.blit(半透明表面, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            else:
                # 直接绘制物品图像
                物品表面.blit(物品图像, (0, 0))
        else:
            # 没有图像时，绘制物品颜色块
            颜色 = 物品.获取颜色() + (透明度,)
            pygame.draw.rect(物品表面, 颜色, 物品表面.get_rect(), border_radius=3)
        
        # 绘制物品数量
        if 物品.数量 > 1:
            # 创建字体
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
            
            font_small = load_font(14)
            数量文本 = font_small.render(str(物品.数量), True, (255, 255, 255))
            物品表面.blit(数量文本, (物品_size - 数量文本.get_width() - 3, 物品_size - 数量文本.get_height() - 3))
        
        # 绘制物品到屏幕
        screen.blit(物品表面, (鼠标位置[0] - 物品_size // 2, 鼠标位置[1] - 物品_size // 2))