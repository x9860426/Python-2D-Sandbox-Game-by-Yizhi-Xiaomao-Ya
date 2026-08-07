import pygame
import random
import math

# 导入boss管理器
from boos生物处理 import boss_manager

# 导入物品定义中的生物ID
from 物品定义 import (
    史莱姆, 土拨鼠, 幽灵, 蝙蝠, 火焰精灵, 蘑菇怪,
    岩石怪, 猴子, 三角龙, 丧尸, 企鹅, 僵尸, 刺球,
    双角骷髅, 变形怪, 可爱幽灵, 吸血鬼, 夜魔, 大史莱姆,
    奶龙, 小恶魔, 小熊猫, 小霸王龙, 小鸡, 岩浆怪, 幽灵人,
    建龙, 异变者, 异变骷髅, 异形眼, 异形球体, 异形蛇, 异形蜘蛛,
    恶魔球, 普通骷髅, 松鼠, 母鸡, 灰兔, 牧羊人, 狗, 独眼人,
    狼人, 猪, 白兔, 章鱼, 章鱼怪, 红眼粘液怪, 老虎, 萌刺,
    蓝怪, 蚂蚁怪物, 贝利亚, 超异变者, 邪恶粘液怪, 邪恶蜘蛛,
    邪恶蝙蝠, 金怪, 问灵, 霸王龙, 骷髅球, 鸟, 肥胖Boss, 死神, 死神祝福
)

# 导入方块属性和物品定义
from 物品定义 import 方块属性
from 物品定义 import 死神祝福

# 导入常用物品ID
from 物品定义 import (
    肉块, 苹果, 面包, 奶油面包
)

# 生物掉落物配置字典
# 格式说明：
# - 键：生物ID
# - 值：字典，包含：
#   - "掉落物品": 字符串，使用*分隔多种物品，*表示一种，**表示两种
#   - "掉落数量": 字符串，*表示固定数量，*-*表示随机数量范围
#   - "概率": 可选，掉落概率（0.0-1.0）
# 注：根据需求，只有生物和动物掉落物品，其他类型（如Boss、怪物）不掉落
生物掉落物配置 = {
    # 普通动物生物 - 掉落物品
    "史莱姆": {"掉落物品": "*肉块", "掉落数量": "1-3"},
    "土拨鼠": {"掉落物品": "*肉块", "掉落数量": "1-2"},
    "企鹅": {"掉落物品": "*肉块", "掉落数量": "1-2"},
    "小鸡": {"掉落物品": "*肉块", "掉落数量": "1"},
    "母鸡": {"掉落物品": "*肉块", "掉落数量": "1-2"},
    "松鼠": {"掉落物品": "*肉块", "掉落数量": "1"},
    "灰兔": {"掉落物品": "*肉块", "掉落数量": "1"},
    "白兔": {"掉落物品": "*肉块", "掉落数量": "1"},
    "猪": {"掉落物品": "*肉块", "掉落数量": "2-4"},
    "狗": {"掉落物品": "*肉块", "掉落数量": "1-2"},
    "老虎": {"掉落物品": "*肉块", "掉落数量": "3-5"},
    "小熊猫": {"掉落物品": "*肉块", "掉落数量": "1-2"},
    "鸟": {"掉落物品": "*肉块", "掉落数量": "1"},
    "章鱼": {"掉落物品": "*肉块", "掉落数量": "1-2"},
    "牧羊人": {"掉落物品": "*肉块", "掉落数量": "1-2"},
    "建龙": {"掉落物品": "*肉块", "掉落数量": "3-5"},
    "霸王龙": {"掉落物品": "*肉块", "掉落数量": "4-6"},
    "小霸王龙": {"掉落物品": "*肉块", "掉落数量": "2-4"},
    "奶龙": {"掉落物品": "*肉块", "掉落数量": "2-3"},
    
    # 怪物生物 - 不掉落物品（设置概率为0）
    "幽灵": {"掉落物品": "*肉块", "掉落数量": "1-2", "概率": 0.0},
    "蝙蝠": {"掉落物品": "*肉块", "掉落数量": "1", "概率": 0.0},
    "火焰精灵": {"掉落物品": "*肉块", "掉落数量": "1-2", "概率": 0.0},
    "蘑菇怪": {"掉落物品": "*肉块", "掉落数量": "2-3", "概率": 0.0},
    "岩石怪": {"掉落物品": "*肉块", "掉落数量": "2-4", "概率": 0.0},
    "丧尸": {"掉落物品": "*肉块", "掉落数量": "1-3", "概率": 0.0},
    "僵尸": {"掉落物品": "*肉块", "掉落数量": "1-3", "概率": 0.0},
    "刺球": {"掉落物品": "*肉块", "掉落数量": "1-2", "概率": 0.0},
    "双角骷髅": {"掉落物品": "*肉块", "掉落数量": "2-3", "概率": 0.0},
    "变形怪": {"掉落物品": "*肉块", "掉落数量": "2-3", "概率": 0.0},
    "可爱幽灵": {"掉落物品": "*肉块", "掉落数量": "1-2", "概率": 0.0},
    "夜魔": {"掉落物品": "*肉块", "掉落数量": "2-4", "概率": 0.0},
    "大史莱姆": {"掉落物品": "*肉块", "掉落数量": "2-4", "概率": 0.0},
    "小恶魔": {"掉落物品": "*肉块", "掉落数量": "1-2", "概率": 0.0},
    "岩浆怪": {"掉落物品": "*肉块", "掉落数量": "2-3", "概率": 0.0},
    "幽灵人": {"掉落物品": "*肉块", "掉落数量": "2-3", "概率": 0.0},
    "异变者": {"掉落物品": "*肉块", "掉落数量": "2-3", "概率": 0.0},
    "异变骷髅": {"掉落物品": "*肉块", "掉落数量": "2-3", "概率": 0.0},
    "异形眼": {"掉落物品": "*肉块", "掉落数量": "1-2", "概率": 0.0},
    "异形球体": {"掉落物品": "*肉块", "掉落数量": "1-2", "概率": 0.0},
    "异形蛇": {"掉落物品": "*肉块", "掉落数量": "2-3", "概率": 0.0},
    "异形蜘蛛": {"掉落物品": "*肉块", "掉落数量": "1-2", "概率": 0.0},
    "恶魔球": {"掉落物品": "*肉块", "掉落数量": "2-3", "概率": 0.0},
    "普通骷髅": {"掉落物品": "*肉块", "掉落数量": "1-2", "概率": 0.0},
    "独眼人": {"掉落物品": "*肉块", "掉落数量": "2-3", "概率": 0.0},
    "狼人": {"掉落物品": "*肉块", "掉落数量": "2-4", "概率": 0.0},
    "章鱼怪": {"掉落物品": "*肉块", "掉落数量": "2-3", "概率": 0.0},
    "红眼粘液怪": {"掉落物品": "*肉块", "掉落数量": "2-3", "概率": 0.0},
    "萌刺": {"掉落物品": "*肉块", "掉落数量": "1-2", "概率": 0.0},
    "蓝怪": {"掉落物品": "*肉块", "掉落数量": "2-3", "概率": 0.0},
    "蚂蚁怪物": {"掉落物品": "*肉块", "掉落数量": "1-2", "概率": 0.0},
    "超异变者": {"掉落物品": "*肉块", "掉落数量": "3-5", "概率": 0.0},
    "邪恶粘液怪": {"掉落物品": "*肉块", "掉落数量": "2-4", "概率": 0.0},
    "邪恶蜘蛛": {"掉落物品": "*肉块", "掉落数量": "1-2", "概率": 0.0},
    "邪恶蝙蝠": {"掉落物品": "*肉块", "掉落数量": "1", "概率": 0.0},
    "金怪": {"掉落物品": "**肉块,苹果", "掉落数量": "2-4,1-2", "概率": 0.0},
    "问灵": {"掉落物品": "**肉块,面包", "掉落数量": "2-4,1-2", "概率": 0.0},
    "骷髅球": {"掉落物品": "*肉块", "掉落数量": "2-3", "概率": 0.0},
    
    # Boss生物 - 不掉落物品（设置概率为0）
    "贝利亚": {"掉落物品": "**肉块,奶油面包", "掉落数量": "5-10,2-3", "概率": 0.0},
    "吸血鬼": {"掉落物品": "**肉块,苹果", "掉落数量": "4-8,2-4", "概率": 0.0},
    "肥胖Boss": {"掉落物品": "**肉块,面包", "掉落数量": "5-10,3-5", "概率": 0.0},
    "死神": {"掉落物品": "**肉块,奶油面包", "掉落数量": "4-8,2-3", "概率": 0.0},
    "死神祝福": {"掉落物品": "**肉块,苹果", "掉落数量": "4-8,2-4", "概率": 0.0}
}

