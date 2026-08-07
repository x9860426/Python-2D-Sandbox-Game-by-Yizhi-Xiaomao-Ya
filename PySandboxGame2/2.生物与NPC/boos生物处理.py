import pygame
import random
import math

# BOSS技能字典，按BOSS类型分开管理
BOSS_SKILLS = {
    "贝利亚": {
        "基础属性": {
            "生命值": 10000,
            "攻击力": 40,
            "攻击范围": 150,
            "视野范围": 30,
            "飞行速度": 5.0,
            "行走速度": 3.0,
            "技能使用概率": 0.8
        },
        "技能": {
            "近战攻击": {
                "冷却时间": 60,
                "伤害": 40,
                "描述": "近距离直接攻击"
            },
            "冲刺": {
                "冷却时间": 120,
                "伤害": 40,
                "冲刺速度": 15.0,
                "持续时间": 30,
                "描述": "向玩家方向高速冲刺"
            },
            "扇形弹幕": {
                "冷却时间": 180,
                "伤害": 20,
                "数量": 8,
                "速度": 8.0,
                "存在时间": 120,
                "描述": "发射8个扇形分布的弹幕"
            },
            "追踪导弹": {
                "冷却时间": 240,
                "伤害": 30,
                "数量": 5,
                "速度": 5.0,
                "存在时间": 180,
                "描述": "发射5个自动追踪玩家的导弹"
            },
            "地面冲击波": {
                "冷却时间": 300,
                "伤害": 40,
                "数量": 3,
                "爆炸半径": 80,
                "存在时间": 60,
                "描述": "在玩家周围生成3个地面冲击波"
            },
            "召唤小怪": {
                "冷却时间": 360,
                "描述": "召唤小型怪物协助战斗"
            },
            "能量护盾": {
                "冷却时间": 420,
                "描述": "激活能量护盾，增强自身防御"
            },
            "激光束": {
                "冷却时间": 480,
                "伤害": 50,
                "数量": 3,
                "长度": 300,
                "存在时间": 90,
                "描述": "发射3道激光束，覆盖不同角度"
            },
            "全屏爆炸": {
                "冷却时间": 540,
                "伤害": 60,
                "数量": 10,
                "爆炸半径": 100,
                "存在时间": 120,
                "描述": "在大范围区域内生成10个爆炸点"
            }
        }
    },
    "吸血鬼": {
        "基础属性": {
            "生命值": 8000,
            "攻击力": 35,
            "攻击范围": 120,
            "视野范围": 25,
            "飞行速度": 6.0,
            "行走速度": 2.5,
            "技能使用概率": 0.75
        },
        "技能": {
            "近战攻击": {
                "冷却时间": 50,
                "伤害": 35,
                "描述": "近距离直接攻击"
            },
            "血爪斩击": {
                "冷却时间": 100,
                "伤害": 45,
                "描述": "挥舞血爪造成范围伤害"
            },
            "吸血蝙蝠": {
                "冷却时间": 180,
                "伤害": 25,
                "数量": 4,
                "描述": "召唤吸血蝙蝠攻击玩家"
            },
            "治愈蝙蝠": {
                "冷却时间": 240,
                "恢复量": 100,
                "数量": 2,
                "描述": "召唤治愈蝙蝠恢复自身生命值"
            },
            "血雾": {
                "冷却时间": 300,
                "伤害": 30,
                "持续时间": 150,
                "描述": "释放血雾，造成持续伤害"
            },
            "刺球召唤": {
                "冷却时间": 360,
                "数量": 3,
                "描述": "召唤刺球攻击玩家"
            },
            "异变骷髅": {
                "冷却时间": 420,
                "数量": 2,
                "描述": "召唤异变骷髅协助战斗"
            }
        }
    }
}

class BossManager:
    def __init__(self):
        self.bosses = []
        self.current_boss = None
    
    def add_boss(self, boss):
        """添加BOSS实例到管理器"""
        self.bosses.append(boss)
        self.current_boss = boss
    
    def create_boss(self, boss_type, x, y):
        """根据boss类型创建boss实例"""
        if boss_type == "贝利亚":
            boss = BelialBoss(x, y)
        elif boss_type == "吸血鬼":
            boss = VampireBoss(x, y)
        else:
            raise ValueError(f"未知的BOSS类型: {boss_type}")
        
        self.add_boss(boss)
        return boss
    
    def update(self, world, player):
        for boss in self.bosses:
            if boss.is_alive():
                boss.update(world, player)
    
    def draw(self, screen, camera_x, camera_y):
        # 只绘制当前被攻击的BOSS
        if self.current_boss and self.current_boss.is_alive():
            self.current_boss.draw(screen, camera_x, camera_y)
    
    def get_current_boss(self):
        return self.current_boss
    
    def clear_bosses(self):
        """清理所有BOSS实例"""
        self.bosses = []
        self.current_boss = None

