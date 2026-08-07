import pygame
import random
import math

# 导入物品定义中的生物ID
from 物品定义 import 死神祝福

class 武器技能管理器:
    def __init__(self):
        self.skills = {}
        self.cooldowns = {}
        self.summoned_entities = []
        
    def register_skill(self, weapon_name, skill_key, skill_func, cooldown):
        """注册武器技能"""
        if weapon_name not in self.skills:
            self.skills[weapon_name] = {}
            self.cooldowns[weapon_name] = {}
        self.skills[weapon_name][skill_key] = skill_func
        self.cooldowns[weapon_name][skill_key] = {
            "cooldown": cooldown,
            "last_used": -cooldown  # 游戏开始时0冷却，可以立即使用
        }
    
    def handle_input(self, event, player, weapon_name):
        """处理武器技能输入"""
        print(f"收到技能输入：事件类型={event.type}，武器名称={weapon_name}")
        # 特殊处理：直接检查是否是特殊武器（死神的镰刀、灵火剑、超暗黑刺刀、亡灵斧头、火焰三叉戟或闪电三叉戟）
        if "死神的镰刀" in weapon_name:
            weapon_name = "死神的镰刀"
            print(f"识别为死神的镰刀")
        elif "灵火剑" in weapon_name:
            weapon_name = "灵火剑"
            print(f"识别为灵火剑")
        elif "超暗黑刺刀" in weapon_name:
            weapon_name = "超暗黑刺刀"
            print(f"识别为超暗黑刺刀")
        elif "亡灵斧头" in weapon_name:
            weapon_name = "亡灵斧头"
            print(f"识别为亡灵斧头")
        elif "火焰三叉戟" in weapon_name:
            weapon_name = "火焰三叉戟"
            print(f"识别为火焰三叉戟")
        elif "闪电三叉戟" in weapon_name:
            weapon_name = "闪电三叉戟"
            print(f"识别为闪电三叉戟")
        elif "骨毒法杖" in weapon_name:
            weapon_name = "骨毒法杖"
            print(f"识别为骨毒法杖")
        elif "七彩法杖" in weapon_name:
            weapon_name = "七彩法杖"
            print(f"识别为七彩法杖")
        elif "森林法杖" in weapon_name:
            weapon_name = "森林法杖"
            print(f"识别为森林法杖")
        elif "亡灵法杖" in weapon_name:
            weapon_name = "亡灵法杖"
            print(f"识别为亡灵法杖")
        elif "齐天金箍棒" in weapon_name:
            weapon_name = "齐天金箍棒"
            print(f"识别为齐天金箍棒")
        
        # 检查武器是否有注册的技能
        if weapon_name not in self.skills:
            print(f"武器 {weapon_name} 没有注册的技能")
            return
        else:
            print(f"武器 {weapon_name} 有注册的技能: {self.skills[weapon_name]}")
        
        current_time = pygame.time.get_ticks() / 1000  # 转换为秒
        
        # 处理按键释放事件
        if event.type == pygame.KEYUP:
            # 检查是否是Q键
            if event.key == pygame.K_q:
                if "q" in self.skills[weapon_name]:
                    cooldown_data = self.cooldowns[weapon_name]["q"]
                    剩余时间 = cooldown_data["cooldown"] - (current_time - cooldown_data["last_used"])
                    if 剩余时间 <= 0:
                        # 执行技能
                        self.skills[weapon_name]["q"](player, self)
                        # 更新冷却时间
                        cooldown_data["last_used"] = current_time
        # 同时处理按键按下事件，确保技能能被触发
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                if "q" in self.skills[weapon_name]:
                    cooldown_data = self.cooldowns[weapon_name]["q"]
                    剩余时间 = cooldown_data["cooldown"] - (current_time - cooldown_data["last_used"])
                    if 剩余时间 <= 0:
                        # 执行技能
                        self.skills[weapon_name]["q"](player, self)
                        # 更新冷却时间
                        cooldown_data["last_used"] = current_time
        # 处理鼠标右键事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # 3是鼠标右键
                if "q" in self.skills[weapon_name]:
                    cooldown_data = self.cooldowns[weapon_name]["q"]
                    剩余时间 = cooldown_data["cooldown"] - (current_time - cooldown_data["last_used"])
                    if 剩余时间 <= 0:
                        # 执行技能
                        self.skills[weapon_name]["q"](player, self)
                        # 更新冷却时间
                        cooldown_data["last_used"] = current_time
    
    def update(self, dt, world, player, game):
        """更新所有武器技能状态"""
        # 更新召唤生物
        for entity in self.summoned_entities[:]:
            entity.update(dt, world, player, game)
            if entity.should_remove():
                self.summoned_entities.remove(entity)
    
    def draw(self, surface, camera_x, camera_y):
        """绘制所有武器技能相关元素"""
        for entity in self.summoned_entities:
            entity.draw(surface, camera_x, camera_y)
    
    def get_remaining_cooldown(self, weapon_name, skill_key="q"):
        """获取特定武器技能的剩余冷却时间（秒）"""
        # 特殊处理：直接检查是否是特殊武器（死神的镰刀、灵火剑、超暗黑刺刀、亡灵斧头、火焰三叉戟或闪电三叉戟）
        if "死神的镰刀" in weapon_name:
            weapon_name = "死神的镰刀"
        elif "灵火剑" in weapon_name:
            weapon_name = "灵火剑"
        elif "超暗黑刺刀" in weapon_name:
            weapon_name = "超暗黑刺刀"
        elif "亡灵斧头" in weapon_name:
            weapon_name = "亡灵斧头"
        elif "火焰三叉戟" in weapon_name:
            weapon_name = "火焰三叉戟"
        elif "闪电三叉戟" in weapon_name:
            weapon_name = "闪电三叉戟"
        elif "骨毒法杖" in weapon_name:
            weapon_name = "骨毒法杖"
        elif "七彩法杖" in weapon_name:
            weapon_name = "七彩法杖"
        elif "森林法杖" in weapon_name:
            weapon_name = "森林法杖"
        
        if weapon_name not in self.skills or skill_key not in self.skills[weapon_name]:
            return 0
        
        current_time = pygame.time.get_ticks() / 1000  # 转换为秒
        cooldown_data = self.cooldowns[weapon_name][skill_key]
        remaining = cooldown_data["cooldown"] - (current_time - cooldown_data["last_used"])
        return max(0, remaining)