class Mob:
    """生物类 - 可以自动移动和跳跃"""
    
    def __init__(self, x, y, mob_id):
        self.x = x
        self.y = y
        self.mob_id = mob_id
        
        # 根据生物ID获取生物属性
        mob_data = self.get_mob_data(mob_id)
        self.width = mob_data["width"]
        self.height = mob_data["height"]
        self.color = mob_data["color"]
        self.name = mob_data["name"]
        
        # 战斗属性
        self.health = mob_data["health"]
        self.max_health = mob_data["health"]
        self.damage = mob_data["damage"]
        self.attack_range = mob_data["attack_range"]
        self.attack_cooldown = 0
        self.attack_cooldown_max = mob_data["attack_cooldown"]
        
        # 移动属性
        self.speed = mob_data["speed"]
        self.jump_strength = mob_data["jump_strength"]
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.5
        self.is_on_ground = False
        
        # 飞行属性
        self.can_fly = mob_data.get("can_fly", False)
        self.fly_speed = self.speed * 0.8  # 飞行时的垂直移动速度
        
        # AI行为
        self.direction = random.choice([-1, 1])  # -1: 左, 1: 右
        self.move_timer = 0
        self.jump_cooldown = 0
        self.idle_timer = 0
        
        # 视野和感知
        self.sight_range = mob_data["sight_range"]  # 视野范围（格子数）
        self.jump_obstacle_range = 3  # 跳跃障碍物检测范围
        
        # 卡方块检测和强行移动
        self.连续碰撞次数 = 0
        self.强行向上力度 = 0
        self.强行向上持续时间 = 0
        self.上次位置 = self.x
        
        # 投掷物相关属性
        self.projectiles = []  # 存储当前活跃的投掷物
        
        # 死亡计时器 - 修复缺少属性导致的崩溃
        self.death_timer = 0  # 初始值为0，防止AttributeError
        self.projectile_timer = 0  # 投掷物发射计时器
        
        # 爆炸特效相关属性
        self.spike_explosions = []  # 存储当前活跃的爆炸特效
        
        # BOSS技能追踪
        self.last_skill = "未使用技能"  # 追踪上次使用的技能
        
        # 技能图片相关属性，所有生物都可以使用
        self.default_image = self.name
        self.current_image = self.default_image
        self.skill_image_duration = 60  # 1秒，假设60FPS
        self.skill_image_timer = 0
        
        # 被攻击状态属性
        self.is_attacked = False
        self.attacked_timer = 0
        
        # 如果是贝利亚、吸血鬼、肥胖Boss或死神，添加到boss管理器
        if mob_id == 贝利亚 or mob_id == 吸血鬼 or mob_id == 肥胖Boss or mob_id == 死神:
            boss_manager.add_boss(self)
            # 贝利亚特殊处理：使用正确的图片名称（不带扩展名）
            if mob_id == 贝利亚:
                self.default_image = "贝利亚"
                self.current_image = self.default_image
            # 吸血鬼特殊处理：使用正确的图片名称（不带扩展名）
            elif mob_id == 吸血鬼:
                self.default_image = "吸血鬼"
                self.current_image = self.default_image
            # 肥胖Boss特殊处理：使用正确的图片名称（不带扩展名）
            elif mob_id == 肥胖Boss:
                self.default_image = "肥婆"
                self.current_image = self.default_image
            # 死神特殊处理：使用正确的图片名称（不带扩展名）
            elif mob_id == 死神:
                self.default_image = "死神"
                self.current_image = self.default_image
            elif mob_id == 死神祝福:
                self.default_image = "死神_祝福"
                self.current_image = self.default_image
        
    def get_mob_data(self, mob_id):
        """获取生物属性数据"""
        # 生物属性定义
        MOBS = {
            史莱姆: {"name": "史莱姆", "color": (0, 200, 0), "width": 32, "height": 32, "speed": 1.0, "jump_strength": -6,
                   "health": 50, "damage": 10, "attack_range": 20, "attack_cooldown": 60, "sight_range": 5, "can_fly": False},
            土拨鼠: {"name": "土拨鼠", "color": (139, 69, 19), "width": 28, "height": 24, "speed": 1.5, "jump_strength": -8,
                   "health": 30, "damage": 8, "attack_range": 15, "attack_cooldown": 80, "sight_range": 4, "can_fly": False},
            幽灵: {"name": "幽灵", "color": (200, 200, 255), "width": 24, "height": 40, "speed": 1.2, "jump_strength": 0,
                   "health": 40, "damage": 12, "attack_range": 25, "attack_cooldown": 50, "sight_range": 7, "can_fly": True},
            蝙蝠: {"name": "蝙蝠", "color": (0, 0, 0), "width": 20, "height": 16, "speed": 2.0, "jump_strength": 0,
                   "health": 25, "damage": 15, "attack_range": 10, "attack_cooldown": 40, "sight_range": 6, "can_fly": True},
            火焰精灵: {"name": "火焰精灵", "color": (255, 100, 0), "width": 20, "height": 30, "speed": 1.8, "jump_strength": 0,
                   "health": 45, "damage": 20, "attack_range": 30, "attack_cooldown": 70, "sight_range": 8, "can_fly": True},
            蘑菇怪: {"name": "蘑菇怪", "color": (255, 0, 255), "width": 36, "height": 40, "speed": 0.8, "jump_strength": -5,
                   "health": 60, "damage": 25, "attack_range": 20, "attack_cooldown": 90, "sight_range": 5, "can_fly": False},
            岩石怪: {"name": "岩石怪", "color": (100, 100, 100), "width": 40, "height": 40, "speed": 0.6, "jump_strength": -4,
                   "health": 100, "damage": 30, "attack_range": 25, "attack_cooldown": 120, "sight_range": 4, "can_fly": False},
            猴子: {"name": "猴子", "color": (139, 69, 19), "width": 28, "height": 32, "speed": 2.0, "jump_strength": -12,
                   "health": 35, "damage": 10, "attack_range": 15, "attack_cooldown": 60, "sight_range": 6, "can_fly": False},
            三角龙: {"name": "三角龙", "color": (150, 100, 50), "width": 96, "height": 80, "speed": 1.2, "jump_strength": -5,
                   "health": 150, "damage": 40, "attack_range": 30, "attack_cooldown": 100, "sight_range": 8, "can_fly": False},
            丧尸: {"name": "丧尸", "color": (100, 200, 100), "width": 32, "height": 40, "speed": 0.8, "jump_strength": -6,
                   "health": 60, "damage": 15, "attack_range": 20, "attack_cooldown": 70, "sight_range": 5, "can_fly": False},
            企鹅: {"name": "企鹅", "color": (200, 200, 255), "width": 28, "height": 32, "speed": 1.0, "jump_strength": -4,
                   "health": 35, "damage": 8, "attack_range": 15, "attack_cooldown": 90, "sight_range": 4, "can_fly": False},
            僵尸: {"name": "僵尸", "color": (50, 100, 50), "width": 48, "height": 60, "speed": 0.9, "jump_strength": -6,
                   "health": 70, "damage": 20, "attack_range": 25, "attack_cooldown": 80, "sight_range": 6, "can_fly": False},
            刺球: {"name": "刺球", "color": (150, 50, 50), "width": 24, "height": 24, "speed": 1.1, "jump_strength": 0,
                   "health": 45, "damage": 18, "attack_range": 18, "attack_cooldown": 65, "sight_range": 5, "can_fly": True},
            双角骷髅: {"name": "双角骷髅", "color": (150, 150, 150), "width": 45, "height": 63, "speed": 1.3, "jump_strength": -8,
                   "health": 85, "damage": 25, "attack_range": 28, "attack_cooldown": 95, "sight_range": 7, "can_fly": False},
            变形怪: {"name": "变形怪", "color": (150, 100, 150), "width": 48, "height": 48, "speed": 1.4, "jump_strength": -9,
                   "health": 55, "damage": 22, "attack_range": 22, "attack_cooldown": 75, "sight_range": 6, "can_fly": False},
            可爱幽灵: {"name": "可爱幽灵", "color": (200, 200, 255), "width": 22, "height": 30, "speed": 1.5, "jump_strength": 0,
                   "health": 35, "damage": 10, "attack_range": 20, "attack_cooldown": 60, "sight_range": 5, "can_fly": True},
            吸血鬼: {"name": "吸血鬼", "color": (150, 50, 100), "width": 120, "height": 125, "speed": 1.8, "jump_strength": 0,
                   "health": 10000, "damage": 30, "attack_range": 30, "attack_cooldown": 85, "sight_range": 36, "can_fly": True},
            夜魔: {"name": "夜魔", "color": (50, 50, 100), "width": 36, "height": 45, "speed": 1.6, "jump_strength": -12,
                   "health": 90, "damage": 35, "attack_range": 35, "attack_cooldown": 110, "sight_range": 10, "can_fly": False},
            大史莱姆: {"name": "大史莱姆", "color": (0, 200, 0), "width": 72, "height": 72, "speed": 0.8, "jump_strength": -4,
                   "health": 120, "damage": 28, "attack_range": 25, "attack_cooldown": 90, "sight_range": 6, "can_fly": False},
            奶龙: {"name": "奶龙", "color": (255, 200, 200), "width": 80, "height": 72, "speed": 1.5, "jump_strength": -8,
                   "health": 100, "damage": 25, "attack_range": 28, "attack_cooldown": 80, "sight_range": 7, "can_fly": False},
            小恶魔: {"name": "小恶魔", "color": (150, 50, 50), "width": 39, "height": 52, "speed": 2.2, "jump_strength": 0,
                   "health": 50, "damage": 20, "attack_range": 22, "attack_cooldown": 60, "sight_range": 8, "can_fly": True},
            小熊猫: {"name": "小熊猫", "color": (200, 150, 100), "width": 28, "height": 28, "speed": 1.4, "jump_strength": -9,
                   "health": 40, "damage": 12, "attack_range": 18, "attack_cooldown": 70, "sight_range": 5, "can_fly": False},
            小霸王龙: {"name": "小霸王龙", "color": (150, 100, 50), "width": 54, "height": 48, "speed": 1.7, "jump_strength": -7,
                   "health": 80, "damage": 30, "attack_range": 30, "attack_cooldown": 90, "sight_range": 8, "can_fly": False},
            小鸡: {"name": "小鸡", "color": (255, 255, 200), "width": 20, "height": 20, "speed": 1.2, "jump_strength": -5,
                   "health": 20, "damage": 5, "attack_range": 10, "attack_cooldown": 50, "sight_range": 3, "can_fly": False},
            岩浆怪: {"name": "岩浆怪", "color": (255, 100, 0), "width": 32, "height": 32, "speed": 1.0, "jump_strength": -6,
                   "health": 100, "damage": 35, "attack_range": 25, "attack_cooldown": 100, "sight_range": 6, "can_fly": False},
            幽灵人: {"name": "幽灵人", "color": (200, 200, 255), "width": 32, "height": 40, "speed": 1.4, "jump_strength": 0,
                   "health": 60, "damage": 18, "attack_range": 25, "attack_cooldown": 70, "sight_range": 8, "can_fly": True},
            建龙: {"name": "建龙", "color": (150, 100, 50), "width": 96, "height": 84, "speed": 1.3, "jump_strength": -8,
                   "health": 130, "damage": 45, "attack_range": 35, "attack_cooldown": 120, "sight_range": 9, "can_fly": False},
            异变者: {"name": "异变者", "color": (150, 50, 50), "width": 51, "height": 63, "speed": 1.5, "jump_strength": -9,
                   "health": 75, "damage": 28, "attack_range": 28, "attack_cooldown": 80, "sight_range": 7, "can_fly": False},
            异变骷髅: {"name": "异变骷髅", "color": (150, 150, 150), "width": 48, "height": 67, "speed": 1.6, "jump_strength": 0,
                   "health": 95, "damage": 32, "attack_range": 30, "attack_cooldown": 90, "sight_range": 8, "can_fly": True},
            异形眼: {"name": "异形眼", "color": (255, 100, 100), "width": 28, "height": 28, "speed": 2.0, "jump_strength": -8,
                   "health": 60, "damage": 25, "attack_range": 22, "attack_cooldown": 70, "sight_range": 10, "can_fly": False},
            异形球体: {"name": "异形球体", "color": (150, 100, 150), "width": 24, "height": 24, "speed": 1.8, "jump_strength": -6,
                   "health": 50, "damage": 20, "attack_range": 18, "attack_cooldown": 60, "sight_range": 8, "can_fly": False},
            异形蛇: {"name": "异形蛇", "color": (100, 150, 50), "width": 36, "height": 20, "speed": 2.2, "jump_strength": -4,
                   "health": 45, "damage": 30, "attack_range": 25, "attack_cooldown": 85, "sight_range": 9, "can_fly": False},
            异形蜘蛛: {"name": "异形蜘蛛", "color": (100, 50, 50), "width": 32, "height": 28, "speed": 2.4, "jump_strength": -10,
                   "health": 55, "damage": 35, "attack_range": 20, "attack_cooldown": 75, "sight_range": 7, "can_fly": False},
            恶魔球: {"name": "恶魔球", "color": (150, 50, 50), "width": 28, "height": 28, "speed": 1.6, "jump_strength": -6,
                   "health": 70, "damage": 22, "attack_range": 25, "attack_cooldown": 80, "sight_range": 6, "can_fly": False},
            普通骷髅: {"name": "普通骷髅", "color": (150, 150, 150), "width": 45, "height": 60, "speed": 1.3, "jump_strength": -8,
                   "health": 65, "damage": 20, "attack_range": 25, "attack_cooldown": 90, "sight_range": 7, "can_fly": False},
            松鼠: {"name": "松鼠", "color": (150, 100, 50), "width": 24, "height": 24, "speed": 2.0, "jump_strength": -9,
                   "health": 30, "damage": 8, "attack_range": 12, "attack_cooldown": 60, "sight_range": 5, "can_fly": False},
            母鸡: {"name": "母鸡", "color": (255, 255, 200), "width": 28, "height": 28, "speed": 1.1, "jump_strength": -5,
                   "health": 25, "damage": 6, "attack_range": 10, "attack_cooldown": 70, "sight_range": 4, "can_fly": False},
            灰兔: {"name": "灰兔", "color": (150, 150, 150), "width": 22, "height": 20, "speed": 2.3, "jump_strength": -10,
                   "health": 20, "damage": 5, "attack_range": 10, "attack_cooldown": 50, "sight_range": 4, "can_fly": False},
            牧羊人: {"name": "牧羊人", "color": (100, 100, 100), "width": 48, "height": 60, "speed": 1.4, "jump_strength": -7,
                   "health": 70, "damage": 18, "attack_range": 22, "attack_cooldown": 85, "sight_range": 6, "can_fly": False},
            狗: {"name": "狗", "color": (150, 100, 50), "width": 28, "height": 28, "speed": 2.5, "jump_strength": -8,
                   "health": 45, "damage": 15, "attack_range": 18, "attack_cooldown": 60, "sight_range": 8, "can_fly": False},
            独眼人: {"name": "独眼人", "color": (150, 100, 100), "width": 54, "height": 63, "speed": 1.2, "jump_strength": -7,
                   "health": 80, "damage": 28, "attack_range": 30, "attack_cooldown": 95, "sight_range": 7, "can_fly": False},
            狼人: {"name": "狼人", "color": (100, 50, 50), "width": 51, "height": 60, "speed": 1.9, "jump_strength": -12,
                   "health": 90, "damage": 32, "attack_range": 32, "attack_cooldown": 80, "sight_range": 9, "can_fly": False},
            猪: {"name": "猪", "color": (200, 150, 150), "width": 32, "height": 28, "speed": 1.0, "jump_strength": -5,
                   "health": 35, "damage": 8, "attack_range": 15, "attack_cooldown": 80, "sight_range": 4, "can_fly": False},
            白兔: {"name": "白兔", "color": (255, 255, 255), "width": 22, "height": 20, "speed": 2.4, "jump_strength": -11,
                   "health": 22, "damage": 6, "attack_range": 10, "attack_cooldown": 55, "sight_range": 4, "can_fly": False},
            章鱼: {"name": "章鱼", "color": (100, 150, 200), "width": 32, "height": 32, "speed": 1.3, "jump_strength": -6,
                   "health": 50, "damage": 18, "attack_range": 20, "attack_cooldown": 70, "sight_range": 6, "can_fly": False},
            章鱼怪: {"name": "章鱼怪", "color": (100, 50, 150), "width": 40, "height": 36, "speed": 1.1, "jump_strength": -5,
                   "health": 85, "damage": 30, "attack_range": 28, "attack_cooldown": 100, "sight_range": 7, "can_fly": False},
            红眼粘液怪: {"name": "红眼粘液怪", "color": (255, 100, 100), "width": 54, "height": 54, "speed": 0.9, "jump_strength": -5,
                   "health": 75, "damage": 25, "attack_range": 22, "attack_cooldown": 85, "sight_range": 5, "can_fly": False},
            老虎: {"name": "老虎", "color": (150, 100, 50), "width": 40, "height": 32, "speed": 2.2, "jump_strength": -10,
                   "health": 120, "damage": 45, "attack_range": 35, "attack_cooldown": 90, "sight_range": 10, "can_fly": False},
            萌刺: {"name": "萌刺", "color": (150, 50, 50), "width": 24, "height": 24, "speed": 1.5, "jump_strength": -6,
                   "health": 40, "damage": 15, "attack_range": 18, "attack_cooldown": 65, "sight_range": 5, "can_fly": False},
            蓝怪: {"name": "蓝怪", "color": (50, 50, 150), "width": 32, "height": 38, "speed": 1.4, "jump_strength": -8,
                   "health": 65, "damage": 22, "attack_range": 25, "attack_cooldown": 75, "sight_range": 7, "can_fly": False},
            蚂蚁怪物: {"name": "蚂蚁怪物", "color": (100, 150, 50), "width": 30, "height": 26, "speed": 2.5, "jump_strength": -9,
                   "health": 45, "damage": 20, "attack_range": 20, "attack_cooldown": 60, "sight_range": 8, "can_fly": False},
            贝利亚: {"name": "贝利亚", "color": (150, 50, 100), "width": 120, "height": 125, "speed": 2.0, "jump_strength": -12,
                   "health": 25000, "damage": 15, "attack_range": 400, "attack_cooldown": 120, "sight_range": 76, "can_fly": True},
            超异变者: {"name": "超异变者", "color": (200, 50, 50), "width": 57, "height": 72, "speed": 1.9, "jump_strength": -10,
                   "health": 150, "damage": 50, "attack_range": 35, "attack_cooldown": 120, "sight_range": 10, "can_fly": False},
            邪恶粘液怪: {"name": "邪恶粘液怪", "color": (100, 50, 100), "width": 60, "height": 60, "speed": 1.0, "jump_strength": -5,
                   "health": 90, "damage": 30, "attack_range": 25, "attack_cooldown": 95, "sight_range": 6, "can_fly": False},
            邪恶蜘蛛: {"name": "邪恶蜘蛛", "color": (50, 50, 50), "width": 36, "height": 32, "speed": 2.6, "jump_strength": -11,
                   "health": 70, "damage": 40, "attack_range": 25, "attack_cooldown": 80, "sight_range": 9, "can_fly": False},
            邪恶蝙蝠: {"name": "邪恶蝙蝠", "color": (50, 50, 50), "width": 48, "height": 40, "speed": 2.8, "jump_strength": 0,
                   "health": 35, "damage": 25, "attack_range": 15, "attack_cooldown": 55, "sight_range": 10, "can_fly": True},
            金怪: {"name": "金怪", "color": (255, 200, 50), "width": 32, "height": 36, "speed": 1.2, "jump_strength": -7,
                   "health": 180, "damage": 55, "attack_range": 35, "attack_cooldown": 130, "sight_range": 8, "can_fly": False},
            问灵: {"name": "问灵", "color": (200, 200, 255), "width": 30, "height": 42, "speed": 1.6, "jump_strength": 0,
                   "health": 100, "damage": 35, "attack_range": 30, "attack_cooldown": 100, "sight_range": 9, "can_fly": True},
            霸王龙: {"name": "霸王龙", "color": (150, 100, 50), "width": 112, "height": 100, "speed": 1.5, "jump_strength": -6,
                   "health": 250, "damage": 70, "attack_range": 45, "attack_cooldown": 160, "sight_range": 12, "can_fly": False},
            骷髅球: {"name": "骷髅球", "color": (150, 150, 150), "width": 28, "height": 28, "speed": 2.1, "jump_strength": -8,
                   "health": 60, "damage": 28, "attack_range": 22, "attack_cooldown": 75, "sight_range": 7, "can_fly": False},
            鸟: {"name": "鸟", "color": (255, 200, 150), "width": 22, "height": 22, "speed": 2.7, "jump_strength": 0,
                   "health": 25, "damage": 8, "attack_range": 12, "attack_cooldown": 50, "sight_range": 6, "can_fly": True},
            肥胖Boss: {"name": "肥胖Boss", "color": (200, 100, 100), "width": 150, "height": 150, "speed": 1.0, "jump_strength": -8,
                   "health": 15000, "damage": 20, "attack_range": 120, "attack_cooldown": 100, "sight_range": 8, "can_fly": False},
            死神: {"name": "死神", "color": (0, 0, 0), "width": 120, "height": 180, "speed": 1.5, "jump_strength": 0,
                   "health": 50000, "damage": 30, "attack_range": 160, "attack_cooldown": 120, "sight_range": 160, "can_fly": True},
            死神祝福: {"name": "死神祝福", "color": (100, 0, 100), "width": 60, "height": 90, "speed": 1.5, "jump_strength": 0,
                   "health": 250, "damage": 40, "attack_range": 160, "attack_cooldown": 120, "sight_range": 160, "can_fly": True}
        }
        
        return MOBS.get(mob_id, {"name": "未知生物", "color": (255, 255, 255), "width": 32, "height": 32, "speed": 1.0, "jump_strength": -8,
                               "health": 50, "damage": 5, "attack_range": 20, "attack_cooldown": 60, "sight_range": 5})
    
    def update(self, world, player):
        # 根据是否能飞决定是否应用重力
        if not self.can_fly:
            self.vel_y += self.gravity
        
        # 死神特殊状态更新
        if self.mob_id == 死神:
            # 检查是否处于特殊激活状态
            if hasattr(self, 'special_activated') and self.special_activated:
                # 更新死亡计时器
                self.death_timer -= 1
                
                # 检查计时器是否结束
                if self.death_timer <= 0:
                    # 创建死神镰刀掉落物
                    for _ in range(1):  # 创建1个镰刀
                        self.create_death_sickle(player)
                    # 设置生命值为0，使其死亡
                    self.health = 0
        
        # 战斗逻辑
        # 计算与玩家的距离
        dx = player.坐标_x - self.x
        dy = player.坐标_y - self.y
        dist = math.hypot(dx, dy)
        
        # 更新投掷物
        if hasattr(self, 'projectiles'):
            for projectile in self.projectiles[:]:
                # 更新投掷物位置，兼容两种属性名
                if 'velocity_x' in projectile:
                    # 旧格式使用velocity_x和velocity_y
                    projectile['x'] += projectile['velocity_x']
                    projectile['y'] += projectile['velocity_y']
                elif 'vx' in projectile:
                    # 新格式使用vx和vy（支持0.016秒的时间缩放）
                    projectile['x'] += projectile['vx'] * 0.016
                    projectile['y'] += projectile['vy'] * 0.016
                
                # 更新计时器（兼容两种计时方式）
                if 'timer' in projectile:
                    if projectile['timer'] > 0:
                        # 倒计时方式
                        projectile['timer'] -= 1
                    else:
                        # 正计时方式
                        projectile['timer'] += 1
                
                # 检查投掷物是否超时
                if 'lifetime' in projectile:
                    if ('timer' in projectile and projectile['timer'] <= 0) or ('timer' in projectile and projectile['timer'] >= projectile['lifetime']):
                        self.projectiles.remove(projectile)
                        continue
                
                # 检查投掷物是否击中玩家
                projectile_rect = pygame.Rect(projectile['x'], projectile['y'], projectile['width'], projectile['height'])
                player_rect = pygame.Rect(player.坐标_x, player.坐标_y, player.宽, player.高)
                
                if projectile_rect.colliderect(player_rect):
                    # 击中玩家，造成伤害
                    player.take_damage(projectile['damage'], self)
                    print(f"玩家被死神镰刀击中！受到 {projectile['damage']} 点伤害！")
                    # 移除投掷物
                    self.projectiles.remove(projectile)
                    continue
        
        # 肥胖Boss的特殊技能：跳跃落地造成区域伤害
        if self.mob_id == 肥胖Boss:
            # 初始化上次落地状态（如果不存在）
            if not hasattr(self, 'last_is_on_ground'):
                self.last_is_on_ground = self.is_on_ground
            
            # 检测是否从空中落地（上一帧不在地面，当前帧在地面）
            if self.is_on_ground and not self.last_is_on_ground:
                # 落地时造成区域伤害
                # 检查是否是超级跳跃落地
                is_super_jump = getattr(self, 'is_super_jump', False)
                if is_super_jump:
                    # 超级跳跃落地：5格范围，18点伤害（减少40%）
                    damage_radius = 160  # 5格 * 32像素/格
                    damage_rect = pygame.Rect(
                        self.x + self.width // 2 - damage_radius // 2,
                        self.y + self.height // 2 - damage_radius // 2,
                        damage_radius,
                        damage_radius
                    )
                    
                    # 检测玩家是否在伤害区域内
                    player_rect = pygame.Rect(player.坐标_x, player.坐标_y, player.宽, player.高)
                    if player_rect.colliderect(damage_rect):
                        # 造成18点伤害，狂暴状态下翻倍
                        base_damage = 18  # 减少40%，从30变为18
                        final_damage = base_damage * 2 if self.is_raging else base_damage
                        player.take_damage(final_damage, self)
                    
                    # 创建超级跳跃落地特效
                    landing_x = self.x + self.width // 2
                    landing_y = self.y + self.height // 2
                    
                    # 使用自身的特效列表，确保特效能够被正确绘制
                    if not hasattr(self, 'landing_effects'):
                        self.landing_effects = []
                    
                    # 超级跳跃特效：更亮的颜色，更大的半径，更长的持续时间
                    effect_color = (255, 50, 50)  # 红色，更醒目
                    effect_max_radius = damage_radius + 50  # 更大的半径
                    effect_duration = 0.7  # 更长的持续时间
                    
                    # 添加特效到列表
                    self.landing_effects.append({
                        'x': landing_x,
                        'y': landing_y,
                        'radius': 0,
                        'max_radius': effect_max_radius,
                        'color': effect_color,
                        'duration': effect_duration,
                        'lifetime': effect_duration
                    })
                    
                    # 清除超级跳跃标记
                    self.is_super_jump = False
                # 普通跳跃无伤害，无特效
            
            # 更新上次落地状态
            self.last_is_on_ground = self.is_on_ground
            
            # 肥胖Boss新技能4：狂暴状态
            # 初始化狂暴状态相关属性
            if not hasattr(self, 'is_raging'):
                self.is_raging = False  # 是否处于狂暴状态
                self.rage_duration = 600  # 狂暴持续时间：10秒 * 60帧/秒
                self.rage_cooldown = 600  # 狂暴冷却时间：10秒 * 60帧/秒（缩短为10秒）
                self.rage_timer = 0  # 狂暴状态计时器
                self.rage_cooldown_timer = 0  # 狂暴冷却计时器
                self.base_damage = self.damage  # 记录基础伤害
                self.original_width = self.width  # 记录原始宽度
                self.original_height = self.height  # 记录原始高度
                self.original_color = self.color  # 记录原始颜色
                # 计算狂暴状态下的颜色（增加20%红色）
                self.rage_color = (
                    min(255, int(self.original_color[0] * 1.2)),  # 红色增加20%
                    self.original_color[1],  # 绿色保持不变
                    self.original_color[2]   # 蓝色保持不变
                )
                print(f"肥胖Boss初始化狂暴状态 - 基础伤害: {self.base_damage}, 原始大小: {self.original_width}x{self.original_height}")
            
            # 更新狂暴状态和冷却计时器
            if self.is_raging:
                self.rage_timer += 1
                # 狂暴状态结束
                if self.rage_timer >= self.rage_duration:
                    self.is_raging = False
                    self.rage_timer = 0
                    self.damage = self.base_damage  # 恢复基础伤害
                    # 恢复原始大小和颜色
                    self.width = self.original_width
                    self.height = self.original_height
                    self.color = self.original_color
                    # 重置技能状态
                    self.last_skill = "未使用技能"
                    print("肥胖Boss狂暴状态结束 - 恢复原始属性")
            else:
                self.rage_cooldown_timer += 1
            
            # 冷却结束后立即触发狂暴状态
            if not self.is_raging and self.rage_cooldown_timer >= self.rage_cooldown:
                self.is_raging = True
                self.rage_cooldown_timer = 0
                self.rage_timer = 0
                self.damage = self.base_damage * 2  # 近战攻击伤害翻倍
                # 应用特效：10%体积增大
                self.width = int(self.original_width * 1.1)
                self.height = int(self.original_height * 1.1)
                # 应用特效：20%红色增强
                self.color = self.rage_color
                # 更新last_skill属性，显示在血量条上
                self.last_skill = "狂暴"
                print(f"肥胖Boss触发狂暴状态 - 伤害: {self.damage}, 大小: {self.width}x{self.height}, 颜色: {self.color}")
            
            # 肥胖Boss新技能：朝向玩家发射3发粉笔，每发造成12点伤害
            # 初始化粉笔发射计时器和冷却时间
            if not hasattr(self, 'chalk_timer'):
                self.chalk_timer = 0
            if not hasattr(self, 'chalk_cooldown'):
                self.chalk_cooldown = 540  # 9秒冷却（增加150%，减少75%频率）
            
            # 更新计时器
            self.chalk_timer += 1
            
            # 肥胖Boss新技能5：天降大量随机距离书，击中玩家震动屏幕，伤害20
            # 初始化书技能相关属性
            if not hasattr(self, 'book_timer'):
                self.book_timer = 0
            if not hasattr(self, 'book_cooldown'):
                self.book_cooldown = 720  # 12秒冷却（增加150%，减少75%频率）
            if not hasattr(self, 'books'):
                self.books = []  # 存储当前活跃的书
            
            # 更新书技能计时器
            self.book_timer += 1
            
            # 肥胖Boss新技能6：粉笔领域，生成三圈顺时针，逆时针，粉笔每圈9发粉笔，触碰造成6伤害
            # 初始化粉笔领域技能相关属性
            if not hasattr(self, 'chalk_field_timer'):
                self.chalk_field_timer = 0
            if not hasattr(self, 'chalk_field_cooldown'):
                self.chalk_field_cooldown = 900  # 15秒冷却（增加150%，减少75%频率）
            if not hasattr(self, 'chalk_field_chalks'):
                self.chalk_field_chalks = []  # 存储当前活跃的粉笔领域粉笔
            
            # 更新粉笔领域技能计时器
            self.chalk_field_timer += 1
            
            # 肥胖Boss新技能7：念经，从语文文章句子字典中选择内容作为投掷物向玩家发射
            # 初始化念经技能相关属性
            if not hasattr(self, 'chant_timer'):
                self.chant_timer = 0
            if not hasattr(self, 'chant_cooldown'):
                self.chant_cooldown = 720  # 12秒冷却（增加150%，减少75%频率）
            if not hasattr(self, 'chant_projectiles'):
                self.chant_projectiles = []  # 存储当前活跃的念经投掷物
            
            # 更新念经技能计时器
            self.chant_timer += 1
            
            # 肥胖Boss新技能8：大叫有特效，玩家离boss越近，造成伤害越高，并击退，造成多次（1-5）伤害
            # 初始化大叫技能相关属性
            if not hasattr(self, 'shout_timer'):
                self.shout_timer = 0
            if not hasattr(self, 'shout_cooldown'):
                self.shout_cooldown = 1080  # 18秒冷却（增加150%，减少75%频率）
            if not hasattr(self, 'is_shouting'):
                self.is_shouting = False  # 是否正在大叫
            if not hasattr(self, 'shout_duration'):
                self.shout_duration = 30  # 大叫持续30帧
            if not hasattr(self, 'shout_frame'):
                self.shout_frame = 0  # 当前大叫帧数
            if not hasattr(self, 'shout_effects'):
                self.shout_effects = []  # 存储大叫特效
            if not hasattr(self, 'shout_damage_count'):
                self.shout_damage_count = 0  # 已造成的伤害次数
            if not hasattr(self, 'max_shout_damages'):
                self.max_shout_damages = random.randint(1, 5)  # 随机1-5次伤害
            
            # 更新大叫技能计时器
            self.shout_timer += 1
            
            # 当冷却时间到了，发射3发粉笔
            if self.chalk_timer >= self.chalk_cooldown:
                self.chalk_timer = 0
                
                # 更新last_skill属性，显示在血量条上
                self.last_skill = "粉笔攻击"
                # 切换到魔法攻击图片
                self.current_image = "肥婆_魔法攻击"
                self.skill_image_timer = self.skill_image_duration
                print(f"肥胖Boss使用魔法攻击 - 切换到图片: {self.current_image}")
                
                # 计算发射位置（肥胖Boss中心）
                start_x = self.x + self.width // 2
                start_y = self.y + self.height // 2
                
                # 计算到玩家的距离和方向
                dx = player.坐标_x - start_x
                dy = player.坐标_y - start_y
                dist = math.hypot(dx, dy)
                
                if dist > 0:
                    # 计算基础方向
                    base_dir_x = dx / dist
                    base_dir_y = dy / dist
                    
                    # 计算基础角度
                    base_angle = math.atan2(dy, dx)
                    
                    # 发射3发粉笔，每发有轻微的角度偏移
                    for i in range(3):
                        # 计算每发粉笔的角度偏移（-10度，0度，+10度）
                        angle_offset = math.radians((i - 1) * 10)
                        current_angle = base_angle + angle_offset
                        
                        # 计算每发粉笔的速度向量
                        chalk_speed = 250
                        vx = math.cos(current_angle) * chalk_speed
                        vy = math.sin(current_angle) * chalk_speed
                        
                        # 计算角度（用于旋转图片）
                        angle = -math.degrees(math.atan2(vy, vx))
                        
                        # 添加粉笔投掷物（使用现有投掷物图片）
                        self.projectiles.append({
                            'x': start_x,
                            'y': start_y,
                            'vx': vx,
                            'vy': vy,
                            'speed': chalk_speed,
                            'target': player,
                            'timer': 180,  # 3秒后消失
                            'image': "5投掷物",  # 使用现有投掷物图片
                            'width': 20,
                            'height': 10,
                            'angle': angle,
                            'damage': 12,  # 每发造成12点伤害
                            'type': 'chalk'  # 标记为粉笔类型
                        })
            
            # 当书技能冷却时间到了，生成天降书
            if self.book_timer >= self.book_cooldown:
                self.book_timer = 0
                
                # 更新last_skill属性，显示在血量条上
                self.last_skill = "天降书"
                # 切换到魔法攻击图片
                self.current_image = "肥婆_魔法攻击"
                self.skill_image_timer = self.skill_image_duration
                print(f"肥胖Boss使用魔法攻击 - 切换到图片: {self.current_image}")
                
                # 生成大量书（10-15本）
                book_count = random.randint(10, 15)
                for _ in range(book_count):
                    # 随机生成书的起始位置（屏幕上方，左右随机）
                    # 以肥胖Boss为中心，左右随机距离
                    random_offset = random.randint(-300, 300)
                    start_x = self.x + self.width // 2 + random_offset
                    start_y = self.y - 200  # 从上方200像素处开始掉落
                    
                    # 随机生成书的速度和旋转角度
                    vx = random.randint(-50, 50)  # 水平速度
                    vy = random.randint(100, 200)  # 垂直速度（向下）
                    angle = random.randint(0, 360)  # 初始旋转角度
                    
                    # 添加书到列表
                    self.books.append({
                        'x': start_x,
                        'y': start_y,
                        'vx': vx,
                        'vy': vy,
                        'angle': angle,
                        'angle_speed': random.randint(-5, 5),  # 旋转速度
                        'timer': 300,  # 5秒后消失
                        'width': 24,
                        'height': 32,
                        'damage': 12,  # 每本书造成12点伤害（减少40%）
                        'type': 'book'  # 标记为书类型
                    })
            
            # 当粉笔领域技能冷却时间到了，生成粉笔领域
            if self.chalk_field_timer >= self.chalk_field_cooldown:
                self.chalk_field_timer = 0
                
                # 更新last_skill属性，显示在血量条上
                self.last_skill = "粉笔领域"
                # 切换到魔法攻击图片
                self.current_image = "肥婆_魔法攻击"
                self.skill_image_timer = self.skill_image_duration
                print(f"肥胖Boss使用魔法攻击 - 切换到图片: {self.current_image}")
                
                # 粉笔领域配置
                circles = 3  # 三圈粉笔
                chalks_per_circle = 9  # 每圈9发粉笔
                circle_radii = [80, 120, 160]  # 三圈的半径（像素）
                rotation_directions = [1, -1, 1]  # 每圈的旋转方向（1顺时针，-1逆时针）
                
                for circle_index in range(circles):
                    radius = circle_radii[circle_index]
                    direction = rotation_directions[circle_index]
                    
                    # 生成每圈的9发粉笔
                    for i in range(chalks_per_circle):
                        # 计算每发粉笔的初始角度（均匀分布在圆周上）
                        angle = (i / chalks_per_circle) * 2 * math.pi
                        
                        # 计算粉笔的初始位置
                        start_x = self.x + self.width // 2 + math.cos(angle) * radius
                        start_y = self.y + self.height // 2 + math.sin(angle) * radius
                        
                        # 计算旋转速度（根据圈数和方向调整）
                        rotation_speed = direction * (2 + circle_index * 0.5)  # 外圈旋转更快
                        
                        # 添加粉笔到列表
                        self.chalk_field_chalks.append({
                            'x': start_x,
                            'y': start_y,
                            'radius': radius,  # 记录所在圈的半径
                            'angle': angle,  # 当前角度
                            'rotation_speed': rotation_speed,  # 旋转速度（弧度/帧）
                            'center_x': self.x + self.width // 2,  # 旋转中心X
                            'center_y': self.y + self.height // 2,  # 旋转中心Y
                            'timer': 240,  # 4秒后消失
                            'width': 15,
                            'height': 5,
                            'damage': 6,  # 每发造成6点伤害
                            'type': 'chalk_field'  # 标记为粉笔领域类型
                        })
            
            # 肥胖Boss新技能7：念经，从语文文章句子字典中选择内容作为投掷物向玩家发射
            # 语文类文章句子字典（包含经典文学作品中的句子）
            chinese_articles = {
                "论语": [
                    "学而时习之，不亦说乎？",
                    "有朋自远方来，不亦乐乎？",
                    "人不知而不愠，不亦君子乎？",
                    "温故而知新，可以为师矣。",
                    "学而不思则罔，思而不学则殆。",
                    "知之为知之，不知为不知，是知也。",
                    "三人行，必有我师焉。择其善者而从之，其不善者而改之。",
                    "岁寒，然后知松柏之后凋也。",
                    "己所不欲，勿施于人。",
                    "士不可以不弘毅，任重而道远。",
                    "见贤思齐焉，见不贤而内自省也。",
                    "君子坦荡荡，小人长戚戚。",
                    "不在其位，不谋其政。",
                    "道不同，不相为谋。",
                    "言必信，行必果。"
                ],
                "道德经": [
                    "道可道，非常道。名可名，非常名。",
                    "有无相生，难易相成。",
                    "上善若水，水善利万物而不争。",
                    "祸兮福之所倚，福兮祸之所伏。",
                    "千里之行，始于足下。",
                    "天地不仁，以万物为刍狗。",
                    "治大国，若烹小鲜。",
                    "知人者智，自知者明。",
                    "胜人者有力，自胜者强。",
                    "知足者富，强行者有志。",
                    "合抱之木，生于毫末。",
                    "九层之台，起于累土。",
                    "天网恢恢，疏而不失。",
                    "知者不言，言者不知。",
                    "大方无隅，大器晚成。"
                ],
                "诗经": [
                    "关关雎鸠，在河之洲。窈窕淑女，君子好逑。",
                    "蒹葭苍苍，白露为霜。所谓伊人，在水一方。",
                    "桃之夭夭，灼灼其华。之子于归，宜其室家。",
                    "投我以木桃，报之以琼瑶。",
                    "青青子衿，悠悠我心。",
                    "我心匪石，不可转也。我心匪席，不可卷也。",
                    "昔我往矣，杨柳依依。今我来思，雨雪霏霏。",
                    "死生契阔，与子成说。执子之手，与子偕老。",
                    "如切如磋，如琢如磨。",
                    "高山仰止，景行行止。",
                    "他山之石，可以攻玉。",
                    "靡不有初，鲜克有终。",
                    "言者无罪，闻者足戒。",
                    "一日不见，如三秋兮。",
                    "巧笑倩兮，美目盼兮。"
                ],
                "唐诗": [
                    "床前明月光，疑是地上霜。举头望明月，低头思故乡。",
                    "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。",
                    "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。",
                    "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。",
                    "离离原上草，一岁一枯荣。野火烧不尽，春风吹又生。",
                    "两个黄鹂鸣翠柳，一行白鹭上青天。",
                    "黄河远上白云间，一片孤城万仞山。",
                    "独在异乡为异客，每逢佳节倍思亲。",
                    "朝辞白帝彩云间，千里江陵一日还。",
                    "飞流直下三千尺，疑是银河落九天。",
                    "天生我材必有用，千金散尽还复来。",
                    "举杯邀明月，对影成三人。",
                    "会当凌绝顶，一览众山小。",
                    "随风潜入夜，润物细无声。",
                    "清明时节雨纷纷，路上行人欲断魂。",
                    "停车坐爱枫林晚，霜叶红于二月花。",
                    "商女不知亡国恨，隔江犹唱后庭花。",
                    "忽如一夜春风来，千树万树梨花开。",
                    "春蚕到死丝方尽，蜡炬成灰泪始干。",
                    "身无彩凤双飞翼，心有灵犀一点通。"
                ]
            }
            
            # 当念经技能冷却时间到了，生成念经投掷物
            if self.chant_timer >= self.chant_cooldown:
                self.chant_timer = 0
                
                # 更新last_skill属性，显示在血量条上
                self.last_skill = "念经"
                # 切换到魔法攻击图片
                self.current_image = "肥婆_魔法攻击"
                self.skill_image_timer = self.skill_image_duration
                print(f"肥胖Boss使用魔法攻击 - 切换到图片: {self.current_image}")
                
                # 生成3-5个念经投掷物
                chant_count = random.randint(3, 5)
                for _ in range(chant_count):
                    # 随机选择一个文章类型
                    article_type = random.choice(list(chinese_articles.keys()))
                    # 从该文章类型中随机选择一个句子
                    sentence = random.choice(chinese_articles[article_type])
                    
                    # 计算发射方向（朝向玩家）
                    dx = player.坐标_x - (self.x + self.width // 2)
                    dy = player.坐标_y - (self.y + self.height // 2)
                    dist = math.hypot(dx, dy)
                    
                    if dist > 0:
                        # 计算朝向玩家的方向
                        dir_x = dx / dist
                        dir_y = dy / dist
                        
                        # 计算初始位置（Boss中心）
                        start_x = self.x + self.width // 2
                        start_y = self.y + self.height // 2
                        
                        # 计算速度
                        speed = random.randint(150, 250)
                        vx = dir_x * speed
                        vy = dir_y * speed
                        
                        # 添加念经投掷物到列表
                        self.chant_projectiles.append({
                            'x': start_x,
                            'y': start_y,
                            'vx': vx,
                            'vy': vy,
                            'speed': speed,
                            'sentence': sentence,
                            'article_type': article_type,
                            'timer': 300,  # 5秒后消失
                            'width': len(sentence) * 10 + 20,  # 根据句子长度调整宽度
                            'height': 30,
                            'damage': 9,  # 每发造成9点伤害（减少40%）
                            'type': 'chant'  # 标记为念经类型
                        })
            
            # 当大叫技能冷却时间到了，开始大叫
            if self.shout_timer >= self.shout_cooldown:
                self.shout_timer = 0
                
                # 更新last_skill属性，显示在血量条上
                self.last_skill = "大叫"
                # 切换到狮吼功图片
                self.current_image = "肥婆_狮吼功"
                self.skill_image_timer = self.skill_image_duration
                print(f"肥胖Boss使用狮吼功 - 切换到图片: {self.current_image}")
                
                # 开始大叫
                self.is_shouting = True
                self.shout_frame = 0
                self.shout_damage_count = 0
                self.max_shout_damages = random.randint(1, 5)  # 随机1-5次伤害
                
                # 生成1-5个不同半径的圈特效
                circle_count = random.randint(1, 5)
                max_radius = 300
                
                for i in range(circle_count):
                    # 每个圈有不同的起始半径和最大半径
                    start_radius = (i / circle_count) * max_radius * 0.3
                    circle_max_radius = max_radius * (0.5 + (i / circle_count) * 0.5)
                    
                    # 每个圈有不同的颜色变化
                    r = 255 - i * 30
                    g = 100 + i * 20
                    b = 100 + i * 20
                    
                    self.shout_effects.append({
                        'x': self.x + self.width // 2,
                        'y': self.y + self.height // 2,
                        'radius': start_radius,
                        'max_radius': circle_max_radius,  # 不同的最大半径
                        'alpha': 255,
                        'timer': self.shout_duration,
                        'color': (r, g, b)  # 不同的颜色
                    })
                
                # 计算玩家与Boss的距离
                dx = player.坐标_x - (self.x + self.width // 2)
                dy = player.坐标_y - (self.y + self.height // 2)
                dist = math.hypot(dx, dy)
                

        
        # 验证是否在视野范围内
        if dist < self.sight_range * 32:  # 将格子数转换为像素
            # 肥胖Boss的移动和近战攻击逻辑
            if self.mob_id == 肥胖Boss:
                # 离玩家攻击范围内
                if dist <= self.attack_range:
                    # 在攻击范围内，停止移动并尝试攻击
                    self.vel_x = 0
                    if self.can_fly:
                        self.vel_y = 0
                    # 攻击玩家
                    self.attack(player)
                else:
                    # 向玩家移动
                    dir_x = dx / dist
                    dir_y = dy / dist
                    self.vel_x = dir_x * self.speed
                    self.direction = 1 if dir_x > 0 else -1
                    self.x += self.vel_x
                    
                    # 飞行生物可以在垂直方向上移动，增加惯性
                    if self.can_fly:
                        self.vel_y = self.vel_y * 0.8 + dir_y * self.fly_speed * 0.7  # 增加惯性，减少突然变化
                        self.y += self.vel_y
        
        # 悬浮子弹碰撞检测：检查玩家是否触碰悬浮子弹
        if hasattr(self, 'floating_bullets') and self.mob_id == 吸血鬼:
            player_rect = pygame.Rect(player.坐标_x, player.坐标_y, player.宽, player.高)
            for bullet in self.floating_bullets[:]:
                bullet_rect = pygame.Rect(bullet['x'], bullet['y'], bullet['width'], bullet['height'])
                if player_rect.colliderect(bullet_rect):
                    # 玩家触碰悬浮子弹，造成伤害
                    player.take_damage(bullet['damage'], self)
                    # 移除被触碰的悬浮子弹
                    self.floating_bullets.remove(bullet)
        
        # 处理召唤的邪恶蝙蝠的行为
        if hasattr(self, 'summoned_bats') and self.mob_id == 吸血鬼:
            player_rect = pygame.Rect(player.坐标_x, player.坐标_y, player.宽, player.高)
            for bat in self.summoned_bats[:]:
                # 计算蝙蝠到玩家的距离和方向
                bat_dx = bat['target'].坐标_x - bat['x']
                bat_dy = bat['target'].坐标_y - bat['y']
                bat_dist = math.hypot(bat_dx, bat_dy)
                
                if bat_dist > 0:
                    # 向玩家移动
                    bat_dir_x = bat_dx / bat_dist
                    bat_dir_y = bat_dy / bat_dist
                    
                    # 更新蝙蝠位置
                    bat['x'] += bat_dir_x * bat['speed']
                    bat['y'] += bat_dir_y * bat['speed']
                
                # 检测蝙蝠是否攻击到玩家
                bat_rect = pygame.Rect(bat['x'], bat['y'], bat['width'], bat['height'])
                if bat_rect.colliderect(player_rect):
                    # 蝙蝠攻击玩家，造成伤害
                    player.take_damage(bat['damage'], self)
                    # 攻击后蝙蝠消失
                    self.summoned_bats.remove(bat)
        
        # 处理召唤的灵魂的行为（可被玩家击败）
        if hasattr(self, 'summoned_souls') and self.mob_id == 死神:
            # 检查玩家是否攻击了灵魂
            # 这里简化处理，直接检测玩家与灵魂的碰撞
            player_rect = pygame.Rect(player.坐标_x, player.坐标_y, player.宽, player.高)
            for soul in self.summoned_souls[:]:
                soul_rect = pygame.Rect(soul['x'], soul['y'], soul['width'], soul['height'])
                # 检测玩家是否击中灵魂
                if player_rect.colliderect(soul_rect):
                    # 玩家击中灵魂，灵魂死亡
                    self.summoned_souls.remove(soul)
                    print(f"玩家击败了灵魂！")
        
        # 验证是否在视野范围内
        if dist < self.sight_range * 32:  # 将格子数转换为像素
            # 牧羊人的特殊行为：远程投掷物攻击
            if self.mob_id == 牧羊人:
                # 离玩家3格（96像素）
                three_tiles = 3 * 32  # 3格 = 96像素
                
                if dist <= three_tiles:
                    # 3格内：移动近战玩家
                    if dist > self.attack_range:
                        # 向玩家移动
                        dir_x = dx / dist
                        dir_y = dy / dist
                        self.vel_x = dir_x * self.speed
                        self.direction = 1 if dir_x > 0 else -1
                        self.x += self.vel_x
                        
                        # 飞行生物可以在垂直方向上移动，增加惯性
                        if self.can_fly:
                            self.vel_y = self.vel_y * 0.8 + dir_y * self.fly_speed * 0.7  # 增加惯性，减少突然变化
                            self.y += self.vel_y
                    else:
                        # 在攻击范围内，停止移动并尝试攻击
                        self.vel_x = 0
                        if self.can_fly:
                            self.vel_y = 0
                        # 攻击玩家
                        self.attack(player)
                else:
                    # 3格外：不靠近玩家，只发射投掷物
                    # 停止移动
                    self.vel_x = 0
                    if self.can_fly:
                        self.vel_y = 0
                    
                    # 发射投掷物
                    self.projectile_timer += 1
                    if self.projectile_timer >= 60:  # 每1秒发射一次
                        self.projectile_timer = 0
                        
                        # 计算发射位置：从牧羊人的正面发射，而不是中心
                        # 根据牧羊人的朝向确定发射位置
                        if dx > 0:  # 玩家在右边，从正面发射
                            start_x = self.x + self.width
                            self.direction = 1
                        else:  # 玩家在左边，从正面发射
                            start_x = self.x
                            self.direction = -1
                        start_y = self.y + self.height // 2
                        
                        # 计算从发射位置到玩家的距离和方向
                        dx_proj = player.坐标_x - start_x
                        dy_proj = player.坐标_y - start_y
                        dist_proj = math.hypot(dx_proj, dy_proj)
                        
                        # 计算投掷物速度
                        projectile_speed = 300
                        vx = dx_proj / dist_proj * projectile_speed
                        vy = dy_proj / dist_proj * projectile_speed
                        
                        # 计算角度
                        angle = -math.degrees(math.atan2(vy, vx))
                        
                        # 加载10.png图片
                        projectile_image = "10投掷物"
                        
                        # 添加投掷物
                        self.projectiles.append({
                            'x': start_x,
                            'y': start_y,
                            'vx': vx,
                            'vy': vy,
                            'speed': projectile_speed,
                            'target': player,
                            'timer': 120,  # 2秒后消失
                            'image': projectile_image,
                            'width': 20,
                            'height': 20,
                            'angle': angle,
                            'damage': int(self.damage * 0.8)  # 投掷物伤害为近战的80%
                        })
            # 贝利亚的特殊行为：完整技能集
            elif self.mob_id == 贝利亚:
                # 初始化冲刺相关属性（如果不存在）
                if not hasattr(self, 'is_dashing'):
                    self.is_dashing = False
                if not hasattr(self, 'dash_timer'):
                    self.dash_timer = 0
                if not hasattr(self, 'dash_direction_x'):
                    self.dash_direction_x = 0
                if not hasattr(self, 'dash_direction_y'):
                    self.dash_direction_y = 0
                if not hasattr(self, 'dash_duration'):
                    self.dash_duration = 15  # 冲刺持续15帧（0.25秒）
                if not hasattr(self, 'dash_cooldown'):
                    self.dash_cooldown = 0
                if not hasattr(self, 'dash_cooldown_max'):
                    self.dash_cooldown_max = 120  # 冲刺冷却2秒
                
                # 更新冲刺冷却
                if self.dash_cooldown > 0:
                    self.dash_cooldown -= 1
                
                # 更新冲刺状态
                if self.is_dashing:
                    self.dash_timer -= 1
                    # 冲刺移动
                    self.x += self.dash_direction_x * 15
                    if self.can_fly:
                        self.y += self.dash_direction_y * 15
                    
                    # 冲刺结束
                    if self.dash_timer <= 0:
                        self.is_dashing = False
                        self.vel_x = 0
                        if self.can_fly:
                            self.vel_y = 0
                        self.last_skill = "冲刺"
                        # 恢复默认图片
                        self.current_image = self.default_image
                        self.skill_image_timer = self.skill_image_duration
                
                # 贝利亚作为BOSS生物，向玩家移动
                if not self.is_dashing:
                    if dist > self.attack_range:
                        # 向玩家移动
                        dir_x = dx / dist
                        dir_y = dy / dist
                        self.vel_x = dir_x * self.speed
                        self.direction = 1 if dir_x > 0 else -1
                        self.x += self.vel_x
                        
                        # 飞行生物可以在垂直方向上移动，增加惯性
                        if self.can_fly:
                            self.vel_y = self.vel_y * 0.8 + dir_y * self.fly_speed * 0.7  # 增加惯性，减少突然变化
                            self.y += self.vel_y
                    else:
                        # 在攻击范围内，停止移动并尝试攻击
                        self.vel_x = 0
                        if self.can_fly:
                            self.vel_y = 0
                        # 攻击玩家
                        self.attack(player)
                
                # 随机使用冲刺技能（频率适中）
                if not self.is_dashing and self.dash_cooldown <= 0:
                    if random.randint(1, 100) == 1:  # 约每1.67秒有1/100几率触发
                        self.is_dashing = True
                        self.dash_timer = self.dash_duration
                        self.dash_cooldown = self.dash_cooldown_max
                        
                        # 计算冲刺方向（向玩家方向）
                        if dist > 0:
                            self.dash_direction_x = dx / dist
                            self.dash_direction_y = dy / dist
                        else:
                            self.dash_direction_x = 1 if dx >= 0 else -1
                            self.dash_direction_y = 0
                        
                        # 更新技能追踪
                        self.last_skill = "冲刺"
                        # 切换到冲刺图片
                        self.current_image = "贝利亚_冲刺"
                        self.skill_image_timer = self.skill_image_duration
                        print(f"贝利亚使用冲刺 - 切换到图片: {self.current_image}")
                
                # 发射散弹技能
                self.projectile_timer += 1
                if self.projectile_timer >= 120:  # 每2秒发射一次
                    self.projectile_timer = 0
                    
                    # 更新last_skill属性
                    self.last_skill = "散弹攻击"
                    # 切换到远程攻击图片
                    self.current_image = "贝利亚_远程技能"
                    self.skill_image_timer = self.skill_image_duration
                    print(f"贝利亚使用散弹攻击 - 切换到图片: {self.current_image}")
                    
                    # 散弹参数：6发3次，间隔0.2秒
                    # 这里简化实现，一次发射18发，模拟6发3次的效果
                    shot_count = 18
                    
                    # 计算发射位置
                    start_x = self.x + self.width // 2
                    start_y = self.y + self.height // 2
                    
                    # 加载2.png图片
                    projectile_image = "2投掷物"
                    
                    # 发射散弹
                    for i in range(shot_count):
                        # 计算随机角度偏移，形成散弹效果
                        angle_offset = random.uniform(-math.pi/6, math.pi/6)  # ±30度范围
                        
                        # 计算方向
                        dir_x = math.cos(math.atan2(dy, dx) + angle_offset)
                        dir_y = math.sin(math.atan2(dy, dx) + angle_offset)
                        
                        # 计算投掷物速度（提高300%）
                        projectile_speed = 600  # 150 * 4 = 600，提高300%
                        vx = dir_x * projectile_speed
                        vy = dir_y * projectile_speed
                        
                        # 计算角度
                        angle = -math.degrees(math.atan2(vy, vx))
                        
                        # 添加投掷物
                        self.projectiles.append({
                            'x': start_x,
                            'y': start_y,
                            'vx': vx,
                            'vy': vy,
                            'speed': projectile_speed,
                            'target': player,
                            'timer': 120,  # 2秒后消失
                            'image': projectile_image,
                            'width': 15,
                            'height': 15,
                            'angle': angle,
                            'damage': 18  # 固定伤害18
                        })
                
                # 新技能：发射激光攻击
                # 初始化激光计时器（如果不存在）
                if not hasattr(self, 'laser_timer'):
                    self.laser_timer = 0
                
                self.laser_timer += 1
                if self.laser_timer >= 240:  # 每4秒发射一次
                    self.laser_timer = 0
                    
                    # 更新last_skill属性
                    self.last_skill = "激光攻击"
                    # 切换到激光攻击图片
                    self.current_image = "贝利亚_激光"
                    self.skill_image_timer = self.skill_image_duration
                    print(f"贝利亚使用激光攻击 - 切换到图片: {self.current_image}")
                    
                    # 计算发射位置
                    laser_start_x = self.x + self.width // 2
                    laser_start_y = self.y + self.height // 2
                    
                    # 计算激光方向（直接向玩家发射）
                    base_laser_dir_x = dx / dist if dist > 0 else 1
                    base_laser_dir_y = dy / dist if dist > 0 else 0
                    
                    # 进一步增强激光速度（更快，接近瞬间命中）
                    laser_speed = 3000  # 速度再提高200%，总计6倍于初始值
                    
                    # 发射多束激光，形成扇形攻击，确保击中玩家
                    laser_count = 8  # 发射8束激光
                    angle_range = math.pi / 4  # ±45度范围
                    
                    for i in range(laser_count):
                        # 计算每束激光的角度偏移
                        angle_offset = (i - laser_count // 2) * (angle_range / laser_count)
                        base_angle = math.atan2(base_laser_dir_y, base_laser_dir_x)
                        laser_angle = base_angle + angle_offset
                        
                        # 计算每束激光的方向
                        laser_dir_x = math.cos(laser_angle)
                        laser_dir_y = math.sin(laser_angle)
                        
                        # 添加激光投掷物，记录起始位置以便绘制完整激光束
                        self.projectiles.append({
                            'x': laser_start_x,
                            'y': laser_start_y,
                            'start_x': laser_start_x,  # 记录起始X位置
                            'start_y': laser_start_y,  # 记录起始Y位置
                            'vx': laser_dir_x * laser_speed,
                            'vy': laser_dir_y * laser_speed,
                            'speed': laser_speed,
                            'target': player,
                            'timer': 18,  # 0.3秒后消失，距离增加2倍
                            'image': "2投掷物",  # 使用现有投掷物图片，后续可替换为激光图片
                            'width': 20,
                            'height': 50,
                            'angle': -math.degrees(laser_angle),
                            'damage': 15,  # 每束激光伤害
                            'type': 'laser'  # 标记为激光类型
                        })
                
                # 新技能：追踪子弹
                # 初始化追踪子弹计时器（如果不存在）
                if not hasattr(self, 'homing_bullet_timer'):
                    self.homing_bullet_timer = 0
                
                self.homing_bullet_timer += 1
                if self.homing_bullet_timer >= 300:  # 每5秒发射一次
                    self.homing_bullet_timer = 0
                    
                    # 更新last_skill属性
                    self.last_skill = "追踪子弹"
                    # 切换到远程攻击图片
                    self.current_image = "贝利亚_远程技能"
                    self.skill_image_timer = self.skill_image_duration
                    print(f"贝利亚使用追踪子弹 - 切换到图片: {self.current_image}")
                    
                    # 计算发射位置
                    bullet_start_x = self.x + self.width // 2
                    bullet_start_y = self.y + self.height // 2
                    
                    # 发射20发追踪子弹
                    bullet_count = 20  # 发射20发子弹
                    bullet_speed = 250  # 子弹速度，增加25%
                    
                    for i in range(bullet_count):
                        # 计算随机初始方向
                        random_angle = random.uniform(0, 2 * math.pi)
                        dir_x = math.cos(random_angle)
                        dir_y = math.sin(random_angle)
                        
                        # 添加追踪子弹投掷物
                        self.projectiles.append({
                            'x': bullet_start_x,
                            'y': bullet_start_y,
                            'start_x': bullet_start_x,  # 记录起始X位置
                            'start_y': bullet_start_y,  # 记录起始Y位置
                            'vx': dir_x * bullet_speed,
                            'vy': dir_y * bullet_speed,
                            'speed': bullet_speed,
                            'target': player,
                            'timer': 630,  # 10.5秒后消失（增加250%）
                            'image': "2投掷物",  # 使用现有投掷物图片
                            'width': 15,
                            'height': 15,
                            'angle': -math.degrees(random_angle),
                            'damage': 12,  # 每发子弹伤害
                            'type': 'homing_bullet',  # 标记为追踪子弹类型
                            'homing_speed': 15,  # 提高追踪加速度，让追踪更明显
                            'homing_delay': 60  # 1秒后开始追踪（60帧）
                        })
                
                # 新技能：360°旋转子弹
                # 初始化旋转子弹计时器和发射计数
                if not hasattr(self, 'rotating_bullet_timer'):
                    self.rotating_bullet_timer = 0
                if not hasattr(self, 'rotating_bullet_wave'):
                    self.rotating_bullet_wave = 0
                if not hasattr(self, 'rotating_bullet_cooldown'):
                    self.rotating_bullet_cooldown = 0
                
                self.rotating_bullet_timer += 1
                
                # 主技能冷却，每8秒触发一次
                if self.rotating_bullet_timer >= 480:
                    self.rotating_bullet_timer = 0
                    self.rotating_bullet_wave = 0
                    
                    # 更新技能追踪
                    self.last_skill = "360°旋转子弹"
                    # 切换到技能1图片
                    self.current_image = "贝利亚_技能1"
                    self.skill_image_timer = self.skill_image_duration
                    print(f"贝利亚使用360°旋转子弹 - 切换到图片: {self.current_image}")
                    
                    # 计算发射位置
                    bullet_start_x = self.x + self.width // 2
                    bullet_start_y = self.y + self.height // 2
                    
                    # 计算向玩家方向的移动分量
                    if dist > 0:
                        player_dir_x = dx / dist
                        player_dir_y = dy / dist
                    else:
                        player_dir_x = 0
                        player_dir_y = 0
                    
                    # 3次合计发射36发子弹，分3组，每组12发
                    total_groups = 3
                    bullets_per_group = 12
                    bullet_speed = 300
                    player_move_speed = 800  # 向玩家方向移动的速度（增加300%）
                    
                    for group in range(total_groups):
                        for i in range(bullets_per_group):
                            # 计算360°方向
                            angle = 2 * math.pi * i / bullets_per_group
                            
                            # 根据组号设置旋转方向
                            # 组1和组3正旋转，组2负旋转
                            if group == 1:
                                rotation_dir = -0.1  # 负旋转
                            else:
                                rotation_dir = 0.1  # 正旋转
                            
                            # 计算初始旋转方向
                            rot_dir_x = math.cos(angle)
                            rot_dir_y = math.sin(angle)
                            
                            # 计算最终速度：旋转速度 + 向玩家方向移动的速度
                            final_vx = rot_dir_x * bullet_speed + player_dir_x * player_move_speed
                            final_vy = rot_dir_y * bullet_speed + player_dir_y * player_move_speed
                            
                            # 计算最终速度大小
                            final_speed = math.hypot(final_vx, final_vy)
                            
                            # 添加旋转子弹投掷物
                            self.projectiles.append({
                                'x': bullet_start_x,
                                'y': bullet_start_y,
                                'vx': final_vx,
                                'vy': final_vy,
                                'speed': final_speed,
                                'target': player,
                                'timer': 240,  # 4秒后消失
                                'image': "2投掷物",  # 使用现有投掷物图片
                                'width': 15,
                                'height': 15,
                                'angle': -math.degrees(angle),
                                'damage': 15,  # 每发子弹伤害
                                'type': 'rotating_bullet',  # 标记为旋转子弹类型
                                'rotation_angle': angle,
                                'rotation_dir': rotation_dir,
                                'rotation_speed': 0.1,  # 旋转速度
                                'player_dir_x': player_dir_x,  # 向玩家方向的X分量
                                'player_dir_y': player_dir_y,  # 向玩家方向的Y分量
                                'player_move_speed': player_move_speed  # 向玩家方向移动的速度
                            })
                
                # 新技能：360°直线黑色子弹
                # 初始化360°子弹计时器和发射计数
                if not hasattr(self, 'circle_bullet_timer'):
                    self.circle_bullet_timer = 0
                if not hasattr(self, 'circle_bullet_wave'):
                    self.circle_bullet_wave = 0
                if not hasattr(self, 'circle_bullet_cooldown'):
                    self.circle_bullet_cooldown = 0
                
                self.circle_bullet_timer += 1
                
                # 主技能冷却，每6秒触发一次
                if self.circle_bullet_timer >= 360 and self.circle_bullet_wave == 0:
                    self.circle_bullet_timer = 0
            # 异变骷髅的特殊行为：和牧羊人一样，有近战和远程攻击
            elif self.mob_id == 异变骷髅:
                # 离玩家3格（96像素）
                three_tiles = 3 * 32  # 3格 = 96像素
                
                if dist <= three_tiles:
                    # 3格内：移动近战玩家
                    if dist > self.attack_range:
                        # 向玩家移动
                        dir_x = dx / dist
                        dir_y = dy / dist
                        self.vel_x = dir_x * self.speed
                        self.direction = 1 if dir_x > 0 else -1
                        self.x += self.vel_x
                        
                        # 飞行生物可以在垂直方向上移动，增加惯性
                        if self.can_fly:
                            self.vel_y = self.vel_y * 0.8 + dir_y * self.fly_speed * 0.7  # 增加惯性，减少突然变化
                            self.y += self.vel_y
                    else:
                        # 在攻击范围内，停止移动并尝试攻击
                        self.vel_x = 0
                        if self.can_fly:
                            self.vel_y = 0
                        # 攻击玩家
                        self.attack(player)
                else:
                    # 3格外：不靠近玩家，只发射投掷物
                    # 停止移动
                    self.vel_x = 0
                    if self.can_fly:
                        self.vel_y = 0
                    
                    # 发射投掷物
                    self.projectile_timer += 1
                    if self.projectile_timer >= 60:  # 每1秒发射一次
                        self.projectile_timer = 0
                        
                        # 计算发射位置：从异变骷髅的正面发射，而不是中心
                        # 根据异变骷髅的朝向确定发射位置
                        if dx > 0:  # 玩家在右边，从正面发射
                            start_x = self.x + self.width
                            self.direction = 1
                        else:  # 玩家在左边，从正面发射
                            start_x = self.x
                            self.direction = -1
                        start_y = self.y + self.height // 2
                        
                        # 计算从发射位置到玩家的距离和方向
                        dx_proj = player.坐标_x - start_x
                        dy_proj = player.坐标_y - start_y
                        dist_proj = math.hypot(dx_proj, dy_proj)
                        
                        if dist_proj > 0:
                            # 计算投掷物速度
                            projectile_speed = 300
                            vx = dx_proj / dist_proj * projectile_speed
                            vy = dy_proj / dist_proj * projectile_speed
                            
                            # 计算角度
                            angle = -math.degrees(math.atan2(vy, vx))
                            
                            # 加载bone类型子弹，和吸血鬼召唤的异变骷髅一样
                            # 添加投掷物（子弹绘制为骨头，和吸血鬼召唤的异变骷髅一样）
                            self.projectiles.append({
                                'x': start_x,
                                'y': start_y,
                                'vx': vx,
                                'vy': vy,
                                'speed': projectile_speed * 0.7,  # 稍微减慢速度
                                'target': player,
                                'timer': 180,  # 3秒后消失
                                'type': 'bone',  # 设置为骨头类型
                                'width': 20,  # 骨头宽度
                                'height': 10,  # 骨头高度
                                'angle': angle,
                                'damage': int(self.damage * 0.8)  # 投掷物伤害为近战的80%
                            })
            
            # 刺球的特殊行为：触碰玩家爆炸
            elif self.mob_id == 刺球:
                # 向玩家移动
                if dist > self.attack_range:
                    # 计算移动方向
                    dir_x = dx / dist
                    dir_y = dy / dist
                    self.vel_x = dir_x * self.speed
                    self.direction = 1 if dir_x > 0 else -1
                    self.x += self.vel_x
                    
                    # 飞行生物可以在垂直方向上移动，增加惯性
                    if self.can_fly:
                        self.vel_y = self.vel_y * 0.8 + dir_y * self.fly_speed * 0.7  # 增加惯性，减少突然变化
                        self.y += self.vel_y
                else:
                    # 在攻击范围内，停止移动
                    self.vel_x = 0
                    if self.can_fly:
                        self.vel_y = 0
                
                # 检查是否触碰玩家（矩形碰撞检测）
                player_rect = pygame.Rect(player.坐标_x, player.坐标_y, player.宽, player.高)
                mob_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                
                if mob_rect.colliderect(player_rect):
                    # 造成20点伤害
                    player.take_damage(20, self)
                    # 创建爆炸特效
                    if hasattr(self, 'game') and self.game:
                        # 使用游戏的全局爆炸特效系统
                        class ExplosionEffect:
                            def __init__(self, x, y, radius, max_radius, color, duration=0.25):
                                self.x = x
                                self.y = y
                                self.radius = radius
                                self.max_radius = max_radius
                                self.color = color
                                self.duration = duration
                                self.lifetime = duration
                            
                            def update(self, dt):
                                self.lifetime -= dt
                                if self.lifetime <= 0:
                                    return True
                                # 更新半径
                                progress = 1 - (self.lifetime / self.duration)
                                self.radius = self.max_radius * progress
                                return False
                            
                            def draw(self, screen, camera_x, camera_y):
                                # 计算透明度：先从透明到不透明，再到透明
                                progress = 1 - (self.lifetime / self.duration)
                                if progress < 0.5:
                                    alpha = int(255 * progress * 2)
                                else:
                                    alpha = int(255 * (1 - (progress - 0.5) * 2))
                                
                                # 绘制爆炸特效
                                screen_x = self.x - camera_x
                                screen_y = self.y - camera_y
                                color_with_alpha = (*self.color, alpha)
                                
                                # 创建带透明度的表面
                                explosion_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
                                # 绘制爆炸圆环
                                pygame.draw.circle(explosion_surface, color_with_alpha, (self.radius, self.radius), self.radius, 5)
                                # 绘制爆炸中心
                                pygame.draw.circle(explosion_surface, color_with_alpha, (self.radius, self.radius), self.radius // 3)
                                
                                screen.blit(explosion_surface, (screen_x - self.radius, screen_y - self.radius))
                        
                        # 添加到游戏的全局爆炸特效列表
                        explosion = ExplosionEffect(
                            self.x,
                            self.y,
                            0,
                            60,
                            (255, 0, 0),
                            0.25
                        )
                        
                        if not hasattr(self.game, 'explosion_effects'):
                            self.game.explosion_effects = []
                        self.game.explosion_effects.append(explosion)
                    else:
                        # 回退方案：使用自身的spike_explosions
                        if hasattr(self, 'spike_explosions'):
                            self.spike_explosions.append({
                                'x': self.x,
                                'y': self.y,
                                'radius': 0,
                                'max_radius': 60,
                                'timer': 15,  # 0.25秒爆炸效果
                                'color': (255, 0, 0)
                            })
                        else:
                            self.spike_explosions = [{
                                'x': self.x,
                                'y': self.y,
                                'radius': 0,
                                'max_radius': 60,
                                'timer': 15,
                                'color': (255, 0, 0)
                            }]
                    # 标记为死亡，会被移除
                    # 通过返回True表示死亡，在调用处处理
                    self.health = 0  # 设置生命值为0，确保死亡
            
            # 吸血鬼的特殊行为：冲刺、近战攻击和跟踪子弹
            elif self.mob_id == 吸血鬼:
                # 吸血鬼作为BOSS生物，向玩家移动
                if dist > self.attack_range:
                    # 向玩家移动
                    dir_x = dx / dist
                    dir_y = dy / dist
                    self.vel_x = dir_x * self.speed
                    self.direction = 1 if dir_x > 0 else -1
                    self.x += self.vel_x
                    
                    # 飞行生物可以在垂直方向上移动，增加惯性
                    if self.can_fly:
                        self.vel_y = self.vel_y * 0.8 + dir_y * self.fly_speed * 0.7  # 增加惯性，减少突然变化
                        self.y += self.vel_y
                else:
                    # 在攻击范围内，停止移动并尝试攻击
                    self.vel_x = 0
                    if self.can_fly:
                        self.vel_y = 0
                    # 攻击玩家
                    self.attack(player)
                
                # 初始化冲刺相关属性（如果不存在）
                if not hasattr(self, 'is_dashing'):
                    self.is_dashing = False
                if not hasattr(self, 'dash_timer'):
                    self.dash_timer = 0
                if not hasattr(self, 'dash_direction_x'):
                    self.dash_direction_x = 0
                if not hasattr(self, 'dash_direction_y'):
                    self.dash_direction_y = 0
                if not hasattr(self, 'dash_duration'):
                    self.dash_duration = 15  # 冲刺持续15帧（0.25秒）
                if not hasattr(self, 'dash_cooldown'):
                    self.dash_cooldown = 0
                if not hasattr(self, 'dash_cooldown_max'):
                    self.dash_cooldown_max = 120  # 冲刺冷却2秒
                
                # 初始化跟踪子弹相关属性（如果不存在）
                if not hasattr(self, 'tracking_bullet_timer'):
                    self.tracking_bullet_timer = 0
                if not hasattr(self, 'tracking_bullet_cooldown'):
                    self.tracking_bullet_cooldown = 0
                if not hasattr(self, 'tracking_bullet_cooldown_max'):
                    self.tracking_bullet_cooldown_max = 180  # 跟踪子弹冷却3秒
                
                # 初始化悬浮子弹相关属性（如果不存在）
                if not hasattr(self, 'floating_bullet_timer'):
                    self.floating_bullet_timer = 0
                if not hasattr(self, 'floating_bullet_cooldown'):
                    self.floating_bullet_cooldown = 0
                if not hasattr(self, 'floating_bullet_cooldown_max'):
                    self.floating_bullet_cooldown_max = 600  # 悬浮子弹冷却10秒
                if not hasattr(self, 'floating_bullets'):
                    self.floating_bullets = []  # 存储当前活跃的悬浮子弹
                if not hasattr(self, 'floating_bullet_duration'):
                    self.floating_bullet_duration = 300  # 悬浮子弹持续5秒
                
                # 初始化狂暴状态相关属性（如果不存在）
                if not hasattr(self, 'rage_mode'):
                    self.rage_mode = False  # 是否处于狂暴状态
                if not hasattr(self, 'rage_duration'):
                    self.rage_duration = 300  # 狂暴状态持续5秒（300帧）
                if not hasattr(self, 'rage_timer'):
                    self.rage_timer = 0  # 狂暴状态计时器
                if not hasattr(self, 'rage_cooldown'):
                    self.rage_cooldown = 0  # 狂暴状态冷却计时器
                if not hasattr(self, 'rage_cooldown_max'):
                    self.rage_cooldown_max = 1080  # 狂暴状态冷却18秒（1080帧）
                if not hasattr(self, 'base_damage'):
                    self.base_damage = self.damage  # 保存基础伤害值
                if not hasattr(self, 'rage_damage_boost'):
                    self.rage_damage_boost = 0  # 当前狂暴伤害加成
                
                # 初始化临时护盾相关属性（如果不存在）
                if not hasattr(self, 'shield_value'):
                    self.shield_value = 0  # 当前护盾值
                if not hasattr(self, 'shield_max'):
                    self.shield_max = 100  # 护盾上限
                if not hasattr(self, 'shield_cooldown'):
                    self.shield_cooldown = 0  # 护盾冷却计时器
                if not hasattr(self, 'shield_cooldown_max'):
                    self.shield_cooldown_max = 1500  # 护盾冷却25秒（1500帧）
                if not hasattr(self, 'shield_timer'):
                    self.shield_timer = 0  # 护盾持续计时器
                
                # 初始化召唤邪恶蝙蝠技能相关属性（如果不存在）
                if not hasattr(self, 'summon_bat_cooldown'):
                    self.summon_bat_cooldown = 0  # 召唤蝙蝠冷却计时器
                if not hasattr(self, 'summon_bat_cooldown_max'):
                    self.summon_bat_cooldown_max = 600  # 召唤蝙蝠冷却10秒（600帧）
                if not hasattr(self, 'summoned_bats'):
                    self.summoned_bats = []  # 存储当前召唤的蝙蝠
                
                # 初始化吸血蝙蝠技能相关属性（如果不存在）
                if not hasattr(self, 'healing_bat_cooldown'):
                    self.healing_bat_cooldown = 0  # 吸血蝙蝠冷却计时器
                if not hasattr(self, 'healing_bat_cooldown_max'):
                    self.healing_bat_cooldown_max = 900  # 吸血蝙蝠冷却15秒（900帧）
                if not hasattr(self, 'healing_bats'):
                    self.healing_bats = []  # 存储当前召唤的吸血蝙蝠
                
                # 初始化刺球召唤技能相关属性（如果不存在）
                if not hasattr(self, 'spike_ball_cooldown'):
                    self.spike_ball_cooldown = 0  # 刺球召唤冷却计时器
                if not hasattr(self, 'spike_ball_cooldown_max'):
                    self.spike_ball_cooldown_max = 720  # 刺球召唤冷却12秒（720帧）
                if not hasattr(self, 'spike_balls'):
                    self.spike_balls = []  # 存储当前召唤的刺球
                if not hasattr(self, 'spike_explosions'):
                    self.spike_explosions = []  # 存储刺球爆炸特效
                
                # 初始化异变骷髅召唤技能相关属性（如果不存在）
                if not hasattr(self, 'mutant_skull_cooldown'):
                    self.mutant_skull_cooldown = 0  # 异变骷髅召唤冷却计时器
                if not hasattr(self, 'mutant_skull_cooldown_max'):
                    self.mutant_skull_cooldown_max = 900  # 异变骷髅召唤冷却15秒（900帧）
                if not hasattr(self, 'mutant_skulls'):
                    self.mutant_skulls = []  # 存储当前召唤的异变骷髅
                if not hasattr(self, 'mutant_skull_projectiles'):
                    self.mutant_skull_projectiles = []  # 存储异变骷髅发射的投掷物
                
                # 更新冲刺冷却
                if self.dash_cooldown > 0:
                    self.dash_cooldown -= 1
                
                # 更新跟踪子弹冷却
                if self.tracking_bullet_cooldown > 0:
                    self.tracking_bullet_cooldown -= 1
                
                # 更新悬浮子弹冷却
                if self.floating_bullet_cooldown > 0:
                    self.floating_bullet_cooldown -= 1
                
                # 更新悬浮子弹持续时间
                for bullet in self.floating_bullets[:]:
                    bullet['timer'] -= 1
                    if bullet['timer'] <= 0:
                        self.floating_bullets.remove(bullet)
                
                # 更新狂暴状态冷却
                if self.rage_cooldown > 0:
                    self.rage_cooldown -= 1
                
                # 更新狂暴状态持续时间
                if self.rage_mode:
                    self.rage_timer -= 1
                    if self.rage_timer <= 0:
                        # 狂暴状态结束，恢复基础伤害
                        self.rage_mode = False
                        self.damage = self.base_damage
                        self.rage_damage_boost = 0
                
                # 更新临时护盾冷却
                if self.shield_cooldown > 0:
                    self.shield_cooldown -= 1
                
                # 更新召唤蝙蝠冷却
                if self.summon_bat_cooldown > 0:
                    self.summon_bat_cooldown -= 1
                
                # 更新召唤蝙蝠的持续时间
                for bat in self.summoned_bats[:]:
                    bat['timer'] -= 1
                    if bat['timer'] <= 0:
                        # 蝙蝠10秒后消失
                        self.summoned_bats.remove(bat)
                
                # 更新吸血蝙蝠冷却
                if self.healing_bat_cooldown > 0:
                    self.healing_bat_cooldown -= 1
                
                # 更新吸血蝙蝠的行为
                for bat in self.healing_bats[:]:
                    # 向Boss（吸血鬼自己）飞行
                    dx = self.x - bat['x']
                    dy = self.y - bat['y']
                    dist = math.hypot(dx, dy)
                    
                    if dist > 5:  # 如果距离大于5像素，继续移动
                        dir_x = dx / dist
                        dir_y = dy / dist
                        # 吸血蝙蝠移动速度更快
                        bat['x'] += dir_x * bat['speed']
                        bat['y'] += dir_y * bat['speed']
                    else:  # 触碰Boss，回复血量
                        # 切换到享受图片
                        self.current_image = "吸血鬼_享受"
                        self.skill_image_timer = self.skill_image_duration
                        print(f"吸血鬼被吸血蝙蝠击中 - 切换到图片: {self.current_image}")
                        
                        # 回复1%的最大生命值
                        heal_amount = self.max_health * 0.01
                        self.health = min(self.health + heal_amount, self.max_health)
                        # 移除蝙蝠
                        self.healing_bats.remove(bat)
                    
                    # 蝙蝠存活时间限制
                    bat['timer'] -= 1
                    if bat['timer'] <= 0:
                        self.healing_bats.remove(bat)
                
                # 更新刺球召唤冷却
                if self.spike_ball_cooldown > 0:
                    self.spike_ball_cooldown -= 1
                
                # 更新刺球的行为
                player_rect = pygame.Rect(player.坐标_x, player.坐标_y, player.宽, player.高)
                for ball in self.spike_balls[:]:
                    # 向玩家冲刺
                    dx = player.坐标_x - ball['x']
                    dy = player.坐标_y - ball['y']
                    dist = math.hypot(dx, dy)
                    
                    if dist > 10:  # 如果距离大于10像素，继续移动
                        dir_x = dx / dist
                        dir_y = dy / dist
                        # 刺球冲刺速度
                        ball['x'] += dir_x * ball['speed']
                        ball['y'] += dir_y * ball['speed']
                        # 旋转效果
                        ball['rotation'] += 10
                    else:  # 触碰玩家，爆炸造成伤害
                        # 造成20点伤害
                        player.take_damage(20, self)
                        # 创建爆炸特效
                        self.spike_explosions.append({
                            'x': ball['x'],
                            'y': ball['y'],
                            'radius': 0,
                            'max_radius': 60,
                            'timer': 15,  # 0.25秒爆炸效果
                            'color': (255, 0, 0)
                        })
                        # 移除刺球
                        self.spike_balls.remove(ball)
                        continue
                    
                    # 检查刺球与玩家的碰撞（矩形碰撞，用于检测快速移动的刺球）
                    ball_rect = pygame.Rect(ball['x'], ball['y'], ball['width'], ball['height'])
                    if ball_rect.colliderect(player_rect):
                        # 造成20点伤害
                        player.take_damage(20, self)
                        # 创建爆炸特效
                        self.spike_explosions.append({
                            'x': ball['x'],
                            'y': ball['y'],
                            'radius': 0,
                            'max_radius': 60,
                            'timer': 15,  # 0.25秒爆炸效果
                            'color': (255, 0, 0)
                        })
                        # 移除刺球
                        self.spike_balls.remove(ball)
                        continue
                    
                    # 刺球存活时间限制
                    ball['timer'] -= 1
                    if ball['timer'] <= 0:
                        # 超时爆炸
                        self.spike_explosions.append({
                            'x': ball['x'],
                            'y': ball['y'],
                            'radius': 0,
                            'max_radius': 40,
                            'timer': 15,
                            'color': (255, 100, 0)
                        })
                        self.spike_balls.remove(ball)
                

                
                # 更新异变骷髅冷却
                if self.mutant_skull_cooldown > 0:
                    self.mutant_skull_cooldown -= 1
                
                # 更新异变骷髅的行为
                player_rect = pygame.Rect(player.坐标_x, player.坐标_y, player.宽, player.高)
                for skull in self.mutant_skulls[:]:
                    # 微移动
                    skull['move_timer'] += 1
                    if skull['move_timer'] >= 60:  # 每秒改变一次移动方向
                        skull['move_timer'] = 0
                        skull['move_dir_x'] = random.choice([-0.5, 0, 0.5])
                        skull['move_dir_y'] = random.choice([-0.5, 0, 0.5])
                    
                    # 应用微移动
                    skull['x'] += skull['move_dir_x']
                    skull['y'] += skull['move_dir_y']
                    
                    # 发射投掷物
                    skull['projectile_timer'] += 1
                    if skull['projectile_timer'] >= 60:  # 每1秒发射一次投掷物，提高频率使效果更明显
                        skull['projectile_timer'] = 0
                        # 计算向玩家的方向
                        dx = player.坐标_x - skull['x']
                        dy = player.坐标_y - skull['y']
                        dist = math.hypot(dx, dy)
                        if dist > 0:
                            dir_x = dx / dist
                            dir_y = dy / dist
                            # 添加投掷物
                            # 将子弹添加到统一的projectiles列表中
                            self.projectiles.append({
                                'x': skull['x'] + skull['width'] // 2,
                                'y': skull['y'] + skull['height'] // 2,
                                'vx': dir_x * 120.0,  # 提高速度到合理值
                                'vy': dir_y * 120.0,
                                'width': 18,  # 进一步增大尺寸
                                'height': 18,
                                'timer': 120,  # 2秒后消失
                                'damage': 15,
                                'target': player,
                                'type': 'bone'  # 设置为骨头类型，统一绘制
                            })
                    
                    # 异变骷髅存活时间限制
                    skull['timer'] -= 1
                    if skull['timer'] <= 0:
                        self.mutant_skulls.remove(skull)
                

                
                # 更新冲刺状态
                if self.is_dashing:
                    self.dash_timer -= 1
                    # 冲刺移动
                    self.x += self.dash_direction_x * 15
                    if self.can_fly:
                        self.y += self.dash_direction_y * 15
                    
                    # 冲刺结束
                    if self.dash_timer <= 0:
                        self.is_dashing = False
                        self.vel_x = 0
                        if self.can_fly:
                            self.vel_y = 0
                        self.last_skill = "冲刺"
                
                # 随机使用冲刺技能（频率适中）
                if not self.is_dashing and self.dash_cooldown <= 0:
                    if random.randint(1, 100) == 1:  # 约每1.67秒有1/100几率触发，频率降低
                        self.is_dashing = True
                        self.dash_timer = self.dash_duration
                        self.dash_cooldown = self.dash_cooldown_max
                        
                        # 切换到冲刺图片
                        self.current_image = "吸血鬼_冲刺"
                        self.skill_image_timer = self.skill_image_duration
                        print(f"吸血鬼使用冲刺 - 切换到图片: {self.current_image}")
                        
                        # 计算冲刺方向（向玩家方向）
                        if dist > 0:
                            self.dash_direction_x = dx / dist
                            self.dash_direction_y = dy / dist
                        else:
                            self.dash_direction_x = random.choice([-1, 1])
                            self.dash_direction_y = random.choice([-1, 1])
                        
                        # 应用冲刺速度
                        self.vel_x = self.dash_direction_x * 15
                        if self.can_fly:
                            self.vel_y = self.dash_direction_y * 15
                
                # 使用跟踪子弹技能（约每0.5秒一次）
                if self.tracking_bullet_cooldown <= 0:
                    if random.randint(1, 30) == 1:  # 约每0.5秒有1/30几率触发，频率提高
                        # 更新last_skill属性
                        self.last_skill = "跟踪子弹"
                        
                        # 切换到远程技能图片
                        self.current_image = "吸血鬼_远程技能"
                        self.skill_image_timer = self.skill_image_duration
                        print(f"吸血鬼使用跟踪子弹 - 切换到图片: {self.current_image}")
                        
                        # 计算发射位置
                        start_x = self.x + self.width // 2
                        start_y = self.y + self.height // 2
                        
                        # 发射3发紫色跟踪子弹
                        bullet_count = 3
                        bullet_speed = 1000  # 子弹速度进一步提高，达到初始值的5倍
                        
                        for i in range(bullet_count):
                            # 计算初始方向（略微分散）
                            angle_offset = (i - bullet_count // 2) * (math.pi / 12)  # 30度范围分散
                            bullet_angle = math.atan2(dy, dx) + angle_offset
                            dir_x = math.cos(bullet_angle)
                            dir_y = math.sin(bullet_angle)
                            
                            # 添加紫色跟踪子弹投掷物
                            self.projectiles.append({
                                'x': start_x,
                                'y': start_y,
                                'vx': dir_x * bullet_speed,
                                'vy': dir_y * bullet_speed,
                                'speed': bullet_speed,
                                'target': player,
                                'timer': 630,  # 10.5秒后消失（增加250%）
                                'image': "2投掷物",  # 使用现有投掷物图片
                                'width': 15,
                                'height': 15,
                                'angle': -math.degrees(bullet_angle),
                                'damage': 15,  # 每发子弹伤害
                                'type': 'homing_bullet',  # 标记为追踪子弹类型
                                'homing_speed': 15,  # 提高追踪加速度
                                'color': (150, 50, 200)  # 紫色子弹颜色
                            })
                        
                        # 设置冷却时间
                        self.tracking_bullet_cooldown = self.tracking_bullet_cooldown_max
                
                # 使用悬浮子弹技能（约每10秒一次）
                if self.floating_bullet_cooldown <= 0:
                    if random.randint(1, 600) == 1:  # 约每10秒有1/600几率触发
                        # 更新last_skill属性
                        self.last_skill = "悬浮子弹"
                        
                        # 切换到远程技能图片
                        self.current_image = "吸血鬼_远程技能"
                        self.skill_image_timer = self.skill_image_duration
                        print(f"吸血鬼使用悬浮子弹 - 切换到图片: {self.current_image}")
                        
                        # 清空现有悬浮子弹
                        self.floating_bullets.clear()
                        
                        # 在吸血鬼周围随机生成50-100个不动子弹
                        bullet_count = random.randint(50, 100)
                        for i in range(bullet_count):
                            # 随机位置：以吸血鬼为中心，半径100-300像素的范围内
                            radius = random.randint(100, 300)
                            angle = random.uniform(0, 2 * math.pi)
                            bullet_x = self.x + self.width // 2 + math.cos(angle) * radius
                            bullet_y = self.y + self.height // 2 + math.sin(angle) * radius
                            
                            # 添加悬浮子弹
                            self.floating_bullets.append({
                                'x': bullet_x,
                                'y': bullet_y,
                                'width': 10,
                                'height': 10,
                                'damage': 8,  # 触碰伤害
                                'timer': self.floating_bullet_duration,  # 持续时间
                                'color': (150, 50, 200)  # 紫色子弹
                            })
                        
                        # 设置冷却时间
                        self.floating_bullet_cooldown = self.floating_bullet_cooldown_max
                
                # 使用狂暴状态技能（约每4秒一次，频率提高350%）
                if not self.rage_mode and self.rage_cooldown <= 0:
                    if random.randint(1, 240) == 1:  # 约每4秒有1/240几率触发
                        # 更新last_skill属性
                        self.last_skill = "狂暴状态"
                        
                        # 切换到狂暴图片
                        self.current_image = "吸血鬼_狂暴"
                        self.skill_image_timer = self.rage_duration  # 狂暴状态持续期间保持图片
                        print(f"吸血鬼进入狂暴状态 - 切换到图片: {self.current_image}")
                        
                        # 计算狂暴伤害加成：10% + (总生命值% - 剩余生命值%) / 5
                        total_health_pct = 100  # 总生命值百分比
                        remaining_health_pct = (self.health / self.max_health) * 100  # 剩余生命值百分比
                        health_diff = total_health_pct - remaining_health_pct  # 生命值差值百分比
                        self.rage_damage_boost = 0.10 + (health_diff / 2) * 0.01  # 转换为小数，分母从5改为2
                        
                        # 应用伤害加成
                        self.damage = int(self.base_damage * (1 + self.rage_damage_boost))
                        
                        # 进入狂暴状态
                        self.rage_mode = True
                        self.rage_timer = self.rage_duration
                        
                        # 设置冷却时间（提高350%频率）
                        self.rage_cooldown = 240  # 4秒冷却
                
                # 使用临时护盾技能（约每5.56秒一次，频率提高350%）
                if self.shield_cooldown <= 0:
                    if random.randint(1, 333) == 1:  # 约每5.56秒有1/333几率触发
                        # 更新last_skill属性
                        self.last_skill = "临时护盾"
                        
                        # 增加100点护盾，不超过上限100
                        self.shield_value = min(self.shield_value + 100, self.shield_max)
                        
                        # 设置冷却时间（提高350%频率）
                        self.shield_cooldown = 333  # 5.56秒冷却
                
                # 使用召唤邪恶蝙蝠技能（约每3秒一次，提高频率以便更容易看到）
                if self.summon_bat_cooldown <= 0:
                    if random.randint(1, 180) == 1:  # 约每3秒有1/180几率触发，提高频率
                        # 更新last_skill属性
                        self.last_skill = "召唤邪恶蝙蝠"
                        
                        # 切换到召唤技能图片
                        self.current_image = "吸血鬼_召唤"
                        self.skill_image_timer = self.skill_image_duration
                        print(f"吸血鬼使用召唤技能 - 切换到图片: {self.current_image}")
                        
                        # 召唤3只邪恶蝙蝠
                        for i in range(3):
                            # 随机位置：以吸血鬼为中心，±3格（±96像素）范围内
                            # 转换为格子坐标计算
                            vampire_tile_x = int(self.x // 32)
                            vampire_tile_y = int(self.y // 32)
                            
                            # 在吸血鬼周围±3格范围内随机选择一个格子
                            bat_tile_x = random.randint(vampire_tile_x - 3, vampire_tile_x + 3)
                            bat_tile_y = random.randint(vampire_tile_y - 3, vampire_tile_y + 3)
                            
                            # 转换为像素坐标，并在格子内随机偏移
                            bat_x = bat_tile_x * 32 + random.randint(0, 32)
                            bat_y = bat_tile_y * 32 + random.randint(0, 32)
                            
                            # 添加邪恶蝙蝠
                            self.summoned_bats.append({
                                'x': bat_x,
                                'y': bat_y,
                                'width': 48,  # 邪恶蝙蝠的宽度
                                'height': 40,  # 邪恶蝙蝠的高度
                                'target': player,  # 攻击目标为玩家
                                'timer': 600,  # 10秒后消失（600帧）
                                'speed': 2.8,  # 邪恶蝙蝠的速度
                                'damage': 25,  # 邪恶蝙蝠的伤害
                                'health': 1,  # 1点血量，可被杀死
                                'no_drop': True  # 标记为不掉落经验和物品
                            })
                        
                        # 设置冷却时间（提高频率后保持一致）
                        self.summon_bat_cooldown = 180  # 3秒冷却
                
                # 使用吸血蝙蝠技能（约每15秒一次）
                if self.healing_bat_cooldown <= 0:
                    if random.randint(1, 900) == 1:  # 约每15秒有1/900几率触发
                        # 更新last_skill属性
                        self.last_skill = "吸血蝙蝠"
                        
                        # 切换到召唤技能图片
                        self.current_image = "吸血鬼_召唤"
                        self.skill_image_timer = self.skill_image_duration
                        print(f"吸血鬼使用召唤技能 - 切换到图片: {self.current_image}")
                        
                        # 召唤3-9只吸血蝙蝠
                        bat_count = random.randint(3, 9)
                        for i in range(bat_count):
                            # 随机位置：以吸血鬼为中心，±3格（±96像素）范围内
                            # 转换为格子坐标计算
                            vampire_tile_x = int(self.x // 32)
                            vampire_tile_y = int(self.y // 32)
                            
                            # 在吸血鬼周围±3格范围内随机选择一个格子
                            bat_tile_x = random.randint(vampire_tile_x - 3, vampire_tile_x + 3)
                            bat_tile_y = random.randint(vampire_tile_y - 3, vampire_tile_y + 3)
                            
                            # 转换为像素坐标，并在格子内随机偏移
                            bat_x = bat_tile_x * 32 + random.randint(0, 32)
                            bat_y = bat_tile_y * 32 + random.randint(0, 32)
                            
                            # 添加吸血蝙蝠
                            self.healing_bats.append({
                                'x': bat_x,
                                'y': bat_y,
                                'width': 48,  # 吸血蝙蝠的宽度
                                'height': 40,  # 吸血蝙蝠的高度
                                'timer': 600,  # 10秒后消失（600帧）
                                'speed': 4.0,  # 吸血蝙蝠速度更快
                                'health': 1,  # 1点血量，可被杀死
                                'no_drop': True  # 标记为不掉落经验和物品
                            })
                        
                        # 设置冷却时间
                        self.healing_bat_cooldown = self.healing_bat_cooldown_max  # 15秒冷却
                
                # 使用刺球召唤技能（约每12秒一次）
                if self.spike_ball_cooldown <= 0:
                    if random.randint(1, 720) == 1:  # 约每12秒有1/720几率触发
                        # 更新last_skill属性
                        self.last_skill = "刺球召唤"
                        
                        # 切换到召唤技能图片
                        self.current_image = "吸血鬼_召唤"
                        self.skill_image_timer = self.skill_image_duration
                        print(f"吸血鬼使用召唤技能 - 切换到图片: {self.current_image}")
                        
                        # 召唤3只刺球
                        for i in range(3):
                            # 随机位置：以吸血鬼为中心，±3格（±96像素）范围内
                            # 转换为格子坐标计算
                            vampire_tile_x = int(self.x // 32)
                            vampire_tile_y = int(self.y // 32)
                            
                            # 在吸血鬼周围±3格范围内随机选择一个格子
                            ball_tile_x = random.randint(vampire_tile_x - 3, vampire_tile_x + 3)
                            ball_tile_y = random.randint(vampire_tile_y - 3, vampire_tile_y + 3)
                            
                            # 转换为像素坐标，并在格子内随机偏移
                            ball_x = ball_tile_x * 32 + random.randint(0, 32)
                            ball_y = ball_tile_y * 32 + random.randint(0, 32)
                            
                            # 添加刺球
                            self.spike_balls.append({
                                'x': ball_x,
                                'y': ball_y,
                                'width': 32,  # 刺球宽度
                                'height': 32,  # 刺球高度
                                'timer': 600,  # 10秒后消失（600帧）
                                'speed': 5.0,  # 刺球冲刺速度
                                'rotation': 0,  # 旋转角度
                                'health': 1,  # 1点血量，可被杀死
                                'no_drop': True  # 标记为不掉落经验和物品
                            })
                        
                        # 设置冷却时间
                        self.spike_ball_cooldown = self.spike_ball_cooldown_max  # 12秒冷却
                
                # 使用异变骷髅召唤技能（约每15秒一次）
                if self.mutant_skull_cooldown <= 0:
                    if random.randint(1, 900) == 1:  # 约每15秒有1/900几率触发
                        # 更新last_skill属性
                        self.last_skill = "异变骷髅召唤"
                        
                        # 切换到召唤技能图片
                        self.current_image = "吸血鬼_召唤"
                        self.skill_image_timer = self.skill_image_duration
                        print(f"吸血鬼使用召唤技能 - 切换到图片: {self.current_image}")
                        
                        # 召唤3只异变骷髅
                        for i in range(3):
                            # 随机位置：以吸血鬼为中心，±3格（±96像素）范围内
                            # 转换为格子坐标计算
                            vampire_tile_x = int(self.x // 32)
                            vampire_tile_y = int(self.y // 32)
                            
                            # 在吸血鬼周围±3格范围内随机选择一个格子
                            skull_tile_x = random.randint(vampire_tile_x - 3, vampire_tile_x + 3)
                            skull_tile_y = random.randint(vampire_tile_y - 3, vampire_tile_y + 3)
                            
                            # 转换为像素坐标，并在格子内随机偏移
                            skull_x = skull_tile_x * 32 + random.randint(0, 32)
                            skull_y = skull_tile_y * 32 + random.randint(0, 32)
                            
                            # 添加异变骷髅
                            self.mutant_skulls.append({
                                'x': skull_x,
                                'y': skull_y,
                                'width': 48,  # 异变骷髅宽度
                                'height': 56,  # 异变骷髅高度
                                'timer': 600,  # 10秒后消失（600帧）
                                'move_timer': 0,  # 移动计时器
                                'move_dir_x': random.choice([-0.5, 0, 0.5]),  # 初始移动方向X
                                'move_dir_y': random.choice([-0.5, 0, 0.5]),  # 初始移动方向Y
                                'projectile_timer': 0,  # 投掷物发射计时器
                                'health': 1,  # 1点血量，可被杀死
                                'no_drop': True  # 标记为不掉落经验和物品
                            })
                        
                        # 设置冷却时间
                        self.mutant_skull_cooldown = self.mutant_skull_cooldown_max  # 15秒冷却
            # 死神Boss的特殊行为：镰刀横扫技能
            elif self.mob_id == 死神:
                # 初始化冲刺相关属性（如果不存在）
                if not hasattr(self, 'is_dashing'):
                    self.is_dashing = False
                if not hasattr(self, 'dash_timer'):
                    self.dash_timer = 0
                if not hasattr(self, 'dash_direction_x'):
                    self.dash_direction_x = 0
                if not hasattr(self, 'dash_direction_y'):
                    self.dash_direction_y = 0
                if not hasattr(self, 'dash_duration'):
                    self.dash_duration = 15  # 冲刺持续15帧（0.25秒）
                if not hasattr(self, 'dash_cooldown'):
                    self.dash_cooldown = 0
                if not hasattr(self, 'dash_cooldown_max'):
                    self.dash_cooldown_max = 120  # 冲刺冷却2秒
                
                # 更新冲刺冷却
                if self.dash_cooldown > 0:
                    self.dash_cooldown -= 1
                
                # 更新冲刺状态
                if self.is_dashing:
                    self.dash_timer -= 1
                    # 冲刺移动
                    self.x += self.dash_direction_x * 15
                    if self.can_fly:
                        self.y += self.dash_direction_y * 15
                    
                    # 冲刺结束
                    if self.dash_timer <= 0:
                        self.is_dashing = False
                        self.vel_x = 0
                        if self.can_fly:
                            self.vel_y = 0
                        self.last_skill = "冲刺"
                        # 恢复默认图片
                        self.current_image = self.default_image
                        self.skill_image_timer = self.skill_image_duration
                
                # 死神作为BOSS生物，向玩家移动
                if not self.is_dashing:
                    if dist > self.attack_range:
                        # 向玩家移动
                        dir_x = dx / dist
                        dir_y = dy / dist
                        self.vel_x = dir_x * self.speed
                        self.direction = 1 if dir_x > 0 else -1
                        self.x += self.vel_x
                        
                        # 飞行生物可以在垂直方向上移动，增加惯性
                        if self.can_fly:
                            self.vel_y = self.vel_y * 0.8 + dir_y * self.fly_speed * 0.7  # 增加惯性，减少突然变化
                            self.y += self.vel_y
                    else:
                        # 在攻击范围内，停止移动并尝试攻击
                        self.vel_x = 0
                        if self.can_fly:
                            self.vel_y = 0
                        # 攻击玩家
                        self.attack(player)
                
                # 初始化镰刀横扫技能相关属性（如果不存在）
                if not hasattr(self, 'sickle_sweep_timer'):
                    self.sickle_sweep_timer = 0  # 技能冷却计时器
                if not hasattr(self, 'sickle_sweep_cooldown'):
                    self.sickle_sweep_cooldown = 8 * 60  # 8秒冷却（60fps）
                if not hasattr(self, 'is_sweeping'):
                    self.is_sweeping = False  # 是否正在使用技能
                if not hasattr(self, 'sweep_duration'):
                    self.sweep_duration = 30  # 技能持续30帧（约0.5秒）
                if not hasattr(self, 'sweep_frame'):
                    self.sweep_frame = 0  # 当前技能帧数
                if not hasattr(self, 'attack_triggered'):
                    self.attack_triggered = False  # 攻击是否已触发
                
                # 初始化镰刀横扫特效相关属性（如果不存在）
                if not hasattr(self, 'sweep_effects'):
                    self.sweep_effects = []  # 存储当前活跃的镰刀横扫特效
                
                # 更新技能冷却计时器
                if self.sickle_sweep_timer < self.sickle_sweep_cooldown:
                    self.sickle_sweep_timer += 1
                
                # 更新技能持续时间
                if self.is_sweeping:
                    self.sweep_frame += 1
                    
                    # 持续更新特效中心位置，使其跟随死神移动
                    for effect in self.sweep_effects:
                        effect['x'] = self.x + self.width // 2  # 更新特效中心X为死神当前中心
                        effect['y'] = self.y + self.height // 2  # 更新特效中心Y为死神当前中心
                    
                    # 计算BOSS朝向（根据玩家位置）
                    boss_direction = math.atan2(dy, dx)
                    
                    # 技能参数
                    skill_range = 10 * 32  # 10格 = 320像素
                    skill_damage = 50  # 造成50点伤害
                    skill_angle = math.pi  # 180°范围
                    
                    # 0.3秒（18帧）时触发攻击
                    if self.sweep_frame == 18 and not self.attack_triggered:
                        # 计算与玩家的距离和角度（使用当前死神位置）
                        dx_attack = player.坐标_x - (self.x + self.width // 2)
                        dy_attack = player.坐标_y - (self.y + self.height // 2)
                        dist_attack = math.hypot(dx_attack, dy_attack)
                        
                        # 计算玩家相对于BOSS的角度
                        player_angle = math.atan2(dy_attack, dx_attack)
                        
                        # 计算角度差（取绝对值）
                        angle_diff = abs(player_angle - boss_direction)
                        # 确保角度差在0到π之间
                        if angle_diff > math.pi:
                            angle_diff = 2 * math.pi - angle_diff
                        
                        # 检查玩家是否在180°范围内
                        if angle_diff <= skill_angle / 2 and dist_attack <= skill_range:
                            # 灵魂收割被动技能：对生命值低于10%的敌人造成致命一击
                            if hasattr(player, 'max_health') and hasattr(player, 'current_health'):
                                # 检查玩家生命值是否低于10%
                                if player.current_health <= player.max_health * 0.1:
                                    # 造成致命伤害
                                    player.take_damage(99999999, self)
                                    print(f"死神使用灵魂收割（镰刀横扫） - 对生命值低于10%的玩家造成致命一击！")
                                else:
                                    # 正常伤害
                                    player.take_damage(skill_damage, self)
                                    print(f"死神镰刀横扫击中玩家 - 伤害: {skill_damage}, 距离: {dist_attack}, 角度差: {angle_diff}")
                            else:
                                # 无法获取玩家生命值信息，使用正常伤害
                                player.take_damage(skill_damage, self)
                                print(f"死神镰刀横扫击中玩家 - 伤害: {skill_damage}, 距离: {dist_attack}, 角度差: {angle_diff}")
                        
                        # 标记攻击已触发
                        self.attack_triggered = True
                    
                    # 技能结束
                    if self.sweep_frame >= self.sweep_duration:
                        self.is_sweeping = False
                        self.sweep_frame = 0
                        self.attack_triggered = False
                        # 恢复默认图片
                        self.current_image = self.default_image
                        # 清除特效
                        self.sweep_effects.clear()
                
                # 更新镰刀横扫特效
                for effect in self.sweep_effects[:]:
                    # 更新特效参数
                    effect['frame'] += 1
                    
                    # 立即显示劈砍区域
                    if effect['frame'] == 1:
                        effect['alpha'] = 255  # 完全显示
                    
                    # 0.25秒（15帧）时区域变红
                    if effect['frame'] == 15:
                        effect['color'] = (255, 0, 0)  # 变为红色
                    
                    # 计算当前旋转角度
                    effect['current_angle'] = effect['start_angle'] + effect['rotation_speed'] * effect['frame']
                    # 计算透明度（先增加，在攻击后减少）
                    if effect['frame'] < 10:
                        # 0.16秒内逐渐显示
                        effect['alpha'] = int(255 * (effect['frame'] / 10))
                    elif effect['frame'] < 18:
                        # 攻击前保持完全显示
                        effect['alpha'] = 255
                    else:
                        # 攻击后逐渐消失
                        effect['alpha'] = int(255 * (1 - (effect['frame'] - 18) / (effect['duration'] - 18)))
                    # 计算缩放比例（逐渐放大）
                    effect['scale'] = 1 + (effect['frame'] / effect['duration']) * 0.5
                    # 检查特效是否结束
                    if effect['frame'] >= effect['duration']:
                        self.sweep_effects.remove(effect)
                
                # 使用镰刀横扫技能（冷却时间到了）
                if not self.is_sweeping and not self.is_dashing and self.sickle_sweep_timer >= self.sickle_sweep_cooldown:
                    # 更新last_skill属性
                    self.last_skill = "镰刀横扫"
                    # 切换到镰刀横扫图片
                    self.current_image = "死神_劈砍"
                    self.skill_image_timer = self.skill_image_duration
                    print(f"死神使用镰刀横扫 - 切换到图片: {self.current_image}")
                    
                    # 开始技能
                    self.is_sweeping = True
                    self.sweep_frame = 0
                    self.attack_triggered = False
                    self.sickle_sweep_timer = 0
                    
                    # 计算BOSS朝向（根据玩家位置）
                    boss_direction = math.atan2(dy, dx)
                    
                    # 技能参数
                    skill_range = 10 * 32  # 10格 = 320像素
                    
                    # 创建镰刀横扫特效
                    self.sweep_effects.append({
                        'x': self.x + self.width // 2,  # 特效中心X
                        'y': self.y + self.height // 2,  # 特效中心Y
                        'start_angle': boss_direction - math.pi / 2,  # 起始角度（向左90°）
                        'current_angle': boss_direction - math.pi / 2,  # 当前角度
                        'end_angle': boss_direction + math.pi / 2,  # 结束角度（向右90°）
                        'range': skill_range,  # 技能范围
                        'width': 50,  # 镰刀宽度
                        'color': (0, 0, 255),  # 初始颜色（蓝色）
                        'alpha': 0,  # 初始透明度
                        'frame': 0,  # 当前帧
                        'duration': self.sweep_duration,  # 特效持续时间
                        'rotation_speed': math.radians(30) / self.sweep_duration,  # 旋转速度（0.5秒旋转30°）
                        'scale': 1.0  # 初始缩放比例
                    })
                    
                # 初始化死亡领域技能相关属性（如果不存在）
                if not hasattr(self, 'death_domain_timer'):
                    self.death_domain_timer = 0  # 死亡领域计时器
                if not hasattr(self, 'death_domain_cooldown'):
                    self.death_domain_cooldown = 0  # 死亡领域冷却计时器
                if not hasattr(self, 'death_domain_duration'):
                    self.death_domain_duration = 300  # 死亡领域持续时间（5秒，60帧/秒）
                if not hasattr(self, 'death_domain_cooldown_max'):
                    self.death_domain_cooldown_max = 1200  # 死亡领域冷却时间（20秒，60帧/秒）
                if not hasattr(self, 'is_death_domain_active'):
                    self.is_death_domain_active = False  # 死亡领域是否激活
                if not hasattr(self, 'death_domain_damage'):
                    self.death_domain_damage = 6  # 每0.2秒伤害
                if not hasattr(self, 'death_domain_range'):
                    self.death_domain_range = 20 * 32  # 20格范围，32像素/格
                if not hasattr(self, 'death_domain_effects'):
                    self.death_domain_effects = []  # 死亡领域特效
                
                # 更新死亡领域冷却
                if self.death_domain_cooldown > 0:
                    self.death_domain_cooldown -= 1
                
                # 更新死亡领域状态
                if self.is_death_domain_active:
                    self.death_domain_timer += 1
                    
                    # 持续更新死亡领域特效位置，使其跟随死神移动
                    for effect in self.death_domain_effects:
                        effect['x'] = self.x + self.width // 2  # 更新特效中心X为死神当前中心
                        effect['y'] = self.y + self.height // 2  # 更新特效中心Y为死神当前中心
                    
                    # 每0.2秒造成伤害（每12帧）
                    if self.death_domain_timer % 12 == 0:
                        # 计算与玩家的距离（使用当前死神位置）
                        dx_domain = player.坐标_x - (self.x + self.width // 2)
                        dy_domain = player.坐标_y - (self.y + self.height // 2)
                        dist_domain = math.hypot(dx_domain, dy_domain)
                        
                        # 检查玩家是否在死亡领域范围内
                        if dist_domain <= self.death_domain_range:
                            # 玩家在范围内，造成伤害
                            player.take_damage(self.death_domain_damage, self)
                            print(f"死神死亡领域击中玩家 - 伤害: {self.death_domain_damage}, 距离: {dist_domain}")
                    
                    # 更新死亡领域特效
                    for effect in self.death_domain_effects[:]:
                        effect['frame'] += 1
                        # 计算透明度（脉动效果）
                        effect['alpha'] = int(100 + 50 * math.sin(effect['frame'] * 0.1))
                        # 检查特效是否结束
                        if effect['frame'] >= self.death_domain_duration:
                            self.death_domain_effects.remove(effect)
                    
                    # 死亡领域结束
                    if self.death_domain_timer >= self.death_domain_duration:
                        self.is_death_domain_active = False
                        self.death_domain_timer = 0
                        self.death_domain_effects.clear()
                        print("死神死亡领域效果结束")
                
                # 随机使用冲刺技能（频率适中）
                if not self.is_sweeping and not self.is_dashing and self.dash_cooldown <= 0:
                    if random.randint(1, 100) == 1:  # 约每1.67秒有1/100几率触发
                        self.is_dashing = True
                        self.dash_timer = self.dash_duration
                        self.dash_cooldown = self.dash_cooldown_max
                        
                        # 计算冲刺方向（向玩家方向）
                        if dist > 0:
                            self.dash_direction_x = dx / dist
                            self.dash_direction_y = dy / dist
                        else:
                            self.dash_direction_x = 1 if dx >= 0 else -1
                            self.dash_direction_y = 0
                        
                        # 更新技能追踪
                        self.last_skill = "冲刺"
                        # 切换到冲刺图片
                        self.current_image = "死神_冲刺"
                        self.skill_image_timer = self.skill_image_duration
                        print(f"死神使用冲刺 - 切换到图片: {self.current_image}")
                
                # 初始化镰刀投掷技能相关属性（如果不存在）
                if not hasattr(self, 'sickle_throw_timer'):
                    self.sickle_throw_timer = 0  # 镰刀投掷计时器
                if not hasattr(self, 'sickle_throw_cooldown'):
                    self.sickle_throw_cooldown = 0  # 镰刀投掷冷却计时器
                if not hasattr(self, 'sickle_throw_cooldown_max'):
                    self.sickle_throw_cooldown_max = 600  # 镰刀投掷冷却时间（10秒，60帧/秒）
                if not hasattr(self, 'sickle_projectiles'):
                    self.sickle_projectiles = []  # 存储当前活跃的镰刀投掷物
                # 初始化灵魂护盾技能相关属性（如果不存在）
                if self.mob_id == 死神:  # 只有死神使用这个护盾系统
                    if not hasattr(self, 'soul_shield_cooldown'):
                        self.soul_shield_cooldown = 0  # 灵魂护盾冷却计时器
                        self.soul_shield_cooldown_max = 1500  # 灵魂护盾冷却时间（25秒，60帧/秒）
                        self.summoned_souls = []  # 存储当前召唤的灵魂
                    if not hasattr(self, 'shield_value'):
                        self.shield_value = 0  # 当前护盾值
                    if not hasattr(self, 'max_shield_value'):
                        self.max_shield_value = 1200  # 最大护盾值
                    if not hasattr(self, 'soul_shield_gain'):
                        self.soul_shield_gain = 100  # 每个灵魂提供的护盾值
                
                # 初始化镰刀领域技能相关属性（如果不存在）
                if not hasattr(self, 'sickle_field_timer'):
                    self.sickle_field_timer = 0  # 镰刀领域计时器
                if not hasattr(self, 'sickle_field_cooldown'):
                    self.sickle_field_cooldown = 0  # 镰刀领域冷却计时器
                if not hasattr(self, 'sickle_field_cooldown_max'):
                    self.sickle_field_cooldown_max = 2100  # 镰刀领域冷却时间（35秒，60帧/秒）
                if not hasattr(self, 'is_sickle_field_active'):
                    self.is_sickle_field_active = False  # 镰刀领域是否激活
                if not hasattr(self, 'sickle_field_duration'):
                    self.sickle_field_duration = 300  # 镰刀领域持续时间（5秒，60帧/秒）
                if not hasattr(self, 'sickle_field_projectiles'):
                    self.sickle_field_projectiles = []  # 存储当前活跃的镰刀
                if not hasattr(self, 'sickle_field_damage'):
                    self.sickle_field_damage = 10  # 每次伤害10点
                if not hasattr(self, 'sickle_field_damage_interval'):
                    self.sickle_field_damage_interval = 12  # 伤害间隔（0.2秒，60帧/秒）
                if not hasattr(self, 'sickle_field_launch_distance'):
                    self.sickle_field_launch_distance = 250  # 发射距离250像素
                if not hasattr(self, 'sickle_field_sickle_count'):
                    self.sickle_field_sickle_count = 6  # 发射6个镰刀
                if not hasattr(self, 'sickle_field_radius'):
                    self.sickle_field_radius = 100  # 镰刀区域半径100像素
                if not hasattr(self, 'sickle_field_rotation_speed'):
                    self.sickle_field_rotation_speed = -0.4  # 镰刀旋转速度，负值表示反向旋转，速度加快300%（0.1 * 4）
                if not hasattr(self, 'player_damage_timers'):
                    self.player_damage_timers = {}  # 玩家伤害计时器，避免重复伤害
                
                # 初始化新技能：旋转跟随镰刀（向250像素发射6把镰刀，全部正旋转，击中玩家不消失）
                if not hasattr(self, 'rotating_follow_sickle_timer'):
                    self.rotating_follow_sickle_timer = 0  # 旋转跟随镰刀计时器
                if not hasattr(self, 'rotating_follow_sickle_cooldown'):
                    self.rotating_follow_sickle_cooldown = 0  # 旋转跟随镰刀冷却计时器
                if not hasattr(self, 'rotating_follow_sickle_cooldown_max'):
                    self.rotating_follow_sickle_cooldown_max = 2400  # 旋转跟随镰刀冷却时间（40秒，60帧/秒）
                if not hasattr(self, 'is_rotating_follow_sickle_active'):
                    self.is_rotating_follow_sickle_active = False  # 旋转跟随镰刀是否激活
                if not hasattr(self, 'rotating_follow_sickle_duration'):
                    self.rotating_follow_sickle_duration = 420  # 旋转跟随镰刀持续时间（7秒，60帧/秒）
                if not hasattr(self, 'rotating_follow_sickle_projectiles'):
                    self.rotating_follow_sickle_projectiles = []  # 存储当前活跃的旋转跟随镰刀
                if not hasattr(self, 'rotating_follow_sickle_damage'):
                    self.rotating_follow_sickle_damage = 12  # 每次伤害12点
                if not hasattr(self, 'rotating_follow_sickle_damage_interval'):
                    self.rotating_follow_sickle_damage_interval = 12  # 伤害间隔（0.2秒，60帧/秒）
                if not hasattr(self, 'rotating_follow_sickle_launch_distance'):
                    self.rotating_follow_sickle_launch_distance = 250  # 发射距离250像素
                if not hasattr(self, 'rotating_follow_sickle_count'):
                    self.rotating_follow_sickle_count = 6  # 发射6个镰刀
                if not hasattr(self, 'rotating_follow_sickle_rotation_speed'):
                    self.rotating_follow_sickle_rotation_speed = 1.25  # 镰刀旋转速度，正值表示正旋转（增加150%）
                if not hasattr(self, 'rotating_follow_sickle_player_damage_timers'):
                    self.rotating_follow_sickle_player_damage_timers = {}  # 玩家伤害计时器，避免重复伤害
                
                # 初始化子弹风暴技能相关属性（如果不存在）
                if not hasattr(self, 'bullet_storm_cooldown'):
                    self.bullet_storm_cooldown = 0  # 子弹风暴冷却计时器
                    self.bullet_storm_cooldown_max = 2400  # 子弹风暴冷却时间（40秒，60帧/秒）
                    self.bullet_storm_projectiles = []  # 存储当前活跃的子弹
                    self.bullet_storm_damage = 10  # 每次伤害10点
                    self.bullet_storm_launch_distance = 250  # 发射距离250像素
                    self.bullet_storm_bullet_count = 12  # 发射12颗子弹
                    self.bullet_storm_speed = 7.5  # 子弹速度（增加150%）
                    self.bullet_storm_width = 20  # 子弹宽度
                    self.bullet_storm_height = 20  # 子弹高度
                    self.bullet_storm_image = "75投掷物"  # 子弹图片
                
                # 更新镰刀投掷冷却
                if self.sickle_throw_cooldown > 0:
                    self.sickle_throw_cooldown -= 1
                
                # 更新镰刀投掷物状态
                for proj in self.sickle_projectiles[:]:
                    proj['frame'] += 1
                    
                    # 移动投掷物
                    proj['x'] += proj['vx']
                    proj['y'] += proj['vy']
                    
                    # 更新旋转角度（正旋转）
                    proj['angle'] += proj['rotation_speed']
                    
                    # 检查是否到达最大距离或需要返回
                    proj['distance_traveled'] += math.hypot(proj['vx'], proj['vy'])
                    
                    if not proj['is_returning']:
                        # 前进阶段
                        if proj['distance_traveled'] >= proj['max_distance']:
                            # 到达最大距离，开始返回
                            proj['is_returning'] = True
                            # 计算返回方向（朝向死神）
                            dx_return = self.x + self.width // 2 - proj['x']
                            dy_return = self.y + self.height // 2 - proj['y']
                            return_dist = math.hypot(dx_return, dy_return)
                            if return_dist > 0:
                                proj['vx'] = dx_return / return_dist * proj['speed']
                                proj['vy'] = dy_return / return_dist * proj['speed']
                    else:
                        # 返回阶段，检查是否到达死神
                        dx_to_boss = self.x + self.width // 2 - proj['x']
                        dy_to_boss = self.y + self.height // 2 - proj['y']
                        dist_to_boss = math.hypot(dx_to_boss, dy_to_boss)
                        if dist_to_boss < 20:  # 足够接近死神
                            self.sickle_projectiles.remove(proj)
                            continue
                    
                    # 检查是否击中玩家
                    if not proj['has_hit_player']:
                        player_rect = pygame.Rect(player.坐标_x, player.坐标_y, player.宽, player.高)
                        proj_rect = pygame.Rect(proj['x'], proj['y'], proj['width'], proj['height'])
                        if proj_rect.colliderect(player_rect):
                            # 造成200%攻击力的伤害
                            damage = int(self.damage * 2)
                            player.take_damage(damage, self)
                            print(f"死神镰刀投掷击中玩家 - 伤害: {damage}")
                            proj['has_hit_player'] = True  # 标记已击中，防止重复伤害
                    
                    # 检查计时器，防止投掷物存在时间过长
                    if proj['frame'] > 1200:  # 20秒后自动消失
                        self.sickle_projectiles.remove(proj)
                
                # 更新子弹风暴冷却
                if self.bullet_storm_cooldown > 0:
                    self.bullet_storm_cooldown -= 1
                
                # 更新子弹风暴子弹状态
                for projectile in self.bullet_storm_projectiles[:]:
                    # 更新子弹位置
                    projectile['x'] += projectile['vx']
                    projectile['y'] += projectile['vy']
                    
                    # 检查是否到达目标位置（转向点）
                    if not projectile['has_turned']:
                        # 计算当前位置到发射点的距离
                        dx_to_start = projectile['x'] - projectile['start_x']
                        dy_to_start = projectile['y'] - projectile['start_y']
                        dist_to_start = math.hypot(dx_to_start, dy_to_start)
                        
                        if dist_to_start >= self.bullet_storm_launch_distance:
                            # 到达目标位置，开始转向玩家
                            projectile['has_turned'] = True
                            # 计算朝向玩家的方向
                            dx_to_player = player.坐标_x + player.宽 // 2 - projectile['x']
                            dy_to_player = player.坐标_y + player.高 // 2 - projectile['y']
                            dist_to_player = math.hypot(dx_to_player, dy_to_player)
                            if dist_to_player > 0:
                                # 计算朝向玩家的速度向量
                                projectile['vx'] = dx_to_player / dist_to_player * self.bullet_storm_speed
                                projectile['vy'] = dy_to_player / dist_to_player * self.bullet_storm_speed
                                # 更新子弹角度以朝向玩家
                                projectile['angle'] = math.degrees(math.atan2(projectile['vy'], projectile['vx']))
                    
                    # 检查是否击中玩家
                    player_rect = pygame.Rect(player.坐标_x, player.坐标_y, player.宽, player.高)
                    bullet_rect = pygame.Rect(projectile['x'], projectile['y'], projectile['width'], projectile['height'])
                    if bullet_rect.colliderect(player_rect):
                        # 击中玩家，造成伤害
                        player.take_damage(self.bullet_storm_damage, self)
                        print(f"死神子弹风暴击中玩家 - 伤害: {self.bullet_storm_damage}")
                        # 移除子弹
                        self.bullet_storm_projectiles.remove(projectile)
                        continue
                    
                    # 检查子弹是否存在时间过长（防止内存泄漏）
                    if projectile['frame'] > 600:  # 10秒后自动消失
                        self.bullet_storm_projectiles.remove(projectile)
                        continue
                    
                    # 更新子弹帧计数器
                    projectile['frame'] += 1
                
                # 更新灵魂护盾冷却
                if self.soul_shield_cooldown > 0:
                    self.soul_shield_cooldown -= 1
                
                # 更新召唤的灵魂行为
                for soul in self.summoned_souls[:]:
                    soul['frame'] += 1
                    
                    # 计算灵魂到死神的距离和方向
                    dx_soul = self.x + self.width // 2 - soul['x']
                    dy_soul = self.y + self.height // 2 - soul['y']
                    dist_soul = math.hypot(dx_soul, dy_soul)
                    
                    # 始终向死神移动，直到触碰到死神
                    if dist_soul > 20:  # 当距离大于20像素时，向死神移动
                        # 向死神移动
                        soul_dir_x = dx_soul / dist_soul
                        soul_dir_y = dy_soul / dist_soul
                        
                        # 更新灵魂位置
                        soul['x'] += soul_dir_x * soul['speed']
                        soul['y'] += soul_dir_y * soul['speed']
                    
                    # 检查灵魂是否触碰到死神（距离小于等于20像素）
                    if dist_soul <= 20:
                        # 灵魂触碰到死神，为死神增加护盾值
                        # 确保使用正确的护盾最大值属性
                        max_shield = self.max_shield_value if hasattr(self, 'max_shield_value') else 1200
                        self.shield_value = min(self.shield_value + self.soul_shield_gain, max_shield)
                        print(f"灵魂触碰到死神 - 增加护盾值 {self.soul_shield_gain}，当前护盾值: {self.shield_value}/{max_shield}")
                        # 移除该灵魂
                        self.summoned_souls.remove(soul)
                        continue
                    
                    # 灵魂存活时间限制
                    if soul['frame'] > 300:  # 5秒后自动消失
                        self.summoned_souls.remove(soul)
                        continue
                
                # 更新新技能：旋转跟随镰刀冷却
                if self.rotating_follow_sickle_cooldown > 0:
                    self.rotating_follow_sickle_cooldown -= 1
                
                # 更新新技能：旋转跟随镰刀状态
                if self.is_rotating_follow_sickle_active:
                    self.rotating_follow_sickle_timer += 1
                    
                    # 计算死神当前位置
                    death_center_x = self.x + self.width // 2
                    death_center_y = self.y + self.height // 2
                    
                    # 更新旋转跟随镰刀状态
                    for projectile in self.rotating_follow_sickle_projectiles[:]:
                        # 更新镰刀位置，使其围绕死神旋转
                        # 计算当前角度，初始角度加上随时间变化的旋转角度
                        current_angle = projectile['initial_angle'] + (self.rotating_follow_sickle_rotation_speed * self.rotating_follow_sickle_timer)
                        # 计算新位置，以死神当前位置为中心，围绕旋转
                        projectile['x'] = death_center_x + math.cos(current_angle) * self.rotating_follow_sickle_launch_distance
                        projectile['y'] = death_center_y + math.sin(current_angle) * self.rotating_follow_sickle_launch_distance
                        
                        # 镰刀自身不旋转，只围绕死神旋转
                        # 移除自身旋转代码：projectile['angle'] += self.rotating_follow_sickle_rotation_speed
                        
                        # 检查是否到达持续时间
                        if self.rotating_follow_sickle_timer >= self.rotating_follow_sickle_duration:
                            # 移除镰刀
                            self.rotating_follow_sickle_projectiles.remove(projectile)
                            continue
                        
                        # 检查镰刀是否击中玩家
                        player_rect = pygame.Rect(player.坐标_x, player.坐标_y, player.宽, player.高)
                        sickle_rect = pygame.Rect(
                            projectile['x'],
                            projectile['y'],
                            projectile['width'],
                            projectile['height']
                        )
                        
                        if sickle_rect.colliderect(player_rect):
                            # 玩家被击中，造成伤害，镰刀不消失
                            player_key = id(player)
                            if player_key not in self.rotating_follow_sickle_player_damage_timers or self.rotating_follow_sickle_player_damage_timers[player_key] == 0:
                                # 造成12点伤害
                                player.take_damage(self.rotating_follow_sickle_damage, self)
                                print(f"死神旋转跟随镰刀击中玩家 - 伤害: {self.rotating_follow_sickle_damage}")
                                # 重置伤害计时器
                                self.rotating_follow_sickle_player_damage_timers[player_key] = self.rotating_follow_sickle_damage_interval
                    
                    # 更新旋转跟随镰刀的玩家伤害计时器
                    for player_key in list(self.rotating_follow_sickle_player_damage_timers.keys()):
                        if self.rotating_follow_sickle_player_damage_timers[player_key] > 0:
                            self.rotating_follow_sickle_player_damage_timers[player_key] -= 1
                        if self.rotating_follow_sickle_player_damage_timers[player_key] < 0:
                            self.rotating_follow_sickle_player_damage_timers[player_key] = 0
                    
                    # 旋转跟随镰刀技能结束
                    if self.rotating_follow_sickle_timer >= self.rotating_follow_sickle_duration:
                        self.is_rotating_follow_sickle_active = False
                        self.rotating_follow_sickle_timer = 0
                        self.rotating_follow_sickle_projectiles.clear()
                        self.rotating_follow_sickle_player_damage_timers.clear()
                        print("死神旋转跟随镰刀效果结束")
                
                # 使用死亡领域技能（冷却时间到了）
                if not self.is_sweeping and not self.is_dashing and not self.is_death_domain_active and self.death_domain_cooldown <= 0:
                    if random.randint(1, 600) == 1:  # 约每10秒有1/600几率触发
                        # 更新last_skill属性
                        self.last_skill = "死亡领域"
                        # 切换到死神领域图片
                        self.current_image = "死神_死神领域"
                        self.skill_image_timer = self.skill_image_duration
                        print(f"死神使用死亡领域 - 生成持续伤害领域！")
                        
                        # 开始技能
                        self.is_death_domain_active = True
                        self.death_domain_timer = 0
                        self.death_domain_cooldown = self.death_domain_cooldown_max
                        
                        # 创建死亡领域特效
                        self.death_domain_effects.append({
                            'x': self.x + self.width // 2,  # 特效中心X
                            'y': self.y + self.height // 2,  # 特效中心Y
                            'frame': 0,  # 当前帧
                            'duration': self.death_domain_duration,  # 特效持续时间
                            'radius': self.death_domain_range,  # 特效半径
                            'alpha': 150,  # 初始透明度
                            'color': (100, 0, 100)  # 紫色特效
                        })
                
                # 使用灵魂护盾技能（约每5秒一次，提高频率以便更容易看到）
                if not self.is_sweeping and not self.is_dashing and not self.is_death_domain_active and not self.is_sickle_field_active and self.soul_shield_cooldown <= 0:
                    if random.randint(1, 300) == 1:  # 约每5秒有1/300几率触发
                        # 更新last_skill属性
                        self.last_skill = "灵魂护盾"
                        print(f"死神使用灵魂护盾 - 召唤灵魂！")
                        
                        # 召唤5-12个灵魂（随机）
                        soul_count = random.randint(5, 12)
                        for i in range(soul_count):
                            # 随机位置：以死神为中心，±3格（±96像素）范围内
                            # 转换为格子坐标计算
                            death_tile_x = int(self.x // 32)
                            death_tile_y = int(self.y // 32)
                            
                            # 在死神周围±3格范围内随机选择一个格子
                            soul_tile_x = random.randint(death_tile_x - 3, death_tile_x + 3)
                            soul_tile_y = random.randint(death_tile_y - 3, death_tile_y + 3)
                            
                            # 转换为像素坐标，并在格子内随机偏移
                            soul_x = soul_tile_x * 32 + random.randint(0, 32)
                            soul_y = soul_tile_y * 32 + random.randint(0, 32)
                            
                            # 添加灵魂
                            self.summoned_souls.append({
                                'x': soul_x,
                                'y': soul_y,
                                'width': 32,  # 灵魂宽度
                                'height': 48,  # 灵魂高度
                                'speed': 2.0,  # 灵魂移动速度
                                'frame': 0,  # 当前帧
                                'health': 1,  # 1点血量，可被杀死
                                'no_drop': True,  # 标记为不掉落经验和物品
                                'image': "幽灵"  # 灵魂使用幽灵图片
                            })
                        
                        # 设置冷却时间
                        self.soul_shield_cooldown = self.soul_shield_cooldown_max  # 25秒冷却
                
                # 更新镰刀领域冷却
                if self.sickle_field_cooldown > 0:
                    self.sickle_field_cooldown -= 1
                
                # 更新镰刀领域状态
                if self.is_sickle_field_active:
                    self.sickle_field_timer += 1
                    
                    # 更新镰刀状态
                    for projectile in self.sickle_field_projectiles[:]:
                        # 镰刀正旋转
                        projectile['angle'] += self.sickle_field_rotation_speed
                        
                        # 检查是否到达停留时间
                        if self.sickle_field_timer >= self.sickle_field_duration:
                            # 移除镰刀
                            self.sickle_field_projectiles.remove(projectile)
                            continue
                        
                        # 检查玩家是否在镰刀区域内
                        player_rect = pygame.Rect(player.坐标_x, player.坐标_y, player.宽, player.高)
                        # 计算镰刀区域的矩形
                        sickle_rect = pygame.Rect(
                            projectile['x'] - self.sickle_field_radius,
                            projectile['y'] - self.sickle_field_radius,
                            self.sickle_field_radius * 2,
                            self.sickle_field_radius * 2
                        )
                        
                        if sickle_rect.colliderect(player_rect):
                            # 玩家在区域内，造成伤害
                            player_key = id(player)
                            if player_key not in self.player_damage_timers or self.player_damage_timers[player_key] == 0:
                                # 造成伤害
                                player.take_damage(self.sickle_field_damage, self)
                                print(f"死神镰刀领域击中玩家 - 伤害: {self.sickle_field_damage}")
                                # 重置伤害计时器
                                self.player_damage_timers[player_key] = self.sickle_field_damage_interval
                        
                    # 更新玩家伤害计时器
                    for player_key in list(self.player_damage_timers.keys()):
                        if self.player_damage_timers[player_key] > 0:
                            self.player_damage_timers[player_key] -= 1
                        if self.player_damage_timers[player_key] < 0:
                            self.player_damage_timers[player_key] = 0
                    
                    # 镰刀领域结束
                    if self.sickle_field_timer >= self.sickle_field_duration:
                        self.is_sickle_field_active = False
                        self.sickle_field_timer = 0
                        self.sickle_field_projectiles.clear()
                        self.player_damage_timers.clear()
                        print("死神镰刀领域效果结束")
                
                # 使用镰刀领域技能（冷却时间到了）
                if not self.is_sweeping and not self.is_dashing and not self.is_death_domain_active and not self.is_sickle_field_active and self.sickle_field_cooldown <= 0:
                    if random.randint(1, 300) == 1:  # 约每5秒有1/300几率触发
                        # 更新last_skill属性
                        self.last_skill = "镰刀领域"
                        # 切换到魔法技能图片
                        self.current_image = "死神_魔法技能"
                        self.skill_image_timer = self.skill_image_duration
                        print(f"死神使用镰刀领域 - 发射6个旋转镰刀！")
                        
                        # 开始技能
                        self.is_sickle_field_active = True
                        self.sickle_field_timer = 0
                        self.sickle_field_cooldown = self.sickle_field_cooldown_max
                        
                        # 发射6个镰刀，360°均匀分布
                        for i in range(self.sickle_field_sickle_count):
                            # 计算发射角度
                            angle = (2 * math.pi / self.sickle_field_sickle_count) * i
                            
                            # 计算发射位置
                            start_x = self.x + self.width // 2
                            start_y = self.y + self.height // 2
                            
                            # 计算目标位置（向外100像素）
                            target_x = start_x + math.cos(angle) * self.sickle_field_launch_distance
                            target_y = start_y + math.sin(angle) * self.sickle_field_launch_distance
                            
                            # 添加镰刀
                            self.sickle_field_projectiles.append({
                                'x': target_x,  # 目标位置X
                                'y': target_y,  # 目标位置Y
                                'width': 60,  # 镰刀宽度（增加100%）
                                'height': 120,  # 镰刀高度（增加100%）
                                'angle': 0,  # 初始角度
                                'rotation_speed': self.sickle_field_rotation_speed,  # 旋转速度
                                'frame': 0,  # 当前帧
                                'is_active': True,  # 是否活跃
                                'image': random.choice(["149投掷物", "150投掷物", "151投掷物"])  # 随机使用149-151投掷物图片
                            })
                
                # 使用新技能：旋转跟随镰刀（冷却时间到了）
                if not self.is_sweeping and not self.is_dashing and not self.is_death_domain_active and not self.is_sickle_field_active and not self.is_rotating_follow_sickle_active and self.rotating_follow_sickle_cooldown <= 0:
                    if random.randint(1, 300) == 1:  # 约每5秒有1/300几率触发
                        # 更新last_skill属性
                        self.last_skill = "旋转跟随镰刀"
                        # 切换到魔法技能图片
                        self.current_image = "死神_魔法技能"
                        self.skill_image_timer = self.skill_image_duration
                        print(f"死神使用旋转跟随镰刀 - 发射6个正旋转镰刀！")
                        
                        # 开始技能
                        self.is_rotating_follow_sickle_active = True
                        self.rotating_follow_sickle_timer = 0
                        self.rotating_follow_sickle_cooldown = self.rotating_follow_sickle_cooldown_max
                        
                        # 发射6个镰刀，360°均匀分布
                        for i in range(self.rotating_follow_sickle_count):
                            # 计算发射角度
                            angle = (2 * math.pi / self.rotating_follow_sickle_count) * i
                            
                            # 计算发射位置
                            start_x = self.x + self.width // 2
                            start_y = self.y + self.height // 2
                            
                            # 计算目标位置（向外250像素）
                            target_x = start_x + math.cos(angle) * self.rotating_follow_sickle_launch_distance
                            target_y = start_y + math.sin(angle) * self.rotating_follow_sickle_launch_distance
                            
                            # 添加镰刀
                            self.rotating_follow_sickle_projectiles.append({
                                'x': target_x,  # 目标位置X
                                'y': target_y,  # 目标位置Y
                                'width': 60,  # 镰刀宽度（增加100%）
                                'height': 120,  # 镰刀高度（增加100%）
                                'angle': 0,  # 初始角度
                                'rotation_speed': self.rotating_follow_sickle_rotation_speed,  # 正旋转速度
                                'frame': 0,  # 当前帧
                                'initial_angle': angle,  # 初始发射角度，用于后续跟随计算
                                'image': random.choice(["149投掷物", "150投掷物", "151投掷物"])  # 随机使用149-151投掷物图片
                            })
                
                # 使用镰刀投掷技能（冷却时间到了）
                if not self.is_sweeping and not self.is_dashing and not self.is_death_domain_active and self.sickle_throw_cooldown <= 0:
                    if random.randint(1, 300) == 1:  # 约每5秒有1/300几率触发
                        # 更新last_skill属性
                        self.last_skill = "镰刀投掷"
                        # 切换到召唤投掷物图片
                        self.current_image = "死神_召唤投掷物"
                        self.skill_image_timer = self.skill_image_duration
                        print(f"死神使用镰刀投掷 - 投掷穿透性镰刀！")
                        
                        # 开始技能
                        self.sickle_throw_timer = 0
                        self.sickle_throw_cooldown = self.sickle_throw_cooldown_max
                        
                        # 计算投掷方向（向玩家方向）
                        if dist > 0:
                            dir_x = dx / dist
                            dir_y = dy / dist
                        else:
                            dir_x = 1  # 默认向右
                            dir_y = 0
                        
                        # 技能参数
                        projectile_speed = 15  # 投掷物速度
                        projectile_width = 30 * 4  # 宽度增加300%（30 -> 120）
                        projectile_height = 15 * 4  # 高度增加300%（15 -> 60）
                        max_travel_distance = 500  # 最大飞行距离（像素）
                        
                        # 投掷5个镰刀，带角度偏移
                        for i in range(5):
                            # 计算角度偏移（-30度到30度）
                            angle_offset = math.radians((i - 2) * 15)  # 每个镰刀偏移15度
                            # 计算当前镰刀的方向
                            current_dir_x = math.cos(angle_offset) * dir_x - math.sin(angle_offset) * dir_y
                            current_dir_y = math.sin(angle_offset) * dir_x + math.cos(angle_offset) * dir_y
                            
                            # 创建镰刀投掷物
                            self.sickle_projectiles.append({
                                'x': self.x + self.width // 2,  # 起始X位置（死神中心）
                                'y': self.y + self.height // 2,  # 起始Y位置（死神中心）
                                'vx': current_dir_x * projectile_speed,  # X速度
                                'vy': current_dir_y * projectile_speed,  # Y速度
                                'speed': projectile_speed,  # 速度大小
                                'max_distance': max_travel_distance,  # 最大飞行距离
                                'distance_traveled': 0,  # 已飞行距离
                                'is_returning': False,  # 是否正在返回
                                'has_hit_player': False,  # 是否已击中玩家
                                'width': projectile_width,  # 宽度
                                'height': projectile_height,  # 高度
                                'image': random.choice(["149投掷物", "150投掷物", "151投掷物"]),  # 随机使用149-151投掷物图片
                                'angle': 0,  # 初始角度
                                'rotation_speed': 5,  # 正旋转速度
                                'frame': 0  # 当前帧
                            })
                    
                    # 如果游戏有其他生物，也可以在这里添加对其他生物的伤害处理
                
                # 使用子弹风暴技能（冷却时间到了）
                if not self.is_sweeping and not self.is_dashing and not self.is_death_domain_active and not self.is_sickle_field_active and self.bullet_storm_cooldown <= 0:
                    if random.randint(1, 300) == 1:  # 约每5秒有1/300几率触发
                        # 更新last_skill属性
                        self.last_skill = "子弹风暴"
                        # 切换到魔法远程图片
                        self.current_image = "死神_魔法远程"
                        self.skill_image_timer = self.skill_image_duration
                        print(f"死神使用子弹风暴 - 发射12颗子弹！")
                        
                        # 开始技能
                        self.bullet_storm_cooldown = self.bullet_storm_cooldown_max
                        
                        # 发射12颗子弹，360°均匀分布
                        for i in range(self.bullet_storm_bullet_count):
                            # 计算发射角度
                            angle = (2 * math.pi / self.bullet_storm_bullet_count) * i
                            
                            # 计算发射位置
                            start_x = self.x + self.width // 2
                            start_y = self.y + self.height // 2
                            
                            # 计算初始速度向量（向外发射）
                            vx = math.cos(angle) * self.bullet_storm_speed
                            vy = math.sin(angle) * self.bullet_storm_speed
                            
                            # 初始化子弹位置在发射点
                            bullet_x = start_x
                            bullet_y = start_y
                            
                            # 计算初始角度（将弧度转换为角度，图片朝向右，需要调整）
                            initial_angle = math.degrees(angle)
                            
                            # 添加子弹
                            self.bullet_storm_projectiles.append({
                                'x': bullet_x,  # 子弹当前X位置
                                'y': bullet_y,  # 子弹当前Y位置
                                'start_x': start_x,  # 子弹发射点X位置
                                'start_y': start_y,  # 子弹发射点Y位置
                                'vx': vx,  # 子弹X方向速度
                                'vy': vy,  # 子弹Y方向速度
                                'width': self.bullet_storm_width,  # 子弹宽度
                                'height': self.bullet_storm_height,  # 子弹高度
                                'frame': 0,  # 当前帧
                                'has_turned': False,  # 是否已转向玩家
                                'damage': self.bullet_storm_damage,  # 子弹伤害
                                'image': self.bullet_storm_image,  # 子弹图片
                                'angle': initial_angle  # 子弹当前角度
                            })
            else:
                # 非Boss生物和非Boss召唤生物变为被动状态，但被攻击时会反击
                if self.mob_id not in [贝利亚, 吸血鬼, 肥胖Boss, 死神, 死神祝福]:
                    if self.is_attacked:  # 被攻击时反击
                        # 向玩家移动
                        if dist > self.attack_range:
                            # 计算移动方向
                            dir_x = dx / dist
                            dir_y = dy / dist
                            self.vel_x = dir_x * self.speed
                            self.direction = 1 if dir_x > 0 else -1
                            self.x += self.vel_x
                            
                            # 飞行生物可以在垂直方向上移动，增加惯性
                            if self.can_fly:
                                self.vel_y = self.vel_y * 0.8 + dir_y * self.fly_speed * 0.7  # 增加惯性，减少突然变化
                                self.y += self.vel_y
                        else:
                            # 在攻击范围内，停止移动并尝试攻击
                            self.vel_x = 0
                            if self.can_fly:
                                self.vel_y = 0
                            # 攻击玩家
                            self.attack(player)
                    else:
                        # 未被攻击时，随机移动
                        self.vel_x = self.direction * self.speed
                        self.x += self.vel_x
                        
                        # 飞行生物的随机垂直移动：增加惯性，减少突变
                        if self.can_fly:
                            # 偶尔小幅度改变垂直方向
                            if random.random() < 0.02:
                                # 小幅度调整，不直接设置
                                self.vel_y += random.uniform(-self.fly_speed * 0.5, self.fly_speed * 0.5)
                            # 限制垂直速度
                            self.vel_y = max(-self.fly_speed, min(self.vel_y, self.fly_speed))
                            # 增加空气阻力
                            self.vel_y *= 0.95
                            self.y += self.vel_y
                else:
                    # Boss生物的正常行为
                    # 向玩家移动
                    if dist > self.attack_range:
                        # 计算移动方向
                        dir_x = dx / dist
                        dir_y = dy / dist
                        self.vel_x = dir_x * self.speed
                        self.direction = 1 if dir_x > 0 else -1
                        self.x += self.vel_x
                        
                        # 飞行生物可以在垂直方向上移动，增加惯性
                        if self.can_fly:
                            self.vel_y = self.vel_y * 0.8 + dir_y * self.fly_speed * 0.7  # 增加惯性，减少突然变化
                            self.y += self.vel_y
                    else:
                        # 在攻击范围内，停止移动并尝试攻击
                        self.vel_x = 0
                        if self.can_fly:
                            self.vel_y = 0
                        # 攻击玩家
                        self.attack(player)
        else:
            # 不在视野范围内，随机移动
            self.vel_x = self.direction * self.speed
            self.x += self.vel_x
            
            # 飞行生物的随机垂直移动：增加惯性，减少突变
            if self.can_fly:
                # 偶尔小幅度改变垂直方向
                if random.random() < 0.02:
                    # 小幅度调整，不直接设置
                    self.vel_y += random.uniform(-self.fly_speed * 0.5, self.fly_speed * 0.5)
                # 限制垂直速度
                self.vel_y = max(-self.fly_speed, min(self.vel_y, self.fly_speed))
                # 增加空气阻力
                self.vel_y *= 0.95
                self.y += self.vel_y
        
        # 更新被攻击状态计时器
        if self.is_attacked:
            self.attacked_timer -= 1
            if self.attacked_timer <= 0:
                self.is_attacked = False
                self.attacked_timer = 0
        
        # 水平碰撞检测（飞行生物也需要水平碰撞检测）
        self.check_collision_x(world)
        
        # 强行向上移动处理
        if self.强行向上持续时间 > 0:
            # 应用向上的力
            self.y += self.强行向上力度
            self.强行向上持续时间 -= 1
            # 重置连续碰撞次数
            self.连续碰撞次数 = 0
        
        # 检查当前位置是否被方块占据（卡进方块） - 与掉落物系统一致的处理逻辑
        current_block_x = int(self.x // 32)
        current_block_y = int(self.y // 32)
        # 安全检查：确保世界高度和宽度有效
        if hasattr(world, '高度') and hasattr(world, '宽度'):
            if world.高度 is not None and world.宽度 is not None:
                if 0 <= current_block_y < world.高度 and 0 <= current_block_x < world.宽度:
                    block_id = world.get_block(current_block_x, current_block_y)
                    if block_id != 0:  # 0是空气
                        block = 方块属性.get(block_id, {})
                        if block.get("固体", False):
                            # 生物卡进了方块，向上推出
                            self.vel_y = -3  # 向上的速度
                            self.y = current_block_y * 32 - self.height  # 直接放在方块上方
        
        # 垂直移动和碰撞检测
        if not self.can_fly:
            # 非飞行生物的垂直移动和碰撞检测
            self.y += self.vel_y
            self.is_on_ground = False
            self.check_collision_y(world)
        else:
            # 飞行生物的垂直移动和碰撞检测
            self.y += self.vel_y
            # 飞行生物向下移动时不能穿透方块，向上可以
            self.check_collision_y_flying(world)
            # 确保飞行生物不会飞出屏幕范围
            if self.y < 0:
                self.y = 0
                self.vel_y = -self.vel_y * 0.5
            elif self.y > world.高度 * 32:
                self.y = world.高度 * 32
                self.vel_y = -self.vel_y * 0.5
        
        # 更新投掷物
        for proj in self.projectiles[:]:
            proj['timer'] -= 1
            if proj['timer'] <= 0:
                self.projectiles.remove(proj)
                continue
            
            # 追踪子弹的特殊处理 - 更新方向追踪玩家
            if proj.get('type') == 'homing_bullet' and proj['target']:
                # 检查是否还在追踪延迟时间内
                if proj.get('homing_delay') is not None:
                    if proj['homing_delay'] > 0:
                        # 还在延迟时间内，减少延迟时间，不进行追踪
                        proj['homing_delay'] -= 1
                    else:
                        # 延迟时间结束，开始追踪
                        # 计算当前位置到玩家的方向
                        target_dx = proj['target'].坐标_x - proj['x']
                        target_dy = proj['target'].坐标_y - proj['y']
                        target_dist = math.hypot(target_dx, target_dy)
                        
                        if target_dist > 0:
                            # 计算目标方向
                            target_dir_x = target_dx / target_dist
                            target_dir_y = target_dy / target_dist
                            
                            # 直接应用追踪加速度，不使用时间缩放因子，增强追踪效果
                            proj['vx'] += target_dir_x * proj.get('homing_speed', 5)
                            proj['vy'] += target_dir_y * proj.get('homing_speed', 5)
                            
                            # 保持子弹速度不变
                            current_speed = math.hypot(proj['vx'], proj['vy'])
                            if current_speed > 0:
                                proj['vx'] = (proj['vx'] / current_speed) * proj['speed']
                                proj['vy'] = (proj['vy'] / current_speed) * proj['speed']
                else:
                    # 没有延迟时间，直接追踪
                    # 计算当前位置到玩家的方向
                    target_dx = proj['target'].坐标_x - proj['x']
                    target_dy = proj['target'].坐标_y - proj['y']
                    target_dist = math.hypot(target_dx, target_dy)
                    
                    if target_dist > 0:
                        # 计算目标方向
                        target_dir_x = target_dx / target_dist
                        target_dir_y = target_dy / target_dist
                        
                        # 直接应用追踪加速度，不使用时间缩放因子，增强追踪效果
                        proj['vx'] += target_dir_x * proj.get('homing_speed', 5)
                        proj['vy'] += target_dir_y * proj.get('homing_speed', 5)
                        
                        # 保持子弹速度不变
                        current_speed = math.hypot(proj['vx'], proj['vy'])
                        if current_speed > 0:
                            proj['vx'] = (proj['vx'] / current_speed) * proj['speed']
                            proj['vy'] = (proj['vy'] / current_speed) * proj['speed']
            
            # 旋转子弹的特殊处理 - 更新旋转角度和方向
            elif proj.get('type') == 'rotating_bullet':
                # 更新旋转角度
                proj['rotation_angle'] += proj.get('rotation_dir', 0.1)
                
                # 计算旋转方向
                rot_dir_x = math.cos(proj['rotation_angle'])
                rot_dir_y = math.sin(proj['rotation_angle'])
                
                # 计算最终速度：旋转速度 + 向玩家方向移动的速度
                # 保持旋转速度的基础上，叠加向玩家方向的移动分量
                move_speed = proj.get('player_move_speed', 800)
                bullet_speed = proj['speed'] - move_speed  # 减去向玩家移动的速度，保持总速度不变
                final_vx = rot_dir_x * bullet_speed + proj.get('player_dir_x', 0) * move_speed
                final_vy = rot_dir_y * bullet_speed + proj.get('player_dir_y', 0) * move_speed
                
                # 更新子弹速度
                proj['vx'] = final_vx
                proj['vy'] = final_vy
                
                # 更新子弹角度，用于绘制
                proj['angle'] = -math.degrees(proj['rotation_angle'])
            
            # 更新位置
            proj['x'] += proj['vx'] * 0.016  # 假设60fps，每帧更新0.016秒
            proj['y'] += proj['vy'] * 0.016
            
            # 方块碰撞检测 - 投掷物无法穿透固态方块
            block_size = 32
            left_tile = int(proj['x'] // block_size)
            right_tile = int((proj['x'] + proj['width']) // block_size)
            top_tile = int(proj['y'] // block_size)
            bottom_tile = int((proj['y'] + proj['height']) // block_size)
            
            collided_with_block = False
            for y in range(top_tile, bottom_tile + 1):
                for x in range(left_tile, right_tile + 1):
                    if world.get_block(x, y) != 0:  # 0是空气
                        block = 方块属性.get(world.get_block(x, y), {})
                        if block.get("固体", False):
                            collided_with_block = True
                            break
                if collided_with_block:
                    break
            
            if collided_with_block:
                self.projectiles.remove(proj)
                continue
            
            # 检测与玩家或其他生物的碰撞
            if proj['target'] and proj in self.projectiles:
                # 处理玩家碰撞
                player_rect = pygame.Rect(proj['target'].坐标_x, proj['target'].坐标_y, proj['target'].宽, proj['target'].高)
                
                if proj.get('type') == 'laser':
                    # 对于激光，使用线段碰撞检测来避免隧道效应
                    prev_x = proj['x'] - proj['vx'] * 0.016
                    prev_y = proj['y'] - proj['vy'] * 0.016
                    
                    if player_rect.clipline((prev_x, prev_y), (proj['x'], proj['y'])):
                        proj['target'].take_damage(proj['damage'])
                        if proj in self.projectiles:
                            self.projectiles.remove(proj)
                else:
                    proj_rect = pygame.Rect(proj['x'], proj['y'], proj['width'], proj['height'])
                    if proj_rect.colliderect(player_rect):
                        proj['target'].take_damage(proj['damage'])
                        if proj in self.projectiles:
                            self.projectiles.remove(proj)
            
            # 处理与其他生物的碰撞（如果生物有game属性）
            if hasattr(self, 'game') and self.game and proj in self.projectiles:
                for mob in self.game.mobs[:]:
                    # 跳过自己
                    if mob == self:
                        continue
                    
                    mob_rect = pygame.Rect(mob.x, mob.y, mob.width, mob.height)
                    
                    if proj.get('type') == 'laser':
                        # 激光与生物的线段碰撞检测
                        prev_x = proj['x'] - proj['vx'] * 0.016
                        prev_y = proj['y'] - proj['vy'] * 0.016
                        if mob_rect.clipline((prev_x, prev_y), (proj['x'], proj['y'])):
                            # 生物受到伤害
                            mob.game = self.game  # 确保生物有game属性
                            死亡 = mob.take_damage(proj['damage'])
                            # 如果生物死亡，生成经验球（如果允许掉落）
                            if 死亡:
                                if not hasattr(mob, 'no_drop') or not mob.no_drop:
                                    self.game.spawn_exp_orbs(mob.x // 32, mob.y // 32)
                            if proj in self.projectiles:
                                self.projectiles.remove(proj)
                            break
                    else:
                        # 普通投掷物与生物的矩形碰撞检测
                        proj_rect = pygame.Rect(proj['x'], proj['y'], proj['width'], proj['height'])
                        if proj_rect.colliderect(mob_rect):
                            # 生物受到伤害
                            mob.game = self.game  # 确保生物有game属性
                            死亡 = mob.take_damage(proj['damage'])
                            # 如果生物死亡，生成经验球（如果允许掉落）
                            if 死亡:
                                if not hasattr(mob, 'no_drop') or not mob.no_drop:
                                    self.game.spawn_exp_orbs(mob.x // 32, mob.y // 32)
                            if proj in self.projectiles:
                                self.projectiles.remove(proj)
                            break
        
        # 更新所有爆炸特效（包括普通刺球的爆炸特效）
        for explosion in self.spike_explosions[:]:
            explosion['radius'] += explosion['max_radius'] / explosion['timer']
            explosion['timer'] -= 1
            if explosion['timer'] <= 0:
                self.spike_explosions.remove(explosion)
        
        # 更新肥胖Boss的落地特效
        if hasattr(self, 'landing_effects'):
            for effect in self.landing_effects[:]:
                # 计算总帧数和当前帧数
                total_frames = effect['duration'] * 60
                elapsed_frames = total_frames - (effect['lifetime'] * 60)
                # 计算半径（从0到max_radius线性增长）
                effect['radius'] = effect['max_radius'] * (elapsed_frames / total_frames)
                # 更新剩余生命周期
                effect['lifetime'] -= 1/60  # 每帧减少1/60秒
                if effect['lifetime'] <= 0:
                    self.landing_effects.remove(effect)
        
        # AI行为更新
        self.update_ai(world, player)
        
        # 边界检查
        if self.x < 0:
            self.x = 0
            self.direction = 1
        
        # 更新计时器
        self.move_timer += 1
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        if self.idle_timer > 0:
            self.idle_timer -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # 更新肥胖Boss的书技能
        if hasattr(self, 'books'):
            for book in self.books[:]:
                # 更新书的位置
                book['x'] += book['vx'] / 60  # 转换为每帧速度
                book['y'] += book['vy'] / 60
                
                # 更新书的旋转角度
                book['angle'] += book['angle_speed'] / 10
                
                # 更新书的计时器
                book['timer'] -= 1
                
                # 检测书是否与玩家碰撞
                player_rect = pygame.Rect(player.坐标_x, player.坐标_y, player.宽, player.高)
                book_rect = pygame.Rect(book['x'], book['y'], book['width'], book['height'])
                
                if player_rect.colliderect(book_rect):
                    # 玩家受到伤害
                    if hasattr(player, 'take_damage'):
                        player.take_damage(book['damage'], self)
                        
                        # 触发屏幕震动效果
                        if hasattr(player, 'game'):
                            # 为游戏对象添加震动效果属性
                            if not hasattr(player.game, 'screen_shake'):
                                player.game.screen_shake = 0
                            player.game.screen_shake = 10  # 震动10帧
                    
                    # 移除被碰撞的书
                    self.books.remove(book)
                elif book['timer'] <= 0:
                    # 时间到，移除书
                    self.books.remove(book)
        
        # 更新肥胖Boss的粉笔领域技能
        if hasattr(self, 'chalk_field_chalks'):
            # 获取当前Boss中心位置
            current_center_x = self.x + self.width // 2
            current_center_y = self.y + self.height // 2
            
            for chalk in self.chalk_field_chalks[:]:
                # 更新粉笔的旋转中心为Boss当前位置（跟随Boss移动）
                chalk['center_x'] = current_center_x
                chalk['center_y'] = current_center_y
                
                # 更新粉笔的角度
                chalk['angle'] += chalk['rotation_speed'] / 60  # 转换为每帧角度
                
                # 根据新角度和新中心计算新位置
                chalk['x'] = chalk['center_x'] + math.cos(chalk['angle']) * chalk['radius']
                chalk['y'] = chalk['center_y'] + math.sin(chalk['angle']) * chalk['radius']
                
                # 更新粉笔的计时器
                chalk['timer'] -= 1
                
                # 检测粉笔是否与玩家碰撞
                player_rect = pygame.Rect(player.坐标_x, player.坐标_y, player.宽, player.高)
                chalk_rect = pygame.Rect(chalk['x'], chalk['y'], chalk['width'], chalk['height'])
                
                if player_rect.colliderect(chalk_rect):
                    # 玩家受到伤害
                    if hasattr(player, 'take_damage'):
                        player.take_damage(chalk['damage'], self)
                    
                    # 移除被碰撞的粉笔
                    self.chalk_field_chalks.remove(chalk)
                elif chalk['timer'] <= 0:
                    # 时间到，移除粉笔
                    self.chalk_field_chalks.remove(chalk)
        
        # 更新肥胖Boss的念经技能
        if hasattr(self, 'chant_projectiles'):
            for projectile in self.chant_projectiles[:]:
                # 更新投掷物的位置
                projectile['x'] += projectile['vx'] / 60  # 转换为每帧速度
                projectile['y'] += projectile['vy'] / 60
                
                # 更新投掷物的计时器
                projectile['timer'] -= 1
                
                # 检测投掷物是否与玩家碰撞
                player_rect = pygame.Rect(player.坐标_x, player.坐标_y, player.宽, player.高)
                projectile_rect = pygame.Rect(projectile['x'], projectile['y'], projectile['width'], projectile['height'])
                
                if player_rect.colliderect(projectile_rect):
                    # 玩家受到伤害
                    if hasattr(player, 'take_damage'):
                        player.take_damage(projectile['damage'], self)
                        
                        # 触发屏幕震动效果
                        if hasattr(player, 'game'):
                            if not hasattr(player.game, 'screen_shake'):
                                player.game.screen_shake = 0
                            player.game.screen_shake = 8  # 震动8帧
                    
                    # 移除被碰撞的投掷物
                    self.chant_projectiles.remove(projectile)
                elif projectile['timer'] <= 0:
                    # 时间到，移除投掷物
                    self.chant_projectiles.remove(projectile)
        
        # 更新肥胖Boss的大叫技能
        if hasattr(self, 'is_shouting') and self.is_shouting:
            # 更新大叫帧数
            self.shout_frame += 1
            
            # 更新大叫特效
            for effect in self.shout_effects[:]:
                # 更新特效半径（线性增长）
                effect['radius'] += effect['max_radius'] / effect['timer']
                effect['timer'] -= 1
                effect['alpha'] -= 255 / self.shout_duration
                
                if effect['timer'] <= 0:
                    self.shout_effects.remove(effect)
            
            # 每5帧尝试造成一次伤害（直到达到最大伤害次数）
            if self.shout_frame % 5 == 0 and self.shout_damage_count < self.max_shout_damages:
                # 计算玩家与Boss的距离
                dx = player.坐标_x - (self.x + self.width // 2)
                dy = player.坐标_y - (self.y + self.height // 2)
                dist = math.hypot(dx, dy)
                
                # 最大效果距离300像素
                max_effect_distance = 300
                if dist < max_effect_distance:
                    # 距离越近，伤害越高
                    # 伤害计算：基础伤害10，最大伤害50，距离越近伤害越高
                    damage = 10 + int((1 - dist / max_effect_distance) * 40)
                    
                    # 玩家受到伤害
                    if hasattr(player, 'take_damage'):
                        player.take_damage(damage, self)
                        
                        # 触发屏幕震动效果
                        if hasattr(player, 'game'):
                            if not hasattr(player.game, 'screen_shake'):
                                player.game.screen_shake = 0
                            player.game.screen_shake = 5  # 震动5帧
                    
                    # 击退效果：距离越近，击退越强
                    knockback_strength = (1 - dist / max_effect_distance) * 30  # 增加击退强度到30
                    
                    # 确保玩家有速度属性
                    if hasattr(player, 'vel_x') and hasattr(player, 'vel_y'):
                        # 计算击退方向（远离Boss）
                        if dist > 0:
                            knockback_dir_x = dx / dist
                            knockback_dir_y = dy / dist
                        else:
                            knockback_dir_x = 1
                            knockback_dir_y = 0
                        
                        # 应用更强的击退
                        player.vel_x += knockback_dir_x * knockback_strength
                        player.vel_y += knockback_dir_y * knockback_strength
                        
                        # 确保玩家有坐标属性，直接添加位置偏移作为额外击退
                        if hasattr(player, '坐标_x') and hasattr(player, '坐标_y'):
                            player.坐标_x += knockback_dir_x * 5  # 额外位置偏移
                            player.坐标_y += knockback_dir_y * 5
                    
                    # 增加伤害次数
                    self.shout_damage_count += 1
            
            # 检查大叫是否结束
            if self.shout_frame >= self.shout_duration:
                self.is_shouting = False
                # 清空特效
                self.shout_effects.clear()
        
        # 更新技能图片计时器
        if self.skill_image_timer > 0:
            self.skill_image_timer -= 1
        elif self.current_image != self.default_image:
            # 技能图片持续时间结束，恢复到默认图片
            # 但吸血鬼狂暴状态特殊处理：保持吸血鬼_狂暴图片
            if not (self.mob_id == 吸血鬼 and self.current_image == "吸血鬼_狂暴"):
                self.current_image = self.default_image
                print(f"生物 {self.name} - 恢复到默认图片: {self.current_image}")
            else:
                # 吸血鬼狂暴状态持续保持狂暴图片
                print(f"吸血鬼持续保持狂暴图片: {self.current_image}")
    
    def attack(self, player):
        """攻击玩家"""
        if self.attack_cooldown <= 0:
            # 使用距离检测而不是严格的碰撞检测，这样生物更容易攻击到玩家
            dx = player.坐标_x - self.x
            dy = player.坐标_y - self.y
            dist = math.hypot(dx, dy)
            
            # 检查是否在攻击范围内
            if dist < self.attack_range:
                # 玩家受到伤害
                if hasattr(player, 'take_damage'):
                    # 灵魂收割被动技能：对生命值低于10%的敌人造成致命一击
                    if self.mob_id == 死神:
                        # 检查玩家是否有max_health和current_health属性
                        if hasattr(player, 'max_health') and hasattr(player, 'current_health'):
                            # 检查玩家生命值是否低于10%
                            if player.current_health <= player.max_health * 0.1:
                                # 造成致命伤害
                                player.take_damage(99999999, self)
                                print(f"死神使用灵魂收割 - 对生命值低于10%的玩家造成致命一击！")
                            else:
                                # 正常伤害
                                player.take_damage(self.damage, self)
                        else:
                            # 无法获取玩家生命值信息，使用正常伤害
                            player.take_damage(self.damage, self)
                    else:
                        # 其他生物使用正常伤害
                        player.take_damage(self.damage)
                # 更新last_skill属性
                if self.mob_id == 贝利亚:  # 贝利亚需要更新技能追踪
                    self.last_skill = "近战攻击"
                    # 切换到近战攻击图片
                    self.current_image = "贝利亚_近战攻击"
                    self.skill_image_timer = self.skill_image_duration
                    print(f"贝利亚使用近战攻击 - 切换到图片: {self.current_image}")
                elif self.mob_id == 吸血鬼:  # 吸血鬼需要更新技能追踪
                    self.last_skill = "近战攻击"
                    # 切换到近战攻击图片
                    self.current_image = "吸血鬼_近战攻击"
                    self.skill_image_timer = self.skill_image_duration
                    print(f"吸血鬼使用近战攻击 - 切换到图片: {self.current_image}")
                elif self.mob_id == 肥胖Boss:  # 肥胖Boss需要更新技能追踪
                    self.last_skill = "近战攻击"
                    # 切换到近战攻击图片
                    self.current_image = "肥婆_近战攻击"
                    self.skill_image_timer = self.skill_image_duration
                    print(f"肥胖Boss使用近战攻击 - 切换到图片: {self.current_image}")
                elif self.mob_id == 死神:  # 死神需要更新技能追踪
                    self.last_skill = "近战攻击"
                    # 切换到近战攻击图片
                    self.current_image = "死神_近战攻击"
                    self.skill_image_timer = self.skill_image_duration
                    print(f"死神使用近战攻击 - 切换到图片: {self.current_image}")
                # 重置攻击冷却
                self.attack_cooldown = self.attack_cooldown_max
    
    def take_damage(self, damage):
        """受到伤害"""
        # 被攻击状态标记，持续3秒（180帧）
        self.is_attacked = True
        self.attacked_timer = 180
        
        # 如果有护盾，先消耗护盾值
        if hasattr(self, 'shield_value') and self.shield_value > 0:
            # 根据生物类型使用正确的护盾最大值属性
            if self.mob_id == 死神:
                max_shield = self.max_shield_value
            else:
                max_shield = self.shield_max if hasattr(self, 'shield_max') else 100
                
            if self.shield_value >= damage:
                # 护盾完全吸收伤害
                self.shield_value -= damage
                damage = 0
                if self.mob_id == 死神:
                    print(f"死神护盾吸收伤害 - 剩余护盾: {self.shield_value}/{max_shield}")
                else:
                    print(f"护盾吸收伤害 - 剩余护盾: {self.shield_value}/{max_shield}")
            else:
                # 护盾部分吸收伤害，剩余伤害影响生命值
                damage -= self.shield_value
                self.shield_value = 0
                if self.mob_id == 死神:
                    print(f"死神护盾已耗尽 - 剩余伤害: {damage}")
                else:
                    print(f"护盾已耗尽 - 剩余伤害: {damage}")
        
        # 扣除剩余伤害
        if damage > 0:
            self.health -= damage
        
        # 死神特殊能力：血量低于20%时瞬间满血，1秒后死亡
        if self.mob_id == 死神:
            # 初始化死神特殊状态属性
            if not hasattr(self, 'special_activated'):
                self.special_activated = False
                self.death_timer = 0
            
            # 检查是否触发特殊能力
            health_percentage = self.health / self.max_health
            if health_percentage <= 0.2 and not self.special_activated:
                print("死神触发特殊能力：瞬间满血！1秒后消失！")
                # 瞬间满血
                self.health = self.max_health
                # 激活特殊状态
                self.special_activated = True
                # 重置死亡计时器（60帧 = 1秒）
                self.death_timer = 60
        
        # 如果是BOSS，更新boss_manager的当前BOSS
        if self.mob_id == 贝利亚 or self.mob_id == 吸血鬼 or self.mob_id == 肥胖Boss or self.mob_id == 死神:
            from boos生物处理 import boss_manager
            boss_manager.current_boss = self
        
        # 创建伤害数字的代码已移除，避免依赖DamageText类
        
        return self.health <= 0  # 返回是否死亡
    
    def is_alive(self):
        """检查生物是否存活"""
        return self.health > 0
    
    def create_death_sickle(self, player):
        """
        创建死神镰刀掉落物，带特效
        """
        print("创建死神镰刀掉落物！")
        
        # 计算掉落物的方块坐标
        block_x = int((self.x + self.width // 2) // 32)
        block_y = int((self.y + self.height // 2) // 32)
        
        # 导入所需模块和常量
        from 物品定义 import 死神的镰刀
        
        # 直接获取世界实例
        world = getattr(self, 'game', None)
        
        # 检查世界中是否已经存在死神的镰刀，如果存在则不创建新的
        if world and hasattr(world, 'items'):
            for item in world.items:
                if hasattr(item, 'item_id') and item.item_id == 死神的镰刀:
                    print(f"世界中已存在死神的镰刀，不重复创建")
                    return
        
        # 使用世界的spawn_item方法创建掉落物
        if world and hasattr(world, 'spawn_item'):
            world.spawn_item(
                block_x,  # 方块坐标X
                block_y,  # 方块坐标Y
                死神的镰刀,  # 物品ID
                1,  # 数量
                is_special=True,  # 标记为特殊掉落物
                special_type="death_sickle",  # 特殊类型
                target_player=player  # 目标玩家
            )
            print(f"已通过spawn_item创建死神的镰刀，坐标：({block_x}, {block_y})")
        
        print(f"死神的镰刀创建成功，方块坐标：({block_x}, {block_y})")


    
    def draw_health_bar(self, screen, x, y):
        """绘制生物生命值条和护盾条"""
        # 贝利亚、吸血鬼、肥胖Boss和死神不显示普通血条（只显示BOSS血条）
        if self.mob_id == 20051 or self.mob_id == 20016 or self.mob_id == 肥胖Boss or self.mob_id == 死神:  # 20051是贝利亚的ID，20016是吸血鬼的ID，肥胖Boss和死神使用常量
            # 但是死神需要显示护盾条
            if self.mob_id == 死神 and hasattr(self, 'shield_value') and self.shield_value > 0:
                # 计算护盾条的位置和大小
                bar_width = self.width
                bar_height = 4
                bar_x = x
                bar_y = y - 12  # 护盾条在生物上方，生命值条的上方
                
                # 计算护盾比例
                # 死神使用max_shield_value，其他生物可能使用shield_max
                if hasattr(self, 'max_shield_value'):
                    max_shield = self.max_shield_value
                elif hasattr(self, 'shield_max'):
                    max_shield = self.shield_max
                else:
                    max_shield = 1200  # 默认值
                shield_ratio = self.shield_value / max_shield
                
                # 绘制护盾条背景
                pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))
                
                # 绘制当前护盾值（蓝色）
                current_width = int(bar_width * shield_ratio)
                pygame.draw.rect(screen, (0, 0, 255), (bar_x, bar_y, current_width, bar_height))
            return
            
        # 1. 满血时不显示血条
        if self.health >= self.max_health:
            return
        
        # 计算生命值条的位置和大小
        bar_width = self.width
        bar_height = 4
        bar_x = x
        bar_y = y - 8  # 生命值条在生物上方
        
        # 计算生命值比例
        health_ratio = self.health / self.max_health
        
        # 绘制生命值条背景
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # 根据生命值比例绘制不同颜色的生命值条
        if health_ratio > 0.7:
            health_color = (0, 255, 0)  # 绿色
        elif health_ratio > 0.3:
            health_color = (255, 255, 0)  # 黄色
        else:
            health_color = (255, 0, 0)  # 红色
        
        # 绘制当前生命值
        current_width = int(bar_width * health_ratio)
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, current_width, bar_height))
    
    def check_collision_x(self, world):
        """水平碰撞检测"""
        block_size = 32  # 方块大小
        left_tile = int(self.x // block_size)
        right_tile = int((self.x + self.width) // block_size)
        top_tile = int(self.y // block_size)
        bottom_tile = int((self.y + self.height - 1) // block_size)
        
        collided = False
        for y in range(top_tile, bottom_tile + 1):
            for x in [left_tile, right_tile]:
                block_id = world.get_block(x, y)
                if block_id != 0:  # 0是空气
                    # 肥胖Boss穿透植物方块：木头(10004)、乔木(10026)、仙人掌(10025)
                    plant_blocks = [10004, 10026, 10025]
                    if self.mob_id == 肥胖Boss and block_id in plant_blocks:
                        continue  # 穿透植物方块
                    
                    block = 方块属性.get(block_id, {})
                    if block.get("固体", False):
                        if self.vel_x > 0:  # 向右移动
                            self.x = x * block_size - self.width
                            self.direction = -1  # 转向左
                        elif self.vel_x < 0:  # 向左移动
                            self.x = (x + 1) * block_size
                            self.direction = 1  # 转向右
                        self.vel_x = 0
                        self.idle_timer = 30  # 短暂停留后再移动
                        collided = True
        
        # 卡方块检测：如果位置几乎没变且发生了碰撞，增加连续碰撞次数
        if collided and abs(self.x - self.上次位置) < 1:
            self.连续碰撞次数 += 1
        else:
            self.连续碰撞次数 = 0
        
        # 更新上次位置
        self.上次位置 = self.x
        
        # 如果连续碰撞次数过多，触发强行向上移动
        if self.连续碰撞次数 > 10:  # 连续碰撞10帧（约0.17秒）判定为卡住
            self.强行向上力度 = -15  # 向上的力度
            self.强行向上持续时间 = 5  # 持续5帧
        
        return collided
    
    def check_collision_y(self, world):
        """垂直碰撞检测"""
        block_size = 32  # 方块大小
        left_tile = int(self.x // block_size)
        right_tile = int((self.x + self.width - 1) // block_size)
        top_tile = int(self.y // block_size)
        bottom_tile = int((self.y + self.height) // block_size)
        
        for x in range(left_tile, right_tile + 1):
            for y in [top_tile, bottom_tile]:
                block_id = world.get_block(x, y)
                if block_id != 0:  # 0是空气
                    # 肥胖Boss穿透植物方块：木头(10004)、乔木(10026)、仙人掌(10025)
                    plant_blocks = [10004, 10026, 10025]
                    if self.mob_id == 肥胖Boss and block_id in plant_blocks:
                        continue  # 穿透植物方块
                    
                    block = 方块属性.get(block_id, {})
                    if block.get("固体", False):
                        if self.vel_y > 0:  # 下落
                            self.y = y * block_size - self.height
                            self.is_on_ground = True
                        elif self.vel_y < 0:  # 上升
                            self.y = (y + 1) * block_size
                        self.vel_y = 0
                        return True
        return False
    
    def check_collision_y_flying(self, world):
        """飞行生物的垂直碰撞检测 - 向下不能穿透方块，向上可以"""
        block_size = 32  # 方块大小
        left_tile = int(self.x // block_size)
        right_tile = int((self.x + self.width - 1) // block_size)
        bottom_tile = int((self.y + self.height) // block_size)
        
        # 只检查底部碰撞（向下移动时）
        if self.vel_y > 0:  # 只有向下移动时才检测碰撞
            for x in range(left_tile, right_tile + 1):
                block_id = world.get_block(x, bottom_tile)
                if block_id != 0:  # 0是空气
                    # 肥胖Boss穿透植物方块：木头(10004)、乔木(10026)、仙人掌(10025)
                    plant_blocks = [10004, 10026, 10025]
                    if self.mob_id == 肥胖Boss and block_id in plant_blocks:
                        continue  # 穿透植物方块
                    
                    block = 方块属性.get(block_id, {})
                    if block.get("固体", False):
                        # 调整位置到方块顶部
                        self.y = bottom_tile * block_size - self.height
                        self.vel_y = 0
                        return True
        return False
    
    def can_jump_over_obstacle(self, world):
        """检查前方是否有需要跳跃的障碍物"""
        block_size = 32
        check_distance = self.jump_obstacle_range
        
        # 根据方向确定检查位置
        if self.direction > 0:  # 向右
            front_x = int((self.x + self.width) // block_size) + 1
        else:  # 向左
            front_x = int(self.x // block_size) - 1
        
        # 检查前方是否有方块阻挡
        for i in range(check_distance):
            check_x = front_x + i * self.direction
            foot_y = int((self.y + self.height) // block_size)
            head_y = int(self.y // block_size)
            
            # 检查脚部高度是否有方块
            if world.get_block(check_x, foot_y) != 0:
                # 检查头部高度是否可以通过
                if world.get_block(check_x, head_y) == 0:
                    return True
        return False
    
    def should_jump(self, world):
        """判断是否应该跳跃"""
        # 冷却期间不跳跃
        if self.jump_cooldown > 0:
            return False
        
        # 不在地面上不能跳跃
        if not self.is_on_ground:
            return False
        
        # 随机跳跃（增加行为多样性）
        if random.random() < 0.01:  # 1%的几率随机跳跃
            return True
        
        # 前方有可跳跃的障碍物
        if self.can_jump_over_obstacle(world):
            return True
        
        return False
    
    def should_turn_around(self, world):
        """检查是否应该转身（前方是悬崖）"""
        block_size = 32
        # 根据方向检查前方是否有地面
        if self.direction > 0:  # 向右
            check_x = int((self.x + self.width) // block_size) + 1
        else:  # 向左
            check_x = int(self.x // block_size) - 1
        
        ground_y = int((self.y + self.height) // block_size) + 1
        
        # 检查前方一格是否有地面支撑
        if world.get_block(check_x, ground_y) == 0:
            return True
        return False
    
    def update_ai(self, world, player):
        """更新AI行为"""
        # 降低AI评估频率，每120帧重新评估一次行为，减少计算量
        if self.move_timer >= 120:
            self.move_timer = 0
            
            # 20%的几率改变方向，降低随机计算频率
            if random.random() < 0.2:
                self.direction = random.choice([-1, 1])
            
            # 5%的几率短暂停留，降低随机计算频率
            if random.random() < 0.05:  # 5%的几率短暂停留
                self.idle_timer = random.randint(60, 180)  # 1-3秒，延长停留时间
        
        # 停留期间不移动
        if self.idle_timer > 0:
            self.vel_x = 0
            if self.can_fly:
                self.vel_y = 0
            return
        
        # 对于非飞行生物，检查是否需要转身和跳跃
        if not self.can_fly:
            # 检查是否需要转身
            if self.should_turn_around(world):
                self.direction *= -1
                self.idle_timer = 30  # 转身后短暂停留
            
            # 检查是否需要跳跃
            if self.should_jump(world):
                self.jump()
    
    def jump(self):
        """跳跃"""
        if self.is_on_ground:
            # 肥胖Boss特殊跳跃逻辑：30%概率触发超级跳跃
            if self.mob_id == 肥胖Boss:
                # 30%概率触发超级跳跃
                if random.random() < 0.3:
                    # 超级跳跃：更强的跳跃力度，落地造成伤害
                    # 更强的跳跃力度（原始跳跃强度的2倍）
                    self.vel_y = self.jump_strength * 2
                    # 标记为超级跳跃，用于落地时检测
                    self.is_super_jump = True
                else:
                    # 普通跳跃
                    self.vel_y = self.jump_strength
                    # 清除超级跳跃标记
                    self.is_super_jump = False
            else:
                # 其他生物普通跳跃
                self.vel_y = self.jump_strength
            
            self.is_on_ground = False
            self.jump_cooldown = 30  # 跳跃冷却时间
    
    def draw(self, screen, camera_x, camera_y):
        """绘制生物"""
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # 尝试加载生物图片
        mob_image = None
        try:
            from 图片加载 import 图片管理器
            if 图片管理器 is not None:
                # 优先使用当前技能图片（如果有）
                if hasattr(self, 'current_image') and 图片管理器.图片是否已加载(self.current_image):
                    mob_image = 图片管理器.获取图片(self.current_image)
                # 1. 直接使用生物名称
                if mob_image is None and 图片管理器.图片是否已加载(self.name):
                    mob_image = 图片管理器.获取图片(self.name)
                # 2. 尝试添加"小"前缀
                if mob_image is None and 图片管理器.图片是否已加载(f"小{self.name}"):
                    mob_image = 图片管理器.获取图片(f"小{self.name}")
                # 3. 特殊处理：幽灵 -> 小幽灵
                if mob_image is None and self.name == "幽灵" and 图片管理器.图片是否已加载("小幽灵"):
                    mob_image = 图片管理器.获取图片("小幽灵")
                # 4. 特殊处理：蝙蝠 -> 小蝙蝠
                if mob_image is None and self.name == "蝙蝠" and 图片管理器.图片是否已加载("小蝙蝠"):
                    mob_image = 图片管理器.获取图片("小蝙蝠")
                # 5. 特殊处理：死神祝福 -> 死神_祝福（优先）
                if mob_image is None and self.name == "死神祝福" and 图片管理器.图片是否已加载("死神_祝福"):
                    mob_image = 图片管理器.获取图片("死神_祝福")
                # 6. 其次尝试小死神祝福
                if mob_image is None and self.name == "死神祝福" and 图片管理器.图片是否已加载("小死神祝福"):
                    mob_image = 图片管理器.获取图片("小死神祝福")

        except Exception as e:
            # 图片加载失败，使用默认色块
            pass
        
        if mob_image:
            # 有图片时绘制图片
            # 缩放图片到生物尺寸
            scaled_image = pygame.transform.scale(mob_image, (self.width, self.height))
            # 根据生物朝向翻转图片
            if not self.direction > 0:  # 向左看时翻转图片
                scaled_image = pygame.transform.flip(scaled_image, True, False)
            
            # 狂暴状态特效：增加20%红色
            if hasattr(self, 'is_raging') and self.is_raging:
                # 创建红色滤镜表面
                red_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                # 使用20%透明度的红色叠加
                red_surface.fill((255, 0, 0, 51))  # 51是20%的255
                # 将红色滤镜叠加到图片上
                scaled_image.blit(red_surface, (0, 0), special_flags=pygame.BLEND_ADD)
            
            # 绘制图片
            screen.blit(scaled_image, (screen_x, screen_y))
        else:
            # 没有图片时绘制默认色块
            # 绘制生物身体
            mob_rect = pygame.Rect(screen_x, screen_y, self.width, self.height)
            pygame.draw.rect(screen, self.color, mob_rect)
            
            # 绘制生物眼睛（显示方向）
            eye_offset = 4
            if self.direction > 0:  # 向右看
                eye_x = screen_x + self.width - 8
            else:  # 向左看
                eye_x = screen_x + 4
            
            pygame.draw.circle(screen, (0, 0, 0), (eye_x, screen_y + 10), 3)
            pygame.draw.circle(screen, (255, 255, 255), (eye_x, screen_y + 10), 1)
        
        # 绘制生命值条
        self.draw_health_bar(screen, screen_x, screen_y)
        
        # 绘制肥胖Boss的书技能
        if hasattr(self, 'books'):
            for book in self.books:
                book_screen_x = book['x'] - camera_x
                book_screen_y = book['y'] - camera_y
                
                # 绘制书的基本形状（矩形代表书）
                book_rect = pygame.Rect(book_screen_x, book_screen_y, book['width'], book['height'])
                
                # 绘制书的封面（红色）
                pygame.draw.rect(screen, (150, 0, 0), book_rect)
                
                # 绘制书的白色边缘
                pygame.draw.rect(screen, (255, 255, 255), book_rect, 2)
                
                # 绘制书的页面（内部白色矩形）
                page_rect = pygame.Rect(book_screen_x + 5, book_screen_y + 5, book['width'] - 10, book['height'] - 10)
                pygame.draw.rect(screen, (255, 255, 255), page_rect)
                
                # 绘制书的文字线（黑色线条）
                for i in range(4):
                    line_y = book_screen_y + 10 + i * 5
                    pygame.draw.line(screen, (0, 0, 0), 
                                    (book_screen_x + 7, line_y), 
                                    (book_screen_x + book['width'] - 7, line_y), 1)
        
        # 绘制肥胖Boss的粉笔领域技能
        if hasattr(self, 'chalk_field_chalks'):
            for chalk in self.chalk_field_chalks:
                chalk_screen_x = chalk['x'] - camera_x
                chalk_screen_y = chalk['y'] - camera_y
                
                # 绘制粉笔的基本形状（矩形代表粉笔）
                chalk_rect = pygame.Rect(chalk_screen_x, chalk_screen_y, chalk['width'], chalk['height'])
                
                # 绘制粉笔的主体（白色）
                pygame.draw.rect(screen, (255, 255, 255), chalk_rect)
                
                # 绘制粉笔的红色尖端
                tip_rect = pygame.Rect(chalk_screen_x + chalk['width'] - 3, chalk_screen_y + 1, 3, chalk['height'] - 2)
                pygame.draw.rect(screen, (255, 0, 0), tip_rect)
                
                # 绘制粉笔的黑色线条
                line_y = chalk_screen_y + chalk['height'] // 2
                pygame.draw.line(screen, (0, 0, 0), 
                                (chalk_screen_x, line_y), 
                                (chalk_screen_x + chalk['width'], line_y), 1)
        
        # 绘制肥胖Boss的念经技能
        if hasattr(self, 'chant_projectiles'):
            for projectile in self.chant_projectiles:
                # 计算屏幕上的位置
                projectile_screen_x = projectile['x'] - camera_x
                projectile_screen_y = projectile['y'] - camera_y
                
                # 渲染中文句子（不要背景，直接显示文本）
                try:
                    # 创建字体对象，支持中文
                    font = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial Unicode MS'], 16)
                    
                    # 渲染文本，直接显示，没有背景
                    text_surface = font.render(projectile['sentence'], True, (255, 255, 255))
                    
                    # 计算文本位置（左上角对齐）
                    text_x = projectile_screen_x
                    text_y = projectile_screen_y
                    
                    # 绘制文本
                    screen.blit(text_surface, (text_x, text_y))
                except Exception as e:
                    # 字体渲染失败时，绘制简单的红色文本
                    try:
                        # 尝试使用默认字体绘制
                        default_font = pygame.font.Font(None, 16)
                        error_surface = default_font.render("文本渲染失败", True, (255, 0, 0))
                        screen.blit(error_surface, (projectile_screen_x, projectile_screen_y))
                    except:
                        pass
        
        # 绘制肥胖Boss的大叫技能特效
        if hasattr(self, 'shout_effects'):
            for effect in self.shout_effects:
                # 计算屏幕上的位置
                effect_screen_x = effect['x'] - camera_x
                effect_screen_y = effect['y'] - camera_y
                
                # 创建足够大的半透明表面
                surface_size = int(effect['max_radius'] * 2)
                effect_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
                center = (surface_size // 2, surface_size // 2)
                
                # 绘制主圈（更宽的线）
                pygame.draw.circle(
                    effect_surface,
                    (effect['color'][0], effect['color'][1], effect['color'][2], int(effect['alpha'])),
                    center,
                    int(effect['radius']),
                    10  # 线宽增加到10像素，更明显
                )
                
                # 绘制内圈光晕效果
                pygame.draw.circle(
                    effect_surface,
                    (effect['color'][0], effect['color'][1], effect['color'][2], int(effect['alpha'] * 0.3)),
                    center,
                    int(effect['radius'] * 0.9),
                    5  # 线宽5像素
                )
                
                # 绘制外圈光晕效果
                pygame.draw.circle(
                    effect_surface,
                    (effect['color'][0], effect['color'][1], effect['color'][2], int(effect['alpha'] * 0.2)),
                    center,
                    int(effect['radius'] * 1.1),
                    3  # 线宽3像素
                )
                
                # 绘制中心亮点
                pygame.draw.circle(
                    effect_surface,
                    (255, 255, 255, int(effect['alpha'])),
                    center,
                    15  # 半径15像素，更大的中心亮点
                )
                
                # 绘制中心光晕
                glow_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
                pygame.draw.circle(
                    glow_surface,
                    (effect['color'][0], effect['color'][1], effect['color'][2], int(effect['alpha'] * 0.4)),
                    center,
                    30  # 更大的中心光晕
                )
                effect_surface.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_ADD)
                
                # 绘制到屏幕上
                screen.blit(
                    effect_surface,
                    (effect_screen_x - surface_size // 2, effect_screen_y - surface_size // 2)
                )
        
        # 绘制投掷物
        for proj in getattr(self, 'projectiles', []) + getattr(self, 'sickle_projectiles', []):
            proj_screen_x = proj['x'] - camera_x
            proj_screen_y = proj['y'] - camera_y
            
            # 特殊处理贝利亚的激光攻击，绘制黑激光束
            if proj.get('type') == 'laser':
                # 计算激光起点和终点
                start_x = proj.get('start_x', proj['x'] - proj['vx'] * 0.1) - camera_x
                start_y = proj.get('start_y', proj['y'] - proj['vy'] * 0.1) - camera_y
                end_x = proj_screen_x
                end_y = proj_screen_y
                
                # 绘制黑激光束，线宽18像素（再增加200%，总计600%于初始值）
                pygame.draw.line(screen, (0, 0, 0), (start_x, start_y), (end_x, end_y), 18)
                continue
            
            # 尝试加载并绘制投掷物图片
            try:
                from 图片加载 import 图片管理器
                
                # 检查是否为追踪子弹且有颜色属性
                is_purple_bullet = proj.get('type') == 'homing_bullet' and proj.get('color')
                
                # 检查是否为骨头类型子弹（bone）
                is_bone_bullet = proj.get('type') == 'bone'
                
                if is_purple_bullet:
                    # 绘制紫色子弹
                    radius = proj['width'] // 2
                    center_x = proj_screen_x + radius
                    center_y = proj_screen_y + radius
                    pygame.draw.circle(screen, proj['color'], (center_x, center_y), radius)
                elif is_bone_bullet:
                    # 绘制骨头类型子弹，和吸血鬼召唤的异变骷髅一样
                    # 绘制骨头形状：白色主体+红色外框+左右骨节
                    # 主骨 - 白色主体，红色轮廓
                    main_rect = pygame.Rect(proj_screen_x, proj_screen_y, proj['width'], proj['height'])
                    pygame.draw.rect(screen, (200, 0, 0), main_rect.inflate(4, 4))  # 红色外框
                    pygame.draw.rect(screen, (255, 255, 255), main_rect)  # 白色主体
                    # 骨节 - 白色主体，红色轮廓
                    joint_radius = proj['width'] // 3
                    # 左侧骨节
                    pygame.draw.circle(screen, (200, 0, 0), 
                                     (proj_screen_x, proj_screen_y + proj['height'] // 2), 
                                     joint_radius + 2)  # 红色外框
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (proj_screen_x, proj_screen_y + proj['height'] // 2), 
                                     joint_radius)  # 白色主体
                    # 右侧骨节
                    pygame.draw.circle(screen, (200, 0, 0), 
                                     (proj_screen_x + proj['width'], proj_screen_y + proj['height'] // 2), 
                                     joint_radius + 2)  # 红色外框
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (proj_screen_x + proj['width'], proj_screen_y + proj['height'] // 2), 
                                     joint_radius)  # 白色主体
                elif 图片管理器 is not None:
                    # 尝试加载投掷物图片，使用投掷物的image属性
                    if 图片管理器.图片是否已加载(proj['image']):
                        proj_image = 图片管理器.获取图片(proj['image'])
                        # 先将图片缩放到合适大小
                        scaled_image = pygame.transform.scale(proj_image, (proj['width'], proj['height']))
                        # 旋转图片
                        rotated_image = pygame.transform.rotate(scaled_image, proj.get('angle', 0))
                        # 获取旋转后的图片尺寸
                        rotated_rect = rotated_image.get_rect(center=(proj_screen_x + proj['width']//2, proj_screen_y + proj['height']//2))
                        # 绘制旋转后的图片
                        screen.blit(rotated_image, rotated_rect.topleft)
                    else:
                        # 如果图片未加载，绘制黑色球体作为备用
                        radius = proj['width'] // 2
                        center_x = proj_screen_x + radius
                        center_y = proj_screen_y + radius
                        pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius)
                else:
                    # 如果图片管理器不可用，绘制黑色球体
                    radius = proj['width'] // 2
                    center_x = proj_screen_x + radius
                    center_y = proj_screen_y + radius
                    pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius)
            except Exception as e:
                # 发生错误时，检查是否为紫色子弹或骨头子弹
                is_purple_bullet = proj.get('type') == 'homing_bullet' and proj.get('color')
                is_bone_bullet = proj.get('type') == 'bone'
                
                if is_purple_bullet:
                    # 绘制紫色子弹
                    radius = proj['width'] // 2
                    center_x = proj_screen_x + radius
                    center_y = proj_screen_y + radius
                    pygame.draw.circle(screen, proj['color'], (center_x, center_y), radius)
                elif is_bone_bullet:
                    # 绘制骨头类型子弹，和吸血鬼召唤的异变骷髅一样
                    # 绘制骨头形状：白色主体+红色外框+左右骨节
                    # 主骨 - 白色主体，红色轮廓
                    main_rect = pygame.Rect(proj_screen_x, proj_screen_y, proj['width'], proj['height'])
                    pygame.draw.rect(screen, (200, 0, 0), main_rect.inflate(4, 4))  # 红色外框
                    pygame.draw.rect(screen, (255, 255, 255), main_rect)  # 白色主体
                    # 骨节 - 白色主体，红色轮廓
                    joint_radius = proj['width'] // 3
                    # 左侧骨节
                    pygame.draw.circle(screen, (200, 0, 0), 
                                     (proj_screen_x, proj_screen_y + proj['height'] // 2), 
                                     joint_radius + 2)  # 红色外框
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (proj_screen_x, proj_screen_y + proj['height'] // 2), 
                                     joint_radius)  # 白色主体
                    # 右侧骨节
                    pygame.draw.circle(screen, (200, 0, 0), 
                                     (proj_screen_x + proj['width'], proj_screen_y + proj['height'] // 2), 
                                     joint_radius + 2)  # 红色外框
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (proj_screen_x + proj['width'], proj_screen_y + proj['height'] // 2), 
                                     joint_radius)  # 白色主体
                else:
                    # 绘制黑色球体作为备用
                    radius = proj['width'] // 2
                    center_x = proj_screen_x + radius
                    center_y = proj_screen_y + radius
                    pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius)
        
        # 绘制死神的镰刀横扫特效
        if hasattr(self, 'sweep_effects'):
            for effect in self.sweep_effects:
                # 计算屏幕上的位置
                effect_screen_x = effect['x'] - camera_x
                effect_screen_y = effect['y'] - camera_y
                
                # 计算镰刀的旋转角度范围（180°）
                angle_step = math.pi / 20  # 20个点绘制扇形
                for i in range(21):
                    # 计算当前角度
                    current_angle = effect['start_angle'] + i * angle_step
                    # 计算扇形边缘的点
                    outer_x = effect_screen_x + math.cos(current_angle) * effect['range'] * effect['scale']
                    outer_y = effect_screen_y + math.sin(current_angle) * effect['range'] * effect['scale']
                    inner_x = effect_screen_x + math.cos(current_angle) * (effect['range'] - effect['width']) * effect['scale']
                    inner_y = effect_screen_y + math.sin(current_angle) * (effect['range'] - effect['width']) * effect['scale']
                    
                    # 绘制扇形边缘线
                    pygame.draw.line(
                        screen,
                        (effect['color'][0], effect['color'][1], effect['color'][2], effect['alpha']),
                        (inner_x, inner_y),
                        (outer_x, outer_y),
                        int(effect['width'] * 0.3)
                    )
                
                # 绘制扇形填充效果
                points = []
                # 添加中心到扇形外边缘的点
                for i in range(21):
                    current_angle = effect['start_angle'] + i * angle_step
                    x = effect_screen_x + math.cos(current_angle) * effect['range'] * effect['scale']
                    y = effect_screen_y + math.sin(current_angle) * effect['range'] * effect['scale']
                    points.append((x, y))
                # 连接回起点形成封闭扇形
                current_angle = effect['start_angle']
                x = effect_screen_x + math.cos(current_angle) * (effect['range'] - effect['width']) * effect['scale']
                y = effect_screen_y + math.sin(current_angle) * (effect['range'] - effect['width']) * effect['scale']
                points.append((x, y))
                # 绘制半透明扇形
                if len(points) > 2:
                    # 创建半透明表面
                    fan_surface = pygame.Surface((int(effect['range'] * 4), int(effect['range'] * 4)), pygame.SRCALPHA)
                    fan_center = (fan_surface.get_width() // 2, fan_surface.get_height() // 2)
                    # 转换点到表面坐标系
                    surface_points = []
                    for (x, y) in points:
                        surface_x = x - effect_screen_x + fan_center[0]
                        surface_y = y - effect_screen_y + fan_center[1]
                        surface_points.append((surface_x, surface_y))
                    # 绘制扇形
                    pygame.draw.polygon(
                        fan_surface,
                        (effect['color'][0], effect['color'][1], effect['color'][2], int(effect['alpha'] * 0.2)),
                        surface_points
                    )
                    # 绘制到屏幕
                    screen.blit(
                        fan_surface,
                        (effect_screen_x - fan_center[0], effect_screen_y - fan_center[1])
                    )
        
        # 绘制死神的死亡领域特效
        if hasattr(self, 'death_domain_effects'):
            for effect in self.death_domain_effects:
                # 计算屏幕上的位置
                effect_screen_x = effect['x'] - camera_x
                effect_screen_y = effect['y'] - camera_y
                
                # 创建半透明表面
                domain_surface = pygame.Surface((effect['radius'] * 2, effect['radius'] * 2), pygame.SRCALPHA)
                domain_center = (effect['radius'], effect['radius'])
                
                # 绘制死亡领域的环形区域
                # 外圈
                pygame.draw.circle(
                    domain_surface,
                    (effect['color'][0], effect['color'][1], effect['color'][2], int(effect['alpha'] * 0.1)),
                    domain_center,
                    effect['radius']
                )
                # 内圈（中心透明）
                pygame.draw.circle(
                    domain_surface,
                    (0, 0, 0, 0),
                    domain_center,
                    effect['radius'] - 50
                )
                # 绘制脉动的边缘
                pygame.draw.circle(
                    domain_surface,
                    (effect['color'][0], effect['color'][1], effect['color'][2], effect['alpha']),
                    domain_center,
                    effect['radius'],
                    5
                )
                # 绘制内部的脉冲效果
                pulse_radius = effect['radius'] * 0.7 + 30 * math.sin(effect['frame'] * 0.05)
                pygame.draw.circle(
                    domain_surface,
                    (effect['color'][0], effect['color'][1], effect['color'][2], int(effect['alpha'] * 0.3)),
                    domain_center,
                    int(pulse_radius)
                )
                
                # 绘制到屏幕
                screen.blit(
                    domain_surface,
                    (effect_screen_x - effect['radius'], effect_screen_y - effect['radius'])
                )
        
        # 绘制死神的镰刀投掷物
        if hasattr(self, 'sickle_projectiles'):
            for proj in self.sickle_projectiles:
                # 计算屏幕上的位置
                proj_screen_x = proj['x'] - camera_x
                proj_screen_y = proj['y'] - camera_y
                
                # 尝试加载并绘制投掷物图片
                try:
                    from 图片加载 import 图片管理器
                    
                    if 图片管理器 is not None and 图片管理器.图片是否已加载(proj['image']):
                        proj_image = 图片管理器.获取图片(proj['image'])
                        # 缩放到合适大小
                        scaled_image = pygame.transform.scale(proj_image, (proj['width'], proj['height']))
                        # 正旋转（根据angle属性）
                        rotated_image = pygame.transform.rotate(scaled_image, proj['angle'])
                        # 获取旋转后的图片尺寸
                        rotated_rect = rotated_image.get_rect(center=(proj_screen_x + proj['width']//2, proj_screen_y + proj['height']//2))
                        # 绘制旋转后的图片
                        screen.blit(rotated_image, rotated_rect.topleft)
                    else:
                        # 如果图片未加载，绘制简单的镰刀形状
                        # 绘制一个简单的镰刀形状（红色）
                        pygame.draw.rect(screen, (255, 0, 0), (proj_screen_x, proj_screen_y, proj['width'], proj['height']))
                        # 绘制旋转指示器（黑色线条）
                        center_x = proj_screen_x + proj['width'] // 2
                        center_y = proj_screen_y + proj['height'] // 2
                        end_x = center_x + math.cos(math.radians(proj['angle'])) * proj['width']
                        end_y = center_y + math.sin(math.radians(proj['angle'])) * proj['height']
                        pygame.draw.line(screen, (0, 0, 0), (center_x, center_y), (end_x, end_y), 2)
                except Exception as e:
                    # 发生错误时，绘制简单的镰刀形状
                    pygame.draw.rect(screen, (255, 0, 0), (proj_screen_x, proj_screen_y, proj['width'], proj['height']))
                    # 绘制旋转指示器
                    center_x = proj_screen_x + proj['width'] // 2
                    center_y = proj_screen_y + proj['height'] // 2
                    end_x = center_x + math.cos(math.radians(proj['angle'])) * proj['width']
                    end_y = center_y + math.sin(math.radians(proj['angle'])) * proj['height']
                    pygame.draw.line(screen, (0, 0, 0), (center_x, center_y), (end_x, end_y), 2)
        
        # 绘制召唤的灵魂
        if hasattr(self, 'summoned_souls'):
            for soul in self.summoned_souls:
                # 计算屏幕上的位置
                soul_screen_x = soul['x'] - camera_x
                soul_screen_y = soul['y'] - camera_y
                
                # 尝试加载并绘制灵魂图片
                try:
                    from 图片加载 import 图片管理器
                    
                    if 图片管理器 is not None and 图片管理器.图片是否已加载(soul['image']):
                        soul_image = 图片管理器.获取图片(soul['image'])
                        # 缩放到合适大小
                        scaled_image = pygame.transform.scale(soul_image, (soul['width'], soul['height']))
                        # 绘制灵魂
                        screen.blit(scaled_image, (soul_screen_x, soul_screen_y))
                    else:
                        # 如果图片未加载，绘制简单的灵魂形状
                        # 绘制一个半透明的蓝色圆形
                        radius = soul['width'] // 2
                        center_x = soul_screen_x + radius
                        center_y = soul_screen_y + radius
                        # 创建半透明表面
                        soul_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                        pygame.draw.circle(soul_surface, (*soul['color'], 150), (radius, radius), radius)
                        screen.blit(soul_surface, (center_x - radius, center_y - radius))
                except Exception as e:
                    # 发生错误时，绘制简单的灵魂形状
                    radius = soul['width'] // 2
                    center_x = soul_screen_x + radius
                    center_y = soul_screen_y + radius
                    pygame.draw.circle(screen, (*soul['color'], 150), (center_x, center_y), radius)
        
        # 绘制召唤的邪恶蝙蝠
        if hasattr(self, 'summoned_bats') and self.mob_id == 吸血鬼:
            for bat in self.summoned_bats:
                bat_screen_x = bat['x'] - camera_x
                bat_screen_y = bat['y'] - camera_y
                
                # 计算蝙蝠朝向（根据移动方向）
                if 'target' in bat and hasattr(bat['target'], '坐标_x'):
                    target_x = bat['target'].坐标_x
                    # 朝向玩家方向
                    if target_x < bat['x']:  # 玩家在左边，蝙蝠朝左
                        facing_left = True
                    else:  # 玩家在右边，蝙蝠朝右
                        facing_left = False
                else:
                    facing_left = False
                
                # 尝试加载邪恶蝙蝠图片
                try:
                    from 图片加载 import 图片管理器
                    if 图片管理器 is not None and 图片管理器.图片是否已加载("邪恶蝙蝠"):
                        bat_image = 图片管理器.获取图片("邪恶蝙蝠")
                        # 缩放到合适大小
                        scaled_image = pygame.transform.scale(bat_image, (bat['width'], bat['height']))
                        # 根据朝向翻转图片
                        if facing_left:
                            scaled_image = pygame.transform.flip(scaled_image, True, False)  # 水平翻转
                        screen.blit(scaled_image, (bat_screen_x, bat_screen_y))
                    else:
                        # 如果图片未加载，绘制默认色块
                        bat_rect = pygame.Rect(bat_screen_x, bat_screen_y, bat['width'], bat['height'])
                        pygame.draw.rect(screen, (50, 50, 50), bat_rect)  # 灰色蝙蝠
                        # 绘制蝙蝠眼睛，根据朝向调整位置
                        if facing_left:
                            eye_x = bat_screen_x + bat['width'] - 10
                        else:
                            eye_x = bat_screen_x + 10
                        eye_y = bat_screen_y + 10
                        pygame.draw.circle(screen, (255, 0, 0), (eye_x, eye_y), 5)
                        pygame.draw.circle(screen, (255, 255, 255), (eye_x, eye_y), 2)
                except Exception as e:
                    # 发生错误时，绘制默认色块
                    bat_rect = pygame.Rect(bat_screen_x, bat_screen_y, bat['width'], bat['height'])
                    pygame.draw.rect(screen, (50, 50, 50), bat_rect)  # 灰色蝙蝠
                    # 绘制蝙蝠眼睛，根据朝向调整位置
                    if facing_left:
                        eye_x = bat_screen_x + bat['width'] - 10
                    else:
                        eye_x = bat_screen_x + 10
                    eye_y = bat_screen_y + 10
                    pygame.draw.circle(screen, (255, 0, 0), (eye_x, eye_y), 5)
                    pygame.draw.circle(screen, (255, 255, 255), (eye_x, eye_y), 2)
        
        # 绘制召唤的吸血蝙蝠
        if hasattr(self, 'healing_bats') and self.mob_id == 吸血鬼:
            for bat in self.healing_bats:
                bat_screen_x = bat['x'] - camera_x
                bat_screen_y = bat['y'] - camera_y
                
                # 计算蝙蝠朝向（吸血蝙蝠朝向吸血鬼）
                target_x = self.x  # 目标是吸血鬼自己
                # 朝向吸血鬼方向
                if target_x < bat['x']:  # 吸血鬼在左边，蝙蝠朝左
                    facing_left = True
                else:  # 吸血鬼在右边，蝙蝠朝右
                    facing_left = False
                
                # 尝试加载邪恶蝙蝠图片，吸血蝙蝠使用红色调以区分
                try:
                    from 图片加载 import 图片管理器
                    if 图片管理器 is not None and 图片管理器.图片是否已加载("邪恶蝙蝠"):
                        bat_image = 图片管理器.获取图片("邪恶蝙蝠")
                        # 缩放到合适大小
                        scaled_image = pygame.transform.scale(bat_image, (bat['width'], bat['height']))
                        # 根据朝向翻转图片
                        if facing_left:
                            scaled_image = pygame.transform.flip(scaled_image, True, False)  # 水平翻转
                        # 添加红色滤镜
                        red_surface = pygame.Surface(scaled_image.get_size(), pygame.SRCALPHA)
                        red_surface.fill((255, 0, 0, 80))
                        scaled_image.blit(red_surface, (0, 0), special_flags=pygame.BLEND_ADD)
                        screen.blit(scaled_image, (bat_screen_x, bat_screen_y))
                    else:
                        # 如果图片未加载，绘制红色蝙蝠以区分
                        bat_rect = pygame.Rect(bat_screen_x, bat_screen_y, bat['width'], bat['height'])
                        pygame.draw.rect(screen, (150, 0, 0), bat_rect)  # 红色吸血蝙蝠
                        # 绘制蝙蝠眼睛，根据朝向调整位置
                        if facing_left:
                            eye_x = bat_screen_x + bat['width'] - 10
                        else:
                            eye_x = bat_screen_x + 10
                        eye_y = bat_screen_y + 10
                        pygame.draw.circle(screen, (255, 255, 255), (eye_x, eye_y), 5)
                        pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), 2)
                except Exception as e:
                    # 发生错误时，绘制红色蝙蝠
                    bat_rect = pygame.Rect(bat_screen_x, bat_screen_y, bat['width'], bat['height'])
                    pygame.draw.rect(screen, (150, 0, 0), bat_rect)  # 红色吸血蝙蝠
                    # 绘制蝙蝠眼睛，根据朝向调整位置
                    if facing_left:
                        eye_x = bat_screen_x + bat['width'] - 10
                    else:
                        eye_x = bat_screen_x + 10
                    eye_y = bat_screen_y + 10
                    pygame.draw.circle(screen, (255, 255, 255), (eye_x, eye_y), 5)
                    pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), 2)
        
        # 绘制死神的镰刀领域技能
        if hasattr(self, 'sickle_field_projectiles'):
            for projectile in self.sickle_field_projectiles:
                # 计算屏幕位置，使用不同变量名避免覆盖生物位置
                skill_screen_x = projectile['x'] - camera_x
                skill_screen_y = projectile['y'] - camera_y
                
                # 尝试加载对应投掷物图片
                sickle_image = None
                try:
                    from 图片加载 import 图片管理器
                    if 图片管理器 is not None and 图片管理器.图片是否已加载(projectile['image']):
                        sickle_image = 图片管理器.获取图片(projectile['image'])
                except Exception as e:
                    pass
                
                if sickle_image:
                    # 缩放图片
                    scaled_image = pygame.transform.scale(sickle_image, (projectile['width'], projectile['height']))
                    # 旋转图片
                    rotated_image = pygame.transform.rotate(scaled_image, math.degrees(projectile['angle']))
                    # 计算旋转后的图片位置（居中于技能位置）
                    rotated_rect = rotated_image.get_rect(center=(skill_screen_x, skill_screen_y))
                    # 绘制图片
                    screen.blit(rotated_image, rotated_rect.topleft)
                else:
                    # 没有图片时绘制默认形状
                    # 绘制旋转的矩形代表镰刀
                    temp_surface = pygame.Surface((projectile['width'], projectile['height']), pygame.SRCALPHA)
                    pygame.draw.rect(temp_surface, (255, 0, 0), (0, 0, projectile['width'], projectile['height']))
                    # 旋转表面
                    rotated_surface = pygame.transform.rotate(temp_surface, math.degrees(projectile['angle']))
                    # 计算旋转后的位置（居中于技能位置）
                    rotated_rect = rotated_surface.get_rect(center=(skill_screen_x, skill_screen_y))
                    # 绘制旋转后的表面
                    screen.blit(rotated_surface, rotated_rect.topleft)
                
                # 绘制镰刀区域范围（半透明圆圈）
                circle_surface = pygame.Surface((self.sickle_field_radius * 2, self.sickle_field_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, (255, 0, 0, 50), (self.sickle_field_radius, self.sickle_field_radius), self.sickle_field_radius)
                # 使用每个镰刀自己的位置绘制范围圈
                screen.blit(circle_surface, (skill_screen_x - self.sickle_field_radius, skill_screen_y - self.sickle_field_radius))
        
        # 绘制死神的旋转跟随镰刀技能
        if hasattr(self, 'rotating_follow_sickle_projectiles'):
            for projectile in self.rotating_follow_sickle_projectiles:
                # 计算屏幕位置，使用特定变量名避免覆盖
                follow_sickle_screen_x = projectile['x'] - camera_x
                follow_sickle_screen_y = projectile['y'] - camera_y
                
                # 尝试加载对应投掷物图片
                sickle_image = None
                try:
                    from 图片加载 import 图片管理器
                    if 图片管理器 is not None and 图片管理器.图片是否已加载(projectile['image']):
                        sickle_image = 图片管理器.获取图片(projectile['image'])
                except Exception as e:
                    pass
                
                if sickle_image:
                    # 缩放图片
                    scaled_image = pygame.transform.scale(sickle_image, (projectile['width'], projectile['height']))
                    # 旋转图片
                    rotated_image = pygame.transform.rotate(scaled_image, math.degrees(projectile['angle']))
                    # 计算旋转后的图片位置（居中）
                    rotated_rect = rotated_image.get_rect(center=(follow_sickle_screen_x, follow_sickle_screen_y))
                    # 绘制图片
                    screen.blit(rotated_image, rotated_rect.topleft)
                else:
                    # 没有图片时绘制默认形状
                    # 绘制旋转的矩形代表镰刀
                    temp_surface = pygame.Surface((projectile['width'], projectile['height']), pygame.SRCALPHA)
                    pygame.draw.rect(temp_surface, (255, 255, 0), (0, 0, projectile['width'], projectile['height']))
                    # 旋转表面
                    rotated_surface = pygame.transform.rotate(temp_surface, math.degrees(projectile['angle']))
                    # 计算旋转后的位置
                    rotated_rect = rotated_surface.get_rect(center=(follow_sickle_screen_x, follow_sickle_screen_y))
                    # 绘制旋转后的表面
                    screen.blit(rotated_surface, rotated_rect.topleft)
        
        # 绘制死神的子弹风暴技能
        if hasattr(self, 'bullet_storm_projectiles'):
            for projectile in self.bullet_storm_projectiles:
                # 计算屏幕位置，使用特定变量名避免覆盖
                bullet_screen_x = projectile['x'] - camera_x
                bullet_screen_y = projectile['y'] - camera_y
                
                # 尝试加载并绘制子弹图片
                try:
                    from 图片加载 import 图片管理器
                    if 图片管理器 is not None and 图片管理器.图片是否已加载(projectile['image']):
                        bullet_image = 图片管理器.获取图片(projectile['image'])
                        # 缩放到合适大小
                        scaled_image = pygame.transform.scale(bullet_image, (projectile['width'], projectile['height']))
                        # 旋转图片（图片朝向右，根据角度调整）
                        rotated_image = pygame.transform.rotate(scaled_image, projectile['angle'])
                        # 计算旋转后的图片位置（居中）
                        rotated_rect = rotated_image.get_rect(center=(bullet_screen_x + projectile['width']//2, bullet_screen_y + projectile['height']//2))
                        # 绘制图片
                        screen.blit(rotated_image, rotated_rect.topleft)
                    else:
                        # 如果图片未加载，绘制简单的红色圆形
                        pygame.draw.circle(screen, (255, 0, 0), (int(bullet_screen_x + projectile['width']//2), int(bullet_screen_y + projectile['height']//2)), int(projectile['width'] // 2))
                except Exception as e:
                    # 发生错误时，绘制简单的红色圆形
                    pygame.draw.circle(screen, (255, 0, 0), (int(bullet_screen_x + projectile['width']//2), int(bullet_screen_y + projectile['height']//2)), int(projectile['width'] // 2))
        
        # 绘制召唤的刺球
        if hasattr(self, 'spike_balls') and self.mob_id == 吸血鬼:
            for ball in self.spike_balls:
                ball_screen_x = ball['x'] - camera_x
                ball_screen_y = ball['y'] - camera_y
                
                # 尝试加载刺球图片
                try:
                    from 图片加载 import 图片管理器
                    if 图片管理器 is not None and 图片管理器.图片是否已加载("刺球"):
                        ball_image = 图片管理器.获取图片("刺球")
                        # 旋转并缩放到合适大小
                        scaled_image = pygame.transform.scale(ball_image, (ball['width'], ball['height']))
                        rotated_image = pygame.transform.rotate(scaled_image, ball['rotation'])
                        # 计算旋转后的矩形位置（保持中心不变）
                        rotated_rect = rotated_image.get_rect(center=(ball_screen_x + ball['width']//2, ball_screen_y + ball['height']//2))
                        screen.blit(rotated_image, rotated_rect.topleft)
                    else:
                        # 如果图片未加载，绘制旋转的刺球
                        # 绘制刺球主体
                        center_x = ball_screen_x + ball['width'] // 2
                        center_y = ball_screen_y + ball['height'] // 2
                        radius = ball['width'] // 2
                        # 绘制旋转的刺球
                        pygame.draw.circle(screen, (150, 50, 50), (center_x, center_y), radius)
                        # 绘制刺
                        for i in range(8):
                            angle = math.radians(ball['rotation'] + i * 45)
                            spike_x = center_x + math.cos(angle) * radius
                            spike_y = center_y + math.sin(angle) * radius
                            spike_end_x = center_x + math.cos(angle) * (radius + 8)
                            spike_end_y = center_y + math.sin(angle) * (radius + 8)
                            pygame.draw.line(screen, (200, 0, 0), (spike_x, spike_y), (spike_end_x, spike_end_y), 3)
                except Exception as e:
                    # 发生错误时，绘制简单的刺球
                    center_x = ball_screen_x + ball['width'] // 2
                    center_y = ball_screen_y + ball['height'] // 2
                    radius = ball['width'] // 2
                    pygame.draw.circle(screen, (150, 50, 50), (center_x, center_y), radius)
                    # 绘制刺
                    for i in range(8):
                        angle = math.radians(ball['rotation'] + i * 45)
                        spike_x = center_x + math.cos(angle) * radius
                        spike_y = center_y + math.sin(angle) * radius
                        spike_end_x = center_x + math.cos(angle) * (radius + 8)
                        spike_end_y = center_y + math.sin(angle) * (radius + 8)
                        pygame.draw.line(screen, (200, 0, 0), (spike_x, spike_y), (spike_end_x, spike_end_y), 3)
        
        # 绘制刺球爆炸特效
        if hasattr(self, 'spike_explosions'):
            for explosion in self.spike_explosions:
                explosion_screen_x = explosion['x'] - camera_x
                explosion_screen_y = explosion['y'] - camera_y
                # 计算透明度（先从透明到不透明，再到透明）
                max_life = 15
                current_life = explosion['timer']
                if current_life > max_life / 2:
                    # 前半段：从透明到不透明
                    progress = 1 - (current_life - max_life/2) / (max_life/2)
                    alpha = int(255 * progress)
                else:
                    # 后半段：从不透明到透明
                    progress = current_life / (max_life/2)
                    alpha = int(255 * progress)
                # 创建爆炸表面
                explosion_surface = pygame.Surface((explosion['radius'] * 2, explosion['radius'] * 2), pygame.SRCALPHA)
                # 绘制爆炸圆环
                pygame.draw.circle(explosion_surface, 
                                 (explosion['color'][0], explosion['color'][1], explosion['color'][2], alpha),
                                 (explosion['radius'], explosion['radius']),
                                 explosion['radius'],
                                 5)  # 线宽5
                # 绘制爆炸中心
                pygame.draw.circle(explosion_surface, 
                                 (explosion['color'][0], explosion['color'][1], explosion['color'][2], alpha),
                                 (explosion['radius'], explosion['radius']),
                                 explosion['radius'] // 3)
                # 绘制到屏幕
                screen.blit(explosion_surface, (explosion_screen_x - explosion['radius'], explosion_screen_y - explosion['radius']))

        # 绘制肥胖Boss的落地特效
        # 无论特效是添加到自身的landing_effects列表还是游戏的explosion_effects列表，都需要确保能正确绘制
        # 1. 绘制自身landing_effects列表中的特效
        if hasattr(self, 'landing_effects'):
            for effect in self.landing_effects:
                effect_screen_x = effect['x'] - camera_x
                effect_screen_y = effect['y'] - camera_y
                # 计算透明度（先从透明到不透明，再到透明）
                max_life = effect['duration']
                current_life = effect['lifetime']
                progress = 1 - (current_life / max_life)
                if progress < 0.5:
                    # 前半段：从透明到不透明
                    alpha = int(255 * progress * 2)
                else:
                    # 后半段：从不透明到透明
                    alpha = int(255 * (1 - (progress - 0.5) * 2))
                # 创建特效表面
                effect_surface = pygame.Surface((int(effect['radius'] * 2), int(effect['radius'] * 2)), pygame.SRCALPHA)
                # 只绘制上半部分圆的特效
                # 1. 绘制外层圆弧（上半部分：从右侧到右侧，经过顶部）
                pygame.draw.arc(effect_surface, 
                              (effect['color'][0], effect['color'][1], effect['color'][2], alpha),
                              (0, 0, int(effect['radius'] * 2), int(effect['radius'] * 2)),
                              0,  # 起始角度：0度（右侧）
                              math.pi,  # 结束角度：180度（左侧）
                              10)  # 线宽10
                # 2. 绘制中层圆弧（上半部分）
                pygame.draw.arc(effect_surface, 
                              (effect['color'][0], effect['color'][1], effect['color'][2], alpha),
                              (int(effect['radius'] // 2), int(effect['radius'] // 2), int(effect['radius']), int(effect['radius'])),
                              0,  # 起始角度：0度（右侧）
                              math.pi,  # 结束角度：180度（左侧）
                              5)  # 线宽5
                # 3. 绘制内层圆弧（上半部分）
                pygame.draw.arc(effect_surface, 
                              (effect['color'][0], effect['color'][1], effect['color'][2], alpha),
                              (int(effect['radius'] // 4 * 3), int(effect['radius'] // 4 * 3), int(effect['radius'] // 2), int(effect['radius'] // 2)),
                              0,  # 起始角度：0度（右侧）
                              math.pi,  # 结束角度：180度（左侧）
                              3)  # 线宽3
                # 4. 绘制中心亮点（上半部分）
                # 只绘制上半部分的中心亮点
                center_half_radius = int(effect['radius'] // 10)
                pygame.draw.arc(effect_surface, 
                              (effect['color'][0], effect['color'][1], effect['color'][2], alpha),
                              (int(effect['radius'] - center_half_radius), int(effect['radius'] - center_half_radius), int(center_half_radius * 2), int(center_half_radius * 2)),
                              0,  # 起始角度：0度（右侧）
                              math.pi,  # 结束角度：180度（左侧）
                              center_half_radius)  # 线宽等于半径，形成实心半圆
                # 绘制到屏幕，下降3格（3*32=96像素）
                screen.blit(effect_surface, (effect_screen_x - effect['radius'], effect_screen_y - effect['radius'] + 96))
        
        # 2. 确保肥胖Boss的落地特效始终使用自身的landing_effects列表
        # 修改特效创建逻辑，无论self.game是否存在，都将特效添加到自身的landing_effects列表中
        
        # 绘制召唤的异变骷髅
        if hasattr(self, 'mutant_skulls') and self.mob_id == 吸血鬼:
            for skull in self.mutant_skulls:
                skull_screen_x = skull['x'] - camera_x
                skull_screen_y = skull['y'] - camera_y
                
                # 计算骷髅朝向（根据移动方向）
                # 根据移动方向判断朝向
                if skull['move_dir_x'] < 0:  # 向左移动，朝左
                    facing_left = True
                elif skull['move_dir_x'] > 0:  # 向右移动，朝右
                    facing_left = False
                else:
                    # 如果没有水平移动，默认朝右
                    facing_left = False
                
                # 尝试加载异变骷髅图片
                try:
                    from 图片加载 import 图片管理器
                    if 图片管理器 is not None and 图片管理器.图片是否已加载("异变骷髅"):
                        skull_image = 图片管理器.获取图片("异变骷髅")
                        # 缩放到合适大小
                        scaled_image = pygame.transform.scale(skull_image, (skull['width'], skull['height']))
                        # 根据朝向翻转图片
                        if facing_left:
                            scaled_image = pygame.transform.flip(scaled_image, True, False)  # 水平翻转
                        screen.blit(scaled_image, (skull_screen_x, skull_screen_y))
                    else:
                        # 如果图片未加载，绘制默认色块
                        skull_rect = pygame.Rect(skull_screen_x, skull_screen_y, skull['width'], skull['height'])
                        pygame.draw.rect(screen, (100, 100, 100), skull_rect)  # 灰色骷髅
                        # 绘制骷髅特征，根据朝向调整位置
                        if facing_left:
                            # 朝左，眼睛在右侧
                            eye1_x = skull_screen_x + skull['width'] - 12
                            eye2_x = skull_screen_x + skull['width'] - 32
                            # 嘴巴朝左
                            pygame.draw.line(screen, (255, 0, 0), 
                                           (skull_screen_x + skull['width'] - 15, skull_screen_y + 30), 
                                           (skull_screen_x + skull['width'] - 30, skull_screen_y + 35), 3)
                        else:
                            # 朝右，眼睛在左侧
                            eye1_x = skull_screen_x + 12
                            eye2_x = skull_screen_x + 32
                            # 嘴巴朝右
                            pygame.draw.line(screen, (255, 0, 0), 
                                           (skull_screen_x + 15, skull_screen_y + 30), 
                                           (skull_screen_x + 30, skull_screen_y + 35), 3)
                        
                        eye1_y = skull_screen_y + 15
                        eye2_y = skull_screen_y + 15
                        pygame.draw.circle(screen, (255, 0, 0), (eye1_x, eye1_y), 6)
                        pygame.draw.circle(screen, (255, 0, 0), (eye2_x, eye2_y), 6)
                except Exception as e:
                    # 发生错误时，绘制简单的骷髅
                    skull_rect = pygame.Rect(skull_screen_x, skull_screen_y, skull['width'], skull['height'])
                    pygame.draw.rect(screen, (100, 100, 100), skull_rect)
                    # 绘制眼睛，根据朝向调整位置
                    if facing_left:
                        eye1_x = skull_screen_x + skull['width'] - 12
                        eye2_x = skull_screen_x + skull['width'] - 32
                    else:
                        eye1_x = skull_screen_x + 12
                        eye2_x = skull_screen_x + 32
                    eye1_y = skull_screen_y + 15
                    eye2_y = skull_screen_y + 15
                    pygame.draw.circle(screen, (255, 0, 0), (eye1_x, eye1_y), 6)
                    pygame.draw.circle(screen, (255, 0, 0), (eye2_x, eye2_y), 6)
        

        
        # 绘制悬浮子弹
        if hasattr(self, 'floating_bullets') and self.mob_id == 吸血鬼:
            for bullet in self.floating_bullets:
                bullet_screen_x = bullet['x'] - camera_x
                bullet_screen_y = bullet['y'] - camera_y
                
                # 绘制紫色悬浮子弹
                radius = bullet['width'] // 2
                center_x = bullet_screen_x + radius
                center_y = bullet_screen_y + radius
                pygame.draw.circle(screen, bullet['color'], (center_x, center_y), radius)
        
        # 绘制狂暴状态特效
        if hasattr(self, 'rage_mode') and self.rage_mode:
            # 红色边框特效
            pygame.draw.rect(screen, (255, 0, 0), 
                             (screen_x - 5, screen_y - 5, self.width + 10, self.height + 10), 3)
            # 脉动效果
            pulse_size = 5 + abs(math.sin(pygame.time.get_ticks() * 0.01) * 10)
            pygame.draw.rect(screen, (255, 50, 50), 
                             (screen_x - pulse_size, screen_y - pulse_size, self.width + pulse_size * 2, self.height + pulse_size * 2), 2)
        
        # 绘制临时护盾特效
        if hasattr(self, 'shield_value') and self.shield_value > 0:
            # 蓝色半透明护盾特效
            shield_surface = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (50, 100, 255, 100), 
                              (self.width // 2 + 10, self.height // 2 + 10), 
                              max(self.width, self.height) // 2 + 15)
            screen.blit(shield_surface, (screen_x - 10, screen_y - 10))
            # 护盾值文本提示 - 使用英文字体避免中文渲染问题
            font = pygame.font.Font(None, 24)
            shield_text = font.render(f"Shield: {self.shield_value}", True, (100, 200, 255))
            screen.blit(shield_text, (screen_x, screen_y - 30))
        