class BelialBoss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 120
        self.height = 125
        
        # 使用BOSS_SKILLS字典中的配置
        self.boss_type = "贝利亚"
        self.boss_config = BOSS_SKILLS[self.boss_type]
        
        # 基础属性
        self.health = self.boss_config["基础属性"]["生命值"]
        self.max_health = self.boss_config["基础属性"]["生命值"]
        self.damage = self.boss_config["基础属性"]["攻击力"]
        self.speed = self.boss_config["基础属性"]["行走速度"]
        self.fly_speed = self.boss_config["基础属性"]["飞行速度"]
        self.attack_range = self.boss_config["基础属性"]["攻击范围"]
        self.sight_range = self.boss_config["基础属性"]["视野范围"]
        self.can_fly = True
        self.is_flying = False
        self.phase = 1
        self.direction = 1
        self.last_skill = "未使用技能"
        
        # 技能相关 - 使用技能字典映射
        self.skill_map = {
            "melee": "近战攻击",
            "dash": "冲刺",
            "skill1": "扇形弹幕",
            "skill2": "追踪导弹",
            "skill3": "地面冲击波",
            "skill4": "召唤小怪",
            "skill5": "能量护盾",
            "skill6": "激光束",
            "skill7": "全屏爆炸"
        }
        
        # 初始化技能冷却
        self.skill_cooldowns = {
            "melee": 0,
            "dash": 0,
            "skill1": 0,
            "skill2": 0,
            "skill3": 0,
            "skill4": 0,
            "skill5": 0,
            "skill6": 0,
            "skill7": 0
        }
        
        # 从配置中获取冷却时间
        self.skill_cooldown_max = {
            "melee": self.boss_config["技能"]["近战攻击"]["冷却时间"],
            "dash": self.boss_config["技能"]["冲刺"]["冷却时间"],
            "skill1": self.boss_config["技能"]["扇形弹幕"]["冷却时间"],
            "skill2": self.boss_config["技能"]["追踪导弹"]["冷却时间"],
            "skill3": self.boss_config["技能"]["地面冲击波"]["冷却时间"],
            "skill4": self.boss_config["技能"]["召唤小怪"]["冷却时间"],
            "skill5": self.boss_config["技能"]["能量护盾"]["冷却时间"],
            "skill6": self.boss_config["技能"]["激光束"]["冷却时间"],
            "skill7": self.boss_config["技能"]["全屏爆炸"]["冷却时间"]
        }
        
        # 冲刺相关
        self.dashing = False
        self.dash_timer = 0
        self.dash_duration = 30
        self.dash_speed = 15.0
        self.dash_direction_x = 0
        self.dash_direction_y = 0
        
        # 技能效果
        self.projectiles = []
        self.explosions = []
        
        # 动画相关
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10
        
        # 技能图片相关
        self.default_image = "贝利亚"
        self.current_image = self.default_image
        self.skill_image_duration = 60  # 1秒，假设60FPS
        self.skill_image_timer = 0
        print(f"贝利亚初始化 - 默认图片: {self.default_image}")
        
        # 尝试从图片加载器获取图片
        try:
            from 图片加载 import 图片管理器
            print(f"贝利亚初始化 - 检查默认图片是否已加载: {self.default_image} - {图片管理器.图片是否已加载(self.default_image)}")
            # 检查所有技能图片
            skill_images = ["贝利亚_近战攻击", "贝利亚_冲刺", "贝利亚_远程技能", "贝利亚_激光"]
            for img in skill_images:
                print(f"贝利亚初始化 - 检查技能图片是否已加载: {img} - {图片管理器.图片是否已加载(img)}")
        except Exception as e:
            print(f"贝利亚初始化 - 检查图片失败: {e}")
    
    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return True
        return False
    
    def update(self, world, player):
        # 更新技能冷却
        for skill in self.skill_cooldowns:
            if self.skill_cooldowns[skill] > 0:
                self.skill_cooldowns[skill] -= 1
        
        # 更新冲刺状态
        if self.dashing:
            self.update_dash()
        
        # 更新投掷物
        self.update_projectiles()
        
        # 更新爆炸效果
        self.update_explosions()
        
        # 更新动画
        self.update_animation()
        
        # 更新技能图片计时器
        if self.skill_image_timer > 0:
            self.skill_image_timer -= 1
            if self.skill_image_timer % 10 == 0:  # 每10帧打印一次
                print(f"贝利亚更新 - 当前图片: {self.current_image}, 计时器: {self.skill_image_timer}")
        elif self.current_image != self.default_image:
            # 技能图片持续时间结束，恢复到默认图片
            self.current_image = self.default_image
            print(f"贝利亚更新 - 恢复到默认图片: {self.current_image}")
        
        # 决定行动：行走、飞行或使用技能
        self.decide_action(player)
    
    def decide_action(self, player):
        dx = player.坐标_x - self.x
        dy = player.坐标_y - self.y
        dist = math.hypot(dx, dy)
        
        # 随机选择行动
        action = random.randint(1, 100)
        
        # 80%几率使用技能，20%几率移动
        if action <= 80 and not self.dashing:
            self.use_skill(player, dist, dx, dy)
        else:
            self.move(player, dist, dx, dy)
    
    def move(self, player, dist, dx, dy):
        # 决定是行走还是飞行
        if random.randint(1, 2) == 1:
            self.is_flying = True
        else:
            self.is_flying = False
        
        if self.is_flying:
            # 飞行移动
            if dist > 200:
                # 向玩家靠近
                dir_x = dx / dist
                dir_y = dy / dist
                self.x += dir_x * self.fly_speed
                self.y += dir_y * self.fly_speed
            else:
                # 围绕玩家飞行
                angle = math.atan2(dy, dx)
                self.x += math.cos(angle + math.pi/2) * self.fly_speed
                self.y += math.sin(angle + math.pi/2) * self.fly_speed
        else:
            # 地面行走
            if dist > 150:
                # 向玩家靠近
                dir_x = dx / dist
                self.x += dir_x * self.speed
                self.direction = 1 if dir_x > 0 else -1
            else:
                # 左右移动
                self.x += self.direction * self.speed
                if random.randint(1, 60) == 1:
                    self.direction *= -1
    
    def use_skill(self, player, dist, dx, dy):
        # 根据距离和冷却时间选择技能
        available_skills = []
        
        # 近战攻击
        if dist < 100 and self.skill_cooldowns["melee"] == 0:
            available_skills.append("melee")
        
        # 冲刺
        if self.skill_cooldowns["dash"] == 0:
            available_skills.append("dash")
        
        # 技能1-7
        for i in range(1, 8):
            if self.skill_cooldowns[f"skill{i}"] == 0:
                available_skills.append(f"skill{i}")
        
        if available_skills:
            skill = random.choice(available_skills)
            
            if skill == "melee":
                self.melee_attack(player)
            elif skill == "dash":
                self.dash(player, dx, dy, dist)
            elif skill == "skill1":
                self.skill1(player, dx, dy)
            elif skill == "skill2":
                self.skill2(player, dx, dy)
            elif skill == "skill3":
                self.skill3(player)
            elif skill == "skill4":
                self.skill4(player)
            elif skill == "skill5":
                self.skill5(player)
            elif skill == "skill6":
                self.skill6(player, dx, dy)
            elif skill == "skill7":
                self.skill7(player)
    
    def melee_attack(self, player):
        # 近战攻击
        print("贝利亚使用了近战攻击")
        self.last_skill = "近战攻击"
        self.skill_cooldowns["melee"] = self.skill_cooldown_max["melee"]
        # 切换到近战攻击图片
        self.current_image = "贝利亚_近战攻击"
        self.skill_image_timer = self.skill_image_duration
        print(f"贝利亚使用近战攻击 - 切换到图片: {self.current_image}")
        # 这里可以添加近战攻击的伤害判定和效果
    
    def dash(self, player, dx, dy, dist):
        # 冲刺攻击
        self.dashing = True
        self.dash_timer = self.dash_duration
        
        # 向玩家方向冲刺
        if dist > 0:
            self.dash_direction_x = dx / dist
            self.dash_direction_y = dy / dist
        else:
            self.dash_direction_x = 1
            self.dash_direction_y = 0
        
        print("贝利亚使用了冲刺")
        self.last_skill = "冲刺"
        self.skill_cooldowns["dash"] = self.skill_cooldown_max["dash"]
        # 切换到冲刺图片
        self.current_image = "贝利亚_冲刺"
        self.skill_image_timer = self.skill_image_duration
        print(f"贝利亚使用冲刺 - 切换到图片: {self.current_image}")
    
    def update_dash(self):
        # 更新冲刺状态
        self.x += self.dash_direction_x * self.dash_speed
        self.y += self.dash_direction_y * self.dash_speed
        
        self.dash_timer -= 1
        if self.dash_timer <= 0:
            self.dashing = False
    
    def skill1(self, player, dx, dy):
        # 技能1：扇形弹幕
        print("贝利亚使用了技能1：扇形弹幕")
        self.last_skill = "扇形弹幕"
        self.skill_cooldowns["skill1"] = self.skill_cooldown_max["skill1"]
        # 切换到远程攻击图片
        self.current_image = "贝利亚_远程技能"
        self.skill_image_timer = self.skill_image_duration
        print(f"贝利亚使用扇形弹幕 - 切换到图片: {self.current_image}")
        
        # 发射扇形弹幕
        for i in range(8):
            angle = math.atan2(dy, dx) - math.pi/2 + (i * math.pi/4)
            speed = 8.0
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            self.projectiles.append({
                'x': self.x,
                'y': self.y,
                'vx': vx,
                'vy': vy,
                'timer': 120,
                'damage': 20,
                'type': 'skill1'
            })
    
    def skill2(self, player, dx, dy):
        # 技能2：追踪导弹
        print("贝利亚使用了技能2：追踪导弹")
        self.last_skill = "追踪导弹"
        self.skill_cooldowns["skill2"] = self.skill_cooldown_max["skill2"]
        # 切换到远程攻击图片
        self.current_image = "贝利亚_远程技能"
        self.skill_image_timer = self.skill_image_duration
        print(f"贝利亚使用追踪导弹 - 切换到图片: {self.current_image}")
        
        # 发射追踪导弹
        for i in range(5):
            self.projectiles.append({
                'x': self.x,
                'y': self.y,
                'vx': 0,
                'vy': 0,
                'target': player,
                'timer': 180,
                'damage': 30,
                'speed': 5.0,
                'type': 'skill2'
            })
    
    def skill3(self, player):
        # 技能3：地面冲击波
        print("贝利亚使用了技能3：地面冲击波")
        self.last_skill = "地面冲击波"
        self.skill_cooldowns["skill3"] = self.skill_cooldown_max["skill3"]
        
        # 生成地面冲击波
        for i in range(3):
            self.explosions.append({
                'x': player.坐标_x + random.randint(-100, 100),
                'y': player.坐标_y + 50,
                'timer': 60,
                'radius': 0,
                'max_radius': 80,
                'damage': 40,
                'type': 'skill3'
            })
    
    def skill4(self, player):
        # 技能4：召唤小怪
        print("贝利亚使用了技能4：召唤小怪")
        self.last_skill = "召唤小怪"
        self.skill_cooldowns["skill4"] = self.skill_cooldown_max["skill4"]
        # 这里可以添加召唤小怪的逻辑
    
    def skill5(self, player):
        # 技能5：能量护盾
        print("贝利亚使用了技能5：能量护盾")
        self.last_skill = "能量护盾"
        self.skill_cooldowns["skill5"] = self.skill_cooldown_max["skill5"]
        # 这里可以添加能量护盾的逻辑
    
    def skill6(self, player, dx, dy):
        # 技能6：激光束
        print("贝利亚使用了技能6：激光束")
        self.last_skill = "激光束"
        self.skill_cooldowns["skill6"] = self.skill_cooldown_max["skill6"]
        # 切换到激光图片
        self.current_image = "贝利亚_激光"
        self.skill_image_timer = self.skill_image_duration
        print(f"贝利亚使用激光束 - 切换到图片: {self.current_image}")
        
        # 发射激光束
        angle = math.atan2(dy, dx)
        for i in range(3):
            self.projectiles.append({
                'x': self.x,
                'y': self.y,
                'angle': angle + (i - 1) * math.pi/18,
                'length': 0,
                'max_length': 300,
                'timer': 90,
                'damage': 50,
                'type': 'skill6'
            })
    
    def skill7(self, player):
        # 技能7：全屏爆炸
        print("贝利亚使用了技能7：全屏爆炸")
        self.last_skill = "全屏爆炸"
        self.skill_cooldowns["skill7"] = self.skill_cooldown_max["skill7"]
        
        # 生成全屏爆炸效果
        for i in range(10):
            self.explosions.append({
                'x': random.randint(int(self.x) - 200, int(self.x) + 200),
                'y': random.randint(int(self.y) - 200, int(self.y) + 200),
                'timer': 120,
                'radius': 0,
                'max_radius': 100,
                'damage': 60,
                'type': 'skill7'
            })
    
    def update_projectiles(self):
        # 更新投掷物
        for proj in self.projectiles[:]:
            proj['timer'] -= 1
            
            if proj['type'] == 'skill1':
                # 普通弹幕
                proj['x'] += proj['vx']
                proj['y'] += proj['vy']
            elif proj['type'] == 'skill2':
                # 追踪导弹
                if proj['target']:
                    dx = proj['target'].坐标_x - proj['x']
                    dy = proj['target'].坐标_y - proj['y']
                    dist = math.hypot(dx, dy)
                    if dist > 0:
                        dir_x = dx / dist
                        dir_y = dy / dist
                        proj['vx'] += dir_x * 0.2
                        proj['vy'] += dir_y * 0.2
                        # 限制速度
                        speed = math.hypot(proj['vx'], proj['vy'])
                        if speed > proj['speed']:
                            proj['vx'] = (proj['vx'] / speed) * proj['speed']
                            proj['vy'] = (proj['vy'] / speed) * proj['speed']
                    proj['x'] += proj['vx']
                    proj['y'] += proj['vy']
            elif proj['type'] == 'skill6':
                # 激光束
                proj['length'] = min(proj['length'] + 10, proj['max_length'])
            
            if proj['timer'] <= 0:
                self.projectiles.remove(proj)
    
    def update_explosions(self):
        # 更新爆炸效果
        for explosion in self.explosions[:]:
            explosion['timer'] -= 1
            if explosion['radius'] < explosion['max_radius']:
                explosion['radius'] += 2
            
            if explosion['timer'] <= 0:
                self.explosions.remove(explosion)
    
    def update_animation(self):
        # 更新动画
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
    
    def draw(self, screen, camera_x, camera_y):
        # 绘制贝利亚
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        print(f"贝利亚绘制 - 当前图片: {self.current_image}")
        
        # 尝试从图片加载器获取当前图片
        try:
            from 图片加载 import 图片管理器
            print(f"贝利亚绘制 - 尝试从图片管理器获取图片: {self.current_image}")
            if 图片管理器.图片是否已加载(self.current_image):
                boss_image = 图片管理器.get图片(self.current_image)
                print(f"贝利亚绘制 - 获取到图片: {self.current_image} - {boss_image}")
                if boss_image:
                    # 绘制贝利亚图片
                    screen.blit(boss_image, (screen_x - self.width//2, screen_y - self.height//2))
                    print(f"贝利亚绘制 - 成功绘制图片: {self.current_image}")
                    return
            else:
                print(f"贝利亚绘制 - 图片未加载: {self.current_image}")
        except Exception as e:
            print(f"贝利亚绘制失败: {e}")
        
        # 如果获取图片失败，使用默认的矩形绘制
        color = (150, 50, 100)
        if self.is_flying:
            color = (200, 100, 150)
        if self.dashing:
            color = (255, 255, 0)
        
        pygame.draw.rect(screen, color, (screen_x - self.width//2, screen_y - self.height//2, self.width, self.height))
        print(f"贝利亚绘制 - 使用默认矩形绘制")
        
        # 绘制投掷物
        for proj in self.projectiles:
            proj_screen_x = proj['x'] - camera_x
            proj_screen_y = proj['y'] - camera_y
            
            if proj['type'] == 'skill1':
                pygame.draw.circle(screen, (255, 100, 100), (int(proj_screen_x), int(proj_screen_y)), 8)
            elif proj['type'] == 'skill2':
                pygame.draw.circle(screen, (100, 100, 255), (int(proj_screen_x), int(proj_screen_y)), 10)
            elif proj['type'] == 'skill6':
                # 绘制激光束
                end_x = proj_screen_x + math.cos(proj['angle']) * proj['length']
                end_y = proj_screen_y + math.sin(proj['angle']) * proj['length']
                pygame.draw.line(screen, (255, 0, 0), (int(proj_screen_x), int(proj_screen_y)), (int(end_x), int(end_y)), 5)
        
        # 绘制爆炸效果
        for explosion in self.explosions:
            explosion_screen_x = explosion['x'] - camera_x
            explosion_screen_y = explosion['y'] - camera_y
            pygame.draw.circle(screen, (255, 100, 100), (int(explosion_screen_x), int(explosion_screen_y)), explosion['radius'], 3)
        
        # 绘制生命值条
        self.draw_health_bar(screen, camera_x, camera_y)
    
    def draw_health_bar(self, screen, camera_x, camera_y):
        # 绘制贝利亚的生命值条
        screen_x = self.x - camera_x - 250
        screen_y = self.y - camera_y - 60
        
        # 血量条宽度和高度
        bar_width = 500
        bar_height = 30
        
        # 计算血量百分比
        health_ratio = self.health / self.max_health
        
        # 玩家要求：使用红色
        health_color = pygame.Color(255, 0, 0)
        glow_color = pygame.Color(255, 0, 0)
        
        # 添加红色发光效果
        for i in range(5, 0, -1):
            alpha = 30 - i * 5
            glow_surface = pygame.Surface((bar_width + i*2, bar_height + i*2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*glow_color, alpha), 
                           (i, i, bar_width, bar_height), 
                           border_radius=15)
            screen.blit(glow_surface, (screen_x - i, screen_y - i))
        
        # 背景
        pygame.draw.rect(screen, (50, 50, 50), 
                       (screen_x, screen_y, bar_width, bar_height), 
                       border_radius=15)
        
        # 生命值
        health_rect = pygame.Rect(screen_x + 3, screen_y + 3, 
                                bar_width * health_ratio - 6, bar_height - 6)
        pygame.draw.rect(screen, health_color, 
                       health_rect, 
                       border_radius=12)
        
        # 高光效果
        highlight_surface = pygame.Surface((bar_width * health_ratio - 6, bar_height - 6), pygame.SRCALPHA)
        pygame.draw.rect(highlight_surface, (255, 255, 255, 40), 
                       (0, 0, bar_width * health_ratio - 6, (bar_height - 6) // 2), 
                       border_radius=12)
        screen.blit(highlight_surface, (screen_x + 3, screen_y + 3))
        
        # 边框
        pygame.draw.rect(screen, (255, 255, 255), 
                       (screen_x, screen_y, bar_width, bar_height), 
                       3, border_radius=15)
        pygame.draw.rect(screen, (100, 100, 100), 
                       (screen_x + 1, screen_y + 1, bar_width - 2, bar_height - 2), 
                       1, border_radius=14)
        
        # 添加文字
        # 获取BOSS名称
        boss_name = "贝利亚"
        # 检查是否是吸血鬼BOSS（通过检查位置和尺寸）
        if hasattr(self, 'name') and self.name == "吸血鬼":
            boss_name = "吸血鬼"
        
        try:
            # 使用系统中文字体
            font = pygame.font.SysFont(["SimHei", "Microsoft YaHei", "黑体", "微软雅黑"], 20, bold=True)
            health_text = f"{boss_name} - {int(health_ratio * 100)}%"
            text_surface = font.render(health_text, True, (255, 255, 255))
            text_x = screen_x + (bar_width - text_surface.get_width()) // 2
            text_y = screen_y + (bar_height - text_surface.get_height()) // 2
            screen.blit(text_surface, (text_x, text_y))
        except Exception as e:
            # 降级方案
            font = pygame.font.Font(None, 20)
            health_text = f"{boss_name} - {int(health_ratio * 100)}%"
            text_surface = font.render(health_text, True, (255, 255, 255))
            text_x = screen_x + (bar_width - text_surface.get_width()) // 2
            text_y = screen_y + (bar_height - text_surface.get_height()) // 2
            screen.blit(text_surface, (text_x, text_y))

# 全局boss管理器实例
boss_manager = BossManager()