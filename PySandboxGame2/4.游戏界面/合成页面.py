import pygame
import sys

# 导入图片加载器
from 图片加载 import 图片管理器
from 物品定义 import 小煤块, 岩石, 物品, 红石, 金锭
from 音频输出 import audio_manager

# 深色主题配色方案
主背景色 = (26, 27, 29)      # 更深灰色主背景
次级背景色 = (39, 40, 40)    # 深灰色次级背景
边框颜色 = (70, 70, 70)      # 中灰色边框
标题颜色 = (220, 220, 220)   # 浅色标题
文本颜色 = (240, 240, 240)   # 浅色文本
阴影颜色 = (0, 0, 0, 80)     # 更明显的半透明黑色阴影
普通格子背景 = (48, 48, 48)  # 普通格子背景色
悬停格子背景 = (60, 60, 60)  # 悬停格子背景色
结果槽背景 = (90, 70, 50)    # 结果槽背景色

class CraftingPage:
    """合成页面类，负责处理游戏中的物品合成功能"""
    def __init__(self, game):
        """初始化合成页面"""
        self.game = game
        self.is_open = False  # 默认关闭合成页面
        self.slot_size = 48  # 格子大小
        self.slot_margin = 4  # 格子间距
        
        # 界面尺寸和位置
        self.底1宽度 = 200  # 左侧面板宽度
        self.底1高度 = 700  # 左侧面板高度
        self.底2宽度 = 850  # 右侧面板宽度
        self.底2高度 = 700  # 右侧面板高度
        self.间隔 = 10      # 两面板间隔
        
        # 合成区域配置
        self.crafting_grid_size = 3  # 3x3合成格
        
        # 圆角半径和字体设置
        self.圆角半径 = 10
        try:
            self.标题字体 = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial Unicode MS", "SimSun"], 24, True)
            self.文本字体 = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial Unicode MS", "SimSun"], 16)
            # 提示文字字体
            self.提示字体 = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial Unicode MS", "SimSun"], 20, True)
        except:
            self.标题字体 = pygame.font.SysFont(None, 24, True)
            self.文本字体 = pygame.font.SysFont(None, 16)
            self.提示字体 = pygame.font.SysFont(None, 20, True)
        
        # 当前悬停的格子
        self.hovered_slot = None
        
        # 提示文字相关属性
        self.notifications = []  # 存储当前显示的提示信息列表
        self.提示移动速度 = 50  # 提示文字向上移动的速度（像素/秒）
        self.提示显示时间 = 3.0  # 提示文字显示的总时间（秒）
        self.当前时间 = pygame.time.get_ticks() / 1000.0  # 当前时间（秒）
        
        # 当前悬停的格子
        self.hovered_slot = None
        
        # 初始化解锁的合成配方
        self.unlocked_recipes = []
        
        # 合成分类按钮配置
        self.crafting_categories = ["基础", "装备类", "建筑类", "特殊类", "材料类", "方块类", "其他"]
        self.current_category = "基础"  # 当前选中的分类
        
        # 打开方式：'workbench' 或 'keyboard'（C键）
        self.open_type = None
        
        # 创建物品ID映射表，将图标名称映射到物品定义中的物品ID
        # 直接使用物品ID的数值，避免导入问题
        self.物品_id映射 = {
            "火把": 10012,
            "熔炉": 10043,
            "工作台": 10033,
            "床_完整": 10032,
            "木斧": 16200,
            "木镐": 16100,
            "木铲": 16300,
            "石斧": 16201,
            "石镐": 16101,
            "石铲": 16301,
            "铁斧": 16203,
            "铁镐": 16103,
            "铁铲": 16303,
            "铜斧": 16202,
            "铜镐": 16102,
            "铜铲": 16302,
            "金斧": 16204,
            "金镐": 16104,
            "金铲": 16304,
            "钻石斧头": 16205,
            "钻石镐": 16105,
            "钻石铲": 16305,
            "木板": 10017,
            "箱子": 10011,
            # 基础材料
            "木头": 10004,
            "乔木": 10026,
            "岩石": 10003,
            "木炭": 15008,
            # 建筑方块
            "金块": 10019,
            "铁块": 10020,
            "钻石块": 10021,
            "铜块": 10022,
            "红方块": 10034,
            "红石块": 10036,
            "蓝方块": 10037,
            "蓝石块": 10039,
            "紫石块": 10042,
            # 头盔类装备
            "1级头盔": 19000,
            "2级头盔": 19001,
            "3级头盔": 19002,
            "4级头盔": 19003,
            "5级头盔": 19004,
            # 盔甲类装备
            "1级盔甲": 19010,
            "2级盔甲": 19011,
            "3级盔甲": 19012,
            "4级盔甲": 19013,
            "5级盔甲": 19014,
            # 靴子类装备
            "1级靴子": 19020,
            "2级靴子": 19021,
            "3级靴子": 19022,
            "4级靴子": 19023,
            "5级靴子": 19024,
            # 特殊装备
            "1级斗篷": 19030,
            "2级披风": 19031,
            "3级灵服": 19032,
            "4级披风": 19033,
            "5级腰带": 19034,
            # 剑类武器
            "木剑": 16000,
            "石剑": 16001,
            "铜剑": 16002,
            "铁剑": 16003,
            "金剑": 16004,
            "钻石剑": 16005,
            # 远程武器
            "木弓箭": 16020,
            "木箭": 16021,
            "弩": 16032,
            # 高科技武器
            "未来弩": 16026,
            "激光炮": 16027,
            # 枪械武器
            "步枪": 16022,
            "手枪": 16023,
            "狙击枪": 16024,
            "喷子": 16034,
            "子弹": 16025,
            # 重型武器
            "火箭筒": 16028,
            "火箭弹": 16029,
            #特殊类
            "煤块" : 10040,
            # 材料类
            "红石": 15000,
            "金锭": 15001,
            "蓝石": 15002,
            "石子": 15003,
            "铁锭": 15004,
            "铜锭": 15005,
            "小煤块": 15006,
            "钻石": 15007,
            # 方块类
            "玻璃": 10044,
            #其他
            "枯草": 10024,
            "沙子": 10023,

            # 回血瓶
            "1级回血瓶": 18000,
            "2级回血瓶": 18001,
            "3级回血瓶": 18002,
            "4级回血瓶": 18003,
            # 食物
            "苹果": 17000,
            "肉块": 17001,
            "乔木果": 17002,
            "红花": 10014,
            "草": 10015,
        }
        
        self.craftable_items = {
            "基础": [
                {"icon": "火把", "recipe": {"木板": 1, "煤块": 1}, "quantity": 4},
                {"icon": "熔炉", "recipe": {"岩石": 4}, "quantity": 1},
                {"icon": "工作台", "recipe": {"木板": 4}, "quantity": 1},
                {"icon": "箱子", "recipe": {"木头": 1, "木板": 3}, "quantity": 1},
                {"icon": "床_完整", "recipe": {"木板": 2, "枯草": 2}, "quantity": 1},
                {"icon": "木斧", "recipe": {"木板": 4}, "quantity": 1},
                {"icon": "木镐", "recipe": {"木板": 4}, "quantity": 1},
                {"icon": "木铲", "recipe": {"木板": 3}, "quantity": 1},
                {"icon": "石斧", "recipe": {"岩石": 2, "木板": 2}, "quantity": 1},
                {"icon": "石镐", "recipe": {"岩石": 2, "木板": 2}, "quantity": 1},
                {"icon": "石铲", "recipe": {"岩石": 2, "木板": 2}, "quantity": 1},
                {"icon": "铁斧", "recipe": {"铁锭": 3, "木板": 2}, "quantity": 1},
                {"icon": "铁镐", "recipe": {"铁锭": 3, "木板": 2}, "quantity": 1},
                {"icon": "铁铲", "recipe": {"铁锭": 2, "木板": 2}, "quantity": 1},
                {"icon": "铜斧", "recipe": {"铜锭": 3, "木板": 2}, "quantity": 1},
                {"icon": "铜镐", "recipe": {"铜锭": 3, "木板": 2}, "quantity": 1},
                {"icon": "铜铲", "recipe": {"铜锭": 2, "木板": 2}, "quantity": 1},
                {"icon": "金斧", "recipe": {"金锭": 3, "木板": 2}, "quantity": 1},
                {"icon": "金镐", "recipe": {"金锭": 3, "木板": 2}, "quantity": 1},
                {"icon": "金铲", "recipe": {"金锭": 2, "木板": 2}, "quantity": 1},
                {"icon": "钻石斧头", "recipe": {"钻石": 2, "木板": 2}, "quantity": 1},
                {"icon": "钻石镐", "recipe": {"钻石": 3, "木板": 2}, "quantity": 1},
                {"icon": "钻石铲", "recipe": {"钻石": 2, "木板": 2}, "quantity": 1},
                {"icon": "木板", "recipe": {"木头": 1}, "quantity": 3},
                {"icon": "木板", "recipe": {"乔木": 1}, "quantity": 4}
            ],
            "装备类": [
                # 头盔类装备
                {"icon": "1级头盔", "recipe": {"铜锭": 4}, "quantity": 1},
                {"icon": "2级头盔", "recipe": {"铁锭": 4}, "quantity": 1},
                {"icon": "3级头盔", "recipe": {"金锭": 4}, "quantity": 1},
                {"icon": "4级头盔", "recipe": {"钻石": 1, "金锭": 3}, "quantity": 1},
                {"icon": "5级头盔", "recipe": {"钻石": 4}, "quantity": 1},
                # 盔甲类装备
                {"icon": "1级盔甲", "recipe": {"铜锭": 4}, "quantity": 1},
                {"icon": "2级盔甲", "recipe": {"铁锭": 4}, "quantity": 1},
                {"icon": "3级盔甲", "recipe": {"金锭": 4}, "quantity": 1},
                {"icon": "4级盔甲", "recipe": {"钻石": 1, "金锭": 3}, "quantity": 1},
                {"icon": "5级盔甲", "recipe": {"钻石": 4}, "quantity": 1},
                # 靴子类装备
                {"icon": "1级靴子", "recipe": {"铜锭": 4}, "quantity": 1},
                {"icon": "2级靴子", "recipe": {"铁锭": 4}, "quantity": 1},
                {"icon": "3级靴子", "recipe": {"金锭": 4}, "quantity": 1},
                {"icon": "4级靴子", "recipe": {"钻石": 1, "金锭": 3}, "quantity": 1},
                {"icon": "5级靴子", "recipe": {"钻石": 4}, "quantity": 1},
                # 特殊装备
                {"icon": "1级斗篷", "recipe": {"铜锭": 4, "枯草": 1}, "quantity": 1},
                {"icon": "2级披风", "recipe": {"铁锭": 4, "枯草": 1}, "quantity": 1},
                {"icon": "3级灵服", "recipe": {"金锭": 4, "枯草": 1}, "quantity": 1},
                {"icon": "4级披风", "recipe": {"钻石": 1, "金锭": 3, "枯草": 1}, "quantity": 1},
                {"icon": "5级腰带", "recipe": {"钻石": 4, "枯草": 1}, "quantity": 1},
                # 剑类武器
                {"icon": "木剑", "recipe": {"木头": 3, "木板": 2}, "quantity": 1},
                {"icon": "石剑", "recipe": {"岩石": 3, "木板": 2}, "quantity": 1},
                {"icon": "铜剑", "recipe": {"铜锭": 3, "木板": 2}, "quantity": 1},
                {"icon": "铁剑", "recipe": {"铁锭": 3, "木板": 2}, "quantity": 1},
                {"icon": "金剑", "recipe": {"金锭": 3, "木板": 2}, "quantity": 1},
                {"icon": "钻石剑", "recipe": {"钻石": 3, "木板": 2}, "quantity": 1},
                # 远程武器
                {"icon": "木弓箭", "recipe": {"木头": 3, "枯草": 2, "木板": 2}, "quantity": 1},
                {"icon": "木箭", "recipe": {"枯草": 2, "木板": 1}, "quantity": 10},
                {"icon": "弩", "recipe": {"铁锭": 3, "木头": 2, "枯草": 2}, "quantity": 1},
                # 高科技武器
                {"icon": "未来弩", "recipe": {"钻石": 88}, "quantity": 1},
                {"icon": "激光炮", "recipe": {"钻石": 88}, "quantity": 1},
                # 枪械武器
                {"icon": "步枪", "recipe": {"铁锭": 3, "钻石": 1, "金锭": 1}, "quantity": 1},
                {"icon": "手枪", "recipe": {"铁锭": 3, "金锭": 1}, "quantity": 1},
                {"icon": "狙击枪", "recipe": {"铁锭": 3, "钻石": 2, "金锭": 1}, "quantity": 1},
                {"icon": "喷子", "recipe": {"铁锭": 4, "金锭": 2}, "quantity": 1},
                {"icon": "子弹", "recipe": {"铁锭": 1, "木炭": 1, "小煤块": 1}, "quantity": 10},
                # 重型武器
                {"icon": "火箭筒", "recipe": {"铁锭": 3, "钻石": 3, "金锭": 1}, "quantity": 1},
                {"icon": "火箭弹", "recipe": {"铁锭": 1, "木炭": 1, "小煤块": 1}, "quantity": 1}
            ],
            "建筑类": [
                # 建筑方块
                {"icon": "金块", "recipe": {"金锭": 9}, "quantity": 1},
                {"icon": "铁块", "recipe": {"铁锭": 9}, "quantity": 1},
                {"icon": "钻石块", "recipe": {"钻石": 9}, "quantity": 1},
                {"icon": "铜块", "recipe": {"铜锭": 9}, "quantity": 1},
                {"icon": "红方块", "recipe": {"红石": 1, "岩石": 1}, "quantity": 1},
                {"icon": "红石块", "recipe": {"红石": 9}, "quantity": 1},
                {"icon": "蓝方块", "recipe": {"蓝石": 1, "岩石": 1}, "quantity": 1},
                {"icon": "蓝石块", "recipe": {"蓝石": 9}, "quantity": 1},
                {"icon": "紫石块", "recipe": {"红石": 4, "蓝石": 4}, "quantity": 1}
            ],
            "特殊类": [
                {"icon": "煤块", "recipe": {"小煤块": 9}, "quantity": 1}  # 原逻辑可能是小煤块合成煤块，修正避免循环
            ],
            "材料类": [
                # 材料类物品
                {"icon": "红石", "recipe": {"红石块": 1}, "quantity": 9},
                {"icon": "金锭", "recipe": {"金块": 1}, "quantity": 9},
                {"icon": "蓝石", "recipe": {"蓝石块": 1}, "quantity": 9},
                {"icon": "石子", "recipe": {"岩石": 1}, "quantity": 9},
                {"icon": "铁锭", "recipe": {"铁块": 1}, "quantity": 9},
                {"icon": "铜锭", "recipe": {"铜块": 1}, "quantity": 9},
                {"icon": "小煤块", "recipe": {"煤块": 1}, "quantity": 9},
                {"icon": "钻石", "recipe": {"钻石块": 1}, "quantity": 9},
            ],
            "方块类": [
                {"icon": "玻璃", "recipe": {"沙子": 5}, "quantity": 1},
            ],
            "其他": [
                {"icon": "1级回血瓶", "recipe": {"草": 1,"红花": 1}, "quantity": 2},
                {"icon": "2级回血瓶", "recipe": {"草": 1,"红花": 1,"苹果": 1}, "quantity": 2},
                {"icon": "3级回血瓶", "recipe": {"草": 1,"红花": 1,"苹果": 1,"乔木果": 1}, "quantity": 2},
                {"icon": "4级回血瓶", "recipe": {"草": 1,"红花": 1,"苹果": 1,"乔木果": 1,"肉块": 1}, "quantity": 2},
            ]
        }
        # 当前选中的物品
        self.selected_item = None
        
        # 物品网格配置
        self.item_grid_size = 9  # 每行显示4个物品
        self.item_slot_size = 48  # 物品格子大小
        self.item_slot_margin = 8  # 物品格子间距
        self.button_height = 40  # 按钮高度
        self.button_padding = 5  # 按钮内边距
        self.button_margin = 10  # 按钮间距
        self.normal_button_color = (48, 48, 48)  # 按钮正常颜色
        self.hovered_button_color = (60, 60, 60)  # 按钮悬停颜色
        self.selected_button_color = (70, 70, 70)  # 按钮选中颜色
        self.button_text_color = (220, 220, 220)  # 按钮文字颜色
        # 退出按钮颜色设置
        self.exit_button_normal_color = (80, 80, 80)
        self.exit_button_hover_color = (100, 100, 100)
        self.exit_button_text_color = (240, 240, 240)
        
        # 合成数量控制相关属性
        self.craft_amount = 1  # 当前合成数量
        self.min_amount = 1    # 最小合成数量
        self.max_amount = 99   # 最大合成数量
        
        # 数量控制按钮属性
        self.control_button_width = 40  # 控制按钮宽度
        self.control_button_height = 30  # 控制按钮高度
        self.input_width = 60  # 输入框宽度
        self.input_height = 30  # 输入框高度
        self.confirm_button_width = 120  # 确定按钮宽度
        self.confirm_button_height = 40  # 确定按钮高度
        self.button_spacing = 5  # 按钮间距
        
        # 数量控制按钮颜色
        self.control_button_normal = (48, 48, 48)
        self.control_button_hover = (60, 60, 60)
        self.control_button_text = (220, 220, 220)
        self.confirm_button_normal = (50, 100, 50)
        self.confirm_button_hover = (60, 120, 60)
        self.confirm_button_text = (240, 240, 240)
        self.input_bg_color = (30, 30, 30)
        self.input_active_bg_color = (45, 45, 45)
        self.input_border_color = (70, 70, 70)
        self.input_active_border_color = (72, 133, 237)  # 蓝色强调色
        
        # 悬停状态
        self.hovered_control_button = None  # 当前悬停的控制按钮
        self.hovered_confirm_button = False  # 是否悬停在确定按钮上
        self.hovered_input_box = False  # 是否悬停在输入框上
        
        # 输入框相关属性
        self.is_input_active = False  # 输入框是否激活
        self.input_text = str(self.craft_amount)  # 输入框文本
        self.active_input = None  # 当前激活的输入框类型
        self.cursor_visible = True  # 光标是否可见
        self.cursor_blink_time = 0  # 光标闪烁计时器
        self.cursor_blink_interval = 0.5  # 光标闪烁间隔（秒）
        
        # 初始化面板位置
        self._update_panel_positions()
        
    def toggle(self, open_type='keyboard'):
        """切换合成页面的显示状态"""
        self.is_open = not self.is_open
        if self.is_open:
            self.open_type = open_type
    
    def open(self, open_type='keyboard'):
        """直接打开合成页面"""
        self.is_open = True
        self.open_type = open_type
    
    def close(self):
        """直接关闭合成页面"""
        self.is_open = False
        self.open_type = None
    
    def _update_panel_positions(self):
        """更新面板位置（响应窗口大小变化）"""
        # 获取屏幕尺寸
        screen_width, screen_height = self.game.屏幕.get_size()
        
        # 计算面板位置，使其在屏幕上居中
        self.底1_x = (screen_width - self.底1宽度 - self.间隔 - self.底2宽度) // 2
        self.底2_x = self.底1_x + self.底1宽度 + self.间隔
        self.底_y = (screen_height - max(self.底1高度, self.底2高度)) // 2
    
    def 获取背包物品数量(self, 物品_id):
        """获取背包中指定物品ID的总数量"""
        # 检查游戏实例是否有背包管理器
        if hasattr(self.game, '背包管理器'):
            return self.game.背包管理器.获取物品总数量(物品_id)
        return 0
    
    def 检查材料是否充足(self, 物品):
        """检查合成指定物品的材料是否充足"""
        recipe = 物品["recipe"]
        materials_count = {}
        
        # 检查recipe类型，如果是字典格式，直接使用键值对
        if isinstance(recipe, dict):
            # 直接使用字典的键值对作为材料和数量
            materials_count = recipe
        else:
            # 原有逻辑：处理二维列表格式的配方
            for row in recipe:
                for ingredient in row:
                    if ingredient:  # 跳过空材料
                        if ingredient in materials_count:
                            materials_count[ingredient] += 1
                        else:
                            materials_count[ingredient] = 1
        
        # 检查每种材料是否充足
        for 材料名称, 需要数量 in materials_count.items():
            # 获取材料的物品ID
            材料_id = self.物品_id映射.get(材料名称)
            if not 材料_id:
                # 材料不存在于映射表中，无法合成
                return False
            
            # 获取背包中该材料的数量
            背包数量 = self.获取背包物品数量(材料_id)
            
            # 检查数量是否足够
            if 背包数量 < 需要数量:
                return False
        
        return True
        
    def draw(self, screen):
        """绘制合成界面"""
        if not self.is_open:
            return
        
        # 更新面板位置
        self._update_panel_positions()
        
        # 绘制半透明背景遮罩
        screen_width, screen_height = screen.get_size()
        半透明背景 = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        半透明背景.fill((0, 0, 0, 180))
        screen.blit(半透明背景, (0, 0))
        
        # 绘制左侧面板（底1）
        # 绘制阴影
        shadow_rect = pygame.Rect(self.底1_x + 5, self.底_y + 5, self.底1宽度, self.底1高度)
        pygame.draw.rect(screen, 阴影颜色, shadow_rect, border_radius=self.圆角半径)
        
        # 面板背景和边框
        pygame.draw.rect(screen, 主背景色, 
                         (self.底1_x, self.底_y, self.底1宽度, self.底1高度), 
                         border_radius=self.圆角半径)
        pygame.draw.rect(screen, 边框颜色, 
                         (self.底1_x, self.底_y, self.底1宽度, self.底1高度), 
                         2, border_radius=self.圆角半径)
        
        # 绘制右侧面板（底2）
        # 绘制阴影
        shadow_rect = pygame.Rect(self.底2_x + 5, self.底_y + 5, self.底2宽度, self.底2高度)
        pygame.draw.rect(screen, 阴影颜色, shadow_rect, border_radius=self.圆角半径)
        
        # 面板背景和边框
        pygame.draw.rect(screen, 主背景色, 
                         (self.底2_x, self.底_y, self.底2宽度, self.底2高度), 
                         border_radius=self.圆角半径)
        pygame.draw.rect(screen, 边框颜色, 
                         (self.底2_x, self.底_y, self.底2宽度, self.底2高度), 
                         2, border_radius=self.圆角半径)
        
        # 在底2中添加两个子面板
        子面板间隔 = 10
        
        底2_1宽度 = 520  # 左侧子面板宽度
        底2_2宽度 = 300  # 右侧子面板宽度
        子面板高度 = 660  # 子面板高度
        
        # 计算子面板位置
        底2_1_x = self.底2_x + 10
        底2_2_x = 底2_1_x + 底2_1宽度 + 子面板间隔
        子面板_y = self.底_y + 20
        
        # 绘制2-1底（左侧子面板）
        pygame.draw.rect(screen, 阴影颜色, 
                         (底2_1_x + 3, 子面板_y + 3, 底2_1宽度, 子面板高度), 
                         border_radius=5)
        pygame.draw.rect(screen, 次级背景色, 
                         (底2_1_x, 子面板_y, 底2_1宽度, 子面板高度), 
                         border_radius=5)
        pygame.draw.rect(screen, 边框颜色, 
                         (底2_1_x, 子面板_y, 底2_1宽度, 子面板高度), 
                         1, border_radius=5)
        
        # 在2-1面板中绘制可合成物品列表
        # 获取当前分类的物品列表
        current_items = self.craftable_items[self.current_category]
        
        # 根据打开方式过滤物品
        if self.open_type == 'keyboard':  # 通过C键打开，只显示基础物品
            # 只显示的物品图标列表，排除箱子（只能通过工作台合成）
            allowed_icons = ['火把', '工作台', '木斧', '木镐', '木铲', '石斧', '石镐', '石铲', '木板']
            # 过滤物品列表
            current_items = [item for item in current_items if item['icon'] in allowed_icons]
        
        # 对物品进行排序：材料充足的在前，不足的在后
        sorted_items = sorted(current_items, key=lambda x: 0 if self.检查材料是否充足(x) else 1)
        
        # 绘制分类标题
        category_title = self.标题字体.render(f"{self.current_category}物品", True, 标题颜色)
        category_title_rect = category_title.get_rect(x=底2_1_x + 10, y=子面板_y + 10)
        screen.blit(category_title, category_title_rect)
        
        # 计算物品网格的起始位置
        item_start_y = category_title_rect.bottom + 10
        item_start_x = 底2_1_x + 10
        
        # 遍历并绘制可合成物品
        for index, item in enumerate(sorted_items):
            # 计算物品在网格中的位置
            row = index // self.item_grid_size
            col = index % self.item_grid_size
            
            item_x = item_start_x + col * (self.item_slot_size + self.item_slot_margin)
            item_y = item_start_y + row * (self.item_slot_size + self.item_slot_margin)
            
            # 检查物品位置是否超出面板范围
            if item_y + self.item_slot_size > 子面板_y + 子面板高度:
                break  # 超出范围，停止绘制
            
            # 绘制物品格子
            item_rect = pygame.Rect(item_x, item_y, self.item_slot_size, self.item_slot_size)
            
            # 检查鼠标是否悬停在物品上
            mouse_pos = pygame.mouse.get_pos()
            is_hovered = item_rect.collidepoint(mouse_pos)
            
            # 绘制格子背景
            if is_hovered:
                pygame.draw.rect(screen, 悬停格子背景, item_rect)
            else:
                pygame.draw.rect(screen, 普通格子背景, item_rect)
            
            # 绘制格子边框
            pygame.draw.rect(screen, 边框颜色, item_rect, 2)
            
            # 获取物品ID
            item_id = self.物品_id映射.get(item["icon"])
            
            # 检查材料是否充足
            is_material_sufficient = self.检查材料是否充足(item)
            
            # 绘制物品图标
            item_icon = 图片管理器.获取物品图片(item_id)
            if item_icon:
                # 缩放图标到底框的90%大小
                icon_size = int(self.item_slot_size * 0.8)  # 90%大小
                scaled_icon = pygame.transform.scale(item_icon, (icon_size, icon_size))
                
                # 如果材料不足，将图标转换为灰色
                if not is_material_sufficient:
                    # 将彩色图标转换为灰度图
                    scaled_icon = scaled_icon.convert()
                    # 获取图标像素数据
                    pixels = pygame.PixelArray(scaled_icon)
                    for x in range(scaled_icon.get_width()):
                        for y in range(scaled_icon.get_height()):
                            # 获取RGB值
                            color = scaled_icon.unmap_rgb(pixels[x][y])
                            # 计算灰度值
                            gray = int(0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2])
                            # 设置为灰度
                            pixels[x][y] = scaled_icon.map_rgb((gray, gray, gray))
                    del pixels  # 释放PixelArray资源
                
                icon_rect = scaled_icon.get_rect(center=item_rect.center)
                screen.blit(scaled_icon, icon_rect)
                
                # 获取物品的合成数量，如果没有定义则默认为1
                craft_quantity = item.get("quantity", 1)
                # 当合成数量为1时不显示文字
                if craft_quantity != 1:
                    # 创建加粗字体
                    try:
                        bold_font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial Unicode MS", "SimSun"], 16, True)
                    except:
                        bold_font = pygame.font.SysFont(None, 16, True)
                    
                    # 根据材料是否充足设置文字颜色
                    if is_material_sufficient:
                        # 材料充足，使用正常的外黑里白效果
                        count_text = bold_font.render(str(craft_quantity), True, (0, 0, 0))  # 黑色描边
                        # 计算位置：物品格子右下角，距离边缘5像素
                        count_x = item_x + self.item_slot_size - count_text.get_width() - 5
                        count_y = item_y + self.item_slot_size - count_text.get_height() - 5
                        # 绘制黑色描边（偏移1像素）
                        screen.blit(count_text, (count_x - 1, count_y - 1))
                        screen.blit(count_text, (count_x + 1, count_y - 1))
                        screen.blit(count_text, (count_x - 1, count_y + 1))
                        screen.blit(count_text, (count_x + 1, count_y + 1))
                        # 绘制白色填充
                        count_text = bold_font.render(str(craft_quantity), True, (255, 255, 255))
                        screen.blit(count_text, (count_x, count_y))
                    else:
                        # 材料不足，使用灰色文字，无描边
                        count_text = bold_font.render(str(craft_quantity), True, (128, 128, 128))  # 灰色
                        # 计算位置：物品格子右下角，距离边缘5像素
                        count_x = item_x + self.item_slot_size - count_text.get_width() - 5
                        count_y = item_y + self.item_slot_size - count_text.get_height() - 5
                        screen.blit(count_text, (count_x, count_y))
            else:
                # 如果图标不存在，显示物品名称作为替代
                item_info = 物品.get(item_id, {})
                item_name = item_info.get("名称", item["icon"])
                
                # 根据材料是否充足设置文字颜色
                text_color = 文本颜色 if is_material_sufficient else (128, 128, 128)  # 灰色
                
                item_text = self.文本字体.render(item_name, True, text_color)
                item_text_rect = item_text.get_rect(center=item_rect.center)
                screen.blit(item_text, item_text_rect)
                
                # 如果是火把，在文字右下方绘制数字4
                if item["icon"] == "火把":
                    count_text = self.文本字体.render("4", True, text_color)
                    count_x = item_x + self.item_slot_size - count_text.get_width() - 4
                    count_y = item_y + self.item_slot_size - count_text.get_height() - 1
                    screen.blit(count_text, (count_x, count_y))
                # 如果是木板，根据配方绘制不同的数字
                elif item["icon"] == "木板":
                    # 获取当前物品在列表中的索引
                    item_index = sorted_items.index(item)
                    # 根据配方不同绘制不同的数字
                    if item_index == 22:  # 配方1：1个木头合成4个木板
                        count_text = self.文本字体.render("3", True, text_color)
                    elif item_index == 23:  # 配方2：2个木头合成8个木板
                        count_text = self.文本字体.render("4", True, text_color)
                    else:
                        count_text = None
                    
                    # 如果需要绘制数字，计算位置并绘制
                    if count_text:
                        count_x = item_x + self.item_slot_size - count_text.get_width() - 4
                        count_y = item_y + self.item_slot_size - count_text.get_height() - 1
                        screen.blit(count_text, (count_x, count_y))
            
            # 移除在格子下面绘制文字的代码
        
        # 绘制2-2底（右侧子面板）
        pygame.draw.rect(screen, 阴影颜色, 
                         (底2_2_x + 3, 子面板_y + 3, 底2_2宽度, 子面板高度), 
                         border_radius=5)
        pygame.draw.rect(screen, 次级背景色, 
                         (底2_2_x, 子面板_y, 底2_2宽度, 子面板高度), 
                         border_radius=5)
        pygame.draw.rect(screen, 边框颜色, 
                         (底2_2_x, 子面板_y, 底2_2宽度, 子面板高度), 
                         1, border_radius=5)
        
        # 绘制提示文字（在所有UI元素之后绘制，确保显示在最上层）
        for notification in self.notifications:
            # 创建文字表面
            text_surface = self.提示字体.render(notification["text"], True, (255, 255, 255))
            # 设置透明度
            text_surface.set_alpha(notification["alpha"])
            # 计算文字居中位置
            text_rect = text_surface.get_rect(center=(notification["x"], notification["y"]))
            # 绘制文字
            screen.blit(text_surface, text_rect)
        
        # 如果有选中的物品，显示物品详情
        if self.selected_item:
            # 获取物品ID
            item_id = self.物品_id映射.get(self.selected_item["icon"])
            item_info = 物品.get(item_id, {})
            
            # 获取物品名称和描述
            item_name = item_info.get("名称", self.selected_item["icon"])
            item_description = item_info.get("说明", "暂无说明")
            
            # 显示物品名称
            item_name_text = self.标题字体.render(item_name, True, 标题颜色)
            item_name_rect = item_name_text.get_rect(centerx=底2_2_x + 底2_2宽度 // 2, y=子面板_y + 25)
            screen.blit(item_name_text, item_name_rect)
            
            # 显示物品图标
            合成物品_底ui = 70
            square_x = 底2_2_x + (底2_2宽度 - 合成物品_底ui) // 2
            square_y = item_name_rect.bottom + 25
            
            pygame.draw.rect(screen, 普通格子背景, (square_x, square_y, 合成物品_底ui, 合成物品_底ui))
            pygame.draw.rect(screen, 边框颜色, (square_x, square_y, 合成物品_底ui, 合成物品_底ui), 2)
            
            # 获取物品ID
            item_id = self.物品_id映射.get(self.selected_item["icon"])
            
            # 绘制物品图标
            item_icon = 图片管理器.获取物品图片(item_id)
            if item_icon:
                # 缩放图标到底框的80%大小
                icon_size = int(合成物品_底ui * 0.8)  # 80%大小
                scaled_icon = pygame.transform.scale(item_icon, (icon_size, icon_size))
                icon_rect = scaled_icon.get_rect(center=(square_x + 合成物品_底ui // 2, square_y + 合成物品_底ui // 2))
                screen.blit(scaled_icon, icon_rect)
                
                # 获取物品的合成数量，如果没有定义则默认为1
                craft_quantity = self.selected_item.get("quantity", 1)
                # 当合成数量为1时不显示文字
                if craft_quantity != 1:
                    # 创建加粗字体
                    try:
                        bold_font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial Unicode MS", "SimSun"], 16, True)
                    except:
                        bold_font = pygame.font.SysFont(None, 16, True)
                    # 在图标右下方绘制合成数量，外黑里白效果
                    count_text = bold_font.render(str(craft_quantity), True, (0, 0, 0))  # 黑色描边
                    # 计算位置：图标右下方，距离边缘5像素
                    count_x = square_x + 合成物品_底ui - count_text.get_width() - 5
                    count_y = square_y + 合成物品_底ui - count_text.get_height() - 5
                    # 绘制黑色描边（偏移1像素）
                    screen.blit(count_text, (count_x - 1, count_y - 1))
                    screen.blit(count_text, (count_x + 1, count_y - 1))
                    screen.blit(count_text, (count_x - 1, count_y + 1))
                    screen.blit(count_text, (count_x + 1, count_y + 1))
                    # 绘制白色填充
                    count_text = bold_font.render(str(craft_quantity), True, (255, 255, 255))
                    screen.blit(count_text, (count_x, count_y))
            else:
                # 如果图标不存在，显示物品名称作为替代
                item_icon_text = self.文本字体.render(item_name, True, 文本颜色)
                item_icon_rect = item_icon_text.get_rect(center=(square_x + 合成物品_底ui // 2, square_y + 合成物品_底ui // 2))
                screen.blit(item_icon_text, item_icon_rect)
                
                # 如果是火把，在文字右下方绘制数字4
                if self.selected_item["icon"] == "火把":
                    count_text = self.文本字体.render("4", True, 文本颜色)
                    count_x = square_x + 合成物品_底ui - count_text.get_width() - 5
                    count_y = square_y + 合成物品_底ui - count_text.get_height() - 5
                    screen.blit(count_text, (count_x, count_y))
                # 如果是木板，根据配方绘制不同的数字
                elif self.selected_item["icon"] == "木板":
                    # 获取当前分类下的物品列表
                    current_items = self.craftable_items[self.current_category]
                    # 找到当前选中的物品在列表中的索引
                    item_index = current_items.index(self.selected_item)
                    # 根据配方不同绘制不同的数字
                    if item_index == 22:  # 配方1：1个木头合成4个木板
                        count_text = self.文本字体.render("3", True, 文本颜色)
                    elif item_index == 23:  # 配方2：2个木头合成8个木板
                        count_text = self.文本字体.render("4", True, 文本颜色)
                    else:
                        count_text = None
                    
                    # 如果需要绘制数字，计算位置并绘制
                    if count_text:
                        count_x = square_x + 合成物品_底ui - count_text.get_width() - 5
                        count_y = square_y + 合成物品_底ui - count_text.get_height() - 5
                        screen.blit(count_text, (count_x, count_y))
            
            # 显示物品介绍
            物品介绍文字 = "物品介绍"
            介绍文字_surface = self.文本字体.render(物品介绍文字, True, 文本颜色)
            介绍文字_rect = 介绍文字_surface.get_rect(centerx=底2_2_x + 底2_2宽度 // 2, y=square_y + 合成物品_底ui + 25)
            screen.blit(介绍文字_surface, 介绍文字_rect)
            
            # 绘制介绍底框
            介绍底高度 = 100
            介绍底_y = 介绍文字_rect.bottom + 10
            介绍底_x = 底2_2_x + 20
            介绍底宽度 = 底2_2宽度 - 40
            
            pygame.draw.rect(screen, 次级背景色, (介绍底_x, 介绍底_y, 介绍底宽度, 介绍底高度))
            pygame.draw.rect(screen, 边框颜色, (介绍底_x, 介绍底_y, 介绍底宽度, 介绍底高度), 2)
            
            # 绘制物品描述 - 每20字自动换行
            description_lines = []
            # 将描述文字按每20字分割成多行
            full_text = item_description
            line_length = 15
            for i in range(0, len(full_text), line_length):
                description_lines.append(full_text[i:i+line_length])
            
            for i, line in enumerate(description_lines):
                line_surface = self.文本字体.render(line, True, 文本颜色)
                line_rect = line_surface.get_rect(x=介绍底_x + 10, y=介绍底_y + 10 + i * 20)
                screen.blit(line_surface, line_rect)
            
            # 显示合成材料
            合成材料文字 = self.文本字体.render("合成材料", True, 文本颜色)
            合成材料文字_y = 介绍底_y + 介绍底高度 + 10
            合成材料文字_x = 介绍底_x + (介绍底宽度 // 2) - (合成材料文字.get_width() // 2)
            screen.blit(合成材料文字, (合成材料文字_x, 合成材料文字_y))
            
            # 绘制合成材料底框
            合成材料底高度 = 150
            合成材料底_y = 合成材料文字_y + 合成材料文字.get_height() + 10
            合成材料底_x = 介绍底_x
            合成材料底宽度 = 介绍底宽度
            
            pygame.draw.rect(screen, 次级背景色, (合成材料底_x, 合成材料底_y, 合成材料底宽度, 合成材料底高度))
            pygame.draw.rect(screen, 边框颜色, (合成材料底_x, 合成材料底_y, 合成材料底宽度, 合成材料底高度), 2)
            
            # 绘制合成配方（中心左右物品+数量显示）
            recipe = self.selected_item["recipe"]
            slot_size = 40
            slot_margin = 8
            
            # 合并重复的材料，计算每个材料的数量
            materials_count = {}
            
            # 检查recipe类型，如果是字典格式，直接使用键值对
            if isinstance(recipe, dict):
                # 直接使用字典的键值对作为材料和数量
                materials_count = recipe
            else:
                # 原有逻辑：处理二维列表格式的配方
                for row in recipe:
                    for ingredient in row:
                        if ingredient:  # 跳过空材料
                            if ingredient in materials_count:
                                materials_count[ingredient] += 1
                            else:
                                materials_count[ingredient] = 1
            
            # 转换为列表格式，用于绘制
            merged_materials = list(materials_count.items())
            
            # 计算起始位置，居中显示
            total_width = len(merged_materials) * (slot_size + slot_margin) - slot_margin
            recipe_start_x = 合成材料底_x + (合成材料底宽度 - total_width) // 2
            recipe_start_y = 合成材料底_y + 55
            
            # 绘制每个合并后的材料
            for idx, (ingredient, count) in enumerate(merged_materials):
                slot_x = recipe_start_x + idx * (slot_size + slot_margin)
                slot_y = recipe_start_y
                
                # 绘制材料格子
                pygame.draw.rect(screen, 普通格子背景, (slot_x, slot_y, slot_size, slot_size))
                pygame.draw.rect(screen, 边框颜色, (slot_x, slot_y, slot_size, slot_size), 1)
                
                # 绘制材料图标或名称
                if ingredient:
                    # 尝试加载材料图标
                    ingredient_icon = 图片管理器.获取物品图片(ingredient)
                    if ingredient_icon:
                        # 缩放图标到底框的90%大小
                        icon_size = int(slot_size * 0.9)  # 90%大小
                        scaled_ingredient_icon = pygame.transform.scale(ingredient_icon, (icon_size, icon_size))
                        ingredient_icon_rect = scaled_ingredient_icon.get_rect(center=(slot_x + slot_size // 2, slot_y + slot_size // 2))
                        screen.blit(scaled_ingredient_icon, ingredient_icon_rect)
                    else:
                        # 如果图标不存在，显示材料名称
                        ingredient_text = self.文本字体.render(ingredient, True, 文本颜色)
                        ingredient_rect = ingredient_text.get_rect(center=(slot_x + slot_size // 2, slot_y + slot_size // 2))
                        screen.blit(ingredient_text, ingredient_rect)
                    
                    # 绘制材料数量，外黑里白效果
                    # 创建加粗字体
                    try:
                        bold_font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial Unicode MS", "SimSun"], 16, True)
                    except:
                        bold_font = pygame.font.SysFont(None, 16, True)
                    # 黑色描边
                    amount_text = bold_font.render(str(count), True, (0, 0, 0))
                    amount_rect = amount_text.get_rect(bottomright=(slot_x + slot_size - 2, slot_y + slot_size - 2))
                    # 绘制黑色描边（偏移1像素）
                    screen.blit(amount_text, (amount_rect.x - 1, amount_rect.y - 1))
                    screen.blit(amount_text, (amount_rect.x + 1, amount_rect.y - 1))
                    screen.blit(amount_text, (amount_rect.x - 1, amount_rect.y + 1))
                    screen.blit(amount_text, (amount_rect.x + 1, amount_rect.y + 1))
                    # 白色填充
                    amount_text = bold_font.render(str(count), True, (255, 255, 255))
                    screen.blit(amount_text, amount_rect)
        else:
            # 没有选中物品时显示提示
            original_font_size = 16
            larger_font_size = int(original_font_size * 1.5)
            try:
                larger_font = pygame.font.SysFont(["Microsoft YaHei", "SimHei", "Arial Unicode MS", "SimSun"], larger_font_size)
            except:
                larger_font = pygame.font.SysFont(None, larger_font_size)
            
            hint_text = larger_font.render("请点击合成道具", True, 文本颜色)
            hint_text_rect = hint_text.get_rect(centerx=底2_2_x + 底2_2宽度 // 2, y=子面板_y + 25)
            screen.blit(hint_text, hint_text_rect)
            
            # 添加合成物品底UI
            合成物品_底ui = 70
            square_x = 底2_2_x + (底2_2宽度 - 合成物品_底ui) // 2
            square_y = hint_text_rect.bottom + 25
            
            pygame.draw.rect(screen, 普通格子背景, (square_x, square_y, 合成物品_底ui, 合成物品_底ui))
            pygame.draw.rect(screen, 边框颜色, (square_x, square_y, 合成物品_底ui, 合成物品_底ui), 2)
            
            # 显示默认介绍
            物品介绍文字 = "物品介绍"
            介绍文字_surface = self.文本字体.render(物品介绍文字, True, 文本颜色)
            介绍文字_rect = 介绍文字_surface.get_rect(centerx=底2_2_x + 底2_2宽度 // 2, y=square_y + 合成物品_底ui + 25)
            screen.blit(介绍文字_surface, 介绍文字_rect)
            
            # 绘制默认介绍底框
            介绍底高度 = 100
            介绍底_y = 介绍文字_rect.bottom + 10
            介绍底_x = 底2_2_x + 20
            介绍底宽度 = 底2_2宽度 - 40
            
            pygame.draw.rect(screen, 次级背景色, (介绍底_x, 介绍底_y, 介绍底宽度, 介绍底高度))
            pygame.draw.rect(screen, 边框颜色, (介绍底_x, 介绍底_y, 介绍底宽度, 介绍底高度), 2)
            
            # 显示默认合成材料提示
            合成材料文字 = self.文本字体.render("合成材料", True, 文本颜色)
            合成材料文字_y = 介绍底_y + 介绍底高度 + 10
            合成材料文字_x = 介绍底_x + (介绍底宽度 // 2) - (合成材料文字.get_width() // 2)
            screen.blit(合成材料文字, (合成材料文字_x, 合成材料文字_y))
            
            # 绘制默认合成材料底框
            合成材料底高度 = 150
            合成材料底_y = 合成材料文字_y + 合成材料文字.get_height() + 10
            合成材料底_x = 介绍底_x
            合成材料底宽度 = 介绍底宽度
            
            pygame.draw.rect(screen, 次级背景色, (合成材料底_x, 合成材料底_y, 合成材料底宽度, 合成材料底高度))
            pygame.draw.rect(screen, 边框颜色, (合成材料底_x, 合成材料底_y, 合成材料底宽度, 合成材料底高度), 2)
        
        # 绘制数量控制区域（在合成材料底框下方）
        control_area_y = 合成材料底_y + 合成材料底高度 + 15  # 间距15像素
        
        # 计算第一行控件的总宽度和居中位置
        total_control_width = (self.control_button_width * 4) + self.input_width + (self.button_spacing * 4)
        start_x = 底2_2_x + (底2_2宽度 - total_control_width) // 2
        
        # 第一行：最小按钮
        min_button_rect = pygame.Rect(start_x, control_area_y, self.control_button_width, self.control_button_height)
        min_button_color = self.control_button_hover if self.hovered_control_button == "最小" else self.control_button_normal
        pygame.draw.rect(screen, min_button_color, min_button_rect, border_radius=3)
        pygame.draw.rect(screen, 边框颜色, min_button_rect, 1, border_radius=3)
        min_text = self.文本字体.render("最小", True, self.control_button_text)
        min_text_rect = min_text.get_rect(center=min_button_rect.center)
        screen.blit(min_text, min_text_rect)
        
        # 第一行：-1按钮
        minus_button_rect = pygame.Rect(start_x + self.control_button_width + self.button_spacing, control_area_y, self.control_button_width, self.control_button_height)
        minus_button_color = self.control_button_hover if self.hovered_control_button == "-1" else self.control_button_normal
        pygame.draw.rect(screen, minus_button_color, minus_button_rect, border_radius=3)
        pygame.draw.rect(screen, 边框颜色, minus_button_rect, 1, border_radius=3)
        minus_text = self.文本字体.render("-1", True, self.control_button_text)
        minus_text_rect = minus_text.get_rect(center=minus_button_rect.center)
        screen.blit(minus_text, minus_text_rect)
        
        # 第一行：输入框
        input_rect = pygame.Rect(start_x + (self.control_button_width * 2) + (self.button_spacing * 2), control_area_y, self.input_width, self.input_height)
        
        # 检查鼠标是否悬停在输入框上
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_input_box = input_rect.collidepoint(mouse_pos)
        
        # 根据状态设置输入框样式
        if self.is_input_active:
            # 激活状态
            input_bg_color = self.input_active_bg_color
            input_border_color = self.input_active_border_color
        elif self.hovered_input_box:
            # 悬停状态
            input_bg_color = self.input_bg_color
            input_border_color = self.input_active_border_color
        else:
            # 普通状态
            input_bg_color = self.input_bg_color
            input_border_color = self.input_border_color
        
        # 绘制输入框背景和边框
        pygame.draw.rect(screen, input_bg_color, input_rect)
        pygame.draw.rect(screen, input_border_color, input_rect, 1)
        
        # 绘制输入框文本
        input_text = self.文本字体.render(self.input_text, True, 文本颜色)
        text_rect = input_text.get_rect(center=input_rect.center)
        screen.blit(input_text, text_rect)
        
        # 绘制光标（仅在激活状态下）
        if self.is_input_active and self.cursor_visible:
            cursor_x = text_rect.x + input_text.get_width() + 2
            cursor_y = text_rect.y + 2
            cursor_height = input_text.get_height() - 4
            pygame.draw.line(screen, 文本颜色, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)
        
        # 第一行：+1按钮
        plus_button_rect = pygame.Rect(start_x + (self.control_button_width * 2) + self.input_width + (self.button_spacing * 3), control_area_y, self.control_button_width, self.control_button_height)
        plus_button_color = self.control_button_hover if self.hovered_control_button == "+1" else self.control_button_normal
        pygame.draw.rect(screen, plus_button_color, plus_button_rect, border_radius=3)
        pygame.draw.rect(screen, 边框颜色, plus_button_rect, 1, border_radius=3)
        plus_text = self.文本字体.render("+1", True, self.control_button_text)
        plus_text_rect = plus_text.get_rect(center=plus_button_rect.center)
        screen.blit(plus_text, plus_text_rect)
        
        # 第一行：最大按钮
        max_button_rect = pygame.Rect(start_x + (self.control_button_width * 3) + self.input_width + (self.button_spacing * 4), control_area_y, self.control_button_width, self.control_button_height)
        max_button_color = self.control_button_hover if self.hovered_control_button == "最大" else self.control_button_normal
        pygame.draw.rect(screen, max_button_color, max_button_rect, border_radius=3)
        pygame.draw.rect(screen, 边框颜色, max_button_rect, 1, border_radius=3)
        max_text = self.文本字体.render("最大", True, self.control_button_text)
        max_text_rect = max_text.get_rect(center=max_button_rect.center)
        screen.blit(max_text, max_text_rect)
        
        # 第二行：确定合成按钮
        confirm_y = control_area_y + self.control_button_height + 10  # 间距10像素
        confirm_x = 底2_2_x + (底2_2宽度 - self.confirm_button_width) // 2
        confirm_rect = pygame.Rect(confirm_x, confirm_y, self.confirm_button_width, self.confirm_button_height)
        
        # 检查当前选中的物品是否存在以及材料是否充足
        if self.selected_item and self.检查材料是否充足(self.selected_item):
            # 材料充足，按钮显示绿色和"确定合成"
            confirm_color = self.confirm_button_hover if self.hovered_confirm_button else self.confirm_button_normal
            confirm_text_content = "确定合成"
        else:
            # 材料不足或没有选中物品，按钮显示红色和"X材料不足X"
            if self.hovered_confirm_button:
                confirm_color = (255, 60, 60)  # 亮红色（悬停）
            else:
                confirm_color = (255, 0, 0)  # 红色
            confirm_text_content = "X材料不足X"
        
        pygame.draw.rect(screen, confirm_color, confirm_rect, border_radius=5)
        pygame.draw.rect(screen, 边框颜色, confirm_rect, 1, border_radius=5)
        confirm_text = self.文本字体.render(confirm_text_content, True, self.confirm_button_text)
        confirm_text_rect = confirm_text.get_rect(center=confirm_rect.center)
        screen.blit(confirm_text, confirm_text_rect)
        

        
        # 在左侧面板添加标题
        title_text = self.标题字体.render("合成类型", True, 标题颜色)
        title_rect = title_text.get_rect(centerx=self.底1_x + self.底1宽度 // 2, y=self.底_y + 20)
        screen.blit(title_text, title_rect)
        
        # 绘制分类按钮
        button_y = title_rect.bottom + self.button_margin
        button_width = self.底1宽度 - 40
        button_x = self.底1_x + 20
        
        for category in self.crafting_categories:
            if category == self.current_category:
                button_color = self.selected_button_color
            elif hasattr(self, 'hovered_button') and self.hovered_button == category:
                button_color = self.hovered_button_color
            else:
                button_color = self.normal_button_color
            
            button_rect = pygame.Rect(button_x, button_y, button_width, self.button_height)
            pygame.draw.rect(screen, button_color, button_rect, border_radius=5)
            pygame.draw.rect(screen, 边框颜色, button_rect, 1, border_radius=5)
            
            button_text = self.文本字体.render(category, True, self.button_text_color)
            text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, text_rect)
            
            button_y += self.button_height + self.button_margin
        
        # 绘制底部退出按钮
        exit_button_y = self.底_y + self.底1高度 - 60
        exit_button_rect = pygame.Rect(button_x, exit_button_y, button_width, self.button_height)
        
        if hasattr(self, 'hovered_exit_button') and self.hovered_exit_button:
            exit_button_color = self.exit_button_hover_color
        else:
            exit_button_color = self.exit_button_normal_color
        
        pygame.draw.rect(screen, exit_button_color, exit_button_rect, border_radius=5)
        pygame.draw.rect(screen, 边框颜色, exit_button_rect, 1, border_radius=5)
        
        exit_text = self.文本字体.render("退出页面", True, self.exit_button_text_color)
        exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
        screen.blit(exit_text, exit_text_rect)
    
    def handle_keyboard(self, event):
        """处理键盘事件"""
        if not self.is_open:
            return False
        
        # ESC键关闭合成页面
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.is_input_active:
                    # 如果输入框激活，先关闭输入框
                    self.is_input_active = False
                    # 尝试解析输入值
                    try:
                        new_amount = int(self.input_text)
                        # 确保数量在有效范围内
                        self.craft_amount = max(self.min_amount, min(self.max_amount, new_amount))
                        self.input_text = str(self.craft_amount)  # 更新输入框文本为有效数量
                        print(f"合成数量设置为: {self.craft_amount}")
                    except ValueError:
                        # 输入无效，恢复原有数量
                        self.input_text = str(self.craft_amount)
                    return True
                else:
                    # 否则关闭合成页面
                    self.close()
                    # 同时更新游戏主类的页面管理器状态，确保状态同步
                    if hasattr(self.game, 'page_manager'):
                        self.game.page_manager.page_states['c'] = False
                    return True
            
            # 输入框激活时处理键盘输入
            if self.is_input_active:
                # 退格键删除字符
                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                # 回车键确认输入
                elif event.key == pygame.K_RETURN:
                    # 尝试解析输入值
                    try:
                        new_amount = int(self.input_text)
                        # 确保数量在有效范围内
                        self.craft_amount = max(self.min_amount, min(self.max_amount, new_amount))
                        self.input_text = str(self.craft_amount)  # 更新输入框文本为有效数量
                        print(f"合成数量设置为: {self.craft_amount}")
                    except ValueError:
                        # 输入无效，恢复原有数量
                        self.input_text = str(self.craft_amount)
                    # 关闭输入框
                    self.is_input_active = False
                # 数字键输入
                elif event.unicode.isdigit():
                    # 限制输入长度
                    if len(self.input_text) < 3:
                        self.input_text += event.unicode
                return True
        
        return False
    
    def _update_hovered_slot(self):
        """更新当前悬停的格子"""
        if not self.is_open:
            self.hovered_slot = None
            self.hovered_button = None
            return
        
        self._update_panel_positions()
        
        mouse_pos = pygame.mouse.get_pos()
        mx, my = mouse_pos
        
        if not (self.底1_x <= mx <= self.底2_x + self.底2宽度 and 
                self.底_y <= my <= self.底_y + max(self.底1高度, self.底2高度)):
            self.hovered_slot = None
            self.hovered_button = None
            return
        
        # 检查分类按钮悬停
        self.hovered_button = None
        button_y = self.底_y + 20 + self.标题字体.get_height() + self.button_margin
        button_width = self.底1宽度 - 40
        button_x = self.底1_x + 20
        
        for category in self.crafting_categories:
            button_rect = pygame.Rect(button_x, button_y, button_width, self.button_height)
            if button_rect.collidepoint(mx, my):
                self.hovered_button = category
                self.hovered_slot = None
                self.hovered_exit_button = False
                return
            button_y += self.button_height + self.button_margin
        
        # 检查退出按钮悬停
        exit_button_y = self.底_y + self.底1高度 - 60
        exit_button_rect = pygame.Rect(button_x, exit_button_y, button_width, self.button_height)
        if exit_button_rect.collidepoint(mx, my):
            self.hovered_exit_button = True
            self.hovered_slot = None
            self.hovered_button = None
            self.hovered_control_button = None
            self.hovered_confirm_button = False
            return
        else:
            self.hovered_exit_button = False
        
        # 检查数量控制按钮悬停
        self.hovered_control_button = None
        self.hovered_confirm_button = False
        
        # 重新计算子面板位置（与draw方法完全相同）
        底2_1_x = self.底2_x + 10
        底2_2_x = 底2_1_x + 520 + 10
        底2_2宽度 = 300
        子面板_y = self.底_y + 20
        
        # 计算数量控制区域的位置（与draw方法完全相同的计算方式）
        # 首先计算合成材料底框的位置
        介绍底_x = 底2_2_x + 20
        介绍底_y = 子面板_y + 25 + 70 + 25 + 100 + 10
        合成材料文字_y = 介绍底_y + 100 + 10
        合成材料底_y = 合成材料文字_y + 16 + 10
        合成材料底高度 = 150
        
        # 计算数量控制区域位置
        control_area_y = 合成材料底_y + 合成材料底高度 + 15  # 间距15像素
        total_control_width = (self.control_button_width * 4) + self.input_width + (self.button_spacing * 4)
        start_x = 底2_2_x + (底2_2宽度 - total_control_width) // 2
        
        # 检查第一行按钮悬停
        # 最小按钮
        min_button_rect = pygame.Rect(start_x, control_area_y, self.control_button_width, self.control_button_height)
        if min_button_rect.collidepoint(mx, my):
            self.hovered_control_button = "最小"
            self.hovered_slot = None
            self.hovered_button = None
            return
        
        # -1按钮
        minus_button_rect = pygame.Rect(start_x + self.control_button_width + self.button_spacing, control_area_y, self.control_button_width, self.control_button_height)
        if minus_button_rect.collidepoint(mx, my):
            self.hovered_control_button = "-1"
            self.hovered_slot = None
            self.hovered_button = None
            return
        
        # +1按钮
        plus_button_rect = pygame.Rect(start_x + (self.control_button_width * 2) + self.input_width + (self.button_spacing * 3), control_area_y, self.control_button_width, self.control_button_height)
        if plus_button_rect.collidepoint(mx, my):
            self.hovered_control_button = "+1"
            self.hovered_slot = None
            self.hovered_button = None
            return
        
        # 最大按钮
        max_button_rect = pygame.Rect(start_x + (self.control_button_width * 3) + self.input_width + (self.button_spacing * 4), control_area_y, self.control_button_width, self.control_button_height)
        if max_button_rect.collidepoint(mx, my):
            self.hovered_control_button = "最大"
            self.hovered_slot = None
            self.hovered_button = None
            return
        
        # 检查确定合成按钮悬停
        confirm_y = control_area_y + self.control_button_height + 10
        confirm_x = self.底2_x + 10 + 520 + 10 + (300 - self.confirm_button_width) // 2
        confirm_rect = pygame.Rect(confirm_x, confirm_y, self.confirm_button_width, self.confirm_button_height)
        if confirm_rect.collidepoint(mx, my):
            self.hovered_confirm_button = True
            self.hovered_slot = None
            self.hovered_button = None
            self.hovered_control_button = None
            return
        
        self.hovered_slot = None
    
    def update(self, delta_time):
        """更新合成系统状态"""
        if not self.is_open:
            return
        
        # 更新提示文字
        updated_notifications = []
        for notification in self.notifications:
            # 计算经过的时间
            current_time = pygame.time.get_ticks() / 1000.0
            elapsed = current_time - notification["start_time"]
            
            # 如果超出显示时间，跳过此提示
            if elapsed > 3.0:  # 显示3秒后消失
                continue
            
            # 更新位置（向上移动）
            notification["y"] -= notification["speed"] * delta_time
            
            # 更新透明度（淡出效果）
            if elapsed > 2.0:  # 2秒后开始淡出
                fade_elapsed = elapsed - 2.0
                fade_duration = 1.0
                fade_ratio = fade_elapsed / fade_duration
                notification["alpha"] = int(255 * (1 - fade_ratio))
            
            # 添加到更新后的列表
            updated_notifications.append(notification)
        
        # 更新提示列表
        self.notifications = updated_notifications
        
        # 调用原始的update逻辑
        self._update_hovered_slot()
        
        # 更新光标闪烁
        if self.is_input_active:
            self.cursor_blink_time += delta_time
            if self.cursor_blink_time >= self.cursor_blink_interval:
                self.cursor_visible = not self.cursor_visible
                self.cursor_blink_time = 0
        else:
            self.cursor_visible = True
            self.cursor_blink_time = 0
    
    def handle_click(self, mx, my, button=1):
        """处理鼠标点击事件"""
        if not self.is_open:
            return False
        
        self._update_panel_positions()
        
        # 检查分类按钮点击
        button_y = self.底_y + 20 + self.标题字体.get_height() + self.button_margin
        button_width = self.底1宽度 - 40
        button_x = self.底1_x + 20
        
        for category in self.crafting_categories:
            button_rect = pygame.Rect(button_x, button_y, button_width, self.button_height)
            if button_rect.collidepoint(mx, my):
                self.current_category = category
                print(f"选择了分类：{category}")
                return True
            button_y += self.button_height + self.button_margin
        
        # 检查退出按钮点击
        exit_button_y = self.底_y + self.底1高度 - 60
        exit_button_rect = pygame.Rect(button_x, exit_button_y, button_width, self.button_height)
        if exit_button_rect.collidepoint(mx, my):
            print("按下了退出按钮")
            self.close()
            return True
        
        # 检查可合成物品点击
        # 计算物品网格的起始位置
        底2_1_x = self.底2_x + 10
        底2_2_x = 底2_1_x + 520 + 10
        底2_2宽度 = 300
        子面板_y = self.底_y + 20
        
        # 计算分类标题位置
        category_title = self.标题字体.render(f"{self.current_category}物品", True, 标题颜色)
        category_title_rect = category_title.get_rect(x=底2_1_x + 10, y=子面板_y + 10)
        
        # 计算物品网格的起始位置
        item_start_y = category_title_rect.bottom + 10
        item_start_x = 底2_1_x + 10
        
        # 获取当前分类的物品列表，并按照材料充足情况排序
        current_items = self.craftable_items[self.current_category]
        
        # 根据打开方式过滤物品
        if self.open_type == 'keyboard':  # 通过C键打开，只显示基础物品
            # 只显示的物品图标列表，排除箱子（只能通过工作台合成）
            allowed_icons = ['火把', '工作台', '木斧', '木镐', '木铲', '石斧', '石镐', '石铲', '木板']
            # 过滤物品列表
            current_items = [item for item in current_items if item['icon'] in allowed_icons]
        
        # 对物品进行排序：材料充足的在前，不足的在后
        sorted_items = sorted(current_items, key=lambda x: 0 if self.检查材料是否充足(x) else 1)
        
        # 遍历并检查可合成物品点击
        for index, item in enumerate(sorted_items):
            # 计算物品在网格中的位置
            row = index // self.item_grid_size
            col = index % self.item_grid_size
            
            item_x = item_start_x + col * (self.item_slot_size + self.item_slot_margin)
            item_y = item_start_y + row * (self.item_slot_size + self.item_slot_margin)
            
            # 检查物品位置是否超出面板范围
            if item_y + self.item_slot_size > 子面板_y + 660:
                break  # 超出范围，停止检查
            
            # 检查点击是否在物品格子内
            item_rect = pygame.Rect(item_x, item_y, self.item_slot_size, self.item_slot_size)
            if item_rect.collidepoint(mx, my):
                self.selected_item = item
                # 从物品定义中获取物品名称
                item_id = self.物品_id映射.get(item["icon"])
                item_info = 物品.get(item_id, {})
                item_name = item_info.get("名称", item["icon"])
                print(f"选中了物品: {item_name}")
                return True
        
        # 检查数量控制按钮点击
        # 计算合成材料底框的位置
        介绍底_y = 子面板_y + 25 + 70 + 25 + 100 + 10
        合成材料文字_y = 介绍底_y + 100 + 10
        合成材料底_y = 合成材料文字_y + 16 + 10
        合成材料底高度 = 150
        
        # 计算数量控制区域位置
        control_area_y = 合成材料底_y + 合成材料底高度 + 15  # 间距15像素
        total_control_width = (self.control_button_width * 4) + self.input_width + (self.button_spacing * 4)
        start_x = 底2_2_x + (底2_2宽度 - total_control_width) // 2
        
        # 检查第一行按钮点击
        # 最小按钮
        min_button_rect = pygame.Rect(start_x, control_area_y, self.control_button_width, self.control_button_height)
        if min_button_rect.collidepoint(mx, my):
            self.craft_amount = self.min_amount
            self.input_text = str(self.craft_amount)  # 更新输入框文本
            self.is_input_active = False  # 点击按钮后关闭输入框激活状态
            print(f"按下了最小按钮，合成数量: {self.craft_amount}")
            return True
        
        # -1按钮
        minus_button_rect = pygame.Rect(start_x + self.control_button_width + self.button_spacing, control_area_y, self.control_button_width, self.control_button_height)
        if minus_button_rect.collidepoint(mx, my):
            self.craft_amount = max(self.min_amount, self.craft_amount - 1)
            self.input_text = str(self.craft_amount)  # 更新输入框文本
            self.is_input_active = False  # 点击按钮后关闭输入框激活状态
            print(f"按下了-1按钮，合成数量: {self.craft_amount}")
            return True
        
        # 输入框点击
        input_rect = pygame.Rect(start_x + (self.control_button_width * 2) + (self.button_spacing * 2), control_area_y, self.input_width, self.input_height)
        if input_rect.collidepoint(mx, my):
            self.is_input_active = not self.is_input_active
            if self.is_input_active:
                self.input_text = str(self.craft_amount)  # 激活时显示当前数量
            else:
                # 关闭时尝试解析输入值
                try:
                    new_amount = int(self.input_text)
                    # 确保数量在有效范围内
                    self.craft_amount = max(self.min_amount, min(self.max_amount, new_amount))
                    self.input_text = str(self.craft_amount)  # 更新输入框文本为有效数量
                    print(f"合成数量设置为: {self.craft_amount}")
                except ValueError:
                    # 输入无效，恢复原有数量
                    self.input_text = str(self.craft_amount)
            return True
        
        # +1按钮
        plus_button_rect = pygame.Rect(start_x + (self.control_button_width * 2) + self.input_width + (self.button_spacing * 3), control_area_y, self.control_button_width, self.control_button_height)
        if plus_button_rect.collidepoint(mx, my):
            self.craft_amount = min(self.max_amount, self.craft_amount + 1)
            self.input_text = str(self.craft_amount)  # 更新输入框文本
            self.is_input_active = False  # 点击按钮后关闭输入框激活状态
            print(f"按下了+1按钮，合成数量: {self.craft_amount}")
            return True
        
        # 最大按钮
        max_button_rect = pygame.Rect(start_x + (self.control_button_width * 3) + self.input_width + (self.button_spacing * 4), control_area_y, self.control_button_width, self.control_button_height)
        if max_button_rect.collidepoint(mx, my):
            self.craft_amount = self.max_amount
            self.input_text = str(self.craft_amount)  # 更新输入框文本
            self.is_input_active = False  # 点击按钮后关闭输入框激活状态
            print(f"按下了最大按钮，合成数量: {self.craft_amount}")
            return True
        
        # 检查确定合成按钮点击
        confirm_y = control_area_y + self.control_button_height + 10
        confirm_x = self.底2_x + 10 + 520 + 10 + (300 - self.confirm_button_width) // 2
        confirm_rect = pygame.Rect(confirm_x, confirm_y, self.confirm_button_width, self.confirm_button_height)
        if confirm_rect.collidepoint(mx, my):
            # 检查是否选中了物品且材料充足
            if self.selected_item and self.检查材料是否充足(self.selected_item):
                print(f"按下了确定合成按钮，合成数量: {self.craft_amount}")
                
                # 获取合成配方
                recipe = self.selected_item["recipe"]
                materials_count = {}
                
                # 检查recipe类型，如果是字典格式，直接使用键值对
                if isinstance(recipe, dict):
                    # 直接使用字典的键值对作为材料和数量
                    materials_count = recipe
                else:
                    # 原有逻辑：处理二维列表格式的配方
                    for row in recipe:
                        for ingredient in row:
                            if ingredient:  # 跳过空材料
                                if ingredient in materials_count:
                                    materials_count[ingredient] += 1
                                else:
                                    materials_count[ingredient] = 1
                
                # 获取背包管理器
                if hasattr(self.game, '背包管理器'):
                    背包管理器 = self.game.背包管理器
                    
                    # 遍历材料，减少背包中的材料数量
                    for 材料名称, 需要数量 in materials_count.items():
                        # 获取材料的物品ID
                        材料_id = self.物品_id映射.get(材料名称)
                        if 材料_id:
                            # 计算需要减少的总数量（考虑合成数量）
                            总需要数量 = 需要数量 * self.craft_amount
                            # 从背包中减少材料
                            背包管理器.减少物品数量(材料_id, 总需要数量)
                    
                    # 获取合成物品的ID
                    合成物品_icon = self.selected_item["icon"]
                    合成物品_id = self.物品_id映射.get(合成物品_icon)
                    if 合成物品_id:
                        # 获取合成数量
                        合成数量 = self.selected_item.get("quantity", 1) * self.craft_amount
                        # 向背包中添加合成物品
                    if 背包管理器.添加物品到快捷栏(合成物品_id, 合成数量):
                        print(f"成功合成: {合成物品_icon} x{合成数量}")
                        # 播放合成成功音效
                        audio_manager.play_sound("敲击")
                        # 添加合成成功提示，格式：物品*合成数量合成成功
                        self.add_notification(f"{合成物品_icon}*{合成数量}合成成功")
                    else:
                        # 如果快捷栏已满，尝试添加到背包
                        if 背包管理器.添加物品到背包(合成物品_id, 合成数量):
                            print(f"成功合成: {合成物品_icon} x{合成数量}")
                            # 播放合成成功音效
                            audio_manager.play_sound("敲击")
                            # 添加合成成功提示，格式：物品*合成数量合成成功
                            self.add_notification(f"{合成物品_icon}*{合成数量}合成成功")
                        else:
                            print(f"合成失败: 背包已满")
                            # 播放合成失败音效
                            audio_manager.play_sound("警告")
                            # 添加背包满提示
                            self.add_notification("背包满了")
            return True
        
        return True
    
    def add_notification(self, text):
        """添加提示信息
        
        参数:
            text: 提示文字内容
        """
        # 获取屏幕尺寸
        screen_width, screen_height = self.game.屏幕.get_size()
        
        # 创建新的提示信息
        notification = {
            "text": text,
            "x": screen_width // 2,  # 屏幕中心
            "y": screen_height // 3 - 100,  # 屏幕上方向上飘，向上调整*像素
            "alpha": 255,  # 初始透明度
            "start_time": pygame.time.get_ticks() / 1000.0,  # 开始时间
            "speed": self.提示移动速度  # 移动速度
        }
        
        # 添加到提示列表
        self.notifications.append(notification)
    
    def handle_event(self, event):
        """处理事件"""
        if not self.is_open:
            return False
        
        if event.type == pygame.KEYDOWN:
            return self.handle_keyboard(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            return self.handle_click(mx, my, event.button)
        
        return False

# 简单的游戏类，用于测试合成页面
class Game:
    """简单的游戏类，模拟原代码中的game实例"""
    def __init__(self):
        self.屏幕 = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
        pygame.display.set_caption("合成系统演示")
        self.crafting_page = CraftingPage(self)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        """游戏主循环"""
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0
            
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and not self.crafting_page.is_open:
                        self.running = False
                    else:
                        self.crafting_page.handle_keyboard(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键点击
                        mx, my = pygame.mouse.get_pos()
                        self.crafting_page.handle_click(mx, my)
                elif event.type == pygame.VIDEORESIZE:
                    # 窗口大小改变时重新设置屏幕
                    self.屏幕 = pygame.display.set_mode(
                        (event.w, event.h), pygame.RESIZABLE)
            
            # 更新
            self.crafting_page.update(delta_time)
            
            # 渲染
            self.屏幕.fill(主背景色)
            self.crafting_page.draw(self.屏幕)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

# 测试代码
if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.crafting_page.open()  # 默认打开合成页面
    game.run()