class 死神祝福实体:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        # 将大小调整为原来的50%（小50%）
        self.width = 60  # 120 * 0.5
        self.height = 90  # 180 * 0.5
        self.health = 250
        self.max_health = 250
        self.player = player
        self.target = None
        self.speed = 3.75  # 移动速度 +250% (1.5 * 2.5)
        self.attack_range = 5 * 32  # 5格近战攻击范围
        self.ranged_attack_range = 10 * 32  # 10格远程攻击范围
        self.sight_range = 1000 * 32  # 视野 +10000% (10 * 100)
        self.attack_cooldown = 24  # 攻击频率 +250% (60 / 2.5)
        self.last_attack_time = 0
        self.lifetime = 0
        self.max_lifetime = 25  # 存活时间（秒）
        self.projectiles = []
        self.direction = 1  # 朝向，1为右，-1为左
        self.name = "死神祝福"  # 设置生物名称，用于加载图片
        
        # 动画相关
        self.animation_frame = 0
        self.animation_timer = 0
        
        # 状态
        self.is_attacking = False
        self.is_moving = False
    
    def update(self, dt, world, player, game):
        """更新死神祝福状态"""
        self.lifetime += dt
        
        # 如果没有目标，主动寻找视野范围内的生物
        if not self.target:
            self.find_target(game)
        
        # 跟随玩家
        self.follow_player()
        
        # 如果有目标，攻击目标
        if self.target:
            self.attack_target(dt, game)
        
        # 更新投掷物
        self.update_projectiles(dt, world)
    
    def find_target(self, game):
        """寻找视野范围内的生物作为目标"""
        # 获取所有生物列表
        if hasattr(game, '世界') and hasattr(game.世界, 'mobs'):
            all_mobs = game.世界.mobs.copy()
        else:
            return
        
        # 检查是否有当前boss
        try:
            from boos生物处理 import boss_manager
            if boss_manager.current_boss and boss_manager.current_boss.is_alive():
                all_mobs.append(boss_manager.current_boss)
        except Exception as e:
            pass
        
        closest_target = None
        closest_distance = float('inf')
        
        # 遍历所有生物，寻找视野范围内最近的生物
        for mob in all_mobs:
            # 跳过玩家
            if hasattr(mob, 'is_player') and mob.is_player:
                continue
            
            # 计算到生物的距离
            dx = mob.x - self.x
            dy = mob.y - self.y
            distance = math.hypot(dx, dy)
            
            # 如果在视野范围内，并且是最近的生物
            if distance <= self.sight_range and distance < closest_distance:
                closest_target = mob
                closest_distance = distance
        
        # 设置最近的生物为目标
        if closest_target:
            self.target = closest_target
    
    def follow_player(self):
        """跟随玩家"""
        # 只有在没有目标时才跟随玩家
        if not self.target:
            # 计算到玩家的距离
            dx = self.player.坐标_x - self.x
            dy = self.player.坐标_y - self.y
            distance = math.hypot(dx, dy)
            
            # 设置跟随距离阈值为5格，确保总是跟随玩家
            follow_distance = 5 * 32
            if distance > follow_distance:
                # 归一化方向向量
                if distance > 0:
                    dir_x = dx / distance
                    dir_y = dy / distance
                else:
                    dir_x = 0
                    dir_y = 0
                
                # 移动
                self.x += dir_x * self.speed
                self.y += dir_y * self.speed
                
                # 更新朝向
                if dir_x > 0:
                    self.direction = 1
                elif dir_x < 0:
                    self.direction = -1
    
    def set_target(self, target):
        """设置攻击目标"""
        self.target = target
    
    def attack_target(self, dt, game):
        """攻击目标"""
        if not self.target:
            return
        
        # 计算到目标的距离
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.hypot(dx, dy)
        
        # 近战攻击
        if distance <= self.attack_range:
            # 移动到攻击范围内
            if distance > self.attack_range * 0.5:
                # 归一化方向向量
                dir_x = dx / distance
                dir_y = dy / distance
                
                # 移动
                self.x += dir_x * self.speed
                self.y += dir_y * self.speed
                
                # 更新朝向
                if dir_x > 0:
                    self.direction = 1
                elif dir_x < 0:
                    self.direction = -1
            
            # 近战攻击 - 使用dt计算时间
            self.last_attack_time += dt
            if self.last_attack_time >= self.attack_cooldown / 60:  # 将攻击间隔转换为秒
                self.last_attack_time = 0
                # 检查目标是否还活着
                if hasattr(self.target, 'health') and self.target.health > 0:
                    # 造成伤害
                    self.target.game = game
                    damage = 40  # 近战伤害
                    # 攻击目标
                    死亡 = self.target.take_damage(damage)
                    # 只有在目标活着时才创建伤害文本
                    if not 死亡 or (hasattr(self.target, 'health') and self.target.health > 0):
                        game.damage_texts.append(game.DamageText(self.target.x + self.target.width // 2, self.target.y - 10, damage))
                    # 如果目标死亡，生成掉落物、经验，并清除目标
                    if 死亡:
                        # 生成经验球
                        if hasattr(game, 'spawn_exp_orbs'):
                            game.spawn_exp_orbs(self.target.x // 32, self.target.y // 32)
                        
                        # 生成掉落物
                        try:
                            from 掉落物 import 掉落物管理器实例
                            from 生物系统 import 生物掉落物配置
                            掉落物管理器实例.生成生物掉落物(
                                game.世界, 
                                int(self.target.x // 32), 
                                int(self.target.y // 32), 
                                getattr(self.target, 'name', ''), 
                                getattr(self.target, 'mob_id', 0), 
                                生物掉落物配置
                            )
                        except Exception as e:
                            print(f"生成生物掉落物失败: {e}")
                            # 备用方案 - 生成肉块
                            from 物品定义 import 肉块
                            game.世界.spawn_item(int(self.target.x // 32), int(self.target.y // 32), 肉块, random.randint(1, 3))
                        
                        # 清除目标
                        self.target = None
        # 远程攻击
        elif distance <= self.ranged_attack_range:
            # 更新朝向
            if dx > 0:
                self.direction = 1
            elif dx < 0:
                self.direction = -1
            
            # 远程攻击 - 使用dt计算时间
            self.last_attack_time += dt
            if self.last_attack_time >= self.attack_cooldown / 60:  # 将攻击间隔转换为秒
                self.last_attack_time = 0
                # 发射投掷物
                self.fire_projectile()
        else:
            # 如果目标太远，尝试接近目标
            # 归一化方向向量
            dir_x = dx / distance
            dir_y = dy / distance
            
            # 移动
            self.x += dir_x * self.speed
            self.y += dir_y * self.speed
            
            # 更新朝向
            if dir_x > 0:
                self.direction = 1
            elif dir_x < 0:
                self.direction = -1
    
    def fire_projectile(self):
        """发射远程投掷物"""
        if not self.target:
            return
        
        # 计算投掷物速度和方向
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.hypot(dx, dy)
        
        if distance > 0:
            dir_x = dx / distance
            dir_y = dy / distance
        else:
            dir_x = 1
            dir_y = 0
        
        # 创建投掷物
        projectile = {
            "x": self.x + self.width // 2,
            "y": self.y + self.height // 2,
            "vx": dir_x * 300,
            "vy": dir_y * 300,
            "damage": 20,
            "width": 20,
            "height": 20,
            "lifetime": 3.0,
            "color": (100, 0, 100)
        }
        
        self.projectiles.append(projectile)
    
    def update_projectiles(self, dt, world):
        """更新投掷物"""
        for projectile in self.projectiles[:]:
            # 更新位置
            projectile["x"] += projectile["vx"] * dt
            projectile["y"] += projectile["vy"] * dt
            
            # 减少生命周期
            projectile["lifetime"] -= dt
            
            # 检查是否过期
            if projectile["lifetime"] <= 0:
                self.projectiles.remove(projectile)
                continue
            
            # 检查与目标生物的碰撞
            if self.target:
                # 检查目标是否还活着
                if hasattr(self.target, 'health') and self.target.health <= 0:
                    # 目标已经死亡，清除目标
                    self.target = None
                    continue
                    
                # 创建投掷物矩形
                proj_rect = pygame.Rect(
                    projectile["x"], 
                    projectile["y"], 
                    projectile["width"], 
                    projectile["height"]
                )
                
                # 创建目标矩形
                target_rect = pygame.Rect(
                    self.target.x, 
                    self.target.y, 
                    self.target.width, 
                    self.target.height
                )
                
                # 检查碰撞
                if proj_rect.colliderect(target_rect):
                    # 造成伤害
                    # 确保mob.game存在
                    self.target.game = self.player.game
                    game = self.player.game
                    死亡 = self.target.take_damage(projectile["damage"])
                    # 移除投掷物
                    self.projectiles.remove(projectile)
                    
                    # 创建伤害文本
                    if game and hasattr(game, 'damage_texts'):
                        game.damage_texts.append(game.DamageText(
                            self.target.x + self.target.width // 2, 
                            self.target.y - 10, 
                            projectile["damage"]
                        ))
                    
                    # 如果目标死亡，生成掉落物和经验
                    if 死亡:
                        # 生成经验球
                        if game and hasattr(game, 'spawn_exp_orbs'):
                            game.spawn_exp_orbs(self.target.x // 32, self.target.y // 32)
                        
                        # 生成掉落物
                        try:
                            from 掉落物 import 掉落物管理器实例
                            from 生物系统 import 生物掉落物配置
                            if game:
                                掉落物管理器实例.生成生物掉落物(
                                    game.世界, 
                                    int(self.target.x // 32), 
                                    int(self.target.y // 32), 
                                    getattr(self.target, 'name', ''), 
                                    getattr(self.target, 'mob_id', 0), 
                                    生物掉落物配置
                                )
                        except Exception as e:
                            print(f"生成生物掉落物失败: {e}")
                            # 备用方案 - 生成肉块
                            from 物品定义 import 肉块
                            if game:
                                game.世界.spawn_item(int(self.target.x // 32), int(self.target.y // 32), 肉块, random.randint(1, 3))
                        
                        # 清除目标
                        self.target = None
                    continue
            
            # 检查与世界的碰撞
            tile_x = int((projectile["x"] + projectile["width"] // 2) // 32)
            tile_y = int((projectile["y"] + projectile["height"] // 2) // 32)
            
            if 0 <= tile_y < world.高度 and 0 <= tile_x < world.宽度:
                block_id = world.get_block(tile_x, tile_y)
                if block_id != 0:  # 0是空气
                    self.projectiles.remove(projectile)
                    continue
    
    def should_remove(self):
        """检查是否应该被移除"""
        return self.health <= 0 or self.lifetime >= self.max_lifetime
    
    def draw(self, surface, camera_x, camera_y):
        """绘制死神祝福"""
        # 计算屏幕位置
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
                # 2. 尝试使用带下划线的版本（死神_祝福）
                if mob_image is None and 图片管理器.图片是否已加载("死神_祝福"):
                    mob_image = 图片管理器.获取图片("死神_祝福")
                # 3. 尝试添加"小"前缀
                if mob_image is None and 图片管理器.图片是否已加载(f"小{self.name}"):
                    mob_image = 图片管理器.获取图片(f"小{self.name}")
                # 4. 尝试添加"小"前缀的带下划线版本
                if mob_image is None and 图片管理器.图片是否已加载("小死神_祝福"):
                    mob_image = 图片管理器.获取图片("小死神_祝福")
        except Exception as e:
            # 图片加载失败，使用默认色块
            pass
        
        if mob_image:
            # 有图片时绘制图片
            # 缩放图片到生物尺寸
            scaled_image = pygame.transform.scale(mob_image, (self.width, self.height))
            # 根据生物朝向翻转图片
            if self.direction < 0:  # 向左看时翻转图片
                scaled_image = pygame.transform.flip(scaled_image, True, False)
            
            # 绘制图片
            surface.blit(scaled_image, (screen_x, screen_y))
        else:
            # 没有图片时绘制默认色块
            # 绘制生物身体
            color = (100, 0, 100)  # 紫色
            mob_rect = pygame.Rect(screen_x, screen_y, self.width, self.height)
            pygame.draw.rect(surface, color, mob_rect)
            
            # 绘制生物眼睛（显示方向）
            eye_offset = 4
            if self.direction > 0:  # 向右看
                eye_x = screen_x + self.width - 8
            else:  # 向左看
                eye_x = screen_x + 4
            
            pygame.draw.circle(surface, (0, 0, 0), (eye_x, screen_y + 10), 3)
            pygame.draw.circle(surface, (255, 255, 255), (eye_x, screen_y + 10), 1)
        
        # 绘制血条
        bar_width = self.width
        bar_height = 5
        bar_x = screen_x
        bar_y = screen_y - 10
        
        # 背景血条
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # 当前血条
        health_ratio = self.health / self.max_health
        current_width = int(bar_width * health_ratio)
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, current_width, bar_height))
        
        # 绘制投掷物
        for projectile in self.projectiles:
            proj_screen_x = projectile["x"] - camera_x
            proj_screen_y = projectile["y"] - camera_y
            pygame.draw.circle(surface, projectile["color"], 
                              (int(proj_screen_x + projectile["width"] // 2), 
                               int(proj_screen_y + projectile["height"] // 2)), 
                              projectile["width"] // 2)
    
    def take_damage(self, damage):
        """受到伤害"""
        # 玩家无法攻击死神祝福，直接返回
        return False

# 武器形态数据存储
# 齐天金箍棒形态数据：(攻击速度, 伤害, 距离)
齐天金箍棒形态数据 = [
    (0.45, 90, 3),   # 形态1：正常形态
    (0.1, 60, 2),    # 形态2：快速形态
    (0.8, 500, 9)    # 形态3：强力形态
]

# 武器技能管理器实例
武器技能管理器实例 = 武器技能管理器()

# 注册死神的镰刀技能
def 死神的镰刀_q技能(player, weapon_skill_manager):
    """死神的镰刀Q技能：召唤死神祝福"""
    print("死神的镰刀技能被触发了！")
    
    # 获取游戏实例
    game = player.game
    if game:
        # 1. 获取当前手持工具，消耗耐久
        工具实例, 当前工具 = game.获取当前手持工具()
        if 工具实例 and 当前工具:
            # 消耗1点耐久
            if 工具实例.take_damage(1):
                # 物品损坏，从快捷栏中移除
                当前选中格子 = game.当前选中格子
                if 0 <= 当前选中格子 < len(game.背包管理器.快捷栏物品):
                    game.背包管理器.快捷栏物品[当前选中格子] = None
    
    # 召唤位置在玩家正上方
    summon_x = player.坐标_x
    summon_y = player.坐标_y - 100  # 玩家上方100像素
    
    # 创建死神祝福实体
    death_blessing = 死神祝福实体(summon_x, summon_y, player)
    
    # 添加到召唤实体列表
    weapon_skill_manager.summoned_entities.append(death_blessing)

# 注册死神的镰刀技能
武器技能管理器实例.register_skill("死神的镰刀", "q", 死神的镰刀_q技能, 25.0)  # 25秒冷却时间

# 注册齐天金箍棒技能

def 齐天金箍棒_q技能(player, weapon_skill_manager):
    """齐天金箍棒Q技能：形态切换"""
    print("齐天金箍棒形态切换技能被触发了！")
    
    # 获取当前形态，默认0
    if not hasattr(player, '齐天金箍棒形态'):
        player.齐天金箍棒形态 = 0
    
    # 切换到下一个形态
    player.齐天金箍棒形态 = (player.齐天金箍棒形态 + 1) % len(齐天金箍棒形态数据)
    
    # 发送漂浮文字显示
    当前形态 = player.齐天金箍棒形态 + 1
    # 通过玩家对象访问游戏实例，然后调用_show_notification方法
    if hasattr(player, 'game') and hasattr(player.game, '_show_notification'):
        player.game._show_notification(f"切换形态 {当前形态}")
    
    形态参数 = 齐天金箍棒形态数据[player.齐天金箍棒形态]
    print(f"齐天金箍棒已切换到形态 {当前形态}，攻速：{形态参数[0]}，伤害：{形态参数[1]}，距离：{形态参数[2]}")

# 注册齐天金箍棒技能
武器技能管理器实例.register_skill("齐天金箍棒", "q", 齐天金箍棒_q技能, 0.5)  # 0.5秒冷却时间

# 注册灵火剑技能
def 灵火剑_q技能(player, weapon_skill_manager):
    """灵火剑Q技能：向前冲刺，对生物造成20*5幽灵火焰伤害，冷却10秒"""
    print("灵火剑技能被触发了！")
    # 玩家朝向
    direction = 1 if player.朝向右 else -1
    
    # 冲刺距离和速度 - 调整为8格
    dash_speed = 20  # 统一冲刺速度为20
    
    # 执行冲刺
    player.速度_x = direction * dash_speed  # 直接设置速度，而不是累加
    # 设置冲刺状态
    player.正在冲刺 = True
    player.冲刺计时器 = 0
    # 设置灵火剑的冲刺持续时间，以达到8格的冲刺距离
    player.冲刺持续时间 = 8 * 32 / dash_speed  # 距离 = 速度 * 时间，时间 = 距离 / 速度
    
    # 获取游戏实例
    game = player.game
    if game:
        # 1. 获取当前手持工具，消耗耐久
        工具实例, 当前工具 = game.获取当前手持工具()
        if 工具实例 and 当前工具:
            # 消耗1点耐久
            if 工具实例.take_damage(1):
                # 物品损坏，从快捷栏中移除
                当前选中格子 = game.当前选中格子
                if 0 <= 当前选中格子 < len(game.背包管理器.快捷栏物品):
                    game.背包管理器.快捷栏物品[当前选中格子] = None
        
        # 2. 对路径上的生物造成伤害
        # 创建玩家的碰撞箱 - 增大伤害范围，宽度和高度各增加100像素
        collision_range = 50  # 增加的范围
        player_rect = pygame.Rect(
            player.坐标_x - collision_range, 
            player.坐标_y - collision_range, 
            player.宽 + collision_range * 2, 
            player.高 + collision_range * 2
        )
        
        # 获取所有生物
        all_mobs = []
        if hasattr(game, '世界') and hasattr(game.世界, 'mobs'):
            all_mobs = game.世界.mobs.copy()
        
        # 添加当前boss
        try:
            from boos生物处理 import boss_manager
            if boss_manager.current_boss and boss_manager.current_boss.is_alive():
                all_mobs.append(boss_manager.current_boss)
        except Exception as e:
            pass
        
        # 检查碰撞并造成伤害
        for mob in all_mobs:
            mob_rect = pygame.Rect(mob.x, mob.y, mob.width, mob.height)
            if player_rect.colliderect(mob_rect):
                # 对生物造成伤害
                mob.game = game
                damage = 20
                死亡 = mob.take_damage(damage)
                
                # 创建伤害文本
                if hasattr(game, 'damage_texts'):
                    game.damage_texts.append(game.DamageText(
                        mob.x + mob.width // 2, 
                        mob.y - 10, 
                        damage, 
                        color=(0, 0, 255)
                    ))
                
                # 如果生物死亡，生成掉落物和经验
                if 死亡:
                    # 生成经验球
                    if hasattr(game, 'spawn_exp_orbs'):
                        game.spawn_exp_orbs(mob.x // 32, mob.y // 32)
                    
                    # 生成掉落物
                    try:
                        from 掉落物 import 掉落物管理器实例
                        from 生物系统 import 生物掉落物配置
                        掉落物管理器实例.生成生物掉落物(
                            game.世界, 
                            int(mob.x // 32), 
                            int(mob.y // 32), 
                            mob.name, 
                            getattr(mob, 'mob_id', 0), 
                            生物掉落物配置
                        )
                    except Exception as e:
                        print(f"生成生物掉落物失败: {e}")
                        # 备用方案 - 生成肉块
                        from 物品定义 import 肉块
                        game.世界.spawn_item(int(mob.x // 32), int(mob.y // 32), 肉块, random.randint(1, 3))
        
        # 3. 实现持续伤害效果：每秒20点伤害，持续5秒
        # 创建持续伤害效果
        class 灵火剑持续伤害:
            def __init__(self, target, damage, duration, interval=1.0):
                self.target = target
                self.damage = damage
                self.duration = duration
                self.interval = interval
                self.time_since_last_damage = 0
                self.total_time = 0
                
            def update(self, dt, game):
                self.total_time += dt
                self.time_since_last_damage += dt
                
                # 到达伤害间隔
                if self.time_since_last_damage >= self.interval:
                    # 造成伤害
                    if self.target and hasattr(self.target, 'health') and self.target.health > 0:
                        self.target.game = game
                        死亡 = self.target.take_damage(self.damage)
                        
                        # 创建伤害文本
                        if hasattr(game, 'damage_texts'):
                            game.damage_texts.append(game.DamageText(
                                self.target.x + self.target.width // 2, 
                                self.target.y - 10, 
                                self.damage, 
                                color=(0, 0, 255)
                            ))
                        
                        # 如果生物死亡，生成掉落物和经验
                        if 死亡:
                            # 生成经验球
                            if hasattr(game, 'spawn_exp_orbs'):
                                game.spawn_exp_orbs(self.target.x // 32, self.target.y // 32)
                            
                            # 生成掉落物
                            try:
                                from 掉落物 import 掉落物管理器实例
                                from 生物系统 import 生物掉落物配置
                                掉落物管理器实例.生成生物掉落物(
                                    game.世界, 
                                    int(self.target.x // 32), 
                                    int(self.target.y // 32), 
                                    getattr(self.target, 'name', ''), 
                                    getattr(self.target, 'mob_id', 0), 
                                    生物掉落物配置
                                )
                            except Exception as e:
                                print(f"生成生物掉落物失败: {e}")
                                # 备用方案 - 生成肉块
                                from 物品定义 import 肉块
                                game.世界.spawn_item(int(self.target.x // 32), int(self.target.y // 32), 肉块, random.randint(1, 3))
                    
                    # 重置伤害间隔计时器
                    self.time_since_last_damage = 0
                
                # 检查是否结束
                return self.total_time >= self.duration or (self.target and (not hasattr(self.target, 'health') or self.target.health <= 0))
        
        # 为所有碰撞到的生物添加持续伤害效果
        if not hasattr(game, 'linghuo_sword_effects'):
            game.linghuo_sword_effects = []
        
        for mob in all_mobs:
            mob_rect = pygame.Rect(mob.x, mob.y, mob.width, mob.height)
            if player_rect.colliderect(mob_rect):
                # 添加持续伤害效果
                effect = 灵火剑持续伤害(mob, 20, 5.0)
                game.linghuo_sword_effects.append(effect)

# 注册灵火剑技能
print(f"正在注册灵火剑技能，当前技能字典: {武器技能管理器实例.skills}")
武器技能管理器实例.register_skill("灵火剑", "q", 灵火剑_q技能, 10.0)  # 10秒冷却时间

# 注册超暗黑刺刀技能
def 超暗黑刺刀_q技能(player, weapon_skill_manager):
    """超暗黑刺刀Q技能：向前冲刺，直接造成伤害，冷却1秒"""
    print("超暗黑刺刀技能被触发了！")
    # 玩家朝向
    direction = 1 if player.朝向右 else -1
    
    # 冲刺距离和速度 - 调整为5格
    dash_speed = 20  # 统一冲刺速度为20
    
    # 执行冲刺
    player.速度_x = direction * dash_speed  # 直接设置速度
    # 设置冲刺状态
    player.正在冲刺 = True
    player.冲刺计时器 = 0
    # 设置超暗黑刺刀的冲刺持续时间，以达到5格的冲刺距离
    player.冲刺持续时间 = 5 * 32 / dash_speed  # 距离 = 速度 * 时间，时间 = 距离 / 速度
    
    # 获取游戏实例
    game = player.game
    if game:
        # 1. 获取当前手持工具，消耗耐久
        工具实例, 当前工具 = game.获取当前手持工具()
        if 工具实例 and 当前工具:
            # 消耗1点耐久
            if 工具实例.take_damage(1):
                # 物品损坏，从快捷栏中移除
                当前选中格子 = game.当前选中格子
                if 0 <= 当前选中格子 < len(game.背包管理器.快捷栏物品):
                    game.背包管理器.快捷栏物品[当前选中格子] = None
        # 1. 对路径上的生物造成伤害
        # 创建玩家的碰撞箱 - 增大伤害范围
        collision_range = 50  # 增加的范围
        player_rect = pygame.Rect(
            player.坐标_x - collision_range, 
            player.坐标_y - collision_range, 
            player.宽 + collision_range * 2, 
            player.高 + collision_range * 2
        )
        
        # 获取所有生物
        all_mobs = []
        if hasattr(game, '世界') and hasattr(game.世界, 'mobs'):
            all_mobs = game.世界.mobs.copy()
        
        # 添加当前boss
        try:
            from boos生物处理 import boss_manager
            if boss_manager.current_boss and boss_manager.current_boss.is_alive():
                all_mobs.append(boss_manager.current_boss)
        except Exception as e:
            pass
        
        # 检查碰撞并造成伤害
        for mob in all_mobs:
            mob_rect = pygame.Rect(mob.x, mob.y, mob.width, mob.height)
            if player_rect.colliderect(mob_rect):
                # 对生物造成伤害
                mob.game = game
                damage = 50  # 直接造成伤害
                死亡 = mob.take_damage(damage)
                
                # 创建黑色伤害文本
                if hasattr(game, 'damage_texts'):
                    game.damage_texts.append(game.DamageText(
                        mob.x + mob.width // 2, 
                        mob.y - 10, 
                        damage, 
                        color=(0, 0, 0)  # 黑色伤害状态
                    ))
                
                # 如果生物死亡，生成掉落物和经验
                if 死亡:
                    # 生成经验球
                    if hasattr(game, 'spawn_exp_orbs'):
                        game.spawn_exp_orbs(mob.x // 32, mob.y // 32)
                    
                    # 生成掉落物
                    try:
                        from 掉落物 import 掉落物管理器实例
                        from 生物系统 import 生物掉落物配置
                        掉落物管理器实例.生成生物掉落物(
                            game.世界, 
                            int(mob.x // 32), 
                            int(mob.y // 32), 
                            getattr(mob, 'name', ''), 
                            getattr(mob, 'mob_id', 0), 
                            生物掉落物配置
                        )
                    except Exception as e:
                        print(f"生成生物掉落物失败: {e}")
                        # 备用方案 - 生成肉块
                        from 物品定义 import 肉块
                        game.世界.spawn_item(int(mob.x // 32), int(mob.y // 32), 肉块, random.randint(1, 3))

# 注册超暗黑刺刀技能
print(f"灵火剑技能注册完成，当前技能字典: {武器技能管理器实例.skills}")
武器技能管理器实例.register_skill("超暗黑刺刀", "q", 超暗黑刺刀_q技能, 1.0)  # 1秒冷却时间

# 注册亡灵斧头技能
def 亡灵斧头_q技能(player, weapon_skill_manager):
    """亡灵斧头Q技能：5x5范围，间隔0.3秒重复5次造成伤害，冷却30秒"""
    print("亡灵斧头技能被触发了！")
    
    # 获取游戏实例
    game = player.game
    if game:
        # 1. 获取当前手持工具，消耗耐久
        工具实例, 当前工具 = game.获取当前手持工具()
        if 工具实例 and 当前工具:
            # 消耗1点耐久
            if 工具实例.take_damage(1):
                # 物品损坏，从快捷栏中移除
                当前选中格子 = game.当前选中格子
                if 0 <= 当前选中格子 < len(game.背包管理器.快捷栏物品):
                    game.背包管理器.快捷栏物品[当前选中格子] = None
        # 1. 获取玩家位置
        player_x = player.坐标_x
        player_y = player.坐标_y
        
        # 2. 创建伤害范围：5x5方块，每个方块32像素
        tile_size = 32
        half_range = 2  # 5x5范围，中心为玩家位置，所以向四周扩展2个方块
        
        # 3. 执行多次伤害，每次间隔0.3秒，共5次
        for i in range(5):
            # 计算每次伤害的延迟时间
            delay = i * 0.3
            
            # 在指定延迟后执行伤害
            # 使用pygame的定时器事件来实现延迟伤害
            # 首先获取当前事件类型
            event_type = pygame.USEREVENT + 1000 + i  # 使用唯一的事件类型
            
            # 创建自定义事件，包含伤害信息
            damage_event = pygame.event.Event(event_type, {
                'player_x': player_x,
                'player_y': player_y,
                'half_range': half_range,
                'tile_size': tile_size,
                'damage': 30,  # 每次伤害值
                'game': game
            })
            
            # 设置定时器，在指定延迟后触发事件
            pygame.time.set_timer(damage_event, int(delay * 1000), loops=1)

# 注册亡灵斧头技能
武器技能管理器实例.register_skill("亡灵斧头", "q", 亡灵斧头_q技能, 30.0)  # 30秒冷却时间

# 注册火焰三叉戟技能
def 火焰三叉戟_q技能(player, weapon_skill_manager):
    """火焰三叉戟Q技能：提升攻击速度、伤害和范围，冷却30秒，持续20秒"""
    print("火焰三叉戟技能被触发了！")
    
    # 获取游戏实例
    game = player.game
    if game:
        # 1. 获取当前手持工具，消耗耐久
        工具实例, 当前工具 = game.获取当前手持工具()
        if 工具实例 and 当前工具:
            # 消耗1点耐久
            if 工具实例.take_damage(1):
                # 物品损坏，从快捷栏中移除
                当前选中格子 = game.当前选中格子
                if 0 <= 当前选中格子 < len(game.背包管理器.快捷栏物品):
                    game.背包管理器.快捷栏物品[当前选中格子] = None
        # 应用火焰三叉戟buff效果
        player.火焰三叉戟_buff_active = True
        player.火焰三叉戟_buff_duration = 20.0  # 持续20秒
        player.火焰三叉戟_buff_timer = 0.0  # 计时器重置
        
        # 记录原始属性（如果还没有记录）
        if not hasattr(player, '原始攻击间隔'):
            player.原始攻击间隔 = 0.4  # 假设原始攻击间隔为0.4秒
        if not hasattr(player, '原始伤害加成'):
            player.原始伤害加成 = 1.0  # 原始伤害倍率
        if not hasattr(player, '原始攻击范围'):
            player.原始攻击范围 = 1  # 3x3范围，中心为玩家，向四周扩展1个方块

# 注册火焰三叉戟技能
武器技能管理器实例.register_skill("火焰三叉戟", "q", 火焰三叉戟_q技能, 30.0)  # 30秒冷却时间
print(f"火焰三叉戟技能注册完成，当前技能字典: {武器技能管理器实例.skills}")

# 注册闪电三叉戟技能
def 闪电三叉戟_q技能(player, weapon_skill_manager):
    """闪电三叉戟Q技能：提升攻击速度、伤害和范围，冷却60秒，持续45秒"""
    print("闪电三叉戟技能被触发了！")
    
    # 获取游戏实例
    game = player.game
    if game:
        # 1. 获取当前手持工具，消耗耐久
        工具实例, 当前工具 = game.获取当前手持工具()
        if 工具实例 and 当前工具:
            # 消耗1点耐久
            if 工具实例.take_damage(1):
                # 物品损坏，从快捷栏中移除
                当前选中格子 = game.当前选中格子
                if 0 <= 当前选中格子 < len(game.背包管理器.快捷栏物品):
                    game.背包管理器.快捷栏物品[当前选中格子] = None
        # 应用闪电三叉戟buff效果
        player.闪电三叉戟_buff_active = True
        player.闪电三叉戟_buff_duration = 45.0  # 持续45秒
        player.闪电三叉戟_buff_timer = 0.0  # 计时器重置
        
        # 记录原始属性（如果还没有记录）
        if not hasattr(player, '原始攻击间隔'):
            player.原始攻击间隔 = 0.4  # 假设原始攻击间隔为0.4秒
        if not hasattr(player, '原始伤害加成'):
            player.原始伤害加成 = 1.0  # 原始伤害倍率
        if not hasattr(player, '原始攻击范围'):
            player.原始攻击范围 = 1  # 3x3范围，中心为玩家，向四周扩展1个方块

# 注册闪电三叉戟技能
武器技能管理器实例.register_skill("闪电三叉戟", "q", 闪电三叉戟_q技能, 60.0)  # 60秒冷却时间
print(f"闪电三叉戟技能注册完成，当前技能字典: {武器技能管理器实例.skills}")

# 七彩法杖Q技能
def 七彩法杖_q技能(player, weapon_skill_manager):
    """七彩法杖Q技能：360°发射10发子弹，有目标向外120像素才开始追踪，无目标一直向外"""
    print("七彩法杖技能被触发了！")
    
    # 获取游戏实例
    game = player.game
    if game:
        # 1. 获取当前手持工具，消耗耐久
        工具实例, 当前工具 = game.获取当前手持工具()
        if 工具实例 and 当前工具:
            # 消耗1点耐久
            if 工具实例.take_damage(1):
                # 物品损坏，从快捷栏中移除
                当前选中格子 = game.当前选中格子
                if 0 <= 当前选中格子 < len(game.背包管理器.快捷栏物品):
                    game.背包管理器.快捷栏物品[当前选中格子] = None
        
        # 2. 360°发射10发子弹
        player_x = player.坐标_x + player.宽 // 2
        player_y = player.坐标_y + player.高 // 2
        bullet_count = 10
        damage = 40
        speed = 500
        
        # 可用的子弹图片列表，与普通法杖投掷物保持一致，不包含.png后缀
        bullet_images = [
            "18子弹橙", "18子弹粉", "18子弹红",
            "18子弹蓝", "18子弹绿", "18子弹青"
        ]
        
        # 计算每发子弹的角度间隔
        angle_step = (2 * math.pi) / bullet_count
        
        for i in range(bullet_count):
            # 计算当前子弹的角度
            angle = i * angle_step
            
            # 随机选择一个子弹图片
            image_name = random.choice(bullet_images)
            
            # 创建七彩子弹实例
            bullet = 七彩子弹(
                player_x,
                player_y,
                damage,
                player,
                speed,
                angle,
                image_name
            )
            
            # 添加到武器技能管理器的召唤实体列表
            weapon_skill_manager.summoned_entities.append(bullet)

# 注册七彩法杖技能
武器技能管理器实例.register_skill("七彩法杖", "q", 七彩法杖_q技能, 5.0)  # 5秒冷却时间
print(f"七彩法杖技能注册完成，当前技能字典: {武器技能管理器实例.skills}")

# 森林法杖Q技能
def 森林法杖_q技能(player, weapon_skill_manager):
    """森林法杖Q技能：在玩家周围4*4随机位置召唤5-9颗森林子弹"""
    print("森林法杖技能被触发了！")
    
    # 获取游戏实例
    game = player.game
    if game:
        # 1. 获取当前手持工具，消耗耐久
        工具实例, 当前工具 = game.获取当前手持工具()
        if 工具实例 and 当前工具:
            # 消耗1点耐久
            if 工具实例.take_damage(1):
                # 物品损坏，从快捷栏中移除
                当前选中格子 = game.当前选中格子
                if 0 <= 当前选中格子 < len(game.背包管理器.快捷栏物品):
                    game.背包管理器.快捷栏物品[当前选中格子] = None
        
        # 2. 在玩家周围4*4随机位置召唤5-9颗森林子弹
        player_x = player.坐标_x + player.宽 // 2
        player_y = player.坐标_y + player.高 // 2
        bullet_count = random.randint(5, 9)  # 5-9颗子弹
        damage = 35  # 伤害35
        
        # 4*4范围，每格32像素，所以范围是4*32=128像素
        half_range = 2 * 32  # 64像素
        
        for _ in range(bullet_count):
            # 在玩家周围4*4范围内随机选择一个位置
            offset_x = random.randint(-half_range, half_range)
            offset_y = random.randint(-half_range, half_range)
            
            bullet_x = player_x + offset_x
            bullet_y = player_y + offset_y
            
            # 创建森林子弹实例
            bullet = 森林子弹(bullet_x, bullet_y, damage, player)
            
            # 添加到武器技能管理器的召唤实体列表
            weapon_skill_manager.summoned_entities.append(bullet)

# 注册森林法杖技能
武器技能管理器实例.register_skill("森林法杖", "q", 森林法杖_q技能, 3.0)  # 3秒冷却时间
print(f"森林法杖技能注册完成，当前技能字典: {武器技能管理器实例.skills}")

# 亡灵法杖Q技能
def 亡灵法杖_q技能(player, weapon_skill_manager):
    """亡灵法杖Q技能：3秒内随机召唤21颗子弹，追踪攻击9*9范围内的生物"""
    print("亡灵法杖技能被触发了！")
    
    # 获取游戏实例
    game = player.game
    if game:
        # 1. 获取当前手持工具，消耗耐久
        工具实例, 当前工具 = game.获取当前手持工具()
        if 工具实例 and 当前工具:
            # 消耗1点耐久
            if 工具实例.take_damage(1):
                # 物品损坏，从快捷栏中移除
                当前选中格子 = game.当前选中格子
                if 0 <= 当前选中格子 < len(game.背包管理器.快捷栏物品):
                    game.背包管理器.快捷栏物品[当前选中格子] = None
        
        # 2. 创建亡灵法杖技能效果类，用于3秒内随机召唤子弹
        class 亡灵法杖技能效果:
            def __init__(self, game, player, weapon_skill_manager):
                self.game = game
                self.player = player
                self.weapon_skill_manager = weapon_skill_manager
                self.duration = 3.0  # 持续3秒
                self.lifetime = 0.0  # 当前已持续时间
                self.bullet_count = 21  # 总共召唤21颗子弹
                self.bullets_summoned = 0  # 已召唤子弹数量
                self.last_summon_time = 0.0  # 上次召唤时间
                self.summon_interval = 0.15  # 平均每0.15秒召唤一颗子弹
                self.damage = 12  # 伤害12
                
            def update(self, dt):
                """更新技能效果，随机召唤子弹"""
                self.lifetime += dt
                self.last_summon_time += dt
                
                # 检查是否需要召唤子弹
                if self.bullets_summoned < self.bullet_count:
                    # 随机召唤，平均每0.15秒召唤一颗
                    if self.last_summon_time >= self.summon_interval or random.random() < 0.3 * dt:
                        self.summon_bullet()
                        self.last_summon_time = 0.0
                
                # 返回是否结束
                return self.lifetime >= self.duration or self.bullets_summoned >= self.bullet_count
            
            def summon_bullet(self):
                """在9*9范围内随机位置召唤一颗亡灵子弹"""
                # 9*9范围，每格32像素，所以范围是9*32=288像素
                max_range = 9 * 32  # 288像素
                
                # 玩家中心位置
                player_x = self.player.坐标_x + self.player.宽 // 2
                player_y = self.player.坐标_y + self.player.高 // 2
                
                # 在9*9范围内随机选择一个位置
                offset_x = random.randint(-max_range // 2, max_range // 2)
                offset_y = random.randint(-max_range // 2, max_range // 2)
                
                bullet_x = player_x + offset_x
                bullet_y = player_y + offset_y
                
                # 创建亡灵子弹实例
                bullet = 亡灵子弹(bullet_x, bullet_y, self.damage, self.player)
                
                # 添加到武器技能管理器的召唤实体列表
                self.weapon_skill_manager.summoned_entities.append(bullet)
                
                # 增加已召唤子弹数量
                self.bullets_summoned += 1
        
        # 3. 创建并启动技能效果
        skill_effect = 亡灵法杖技能效果(game, player, weapon_skill_manager)
        
        # 4. 将技能效果添加到游戏的更新列表中
        if not hasattr(game, 'skill_effects'):
            game.skill_effects = []
        game.skill_effects.append(skill_effect)

# 注册亡灵法杖技能
武器技能管理器实例.register_skill("亡灵法杖", "q", 亡灵法杖_q技能, 10.0)  # 10秒冷却时间
print(f"亡灵法杖技能注册完成，当前技能字典: {武器技能管理器实例.skills}")

# 电磁发射器Q技能
def 电磁发射器_q技能(player, weapon_skill_manager):
    """电磁发射器Q技能：以玩家为中心9*9范围内，10s内每0.5s对生物造成1-30伤害，内圈伤害高，外圈减少到1，冷却20s"""
    print("电磁发射器技能被触发了！")
    
    # 获取游戏实例
    game = player.game
    if game:
        # 1. 获取当前手持工具，消耗耐久
        工具实例, 当前工具 = game.获取当前手持工具()
        if 工具实例 and 当前工具:
            # 消耗1点耐久
            if 工具实例.take_damage(1):
                # 物品损坏，从快捷栏中移除
                当前选中格子 = game.当前选中格子
                if 0 <= 当前选中格子 < len(game.背包管理器.快捷栏物品):
                    game.背包管理器.快捷栏物品[当前选中格子] = None
        
        # 2. 创建电磁发射器技能效果类，用于10秒内持续伤害
        class 电磁发射器技能效果:
            def __init__(self, game, player, weapon_skill_manager):
                self.game = game
                self.player = player
                self.weapon_skill_manager = weapon_skill_manager
                self.duration = 10.0  # 持续10秒
                self.lifetime = 0.0  # 当前已持续时间
                self.last_damage_time = 0.0  # 上次伤害时间
                self.damage_interval = 0.5  # 每0.5秒造成一次伤害
                self.max_damage = 30  # 最大伤害
                self.min_damage = 1  # 最小伤害
                self.range = 9 * 32  # 9*9范围，每格32像素
                
            def update(self, dt):
                """更新技能效果，每0.5秒造成一次伤害"""
                self.lifetime += dt
                self.last_damage_time += dt
                
                # 每0.5秒对范围内生物造成伤害
                if self.last_damage_time >= self.damage_interval:
                    # 重置伤害计时器
                    self.last_damage_time = 0.0
                    
                    # 计算玩家中心位置
                    player_center_x = self.player.坐标_x + self.player.宽 // 2
                    player_center_y = self.player.坐标_y + self.player.高 // 2
                    
                    # 获取所有生物
                    all_mobs = []
                    if hasattr(self.game.世界, 'mobs'):
                        all_mobs = self.game.世界.mobs.copy()
                    
                    # 添加当前boss
                    try:
                        from boos生物处理 import boss_manager
                        if boss_manager.current_boss and boss_manager.current_boss.is_alive():
                            all_mobs.append(boss_manager.current_boss)
                    except:
                        pass
                    
                    # 对范围内生物造成伤害
                    for mob in all_mobs:
                        # 计算生物中心位置
                        mob_center_x = mob.x + mob.width // 2
                        mob_center_y = mob.y + mob.height // 2
                        
                        # 计算生物到玩家的距离
                        distance = ((mob_center_x - player_center_x) ** 2 + (mob_center_y - player_center_y) ** 2) ** 0.5
                        
                        # 如果在9*9范围内
                        if distance <= self.range:
                            # 计算伤害：内圈高，外圈低，线性减少
                            damage_ratio = max(0, 1 - (distance / self.range))
                            damage = int(self.min_damage + (self.max_damage - self.min_damage) * damage_ratio)
                            
                            # 对生物造成伤害
                            mob.game = self.game
                            death = mob.take_damage(damage)
                            
                            # 显示伤害数字
                            if hasattr(self.game, 'damage_texts'):
                                from 游玩 import DamageText
                                damage_text = DamageText(mob.x, mob.y, damage, is_player=False, color=(135, 206, 250))
                                self.game.damage_texts.append(damage_text)
                            
                            # 如果目标死亡，生成经验球和掉落物
                            if death:
                                if hasattr(self.game, 'spawn_exp_orbs'):
                                    self.game.spawn_exp_orbs(mob.x // 32, mob.y // 32)
                                
                                # 尝试生成掉落物
                                try:
                                    from 掉落物 import 掉落物管理器实例
                                    from 生物系统 import 生物掉落物配置
                                    掉落物管理器实例.生成生物掉落物(
                                        self.game.世界,
                                        int(mob.x // 32),
                                        int(mob.y // 32),
                                        getattr(mob, 'name', ''),
                                        getattr(mob, 'mob_id', 0),
                                        生物掉落物配置
                                    )
                                except Exception as e:
                                    print(f"生成生物掉落物失败: {e}")
                
                # 返回是否应该移除（持续时间结束）
                return self.lifetime >= self.duration
        
        # 添加技能效果到游戏的skill_effects列表
        if not hasattr(game, 'skill_effects'):
            game.skill_effects = []
        
        # 创建技能效果实例
        skill_effect = 电磁发射器技能效果(game, player, weapon_skill_manager)
        game.skill_effects.append(skill_effect)

# 注册电磁发射器技能
武器技能管理器实例.register_skill("电磁发射器", "q", 电磁发射器_q技能, 20.0)  # 20秒冷却时间
print(f"电磁发射器技能注册完成，当前技能字典: {武器技能管理器实例.skills}")

# 星星投掷物类
class 星星投掷物:
    """星星投掷物类，自动攻击目标，无目标时悬浮"""
    def __init__(self, x, y, damage, owner, lifetime=10.0):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.damage = damage
        self.owner = owner
        self.lifetime = lifetime
        self.target = None
        self.speed = 200
        self.hover_offset = 0
        self.hover_direction = 1
        self.hover_speed = 100
    
    def update(self, dt, world, player, game):
        """更新星星投掷物状态"""
        self.lifetime -= dt
        
        # 寻找目标
        if not self.target:
            self.find_target(world.mobs)
        
        # 移动逻辑
        if self.target:
            # 向目标移动
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                # 计算移动方向
                move_x = (dx / distance) * self.speed * dt
                move_y = (dy / distance) * self.speed * dt
                self.x += move_x
                self.y += move_y
            
            # 检查是否击中目标
            if self.rect.colliderect(pygame.Rect(self.target.x, self.target.y, self.target.width, self.target.height)):
                # 造成伤害
                if hasattr(self.target, 'take_damage'):
                    self.target.take_damage(self.damage)
                    
                    # 1. 显示伤害数字
                    if hasattr(game, 'damage_texts'):
                        from 游玩 import DamageText
                        damage_text = DamageText(self.target.x, self.target.y, self.damage, is_player=False)
                        game.damage_texts.append(damage_text)
                    
                    # 2. 生成经验球
                    game.spawn_exp_orbs(self.target.x // 32, self.target.y // 32)
                    

                # 设置寿命为0，表示需要移除
                self.lifetime = 0
        else:
            # 无目标时悬浮
            self.hover_offset += self.hover_speed * self.hover_direction * dt
            if self.hover_offset > 16 or self.hover_offset < -16:
                self.hover_direction *= -1
            self.y += self.hover_direction * self.hover_speed * dt
        
        # 更新矩形
        self.rect.x = self.x
        self.rect.y = self.y + self.hover_offset
        
        # 不需要返回值，should_remove()方法会处理移除逻辑
    
    def find_target(self, mobs):
        """寻找玩家9*9范围内最近的可攻击生物"""
        min_distance = float('inf')
        closest_mob = None
        
        # 9*9范围，每个方块32像素，所以总范围是9*32=288像素
        max_range = 288
        
        for mob in mobs:
            # 跳过玩家本身
            if hasattr(mob, 'is_player') and mob.is_player:
                continue
            # 跳过无敌或不可攻击的生物
            if hasattr(mob, 'is_invulnerable') and mob.is_invulnerable:
                continue
            
            # 检查目标是否在玩家9*9范围内
            # 首先获取玩家位置
            player_x = self.owner.坐标_x
            player_y = self.owner.坐标_y
            
            # 计算目标到玩家的距离
            dx_player = mob.x - player_x
            dy_player = mob.y - player_y
            distance_to_player = math.sqrt(dx_player**2 + dy_player**2)
            
            if distance_to_player <= max_range:
                # 计算到投掷物的距离
                dx = mob.x - self.x
                dy = mob.y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance < min_distance:
                    min_distance = distance
                    closest_mob = mob
        
        self.target = closest_mob
    
    def draw(self, surface, camera_x, camera_y):
        """绘制星星投掷物"""
        # 使用图片加载器绘制星星投掷物
        try:
            from 图片加载 import 图片管理器
            图片 = 图片管理器.获取图片("星星投掷物")
            if 图片:
                # 计算绘制位置
                draw_x = self.x - camera_x
                draw_y = self.y + self.hover_offset - camera_y
                # 缩放图片为20*20像素
                scaled_image = pygame.transform.scale(图片, (self.width, self.height))
                surface.blit(scaled_image, (draw_x, draw_y))
        except Exception as e:
            # 如果图片加载失败，绘制一个黄色矩形作为占位符
            draw_x = self.x - camera_x
            draw_y = self.y + self.hover_offset - camera_y
            pygame.draw.rect(surface, (255, 255, 0), (draw_x, draw_y, self.width, self.height))
    
    def should_remove(self):
        """判断是否需要移除"""
        return self.lifetime <= 0

# 星星法杖Q技能
def 星星法杖_q技能(player, weapon_skill_manager):
    """星星法杖Q技能：在3x3范围内随机生成星星投掷物，自动攻击目标"""
    print("星星法杖技能被触发了！")
    
    # 获取游戏实例
    game = player.game
    if game:
        # 1. 获取当前手持工具，消耗耐久
        工具实例, 当前工具 = game.获取当前手持工具()
        if 工具实例 and 当前工具:
            # 消耗1点耐久
            if 工具实例.take_damage(1):
                # 物品损坏，从快捷栏中移除
                当前选中格子 = game.当前选中格子
                if 0 <= 当前选中格子 < len(game.背包管理器.快捷栏物品):
                    game.背包管理器.快捷栏物品[当前选中格子] = None
        
        # 2. 在玩家周围3x3范围内随机生成星星投掷物
        player_x = player.坐标_x
        player_y = player.坐标_y
        tile_size = 32
        half_range = 1  # 3x3范围，中心为玩家，向四周扩展1个方块
        
        # 生成3-7个星星投掷物
        star_count = random.randint(3, 7)
        for _ in range(star_count):
            # 在3x3范围内随机选择一个位置
            offset_x = random.randint(-half_range, half_range) * tile_size
            offset_y = random.randint(-half_range, half_range) * tile_size
            star_x = player_x + offset_x
            star_y = player_y + offset_y
            
            # 创建星星投掷物实例
            star = 星星投掷物(star_x, star_y, 30, player, lifetime=10.0)
            
            # 添加到武器技能管理器的召唤实体列表
            weapon_skill_manager.summoned_entities.append(star)

# 七彩法杖子弹类
class 七彩子弹:
    """七彩法杖子弹类，360°发射，有目标向外120像素才开始追踪，无目标一直向外"""
    def __init__(self, x, y, damage, owner, speed, angle, image_name, lifetime=10.0):
        self.x = x
        self.y = y
        self.初始位置_x = x  # 记录初始发射位置
        self.初始位置_y = y  # 记录初始发射位置
        self.width = 30  # 改为30像素宽
        self.height = 30  # 改为30像素高
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.damage = damage
        self.owner = owner
        self.speed = speed
        self.angle = angle
        self.image_name = image_name.replace('.png', '')  # 移除.png后缀，与普通法杖投掷物保持一致
        self.lifetime = lifetime
        self.target = None
        self.has_started_tracking = False
        self.has_moved_120_pixels = False  # 标记是否已移动120像素
        self.velocity_x = math.cos(angle) * speed
        self.velocity_y = math.sin(angle) * speed
        
    def update(self, dt, world, player, game):
        """更新七彩子弹状态"""
        self.lifetime -= dt
        
        # 计算从初始位置移动的距离
        dx_from_start = self.x - self.初始位置_x
        dy_from_start = self.y - self.初始位置_y
        distance_from_start = math.hypot(dx_from_start, dy_from_start)
        
        # 如果还没有移动120像素，继续直线飞行
        if distance_from_start < 120:
            # 记录还没有移动120像素
            self.has_moved_120_pixels = False
        else:
            # 已经移动了120像素，可以开始寻找目标和追踪
            self.has_moved_120_pixels = True
            
            # 寻找目标
            if not self.target:
                self.find_target(world)
            
            # 如果有目标，开始追踪
            if self.target and not self.has_started_tracking:
                self.has_started_tracking = True
        
        # 如果已经开始追踪目标
        if self.target and self.has_started_tracking:
            # 追踪目标
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            distance = math.hypot(dx, dy)
            
            if distance > 0:
                # 计算追踪方向
                dir_x = dx / distance
                dir_y = dy / distance
                
                # 更新速度方向和角度
                self.velocity_x = dir_x * self.speed
                self.velocity_y = dir_y * self.speed
                self.angle = math.atan2(self.velocity_y, self.velocity_x)
        
        # 更新位置
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # 更新矩形
        self.rect.x = self.x
        self.rect.y = self.y
        
        # 检查是否击中目标
        if self.target:
            if self.rect.colliderect(pygame.Rect(self.target.x, self.target.y, self.target.width, self.target.height)):
                # 造成伤害
                if hasattr(self.target, 'take_damage'):
                    self.target.game = game
                    death = self.target.take_damage(self.damage)
                    
                    # 创建伤害文本
                    if hasattr(game, 'damage_texts'):
                        game.damage_texts.append(game.DamageText(
                            self.target.x + self.target.width // 2,
                            self.target.y - 10,
                            self.damage
                        ))
                    
                    # 如果目标死亡，生成经验球和掉落物
                    if death:
                        if hasattr(game, 'spawn_exp_orbs'):
                            game.spawn_exp_orbs(self.target.x // 32, self.target.y // 32)
                        
                        # 尝试生成掉落物
                        try:
                            from 掉落物 import 掉落物管理器实例
                            from 生物系统 import 生物掉落物配置
                            掉落物管理器实例.生成生物掉落物(
                                game.世界,
                                int(self.target.x // 32),
                                int(self.target.y // 32),
                                getattr(self.target, 'name', ''),
                                getattr(self.target, 'mob_id', 0),
                                生物掉落物配置
                            )
                        except Exception as e:
                            print(f"生成生物掉落物失败: {e}")
                
                # 子弹命中后消失
                self.lifetime = 0
        
    def find_target(self, world):
        """寻找12*12范围内的目标"""
        if hasattr(world, 'mobs'):
            all_mobs = world.mobs.copy()
            
            # 添加当前boss
            try:
                from boos生物处理 import boss_manager
                if boss_manager.current_boss and boss_manager.current_boss.is_alive():
                    all_mobs.append(boss_manager.current_boss)
            except Exception as e:
                pass
            
            # 12*12范围，每格32像素，所以范围是12*32=384像素
            max_range = 12 * 32  # 384像素
            
            # 寻找12*12范围内最近的目标
            closest_target = None
            closest_distance = float('inf')
            
            for mob in all_mobs:
                # 跳过玩家
                if hasattr(mob, 'is_player') and mob.is_player:
                    continue
                
                # 计算距离
                dx = mob.x - self.x
                dy = mob.y - self.y
                distance = math.hypot(dx, dy)
                
                # 只考虑12*12范围内的目标
                if distance < closest_distance and distance <= max_range:
                    closest_target = mob
                    closest_distance = distance
            
            self.target = closest_target
    
    def draw(self, surface, camera_x, camera_y):
        """绘制七彩子弹，参考普通法杖投掷物的绘制方式"""
        # 使用图片加载器绘制投掷物，根据角度调整方向
        try:
            from 图片加载 import 图片管理器
            图片 = 图片管理器.获取图片(self.image_name)
            if 图片:
                # 计算绘制位置
                draw_x = self.x - camera_x
                draw_y = self.y - camera_y
                
                # 调整图片大小为30*30像素
                scaled_image = pygame.transform.scale(图片, (self.width, self.height))
                
                # 旋转图片，使投掷物面向移动方向
                # 图片默认朝向右，所以需要将角度转换为合适的旋转角度
                rotated_image = pygame.transform.rotate(scaled_image, -math.degrees(self.angle))
                
                # 计算旋转后的矩形，确保中心位置正确
                rotated_rect = rotated_image.get_rect(center=(draw_x + self.width//2, draw_y + self.height//2))
                surface.blit(rotated_image, rotated_rect)
        except Exception as e:
            # 如果图片加载失败，绘制一个彩色矩形作为占位符
            draw_x = self.x - camera_x
            draw_y = self.y - camera_y
            # 根据图片名称选择颜色
            color_map = {
                "18子弹橙": (255, 165, 0),
                "18子弹粉": (255, 192, 203),
                "18子弹红": (255, 0, 0),
                "18子弹蓝": (0, 0, 255),
                "18子弹绿": (0, 255, 0),
                "18子弹青": (0, 255, 255)
            }
            color = color_map.get(self.image_name, (255, 255, 255))
            pygame.draw.rect(surface, color, (draw_x, draw_y, self.width, self.height))
    
    def should_remove(self):
        """判断是否需要移除"""
        return self.lifetime <= 0

# 亡灵法杖子弹类
class 亡灵子弹:
    """亡灵法杖子弹类，追踪攻击9*9范围内的生物"""
    def __init__(self, x, y, damage, owner, lifetime=10.0):
        self.x = x
        self.y = y
        self.width = 18  # 18像素宽
        self.height = 18  # 18像素高
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.damage = damage
        self.owner = owner
        self.lifetime = lifetime
        self.target = None
        self.speed = 400  # 移动速度
        self.sight_range = 9 * 32  # 9格视野范围
        self.velocity_x = 0
        self.velocity_y = 0
        self.image_name = "21子弹黑"  # 图片名称
        
    def update(self, dt, world, player, game):
        """更新亡灵子弹状态：有目标追踪，无目标围绕玩家旋转"""
        self.lifetime -= dt
        
        # 寻找目标
        if not self.target:
            self.find_target(world)
        
        # 玩家中心位置
        player_center_x = player.坐标_x + player.宽 // 2
        player_center_y = player.坐标_y + player.高 // 2
        
        # 移动逻辑
        if self.target:
            # 追踪目标
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            distance = math.hypot(dx, dy)
            
            if distance > 0:
                # 计算追踪方向
                dir_x = dx / distance
                dir_y = dy / distance
                
                # 更新速度方向
                self.velocity_x = dir_x * self.speed
                self.velocity_y = dir_y * self.speed
        else:
            # 无目标时，围绕玩家高速旋转
            # 计算当前位置到玩家中心的距离
            dx = self.x - player_center_x
            dy = self.y - player_center_y
            current_distance = math.hypot(dx, dy)
            
            # 如果距离为0，设置一个初始距离
            if current_distance < 0.1:
                current_distance = 50
                self.x = player_center_x + current_distance
                self.y = player_center_y
            
            # 计算当前角度
            current_angle = math.atan2(dy, dx)
            
            # 高速旋转：增加角度
            rotation_speed = 5.0  # 每秒旋转5圈
            new_angle = current_angle + rotation_speed * dt
            
            # 计算新位置
            self.x = player_center_x + math.cos(new_angle) * current_distance
            self.y = player_center_y + math.sin(new_angle) * current_distance
        
        # 更新位置
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # 更新矩形
        self.rect.x = self.x
        self.rect.y = self.y
        
        # 检查是否击中目标
        if self.target:
            if self.rect.colliderect(pygame.Rect(self.target.x, self.target.y, self.target.width, self.target.height)):
                # 造成伤害
                if hasattr(self.target, 'take_damage'):
                    self.target.game = game
                    death = self.target.take_damage(self.damage)
                    
                    # 创建伤害文本
                    if hasattr(game, 'damage_texts'):
                        game.damage_texts.append(game.DamageText(
                            self.target.x + self.target.width // 2,
                            self.target.y - 10,
                            self.damage
                        ))
                    
                    # 如果目标死亡，生成经验球和掉落物
                    if death:
                        if hasattr(game, 'spawn_exp_orbs'):
                            game.spawn_exp_orbs(self.target.x // 32, self.target.y // 32)
                        
                        # 尝试生成掉落物
                        try:
                            from 掉落物 import 掉落物管理器实例
                            from 生物系统 import 生物掉落物配置
                            掉落物管理器实例.生成生物掉落物(
                                game.世界,
                                int(self.target.x // 32),
                                int(self.target.y // 32),
                                getattr(self.target, 'name', ''),
                                getattr(self.target, 'mob_id', 0),
                                生物掉落物配置
                            )
                        except Exception as e:
                            print(f"生成生物掉落物失败: {e}")
                
                # 子弹命中后消失
                self.lifetime = 0
        
    def find_target(self, world):
        """寻找9*9范围内的目标"""
        if hasattr(world, 'mobs'):
            all_mobs = world.mobs.copy()
            
            # 添加当前boss
            try:
                from boos生物处理 import boss_manager
                if boss_manager.current_boss and boss_manager.current_boss.is_alive():
                    all_mobs.append(boss_manager.current_boss)
            except Exception as e:
                pass
            
            # 9*9范围，每格32像素，所以范围是9*32=288像素
            max_range = 9 * 32  # 288像素
            
            # 寻找9*9范围内最近的目标
            closest_target = None
            closest_distance = float('inf')
            
            for mob in all_mobs:
                # 跳过玩家
                if hasattr(mob, 'is_player') and mob.is_player:
                    continue
                
                # 计算距离
                dx = mob.x - self.x
                dy = mob.y - self.y
                distance = math.hypot(dx, dy)
                
                if distance <= max_range and distance < closest_distance:
                    closest_target = mob
                    closest_distance = distance
            
            self.target = closest_target
    
    def draw(self, surface, camera_x, camera_y):
        """绘制亡灵子弹"""
        # 使用图片加载器绘制子弹
        try:
            from 图片加载 import 图片管理器
            图片 = 图片管理器.获取图片(self.image_name)
            if 图片:
                # 计算绘制位置
                draw_x = self.x - camera_x
                draw_y = self.y - camera_y
                
                # 调整图片大小为18*18像素
                scaled_image = pygame.transform.scale(图片, (self.width, self.height))
                surface.blit(scaled_image, (draw_x, draw_y))
        except Exception as e:
            # 如果图片加载失败，绘制一个黑色矩形作为占位符
            draw_x = self.x - camera_x
            draw_y = self.y - camera_y
            pygame.draw.rect(surface, (0, 0, 0), (draw_x, draw_y, self.width, self.height))
    
    def should_remove(self):
        """判断是否需要移除"""
        return self.lifetime <= 0

# 森林法杖子弹类
class 森林子弹:
    """森林法杖子弹类，围绕玩家旋转向外移动，不超过9*9范围"""
    def __init__(self, x, y, damage, owner, lifetime=10.0):
        self.x = x
        self.y = y
        self.初始位置_x = x
        self.初始位置_y = y
        self.width = 18  # 18像素宽
        self.height = 18  # 18像素高
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.damage = damage
        self.owner = owner
        self.lifetime = lifetime
        self.speed = 400  # 速度400
        
        # 旋转相关属性
        self.angle = random.uniform(0, 2 * math.pi)  # 初始角度随机
        self.旋转速度 = random.uniform(1.0, 3.0)  # 旋转速度随机
        self.移动距离 = 0  # 已移动距离
        self.移动速度 = 20  # 向外移动速度
        
        # 9*9范围，每格32像素，所以最大范围是4.5*32=144像素
        self.max_range = 4.5 * 32  # 144像素
        
        # 计算与玩家的初始相对位置
        self.player_center_x = owner.坐标_x + owner.宽 // 2
        self.player_center_y = owner.坐标_y + owner.高 // 2
        
        # 计算初始距离
        dx = self.x - self.player_center_x
        dy = self.y - self.player_center_y
        self.initial_distance = math.hypot(dx, dy)
        
    def update(self, dt, world, player, game):
        """更新森林子弹状态：围绕玩家旋转向外移动"""
        self.lifetime -= dt
        
        # 更新玩家中心位置
        self.player_center_x = player.坐标_x + player.宽 // 2
        self.player_center_y = player.坐标_y + player.高 // 2
        
        # 1. 旋转：增加角度
        self.angle += self.旋转速度 * dt
        
        # 2. 向外移动：增加移动距离
        self.移动距离 += self.移动速度 * dt
        
        # 3. 计算当前距离（初始距离 + 向外移动距离）
        current_distance = self.initial_distance + self.移动距离
        
        # 4. 限制在9*9范围内
        current_distance = min(current_distance, self.max_range)
        
        # 5. 计算新位置
        self.x = self.player_center_x + math.cos(self.angle) * current_distance
        self.y = self.player_center_y + math.sin(self.angle) * current_distance
        
        # 6. 更新矩形
        self.rect.x = self.x
        self.rect.y = self.y
        
        # 7. 检查是否击中任何生物
        if hasattr(world, 'mobs'):
            all_mobs = world.mobs.copy()
            
            # 添加当前boss
            try:
                from boos生物处理 import boss_manager
                if boss_manager.current_boss and boss_manager.current_boss.is_alive():
                    all_mobs.append(boss_manager.current_boss)
            except Exception as e:
                pass
            
            for mob in all_mobs:
                # 跳过玩家
                if hasattr(mob, 'is_player') and mob.is_player:
                    continue
                
                # 检查碰撞
                mob_rect = pygame.Rect(mob.x, mob.y, mob.width, mob.height)
                if self.rect.colliderect(mob_rect):
                    # 造成伤害
                    if hasattr(mob, 'take_damage'):
                        mob.game = game
                        death = mob.take_damage(self.damage)
                        
                        # 创建伤害文本
                        if hasattr(game, 'damage_texts'):
                            game.damage_texts.append(game.DamageText(
                                mob.x + mob.width // 2,
                                mob.y - 10,
                                self.damage
                            ))
                        
                        # 如果目标死亡，生成经验球和掉落物
                        if death:
                            if hasattr(game, 'spawn_exp_orbs'):
                                game.spawn_exp_orbs(mob.x // 32, mob.y // 32)
                            
                            # 尝试生成掉落物
                            try:
                                from 掉落物 import 掉落物管理器实例
                                from 生物系统 import 生物掉落物配置
                                掉落物管理器实例.生成生物掉落物(
                                    game.世界,
                                    int(mob.x // 32),
                                    int(mob.y // 32),
                                    getattr(mob, 'name', ''),
                                    getattr(mob, 'mob_id', 0),
                                    生物掉落物配置
                                )
                            except Exception as e:
                                print(f"生成生物掉落物失败: {e}")
                    
                    # 子弹命中后消失
                    self.lifetime = 0
                    break
        
    def find_target(self, world):
        """不再需要寻找目标，直接返回"""
        pass
    
    def draw(self, surface, camera_x, camera_y):
        """绘制森林子弹，大小18*18像素"""
        # 使用图片加载器绘制子弹
        try:
            from 图片加载 import 图片管理器
            图片 = 图片管理器.获取图片("森林子弹")
            if 图片:
                # 计算绘制位置
                draw_x = self.x - camera_x
                draw_y = self.y - camera_y
                
                # 调整图片大小为18*18像素
                scaled_image = pygame.transform.scale(图片, (self.width, self.height))
                surface.blit(scaled_image, (draw_x, draw_y))
        except Exception as e:
            # 如果图片加载失败，绘制一个绿色矩形作为占位符
            draw_x = self.x - camera_x
            draw_y = self.y - camera_y
            pygame.draw.rect(surface, (0, 255, 128), (draw_x, draw_y, self.width, self.height))
    
    def should_remove(self):
        """判断是否需要移除"""
        return self.lifetime <= 0

# 骨毒法杖投掷物类
class 骨毒投掷物:
    """骨毒法杖投掷物类，无目标时缓慢远离玩家，有目标时追踪"""
    def __init__(self, x, y, damage, owner, lifetime=10.0):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.damage = damage
        self.owner = owner
        self.lifetime = lifetime
        self.target = None
        self.speed = 100  # 缓慢移动
        self.angle = random.uniform(0, 2 * math.pi)  # 随机初始角度
        self.velocity_x = math.cos(self.angle) * self.speed
        self.velocity_y = math.sin(self.angle) * self.speed
        
    def update(self, dt, world, player, game):
        """更新骨毒投掷物状态"""
        self.lifetime -= dt
        
        # 寻找目标（9*9范围内）
        if not self.target:
            self.find_target(world.mobs)
        
        # 移动逻辑
        if self.target:
            # 向目标移动
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                # 计算移动方向
                move_x = (dx / distance) * self.speed * dt
                move_y = (dy / distance) * self.speed * dt
                self.x += move_x
                self.y += move_y
                
                # 更新角度，使投掷物面向目标
                self.angle = math.atan2(dy, dx)
        else:
            # 无目标时向外移动
            self.x += self.velocity_x * dt
            self.y += self.velocity_y * dt
        
        # 更新矩形
        self.rect.x = self.x
        self.rect.y = self.y
        
        # 检查是否击中目标
        if self.target:
            if self.rect.colliderect(pygame.Rect(self.target.x, self.target.y, self.target.width, self.target.height)):
                # 造成伤害
                if hasattr(self.target, 'take_damage'):
                    self.target.take_damage(self.damage)
                    
                    # 显示伤害数字
                    if hasattr(game, 'damage_texts'):
                        from 游玩 import DamageText
                        damage_text = DamageText(self.target.x, self.target.y, self.damage, is_player=False)
                        game.damage_texts.append(damage_text)
                    
                    # 生成经验球
                    game.spawn_exp_orbs(self.target.x // 32, self.target.y // 32)
                
                # 设置寿命为0，表示需要移除
                self.lifetime = 0
        
        # 不需要返回值，should_remove()方法会处理移除逻辑
    
    def find_target(self, mobs):
        """寻找玩家9*9范围内最近的可攻击生物"""
        min_distance = float('inf')
        closest_mob = None
        
        # 9*9范围，每个方块32像素，所以总范围是9*32=288像素
        max_range = 288
        
        for mob in mobs:
            # 跳过玩家本身
            if hasattr(mob, 'is_player') and mob.is_player:
                continue
            # 跳过无敌或不可攻击的生物
            if hasattr(mob, 'is_invulnerable') and mob.is_invulnerable:
                continue
            
            # 检查目标是否在玩家9*9范围内
            player_x = self.owner.坐标_x
            player_y = self.owner.坐标_y
            
            # 计算目标到玩家的距离
            dx_player = mob.x - player_x
            dy_player = mob.y - player_y
            distance_to_player = math.sqrt(dx_player**2 + dy_player**2)
            
            if distance_to_player <= max_range:
                # 计算到投掷物的距离
                dx = mob.x - self.x
                dy = mob.y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance < min_distance:
                    min_distance = distance
                    closest_mob = mob
        
        self.target = closest_mob
    
    def draw(self, surface, camera_x, camera_y):
        """绘制骨毒投掷物"""
        # 使用图片加载器绘制投掷物，根据角度调整方向
        try:
            from 图片加载 import 图片管理器
            图片 = 图片管理器.获取图片("67投掷物")
            if 图片:
                # 计算绘制位置
                draw_x = self.x - camera_x
                draw_y = self.y - camera_y
                
                # 调整图片大小
                scaled_image = pygame.transform.scale(图片, (self.width, self.height))
                
                # 旋转图片，使投掷物面向移动方向
                # 图片默认朝向右，所以需要将角度转换为合适的旋转角度
                rotated_image = pygame.transform.rotate(scaled_image, -math.degrees(self.angle))
                
                # 计算旋转后的矩形，确保中心位置正确
                rotated_rect = rotated_image.get_rect(center=(draw_x + self.width//2, draw_y + self.height//2))
                surface.blit(rotated_image, rotated_rect)
        except Exception as e:
            # 如果图片加载失败，绘制一个绿色矩形作为占位符
            draw_x = self.x - camera_x
            draw_y = self.y - camera_y
            pygame.draw.rect(surface, (0, 255, 0), (draw_x, draw_y, self.width, self.height))
    
    def should_remove(self):
        """判断是否需要移除"""
        return self.lifetime <= 0

# 骨毒法杖Q技能
def 骨毒法杖_q技能(player, weapon_skill_manager):
    """骨毒法杖Q技能：召唤骨毒投掷物，自动攻击9*9范围内的目标"""
    print("骨毒法杖技能被触发了！")
    
    # 获取游戏实例
    game = player.game
    if game:
        # 1. 获取当前手持工具，消耗耐久
        工具实例, 当前工具 = game.获取当前手持工具()
        if 工具实例 and 当前工具:
            # 消耗1点耐久
            if 工具实例.take_damage(1):
                # 物品损坏，从快捷栏中移除
                当前选中格子 = game.当前选中格子
                if 0 <= 当前选中格子 < len(game.背包管理器.快捷栏物品):
                    game.背包管理器.快捷栏物品[当前选中格子] = None
        
        # 2. 在玩家位置生成骨毒投掷物
        player_x = player.坐标_x
        player_y = player.坐标_y
        
        # 创建骨毒投掷物实例
        star = 骨毒投掷物(player_x, player_y, 25, player, lifetime=10.0)
        
        # 添加到武器技能管理器的召唤实体列表
        weapon_skill_manager.summoned_entities.append(star)

# 普通法杖投掷物类
class 普通法杖投掷物:
    """普通法杖投掷物类，跟随鼠标位置，击中目标造成伤害"""
    def __init__(self, x, y, damage, owner, mouse_pos, camera_x, camera_y, lifetime=10.0):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.damage = damage
        self.owner = owner
        self.lifetime = lifetime
        self.speed = 300  # 投掷物速度300
        
        # 计算鼠标在世界坐标中的位置
        self.world_mouse_x = mouse_pos[0] + camera_x
        self.world_mouse_y = mouse_pos[1] + camera_y
        
        # 计算初始角度和速度向量
        dx = self.world_mouse_x - x
        dy = self.world_mouse_y - y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.angle = math.atan2(dy, dx)
            self.velocity_x = (dx / distance) * self.speed
            self.velocity_y = (dy / distance) * self.speed
        else:
            self.angle = 0
            self.velocity_x = self.speed
            self.velocity_y = 0
        
    def update(self, dt, world, player, game):
        """更新普通法杖投掷物状态"""
        self.lifetime -= dt
        
        # 移动逻辑：沿着初始方向直线飞行
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # 更新矩形
        self.rect.x = self.x
        self.rect.y = self.y
        
        # 检查是否击中任何生物
        all_mobs = world.mobs.copy()
        # 添加当前boss到检查列表
        try:
            from boos生物处理 import boss_manager
            if boss_manager.current_boss and boss_manager.current_boss.is_alive():
                all_mobs.append(boss_manager.current_boss)
        except Exception as e:
            pass
        
        for mob in all_mobs:
            # 跳过玩家本身
            if hasattr(mob, 'is_player') and mob.is_player:
                continue
            
            # 检查碰撞
            mob_rect = pygame.Rect(mob.x, mob.y, mob.width, mob.height)
            if self.rect.colliderect(mob_rect):
                # 造成伤害
                if hasattr(mob, 'take_damage'):
                    mob.take_damage(self.damage)
                    
                    # 显示伤害数字
                    if hasattr(game, 'damage_texts'):
                        from 游玩 import DamageText
                        damage_text = DamageText(mob.x, mob.y, self.damage, is_player=False)
                        game.damage_texts.append(damage_text)
                    
                    # 生成经验球
                    game.spawn_exp_orbs(mob.x // 32, mob.y // 32)
                
                # 设置寿命为0，表示需要移除
                self.lifetime = 0
                break
        
        # 不需要返回值，should_remove()方法会处理移除逻辑
    
    def draw(self, surface, camera_x, camera_y):
        """绘制普通法杖投掷物"""
        # 使用图片加载器绘制投掷物，根据角度调整方向
        try:
            from 图片加载 import 图片管理器
            图片 = 图片管理器.获取图片("18子弹粉")
            if 图片:
                # 计算绘制位置
                draw_x = self.x - camera_x
                draw_y = self.y - camera_y
                
                # 调整图片大小为30*30像素
                scaled_image = pygame.transform.scale(图片, (self.width, self.height))
                
                # 旋转图片，使投掷物面向移动方向
                # 图片默认朝向右，所以需要将角度转换为合适的旋转角度
                rotated_image = pygame.transform.rotate(scaled_image, -math.degrees(self.angle))
                
                # 计算旋转后的矩形，确保中心位置正确
                rotated_rect = rotated_image.get_rect(center=(draw_x + self.width//2, draw_y + self.height//2))
                surface.blit(rotated_image, rotated_rect)
        except Exception as e:
            # 如果图片加载失败，绘制一个蓝色矩形作为占位符
            draw_x = self.x - camera_x
            draw_y = self.y - camera_y
            pygame.draw.rect(surface, (0, 0, 255), (draw_x, draw_y, self.width, self.height))
    
    def should_remove(self):
        """判断是否需要移除"""
        return self.lifetime <= 0

# 普通法杖Q技能
def 普通法杖_q技能(player, weapon_skill_manager):
    """普通法杖Q技能：发射子弹粉投掷物，跟随鼠标位置飞行，击中目标造成伤害"""
    print("普通法杖技能被触发了！")
    
    # 获取游戏实例
    game = player.game
    if game:
        # 1. 获取当前手持工具，消耗耐久
        工具实例, 当前工具 = game.获取当前手持工具()
        if 工具实例 and 当前工具:
            # 消耗1点耐久
            if 工具实例.take_damage(1):
                # 物品损坏，从快捷栏中移除
                当前选中格子 = game.当前选中格子
                if 0 <= 当前选中格子 < len(game.背包管理器.快捷栏物品):
                    game.背包管理器.快捷栏物品[当前选中格子] = None
        
        # 2. 获取鼠标位置和相机位置
        mouse_pos = pygame.mouse.get_pos()  # 获取屏幕坐标中的鼠标位置
        camera_x = game.相机_x  # 获取相机的x坐标
        camera_y = game.相机_y  # 获取相机的y坐标
        
        # 3. 在玩家位置生成普通法杖投掷物
        player_x = player.坐标_x
        player_y = player.坐标_y
        
        # 创建普通法杖投掷物实例，传递鼠标位置和相机位置
        projectile = 普通法杖投掷物(player_x, player_y, 40, player, mouse_pos, camera_x, camera_y, lifetime=10.0)
        
        # 添加到武器技能管理器的召唤实体列表
        weapon_skill_manager.summoned_entities.append(projectile)

# 注册普通法杖技能 - 普通魔法杖使用普通法杖Q技能
武器技能管理器实例.register_skill("普通魔法杖", "q", 普通法杖_q技能, 0.4)  # 0.4秒冷却时间

# 注册星星法杖技能 - 其他法杖使用星星法杖Q技能
for 法杖名称 in ['星光法杖']:
    武器技能管理器实例.register_skill(法杖名称, 'q', 星星法杖_q技能, 2.5)  # 2.5秒冷却时间

# 注册骨毒法杖技能
武器技能管理器实例.register_skill("骨毒法杖", 'q', 骨毒法杖_q技能, 0.2)  # 0.2秒冷却时间

# 处理玩家攻击事件
def handle_player_attack(attacked_entity, weapon_skill_manager):
    """处理玩家攻击事件，通知所有召唤的死神祝福攻击被攻击的实体"""
    for entity in weapon_skill_manager.summoned_entities:
        if isinstance(entity, 死神祝福实体):
            entity.set_target(attacked_entity)
        elif isinstance(entity, 星星投掷物):
            # 通知星星投掷物攻击被攻击的实体
            entity.target = attacked_entity