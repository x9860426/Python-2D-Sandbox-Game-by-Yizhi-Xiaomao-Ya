import pygame
import random
import math
import sys
import time
import json
import os
from datetime import datetime
import pygame
from save_helper import SaveHelper
from 新箱子页面功能 import NewChestPageManager

class DamageText:
    """伤害显示文本类，用于在游戏中显示伤害数值""" 
    def __init__(self, x, y, damage, is_critical=False):
        self.x = x
        self.y = y
        self.damage = damage
        self.is_critical = is_critical  # 是否为暴击伤害
        self.lifetime = 1.0  # 文本显示时间（秒）
        self.velocity_y = -100  # 文本向上移动速度
        self.color = (255, 140, 0) if is_critical else (255, 255, 255)  # 暴击为橙色，普通为白色
        self.alpha = 255  # 初始透明度设为不透明
        
    def update(self, dt):
        """更新伤害文本位置和生命周期"""
        # 向上移动
        self.y += self.velocity_y * dt
        # 减少生命周期
        self.lifetime -= dt
        # 随着时间推移略微增加透明度
        self.alpha = int(255 * min(self.lifetime / 0.5, 1.0))
        
    def is_finished(self):
        """检查伤害文本是否已结束显示"""
        return self.lifetime <= 0
        
    def draw(self, screen, camera_x, camera_y):
        """在屏幕上绘制伤害文本"""
        # 创建文本表面
        font = pygame.font.SysFont(None, 24)
        
        # 处理伤害文本格式
        if self.damage < 0:
            # 环境伤害（岩浆、摔伤等）格式：-（伤害）
            text = f"-{abs(int(self.damage))}"
            # 设置环境伤害的颜色为红色
            color = (255, 0, 0)
        else:
            # 普通伤害格式
            text = f"{int(self.damage)}"
            color = (255, 140, 0) if self.is_critical else (255, 255, 255)
        
        # 创建文本表面并应用颜色
        text_surface = font.render(text, True, color)
        
        # 应用透明度
        text_surface.set_alpha(self.alpha)
        
        # 计算屏幕位置（考虑相机偏移）
        screen_x = self.x - camera_x - text_surface.get_width() // 2
        screen_y = self.y - camera_y - text_surface.get_height() // 2
        
        # 绘制到屏幕
        screen.blit(text_surface, (screen_x, screen_y))

class Arrow:
    """箭矢类，处理箭矢的物理运动和碰撞检测"""
    def __init__(self, x, y, direction_x, direction_y, damage=10, owner=None, weapon_type='arrow'):
        self.x = x
        self.y = y
        self.width = 12
        self.height = 6
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.damage = damage
        self.owner = owner  # 箭矢所有者，通常是玩家
        self.lifetime = 5.0  # 箭矢存在时间（秒）
        self.explosion_radius = 3  # 爆炸半径（以方块为单位，6*6范围的一半）
        self.explosion_damage = 400  # 爆炸伤害
        
        # 计算速度向量，总速度为500像素/秒
        speed = 500
        magnitude = math.sqrt(direction_x*direction_x + direction_y*direction_y)
        if magnitude > 0:
            self.velocity_x = (direction_x / magnitude) * speed
            self.velocity_y = (direction_y / magnitude) * speed
        else:
            self.velocity_x = speed
            self.velocity_y = 0
        
        # 计算旋转角度
        self.angle = math.degrees(math.atan2(direction_y, direction_x))
        self.stuck = False
        self.stuck_position = None
        self.stuck_time = 0
        self.weapon_type = weapon_type  # 添加武器类型标识
        
    def update(self, dt, world, creatures, game):
        """更新箭矢位置和状态"""
        # 减少生命周期
        self.lifetime -= dt
        
        if self.stuck:
            # 如果箭矢已插入，只更新插入时间
            self.stuck_time += dt
            return
        
        # 更新位置
        new_x = self.x + self.velocity_x * dt
        new_y = self.y + self.velocity_y * dt
        
        # 简单的重力效果
        self.velocity_y += 100 * dt
        
        # 检查与世界的碰撞
        hit_block = False
        for i in range(2):  # 分别检查X和Y方向的碰撞
            tile_x = int((new_x + self.width // 2) // TILE_SIZE)
            tile_y = int((new_y + self.height // 2) // TILE_SIZE)
            
            if 0 <= tile_y < WORLD_HEIGHT and 0 <= tile_x < WORLD_WIDTH:
                block_id = world.get_block(tile_x, tile_y)
                if block_id != AIR:
                    # 只有固体方块才会让箭矢卡住
                    block_info = BLOCKS.get(block_id, {})
                    if block_info.get('solid', False):
                        # 箭矢击中方块
                        # 根据武器类型决定是卡住还是反弹
                        # 弩发射的箭矢会反弹
                        if hasattr(self, 'weapon_type') and self.weapon_type == 'crossbow':
                            # 反弹：反转速度向量的相应分量
                            if i == 0:  # X方向碰撞，反转X速度
                                self.velocity_x = -self.velocity_x * 0.8  # 保留80%的速度
                            else:  # Y方向碰撞，反转Y速度
                                self.velocity_y = -self.velocity_y * 0.8  # 保留80%的速度
                            # 减少反弹次数，防止无限反弹
                            self.bounce_count = getattr(self, 'bounce_count', 0) + 1
                            if self.bounce_count >= 3:  # 最多反弹3次
                                self.stuck = True
                                self.stuck_position = (self.x, self.y)
                        elif hasattr(self, 'weapon_type') and self.weapon_type == 'rocket':
                            # 火箭弹击中方块，触发爆炸
                            self.explode(world, creatures, game)
                            self.lifetime = 0  # 火箭弹消失
                        else:
                            # 其他武器发射的箭矢卡住
                            self.stuck = True
                            self.stuck_position = (self.x, self.y)
                        hit_block = True
                    break
            
            # 检查是否超出世界边界
            if new_x < 0 or new_x + self.width > WORLD_WIDTH * TILE_SIZE or \
               new_y < 0 or new_y + self.height > WORLD_HEIGHT * TILE_SIZE:
                self.stuck = True
                self.stuck_position = (self.x, self.y)
                hit_block = True
                break
        
        if not hit_block:
            # 检查与生物的碰撞
            for creature in creatures:
                # 不击中自己
                if self.owner == creature:
                    continue
                
                creature_rect = pygame.Rect(creature.x, creature.y, creature.width, creature.height)
                
                # 创建箭矢的碰撞箱
                arrow_rect = pygame.Rect(new_x, new_y, self.width, self.height)
                
                if arrow_rect.colliderect(creature_rect):
                    # 箭矢击中生物
                    # take_damage方法返回True表示生物死亡
                    if hasattr(self, 'weapon_type') and self.weapon_type == 'rocket':
                        # 火箭弹击中生物，触发爆炸
                        self.explode(world, creatures, game)
                        self.lifetime = 0  # 火箭弹消失
                    else:
                        # 普通箭矢击中生物
                        drops = []  # 初始化掉落物列表
                        if creature.take_damage(self.damage):
                            print(f"[调试] 生物死亡: {creature.__class__.__name__}")
                            # 生物死亡，处理掉落物
                            drops = creature.get_drops()
                            print(f"[调试] 掉落物: {drops}")
                        # 创建掉落物实体
                        for drop in drops:
                            # 为每个掉落物创建一个实体
                            drop_x = creature.x + creature.width // 2 - 12 + random.randint(-20, 20)
                            drop_y = creature.y + creature.height // 2 - 12 + random.randint(-20, 20)
                            item_entity = ItemEntity(
                                drop_x,
                                drop_y,
                                drop["item_id"],
                                drop["quantity"]
                            )
                            game.item_entities.append(item_entity)
                            print(f"[调试] 创建掉落物实体: {drop['item_id']} x {drop['quantity']}")
                        
                        # 给予玩家经验值奖励
                        if creature.properties.get('boss', False):
                            exp_reward = 20  # BOSS给予20经验
                        elif creature.properties.get('hostile', False):
                            # 敌对生物给予5-15经验
                            if creature.properties.get('health', 10) > 50:
                                exp_reward = 15
                            else:
                                exp_reward = 10
                        else:
                            exp_reward = 5  # 其他生物给予5经验
                        
                        # 如果所有者是玩家，添加经验值
                        if self.owner and hasattr(self.owner, 'add_experience'):
                            self.owner.add_experience(exp_reward)
                    
                    self.lifetime = 0  # 箭矢消失
                    
                    # 创建伤害文本
                    text_x = creature.x + creature.width // 2
                    text_y = creature.y - 10
                    game.damage_texts.append(DamageText(text_x, text_y, self.damage))
                    break
        
        # 如果没有击中任何物体，更新位置
        if not self.stuck:
            self.x = new_x
            self.y = new_y
            self.rect.x = self.x
            self.rect.y = self.y
    
    def is_finished(self):
        """检查箭矢是否应被移除"""
        return self.lifetime <= 0 or (self.stuck and self.stuck_time > 2.0)
    
    def explode(self, world, creatures, game):
        """火箭弹爆炸效果"""
        # 获取爆炸中心的方块坐标
        center_tile_x = int((self.x + self.width // 2) // TILE_SIZE)
        center_tile_y = int((self.y + self.height // 2) // TILE_SIZE)
        
        # 获取爆炸中心的世界坐标
        explosion_center_x = self.x + self.width // 2
        explosion_center_y = self.y + self.height // 2
        
        # 创建爆炸特效（朝玩家方向发射的白色线条，类似箭矢）
        # 检查游戏对象是否有explosions列表，如果没有则创建
        if not hasattr(game, 'explosions'):
            game.explosions = []
        
        # 添加新的爆炸特效
        game.explosions.append({
            'center_x': explosion_center_x,
            'center_y': explosion_center_y,
            'radius': 0,
            'max_radius': self.explosion_radius * TILE_SIZE * 1.5,  # 白线范围略大于爆炸范围
            'duration': 0.3,  # 特效持续时间
            'remaining_time': 0.3  # 剩余时间
        })
        
        # 破坏爆炸范围内的方块（6*6范围）
        for dy in range(-self.explosion_radius, self.explosion_radius + 1):
            for dx in range(-self.explosion_radius, self.explosion_radius + 1):
                tile_x = center_tile_x + dx
                tile_y = center_tile_y + dy
                
                # 检查是否在世界范围内
                if 0 <= tile_y < WORLD_HEIGHT and 0 <= tile_x < WORLD_WIDTH:
                    block_id = world.get_block(tile_x, tile_y)
                    # 只破坏非空气方块
                    if block_id != AIR:
                        # 移除方块
                        world.set_block(tile_x, tile_y, AIR)
                        
                        # 创建方块掉落物（如果有）
                        block_info = BLOCKS.get(block_id, {})
                        if 'drops' in block_info:
                            for drop in block_info['drops']:
                                # 计算掉落位置（方块中心）
                                drop_x = tile_x * TILE_SIZE + TILE_SIZE // 2
                                drop_y = tile_y * TILE_SIZE + TILE_SIZE // 2
                                
                                # 创建掉落物实体
                                item_entity = ItemEntity(
                                    drop_x,
                                    drop_y,
                                    drop["item_id"],
                                    drop["quantity"]
                                )
                                game.item_entities.append(item_entity)
        
        # 对爆炸范围内的生物造成伤害
        for creature in creatures:
            # 不伤害自己
            if self.owner == creature:
                continue
            
            # 计算生物中心到爆炸中心的距离
            creature_center_x = creature.x + creature.width // 2
            creature_center_y = creature.y + creature.height // 2
            
            distance = math.sqrt((creature_center_x - explosion_center_x) ** 2 + 
                                (creature_center_y - explosion_center_y) ** 2)
            
            # 检查生物是否在爆炸范围内
            max_distance = self.explosion_radius * TILE_SIZE
            if distance <= max_distance:
                # 生物在爆炸范围内，造成伤害
                creature.take_damage(self.explosion_damage)
                
                # 创建伤害文本
                game.damage_texts.append(DamageText(creature_center_x, creature_center_y - 10, self.explosion_damage))
    
    def draw(self, screen, camera_x, camera_y, images):
        """绘制箭矢"""
        # 激光炮发射的子弹不渲染（白色光柱）
        if hasattr(self, 'weapon_type') and self.weapon_type == 'laser_cannon':
            return
            
        # 计算屏幕位置
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # 创建一个简单的箭矢/子弹图形
        arrow_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # 根据武器类型设置不同颜色或图片
        if hasattr(self, 'weapon_type') and self.weapon_type == 'rocket':
            # 使用火箭筒发射的子弹图片
            rocket_texture = "火箭弹_发射"
            if rocket_texture in images:
                # 放大图片1000%（10倍）
                scaled_image = pygame.transform.scale(images[rocket_texture], (int(self.width * 5), int(self.height * 5)))
                # 然后旋转缩放后的图片
                rotated_image = pygame.transform.rotate(scaled_image, -self.angle)
                image_rect = rotated_image.get_rect(center=(screen_x + self.width // 2, screen_y + self.height // 2))
                screen.blit(rotated_image, image_rect.topleft)
                
                # 绘制火箭弹尾部的随机像素白线效果
                import random
                # 计算火箭弹尾部中心点（移动方向的反方向）
                tail_x = screen_x + self.width // 2 - math.cos(self.angle) * (self.width * 5) // 2
                tail_y = screen_y + self.height // 2 - math.sin(self.angle) * (self.height * 5) // 2
                
                # 绘制多条随机长度和角度的白色像素线
                for _ in range(10):  # 绘制10条线
                    # 计算与火箭弹方向相反的基础方向
                    base_angle = self.angle + math.pi
                    # 添加一些随机角度偏移
                    line_angle = base_angle + random.uniform(-0.3, 0.3)
                    # 随机线长
                    line_length = random.randint(5, 20)
                    # 计算线的终点
                    end_x = tail_x + math.cos(line_angle) * line_length
                    end_y = tail_y + math.sin(line_angle) * line_length
                    # 绘制白色像素线
                    pygame.draw.line(screen, (255, 255, 255), (tail_x, tail_y), (end_x, end_y), 1)
                
                return
            else:
                # 如果图片不存在，使用红色矩形作为后备
                pygame.draw.rect(arrow_surface, (255, 0, 0), (0, 0, self.width, self.height))
        elif hasattr(self, 'owner') and self.owner and hasattr(self.owner, 'get_selected_item'):
            weapon = self.owner.get_selected_item()
            if weapon and weapon.get('item_id') == SNIPER:
                pygame.draw.rect(arrow_surface, (192, 192, 192), (0, 0, self.width, self.height))  # 灰色子弹
            else:
                pygame.draw.rect(arrow_surface, (139, 69, 19), (0, 0, self.width, self.height))  # 棕色箭矢
        else:
            pygame.draw.rect(arrow_surface, (139, 69, 19), (0, 0, self.width, self.height))  # 默认棕色箭矢
        
        # 旋转箭矢
        rotated_surface = pygame.transform.rotate(arrow_surface, -self.angle)
        rotated_rect = rotated_surface.get_rect(center=(screen_x + self.width // 2, 
                                                       screen_y + self.height // 2))
        
        screen.blit(rotated_surface, rotated_rect.topleft)


class ItemEntity:
    """物品实体类，表示地面上的掉落物"""
    def __init__(self, x, y, item_id, quantity=1):
        self.x = x
        self.y = y
        self.item_id = item_id
        self.quantity = quantity
        self.width = 24
        self.height = 24
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.lifetime = 30.0  # 掉落物存在时间（秒）
        self.velocity_y = 0
        self.gravity = 990
        self.bounce_factor = 0.4  # 弹跳系数
        self.on_ground = False
        self.animation_offset = 0  # 用于呼吸动画
        self.animation_speed = 2  # 呼吸动画速度
        self.picked_up = False  # 初始为未拾取状态
        
        # 随机初始水平速度，使物品散落在周围
        self.velocity_x = random.uniform(-30, 30)
        
    def update(self, dt, world, player):
        """更新物品实体位置和状态"""
        # 减少生命周期
        self.lifetime -= dt
        
        # 检查是否被玩家拾取
        if not self.picked_up:
            # 计算物品与玩家的距离
            dx = player.x + player.width // 2 - (self.x + self.width // 2)
            dy = player.y + player.height // 2 - (self.y + self.height // 2)
            distance = math.sqrt(dx*dx + dy*dy)
            
            # 如果玩家足够接近，尝试拾取物品
            if distance < 30:  # 拾取范围
                # 只有成功添加所有物品到背包时，才标记为已拾取
                # 这样当背包满时，玩家将无法拾取物品
                if player.add_item(self.item_id, self.quantity):
                    self.picked_up = True
        
        # 应用重力
        if not self.on_ground:
            self.velocity_y += self.gravity * dt
            self.y += self.velocity_y * dt
            
            # 检查是否落地
            tile_y = int((self.y + self.height) // TILE_SIZE)
            tile_x = int((self.x + self.width // 2) // TILE_SIZE)
            
            if 0 <= tile_y < WORLD_HEIGHT and 0 <= tile_x < WORLD_WIDTH:
                if world.get_block(tile_x, tile_y) != AIR:
                    # 落地反弹
                    self.y = tile_y * TILE_SIZE - self.height
                    self.velocity_y = -self.velocity_y * self.bounce_factor
                    if abs(self.velocity_y) < 10:
                        self.velocity_y = 0
                        self.on_ground = True
        
        # 如果在地面上，应用一点水平摩擦力
        if self.on_ground:
            self.velocity_x *= 0.9
            if abs(self.velocity_x) < 0.1:
                self.velocity_x = 0
        
        # 更新水平位置
        self.x += self.velocity_x * dt
        
        # 更新矩形位置
        self.rect.x = self.x
        self.rect.y = self.y
        
        # 更新呼吸动画
        self.animation_offset = math.sin(time.time() * self.animation_speed) * 2
    
    def is_finished(self):
        """检查物品实体是否已消失"""
        return self.lifetime <= 0
        
    def draw(self, screen, camera_x, camera_y, images):
        """在屏幕上绘制物品实体"""
        item_info = ITEMS.get(self.item_id)
        if not item_info:
            return
            
        # 计算屏幕位置
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y + self.animation_offset
        
        # 绘制物品图标
        if item_info.get("texture") in images:
            # 缩放图标到合适大小
            item_image = pygame.transform.scale(images[item_info["texture"]], (self.width, self.height))
            screen.blit(item_image, (screen_x, screen_y))
        else:
            # 没有纹理时使用颜色块
            pygame.draw.rect(screen, item_info.get("color", (150, 150, 150)), 
                            (screen_x, screen_y, self.width, self.height))
        
        # 绘制物品数量（如果数量大于1）
        if self.quantity > 1:
            font = load_font(12)
            quantity_text = font.render(str(self.quantity), True, (255, 255, 255))
            # 添加黑色背景以提高可见性
            bg_rect = quantity_text.get_rect(topleft=(screen_x + 2, screen_y + 2))
            bg_rect.inflate_ip(4, 2)
            pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect, border_radius=3)
            screen.blit(quantity_text, (screen_x + 4, screen_y + 3))
    
    def can_pickup(self, player):
        """检查玩家是否可以拾取该物品"""
        # 简单的碰撞检测
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        return player_rect.colliderect(self.rect)
        
        text_surface = font.render(text, True, color)
        # 设置透明度
        text_surface.set_alpha(self.alpha)
        # 计算屏幕位置
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        # 绘制文本
        screen.blit(text_surface, (screen_x - text_surface.get_width() // 2, 
                                  screen_y - text_surface.get_height() // 2))

# 初始化pygame
pygame.init()
pygame.mixer.init()

# 确保中文显示正常
pygame.font.init()

# 游戏设置
WIDTH, HEIGHT = 1200, 800
TILE_SIZE = 32
WORLD_WIDTH, WORLD_HEIGHT = 500, 300  # 扩大地图尺寸
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("方块生成1.0")
clock = pygame.time.Clock()

# 加载中文字体，确保中文显示正常
pygame.font.init()

# 确保中文显示正常的字体加载函数
def load_font(size=16, bold=False, italic=False):
    """
    加载支持中文的字体
    size: 字体大小
    bold: 是否粗体
    italic: 是否斜体
    """
    # Windows系统上常见的中文字体
    chinese_fonts = ["SimHei", "Microsoft YaHei", "NSimSun", "SimSun", 
                    "FangSong", "KaiTi", "WenQuanYi Micro Hei", "Heiti TC"]
    
    for font_name in chinese_fonts:
        try:
            font = pygame.font.SysFont(font_name, size, bold=bold, italic=italic)
            # 测试字体是否能正确渲染中文
            test_text = font.render("测试中文", True, (255, 255, 255))
            if test_text.get_width() > 10:  # 确保渲染结果有效
                return font
        except:
            continue
    
    # 如果所有中文字体都加载失败，使用系统默认字体
    try:
        font = pygame.font.SysFont(None, size, bold=bold, italic=italic)
        return font
    except:
        # 最后的备用方案：使用pygame默认字体
        return pygame.font.Font(None, size)

# 初始化字体
try:
    font_small = load_font(16)
    font_medium = load_font(20)
    font_large = load_font(24, bold=True)
except:
    # 最后的保障
    font_small = pygame.font.Font(None, 16)
    font_medium = pygame.font.Font(None, 20)
    font_large = pygame.font.Font(None, 24)

# 颜色定义
SKY_DAY = (135, 206, 235)
SKY_NIGHT = (25, 25, 112)
SUNSET_ORANGE = (255, 140, 0)
RAIN_GRAY = (180, 180, 180)  # 下雨时的白灰色天空颜色
GRASS_GREEN = (60, 180, 75)
DIRT_BROWN = (139, 69, 19)
STONE_GRAY = (105, 105, 105)
ORE_SILVER = (192, 192, 192)
GOLD_YELLOW = (255, 215, 0)
DIAMOND_BLUE = (30, 144, 255)
WOOD_BROWN = (150, 75, 0)
LEAF_GREEN = (34, 139, 34)
WATER_BLUE = (65, 105, 225, 180)
LAVA_RED = (220, 20, 60, 200)
CHEST_COLOR = (160, 120, 80)
TORCH_ORANGE = (255, 140, 0)
PLAYER_SKIN = (240, 184, 160)
PLAYER_SHIRT = (220, 20, 60)
PLAYER_PANTS = (30, 144, 255)
UI_BG = (40, 40, 40, 200)
UI_BORDER = (80, 80, 80)
UI_HIGHLIGHT = (100, 100, 255)

# 方块ID
AIR = 0
DIRT = 1
GRASS = 2
STONE = 3
WOOD = 4
LEAF = 5
IRON_ORE = 6
GOLD_ORE = 7
DIAMOND_ORE = 8
WATER = 9
LAVA = 10
CHEST = 11
TORCH = 12
BLACK_DIRT = 13  # 黑土块
RED_FLOWER = 14  # 红花

# 物品ID
GRASS_PLANT = 15  # 草
BEDROCK = 16  # 基岩
WOOD_PLANK = 17  # 木板
COPPER_ORE = 18  # 铜矿石
GOLD_BLOCK = 19
IRON_BLOCK = 20
DIAMOND_BLOCK = 21
COPPER_BLOCK = 22
SAND = 23  # 沙子
DRY_GRASS = 24  # 枯草
CACTUS = 25  # 仙人掌
# 雨林新增方块
JUNGLE_TREE = 26  # 乔木
JUNGLE_LEAF = 27  # 乔木叶
SHRUB = 28  # 灌木
STONE_BOTTOM = 29  # 岩石_底方块

# 工具和物品ID
WOOD_SWORD = 100
STONE_SWORD = 101
COPPER_SWORD = 102
IRON_SWORD = 103
GOLD_SWORD = 104
DIAMOND_SWORD = 105
# 远程武器
WOOD_BOW = 120  # 木弓箭
WOOD_ARROW = 121  # 木箭
CROSSBOW = 126  # 弩
LASER_CANNON = 127  # 激光炮
# 枪械武器
RIFLE = 122  # 步枪
PISTOL = 123  # 手枪
SNIPER = 124  # 狙击枪
BULLET = 125  # 子弹
# 火箭筒武器
ROCKET_LAUNCHER = 128  # 火箭筒
ROCKET = 129  # 火箭弹
ROCKET_D = 130  # 火箭弹_发射
WOOD_PICKAXE = 200
STONE_PICKAXE = 201
COPPER_PICKAXE = 202
IRON_PICKAXE = 203
GOLD_PICKAXE = 204
DIAMOND_PICKAXE = 205

WOOD_AXE = 300
STONE_AXE = 301
COPPER_AXE = 302
IRON_AXE = 303
GOLD_AXE = 304
DIAMOND_AXE = 305

WOOD_SHOVEL = 400
STONE_SHOVEL = 401
COPPER_SHOVEL = 402
IRON_SHOVEL = 403
GOLD_SHOVEL = 404
DIAMOND_SHOVEL = 405

APPLE = 500
MEAT = 501
GOLD_INGOT = 502
IRON_INGOT = 503
COPPER_INGOT = 504
DIAMOND = 505
# 雨林新增食物
JUNGLE_FRUIT = 506  # 乔木果

# 药水类型
HEALTH_POTION_1 = 600  # 一级回血瓶
HEALTH_POTION_2 = 601  # 二级回血瓶
HEALTH_POTION_3 = 602  # 三级回血瓶
HEALTH_POTION_4 = 603  # 四级回血瓶

# 装备类型
# 头盔
HELMET_1 = 700  # 1级头盔
HELMET_2 = 701  # 2级头盔
HELMET_3 = 702  # 3级头盔
HELMET_4 = 703  # 4级头盔
HELMET_5 = 704  # 5级头盔
# 盔甲
ARMOR_1 = 710  # 1级盔甲
ARMOR_2 = 711  # 2级盔甲
ARMOR_3 = 712  # 3级盔甲
ARMOR_4 = 713  # 4级盔甲
ARMOR_5 = 714  # 5级盔甲
# 靴子
BOOTS_1 = 720  # 1级靴子
BOOTS_2 = 721  # 2级靴子
BOOTS_3 = 722  # 3级靴子
BOOTS_4 = 723  # 4级靴子
BOOTS_5 = 724  # 5级靴子
# 特殊装备
SPECIAL_1 = 730  # 1级斗篷
SPECIAL_2 = 731  # 2级披风
SPECIAL_3 = 732  # 3级灵服
SPECIAL_4 = 733  # 4级披风
SPECIAL_5 = 734  # 5级腰带

# 生物类型
SLIME = 1000
MARMOT = 1001
GHOST = 1002
BAT = 1003
FIRE_SPIRIT = 1004
MUSHROOM_MONSTER = 1005
ROCK_MONSTER = 1006
# 沙漠专属生物
DESERT_WORM = 1007
SAND_WORM = 1008
BOSS_SAND_WORM = 1009
# 雨林新增生物
SCORPION = 1010  # 蝎子
MONKEY = 1011  # 猴子

# 方块属性
BLOCKS = {
    AIR: {"name": "空气", "color": None, "solid": False, "hardness": 0, "texture": None},
    DIRT: {"name": "土块", "color": DIRT_BROWN, "solid": True, "hardness": 1, "texture": "土块"},
    GRASS: {"name": "草方块", "color": GRASS_GREEN, "solid": True, "hardness": 1, "texture": "草方块"},
    STONE: {"name": "岩石", "color": STONE_GRAY, "solid": True, "hardness": 2, "texture": "岩石"},
    WOOD: {"name": "木头", "color": WOOD_BROWN, "solid": True, "hardness": 1, "texture": "木头"},
    LEAF: {"name": "树叶", "color": LEAF_GREEN, "solid": False, "hardness": 0.5, "texture": "树叶"},
    IRON_ORE: {"name": "铁矿石", "color": ORE_SILVER, "solid": True, "hardness": 3, "texture": "铁矿石"},
    GOLD_ORE: {"name": "金矿石", "color": GOLD_YELLOW, "solid": True, "hardness": 4, "texture": "金矿石"},
    DIAMOND_ORE: {"name": "钻石矿石", "color": DIAMOND_BLUE, "solid": True, "hardness": 5, "texture": "钻石矿石"},
    WATER: {"name": "水", "color": WATER_BLUE, "solid": False, "hardness": 0, "texture": "水", "liquid": True},
    LAVA: {"name": "岩浆", "color": LAVA_RED, "solid": False, "hardness": 0, "texture": "岩浆", "liquid": True},
    CHEST: {"name": "箱子", "color": CHEST_COLOR, "solid": True, "hardness": 2, "texture": "箱子"},
    TORCH: {"name": "火把", "color": TORCH_ORANGE, "solid": False, "hardness": 0, "texture": "火把"},
    BLACK_DIRT: {"name": "黑土块", "color": (60, 30, 10), "solid": True, "hardness": 1, "texture": "黑土块"},
    STONE_BOTTOM: {"name": "岩石_底", "color": (32, 32, 32), "solid": False, "hardness": 1, "texture": "岩石_底"}, # 原始岩石颜色的70%黑色 (105,105,105) * 0.3
    RED_FLOWER: {"name": "红花", "color": (255, 0, 0), "solid": False, "hardness": 0, "texture": "红花"},
    GRASS_PLANT: {"name": "草", "color": (0, 200, 0), "solid": False, "hardness": 0, "texture": "草"},
    GOLD_BLOCK: {"name": "金块", "color": GOLD_YELLOW, "solid": True, "hardness": 3, "texture": "金块"},
    IRON_BLOCK: {"name": "铁块", "color": ORE_SILVER, "solid": True, "hardness": 3, "texture": "铁块"},
    DIAMOND_BLOCK: {"name": "钻石块", "color": DIAMOND_BLUE, "solid": True, "hardness": 4, "texture": "钻石块"},
    COPPER_BLOCK: {"name": "铜块", "color": (184, 115, 51), "solid": True, "hardness": 2, "texture": "铜块"},
    BEDROCK: {"name": "基岩", "type": "block", "color": (60, 60, 60), "solid": True, "hardness": -1, "texture": "基岩"},
    WOOD_PLANK: {"name": "木板", "type": "block", "color": WOOD_BROWN, "solid": True, "hardness": 1, "texture": "木板"},
    COPPER_ORE: {"name": "铜矿石", "type": "block", "color": (184, 115, 51), "solid": True, "hardness": 3, "texture": "铜矿石"},
    SAND: {"name": "沙子", "color": (255, 215, 0), "solid": True, "hardness": 1, "texture": "沙子", "cannot_float": True},
    DRY_GRASS: {"name": "枯草", "color": (200, 180, 50), "solid": False, "hardness": 0, "texture": "枯草"},
    CACTUS: {"name": "仙人掌", "color": (0, 150, 0), "solid": True, "hardness": 1, "texture": "仙人掌", "cactus": True},
    
    # 雨林新增方块
    JUNGLE_TREE: {"name": "乔木", "color": (101, 67, 33), "solid": True, "hardness": 1.5, "texture": "乔木"},
    JUNGLE_LEAF: {"name": "乔木叶", "color": (34, 177, 76), "solid": False, "hardness": 0.5, "texture": "乔木叶"},
    SHRUB: {"name": "灌木", "color": (50, 200, 50), "solid": False, "hardness": 0, "texture": "灌木", "damage": 4},  # 灌木对玩家造成4点伤害
    JUNGLE_FRUIT: {"name": "乔木果", "color": (255, 140, 0), "solid": False, "hardness": 0, "texture": "乔木果"}
}

# 物品系统
ITEMS = {
    # 方块类
    DIRT: {"name": "土块", "type": "block", "block_id": DIRT, "color": DIRT_BROWN, "texture": "土块"},
    GRASS: {"name": "草方块", "type": "block", "block_id": GRASS, "color": GRASS_GREEN, "texture": "草方块"},
    STONE: {"name": "岩石", "type": "block", "block_id": STONE, "color": STONE_GRAY, "texture": "岩石"},
    WOOD: {"name": "木头", "type": "block", "block_id": WOOD, "color": WOOD_BROWN, "texture": "木头"},
    LEAF: {"name": "树叶", "type": "block", "block_id": LEAF, "color": LEAF_GREEN, "texture": "树叶"},
    IRON_ORE: {"name": "铁矿石", "type": "block", "block_id": IRON_ORE, "color": ORE_SILVER, "texture": "铁矿石"},
    GOLD_ORE: {"name": "金矿石", "type": "block", "block_id": GOLD_ORE, "color": GOLD_YELLOW, "texture": "金矿石"},
    DIAMOND_ORE: {"name": "钻石矿石", "type": "block", "block_id": DIAMOND_ORE, "color": DIAMOND_BLUE,
                  "texture": "钻石矿石"},
    WATER: {"name": "水", "type": "block", "block_id": WATER, "color": WATER_BLUE, "texture": "水"},
    LAVA: {"name": "岩浆", "type": "block", "block_id": LAVA, "color": LAVA_RED, "texture": "岩浆"},
    CHEST: {"name": "箱子", "type": "block", "block_id": CHEST, "color": CHEST_COLOR, "texture": "箱子"},
    RED_FLOWER: {"name": "红花", "type": "block", "block_id": RED_FLOWER, "color": (255, 0, 0), "texture": "红花"},
    GRASS_PLANT: {"name": "草", "type": "block", "block_id": GRASS_PLANT, "color": (0, 200, 0), "texture": "草"},
    TORCH: {"name": "火把", "type": "block", "block_id": TORCH, "color": TORCH_ORANGE, "texture": "火把"},
    BLACK_DIRT: {"name": "黑土块", "type": "block", "block_id": BLACK_DIRT, "color": (60, 30, 10), "texture": "黑土块"},
    GOLD_INGOT: {"name": "金块", "type": "block", "block_id": GOLD_BLOCK, "color": GOLD_YELLOW, "texture": "金块"},
    STONE_BOTTOM: {"name": "岩石_底", "type": "block", "block_id": STONE_BOTTOM, "color": STONE_GRAY, "texture": "岩石_底"},
    IRON_INGOT: {"name": "铁块", "type": "block", "block_id": IRON_BLOCK, "color": ORE_SILVER, "texture": "铁块"},
    COPPER_INGOT: {"name": "铜块", "type": "block", "block_id": COPPER_BLOCK, "color": (184, 115, 51), "texture": "铜块"},
    DIAMOND: {"name": "钻石块", "type": "block", "block_id": DIAMOND_BLOCK, "color": DIAMOND_BLUE, "texture": "钻石块"},
    # 添加方块ID的映射，与配方中的item_id对应
    GOLD_BLOCK: {"name": "金块", "type": "block", "block_id": GOLD_BLOCK, "color": GOLD_YELLOW, "texture": "金块"},
    IRON_BLOCK: {"name": "铁块", "type": "block", "block_id": IRON_BLOCK, "color": ORE_SILVER, "texture": "铁块"},
    COPPER_BLOCK: {"name": "铜块", "type": "block", "block_id": COPPER_BLOCK, "color": (184, 115, 51), "texture": "铜块"},
    DIAMOND_BLOCK: {"name": "钻石块", "type": "block", "block_id": DIAMOND_BLOCK, "color": DIAMOND_BLUE, "texture": "钻石块"},
    
    # 新添加的方块物品定义
    BEDROCK: {"name": "基岩", "type": "block", "block_id": BEDROCK, "color": (60, 60, 60), "texture": "基岩"},
    WOOD_PLANK: {"name": "木板", "type": "block", "block_id": WOOD_PLANK, "color": WOOD_BROWN, "texture": "木板"},
    COPPER_ORE: {"name": "铜矿石", "type": "block", "block_id": COPPER_ORE, "color": (184, 115, 51), "texture": "铜矿石"},
    SAND: {"name": "沙子", "type": "block", "block_id": SAND, "color": (255, 215, 0), "texture": "沙子"},
    DRY_GRASS: {"name": "枯草", "type": "block", "block_id": DRY_GRASS, "color": (200, 180, 50), "texture": "枯草"},
    CACTUS: {"name": "仙人掌", "type": "block", "block_id": CACTUS, "color": (0, 150, 0), "texture": "仙人掌"},
    
    # 工具类 - 剑
    WOOD_SWORD: {"name": "木剑", "type": "weapon", "damage": 5, "color": WOOD_BROWN, "texture": "木剑", "speed": 2.0},
    STONE_SWORD: {"name": "石剑", "type": "weapon", "damage": 7, "color": STONE_GRAY, "texture": "石剑", "speed": 2.2},
    COPPER_SWORD: {"name": "铜剑", "type": "weapon", "damage": 8, "color": (184, 115, 51), "texture": "铜剑", "speed": 2.4},
    IRON_SWORD: {"name": "铁剑", "type": "weapon", "damage": 11, "color": ORE_SILVER, "texture": "铁剑", "speed": 2.8},
    GOLD_SWORD: {"name": "金剑", "type": "weapon", "damage": 10, "color": GOLD_YELLOW, "texture": "金剑", "speed": 2.6},
    DIAMOND_SWORD: {"name": "钻石剑", "type": "weapon", "damage": 15, "color": DIAMOND_BLUE, "texture": "钻石剑",
                    "speed": 3.2},
    
    # 远程武器
    WOOD_BOW: {"name": "木弓箭", "type": "weapon", "damage": 8, "color": WOOD_BROWN, "texture": "木弓箭", "speed": 2.5},
    WOOD_ARROW: {"name": "木箭", "type": "arrow", "damage": 8, "color": WOOD_BROWN, "texture": "木箭", "stack_limit": 64},
    CROSSBOW: {"name": "未来弩", "type": "weapon", "damage": 20, "color": ORE_SILVER, "texture": "未来弩", "speed": 10.0},
    LASER_CANNON: {"name": "激光炮", "type": "weapon", "damage": 50, "color": (0, 255, 255), "texture": "激光炮", "speed": 5.0},
    
    # 枪械武器
    RIFLE: {"name": "步枪", "type": "weapon", "damage": 50, "color": ORE_SILVER, "texture": "步枪", "speed": 3.0},
    PISTOL: {"name": "手枪", "type": "weapon", "damage": 25, "color": ORE_SILVER, "texture": "手枪", "speed": 4.0},
    SNIPER: {"name": "狙击枪", "type": "weapon", "damage": 800, "color": ORE_SILVER, "texture": "狙击枪", "speed": 1.5},
    BULLET: {"name": "子弹", "type": "bullet", "damage": 0, "color": ORE_SILVER, "texture": "子弹", "stack_limit": 64},
    # 火箭筒武器
    ROCKET_LAUNCHER: {"name": "火箭筒", "type": "weapon", "damage": 100, "color": (100, 100, 100), "texture": "火箭筒", "speed": 1.0},
    ROCKET: {"name": "火箭弹", "type": "bullet", "damage": 0, "color": (255, 100, 0), "texture": "火箭弹_图片", "stack_limit": 32},
    ROCKET_D: {"name": "火箭弹_发射", "type": "bullet", "damage": 0, "color": (255, 100, 0), "texture": "火箭弹_发射", "stack_limit": 32},

    # 工具类 - 稿
    WOOD_PICKAXE: {"name": "木镐", "type": "pickaxe", "damage": 3, "color": WOOD_BROWN, "texture": "木镐",
                   "speed": 2.0},
    STONE_PICKAXE: {"name": "石镐", "type": "pickaxe", "damage": 4, "color": STONE_GRAY, "texture": "石镐",
                    "speed": 2.4},
    COPPER_PICKAXE: {"name": "铜镐", "type": "pickaxe", "damage": 5, "color": (184, 115, 51), "texture": "铜镐",
                   "speed": 2.8},
    IRON_PICKAXE: {"name": "铁镐", "type": "pickaxe", "damage": 6, "color": ORE_SILVER, "texture": "铁镐",
                   "speed": 3.4},
    GOLD_PICKAXE: {"name": "金镐", "type": "pickaxe", "damage": 5, "color": GOLD_YELLOW, "texture": "金镐",
                   "speed": 3.0},
    DIAMOND_PICKAXE: {"name": "钻石镐", "type": "pickaxe", "damage": 8, "color": DIAMOND_BLUE, "texture": "钻石镐",
                      "speed": 4.0},

    # 工具类 - 斧头
    WOOD_AXE: {"name": "木斧", "type": "axe", "damage": 4, "color": WOOD_BROWN, "texture": "木斧", "speed": 2.0},
    STONE_AXE: {"name": "石斧", "type": "axe", "damage": 6, "color": STONE_GRAY, "texture": "石斧", "speed": 2.4},
    COPPER_AXE: {"name": "铜斧", "type": "axe", "damage": 7, "color": (184, 115, 51), "texture": "铜斧", "speed": 2.8},
    IRON_AXE: {"name": "铁斧", "type": "axe", "damage": 9, "color": ORE_SILVER, "texture": "铁斧", "speed": 3.4},
    GOLD_AXE: {"name": "金斧", "type": "axe", "damage": 8, "color": GOLD_YELLOW, "texture": "金斧", "speed": 3.0},
    DIAMOND_AXE: {"name": "钻石斧头", "type": "axe", "damage": 12, "color": DIAMOND_BLUE, "texture": "钻石斧头",
                  "speed": 4.0},

    # 工具类 - 铲子
    WOOD_SHOVEL: {"name": "木铲", "type": "shovel", "damage": 2, "color": WOOD_BROWN, "texture": "木铲", "speed": 2.0},
    STONE_SHOVEL: {"name": "石铲", "type": "shovel", "damage": 3, "color": STONE_GRAY, "texture": "石铲", "speed": 2.4},
    COPPER_SHOVEL: {"name": "铜铲", "type": "shovel", "damage": 4, "color": (184, 115, 51), "texture": "铜铲", "speed": 2.8},
    IRON_SHOVEL: {"name": "铁铲", "type": "shovel", "damage": 5, "color": ORE_SILVER, "texture": "铁铲", "speed": 3.4},
    GOLD_SHOVEL: {"name": "金铲", "type": "shovel", "damage": 4, "color": GOLD_YELLOW, "texture": "金铲", "speed": 3.0},
    DIAMOND_SHOVEL: {"name": "钻石铲", "type": "shovel", "damage": 6, "color": DIAMOND_BLUE, "texture": "钻石铲",
                     "speed": 4.0},

    # 物品类
    APPLE: {"name": "苹果", "type": "food", "hunger": 20, "health": 5, "color": (255, 0, 0), "texture": "苹果"},
    MEAT: {"name": "肉块", "type": "food", "hunger": 40, "health": 10, "color": (139, 69, 19), "texture": "肉块"},
    # 雨林新增食物
    JUNGLE_FRUIT: {"name": "乔木果", "type": "food", "hunger": 25, "health": 8, "color": (255, 140, 0), "texture": "乔木果"},
    
    # 药水类
    HEALTH_POTION_1: {"name": "一级回血瓶", "type": "potion", "health": 30, "color": (255, 0, 0), "texture": "一级回血瓶"},
    HEALTH_POTION_2: {"name": "二级回血瓶", "type": "potion", "health": 60, "extra_health": 10, "color": (255, 100, 100), "texture": "二级回血瓶"},
    HEALTH_POTION_3: {"name": "三级回血瓶", "type": "potion", "health": 100, "extra_health": 25, "color": (255, 50, 50), "texture": "三级回血瓶"},
    HEALTH_POTION_4: {"name": "四级回血瓶", "type": "potion", "health": 150, "extra_health": 50, "color": (255, 0, 0), "texture": "四级回血瓶"},
    
    # 雨林新增方块
    JUNGLE_TREE: {"name": "乔木", "type": "block", "block_id": JUNGLE_TREE, "color": (101, 67, 33), "texture": "乔木"},
    JUNGLE_LEAF: {"name": "乔木叶", "type": "block", "block_id": JUNGLE_LEAF, "color": (34, 177, 76), "texture": "乔木叶"},
    SHRUB: {"name": "灌木", "type": "block", "block_id": SHRUB, "color": (50, 200, 50), "texture": "灌木"},
    
    # 头盔类装备
    HELMET_1: {"name": "1级头盔", "type": "helmet", "defense": 1, "damage_bonus": 1, "color": (100, 100, 100), "texture": "1级头盔"},
    HELMET_2: {"name": "2级头盔", "type": "helmet", "defense": 2, "damage_bonus": 2, "color": (150, 150, 150), "texture": "2级头盔"},
    HELMET_3: {"name": "3级头盔", "type": "helmet", "defense": 3, "damage_bonus": 3, "color": (200, 200, 200), "texture": "3级头盔"},
    HELMET_4: {"name": "4级头盔", "type": "helmet", "defense": 5, "damage_bonus": 5, "color": (220, 220, 220), "texture": "4级头盔"},
    HELMET_5: {"name": "5级头盔", "type": "helmet", "defense": 8, "damage_bonus": 8, "color": (255, 255, 255), "texture": "5级头盔"},
    
    # 盔甲类装备
    ARMOR_1: {"name": "1级盔甲", "type": "armor", "defense": 3, "color": (100, 100, 100), "texture": "1级盔甲"},
    ARMOR_2: {"name": "2级盔甲", "type": "armor", "defense": 4, "color": (150, 150, 150), "texture": "2级盔甲"},
    ARMOR_3: {"name": "3级盔甲", "type": "armor", "defense": 5, "color": (200, 200, 200), "texture": "3级盔甲"},
    ARMOR_4: {"name": "4级盔甲", "type": "armor", "defense": 8, "color": (220, 220, 220), "texture": "4级盔甲"},
    ARMOR_5: {"name": "5级盔甲", "type": "armor", "defense": 12, "color": (255, 255, 255), "texture": "5级盔甲"},
    
    # 靴子类装备
    BOOTS_1: {"name": "1级靴子", "type": "boots", "defense": 1, "jump_bonus": 1, "fall_damage_reduction": 5, "color": (100, 100, 100), "texture": "1级靴子"},
    BOOTS_2: {"name": "2级靴子", "type": "boots", "defense": 2, "jump_bonus": 2, "fall_damage_reduction": 10, "color": (150, 150, 150), "texture": "2级靴子"},
    BOOTS_3: {"name": "3级靴子", "type": "boots", "defense": 3, "jump_bonus": 3, "fall_damage_reduction": 20, "color": (200, 200, 200), "texture": "3级靴子"},
    BOOTS_4: {"name": "4级靴子", "type": "boots", "defense": 5, "jump_bonus": 5, "fall_damage_reduction": 30, "color": (220, 220, 220), "texture": "4级靴子"},
    BOOTS_5: {"name": "5级靴子", "type": "boots", "defense": 8, "jump_bonus": 8, "fall_damage_reduction": 50, "color": (255, 255, 255), "texture": "5级靴子"},
    
    # 特殊类装备
    SPECIAL_1: {"name": "1级斗篷", "type": "special", "defense": 1, "speed_bonus": 2, "color": (100, 100, 200), "texture": "1级斗篷"},
    SPECIAL_2: {"name": "2级披风", "type": "special", "defense": 2, "speed_bonus": 4, "color": (150, 150, 255), "texture": "2级披风"},
    SPECIAL_3: {"name": "3级灵服", "type": "special", "defense": 3, "speed_bonus": 6, "color": (100, 200, 100), "texture": "3级灵服"},
    SPECIAL_4: {"name": "4级披风", "type": "special", "defense": 5, "speed_bonus": 9, "color": (150, 255, 150), "texture": "4级披风"},
    SPECIAL_5: {"name": "5级腰带", "type": "special", "defense": 8, "speed_bonus": 14, "color": (255, 200, 100), "texture": "5级腰带"}
    
}

# 生物属性
CREATURES = {
    SLIME: {"name": "史莱姆", "health": 20, "damage": 3, "speed": 1.5, "hostile": False, "texture": "史莱姆",
            "drops": [(MEAT, 0.3)], "jump_strength": 8},
    MARMOT: {"name": "土拨鼠", "health": 15, "damage": 2, "speed": 2.0, "hostile": False, "texture": "土拨鼠",
             "drops": [(MEAT, 0.5)], "jump_strength": 10},
    GHOST: {"name": "小幽灵", "health": 30, "damage": 5, "speed": 2.5, "hostile": True, "texture": "小幽灵",
            "drops": [], "jump_strength": 12, "flying": True},
    BAT: {"name": "小蝙蝠", "health": 10, "damage": 1, "speed": 3.0, "hostile": True, "texture": "小蝙蝠", "drops": [], "jump_strength": 15, "flying": True},
    FIRE_SPIRIT: {"name": "火焰精灵", "health": 40, "damage": 7, "speed": 2.0, "hostile": True, "texture": "火焰精灵",
                  "drops": [(MEAT, 0.7)], "jump_strength": 9},
    MUSHROOM_MONSTER: {"name": "蘑菇怪", "health": 35, "damage": 4, "speed": 1.8, "hostile": True, "texture": "蘑菇怪",
                       "drops": [(MEAT, 0.6)], "jump_strength": 7},
    ROCK_MONSTER: {"name": "岩石怪", "health": 50, "damage": 6, "speed": 1.2, "hostile": True, "texture": "岩石怪",
                   "drops": [(MEAT, 0.8)]},
    # 沙漠专属生物
    DESERT_WORM: {"name": "沙漠虫子", "health": 120, "damage": 5, "speed": 1.8, "hostile": True, "texture": "沙漠虫子",
                  "drops": [(MEAT, 0.8)], "desert_exclusive": True, "jump_strength": 6},
    SAND_WORM: {"name": "小沙虫", "health": 300, "damage": 20, "speed": 1.5, "hostile": True, "texture": "小沙虫",
                "drops": [(MEAT, 1.0), (GOLD_INGOT, 0.3)], "desert_exclusive": True, "scale": 2.0, "jump_strength": 5},
    BOSS_SAND_WORM: {"name": "BOSS沙虫", "health": 1500, "damage": 90, "speed": 1.2, "hostile": True, "texture": "boos沙虫",
                    "drops": [(MEAT, 2.0), (GOLD_INGOT, 0.6), (DIAMOND, 0.2)], "desert_exclusive": True, "boss": True, "scale": 4.0},
    # 雨林新增生物
    SCORPION: {"name": "蝎子", "health": 45, "damage": 8, "speed": 2.0, "hostile": True, "texture": "蝎子",
               "drops": [(MEAT, 0.7), (JUNGLE_FRUIT, 0.3)], "jungle_exclusive": True, "jump_strength": 6},
    MONKEY: {"name": "猴子", "health": 30, "damage": 3, "speed": 2.5, "hostile": False, "texture": "猴子",
             "drops": [(MEAT, 0.6), (JUNGLE_FRUIT, 0.8)], "jungle_exclusive": True, "jump_strength": 12}
}

# 交互范围
INTERACTION_RANGE = 5  # 以玩家为中心的半径


class ImageLoader:
    """图片加载器，处理所有游戏图片的加载和管理"""

    def __init__(self):
        self.images = {}
        self.load_all_images()

    def load_image(self, name):
        """加载单个图片，根据原始图片尺寸采用不同的压缩策略"""
        try:
            img = pygame.image.load(f"{name}.png").convert_alpha()
            
            # 获取原始图片尺寸
            orig_width, orig_height = img.get_size()
            max_dimension = max(orig_width, orig_height)
            
            # 根据最大尺寸决定压缩目标
            if max_dimension > 32 and max_dimension < 128:
                # 大于32小于128，压缩到32
                target_size = 32
            elif max_dimension >= 128 and max_dimension < 512:
                # 大于等于128小于512，压缩到128
                target_size = 128
            elif max_dimension >= 512 and max_dimension < 1280:
                # 大于等于512小于1280，压缩到1280
                target_size = 1280
            elif max_dimension >= 1280:
                # 大于等于1280，压缩到1280
                target_size = 1280
            else:
                # 小于等于32，保持原尺寸
                return img
            
            # 计算缩放比例，保持宽高比
            scale_factor = target_size / max_dimension
            new_width = int(orig_width * scale_factor)
            new_height = int(orig_height * scale_factor)
            
            return pygame.transform.scale(img, (new_width, new_height))
            
        except FileNotFoundError:
            print(f"警告: 无法加载图像 {name}.png: 文件未找到。")
            # 创建一个替代颜色块
            surf = pygame.Surface((32, 32), pygame.SRCALPHA)
            color = self.get_fallback_color(name)
            surf.fill(color)
            return surf
        except Exception as e:
            print(f"警告: 加载图像 {name}.png 时出错: {e}")
            # 创建一个替代颜色块
            surf = pygame.Surface((32, 32), pygame.SRCALPHA)
            surf.fill((255, 0, 255))  # 紫色作为错误颜色
            return surf

    def get_fallback_color(self, name):
        """为缺失的图片提供替代颜色"""
        color_map = {
            "土块": DIRT_BROWN,
            "草方块": GRASS_GREEN,
            "岩石": STONE_GRAY,
            "木头": WOOD_BROWN,
            "药水": (255, 0, 0),  # 红色作为药水的默认颜色
            "一级回血瓶": (255, 0, 0),
            "二级回血瓶": (255, 100, 100),
            "三级回血瓶": (255, 50, 50),
            "四级回血瓶": (255, 0, 0),
            "树叶": LEAF_GREEN,
            "铁矿石": ORE_SILVER,
            "金矿石": GOLD_YELLOW,
            "钻石矿石": DIAMOND_BLUE,
            # 远程武器
            "木弓箭": WOOD_BROWN,
            "木箭": WOOD_BROWN,
            # 枪械武器
            "步枪": ORE_SILVER,
            "手枪": ORE_SILVER,
            "狙击枪": ORE_SILVER,
            "子弹": ORE_SILVER,
            "水": WATER_BLUE,
            "岩浆": LAVA_RED,
            "箱子": CHEST_COLOR,
            "黑土块": (60, 30, 10),
            "木剑": WOOD_BROWN,
            "石剑": STONE_GRAY,
            "铜剑": (184, 115, 51),
            "铁剑": ORE_SILVER,
            "金剑": GOLD_YELLOW,
            "钻石剑": DIAMOND_BLUE,
            "木镐": WOOD_BROWN,
            "石镐": STONE_GRAY,
            "铜镐": (184, 115, 51),
            "铁镐": ORE_SILVER,
            "金镐": GOLD_YELLOW,
            "钻石镐": DIAMOND_BLUE,
            "木斧": WOOD_BROWN,
            "石斧": STONE_GRAY,
            "铜斧": (184, 115, 51),
            "铁斧": ORE_SILVER,
            "金斧": GOLD_YELLOW,
            "钻石斧头": DIAMOND_BLUE,
            "木铲": WOOD_BROWN,
            "石铲": STONE_GRAY,
            "铜铲": (184, 115, 51),
            "铁铲": ORE_SILVER,
            "金铲": GOLD_YELLOW,
            "钻石铲": DIAMOND_BLUE,
            "苹果": (255, 0, 0),
            "肉块": (139, 69, 19),
            "金块": GOLD_YELLOW,
            "铁块": ORE_SILVER,
            "铜块": (184, 115, 51),
            "钻石块": DIAMOND_BLUE,
            "基岩": (60, 60, 60),
            "木板": WOOD_BROWN,
            "铜矿石": (184, 115, 51),
            "史莱姆": (0, 255, 0),
            "土拨鼠": (139, 69, 19),
            "小幽灵": (200, 200, 255, 180),
            "小蝙蝠": (50, 50, 50),
            "火焰精灵": (255, 100, 0),
            "蘑菇怪": (200, 50, 200),
            "岩石怪": (100, 100, 100)
        }
        return color_map.get(name, (255, 0, 255))  # 默认紫色

    def load_all_images(self):
        """加载所有需要的图片"""
        # 方块图片
        for block_id in BLOCKS:
            block = BLOCKS[block_id]
            if block["texture"]:
                self.images[block["texture"]] = self.load_image(block["texture"])

        # 物品和工具图片
        for item_id in ITEMS:
            item = ITEMS[item_id]
            if item["texture"]:
                self.images[item["texture"]] = self.load_image(item["texture"])

        # 生物图片
        for creature_id in CREATURES:
            creature = CREATURES[creature_id]
            if creature["texture"]:
                self.images[creature["texture"]] = self.load_image(creature["texture"])


class Chest:
    """箱子类，存储物品并处理交互"""

    def __init__(self, x, y, generate_loot=True):
        self.x = x  # 世界坐标（像素）
        self.y = y  # 世界坐标（像素）
        self.tile_x = x // TILE_SIZE  # 格子坐标
        self.tile_y = y // TILE_SIZE  # 格子坐标
        self.items = []  # 存储物品 [(item_id, count), ...]，支持同一种物品有多个堆叠
        self.is_open = False
        # 只有在游戏生成的箱子中才自动生成物品，玩家放置的箱子默认为空
        if generate_loot:
            self.generate_loot()

    def generate_loot(self):
        """生成随机战利品"""
        loot_table = [
            (DIRT, 5, 20, 0.7),
            (STONE, 3, 15, 0.6),
            (WOOD, 5, 25, 0.7),
            (COPPER_ORE, 2, 10, 0.5),
            (IRON_ORE, 2, 8, 0.4),
            (GOLD_ORE, 1, 3, 0.2),
            (APPLE, 3, 8, 0.5),
            (GOLD_INGOT, 1, 3, 0.1),
            (IRON_INGOT, 2, 5, 0.2),

        ]

        for item_id, min_count, max_count, chance in loot_table:
            if random.random() < chance:
                count = random.randint(min_count, max_count)
                # 对于生成的战利品，我们仍然将相同类型的物品堆叠在一起
                # 但使用列表结构以便后续处理超过99的情况
                found = False
                for i, (existing_id, existing_count) in enumerate(self.items):
                    if existing_id == item_id:
                        self.items[i] = (item_id, existing_count + count)
                        found = True
                        break
                if not found:
                    self.items.append((item_id, count))

    def draw(self, screen, camera_x, camera_y, images):
        """绘制箱子"""
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y

        # 绘制箱子图片
        if "箱子" in images:
            screen.blit(images["箱子"], (draw_x, draw_y))
        else:
            pygame.draw.rect(screen, CHEST_COLOR, (draw_x, draw_y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, (100, 100, 100), (draw_x, draw_y, TILE_SIZE, TILE_SIZE), 2)

        # 箱子名称
        name_text = font_small.render("箱子", True, (255, 255, 255))
        screen.blit(name_text, (draw_x + 5, draw_y - 20))


class Creature:
    """生物类，处理所有生物的行为"""

    def __init__(self, creature_type, x, y):
        self.type = creature_type
        self.properties = CREATURES[creature_type]
        self.x = x  # 像素坐标
        self.y = y  # 像素坐标
        base_width = TILE_SIZE * 0.8
        base_height = TILE_SIZE * 0.8
        
        # 应用体积缩放因子
        self.scale = self.properties.get("scale", 1.0)
        self.width = base_width * self.scale
        self.height = base_height * self.scale
        
        self.health = self.properties["health"]
        self.max_health = self.properties["health"]
        self.damage = self.properties["damage"]
        self.speed = self.properties["speed"]
        self.hostile = self.properties["hostile"]
        self.vel_x = 0
        self.vel_y = 0
        self.attack_cooldown = 0
        self.immune_time = 0
        self.target = None
        self.wander_timer = 0
        self.wander_direction = random.uniform(0, math.pi * 2)
        self.jump_strength = self.properties.get("jump_strength", 0)
        self.jump_cooldown = 0
        self.is_on_ground = False
        self.defense = 0  # 默认防御力为0

    def update(self, world, player, dt):
        """更新生物状态和行为"""
        # 处理免疫时间
        if self.immune_time > 0:
            self.immune_time -= dt

        # 处理攻击冷却
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        # 生物AI
        if self.hostile:
            # 敌对生物追踪玩家
            self.target = player
            self.chase_target(dt)
        else:
            # 中立生物随机游荡
            self.wander(dt)

        # 检查是否是沙漠专属生物且在沙子中
        is_desert_creature = self.properties.get("desert_exclusive", False)
        in_sand = False
        # 检查生物是否在沙子中
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)
        if 0 <= tile_x < WORLD_WIDTH and 0 <= tile_y < WORLD_HEIGHT:
            if world.blocks[tile_y][tile_x] == SAND:
                in_sand = True
        
        # 应用重力
        gravity = 1.5
        # 沙漠生物在沙子中降低重力
        if is_desert_creature and in_sand:
            gravity = 0.3  # 沙子中的低重力
        
        # 飞行生物不受重力影响
        if self.properties.get("flying", False):
            gravity = 0
        
        self.vel_y += gravity

        # 限制最大下落速度
        max_fall_speed = 10
        # 沙漠生物在沙子中降低下落速度
        if is_desert_creature and in_sand:
            max_fall_speed = 3
        
        self.vel_y = min(self.vel_y, max_fall_speed)
        
        # 限制上升速度，允许生物跳跃
        max_rise_speed = -5.0  # 增加允许的最大上升速度，让跳跃更明显
        self.vel_y = max(self.vel_y, max_rise_speed)
        
        # 非飞行生物有3%概率无条件向上移动6格
        if not self.properties.get("flying", False) and random.random() < 0.03:
            self.vel_y = -self.jump_strength * 3.0  # 向上移动6格的速度


        # 水平移动
        move_speed_multiplier = 1.0
        # 沙漠生物在沙子中降低移动速度（类似玩家在水中行走）
        if is_desert_creature and in_sand:
            move_speed_multiplier = 0.6  # 沙子中的移动速度降低
        
        new_x = self.x + self.vel_x * dt * 60 * move_speed_multiplier
        if not self.check_collision(new_x, self.y, world):
            self.x = new_x
        else:
            self.vel_x = 0
            self.wander_direction = random.uniform(0, math.pi * 2)  # 碰撞后改变方向

        # 检查是否在地面上
        self.is_on_ground = self.check_collision(self.x, self.y + 1, world)
        
        # 处理跳跃冷却
        if self.jump_cooldown > 0:
            self.jump_cooldown -= dt
        
        # 垂直移动
        new_y = self.y + self.vel_y * dt * 60
        if not self.check_collision(self.x, new_y, world):
            self.y = new_y
        else:
            self.vel_y = 0

        # 攻击目标
        if self.target and self.attack_cooldown <= 0:
            tx, ty = self.target.x + self.target.width // 2, self.target.y + self.target.height // 2
            cx, cy = self.x + self.width // 2, self.y + self.height // 2
            distance = math.sqrt((tx - cx) ** 2 + (ty - cy) ** 2)

            if distance < TILE_SIZE * 1.5:  # 在攻击范围内
                # 生物攻击没有暴击
                if self.target.take_damage(self.damage):
                    # 标记为生物攻击，让Game类在update中处理伤害显示
                    self.target.last_damage_by_creature = self
                    self.target.last_damage_amount = self.damage
                self.attack_cooldown = 1.0  # 1秒冷却

    def check_shrub_damage(self, world):
        """检查是否触碰到灌木，若是则减少4点血量"""
        # 获取玩家所在格子的坐标
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)
        
        # 扩大检查范围，确保能检测到灌木碰撞
        for dy in range(-2, 3):  # 检查更大范围
            for dx in range(-2, 3):
                check_x = tile_x + dx
                check_y = tile_y + dy
    
    def check_shrub_damage(self, world):
        """检查是否触碰到灌木，若是则减少血量"""
        # 获取玩家所在格子的坐标
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)
        
        # 扩大检查范围，确保能检测到灌木碰撞
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                check_x = tile_x + dx
                check_y = tile_y + dy
                
                if 0 <= check_x < WORLD_WIDTH and 0 <= check_y < WORLD_HEIGHT:
                    if world.blocks[check_y][check_x] == SHRUB:
                        # 处理伤害逻辑
                        if not self.is_resurrection_immune and self.immune_time <= 0:
                            # 扣除4点血量
                            self.take_damage(4, "shrub")
                            # 增加无敌时间，减少伤害频率
                            self.immune_time = 1.0
                        
                        # 标记碰撞成功，直接返回
                        return
                
                if 0 <= check_x < WORLD_WIDTH and 0 <= check_y < WORLD_HEIGHT:
                    block_id = world.blocks[check_y][check_x]
                    if block_id == SHRUB:
                        # 处理伤害逻辑
                        if not self.is_resurrection_immune and self.immune_time <= 0:
                            # 扣除4点血量
                            damage = BLOCKS[SHRUB].get("damage", 4)
                            self.take_damage(damage, "shrub")
                            # 增加无敌时间，减少伤害频率
                            self.immune_time = 1.0
                        
                        # 标记碰撞成功，直接返回
                        return
        
    def check_collision(self, x, y, world):
        """检查与世界方块的碰撞"""
        points = [
            (x, y),
            (x + self.width, y),
            (x, y + self.height),
            (x + self.width, y + self.height)
        ]

        # 检查是否是沙漠专属生物
        is_desert_creature = self.properties.get("desert_exclusive", False)
        in_sand = False
        for px, py in points:
            tile_x = int(px // TILE_SIZE)
            tile_y = int(py // TILE_SIZE)

            if 0 <= tile_x < WORLD_WIDTH and 0 <= tile_y < WORLD_HEIGHT:
                block = world.blocks[tile_y][tile_x]
                # 沙漠生物可以穿透沙子、草和枯草
                if (block == SAND or block == GRASS or block == DRY_GRASS) and is_desert_creature:
                    if block == SAND:
                        in_sand = True
                    continue  # 跳过碰撞检测
                if block != AIR and BLOCKS[block]["solid"]:
                    return True
        return False

    def chase_target(self, dt):
        """追逐目标"""
        if not self.target:
            return

        # 计算朝向目标的方向
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 0:
            # 移动方向标准化
            self.vel_x = (dx / distance) * self.speed
            self.vel_y = (dy / distance) * self.speed * 0.5  # 垂直方向移动速度减半
            
            # 如果有跳跃能力且在地面上且在冷却时间外，则随机跳跃
            if self.jump_strength > 0 and self.is_on_ground and self.jump_cooldown <= 0:
                # 随机决定是否跳跃
                if random.random() < 0.8:  # 增加到80%的概率跳跃
                    self.jump()

    def wander(self, dt):
        """随机游荡"""
        self.wander_timer -= dt
        if self.wander_timer <= 0:
            self.wander_direction = random.uniform(0, math.pi * 2)
            self.wander_timer = random.uniform(1, 3)  # 1-3秒改变一次方向

        # 基于当前方向移动
        self.vel_x = math.cos(self.wander_direction) * self.speed
        self.vel_y = math.sin(self.wander_direction) * self.speed * 0.3  # 垂直方向移动较少
        
        # 如果有跳跃能力且在地面上且在冷却时间外，则随机跳跃
        if self.jump_strength > 0 and self.is_on_ground and self.jump_cooldown <= 0:
            # 随机决定是否跳跃
            if random.random() < 0.6:  # 增加到60%的概率跳跃
                self.jump()
    
    def jump(self):
        """生物跳跃"""
        if self.jump_strength > 0 and self.is_on_ground:
            self.vel_y = -self.jump_strength
            self.is_on_ground = False
            self.jump_cooldown = 1.0  # 减少冷却时间到1秒，让跳跃更频繁

    def take_damage(self, amount):
        """受到伤害，考虑装备防御力和免伤百分比，返回是否死亡"""
        if self.immune_time <= 0:
            # 计算最终伤害（使用免伤百分比，如果属性不存在则使用默认值0）
            damage_reduction = getattr(self, 'damage_reduction', 0)
            damage_reduction_factor = 1 - (damage_reduction / 100)
            final_damage = max(1, amount * damage_reduction_factor)  # 最小伤害为1
            self.health -= final_damage
            self.immune_time = 0.5  # 0.5秒免疫
            # 只有当生物确实死亡时才返回True
            return self.is_dead()
        return False

    def is_dead(self):
        """检查是否死亡"""
        return self.health <= 0

    def get_drops(self):
        """获取死亡掉落物"""
        drops = []
        for item_id, chance in self.properties["drops"]:
            if random.random() < chance:
                count = random.randint(1, 2)
                drops.append({"item_id": item_id, "quantity": count})
        return drops

    def draw(self, screen, camera_x, camera_y, images):
        """绘制生物"""
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y

        # 绘制生物图片 - 始终可见，不再使用闪烁消失效果
        texture_name = self.properties["texture"]
        if texture_name in images:
            # 始终缩放纹理以匹配生物的碰撞区域大小
            scaled_texture = pygame.transform.scale(images[texture_name], (int(self.width), int(self.height)))
            # 受伤时添加视觉反馈（轻微闪烁但不完全消失）
            if self.immune_time > 0 and self.immune_time % 0.1 < 0.05:
                # 使用半透明效果代替消失
                temp_surface = pygame.Surface((scaled_texture.get_width(), scaled_texture.get_height()), pygame.SRCALPHA)
                temp_surface.fill((255, 255, 255, 128))  # 半透明白色
                temp_surface.blit(scaled_texture, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                screen.blit(temp_surface, (draw_x, draw_y))
            else:
                screen.blit(scaled_texture, (draw_x, draw_y))
        else:
            # 默认矩形表示
            color = (100, 200, 100)
            # 受伤时稍微改变颜色以提供反馈
            if self.immune_time > 0:
                color = (200, 200, 200)  # 受伤时变灰
            pygame.draw.rect(screen, color, (draw_x, draw_y, self.width, self.height))

        # 绘制生命值
        health_bar_length = self.width
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (100, 0, 0), (draw_x, draw_y - 10, health_bar_length, 5))
        pygame.draw.rect(screen, (0, 255, 0), (draw_x, draw_y - 10, health_bar_length * health_ratio, 5))


class Player:
    """玩家类，处理玩家行为和状态"""

    def __init__(self, x, y):
        self.x = x  # 像素坐标
        self.y = y  # 像素坐标
        self.width = 28
        self.height = 56
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_strength = -10
        self.health = 100
        self.max_health = 100
        self.damage = 2  # 玩家初始伤害值
        self.hunger = 100
        self.max_hunger = 100
        self.oxygen = 100  # 氧气值
        self.max_oxygen = 100  # 最大氧气值
        self.extra_health = 0  # 额外血量（不可叠加）
        # 新增游戏变量
        self.defense = 0  # 防御力
        self.damage_reduction = 0  # 免伤百分比（0-100）
        self.damage_bonus = 0  # 伤害加成百分比（0-100）
        self.fall_damage_reduction = 0  # 摔伤减免百分比（0-100）
        self.speed_bonus = 0  # 移速加成百分比（0-100）
        # 装备系统
        self.equipment = {
            'helmet': 0,   # 头盔
            'armor': 0,    # 盔甲
            'boots': 0,    # 靴子
            'special': 0   # 特殊装备
        }
        # 背包和快捷栏都改为[[物品ID, 数量], [物品ID, 数量], ...]的结构
        self.inventory = []  # 背包，30格，每个元素是[物品ID, 数量]
        self.hotbar = []  # 快捷栏，8格，每个元素是[物品ID, 数量]
        self.selected_slot = 0  # 当前选中的快捷栏槽位
        
        # 初始化快捷栏为8个空格子，每个格子存储[0, 0]表示空物品和0数量
        for _ in range(8):
            self.hotbar.append([0, 0])  # [物品ID, 数量]
            
        self.backpack_slots = 30  # 背包格子数量
        # 初始化背包为30个空格子，每个格子存储[0, 0]表示空物品和0数量
        for _ in range(self.backpack_slots):  # 30格背包
            self.inventory.append([0, 0])  # [物品ID, 数量]
        self.facing_right = True
        self.on_ground = False
        self.in_water = False
        self.in_lava = False
        self.attack_cooldown = 0
        self.immune_time = 0
        self.is_resurrection_immune = False  # 标记无敌状态是否来自复活
        self.is_inventory_open = False
        self.is_crafting_open = False
        self.is_chest_open = False
        self.current_chest = None
        self.dragging_item = None  # 正在拖动的物品 {item_id, quantity}
        self.dragging_source = None  # 拖动来源: 'hotbar', 'inventory', 'chest'
        self.dragging_slot = None  # 拖动的槽位索引
        self.is_split_dragging = False  # 是否是右键拆分的物品拖动

        self.fall_start_y = None  # 记录开始下落的位置，用于计算重力伤害
        self.last_hunger_to_health_time = 0  # 记录上次饥饿值转换为生命值的时间
        self.last_hunger_decrease_time = 0  # 记录上次饥饿值减少的时间
        
        # 环境伤害相关属性
        self.last_environment_damage_type = None
        self.last_environment_damage_amount = 0
        self.last_environment_damage_position = (0, 0)
        
        # 燃烧状态相关属性
        self.burn_time = 0  # 燃烧状态剩余时间（秒）

        # 开局清空背包，不添加任何初始物品
        # 快捷栏保持初始的[0, 0, 0, 0, 0, 0, 0, 0]状态

        # 经验值和星星系统
        self.experience = 0  # 当前经验值
        self.stars = 10  # 默认10颗星星
        self.max_experience = 100  # 每100经验转换为1星星
        
        # 装备槽位
        self.equipment = {
            'helmet': 0,  # 头盔槽位
            'armor': 0,   # 盔甲槽位
            'boots': 0,   # 靴子槽位
            'special': 0  # 特殊装备槽位
        }
        
        # 装备加成属性
        self.defense = 0  # 当前防御力
        self.speed_boost = 0  # 当前速度加成
        self.health_boost = 0  # 当前生命值加成
        self.damage_boost = 0  # 当前伤害加成

    def equip_item(self, slot_type, item_id):
        """穿戴装备并更新游戏中的装备属性变量"""
        item_info = ITEMS.get(item_id)
        if not item_info or slot_type not in ['helmet', 'armor', 'boots', 'special']:
            return None
            
        # 保存之前的装备（如果有）
        previous_item = self.equipment[slot_type]
        
        # 装备新物品
        self.equipment[slot_type] = item_id
        
        # 更新装备加成
        self.update_equipment_bonuses()
        
        # 返回之前的装备（如果有）
        return previous_item
        
    def unequip_item(self, slot_type):
        """脱下装备"""
        if slot_type not in self.equipment:
            return None
            
        # 保存当前装备
        item_id = self.equipment[slot_type]
        
        # 移除装备
        self.equipment[slot_type] = 0
        
        # 更新装备加成
        self.update_equipment_bonuses()
        
        # 返回脱下的装备
        return item_id
        
    def update_equipment_bonuses(self):
        """更新装备提供的属性加成，并同步更新Game类中的装备属性变量"""
        # 重置所有加成
        self.defense = 0
        self.speed_boost = 0
        self.health_boost = 0
        self.damage_boost = 0
        self.damage_bonus = 0  # 伤害加成百分比
        self.fall_damage_reduction = 0  # 摔伤减免百分比
        self.speed_bonus = 0  # 移速加成百分比
        self.damage_reduction = 0  # 免伤百分比
        
        # 重置装备属性变量
        # 直接使用全局的game实例
        global game
        if 'game' in globals():
            game.头盔_伤害 = 0
            game.头盔_防御 = 0
            game.盔甲_防御 = 0
            game.靴子_摔伤 = 0
            game.靴子_跳跃 = 0
            game.靴子_防御 = 0
            game.特殊_移速 = 0
            game.特殊_防御 = 0
        
        # 计算所有已装备物品的加成
        for slot_type, item_id in self.equipment.items():
            if item_id != 0:
                item_info = ITEMS.get(item_id)
                if item_info:
                    self.defense += item_info.get('defense', 0)
                    self.speed_boost += item_info.get('speed_boost', 0)
                    self.health_boost += item_info.get('health_boost', 0)
                    self.damage_boost += item_info.get('damage_boost', 0)
                    self.damage_bonus += item_info.get('damage_bonus', 0)
                    self.fall_damage_reduction += item_info.get('fall_damage_reduction', 0)
                    self.speed_bonus += item_info.get('speed_bonus', 0)
                    
                    # 更新Game类中的装备属性变量
                    if 'game' in globals():
                        if slot_type == 'helmet':
                            game.头盔_伤害 = item_info.get('damage_bonus', 0)
                            game.头盔_防御 = item_info.get('defense', 0)
                        elif slot_type == 'armor':
                            game.盔甲_防御 = item_info.get('defense', 0)
                        elif slot_type == 'boots':
                            game.靴子_摔伤 = item_info.get('fall_damage_reduction', 0)
                            game.靴子_跳跃 = item_info.get('jump_bonus', 0)
                            game.靴子_防御 = item_info.get('defense', 0)
                        elif slot_type == 'special':
                            game.特殊_移速 = item_info.get('speed_bonus', 0)
                            game.特殊_防御 = item_info.get('defense', 0)
        
        # 计算免伤百分比：优先使用game变量中的防御值总和（如果大于0）
        defense_value = self.defense
        # 检查全局game实例中是否有防御相关值，且它们的总和大于0
        if 'game' in globals():
            game_defense_sum = 0
            if hasattr(game, '头盔_防御'):
                game_defense_sum += game.头盔_防御
            if hasattr(game, '盔甲_防御'):
                game_defense_sum += game.盔甲_防御
            if hasattr(game, '靴子_防御'):
                game_defense_sum += game.靴子_防御
            if hasattr(game, '特殊_防御'):
                game_defense_sum += game.特殊_防御
            if game_defense_sum > 0:
                defense_value = game_defense_sum
        
        if defense_value > 0:
            # 使用公式：免伤百分比 = (defense * 100) / (defense + 100)
            # 这样可以满足1防御≈1%，100防御=50%，且随防御增加逐渐趋近于100%但不超过
            self.damage_reduction = round((defense_value * 100) / (defense_value + 100), 1)
            # 确保不超过99.9%
            self.damage_reduction = min(99.9, self.damage_reduction)
        
        # 更新最大生命值（考虑生命值加成）
        base_max_health = 100  # 基础最大生命值
        self.max_health = base_max_health + self.health_boost
        # 如果当前生命值超过最大生命值，调整为最大生命值
        if self.health > self.max_health:
            self.health = self.max_health
        
    def add_item(self, item_id, quantity):
        """添加物品到背包，优先在已有相同物品的格子中添加数量，返回是否成功添加所有物品"""
        # 获取物品类型，确定堆叠上限
        item_type = ITEMS.get(item_id, {}).get('type', 'block')
        # 工具类物品（武器、镐、斧、铲）堆叠上限为1
        if item_type in ['weapon', 'pickaxe', 'axe', 'shovel']:
            max_stack = 1
        else:
            # 其他物品堆叠上限为99
            max_stack = 99
        
        # 先检查背包中是否有相同物品的格子且未达到堆叠上限
        for i in range(len(self.inventory)):
            if self.inventory[i][0] == item_id and self.inventory[i][1] > 0 and self.inventory[i][1] < max_stack:
                # 计算可以添加的数量
                add_amount = min(quantity, max_stack - self.inventory[i][1])
                self.inventory[i][1] += add_amount
                quantity -= add_amount
                if quantity <= 0:
                    return True
                # 继续寻找其他格子添加剩余数量
                continue
                
        # 检查快捷栏中是否有相同物品的格子且未达到堆叠上限
        for i in range(len(self.hotbar)):
            if self.hotbar[i][0] == item_id and self.hotbar[i][1] > 0 and self.hotbar[i][1] < max_stack:
                # 计算可以添加的数量
                add_amount = min(quantity, max_stack - self.hotbar[i][1])
                self.hotbar[i][1] += add_amount
                quantity -= add_amount
                if quantity <= 0:
                    return True
                # 继续寻找其他格子添加剩余数量
                continue
        
        # 如果没有相同物品，找一个空格子添加
        remaining_quantity = quantity
        while remaining_quantity > 0:
            # 计算当前格子可以添加的数量（不超过堆叠上限）
            add_amount = min(remaining_quantity, max_stack)
            
            # 先找背包空格子
            for i in range(len(self.inventory)):
                if self.inventory[i][0] == 0:
                    self.inventory[i] = [item_id, add_amount]
                    remaining_quantity -= add_amount
                    break
            else:
                # 背包满了，找快捷栏空格子
                for i in range(len(self.hotbar)):
                    if self.hotbar[i][0] == 0:
                        self.hotbar[i] = [item_id, add_amount]
                        remaining_quantity -= add_amount
                        break
                else:
                    # 都满了，无法添加物品
                    return False
        
        # 成功添加所有物品
        return True

    def remove_item(self, item_id, quantity):
        """从背包移除物品"""
        remaining_quantity = quantity
        
        # 先从背包中移除
        for i in range(len(self.inventory)):
            if self.inventory[i][0] == item_id and self.inventory[i][1] > 0:
                if self.inventory[i][1] >= remaining_quantity:
                    self.inventory[i][1] -= remaining_quantity
                    if self.inventory[i][1] <= 0:
                        self.inventory[i] = [0, 0]  # 设为空格子
                    return True
                else:
                    remaining_quantity -= self.inventory[i][1]
                    self.inventory[i] = [0, 0]  # 设为空格子
        
        # 再从快捷栏中移除
        for i in range(len(self.hotbar)):
            if self.hotbar[i][0] == item_id and self.hotbar[i][1] > 0:
                if self.hotbar[i][1] >= remaining_quantity:
                    self.hotbar[i][1] -= remaining_quantity
                    if self.hotbar[i][1] <= 0:
                        self.hotbar[i] = [0, 0]  # 设为空格子
                    return True
                else:
                    remaining_quantity -= self.hotbar[i][1]
                    self.hotbar[i] = [0, 0]  # 设为空格子
        
        # 物品不足或不存在
        return False

    def has_item(self, item_id, quantity=1):
        """检查是否拥有足够数量的物品"""
        total_quantity = 0
        
        # 计算背包中的物品总数量
        for item in self.inventory:
            if item[0] == item_id:
                total_quantity += item[1]
        
        # 计算快捷栏中的物品总数量
        for item in self.hotbar:
            if item[0] == item_id:
                total_quantity += item[1]
        
        return total_quantity >= quantity

    def get_selected_item(self):
        """获取当前选中的物品，只有物品ID不为0且数量大于0时才返回"""
        selected_item = self.hotbar[self.selected_slot]
        item_id, quantity = selected_item
        if item_id == 0 or quantity <= 0:
            return None
        return {
            "item_id": item_id,
            "quantity": quantity
        }

    def move(self, world, dt):
        """移动玩家并处理碰撞"""
        # 如果处于飞行模式，则忽略重力和地面检测
        if hasattr(self, 'fly_mode') and self.fly_mode:
            # 重置速度，准备飞行控制
            self.vel_y = 0
            
            # 检查是否按下W键或上箭头键（上升）
            if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP]:
                self.vel_y = -self.speed * 0.7  # 向上飞行
            # 检查是否按下S键或下箭头键（下降）
            if pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN]:
                self.vel_y = self.speed * 0.7  # 向下飞行
        else:
            # 应用重力
            gravity = 0.3 if self.in_water else 0.5
            # 如果设置了自定义重力，则使用自定义重力值
            gravity = getattr(self, 'gravity', gravity)
            if not self.on_ground:
                self.vel_y += gravity
            
            # 限制最大下落速度
            max_fall_speed = 3 if self.in_water else 10
            self.vel_y = min(self.vel_y, max_fall_speed)
            
            # 记录开始下落的位置
            if self.on_ground and self.fall_start_y is None:
                self.fall_start_y = self.y
            elif not self.on_ground and self.fall_start_y is None:
                self.fall_start_y = self.y

        # 水平移动
        new_x = self.x + self.vel_x * dt * 60
        if not self.check_collision(new_x, self.y, world):
            self.x = new_x

        # 垂直移动
        new_y = self.y + self.vel_y * dt * 60
        collision = self.check_collision(self.x, new_y, world)
        if not collision:
            self.y = new_y
            self.on_ground = False
        else:
            # 玩家落地，检查是否需要计算下落伤害
            if self.vel_y > 0:
                self.on_ground = True
                # 计算下落距离（以格为单位）
                if self.fall_start_y is not None:
                    fall_distance_pixels = self.fall_start_y - self.y
                    fall_distance_tiles = abs(fall_distance_pixels) / TILE_SIZE
                    # 8格摔下5生命值，每提高1格+5生命值伤害（修复负数伤害问题）
                    if fall_distance_tiles >= 8:
                        # 确保伤害始终为正数
                        damage = max(1, 5 + int((fall_distance_tiles - 6) * 5))
                        # 应用摔伤减免百分比，优先使用game变量中的值（如果大于0）
                        fall_damage_reduction = getattr(self, 'fall_damage_reduction', 0)
                        # 检查全局game实例中是否有靴子_摔伤值，且该值大于0
                        if 'game' in globals() and hasattr(game, '靴子_摔伤') and game.靴子_摔伤 > 0:
                            fall_damage_reduction = game.靴子_摔伤
                        fall_reduction_factor = 1 - (fall_damage_reduction / 100)
                        reduced_damage = max(1, int(damage * fall_reduction_factor))
                        self.take_damage(reduced_damage, "fall")
                    # 重置下落起始位置
                    self.fall_start_y = None
            self.vel_y = 0

        # 检查是否在水中
        self.check_water(world)
        
        # 检查是否触碰到仙人掌
        self.check_cactus_collision(world)
        # 检查是否触碰到灌木
        self.check_shrub_damage(world)
    
    def check_cactus_collision(self, world):
        """检查是否触碰到仙人掌，若是则减少血量（增加无敌时间）"""
        # 获取玩家所在格子的坐标
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)
        
        # 扩大检查范围，确保能检测到仙人掌碰撞
        for dy in range(-2, 3):  # 检查更大范围
            for dx in range(-2, 3):
                check_x = tile_x + dx
                check_y = tile_y + dy
                
                if 0 <= check_x < WORLD_WIDTH and 0 <= check_y < WORLD_HEIGHT:
                    if world.blocks[check_y][check_x] == CACTUS:
                        # 处理伤害逻辑
                        if not self.is_resurrection_immune and self.immune_time <= 0:
                            # 扣除3点血量
                            self.take_damage(3, "cactus")
                            # 增加无敌时间，减少伤害频率
                            self.immune_time = 2.0
                        
                        # 标记碰撞成功，直接返回
                        return
                        
    def check_shrub_damage(self, world):
        """检查是否触碰到灌木，若是则减少血量"""
        # 获取玩家所在格子的坐标
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)
        
        # 扩大检查范围，确保能检测到灌木碰撞
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                check_x = tile_x + dx
                check_y = tile_y + dy
                
                if 0 <= check_x < WORLD_WIDTH and 0 <= check_y < WORLD_HEIGHT:
                    if world.blocks[check_y][check_x] == SHRUB:
                        # 处理伤害逻辑
                        if not self.is_resurrection_immune and self.immune_time <= 0:
                            # 扣除4点血量
                            self.take_damage(4, "shrub")
                            # 增加无敌时间，减少伤害频率
                            self.immune_time = 1.0
                        
                        # 标记碰撞成功，直接返回
                        return

    def check_collision(self, x, y, world):
        """检查与世界方块的碰撞"""
        points = [
            (x, y),
            (x + self.width, y),
            (x, y + self.height),
            (x + self.width, y + self.height)
        ]

        for px, py in points:
            tile_x = int(px // TILE_SIZE)
            tile_y = int(py // TILE_SIZE)

            if 0 <= tile_x < WORLD_WIDTH and 0 <= tile_y < WORLD_HEIGHT:
                block = world.blocks[tile_y][tile_x]
                if block != AIR and BLOCKS[block]["solid"]:
                    return True
        return False

    def check_water(self, world):
        """检查是否在水中或岩浆中"""
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)
        self.in_water = False
        self.in_lava = False

        if 0 <= tile_x < WORLD_WIDTH and 0 <= tile_y < WORLD_HEIGHT:
            if world.blocks[tile_y][tile_x] == WATER:
                self.in_water = True
            elif world.blocks[tile_y][tile_x] == LAVA:
                self.in_lava = True

    def jump(self, world):
        """跳跃，增加向上概率机制以解决卡方块问题"""
        import random
        # 正常跳跃逻辑
        if self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False
        # 添加向上概率机制 - 当玩家紧贴地面但因为碰撞检测问题无法正常跳跃时
        elif random.random() < 0.3:  # 30%的概率可以向上跳跃
            # 检查玩家脚下方块
            tile_x = int(self.x // TILE_SIZE)
            tile_y = int((self.y + self.height) // TILE_SIZE)
            # 获取下方2格内的方块
            can_jump = False
            for dy in range(2):
                check_y = tile_y + dy
                if 0 <= check_y < WORLD_HEIGHT:
                    try:
                        block = world.blocks[check_y][tile_x]
                        if block != AIR and BLOCKS.get(block, {}).get("solid", False):
                            can_jump = True
                            break
                    except (IndexError, AttributeError):
                        # 防止索引越界或world对象属性问题
                        pass
            
            if can_jump:
                self.vel_y = self.jump_strength * 0.8  # 稍微降低跳跃力度
                self.on_ground = False

    def take_damage(self, amount, damage_type=None):
        """受到伤害，支持标记伤害类型以显示不同的伤害文本。优先消耗额外生命值"""
        if self.immune_time <= 0:
            # 初始化伤害到额外生命值的变量，确保在所有路径中都有定义
            damage_to_extra = 0
            # 应用免伤百分比，如果属性不存在则使用默认值0
            damage_reduction = getattr(self, 'damage_reduction', 0)
            damage_reduction_factor = 1 - (damage_reduction / 100)
            # 计算最终伤害，但不强制最小伤害为1，允许完全减免
            final_amount = max(0, amount * damage_reduction_factor)
            
            # 优先消耗额外生命值
            if self.extra_health > 0:
                damage_to_extra = min(final_amount, self.extra_health)
                self.extra_health -= damage_to_extra
                final_amount -= damage_to_extra
                
            # 剩余伤害消耗普通生命值，允许生命值降到0以下
            if final_amount > 0:
                self.health = self.health - final_amount
                
            self.immune_time = 1.0  # 1秒免疫
            # 受伤时不标记为复活无敌
            self.is_resurrection_immune = False
            
            # 如果是环境伤害（岩浆、摔伤等），标记伤害类型和最终实际伤害值
            if damage_type:
                self.last_environment_damage_type = damage_type
                # 记录最终实际扣除的生命值（已经过所有减免）
                actual_damage = damage_to_extra + (final_amount if final_amount > 0 else 0)
                self.last_environment_damage_amount = actual_damage
                self.last_environment_damage_position = (self.x + self.width // 2, self.y)
                
            return True
        return False

    def heal(self, amount):
        """恢复生命值。优先恢复普通生命值"""
        # 优先恢复普通生命值到最大值
        health_deficit = self.max_health - self.health
        if health_deficit > 0:
            heal_amount = min(amount, health_deficit)
            self.health += heal_amount
            amount -= heal_amount
            
        # 剩余治疗量用于恢复额外生命值
        if amount > 0 and self.extra_health > 0:  # 只在已有额外生命值时才恢复
            self.extra_health += amount

    def eat(self, item_id):
        """吃东西恢复饥饿度和生命值，或使用药水恢复生命值和增加额外血量"""
        if item_id in ITEMS:
            # 处理食物
            if ITEMS[item_id]["type"] == "food":
                if self.remove_item(item_id, 1):
                    self.hunger = min(self.max_hunger, self.hunger + ITEMS[item_id]["hunger"])
                    self.heal(ITEMS[item_id]["health"])
                    return True
            # 处理药水
            elif ITEMS[item_id]["type"] == "potion":
                if self.remove_item(item_id, 1):
                    # 恢复当前生命值
                    self.heal(ITEMS[item_id]["health"])
                    # 增加不可叠加的额外血量（只有更高等级的药水才能替换当前的额外血量）
                    if "extra_health" in ITEMS[item_id] and ITEMS[item_id]["extra_health"] > self.extra_health:
                        self.extra_health = ITEMS[item_id]["extra_health"]
                        print(f"[{time.strftime('%H:%M:%S')}] 获得额外血量: {self.extra_health}")
                    return True
        return False
        
    def add_experience(self, amount):
        """增加经验值，如果达到100经验则转换为1颗星星"""
        self.experience += amount
        
        # 检查是否可以转换为星星
        if self.experience >= self.max_experience:
            # 计算可以转换的星星数量
            star_increase = self.experience // self.max_experience
            self.stars += star_increase
            # 保留剩余经验值
            self.experience = self.experience % self.max_experience
            
            # 返回获得的星星数量，用于显示信息
            return star_increase
        
        return 0  # 没有获得星星
    
    def is_dead(self):
        """检查玩家是否死亡"""
        return self.health <= 0

    def attack(self, creatures):
        """攻击范围内的生物"""
        if self.attack_cooldown > 0:
            return

        # 获取当前手持物品
        weapon = self.get_selected_item()
        damage = 2  # 空手伤害

        # 如果有武器，使用武器伤害
        if weapon and ITEMS[weapon["item_id"]]["type"] in ["weapon", "axe", "pickaxe", "shovel"]:
            damage = ITEMS[weapon["item_id"]]["damage"]
            # 设置冷却时间（基于武器速度）
            self.attack_cooldown = 1.0 / ITEMS[weapon["item_id"]]["speed"]
        else:
            self.attack_cooldown = 1.0  # 空手冷却时间

        # 检查范围内的生物
        cx, cy = self.x + self.width // 2, self.y + self.height // 2
        for creature in creatures:
            tx, ty = creature.x + creature.width // 2, creature.y + creature.height // 2
            distance = math.sqrt((tx - cx) ** 2 + (ty - cy) ** 2)

            if distance < TILE_SIZE * INTERACTION_RANGE:  # 在交互范围内
                creature.take_damage(damage)
                # 如果生物死亡，掉落物品
                if creature.is_dead():
                        drops = creature.get_drops()
                        # 创建掉落物实体
                        for drop in drops:
                            # 在生物位置创建物品实体
                            item_entity = ItemEntity(
                                creature.x + creature.width // 2 - 12,  # 居中
                                creature.y + creature.height // 2 - 12,  # 居中
                                drop["item_id"],
                                drop["quantity"]
                            )
                            # 添加到游戏的物品实体列表
                            game.item_entities.append(item_entity)
                        break

    def update(self, keys, world, dt):
        """更新玩家状态"""
        if self.is_inventory_open or self.is_crafting_open:
            return  # 打开界面时暂停移动

        self.vel_x = 0
        # 应用速度加成百分比，优先使用game变量中的值（如果大于0）
        speed_bonus = getattr(self, 'speed_bonus', 0)
        # 检查全局game实例中是否有特殊_移速值，且该值大于0
        if 'game' in globals() and hasattr(game, '特殊_移速') and game.特殊_移速 > 0:
            speed_bonus = game.特殊_移速
        speed_bonus_factor = 1 + (speed_bonus / 100)
        effective_speed = self.speed * speed_bonus_factor
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -effective_speed
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = effective_speed
            self.facing_right = True

        # 检查玩家是否位于世界高度以下（岩层下方）
        if self.y > WORLD_HEIGHT * TILE_SIZE:
            # 传送回出生点
            self.x = WORLD_WIDTH * TILE_SIZE // 2
            self.y = 0
            # 设置短暂无敌状态，避免传送后立即受到伤害
            self.immune_time = 2.0
        
        # 检查玩家x坐标边界，实现水平传送
        # 转换像素坐标为世界坐标（格子坐标）
        tile_x = int(self.x // TILE_SIZE)
        if tile_x <= -1:
            # 当玩家x坐标为-1时，传送到世界宽度-2的位置
            self.x = (WORLD_WIDTH - 2) * TILE_SIZE
        elif tile_x >= WORLD_WIDTH - 1:
            # 当玩家x坐标大于等于世界宽度-1时，传送回0位置
            self.x = 0 * TILE_SIZE

        self.move(world, dt)

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump(world)

        # 更新冷却时间
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        if self.immune_time > 0:
            self.immune_time -= dt
            # 当无敌时间结束时，重置复活无敌标志
            if self.immune_time <= 0:
                self.is_resurrection_immune = False

        # 饥饿消耗 - 基于游戏内时间的每小时减少1饥饿值
        # 游戏内一小时 = 100个时间单位 (游戏内一天2400单位，24小时)
        current_time = world.time_of_day
        # 计算当前是第几小时
        current_hour = int(current_time / 100)
        # 记录上次减少时的小时
        if not hasattr(self, 'last_hunger_decrease_hour'):
            self.last_hunger_decrease_hour = current_hour
        
        # 如果进入了新的游戏内小时
        if current_hour != self.last_hunger_decrease_hour:
            self.hunger = max(0, self.hunger - 1)
            self.last_hunger_decrease_hour = current_hour
        
        # 当饥饿值为0时，玩家死亡
        if self.hunger <= 0:
            self.health = 0
        
        # 饥饿值转换为生命值（血不满且饥饿值大于20且玩家未死亡时）
        self.last_hunger_to_health_time += dt
        if self.health < self.max_health and self.health > 0 and self.hunger > 20 and self.last_hunger_to_health_time >= 5.0:
            # 每1饥饿值转换5生命值
            hunger_to_convert = 1
            health_to_heal = hunger_to_convert * 5
            
            self.hunger = max(0, self.hunger - hunger_to_convert)
            self.health = min(self.max_health, self.health + health_to_heal)
            
            # 重置计时器
            self.last_hunger_to_health_time = 0

        # 氧气系统
        # 在水中或岩浆中消耗氧气（30秒完全消耗）
        if self.in_water or self.in_lava:
            oxygen_consumption_rate = self.max_oxygen / 30  # 30秒消耗完所有氧气
            self.oxygen = max(0, self.oxygen - oxygen_consumption_rate * dt)
            # 氧气值为0时，每秒减少10点生命值
            if self.oxygen <= 0:
                # 每秒减少10点生命值，通过take_damage方法处理，优先消耗额外生命值
                damage_per_second = 10
                # 使用take_damage方法处理伤害，传入"oxygen"作为伤害类型
                self.take_damage(damage_per_second * dt, "oxygen")
            
            # 在岩浆中时，记录在岩浆中的状态
            if not hasattr(self, 'in_lava_last_frame'):
                self.in_lava_last_frame = False
            # 只有在岩浆中时才设置为True，不在水中设置
            if self.in_lava:
                self.in_lava_last_frame = True
        else:
            # 在空气中恢复氧气（每秒恢复20%）
            oxygen_recovery_rate = self.max_oxygen * 0.2  # 每秒恢复20%
            self.oxygen = min(self.max_oxygen, self.oxygen + oxygen_recovery_rate * dt)
            
            # 检查是否刚刚离开岩浆
            if hasattr(self, 'in_lava_last_frame') and self.in_lava_last_frame:
                # 离开岩浆时，设置燃烧状态，持续10秒
                self.burn_time = 10.0
                # 确保in_lava_last_frame只在岩浆中设置为True，不在水中设置
                self.in_lava_last_frame = False
        
        # 处理燃烧状态
        if hasattr(self, 'burn_time') and self.burn_time > 0:
            # 如果玩家在水中，立即解除燃烧状态
            if hasattr(self, 'in_water') and self.in_water:
                self.burn_time = 0
            else:
                # 更新燃烧时间
                self.burn_time = max(0, self.burn_time - dt)
            
            # 燃烧时每秒减少5点生命值
            # 检查是否需要处理燃烧伤害（避免频繁扣血）
            if not hasattr(self, 'last_burn_damage_time'):
                self.last_burn_damage_time = 0
            
            self.last_burn_damage_time += dt
            if self.last_burn_damage_time >= 1.0 and self.immune_time <= 0:
                # 只有当无敌时间结束时才处理燃烧伤害
                # 每秒减少15点生命值，通过take_damage方法处理，优先消耗额外生命值
                self.take_damage(15, "fire")
                self.last_burn_damage_time = 0

    def draw(self, screen, camera_x, camera_y, images):
        """绘制玩家"""
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y

        # 闪烁效果（受伤时）
        if self.immune_time % 0.1 < 0.05 or self.immune_time <= 0:
            # 身体
            pygame.draw.rect(screen, PLAYER_SKIN, (draw_x, draw_y, self.width, self.height))

            # 衣服
            pygame.draw.rect(screen, PLAYER_SHIRT, (draw_x, draw_y + self.height // 3, self.width, self.height // 3))
            pygame.draw.rect(screen, PLAYER_PANTS,
                             (draw_x, draw_y + self.height * 2 // 3, self.width, self.height // 3))

            # 头部
            head_bob = math.sin(time.time() * 5) * 2 if abs(self.vel_x) > 0.1 else 0
            pygame.draw.circle(screen, PLAYER_SKIN, (draw_x + self.width // 2, draw_y - 5 + head_bob), 12)

            # 眼睛
            eye_offset = 3 if self.facing_right else -3
            pygame.draw.circle(screen, (255, 255, 255), (draw_x + self.width // 2 + eye_offset, draw_y - 8 + head_bob),
                               3)

            # 手持物品
            selected_item = self.get_selected_item()
            if selected_item:
                item_info = ITEMS.get(selected_item["item_id"])
                if item_info and item_info["texture"] in images:
                    item_img = images[item_info["texture"]]
                    # 调整物品位置，使其看起来像是握在手中
                    hand_x = draw_x + self.width if self.facing_right else draw_x - TILE_SIZE // 2
                    hand_y = draw_y + self.height // 2
                    screen.blit(pygame.transform.scale(item_img, (TILE_SIZE // 2, TILE_SIZE // 2)), (hand_x, hand_y))
                    
                    # 如果手持狙击枪，绘制半透明红线指示射击方向
                    if selected_item["item_id"] == SNIPER:
                        # 获取鼠标位置
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        # 计算枪口位置（从玩家角色出发）
                        gun_x = draw_x + self.width // 2
                        gun_y = draw_y + self.height // 2
                        # 计算方向向量
                        dx = mouse_x - gun_x
                        dy = mouse_y - gun_y
                        # 计算向量长度
                        length = max(1, (dx**2 + dy**2)**0.5)
                        # 归一化向量
                        normalized_dx = dx / length
                        normalized_dy = dy / length
                        # 计算延伸后的终点（超过鼠标位置三倍距离）
                        extended_x = gun_x + normalized_dx * length * 3
                        extended_y = gun_y + normalized_dy * length * 3
                        # 创建半透明的红线
                        red_line = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                        # 设置半透明红色，透明度为128
                        pygame.draw.line(red_line, (255, 0, 0, 128), (gun_x, gun_y), (extended_x, extended_y), 2)
                        # 绘制到屏幕上
                        screen.blit(red_line, (0, 0))
                     
    def load_from_save(self, save_data):
        """从存档数据加载玩家状态"""
        if "player" in save_data:
            player_data = save_data["player"]
            
            # 加载基本属性
            if "x" in player_data: self.x = player_data["x"]
            if "y" in player_data: self.y = player_data["y"]
            if "health" in player_data: self.health = player_data["health"]
            if "hunger" in player_data: self.hunger = player_data["hunger"]
            if "oxygen" in player_data: self.oxygen = player_data["oxygen"]
            if "facing_right" in player_data: self.facing_right = player_data["facing_right"]
            if "on_ground" in player_data: self.on_ground = player_data["on_ground"]
            
            # 加载经验值和星星系统
            if "experience" in player_data: self.experience = player_data["experience"]
            if "stars" in player_data: self.stars = player_data["stars"]
            if "max_experience" in player_data: self.max_experience = player_data["max_experience"]
            
            # 加载物品栏
            if "inventory" in player_data:
                inventory_data = player_data["inventory"]
                # 检查数据格式并转换为列表结构 [[item_id, quantity]]
                if isinstance(inventory_data, list) and inventory_data and isinstance(inventory_data[0], str):
                    # 从字符串格式解析
                    new_inventory = []
                    for item_str in inventory_data:
                        # 尝试从字符串中提取物品ID和数量
                        try:
                            # 格式: "背包X:道具编号XXX,数量:XX"
                            parts = item_str.split(":")
                            if len(parts) >= 3:
                                item_id_part = parts[1].strip()
                                quantity_part = parts[2].strip().split()[0]
                                # 提取数字部分
                                item_id = int(''.join(filter(str.isdigit, item_id_part)))
                                quantity = int(''.join(filter(str.isdigit, quantity_part)))
                                new_inventory.append([item_id, quantity])
                        except:
                            pass  # 解析失败时跳过此物品
                    # 确保inventory有30个格子
                    while len(new_inventory) < self.backpack_slots:
                        new_inventory.append([0, 0])
                    self.inventory = new_inventory
                else:
                    self.inventory = inventory_data.copy()
            if "hotbar" in player_data:
                hotbar_data = player_data["hotbar"]
                # 检查数据格式并转换为列表结构 [[item_id, quantity]]
                if isinstance(hotbar_data, list) and hotbar_data and isinstance(hotbar_data[0], str):
                    # 从字符串格式解析
                    new_hotbar = []
                    for item_str in hotbar_data:
                        # 尝试从字符串中提取物品ID和数量
                        try:
                            # 格式: "快捷栏X:道具编号XX,数量:XX (选中)" 或 "快捷栏X:道具编号XX,数量:XX"
                            parts = item_str.split(":")
                            if len(parts) >= 3:
                                item_id_part = parts[1].strip()
                                quantity_part = parts[2].strip().split()[0]
                                # 提取数字部分
                                item_id = int(''.join(filter(str.isdigit, item_id_part)))
                                quantity = int(''.join(filter(str.isdigit, quantity_part)))
                                new_hotbar.append([item_id, quantity])
                        except:
                            pass  # 解析失败时跳过此物品
                    # 确保hotbar有8个格子
                    while len(new_hotbar) < self.hotbar_size:
                        new_hotbar.append([0, 0])
                    self.hotbar = new_hotbar
                else:
                    self.hotbar = hotbar_data.copy()
            if "selected_slot" in player_data:
                self.selected_slot = player_data["selected_slot"]


class World:
    """世界类，管理地形、方块和液体物理"""

    def __init__(self, image_loader, world_type="随机世界"):
        self.blocks = [[AIR for _ in range(WORLD_WIDTH)] for _ in range(WORLD_HEIGHT)]
        self.liquids = []  # 存储液体方块的额外信息
        self.chests = []
        self.time_of_day = 600  # 早上6点开始
        self.image_loader = image_loader
        self.world_type = world_type  # 添加世界类型属性
        self.generate_terrain()
        self.lava_burn_timer = 10  # 岩浆烧毁计时器（秒）
        self.is_raining = False  # 下雨状态标记
        # 添加存储不同箱子物品数据的字典，键为(x,y)坐标元组，值为物品列表
        self.chest_data = {}        
        # 存储玩家放置的箱子坐标，用于区分自然生成的箱子
        self.player_placed_chests = set()
    
    def get_chest_items(self, x, y, is_player_placed=False):
        """根据坐标获取箱子的物品列表，区分自然生成和玩家放置的箱子"""
        import random
        key = (x, y)
        if key not in self.chest_data:
            # 创建空的箱子物品列表，默认27个槽位
            chest_items = [[0, 0] for _ in range(27)]
            
            # 只有自然生成的箱子才会生成随机物品
            if not is_player_placed:
                # 基础物资表 (item_id, min_count, max_count, chance)
                loot_table = [
                    (DIRT, 5, 20, 0.7),
                    (STONE, 3, 15, 0.6),
                    (WOOD, 5, 25, 0.7),
                    (COPPER_ORE, 2, 10, 0.5),
                    (IRON_ORE, 2, 8, 0.4),
                    (GOLD_ORE, 1, 3, 0.2),
                    (APPLE, 3, 8, 0.5),
                    (GOLD_INGOT, 1, 3, 0.1),
                    (IRON_INGOT, 2, 5, 0.2),
                ]
                
                # 特殊物资 - 四种等级的回血药水（100%刷新）
                potions = [
                    (HEALTH_POTION_1, 1, 2, 1.0),  # 一级回血瓶（100%概率）
                    (HEALTH_POTION_2, 1, 1, 1.0),  # 二级回血瓶（100%概率）
                    (HEALTH_POTION_3, 1, 1, 1.0),  # 三级回血瓶（100%概率）
                    (HEALTH_POTION_4, 1, 1, 1.0)   # 四级回血瓶（100%概率）
                ]
                
                # 先添加特殊物资（100%刷新）
                potion_slot_indices = random.sample(range(len(chest_items)), len(potions))
                for i, (item_id, min_count, max_count, _) in enumerate(potions):
                    count = random.randint(min_count, max_count)
                    chest_items[potion_slot_indices[i]] = [item_id, count]
                
                # 然后添加基础物资
                filled_slots = len(potions)
                max_items = random.randint(3, 8) + filled_slots  # 加上已填充的药水槽位
                
                for item_id, min_count, max_count, chance in loot_table:
                    if filled_slots >= max_items:
                        break
                    
                    if random.random() < chance:
                        count = random.randint(min_count, max_count)
                        # 随机选择一个空槽位放置物品
                        empty_slots = [i for i, slot in enumerate(chest_items) if slot[0] == 0]
                        if empty_slots:
                            slot_index = random.choice(empty_slots)
                            chest_items[slot_index] = [item_id, count]
                            filled_slots += 1
            
            self.chest_data[key] = chest_items
        return self.chest_data[key]
    
    def set_chest_items(self, x, y, items):
        """设置指定坐标箱子的物品列表"""
        key = (x, y)
        self.chest_data[key] = items
        
    def load_from_save(self, save_data):
        """从存档数据加载世界状态"""
        world_data = save_data.get("world", {})
        # 加载方块数据
        if "blocks" in world_data:
            self.blocks = world_data["blocks"]
        # 加载时间数据
        if "time_of_day" in world_data:
            self.time_of_day = world_data["time_of_day"]
        # 加载下雨状态
        if "is_raining" in world_data:
            self.is_raining = world_data["is_raining"]
        # 加载液体数据
        if "liquids" in world_data:
            self.liquids = world_data["liquids"]
        # 加载箱子数据
        if "chests" in world_data:
            loaded_chests = []
            for chest_data in world_data["chests"]:
                if isinstance(chest_data, dict) and "x" in chest_data and "y" in chest_data:
                    # 创建新的Chest对象
                    new_chest = Chest(chest_data["x"], chest_data["y"], generate_loot=False)
                    # 加载物品数据（如果有）
                    if "items" in chest_data:
                        # 如果items是列表格式（新格式）
                        if isinstance(chest_data["items"], list):
                            new_chest.items = chest_data["items"]
                        # 如果items是字典格式（旧格式）
                        elif isinstance(chest_data["items"], dict):
                            # 转换旧格式（字典）为新格式（列表）
                            new_chest.items = [(item_id, count) for item_id, count in chest_data["items"].items()]
                    loaded_chests.append(new_chest)
                else:
                    # 向后兼容：如果chest_data不是预期的格式，直接添加（例如旧存档格式）
                    loaded_chests.append(chest_data)
            self.chests = loaded_chests

    def generate_terrain(self):
        """生成地形"""
        if hasattr(self, 'world_type') and self.world_type == "平原世界":
            # 平原世界地形生成逻辑
            self.generate_plains_terrain()
        else:
            # 随机世界（默认）地形生成逻辑
            self.generate_random_terrain()
            
    def generate_random_terrain(self):
        """生成随机地形"""
        # 创建高度图
        height_map = [0] * WORLD_WIDTH
        for x in range(WORLD_WIDTH):
            # 使用正弦函数创建地形起伏，根据WORLD_WIDTH调整系数以适应超大地图
            height = 80 + int(math.sin(x * 0.005) * 12 +  # 减小系数以增加波长，使长距离地形变化更平缓
                              math.sin(x * 0.02) * 6 +  # 中等波长提供中等距离变化
                              math.sin(x * 0.1) * 3 +  # 保持短距离变化
                              random.uniform(-2, 2))  # 增加随机偏移以增加地形多样性
            height = max(50, min(height, WORLD_HEIGHT - 30))
            height_map[x] = height
            
        # 添加高山地形
        # 根据地图宽度动态调整高山区域数量
        mountain_count = max(2, WORLD_WIDTH // 1000)  # 每1000宽至少1个高山区域
        mountain_regions = []
        
        for _ in range(mountain_count):
            # 随机选择高山区域的起始位置
            start_x = random.randint(100, WORLD_WIDTH - 300)
            # 随机选择高山区域的宽度
            width = random.randint(150, 250)
            # 随机选择高山的高度峰值（比普通地形高20-40格）
            peak_height = random.randint(40, 60)
            
            mountain_regions.append((start_x, start_x + width))
            
            # 生成高山地形
            for x in range(start_x, start_x + width):
                if 0 <= x < WORLD_WIDTH:
                    # 使用二次函数创建山峰形状（更自然的山体轮廓）
                    distance_from_center = abs(x - (start_x + width // 2))
                    # 距离中心越远，高度越低，使用指数衰减以获得更陡峭的山峰
                    mountain_factor = math.exp(-distance_from_center / (width * 0.3))
                    # 计算山峰高度
                    mountain_height = int(peak_height * mountain_factor)
                    # 确保高山不会超出世界高度
                    new_height = max(50, min(height_map[x] - mountain_height, WORLD_HEIGHT - 30))
                    height_map[x] = new_height
        
        # 添加草原地形（±3起伏）
        # 根据地图宽度动态调整草原区域数量
        grassland_count = max(3, WORLD_WIDTH // 800)  # 每800宽至少1个草原区域
        grassland_regions = []
        
        for _ in range(grassland_count):
            # 随机选择草原区域的起始位置
            start_x = random.randint(100, WORLD_WIDTH - 400)
            # 随机选择草原区域的宽度
            width = random.randint(200, 400)
            
            # 检查是否与高山、沙漠区域重叠
            overlapping = False
            min_distance = 100  # 与其他地形保持最小距离
            
            # 检查是否与高山重叠
            for (m_start, m_end) in mountain_regions:
                if not (start_x + width + min_distance < m_start or start_x - min_distance > m_end):
                    overlapping = True
                    break
            
            if not overlapping:
                grassland_regions.append((start_x, start_x + width))
        
        # 如果草原区域数量不足，强制创建更多
        min_required_grasslands = max(1, grassland_count // 2)  # 至少需要一半的草原区域
        while len(grassland_regions) < min_required_grasslands:
            width = random.randint(150, 300)  # 使用较小的宽度增加成功概率
            start_x = random.randint(50, WORLD_WIDTH - width - 50)
            grassland_regions.append((start_x, start_x + width))
        
        # 应用草原地形的±3起伏限制
        for (g_start, g_end) in grassland_regions:
            # 计算草原区域的平均高度
            total_height = 0
            count = 0
            for x in range(g_start, g_end):
                if 0 <= x < WORLD_WIDTH:
                    total_height += height_map[x]
                    count += 1
            if count > 0:
                avg_height = total_height // count
                
                # 对草原区域应用±3起伏限制
                for x in range(g_start, g_end):
                    if 0 <= x < WORLD_WIDTH:
                        # 限制高度在平均高度±3范围内
                        height_map[x] = max(avg_height - 3, min(height_map[x], avg_height + 3))
        
        # 添加地形平滑处理，但保留更多短距离变化
        # 创建临时数组存储平滑后的高度
        smoothed_heights = [0] * WORLD_WIDTH
        
        # 第一个和最后一个点保持不变
        smoothed_heights[0] = height_map[0]
        smoothed_heights[WORLD_WIDTH - 1] = height_map[WORLD_WIDTH - 1]
        
        # 对中间点进行平滑处理（使用3点加权平均滤波）
        for x in range(1, WORLD_WIDTH - 1):
            # 当前点权重更高，保留更多短距离特征
            smoothed_heights[x] = int((height_map[x-1] * 0.2 + height_map[x] * 0.6 + height_map[x+1] * 0.2))
            
        # 减少一次平滑处理，保留更多原始地形特征
        # 仅对长距离不规则性进行一次额外平滑
        
        # 将平滑后的高度赋值回高度图
        for x in range(WORLD_WIDTH):
            height_map[x] = smoothed_heights[x]
        
        # 标记沙漠区域和雨林区域
        desert_regions = []
        rainforest_regions = []
        
        # 根据地图宽度动态调整沙漠数量
        desert_count = max(3, WORLD_WIDTH // 2000)  # 每2000宽至少1个沙漠区域
        for _ in range(desert_count):  # 创建多个沙漠区域
            start_x = random.randint(100, WORLD_WIDTH - 400)  # 确保有足够空间
            width = random.randint(200, 500)  # 增加沙漠宽度范围
            desert_regions.append((start_x, start_x + width))
        
        # 添加雨林区域
        # 增加雨林区域数量以提高出现概率
        rainforest_count = max(2, WORLD_WIDTH // 1500)  # 每1500宽至少2个雨林区域
        for _ in range(rainforest_count):  # 创建雨林区域
            # 调整宽度和起始位置，适应较小的世界
            width = random.randint(120, 200)  # 减小宽度范围，增加成功创建概率
            start_x = random.randint(50, WORLD_WIDTH - width - 50)  # 确保有足够空间
            
            # 检查是否与沙漠区域重叠，但允许部分重叠以增加雨林出现概率
            overlapping = False
            min_distance = 50  # 允许与沙漠区域保持最小距离
            for (d_start, d_end) in desert_regions:
                if not (start_x + width + min_distance < d_start or start_x - min_distance > d_end):
                    overlapping = True
                    break
            
            # 如果不重叠或者尝试次数较多，就添加这个雨林区域
            if not overlapping or len(rainforest_regions) < max(1, rainforest_count // 2):
                rainforest_regions.append((start_x, start_x + width))
        
        # 如果雨林区域数量不足，强制创建更多的雨林区域
        min_required_rainforests = max(1, rainforest_count // 2)  # 至少需要一半的雨林区域
        while len(rainforest_regions) < min_required_rainforests:
            width = random.randint(100, 180)  # 使用较小的宽度增加成功概率
            start_x = random.randint(50, WORLD_WIDTH - width - 50)
            # 不检查重叠，直接添加，确保至少有足够的雨林区域
            rainforest_regions.append((start_x, start_x + width))
            
        # 在随机世界底部添加5格基岩，无论世界高度如何
        for x in range(WORLD_WIDTH):
            for y in range(WORLD_HEIGHT - 5, WORLD_HEIGHT):
                self.blocks[y][x] = BEDROCK

        # 生成基本地形
        for x in range(WORLD_WIDTH):
            surface_y = height_map[x]
            
            # 检查是否在沙漠区域或雨林区域
            is_desert = False
            is_rainforest = False
            for start, end in desert_regions:
                if start <= x <= end:
                    is_desert = True
                    break
            for start, end in rainforest_regions:
                if start <= x <= end:
                    is_rainforest = True
                    break
            
            if is_desert:
                # 沙漠地形使用沙子
                self.blocks[surface_y][x] = SAND
                
                # 沙子层
                for y in range(surface_y + 1, surface_y + 4):
                    if y < WORLD_HEIGHT:
                        self.blocks[y][x] = SAND
                
                # 沙漠下的黑土块层
                for y in range(surface_y + 4, surface_y + 6):
                    if y < WORLD_HEIGHT:
                        self.blocks[y][x] = BLACK_DIRT
            elif is_rainforest:
                # 雨林地形使用雨林专属方块
                self.blocks[surface_y][x] = GRASS  # 雨林地面也是草方块
                
                # 泥土层
                for y in range(surface_y + 1, surface_y + 4):
                    if y < WORLD_HEIGHT:
                        self.blocks[y][x] = DIRT
                
                # 黑土块层
                for y in range(surface_y + 4, surface_y + 6):
                    if y < WORLD_HEIGHT:
                        self.blocks[y][x] = BLACK_DIRT
            else:
                # 普通地形
                self.blocks[surface_y][x] = GRASS
                
                # 泥土层
                for y in range(surface_y + 1, surface_y + 4):
                    if y < WORLD_HEIGHT:
                        self.blocks[y][x] = DIRT
                
                # 黑土块层
                for y in range(surface_y + 4, surface_y + 6):
                    if y < WORLD_HEIGHT:
                        self.blocks[y][x] = BLACK_DIRT

            # 石头层和矿石
            for y in range(surface_y + 6, WORLD_HEIGHT):
                if y < WORLD_HEIGHT:
                    depth = y - surface_y
                    rand = random.random()

                    if depth < 10:
                        if rand < 0.04:
                            self.blocks[y][x] = COPPER_ORE
                        elif rand < 0.06:
                            self.blocks[y][x] = IRON_ORE
                        else:
                            self.blocks[y][x] = STONE
                    elif depth < 20:
                        if rand < 0.015:
                            self.blocks[y][x] = GOLD_ORE
                        elif rand < 0.03:
                            self.blocks[y][x] = IRON_ORE
                        elif rand < 0.06:
                            self.blocks[y][x] = COPPER_ORE
                        else:
                            self.blocks[y][x] = STONE
                    else:
                        if rand < 0.01:
                            self.blocks[y][x] = DIAMOND_ORE
                        elif rand < 0.02:
                            self.blocks[y][x] = GOLD_ORE
                        elif rand < 0.04:
                            self.blocks[y][x] = IRON_ORE
                        elif rand < 0.06:
                            self.blocks[y][x] = COPPER_ORE
                        else:
                            self.blocks[y][x] = STONE

        # 在地面上生成植物
        for x in range(WORLD_WIDTH):
            surface_y = height_map[x]
            surface_block = self.blocks[surface_y][x]
            
            # 检查是否在沙漠区域或雨林区域
            is_desert = False
            is_rainforest = False
            for start, end in desert_regions:
                if start <= x <= end:
                    is_desert = True
                    break
            for start, end in rainforest_regions:
                if start <= x <= end:
                    is_rainforest = True
                    break
            
            # 沙漠区域生成枯草
            if is_desert and surface_block == SAND:
                # 检查上方是否有空间
                if surface_y > 0 and self.blocks[surface_y - 1][x] == AIR:
                    rand = random.random()
                    # 30%的概率生成枯草（沙漠中植物较少）
                    if rand < 0.30:
                        self.blocks[surface_y - 1][x] = DRY_GRASS
            # 雨林区域生成更多的草、花和灌木
            elif is_rainforest and surface_block == GRASS:
                # 检查上方是否有空间
                if surface_y > 0 and self.blocks[surface_y - 1][x] == AIR:
                    rand = random.random()
                    # 雨林中植物更茂密
                    if rand < 0.35:  # 35%的概率生成草
                        self.blocks[surface_y - 1][x] = GRASS_PLANT
                    elif rand < 0.55:  # 20%的概率生成红花
                        self.blocks[surface_y - 1][x] = RED_FLOWER
                    elif rand < 0.65:  # 10%的概率生成灌木
                        self.blocks[surface_y - 1][x] = SHRUB
            # 普通区域生成草和红花
            elif surface_block == GRASS:
                # 检查上方是否有空间
                if surface_y > 0 and self.blocks[surface_y - 1][x] == AIR:
                    rand = random.random()
                    # 草的生成概率大于红花
                    if rand < 0.15:  # 15%的概率生成草
                        self.blocks[surface_y - 1][x] = GRASS_PLANT
                    elif rand < 0.20:  # 5%的概率生成红花
                        self.blocks[surface_y - 1][x] = RED_FLOWER
        
        # 在沙漠区域生成仙人掌
        for x in range(WORLD_WIDTH):
            surface_y = height_map[x]
            
            # 检查是否在沙漠区域
            is_desert = False
            for start, end in desert_regions:
                if start <= x <= end:
                    is_desert = True
                    break
            
            # 沙漠区域生成仙人掌
            if is_desert and self.blocks[surface_y][x] == SAND:
                rand = random.random()
                # 10%的概率生成仙人掌
                if rand < 0.10:
                    # 检查周围是否有空间
                    has_space = True
                    # 随机选择仙人掌高度（1-3格）
                    cactus_height = random.randint(1, 3)
                    
                    for h in range(cactus_height):
                        if surface_y - h - 1 < 0 or self.blocks[surface_y - h - 1][x] != AIR:
                            has_space = False
                            break
                    
                    if has_space:
                        # 放置仙人掌
                        for h in range(cactus_height):
                            self.blocks[surface_y - h - 1][x] = CACTUS
        
        # 生成树木
        # 先处理雨林区域，使用更密集的树木生成方式
        for x in range(20, WORLD_WIDTH - 20):
            # 检查是否在雨林区域
            is_rainforest = False
            for start, end in rainforest_regions:
                if start <= x <= end:
                    is_rainforest = True
                    break
            
            # 雨林区域使用更密集的树木生成逻辑
            if is_rainforest:
                # 检查是否在沙漠区域
                is_desert = False
                for start, end in desert_regions:
                    if start <= x <= end:
                        is_desert = True
                        break
                
                if not is_desert:
                    # 35%概率生成树木，降低雨林密度
                    if random.random() < 0.35:
                        # 随机偏移一些位置，避免树木排列过于整齐
                        offset_x = random.randint(-2, 2)
                        tree_x = x + offset_x
                        if 20 <= tree_x < WORLD_WIDTH - 20:
                            self.generate_rainforest_tree(tree_x, height_map[tree_x])
        
        # 再处理非雨林区域的普通树木生成
        # 降低步长以增加树木分布密度
        for x in range(20, WORLD_WIDTH - 20, random.randint(4, 8)):
            # 检查是否在沙漠区域或雨林区域
            is_desert = False
            is_rainforest = False
            for start, end in desert_regions:
                if start <= x <= end:
                    is_desert = True
                    break
            for start, end in rainforest_regions:
                if start <= x <= end:
                    is_rainforest = True
                    break
            
            # 只在非沙漠、非雨林区域生成普通树木
            if not is_desert and not is_rainforest:
                # 检查是否为草原地形（+-3起伏）
                is_grassland = True
                # 检查当前位置周围的地形起伏
                for dx in range(-5, 6):
                    check_x = x + dx
                    if 0 <= check_x < WORLD_WIDTH:
                        # 计算与当前位置的高度差
                        height_diff = abs(height_map[check_x] - height_map[x])
                        if height_diff > 3:
                            is_grassland = False
                            break
                
                # 草原地形（+-3起伏）几乎没有树木
                if is_grassland:
                    # 草原地形生成树木概率降低到5%
                    if random.random() < 0.05:
                        self.generate_tree(x, height_map[x])
                else:
                    # 普通区域生成普通树木（60%概率）
                    if random.random() < 0.6:
                        self.generate_tree(x, height_map[x])

        # 生成洞穴
        for y in range(20, WORLD_HEIGHT - 10):
            for x in range(10, WORLD_WIDTH - 10):
                if self.blocks[y][x] in [STONE, IRON_ORE, GOLD_ORE, DIAMOND_ORE, COPPER_ORE]:
                    noise_val = (math.sin(x * 0.1) + math.sin(y * 0.1) +
                                 math.sin((x + y) * 0.05)) / 3
                    if noise_val > 0.2:
                        self.blocks[y][x] = AIR

        # 生成水体
        for x in range(50, WORLD_WIDTH - 50, 30):
            if random.random() < 0.4:
                lake_width = random.randint(5, 12)
                for lx in range(x, min(x + lake_width, WORLD_WIDTH - 1)):
                    surface_y = height_map[lx]
                    for ly in range(surface_y + 1, min(surface_y + 3, WORLD_HEIGHT - 1)):
                        self.blocks[ly][lx] = WATER

        # 生成岩浆池
        for x in range(100, WORLD_WIDTH - 100, 50):
            if random.random() < 0.2:
                lake_width = random.randint(3, 8)
                for lx in range(x, min(x + lake_width, WORLD_WIDTH - 1)):
                    surface_y = height_map[lx] + random.randint(5, 15)
                    if surface_y < WORLD_HEIGHT - 5:
                        for ly in range(surface_y, min(surface_y + 2, WORLD_HEIGHT - 1)):
                            self.blocks[ly][lx] = LAVA
                            # 在岩浆周围添加岩石_底方块
                            for dy in [-1, 0, 1]:
                                for dx in [-1, 0, 1]:
                                    if dx != 0 or dy != 0:
                                        nx, ny = lx + dx, ly + dy
                                        if 0 <= nx < WORLD_WIDTH and 0 <= ny < WORLD_HEIGHT:
                                            # 只替换普通岩石方块，不替换其他方块
                                            if self.blocks[ny][nx] == STONE:
                                                self.blocks[ny][nx] = STONE_BOTTOM

        # 生成箱子
        for _ in range(15):
            x = random.randint(50, WORLD_WIDTH - 50)
            y = height_map[x] - 1
            if 0 <= y < WORLD_HEIGHT and self.blocks[y][x] == AIR:
                self.blocks[y][x] = CHEST
                self.chests.append(Chest(x * TILE_SIZE, y * TILE_SIZE))
            
    def generate_random_terrain(self):
        """生成随机地形"""
        # 创建高度图
        height_map = [0] * WORLD_WIDTH
        for x in range(WORLD_WIDTH):
            # 使用正弦函数创建地形起伏，根据WORLD_WIDTH调整系数以适应超大地图
            height = 80 + int(math.sin(x * 0.005) * 12 +  # 减小系数以增加波长，使长距离地形变化更平缓
                              math.sin(x * 0.02) * 6 +  # 中等波长提供中等距离变化
                              math.sin(x * 0.1) * 3 +  # 保持短距离变化
                              random.uniform(-2, 2))  # 增加随机偏移以增加地形多样性
            height = max(50, min(height, WORLD_HEIGHT - 30))
            height_map[x] = height
        
        # 添加高山地形
        # 根据地图宽度动态调整高山区域数量
        mountain_count = max(2, WORLD_WIDTH // 1000)  # 每1000宽至少1个高山区域
        mountain_regions = []
        
        for _ in range(mountain_count):
            # 随机选择高山区域的起始位置
            start_x = random.randint(100, WORLD_WIDTH - 300)
            # 随机选择高山区域的宽度
            width = random.randint(150, 250)
            # 随机选择高山的高度峰值（比普通地形高20-40格）
            peak_height = random.randint(40, 60)
            
            mountain_regions.append((start_x, start_x + width))
            
            # 生成高山地形
            for x in range(start_x, start_x + width):
                if 0 <= x < WORLD_WIDTH:
                    # 使用二次函数创建山峰形状（更自然的山体轮廓）
                    distance_from_center = abs(x - (start_x + width // 2))
                    # 距离中心越远，高度越低，使用指数衰减以获得更陡峭的山峰
                    mountain_factor = math.exp(-distance_from_center / (width * 0.3))
                    # 计算山峰高度
                    mountain_height = int(peak_height * mountain_factor)
                    # 确保高山不会超出世界高度
                    new_height = max(50, min(height_map[x] - mountain_height, WORLD_HEIGHT - 30))
                    height_map[x] = new_height
        
        # 添加草原地形（±3起伏）
        # 根据地图宽度动态调整草原区域数量
        grassland_count = max(3, WORLD_WIDTH // 800)  # 每800宽至少1个草原区域
        grassland_regions = []
        
        for _ in range(grassland_count):
            # 随机选择草原区域的起始位置
            start_x = random.randint(100, WORLD_WIDTH - 400)
            # 随机选择草原区域的宽度
            width = random.randint(200, 400)
            
            # 检查是否与高山、沙漠区域重叠
            overlapping = False
            min_distance = 100  # 与其他地形保持最小距离
            
            # 检查是否与高山重叠
            for (m_start, m_end) in mountain_regions:
                if not (start_x + width + min_distance < m_start or start_x - min_distance > m_end):
                    overlapping = True
                    break
            
            if not overlapping:
                grassland_regions.append((start_x, start_x + width))
        
        # 如果草原区域数量不足，强制创建更多
        min_required_grasslands = max(1, grassland_count // 2)  # 至少需要一半的草原区域
        while len(grassland_regions) < min_required_grasslands:
            width = random.randint(150, 300)  # 使用较小的宽度增加成功概率
            start_x = random.randint(50, WORLD_WIDTH - width - 50)
            grassland_regions.append((start_x, start_x + width))
        
        # 应用草原地形的±3起伏限制
        for (g_start, g_end) in grassland_regions:
            # 计算草原区域的平均高度
            total_height = 0
            count = 0
            for x in range(g_start, g_end):
                if 0 <= x < WORLD_WIDTH:
                    total_height += height_map[x]
                    count += 1
            if count > 0:
                avg_height = total_height // count
                
                # 对草原区域应用±3起伏限制
                for x in range(g_start, g_end):
                    if 0 <= x < WORLD_WIDTH:
                        # 限制高度在平均高度±3范围内
                        height_map[x] = max(avg_height - 3, min(height_map[x], avg_height + 3))
        
        # 添加地形平滑处理，但保留更多短距离变化
        # 创建临时数组存储平滑后的高度
        smoothed_heights = [0] * WORLD_WIDTH
        
        # 第一个和最后一个点保持不变
        smoothed_heights[0] = height_map[0]
        smoothed_heights[WORLD_WIDTH - 1] = height_map[WORLD_WIDTH - 1]
        
        # 对中间点进行平滑处理（使用3点加权平均滤波）
        for x in range(1, WORLD_WIDTH - 1):
            # 当前点权重更高，保留更多短距离特征
            smoothed_heights[x] = int((height_map[x-1] * 0.2 + height_map[x] * 0.6 + height_map[x+1] * 0.2))
            
        # 减少一次平滑处理，保留更多原始地形特征
        # 仅对长距离不规则性进行一次额外平滑
        
        # 将平滑后的高度赋值回高度图
        for x in range(WORLD_WIDTH):
            height_map[x] = smoothed_heights[x]
        
        # 标记沙漠区域和雨林区域
        desert_regions = []
        rainforest_regions = []
        
        # 根据地图宽度动态调整沙漠数量
        desert_count = max(3, WORLD_WIDTH // 2000)  # 每2000宽至少1个沙漠区域
        for _ in range(desert_count):  # 创建多个沙漠区域
            start_x = random.randint(100, WORLD_WIDTH - 400)  # 确保有足够空间
            width = random.randint(200, 500)  # 增加沙漠宽度范围
            desert_regions.append((start_x, start_x + width))
        
        # 添加雨林区域
        # 增加雨林区域数量以提高出现概率
        rainforest_count = max(2, WORLD_WIDTH // 1500)  # 每1500宽至少2个雨林区域
        for _ in range(rainforest_count):  # 创建雨林区域
            # 调整宽度和起始位置，适应较小的世界
            width = random.randint(120, 200)  # 减小宽度范围，增加成功创建概率
            start_x = random.randint(50, WORLD_WIDTH - width - 50)  # 确保有足够空间
            
            # 检查是否与沙漠区域重叠，但允许部分重叠以增加雨林出现概率
            overlapping = False
            min_distance = 50  # 允许与沙漠区域保持最小距离
            for (d_start, d_end) in desert_regions:
                if not (start_x + width + min_distance < d_start or start_x - min_distance > d_end):
                    overlapping = True
                    break
            
            # 如果不重叠或者尝试次数较多，就添加这个雨林区域
            if not overlapping or len(rainforest_regions) < max(1, rainforest_count // 2):
                rainforest_regions.append((start_x, start_x + width))
        
        # 如果雨林区域数量不足，强制创建更多的雨林区域
        min_required_rainforests = max(1, rainforest_count // 2)  # 至少需要一半的雨林区域
        while len(rainforest_regions) < min_required_rainforests:
            width = random.randint(100, 180)  # 使用较小的宽度增加成功概率
            start_x = random.randint(50, WORLD_WIDTH - width - 50)
            # 不检查重叠，直接添加，确保至少有足够的雨林区域
            rainforest_regions.append((start_x, start_x + width))
            
        # 在世界底部生成基岩层，防止玩家掉下去
        for x in range(WORLD_WIDTH):
            for y in range(WORLD_HEIGHT - 3, WORLD_HEIGHT):
                self.blocks[y][x] = BEDROCK

        # 生成基本地形
        for x in range(WORLD_WIDTH):
            surface_y = height_map[x]
            
            # 检查是否在沙漠区域或雨林区域
            is_desert = False
            is_rainforest = False
            for start, end in desert_regions:
                if start <= x <= end:
                    is_desert = True
                    break
            for start, end in rainforest_regions:
                if start <= x <= end:
                    is_rainforest = True
                    break
            
            if is_desert:
                # 沙漠地形使用沙子
                self.blocks[surface_y][x] = SAND
                
                # 沙子层
                for y in range(surface_y + 1, surface_y + 4):
                    if y < WORLD_HEIGHT:
                        self.blocks[y][x] = SAND
                
                # 沙漠下的黑土块层
                for y in range(surface_y + 4, surface_y + 6):
                    if y < WORLD_HEIGHT:
                        self.blocks[y][x] = BLACK_DIRT
            elif is_rainforest:
                # 雨林地形使用雨林专属方块
                self.blocks[surface_y][x] = GRASS  # 雨林地面也是草方块
                
                # 泥土层
                for y in range(surface_y + 1, surface_y + 4):
                    if y < WORLD_HEIGHT:
                        self.blocks[y][x] = DIRT
                
                # 黑土块层
                for y in range(surface_y + 4, surface_y + 6):
                    if y < WORLD_HEIGHT:
                        self.blocks[y][x] = BLACK_DIRT
            else:
                # 普通地形
                self.blocks[surface_y][x] = GRASS
                
                # 泥土层
                for y in range(surface_y + 1, surface_y + 4):
                    if y < WORLD_HEIGHT:
                        self.blocks[y][x] = DIRT
                
                # 黑土块层
                for y in range(surface_y + 4, surface_y + 6):
                    if y < WORLD_HEIGHT:
                        self.blocks[y][x] = BLACK_DIRT

            # 石头层和矿石
            for y in range(surface_y + 6, WORLD_HEIGHT):
                if y < WORLD_HEIGHT:
                    depth = y - surface_y
                    rand = random.random()

                    if depth < 10:
                        if rand < 0.04:
                            self.blocks[y][x] = COPPER_ORE
                        elif rand < 0.06:
                            self.blocks[y][x] = IRON_ORE
                        else:
                            self.blocks[y][x] = STONE
                    elif depth < 20:
                        if rand < 0.015:
                            self.blocks[y][x] = GOLD_ORE
                        elif rand < 0.03:
                            self.blocks[y][x] = IRON_ORE
                        elif rand < 0.06:
                            self.blocks[y][x] = COPPER_ORE
                        else:
                            self.blocks[y][x] = STONE
                    else:
                        if rand < 0.01:
                            self.blocks[y][x] = DIAMOND_ORE
                        elif rand < 0.02:
                            self.blocks[y][x] = GOLD_ORE
                        elif rand < 0.04:
                            self.blocks[y][x] = IRON_ORE
                        elif rand < 0.06:
                            self.blocks[y][x] = COPPER_ORE
                        else:
                            self.blocks[y][x] = STONE

        # 在地面上生成植物
        for x in range(WORLD_WIDTH):
            surface_y = height_map[x]
            surface_block = self.blocks[surface_y][x]
            
            # 检查是否在沙漠区域或雨林区域
            is_desert = False
            is_rainforest = False
            for start, end in desert_regions:
                if start <= x <= end:
                    is_desert = True
                    break
            for start, end in rainforest_regions:
                if start <= x <= end:
                    is_rainforest = True
                    break
            
            # 沙漠区域生成枯草
            if is_desert and surface_block == SAND:
                # 检查上方是否有空间
                if surface_y > 0 and self.blocks[surface_y - 1][x] == AIR:
                    rand = random.random()
                    # 30%的概率生成枯草（沙漠中植物较少）
                    if rand < 0.30:
                        self.blocks[surface_y - 1][x] = DRY_GRASS
            # 雨林区域生成更多的草、花和灌木
            elif is_rainforest and surface_block == GRASS:
                # 检查上方是否有空间
                if surface_y > 0 and self.blocks[surface_y - 1][x] == AIR:
                    rand = random.random()
                    # 雨林中植物更茂密
                    if rand < 0.35:  # 35%的概率生成草
                        self.blocks[surface_y - 1][x] = GRASS_PLANT
                    elif rand < 0.55:  # 20%的概率生成红花
                        self.blocks[surface_y - 1][x] = RED_FLOWER
                    elif rand < 0.65:  # 10%的概率生成灌木
                        self.blocks[surface_y - 1][x] = SHRUB
            # 普通区域生成草和红花
            elif surface_block == GRASS:
                # 检查上方是否有空间
                if surface_y > 0 and self.blocks[surface_y - 1][x] == AIR:
                    rand = random.random()
                    # 草的生成概率大于红花
                    if rand < 0.15:  # 15%的概率生成草
                        self.blocks[surface_y - 1][x] = GRASS_PLANT
                    elif rand < 0.20:  # 5%的概率生成红花
                        self.blocks[surface_y - 1][x] = RED_FLOWER
        
        # 在沙漠区域生成仙人掌
        for x in range(WORLD_WIDTH):
            surface_y = height_map[x]
            
            # 检查是否在沙漠区域
            is_desert = False
            for start, end in desert_regions:
                if start <= x <= end:
                    is_desert = True
                    break
            
            # 沙漠区域生成仙人掌
            if is_desert and self.blocks[surface_y][x] == SAND:
                rand = random.random()
                # 10%的概率生成仙人掌
                if rand < 0.10:
                    # 检查周围是否有空间
                    has_space = True
                    # 随机选择仙人掌高度（1-3格）
                    cactus_height = random.randint(1, 3)
                    
                    for h in range(cactus_height):
                        if surface_y - h - 1 < 0 or self.blocks[surface_y - h - 1][x] != AIR:
                            has_space = False
                            break
                    
                    if has_space:
                        # 放置仙人掌
                        for h in range(cactus_height):
                            self.blocks[surface_y - h - 1][x] = CACTUS
        
        # 生成树木
        # 先处理雨林区域，使用更密集的树木生成方式
        for x in range(20, WORLD_WIDTH - 20):
            # 检查是否在雨林区域
            is_rainforest = False
            for start, end in rainforest_regions:
                if start <= x <= end:
                    is_rainforest = True
                    break
            
            # 雨林区域使用更密集的树木生成逻辑
            if is_rainforest:
                # 检查是否在沙漠区域
                is_desert = False
                for start, end in desert_regions:
                    if start <= x <= end:
                        is_desert = True
                        break
                
                if not is_desert:
                    # 35%概率生成树木，降低雨林密度
                    if random.random() < 0.35:
                        # 随机偏移一些位置，避免树木排列过于整齐
                        offset_x = random.randint(-2, 2)
                        tree_x = x + offset_x
                        if 20 <= tree_x < WORLD_WIDTH - 20:
                            self.generate_rainforest_tree(tree_x, height_map[tree_x])
        
        # 再处理非雨林区域的普通树木生成
        # 降低步长以增加树木分布密度
        for x in range(20, WORLD_WIDTH - 20, random.randint(4, 8)):
            # 检查是否在沙漠区域或雨林区域
            is_desert = False
            is_rainforest = False
            for start, end in desert_regions:
                if start <= x <= end:
                    is_desert = True
                    break
            for start, end in rainforest_regions:
                if start <= x <= end:
                    is_rainforest = True
                    break
            
            # 只在非沙漠、非雨林区域生成普通树木
            if not is_desert and not is_rainforest:
                # 检查是否为草原地形（+-3起伏）
                is_grassland = True
                # 检查当前位置周围的地形起伏
                for dx in range(-5, 6):
                    check_x = x + dx
                    if 0 <= check_x < WORLD_WIDTH:
                        # 计算与当前位置的高度差
                        height_diff = abs(height_map[check_x] - height_map[x])
                        if height_diff > 3:
                            is_grassland = False
                            break
                
                # 草原地形（+-3起伏）几乎没有树木
                if is_grassland:
                    # 草原地形生成树木概率降低到5%
                    if random.random() < 0.05:
                        self.generate_tree(x, height_map[x])
                else:
                    # 普通区域生成普通树木（60%概率）
                    if random.random() < 0.6:
                        self.generate_tree(x, height_map[x])

        # 生成洞穴
        for y in range(20, WORLD_HEIGHT - 10):
            for x in range(10, WORLD_WIDTH - 10):
                if self.blocks[y][x] in [STONE, IRON_ORE, GOLD_ORE, DIAMOND_ORE, COPPER_ORE]:
                    noise_val = (math.sin(x * 0.1) + math.sin(y * 0.1) +
                                 math.sin((x + y) * 0.05)) / 3
                    if noise_val > 0.2:
                        self.blocks[y][x] = AIR

        # 生成水体
        for x in range(50, WORLD_WIDTH - 50, 30):
            if random.random() < 0.4:
                lake_width = random.randint(5, 12)
                for lx in range(x, min(x + lake_width, WORLD_WIDTH - 1)):
                    surface_y = height_map[lx]
                    for ly in range(surface_y + 1, min(surface_y + 3, WORLD_HEIGHT - 1)):
                        self.blocks[ly][lx] = WATER

        # 生成岩浆池
        for x in range(100, WORLD_WIDTH - 100, 50):
            if random.random() < 0.2:
                lake_width = random.randint(3, 8)
                for lx in range(x, min(x + lake_width, WORLD_WIDTH - 1)):
                    surface_y = height_map[lx] + random.randint(5, 15)
                    if surface_y < WORLD_HEIGHT - 5:
                        for ly in range(surface_y, min(surface_y + 2, WORLD_HEIGHT - 1)):
                            self.blocks[ly][lx] = LAVA
                            # 在岩浆周围添加岩石_底方块
                            for dy in [-1, 0, 1]:
                                for dx in [-1, 0, 1]:
                                    if dx != 0 or dy != 0:
                                        nx, ny = lx + dx, ly + dy
                                        if 0 <= nx < WORLD_WIDTH and 0 <= ny < WORLD_HEIGHT:
                                            # 只替换普通岩石方块，不替换其他方块
                                            if self.blocks[ny][nx] == STONE:
                                                self.blocks[ny][nx] = STONE_BOTTOM

        # 生成箱子
        for _ in range(15):
            x = random.randint(50, WORLD_WIDTH - 50)
            y = height_map[x] - 1
            if 0 <= y < WORLD_HEIGHT and self.blocks[y][x] == AIR:
                self.blocks[y][x] = CHEST
                self.chests.append(Chest(x * TILE_SIZE, y * TILE_SIZE))

    def generate_tree(self, x, surface_y):
        """生成普通树木"""
        tree_height = random.randint(4, 6)
        # 树干
        for y in range(surface_y - tree_height, surface_y):
            if 0 <= y < WORLD_HEIGHT:
                self.blocks[y][x] = WOOD

        # 树叶
        center_y = surface_y - tree_height
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if abs(dx) + abs(dy) <= 3:
                    nx, ny = x + dx, center_y + dy
                    if 0 <= nx < WORLD_WIDTH and 0 <= ny < WORLD_HEIGHT:
                        if random.random() < 0.8:
                            self.blocks[ny][nx] = LEAF
                             
    def generate_plains_terrain(self):
        """生成平原世界地形，按照固定的层次结构生成"""
        # 定义平原地形的层次结构
        # 从顶部到底部依次是：10草方块, 9土块, 8土块, 7土块, 6黑土块, 5黑土块, 4岩石, 3岩石, 2岩石, 1基岩
        # 注意：索引是从0开始的，所以顶层是索引0，底层是索引WORLD_HEIGHT-1
        
        for x in range(WORLD_WIDTH):
            # 计算每层的y坐标
            # 注意：游戏中的y坐标是从上到下递增的
            grass_level = WORLD_HEIGHT - 10  # 草方块层
            dirt_level1 = WORLD_HEIGHT - 9   # 第一层土块
            dirt_level2 = WORLD_HEIGHT - 8   # 第二层土块
            dirt_level3 = WORLD_HEIGHT - 7   # 第三层土块
            black_dirt_level1 = WORLD_HEIGHT - 6  # 第一层黑土块
            black_dirt_level2 = WORLD_HEIGHT - 5  # 第二层黑土块
            stone_level1 = WORLD_HEIGHT - 4   # 第一层岩石
            stone_level2 = WORLD_HEIGHT - 3   # 第二层岩石
            stone_level3 = WORLD_HEIGHT - 2   # 第三层岩石
            bedrock_level = WORLD_HEIGHT - 1  # 基岩层
            
            # 设置各层方块
            # 草方块层以上的空间保持为空
            for y in range(grass_level):
                if 0 <= y < WORLD_HEIGHT:
                    self.blocks[y][x] = AIR
                    
            # 草方块层
            if 0 <= grass_level < WORLD_HEIGHT:
                self.blocks[grass_level][x] = GRASS
                
            # 土块层
            if 0 <= dirt_level1 < WORLD_HEIGHT:
                self.blocks[dirt_level1][x] = DIRT
            if 0 <= dirt_level2 < WORLD_HEIGHT:
                self.blocks[dirt_level2][x] = DIRT
            if 0 <= dirt_level3 < WORLD_HEIGHT:
                self.blocks[dirt_level3][x] = DIRT
                
            # 黑土块层
            if 0 <= black_dirt_level1 < WORLD_HEIGHT:
                self.blocks[black_dirt_level1][x] = BLACK_DIRT
            if 0 <= black_dirt_level2 < WORLD_HEIGHT:
                self.blocks[black_dirt_level2][x] = BLACK_DIRT
                
            # 岩石层
            if 0 <= stone_level1 < WORLD_HEIGHT:
                self.blocks[stone_level1][x] = STONE
            if 0 <= stone_level2 < WORLD_HEIGHT:
                self.blocks[stone_level2][x] = STONE
            if 0 <= stone_level3 < WORLD_HEIGHT:
                self.blocks[stone_level3][x] = STONE
                
            # 基岩层
            if 0 <= bedrock_level < WORLD_HEIGHT:
                self.blocks[bedrock_level][x] = BEDROCK
            
        # 在平原世界生成少量的草和花
        for x in range(WORLD_WIDTH):
            surface_y = WORLD_HEIGHT - 10  # 草方块层
            
            # 检查上方是否有空间
            if surface_y > 0 and self.blocks[surface_y - 1][x] == AIR:
                rand = random.random()
                # 20%的概率生成草
                if rand < 0.20:
                    self.blocks[surface_y - 1][x] = GRASS_PLANT
                # 5%的概率生成红花
                elif rand < 0.25:
                    self.blocks[surface_y - 1][x] = RED_FLOWER
                    
        # 在平原世界生成少量树木
        for x in range(50, WORLD_WIDTH - 50, 100):
            if random.random() < 0.3:
                self.generate_tree(x, WORLD_HEIGHT - 10)
                
        # 在平原世界生成少量水体
        for x in range(100, WORLD_WIDTH - 100, 200):
            if random.random() < 0.15:
                lake_width = random.randint(10, 20)
                for lx in range(x, min(x + lake_width, WORLD_WIDTH - 1)):
                    surface_y = WORLD_HEIGHT - 9  # 略低于草方块层
                    for ly in range(surface_y, min(surface_y + 3, WORLD_HEIGHT - 1)):
                        self.blocks[ly][lx] = WATER
                        
        # 生成少量箱子
        for _ in range(5):
            x = random.randint(100, WORLD_WIDTH - 100)
            y = WORLD_HEIGHT - 11  # 放在草方块上方
            if 0 <= y < WORLD_HEIGHT:
                self.blocks[y][x] = CHEST
                self.chests.append(Chest(x * TILE_SIZE, y * TILE_SIZE))
                
    def generate_rainforest_tree(self, x, surface_y):
        """生成雨林树木，使用乔木和乔木叶方块，并随机生成乔木果"""
        # 减小树干体积以提高生成成功率
        # 随机确定树干宽度（3-8）
        trunk_width = random.randint(3, 8)
        # 随机确定树干高度（8-12）
        tree_height = random.randint(8, 12)
        
        # 检查树干周围是否有足够空间
        has_space = True
        for y in range(surface_y - tree_height, surface_y):
            for wx in range(x - trunk_width // 2, x + trunk_width // 2 + 1):
                if wx < 0 or wx >= WORLD_WIDTH or y < 0 or y >= WORLD_HEIGHT:
                    has_space = False
                    break
                # 允许覆盖小型植物（草、花、灌木），只排除固体方块
                if (self.blocks[y][wx] != AIR and 
                    not (y == surface_y and self.blocks[y][wx] in [GRASS, DIRT, SAND]) and
                    not self.blocks[y][wx] in [GRASS_PLANT, RED_FLOWER, SHRUB]):
                    has_space = False
                    break
            if not has_space:
                break
        
        # 添加强制生成机制，即使空间不足也有20%概率尝试放置
        if has_space or random.random() < 0.2:
            # 生成宽树干（使用乔木方块）
            for y in range(surface_y - tree_height, surface_y):
                for wx in range(x - trunk_width // 2, x + trunk_width // 2 + 1):
                    if 0 <= y < WORLD_HEIGHT and 0 <= wx < WORLD_WIDTH:
                        self.blocks[y][wx] = JUNGLE_TREE
            
            # 生成树叶（使用乔木叶方块）和乔木果
            center_y = surface_y - tree_height
            leaf_radius = trunk_width + 2  # 树叶半径根据树干宽度调整
            for dy in range(-leaf_radius, leaf_radius + 1):
                for dx in range(-leaf_radius, leaf_radius + 1):
                    distance = math.sqrt(dx * dx + dy * dy)
                    # 树叶分布更密集，使用圆形分布
                    if distance <= leaf_radius + 1:
                        nx, ny = x + dx, center_y + dy
                        if 0 <= nx < WORLD_WIDTH and 0 <= ny < WORLD_HEIGHT:
                            # 确保树叶不会覆盖树干顶部
                            if not (ny >= surface_y - tree_height + 2 and abs(nx - x) <= trunk_width // 2):
                                # 树叶生成概率更高（90%）
                                if random.random() < 0.9:
                                    # 3%的概率在树叶位置生成乔木果（大量减少乔木果数量）
                                    if random.random() < 0.03:
                                        self.blocks[ny][nx] = JUNGLE_FRUIT
                                    else:
                                        self.blocks[ny][nx] = JUNGLE_LEAF

    def update_liquids(self, dt, camera_x, camera_y):
        """更新液体物理（水和岩浆）"""
        # 更新岩浆烧毁计时器
        self.lava_burn_timer += dt
        
        # 初始化液体计时器（如果不存在）
        if not hasattr(self, 'water_timer'):
            self.water_timer = 0
            self.lava_timer = 0
            
        # 更新液体计时器
        self.water_timer += dt
        self.lava_timer += dt
        
        # 复制当前方块状态以避免更新影响
        new_blocks = [row.copy() for row in self.blocks]

        # 计算活跃区域的范围（玩家可见区域加上一些缓冲区）
        buffer = 10  # 增加缓冲区以保证物理效果正常
        active_start_x = max(0, int(camera_x // TILE_SIZE) - buffer)
        active_end_x = min(WORLD_WIDTH, int((camera_x + WIDTH) // TILE_SIZE) + buffer + 1)
        active_start_y = max(0, int(camera_y // TILE_SIZE) - buffer)
        active_end_y = min(WORLD_HEIGHT, int((camera_y + HEIGHT) // TILE_SIZE) + buffer + 1)

        # 从下往上处理液体，模拟重力
        for y in range(active_end_y - 1, active_start_y - 1, -1):
            for x in range(active_start_x, active_end_x):
                current_block = self.blocks[y][x]

                # 处理水（每0.1秒流动一次）
                if current_block == WATER and self.water_timer >= 0.1:
                    # 水向下流动 - 可以流入空气或岩石_底方块
                    if self.blocks[y + 1][x] == AIR or self.blocks[y + 1][x] == STONE_BOTTOM:
                        # 10%概率保留原位置（仅下降时）
                        if random.random() < 0.1:
                            new_blocks[y + 1][x] = WATER  # 不清除原位置
                        else:
                            new_blocks[y][x] = AIR
                            new_blocks[y + 1][x] = WATER
                    else:
                        # 水向两侧流动（确保不会悬空）
                        flow_directions = []
                        if x > 0 and (self.blocks[y][x - 1] == AIR or self.blocks[y][x - 1] == STONE_BOTTOM):
                            flow_directions.append(-1)
                        if x < WORLD_WIDTH - 1 and (self.blocks[y][x + 1] == AIR or self.blocks[y][x + 1] == STONE_BOTTOM):
                            flow_directions.append(1)

                        if flow_directions:
                            # 随机选择一个方向流动
                            dir = random.choice(flow_directions)
                            # 90%概率清除原来的位置
                            if random.random() < 0.9:
                                new_blocks[y][x] = AIR  # 清除原来的位置
                            new_blocks[y][x + dir] = WATER

                # 处理岩浆（每0.2秒流动一次）
                elif current_block == LAVA and self.lava_timer >= 0.2:
                    # 岩浆向下流动 - 可以流入空气或岩石_底方块
                    if self.blocks[y + 1][x] == AIR or self.blocks[y + 1][x] == STONE_BOTTOM:
                        # 10%概率保留原位置（仅下降时）
                        if random.random() < 0.1:
                            new_blocks[y + 1][x] = LAVA  # 不清除原位置
                        else:
                            new_blocks[y][x] = AIR
                            new_blocks[y + 1][x] = LAVA
                    else:
                        # 岩浆向两侧流动（确保不会悬空）
                        if random.random() < 0.3:  # 30%概率向侧面流动
                            flow_directions = []
                            if x > 0 and (self.blocks[y][x - 1] == AIR or self.blocks[y][x - 1] == STONE_BOTTOM):
                                flow_directions.append(-1)
                            if x < WORLD_WIDTH - 1 and (self.blocks[y][x + 1] == AIR or self.blocks[y][x + 1] == STONE_BOTTOM):
                                flow_directions.append(1)

                            if flow_directions:
                                dir = random.choice(flow_directions)
                                # 90%概率清除原来的位置
                                if random.random() < 0.9:
                                    new_blocks[y][x] = AIR  # 清除原来的位置
                                new_blocks[y][x + dir] = LAVA

        # 检查岩浆和水接触，生成石头
        for y in range(active_start_y, active_end_y):
            for x in range(active_start_x, active_end_x):
                current_block = self.blocks[y][x]
                if current_block == WATER:
                    # 检查上下左右是否有岩浆
                    directions = [(0, 1), (1, 0), (-1, 0)]
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < WORLD_WIDTH and 0 <= ny < WORLD_HEIGHT:
                            if self.blocks[ny][nx] == LAVA:
                                new_blocks[y][x] = AIR
                                new_blocks[ny][nx] = STONE
                elif current_block == LAVA:
                    # 检查上下左右是否有水
                    directions = [(0, 1), (1, 0), (-1, 0)]
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < WORLD_WIDTH and 0 <= ny < WORLD_HEIGHT:
                            if self.blocks[ny][nx] == WATER:
                                new_blocks[y][x] = AIR
                                new_blocks[ny][nx] = STONE
        
        # 岩浆烧毁木头和树叶（带1秒间隔）
        if self.lava_burn_timer >= 1.0:
            self.lava_burn_timer = 0  # 重置计时器
            for y in range(active_start_y, active_end_y):
                for x in range(active_start_x, active_end_x):
                    current_block = self.blocks[y][x]
                    if current_block == LAVA:
                        # 检查上下左右是否有木头、树叶或火把
                        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
                        for dx, dy in directions:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < WORLD_WIDTH and 0 <= ny < WORLD_HEIGHT:
                                neighbor_block = self.blocks[ny][nx]
                                # 岩浆可以破坏所有植物
                                if neighbor_block == WOOD or neighbor_block == WOOD_PLANK or neighbor_block == LEAF or neighbor_block == TORCH or neighbor_block == RED_FLOWER or neighbor_block == GRASS_PLANT or neighbor_block == CACTUS or neighbor_block == DRY_GRASS or neighbor_block == SHRUB or neighbor_block == JUNGLE_TREE or neighbor_block == JUNGLE_LEAF or neighbor_block == JUNGLE_FRUIT:
                                    new_blocks[ny][nx] = LAVA
                                    
            # 水替换火把和植物，并且可以把沙子变成湿沙（暂时用黑土块代替）
            for y in range(active_start_y, active_end_y):
                for x in range(active_start_x, active_end_x):
                    current_block = self.blocks[y][x]
                    if current_block == WATER:
                        # 检查上下左右是否有火把、植物或沙子
                        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
                        for dx, dy in directions:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < WORLD_WIDTH and 0 <= ny < WORLD_HEIGHT:
                                neighbor_block = self.blocks[ny][nx]
                                if neighbor_block == TORCH or neighbor_block == RED_FLOWER or neighbor_block == GRASS_PLANT or neighbor_block == DRY_GRASS or neighbor_block == SHRUB:
                                    new_blocks[ny][nx] = WATER
                                # 水接触沙子变成黑土块（代表湿沙）
                                elif neighbor_block == SAND:
                                    new_blocks[ny][nx] = BLACK_DIRT
            
            # 沙子物理：沙子无法悬空，当下方没有方块时会下落
            # 从下往上处理沙子，避免多次更新
            for y in range(active_end_y - 1, active_start_y - 1, -1):
                for x in range(active_start_x, active_end_x):
                    current_block = self.blocks[y][x]
                    # 检查是否是沙子且下方是空气、水、岩浆、火把、草、花或岩石_底方块
                    if current_block == SAND and y + 1 < WORLD_HEIGHT and self.blocks[y + 1][x] in [AIR, WATER, LAVA, TORCH, RED_FLOWER, GRASS_PLANT, DRY_GRASS, SHRUB, STONE_BOTTOM]:
                        # 沙子会替换火把、花和草
                        new_blocks[y][x] = AIR
                        new_blocks[y + 1][x] = SAND
            
            # 沙子与草的交互：沙子可以覆盖草方块
            for y in range(active_start_y, active_end_y):
                for x in range(active_start_x, active_end_x):
                    current_block = self.blocks[y][x]
                    # 检查是否是沙子且下方是草方块
                    if current_block == SAND and y + 1 < WORLD_HEIGHT and self.blocks[y + 1][x] == GRASS:
                        new_blocks[y + 1][x] = DIRT

            # 枯草物理：枯草无法悬空，当下方没有方块时会消失
            # 从上往下处理枯草
            for y in range(active_start_y, active_end_y):
                for x in range(active_start_x, active_end_x):
                    current_block = self.blocks[y][x]
                    # 检查是否是枯草且下方没有方块支撑
                    if current_block == DRY_GRASS and (y + 1 >= WORLD_HEIGHT or self.blocks[y + 1][x] == AIR):
                        new_blocks[y][x] = AIR

            # 仙人掌物理：仙人掌无法悬空，当下方没有方块支撑时会消失
            # 从上往下处理仙人掌
            for y in range(active_start_y, active_end_y):
                for x in range(active_start_x, active_end_x):
                    current_block = self.blocks[y][x]
                    # 检查是否是仙人掌且下方没有方块支撑
                    if current_block == CACTUS and (y + 1 >= WORLD_HEIGHT or not BLOCKS.get(self.blocks[y + 1][x], {}).get('solid', False)):
                        new_blocks[y][x] = AIR

            # 火把、草和花物理：无法悬空，当下方没有方块支撑时会消失
            # 从上往下处理火把、草和花
            for y in range(active_start_y, active_end_y):
                for x in range(active_start_x, active_end_x):
                    current_block = self.blocks[y][x]
                    # 检查是否是火把、草或花且下方没有方块支撑
                    if current_block in [TORCH, GRASS_PLANT, RED_FLOWER, SHRUB] and (y + 1 >= WORLD_HEIGHT or self.blocks[y + 1][x] == AIR):
                        new_blocks[y][x] = AIR
            
            # 水可以让枯草变成草
            for y in range(active_start_y, active_end_y - 1):
                for x in range(active_start_x, active_end_x):
                    current_block = self.blocks[y][x]
                    # 检查是否是水且上方或周围有枯草
                    if current_block == WATER:
                        directions = [(0, -1), (1, 0), (-1, 0), (0, 1)]
                        for dx, dy in directions:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < WORLD_WIDTH and 0 <= ny < WORLD_HEIGHT and self.blocks[ny][nx] == DRY_GRASS:
                                # 检查下方是否是支撑方块
                                if ny + 1 < WORLD_HEIGHT and BLOCKS.get(self.blocks[ny + 1][nx], {}).get('solid', False):
                                    # 20%概率将枯草变成草
                                    if random.random() < 0.2:
                                        new_blocks[ny][nx] = GRASS_PLANT

        self.blocks = new_blocks
        
        # 重置液体计时器
        if self.water_timer >= 0.1:
            self.water_timer = 0
        if self.lava_timer >= 0.2:
            self.lava_timer = 0

    def update_time(self, dt):
        """更新时间，设置为240秒一天"""
        self.time_of_day = (self.time_of_day + dt * 10) % 2400

    def get_sky_color(self):
        """获取天空颜色（随时间变化和天气变化）"""
        # 如果正在下雨，返回灰色天空
        if self.is_raining:
            return RAIN_GRAY
        # 否则根据时间返回相应的天空颜色
        if 600 < self.time_of_day < 1800:
            return SKY_DAY
        elif 500 < self.time_of_day < 700 or 1700 < self.time_of_day < 1900:
            return SUNSET_ORANGE
        else:
            return SKY_NIGHT

    def is_within_bounds(self, x, y):
        """检查坐标是否在世界范围内"""
        return 0 <= x < WORLD_WIDTH and 0 <= y < WORLD_HEIGHT

    def get_block(self, x, y):
        """获取指定位置的方块"""
        if self.is_within_bounds(x, y):
            return self.blocks[y][x]
        return None

    def set_block(self, x, y, block_id):
        """设置指定位置的方块"""
        if self.is_within_bounds(x, y):
            self.blocks[y][x] = block_id
            return True
        return False

    def remove_block(self, x, y):
        """移除指定位置的方块（设为空气）"""
        if self.is_within_bounds(x, y):
            block_id = self.blocks[y][x]
            self.blocks[y][x] = AIR
            return block_id
        return None

    def can_place_block(self, x, y):
        """检查是否可以放置方块"""
        return self.is_within_bounds(x, y) and self.blocks[y][x] in [AIR, WATER, LAVA]

    def screen_to_tile(self, screen_x, screen_y, camera_x, camera_y):
        """将屏幕坐标转换为格子坐标"""
        world_x = screen_x + camera_x
        world_y = screen_y + camera_y
        return int(world_x // TILE_SIZE), int(world_y // TILE_SIZE)

    def draw(self, screen, camera_x, camera_y):
        """绘制世界"""
        # 绘制渐变天空
        sky_color = self.get_sky_color()
        for y in range(HEIGHT):
            # 创建渐变效果 - 从顶部到底部变化
            r = int(sky_color[0] * (1 - y/HEIGHT * 0.3))
            g = int(sky_color[1] * (1 - y/HEIGHT * 0.3))
            b = int(sky_color[2] * (1 - y/HEIGHT * 0.3))
            # 确保颜色值在有效范围内
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            # 绘制水平线
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

        # 绘制太阳/月亮
        if 600 < self.time_of_day < 1800:
            sun_pos = (self.time_of_day - 600) / 1200 * WIDTH
            pygame.draw.circle(screen, (255, 255, 0), (sun_pos, 100), 30)
        else:
            moon_pos = ((self.time_of_day + 600) % 2400) / 2400 * WIDTH
            pygame.draw.circle(screen, (200, 200, 200), (moon_pos, 100), 25)

        # 计算可见区域的格子范围
        start_x = max(0, int(camera_x // TILE_SIZE))
        end_x = min(WORLD_WIDTH, int((camera_x + WIDTH) // TILE_SIZE) + 2)
        start_y = max(0, int(camera_y // TILE_SIZE))
        end_y = min(WORLD_HEIGHT, int((camera_y + HEIGHT) // TILE_SIZE) + 2)

        # 绘制方块
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                block_id = self.blocks[y][x]
                if block_id != AIR:
                    block_info = BLOCKS[block_id]
                    screen_x = x * TILE_SIZE - camera_x
                    screen_y = y * TILE_SIZE - camera_y
                    rect = (screen_x, screen_y, TILE_SIZE, TILE_SIZE)

                    # 绘制方块纹理
                    if block_info["texture"] in self.image_loader.images:
                        screen.blit(self.image_loader.images[block_info["texture"]], rect)
                    else:
                        # 使用颜色块替代
                        if block_id in [WATER, LAVA]:
                            # 半透明液体
                            s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                            s.fill(block_info["color"])
                            screen.blit(s, rect)
                        else:
                            pygame.draw.rect(screen, block_info["color"], rect)

                    # 绘制方块边框
                    if block_info["solid"]:
                        pygame.draw.rect(screen, (0, 0, 0), rect, 1)

        # 绘制箱子
        for chest in self.chests:
            # 只有当箱子对应的方块位置不是空气时才渲染箱子
            if 0 <= chest.tile_y < len(self.blocks) and 0 <= chest.tile_x < len(self.blocks[0]):
                if self.blocks[chest.tile_y][chest.tile_x] != AIR:
                    chest.draw(screen, camera_x, camera_y, self.image_loader.images)


class CraftingSystem:
    """合成系统，处理物品合成"""

    def __init__(self):
        self.recipes = self.init_recipes()

    def init_recipes(self):
        """初始化合成配方"""
        return [
            # 木头合成木板
            {
                "name": "木板",
                "inputs": [{"item_id": WOOD, "quantity": 1}],
                "output": {"item_id": WOOD_PLANK, "quantity": 4}
            },
            # 木剑
            {
                "name": "木剑",
                "inputs": [{"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": WOOD_SWORD, "quantity": 1}
            },
            # 木镐
            {
                "name": "木镐",
                "inputs": [{"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": WOOD_PICKAXE, "quantity": 1}
            },
            # 木斧
            {
                "name": "木斧",
                "inputs": [{"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": WOOD_AXE, "quantity": 1}
            },
            # 木铲
            {
                "name": "木铲",
                "inputs": [{"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": WOOD_SHOVEL, "quantity": 1}
            },
            # 石剑
            {
                "name": "石剑",
                "inputs": [{"item_id": STONE, "quantity": 1}, {"item_id": WOOD_PLANK, "quantity": 1}],
                "output": {"item_id": STONE_SWORD, "quantity": 1}
            },
            # 石镐
            {
                "name": "石镐",
                "inputs": [{"item_id": STONE, "quantity": 1}, {"item_id": WOOD_PLANK, "quantity": 1}],
                "output": {"item_id": STONE_PICKAXE, "quantity": 1}
            },
            # 石斧
            {
                "name": "石斧",
                "inputs": [{"item_id": STONE, "quantity": 1}, {"item_id": WOOD_PLANK, "quantity": 1}],
                "output": {"item_id": STONE_AXE, "quantity": 1}
            },
            # 石铲
            {
                "name": "石铲",
                "inputs": [{"item_id": STONE, "quantity": 1}, {"item_id": WOOD_PLANK, "quantity": 1}],
                "output": {"item_id": STONE_SHOVEL, "quantity": 1}
            },
            # 铜剑
            {
                "name": "铜剑",
                "inputs": [{"item_id": COPPER_INGOT, "quantity": 3}, {"item_id": WOOD_PLANK, "quantity": 1}],
                "output": {"item_id": COPPER_SWORD, "quantity": 1}
            },
            # 铜镐
            {
                "name": "铜镐",
                "inputs": [{"item_id": COPPER_INGOT, "quantity": 3}, {"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": COPPER_PICKAXE, "quantity": 1}
            },
            # 铜斧
            {
                "name": "铜斧",
                "inputs": [{"item_id": COPPER_INGOT, "quantity": 3}, {"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": COPPER_AXE, "quantity": 1}
            },
            # 铜铲
            {
                "name": "铜铲",
                "inputs": [{"item_id": COPPER_INGOT, "quantity": 1}, {"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": COPPER_SHOVEL, "quantity": 1}
            },
            # 铁剑
            {
                "name": "铁剑",
                "inputs": [{"item_id": IRON_INGOT, "quantity": 3}, {"item_id": WOOD_PLANK, "quantity": 1}],
                "output": {"item_id": IRON_SWORD, "quantity": 1}
            },
            # 铁镐
            {
                "name": "铁镐",
                "inputs": [{"item_id": IRON_INGOT, "quantity": 3}, {"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": IRON_PICKAXE, "quantity": 1}
            },
            # 铁斧
            {
                "name": "铁斧",
                "inputs": [{"item_id": IRON_INGOT, "quantity": 3}, {"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": IRON_AXE, "quantity": 1}
            },
            # 铁铲
            {
                "name": "铁铲",
                "inputs": [{"item_id": IRON_INGOT, "quantity": 1}, {"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": IRON_SHOVEL, "quantity": 1}
            },
            # 金剑
            {
                "name": "金剑",
                "inputs": [{"item_id": GOLD_INGOT, "quantity": 3}, {"item_id": WOOD_PLANK, "quantity": 1}],
                "output": {"item_id": GOLD_SWORD, "quantity": 1}
            },
            # 金镐
            {
                "name": "金镐",
                "inputs": [{"item_id": GOLD_INGOT, "quantity": 3}, {"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": GOLD_PICKAXE, "quantity": 1}
            },
            # 金斧
            {
                "name": "金斧",
                "inputs": [{"item_id": GOLD_INGOT, "quantity": 3}, {"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": GOLD_AXE, "quantity": 1}
            },
            # 金铲
            {
                "name": "金铲",
                "inputs": [{"item_id": GOLD_INGOT, "quantity": 1}, {"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": GOLD_SHOVEL, "quantity": 1}
            },
            # 钻石剑
            {
                "name": "钻石剑",
                "inputs": [{"item_id": DIAMOND, "quantity": 3}, {"item_id": WOOD_PLANK, "quantity": 1}],
                "output": {"item_id": DIAMOND_SWORD, "quantity": 1}
            },
            # 钻石镐
            {
                "name": "钻石镐",
                "inputs": [{"item_id": DIAMOND, "quantity": 3}, {"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": DIAMOND_PICKAXE, "quantity": 1}
            },
            # 钻石斧
            {
                "name": "钻石斧头",
                "inputs": [{"item_id": DIAMOND, "quantity": 3}, {"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": DIAMOND_AXE, "quantity": 1}
            },
            # 钻石铲
            {
                "name": "钻石铲",
                "inputs": [{"item_id": DIAMOND, "quantity": 1}, {"item_id": WOOD_PLANK, "quantity": 2}],
                "output": {"item_id": DIAMOND_SHOVEL, "quantity": 1}
            },
            # 箱子
            {
                "name": "箱子",
                "inputs": [{"item_id": WOOD_PLANK, "quantity": 8}],
                "output": {"item_id": CHEST, "quantity": 1}
            },
            # 钻石块
            {
                "name": "钻石块",
                "inputs": [{"item_id": DIAMOND_ORE, "quantity": 9}],
                "output": {"item_id": DIAMOND_BLOCK, "quantity": 1}
            },
            # 金块
            {
                "name": "金块",
                "inputs": [{"item_id": GOLD_ORE, "quantity": 9}],
                "output": {"item_id": GOLD_BLOCK, "quantity": 1}
            },
            # 铁块
            {
                "name": "铁块",
                "inputs": [{"item_id": IRON_ORE, "quantity": 9}],
                "output": {"item_id": IRON_BLOCK, "quantity": 1}
            },
            # 铜块
            {
                "name": "铜块",
                "inputs": [{"item_id": COPPER_ORE, "quantity": 9}],
                "output": {"item_id": COPPER_BLOCK, "quantity": 1}
            },
            # 岩石_底（特殊方块）
            {
                "name": "岩石_底",
                "inputs": [{"item_id": STONE, "quantity": 3}],
                "output": {"item_id": STONE_BOTTOM, "quantity": 1}
            }
        ]

    def can_craft(self, recipe_index, player):
        """检查是否可以合成指定配方"""
        if 0 <= recipe_index < len(self.recipes):
            recipe = self.recipes[recipe_index]
            for input_item in recipe["inputs"]:
                if not player.has_item(input_item["item_id"], input_item["quantity"]):
                    return False
            return True
        return False

    def craft(self, recipe_index, player):
        """合成物品"""
        if self.can_craft(recipe_index, player):
            recipe = self.recipes[recipe_index]
            # 消耗材料
            for input_item in recipe["inputs"]:
                player.remove_item(input_item["item_id"], input_item["quantity"])
            # 返回合成结果
            return recipe["output"]
        return None


class Game:
    """游戏主类，协调所有游戏组件"""

    def __init__(self):
        # 地图大小设置
        self.show_map_settings = False
        self.selected_width = 1000  # 默认宽度1000
        self.selected_height = 256  # 默认高度256
        self.width_options = [500, 1000, 2000, 3000, 5000, 10000, 20000, 50000, 570000]
        self.height_options = [51, 128, 256, 384, 512]
        
        # 开发者模式设置，默认开启
        self.is_developer_mode = True
        
        # 创建存档开关，默认开启
        self.save_enabled = False
        
        # 初始化游戏组件
        self.image_loader = ImageLoader()
        self.world = World(self.image_loader)
        self.player = Player(WORLD_WIDTH * TILE_SIZE // 2, 0)
        # 游戏开始时给玩家30秒无敌时间
        self.player.immune_time = 30.0
        self.player.is_resurrection_immune = True
        self.creatures = self.spawn_initial_creatures(30)  # 生成初始生物
        self.crafting = CraftingSystem()
        
        # 下雨系统属性
        self.is_raining = False
        self.rain_drops = []
        self.rain_intensity = 0.1  # 雨的密度（0-1）
        self.rain_timer = 0
        self.rain_duration = 0
        self.min_rain_interval = 60  # 最小下雨间隔（秒）
        self.max_rain_interval = 300  # 最大下雨间隔（秒）
        self.min_rain_duration = 30  # 最小下雨持续时间（秒）
        self.max_rain_duration = 120  # 最大下雨持续时间（秒）
        self.rain_chance = 0.4  # 下雨触发概率（30%）
        
        # 打雷系统属性
        self.is_thundering = False
        self.thunder_timer = 0
        self.thunder_flash_timer = 0
        self.thunder_flash_duration = 0.3  # 闪电闪光持续时间（秒）
        self.thunder_sound_timer = 0
        self.thunder_sound_delay = 0  # 闪电到雷声的延迟（秒）
        self.thunder_chance = 0.005  # 打雷触发概率（0.1%）
        self.show_start_screen = True  # 显示启动画面标志
        self.camera_x = 0
        self.camera_y = 0
        self.breaking_progress = 0
        self.breaking_pos = None  # (x, y) 格子坐标
        
        # 装备属性变量
        self.头盔_伤害 = 0
        self.头盔_防御 = 0
        self.盔甲_防御 = 0
        self.靴子_摔伤 = 0
        self.靴子_防御 = 0
        self.特殊_移速 = 0
        self.特殊_防御 = 0

        
        # 死亡标志和状态
        self.is_player_dead = False
        self.death_screen_buttons = {}
        
        # 合成界面相关
        self.selected_recipe = None  # 当前选中的配方索引
        self.breaking_start_time = 0
        self.running = True
        self.save_file = "world_save.json"
        self.show_controls = False  # 控制操作提示页面的显示状态
        self.help_scroll_offset = 0  # 帮助页面滚动偏移量
        self.help_max_scroll_offset = 0  # 帮助页面最大滚动偏移量
        self.scroll_speed = 40  # 滚动速度
        
        # 存档选择界面相关
        self.show_save_selection = False  # 显示存档选择界面标志
        self.save_list_scroll_offset = 0  # 存档列表滚动偏移量
        self.save_selection_buttons = {}  # 存档选择界面按钮
        
        # 夜间怪物生成相关属性
        self.last_spawn_hour = -1  # 上一次生成怪物的小时
        self.night_spawn_interval = 10  # 夜间生成怪物的最小间隔（秒）
        self.last_night_spawn_time = 0  # 上一次夜间生成怪物的时间戳
        
        # 初始化新箱子页面管理器
        self.new_chest_manager = NewChestPageManager(self, ITEMS)
        
        # 伤害显示文本列表
        self.damage_texts = []
        
        # 物品实体列表，用于管理所有的掉落物
        self.item_entities = []
        
        # 箭矢列表，用于管理所有发射的箭矢
        self.arrows = []
        
        # 创造背包相关属性
        self.is_creative_inventory_open = False  # 创造背包显示状态
        self.selected_creative_category = "工具"  # 当前选中的创造背包分类（默认工具）
        
        # 高级功能页面相关属性
        self.is_advanced_menu_open = False  # 高级功能页面显示状态
        self.target_x = 0  # 目标X坐标
        self.target_y = 0  # 目标Y坐标
        self.input_active = None  # 当前激活的输入框
        self.input_text = ""  # 输入框文本
        self.instant_mining = False  # 秒挖掘开关
        self.god_mode = False  # 最高权限开关（可挖掘基岩）
        self.advanced_scroll_offset = 0  # 高级功能页面滚动偏移量
        self.advanced_max_scroll_offset = 700  # 高级功能页面最大滚动偏移量，增加以容纳所有功能
        self.advanced_menu_buttons = {}  # 高级功能页面按钮字典，用于存储所有可交互元素的矩形区域
        # 新增功能属性
        self.area_place_enabled = False  # 3*3放置功能开关
        self.area_mine_enabled = False  # 3*3范围挖掘功能开关
        self.target_damage = 1  # 玩家初始伤害值（会在玩家创建后更新）
        self.target_gravity = 0.5  # 玩家重力值
        self.fullscreen_click_enabled = False  # 全屏点击任意位置挖掘放置功能开关
        # 新增游戏变量目标值
        self.target_defense = 0  # 目标防御力
        self.target_damage_reduction = 0  # 目标免伤百分比
        self.target_damage_bonus = 0  # 目标伤害加成百分比
        self.target_fall_damage_reduction = 0  # 目标摔伤减免百分比
        self.target_speed_bonus = 0  # 目标移速加成百分比
        
        # 创造背包分类
        self.creative_categories = {
            "工具": [WOOD_SWORD, STONE_SWORD, COPPER_SWORD, IRON_SWORD, GOLD_SWORD, DIAMOND_SWORD,
                     WOOD_PICKAXE, STONE_PICKAXE, COPPER_PICKAXE, IRON_PICKAXE, GOLD_PICKAXE, DIAMOND_PICKAXE,
                     WOOD_AXE, STONE_AXE, COPPER_AXE, IRON_AXE, GOLD_AXE, DIAMOND_AXE,
                     WOOD_SHOVEL, STONE_SHOVEL, COPPER_SHOVEL, IRON_SHOVEL, GOLD_SHOVEL, DIAMOND_SHOVEL,
                     WOOD_BOW, WOOD_ARROW, RIFLE, PISTOL, SNIPER, BULLET, CROSSBOW, LASER_CANNON, ROCKET_LAUNCHER, ROCKET],
            "方块": [DIRT, GRASS, STONE, WOOD, LEAF, IRON_ORE, GOLD_ORE, DIAMOND_ORE, WATER, LAVA,
                     CHEST, TORCH, BLACK_DIRT, RED_FLOWER, GRASS_PLANT, BEDROCK, WOOD_PLANK,
                     COPPER_ORE, GOLD_BLOCK, IRON_BLOCK, DIAMOND_BLOCK, COPPER_BLOCK, SAND, DRY_GRASS, CACTUS,
                     JUNGLE_TREE, JUNGLE_LEAF, SHRUB, STONE_BOTTOM],  # 雨林方块和特殊方块
            "食物": [APPLE, MEAT, JUNGLE_FRUIT, HEALTH_POTION_1, HEALTH_POTION_2, HEALTH_POTION_3, HEALTH_POTION_4],  # 雨林食物和药水
            "生物": [SLIME, MARMOT, GHOST, BAT, FIRE_SPIRIT, MUSHROOM_MONSTER, ROCK_MONSTER, SCORPION, MONKEY],  # 雨林生物
            "装备": [HELMET_1, HELMET_2, HELMET_3, HELMET_4, HELMET_5,
                     ARMOR_1, ARMOR_2, ARMOR_3, ARMOR_4, ARMOR_5,
                     BOOTS_1, BOOTS_2, BOOTS_3, BOOTS_4, BOOTS_5,
                     SPECIAL_1, SPECIAL_2, SPECIAL_3, SPECIAL_4, SPECIAL_5]  # 装备分类，包含头盔、盔甲、靴子和特殊装备
        }
        
        # 创造背包页面滚动偏移量
        self.creative_scroll_offset = 0
        self.creative_max_scroll_offset = 0
        
        # 快捷拿去功能状态变量
        self.quick_take_enabled = True  # 默认开启快捷拿去（一次拿64个）
        self.show_quantity_input = False  # 是否显示数量输入界面
        self.selected_item_for_quantity = None  # 当前正在选择数量的物品ID
        self.quantity_to_take = 1  # 默认拿取数量
        self.quantity_input_rect = None  # 数量输入界面按钮的矩形区域
        
        # 丢弃数量选择功能状态变量
        self.show_drop_quantity_input = False  # 是否显示丢弃数量选择界面
        self.item_to_drop = None  # 要丢弃的物品ID
        self.quantity_to_drop = 1  # 默认丢弃数量
        self.drop_quantity_rect = None  # 丢弃数量选择界面按钮的矩形区域

    def find_ground_position(self, min_distance_from_player=0):
        """查找一个有固体方块支撑的地面位置"""
        player_x = self.player.x if hasattr(self, 'player') else WORLD_WIDTH * TILE_SIZE // 2
        player_y = self.player.y if hasattr(self, 'player') else 0
        
        for _ in range(100):  # 最多尝试100次
            # 随机X位置
            x = random.randint(100, (WORLD_WIDTH - 10) * TILE_SIZE)
            
            # 从顶部向下寻找固体方块的顶部
            for y in range(100, (WORLD_HEIGHT - 10) * TILE_SIZE):
                # 转换为方块坐标
                tile_x = int(x // TILE_SIZE)
                tile_y = int(y // TILE_SIZE)
                
                # 检查当前方块是否为空气，下方方块是否为固体
                if (self.world.is_within_bounds(tile_x, tile_y) and 
                    self.world.is_within_bounds(tile_x, tile_y + 1) and 
                    self.world.get_block(tile_x, tile_y) == AIR and 
                    self.world.get_block(tile_x, tile_y + 1) != AIR and 
                    BLOCKS.get(self.world.get_block(tile_x, tile_y + 1), {}).get('solid', False)):
                    
                    # 检查是否距离玩家足够远
                    distance = math.sqrt((x - player_x) ** 2 + (y - player_y) ** 2)
                    if distance >= min_distance_from_player:
                        return x, y
        
        # 如果找不到合适的位置，返回默认位置
        return random.randint(100, (WORLD_WIDTH - 10) * TILE_SIZE), 100 * TILE_SIZE

    def spawn_initial_creatures(self, count):
        """生成初始生物"""
        creatures = []
        creature_types = list(CREATURES.keys())

        for _ in range(count):
            # 寻找有固体方块支撑的地面位置，远离玩家初始位置
            x, y = self.find_ground_position(min_distance_from_player=TILE_SIZE * 50)

            # 随机生物类型
            creature_type = random.choice(creature_types)
            creatures.append(Creature(creature_type, x, y))

        return creatures

    def update_camera(self):
        """更新相机位置，跟随玩家"""
        target_x = self.player.x - WIDTH // 2
        target_y = self.player.y - HEIGHT // 2

        # 平滑相机移动
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1

        # 限制相机在世界范围内
        self.camera_x = max(0, min(self.camera_x, WORLD_WIDTH * TILE_SIZE - WIDTH))
        self.camera_y = max(0, min(self.camera_y, WORLD_HEIGHT * TILE_SIZE - HEIGHT))

    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # 如果玩家死亡，处理死亡页面的事件
            if self.is_player_dead:
                # 鼠标点击
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左键点击
                    mx, my = event.pos
                    # 检查是否点击了原地复活按钮
                    if 'respawn' in self.death_screen_buttons and self.death_screen_buttons['respawn'].collidepoint(mx, my):
                        # 原地复活：恢复生命值，不清空背包，添加30秒无敌时间
                        if self.is_developer_mode:
                            # 开发者模式下，无条件复活
                            self.player.health = self.player.max_health
                            self.player.hunger = self.player.max_hunger
                            self.player.oxygen = self.player.max_oxygen
                            self.player.immune_time = 30.0  # 30秒无敌时间
                            self.player.is_resurrection_immune = True  # 标记为复活无敌
                            self.is_player_dead = False
                            print(f"[{time.strftime('%H:%M:%S')}] 玩家（开发者模式）选择原地复活")
                        else:
                            # 非开发者模式下，原地复活消耗星星
                            if self.player.stars >= 1:
                                self.player.stars -= 1
                                self.player.health = self.player.max_health
                                self.player.hunger = self.player.max_hunger
                                self.player.oxygen = self.player.max_oxygen
                                self.player.immune_time = 30.0  # 30秒无敌时间
                                self.player.is_resurrection_immune = True  # 标记为复活无敌
                                self.is_player_dead = False
                                print(f"[{time.strftime('%H:%M:%S')}] 玩家消耗1颗星星选择原地复活，剩余星星：{self.player.stars}")
                            else:
                                print(f"[{time.strftime('%H:%M:%S')}] 玩家星星数量不足，无法原地复活")
                    # 检查是否点击了清空背包（坐标复活）按钮
                    elif 'lose_inventory' in self.death_screen_buttons and self.death_screen_buttons['lose_inventory'].collidepoint(mx, my):
                        # 清空背包复活：恢复生命值，清空背包，移动到出生点，添加30秒无敌时间
                        if self.is_developer_mode:
                            # 开发者模式下，无条件复活
                            self.player.health = self.player.max_health
                            self.player.hunger = self.player.max_hunger
                            self.player.oxygen = self.player.max_oxygen
                            self.player.immune_time = 30.0  # 30秒无敌时间
                            self.player.is_resurrection_immune = True  # 标记为复活无敌
                            # 清空背包
                            self.player.inventory = []
                            for _ in range(self.player.backpack_slots):
                                self.player.inventory.append([0, 0])
                            # 清空快捷栏，使用正确的结构格式
                            self.player.hotbar = []
                            for _ in range(8):
                                self.player.hotbar.append([0, 0])
                            # 添加一些基础物品
                            self.player.add_item(DIRT, 10)
                            self.player.add_item(WOOD, 10)
                            self.player.add_item(STONE, 10)
                            self.player.add_item(WOOD_PICKAXE, 1)
                            self.player.add_item(WOOD_AXE, 1)
                            self.player.add_item(APPLE, 5)
                            # 移动到出生点
                            self.player.x = WORLD_WIDTH * TILE_SIZE // 2
                            self.player.y = 0
                            self.is_player_dead = False
                            print(f"[{time.strftime('%H:%M:%S')}] 玩家（开发者模式）选择清空背包复活")
                        else:
                            # 非开发者模式下，清空背包复活不消耗星星
                            # 直接复活，不需要消耗星星
                            self.player.health = self.player.max_health
                            self.player.hunger = self.player.max_hunger
                            self.player.oxygen = self.player.max_oxygen
                            self.player.immune_time = 30.0  # 30秒无敌时间
                            self.player.is_resurrection_immune = True  # 标记为复活无敌
                            # 清空背包
                            self.player.inventory = []
                            for _ in range(self.player.backpack_slots):
                                self.player.inventory.append([0, 0])
                            # 清空快捷栏，使用正确的结构格式
                            self.player.hotbar = []
                            for _ in range(8):
                                self.player.hotbar.append([0, 0])
                            # 添加一些基础物品
                            self.player.add_item(DIRT, 10)
                            self.player.add_item(WOOD, 10)
                            self.player.add_item(STONE, 10)
                            self.player.add_item(WOOD_PICKAXE, 1)
                            self.player.add_item(WOOD_AXE, 1)
                            self.player.add_item(APPLE, 5)
                            # 移动到出生点
                            self.player.x = WORLD_WIDTH * TILE_SIZE // 2
                            self.player.y = 0
                            self.is_player_dead = False
                            print(f"[{time.strftime('%H:%M:%S')}] 玩家选择清空背包复活（不消耗星星）")
                    # 检查是否点击了位置复活按钮
                    elif 'respawn_position' in self.death_screen_buttons and self.death_screen_buttons['respawn_position'].collidepoint(mx, my):
                        # 位置复活：返回出生点，恢复生命值，添加30秒无敌时间
                        if self.is_developer_mode:
                            # 开发者模式下，无条件复活
                            self.player.health = self.player.max_health
                            self.player.hunger = self.player.max_hunger
                            self.player.oxygen = self.player.max_oxygen
                            self.player.immune_time = 30.0  # 30秒无敌时间
                            self.player.is_resurrection_immune = True  # 标记为复活无敌
                            # 移动到出生点
                            self.player.x = WORLD_WIDTH * TILE_SIZE // 2
                            self.player.y = 0
                            self.is_player_dead = False
                            print(f"[{time.strftime('%H:%M:%S')}] 玩家（开发者模式）选择返回出生点复活")
                        else:
                            # 非开发者模式下，消耗1颗星星复活
                            if self.player.stars >= 1:
                                self.player.stars -= 1
                                self.player.health = self.player.max_health
                                self.player.hunger = self.player.max_hunger
                                self.player.oxygen = self.player.max_oxygen
                                self.player.immune_time = 30.0  # 30秒无敌时间
                                self.player.is_resurrection_immune = True  # 标记为复活无敌
                                # 移动到出生点
                                self.player.x = WORLD_WIDTH * TILE_SIZE // 2
                                self.player.y = 0
                                self.is_player_dead = False
                                print(f"[{time.strftime('%H:%M:%S')}] 玩家消耗1颗星星选择返回出生点复活，剩余星星：{self.player.stars}")
                            else:
                                print(f"[{time.strftime('%H:%M:%S')}] 玩家星星数量不足，无法返回出生点复活")
                continue

            if event.type == pygame.KEYDOWN:
                # 快捷栏选择
                if pygame.K_1 <= event.key <= pygame.K_8:
                    slot = event.key - pygame.K_1
                    self.player.selected_slot = slot

                # 打开/关闭背包
                elif event.key == pygame.K_e:
                    self.player.is_inventory_open = not self.player.is_inventory_open
                    self.player.is_crafting_open = False
                    if self.player.is_inventory_open and self.player.is_chest_open:
                        self.player.is_chest_open = False
                        self.player.current_chest = None

                # 打开/关闭合成界面
                elif event.key == pygame.K_c:
                    self.player.is_crafting_open = not self.player.is_crafting_open
                    self.player.is_inventory_open = False
                    self.player.is_chest_open = False
                    self.player.current_chest = None

                # 使用物品（吃食物或射箭/射击）
                elif event.key == pygame.K_q:
                    selected_item = self.player.get_selected_item()
                    if selected_item:
                        # 检查是否是远程武器（弓、手枪或狙击枪）
                        if selected_item["item_id"] == WOOD_BOW or selected_item["item_id"] == PISTOL or selected_item["item_id"] == SNIPER or selected_item["item_id"] == CROSSBOW or selected_item["item_id"] == LASER_CANNON or selected_item["item_id"] == ROCKET_LAUNCHER:
                            # 检查玩家是否在冷却中
                            if not hasattr(self.player, 'attack_cooldown') or self.player.attack_cooldown <= 0:
                                # 执行射击逻辑，与鼠标左键相同
                                self.attack_creatures_with_damage_display()
                                # 记录输入日志
                                if selected_item["item_id"] == WOOD_BOW:
                                    print(f"[{time.strftime('%H:%M:%S')}] 玩家使用了弓: {selected_item['item_id']}")
                                elif selected_item["item_id"] == PISTOL:
                                    print(f"[{time.strftime('%H:%M:%S')}] 玩家使用了手枪: {selected_item['item_id']}")
                                elif selected_item["item_id"] == SNIPER:
                                    print(f"[{time.strftime('%H:%M:%S')}] 玩家使用了狙击枪: {selected_item['item_id']}")
                                elif selected_item["item_id"] == CROSSBOW:
                                    print(f"[{time.strftime('%H:%M:%S')}] 玩家使用了弩: {selected_item['item_id']}")
                                elif selected_item["item_id"] == LASER_CANNON:
                                    print(f"[{time.strftime('%H:%M:%S')}] 玩家使用了激光炮: {selected_item['item_id']}")
                                elif selected_item["item_id"] == ROCKET_LAUNCHER:
                                    print(f"[{time.strftime('%H:%M:%S')}] 玩家使用了火箭筒: {selected_item['item_id']}")
                            else:
                                # 玩家还在冷却中，打印提示信息
                                print(f"[{time.strftime('%H:%M:%S')}] 武器冷却中，请等待...")
                        else:
                            # 其他物品使用eat方法
                            self.player.eat(selected_item["item_id"])
                            # 记录输入日志
                            print(f"[{time.strftime('%H:%M:%S')}] 玩家使用了物品: {selected_item['item_id']}")
                
                # 丢弃快捷栏物品（向前抛出）
                elif event.key == pygame.K_g:
                    selected_item = self.player.get_selected_item()
                    if selected_item:
                        item_id = selected_item["item_id"]
                        quantity = selected_item["quantity"]
                        
                        # 只丢弃一个物品
                        if quantity >= 1:
                            # 创建物品实体，位置在玩家前方
                            spawn_x = self.player.x + 30 * (1 if self.player.facing_right else -1)
                            spawn_y = self.player.y
                            
                            # 创建ItemEntity实例，使用正确的构造函数参数
                            item_entity = ItemEntity(
                                spawn_x,
                                spawn_y,
                                item_id,
                                1  # 丢弃一个物品
                            )
                            
                            # 手动设置向前的水平速度
                            item_entity.velocity_x = 30 if self.player.facing_right else -30
                            # 设置向上的初始速度，产生抛物线路径
                            item_entity.velocity_y = -50
                            # 设置更长的生命周期
                            item_entity.lifetime = 60.0
                            
                            # 添加到物品实体列表
                            self.item_entities.append(item_entity)
                            
                            # 从玩家快捷栏中减去一个物品
                            self.player.hotbar[self.player.selected_slot][1] -= 1
                            # 如果数量变为0，清空物品ID
                            if self.player.hotbar[self.player.selected_slot][1] <= 0:
                                self.player.hotbar[self.player.selected_slot][0] = 0
                                self.player.hotbar[self.player.selected_slot][1] = 0
                            
                            # 记录输入日志
                            print(f"[{time.strftime('%H:%M:%S')}] 玩家丢弃了物品: {item_id}")
                
                # 打开/关闭操作提示
                elif event.key == pygame.K_F1:
                    self.show_controls = not self.show_controls
                    # 记录输入日志
                    print(f"[{time.strftime('%H:%M:%S')}] 玩家按下F1键，操作提示页面 {'打开' if self.show_controls else '关闭'}")

                # 打开/关闭创造背包 - 只有开发者模式开启时才能使用
                elif event.key == pygame.K_F3 and self.is_developer_mode:
                    self.is_creative_inventory_open = not self.is_creative_inventory_open
                    # 关闭其他界面
                    self.player.is_inventory_open = False
                    self.player.is_crafting_open = False
                    self.player.is_chest_open = False
                    self.player.current_chest = None
                    self.show_controls = False
                    self.is_advanced_menu_open = False
                    # 记录输入日志
                    print(f"[{time.strftime('%H:%M:%S')}] 玩家按下F3键，创造背包 {'打开' if self.is_creative_inventory_open else '关闭'}")
                
                # 打开/关闭高级功能页面 - 只有开发者模式开启时才能使用
                elif event.key == pygame.K_F4 and self.is_developer_mode:
                    self.is_advanced_menu_open = not self.is_advanced_menu_open
                    # 关闭其他界面
                    self.player.is_inventory_open = False
                    self.player.is_crafting_open = False
                    self.player.is_chest_open = False
                    self.player.current_chest = None
                    self.show_controls = False
                    self.is_creative_inventory_open = False
                    # 记录输入日志
                    print(f"[{time.strftime('%H:%M:%S')}] 玩家按下F4键，高级功能页面 {'打开' if self.is_advanced_menu_open else '关闭'}")
                
                # 按下ESC键关闭任何打开的页面
                elif event.key == pygame.K_ESCAPE and not self.input_active:
                    # 检查是否有任何页面打开
                    if (self.player.is_inventory_open or self.player.is_chest_open or 
                        self.new_chest_manager.is_open or self.show_controls or 
                        self.is_creative_inventory_open or self.is_advanced_menu_open):
                        # 关闭所有打开的页面
                        self.player.is_inventory_open = False
                        self.player.is_chest_open = False
                        self.player.current_chest = None
                        self.new_chest_manager.close_page()
                        self.show_controls = False
                        self.is_creative_inventory_open = False
                        self.is_advanced_menu_open = False
                        # 记录输入日志
                        print(f"[{time.strftime('%H:%M:%S')}] 玩家按下ESC键，关闭所有打开的页面")

                # 处理坐标输入或数量输入
                elif self.input_active: 
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        # 确认输入
                        try:
                            if self.input_active == 'x':
                                self.target_x = int(self.input_text)
                            elif self.input_active == 'y':
                                self.target_y = int(self.input_text)
                            elif self.input_active == 'quantity':
                                # 处理数量输入
                                input_value = int(self.input_text)
                                self.quantity_to_take = max(1, min(64, input_value))
                        except ValueError:
                            # 输入不是有效的数字，保持原值
                            pass
                        # 取消输入模式
                        self.input_active = None
                        self.input_text = ""
                    elif event.key == pygame.K_ESCAPE:
                        # 取消输入
                        self.input_active = None
                        self.input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        # 删除字符
                        self.input_text = self.input_text[:-1]
                    else:
                        # 添加字符，对于坐标允许数字和负号，对于数量只允许数字
                        # 使用event.unicode获取实际输入的字符
                        key_char = event.unicode
                        if self.input_active == 'quantity':
                            # 数量输入只允许数字
                            if key_char.isdigit():
                                # 限制输入长度，防止输入过大的数字
                                if len(self.input_text) < 3:
                                    self.input_text += key_char
                        else:
                            # 坐标输入允许数字和负号
                            if (key_char.isdigit() or 
                                (key_char == '-' and not self.input_text)):
                                self.input_text += key_char

            # 鼠标点击
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    self.handle_left_click(event.pos)
                elif event.button == 3:  # 右键
                    self.handle_right_click(event.pos)
                # 处理鼠标滚轮事件（使用MOUSEBUTTONDOWN作为替代方案）
                elif self.show_controls:
                    if event.button == 4:  # 滚轮上滚
                        self.help_scroll_offset = max(0, self.help_scroll_offset - self.scroll_speed)
                    elif event.button == 5:  # 滚轮下滚
                        self.help_scroll_offset = min(self.help_max_scroll_offset, self.help_scroll_offset + self.scroll_speed)
                elif self.is_advanced_menu_open:
                    if event.button == 4:  # 滚轮上滚
                        self.advanced_scroll_offset = max(0, self.advanced_scroll_offset - self.scroll_speed)
                    elif event.button == 5:  # 滚轮下滚
                        self.advanced_scroll_offset = min(self.advanced_max_scroll_offset, self.advanced_scroll_offset + self.scroll_speed)
            
            # 处理鼠标滚轮事件（标准方式）
            if event.type == pygame.MOUSEWHEEL:
                if self.show_controls:
                    if event.y > 0:  # 滚轮上滚
                        self.help_scroll_offset = max(0, self.help_scroll_offset - self.scroll_speed)
                    else:  # 滚轮下滚
                        self.help_scroll_offset = min(self.help_max_scroll_offset, self.help_scroll_offset + self.scroll_speed)
                elif self.is_creative_inventory_open:
                    if event.y > 0:  # 滚轮上滚
                        self.creative_scroll_offset = max(0, self.creative_scroll_offset - self.scroll_speed)
                    else:  # 滚轮下滚
                        self.creative_scroll_offset = min(self.creative_max_scroll_offset, self.creative_scroll_offset + self.scroll_speed)
                elif self.is_advanced_menu_open:
                    if event.y > 0:  # 滚轮上滚
                        self.advanced_scroll_offset = max(0, self.advanced_scroll_offset - self.scroll_speed)
                    else:  # 滚轮下滚
                        self.advanced_scroll_offset = min(self.advanced_max_scroll_offset, self.advanced_scroll_offset + self.scroll_speed)
                elif self.show_save_selection:
                    if event.y > 0:  # 滚轮上滚
                        self.save_list_scroll_offset = max(0, self.save_list_scroll_offset - self.scroll_speed)
                    else:  # 滚轮下滚
                        # 计算最大滚动偏移量
                        save_folder = "存档"
                        save_files = []
                        if os.path.exists(save_folder):
                            # 优先使用子文件夹作为存档
                            for item in os.listdir(save_folder):
                                item_path = os.path.join(save_folder, item)
                                if os.path.isdir(item_path):
                                    save_files.append(item)
                            # 如果没有子文件夹，回退使用.json文件
                            if not save_files:
                                for file in os.listdir(save_folder):
                                    if file.endswith(".json"):
                                        save_files.append(file)
                        # 计算存档列表的总高度和最大滚动偏移量
                        item_height = 60
                        item_spacing = 10
                        total_height = len(save_files) * (item_height + item_spacing) - item_spacing
                        list_height = 400
                        max_scroll_offset = max(0, total_height - list_height)
                        self.save_list_scroll_offset = min(max_scroll_offset, self.save_list_scroll_offset + self.scroll_speed)

    def handle_left_click(self, pos):
        """处理左键点击"""
        mx, my = pos

        # 如果新箱子页面打开，优先处理
        if self.new_chest_manager.is_open:
            self.new_chest_manager.handle_click(mx, my)
            return
        
        # 界面交互优先
        if self.is_advanced_menu_open:
            self.handle_advanced_menu_click(mx, my)
            return
            
        if self.is_creative_inventory_open:
            self.handle_creative_inventory_click(mx, my)
            return
        
        # 检查是否点击了关闭按钮（无论是背包还是箱子界面）
        if hasattr(self, 'inventory_close_button') and self.inventory_close_button and self.inventory_close_button.collidepoint(mx, my):
            # 根据当前状态决定关闭什么
            if self.player.is_chest_open:
                # 如果打开了箱子，只关闭箱子
                self.player.is_chest_open = False
                self.player.current_chest = None
            else:
                # 否则关闭背包
                self.player.is_inventory_open = False
                self.player.is_crafting_open = False
            return

        if self.player.is_inventory_open or self.player.is_chest_open:
            self.handle_inventory_click(mx, my)
            return

        if self.player.is_crafting_open:
            self.handle_crafting_click(mx, my)
            return

        # 攻击生物或破坏方块
        tile_x, tile_y = self.world.screen_to_tile(mx, my, self.camera_x, self.camera_y)
        player_tile_x, player_tile_y = int(self.player.x // TILE_SIZE), int(self.player.y // TILE_SIZE)

        # 检查是否在交互范围内或启用了全屏点击功能
        if (self.fullscreen_click_enabled or 
            (abs(tile_x - player_tile_x) <= INTERACTION_RANGE and
             abs(tile_y - player_tile_y) <= INTERACTION_RANGE)):

            # 优先检查是否点击到生物
            # 获取鼠标点击的世界坐标
            world_x = mx + self.camera_x
            world_y = my + self.camera_y
            
            # 检查是否有生物在点击位置
            creature_hit = False
            for creature in self.creatures[:]:
                # 检查鼠标点击是否在生物范围内
                if (creature.x <= world_x <= creature.x + creature.width and 
                    creature.y <= world_y <= creature.y + creature.height):
                    # 攻击生物，带伤害显示
                    self.attack_creatures_with_damage_display()
                    creature_hit = True
                    break
            
            # 如果没有点击到生物，再检查是否破坏方块
            if not creature_hit:
                block_id = self.world.get_block(tile_x, tile_y)
                if block_id and block_id != AIR:
                    # 破坏方块
                    self.start_breaking_block(tile_x, tile_y)
                else:
                    # 没有方块也没有生物，尝试范围内攻击
                    self.attack_creatures_with_damage_display()

    def attack_creatures_with_damage_display(self):
        """攻击生物并显示伤害文本"""
        # 获取当前手持物品
        weapon = self.player.get_selected_item()
        
        # 检查是否手持远程武器（弓或狙击枪）
        if weapon and weapon["item_id"] == WOOD_BOW:
            # 弓类武器，发射箭矢
            # 检查玩家是否有箭矢
            has_arrow = False
            for slot in self.player.hotbar:
                if slot[0] == WOOD_ARROW and slot[1] > 0:
                    has_arrow = True
                    slot[1] -= 1  # 扣除一支箭
                    # 如果数量变为0，清空物品ID
                    if slot[1] <= 0:
                        slot[0] = 0
                    break
            
            # 如果快捷栏没有箭矢，检查背包
            if not has_arrow:
                for slot in self.player.inventory:
                    if slot[0] == WOOD_ARROW and slot[1] > 0:
                        has_arrow = True
                        slot[1] -= 1  # 扣除一支箭
                        # 如果数量变为0，清空物品ID
                        if slot[1] <= 0:
                            slot[0] = 0
                        break
            
            if not has_arrow:
                return  # 没有箭矢，无法射击
            
            # 设置弓的冷却时间为1秒
            self.player.attack_cooldown = 1.0
            
            # 获取鼠标位置，计算射击方向
            mx, my = pygame.mouse.get_pos()
            # 转换为世界坐标
            world_x = mx + self.camera_x
            world_y = my + self.camera_y
            
            # 计算玩家中心位置
            player_center_x = self.player.x + self.player.width // 2
            player_center_y = self.player.y + self.player.height // 2
            
            # 计算方向向量
            dx = world_x - player_center_x
            dy = world_y - player_center_y
            
            # 归一化方向向量
            distance = math.sqrt(dx * dx + dy * dy)
            if distance > 0:
                dx /= distance
                dy /= distance
            else:
                dx, dy = 1, 0  # 默认向右射击
            
            # 设置箭矢速度（基于弓的伤害属性，伤害越高速度越快）
            # 设置弓的伤害为20点
            bow_damage = 20
            arrow_speed = 8 + (bow_damage * 0.5)  # 基础速度8，每点伤害增加0.5速度
            
            # 创建箭矢并添加到游戏中
            arrow = Arrow(
                player_center_x,  # x坐标
                player_center_y,  # y坐标
                dx,  # 方向x（归一化）
                dy,  # 方向y（归一化）
                bow_damage,  # 伤害
                self.player  # 所有者（玩家）
            )
            self.arrows.append(arrow)
            
            return  # 射箭后不进行近战攻击
        elif weapon and weapon["item_id"] == PISTOL:
            # 手枪，发射子弹
            # 检查玩家是否有子弹
            has_bullet = False
            for slot in self.player.hotbar:
                if slot[0] == BULLET and slot[1] > 0:
                    has_bullet = True
                    slot[1] -= 1  # 扣除一颗子弹
                    # 如果数量变为0，清空物品ID
                    if slot[1] <= 0:
                        slot[0] = 0
                    break
            
            # 如果快捷栏没有子弹，检查背包
            if not has_bullet:
                for slot in self.player.inventory:
                    if slot[0] == BULLET and slot[1] > 0:
                        has_bullet = True
                        slot[1] -= 1  # 扣除一颗子弹
                        # 如果数量变为0，清空物品ID
                        if slot[1] <= 0:
                            slot[0] = 0
                        break
            
            if not has_bullet:
                return  # 没有子弹，无法射击
            
            # 设置手枪的冷却时间为0.3秒
            self.player.attack_cooldown = 0.3
            
            # 获取鼠标位置，计算射击方向
            mx, my = pygame.mouse.get_pos()
            # 添加随机偏差，最大±20像素
            random_offset_x = random.randint(-20, 20)
            random_offset_y = random.randint(-20, 20)
            # 应用随机偏差
            world_x = mx + self.camera_x + random_offset_x
            world_y = my + self.camera_y + random_offset_y
            
            # 计算玩家中心位置
            player_center_x = self.player.x + self.player.width // 2
            player_center_y = self.player.y + self.player.height // 2
            
            # 计算方向向量
            dx = world_x - player_center_x
            dy = world_y - player_center_y
            
            # 归一化方向向量
            distance = math.sqrt(dx * dx + dy * dy)
            if distance > 0:
                dx /= distance
                dy /= distance
            else:
                dx, dy = 1, 0  # 默认向右射击
            
            # 设置手枪子弹速度为1200
            pistol_damage = ITEMS[weapon["item_id"]]["damage"]
            bullet_speed = 1200
            
            # 创建子弹并添加到游戏中
            bullet = Arrow(
                player_center_x,  # x坐标
                player_center_y,  # y坐标
                dx,  # 方向x（归一化）
                dy,  # 方向y（归一化）
                pistol_damage,  # 伤害
                self.player  # 所有者（玩家）
            )
            # 应用正确的子弹速度
            magnitude = math.sqrt(dx*dx + dy*dy)
            if magnitude > 0:
                bullet.velocity_x = (dx / magnitude) * bullet_speed
                bullet.velocity_y = (dy / magnitude) * bullet_speed
            else:
                bullet.velocity_x = bullet_speed
                bullet.velocity_y = 0
            
            # 设置子弹的重力为0，使子弹直线飞行
            bullet.gravity = 0
            
            self.arrows.append(bullet)
            
            return  # 射击后不进行近战攻击
        elif weapon and weapon["item_id"] == CROSSBOW:
            # 弩，发射多支箭
            # 不消耗子弹的未来弩
            arrow_count = 15  # 一次发射15支箭
            
            # 设置弩的冷却时间为0.1秒
            self.player.attack_cooldown = 0.1
            
            # 获取鼠标位置，计算射击方向
            mx, my = pygame.mouse.get_pos()
            # 转换为世界坐标
            world_x = mx + self.camera_x
            world_y = my + self.camera_y
            
            # 计算玩家中心位置
            player_center_x = self.player.x + self.player.width // 2
            player_center_y = self.player.y + self.player.height // 2
            
            # 计算主方向向量
            main_dx = world_x - player_center_x
            main_dy = world_y - player_center_y
            
            # 归一化主方向向量
            distance = math.sqrt(main_dx * main_dx + main_dy * main_dy)
            if distance > 0:
                main_dx /= distance
                main_dy /= distance
            else:
                main_dx, main_dy = 1, 0  # 默认向右射击
            
            # 设置弩的伤害为20点
            crossbow_damage = 20
            arrow_speed = 10 + (crossbow_damage * 0.5)  # 基础速度10，每点伤害增加0.5速度
            
            # 发射5支箭，每支箭有轻微的角度偏差
            for i in range(arrow_count):
                # 计算偏差角度（范围：-10度到+10度）
                angle_deviation = random.uniform(-10, 10)
                angle_rad = math.radians(angle_deviation)
                
                # 根据角度偏差计算新的方向向量
                # 使用旋转矩阵：x' = x*cosθ - y*sinθ, y' = x*sinθ + y*cosθ
                dx = main_dx * math.cos(angle_rad) - main_dy * math.sin(angle_rad)
                dy = main_dx * math.sin(angle_rad) + main_dy * math.cos(angle_rad)
                
                # 创建箭矢并添加到游戏中
                arrow = Arrow(
                    player_center_x,  # x坐标
                    player_center_y,  # y坐标
                    dx,  # 方向x（归一化）
                    dy,  # 方向y（归一化）
                    crossbow_damage,  # 伤害
                    self.player,  # 所有者（玩家）
                    'crossbow'  # 武器类型标识
                )
                self.arrows.append(arrow)
            
            return  # 射箭后不进行近战攻击
        elif weapon and weapon["item_id"] == LASER_CANNON:
            # 激光炮，发射激光光束
            # 移除冷却时间，实现无CD效果
            
            # 获取鼠标位置，计算射击方向
            mx, my = pygame.mouse.get_pos()
            # 转换为世界坐标
            world_x = mx + self.camera_x
            world_y = my + self.camera_y
            
            # 计算玩家中心位置
            player_center_x = self.player.x + self.player.width // 2
            player_center_y = self.player.y + self.player.height // 2
            
            # 计算方向向量
            dx = world_x - player_center_x
            dy = world_y - player_center_y
            
            # 归一化方向向量
            distance = math.sqrt(dx * dx + dy * dy)
            if distance > 0:
                dx /= distance
                dy /= distance
            else:
                dx, dy = 1, 0  # 默认向右射击
            
            # 激光伤害设置为800点
            laser_damage = 800
            
        elif weapon and weapon["item_id"] == ROCKET_LAUNCHER:
            # 火箭筒，发射火箭弹
            # 检查玩家是否有火箭弹
            has_rocket = False
            for slot in self.player.hotbar:
                if slot[0] == ROCKET and slot[1] > 0:
                    has_rocket = True
                    slot[1] -= 1  # 扣除一枚火箭弹
                    # 如果数量变为0，清空物品ID
                    if slot[1] <= 0:
                        slot[0] = 0
                    break
            
            # 如果快捷栏没有火箭弹，检查背包
            if not has_rocket:
                for slot in self.player.inventory:
                    if slot[0] == ROCKET and slot[1] > 0:
                        has_rocket = True
                        slot[1] -= 1  # 扣除一枚火箭弹
                        # 如果数量变为0，清空物品ID
                        if slot[1] <= 0:
                            slot[0] = 0
                        break
            
            if not has_rocket:
                return  # 没有火箭弹，无法射击
            
            # 设置火箭筒的冷却时间与木弓箭相同（1秒）
            self.player.attack_cooldown = 1.0
            
            # 获取鼠标位置，计算射击方向
            mx, my = pygame.mouse.get_pos()
            # 转换为世界坐标
            world_x = mx + self.camera_x
            world_y = my + self.camera_y
            
            # 计算玩家中心位置
            player_center_x = self.player.x + self.player.width // 2
            player_center_y = self.player.y + self.player.height // 2
            
            # 计算方向向量
            dx = world_x - player_center_x
            dy = world_y - player_center_y
            
            # 归一化方向向量
            distance = math.sqrt(dx * dx + dy * dy)
            if distance > 0:
                dx /= distance
                dy /= distance
            else:
                dx, dy = 1, 0  # 默认向右射击
            
            # 设置火箭弹速度与木弓箭相同
            rocket_damage = 10  # 初始伤害，实际伤害在爆炸时应用
            rocket_speed = 8 + (20 * 0.5)  # 与木弓箭相同的计算公式
            actual_speed = 500 * rocket_speed / 18  # 基于木弓箭的实际速度比例
            
            # 创建火箭弹并添加到游戏中
            rocket = Arrow(
                player_center_x,  # x坐标
                player_center_y,  # y坐标
                dx,  # 方向x（归一化）
                dy,  # 方向y（归一化）
                rocket_damage,  # 初始伤害（实际伤害在爆炸时应用）
                self.player,  # 所有者（玩家）
                'rocket'  # 武器类型标识
            )
            
            # 应用正确的火箭弹速度
            rocket.velocity_x = dx * actual_speed
            rocket.velocity_y = dy * actual_speed
            
            # 设置火箭弹的重力
            rocket.velocity_y += 50 * 0.016  # 轻微的重力效果
            
            self.arrows.append(rocket)
            
            return  # 射击后不进行近战攻击
            
            # 记录激光光束的起点
            laser_start_x, laser_start_y = player_center_x, player_center_y
            
            # 激光光束破坏鼠标指向路径上的所有方块
            current_x, current_y = player_center_x, player_center_y
            
            # 计算鼠标位置到玩家的距离
            mouse_distance = math.sqrt((world_x - player_center_x)**2 + (world_y - player_center_y)** 2)
            
            # 射线检测方块 - 让激光延伸到鼠标距离的3倍
            max_distance = mouse_distance * 3
            step_size = 5  # 减小步长，确保更精确的检测
            total_steps = int(max_distance / step_size)
            
            for _ in range(total_steps):
                current_x += dx * step_size
                current_y += dy * step_size
                
                # 转换为方块坐标
                block_x = int(current_x // TILE_SIZE)
                block_y = int(current_y // TILE_SIZE)
                
                # 检查是否在世界范围内
                if 0 <= block_x < WORLD_WIDTH and 0 <= block_y < WORLD_HEIGHT:
                    block_id = self.world.get_block(block_x, block_y)
                    # 检查是否为有效方块且不是基岩或箱子
                    if block_id != 0 and block_id != BEDROCK and block_id != CHEST:
                        # 破坏方块
                        self.world.set_block(block_x, block_y, 0)
                        
                        # 生成方块掉落物
                        drop_x = block_x * TILE_SIZE + TILE_SIZE // 2
                        drop_y = block_y * TILE_SIZE + TILE_SIZE // 2
                        item_entity = ItemEntity(drop_x, drop_y, block_id, 1)
                        self.item_entities.append(item_entity)
                else:
                    break
            
            # 对路径上的生物造成伤害
            for creature in self.creatures:
                # 计算生物中心点
                creature_center_x = creature.x + creature.width // 2
                creature_center_y = creature.y + creature.height // 2
                
                # 简化的碰撞检测：检查生物是否在激光路径附近
                # 计算点到直线的距离
                # 使用公式: distance = |(y2 - y1)*px - (x2 - x1)*py + x2*y1 - y2*x1| / sqrt((y2 - y1)^2 + (x2 - x1)^2)
                numerator = abs((current_y - player_center_y) * creature_center_x - (current_x - player_center_x) * creature_center_y + current_x * player_center_y - current_y * player_center_x)
                denominator = math.sqrt((current_y - player_center_y)**2 + (current_x - player_center_x)** 2)
                
                # 避免除以零的情况
                if denominator > 0:
                    dist = numerator / denominator
                    
                    if dist < 20:  # 20像素范围内算击中
                        # 对生物造成伤害
                        creature.take_damage(laser_damage)
            
            # 记录当前活跃的激光光束（用于渲染）
            self.active_laser = {
                'start_x': laser_start_x,
                'start_y': laser_start_y,
                'end_x': current_x,
                'end_y': current_y,
                'time': pygame.time.get_ticks()  # 记录发射时间，用于控制持续时间
            }
            
            return  # 射击后不进行近战攻击
        elif weapon and weapon["item_id"] == SNIPER:
            # 狙击枪，发射子弹
            # 检查玩家是否有子弹
            has_bullet = False
            for slot in self.player.hotbar:
                if slot[0] == BULLET and slot[1] > 0:
                    has_bullet = True
                    slot[1] -= 1  # 扣除一颗子弹
                    # 如果数量变为0，清空物品ID
                    if slot[1] <= 0:
                        slot[0] = 0
                    break
            
            # 如果快捷栏没有子弹，检查背包
            if not has_bullet:
                for slot in self.player.inventory:
                    if slot[0] == BULLET and slot[1] > 0:
                        has_bullet = True
                        slot[1] -= 1  # 扣除一颗子弹
                        # 如果数量变为0，清空物品ID
                        if slot[1] <= 0:
                            slot[0] = 0
                        break
            
            if not has_bullet:
                return  # 没有子弹，无法射击
            
            # 设置狙击枪的冷却时间
            # 直接设置为2.0秒，确保有非常明显的射击间隔，符合狙击枪的特性
            self.player.attack_cooldown = 2.0
            # 确保冷却时间被正确更新，我们可以在这里打印一条调试信息
            print(f"狙击枪冷却时间设置为: {self.player.attack_cooldown}秒")
            
            # 获取鼠标位置，计算射击方向
            mx, my = pygame.mouse.get_pos()
            # 转换为世界坐标
            world_x = mx + self.camera_x
            world_y = my + self.camera_y
            
            # 计算玩家中心位置
            player_center_x = self.player.x + self.player.width // 2
            player_center_y = self.player.y + self.player.height // 2
            
            # 计算方向向量
            dx = world_x - player_center_x
            dy = world_y - player_center_y
            
            # 归一化方向向量
            distance = math.sqrt(dx * dx + dy * dy)
            if distance > 0:
                dx /= distance
                dy /= distance
            else:
                dx, dy = 1, 0  # 默认向右射击
            
            # 设置子弹速度（狙击枪子弹速度更快）
            sniper_damage = ITEMS[weapon["item_id"]]["damage"]
            # 狙击枪基础速度设置为2000，比原来的800更快
            bullet_speed = 2000
            
            # 创建子弹并添加到游戏中
            # 创建一个特殊的Arrow实例作为子弹，设置较小的重力
            bullet = Arrow(
                player_center_x,  # x坐标
                player_center_y,  # y坐标
                dx,  # 方向x（归一化）
                dy,  # 方向y（归一化）
                sniper_damage,  # 伤害
                self.player  # 所有者（玩家）
            )
            # 应用正确的子弹速度
            magnitude = math.sqrt(dx*dx + dy*dy)
            if magnitude > 0:
                bullet.velocity_x = (dx / magnitude) * bullet_speed
                bullet.velocity_y = (dy / magnitude) * bullet_speed
            else:
                bullet.velocity_x = bullet_speed
                bullet.velocity_y = 0
            
            # 修改子弹的重力属性，使其完全不下落
            bullet.gravity = 0  # 设置重力为0，使子弹直线飞行
            
            self.arrows.append(bullet)
            
            return  # 射击后不进行近战攻击
        
        # 近战攻击逻辑（原有逻辑）
        # 使用玩家的初始伤害，如果没有设置则使用默认值2
        damage = getattr(self.player, 'damage', 2)  # 玩家初始伤害或默认值
        
        # 如果有武器，使用武器伤害
        if weapon and ITEMS[weapon["item_id"]]["type"] in ["weapon", "axe", "pickaxe", "shovel"]:
            damage = ITEMS[weapon["item_id"]]["damage"]
            # 设置冷却时间（基于武器速度）
            self.player.attack_cooldown = 1.0 / ITEMS[weapon["item_id"]]["speed"]
        else:
            self.player.attack_cooldown = 1.0  # 空手冷却时间
        
        # 应用伤害加成百分比，优先使用game变量中的值（如果大于0）
        damage_bonus = getattr(self.player, 'damage_bonus', 0)
        # 检查全局game实例中是否有头盔_伤害值，且该值大于0
        if 'game' in globals() and hasattr(game, '头盔_伤害') and game.头盔_伤害 > 0:
            damage_bonus = game.头盔_伤害
        damage_bonus_factor = 1 + (damage_bonus / 100)
        damage = damage * damage_bonus_factor
        
        # 10%的概率产生暴击，造成1.5倍伤害
        is_critical = random.random() < 0.1
        if is_critical:
            damage *= 1.5
        
        # 检查范围内的生物
        cx, cy = self.player.x + self.player.width // 2, self.player.y + self.player.height // 2
        for creature in self.creatures[:]:
            tx, ty = creature.x + creature.width // 2, creature.y + creature.height // 2
            distance = math.sqrt((tx - cx) ** 2 + (ty - cy) ** 2)
            
            if distance < TILE_SIZE * INTERACTION_RANGE:  # 在交互范围内
                # 对生物造成伤害
                if creature.take_damage(damage):
                    # 创建伤害文本
                    text_x = creature.x + creature.width // 2
                    text_y = creature.y - 10  # 在生物上方显示
                    self.damage_texts.append(DamageText(text_x, text_y, damage, is_critical))
                    
                # 如果生物死亡，掉落物品并给予经验值
                    if creature.is_dead():
                        drops = creature.get_drops()
                        # 创建掉落物实体
                        for drop in drops:
                            # 在生物位置创建物品实体
                            item_entity = ItemEntity(
                                creature.x + creature.width // 2 - 12,  # 居中
                                creature.y + creature.height // 2 - 12,  # 居中
                                drop["item_id"],
                                drop["quantity"]
                            )
                            # 添加到游戏的物品实体列表
                            self.item_entities.append(item_entity)
                        
                        # 给予经验值奖励（根据生物类型决定奖励数量）
                        # 简单的经验值奖励系统：越难的生物奖励越多经验
                        if creature.type == "zombie" or creature.type == "ghost":
                            exp_reward = 10
                        elif creature.type == "fire_spirit" or creature.type == "rock_monster":
                            exp_reward = 15
                        elif creature.type == "scorpion" or creature.type == "mushroom_monster":
                            exp_reward = 20
                        else:
                            exp_reward = 5  # 其他生物
                        
                        # 添加经验值
                        stars_gained = self.player.add_experience(exp_reward)
                        
                        # 如果获得了新星星，显示信息
                        if stars_gained > 0:
                            print(f"[{time.strftime('%H:%M:%S')}] 玩家获得了{stars_gained}颗星星！")
                        
                        break
    
    def handle_right_click(self, pos):
        """处理右键点击，包括背包内物品拆分功能"""
        mx, my = pos

        # 界面交互优先
        if self.player.is_inventory_open:
            # 处理背包内右键拆分物品
            self.handle_inventory_right_click(mx, my)
            return
        elif self.player.is_crafting_open:
            return
        elif self.new_chest_manager.is_open:
            # 如果新箱子页面已打开，处理新箱子页面内的右键点击
            self.new_chest_manager.handle_click(mx, my, button=3)
            return

        # 放置方块或打开箱子/新箱子页面
        tile_x, tile_y = self.world.screen_to_tile(mx, my, self.camera_x, self.camera_y)
        player_tile_x, player_tile_y = int(self.player.x // TILE_SIZE), int(self.player.y // TILE_SIZE)

        # 检查是否在交互范围内或启用了全屏点击功能
        if (self.fullscreen_click_enabled or 
            (abs(tile_x - player_tile_x) <= INTERACTION_RANGE and
             abs(tile_y - player_tile_y) <= INTERACTION_RANGE)):

            block_id = self.world.get_block(tile_x, tile_y)

            if block_id == CHEST:
                # 右键点击箱子方块时，打开新箱子页面，并传递箱子坐标
                self.new_chest_manager.open_page(tile_x, tile_y)
                # 关闭其他界面
                self.player.is_inventory_open = False
                self.player.is_crafting_open = False
                self.player.is_chest_open = False
                self.player.current_chest = None
                self.show_controls = False
                self.is_advanced_menu_open = False
                self.is_creative_inventory_open = False
                # 记录输入日志
                print(f"[{time.strftime('%H:%M:%S')}] 玩家右键点击箱子方块，打开新箱子页面")
            else:
                # 放置方块
                selected_item = self.player.get_selected_item()
                if selected_item:
                    item_info = ITEMS.get(selected_item["item_id"])
                    if item_info and item_info["type"] == "block":
                        block_id_to_place = item_info["block_id"]
                        
                        # 检查是否可以放置方块
                        current_block = self.world.blocks[tile_y][tile_x]
                        can_place = False

                        # 对于水和岩浆的特殊处理：可以替换火把、红花和草
                        if block_id_to_place in [WATER, LAVA]:
                            if self.world.is_within_bounds(tile_x, tile_y) and current_block in [AIR, WATER, LAVA, TORCH, RED_FLOWER, GRASS_PLANT]:
                                can_place = True
                        # 普通方块放置条件
                        elif self.world.is_within_bounds(tile_x, tile_y) and current_block in [AIR, WATER, LAVA, STONE_BOTTOM]:
                            can_place = True

                        # 如果可以放置方块
                        if can_place:
                            # 检查是否启用了3*3放置功能
                            if hasattr(self, 'area_place_enabled') and self.area_place_enabled:
                                # 3*3放置，物品只减少1个
                                # 先尝试移除物品
                                if self.player.remove_item(selected_item["item_id"], 1):
                                    # 获取3*3区域内的所有方块位置
                                    for dy in [-1, 0, 1]:
                                        for dx in [-1, 0, 1]:
                                            # 计算当前要放置的方块位置
                                            area_tile_x = tile_x + dx
                                            area_tile_y = tile_y + dy
                                              
                                            # 检查位置是否在世界范围内
                                            if not self.world.is_within_bounds(area_tile_x, area_tile_y):
                                                continue
                                              
                                            # 检查是否在交互范围内或启用了全屏点击功能
                                            area_player_tile_x, area_player_tile_y = int(self.player.x // TILE_SIZE), int(self.player.y // TILE_SIZE)
                                            if not self.fullscreen_click_enabled and (abs(area_tile_x - area_player_tile_x) > INTERACTION_RANGE or
                                                    abs(area_tile_y - area_player_tile_y) > INTERACTION_RANGE):
                                                continue
                                         
                                            # 检查方块是否可以放置在这个位置
                                            area_current_block = self.world.blocks[area_tile_y][area_tile_x]
                                            area_can_place = False
                                         
                                            # 对于水和岩浆的特殊处理
                                            if block_id_to_place in [WATER, LAVA]:
                                                if area_current_block in [AIR, WATER, LAVA, TORCH, RED_FLOWER, GRASS_PLANT]:
                                                    area_can_place = True
                                            # 普通方块放置条件
                                            elif area_current_block in [AIR, WATER, LAVA, STONE_BOTTOM]:
                                                area_can_place = True
                                         
                                            # 特殊方块的支撑检查
                                            if area_can_place and (block_id_to_place == TORCH or block_id_to_place == CACTUS or 
                                                                block_id_to_place == GRASS_PLANT or block_id_to_place == RED_FLOWER or block_id_to_place == DRY_GRASS):
                                                if area_tile_y + 1 >= WORLD_HEIGHT or self.world.blocks[area_tile_y + 1][area_tile_x] == AIR:
                                                    area_can_place = False
                                         
                                            # 放置方块
                                            if area_can_place:
                                                if block_id_to_place == STONE:
                                                    # 放置岩石并标记为玩家放置
                                                    self.world.set_block(area_tile_x, area_tile_y, STONE)
                                                    if not hasattr(self.world, 'player_placed_blocks'):
                                                        self.world.player_placed_blocks = set()
                                                    self.world.player_placed_blocks.add((area_tile_x, area_tile_y))
                                                else:
                                                    # 其他方块正常放置
                                                    self.world.set_block(area_tile_x, area_tile_y, block_id_to_place)
                                                    # 标记矿石类方块为玩家放置的
                                                    if block_id_to_place in [IRON_ORE, GOLD_ORE, DIAMOND_ORE, COPPER_ORE]:
                                                        if not hasattr(self.world, 'player_placed_blocks'):
                                                            self.world.player_placed_blocks = set()
                                                        self.world.player_placed_blocks.add((area_tile_x, area_tile_y))
                                         
                                                # 检查玩家是否与刚放置的方块位置重叠
                                                player_tile_x = int(self.player.x // TILE_SIZE)
                                            player_tile_y = int(self.player.y // TILE_SIZE)
                                            if player_tile_x == area_tile_x and player_tile_y == area_tile_y:
                                                # 将玩家位置向上移动三格（避免卡在方块内）
                                                self.player.y -= TILE_SIZE * 3
                            # 普通放置模式 - 放置在3*3功能检查的else分支中
                            else:
                                # 火把、仙人掌、草和花特殊处理：必须下面有方块才能放置
                                if block_id_to_place == TORCH or block_id_to_place == CACTUS or block_id_to_place == GRASS_PLANT or block_id_to_place == RED_FLOWER or block_id_to_place == DRY_GRASS:
                                    # 检查下方是否有方块支撑
                                    if tile_y + 1 < WORLD_HEIGHT and self.world.blocks[tile_y + 1][tile_x] != AIR:
                                        # 只有成功移除物品后才放置方块
                                        if self.player.remove_item(selected_item["item_id"], 1):
                                            self.world.set_block(tile_x, tile_y, block_id_to_place)
                                else:
                                    # 玩家放置的岩石和矿石方块特殊处理
                                    if block_id_to_place == STONE:
                                        # 先尝试移除物品，成功后才放置方块
                                        if self.player.remove_item(selected_item["item_id"], 1):
                                            # 放置岩石时仍使用STONE，但添加标记表示是玩家放置的
                                            self.world.set_block(tile_x, tile_y, STONE)
                                            # 标记为玩家放置的方块
                                            if not hasattr(self.world, 'player_placed_blocks'):
                                                self.world.player_placed_blocks = set()
                                            self.world.player_placed_blocks.add((tile_x, tile_y))
                                    else:
                                        # 先尝试移除物品，成功后才放置方块
                                        if self.player.remove_item(selected_item["item_id"], 1):
                                            # 其他方块正常放置
                                            self.world.set_block(tile_x, tile_y, block_id_to_place)
                                            # 标记矿石类方块为玩家放置的
                                            if block_id_to_place in [IRON_ORE, GOLD_ORE, DIAMOND_ORE, COPPER_ORE]:
                                                if not hasattr(self.world, 'player_placed_blocks'):
                                                    self.world.player_placed_blocks = set()
                                                self.world.player_placed_blocks.add((tile_x, tile_y))
                                            # 如果是箱子，还需要创建Chest对象
                                            if block_id_to_place == CHEST:
                                                chest_x = tile_x * TILE_SIZE
                                                chest_y = tile_y * TILE_SIZE
                                                # 玩家放置的箱子不自动生成物品，设为generate_loot=False
                                                self.world.chests.append(Chest(chest_x, chest_y, generate_loot=False))
                                                # 将箱子坐标添加到玩家放置的箱子集合中
                                                self.world.player_placed_chests.add((tile_x, tile_y))
                                
                                # 检查玩家是否与刚放置的方块位置重叠
                                player_tile_x = int(self.player.x // TILE_SIZE)
                                player_tile_y = int(self.player.y // TILE_SIZE)
                                # 如果玩家位置与刚放置的方块位置相同
                                if player_tile_x == tile_x and player_tile_y == tile_y:
                                    # 将玩家位置向上移动三格（避免卡在方块内）
                                    self.player.y -= TILE_SIZE * 3

    def handle_inventory_click(self, mx, my, right_click=False):
        """处理背包点击，支持物品拖放和交换，以及箱子交互"""
        mouse_x, mouse_y = mx, my
        
        # 检查是否显示了丢弃数量选择界面
        if hasattr(self, 'show_drop_quantity_input') and self.show_drop_quantity_input and hasattr(self, 'drop_quantity_rect'):
            # 处理滑块交互
            if "slider" in self.drop_quantity_rect and self.drop_quantity_rect["slider"].collidepoint(mouse_x, mouse_y):
                # 获取物品的最大数量
                max_quantity = 0
                # 计算背包中的物品总数量
                for item in self.player.inventory:
                    if item[0] == self.item_to_drop:
                        max_quantity += item[1]
                # 计算快捷栏中的物品总数量
                for item in self.player.hotbar:
                    if item[0] == self.item_to_drop:
                        max_quantity += item[1]
                if max_quantity > 0:
                    # 计算滑块轨道的边界
                    slider_x = self.drop_quantity_rect["slider"].x
                    slider_width = self.drop_quantity_rect["slider"].width - 30  # 减去旋钮半径*2
                    
                    # 计算点击位置对应的数量值
                    click_pos = min(max(mouse_x - slider_x, 0), slider_width)
                    percentage = click_pos / slider_width
                    new_quantity = max(1, int(percentage * max_quantity) + 1 if percentage * max_quantity % 1 >= 0.5 else int(percentage * max_quantity))
                    self.quantity_to_drop = min(max_quantity, new_quantity)
                return
            # 处理-按钮点击
            if "minus" in self.drop_quantity_rect and self.drop_quantity_rect["minus"].collidepoint(mouse_x, mouse_y):
                # 获取物品的最大数量
                max_quantity = 0
                # 计算背包中的物品总数量
                for item in self.player.inventory:
                    if item[0] == self.item_to_drop:
                        max_quantity += item[1]
                # 计算快捷栏中的物品总数量
                for item in self.player.hotbar:
                    if item[0] == self.item_to_drop:
                        max_quantity += item[1]
                self.quantity_to_drop = max(1, self.quantity_to_drop - 1)
                return
            # 处理+按钮点击
            elif "plus" in self.drop_quantity_rect and self.drop_quantity_rect["plus"].collidepoint(mouse_x, mouse_y):
                # 获取物品的最大数量
                max_quantity = 0
                # 计算背包中的物品总数量
                for item in self.player.inventory:
                    if item[0] == self.item_to_drop:
                        max_quantity += item[1]
                # 计算快捷栏中的物品总数量
                for item in self.player.hotbar:
                    if item[0] == self.item_to_drop:
                        max_quantity += item[1]
                self.quantity_to_drop = min(max_quantity, self.quantity_to_drop + 1)
                return
            # 处理确认按钮点击
            elif self.drop_quantity_rect["confirm"].collidepoint(mouse_x, mouse_y):
                # 确保数量在有效范围内
                max_quantity = 0
                # 计算背包中的物品总数量
                for item in self.player.inventory:
                    if item[0] == self.item_to_drop:
                        max_quantity += item[1]
                # 计算快捷栏中的物品总数量
                for item in self.player.hotbar:
                    if item[0] == self.item_to_drop:
                        max_quantity += item[1]
                self.quantity_to_drop = max(1, min(max_quantity, self.quantity_to_drop))
                
                # 从玩家背包中移除指定数量的物品
                if self.item_to_drop:
                    # 获取物品名称用于日志
                    item_info = ITEMS.get(self.item_to_drop, {'name': '未知物品'})
                    # 移除物品
                    self.player.remove_item(self.item_to_drop, self.quantity_to_drop)
                    print(f"[{time.strftime('%H:%M:%S')}] 玩家丢弃了 {item_info['name']} × {self.quantity_to_drop}")
                    
                    # 如果物品数量为0，更新快捷栏
                    if not self.player.has_item(self.item_to_drop):
                        selected_slot = self.player.selected_slot
                        if self.player.hotbar[selected_slot] == self.item_to_drop:
                            self.player.hotbar[selected_slot] = 0
                
                # 重置状态
                self.show_drop_quantity_input = False
                self.item_to_drop = None
                self.quantity_to_drop = 1
                return
            # 处理全部丢弃按钮点击
            elif "drop_all" in self.drop_quantity_rect and self.drop_quantity_rect["drop_all"].collidepoint(mouse_x, mouse_y):
                # 获取物品的最大数量并设置为丢弃数量
                max_quantity = 0
                # 计算背包中的物品总数量
                for item in self.player.inventory:
                    if item[0] == self.item_to_drop:
                        max_quantity += item[1]
                # 计算快捷栏中的物品总数量
                for item in self.player.hotbar:
                    if item[0] == self.item_to_drop:
                        max_quantity += item[1]
                self.quantity_to_drop = max(1, max_quantity)
                # 立即执行丢弃操作
                if self.item_to_drop:
                    # 获取物品名称用于日志
                    item_info = ITEMS.get(self.item_to_drop, {'name': '未知物品'})
                    # 移除物品
                    self.player.remove_item(self.item_to_drop, self.quantity_to_drop)
                    print(f"[{time.strftime('%H:%M:%S')}] 玩家丢弃了全部 {item_info['name']} × {self.quantity_to_drop}")
                    
                    # 如果物品数量为0，更新快捷栏
                    if not self.player.has_item(self.item_to_drop):
                        selected_slot = self.player.selected_slot
                        if self.player.hotbar[selected_slot] == self.item_to_drop:
                            self.player.hotbar[selected_slot] = 0
                
                # 重置状态
                self.show_drop_quantity_input = False
                self.item_to_drop = None
                self.quantity_to_drop = 1
                return
            # 处理取消按钮点击
            elif self.drop_quantity_rect["cancel"].collidepoint(mouse_x, mouse_y):
                
                # 重置状态
                self.show_drop_quantity_input = False
                self.item_to_drop = None
                self.quantity_to_drop = 1
                return
            # 点击背景以外区域关闭
            elif not self.drop_quantity_rect["background"].collidepoint(mouse_x, mouse_y):
                
                self.show_drop_quantity_input = False
                self.item_to_drop = None
                self.quantity_to_drop = 1
                return
        
        # 设置界面参数
        slot_size = 40
        slot_margin = 5
        hotbar_size = len(self.player.hotbar)  # 8格快捷栏
        backpack_size = self.player.backpack_slots  # 30格背包
        chest_rows = 5
        chest_cols = 4
        
        # 根据是否打开箱子调整UI参数
        if self.player.is_chest_open and self.player.current_chest:
            # 如果只打开箱子，使用单独的更紧凑尺寸420x400
            if not self.player.is_inventory_open:
                inv_width = 420
                inv_height = 400
            else:
                # 同时打开背包和箱子时，使用原来的布局
                inv_width = 700
                inv_height = 500
        else:
            # 普通背包界面
            inv_width = 580  # 与draw_inventory函数中的尺寸保持一致
            inv_height = 410  # 与draw_inventory函数中的尺寸保持一致
            equipment_area_width = 180
        
        # 先计算inv_x和inv_y
        inv_x = (WIDTH - inv_width) // 2
        inv_y = (HEIGHT - inv_height) // 2
        
        # 计算箱子区域（如果打开了箱子）
        chest_rect = None
        chest_start_x = None
        chest_start_y = None
        if self.player.is_chest_open and self.player.current_chest:
            if not self.player.is_inventory_open:
                # 只打开箱子时，内容居中显示
                chest_content_width = chest_cols * (slot_size + slot_margin)
                chest_start_x = inv_x + (inv_width - chest_content_width) // 2
                chest_start_y = inv_y + 60  # 留出标题空间
            else:
                # 同时打开背包和箱子时，使用原来的布局
                chest_start_x = inv_x + 50 # 与draw_inventory函数中的值保持一致
                chest_start_y = inv_y + 50 # 与draw_inventory函数中的值保持一致
            
            chest_rect = pygame.Rect(chest_start_x, chest_start_y, 
                                   chest_cols * (slot_size + slot_margin), chest_rows * (slot_size + slot_margin))
        
        # 计算快捷栏区域 - 与draw_inventory函数中的位置保持一致
        hotbar_start_x = inv_x + 80
        hotbar_start_y = inv_y + inv_height - 80
        hotbar_rect = pygame.Rect(hotbar_start_x, hotbar_start_y, 
                                 hotbar_size * (slot_size + slot_margin), slot_size)
        
        # 计算背包区域 - 始终显示背包和快捷栏以便交互
        rows = 5
        cols = 6
        backpack_start_x = None
        backpack_start_y = None
        backpack_rect = None
        
        # 确保背包始终绘制以方便交互
        if self.player.is_inventory_open or self.player.is_chest_open and self.player.current_chest:
            if self.player.is_chest_open and self.player.current_chest:
                backpack_start_x = inv_x + inv_width - 50 - 6 * (40 + 5)
                backpack_start_y = inv_y + 50
            else:
                # 与draw_inventory函数中的背包起始位置保持一致
                backpack_start_x = inv_x + 251
                backpack_start_y = inv_y + 58
            
            backpack_rect = pygame.Rect(backpack_start_x, backpack_start_y, 
                                       cols * (slot_size + slot_margin), rows * (slot_size + slot_margin))
        
        # 计算装备区域（仅在普通背包界面中显示）
        equipment_rects = {}  # 存储各个装备槽的矩形区域
        if not self.player.is_chest_open or not self.player.current_chest:
            # 装备区域位置 - 与draw_inventory函数中的位置保持一致
            equipment_area_x = inv_x + 30
            equipment_area_y = inv_y + 58
            
            # 定义各个装备槽的位置和尺寸（56x56像素的装备槽）
            slot_size_equipment = 56
            slot_margin_equipment = 10
            
            # 头盔槽
            equipment_rects['helmet'] = pygame.Rect(
                equipment_area_x + 40, equipment_area_y + 20,
                slot_size_equipment, slot_size_equipment
            )
            
            # 盔甲槽
            equipment_rects['armor'] = pygame.Rect(
                equipment_area_x + 110, equipment_area_y + 20,
                slot_size_equipment, slot_size_equipment
            )
            
            # 靴子槽
            equipment_rects['boots'] = pygame.Rect(
                equipment_area_x + 40, equipment_area_y + 85,
                slot_size_equipment, slot_size_equipment
            )
            
            # 特殊装备槽
            equipment_rects['special'] = pygame.Rect(
                equipment_area_x + 110, equipment_area_y + 85,
                slot_size_equipment, slot_size_equipment
            )
        
        # 计算箱子区域（如果打开了箱子）
        chest_rect = None
        if self.player.is_chest_open and self.player.current_chest:
            chest_rect = pygame.Rect(chest_start_x, chest_start_y, 
                                   chest_cols * (slot_size + slot_margin), chest_rows * (slot_size + slot_margin))
        
        # 计算销毁区域（在普通背包界面中显示）- 与draw_inventory函数中的位置和尺寸保持一致
        destroy_rect = None
        if not self.player.is_chest_open or not self.player.current_chest:
            destroy_area_x = inv_x + 460
            destroy_area_y = inv_y + 340
            destroy_area_size = 50
            destroy_rect = pygame.Rect(destroy_area_x, destroy_area_y, destroy_area_size, destroy_area_size)
        
        # 检查是否点击了装备区域
        is_in_equipment = False
        clicked_equipment_slot = None
        if equipment_rects:
            for slot_type, rect in equipment_rects.items():
                if rect.collidepoint(mouse_x, mouse_y):
                    is_in_equipment = True
                    clicked_equipment_slot = slot_type
                    break
                
        # 检查是否点击了背包区域或箱子区域或销毁区域或装备区域
        if self.player.is_chest_open and self.player.current_chest:
            is_in_ui = (hotbar_rect.collidepoint(mouse_x, mouse_y) or 
                       (backpack_rect and backpack_rect.collidepoint(mouse_x, mouse_y)) or 
                       chest_rect.collidepoint(mouse_x, mouse_y))
        else:
            is_in_ui = (hotbar_rect.collidepoint(mouse_x, mouse_y) or 
                       (backpack_rect and backpack_rect.collidepoint(mouse_x, mouse_y)) or
                       (destroy_rect and destroy_rect.collidepoint(mouse_x, mouse_y)) or
                       is_in_equipment)
        
        if not is_in_ui:
            # 如果点击了UI外的区域且正在拖动物品，取消拖动
            if self.player.dragging_item:
                self.player.dragging_item = None
                self.player.dragging_source = None
                self.player.dragging_slot = None
                self.player.is_split_dragging = False  # 重置右键拆分拖动标记
                self.player.is_split_dragging = False  # 重置右键拆分拖动标记
            return
            
        # 检查是否点击了销毁区域
        if destroy_rect and destroy_rect.collidepoint(mouse_x, mouse_y):
            if self.player.dragging_item:
                # 获取要销毁的物品信息
                dragged_item_id = self.player.dragging_item["item_id"]
                
                # 显示数量选择界面，而不是直接销毁
                if not hasattr(self, 'show_drop_quantity_input'):
                    self.show_drop_quantity_input = False
                    self.item_to_drop = None
                    self.quantity_to_drop = 1
                    self.drop_quantity_rect = {}
                
                self.show_drop_quantity_input = True
                self.item_to_drop = dragged_item_id
                # 默认丢弃1个物品
                self.quantity_to_drop = 1
                
                # 重置拖动状态
                self.player.dragging_item = None
                self.player.dragging_source = None
                self.player.dragging_slot = None
                self.player.is_split_dragging = False  # 重置右键拆分拖动标记
            else:
                # 如果没有拖动物品，检查是否有选中的物品可以丢弃
                selected_item_id = self.player.hotbar[self.player.selected_slot]
                if selected_item_id != 0 and self.player.has_item(selected_item_id):
                    # 显示数量选择界面
                    if not hasattr(self, 'show_drop_quantity_input'):
                        self.show_drop_quantity_input = False
                        self.item_to_drop = None
                        self.quantity_to_drop = 1
                        self.drop_quantity_rect = {}
                    
                    self.show_drop_quantity_input = True
                    self.item_to_drop = selected_item_id
                    self.quantity_to_drop = 1
            return
        
        # 检查是否点击了装备槽
        if is_in_equipment and clicked_equipment_slot:
            # 获取点击的装备槽类型
            slot_type = clicked_equipment_slot
            
            # 当前装备槽中的物品
            current_equipment_id = self.player.equipment.get(slot_type, 0)
            
            # 如果正在拖动物品
            if self.player.dragging_item:
                dragged_item_id = self.player.dragging_item["item_id"]
                dragged_quantity = self.player.dragging_item["quantity"]
                
                # 检查物品是否是装备类型
                item_info = ITEMS.get(dragged_item_id, {})
                item_type = item_info.get('type', '')
                
                # 根据装备槽类型验证物品是否可以装备
                can_equip = False
                if slot_type == 'helmet' and item_type == 'helmet':
                    can_equip = True
                elif slot_type == 'armor' and item_type == 'armor':
                    can_equip = True
                elif slot_type == 'boots' and item_type == 'boots':
                    can_equip = True
                elif slot_type == 'special' and item_type == 'special':
                    can_equip = True
                
                if can_equip:
                    # 尝试装备物品
                    # 如果装备槽已有装备，先尝试放入背包
                    if current_equipment_id != 0:
                        # 尝试将当前装备放入背包
                        if self.player.add_item(current_equipment_id, 1):
                            # 背包有空位，成功放入，然后装备新物品
                            self.player.equip_item(slot_type, dragged_item_id)
                            
                            # 从拖动来源移除物品
                            if not self.player.is_split_dragging:
                                if self.player.dragging_source == "hotbar":
                                    source_slot = self.player.dragging_slot
                                    self.player.hotbar[source_slot] = [0, 0]
                                elif self.player.dragging_source == "inventory":
                                    source_slot = self.player.dragging_slot
                                    self.player.inventory[source_slot] = [0, 0]
                            
                            # 重置拖动状态
                            self.player.dragging_item = None
                            self.player.dragging_source = None
                            self.player.dragging_slot = None
                            self.player.is_split_dragging = False
                    else:
                        # 装备槽为空，直接装备物品
                        self.player.equip_item(slot_type, dragged_item_id)
                        
                        # 从拖动来源移除物品
                        if not self.player.is_split_dragging:
                            if self.player.dragging_source == "hotbar":
                                source_slot = self.player.dragging_slot
                                self.player.hotbar[source_slot] = [0, 0]
                            elif self.player.dragging_source == "inventory":
                                source_slot = self.player.dragging_slot
                                self.player.inventory[source_slot] = [0, 0]
                        
                        # 重置拖动状态
                        self.player.dragging_item = None
                        self.player.dragging_source = None
                        self.player.dragging_slot = None
                        self.player.is_split_dragging = False
            # 如果没有拖动物品，但装备槽有装备
            elif current_equipment_id != 0:
                # 尝试脱下装备并放入背包
                if self.player.add_item(current_equipment_id, 1):
                    # 背包有空位，脱下装备
                    self.player.equipment[slot_type] = 0
                    self.player.update_equipment_bonuses()
        
        # 检查是否点击了箱子格子（如果打开了箱子）
        if chest_rect and chest_rect.collidepoint(mouse_x, mouse_y):
            # 计算点击的箱子槽位索引
            chest_rows = 5
            chest_cols = 4
            slot_idx = ((mouse_y - chest_start_y) // (slot_size + slot_margin)) * chest_cols + \
                      ((mouse_x - chest_start_x) // (slot_size + slot_margin))
            
            # 确保索引在有效范围内
            if 0 <= slot_idx < len(self.player.current_chest.items):
                chest_item = self.player.current_chest.items[slot_idx]
                chest_item_id, chest_item_count = chest_item
                
                # 如果当前没有在拖动任何物品，且点击的槽位有物品
                if not self.player.dragging_item and chest_item_id != 0:
                    # 开始拖动物品
                    self.player.dragging_item = {"item_id": chest_item_id, "quantity": chest_item_count}
                    self.player.dragging_source = "chest"
                    self.player.dragging_slot = slot_idx
                    self.player.is_split_dragging = False  # 标记为左键拖动整个物品
                # 如果当前正在拖动物品
                elif self.player.dragging_item:
                    dragged_item_id = self.player.dragging_item["item_id"]
                    dragged_quantity = self.player.dragging_item["quantity"]
                    
                    # 如果目标槽位为空
                    if chest_item_id == 0:
                        # 将拖动的物品放入空槽位
                        self.player.current_chest.items[slot_idx] = [dragged_item_id, dragged_quantity]
                        
                        # 根据拖动类型决定是否清空原槽位
                        if not self.player.is_split_dragging:
                            if self.player.dragging_source == "hotbar":
                                source_slot = self.player.dragging_slot
                                self.player.hotbar[source_slot] = [0, 0]
                            elif self.player.dragging_source == "inventory":
                                source_slot = self.player.dragging_slot
                                self.player.inventory[source_slot] = [0, 0]
                            elif self.player.dragging_source == "chest":
                                source_slot = self.player.dragging_slot
                                self.player.current_chest.items[source_slot] = [0, 0]
                        
                        # 不需要立即重置拖动状态，让系统统一处理
                        pass
                    else:
                        # 检查物品是否相同
                        if dragged_item_id == chest_item_id:
                            # 物品相同，合并数量
                            new_count = dragged_quantity + chest_item_count
                            
                            # 检查是否超过堆叠上限（假设99为上限）
                            if new_count <= 99:
                                # 完全合并，更新目标格子数量
                                self.player.current_chest.items[slot_idx] = [chest_item_id, new_count]
                                
                                # 清空或更新原槽位
                                if not self.player.is_split_dragging:
                                    if self.player.dragging_source == "hotbar":
                                        source_slot = self.player.dragging_slot
                                        self.player.hotbar[source_slot] = [0, 0]
                                    elif self.player.dragging_source == "inventory":
                                        source_slot = self.player.dragging_slot
                                        self.player.inventory[source_slot] = [0, 0]
                                    elif self.player.dragging_source == "chest":
                                        source_slot = self.player.dragging_slot
                                        self.player.current_chest.items[source_slot] = [0, 0]
                                
                                # 重置拖动状态
                                self.player.dragging_item = None
                                self.player.dragging_source = None
                                self.player.dragging_slot = None
                                self.player.is_split_dragging = False
        
        # 检查是否点击了快捷栏
        elif hotbar_rect.collidepoint(mouse_x, mouse_y):
            # 计算点击的槽位索引
            slot_idx = (mouse_x - hotbar_start_x) // (slot_size + slot_margin)
            if 0 <= slot_idx < hotbar_size:
                item_id, count = self.player.hotbar[slot_idx]
                
                # 如果当前没有在拖动任何物品，且点击的槽位有物品
                if not self.player.dragging_item and item_id != 0 and self.player.has_item(item_id):
                    # 开始拖动物品
                    self.player.dragging_item = {"item_id": item_id, "quantity": count}
                    self.player.dragging_source = "hotbar"
                    self.player.dragging_slot = slot_idx
                    self.player.is_split_dragging = False  # 标记为左键拖动整个物品
                # 如果当前正在拖动物品
                elif self.player.dragging_item:
                    dragged_item_id = self.player.dragging_item["item_id"]
                    dragged_quantity = self.player.dragging_item["quantity"]
                    
                    target_item = self.player.hotbar[slot_idx]
                    target_id, target_count = target_item
                    
                    # 如果目标槽位为空
                    if target_id == 0:
                        # 将拖动的物品放入空槽位
                        self.player.hotbar[slot_idx] = [dragged_item_id, dragged_quantity]
                        
                        # 根据拖动类型决定是否清空原槽位
                        # 如果是右键拆分的物品拖动，我们不需要清空原槽位
                        # 如果是左键拖动整个物品，我们需要清空原槽位
                        if not self.player.is_split_dragging:
                            if self.player.dragging_source == "hotbar":
                                source_slot = self.player.dragging_slot
                                self.player.hotbar[source_slot] = [0, 0]
                            elif self.player.dragging_source == "inventory":
                                source_slot = self.player.dragging_slot
                                self.player.inventory[source_slot] = [0, 0]
                    else:
                        # 检查物品是否相同
                        if dragged_item_id == target_id:
                            # 物品相同，合并数量
                            new_count = dragged_quantity + target_count
                            
                            # 检查是否超过堆叠上限（假设99为上限）
                            if new_count <= 99:
                                # 完全合并，更新目标格子数量
                                self.player.hotbar[slot_idx] = [target_id, new_count]
                                
                                # 清空或更新原槽位
                                if not self.player.is_split_dragging:
                                    if self.player.dragging_source == "hotbar":
                                        source_slot = self.player.dragging_slot
                                        self.player.hotbar[source_slot] = [0, 0]
                                    elif self.player.dragging_source == "inventory":
                                        source_slot = self.player.dragging_slot
                                        self.player.inventory[source_slot] = [0, 0]
                            else:
                                # 部分合并，目标格子设为99，剩余数量返回原槽位
                                self.player.hotbar[slot_idx] = [target_id, 99]
                                remaining_count = new_count - 99
                                
                                # 更新原槽位剩余数量
                                if self.player.dragging_source == "hotbar":
                                    source_slot = self.player.dragging_slot
                                    self.player.hotbar[source_slot] = [target_id, remaining_count]
                                elif self.player.dragging_source == "inventory":
                                    source_slot = self.player.dragging_slot
                                    self.player.inventory[source_slot] = [target_id, remaining_count]
                        else:
                            # 物品不同，交换物品
                            self.player.hotbar[slot_idx] = [dragged_item_id, dragged_quantity]
                            
                            # 处理来源槽位
                            if self.player.dragging_source == "hotbar":
                                source_slot = self.player.dragging_slot
                                self.player.hotbar[source_slot] = [target_id, target_count]
                            elif self.player.dragging_source == "inventory":
                                source_slot = self.player.dragging_slot
                                self.player.inventory[source_slot] = [target_id, target_count]
                    
                    # 重置拖动状态
                    self.player.dragging_item = None
                    self.player.dragging_source = None
                    self.player.dragging_slot = None
                    self.player.is_split_dragging = False  # 重置右键拆分拖动标记
                    self.player.is_split_dragging = False  # 重置右键拆分拖动标记
        
        # 检查是否点击了背包格子
        elif backpack_rect.collidepoint(mouse_x, mouse_y):
            # 根据界面类型设置不同的计算基准
            if self.player.is_chest_open and self.player.current_chest:
                # 箱子界面：使用原始起始位置
                calc_x = backpack_start_x
                calc_y = backpack_start_y
            else:
                # 普通背包界面：使用考虑了15px边距的起始位置
                calc_x = backpack_start_x - 15
                calc_y = backpack_start_y - 15
            
            # 确保计算方式与渲染时完全一致
            try:
                col = (mouse_x - calc_x) // (slot_size + slot_margin)
                row = (mouse_y - calc_y) // (slot_size + slot_margin)
                
                # 确保行列值在有效范围内
                if 0 <= row < rows and 0 <= col < cols:
                    # 计算索引：确保与渲染时的计算顺序完全一致
                    slot_idx = row * cols + col
                else:
                    slot_idx = -1  # 超出范围，无效索引
            except:
                col = 0
                row = 0
                slot_idx = -1  # 发生异常，使用无效索引
            
            # 如果索引无效，直接返回
            if slot_idx == -1:
                return
            
            if 0 <= slot_idx < backpack_size:
                # 获取背包中的物品列表（除快捷栏外的物品）
                backpack_items = []
                # 提取hotbar中的物品ID列表用于比较
                hotbar_item_ids = [item[0] for item in self.player.hotbar if item[0] != 0]
                # 遍历inventory列表中的每个物品
                for item in self.player.inventory:
                    item_id, count = item
                    if item_id != 0 and item_id not in hotbar_item_ids:
                        backpack_items.append((item_id, count))
                
                # 确保列表长度为30，不足的用None填充
                while len(backpack_items) < backpack_size:
                    backpack_items.append(None)
                
                # 获取目标背包格子的物品
                target_item = self.player.inventory[slot_idx]
                target_id, target_count = target_item
                
                # 如果当前没有在拖动任何物品，且点击的格子有物品
                if not self.player.dragging_item and target_id != 0:
                    # 开始拖动物品
                    self.player.dragging_item = {"item_id": target_id, "quantity": target_count}
                    self.player.dragging_source = "inventory"
                    self.player.dragging_slot = slot_idx
                    self.player.is_split_dragging = False  # 标记为左键拖动整个物品
                # 如果当前正在拖动物品
                elif self.player.dragging_item:
                    # 检查是否点击的是正在拖动的物品的原槽位
                    if (self.player.dragging_source == "inventory" and slot_idx == self.player.dragging_slot):
                        # 取消拖动状态，不进行其他操作
                        self.player.dragging_item = None
                        self.player.dragging_source = None
                        self.player.dragging_slot = None
                        self.player.is_split_dragging = False
                        return
                    
                    dragged_item_id = self.player.dragging_item["item_id"]
                    dragged_quantity = self.player.dragging_item["quantity"]
                    
                    # 如果目标格子为空
                    if target_id == 0:
                        # 将拖动的物品放入空槽位
                        self.player.inventory[slot_idx] = [dragged_item_id, dragged_quantity]
                        
                        # 根据拖动类型决定是否清空原槽位
                        # 如果是右键拆分的物品拖动，我们不需要清空原槽位
                        # 如果是左键拖动整个物品，我们需要清空原槽位
                        if not self.player.is_split_dragging:
                            if self.player.dragging_source == "hotbar":
                                source_slot = self.player.dragging_slot
                                self.player.hotbar[source_slot] = [0, 0]
                            elif self.player.dragging_source == "inventory":
                                source_slot = self.player.dragging_slot
                                self.player.inventory[source_slot] = [0, 0]
                    else:
                        # 检查物品是否相同
                        if dragged_item_id == target_id:
                            # 物品相同，合并数量
                            new_count = dragged_quantity + target_count
                            
                            # 检查物品是否为装备类物品（限制堆叠上限为1）
                            is_equipment = False
                            if 'ITEMS' in globals() and dragged_item_id in ITEMS:
                                item_info = ITEMS[dragged_item_id]
                                if 'type' in item_info and item_info['type'] in ['weapon', 'pickaxe', 'axe', 'shovel', 'helmet', 'armor', 'boots', 'special']:
                                    is_equipment = True
                            
                            # 设置堆叠上限：装备类物品为1，其他物品为99
                            max_stack = 1 if is_equipment else 99
                            
                            # 检查是否超过堆叠上限
                            if new_count <= max_stack:
                                # 完全合并，更新目标格子数量
                                self.player.inventory[slot_idx] = [target_id, new_count]
                                
                                # 清空或更新原槽位
                                if not self.player.is_split_dragging:
                                    if self.player.dragging_source == "hotbar":
                                        source_slot = self.player.dragging_slot
                                        self.player.hotbar[source_slot] = [0, 0]
                                    elif self.player.dragging_source == "inventory":
                                        source_slot = self.player.dragging_slot
                                        self.player.inventory[source_slot] = [0, 0]
                            else:
                                # 部分合并，根据物品类型设置不同的堆叠上限
                                # 目标格子设为最大堆叠数量
                                self.player.inventory[slot_idx] = [target_id, max_stack]
                                # 计算剩余数量
                                remaining_count = new_count - max_stack
                                
                                # 更新原槽位剩余数量
                                if self.player.dragging_source == "hotbar":
                                    source_slot = self.player.dragging_slot
                                    self.player.hotbar[source_slot] = [target_id, remaining_count]
                                elif self.player.dragging_source == "inventory":
                                    source_slot = self.player.dragging_slot
                                    self.player.inventory[source_slot] = [target_id, remaining_count]
                        else:
                            # 物品不同，交换物品
                            self.player.inventory[slot_idx] = [dragged_item_id, dragged_quantity]
                            
                            # 如果拖动来源是快捷栏，将交换的物品放入快捷栏
                            if self.player.dragging_source == "hotbar":
                                source_slot = self.player.dragging_slot
                                self.player.hotbar[source_slot] = [target_id, target_count]
                            # 如果拖动来源是另一个背包格子，交换物品
                            elif self.player.dragging_source == "inventory":
                                source_slot = self.player.dragging_slot
                                self.player.inventory[source_slot] = [target_id, target_count]
                    
                    # 重置拖动状态
                    self.player.dragging_item = None
                    self.player.dragging_source = None
                    self.player.dragging_slot = None
                    self.player.is_split_dragging = False  # 重置右键拆分拖动标记

    def handle_inventory_right_click(self, mx, my):
        """处理背包内右键点击，优先实现右键装备功能，然后是物品拆分功能"""
        # 如果当前已经在拖动物品，不执行任何操作
        if self.player.dragging_item:
            return
        
        # 先尝试处理右键装备功能
        # 设置界面参数并计算inv_x和inv_y
        if self.player.is_chest_open and self.player.current_chest:
            # 检查玩家是否也打开了背包（同时打开背包和箱子）
            player_inventory_open = getattr(self.player, 'is_inventory_open', False) or (self.game_state == 'inventory')
            
            if not player_inventory_open:
                # 仅打开箱子界面 - 使用紧凑布局
                inv_width = 420
                inv_height = 400
            else:
                # 同时打开箱子和背包界面
                inv_width = 700
                inv_height = 500
        else:
            # 普通背包界面
            inv_width = 580
            inv_height = 410
        
        # 计算inv_x和inv_y（必须先计算这两个值）
        inv_x = (WIDTH - inv_width) // 2
        inv_y = (HEIGHT - inv_height) // 2
        
        # 然后计算背包起始位置
        if self.player.is_chest_open and self.player.current_chest and player_inventory_open:
            backpack_start_x = inv_x + inv_width - 50 - 6 * (40 + 5)
            backpack_start_y = inv_y + 50
        else:
            # 与handle_inventory_click函数中的背包起始位置保持一致
            backpack_start_x = inv_x + 251
            backpack_start_y = inv_y + 58
        
        slot_size = 40
        slot_margin = 5
        hotbar_size = len(self.player.hotbar)  # 8格快捷栏
        backpack_size = self.player.backpack_slots  # 30格背包
        
        # 计算快捷栏区域
        hotbar_start_x = inv_x + 80
        hotbar_start_y = inv_y + inv_height - 80
        
        # 计算背包区域
        rows = 5
        cols = 6
        
        # 确保player_inventory_open变量已定义
        player_inventory_open = getattr(self.player, 'is_inventory_open', False) or (self.game_state == 'inventory')
        
        # 1. 检查右键点击是否在快捷栏
        for i in range(hotbar_size):
            x = hotbar_start_x + i * (slot_size + slot_margin)
            y = hotbar_start_y
            slot_rect = pygame.Rect(x, y, slot_size, slot_size)
            if slot_rect.collidepoint(mx, my):
                # 获取物品ID
                item = self.player.hotbar[i]
                if isinstance(item, list):
                    item_id, count = item
                else:
                    item_id, count = item, 1
                
                # 检查物品是否可装备
                if item_id != 0 and 'ITEMS' in globals() and item_id in ITEMS:
                    item_info = ITEMS[item_id]
                    if 'type' in item_info and item_info['type'] in ['helmet', 'armor', 'boots', 'special']:
                        slot_type = item_info['type']
                        # 获取当前装备
                        current_equipment = self.player.equipment.get(slot_type, 0)
                        # 尝试将当前装备放入背包
                        can_equip = True
                        if current_equipment != 0:
                            can_equip = self.player.add_item(current_equipment, 1)
                        # 装备新物品
                        if can_equip:
                            # 调用装备方法并获取之前的装备（如果有）
                            previous_item = self.player.equip_item(slot_type, item_id)
                            # 从快捷栏移除物品
                            if isinstance(self.player.hotbar[i], list):
                                self.player.hotbar[i][1] -= 1
                                if self.player.hotbar[i][1] <= 0:
                                    self.player.hotbar[i] = [0, 0]
                            else:
                                self.player.hotbar[i] = 0
                        return
        
        # 2. 检查右键点击是否在背包格子
        if backpack_start_x and backpack_start_y:
            backpack_rect = pygame.Rect(backpack_start_x, backpack_start_y, 
                                       cols * (slot_size + slot_margin), rows * (slot_size + slot_margin))
            if backpack_rect.collidepoint(mx, my):
                # 计算点击的槽位索引
                col = (mx - backpack_start_x) // (slot_size + slot_margin)
                row = (my - backpack_start_y) // (slot_size + slot_margin)
                slot_idx = row * cols + col
                
                if 0 <= slot_idx < backpack_size:
                    # 获取物品ID
                    item = self.player.inventory[slot_idx]
                    if isinstance(item, list):
                        item_id, count = item
                    else:
                        item_id, count = item, 1
                    
                    # 检查物品是否可装备
                    if item_id != 0 and 'ITEMS' in globals() and item_id in ITEMS:
                        item_info = ITEMS[item_id]
                        if 'type' in item_info and item_info['type'] in ['helmet', 'armor', 'boots', 'special']:
                            slot_type = item_info['type']
                            # 获取当前装备
                            current_equipment = self.player.equipment.get(slot_type, 0)
                            # 尝试将当前装备放入背包
                            can_equip = True
                            if current_equipment != 0:
                                can_equip = self.player.add_item(current_equipment, 1)
                            # 装备新物品
                            if can_equip:
                                # 调用装备方法并获取之前的装备（如果有）
                                previous_item = self.player.equip_item(slot_type, item_id)
                                # 从背包移除物品
                                if isinstance(self.player.inventory[slot_idx], list):
                                    self.player.inventory[slot_idx][1] -= 1
                                    if self.player.inventory[slot_idx][1] <= 0:
                                        self.player.inventory[slot_idx] = [0, 0]
                                else:
                                    self.player.inventory[slot_idx] = 0
                            return
            
        # 根据是否打开箱子调整UI参数
        if self.player.is_chest_open and self.player.current_chest:
            # 检查玩家是否也打开了背包（同时打开背包和箱子）
            player_inventory_open = getattr(self.player, 'is_inventory_open', False) or (self.game_state == 'inventory')
            
            if not player_inventory_open:
                # 仅打开箱子界面 - 使用紧凑布局
                inv_width = 420
                inv_height = 400
                chest_rows = 4
                chest_cols = 5
            else:
                # 同时打开箱子和背包界面
                inv_width = 700
                inv_height = 500
                chest_rows = 4
                chest_cols = 5
        else:
            # 普通背包界面
            inv_width = 580
            inv_height = 410
            equipment_area_width = 180
        
        # 先计算inv_x和inv_y
        inv_x = (WIDTH - inv_width) // 2
        inv_y = (HEIGHT - inv_height) // 2
        
        # 再计算其他依赖inv_x和inv_y的变量
        if self.player.is_chest_open and self.player.current_chest:
            player_inventory_open = getattr(self.player, 'is_inventory_open', False) or (self.game_state == 'inventory')
            
            if not player_inventory_open:
                # 仅打开箱子界面 - 居中显示箱子内容
                chest_start_x = inv_x + 40
                chest_start_y = inv_y + 50
            else:
                # 同时打开箱子和背包界面
                chest_start_x = inv_x + 50
                chest_start_y = inv_y + 50
                backpack_start_x = inv_x + inv_width - 50 - 6 * (40 + 5)
                backpack_start_y = inv_y + 50
        else:
            # 与handle_inventory_click函数中的背包起始位置保持一致
            backpack_start_x = inv_x + 251
            backpack_start_y = inv_y + 58
        
        slot_size = 40
        slot_margin = 5
        hotbar_size = len(self.player.hotbar)  # 8格快捷栏
        backpack_size = self.player.backpack_slots  # 30格背包
        
        # 计算快捷栏区域 - 与handle_inventory_click函数中的位置保持一致
        hotbar_start_x = inv_x + 80
        hotbar_start_y = inv_y + inv_height - 80
        hotbar_rect = pygame.Rect(hotbar_start_x, hotbar_start_y, 
                                 hotbar_size * (slot_size + slot_margin), slot_size)
        
        # 计算背包区域
        rows = 5
        cols = 6
        backpack_rect = pygame.Rect(backpack_start_x, backpack_start_y, 
                                   cols * (slot_size + slot_margin), rows * (slot_size + slot_margin))
        
        # 检查是否点击了快捷栏
        if hotbar_rect.collidepoint(mx, my):
            # 计算点击的槽位索引
            slot_idx = (mx - hotbar_start_x) // (slot_size + slot_margin)
            if 0 <= slot_idx < hotbar_size:
                item_id, count = self.player.hotbar[slot_idx]
                
                # 如果槽位有物品且数量大于1
                if item_id != 0 and count > 1:
                    # 计算要拆分的数量（向下取整）
                    half_count = count // 2
                    
                    # 从原槽位中减去拆分的数量
                    self.player.hotbar[slot_idx] = [item_id, count - half_count]
                    
                    # 开始拖动拆分的物品
                    self.player.dragging_item = {"item_id": item_id, "quantity": half_count}
                    self.player.dragging_source = "hotbar"
                    self.player.dragging_slot = slot_idx
                    self.player.is_split_dragging = True  # 标记为右键拆分的物品拖动
        
        # 检查是否点击了箱子格子（如果打开了箱子）
        elif self.player.is_chest_open and self.player.current_chest:
            player_inventory_open = getattr(self.player, 'is_inventory_open', False) or (self.game_state == 'inventory')
            
            if not player_inventory_open:
                # 仅打开箱子界面
                chest_rect = pygame.Rect(chest_start_x, chest_start_y, 
                                        chest_cols * (slot_size + slot_margin), chest_rows * (slot_size + slot_margin))
                
                if chest_rect.collidepoint(mx, my):
                    # 计算点击的箱子槽位索引
                    col = (mx - chest_start_x) // (slot_size + slot_margin)
                    row = (my - chest_start_y) // (slot_size + slot_margin)
                    slot_idx = row * chest_cols + col
                    
                    # 确保索引在有效范围内
                    if 0 <= slot_idx < len(self.player.current_chest.items):
                        chest_item = self.player.current_chest.items[slot_idx]
                        chest_item_id, chest_item_count = chest_item
                        
                        # 如果格子有物品且数量大于1
                        if chest_item_id != 0 and chest_item_count > 1:
                            # 计算要拆分的数量（向下取整）
                            half_count = chest_item_count // 2
                            
                            # 从原格子中减去拆分的数量
                            self.player.current_chest.items[slot_idx] = [chest_item_id, chest_item_count - half_count]
                            
                            # 开始拖动拆分的物品
                            self.player.dragging_item = {"item_id": chest_item_id, "quantity": half_count}
                            self.player.dragging_source = "chest"
                            self.player.dragging_slot = slot_idx
                            self.player.is_split_dragging = True  # 标记为右键拆分的物品拖动
        # 检查是否点击了背包格子
        elif backpack_rect.collidepoint(mx, my):
            # 计算点击的槽位索引
            col = (mx - backpack_start_x) // (slot_size + slot_margin)
            row = (my - backpack_start_y) // (slot_size + slot_margin)
            slot_idx = row * cols + col
            
            if 0 <= slot_idx < backpack_size:
                # 获取目标背包格子的物品
                target_item = self.player.inventory[slot_idx]
                target_id, target_count = target_item
                
                # 如果格子有物品且数量大于1
                if target_id != 0 and target_count > 1:
                    # 计算要拆分的数量（向下取整）
                    half_count = target_count // 2
                    
                    # 从原格子中减去拆分的数量
                    self.player.inventory[slot_idx] = [target_id, target_count - half_count]
                    
                    # 开始拖动拆分的物品
                    self.player.dragging_item = {"item_id": target_id, "quantity": half_count}
                    self.player.dragging_source = "inventory"
                    self.player.dragging_slot = slot_idx
                    self.player.is_split_dragging = True  # 标记为右键拆分的物品拖动

    def handle_crafting_click(self, mx, my):
        """处理合成界面点击"""
        # 定义界面参数（与draw_crafting方法保持一致）
        spacing = 20
        panel_width = 320  # 与draw_crafting方法保持一致
        panel_height = HEIGHT - 180  # 与draw_crafting方法保持一致
        left_panel_x = (WIDTH // 2 - panel_width) // 2
        right_panel_x = WIDTH // 2 + (WIDTH // 2 - panel_width) // 2
        panel_y = 100
        
        # 检查是否点击了右上角关闭按钮
        close_button_rect = pygame.Rect(WIDTH - 50, 50, 30, 30)
        if close_button_rect.collidepoint(mx, my):
            # 切换回游戏状态，关闭合成界面
            self.game_state = 'game'
            return
        
        # 合成按钮位置和大小
        craft_button_width = panel_width - 2 * spacing
        craft_button_height = 40
        craft_button_x = right_panel_x + spacing
        craft_button_y = panel_y + panel_height - spacing - craft_button_height
        
        # 创建按钮矩形用于碰撞检测
        craft_button_rect = pygame.Rect(craft_button_x, craft_button_y, craft_button_width, craft_button_height)
        
        # 检查是否点击了配方选择区域（图像按钮网格布局）
        icon_size = 50
        grid_cols = 4  # 每行显示4个图标
        grid_spacing = 10  # 网格间距
        
        # 计算网格起始位置使其居中（与draw_crafting方法保持一致）
        grid_width = grid_cols * (icon_size + grid_spacing) - grid_spacing
        grid_start_x = left_panel_x + (panel_width - grid_width) // 2
        grid_start_y = panel_y + 50
        
        for i, recipe in enumerate(self.crafting.recipes):
            # 计算在网格中的位置
            row = i // grid_cols
            col = i % grid_cols
            
            # 计算按钮位置
            button_x = grid_start_x + col * (icon_size + grid_spacing)
            button_y = grid_start_y + row * (icon_size + grid_spacing)
            
            # 创建按钮矩形用于碰撞检测
            recipe_rect = pygame.Rect(button_x, button_y, icon_size, icon_size)
            
            # 检查配方按钮是否被点击
            if recipe_rect.collidepoint(mx, my):
                # 选中这个配方
                if not hasattr(self, 'selected_recipe'):
                    self.selected_recipe = None
                self.selected_recipe = i
                # 显示选中的配方和按钮所在格子信息
                print(f"已选择配方: {recipe['name']}")
                print(f"按钮所在格子: 行 {row}, 列 {col}")
                return
        
        # 检测是否点击了合成按钮
        if craft_button_rect.collidepoint(mx, my):
            # 检查是否已选择配方
            if hasattr(self, 'selected_recipe') and self.selected_recipe is not None:
                recipe_index = self.selected_recipe
                if self.crafting.can_craft(recipe_index, self.player):
                    result = self.crafting.craft(recipe_index, self.player)
                    if result:
                        self.player.add_item(result["item_id"], result["quantity"])
                        print(f"成功合成 {result['quantity']} 个 {ITEMS[result['item_id']]['name']}")
                else:
                    # 获取当前配方的名称
                    if 0 <= recipe_index < len(self.crafting.recipes):
                        recipe_name = self.crafting.recipes[recipe_index]['name']
                        print(f"材料不足，无法合成{recipe_name}")
                    else:
                        print("材料不足，无法合成")
            else:
                print("请先选择要合成的物品")

    def start_breaking_block(self, x, y):
        """开始破坏方块"""
        block_id = self.world.get_block(x, y)
        # 允许破坏所有方块
        if block_id and block_id != AIR and (BLOCKS[block_id]["solid"] or block_id == LEAF or block_id == TORCH or block_id == RED_FLOWER or block_id == GRASS_PLANT or block_id == DRY_GRASS or block_id == SHRUB or block_id == JUNGLE_LEAF or block_id == JUNGLE_FRUIT or block_id == STONE_BOTTOM):
            # 检查方块是否可挖掘（硬度为-1表示不可挖掘，如基岩），如果开启了最高权限，则忽略此检查
            if "hardness" in BLOCKS[block_id] and BLOCKS[block_id]["hardness"] == -1 and not self.god_mode:
                return  # 不可挖掘的方块，直接返回
            
            self.breaking_pos = (x, y)
            self.breaking_start_time = time.time()

            # 根据工具类型和方块硬度计算破坏时间
            tool = self.player.get_selected_item()
            # 获取方块硬度，默认硬度为1
            hardness = BLOCKS[block_id].get("hardness", 1)
            # 基础破坏时间 = 硬度 * 基础时间系数
            base_time = hardness * 1.2  # 空手破坏时间，与方块硬度成正比

            if tool:
                tool_id = tool["item_id"]
                tool_type = ITEMS[tool_id]["type"]
                
                # 火把特殊处理：可以挖掘所有方块但效率较低
                if tool_id == TORCH:
                    # 火把可以挖掘所有类型的方块，但效率是空手的1.5倍
                    base_time /= 1.5
                # 根据工具类型和方块类型调整破坏时间
                elif (tool_type == "pickaxe" and block_id in [STONE, IRON_ORE, GOLD_ORE, DIAMOND_ORE, COPPER_ORE]) or \
                        (tool_type == "axe" and block_id in [WOOD, LEAF]) or \
                        (tool_type == "shovel" and block_id in [DIRT, GRASS, BLACK_DIRT, SAND]):
                    # 合适的工具，加快破坏速度
                    base_time /= ITEMS[tool_id]["speed"]

            # 火把、草、红花和枯草特殊处理：任何工具都能以0.1秒快速挖掘
            if block_id in [TORCH, RED_FLOWER, GRASS_PLANT, DRY_GRASS]:
                self.breaking_time = 0.1
            else:
                # 确保破坏时间不会太短，最小为0.1秒
                self.breaking_time = max(0.1, base_time)
                
            # 如果开启了秒挖掘功能，则设置破坏时间为几乎瞬时
            if self.instant_mining:
                self.breaking_time = 0.01

    def update_breaking(self):
        """更新方块破坏进度"""
        if self.breaking_pos:
            x, y = self.breaking_pos
            current_time = time.time()
            self.breaking_progress = (current_time - self.breaking_start_time) / self.breaking_time

            if self.breaking_progress >= 1.0:
                # 破坏完成
                blocks_to_remove = []
                
                # 判断是否使用3*3范围挖掘
                if hasattr(self, 'area_mine_enabled') and self.area_mine_enabled:
                    # 3*3范围挖掘
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            target_x = x + dx
                            target_y = y + dy
                            # 检查世界范围
                            if 0 <= target_x < WORLD_WIDTH and 0 <= target_y < WORLD_HEIGHT:
                                target_block_id = self.world.get_block(target_x, target_y)
                                # 检查方块是否可以破坏
                                if (target_block_id and target_block_id != AIR and 
                                    (BLOCKS[target_block_id]["solid"] or target_block_id == LEAF or 
                                     target_block_id == TORCH or target_block_id == RED_FLOWER or 
                                     target_block_id == GRASS_PLANT or target_block_id == DRY_GRASS or 
                                     target_block_id == SHRUB or target_block_id == JUNGLE_LEAF or 
                                     target_block_id == JUNGLE_FRUIT or target_block_id == STONE_BOTTOM)):
                                    # 检查方块是否可挖掘（硬度为-1表示不可挖掘，如基岩），如果开启了最高权限，则忽略此检查
                                    if ("hardness" in BLOCKS[target_block_id] and BLOCKS[target_block_id]["hardness"] == -1 and not self.god_mode):
                                        continue  # 不可挖掘的方块，跳过
                                    blocks_to_remove.append((target_x, target_y))
                else:
                    # 普通挖掘
                    blocks_to_remove.append((x, y))
                
                # 处理所有要移除的方块
                for bx, by in blocks_to_remove:
                    block_id = self.world.remove_block(bx, by)
                    if block_id:
                        # 如果破坏的是默认生成的岩石或矿石方块，添加岩石_底方块
                        if block_id in [STONE, IRON_ORE, GOLD_ORE, DIAMOND_ORE, COPPER_ORE]:
                            # 检查是否是玩家放置的方块
                            is_player_placed = hasattr(self.world, 'player_placed_blocks') and (bx, by) in self.world.player_placed_blocks
                            # 只对默认生成的方块添加岩石_底，玩家放置的方块不会生成
                            if not is_player_placed:
                                self.world.set_block(bx, by, STONE_BOTTOM)
                            # 如果是玩家放置的方块，从标记集合中移除
                            elif hasattr(self.world, 'player_placed_blocks'):
                                self.world.player_placed_blocks.discard((bx, by))
                        # 特殊处理箱子方块
                        if block_id == CHEST:
                            # 关闭箱子UI（如果当前打开的是这个箱子）
                            if self.new_chest_manager.is_open and self.new_chest_manager.chest_x == bx and self.new_chest_manager.chest_y == by:
                                self.new_chest_manager.close_page()
                            
                            # 箱子的世界坐标
                            chest_x = bx * TILE_SIZE
                            chest_y = by * TILE_SIZE
                            
                            # 处理箱子内的物品掉落（使用新的箱子数据系统）
                            if hasattr(self.world, 'chest_data') and (bx, by) in self.world.chest_data:
                                chest_items = self.world.chest_data[(bx, by)]
                                for item_data in chest_items:
                                    if item_data and isinstance(item_data, list) and len(item_data) >= 2 and item_data[0] != 0:
                                        item_id, quantity = item_data
                                        if quantity > 0:
                                            # 为每一个物品创建掉落物实体
                                            # 位置略微随机化，让物品散落在箱子周围
                                            drop_x = chest_x + TILE_SIZE // 2 - 12 + random.randint(-20, 20)
                                            drop_y = chest_y - 24 + random.randint(-10, 10)
                                            item_entity = ItemEntity(drop_x, drop_y, item_id, quantity)
                                            self.item_entities.append(item_entity)
                                
                                # 从chest_data中删除对应的箱子数据
                                del self.world.chest_data[(bx, by)]
                            
                            # 同时处理旧箱子系统的数据
                            for chest in self.world.chests[:]:
                                if chest.tile_x == bx and chest.tile_y == by:
                                    for item_id, quantity in chest.items:
                                        if quantity > 0:
                                            drop_x = chest_x + TILE_SIZE // 2 - 12 + random.randint(-20, 20)
                                            drop_y = chest_y - 24 + random.randint(-10, 10)
                                            item_entity = ItemEntity(drop_x, drop_y, item_id, quantity)
                                            self.item_entities.append(item_entity)
                                
                                self.world.chests.remove(chest)
                                break
                            
                            # 确保方块已被设置为空气，防止箱子继续渲染
                            self.world.blocks[by][bx] = AIR
                            
                            # 创建箱子本身的掉落物
                            drop_x = chest_x + TILE_SIZE // 2 - 12
                            drop_y = chest_y - 24
                            chest_item_entity = ItemEntity(drop_x, drop_y, CHEST, 1)
                            self.item_entities.append(chest_item_entity)
                            
                            # 如果玩家当前打开的是旧箱子系统的箱子，关闭UI
                            if self.player.is_chest_open and self.player.current_chest and self.player.current_chest.tile_x == bx and self.player.current_chest.tile_y == by:
                                self.player.is_chest_open = False
                                self.player.current_chest = None
                        
                        # 创建方块掉落物实体
                        # 确保添加正确的物品类型
                        if block_id == STONE_BOTTOM:
                            # 挖掘岩石_底方块时，添加普通岩石物品
                            drop_item_id = STONE
                        else:
                            drop_item_id = block_id
                        
                        # 创建掉落物实体，位置略微随机化，让物品散落在周围
                        drop_x = bx * TILE_SIZE + TILE_SIZE // 2 - 12 + random.randint(-10, 10)
                        drop_y = by * TILE_SIZE - 24
                        item_entity = ItemEntity(drop_x, drop_y, drop_item_id, 1)
                        self.item_entities.append(item_entity)

                    # 树叶30%概率掉落苹果
                    if block_id == LEAF:
                        if random.random() < 0.3:
                            # 创建苹果掉落物实体
                            drop_x = bx * TILE_SIZE + TILE_SIZE // 2 - 12 + random.randint(-10, 10)
                            drop_y = by * TILE_SIZE - 24
                            item_entity = ItemEntity(drop_x, drop_y, APPLE, 1)
                            self.item_entities.append(item_entity)

                self.breaking_pos = None
                self.breaking_progress = 0

    def save_game(self):
        """保存游戏状态到存档文件夹，按照存档名称创建子文件夹"""
        try:
            # 确保save_name属性存在
            if not hasattr(self, 'save_name'):
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                self.save_name = f"New World_{timestamp}"
                print(f"使用默认存档名称: {self.save_name}")
            
            # 获取当前程序文件所在目录
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # 存档文件夹路径（相对于程序文件所在目录）
            root_save_folder = os.path.join(current_dir, "存档")
            if not os.path.exists(root_save_folder):
                os.makedirs(root_save_folder)
                print(f"创建存档根文件夹: {root_save_folder}")
            
            # 创建以存档名称命名的子文件夹
            save_subfolder = os.path.join(root_save_folder, self.save_name)
            
            # 检查存档子文件夹是否已存在
            if os.path.exists(save_subfolder):
                print(f"保存失败: 存档 '{self.save_name}' 已存在")
                # 弹出提示消息（这里简化处理，实际游戏中可以显示一个弹窗）
                return
            
            # 创建存档子文件夹
            os.makedirs(save_subfolder)
            print(f"创建存档子文件夹: {save_subfolder}")
            
            # 准备地形数据
            terrain_data = {
                "blocks": self.world.blocks,
                "world_width": WORLD_WIDTH,
                "world_height": WORLD_HEIGHT
            }
            
            # 保存地形数据到terrain_data.json
            terrain_file = os.path.join(save_subfolder, "terrain_data.json")
            with open(terrain_file, 'w', encoding='utf-8') as f:
                json.dump(terrain_data, f, ensure_ascii=False, indent=2)
            
            # 准备玩家数据
            player_data = {
                "x": self.player.x,
                "y": self.player.y,
                "is_developer": hasattr(self, 'is_developer_mode') and self.is_developer_mode,
                "max_health": self.player.max_health,
                "current_health": self.player.health,
                "current_hunger": self.player.hunger,
                "max_hunger": self.player.max_hunger,
                "current_oxygen": self.player.oxygen,
                "is_dead": self.player.health <= 0,
                "remaining_immune_time": self.player.immune_time,
                "stars": self.player.stars,
                "star_experience": f"{self.player.experience}/{self.player.max_experience}",
                "hotbar": [],
                "inventory": []
            }
            
            # 添加快捷栏数据
            for i, item_id in enumerate(self.player.hotbar):
                quantity = self.player.inventory.get(item_id, 0)
                if i == self.player.selected_slot:
                    player_data["hotbar"].append(f"快捷栏{i+1}:道具编号{item_id:02d},数量:{quantity:02d} (选中)")
                else:
                    player_data["hotbar"].append(f"快捷栏{i+1}:道具编号{item_id:02d},数量:{quantity:02d}")
            
            # 添加背包数据
            backpack_index = 1
            for item_id, quantity in self.player.inventory.items():
                player_data["inventory"].append(f"背包{backpack_index}:道具编号{item_id:03d},数量:{quantity:02d}")
                backpack_index += 1
            
            # 保存玩家数据到player_data.json
            player_file = os.path.join(save_subfolder, "player_data.json")
            with open(player_file, 'w', encoding='utf-8') as f:
                json.dump(player_data, f, ensure_ascii=False, indent=2)
            
            # 准备生物数据
            creatures_data = []
            for creature in self.creatures:
                creature_info = {
                    "type": creature.type,
                    "x": creature.x,
                    "y": creature.y,
                    "health": creature.health,
                    "max_health": creature.max_health,
                    "damage": creature.damage,
                    "speed": creature.speed,
                    "hostile": creature.hostile
                }
                creatures_data.append(creature_info)
            
            # 保存生物数据到creatures_data.json
            creatures_file = os.path.join(save_subfolder, "creatures_data.json")
            with open(creatures_file, 'w', encoding='utf-8') as f:
                json.dump(creatures_data, f, ensure_ascii=False, indent=2)
            
            # 准备特殊方块数据
            special_blocks_data = {
                "chests": []
            }
            
            # 添加箱子数据
            for chest in self.world.chests:
                chest_info = {
                    "x": chest.x,
                    "y": chest.y,
                    "items": []
                }
                for item_id, quantity in chest.items:
                    chest_info["items"].append(f"道编码:{item_id:03d},道具数量:{quantity:02d}")
                special_blocks_data["chests"].append(chest_info)
            
            # 保存特殊方块数据到special_blocks_data.json
            special_blocks_file = os.path.join(save_subfolder, "special_blocks_data.json")
            with open(special_blocks_file, 'w', encoding='utf-8') as f:
                json.dump(special_blocks_data, f, ensure_ascii=False, indent=2)
            
            # 准备其他数据
            other_data = {
                "world_current_time": self.world.time_of_day,
                "is_raining": self.world.is_raining,
                "save_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 保存其他数据到other_data.json
            other_file = os.path.join(save_subfolder, "other_data.json")
            with open(other_file, 'w', encoding='utf-8') as f:
                json.dump(other_data, f, ensure_ascii=False, indent=2)
            
            # 同时保存到默认文件
            save_data = {
                "player": player_data,
                "world": {
                    "blocks": self.world.blocks,
                    "time_of_day": self.world.time_of_day
                }
            }
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            print(f"存档 '{self.save_name}' 创建成功")
            
        except Exception as e:
            print(f"保存失败: {e}")

    def import_save_game(self):
        """从存档文件夹导入游戏存档"""
        try:
            # 获取存档文件夹路径
            save_folder = "存档"
            
            # 检查存档文件夹是否存在
            if not os.path.exists(save_folder):
                print("存档文件夹不存在")
                return
            
            # 获取存档文件夹中的所有JSON文件
            save_files = [f for f in os.listdir(save_folder) if f.endswith('.json')]
            
            if not save_files:
                print("存档文件夹中没有找到存档文件")
                return
            
            # 简单实现：加载第一个找到的存档文件
            # 实际游戏中可以实现更复杂的选择界面
            selected_save = os.path.join(save_folder, save_files[0])
            print(f"加载存档: {selected_save}")
            
            # 读取存档文件
            with open(selected_save, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # 初始化游戏世界和玩家（如果尚未初始化）
            if not hasattr(self, 'world') or not hasattr(self, 'player'):
                self.world = World(self.image_loader)
                self.player = Player(WIDTH * TILE_SIZE // 2, 0)
                self.creatures = self.spawn_initial_creatures(30)
            
            # 恢复玩家状态
            if "player" in save_data:
                player_data = save_data["player"]
                self.player.x = player_data.get("x", WIDTH * TILE_SIZE // 2)
                self.player.y = player_data.get("y", 0)
                self.player.health = player_data.get("health", 20)
                self.player.hunger = player_data.get("hunger", 20)
                
                # 处理物品栏数据格式转换
                inventory_data = player_data.get("inventory", {})
                if isinstance(inventory_data, list) and inventory_data and isinstance(inventory_data[0], str):
                    # 从字符串格式解析
                    new_inventory = []
                    for item_str in inventory_data:
                        try:
                            parts = item_str.split(":")
                            if len(parts) >= 3:
                                item_id_part = parts[1].strip()
                                quantity_part = parts[2].strip().split()[0]
                                item_id = int(''.join(filter(str.isdigit, item_id_part)))
                                quantity = int(''.join(filter(str.isdigit, quantity_part)))
                                new_inventory.append([item_id, quantity])
                        except:
                            pass
                    # 确保有30个格子
                    while len(new_inventory) < self.player.backpack_slots:
                        new_inventory.append([0, 0])
                    self.player.inventory = new_inventory
                elif isinstance(inventory_data, dict):
                    # 从字典格式转换
                    new_inventory = [[0, 0] for _ in range(self.player.backpack_slots)]
                    index = 0
                    for item_id, quantity in inventory_data.items():
                        if index < self.player.backpack_slots:
                            new_inventory[index] = [int(item_id), quantity]
                            index += 1
                    self.player.inventory = new_inventory
                else:
                    self.player.inventory = inventory_data
                
                # 处理快捷栏数据格式转换
                hotbar_data = player_data.get("hotbar", [])
                if isinstance(hotbar_data, list) and hotbar_data and isinstance(hotbar_data[0], str):
                    # 从字符串格式解析
                    new_hotbar = []
                    for item_str in hotbar_data:
                        try:
                            parts = item_str.split(":")
                            if len(parts) >= 3:
                                item_id_part = parts[1].strip()
                                quantity_part = parts[2].strip().split()[0]
                                item_id = int(''.join(filter(str.isdigit, item_id_part)))
                                quantity = int(''.join(filter(str.isdigit, quantity_part)))
                                new_hotbar.append([item_id, quantity])
                        except:
                            pass
                    # 确保有8个格子
                    while len(new_hotbar) < self.player.hotbar_size:
                        new_hotbar.append([0, 0])
                    self.player.hotbar = new_hotbar
                elif isinstance(hotbar_data, dict):
                    # 从字典格式转换
                    new_hotbar = [[0, 0] for _ in range(self.player.hotbar_size)]
                    for slot, item_id in hotbar_data.items():
                        if 0 <= int(slot) < self.player.hotbar_size:
                            # 在inventory中查找该物品的数量
                            quantity = 0
                            for item in self.player.inventory:
                                if item[0] == int(item_id):
                                    quantity = item[1]
                                    break
                            new_hotbar[int(slot)] = [int(item_id), quantity]
                    self.player.hotbar = new_hotbar
                else:
                    self.player.hotbar = hotbar_data
                
                self.player.selected_slot = player_data.get("selected_slot", 0)
            
            # 恢复世界状态
            if "world" in save_data:
                world_data = save_data["world"]
                self.world.blocks = world_data.get("blocks", {})
                self.world.time_of_day = world_data.get("time_of_day", 0)
            
            print(f"成功导入存档: {save_files[0]}")
            # 关闭启动画面，进入游戏
            self.show_start_screen = False
            
        except Exception as e:
            print(f"导入存档失败: {e}")
    
    def load_game(self):
        """加载游戏状态"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)

                # 恢复玩家状态
                player_data = save_data["player"]
                self.player.x = player_data["x"]
                self.player.y = player_data["y"]
                self.player.health = player_data["health"]
                self.player.hunger = player_data["hunger"]
                self.player.inventory = player_data["inventory"]
                self.player.hotbar = player_data["hotbar"]
                self.player.selected_slot = player_data["selected_slot"]

                # 恢复世界状态
                world_data = save_data["world"]
                self.world.blocks = world_data["blocks"]
                self.world.time_of_day = world_data["time_of_day"]

                print("游戏已加载")
            except Exception as e:
                print(f"加载失败: {e}")

    def create_rain_drops(self):
        """创建雨滴"""
        # 计算可见区域的宽度（考虑相机移动）
        visible_width = WIDTH
        # 雨滴宽度范围
        rain_width_min = 1
        rain_width_max = 3
        # 雨滴长度范围
        rain_length_min = 10
        rain_length_max = 20
        # 雨滴速度范围
        rain_speed_min = 500
        rain_speed_max = 700
        # 雨滴颜色
        rain_color = (100, 149, 237, 128)  # 蓝色半透明
        
        # 根据雨的密度创建雨滴
        for _ in range(int(visible_width * self.rain_intensity)):
            # 随机位置（在可见区域左侧到右侧的x轴范围）
            x = random.randint(-100, WIDTH + 100) + self.camera_x
            # 随机y位置（从屏幕上方）
            y = random.randint(-200, 0)
            # 随机宽度和长度
            width = random.randint(rain_width_min, rain_width_max)
            length = random.randint(rain_length_min, rain_length_max)
            # 随机速度
            speed = random.randint(rain_speed_min, rain_speed_max)
            # 添加雨滴
            self.rain_drops.append({
                "x": x,
                "y": y,
                "width": width,
                "length": length,
                "speed": speed,
                "color": rain_color
            })
    
    def update_rain(self, dt):
        """更新下雨系统"""
        # 更新下雨计时器
        self.rain_timer += dt
        
        # 检查是否需要开始下雨
        if not self.is_raining and self.rain_timer >= self.rain_duration:
            # 随机决定是否开始下雨
            if random.random() < self.rain_chance:
                self.is_raining = True
                self.world.is_raining = True  # 更新World类的下雨状态
                self.rain_duration = random.uniform(self.min_rain_duration, self.max_rain_duration)
                self.rain_timer = 0
                self.rain_intensity = random.uniform(0.05, 0.2)  # 随机雨的密度
                # 创建初始雨滴
                self.create_rain_drops()
            else:
                # 设置下一次检查时间
                self.rain_duration = random.uniform(self.min_rain_interval, self.max_rain_interval)
                self.rain_timer = 0
        # 检查是否需要停止下雨
        elif self.is_raining and self.rain_timer >= self.rain_duration:
            self.is_raining = False
            self.world.is_raining = False  # 更新World类的下雨状态
            self.rain_drops.clear()
            # 设置下一次可能下雨的时间间隔
            self.rain_duration = random.uniform(self.min_rain_interval, self.max_rain_interval)
            self.rain_timer = 0
        # 更新雨滴
        elif self.is_raining:
            # 定期创建新雨滴
            if random.random() < 0.1:  # 10%的概率创建新雨滴
                self.create_rain_drops()
            
            # 更新所有雨滴的位置
            for drop in self.rain_drops[:]:
                drop["y"] += drop["speed"] * dt
                # 如果雨滴超出屏幕底部，移除它
                if drop["y"] - self.camera_y > HEIGHT + 100:
                    self.rain_drops.remove(drop)
            
            # 在下雨时，有小概率开始打雷
            if not self.is_thundering and random.random() < self.thunder_chance:
                self.is_thundering = True
                self.thunder_timer = random.uniform(5, 15)  # 打雷持续时间（5-15秒）
    
    def update_thunder(self, dt):
        """更新打雷系统"""
        if self.is_thundering:
            # 更新打雷计时器
            self.thunder_timer -= dt
            
            # 如果闪电正在闪烁，更新闪烁计时器
            if self.thunder_flash_timer > 0:
                self.thunder_flash_timer -= dt
            elif self.thunder_sound_timer > 0:
                self.thunder_sound_timer -= dt
            # 否则，随机生成闪电
            elif random.random() < 0.02:  # 2%的概率生成闪电
                # 设置闪电闪光计时器
                self.thunder_flash_timer = self.thunder_flash_duration
                # 设置雷声延迟（距离越远，延迟越长）
                self.thunder_sound_delay = random.uniform(0, 2)
                self.thunder_sound_timer = self.thunder_sound_delay
                
            # 检查打雷是否结束
            if self.thunder_timer <= 0:
                self.is_thundering = False
                self.thunder_flash_timer = 0
                self.thunder_sound_timer = 0
    
    def draw_rain(self, screen):
        """绘制雨滴"""
        if self.is_raining:
            # 创建临时的surface用于绘制半透明雨滴
            temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            
            # 绘制所有雨滴
            for drop in self.rain_drops:
                # 计算雨滴在屏幕上的位置
                screen_x = drop["x"] - self.camera_x
                screen_y = drop["y"] - self.camera_y
                
                # 只绘制在屏幕内的雨滴
                if -100 <= screen_x <= WIDTH and -100 <= screen_y <= HEIGHT + 100:
                    # 绘制雨滴（一条线）
                    pygame.draw.line(
                        temp_surface,
                        drop["color"],
                        (screen_x, screen_y),
                        (screen_x + drop["width"], screen_y + drop["length"]),
                        1
                    )
            
            # 将临时surface绘制到屏幕上
            screen.blit(temp_surface, (0, 0))
    
    def draw_thunder_flash(self, screen):
        """绘制闪电闪光效果"""
        if self.is_thundering and self.thunder_flash_timer > 0:
            # 计算闪光强度（随时间衰减）
            flash_intensity = self.thunder_flash_timer / self.thunder_flash_duration
            # 创建一个半透明的白色surface覆盖整个屏幕
            flash_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash_color = (255, 255, 255, int(flash_intensity * 150))  # 半透明白色
            flash_surface.fill(flash_color)
            # 将闪光surface绘制到屏幕上
            screen.blit(flash_surface, (0, 0))
    
    def is_desert_area(self, x, y):
        """判断指定位置是否为沙漠区域"""
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)
        
        # 检查周围5x5范围内的方块
        sand_count = 0
        cactus_count = 0
        
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                check_x = tile_x + dx
                check_y = tile_y + dy
                
                if 0 <= check_x < WORLD_WIDTH and 0 <= check_y < WORLD_HEIGHT:
                    block_id = self.world.get_block(check_x, check_y)
                    if block_id == SAND:
                        sand_count += 1
                    elif block_id == CACTUS or block_id == DRY_GRASS:
                        cactus_count += 1
        
        # 如果有足够的沙子和仙人掌，则认为是沙漠区域
        return sand_count >= 10 and cactus_count >= 2
        
    def is_jungle_area(self, x, y):
        """判断指定位置是否为雨林区域"""
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)
        
        # 检查周围5x5范围内的方块
        jungle_tree_count = 0
        jungle_leaf_count = 0
        shrub_count = 0
        
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                check_x = tile_x + dx
                check_y = tile_y + dy
                
                if 0 <= check_x < WORLD_WIDTH and 0 <= check_y < WORLD_HEIGHT:
                    block_id = self.world.get_block(check_x, check_y)
                    if block_id == JUNGLE_TREE:
                        jungle_tree_count += 1
                    elif block_id == JUNGLE_LEAF:
                        jungle_leaf_count += 1
                    elif block_id == SHRUB:
                        shrub_count += 1
        
        # 如果有足够的乔木、乔木叶或灌木，则认为是雨林区域
        return (jungle_tree_count >= 5 and jungle_leaf_count >= 8) or (jungle_leaf_count >= 10 and shrub_count >= 3)

    def update(self, dt):
        """更新游戏状态"""
        # 更新玩家
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.world, dt)
        
        # 检查鼠标左键是否仍然按住，如果没有按住，则取消挖掘
        mouse_pressed = pygame.mouse.get_pressed()
        if self.breaking_pos and not mouse_pressed[0]:
            self.breaking_pos = None
            self.breaking_progress = 0
        
        # 更新下雨和打雷系统
        self.update_rain(dt)
        self.update_thunder(dt)
        
        # 更新爆炸特效
        if hasattr(self, 'explosions'):
            for explosion in self.explosions[:]:
                # 减少剩余时间
                explosion['remaining_time'] -= dt
                # 增加爆炸半径
                progress = 1 - (explosion['remaining_time'] / explosion['duration'])
                explosion['radius'] = explosion['max_radius'] * progress
                
                # 移除已经结束的特效
                if explosion['remaining_time'] <= 0:
                    self.explosions.remove(explosion)

        # 更新生物
        for creature in self.creatures[:]:
            if creature.is_dead():
                # 创建掉落物实体
                drops = creature.get_drops()
                for drop in drops:
                    # 在生物位置创建物品实体
                    item_entity = ItemEntity(
                        creature.x + creature.width // 2 - 12,  # 居中
                        creature.y + creature.height // 2 - 12,  # 居中
                        drop["item_id"],
                        drop["quantity"]
                    )
                    # 添加到游戏的物品实体列表
                    self.item_entities.append(item_entity)
                
                self.creatures.remove(creature)
            else:
                creature.update(self.world, self.player, dt)

        # 定期生成新生物
        if random.random() < 0.001 and len(self.creatures) < 40:
            # 首先找到一个随机X坐标
            base_x = random.randint(10, (WORLD_WIDTH - 10) * TILE_SIZE)
            base_y = random.randint(10, (WORLD_HEIGHT - 10) * TILE_SIZE)
            
            # 尝试在周围寻找合适的地面位置
            x, y = base_x, base_y
            
            for _ in range(50):
                # 转换为方块坐标
                tile_x = int(x // TILE_SIZE)
                tile_y = int(y // TILE_SIZE)
                
                # 检查当前方块是否为空气，下方方块是否为固体
                if (self.world.is_within_bounds(tile_x, tile_y) and 
                    self.world.is_within_bounds(tile_x, tile_y + 1) and 
                    self.world.get_block(tile_x, tile_y) == AIR and 
                    self.world.get_block(tile_x, tile_y + 1) != AIR and 
                    BLOCKS.get(self.world.get_block(tile_x, tile_y + 1), {}).get('solid', False)):
                    break
                
                # 如果没有找到，在周围随机移动一点
                x = base_x + random.randint(-100, 100)
                y = base_y + random.randint(-50, 50)
                x = max(10, min(x, (WORLD_WIDTH - 10) * TILE_SIZE))
                y = max(10, min(y, (WORLD_HEIGHT - 10) * TILE_SIZE))
            
            # 判断是否在沙漠区域或雨林区域
            is_desert = self.is_desert_area(x, y)
            is_jungle = self.is_jungle_area(x, y)
            
            # 根据区域类型选择生物类型
            if is_desert:
                # 沙漠区域：60%概率生成沙漠虫子，30%概率生成小沙虫，10%概率生成BOSS沙虫
                rand = random.random()
                if rand < 0.6:
                    creature_type = DESERT_WORM
                elif rand < 0.9:
                    creature_type = SAND_WORM
                else:
                    creature_type = BOSS_SAND_WORM
                self.creatures.append(Creature(creature_type, x, y))
            elif is_jungle:
                # 雨林区域：50%概率生成蝎子，50%概率生成猴子
                rand = random.random()
                if rand < 0.5:
                    creature_type = SCORPION
                else:
                    creature_type = MONKEY
                self.creatures.append(Creature(creature_type, x, y))
            else:
                # 其他区域：随机选择非沙漠和非雨林专属生物
                other_creatures = [ctype for ctype in CREATURES.keys() if not CREATURES[ctype].get("desert_exclusive", False) and not CREATURES[ctype].get("jungle_exclusive", False)]
                creature_type = random.choice(other_creatures)
                self.creatures.append(Creature(creature_type, x, y))
        
        # 夜间（20:00-4:00）每小时生成2-5个怪物攻击玩家
        current_hour = int(self.world.time_of_day // 100)
        current_time = time.time()
        
        # 判断是否在夜间时间范围内（20:00-4:00）
        is_night_time = (current_hour >= 20) or (current_hour < 4)
        
        if is_night_time and len(self.creatures) < 50:
            # 检查是否到了新的小时或者距离上次生成已经过了足够的时间
            if (current_hour != self.last_spawn_hour or 
                current_time - self.last_night_spawn_time >= self.night_spawn_interval):
                
                # 生成2-5个怪物
                spawn_count = random.randint(2, 5)
                for _ in range(spawn_count):
                    # 在玩家周围随机位置生成怪物（但不太远）
                    player_x = self.player.x
                    player_y = self.player.y
                    
                    # 计算生成范围（离玩家800-1200像素远）
                    distance = random.randint(800, 1200)
                    angle = random.uniform(0, 2 * math.pi)
                    
                    spawn_x = player_x + distance * math.cos(angle)
                    spawn_y = player_y + distance * math.sin(angle)
                    
                    # 确保生成位置在世界范围内
                    spawn_x = max(100, min(spawn_x, (WORLD_WIDTH - 10) * TILE_SIZE))
                    spawn_y = max(100, min(spawn_y, (WORLD_HEIGHT - 10) * TILE_SIZE))
                    
                    # 在玩家周围寻找有固体方块支撑的地面位置
                    original_x, original_y = spawn_x, spawn_y
                    
                    # 尝试在周围寻找合适的地面位置
                    for _ in range(50):
                        # 转换为方块坐标
                        tile_x = int(spawn_x // TILE_SIZE)
                        tile_y = int(spawn_y // TILE_SIZE)
                        
                        # 检查当前方块是否为空气，下方方块是否为固体
                        if (self.world.is_within_bounds(tile_x, tile_y) and 
                            self.world.is_within_bounds(tile_x, tile_y + 1) and 
                            self.world.get_block(tile_x, tile_y) == AIR and 
                            self.world.get_block(tile_x, tile_y + 1) != AIR and 
                            BLOCKS.get(self.world.get_block(tile_x, tile_y + 1), {}).get('solid', False)):
                            break
                        
                        # 如果没有找到，在周围随机移动一点
                        spawn_x = original_x + random.randint(-100, 100)
                        spawn_y = original_y + random.randint(-50, 50)
                        spawn_x = max(100, min(spawn_x, (WORLD_WIDTH - 10) * TILE_SIZE))
                        spawn_y = max(100, min(spawn_y, (WORLD_HEIGHT - 10) * TILE_SIZE))
                    
                    # 随机选择怪物类型
                    creature_type = random.choice(list(CREATURES.keys()))
                    self.creatures.append(Creature(creature_type, spawn_x, spawn_y))
                
                # 更新记录
                self.last_spawn_hour = current_hour
                self.last_night_spawn_time = current_time
                print(f"[{time.strftime('%H:%M:%S')}] 夜间生成了{spawn_count}个怪物")

        # 更新液体，传入相机位置以优化性能
        self.world.update_liquids(dt, self.camera_x, self.camera_y)

        # 更新时间
        self.world.update_time(dt)

        # 更新相机
        self.update_camera()

        # 更新方块破坏
        if self.breaking_pos:
            self.update_breaking()

        # 检查并处理生物对玩家的伤害显示
        if hasattr(self.player, 'last_damage_by_creature') and self.player.last_damage_by_creature:
            # 创建伤害文本
            text_x = self.player.x + self.player.width // 2
            text_y = self.player.y - 10  # 在玩家上方显示
            self.damage_texts.append(DamageText(text_x, text_y, self.player.last_damage_amount))
            # 清除标记，避免重复显示
            delattr(self.player, 'last_damage_by_creature')
            delattr(self.player, 'last_damage_amount')
        
        # 检查并处理环境伤害（岩浆、摔伤等）显示
        if hasattr(self.player, 'last_environment_damage_type') and self.player.last_environment_damage_type:
            # 创建伤害文本，传入负值以区分环境伤害，由DamageText类内部处理显示格式
            text_x, text_y = self.player.last_environment_damage_position
            self.damage_texts.append(DamageText(text_x, text_y, -self.player.last_environment_damage_amount))
            # 清除标记，避免重复显示
            self.player.last_environment_damage_type = None
            self.player.last_environment_damage_amount = 0
            self.player.last_environment_damage_position = (0, 0)
            
        # 检查岩浆触碰
        # 为玩家添加岩浆伤害计时器属性（如果不存在）
        if not hasattr(self.player, 'lava_damage_timer'):
            self.player.lava_damage_timer = 0
        
        # 更新玩家岩浆伤害计时器
        self.player.lava_damage_timer = max(0, self.player.lava_damage_timer - dt)
        
        # 检查玩家是否接触岩浆
        player_tile_x = int(self.player.x // TILE_SIZE)
        player_tile_y = int(self.player.y // TILE_SIZE)
        
        # 检查玩家周围3x3范围内的方块
        lava_damage_amount = 15  # 每次受到的伤害值
        lava_damage_interval = 1.0  # 伤害间隔（秒）
        
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                check_x = player_tile_x + dx
                check_y = player_tile_y + dy
                
                if 0 <= check_x < WORLD_WIDTH and 0 <= check_y < WORLD_HEIGHT:
                    if self.world.get_block(check_x, check_y) == LAVA and self.player.lava_damage_timer <= 0:
                            self.player.take_damage(lava_damage_amount, "lava")
                            self.player.lava_damage_timer = lava_damage_interval
                            break
            if self.player.lava_damage_timer > 0:
                break
        
        # 检查生物是否接触岩浆
        for creature in self.creatures[:]:
            # 为生物添加岩浆伤害计时器属性（如果不存在）
            if not hasattr(creature, 'lava_damage_timer'):
                creature.lava_damage_timer = 0
            
            # 更新生物岩浆伤害计时器
            creature.lava_damage_timer = max(0, creature.lava_damage_timer - dt)
            
            # 检查生物是否接触岩浆
            creature_tile_x = int(creature.x // TILE_SIZE)
            creature_tile_y = int(creature.y // TILE_SIZE)
            
            # 检查生物周围3x3范围内的方块
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    check_x = creature_tile_x + dx
                    check_y = creature_tile_y + dy
                    
                    if 0 <= check_x < WORLD_WIDTH and 0 <= check_y < WORLD_HEIGHT:
                        if self.world.get_block(check_x, check_y) == LAVA and creature.lava_damage_timer <= 0:
                            creature.take_damage(lava_damage_amount)
                            creature.lava_damage_timer = lava_damage_interval
                            break
                if creature.lava_damage_timer > 0:
                    break
        
        # 更新伤害文本
        for damage_text in self.damage_texts[:]:
            damage_text.update(dt)
            if damage_text.is_finished():
                self.damage_texts.remove(damage_text)
                
        # 更新箭矢
        for arrow in self.arrows[:]:
            arrow.update(dt, self.world, self.creatures, self)
            # 检查并移除箭矢
            if arrow.is_finished():
                self.arrows.remove(arrow)
                
        # 更新物品实体
        for item_entity in self.item_entities[:]:
            item_entity.update(dt, self.world, self.player)
            # 检查并移除物品实体
            if item_entity.picked_up or item_entity.lifetime <= 0:
                self.item_entities.remove(item_entity)
                
        # 检查玩家是否死亡
        if self.player.is_dead():
            self.is_player_dead = True
    def draw_ui(self, screen):
        """绘制用户界面"""
        # 快捷栏
        hotbar_y = HEIGHT - 70
        
        # 绘制经验值进度条（高15） - 移到更靠上的位置避免与星星文本重叠
        progress_bar_x = 10
        progress_bar_y = hotbar_y - 50  # 移到更靠上的位置
        progress_bar_width = 200
        progress_bar_height = 15
        
        # 进度条背景 - 添加圆角和内阴影效果
        bg_rect = pygame.Rect(progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height)
        # 背景层
        pygame.draw.rect(screen, (40, 40, 40), bg_rect, 0, 5)  # 圆角矩形
        # 内阴影效果
        shadow_surface = pygame.Surface((progress_bar_width, progress_bar_height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, 80), (0, 0, progress_bar_width, progress_bar_height), 0, 5)
        pygame.draw.rect(shadow_surface, (255, 255, 255, 20), (1, 1, progress_bar_width-2, progress_bar_height-2), 0, 4)
        screen.blit(shadow_surface, bg_rect.topleft)
        
        # 计算进度 - 显示经验值进度，每100经验升1星星
        progress = min(self.player.experience / self.player.max_experience, 1.0) if self.player.max_experience > 0 else 0
        
        # 在进度条下方显示星星数量和当前经验值，添加文本阴影
        star_text = font_medium.render(f"星星: {self.player.stars} | 经验: {self.player.experience}/{self.player.max_experience}", True, (255, 215, 0))
        star_shadow = font_medium.render(f"星星: {self.player.stars} | 经验: {self.player.experience}/{self.player.max_experience}", True, (0, 0, 0))
        star_x = 10
        star_y = hotbar_y - 30
        screen.blit(star_shadow, (star_x + 1, star_y + 1))
        screen.blit(star_text, (star_x, star_y))
        
        # 绘制进度条填充 - 金色带有渐变效果
        if progress > 0:
            fill_rect = pygame.Rect(progress_bar_x + 1, progress_bar_y + 1, (progress_bar_width - 2) * progress, progress_bar_height - 2)
            # 创建渐变表面
            gradient_surface = pygame.Surface((fill_rect.width, fill_rect.height), pygame.SRCALPHA)
            for x in range(fill_rect.width):
                alpha = 255 - int(x * 50 / fill_rect.width)
                gradient_surface.set_at((x, 0), (255, 215, 0, alpha))
            pygame.draw.rect(gradient_surface, (255, 230, 100), (0, 0, fill_rect.width, fill_rect.height), 0, 3)
            screen.blit(gradient_surface, fill_rect.topleft)
        
        # 绘制快捷栏背景 - 添加渐变和阴影效果
        hotbar_bg_rect = pygame.Rect(5, hotbar_y - 5, 8 * 60 + 5, 60)
        # 渐变背景
        hotbar_surface = pygame.Surface((hotbar_bg_rect.width, hotbar_bg_rect.height), pygame.SRCALPHA)
        # 创建从下到上的渐变
        for y in range(hotbar_bg_rect.height):
            alpha = 150 + int(y * 50 / hotbar_bg_rect.height)
            pygame.draw.line(hotbar_surface, (60, 60, 80, alpha), (0, y), (hotbar_bg_rect.width, y))
        # 绘制圆角矩形
        pygame.draw.rect(hotbar_surface, (60, 60, 80, 200), (0, 0, hotbar_bg_rect.width, hotbar_bg_rect.height), 0, 8)
        # 顶部高光
        pygame.draw.line(hotbar_surface, (200, 200, 200, 100), (2, 2), (hotbar_bg_rect.width - 4, 2))
        # 绘制到屏幕
        screen.blit(hotbar_surface, hotbar_bg_rect.topleft)
        
        # 绘制快捷栏槽位和物品
        for i in range(8):
            x = 10 + i * 60
            is_selected = (i == self.player.selected_slot)
            
            # 绘制槽位背景
            slot_rect = pygame.Rect(x, hotbar_y, 50, 50)
            if is_selected:
                # 选中的槽位高亮效果
                highlight_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
                pygame.draw.rect(highlight_surface, (255, 215, 0, 80), (0, 0, 50, 50), 0, 4)
                screen.blit(highlight_surface, slot_rect.topleft)
                pygame.draw.rect(screen, (255, 215, 0), slot_rect, 2, 4)
            else:
                # 普通槽位带内阴影
                slot_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
                pygame.draw.rect(slot_surface, (40, 40, 60, 150), (0, 0, 50, 50), 0, 4)
                pygame.draw.rect(slot_surface, (255, 255, 255, 10), (1, 1, 48, 48), 0, 3)
                screen.blit(slot_surface, slot_rect.topleft)
                pygame.draw.rect(screen, (100, 100, 120), slot_rect, 1, 4)

            # 绘制物品
            # 修复：获取快捷栏中正确的物品ID（每个格子是[物品ID, 数量]的列表）
            item_id = self.player.hotbar[i][0]
            if item_id != 0 and self.player.has_item(item_id):
                # 修复：直接从快捷栏获取数量，因为快捷栏中已包含物品ID和数量
                count = self.player.hotbar[i][1]
                item_info = ITEMS.get(item_id)

                if item_info:
                    if item_info["texture"] in self.image_loader.images:
                        screen.blit(
                            pygame.transform.scale(self.image_loader.images[item_info["texture"]], (40, 40)),
                            (x + 5, hotbar_y + 5)
                        )
                    else:
                        # 物品方块带边框和高光
                        pygame.draw.rect(screen, item_info["color"], (x + 5, hotbar_y + 5, 40, 40))
                        pygame.draw.rect(screen, (255, 255, 255, 50), (x + 5, hotbar_y + 5, 40, 40), 1)
                        pygame.draw.line(screen, (255, 255, 255, 80), (x + 5, hotbar_y + 5), (x + 45, hotbar_y + 5), 1)
                        pygame.draw.line(screen, (255, 255, 255, 80), (x + 5, hotbar_y + 5), (x + 5, hotbar_y + 45), 1)

                # 绘制数量 - 添加文本阴影
                count_text = font_small.render(str(count), True, (255, 255, 255))
                count_shadow = font_small.render(str(count), True, (0, 0, 0))
                screen.blit(count_shadow, (x + 36, hotbar_y + 36))
                screen.blit(count_text, (x + 35, hotbar_y + 35))

            # 绘制快捷键 - 添加文本阴影
            key_text = font_small.render(str(i + 1), True, (255, 255, 255))
            key_shadow = font_small.render(str(i + 1), True, (0, 0, 0))
            screen.blit(key_shadow, (x + 6, hotbar_y + 6))
            screen.blit(key_text, (x + 5, hotbar_y + 5))

        # 根据用户需求，移除状态面板背景，只保留状态条显示
        status_panel_width = 220
        
        # 血条 - 普通生命值
        health_bar_length = 200
        health_bar_height = 20
        health_bar_x = 20
        health_bar_y = 20
        health_ratio = self.player.health / self.player.max_health
        
        # 血条背景
        pygame.draw.rect(screen, (60, 20, 20), (health_bar_x, health_bar_y, health_bar_length, health_bar_height), 0, 5)
        # 内阴影效果
        health_shadow = pygame.Surface((health_bar_length, health_bar_height), pygame.SRCALPHA)
        pygame.draw.rect(health_shadow, (0, 0, 0, 50), (0, 0, health_bar_length, health_bar_height), 0, 5)
        pygame.draw.rect(health_shadow, (255, 255, 255, 10), (1, 1, health_bar_length - 2, health_bar_height - 2), 0, 4)
        screen.blit(health_shadow, (health_bar_x, health_bar_y))
        
        # 血条填充 - 红色渐变
        if health_ratio > 0:
            health_fill_rect = pygame.Rect(health_bar_x + 1, health_bar_y + 1, (health_bar_length - 2) * health_ratio, health_bar_height - 2)
            health_gradient = pygame.Surface((health_fill_rect.width, health_fill_rect.height), pygame.SRCALPHA)
            for x in range(health_fill_rect.width):
                r = 255 - int(x * 80 / health_fill_rect.width)
                g = 0
                b = 0
                health_gradient.set_at((x, 0), (r, g, b, 255))
            pygame.draw.rect(health_gradient, (255, 80, 80), (0, 0, health_fill_rect.width, health_fill_rect.height), 0, 3)
            screen.blit(health_gradient, health_fill_rect.topleft)
        
        # 额外生命值血条
        if self.player.extra_health > 0:
            extra_health_bar_length = 200
            extra_health_bar_height = 10
            extra_health_bar_x = 20
            extra_health_bar_y = 45
            
            # 额外生命值血条背景
            pygame.draw.rect(screen, (20, 20, 60), (extra_health_bar_x, extra_health_bar_y, extra_health_bar_length, extra_health_bar_height), 0, 3)
            
            # 额外生命值血条填充 - 蓝色渐变
            extra_health_fill_rect = pygame.Rect(extra_health_bar_x + 1, extra_health_bar_y + 1, extra_health_bar_length - 2, extra_health_bar_height - 2)
            extra_health_gradient = pygame.Surface((extra_health_fill_rect.width, extra_health_fill_rect.height), pygame.SRCALPHA)
            for x in range(extra_health_fill_rect.width):
                r = 0
                g = 0
                b = 255 - int(x * 80 / extra_health_fill_rect.width)
                extra_health_gradient.set_at((x, 0), (r, g, b, 255))
            pygame.draw.rect(extra_health_gradient, (80, 80, 255), (0, 0, extra_health_fill_rect.width, extra_health_fill_rect.height), 0, 2)
            screen.blit(extra_health_gradient, extra_health_fill_rect.topleft)
            
            # 额外生命值图标
            extra_health_icon = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.rect(extra_health_icon, (0, 0, 255), (0, 0, 8, 8))
            screen.blit(extra_health_icon, (extra_health_bar_x - 12, extra_health_bar_y + 1))
        
        # 血条文本 - 添加阴影，显示格式：有额外生命值则100(+10)/100，否则100/100
        if self.player.extra_health > 0:
            health_text = font_medium.render(f"生命值: {int(self.player.health)}(+{int(self.player.extra_health)})/{self.player.max_health}", True, (255, 255, 255))
            health_shadow = font_medium.render(f"生命值: {int(self.player.health)}(+{int(self.player.extra_health)})/{self.player.max_health}", True, (0, 0, 0))
            text_y = 60  # 有额外生命值时的文本位置 - 上调5像素
        else:
            health_text = font_medium.render(f"生命值: {int(self.player.health)}/{self.player.max_health}", True, (255, 255, 255))
            health_shadow = font_medium.render(f"生命值: {int(self.player.health)}/{self.player.max_health}", True, (0, 0, 0))
            text_y = 40  # 无额外生命值时的文本位置 - 上调5像素
        
        screen.blit(health_shadow, (21, text_y + 1))
        screen.blit(health_text, (20, text_y))

        # 饥饿度
        hunger_bar_length = 200
        hunger_bar_height = 20
        hunger_bar_x = 20
        hunger_bar_y = 90  # 饥饿度血条位置
        hunger_ratio = self.player.hunger / self.player.max_hunger
        
        # 饥饿度背景
        pygame.draw.rect(screen, (60, 60, 20), (hunger_bar_x, hunger_bar_y, hunger_bar_length, hunger_bar_height), 0, 5)
        # 内阴影效果
        hunger_shadow = pygame.Surface((hunger_bar_length, hunger_bar_height), pygame.SRCALPHA)
        pygame.draw.rect(hunger_shadow, (0, 0, 0, 50), (0, 0, hunger_bar_length, hunger_bar_height), 0, 5)
        pygame.draw.rect(hunger_shadow, (255, 255, 255, 10), (1, 1, hunger_bar_length - 2, hunger_bar_height - 2), 0, 4)
        screen.blit(hunger_shadow, (hunger_bar_x, hunger_bar_y))
        
        # 饥饿度填充 - 黄色渐变
        if hunger_ratio > 0:
            hunger_fill_rect = pygame.Rect(hunger_bar_x + 1, hunger_bar_y + 1, (hunger_bar_length - 2) * hunger_ratio, hunger_bar_height - 2)
            hunger_gradient = pygame.Surface((hunger_fill_rect.width, hunger_fill_rect.height), pygame.SRCALPHA)
            for x in range(hunger_fill_rect.width):
                r = 255
                g = 255 - int(x * 50 / hunger_fill_rect.width)
                b = 0
                hunger_gradient.set_at((x, 0), (r, g, b, 255))
            pygame.draw.rect(hunger_gradient, (255, 255, 120), (0, 0, hunger_fill_rect.width, hunger_fill_rect.height), 0, 3)
            screen.blit(hunger_gradient, hunger_fill_rect.topleft)
        
        # 饥饿度文本 - 添加阴影（向下移动一些位置）
        hunger_text = font_medium.render(f"饥饿度: {int(self.player.hunger)}/{self.player.max_hunger}", True, (255, 255, 255))
        hunger_shadow = font_medium.render(f"饥饿度: {int(self.player.hunger)}/{self.player.max_hunger}", True, (0, 0, 0))
        screen.blit(hunger_shadow, (21, 115))
        screen.blit(hunger_text, (20, 114))

        # 氧气值 - 只有当氧气不满时才显示
        if self.player.oxygen < self.player.max_oxygen:
            oxygen_bar_length = 200
            oxygen_bar_height = 10  # 变细，从20px改为10px
            oxygen_bar_x = 10
            oxygen_bar_y = hotbar_y - 70 # 调整位置到星星文本上方一点（热键栏上方45像素）
            oxygen_ratio = self.player.oxygen / self.player.max_oxygen
            
            # 氧气背景
            pygame.draw.rect(screen, (20, 20, 60), (oxygen_bar_x, oxygen_bar_y, oxygen_bar_length, oxygen_bar_height), 0, 3)  # 圆角变小
            # 内阴影效果
            oxygen_shadow = pygame.Surface((oxygen_bar_length, oxygen_bar_height), pygame.SRCALPHA)
            pygame.draw.rect(oxygen_shadow, (0, 0, 0, 50), (0, 0, oxygen_bar_length, oxygen_bar_height), 0, 3)
            pygame.draw.rect(oxygen_shadow, (255, 255, 255, 10), (1, 1, oxygen_bar_length - 2, oxygen_bar_height - 2), 0, 2)
            screen.blit(oxygen_shadow, (oxygen_bar_x, oxygen_bar_y))
            
            # 氧气填充 - 蓝色渐变
            if oxygen_ratio > 0:
                oxygen_fill_rect = pygame.Rect(oxygen_bar_x + 1, oxygen_bar_y + 1, (oxygen_bar_length - 2) * oxygen_ratio, oxygen_bar_height - 2)
                oxygen_gradient = pygame.Surface((oxygen_fill_rect.width, oxygen_fill_rect.height), pygame.SRCALPHA)
                for x in range(oxygen_fill_rect.width):
                    r = 0
                    g = 100 - int(x * 20 / oxygen_fill_rect.width)
                    b = 255 - int(x * 80 / oxygen_fill_rect.width)
                    oxygen_gradient.set_at((x, 0), (r, g, b, 255))
                pygame.draw.rect(oxygen_gradient, (100, 180, 255), (0, 0, oxygen_fill_rect.width, oxygen_fill_rect.height), 0, 1)
                screen.blit(oxygen_gradient, oxygen_fill_rect.topleft)
        
        # 无敌状态显示 - 只有当是复活无敌且无敌时间>0时才显示
        if self.player.immune_time > 0 and self.player.is_resurrection_immune:
            # 无敌图标设置
            icon_size = 44  # 使用44x44的方形图片
            icon_x = 20
            icon_y = 145  # 向下调整25像素
            
            # 尝试加载无敌状态图片，不存在则使用橙色替代
            try:
                # 尝试加载无敌状态.png（使用相对路径）
                immunity_icon = pygame.image.load("无敌状态.png").convert_alpha()
                # 调整图片大小以匹配设定的图标尺寸
                immunity_icon = pygame.transform.scale(immunity_icon, (icon_size, icon_size))
                # 创建新的带边框的图标表面
                immunity_icon_with_border = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
                immunity_icon_with_border.blit(immunity_icon, (0, 0))
                # 绘制边框
                pygame.draw.rect(immunity_icon_with_border, (255, 215, 0), (0, 0, icon_size, icon_size), 2, 8)  # 金色边框，增加圆角半径
                immunity_icon = immunity_icon_with_border
            except (pygame.error, FileNotFoundError):
                # 捕获所有可能的图片加载错误，创建橙色背景作为替代
                immunity_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
                pygame.draw.rect(immunity_icon, (255, 165, 0), (0, 0, icon_size, icon_size), 0, 5)  # 橙色圆角矩形
                pygame.draw.rect(immunity_icon, (255, 215, 0), (0, 0, icon_size, icon_size), 2, 5)  # 边框
            
            # 绘制图标
            screen.blit(immunity_icon, (icon_x, icon_y))
            
            # 无敌时间文字 - 放在图标右下方，字体小10%
            status_font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 15)
            time_text = status_font.render(f"{int(self.player.immune_time)}秒", True, (255, 255, 255))
            time_shadow = status_font.render(f"{int(self.player.immune_time)}秒", True, (0, 0, 0))
            # 计算时间文字位置，放在图标右侧（）像素，底部对齐
            text_x = icon_x + icon_size + 2
            text_y = icon_y + icon_size - time_text.get_height()
            screen.blit(time_shadow, (text_x + 1, text_y + 1))
            screen.blit(time_text, (text_x, text_y))
            
        # 燃烧状态显示 - 只有当燃烧时间>0时才显示
        if hasattr(self.player, 'burn_time') and self.player.burn_time > 0:
            # 燃烧图标设置
            icon_size = 44  # 使用44x44的方形图片
            icon_x = 20
            # 根据无敌状态动态调整燃烧图标位置
            # 如果无敌状态存在，则放在无敌图标的下方（间隔10像素）
            # 如果无敌状态不存在，则占据无敌图标的位置
            if hasattr(self.player, 'immune_time') and self.player.immune_time > 0 and getattr(self.player, 'is_resurrection_immune', False):
                icon_y = 195  # 无敌状态存在时，放在无敌图标下方
            else:
                icon_y = 145  # 无敌状态不存在时，占据无敌图标位置
            
            # 尝试加载燃烧状态.png（使用相对路径）
            try:
                burn_icon = pygame.image.load("燃烧状态.png").convert_alpha()
                # 调整图片大小以匹配设定的图标尺寸
                burn_icon = pygame.transform.scale(burn_icon, (icon_size, icon_size))
                # 创建新的带边框的图标表面
                burn_icon_with_border = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
                burn_icon_with_border.blit(burn_icon, (0, 0))
                # 绘制边框
                pygame.draw.rect(burn_icon_with_border, (255, 100, 100), (0, 0, icon_size, icon_size), 2, 8)  # 浅红色边框，增加圆角半径
                burn_icon = burn_icon_with_border
            except (pygame.error, FileNotFoundError):
                # 捕获所有可能的图片加载错误，创建红色背景作为替代
                burn_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
                pygame.draw.rect(burn_icon, (255, 0, 0), (0, 0, icon_size, icon_size), 0, 5)  # 红色圆角矩形
                pygame.draw.rect(burn_icon, (255, 100, 100), (0, 0, icon_size, icon_size), 2, 5)  # 边框
            
            # 绘制图标
            screen.blit(burn_icon, (icon_x, icon_y))
            
            # 燃烧时间文字 - 放在图标右下方，使用英文时间单位
            status_font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 15)
            time_text = status_font.render(f"{int(self.player.burn_time)}s", True, (255, 255, 255))
            time_shadow = status_font.render(f"{int(self.player.burn_time)}s", True, (0, 0, 0))
            # 计算时间文字位置，放在图标右侧，底部对齐
            text_x = icon_x + icon_size + 2
            text_y = icon_y + icon_size - time_text.get_height()
            screen.blit(time_shadow, (text_x + 1, text_y + 1))
            screen.blit(time_text, (text_x, text_y))
            
        # 坐标和时间显示面板
        info_panel_width = 200
        info_panel_height = 80
        info_panel_x = WIDTH - info_panel_width - 10
        info_panel_y = 10
        
        # 面板背景（根据需求降低透明度到50%）
        info_surface = pygame.Surface((info_panel_width, info_panel_height), pygame.SRCALPHA)
        pygame.draw.rect(info_surface, (40, 40, 60, 60), (0, 0, info_panel_width, info_panel_height), 0, 8)  # 透明度调整到60
        # 顶部和左侧高光，降低透明度
        pygame.draw.line(info_surface, (150, 150, 180, 40), (2, 2), (info_panel_width - 4, 2))
        pygame.draw.line(info_surface, (150, 150, 180, 40), (2, 2), (2, info_panel_height - 4))
        screen.blit(info_surface, (info_panel_x, info_panel_y))
        
        # 坐标显示 - 添加文本阴影
        pos_x = int(self.player.x // TILE_SIZE)
        pos_y = int(self.player.y // TILE_SIZE)
        pos_text = font_medium.render(f"坐标: X={pos_x}, Y={pos_y}", True, (255, 255, 255))
        pos_shadow = font_medium.render(f"坐标: X={pos_x}, Y={pos_y}", True, (0, 0, 0))
        screen.blit(pos_shadow, (WIDTH - 200 + 1, 20 + 1))
        screen.blit(pos_text, (WIDTH - 200, 20))

        # 时间显示 - 添加文本阴影和动态颜色
        hours = int(self.world.time_of_day // 100)
        minutes = int(self.world.time_of_day % 100)
        
        # 根据时间设置不同颜色
        if 6 <= hours < 18:  # 白天
            time_color = (255, 255, 255)
        else:  # 夜晚
            time_color = (200, 200, 255)
        
        time_text = font_medium.render(f"时间: {hours:02d}:{minutes:02d}", True, time_color)
        time_shadow = font_medium.render(f"时间: {hours:02d}:{minutes:02d}", True, (0, 0, 0))
        screen.blit(time_shadow, (WIDTH - 200 + 1, 50 + 1))
        screen.blit(time_text, (WIDTH - 200, 50))



    def draw_inventory(self, screen):
        """绘制背包界面，支持30格背包的显示和物品交换，以及箱子UI的显示"""
        # 整体（除快捷栏按钮和背包格外）缩小约30%，原尺寸1000×600
        slot_size = 40  # 保持背包格子尺寸不变
        
        # 设置标题
        if self.player.is_chest_open and self.player.current_chest:
            title = "箱子"
            # 如果只打开箱子，使用单独的更紧凑尺寸420x400
            if not self.player.is_inventory_open:
                inv_width = 420
                inv_height = 400
            else:
                inv_width = 580
                inv_height = 410
        else:
            title = "背包"
            inv_width = 580
            inv_height = 410
            
        inv_x = (WIDTH - inv_width) // 2
        inv_y = (HEIGHT - inv_height) // 2
        slot_margin = 4
        hotbar_size = len(self.player.hotbar)  # 8格快捷栏
        backpack_size = self.player.backpack_slots  # 30格背包

        # 绘制半透明背景覆盖整个屏幕
        bg_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 180))  # 半透明黑色背景
        screen.blit(bg_surface, (0, 0))
        
        # 检查是否显示丢弃数量选择界面
        if hasattr(self, 'show_drop_quantity_input') and self.show_drop_quantity_input and self.item_to_drop:
            # 计算数量输入界面位置 - 进一步优化布局避免文字和按钮重叠
            input_bg_width = 400  # 显著增加宽度提供更宽敞的布局
            input_bg_height = 300  # 增加高度提供更宽敞的布局
            input_bg_x = (WIDTH - input_bg_width) // 2
            input_bg_y = (HEIGHT - input_bg_height) // 2
            
            # 绘制数量输入界面背景（半透明黑色）
            input_bg_rect = pygame.Rect(input_bg_x, input_bg_y, input_bg_width, input_bg_height)
            
            # 添加渐变背景效果
            bg_gradient = pygame.Surface((input_bg_width, input_bg_height), pygame.SRCALPHA)
            for y in range(input_bg_height):
                alpha = 220 - (y / input_bg_height * 40)  # 从下到上透明度降低
                bg_gradient.fill((50, 50, 70, alpha), (0, y, input_bg_width, 1))
            screen.blit(bg_gradient, input_bg_rect)
            
            # 添加边框效果，增强立体感
            pygame.draw.rect(screen, (100, 100, 120), input_bg_rect, 2)  # 外边框
            pygame.draw.rect(screen, (70, 70, 90), (input_bg_x + 2, input_bg_y + 2, input_bg_width - 4, input_bg_height - 4), 1)  # 内边框
            
            # 绘制标题
            item_info = ITEMS.get(self.item_to_drop, {'name': '未知物品'})
            title_text = font_large.render(f"选择丢弃数量", True, (255, 220, 50))
            # 添加标题阴影
            shadow_title = font_large.render(f"选择丢弃数量", True, (0, 0, 0, 150))
            screen.blit(shadow_title, (input_bg_x + input_bg_width // 2 - title_text.get_width() // 2 + 1, input_bg_y + 20 + 1))
            screen.blit(title_text, (input_bg_x + input_bg_width // 2 - title_text.get_width() // 2, input_bg_y + 20))
            
            # 绘制物品图标
            item_size = 48
            item_x = input_bg_x + input_bg_width // 2 - item_size // 2
            item_y = input_bg_y + 60
            item_rect = pygame.Rect(item_x, item_y, item_size, item_size)
            
            if item_info and item_info["texture"] in self.image_loader.images:
                screen.blit(
                    pygame.transform.scale(self.image_loader.images[item_info["texture"]], (item_size, item_size)),
                    item_rect
                )
            else:
                pygame.draw.rect(screen, item_info["color"], item_rect)
            
            # 绘制数量选择滑块区域
            slider_width = 300  # 滑块轨道宽度
            slider_height = 20  # 滑块轨道高度
            slider_x = input_bg_x + input_bg_width // 2 - slider_width // 2
            slider_y = input_bg_y + 140  # 滑块垂直位置
            
            # 计算最大可丢弃数量（累加所有相同物品数量，包括背包和快捷栏）
            max_quantity = 0
            # 计算背包中的物品总数量
            for item_id, quantity in self.player.inventory:
                if item_id == self.item_to_drop:
                    max_quantity += quantity
            # 计算快捷栏中的物品总数量
            for item_id, quantity in self.player.hotbar:
                if item_id == self.item_to_drop:
                    max_quantity += quantity
            
            # 绘制滑块轨道背景
            slider_track_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
            pygame.draw.rect(screen, (70, 70, 90), slider_track_rect, 0, 10)
            
            # 绘制滑块轨道填充（根据当前值）
            fill_width = int((self.quantity_to_drop / max_quantity) * slider_width) if max_quantity > 0 else 0
            slider_fill_rect = pygame.Rect(slider_x, slider_y, fill_width, slider_height)
            pygame.draw.rect(screen, (100, 140, 100), slider_fill_rect, 0, 10)
            
            # 绘制滑块轨道边框
            pygame.draw.rect(screen, (120, 120, 140), slider_track_rect, 2, 10)
            
            # 计算滑块位置
            if max_quantity > 0:
                slider_pos_x = slider_x + (self.quantity_to_drop / max_quantity) * slider_width
            else:
                slider_pos_x = slider_x
            slider_knob_radius = 15  # 滑块旋钮半径
            slider_knob_y = slider_y + slider_height // 2  # 滑块旋钮垂直居中
            
            # 检查鼠标是否悬停在滑块上
            mouse_pos = pygame.mouse.get_pos()
            is_slider_hover = pygame.math.Vector2(slider_pos_x, slider_knob_y).distance_to(mouse_pos) <= slider_knob_radius
            
            # 绘制滑块旋钮
            knob_color = (200, 200, 200) if is_slider_hover else (170, 170, 170)
            pygame.draw.circle(screen, knob_color, (int(slider_pos_x), slider_knob_y), slider_knob_radius)
            pygame.draw.circle(screen, (220, 220, 220), (int(slider_pos_x), slider_knob_y), slider_knob_radius - 3)
            
            # 绘制当前数量显示
            quantity_display_text = font_large.render(f"{self.quantity_to_drop}/{max_quantity}", True, (255, 230, 100))
            # 添加文本阴影
            shadow_quantity = font_large.render(f"{self.quantity_to_drop}/{max_quantity}", True, (0, 0, 0, 120))
            screen.blit(shadow_quantity, (input_bg_x + input_bg_width // 2 - quantity_display_text.get_width() // 2 + 1, slider_y + 40 + 1))
            screen.blit(quantity_display_text, (input_bg_x + input_bg_width // 2 - quantity_display_text.get_width() // 2, slider_y + 40))
            
            # 绘制-和+按钮
            btn_size = 40  # 按钮尺寸
            center_x = input_bg_x + input_bg_width // 2
            minus_btn_x = center_x - btn_size - 60  # -按钮位置
            plus_btn_x = center_x + 60  # +按钮位置
            btn_y = slider_y + 40  # 按钮垂直位置 (向上调整40像素)
            
            # 检查鼠标是否悬停在按钮上
            is_minus_hover = pygame.Rect(minus_btn_x, btn_y, btn_size, btn_size).collidepoint(mouse_pos)
            is_plus_hover = pygame.Rect(plus_btn_x, btn_y, btn_size, btn_size).collidepoint(mouse_pos)
            
            # -按钮
            minus_btn_rect = pygame.Rect(minus_btn_x, btn_y, btn_size, btn_size)
            minus_surface = pygame.Surface((btn_size, btn_size), pygame.SRCALPHA)
            # 根据悬停状态改变按钮颜色
            if is_minus_hover:
                pygame.draw.rect(minus_surface, (120, 80, 80, 240), (0, 0, btn_size, btn_size), 0, 8)
                pygame.draw.rect(minus_surface, (140, 100, 100, 100), (0, 0, btn_size, btn_size//2), 0, 8)
            else:
                pygame.draw.rect(minus_surface, (100, 60, 60, 220), (0, 0, btn_size, btn_size), 0, 8)
                pygame.draw.rect(minus_surface, (120, 80, 80, 80), (0, 0, btn_size, btn_size//2), 0, 8)
            screen.blit(minus_surface, minus_btn_rect)
            pygame.draw.rect(screen, (200, 200, 200), minus_btn_rect, 2, 8)
            
            minus_text = font_large.render("-", True, (255, 255, 255))
            minus_text_x = minus_btn_x + btn_size // 2 - minus_text.get_width() // 2
            minus_text_y = btn_y + btn_size // 2 - minus_text.get_height() // 2
            # 添加文本阴影
            shadow_minus = font_large.render("-", True, (0, 0, 0, 150))
            screen.blit(shadow_minus, (minus_text_x + 1, minus_text_y + 1))
            screen.blit(minus_text, (minus_text_x, minus_text_y))
            
            # +按钮
            plus_btn_rect = pygame.Rect(plus_btn_x, btn_y, btn_size, btn_size)
            plus_surface = pygame.Surface((btn_size, btn_size), pygame.SRCALPHA)
            # 根据悬停状态改变按钮颜色
            if is_plus_hover:
                pygame.draw.rect(plus_surface, (80, 120, 80, 240), (0, 0, btn_size, btn_size), 0, 8)
                pygame.draw.rect(plus_surface, (100, 140, 100, 100), (0, 0, btn_size, btn_size//2), 0, 8)
            else:
                pygame.draw.rect(plus_surface, (60, 100, 60, 220), (0, 0, btn_size, btn_size), 0, 8)
                pygame.draw.rect(plus_surface, (80, 120, 80, 80), (0, 0, btn_size, btn_size//2), 0, 8)
            screen.blit(plus_surface, plus_btn_rect)
            pygame.draw.rect(screen, (200, 200, 200), plus_btn_rect, 2, 8)
            
            plus_text = font_large.render("+", True, (255, 255, 255))
            plus_text_x = plus_btn_x + btn_size // 2 - plus_text.get_width() // 2
            plus_text_y = btn_y + btn_size // 2 - plus_text.get_height() // 2
            # 添加文本阴影
            shadow_plus = font_large.render("+", True, (0, 0, 0, 150))
            screen.blit(shadow_plus, (plus_text_x + 1, plus_text_y + 1))
            screen.blit(plus_text, (plus_text_x, plus_text_y))
            
            # 保存滑块和按钮矩形供点击检测
            slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height + 2 * slider_knob_radius)
            
            # 绘制确认按钮
            confirm_width = 120
            confirm_height = 45
            confirm_x = input_bg_x + input_bg_width - confirm_width - 25
            confirm_y = input_bg_y + input_bg_height - confirm_height - 25  # 调整位置，增加与上方元素的间距
            
            # 检查鼠标是否悬停在确认按钮上
            is_confirm_hover = pygame.Rect(confirm_x, confirm_y, confirm_width, confirm_height).collidepoint(mouse_pos)
            
            confirm_btn_rect = pygame.Rect(confirm_x, confirm_y, confirm_width, confirm_height)
            confirm_surface = pygame.Surface((confirm_width, confirm_height), pygame.SRCALPHA)
            # 根据悬停状态改变按钮颜色
            if is_confirm_hover:
                pygame.draw.rect(confirm_surface, (100, 140, 100, 240), (0, 0, confirm_width, confirm_height), 0, 8)
                pygame.draw.rect(confirm_surface, (120, 160, 120, 100), (0, 0, confirm_width, confirm_height//2), 0, 8)
            else:
                pygame.draw.rect(confirm_surface, (80, 120, 80, 220), (0, 0, confirm_width, confirm_height), 0, 8)
                pygame.draw.rect(confirm_surface, (100, 140, 100, 80), (0, 0, confirm_width, confirm_height//2), 0, 8)
            screen.blit(confirm_surface, confirm_btn_rect)
            pygame.draw.rect(screen, (200, 200, 200), confirm_btn_rect, 2, 8)
            
            confirm_text = font_small.render("确认", True, (255, 255, 255))
            confirm_text_x = confirm_x + confirm_width // 2 - confirm_text.get_width() // 2
            confirm_text_y = confirm_y + confirm_height // 2 - confirm_text.get_height() // 2
            # 添加文本阴影
            shadow_confirm = font_small.render("确认", True, (0, 0, 0, 150))
            screen.blit(shadow_confirm, (confirm_text_x + 1, confirm_text_y + 1))
            screen.blit(confirm_text, (confirm_text_x, confirm_text_y))
            
            # 绘制取消按钮
            cancel_width = 120
            cancel_height = 45
            cancel_x = input_bg_x + 25
            cancel_y = input_bg_y + input_bg_height - cancel_height - 25  # 调整位置，增加与上方元素的间距
            
            # 检查鼠标是否悬停在取消按钮上
            is_cancel_hover = pygame.Rect(cancel_x, cancel_y, cancel_width, cancel_height).collidepoint(mouse_pos)
            
            cancel_btn_rect = pygame.Rect(cancel_x, cancel_y, cancel_width, cancel_height)
            cancel_surface = pygame.Surface((cancel_width, cancel_height), pygame.SRCALPHA)
            # 根据悬停状态改变按钮颜色
            if is_cancel_hover:
                pygame.draw.rect(cancel_surface, (140, 100, 100, 240), (0, 0, cancel_width, cancel_height), 0, 8)
                pygame.draw.rect(cancel_surface, (160, 120, 120, 100), (0, 0, cancel_width, cancel_height//2), 0, 8)
            else:
                pygame.draw.rect(cancel_surface, (120, 80, 80, 220), (0, 0, cancel_width, cancel_height), 0, 8)
                pygame.draw.rect(cancel_surface, (140, 100, 100, 80), (0, 0, cancel_width, cancel_height//2), 0, 8)
            screen.blit(cancel_surface, cancel_btn_rect)
            pygame.draw.rect(screen, (200, 200, 200), cancel_btn_rect, 2, 8)
            
            cancel_text = font_small.render("取消", True, (255, 255, 255))
            cancel_text_x = cancel_x + cancel_width // 2 - cancel_text.get_width() // 2
            cancel_text_y = cancel_y + cancel_height // 2 - cancel_text.get_height() // 2
            # 添加文本阴影
            shadow_cancel = font_small.render("取消", True, (0, 0, 0, 150))
            screen.blit(shadow_cancel, (cancel_text_x + 1, cancel_text_y + 1))
            screen.blit(cancel_text, (cancel_text_x, cancel_text_y))
            
            # 绘制全部丢弃按钮（在取消和确定中间）
            drop_all_width = 120
            drop_all_height = 45
            drop_all_x = (cancel_x + cancel_width + confirm_x) // 2 - drop_all_width // 2  # 居中在取消和确定按钮之间
            drop_all_y = input_bg_y + input_bg_height - drop_all_height - 25  # 与其他按钮在同一水平线上
            
            # 检查鼠标是否悬停在全部丢弃按钮上
            is_drop_all_hover = pygame.Rect(drop_all_x, drop_all_y, drop_all_width, drop_all_height).collidepoint(mouse_pos)
            
            drop_all_btn_rect = pygame.Rect(drop_all_x, drop_all_y, drop_all_width, drop_all_height)
            drop_all_surface = pygame.Surface((drop_all_width, drop_all_height), pygame.SRCALPHA)
            # 根据悬停状态改变按钮颜色
            if is_drop_all_hover:
                pygame.draw.rect(drop_all_surface, (140, 120, 80, 240), (0, 0, drop_all_width, drop_all_height), 0, 8)
                pygame.draw.rect(drop_all_surface, (160, 140, 100, 100), (0, 0, drop_all_width, drop_all_height//2), 0, 8)
            else:
                pygame.draw.rect(drop_all_surface, (120, 100, 60, 220), (0, 0, drop_all_width, drop_all_height), 0, 8)
                pygame.draw.rect(drop_all_surface, (140, 120, 80, 80), (0, 0, drop_all_width, drop_all_height//2), 0, 8)
            screen.blit(drop_all_surface, drop_all_btn_rect)
            pygame.draw.rect(screen, (200, 200, 200), drop_all_btn_rect, 2, 8)
            
            drop_all_text = font_small.render("全部丢弃", True, (255, 255, 255))
            drop_all_text_x = drop_all_x + drop_all_width // 2 - drop_all_text.get_width() // 2
            drop_all_text_y = drop_all_y + drop_all_height // 2 - drop_all_text.get_height() // 2
            # 添加文本阴影
            shadow_drop_all = font_small.render("全部丢弃", True, (0, 0, 0, 150))
            screen.blit(shadow_drop_all, (drop_all_text_x + 1, drop_all_text_y + 1))
            screen.blit(drop_all_text, (drop_all_text_x, drop_all_text_y))
            
            # 保存按钮矩形供点击检测
            if not hasattr(self, 'drop_quantity_rect') or self.drop_quantity_rect is None:
                self.drop_quantity_rect = {}
            self.drop_quantity_rect.update({
                "slider": slider_rect,
                "minus": minus_btn_rect,
                "plus": plus_btn_rect,
                "confirm": confirm_btn_rect,
                "cancel": cancel_btn_rect,
                "drop_all": drop_all_btn_rect,
                "background": input_bg_rect
            })
            
            # 绘制提示文本 - 显示物品名称
            item_name_text = font_small.render(f"物品: {item_info['name']}", True, (220, 220, 220))
            screen.blit(item_name_text, (input_bg_x + 40, input_bg_y + 100))
            
            # 绘制最大可丢弃数量
            max_quantity = 0
            for item_id, quantity in self.player.inventory:
                if item_id == self.item_to_drop:
                    max_quantity = quantity
                    break
            max_text = font_small.render(f"最大: {max_quantity}", True, (220, 220, 220))
            screen.blit(max_text, (input_bg_x + input_bg_width - 120, input_bg_y + 100))
            
            return  # 先返回，避免绘制背包界面


        # 绘制现代化背包背景和边框
        s = pygame.Surface((inv_width, inv_height), pygame.SRCALPHA)
        s.fill((50, 50, 50, 240))  # 略微加深背景色，提高不透明度
        screen.blit(s, (inv_x, inv_y))
        
        # 添加现代化边框效果
        pygame.draw.rect(screen, (100, 100, 100), (inv_x, inv_y, inv_width, inv_height), 1)  # 内边框
        pygame.draw.rect(screen, (70, 70, 70), (inv_x+1, inv_y+1, inv_width-2, inv_height-2), 1)  # 次内边框
        pygame.draw.rect(screen, (40, 40, 40), (inv_x-1, inv_y-1, inv_width+2, inv_height+2), 1)  # 外边框

        # 添加顶部光泽效果
        gloss_surface = pygame.Surface((inv_width, inv_height//3), pygame.SRCALPHA)
        for y in range(gloss_surface.get_height()):
            alpha = 30 - (y / gloss_surface.get_height() * 30)
            pygame.draw.line(gloss_surface, (255, 255, 255, alpha), 
                            (0, y), (gloss_surface.get_width(), y))
        screen.blit(gloss_surface, (inv_x, inv_y))

        # 绘制标题，位置调整为缩小后的比例
        title_text = font_large.render(title, True, (255, 255, 255))
        shadow_text = font_large.render(title, True, (0, 0, 0, 120))
        screen.blit(shadow_text, (inv_x + 280 + 1, inv_y + 10 + 1))  # 420 * 0.7 = 294，略微调整位置
        screen.blit(title_text, (inv_x + 280, inv_y + 10))


        # 绘制关闭按钮，尺寸调整为
        close_button_rect = pygame.Rect(inv_x + 530, inv_y + 5, 40, 40)  # 920 * 0.7 - 原inv_x的变化需要调整位置
        mouse_pos = pygame.mouse.get_pos()
        is_close_hovered = close_button_rect.collidepoint(mouse_pos)
        self.draw_button(screen, close_button_rect, "X", is_close_hovered, False, 'danger')

        # 如果打开了箱子，先绘制箱子内容
        if self.player.is_chest_open and self.player.current_chest:
            # 箱子格子（20格，5行4列）
            chest_rows = 5
            chest_cols = 4
            
            # 计算箱子内容居中位置
            chest_content_width = chest_cols * (slot_size + slot_margin)
            chest_content_height = chest_rows * (slot_size + slot_margin)
            
            # 无论是否同时打开背包，都将箱子内容放在左侧，背包放在右侧
            chest_start_x = inv_x + 30
            chest_start_y = inv_y + 60  # 留出标题空间
            
            # 绘制箱子标题，添加现代风格
            chest_title = font_medium.render("箱子内容", True, (255, 255, 255))
            # 标题阴影
            chest_shadow = font_medium.render("箱子内容", True, (0, 0, 0, 120))
            screen.blit(chest_shadow, (chest_start_x + 1, inv_y + 35))
            screen.blit(chest_title, (chest_start_x, inv_y + 34))
            
            # 绘制箱子内容区域背景
            chest_area_rect = pygame.Rect(chest_start_x - 10, chest_start_y - 10, 
                                        chest_cols * (slot_size + slot_margin) + 20, 
                                        chest_rows * (slot_size + slot_margin) + 20)
            
            chest_bg = pygame.Surface((chest_area_rect.width, chest_area_rect.height), pygame.SRCALPHA)
            chest_bg.fill((60, 60, 60, 180))
            screen.blit(chest_bg, (chest_area_rect.x, chest_area_rect.y))
            pygame.draw.rect(screen, (80, 80, 80), chest_area_rect, 1)
            
            # 获取箱子中的物品列表
            chest_items = self.player.current_chest.items.copy()
            
            # 确保列表长度为20，不足的用None填充
            while len(chest_items) < 20:
                chest_items.append(None)
            
            for i in range(20):
                row = i // chest_cols
                col = i % chest_cols
                x = chest_start_x + col * (slot_size + slot_margin)
                y = chest_start_y + row * (slot_size + slot_margin)
                
                # 绘制现代化槽位（圆角矩形，带悬停效果）
                slot_rect = pygame.Rect(x, y, slot_size, slot_size)
                is_slot_hovered = slot_rect.collidepoint(mouse_pos)
                
                # 槽位背景
                slot_bg_color = (70, 70, 70) if not is_slot_hovered else (80, 80, 80)
                pygame.draw.rect(screen, slot_bg_color, slot_rect, 0, 3)  # 圆角
                
                # 槽位边框 - 显示红色边缘
                slot_border_color = (255, 0, 0)  # 红色边框
                # 检查槽位是否在屏幕内
                if 0 <= slot_rect.x < WIDTH and 0 <= slot_rect.y < HEIGHT:
                    pygame.draw.rect(screen, slot_border_color, slot_rect, 2, 3)  # 加粗红色边框表示在屏幕内
                else:
                    # 槽位不在屏幕内时使用淡红色边框
                    pygame.draw.rect(screen, (150, 0, 0), slot_rect, 1, 3)
                
                # 绘制物品
                if i < len(chest_items) and chest_items[i]:
                    item_id, count = chest_items[i]
                    item_info = ITEMS.get(item_id)
                    
                    if item_info:
                        if item_info["texture"] in self.image_loader.images:
                            screen.blit(
                                pygame.transform.scale(self.image_loader.images[item_info["texture"]], (32, 32)),
                                (x + 4, y + 4)
                            )
                        elif "color" in item_info:
                            pygame.draw.rect(screen, item_info["color"], (x + 4, y + 4, 32, 32))
                    
                    # 绘制数量
                    count_text = font_small.render(str(count), True, (255, 255, 255))
                    screen.blit(count_text, (x + 28, y + 28))
        
        # 当背包打开或箱子打开时，都绘制快捷栏，方便交互
        if self.player.is_inventory_open or (self.player.is_chest_open and self.player.current_chest):
            # 绘制快捷栏（8格）：保持按钮尺寸不变
            # 注意：快捷栏y坐标看起来是相对于屏幕的，这里做适当调整以适应背包界面
            hotbar_start_x = inv_x + 80
            hotbar_start_y = inv_y + inv_height - 80
            
            # 绘制快捷栏区域背景 - 保持按钮尺寸不变，只调整背景区域大小
            hotbar_area_rect = pygame.Rect(hotbar_start_x - 10, hotbar_start_y - 10, 
                                         hotbar_size * (slot_size + slot_margin) + 20, 
                                         slot_size + 20)
            hotbar_bg = pygame.Surface((hotbar_area_rect.width, hotbar_area_rect.height), pygame.SRCALPHA)
            hotbar_bg.fill((60, 60, 60, 180))
            screen.blit(hotbar_bg, (hotbar_area_rect.x, hotbar_area_rect.y))
            pygame.draw.rect(screen, (80, 80, 80), hotbar_area_rect, 1)
            
            # 绘制快捷栏标题
            hotbar_title = font_small.render("快捷栏", True, (200, 200, 200))
            screen.blit(hotbar_title, (hotbar_start_x, hotbar_start_y - 20))
            
            for i in range(hotbar_size):
                x = hotbar_start_x + i * (slot_size + slot_margin)
                y = hotbar_start_y
                
                # 绘制现代化槽位（圆角矩形，带悬停效果）
                slot_rect = pygame.Rect(x, y, slot_size, slot_size)
                is_slot_hovered = slot_rect.collidepoint(mouse_pos)
                is_selected = (i == self.player.selected_slot)
                
                # 槽位背景
                if is_selected:
                    slot_bg_color = (80, 80, 120)  # 选中的背景色
                else:
                    slot_bg_color = (70, 70, 70) if not is_slot_hovered else (80, 80, 80)
                pygame.draw.rect(screen, slot_bg_color, slot_rect, 0, 3)  # 圆角
                
                # 槽位边框
                if is_selected:
                    slot_border_color = UI_HIGHLIGHT
                else:
                    slot_border_color = (100, 100, 100) if not is_slot_hovered else UI_HIGHLIGHT
                pygame.draw.rect(screen, slot_border_color, slot_rect, 1, 3)
                
                # 绘制物品
                item_data = self.player.hotbar[i]
                item_id, count = item_data
                if item_id != 0 and count > 0:
                    item_info = ITEMS.get(item_id)
                    
                    if item_info:
                        if item_info["texture"] in self.image_loader.images:
                            screen.blit(
                                pygame.transform.scale(self.image_loader.images[item_info["texture"]], (32, 32)),
                                (x + 4, y + 4)
                            )
                        else:
                            pygame.draw.rect(screen, item_info["color"], (x + 4, y + 4, 32, 32))
                    
                    # 绘制数量
                    count_text = font_small.render(str(count), True, (255, 255, 255))
                    screen.blit(count_text, (x + 28, y + 28))
                
                # 绘制快捷键
                key_text = font_small.render(str(i + 1), True, (255, 255, 255))
                screen.blit(key_text, (x + 2, y + 2))
            
            # 绘制装备底位置（x=20,y=85,大小210*260，缩小约30%）
            equipment_area_rect = pygame.Rect(inv_x + 20, inv_y + 45, 210, 260)  # 295*0.7≈206.5，取210；372*0.7≈260
            equipment_bg = pygame.Surface((equipment_area_rect.width, equipment_area_rect.height), pygame.SRCALPHA)
            equipment_bg.fill((60, 60, 60, 180))
            screen.blit(equipment_bg, (equipment_area_rect.x, equipment_area_rect.y))
            pygame.draw.rect(screen, (80, 80, 80), equipment_area_rect, 1)
            
            # 绘制装备头盔底：尺寸缩小30%，从80*80变为56*56，调整位置
            helmet_slot_rect = pygame.Rect(inv_x + 60, inv_y + 65, 56, 56)
            pygame.draw.rect(screen, (70, 70, 70), helmet_slot_rect)
            pygame.draw.rect(screen, (100, 100, 100), helmet_slot_rect, 2)
            
            # 绘制装备头盔槽中的物品
            if self.player.equipment['helmet']:
                helmet_item_id = self.player.equipment['helmet']
                helmet_info = ITEMS.get(helmet_item_id)
                if helmet_info:
                    # 绘制装备物品图标
                    if helmet_info['texture'] in self.image_loader.images:
                        screen.blit(
                            pygame.transform.scale(self.image_loader.images[helmet_info['texture']], (48, 48)),
                            (helmet_slot_rect.x + 4, helmet_slot_rect.y + 4)
                        )
                    else:
                        # 如果没有图片，使用颜色块代替
                        if 'color' in helmet_info:
                            pygame.draw.rect(screen, helmet_info['color'], (helmet_slot_rect.x + 4, helmet_slot_rect.y + 4, 48, 48))
            
            # 绘制盔甲底：尺寸缩小30%，从80*80变为56*56，调整位置
            armor_slot_rect = pygame.Rect(inv_x + 130, inv_y + 65, 56, 56)
            pygame.draw.rect(screen, (70, 70, 70), armor_slot_rect)
            pygame.draw.rect(screen, (100, 100, 100), armor_slot_rect, 2)
            
            # 绘制装备盔甲槽中的物品
            if self.player.equipment['armor']:
                armor_item_id = self.player.equipment['armor']
                armor_info = ITEMS.get(armor_item_id)
                if armor_info:
                    # 绘制装备物品图标
                    if armor_info['texture'] in self.image_loader.images:
                        screen.blit(
                            pygame.transform.scale(self.image_loader.images[armor_info['texture']], (48, 48)),
                            (armor_slot_rect.x + 4, armor_slot_rect.y + 4)
                        )
                    else:
                        # 如果没有图片，使用颜色块代替
                        if 'color' in armor_info:
                            pygame.draw.rect(screen, armor_info['color'], (armor_slot_rect.x + 4, armor_slot_rect.y + 4, 48, 48))
            
            # 绘制靴子底：尺寸缩小30%，从80*80变为56*56，调整位置
            boots_slot_rect = pygame.Rect(inv_x + 60, inv_y + 130, 56, 56)
            pygame.draw.rect(screen, (70, 70, 70), boots_slot_rect)
            pygame.draw.rect(screen, (100, 100, 100), boots_slot_rect, 2)
            
            # 绘制装备靴子槽中的物品
            if self.player.equipment['boots']:
                boots_item_id = self.player.equipment['boots']
                boots_info = ITEMS.get(boots_item_id)
                if boots_info:
                    # 绘制装备物品图标
                    if boots_info['texture'] in self.image_loader.images:
                        screen.blit(
                            pygame.transform.scale(self.image_loader.images[boots_info['texture']], (48, 48)),
                            (boots_slot_rect.x + 4, boots_slot_rect.y + 4)
                        )
                    else:
                        # 如果没有图片，使用颜色块代替
                        if 'color' in boots_info:
                            pygame.draw.rect(screen, boots_info['color'], (boots_slot_rect.x + 4, boots_slot_rect.y + 4, 48, 48))
            
            # 绘制特殊底：尺寸缩小30%，从80*80变为56*56，调整位置
            special_slot_rect = pygame.Rect(inv_x + 130, inv_y + 130, 56, 56)
            pygame.draw.rect(screen, (70, 70, 70), special_slot_rect)
            pygame.draw.rect(screen, (100, 100, 100), special_slot_rect, 2)
            
            # 绘制装备特殊槽中的物品
            if self.player.equipment['special']:
                special_item_id = self.player.equipment['special']
                special_info = ITEMS.get(special_item_id)
                if special_info:
                    # 绘制装备物品图标
                    if special_info['texture'] in self.image_loader.images:
                        screen.blit(
                            pygame.transform.scale(self.image_loader.images[special_info['texture']], (48, 48)),
                            (special_slot_rect.x + 4, special_slot_rect.y + 4)
                        )
                    else:
                        # 如果没有图片，使用颜色块代替
                        if 'color' in special_info:
                            pygame.draw.rect(screen, special_info['color'], (special_slot_rect.x + 4, special_slot_rect.y + 4, 48, 48))
        
        # 仅当背包打开时，才绘制显示属性区域
        if self.player.is_inventory_open:
            # 绘制显示属性位置：x=25y=280，大小190*100，缩小约30%
            stats_area_rect = pygame.Rect(inv_x + 30, inv_y + 200, 190, 100)  # 265*0.7≈185.5，取190；140*0.7=98，取100
            stats_bg = pygame.Surface((stats_area_rect.width, stats_area_rect.height), pygame.SRCALPHA)
            stats_bg.fill((50, 50, 50, 180))
            screen.blit(stats_bg, (stats_area_rect.x, stats_area_rect.y))
            pygame.draw.rect(screen, (80, 80, 80), stats_area_rect, 1)
            
            # 在属性区域内显示防御、免伤、伤害、摔伤和移速属性
            # 设置字体大小和位置偏移
            stat_font = font_small  # 使用小号字体以适应区域
            line_height = 18
            start_y = stats_area_rect.y + 10
            
            # 防御
            defense_text = stat_font.render(f"防御: {self.player.defense}", True, (255, 255, 255))
            screen.blit(defense_text, (stats_area_rect.x + 10, start_y))
            
            # 免伤
            damage_reduction_text = stat_font.render(f"免伤: {self.player.damage_reduction}%", True, (255, 255, 255))
            screen.blit(damage_reduction_text, (stats_area_rect.x + 10, start_y + line_height))
            
            # 伤害
            damage_bonus_text = stat_font.render(f"伤害: {self.player.damage_bonus}%", True, (255, 255, 255))
            screen.blit(damage_bonus_text, (stats_area_rect.x + 10, start_y + line_height * 2))
            
            # 摔伤
            fall_damage_text = stat_font.render(f"摔伤: {self.player.fall_damage_reduction}%", True, (255, 255, 255))
            screen.blit(fall_damage_text, (stats_area_rect.x + 10, start_y + line_height * 3))
            
            # 移速
            speed_bonus_text = stat_font.render(f"移速: {self.player.speed_bonus}%", True, (255, 255, 255))
            screen.blit(speed_bonus_text, (stats_area_rect.x + 10, start_y + line_height * 4))
        
        # 当背包打开或箱子打开时，都绘制背包内容，方便交互
        if self.player.is_inventory_open or (self.player.is_chest_open and self.player.current_chest):
            # 初始化背包格子参数：x=251y=58大小:420*250，缩小约30%（保持格子尺寸不变）
            rows = 5
            cols = 6
            backpack_start_x = inv_x + 251  # 358*0.7≈250.6，取251
            backpack_start_y = inv_y + 58  # 83*0.7≈58.1，取58
            
            # 根据不同界面状态绘制不同的背包背景
            if self.player.is_chest_open and self.player.current_chest:
                # 箱子界面中，背包位于右侧
                # 调整背包起始位置，使其不与箱子重叠
                backpack_start_x = inv_x + 200  # 调整为更靠右的位置
                
                # 绘制背包标题，添加现代风格
                backpack_title = font_medium.render("你的背包", True, (255, 255, 255))
                # 标题阴影
                backpack_shadow = font_medium.render("你的背包", True, (0, 0, 0, 120))
                screen.blit(backpack_shadow, (backpack_start_x + 1, inv_y + 35))
                screen.blit(backpack_title, (backpack_start_x, inv_y + 34))
                
                # 绘制背包内容区域背景 - 缩小约30%
                backpack_area_rect = pygame.Rect(backpack_start_x - 10, backpack_start_y - 10, 280, 250)  # 调整宽度，避免重叠
                backpack_bg = pygame.Surface((backpack_area_rect.width, backpack_area_rect.height), pygame.SRCALPHA)
                backpack_bg.fill((60, 60, 60, 180))
                screen.blit(backpack_bg, (backpack_area_rect.x, backpack_area_rect.y))
                pygame.draw.rect(screen, (80, 80, 80), backpack_area_rect, 1)
            elif self.player.is_inventory_open:
                # 普通背包界面
                # 绘制背包内容区域背景 - 缩小约30%
                backpack_area_rect = pygame.Rect(backpack_start_x - 10, backpack_start_y - 10, 290, 250)  # 620*0.7≈434，调整为420以适应5x6布局；372*0.7≈260，取250
                backpack_bg = pygame.Surface((backpack_area_rect.width, backpack_area_rect.height), pygame.SRCALPHA)
                backpack_bg.fill((70, 70, 70, 180))
                screen.blit(backpack_bg, (backpack_area_rect.x, backpack_area_rect.y))
                pygame.draw.rect(screen, (100, 100, 100), backpack_area_rect, 2)
            
            # 背包物品列表直接使用inventory列表（每个元素是[物品ID, 数量]）
            backpack_items = []
            for item_data in self.player.inventory:
                try:
                    # 确保item_data是有效的格式
                    if isinstance(item_data, (list, tuple)) and len(item_data) >= 2:
                        item_id, count = item_data
                        if item_id != 0:
                            backpack_items.append((item_id, count))
                        else:
                            backpack_items.append(None)
                    else:
                        # 如果格式不正确，添加None占位
                        backpack_items.append(None)
                except (ValueError, TypeError):
                    # 捕获任何可能的解包错误
                    backpack_items.append(None)
            
            # 绘制背包内容
            for i in range(backpack_size):
                row = i // cols
                col = i % cols
                x = backpack_start_x + col * (slot_size + slot_margin)
                y = backpack_start_y + row * (slot_size + slot_margin)
                
                # 绘制现代化槽位（圆角矩形，带悬停效果）
                slot_rect = pygame.Rect(x, y, slot_size, slot_size)
                is_slot_hovered = slot_rect.collidepoint(mouse_pos)
                
                # 槽位背景
                slot_bg_color = (70, 70, 70) if not is_slot_hovered else (80, 80, 80)
                pygame.draw.rect(screen, slot_bg_color, slot_rect, 0, 3)  # 圆角
                
                # 槽位边框
                slot_border_color = (100, 100, 100) if not is_slot_hovered else UI_HIGHLIGHT
                pygame.draw.rect(screen, slot_border_color, slot_rect, 1, 3)
                
                # 绘制物品
                if i < len(backpack_items) and backpack_items[i]:
                    item_id, count = backpack_items[i]
                    item_info = ITEMS.get(item_id)
                    
                    if item_info:
                        if item_info["texture"] in self.image_loader.images:
                            screen.blit(
                                pygame.transform.scale(self.image_loader.images[item_info["texture"]], (32, 32)),
                                (x + 4, y + 4)
                            )
                        elif "color" in item_info:
                            pygame.draw.rect(screen, item_info["color"], (x + 4, y + 4, 32, 32))
                    
                    # 绘制数量
                    count_text = font_small.render(str(count), True, (255, 255, 255))
                    screen.blit(count_text, (x + 28, y + 28))
            
        # 绘制销毁区域（仅在普通背包界面中显示）
        if self.player.is_inventory_open and (not self.player.is_chest_open or not self.player.current_chest):
            # 绘制丢弃按钮：尺寸调整为60*60
            destroy_area_rect = pygame.Rect(inv_x + 460, inv_y + 340, 50, 50)  # 880*0.7≈616，485*0.7≈339.5，取340
            is_destroy_hovered = destroy_area_rect.collidepoint(mouse_pos)
            
            # 使用现代化按钮样式绘制丢弃区域
            self.draw_button(screen, destroy_area_rect, "丢弃", is_destroy_hovered, False, 'danger')
        
        # 绘制拖动的物品（如果有）
        if self.player.dragging_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            item_id = self.player.dragging_item["item_id"]
            quantity = self.player.dragging_item["quantity"]
            item_info = ITEMS.get(item_id)
            
            if item_info and item_info["texture"] in self.image_loader.images:
                screen.blit(
                    pygame.transform.scale(self.image_loader.images[item_info["texture"]], (48, 48)),
                    (mouse_x - 24, mouse_y - 24)
                )
            else:
                pygame.draw.rect(screen, item_info["color"], (mouse_x - 24, mouse_y - 24, 48, 48))
            
            # 绘制数量，添加背景使数字更清晰
            count_text = font_medium.render(str(quantity), True, (255, 255, 255))
            # 数量文本背景
            count_bg = pygame.Surface((count_text.get_width() + 8, count_text.get_height() + 4), pygame.SRCALPHA)
            count_bg.fill((0, 0, 0, 180))
            screen.blit(count_bg, (mouse_x + 8, mouse_y + 8))
            screen.blit(count_text, (mouse_x + 12, mouse_y + 10))
            
        # 绘制操作提示
        help_text = font_small.render("鼠标拖放物品 | 点击ESC关闭", True, (200, 200, 200))
        help_x = inv_x + inv_width // 2 - help_text.get_width() // 2
        help_y = inv_y + inv_height - 25
        screen.blit(help_text, (help_x, help_y))
        
        return close_button_rect  # 返回关闭按钮矩形，以便处理点击事件

    def draw_crafting(self, screen):
        """绘制合成界面"""
        # 绘制半透明背景
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        screen.blit(s, (0, 0))
        
        # 绘制界面标题 - 添加阴影效果
        title_text = "合成界面"
        title = font_large.render(title_text, True, (255, 215, 0))  # 金色标题
        title_shadow = font_large.render(title_text, True, (0, 0, 0))  # 黑色阴影
        title_x = WIDTH // 2 - title.get_width() // 2
        title_y = 50
        # 先绘制阴影，再绘制标题，创建阴影效果
        screen.blit(title_shadow, (title_x + 2, title_y + 2))
        screen.blit(title, (title_x, title_y))
        
        # 定义界面参数
        item_slot_size = 60
        spacing = 20  # 统一的间距
        
        # 优化面板位置和尺寸
        panel_width = 320  # 增加面板宽度以容纳更多内容
        panel_height = HEIGHT - 180  # 适当增加高度
        left_panel_x = (WIDTH // 2 - panel_width) // 2
        right_panel_x = WIDTH // 2 + (WIDTH // 2 - panel_width) // 2
        panel_y = 100
        
        # 添加右上角关闭按钮
        self.close_button_rect = pygame.Rect(WIDTH - 50, 50, 30, 30)
        pygame.draw.rect(screen, (200, 50, 50), self.close_button_rect)  # 红色背景
        pygame.draw.rect(screen, (255, 100, 100), self.close_button_rect, 2)  # 红色边框
        # 绘制关闭符号
        close_font = pygame.font.SysFont("SimHei", 20)
        close_text = close_font.render("X", True, (255, 255, 255))
        close_text_x = WIDTH - 50 + 15 - close_text.get_width() // 2
        close_text_y = 50 + 15 - close_text.get_height() // 2
        screen.blit(close_text, (close_text_x, close_text_y))
        
        # 左侧面板：合成配方选择
        pygame.draw.rect(screen, (50, 50, 50), 
                        (left_panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (80, 80, 80), 
                        (left_panel_x, panel_y, panel_width, panel_height), 2)
        
        # 左侧面板标题
        left_title = font_medium.render("合成配方", True, (200, 200, 200))
        left_title_x = left_panel_x + panel_width // 2 - left_title.get_width() // 2
        left_title_y = panel_y + spacing
        screen.blit(left_title, (left_title_x, left_title_y))
        
        # 绘制配方选择图像按钮 - 网格布局 - 增加网格列数和行数以提高底面积
        icon_size = 50
        grid_cols = 4  # 每行显示4个图标
        grid_rows = 5  # 每页显示5行
        grid_spacing = 10  # 网格间距
        
        # 计算网格起始位置使其居中
        grid_width = grid_cols * (icon_size + grid_spacing) - grid_spacing
        grid_height = grid_rows * (icon_size + grid_spacing) - grid_spacing
        grid_start_x = left_panel_x + (panel_width - grid_width) // 2
        grid_start_y = panel_y + 50
        
        # 遍历所有配方
        for i, recipe in enumerate(self.crafting.recipes):
            # 计算在网格中的位置
            row = i // grid_cols
            col = i % grid_cols
            
            # 跳过当前页显示范围外的配方（如果需要分页功能）
            # if row >= grid_rows:
            #     continue
            
            # 计算按钮位置
            button_x = grid_start_x + col * (icon_size + grid_spacing)
            button_y = grid_start_y + row * (icon_size + grid_spacing)
            
            # 检查是否选中了这个配方
            is_selected = hasattr(self, 'selected_recipe') and self.selected_recipe == i
            
            # 绘制按钮背景
            button_color = (70, 70, 70) if not is_selected else (100, 100, 150)  # 选中的按钮颜色不同
            pygame.draw.rect(screen, button_color, 
                            (button_x, button_y, icon_size, icon_size))
            pygame.draw.rect(screen, (120, 120, 120), 
                            (button_x, button_y, icon_size, icon_size), 2)
            
            # 获取配方的输出物品信息
            output_item = recipe["output"]
            output_id = output_item["item_id"]
            output_info = ITEMS.get(output_id, {"name": "未知物品", "color": (150, 150, 150)})
            
            # 绘制物品图标
            icon_inner_size = icon_size - 8
            icon_x = button_x + 4
            icon_y = button_y + 4
            
            if output_info.get("texture") in self.image_loader.images:
                screen.blit(
                    pygame.transform.scale(self.image_loader.images[output_info["texture"]], (icon_inner_size, icon_inner_size)),
                    (icon_x, icon_y)
                )
            else:
                pygame.draw.rect(screen, output_info["color"], (icon_x, icon_y, icon_inner_size, icon_inner_size))
            
            # 绘制物品数量（如果大于1）
            output_quantity = output_item["quantity"]
            if output_quantity > 1:
                quantity_text = font_small.render(str(output_quantity), True, (255, 255, 255))
                screen.blit(quantity_text, (button_x + icon_size - 20, button_y + icon_size - 20))
            
            # 在图标下方绘制配方名称（如果空间允许）
            if icon_size >= 40:
                recipe_name = font_small.render(recipe["name"], True, (255, 255, 255))
                # 如果名称太长，截断显示
                if recipe_name.get_width() > icon_size:
                    # 尝试截断文本直到适合图标宽度
                    truncated_name = recipe["name"]
                    while len(truncated_name) > 1 and font_small.render(truncated_name + "...", True, (255, 255, 255)).get_width() > icon_size:
                        truncated_name = truncated_name[:-1]
                    recipe_name = font_small.render(truncated_name + "...", True, (255, 255, 255))
                recipe_name_x = button_x + (icon_size - recipe_name.get_width()) // 2
                recipe_name_y = button_y + icon_size + 5
                if recipe_name_y + recipe_name.get_height() < panel_y + panel_height:
                    screen.blit(recipe_name, (recipe_name_x, recipe_name_y))
        
        # 右侧面板：材料需求和合成按钮
        pygame.draw.rect(screen, (60, 60, 60), 
                        (right_panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, (100, 100, 100), 
                        (right_panel_x, panel_y, panel_width, panel_height), 2)
        
        # 右侧面板标题
        right_title = font_medium.render("合成信息", True, (200, 200, 200))
        right_title_x = right_panel_x + panel_width // 2 - right_title.get_width() // 2
        right_title_y = panel_y + spacing
        screen.blit(right_title, (right_title_x, right_title_y))
        
        # 绘制材料需求区域
        materials_title = font_small.render("所需材料：", True, (200, 200, 200))
        materials_x = right_panel_x + spacing
        materials_y = panel_y + 50
        screen.blit(materials_title, (materials_x, materials_y))
        
        # 材料列表区域背景
        materials_box_x = right_panel_x + spacing
        materials_box_y = materials_y + 25
        materials_box_width = panel_width - 2 * spacing
        materials_box_height = 100  # 增加高度以容纳图标
        pygame.draw.rect(screen, (40, 40, 40), 
                        (materials_box_x, materials_box_y, materials_box_width, materials_box_height))
        pygame.draw.rect(screen, (70, 70, 70), 
                        (materials_box_x, materials_box_y, materials_box_width, materials_box_height), 1)
        
        # 检查是否已选择配方
        if hasattr(self, 'selected_recipe') and self.selected_recipe is not None and self.selected_recipe < len(self.crafting.recipes):
            recipe = self.crafting.recipes[self.selected_recipe]
            
            # 显示选中配方的材料需求 - 改进的UI显示
            materials = []
            can_craft = True  # 标记是否可以合成
            
            for i, input_item in enumerate(recipe["inputs"]):
                item_id = input_item["item_id"]
                quantity = input_item["quantity"]
                item_info = ITEMS.get(item_id, {"name": "未知物品", "color": (150, 150, 150)})
                
                # 检查玩家是否拥有足够的材料
                has_enough = self.player.has_item(item_id, quantity)
                if not has_enough:
                    can_craft = False
                
                text_color = (255, 255, 255) if has_enough else (255, 100, 100)  # 不足时显示红色
                
                # 获取玩家实际拥有的数量
                player_has = 0
                try:
                    # 尝试获取更精确的数量
                    for slot in self.player.inventory:
                        if slot and slot["item_id"] == item_id:
                            player_has += slot["quantity"]
                except:
                    # 如果无法获取精确数量，使用基本检查
                    player_has = quantity if has_enough else 0
                
                # 绘制材料图标
                material_icon_size = 30
                material_icon_x = materials_box_x + 10
                material_icon_y = materials_box_y + 10 + i * 22
                
                if item_info.get("texture") in self.image_loader.images:
                    screen.blit(
                        pygame.transform.scale(self.image_loader.images[item_info["texture"]], (material_icon_size, material_icon_size)),
                        (material_icon_x, material_icon_y)
                    )
                else:
                    pygame.draw.rect(screen, item_info["color"], (material_icon_x, material_icon_y, material_icon_size, material_icon_size))
                    pygame.draw.rect(screen, (100, 100, 100), (material_icon_x, material_icon_y, material_icon_size, material_icon_size), 1)
                
                # 绘制材料名称和数量 - 改进的显示格式
                material_text = font_small.render(f"{item_info['name']} ({player_has}/{quantity})", True, text_color)
                screen.blit(material_text, (material_icon_x + material_icon_size + 10, material_icon_y + 5))
            
            # 保存can_craft状态用于合成按钮显示
            self.can_craft = can_craft
                
            # 绘制合成结果预览
            result_title = font_small.render("合成结果：", True, (200, 200, 200))
            result_x = right_panel_x + spacing
            result_y = materials_box_y + materials_box_height + 20
            screen.blit(result_title, (result_x, result_y))
            
            # 结果预览框
            result_slot_x = right_panel_x + panel_width // 2 - item_slot_size // 2
            result_slot_y = result_y + 25
            pygame.draw.rect(screen, (80, 80, 80), 
                            (result_slot_x, result_slot_y, item_slot_size, item_slot_size))
            pygame.draw.rect(screen, (120, 120, 120), 
                            (result_slot_x, result_slot_y, item_slot_size, item_slot_size), 2)
            
            # 显示合成结果物品
            output_item = recipe["output"]
            output_id = output_item["item_id"]
            output_quantity = output_item["quantity"]
            output_info = ITEMS.get(output_id, {"name": "未知物品", "color": (150, 150, 150)})
            
            # 绘制物品图标
            if output_info.get("texture") in self.image_loader.images:
                screen.blit(
                    pygame.transform.scale(self.image_loader.images[output_info["texture"]], (item_slot_size - 10, item_slot_size - 10)),
                    (result_slot_x + 5, result_slot_y + 5)
                )
            else:
                pygame.draw.rect(screen, output_info["color"], (result_slot_x + 5, result_slot_y + 5, item_slot_size - 10, item_slot_size - 10))
            
            # 绘制物品名称 - 确保在图标下方
            result_text = font_small.render(output_info["name"], True, (255, 255, 255))
            result_text_x = result_slot_x + item_slot_size // 2 - result_text.get_width() // 2
            result_text_y = result_slot_y + item_slot_size + 10
            screen.blit(result_text, (result_text_x, result_text_y))
            
            # 绘制物品数量 - 确保在图标的右上角，在名称之后绘制以避免遮挡
            if output_quantity > 1:
                quantity_text = font_small.render(str(output_quantity), True, (255, 255, 255))
                screen.blit(quantity_text, (result_slot_x + item_slot_size - 20, result_slot_y + item_slot_size - 20))
        else:
            # 未选择配方时的提示
            hint_text = font_small.render("请从左侧选择一个配方", True, (180, 180, 180))
            hint_x = right_panel_x + panel_width // 2 - hint_text.get_width() // 2
            hint_y = materials_box_y + 40
            screen.blit(hint_text, (hint_x, hint_y))
        
        # 绘制合成按钮 - 根据材料是否充足显示不同状态
        craft_button_width = panel_width - 2 * spacing
        craft_button_height = 40
        craft_button_x = right_panel_x + spacing
        craft_button_y = panel_y + panel_height - spacing - craft_button_height
        
        # 根据can_craft状态设置按钮颜色和样式
        if hasattr(self, 'can_craft') and self.can_craft:
            # 可合成状态 - 绿色带圆角
            button_color = (0, 150, 0)
            border_color = (0, 200, 0)
            corner_radius = 5  # 圆角半径
        else:
            # 不可合成状态 - 灰色无圆角
            button_color = (100, 100, 100)
            border_color = (150, 150, 150)
            corner_radius = 0
        
        # 绘制按钮
        if corner_radius > 0:
            # 创建圆角矩形
            button_rect = pygame.Rect(craft_button_x, craft_button_y, craft_button_width, craft_button_height)
            # 检查pygame版本是否支持border_radius参数
            try:
                pygame.draw.rect(screen, button_color, button_rect, border_radius=corner_radius)
                pygame.draw.rect(screen, border_color, button_rect, 2, border_radius=corner_radius)
            except TypeError:
                # 如果不支持圆角，回退到普通矩形
                pygame.draw.rect(screen, button_color, button_rect)
                pygame.draw.rect(screen, border_color, button_rect, 2)
        else:
            # 普通矩形
            pygame.draw.rect(screen, button_color, 
                            (craft_button_x, craft_button_y, craft_button_width, craft_button_height))
            pygame.draw.rect(screen, border_color, 
                            (craft_button_x, craft_button_y, craft_button_width, craft_button_height), 2)
        
        # 按钮文本
        craft_text = font_medium.render("确定合成", True, (255, 255, 255))
        craft_text_x = craft_button_x + craft_button_width // 2 - craft_text.get_width() // 2
        craft_text_y = craft_button_y + craft_button_height // 2 - craft_text.get_height() // 2
        screen.blit(craft_text, (craft_text_x, craft_text_y))
        
        # 关闭提示文本 - 更新为包含点击右上角关闭按钮的提示
        close_hint = font_medium.render("按C键、ESC键或点击右上角关闭按钮", True, (255, 255, 255))
        close_hint_x = WIDTH // 2 - close_hint.get_width() // 2
        close_hint_y = HEIGHT - 50
        screen.blit(close_hint, (close_hint_x, close_hint_y))
        
    def draw_death_screen(self, screen):
        """绘制死亡页面"""
        # 绘制半透明黑色背景
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        screen.blit(s, (0, 0))
        
        # 绘制死亡标题
        death_title = font_large.render("你已死亡！", True, (255, 0, 0))
        title_x = WIDTH // 2 - death_title.get_width() // 2
        title_y = HEIGHT // 2 - 100
        screen.blit(death_title, (title_x, title_y))
        
        # 显示当前星星数量
        if not self.is_developer_mode:
            star_info = font_medium.render(f"当前星星数量: {self.player.stars}", True, (255, 215, 0))
            star_info_x = WIDTH // 2 - star_info.get_width() // 2
            star_info_y = title_y + 50
            screen.blit(star_info, (star_info_x, star_info_y))
            
            # 显示复活消耗提示
            cost_info = font_medium.render("复活需要消耗1颗星星", True, (255, 255, 255))
            cost_info_x = WIDTH // 2 - cost_info.get_width() // 2
            cost_info_y = star_info_y + 30
            screen.blit(cost_info, (cost_info_x, cost_info_y))
        
        # 绘制复活选项按钮
        button_width = 300
        button_height = 50
        button_y_spacing = 20
        button_start_y = HEIGHT // 2
        
        # 原地复活按钮
        respawn_button_rect = pygame.Rect(WIDTH//2 - button_width//2, button_start_y, button_width, button_height)
        pygame.draw.rect(screen, (100, 100, 200), respawn_button_rect)
        pygame.draw.rect(screen, (200, 200, 255), respawn_button_rect, 2)
        respawn_text = font_medium.render("原地复活", True, (255, 255, 255))
        text_x = respawn_button_rect.centerx - respawn_text.get_width()//2
        text_y = respawn_button_rect.centery - respawn_text.get_height()//2
        screen.blit(respawn_text, (text_x, text_y))
        
        # 清空背包（坐标复活）按钮
        lose_inventory_button_rect = pygame.Rect(WIDTH//2 - button_width//2, 
                                               button_start_y + button_height + button_y_spacing, 
                                               button_width, button_height)
        pygame.draw.rect(screen, (150, 50, 50), lose_inventory_button_rect)
        pygame.draw.rect(screen, (200, 100, 100), lose_inventory_button_rect, 2)
        lose_inventory_text = font_medium.render("清空背包（坐标复活）", True, (255, 255, 255))
        text_x = lose_inventory_button_rect.centerx - lose_inventory_text.get_width()//2
        text_y = lose_inventory_button_rect.centery - lose_inventory_text.get_height()//2
        screen.blit(lose_inventory_text, (text_x, text_y))
        
        # 位置复活按钮
        respawn_position_button_rect = pygame.Rect(WIDTH//2 - button_width//2, 
                                                 button_start_y + 2*(button_height + button_y_spacing), 
                                                 button_width, button_height)
        pygame.draw.rect(screen, (50, 100, 50), respawn_position_button_rect)
        pygame.draw.rect(screen, (100, 200, 100), respawn_position_button_rect, 2)
        respawn_position_text = font_medium.render("位置复活（返回出生点）", True, (255, 255, 255))
        text_x = respawn_position_button_rect.centerx - respawn_position_text.get_width()//2
        text_y = respawn_position_button_rect.centery - respawn_position_text.get_height()//2
        screen.blit(respawn_position_text, (text_x, text_y))
        
        # 存储按钮矩形以便稍后检测点击
        self.death_screen_buttons = {
            'respawn': respawn_button_rect,
            'lose_inventory': lose_inventory_button_rect,
            'respawn_position': respawn_position_button_rect
        }
        
    def draw_controls_screen(self, screen):
        """绘制操作提示页面，显示所有游戏操作说明"""
        # 绘制半透明背景
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 220))
        screen.blit(s, (0, 0))
        
        # 绘制标题
        title = font_large.render("游戏操作指南", True, (255, 215, 0))  # 金色标题更醒目
        title_x = WIDTH // 2 - title.get_width() // 2
        title_y = 50
        screen.blit(title, (title_x, title_y))
        
        # 绘制分隔线
        pygame.draw.line(screen, (100, 100, 100), (title_x - 50, title_y + 40), 
                         (title_x + title.get_width() + 50, title_y + 40), 2)
        
        # 绘制提示内容，优化布局和组织
        sections = [
            {
                "title": "基础移动",
                "items": [
                    "WASD 或 方向键 - 上下左右移动",
                    "空格 - 跳跃"
                ]
            },
            {
                "title": "物品操作",
                "items": [
                    "1-8 数字键 - 选择快捷栏物品",
                    "E 键 - 打开/关闭背包",
                    "C 键 - 打开/关闭合成界面",
                    "Q 键 - 使用手中物品（吃食物）"
                ]
            },
            {
                "title": "交互操作",
                "items": [
                    "鼠标左键 - 破坏方块/攻击生物",
                    "鼠标右键 - 放置方块/打开箱子"
                ]
            },
            {
                "title": "游戏功能",
                "items": [
                    "Ctrl+S - 保存游戏进度",
                    "Ctrl+L - 加载游戏存档",
                    "F1 - 打开/关闭此操作指南"
                ]
            },
            {
                "title": "游戏机制",
                "items": [
                    "水和岩浆可以自动替换相邻的火把",
                    "岩浆每1秒检查并替换相邻火把为岩浆",
                    "水每1秒检查并替换相邻火把为水",
                    "玩家放置水和岩浆也会立即替换火把",
                    "游戏现在采用空手开局机制，玩家出生时没有任何物品"
                ]
            },
            {
                "title": "生存提示",
                "items": [
                    "注意保持饥饿值，饥饿时体力会下降",
                    "水下活动会消耗氧气值",
                    "远离岩浆，会造成持续伤害",
                    "合理规划背包空间"
                ]
            }
        ]
        
        # 计算内容区域宽度和位置
        max_width = 800
        start_x = (WIDTH - max_width) // 2
        content_y = title_y + 80 - self.help_scroll_offset
        section_spacing = 40
        
        # 先计算总内容高度以确定最大滚动偏移量
        total_height = self.calculate_total_content_height(sections, section_spacing)
        visible_height = HEIGHT - 180  # 可见区域高度
        self.help_max_scroll_offset = max(0, total_height - visible_height)
        
        for section in sections:
            # 绘制章节标题
            section_title = font_medium.render(section["title"], True, (255, 165, 0))  # 橙色标题
            # 只绘制在可见区域内的内容
            if content_y + 35 > 0 and content_y < HEIGHT:
                screen.blit(section_title, (start_x, content_y))
            content_y += 35
            
            # 绘制章节内容
            for item in section["items"]:
                text = font_medium.render(item, True, (255, 255, 255))
                # 只绘制在可见区域内的内容
                if content_y + 28 > 0 and content_y < HEIGHT:
                    screen.blit(text, (start_x + 20, content_y))
                content_y += 28
            
            content_y += section_spacing
        
        # 绘制滚动条
        if self.help_max_scroll_offset > 0:
            self.draw_scrollbar(screen, visible_height, total_height, title_y)
        
        # 绘制底部提示
        footer_text = font_medium.render("按F1键关闭此指南", True, (255, 255, 255))
        footer_x = WIDTH // 2 - footer_text.get_width() // 2
        footer_y = HEIGHT - 80
        screen.blit(footer_text, (footer_x, footer_y))
        
        # 绘制滚动提示
        if self.help_max_scroll_offset > 0:
            scroll_hint = font_small.render("使用鼠标滚轮滚动查看更多内容", True, (200, 200, 200))
            scroll_hint_x = WIDTH // 2 - scroll_hint.get_width() // 2
            scroll_hint_y = HEIGHT - 110
            screen.blit(scroll_hint, (scroll_hint_x, scroll_hint_y))
        
        # 添加版本信息
        version_text = font_small.render("游戏版本 1.1", True, (150, 150, 150))
        screen.blit(version_text, (WIDTH - 100, HEIGHT - 30))
    
    def calculate_total_content_height(self, sections, section_spacing):
        """计算帮助页面内容的总高度"""
        total_height = 0
        for section in sections:
            total_height += 35  # 章节标题高度
            total_height += len(section["items"]) * 28  # 章节内容高度
            total_height += section_spacing  # 章节间距
        return total_height
    
    def draw_scrollbar(self, screen, visible_height, total_height, title_y):
        """绘制滚动条"""
        # 滚动条位置和尺寸
        scrollbar_width = 10
        scrollbar_x = WIDTH - 60
        scrollbar_height = max(20, int(visible_height * visible_height / total_height))
        
        # 计算滚动条位置
        if self.help_max_scroll_offset > 0:
            scrollbar_y = title_y + 80 + (visible_height - scrollbar_height) * self.help_scroll_offset / self.help_max_scroll_offset
        else:
            scrollbar_y = title_y + 80
        
        # 绘制滚动条背景
        pygame.draw.rect(screen, (50, 50, 50), 
                         (scrollbar_x, title_y + 80, scrollbar_width, visible_height))
        # 绘制滚动条滑块
        pygame.draw.rect(screen, (150, 150, 150), 
                         (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height))
        # 绘制滚动条边框
        pygame.draw.rect(screen, (100, 100, 100), 
                         (scrollbar_x, title_y + 80, scrollbar_width, visible_height), 1)

    def draw_breaking_progress(self, screen):
        """绘制破坏进度条"""
        if self.breaking_pos:
            x, y = self.breaking_pos
            screen_x = x * TILE_SIZE - self.camera_x
            screen_y = y * TILE_SIZE - self.camera_y - 10

            # 进度条背景
            pygame.draw.rect(screen, (50, 50, 50), (screen_x, screen_y, TILE_SIZE, 5))
            # 进度条
            pygame.draw.rect(screen, (255, 165, 0), (screen_x, screen_y, TILE_SIZE * self.breaking_progress, 5))

    def draw_start_screen(self, screen):
        """绘制游戏启动画面，根据当前状态显示不同界面"""
        # 清空屏幕
        screen.fill((0, 0, 0))
        
        # 根据当前状态显示不同界面
        if self.show_save_selection:
            # 显示存档选择界面
            self.draw_save_selection(screen)
        elif self.show_map_settings:
            # 显示默认渐变背景（不使用图片背景）
            gradient_surface = pygame.Surface((WIDTH, HEIGHT))
            for y in range(HEIGHT):
                # 从深蓝到浅蓝的垂直渐变
                r = 0
                g = 50 + int(y * 205 / HEIGHT)
                b = 100 + int(y * 155 / HEIGHT)
                pygame.draw.line(gradient_surface, (r, g, b), (0, y), (WIDTH, y))
            screen.blit(gradient_surface, (0, 0))
            
            # 绘制半透明遮罩以确保文字清晰可见
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 80))  # 半透明黑色
            screen.blit(overlay, (0, 0))
            
            # 添加页面标题
            title_font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 48, bold=True)
            title_text = title_font.render("创建新世界", True, (255, 255, 255))
            title_shadow = title_font.render("创建新世界", True, (0, 0, 0))
            screen.blit(title_shadow, (WIDTH//2 - title_text.get_width()//2 + 2, 20 + 2))
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 20))
            
            # 定义需要的字体和变量
            font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 26)  # 原32减小约20%
            font_medium = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 20)  # 原24减小约20%
            width_font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 22)  # 原28减小约20%
            input_height = 50
            
            # 确保save_name属性存在并设置默认值
            if not hasattr(self, 'save_name'):
                # 查找存档目录中的新世界存档数量
                save_folder = "存档"
                new_world_count = 1
                if os.path.exists(save_folder):
                    for file in os.listdir(save_folder):
                        if file.startswith("New World."):
                            try:
                                num = int(file.split(".")[1].split(".")[0])
                                if num >= new_world_count:
                                    new_world_count = num + 1
                            except:
                                pass
                self.save_name = f"New World.{new_world_count}"
            
            # 定义存档名称输入框
            save_name_input_width = 300
            save_name_input_height = 40
            save_name_input_rect = pygame.Rect(WIDTH//2 - save_name_input_width//2, 125, save_name_input_width, save_name_input_height)
            # 根据输入状态设置背景颜色
            if hasattr(self, 'input_active') and self.input_active == 'save_name':
                pygame.draw.rect(screen, (255, 255, 200), save_name_input_rect)  # 浅黄色背景表示激活状态
                pygame.draw.rect(screen, (255, 215, 0), save_name_input_rect, 3)  # 金色边框表示焦点
            else:
                pygame.draw.rect(screen, (200, 200, 200), save_name_input_rect)  # 灰色背景表示非激活状态
                pygame.draw.rect(screen, (100, 100, 100), save_name_input_rect, 2)  # 深灰色边框
            
            # 显示存档名称标签
            save_name_label = font.render("存档名称:", True, (255, 255, 255))
            # 添加标签阴影
            save_name_label_shadow = font.render("存档名称:", True, (0, 0, 0))
            screen.blit(save_name_label_shadow, (WIDTH//2 - 150 + 1, 85 + 1))
            screen.blit(save_name_label, (WIDTH//2 - 150, 85))
            
            # 显示存档名称文本
            if hasattr(self, 'input_active') and self.input_active == 'save_name' and hasattr(self, 'input_text'):
                save_name_text = font_medium.render(self.input_text, True, (0, 0, 0))
            else:
                save_name_text = font_medium.render(self.save_name, True, (0, 0, 0))
            
            save_name_text_x = save_name_input_rect.x + 10
            save_name_text_y = save_name_input_rect.y + (save_name_input_height - save_name_text.get_height()) // 2
            screen.blit(save_name_text, (save_name_text_x, save_name_text_y))
            
            # 存档名称数字加1按钮
            save_name_plus_btn = pygame.Rect(save_name_input_rect.x + save_name_input_rect.width + 10, 125, 40, 40)  # 右侧10像素间距
            # 获取鼠标位置以实现悬停效果
            mouse_pos = pygame.mouse.get_pos()
            if save_name_plus_btn.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (130, 130, 130), save_name_plus_btn)  # 悬停时颜色变亮
                pygame.draw.rect(screen, (180, 180, 180), save_name_plus_btn, 2)  # 边框变亮
            else:
                pygame.draw.rect(screen, (100, 100, 100), save_name_plus_btn)
                pygame.draw.rect(screen, (150, 150, 150), save_name_plus_btn, 2)
            plus_symbol = font_medium.render("+", True, (255, 255, 255))
            screen.blit(plus_symbol, (save_name_plus_btn.x + (save_name_plus_btn.width - plus_symbol.get_width())//2, save_name_plus_btn.y + (save_name_plus_btn.height - plus_symbol.get_height())//2))
            
            # 定义宽度输入框
            width_input_width = 200
            width_input_height = 45
            width_input_rect = pygame.Rect(WIDTH//2 - width_input_width//2, 205, width_input_width, width_input_height)
            # 根据输入状态设置背景颜色
            if hasattr(self, 'input_active') and self.input_active == 'width':
                pygame.draw.rect(screen, (255, 255, 200), width_input_rect)  # 浅黄色背景表示激活状态
                pygame.draw.rect(screen, (255, 215, 0), width_input_rect, 3)  # 金色边框表示焦点
            else:
                pygame.draw.rect(screen, (200, 200, 200), width_input_rect)  # 灰色背景表示非激活状态
                pygame.draw.rect(screen, (100, 100, 100), width_input_rect, 2)  # 深灰色边框
            
            # 显示宽度标签
            width_label = font.render("地图宽度:", True, (255, 255, 255))
            # 添加标签阴影
            width_label_shadow = font.render("地图宽度:", True, (0, 0, 0))
            screen.blit(width_label_shadow, (WIDTH//2 - 150 + 1, 165 + 1))
            screen.blit(width_label, (WIDTH//2 - 150, 165))
            
            # 显示宽度，根据输入状态决定显示内容
            if hasattr(self, 'input_active') and self.input_active == 'width' and hasattr(self, 'input_text'):
                width_text = font_medium.render(self.input_text, True, (0, 0, 0))
            else:
                width_text = font_medium.render(str(self.selected_width), True, (0, 0, 0))
            width_text_x = width_input_rect.x + 10
            width_text_y = width_input_rect.y + (width_input_height - width_text.get_height()) // 2
            screen.blit(width_text, (width_text_x, width_text_y))
            
            # 宽度加减按钮 - 调整位置以避免与输入框重叠并对齐（减小30%大小）
            width_input_right = width_input_rect.x + width_input_rect.width
            gap = 10  # 输入框和按钮之间的间距
            # 计算按钮垂直居中位置，使其与输入框在视觉上对齐
            button_y = width_input_rect.y + (width_input_height - 35) // 2  # 35是新按钮高度（原50减小30%）
            button_width = 42  # 原60减小30%
            button_height = 35  # 原50减小30%
            button_gap = 50  # 按钮之间的间距（原70调整为适应小按钮）
            width_minus_btn = pygame.Rect(width_input_right + gap, button_y, button_width, button_height)
            width_plus_btn = pygame.Rect(width_input_right + gap + button_gap, button_y, button_width, button_height)
            # 添加悬停效果
            if width_minus_btn.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (130, 130, 130), width_minus_btn)
                pygame.draw.rect(screen, (180, 180, 180), width_minus_btn, 2)
            else:
                pygame.draw.rect(screen, (100, 100, 100), width_minus_btn)
                pygame.draw.rect(screen, (150, 150, 150), width_minus_btn, 2)
            
            if width_plus_btn.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (130, 130, 130), width_plus_btn)
                pygame.draw.rect(screen, (180, 180, 180), width_plus_btn, 2)
            else:
                pygame.draw.rect(screen, (100, 100, 100), width_plus_btn)
                pygame.draw.rect(screen, (150, 150, 150), width_plus_btn, 2)
            
            minus_text = width_font.render("-", True, (255, 255, 255))
            plus_text = width_font.render("+", True, (255, 255, 255))
            # 在按钮中心显示加减符号
            screen.blit(minus_text, (width_minus_btn.x + (width_minus_btn.width - minus_text.get_width())//2, width_minus_btn.y + (width_minus_btn.height - minus_text.get_height())//2))
            screen.blit(plus_text, (width_plus_btn.x + (width_plus_btn.width - plus_text.get_width())//2, width_plus_btn.y + (width_plus_btn.height - plus_text.get_height())//2))
            
            # 多个宽度快捷设置按钮 - 优化为两行显示
            quick_widths = [
                (500, "最小"),
                (1000, "常见"),
                (5000, "较高"),
                (10000, "高性能"),
                (50000, "超大"),
                (570000, "极限")
            ]
            self.quick_width_buttons = {}
            btn_width = 110
            btn_height = 45
            rows = 2
            cols = len(quick_widths) // rows + (1 if len(quick_widths) % rows > 0 else 0)
            start_x = WIDTH // 2 - (cols * btn_width + (cols - 1) * 10) // 2
            start_y = 275
            for i, (value, label) in enumerate(quick_widths):
                row = i // cols
                col = i % cols
                btn = pygame.Rect(start_x + col * (btn_width + 10), start_y + row * (btn_height + 10), btn_width, btn_height)
                # 添加悬停效果
                if btn.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (70, 70, 180), btn)
                    pygame.draw.rect(screen, (100, 100, 230), btn, 2)
                else:
                    pygame.draw.rect(screen, (50, 50, 150), btn)
                    pygame.draw.rect(screen, (80, 80, 200), btn, 2)
                btn_text = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 15).render(f"{value}-{label}", True, (255, 255, 255))  # 原18减小约20%
                screen.blit(btn_text, (btn.x + (btn_width - btn_text.get_width())//2, btn.y + (btn_height - btn_text.get_height())//2))
                self.quick_width_buttons[i] = (btn, value)
            
            # 绘制地图高度设置（下降8像素）
            height_label = font.render("地图高度:", True, (255, 255, 255))
            height_label_shadow = font.render("地图高度:", True, (0, 0, 0))
            screen.blit(height_label_shadow, (WIDTH//2 - 150 + 1, 383 + 1))
            screen.blit(height_label, (WIDTH//2 - 150, 383))
            
            height_font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 26)  # 原32减小约20%
            height_value_text = height_font.render(f"{self.selected_height}", True, (255, 255, 255))
            height_value_shadow = height_font.render(f"{self.selected_height}", True, (0, 0, 0))
            screen.blit(height_value_shadow, (WIDTH//2 + 50 + 1, 383 + 1))
            screen.blit(height_value_text, (WIDTH//2 + 50, 383))
            
            # 高度加减按钮 - 动态定位以避免与其他元素重叠并与文本垂直对齐（下降8像素，减小30%大小）
            # 计算按钮垂直位置，使其与文本在视觉上居中对齐
            button_y = 383 + (40 - 35) // 2  # 40是文本高度，35是新按钮高度（原50减小30%）
            button_width = 42  # 原60减小30%
            button_height = 35  # 原50减小30%
            button_gap = 50  # 按钮之间的间距（原70调整为适应小按钮）
            height_minus_btn = pygame.Rect(WIDTH//2 + 150, button_y, button_width, button_height)  # 文本右侧
            height_plus_btn = pygame.Rect(WIDTH//2 + 150 + button_gap, button_y, button_width, button_height)  # 减号按钮右侧
            # 添加悬停效果
            if height_minus_btn.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (130, 130, 130), height_minus_btn)
                pygame.draw.rect(screen, (180, 180, 180), height_minus_btn, 2)
            else:
                pygame.draw.rect(screen, (100, 100, 100), height_minus_btn)
                pygame.draw.rect(screen, (150, 150, 150), height_minus_btn, 2)
            
            if height_plus_btn.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (130, 130, 130), height_plus_btn)
                pygame.draw.rect(screen, (180, 180, 180), height_plus_btn, 2)
            else:
                pygame.draw.rect(screen, (100, 100, 100), height_plus_btn)
                pygame.draw.rect(screen, (150, 150, 150), height_plus_btn, 2)
            
            # 在按钮中央显示加减符号
            screen.blit(minus_text, (height_minus_btn.x + (height_minus_btn.width - minus_text.get_width())//2, height_minus_btn.y + (height_minus_btn.height - minus_text.get_height())//2))
            screen.blit(plus_text, (height_plus_btn.x + (height_plus_btn.width - plus_text.get_width())//2, height_plus_btn.y + (height_plus_btn.height - plus_text.get_height())//2))
            
            # 多个高度快捷设置按钮
            quick_heights = [
                (51, "最小"),
                (150, "小"),
                (300, "常见"),
                (600, "最大")
            ]
            self.quick_height_buttons = {}
            btn_width = 120
            btn_height = 45
            start_x = WIDTH // 2 - (len(quick_heights) * btn_width + (len(quick_heights) - 1) * 10) // 2
            for i, (value, label) in enumerate(quick_heights):
                btn = pygame.Rect(start_x + i * (btn_width + 10), 445, btn_width, btn_height)
                # 添加悬停效果
                if btn.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (70, 70, 180), btn)
                    pygame.draw.rect(screen, (100, 100, 230), btn, 2)
                else:
                    pygame.draw.rect(screen, (50, 50, 150), btn)
                    pygame.draw.rect(screen, (80, 80, 200), btn, 2)
                btn_text = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 18).render(f"{value}-{label}", True, (255, 255, 255))
                screen.blit(btn_text, (btn.x + (btn_width - btn_text.get_width())//2, btn.y + (btn_height - btn_text.get_height())//2))
                self.quick_height_buttons[i] = (btn, value)
            
            # 返回按钮
            back_btn = pygame.Rect(50, 50, 120, 50)
            # 添加悬停效果
            if back_btn.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (180, 60, 60), back_btn)
                pygame.draw.rect(screen, (230, 100, 100), back_btn, 2)
            else:
                pygame.draw.rect(screen, (150, 50, 50), back_btn)
                pygame.draw.rect(screen, (200, 80, 80), back_btn, 2)
            back_text = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 28).render("返回", True, (255, 255, 255))
            screen.blit(back_text, (50 + (120 - back_text.get_width())//2, 50 + (50 - back_text.get_height())//2))
            
            # 开发者模式开关
            dev_mode_label = font.render("开发者模式:", True, (255, 255, 255))
            dev_mode_label_shadow = font.render("开发者模式:", True, (0, 0, 0))
            screen.blit(dev_mode_label_shadow, (WIDTH//2 - 300 + 1, 580 + 1))
            screen.blit(dev_mode_label, (WIDTH//2 - 300, 580))
            
            # 开关按钮
            dev_mode_switch = pygame.Rect(WIDTH//2 - 100, 580, 100, 40)
            # 添加悬停效果
            if dev_mode_switch.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (130, 130, 130), dev_mode_switch)
                pygame.draw.rect(screen, (180, 180, 180), dev_mode_switch, 2)
            else:
                pygame.draw.rect(screen, (100, 100, 100), dev_mode_switch)
                pygame.draw.rect(screen, (150, 150, 150), dev_mode_switch, 2)
            
            # 开关滑块
            switch_slider = pygame.Rect(WIDTH//2 - 95 + (50 if self.is_developer_mode else 0), 585, 40, 30)
            if self.is_developer_mode:
                pygame.draw.rect(screen, (0, 200, 0), switch_slider)
            else:
                pygame.draw.rect(screen, (200, 200, 200), switch_slider)
            
            # 显示当前状态文本
            dev_mode_status = "开启" if self.is_developer_mode else "关闭"
            status_color = (0, 255, 0) if self.is_developer_mode else (255, 0, 0)
            status_text = font_medium.render(dev_mode_status, True, status_color)
            # 调整状态文本位置，向右移动一些以避免与按钮重叠
            screen.blit(status_text, (WIDTH//2 + 20, 585))
            
            # 创建存档开关
            save_switch_label = font.render("创建存档:", True, (255, 255, 255))
            save_switch_label_shadow = font.render("创建存档:", True, (0, 0, 0))
            screen.blit(save_switch_label_shadow, (WIDTH//2 - 300 + 1, 630 + 1))
            screen.blit(save_switch_label, (WIDTH//2 - 300, 630))
            
            # 确保save_enabled属性存在并设置默认值
            if not hasattr(self, 'save_enabled'):
                self.save_enabled = True
            
            # 开关按钮
            save_switch = pygame.Rect(WIDTH//2 - 100, 630, 100, 40)
            # 添加悬停效果
            if save_switch.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (130, 130, 130), save_switch)
                pygame.draw.rect(screen, (180, 180, 180), save_switch, 2)
            else:
                pygame.draw.rect(screen, (100, 100, 100), save_switch)
                pygame.draw.rect(screen, (150, 150, 150), save_switch, 2)
            
            # 开关滑块
            switch_slider = pygame.Rect(WIDTH//2 - 95 + (50 if self.save_enabled else 0), 635, 40, 30)
            if self.save_enabled:
                pygame.draw.rect(screen, (0, 200, 0), switch_slider)
            else:
                pygame.draw.rect(screen, (200, 200, 200), switch_slider)
            
            # 显示当前状态文本
            save_status = "开启" if self.save_enabled else "关闭"
            status_color = (0, 255, 0) if self.save_enabled else (255, 0, 0)
            status_text = font_medium.render(save_status, True, status_color)
            screen.blit(status_text, (WIDTH//2 + 20, 635))
            
            # 确认按钮（开始游戏）
            confirm_btn = pygame.Rect(WIDTH//2 - 120, 500, 240, 70)
            # 添加悬停效果
            if confirm_btn.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (0, 180, 0), confirm_btn)
                pygame.draw.rect(screen, (0, 230, 0), confirm_btn, 3)
                # 添加发光效果
                glow_surface = pygame.Surface((240-6, 70-6), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (100, 255, 100, 80), (0, 0, 240-6, 70-6))
                screen.blit(glow_surface, (WIDTH//2 - 120+3, 500+3))
            else:
                pygame.draw.rect(screen, (0, 150, 0), confirm_btn)
                pygame.draw.rect(screen, (0, 200, 0), confirm_btn, 3)
            confirm_text = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 36).render("开始游戏", True, (255, 255, 255))
            screen.blit(confirm_text, (WIDTH//2 - confirm_text.get_width()//2, 500 + (70 - confirm_text.get_height())//2))

            # 世界类型选择下拉框
            world_type_label = font.render("世界类型:", True, (255, 255, 255))
            world_type_label_shadow = font.render("世界类型:", True, (0, 0, 0))
            screen.blit(world_type_label_shadow, (WIDTH//2 - 300 + 1, 680 + 1))
            screen.blit(world_type_label, (WIDTH//2 - 300, 680))
            
            # 世界类型选项
            world_type_options = ["随机世界", "平原世界"]
            # 确保world_type属性存在并设置默认值
            if not hasattr(self, 'selected_world_type'):
                self.selected_world_type = "随机世界"
            
            # 绘制下拉框背景
            dropdown_rect = pygame.Rect(WIDTH//2 - 150, 680, 200, 40)
            # 添加悬停效果
            if dropdown_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (230, 230, 230), dropdown_rect)
                pygame.draw.rect(screen, (180, 180, 180), dropdown_rect, 2)
            else:
                pygame.draw.rect(screen, (200, 200, 200), dropdown_rect)
                pygame.draw.rect(screen, (150, 150, 150), dropdown_rect, 2)
            
            # 绘制当前选中的选项文本
            world_type_text = font_medium.render(self.selected_world_type, True, (0, 0, 0))
            screen.blit(world_type_text, (dropdown_rect.x + 10, dropdown_rect.y + (40 - world_type_text.get_height())//2))
            
            # 绘制下拉箭头
            arrow_x = dropdown_rect.x + dropdown_rect.width - 30
            arrow_y = dropdown_rect.y + (40 - 10) // 2
            pygame.draw.polygon(screen, (100, 100, 100), [(arrow_x, arrow_y), (arrow_x + 10, arrow_y + 10), (arrow_x + 20, arrow_y)])
            
            # 存储设置界面按钮引用
            self.map_settings_buttons = {
                'save_name_input': save_name_input_rect,
                'save_name_plus': save_name_plus_btn,
                'width_minus': width_minus_btn,
                'width_plus': width_plus_btn,
                'width_input': width_input_rect,
                'height_minus': height_minus_btn,
                'height_plus': height_plus_btn,
                'back': back_btn,
                'confirm': confirm_btn,
                'dev_mode_switch': dev_mode_switch,
                'world_type': dropdown_rect,
                'save_switch': save_switch
            }
        else:
            # 显示默认的开始界面
            # 加载并显示背景图1.jpg
            try:
                # 使用相对路径在当前代码目录查找背景图
                background_image = pygame.image.load("背景图1.jpg")
                # 调整背景图大小以适应整个屏幕
                background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
                screen.blit(background_image, (0, 0))
            except Exception as e:
                # 如果加载图片失败，显示默认渐变背景
                gradient_surface = pygame.Surface((WIDTH, HEIGHT))
                for y in range(HEIGHT):
                    # 从深蓝到浅蓝的垂直渐变
                    r = 0
                    g = 50 + int(y * 205 / HEIGHT)
                    b = 100 + int(y * 155 / HEIGHT)
                    pygame.draw.line(gradient_surface, (r, g, b), (0, y), (WIDTH, y))
                screen.blit(gradient_surface, (0, 0))
                #print(f"加载背景图失败: {e}")
                
            # 绘制半透明遮罩以确保文字清晰可见
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 80))  # 半透明黑色
            screen.blit(overlay, (0, 0))
                
            # 绘制'方块世界'文字 - 增加阴影效果
            font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 72, bold=True)
            # 文字阴影
            shadow_surface = font.render("方块世界", True, (0, 0, 0))
            screen.blit(shadow_surface, (WIDTH//2 - shadow_surface.get_width()//2 + 3, HEIGHT//2 - 150 + 3))
            # 主文字
            text_surface = font.render("方块世界", True, (255, 255, 255))
            screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, HEIGHT//2 - 150))
            
            # 定义中等大小字体
            font_medium = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 28, bold=True)
            
            # 手动导入存档按钮 - 优化UI
            import_button_width = 240
            import_button_height = 60
            import_button_x = WIDTH // 2 - import_button_width // 2
            import_button_y = HEIGHT // 2 + 50
            import_button_rect = pygame.Rect(import_button_x, import_button_y, import_button_width, import_button_height)
            
            # 按钮背景 - 不使用border_radius以确保兼容性
            pygame.draw.rect(screen, (120, 120, 120), import_button_rect)
            pygame.draw.rect(screen, (150, 150, 150), import_button_rect, 3)
            
            # 按钮内发光效果
            glow_surface = pygame.Surface((import_button_width-6, import_button_height-6), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (200, 200, 200, 80), (0, 0, import_button_width-6, import_button_height-6))
            screen.blit(glow_surface, (import_button_x+3, import_button_y+3))
            
            # 导入存档文本 - 居中显示
            import_text = font_medium.render("导入存档", True, (255, 255, 255))
            import_text_x = import_button_x + import_button_width // 2 - import_text.get_width() // 2
            import_text_y = import_button_y + import_button_height // 2 - import_text.get_height() // 2
            screen.blit(import_text, (import_text_x, import_text_y))
            
            # 创建新世界按钮 - 优化UI
            create_button_width = 240
            create_button_height = 60
            create_button_x = WIDTH // 2 - create_button_width // 2
            create_button_y = HEIGHT // 2 + 130
            create_button_rect = pygame.Rect(create_button_x, create_button_y, create_button_width, create_button_height)
            
            # 按钮背景 - 不使用border_radius以确保兼容性
            pygame.draw.rect(screen, (50, 120, 50), create_button_rect)
            pygame.draw.rect(screen, (80, 150, 80), create_button_rect, 3)
            
            # 按钮内发光效果
            glow_surface = pygame.Surface((create_button_width-6, create_button_height-6), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (100, 200, 100, 80), (0, 0, create_button_width-6, create_button_height-6))
            screen.blit(glow_surface, (create_button_x+3, create_button_y+3))
            
            # 创建新世界文本 - 居中显示
            create_text = font_medium.render("创建新世界", True, (255, 255, 255))
            create_text_x = create_button_x + create_button_width // 2 - create_text.get_width() // 2
            create_text_y = create_button_y + create_button_height // 2 - create_text.get_height() // 2
            screen.blit(create_text, (create_text_x, create_text_y))
            
            # 存储按钮引用以便事件处理
            self.start_screen_buttons = {
                'create_new': create_button_rect
            }

    def run(self):
        """游戏主循环"""
        # 声明全局变量
        global WORLD_WIDTH, WORLD_HEIGHT
        
        print("游戏控制:")
        print("WASD 或 方向键 - 移动")
        print("空格 - 跳跃")
        print("1-9 - 选择快捷栏物品")
        print("E - 打开/关闭背包")
        print("C - 打开/关闭合成界面")
        print("Q - 使用手中物品（持弓时射箭，其他物品吃食物）")
        print("鼠标左键 - 破坏方块/攻击")
        print("鼠标右键 - 放置方块/打开箱子")
        print("Ctrl+S - 保存游戏")
        print("Ctrl+L - 加载游戏")

        while self.running:
            dt = clock.tick(60) / 1000.0  # 转换为秒

            # 处理启动画面的事件
            if self.show_start_screen:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # 左键点击
                            mx, my = event.pos
                            
                            # 存档选择界面的事件处理
                            if self.show_save_selection:
                                # 处理存档选择界面的按钮点击
                                if hasattr(self, 'save_selection_buttons'):
                                    for key, value in self.save_selection_buttons.items():
                                        # 检查返回按钮
                                        if key == 'back' and value.collidepoint(mx, my):
                                            self.show_save_selection = False
                                        # 检查创建新世界按钮
                                        elif key == 'create_new' and value.collidepoint(mx, my):
                                            self.show_save_selection = False
                                            self.show_map_settings = True
                                        # 检查存档项
                                        elif key.startswith('save_') and isinstance(value, tuple) and len(value) == 2:
                                            rect, file_name = value
                                            if rect.collidepoint(mx, my):
                                                # 加载选中的存档
                                                try:
                                                    save_path = os.path.join('存档', file_name)
                                                    with open(save_path, 'r', encoding='utf-8') as f:
                                                        save_data = json.load(f)
                                                     
                                                    # 恢复游戏状态
                                                    self.world = World(self.image_loader)
                                                    self.player = Player(0, 0)
                                                    self.player.load_from_save(save_data)
                                                    self.world.load_from_save(save_data)
                                                     
                                                    # 设置世界尺寸
                                                    WORLD_WIDTH = self.world.width
                                                    WORLD_HEIGHT = self.world.height
                                                     
                                                    # 恢复生物和其他状态
                                                    self.creatures = []
                                                    if 'creatures' in save_data:
                                                        for creature_data in save_data['creatures']:
                                                            if creature_data['type'] == 'zombie':
                                                                creature = Zombie(creature_data['x'], creature_data['y'])
                                                                creature.load_from_save(creature_data)
                                                                self.creatures.append(creature)
                                                     
                                                    # 进入游戏
                                                    self.show_start_screen = False
                                                    self.show_save_selection = False
                                                     
                                                    print(f"成功加载存档: {file_name}")
                                                except Exception as e:
                                                    print(f"加载存档失败: {e}")
                            # 主启动画面的事件处理
                            elif not self.show_map_settings:
                                # 在主启动画面
                                if hasattr(self, 'start_screen_buttons'):
                                    if 'create_new' in self.start_screen_buttons and self.start_screen_buttons['create_new'].collidepoint(mx, my):
                                        # 显示创建新世界的地图设置界面
                                        self.show_map_settings = True
                            else:
                                # 在地图设置界面
                                if hasattr(self, 'map_settings_buttons'):
                                    if 'back' in self.map_settings_buttons and self.map_settings_buttons['back'].collidepoint(mx, my):
                                        # 返回主启动画面
                                        self.show_map_settings = False
                                    elif 'confirm' in self.map_settings_buttons and self.map_settings_buttons['confirm'].collidepoint(mx, my):
                                        # 确认设置并开始游戏
                                        # 重新初始化游戏世界，使用新的地图大小
                                        WORLD_WIDTH = self.selected_width
                                        WORLD_HEIGHT = self.selected_height
                                        # 重新创建世界和玩家
                                        # 传递world_type参数
                                        world_type = getattr(self, 'selected_world_type', '随机世界')
                                        self.world = World(self.image_loader, world_type=world_type)
                                        self.player = Player(WORLD_WIDTH * TILE_SIZE // 2, 0)
                                        self.player.immune_time = 30.0
                                        self.player.is_resurrection_immune = True
                                        self.creatures = self.spawn_initial_creatures(30)
                                        self.show_start_screen = False
                                        
                                        # 如果存档开关开启，则保存游戏
                                        if hasattr(self, 'save_enabled') and self.save_enabled:
                                            print("创建存档")
                                            self.save_game()
                                    # 宽度调整按钮
                                    elif 'width_minus' in self.map_settings_buttons and self.map_settings_buttons['width_minus'].collidepoint(mx, my):
                                        # 减小宽度，按100为间隔
                                        if self.selected_width > 500:
                                            self.selected_width = max(500, self.selected_width - 100)
                                    elif 'width_plus' in self.map_settings_buttons and self.map_settings_buttons['width_plus'].collidepoint(mx, my):
                                        # 增加宽度，按100为间隔
                                        if self.selected_width < 570000:
                                            self.selected_width = min(570000, self.selected_width + 100)
                                    # 检查是否点击了存档名称输入框
                                    elif 'save_name_input' in self.map_settings_buttons and self.map_settings_buttons['save_name_input'].collidepoint(mx, my):
                                        self.input_active = 'save_name'
                                        self.input_text = self.save_name
                                    # 检查是否点击了存档名称数字加1按钮
                                    elif 'save_name_plus' in self.map_settings_buttons and self.map_settings_buttons['save_name_plus'].collidepoint(mx, my):
                                        # 解析存档名称，提取数字并加1
                                        try:
                                            # 检查存档名称格式，如"New World.1"
                                            if self.save_name.startswith("New World."):
                                                current_num = int(self.save_name.split(".")[1])
                                                new_num = current_num + 1
                                                self.save_name = f"New World.{new_num}"
                                                # 如果当前正在编辑存档名称，同步更新输入文本
                                                if hasattr(self, 'input_active') and self.input_active == 'save_name':
                                                    self.input_text = self.save_name
                                        except:
                                            # 如果解析失败，使用默认逻辑
                                            new_world_count = 1
                                            save_folder = "存档"
                                            if os.path.exists(save_folder):
                                                for file in os.listdir(save_folder):
                                                    if file.startswith("New World."):
                                                        try:
                                                            num = int(file.split(".")[1].split(".")[0])
                                                            if num >= new_world_count:
                                                                new_world_count = num + 1
                                                        except:
                                                            pass
                                            self.save_name = f"New World.{new_world_count}"
                                            # 同步更新输入文本
                                            if hasattr(self, 'input_active') and self.input_active == 'save_name':
                                                self.input_text = self.save_name
                                    # 检查是否点击了宽度输入框
                                    elif 'width_input' in self.map_settings_buttons and self.map_settings_buttons['width_input'].collidepoint(mx, my):
                                        self.input_active = 'width'
                                        self.input_text = str(self.selected_width)
                                    # 检查是否点击了开发者模式开关
                                    elif 'dev_mode_switch' in self.map_settings_buttons and self.map_settings_buttons['dev_mode_switch'].collidepoint(mx, my):
                                        # 切换开发者模式状态
                                        self.is_developer_mode = not self.is_developer_mode
                                    # 检查是否点击了创建存档开关
                                    elif 'save_switch' in self.map_settings_buttons and self.map_settings_buttons['save_switch'].collidepoint(mx, my):
                                        # 切换创建存档状态
                                        self.save_enabled = not self.save_enabled
                                    # 高度调整按钮
                                    elif 'height_minus' in self.map_settings_buttons and self.map_settings_buttons['height_minus'].collidepoint(mx, my):
                                        # 减小高度
                                        if self.selected_height > 51:
                                            self.selected_height = max(51, self.selected_height - 1)
                                    elif 'height_plus' in self.map_settings_buttons and self.map_settings_buttons['height_plus'].collidepoint(mx, my):
                                        # 增加高度
                                        if self.selected_height < 600:
                                            self.selected_height = min(600, self.selected_height + 1)
                                    # 检查是否点击了世界类型选择框
                                    elif 'world_type' in self.map_settings_buttons and self.map_settings_buttons['world_type'].collidepoint(mx, my):
                                        # 切换世界类型
                                        world_type_options = ["随机世界", "平原世界"]
                                        current_index = world_type_options.index(getattr(self, 'selected_world_type', '随机世界'))
                                        new_index = (current_index + 1) % len(world_type_options)
                                        self.selected_world_type = world_type_options[new_index]
                                # 处理宽度快捷设置按钮
                                if hasattr(self, 'quick_width_buttons'):
                                    for i, (btn, value) in self.quick_width_buttons.items():
                                        if btn.collidepoint(mx, my):
                                            self.selected_width = value
                                            break
                                # 处理高度快捷设置按钮
                                if hasattr(self, 'quick_height_buttons'):
                                    for i, (btn, value) in self.quick_height_buttons.items():
                                        if btn.collidepoint(mx, my):
                                            self.selected_height = value
                                            break

                        # 鼠标滚轮事件（处理存档列表滚动）
                        elif event.button == 4 or event.button == 5:  # 滚轮上/下
                            if self.show_save_selection:
                                # 获取存档列表以确定最大滚动偏移量
                                save_folder = "存档"
                                save_files = []
                                if os.path.exists(save_folder):
                                    # 优先使用子文件夹作为存档
                                    for item in os.listdir(save_folder):
                                        item_path = os.path.join(save_folder, item)
                                        if os.path.isdir(item_path):
                                            save_files.append(item)
                                
                                    # 如果没有子文件夹，回退使用.json文件
                                    if not save_files:
                                        for file in os.listdir(save_folder):
                                            if file.endswith(".json"):
                                                save_files.append(file)
                                
                                visible_items = 5  # 可见的存档数量
                                max_offset = max(0, len(save_files) - visible_items)
                                
                                # 根据滚轮方向调整滚动偏移量
                                if event.button == 4:  # 上滚
                                    self.save_list_scroll_offset = max(0, self.save_list_scroll_offset - 1)
                                elif event.button == 5:  # 下滚
                                    self.save_list_scroll_offset = min(max_offset, self.save_list_scroll_offset + 1)
                    # 键盘控制
                    elif event.type == pygame.KEYDOWN:
                        if hasattr(self, 'input_active'):
                            # 处理存档名称输入
                            if self.input_active == 'save_name':
                                # 处理输入框的按键事件
                                if event.key == pygame.K_ESCAPE:
                                    # 取消输入模式
                                    self.input_active = None
                                    self.input_text = ""
                                elif event.key == pygame.K_BACKSPACE:
                                    # 删除一个字符
                                    if hasattr(self, 'input_text'):
                                        self.input_text = self.input_text[:-1]
                                elif event.key == pygame.K_RETURN:
                                    # 确认输入
                                    self.save_name = self.input_text
                                    self.input_active = None
                                    self.input_text = ""
                                else:
                                    # 处理文本输入，允许大多数字符
                                    if hasattr(self, 'input_text'):
                                        if len(self.input_text) < 50:
                                            self.input_text += event.unicode
                            # 处理宽度输入
                            elif self.input_active == 'width':
                                # 处理输入框的按键事件
                                if event.key == pygame.K_ESCAPE:
                                    # 取消输入模式
                                    self.input_active = None
                                    self.input_text = ""
                                elif event.key == pygame.K_BACKSPACE:
                                    # 删除一个字符
                                    if hasattr(self, 'input_text'):
                                        self.input_text = self.input_text[:-1]
                                elif event.key == pygame.K_RETURN:
                                    # 确认输入
                                    try:
                                        value = int(self.input_text)
                                        # 验证输入的宽度在有效范围内
                                        if 500 <= value <= 570000:
                                            self.selected_width = value
                                        else:
                                            print("错误: 地图宽度必须在500到570000之间")
                                    except ValueError:
                                        print("错误: 请输入有效的数字")
                                    finally:
                                        self.input_active = None
                                        self.input_text = ""
                                else:
                                    # 使用event.unicode获取实际输入的字符
                                    if hasattr(self, 'input_text'):
                                        if (event.unicode.isdigit() or (event.unicode == '-' and not self.input_text)) and len(self.input_text) < 10:
                                            self.input_text += event.unicode
                                    else:
                                        self.input_text = ""
                                        if event.unicode.isdigit():
                                            self.input_text += event.unicode
                        else:
                            if event.key == pygame.K_ESCAPE:
                                if self.show_map_settings:
                                    self.show_map_settings = False
                                else:
                                    self.show_start_screen = False
                            elif not self.show_map_settings and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                                self.show_start_screen = False
                
                # 绘制启动画面
                self.draw_start_screen(screen)
                pygame.display.flip()
                continue

            self.handle_events()
            
            # 如果玩家死亡，不更新游戏状态
            if not self.is_player_dead:
                self.update(dt)

            # 绘制
            self.world.draw(screen, self.camera_x, self.camera_y)
            
            # 绘制下雨效果
            self.draw_rain(screen)
            
            # 绘制生物
            for creature in self.creatures:
                creature.draw(screen, self.camera_x, self.camera_y, self.image_loader.images)

            # 绘制玩家
            self.player.draw(screen, self.camera_x, self.camera_y, self.image_loader.images)
            
            # 绘制箭矢
            # 绘制激光炮红线瞄准效果（狙击枪风格）
            weapon = self.player.get_selected_item()
            if weapon and weapon["item_id"] == LASER_CANNON:
                # 获取鼠标位置，计算瞄准方向
                mx, my = pygame.mouse.get_pos()
                
                # 计算玩家中心位置
                player_center_x = self.player.x + self.player.width // 2
                player_center_y = self.player.y + self.player.height // 2
                
                # 转换玩家中心位置到屏幕坐标
                player_screen_x = player_center_x - self.camera_x
                player_screen_y = player_center_y - self.camera_y
                
                # 计算鼠标相对于玩家的方向向量
                dx_mouse = mx - player_screen_x
                dy_mouse = my - player_screen_y
                
                # 归一化方向向量
                distance_mouse = math.sqrt(dx_mouse * dx_mouse + dy_mouse * dy_mouse)
                if distance_mouse > 0:
                    dx_mouse_normalized = dx_mouse / distance_mouse
                    dy_mouse_normalized = dy_mouse / distance_mouse
                else:
                    dx_mouse_normalized, dy_mouse_normalized = 1, 0
                
                # 计算超出鼠标位置的终点（延伸3倍距离）
                extended_length = distance_mouse * 3
                extended_end_x = player_screen_x + dx_mouse_normalized * extended_length
                extended_end_y = player_screen_y + dy_mouse_normalized * extended_length
                
                # 绘制红色瞄准线（半透明，线宽2），延伸到超出鼠标位置
                pygame.draw.line(screen, (255, 50, 50, 180), 
                                (player_screen_x, player_screen_y), 
                                (extended_end_x, extended_end_y), 
                                2)
            
            for arrow in self.arrows:
                arrow.draw(screen, self.camera_x, self.camera_y, self.image_loader.images)
            
            # 绘制火箭筒子弹特效（朝玩家方向发射的白色线条，类似弓箭）
            if hasattr(self, 'explosions'):
                import random
                for explosion in self.explosions:
                    # 转换为屏幕坐标
                    center_screen_x = explosion['center_x'] - self.camera_x
                    center_screen_y = explosion['center_y'] - self.camera_y
                    
                    # 计算透明度，随时间衰减
                    alpha = int(255 * (explosion['remaining_time'] / explosion['duration']))
                    
                    # 获取玩家位置
                    player_x = self.player.x + self.player.width // 2
                    player_y = self.player.y + self.player.height // 2
                    
                    # 计算爆炸中心到玩家的方向
                    dx = player_x - explosion['center_x']
                    dy = player_y - explosion['center_y']
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance > 0:  # 避免除零错误
                        dx /= distance
                        dy /= distance
                    
                    # 设置线条数量和扩散角度
                    num_lines = random.randint(8, 16)  # 减少线条数量，更清晰
                    max_spread = math.pi / 6  # 最大扩散角度（30度），更集中朝向玩家
                    
                    for i in range(num_lines):
                        # 基础方向是朝玩家
                        # 添加随机偏移，使线条有扩散效果
                        random_angle = random.uniform(-max_spread, max_spread)
                        
                        # 计算旋转后的方向
                        line_dx = dx * math.cos(random_angle) - dy * math.sin(random_angle)
                        line_dy = dx * math.sin(random_angle) + dy * math.cos(random_angle)
                        
                        # 随机发射距离（核心改进）
                        # 距离范围从爆炸半径的0.5倍到1.5倍
                        random_distance = explosion['radius'] * random.uniform(0.5, 1.5)
                        
                        # 计算线条终点
                        end_x = center_screen_x + line_dx * random_distance
                        end_y = center_screen_y + line_dy * random_distance
                        
                        # 绘制白色线条，线宽与弓箭射出的箭相同
                        # 假设弓箭的线宽是1，使用相同粗细
                        pygame.draw.line(screen, (255, 255, 255, alpha),
                                        (center_screen_x, center_screen_y),
                                        (end_x, end_y),
                                        1)  # 线宽1，与弓箭保持一致
            
            # 绘制激光光束效果
            if hasattr(self, 'active_laser') and self.active_laser:
                # 计算激光光束的持续时间（例如50毫秒）
                if pygame.time.get_ticks() - self.active_laser['time'] < 50:
                    # 转换为屏幕坐标
                    start_screen_x = self.active_laser['start_x'] - self.camera_x
                    start_screen_y = self.active_laser['start_y'] - self.camera_y
                    end_screen_x = self.active_laser['end_x'] - self.camera_x
                    end_screen_y = self.active_laser['end_y'] - self.camera_y
                    
                    # 绘制更粗的白色激光光束，增加像素数量
                    # 最外层光晕，半透明
                    pygame.draw.line(screen, (255, 255, 255, 100), 
                                    (start_screen_x, start_screen_y), 
                                    (end_screen_x, end_screen_y), 
                                    8)  # 外层线宽为8
                    # 中间层光线，中等透明度
                    pygame.draw.line(screen, (255, 255, 255, 180), 
                                    (start_screen_x, start_screen_y), 
                                    (end_screen_x, end_screen_y), 
                                    5)  # 中间层线宽为5
                    # 内层光线，较高透明度
                    pygame.draw.line(screen, (255, 255, 255, 220), 
                                    (start_screen_x, start_screen_y), 
                                    (end_screen_x, end_screen_y), 
                                    3)  # 内层线宽为3
                    # 最亮的中心光线
                    pygame.draw.line(screen, (255, 255, 255, 255), 
                                    (start_screen_x, start_screen_y), 
                                    (end_screen_x, end_screen_y), 
                                    2)  # 中心光线线宽为2
                else:
                    # 激光光束时间到期，清除
                    self.active_laser = None
            
            # 绘制闪电闪光效果（在所有内容之上）
            self.draw_thunder_flash(screen)

            # 绘制破坏进度
            self.draw_breaking_progress(screen)
            
            # 绘制伤害文本
            for damage_text in self.damage_texts:
                damage_text.draw(screen, self.camera_x, self.camera_y)
                
            # 绘制物品实体
            for item_entity in self.item_entities:
                item_entity.draw(screen, self.camera_x, self.camera_y, self.image_loader.images)

            # 绘制UI
            if not self.is_player_dead:  # 玩家死亡时不显示普通UI
                # 如果显示高级功能页面，优先绘制
                if self.is_advanced_menu_open:
                    self.draw_advanced_menu(screen)
                # 如果显示操作提示页面，优先绘制
                elif self.show_controls:
                    self.draw_controls_screen(screen)
                elif self.is_creative_inventory_open:  # 如果打开了创造背包，优先绘制
                    self.draw_creative_inventory(screen)
                elif self.new_chest_manager.is_open:
                    self.new_chest_manager.draw(screen)
                else:
                    self.draw_ui(screen)

                    # 绘制背包或箱子
                    self.inventory_close_button = None
                    if self.player.is_inventory_open or self.player.is_chest_open:
                        self.inventory_close_button = self.draw_inventory(screen)

                    # 绘制合成界面
                    if self.player.is_crafting_open:
                        self.draw_crafting(screen)
            else:
                # 绘制死亡页面
                self.draw_death_screen(screen)

            pygame.display.flip()
    
    def draw_button(self, screen, rect, text, is_hovered=False, is_active=False, button_type='primary'):
        """绘制现代化风格的按钮"""
        # 设置按钮颜色主题
        if button_type == 'primary':
            base_color = (50, 120, 180) if not is_hovered else (60, 140, 210)
            highlight_color = (70, 160, 240) if not is_hovered else (80, 180, 255)
            border_color = (100, 180, 255) if not is_hovered else (120, 200, 255)
        elif button_type == 'success':
            base_color = (50, 120, 50) if not is_hovered else (60, 140, 60)
            highlight_color = (70, 160, 70) if not is_hovered else (80, 180, 80)
            border_color = (100, 200, 100) if not is_hovered else (120, 220, 120)
        elif button_type == 'danger':
            base_color = (120, 50, 50) if not is_hovered else (140, 60, 60)
            highlight_color = (160, 70, 70) if not is_hovered else (180, 80, 80)
            border_color = (200, 100, 100) if not is_hovered else (220, 120, 120)
        elif button_type == 'secondary':
            base_color = (80, 80, 80) if not is_hovered else (100, 100, 100)
            highlight_color = (100, 100, 100) if not is_hovered else (120, 120, 120)
            border_color = (140, 140, 140) if not is_hovered else (160, 160, 160)
        else:
            base_color = (60, 60, 60) if not is_hovered else (80, 80, 80)
            highlight_color = (80, 80, 80) if not is_hovered else (100, 100, 100)
            border_color = (120, 120, 120) if not is_hovered else (140, 140, 140)
        
        # 创建按钮表面
        button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        
        # 绘制圆角矩形背景
        pygame.draw.rect(button_surface, base_color, (0, 0, rect.width, rect.height), 0, 8)
        
        # 绘制顶部高亮渐变（立体感）
        highlight_rect = pygame.Rect(0, 0, rect.width, rect.height // 2)
        highlight_surface = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
        for y in range(highlight_rect.height):
            # 顶部透明度高，底部透明度低
            alpha = 100 - (y / highlight_rect.height * 80)
            pygame.draw.line(highlight_surface, (*highlight_color, alpha), 
                            (0, y), (highlight_rect.width, y))
        button_surface.blit(highlight_surface, highlight_rect)
        
        # 绘制边框
        pygame.draw.rect(button_surface, border_color, (0, 0, rect.width, rect.height), 2, 8)
        
        # 如果按钮被按下，添加按下效果
        if is_active:
            shadow_offset = 2
            # 创建阴影效果
            shadow_surface = pygame.Surface((rect.width - shadow_offset*2, rect.height - shadow_offset*2), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surface, (*base_color, 150), (0, 0, shadow_surface.get_width(), shadow_surface.get_height()), 0, 6)
            screen.blit(shadow_surface, (rect.x + shadow_offset, rect.y + shadow_offset))
            # 绘制按钮本身，向下偏移
            screen.blit(button_surface, (rect.x, rect.y))
        else:
            # 添加轻微阴影
            shadow_surface = pygame.Surface((rect.width - 2, rect.height - 2), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surface, (0, 0, 0, 50), (0, 0, shadow_surface.get_width(), shadow_surface.get_height()), 0, 6)
            screen.blit(shadow_surface, (rect.x + 2, rect.y + 2))
            # 正常绘制按钮
            screen.blit(button_surface, (rect.x, rect.y))
        
        # 绘制按钮文本
        text_surface = font_medium.render(text, True, (255, 255, 255))
        text_x = rect.x + (rect.width - text_surface.get_width()) // 2
        text_y = rect.y + (rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))
        
        return rect
        
    def draw_advanced_menu(self, screen):
        """绘制高级功能页面"""
        # 绘制全屏背景
        bg_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        pygame.draw.rect(screen, (50, 50, 50), bg_rect)
        pygame.draw.rect(screen, (100, 100, 100), bg_rect, 2)
        
        # 应用滚动偏移量
        scroll_offset = -self.advanced_scroll_offset
        
        # 确保target_damage设置为玩家当前的damage值
        if hasattr(self, 'player') and hasattr(self.player, 'damage'):
            self.target_damage = self.player.damage
        
        # 确保target_gravity设置为玩家当前的gravity值（如果有）
        if hasattr(self, 'player'):
            self.target_gravity = getattr(self.player, 'gravity', 0.5)
        
        # 绘制标题 - 带发光效果，标题随页面滚动
        glow_radius = 4
        
        # 创建主发光表面
        title_text = "高级功能"
        glow_title = font_large.render(title_text, True, (255, 165, 0))  # 橙色标题
        
        # 计算标题位置（居中）
        glow_x = WIDTH // 2 - glow_title.get_width() // 2
        glow_y = 80 + scroll_offset
        
        # 创建临时表面用于绘制模糊效果
        temp_surface = pygame.Surface((glow_title.get_width() + glow_radius * 4, 
                                       glow_title.get_height() + glow_radius * 4), 
                                      pygame.SRCALPHA)
        
        # 绘制多个模糊层来创建发光效果
        for i in range(glow_radius):
            # 使用smoothscale实现模糊效果，这在所有pygame版本中都兼容
            scaled_size = (glow_title.get_width() + i * 2, glow_title.get_height() + i * 2)
            blurred = pygame.transform.smoothscale(glow_title, scaled_size)
            blurred_x = (temp_surface.get_width() - blurred.get_width()) // 2
            blurred_y = (temp_surface.get_height() - blurred.get_height()) // 2
            temp_surface.blit(blurred, (blurred_x, blurred_y))
        
        # 将带有发光效果的标题绘制到屏幕上
        screen.blit(temp_surface, (glow_x - glow_radius * 2, glow_y - glow_radius * 2))
        
        # 在发光效果上绘制原始标题
        screen.blit(glow_title, (glow_x, glow_y))
        
        # 输入框通用配置
        input_width = 200
        input_height = 40
        section_spacing = 80  # 功能区块间距
        element_spacing = 60  # 元素间距
        
        # 应用滚动偏移量
        scroll_offset = -self.advanced_scroll_offset
        
        # 功能1: 玩家传送
        section1_y = 150 + scroll_offset
        section_title = font_medium.render("功能1: 玩家传送", True, (255, 165, 0))  # 橙色标题
        section_x = WIDTH // 2 - section_title.get_width() // 2
        screen.blit(section_title, (section_x, section1_y))
        
        # X坐标输入框 - 左对齐
        x_label = font_medium.render("目标X坐标:", True, (255, 255, 255))
        x_label_x = WIDTH // 2 - 300
        x_label_y = section1_y + 60
        screen.blit(x_label, (x_label_x, x_label_y))
        
        x_input_rect = pygame.Rect(WIDTH // 2 - 180, x_label_y, input_width, input_height)
        # 根据输入状态设置背景颜色
        if self.input_active == 'x':
            pygame.draw.rect(screen, (255, 255, 200), x_input_rect)  # 浅黄色背景表示激活状态
        else:
            pygame.draw.rect(screen, (200, 200, 200), x_input_rect)  # 灰色背景表示非激活状态
        pygame.draw.rect(screen, (100, 100, 100), x_input_rect, 2)
        
        # 显示X坐标，根据输入状态决定显示内容
        if self.input_active == 'x':
            x_text = font_medium.render(self.input_text, True, (0, 0, 0))
        else:
            x_text = font_medium.render(str(self.target_x), True, (0, 0, 0))
        x_text_x = x_input_rect.x + 10
        x_text_y = x_input_rect.y + (input_height - x_text.get_height()) // 2
        screen.blit(x_text, (x_text_x, x_text_y))
        
        # Y坐标输入框 - 右对齐
        y_label = font_medium.render("目标Y坐标:", True, (255, 255, 255))
        y_label_x = WIDTH // 2 + 100
        y_label_y = section1_y + 60
        screen.blit(y_label, (y_label_x, y_label_y))
        
        y_input_rect = pygame.Rect(WIDTH // 2 + 220, y_label_y, input_width, input_height)
        # 根据输入状态设置背景颜色
        if self.input_active == 'y':
            pygame.draw.rect(screen, (255, 255, 200), y_input_rect)  # 浅黄色背景表示激活状态
        else:
            pygame.draw.rect(screen, (200, 200, 200), y_input_rect)  # 灰色背景表示非激活状态
        pygame.draw.rect(screen, (100, 100, 100), y_input_rect, 2)
        
        # 显示Y坐标，根据输入状态决定显示内容
        if self.input_active == 'y':
            y_text = font_medium.render(self.input_text, True, (0, 0, 0))
        else:
            y_text = font_medium.render(str(self.target_y), True, (0, 0, 0))
        y_text_x = y_input_rect.x + 10
        y_text_y = y_input_rect.y + (input_height - y_text.get_height()) // 2
        screen.blit(y_text, (y_text_x, y_text_y))
        
        # 确认传送按钮 - 居中 - 优化样式
        confirm_btn = pygame.Rect(WIDTH // 2 - 100, section1_y + 120, 200, 50)
        
        # 创建按钮表面用于绘制渐变和效果
        button_surface = pygame.Surface((confirm_btn.width, confirm_btn.height), pygame.SRCALPHA)
        
        # 绘制按钮渐变背景
        for y in range(confirm_btn.height):
            # 从顶部到底部的渐变
            r = 0
            g = 130 + int((y / confirm_btn.height) * 40)
            b = 0
            pygame.draw.line(button_surface, (r, g, b), (0, y), (confirm_btn.width, y))
        
        # 绘制按钮圆角边框
        pygame.draw.rect(button_surface, (0, 220, 0), pygame.Rect(0, 0, confirm_btn.width, confirm_btn.height), 3, 8)  # 圆角半径8
        
        # 添加按钮高光效果（顶部边缘）
        pygame.draw.line(button_surface, (100, 255, 100), (3, 3), (confirm_btn.width-4, 3), 2)
        pygame.draw.line(button_surface, (50, 255, 50), (3, 5), (confirm_btn.width-4, 5), 1)
        
        # 将按钮表面绘制到屏幕上
        screen.blit(button_surface, confirm_btn.topleft)
        
        # 绘制按钮文本，增加轻微的阴影效果
        confirm_text = font_medium.render("确认传送", True, (255, 255, 255))
        confirm_shadow = font_medium.render("确认传送", True, (0, 0, 0, 100))
        confirm_text_x = confirm_btn.x + (confirm_btn.width - confirm_text.get_width()) // 2
        confirm_text_y = confirm_btn.y + (confirm_btn.height - confirm_text.get_height()) // 2
        screen.blit(confirm_shadow, (confirm_text_x + 1, confirm_text_y + 1))
        screen.blit(confirm_text, (confirm_text_x, confirm_text_y))
        
        # 功能2: 玩家属性
        section2_y = section1_y + 200
        player_section_title = font_medium.render("功能2: 玩家属性", True, (255, 165, 0))  # 橙色标题
        player_section_x = WIDTH // 2 - player_section_title.get_width() // 2
        screen.blit(player_section_title, (player_section_x, section2_y))
        
        # 生命值输入框 - 左对齐
        health_label = font_medium.render("生命值:", True, (255, 255, 255))
        health_label_x = WIDTH // 2 - 300
        health_label_y = section2_y + 60
        screen.blit(health_label, (health_label_x, health_label_y))
        
        health_input_rect = pygame.Rect(WIDTH // 2 - 180, health_label_y, input_width, input_height)
        if self.input_active == 'health':
            pygame.draw.rect(screen, (255, 255, 200), health_input_rect)
        else:
            pygame.draw.rect(screen, (200, 200, 200), health_input_rect)
        pygame.draw.rect(screen, (100, 100, 100), health_input_rect, 2)
        
        if self.input_active == 'health':
            health_text = font_medium.render(self.input_text, True, (0, 0, 0))
        else:
            # 初始化玩家属性值
            if not hasattr(self, 'target_health'):
                self.target_health = self.player.health
            health_text = font_medium.render(str(self.target_health), True, (0, 0, 0))
        screen.blit(health_text, (health_input_rect.x + 10, health_input_rect.y + (input_height - health_text.get_height()) // 2))
        
        # 移动速度输入框 - 右对齐
        speed_label = font_medium.render("移动速度:", True, (255, 255, 255))
        speed_label_x = WIDTH // 2 + 100
        speed_label_y = section2_y + 60
        screen.blit(speed_label, (speed_label_x, speed_label_y))
        
        speed_input_rect = pygame.Rect(WIDTH // 2 + 220, speed_label_y, input_width, input_height)
        if self.input_active == 'speed':
            pygame.draw.rect(screen, (255, 255, 200), speed_input_rect)
        else:
            pygame.draw.rect(screen, (200, 200, 200), speed_input_rect)
        pygame.draw.rect(screen, (100, 100, 100), speed_input_rect, 2)
        
        if self.input_active == 'speed':
            speed_text = font_medium.render(self.input_text, True, (0, 0, 0))
        else:
            # 初始化玩家属性值
            if not hasattr(self, 'target_speed'):
                self.target_speed = self.player.speed
            speed_text = font_medium.render(str(self.target_speed), True, (0, 0, 0))
        screen.blit(speed_text, (speed_input_rect.x + 10, speed_input_rect.y + (input_height - speed_text.get_height()) // 2))
        
        # 跳跃力输入框 - 左对齐
        jump_label = font_medium.render("跳跃力:", True, (255, 255, 255))
        jump_label_x = WIDTH // 2 - 300
        jump_label_y = section2_y + 120
        screen.blit(jump_label, (jump_label_x, jump_label_y))
        
        jump_input_rect = pygame.Rect(WIDTH // 2 - 180, jump_label_y, input_width, input_height)
        if self.input_active == 'jump':
            pygame.draw.rect(screen, (255, 255, 200), jump_input_rect)
        else:
            pygame.draw.rect(screen, (200, 200, 200), jump_input_rect)
        pygame.draw.rect(screen, (100, 100, 100), jump_input_rect, 2)
        
        if self.input_active == 'jump':
            jump_text = font_medium.render(self.input_text, True, (0, 0, 0))
        else:
            # 初始化玩家属性值
            if not hasattr(self, 'target_jump'):
                self.target_jump = self.player.jump_strength
            jump_text = font_medium.render(str(self.target_jump), True, (0, 0, 0))
        screen.blit(jump_text, (jump_input_rect.x + 10, jump_input_rect.y + (input_height - jump_text.get_height()) // 2))
        
        # 初始伤害输入框 - 右对齐
        damage_label = font_medium.render("初始伤害:", True, (255, 255, 255))
        damage_label_x = WIDTH // 2 + 100
        damage_label_y = section2_y + 120
        screen.blit(damage_label, (damage_label_x, damage_label_y))
        
        damage_input_rect = pygame.Rect(WIDTH // 2 + 220, damage_label_y, input_width, input_height)
        if self.input_active == 'damage':
            pygame.draw.rect(screen, (255, 255, 200), damage_input_rect)
        else:
            pygame.draw.rect(screen, (200, 200, 200), damage_input_rect)
        pygame.draw.rect(screen, (100, 100, 100), damage_input_rect, 2)
        
        if self.input_active == 'damage':
            damage_text = font_medium.render(self.input_text, True, (0, 0, 0))
        else:
            damage_text = font_medium.render(str(self.target_damage), True, (0, 0, 0))
        screen.blit(damage_text, (damage_input_rect.x + 10, damage_input_rect.y + (input_height - damage_text.get_height()) // 2))
        
        # 重力设置输入框 - 左对齐
        gravity_label = font_medium.render("重力值:", True, (255, 255, 255))
        gravity_label_x = WIDTH // 2 - 300
        gravity_label_y = section2_y + 180
        screen.blit(gravity_label, (gravity_label_x, gravity_label_y))
        
        gravity_input_rect = pygame.Rect(WIDTH // 2 - 180, gravity_label_y, input_width, input_height)
        if self.input_active == 'gravity':
            pygame.draw.rect(screen, (255, 255, 200), gravity_input_rect)
        else:
            pygame.draw.rect(screen, (200, 200, 200), gravity_input_rect)
        pygame.draw.rect(screen, (100, 100, 100), gravity_input_rect, 2)
        
        if self.input_active == 'gravity':
            gravity_text = font_medium.render(self.input_text, True, (0, 0, 0))
        else:
            gravity_text = font_medium.render(str(round(self.target_gravity, 1)), True, (0, 0, 0))
        screen.blit(gravity_text, (gravity_input_rect.x + 10, gravity_input_rect.y + (input_height - gravity_text.get_height()) // 2))
        
        # 重力+0.1按钮 - 优化样式
        gravity_plus_btn = pygame.Rect(WIDTH // 2 + 30, gravity_label_y, 50, input_height)
        
        # 创建按钮表面用于绘制渐变和效果
        plus_surface = pygame.Surface((gravity_plus_btn.width, gravity_plus_btn.height), pygame.SRCALPHA)
        
        # 绘制按钮渐变背景
        for y in range(gravity_plus_btn.height):
            # 从顶部到底部的渐变
            r = 0
            g = 130 + int((y / gravity_plus_btn.height) * 40)
            b = 0
            pygame.draw.line(plus_surface, (r, g, b), (0, y), (gravity_plus_btn.width, y))
        
        # 绘制按钮圆角边框
        pygame.draw.rect(plus_surface, (0, 220, 0), pygame.Rect(0, 0, gravity_plus_btn.width, gravity_plus_btn.height), 2, 6)  # 圆角半径6
        
        # 添加按钮高光效果
        pygame.draw.line(plus_surface, (100, 255, 100), (2, 2), (gravity_plus_btn.width-3, 2), 1)
        
        # 将按钮表面绘制到屏幕上
        screen.blit(plus_surface, gravity_plus_btn.topleft)
        
        # 绘制按钮文本
        gravity_plus_text = font_medium.render("+0.1", True, (255, 255, 255))
        gravity_plus_text_x = gravity_plus_btn.x + (gravity_plus_btn.width - gravity_plus_text.get_width()) // 2
        gravity_plus_text_y = gravity_plus_btn.y + (gravity_plus_btn.height - gravity_plus_text.get_height()) // 2
        screen.blit(gravity_plus_text, (gravity_plus_text_x, gravity_plus_text_y))
        
        # 重力-0.1按钮 - 优化样式
        gravity_minus_btn = pygame.Rect(WIDTH // 2 + 90, gravity_label_y, 50, input_height)
        
        # 创建按钮表面用于绘制渐变和效果
        minus_surface = pygame.Surface((gravity_minus_btn.width, gravity_minus_btn.height), pygame.SRCALPHA)
        
        # 绘制按钮渐变背景
        for y in range(gravity_minus_btn.height):
            # 从顶部到底部的渐变
            r = 130 + int((y / gravity_minus_btn.height) * 40)
            g = 0
            b = 0
            pygame.draw.line(minus_surface, (r, g, b), (0, y), (gravity_minus_btn.width, y))
        
        # 绘制按钮圆角边框
        pygame.draw.rect(minus_surface, (220, 0, 0), pygame.Rect(0, 0, gravity_minus_btn.width, gravity_minus_btn.height), 2, 6)  # 圆角半径6
        
        # 添加按钮高光效果
        pygame.draw.line(minus_surface, (255, 100, 100), (2, 2), (gravity_minus_btn.width-3, 2), 1)
        
        # 将按钮表面绘制到屏幕上
        screen.blit(minus_surface, gravity_minus_btn.topleft)
        
        # 绘制按钮文本
        gravity_minus_text = font_medium.render("-0.1", True, (255, 255, 255))
        gravity_minus_text_x = gravity_minus_btn.x + (gravity_minus_btn.width - gravity_minus_text.get_width()) // 2
        gravity_minus_text_y = gravity_minus_btn.y + (gravity_minus_btn.height - gravity_minus_text.get_height()) // 2
        screen.blit(gravity_minus_text, (gravity_minus_text_x, gravity_minus_text_y))
        
        # 增加与功能3之间的间距
        section2_y_extended = section2_y + 240
        
        # 防御力输入框 - 左对齐
        defense_label = font_medium.render("防御:", True, (255, 255, 255))
        defense_label_x = WIDTH // 2 - 300
        defense_label_y = section2_y_extended
        screen.blit(defense_label, (defense_label_x, defense_label_y))
        
        defense_input_rect = pygame.Rect(WIDTH // 2 - 180, defense_label_y, input_width, input_height)
        if self.input_active == 'defense':
            pygame.draw.rect(screen, (255, 255, 200), defense_input_rect)
        else:
            pygame.draw.rect(screen, (200, 200, 200), defense_input_rect)
        pygame.draw.rect(screen, (100, 100, 100), defense_input_rect, 2)
        
        if self.input_active == 'defense':
            defense_text = font_medium.render(self.input_text, True, (0, 0, 0))
        else:
            defense_text = font_medium.render(str(self.target_defense), True, (0, 0, 0))
        screen.blit(defense_text, (defense_input_rect.x + 10, defense_input_rect.y + (input_height - defense_text.get_height()) // 2))
        
        # 免伤百分比输入框 - 右对齐
        damage_reduction_label = font_medium.render("免伤:+%", True, (255, 255, 255))
        damage_reduction_label_x = WIDTH // 2 + 100
        damage_reduction_label_y = section2_y_extended
        screen.blit(damage_reduction_label, (damage_reduction_label_x, damage_reduction_label_y))
        
        damage_reduction_input_rect = pygame.Rect(WIDTH // 2 + 220, damage_reduction_label_y, input_width, input_height)
        if self.input_active == 'damage_reduction':
            pygame.draw.rect(screen, (255, 255, 200), damage_reduction_input_rect)
        else:
            pygame.draw.rect(screen, (200, 200, 200), damage_reduction_input_rect)
        pygame.draw.rect(screen, (100, 100, 100), damage_reduction_input_rect, 2)
        
        if self.input_active == 'damage_reduction':
            damage_reduction_text = font_medium.render(self.input_text, True, (0, 0, 0))
        else:
            damage_reduction_text = font_medium.render(str(self.target_damage_reduction), True, (0, 0, 0))
        screen.blit(damage_reduction_text, (damage_reduction_input_rect.x + 10, damage_reduction_input_rect.y + (input_height - damage_reduction_text.get_height()) // 2))
        
        # 伤害加成输入框 - 左对齐
        damage_bonus_label = font_medium.render("伤害:+%", True, (255, 255, 255))
        damage_bonus_label_x = WIDTH // 2 - 300
        damage_bonus_label_y = section2_y_extended + 60
        screen.blit(damage_bonus_label, (damage_bonus_label_x, damage_bonus_label_y))
        
        damage_bonus_input_rect = pygame.Rect(WIDTH // 2 - 180, damage_bonus_label_y, input_width, input_height)
        if self.input_active == 'damage_bonus':
            pygame.draw.rect(screen, (255, 255, 200), damage_bonus_input_rect)
        else:
            pygame.draw.rect(screen, (200, 200, 200), damage_bonus_input_rect)
        pygame.draw.rect(screen, (100, 100, 100), damage_bonus_input_rect, 2)
        
        if self.input_active == 'damage_bonus':
            damage_bonus_text = font_medium.render(self.input_text, True, (0, 0, 0))
        else:
            damage_bonus_text = font_medium.render(str(self.target_damage_bonus), True, (0, 0, 0))
        screen.blit(damage_bonus_text, (damage_bonus_input_rect.x + 10, damage_bonus_input_rect.y + (input_height - damage_bonus_text.get_height()) // 2))
        
        # 摔伤减免输入框 - 右对齐
        fall_damage_reduction_label = font_medium.render("摔伤:-%", True, (255, 255, 255))
        fall_damage_reduction_label_x = WIDTH // 2 + 100
        fall_damage_reduction_label_y = section2_y_extended + 60
        screen.blit(fall_damage_reduction_label, (fall_damage_reduction_label_x, fall_damage_reduction_label_y))
        
        fall_damage_reduction_input_rect = pygame.Rect(WIDTH // 2 + 220, fall_damage_reduction_label_y, input_width, input_height)
        if self.input_active == 'fall_damage_reduction':
            pygame.draw.rect(screen, (255, 255, 200), fall_damage_reduction_input_rect)
        else:
            pygame.draw.rect(screen, (200, 200, 200), fall_damage_reduction_input_rect)
        pygame.draw.rect(screen, (100, 100, 100), fall_damage_reduction_input_rect, 2)
        
        if self.input_active == 'fall_damage_reduction':
            fall_damage_reduction_text = font_medium.render(self.input_text, True, (0, 0, 0))
        else:
            fall_damage_reduction_text = font_medium.render(str(self.target_fall_damage_reduction), True, (0, 0, 0))
        screen.blit(fall_damage_reduction_text, (fall_damage_reduction_input_rect.x + 10, fall_damage_reduction_input_rect.y + (input_height - fall_damage_reduction_text.get_height()) // 2))
        
        # 移速加成输入框 - 居中
        speed_bonus_label = font_medium.render("移速:+%", True, (255, 255, 255))
        speed_bonus_label_x = WIDTH // 2 - 200
        speed_bonus_label_y = section2_y_extended + 120
        screen.blit(speed_bonus_label, (speed_bonus_label_x, speed_bonus_label_y))
        
        speed_bonus_input_rect = pygame.Rect(WIDTH // 2 - 80, speed_bonus_label_y, input_width, input_height)
        if self.input_active == 'speed_bonus':
            pygame.draw.rect(screen, (255, 255, 200), speed_bonus_input_rect)
        else:
            pygame.draw.rect(screen, (200, 200, 200), speed_bonus_input_rect)
        pygame.draw.rect(screen, (100, 100, 100), speed_bonus_input_rect, 2)
        
        if self.input_active == 'speed_bonus':
            speed_bonus_text = font_medium.render(self.input_text, True, (0, 0, 0))
        else:
            speed_bonus_text = font_medium.render(str(self.target_speed_bonus), True, (0, 0, 0))
        screen.blit(speed_bonus_text, (speed_bonus_input_rect.x + 10, speed_bonus_input_rect.y + (input_height - speed_bonus_text.get_height()) // 2))
        
        # 更新advanced_menu_buttons字典，添加新输入框区域
        self.advanced_menu_buttons['defense_input'] = defense_input_rect
        self.advanced_menu_buttons['damage_reduction_input'] = damage_reduction_input_rect
        self.advanced_menu_buttons['damage_bonus_input'] = damage_bonus_input_rect
        self.advanced_menu_buttons['fall_damage_reduction_input'] = fall_damage_reduction_input_rect
        self.advanced_menu_buttons['speed_bonus_input'] = speed_bonus_input_rect
        
        # 确认修改按钮 - 居中 - 优化样式
        confirm_player_btn = pygame.Rect(WIDTH // 2 - 100, section2_y + 425, 200, 50)  
        
        # 创建按钮表面用于绘制渐变和效果
        player_btn_surface = pygame.Surface((confirm_player_btn.width, confirm_player_btn.height), pygame.SRCALPHA)
        
        # 绘制按钮渐变背景
        for y in range(confirm_player_btn.height):
            # 从顶部到底部的渐变
            r = 0
            g = 130 + int((y / confirm_player_btn.height) * 40)
            b = 0
            pygame.draw.line(player_btn_surface, (r, g, b), (0, y), (confirm_player_btn.width, y))
        
        # 绘制按钮圆角边框
        pygame.draw.rect(player_btn_surface, (0, 220, 0), pygame.Rect(0, 0, confirm_player_btn.width, confirm_player_btn.height), 3, 8)  # 圆角半径8
        
        # 添加按钮高光效果（顶部边缘）
        pygame.draw.line(player_btn_surface, (100, 255, 100), (3, 3), (confirm_player_btn.width-4, 3), 2)
        pygame.draw.line(player_btn_surface, (50, 255, 50), (3, 5), (confirm_player_btn.width-4, 5), 1)
        
        # 将按钮表面绘制到屏幕上
        screen.blit(player_btn_surface, confirm_player_btn.topleft)
        
        # 绘制按钮文本，增加轻微的阴影效果
        confirm_player_text = font_medium.render("确认修改", True, (255, 255, 255))
        confirm_player_shadow = font_medium.render("确认修改", True, (0, 0, 0, 100))
        confirm_player_text_x = confirm_player_btn.x + (confirm_player_btn.width - confirm_player_text.get_width()) // 2
        confirm_player_text_y = confirm_player_btn.y + (confirm_player_btn.height - confirm_player_text.get_height()) // 2
        screen.blit(confirm_player_text, (confirm_player_text_x, confirm_player_text_y))
        
        # 功能3: 游戏选项 - 向下调整位置，增加距离避免与功能2的确认按钮重叠
        section3_y = section2_y + 540  # 向下移动100像素
        advanced_option_title = font_medium.render("功能3: 游戏选项", True, (255, 165, 0))  # 橙色标题
        advanced_option_x = WIDTH // 2 - advanced_option_title.get_width() // 2
        screen.blit(advanced_option_title, (advanced_option_x, section3_y))
        
        # 秒挖掘开关 - 居中
        instant_mining_label = font_medium.render("秒挖掘（挖掘无时间限制）", True, (255, 255, 255))
        instant_mining_label_x = WIDTH // 2 - 250
        instant_mining_label_y = section3_y + 60
        screen.blit(instant_mining_label, (instant_mining_label_x, instant_mining_label_y))
        
        # 秒挖掘复选框
        instant_mining_checkbox = pygame.Rect(WIDTH // 2 + 150, section3_y + 60, 30, 30)
        pygame.draw.rect(screen, (200, 200, 200), instant_mining_checkbox)
        pygame.draw.rect(screen, (100, 100, 100), instant_mining_checkbox, 2)
        # 如果秒挖掘功能开启，绘制勾选标记
        if self.instant_mining:
            pygame.draw.line(screen, (0, 150, 0), (instant_mining_checkbox.x + 5, instant_mining_checkbox.y + 15), 
                             (instant_mining_checkbox.x + 13, instant_mining_checkbox.y + 23), 3)
            pygame.draw.line(screen, (0, 150, 0), (instant_mining_checkbox.x + 13, instant_mining_checkbox.y + 23), 
                             (instant_mining_checkbox.x + 25, instant_mining_checkbox.y + 5), 3)
        
        # 最高权限开关 - 居中
        god_mode_label = font_medium.render("最高权限（可挖掘基岩）", True, (255, 255, 255))
        god_mode_label_x = WIDTH // 2 - 250
        god_mode_label_y = section3_y + 110
        screen.blit(god_mode_label, (god_mode_label_x, god_mode_label_y))
        
        # 最高权限复选框
        god_mode_checkbox = pygame.Rect(WIDTH // 2 + 150, section3_y + 110, 30, 30)
        pygame.draw.rect(screen, (200, 200, 200), god_mode_checkbox)
        pygame.draw.rect(screen, (100, 100, 100), god_mode_checkbox, 2)
        # 如果最高权限功能开启，绘制勾选标记
        if self.god_mode:
            pygame.draw.line(screen, (0, 150, 0), (god_mode_checkbox.x + 5, god_mode_checkbox.y + 15), 
                             (god_mode_checkbox.x + 13, god_mode_checkbox.y + 23), 3)
            pygame.draw.line(screen, (0, 150, 0), (god_mode_checkbox.x + 13, god_mode_checkbox.y + 23), 
                             (god_mode_checkbox.x + 25, god_mode_checkbox.y + 5), 3)
        
        # 3*3放置复选框 - 居中
        area_place_label = font_medium.render("3*3放置（快捷栏物品只减少1个）", True, (255, 255, 255))
        area_place_label_x = WIDTH // 2 - 250
        area_place_label_y = section3_y + 160
        screen.blit(area_place_label, (area_place_label_x, area_place_label_y))
        
        # 3*3放置复选框
        area_place_checkbox = pygame.Rect(WIDTH // 2 + 150, section3_y + 160, 30, 30)
        pygame.draw.rect(screen, (200, 200, 200), area_place_checkbox)
        pygame.draw.rect(screen, (100, 100, 100), area_place_checkbox, 2)
        # 如果3*3放置功能开启，绘制勾选标记
        if self.area_place_enabled:
            pygame.draw.line(screen, (0, 150, 0), (area_place_checkbox.x + 5, area_place_checkbox.y + 15), 
                             (area_place_checkbox.x + 13, area_place_checkbox.y + 23), 3)
            pygame.draw.line(screen, (0, 150, 0), (area_place_checkbox.x + 13, area_place_checkbox.y + 23), 
                             (area_place_checkbox.x + 25, area_place_checkbox.y + 5), 3)
        
        # 3*3范围挖掘复选框 - 居中
        area_mine_label = font_medium.render("3*3范围挖掘", True, (255, 255, 255))
        area_mine_label_x = WIDTH // 2 - 250
        area_mine_label_y = section3_y + 210
        screen.blit(area_mine_label, (area_mine_label_x, area_mine_label_y))
        
        # 3*3范围挖掘复选框
        area_mine_checkbox = pygame.Rect(WIDTH // 2 + 150, section3_y + 210, 30, 30)
        pygame.draw.rect(screen, (200, 200, 200), area_mine_checkbox)
        pygame.draw.rect(screen, (100, 100, 100), area_mine_checkbox, 2)
        # 如果3*3范围挖掘功能开启，绘制勾选标记
        if self.area_mine_enabled:
            pygame.draw.line(screen, (0, 150, 0), (area_mine_checkbox.x + 5, area_mine_checkbox.y + 15), 
                             (area_mine_checkbox.x + 13, area_mine_checkbox.y + 23), 3)
            pygame.draw.line(screen, (0, 150, 0), (area_mine_checkbox.x + 13, area_mine_checkbox.y + 23), 
                             (area_mine_checkbox.x + 25, area_mine_checkbox.y + 5), 3)
        
        # 全屏点击任意位置挖掘放置复选框 - 居中
        fullscreen_click_label = font_medium.render("全屏点击任意位置挖掘放置", True, (255, 255, 255))
        fullscreen_click_label_x = WIDTH // 2 - 250
        fullscreen_click_label_y = section3_y + 260
        screen.blit(fullscreen_click_label, (fullscreen_click_label_x, fullscreen_click_label_y))
        
        # 全屏点击任意位置挖掘放置复选框
        fullscreen_click_checkbox = pygame.Rect(WIDTH // 2 + 150, section3_y + 260, 30, 30)
        pygame.draw.rect(screen, (200, 200, 200), fullscreen_click_checkbox)
        pygame.draw.rect(screen, (100, 100, 100), fullscreen_click_checkbox, 2)
        # 如果全屏点击功能开启，绘制勾选标记
        if self.fullscreen_click_enabled:
            pygame.draw.line(screen, (0, 150, 0), (fullscreen_click_checkbox.x + 5, fullscreen_click_checkbox.y + 15), 
                             (fullscreen_click_checkbox.x + 13, fullscreen_click_checkbox.y + 23), 3)
            pygame.draw.line(screen, (0, 150, 0), (fullscreen_click_checkbox.x + 13, fullscreen_click_checkbox.y + 23), 
                             (fullscreen_click_checkbox.x + 25, fullscreen_click_checkbox.y + 5), 3)
        
        # 飞行模式开关 - 居中
        fly_mode_label = font_medium.render("开启飞行模式(按w上升,按s下降)", True, (255, 255, 255))
        fly_mode_label_x = WIDTH // 2 - 250
        fly_mode_label_y = section3_y + 320
        screen.blit(fly_mode_label, (fly_mode_label_x, fly_mode_label_y))
        
        # 飞行模式复选框
        fly_mode_checkbox = pygame.Rect(WIDTH // 2 + 150, section3_y + 320, 30, 30)
        pygame.draw.rect(screen, (200, 200, 200), fly_mode_checkbox)
        pygame.draw.rect(screen, (100, 100, 100), fly_mode_checkbox, 2)
        # 如果飞行模式开启，绘制勾选标记
        if hasattr(self.player, 'fly_mode') and self.player.fly_mode:
            pygame.draw.line(screen, (0, 150, 0), (fly_mode_checkbox.x + 5, fly_mode_checkbox.y + 15), 
                             (fly_mode_checkbox.x + 13, fly_mode_checkbox.y + 23), 3)
            pygame.draw.line(screen, (0, 150, 0), (fly_mode_checkbox.x + 13, fly_mode_checkbox.y + 23), 
                             (fly_mode_checkbox.x + 25, fly_mode_checkbox.y + 5), 3)
        
        # 绘制关闭提示 - 底部居中，不随页面滚动
        close_hint = font_medium.render("按F4键关闭此页面", True, (200, 200, 200))
        close_hint_x = WIDTH // 2 - close_hint.get_width() // 2
        close_hint_y = HEIGHT - 80
        screen.blit(close_hint, (close_hint_x, close_hint_y))
        
        # 功能4: 世界设置 - 向下调整位置
        section4_y = section3_y + 400  # 保持与功能3的相对位置，由于功能3已下移，功能4也会相应下移
        world_setting_title = font_medium.render("功能4: 世界设置", True, (255, 165, 0))  # 橙色标题
        world_setting_x = WIDTH // 2 - world_setting_title.get_width() // 2
        screen.blit(world_setting_title, (world_setting_x, section4_y))
        
        # 世界时间设置
        time_label = font_medium.render("世界时间 (00:00-23:59):", True, (255, 255, 255))
        time_label_x = WIDTH // 2 - 300
        time_label_y = section4_y + 60
        screen.blit(time_label, (time_label_x, time_label_y))
        
        # 获取当前世界时间
        hours = int(self.world.time_of_day // 100)
        minutes = int(self.world.time_of_day % 100)
        time_str = f"{hours:02d}:{minutes:02d}"
        
        time_input_rect = pygame.Rect(WIDTH // 2 - 100, time_label_y, 120, input_height)
        if self.input_active == 'time':
            pygame.draw.rect(screen, (255, 255, 200), time_input_rect)
        else:
            pygame.draw.rect(screen, (200, 200, 200), time_input_rect)
        pygame.draw.rect(screen, (100, 100, 100), time_input_rect, 2)
        
        if self.input_active == 'time':
            time_text = font_medium.render(self.input_text, True, (0, 0, 0))
        else:
            time_text = font_medium.render(time_str, True, (0, 0, 0))
        screen.blit(time_text, (time_input_rect.x + 10, time_input_rect.y + (input_height - time_text.get_height()) // 2))
        
        # 时间+01:00按钮
        time_plus_btn = pygame.Rect(WIDTH // 2 + 40, time_label_y, 80, input_height)
        pygame.draw.rect(screen, (0, 150, 0), time_plus_btn)
        pygame.draw.rect(screen, (0, 200, 0), time_plus_btn, 2)
        time_plus_text = font_medium.render("+01:00", True, (255, 255, 255))
        time_plus_text_x = time_plus_btn.x + (time_plus_btn.width - time_plus_text.get_width()) // 2
        time_plus_text_y = time_plus_btn.y + (time_plus_btn.height - time_plus_text.get_height()) // 2
        screen.blit(time_plus_text, (time_plus_text_x, time_plus_text_y))
        
        # 时间-01:00按钮
        time_minus_btn = pygame.Rect(WIDTH // 2 + 130, time_label_y, 80, input_height)
        pygame.draw.rect(screen, (150, 0, 0), time_minus_btn)
        pygame.draw.rect(screen, (200, 0, 0), time_minus_btn, 2)
        time_minus_text = font_medium.render("-01:00", True, (255, 255, 255))
        time_minus_text_x = time_minus_btn.x + (time_minus_btn.width - time_minus_text.get_width()) // 2
        time_minus_text_y = time_minus_btn.y + (time_minus_btn.height - time_minus_text.get_height()) // 2
        screen.blit(time_minus_text, (time_minus_text_x, time_minus_text_y))
        

        
        # 生成生物数量设置
        creature_label = font_medium.render("生成生物数量:", True, (255, 255, 255))
        creature_label_x = WIDTH // 2 - 300
        creature_label_y = section4_y + 120
        screen.blit(creature_label, (creature_label_x, creature_label_y))
        
        creature_input_rect = pygame.Rect(WIDTH // 2 - 100, creature_label_y, 120, input_height)
        if self.input_active == 'creature':
            pygame.draw.rect(screen, (255, 255, 200), creature_input_rect)
        else:
            pygame.draw.rect(screen, (200, 200, 200), creature_input_rect)
        pygame.draw.rect(screen, (100, 100, 100), creature_input_rect, 2)
        
        if self.input_active == 'creature':
            creature_text = font_medium.render(self.input_text, True, (0, 0, 0))
        else:
            creature_text = font_medium.render("10", True, (0, 0, 0))  # 默认值10
        screen.blit(creature_text, (creature_input_rect.x + 10, creature_input_rect.y + (input_height - creature_text.get_height()) // 2))
        
        # 生成生物按钮
        spawn_creature_btn = pygame.Rect(WIDTH // 2 + 40, creature_label_y, 120, input_height)
        pygame.draw.rect(screen, (0, 150, 0), spawn_creature_btn)
        pygame.draw.rect(screen, (0, 200, 0), spawn_creature_btn, 2)
        spawn_creature_text = font_medium.render("生成生物", True, (255, 255, 255))
        spawn_creature_text_x = spawn_creature_btn.x + (spawn_creature_btn.width - spawn_creature_text.get_width()) // 2
        spawn_creature_text_y = spawn_creature_btn.y + (spawn_creature_btn.height - spawn_creature_text.get_height()) // 2
        screen.blit(spawn_creature_text, (spawn_creature_text_x, spawn_creature_text_y))
        
        # 存储按钮引用以便事件处理 - 考虑滚动偏移
        scroll_offset = -self.advanced_scroll_offset
        self.advanced_menu_buttons = {
            'x_input': pygame.Rect(x_input_rect.x, x_input_rect.y + scroll_offset, x_input_rect.width, x_input_rect.height),
            'y_input': pygame.Rect(y_input_rect.x, y_input_rect.y + scroll_offset, y_input_rect.width, y_input_rect.height),
            'confirm': pygame.Rect(confirm_btn.x, confirm_btn.y + scroll_offset, confirm_btn.width, confirm_btn.height),
            'health_input': pygame.Rect(health_input_rect.x, health_input_rect.y + scroll_offset, health_input_rect.width, health_input_rect.height),
            'speed_input': pygame.Rect(speed_input_rect.x, speed_input_rect.y + scroll_offset, speed_input_rect.width, speed_input_rect.height),
            'jump_input': pygame.Rect(jump_input_rect.x, jump_input_rect.y + scroll_offset, jump_input_rect.width, jump_input_rect.height),
            'damage_input': pygame.Rect(damage_input_rect.x, damage_input_rect.y + scroll_offset, damage_input_rect.width, damage_input_rect.height),
            'gravity_input': pygame.Rect(gravity_input_rect.x, gravity_input_rect.y + scroll_offset, gravity_input_rect.width, gravity_input_rect.height),
            'gravity_plus_btn': pygame.Rect(gravity_plus_btn.x, gravity_plus_btn.y + scroll_offset, gravity_plus_btn.width, gravity_plus_btn.height),
            'gravity_minus_btn': pygame.Rect(gravity_minus_btn.x, gravity_minus_btn.y + scroll_offset, gravity_minus_btn.width, gravity_minus_btn.height),
            'confirm_player': pygame.Rect(confirm_player_btn.x, confirm_player_btn.y + scroll_offset, confirm_player_btn.width, confirm_player_btn.height),
            'instant_mining_checkbox': pygame.Rect(instant_mining_checkbox.x, instant_mining_checkbox.y + scroll_offset, instant_mining_checkbox.width, instant_mining_checkbox.height),
            'god_mode_checkbox': pygame.Rect(god_mode_checkbox.x, god_mode_checkbox.y + scroll_offset, god_mode_checkbox.width, god_mode_checkbox.height),
            'area_place_checkbox': pygame.Rect(area_place_checkbox.x, area_place_checkbox.y + scroll_offset, area_place_checkbox.width, area_place_checkbox.height),
            'area_mine_checkbox': pygame.Rect(area_mine_checkbox.x, area_mine_checkbox.y + scroll_offset, area_mine_checkbox.width, area_mine_checkbox.height),
            'fullscreen_click_checkbox': pygame.Rect(fullscreen_click_checkbox.x, fullscreen_click_checkbox.y + scroll_offset, fullscreen_click_checkbox.width, fullscreen_click_checkbox.height),
            'fly_mode_checkbox': pygame.Rect(fly_mode_checkbox.x, fly_mode_checkbox.y + scroll_offset, fly_mode_checkbox.width, fly_mode_checkbox.height),
            'time_input': pygame.Rect(time_input_rect.x, time_input_rect.y + scroll_offset, time_input_rect.width, time_input_rect.height),
            'time_plus_btn': pygame.Rect(time_plus_btn.x, time_plus_btn.y + scroll_offset, time_plus_btn.width, time_plus_btn.height),
            'time_minus_btn': pygame.Rect(time_minus_btn.x, time_minus_btn.y + scroll_offset, time_minus_btn.width, time_minus_btn.height),
            'creature_input': pygame.Rect(creature_input_rect.x, creature_input_rect.y + scroll_offset, creature_input_rect.width, creature_input_rect.height),
            'spawn_creature_btn': pygame.Rect(spawn_creature_btn.x, spawn_creature_btn.y + scroll_offset, spawn_creature_btn.width, spawn_creature_btn.height),
            # 添加缺失的新输入框
            'defense_input': pygame.Rect(defense_input_rect.x, defense_input_rect.y + scroll_offset, defense_input_rect.width, defense_input_rect.height),
            'damage_reduction_input': pygame.Rect(damage_reduction_input_rect.x, damage_reduction_input_rect.y + scroll_offset, damage_reduction_input_rect.width, damage_reduction_input_rect.height),
            'damage_bonus_input': pygame.Rect(damage_bonus_input_rect.x, damage_bonus_input_rect.y + scroll_offset, damage_bonus_input_rect.width, damage_bonus_input_rect.height),
            'fall_damage_reduction_input': pygame.Rect(fall_damage_reduction_input_rect.x, fall_damage_reduction_input_rect.y + scroll_offset, fall_damage_reduction_input_rect.width, fall_damage_reduction_input_rect.height),
            'speed_bonus_input': pygame.Rect(speed_bonus_input_rect.x, speed_bonus_input_rect.y + scroll_offset, speed_bonus_input_rect.width, speed_bonus_input_rect.height)
        }
        
    def handle_advanced_menu_click(self, mx, my):
        """处理高级功能页面的点击事件"""
        # 创建考虑滚动偏移量的鼠标位置
        # 注意：与draw_advanced_menu中的scroll_offset = -self.advanced_scroll_offset保持一致
        # 当界面向下滚动时，UI元素向上移动，所以实际点击位置也应该向上调整
        adjusted_mouse_y = my - self.advanced_scroll_offset
        adjusted_pos = (mx, adjusted_mouse_y)
        
        # 检查是否点击了X坐标输入框
        if 'x_input' in self.advanced_menu_buttons and self.advanced_menu_buttons['x_input'].collidepoint(adjusted_pos):
            self.input_active = 'x'
            self.input_text = str(self.target_x)
        # 检查是否点击了Y坐标输入框
        elif 'y_input' in self.advanced_menu_buttons and self.advanced_menu_buttons['y_input'].collidepoint(adjusted_pos):
            self.input_active = 'y'
            self.input_text = str(self.target_y)
        # 检查是否点击了确认传送按钮
        elif 'confirm' in self.advanced_menu_buttons and self.advanced_menu_buttons['confirm'].collidepoint(adjusted_pos):
            try:
                # 尝试将玩家传送到指定坐标
                if self.input_active == 'x':
                    self.target_x = int(self.input_text)
                    self.input_active = None
                elif self.input_active == 'y':
                    self.target_y = int(self.input_text)
                    self.input_active = None
                
                # 执行传送
                self.player.x = self.target_x * TILE_SIZE
                self.player.y = self.target_y * TILE_SIZE
                self.camera_x = self.player.x - WIDTH // 2
                self.camera_y = self.player.y - HEIGHT // 2
                
                # 记录传送日志
                print(f"玩家已传送到坐标: ({self.target_x}, {self.target_y})")
            except ValueError:
                # 处理无效的坐标输入
                print("错误: 请输入有效的数字坐标")
        # 检查是否点击了生命值输入框
        elif 'health_input' in self.advanced_menu_buttons and self.advanced_menu_buttons['health_input'].collidepoint(adjusted_pos):
            self.input_active = 'health'
            # 初始化玩家属性值
            if not hasattr(self, 'target_health'):
                self.target_health = self.player.health
            self.input_text = str(self.target_health)
        # 检查是否点击了移动速度输入框
        elif 'speed_input' in self.advanced_menu_buttons and self.advanced_menu_buttons['speed_input'].collidepoint(adjusted_pos):
            self.input_active = 'speed'
            # 初始化玩家属性值
            if not hasattr(self, 'target_speed'):
                self.target_speed = self.player.speed
            self.input_text = str(self.target_speed)
        # 检查是否点击了跳跃力输入框
        elif 'jump_input' in self.advanced_menu_buttons and self.advanced_menu_buttons['jump_input'].collidepoint(adjusted_pos):
            self.input_active = 'jump'
            # 初始化玩家属性值
            if not hasattr(self, 'target_jump'):
                self.target_jump = self.player.jump_strength
            self.input_text = str(self.target_jump)
        # 检查是否点击了初始伤害输入框
        elif 'damage_input' in self.advanced_menu_buttons and self.advanced_menu_buttons['damage_input'].collidepoint(adjusted_pos):
            self.input_active = 'damage'
            self.input_text = str(self.target_damage)
        # 检查是否点击了防御力输入框
        elif 'defense_input' in self.advanced_menu_buttons and self.advanced_menu_buttons['defense_input'].collidepoint(adjusted_pos):
            self.input_active = 'defense'
            self.input_text = str(self.target_defense)
        # 检查是否点击了免伤百分比输入框
        elif 'damage_reduction_input' in self.advanced_menu_buttons and self.advanced_menu_buttons['damage_reduction_input'].collidepoint(adjusted_pos):
            self.input_active = 'damage_reduction'
            self.input_text = str(self.target_damage_reduction)
        # 检查是否点击了伤害加成输入框
        elif 'damage_bonus_input' in self.advanced_menu_buttons and self.advanced_menu_buttons['damage_bonus_input'].collidepoint(adjusted_pos):
            self.input_active = 'damage_bonus'
            self.input_text = str(self.target_damage_bonus)
        # 检查是否点击了摔伤减免输入框
        elif 'fall_damage_reduction_input' in self.advanced_menu_buttons and self.advanced_menu_buttons['fall_damage_reduction_input'].collidepoint(adjusted_pos):
            self.input_active = 'fall_damage_reduction'
            self.input_text = str(self.target_fall_damage_reduction)
        # 检查是否点击了移速加成输入框
        elif 'speed_bonus_input' in self.advanced_menu_buttons and self.advanced_menu_buttons['speed_bonus_input'].collidepoint(adjusted_pos):
            self.input_active = 'speed_bonus'
            self.input_text = str(self.target_speed_bonus)
        # 检查是否点击了重力输入框
        elif 'gravity_input' in self.advanced_menu_buttons and self.advanced_menu_buttons['gravity_input'].collidepoint(adjusted_pos):
            self.input_active = 'gravity'
            self.input_text = str(round(self.target_gravity, 1))
        # 检查是否点击了重力+0.1按钮
        elif 'gravity_plus_btn' in self.advanced_menu_buttons and self.advanced_menu_buttons['gravity_plus_btn'].collidepoint(adjusted_pos):
            self.target_gravity = round(self.target_gravity + 0.1, 1)
            self.player.gravity = self.target_gravity
            self.input_active = None
            print(f"玩家重力已设置为: {self.target_gravity}")
        # 检查是否点击了重力-0.1按钮
        elif 'gravity_minus_btn' in self.advanced_menu_buttons and self.advanced_menu_buttons['gravity_minus_btn'].collidepoint(adjusted_pos):
            self.target_gravity = max(0, round(self.target_gravity - 0.1, 1))
            self.player.gravity = self.target_gravity
            self.input_active = None
            print(f"玩家重力已设置为: {self.target_gravity}")
        # 检查是否点击了确认修改按钮
        elif 'confirm_player' in self.advanced_menu_buttons and self.advanced_menu_buttons['confirm_player'].collidepoint(adjusted_pos):
            try:
                # 尝试更新玩家属性
                if self.input_active == 'health':
                    self.target_health = int(self.input_text)
                    self.input_active = None
                elif self.input_active == 'speed':
                    self.target_speed = int(self.input_text)
                    self.input_active = None
                elif self.input_active == 'jump':
                    self.target_jump = int(self.input_text)
                    self.input_active = None
                
                # 执行更新（无上限设置）
                if hasattr(self, 'target_health'):
                    self.player.health = max(0, self.target_health)  # 允许生命值降为0，无最大值限制
                    self.player.max_health = self.player.health
                if hasattr(self, 'target_speed'):
                    self.player.speed = max(1, self.target_speed)  # 限制最小值为1，无最大值限制
                if hasattr(self, 'target_jump'):
                    self.player.jump_strength = min(max(-50, self.target_jump), -1)  # 限制范围为-50到-1（确保负值以便正常跳跃）
                
                # 更新初始伤害
                if self.input_active == 'damage':
                    self.target_damage = int(self.input_text)
                    self.input_active = None
                    self.player.damage = self.target_damage  # 将伤害值设置到玩家对象上
                # 更新重力值
                elif self.input_active == 'gravity':
                    self.target_gravity = float(self.input_text)
                    self.input_active = None
                    if self.target_gravity >= 0:
                        self.player.gravity = self.target_gravity
                    else:
                        # 如果重力值无效，则移除自定义重力属性
                        if hasattr(self.player, 'gravity'):
                            delattr(self.player, 'gravity')
                # 更新防御力
                elif self.input_active == 'defense':
                    self.target_defense = int(self.input_text)
                    self.input_active = None
                    self.player.defense = self.target_defense
                # 更新免伤百分比
                elif self.input_active == 'damage_reduction':
                    self.target_damage_reduction = int(self.input_text)
                    self.input_active = None
                    self.player.damage_reduction = self.target_damage_reduction
                # 更新伤害加成
                elif self.input_active == 'damage_bonus':
                    self.target_damage_bonus = int(self.input_text)
                    self.input_active = None
                    self.player.damage_bonus = self.target_damage_bonus
                # 更新摔伤减免
                elif self.input_active == 'fall_damage_reduction':
                    self.target_fall_damage_reduction = int(self.input_text)
                    self.input_active = None
                    self.player.fall_damage_reduction = self.target_fall_damage_reduction
                # 更新移速加成
                elif self.input_active == 'speed_bonus':
                    self.target_speed_bonus = int(self.input_text)
                    self.input_active = None
                    self.player.speed_bonus = self.target_speed_bonus
                
                # 记录属性修改日志
                gravity_status = getattr(self.player, 'gravity', '默认')
                if gravity_status != '默认':
                    gravity_status = round(gravity_status, 1)
                print(f"玩家属性已更新: 生命值={self.player.health}, 移动速度={self.player.speed}, 跳跃力={self.player.jump_strength}, 初始伤害={self.player.damage}, 重力={gravity_status}, 防御={self.player.defense}, 免伤={self.player.damage_reduction}%, 伤害加成={self.player.damage_bonus}%, 摔伤减免={self.player.fall_damage_reduction}%, 移速加成={self.player.speed_bonus}%")
            except ValueError:
                # 处理无效的输入
                print("错误: 请输入有效的数字")
        # 检查是否点击了秒挖掘复选框
        elif 'instant_mining_checkbox' in self.advanced_menu_buttons and self.advanced_menu_buttons['instant_mining_checkbox'].collidepoint(adjusted_pos):
            self.instant_mining = not self.instant_mining
            self.input_active = None
            print(f"秒挖掘功能已{'开启' if self.instant_mining else '关闭'}")
        # 检查是否点击了最高权限复选框
        elif 'god_mode_checkbox' in self.advanced_menu_buttons and self.advanced_menu_buttons['god_mode_checkbox'].collidepoint(adjusted_pos):
            self.god_mode = not self.god_mode
            self.input_active = None
            print(f"最高权限功能已{'开启' if self.god_mode else '关闭'}")
        # 检查是否点击了3*3放置复选框
        elif 'area_place_checkbox' in self.advanced_menu_buttons and self.advanced_menu_buttons['area_place_checkbox'].collidepoint(adjusted_pos):
            self.area_place_enabled = not self.area_place_enabled
            self.input_active = None
            print(f"3*3放置功能已{'开启' if self.area_place_enabled else '关闭'}")
        # 检查是否点击了3*3范围挖掘复选框
        elif 'area_mine_checkbox' in self.advanced_menu_buttons and self.advanced_menu_buttons['area_mine_checkbox'].collidepoint(adjusted_pos):
            self.area_mine_enabled = not self.area_mine_enabled
            self.input_active = None
            print(f"3*3范围挖掘功能已{'开启' if self.area_mine_enabled else '关闭'}")
        # 检查是否点击了全屏点击任意位置挖掘放置复选框
        elif 'fullscreen_click_checkbox' in self.advanced_menu_buttons and self.advanced_menu_buttons['fullscreen_click_checkbox'].collidepoint(adjusted_pos):
            self.fullscreen_click_enabled = not self.fullscreen_click_enabled
            self.input_active = None
            print(f"全屏点击任意位置挖掘放置功能已{'开启' if self.fullscreen_click_enabled else '关闭'}")
        # 检查是否点击了飞行模式复选框
        elif 'fly_mode_checkbox' in self.advanced_menu_buttons and self.advanced_menu_buttons['fly_mode_checkbox'].collidepoint(adjusted_pos):
            if not hasattr(self.player, 'fly_mode'):
                self.player.fly_mode = False
            self.player.fly_mode = not self.player.fly_mode
            self.input_active = None
            print(f"飞行模式已{'开启' if self.player.fly_mode else '关闭'}")
        # 检查是否点击了时间输入框
        elif 'time_input' in self.advanced_menu_buttons and self.advanced_menu_buttons['time_input'].collidepoint(adjusted_pos):
            self.input_active = 'time'
            hours = int(self.world.time_of_day // 100)
            minutes = int(self.world.time_of_day % 100)
            self.input_text = f"{hours:02d}:{minutes:02d}"
        # 检查是否点击了时间+01:00按钮
        elif 'time_plus_btn' in self.advanced_menu_buttons and self.advanced_menu_buttons['time_plus_btn'].collidepoint(adjusted_pos):
            try:
                # 获取当前时间
                current_time = self.world.time_of_day
                hours = int(current_time // 100)
                minutes = int(current_time % 100)
                
                # 增加1小时
                new_hours = (hours + 1) % 24
                self.world.time_of_day = new_hours * 100 + minutes
                print(f"世界时间已设置为: {new_hours:02d}:{minutes:02d}")
                self.input_active = None
            except:
                print("错误: 调整时间失败")
        # 检查是否点击了时间-01:00按钮
        elif 'time_minus_btn' in self.advanced_menu_buttons and self.advanced_menu_buttons['time_minus_btn'].collidepoint(adjusted_pos):
            try:
                # 获取当前时间
                current_time = self.world.time_of_day
                hours = int(current_time // 100)
                minutes = int(current_time % 100)
                
                # 减少1小时
                new_hours = (hours - 1) % 24
                self.world.time_of_day = new_hours * 100 + minutes
                print(f"世界时间已设置为: {new_hours:02d}:{minutes:02d}")
                self.input_active = None
            except:
                print("错误: 调整时间失败")
        # 检查是否点击了生物数量输入框
        elif 'creature_input' in self.advanced_menu_buttons and self.advanced_menu_buttons['creature_input'].collidepoint(adjusted_pos):
            self.input_active = 'creature'
            self.input_text = "10"  # 默认值
        # 检查是否点击了生成生物按钮
        elif 'spawn_creature_btn' in self.advanced_menu_buttons and self.advanced_menu_buttons['spawn_creature_btn'].collidepoint(adjusted_pos):
            try:
                if self.input_active == 'creature':
                    count = int(self.input_text)
                    self.input_active = None
                else:
                    count = 10  # 默认生成10只生物
                
                if count > 0 and count <= 100:  # 限制生成数量在1-100之间
                    # 生成指定数量的生物
                    new_creatures = self.spawn_initial_creatures(count)
                    self.creatures.extend(new_creatures)
                    print(f"已生成 {count} 只生物")
                else:
                    print("错误: 生成数量应在1-100之间")
            except:
                print("错误: 无效的生物数量")
        else:
            # 点击了其他区域，取消输入状态
            self.input_active = None
    
    def draw_creative_inventory(self, screen):
        """绘制创造背包界面"""
        # 获取当前时间（用于呼吸效果）
        current_time = pygame.time.get_ticks()
        
        # 绘制径向渐变背景
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        radius = max(WIDTH, HEIGHT) // 2
        for r in range(radius, 0, -2):
            alpha = int(200 * (r / radius))  # 从中心向外透明度递减
            color = (30, 30, 40)  # 深色背景
            pygame.draw.circle(screen, (color[0], color[1], color[2], alpha), 
                              (center_x, center_y), r)
        
        # 绘制主界面背景
        bg_rect = pygame.Rect(50, 50, WIDTH - 100, HEIGHT - 100)
        # 创建半透明的深色背景
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((40, 40, 50, 220))
        screen.blit(bg_surface, bg_rect)
        # 添加边框
        pygame.draw.rect(screen, (100, 100, 120), bg_rect, 3, 10)  # 圆角边框
        
        # 绘制标题（金色带发光效果）
        title_text = "创造背包"
        
        # 绘制标题发光效果
        glow_radius = 4
        glow_y = 80
        
        # 创建一个主发光表面，统一处理所有发光层
        final_glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # 绘制多层淡色发光
        for i in range(glow_radius, 0, -1):
            alpha = int(100 * (i / glow_radius))
            temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            glow_font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 50)
            glow_title = glow_font.render(title_text, True, (255, 215, 0, alpha))
            # 计算正确的居中位置
            glow_x = WIDTH // 2 - glow_title.get_width() // 2
            temp_surface.blit(glow_title, (glow_x, glow_y))
            
            # 模糊效果（兼容性实现）
            for _ in range(i):
                scale_factor = 0.5
                small_surface = pygame.transform.smoothscale(temp_surface, (
                    int(temp_surface.get_width() * scale_factor),
                    int(temp_surface.get_height() * scale_factor)
                ))
                temp_surface = pygame.transform.smoothscale(small_surface, temp_surface.get_size())
            
            # 将模糊后的发光效果添加到主表面
            final_glow_surface.blit(temp_surface, (0, 0))
        
        # 一次性将所有发光效果绘制到屏幕
        screen.blit(final_glow_surface, (0, 0))
        
        # 绘制主标题（可选，根据需要保留或移除）

        
        # 绘制分类按钮
        button_width = 120
        button_height = 45
        button_margin = 15
        total_width = len(self.creative_categories) * (button_width + button_margin) - button_margin
        start_x = WIDTH // 2 - total_width // 2
        start_y = 140
        
        self.creative_buttons = {}
        
        # 分类按钮颜色映射
        category_colors = {
            "方块": (80, 120, 80),
            "工具": (120, 80, 80),
            "武器": (150, 60, 60),
            "食物": (100, 100, 60),
            "材料": (80, 80, 120),
            "其他": (90, 90, 90),
            "装备": (100, 60, 120)  # 紫色系，代表装备的特殊性
        }
        
        for i, category in enumerate(self.creative_categories.keys()):
            button_x = start_x + i * (button_width + button_margin)
            button_rect = pygame.Rect(button_x, start_y, button_width, button_height)
            
            # 按钮背景和悬停效果
            button_color = category_colors.get(category, (80, 80, 80))
            if category == self.selected_creative_category:
                # 选中的分类按钮高亮
                selected_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
                pygame.draw.rect(selected_surface, (button_color[0] + 40, button_color[1] + 40, button_color[2] + 40, 255), 
                                (0, 0, button_width, button_height), 0, 5)
                # 内发光效果
                for radius in range(1, 3):
                    glow_surface = pygame.Surface((button_width + radius*2, button_height + radius*2), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surface, (255, 215, 0, 50 - radius*15), 
                                   (0, 0, button_width + radius*2, button_height + radius*2), 0, 5 + radius)
                    screen.blit(glow_surface, (button_x - radius, start_y - radius))
                screen.blit(selected_surface, button_rect)
            else:
                # 普通按钮带渐变效果
                gradient_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
                for y in range(button_height):
                    brightness_factor = 1.0 - y * 0.1 / button_height
                    r = int(button_color[0] * brightness_factor)
                    g = int(button_color[1] * brightness_factor)
                    b = int(button_color[2] * brightness_factor)
                    pygame.draw.line(gradient_surface, (r, g, b, 220), (0, y), (button_width, y))
                screen.blit(gradient_surface, button_rect)
            
            # 按钮边框
            pygame.draw.rect(screen, (200, 200, 200), button_rect, 2, 5)
            
            # 绘制按钮文本
            text = font_medium.render(category, True, (255, 255, 255))
            text_x = button_x + button_width // 2 - text.get_width() // 2
            text_y = start_y + button_height // 2 - text.get_height() // 2
            screen.blit(text, (text_x, text_y))
            
            # 保存按钮矩形供点击检测
            self.creative_buttons[category] = button_rect
        
        # 绘制物品网格
        item_size = 70
        grid_cols = 11  # 调整为11列以适应更宽的物品格
        grid_spacing = 10
        
        grid_width = grid_cols * (item_size + grid_spacing) - grid_spacing
        grid_height = HEIGHT - 320  # 调整高度
        grid_x = WIDTH // 2 - grid_width // 2
        grid_y = 200  # 网格Y位置
        
        # 绘制网格背景
        grid_bg_rect = pygame.Rect(grid_x - 10, grid_y - 10, grid_width + 20, grid_height + 20)
        grid_bg_surface = pygame.Surface((grid_bg_rect.width, grid_bg_rect.height), pygame.SRCALPHA)
        grid_bg_surface.fill((35, 35, 45, 200))
        screen.blit(grid_bg_surface, grid_bg_rect)
        pygame.draw.rect(screen, (80, 80, 100), grid_bg_rect, 2, 5)
        
        # 绘制物品
        selected_items = self.creative_categories[self.selected_creative_category]
        item_count = len(selected_items)
        rows = (item_count + grid_cols - 1) // grid_cols
        total_height = rows * (item_size + 30) - 10  # 增加物品名称的垂直空间
        
        # 更新最大滚动偏移量
        self.creative_max_scroll_offset = max(0, total_height - grid_height)
        
        # 确保滚动偏移量不超过最大值
        self.creative_scroll_offset = min(self.creative_scroll_offset, self.creative_max_scroll_offset)
        
        # 绘制物品格子和物品
        for i, item_id in enumerate(selected_items):
            row = i // grid_cols
            col = i % grid_cols
            
            item_x = grid_x + col * (item_size + grid_spacing)
            item_y = grid_y + row * (item_size + 30) - self.creative_scroll_offset  # 增加垂直间距
            
            # 只有当物品在可见区域内时才绘制
            if 0 <= item_y < HEIGHT:
                # 获取鼠标位置，检查是否悬停
                mouse_pos = pygame.mouse.get_pos()
                is_hovered = pygame.Rect(item_x, item_y, item_size, item_size + 25).collidepoint(mouse_pos)
                
                # 绘制物品格子 - 添加悬停效果和立体感
                if is_hovered:
                    # 悬停时的高亮背景
                    hover_surface = pygame.Surface((item_size, item_size), pygame.SRCALPHA)
                    pygame.draw.rect(hover_surface, (100, 100, 120, 200), (0, 0, item_size, item_size), 0, 3)
                    # 内发光效果
                    glow_surface = pygame.Surface((item_size + 4, item_size + 4), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surface, (255, 215, 0, 70), (0, 0, item_size + 4, item_size + 4), 0, 5)
                    screen.blit(glow_surface, (item_x - 2, item_y - 2))
                    screen.blit(hover_surface, (item_x, item_y))
                else:
                    # 普通背景 - 添加渐变效果
                    item_bg_surface = pygame.Surface((item_size, item_size), pygame.SRCALPHA)
                    for y in range(item_size):
                        brightness = 70 + y * 0.4  # 从上到下变亮
                        pygame.draw.line(item_bg_surface, (brightness, brightness, brightness, 200), (0, y), (item_size, y))
                    screen.blit(item_bg_surface, (item_x, item_y))
                
                # 绘制边框
                pygame.draw.rect(screen, (100, 100, 100), (item_x, item_y, item_size, item_size), 1)
                # 上边框和左边框使用亮色，增强立体感
                pygame.draw.line(screen, (150, 150, 150), (item_x, item_y), (item_x + item_size, item_y), 1)
                pygame.draw.line(screen, (150, 150, 150), (item_x, item_y), (item_x, item_y + item_size), 1)
                
                # 尝试加载和显示物品图像，如果失败则使用颜色方块
                item_info = ITEMS.get(item_id)
                if item_info and item_info.get("texture") in self.image_loader.images:
                    # 图像存在，显示图像
                    item_img = pygame.transform.scale(
                        self.image_loader.images[item_info["texture"]], 
                        (item_size - 12, item_size - 12)
                    )
                    # 添加轻微阴影
                    shadow_offset = 2
                    shadow_surface = pygame.Surface((item_size - 12, item_size - 12), pygame.SRCALPHA)
                    shadow_surface.fill((0, 0, 0, 100))
                    screen.blit(shadow_surface, (item_x + 5 + shadow_offset, item_y + 5 + shadow_offset))
                    screen.blit(item_img, (item_x + 5, item_y + 5))
                else:
                    # 图像不存在，使用颜色方块
                    if item_id in BLOCKS:
                        block_color = BLOCKS[item_id].get("color", (200, 200, 200))
                    elif item_id in ITEMS:
                        # 对于非方块物品，使用物品类型的默认颜色
                        item_type = ITEMS[item_id].get("type", "")
                        if item_type == "weapon":
                            block_color = (200, 80, 80)  # 武器红色
                        elif item_type == "tool":
                            block_color = (80, 200, 80)  # 工具绿色
                        elif item_type == "food":
                            block_color = (255, 220, 100)  # 食物黄色
                        else:
                            block_color = (150, 150, 150)  # 默认灰色
                    else:
                        block_color = (150, 150, 150)  # 未知物品灰色
                    
                    # 绘制带渐变的颜色方块
                    item_surface = pygame.Surface((item_size - 10, item_size - 10), pygame.SRCALPHA)
                    for y in range(item_size - 10):
                        brightness_factor = 0.7 + y * 0.3 / (item_size - 10)
                        r = int(block_color[0] * brightness_factor)
                        g = int(block_color[1] * brightness_factor)
                        b = int(block_color[2] * brightness_factor)
                        pygame.draw.line(item_surface, (r, g, b, 255), (0, y), (item_size - 10, y))
                    screen.blit(item_surface, (item_x + 5, item_y + 5))
                
                # 绘制物品名称
                item_name = ITEMS.get(item_id, {"name": "未知物品"})["name"]
                
                # 确保文字不超过格子宽度，如果超过则截断显示
                max_text_width = item_size - 8
                display_name = item_name
                while len(display_name) > 0:
                    name_text = font_small.render(display_name, True, (255, 255, 255))
                    if name_text.get_width() <= max_text_width or len(display_name) == 1:
                        break
                    display_name = display_name[:-1]
                
                if len(display_name) < len(item_name):
                    display_name = display_name[:-1] + "..."
                
                # 添加文字背景以增强可读性
                name_text = font_small.render(display_name, True, (255, 255, 255))
                text_bg_rect = pygame.Rect(item_x + 1, item_y + item_size + 2, name_text.get_width() + 2, name_text.get_height() + 1)
                pygame.draw.rect(screen, (50, 50, 50, 230), text_bg_rect)
                pygame.draw.rect(screen, (80, 80, 80), text_bg_rect, 1)  # 边框
                screen.blit(name_text, (item_x + 2, item_y + item_size + 3))
        
        # 绘制滚动条
        if self.creative_max_scroll_offset > 0:
            scrollbar_width = 12
            scrollbar_x = grid_x + grid_width + 15
            scrollbar_height = max(30, grid_height * grid_height / total_height)
            scrollbar_y = grid_y + (grid_height - scrollbar_height) * self.creative_scroll_offset / self.creative_max_scroll_offset
            
            # 绘制滚动条背景槽
            track_rect = pygame.Rect(scrollbar_x - 2, grid_y - 2, scrollbar_width + 4, grid_height + 4)
            pygame.draw.rect(screen, (30, 30, 40), track_rect, 0, 5)
            pygame.draw.rect(screen, (60, 60, 80), track_rect, 1)
            
            # 绘制滚动条滑块（带渐变和悬停效果）
            slider_rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height)
            mouse_pos = pygame.mouse.get_pos()
            is_hovered = slider_rect.collidepoint(mouse_pos)
            
            # 滑块渐变效果
            slider_surface = pygame.Surface((scrollbar_width, scrollbar_height), pygame.SRCALPHA)
            for x in range(scrollbar_width):
                # 从左到右渐变
                left_brightness = 180 if is_hovered else 120
                right_brightness = 120 if is_hovered else 80
                brightness = left_brightness + (right_brightness - left_brightness) * x / scrollbar_width
                pygame.draw.line(slider_surface, (brightness, brightness, brightness, 255), (x, 0), (x, scrollbar_height))
            
            # 滑块边框
            screen.blit(slider_surface, slider_rect)
            pygame.draw.rect(screen, (200, 200, 200), slider_rect, 1)
            # 顶部和左侧亮色边框，增强立体感
            pygame.draw.line(screen, (220, 220, 220), (scrollbar_x, scrollbar_y), (scrollbar_x + scrollbar_width, scrollbar_y), 1)
            pygame.draw.line(screen, (220, 220, 220), (scrollbar_x, scrollbar_y), (scrollbar_x, scrollbar_y + scrollbar_height), 1)
        
        # 绘制关闭提示（呼吸效果）
        # 计算呼吸效果的亮度
        breathing_effect = 150 + 50 * math.sin(current_time * 0.002)
        close_hint = font_small.render("按F3键关闭创造背包", True, (int(breathing_effect), int(breathing_effect), int(breathing_effect)))
        
        # 添加发光背景
        hint_bg_rect = pygame.Rect(
            WIDTH // 2 - close_hint.get_width() // 2 - 10,
            HEIGHT - 55,
            close_hint.get_width() + 20,
            close_hint.get_height() + 10
        )
        
        # 发光背景
        glow_alpha = 100 + 50 * math.sin(current_time * 0.003)
        glow_surface = pygame.Surface((hint_bg_rect.width, hint_bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (255, 215, 0, int(glow_alpha)), 
                       (0, 0, hint_bg_rect.width, hint_bg_rect.height), 0, 10)
        # 轻微模糊效果（兼容性实现）
        scale_factor = 0.5
        small_surface = pygame.transform.smoothscale(glow_surface, (
            int(glow_surface.get_width() * scale_factor),
            int(glow_surface.get_height() * scale_factor)
        ))
        glow_surface = pygame.transform.smoothscale(small_surface, glow_surface.get_size())
        screen.blit(glow_surface, (hint_bg_rect.x, hint_bg_rect.y))
        
        # 绘制边框
        pygame.draw.rect(screen, (150, 150, 170), hint_bg_rect, 2, 10)
        
        # 绘制文本
        close_x = WIDTH // 2 - close_hint.get_width() // 2
        close_y = HEIGHT - 50
        screen.blit(close_hint, (close_x, close_y))
        
        # 绘制滚动提示
        scroll_hint = font_small.render("使用鼠标滚轮滚动浏览物品", True, (150, 150, 170))
        scroll_x = WIDTH // 2 - scroll_hint.get_width() // 2
        scroll_y = HEIGHT - 80
        screen.blit(scroll_hint, (scroll_x, scroll_y))
        
        # 绘制快捷拿去按钮（右下角）
        button_width = 160
        button_height = 45
        button_x = WIDTH - 60 - button_width
        button_y = HEIGHT - 60 - button_height
        
        # 按钮背景和状态颜色
        button_color = (80, 120, 80) if self.quick_take_enabled else (120, 80, 80)
        
        # 绘制按钮背景带渐变
        button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        for y in range(button_height):
            brightness_factor = 1.0 - y * 0.15 / button_height
            r = int(button_color[0] * brightness_factor)
            g = int(button_color[1] * brightness_factor)
            b = int(button_color[2] * brightness_factor)
            pygame.draw.line(button_surface, (r, g, b, 220), (0, y), (button_width, y))
        screen.blit(button_surface, (button_x, button_y))
        
        # 按钮边框
        pygame.draw.rect(screen, (200, 200, 200), (button_x, button_y, button_width, button_height), 2, 5)
        
        # 绘制按钮文本
        button_text = "快捷拿去: ON" if self.quick_take_enabled else "快捷拿去: OFF"
        text = font_small.render(button_text, True, (255, 255, 255))
        text_x = button_x + button_width // 2 - text.get_width() // 2
        text_y = button_y + button_height // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))
        
        # 保存按钮矩形供点击检测
        self.quick_take_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        # 绘制数量输入界面（如果需要显示）
        if self.show_quantity_input:
            # 计算界面位置和大小
            input_width = 300
            input_height = 200
            input_x = WIDTH // 2 - input_width // 2
            input_y = HEIGHT // 2 - input_height // 2
            
            # 创建半透明黑色背景遮罩，添加轻微模糊效果
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # 稍微加深背景遮罩
            screen.blit(overlay, (0, 0))
            
            # 绘制输入界面背景，添加光影效果
            input_bg_rect = pygame.Rect(input_x, input_y, input_width, input_height)
            input_bg_surface = pygame.Surface((input_width, input_height), pygame.SRCALPHA)
            
            # 界面渐变背景
            pygame.draw.rect(input_bg_surface, (60, 60, 80, 240), (0, 0, input_width, input_height), 0, 10)
            pygame.draw.rect(input_bg_surface, (70, 70, 90, 120), (0, 0, input_width, input_height//2), 0, 10)
            
            screen.blit(input_bg_surface, input_bg_rect)
            # 添加两层边框，增强立体感
            pygame.draw.rect(screen, (110, 110, 130), input_bg_rect, 3, 10)
            pygame.draw.rect(screen, (140, 140, 160), (input_x+1, input_y+1, input_width-2, input_height-2), 1, 9)
            
            # 绘制标题
            title_text = font_medium.render("选择拿取数量", True, (255, 220, 50))
            title_x = input_x + input_width // 2 - title_text.get_width() // 2
            title_y = input_y + 25
            screen.blit(title_text, (title_x, title_y))
            
            # 添加标题阴影效果
            shadow_text = font_medium.render("选择拿取数量", True, (0, 0, 0, 100))
            screen.blit(shadow_text, (title_x + 2, title_y + 2))
            
            # 绘制数量输入文本框
            input_box_width = 120
            input_box_height = 45
            input_box_x = input_x + input_width // 2 - input_box_width // 2
            input_box_y = input_y + 85
            input_box_rect = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)
            
            # 保存文本框矩形供点击检测
            if not hasattr(self, 'quantity_input_rect') or self.quantity_input_rect is None:
                self.quantity_input_rect = {}
            self.quantity_input_rect["input_box"] = input_box_rect
            
            # 绘制文本框背景，添加渐变效果
            box_surface = pygame.Surface((input_box_width, input_box_height), pygame.SRCALPHA)
            if self.input_active == 'quantity':
                # 激活状态的颜色
                pygame.draw.rect(box_surface, (120, 120, 140, 255), (0, 0, input_box_width, input_box_height), 0, 5)
                pygame.draw.rect(box_surface, (140, 140, 160, 100), (0, 0, input_box_width, input_box_height//2), 0, 5)
            else:
                # 非激活状态的颜色
                pygame.draw.rect(box_surface, (90, 90, 110, 220), (0, 0, input_box_width, input_box_height), 0, 5)
                pygame.draw.rect(box_surface, (110, 110, 130, 80), (0, 0, input_box_width, input_box_height//2), 0, 5)
            screen.blit(box_surface, input_box_rect)
            
            # 添加边框效果
            pygame.draw.rect(screen, (200, 200, 200), input_box_rect, 2, 5)
            if self.input_active == 'quantity':
                # 激活状态下的额外边框
                pygame.draw.rect(screen, (255, 220, 50), (input_box_x-1, input_box_y-1, input_box_width+2, input_box_height+2), 1, 6)
            
            # 绘制输入文本
            if self.input_active == 'quantity':
                # 显示用户正在输入的文本
                display_text = self.input_text if self.input_text else '0'
            else:
                # 显示当前数量
                display_text = str(self.quantity_to_take)
            
            # 使用更适合数字显示的字体颜色
            quantity_color = (255, 230, 100) if self.input_active == 'quantity' else (255, 255, 255)
            quantity_text = font_large.render(display_text, True, quantity_color)
            quantity_text_x = input_box_x + input_box_width // 2 - quantity_text.get_width() // 2
            quantity_text_y = input_box_y + input_box_height // 2 - quantity_text.get_height() // 2
            
            # 添加文本阴影效果
            shadow_text = font_large.render(display_text, True, (0, 0, 0, 150))
            screen.blit(shadow_text, (quantity_text_x + 1, quantity_text_y + 1))
            screen.blit(quantity_text, (quantity_text_x, quantity_text_y))
            
            # 如果正在输入，绘制光标
            if self.input_active == 'quantity':
                cursor_x = quantity_text_x + quantity_text.get_width() + 2
                cursor_y = input_box_y + 5
                cursor_height = input_box_height - 10
                pygame.draw.line(screen, (255, 255, 255), (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)
            
            # 绘制-和+按钮
            btn_size = 45
            minus_btn_x = input_x + input_width // 2 - btn_size * 2 - 10  # 调整间距
            plus_btn_x = input_x + input_width // 2 + btn_size + 10      # 调整间距
            btn_y = input_y + 82
            
            # 检查鼠标是否悬停在按钮上
            is_minus_hover = pygame.Rect(minus_btn_x, btn_y, btn_size, btn_size).collidepoint(pygame.mouse.get_pos())
            is_plus_hover = pygame.Rect(plus_btn_x, btn_y, btn_size, btn_size).collidepoint(pygame.mouse.get_pos())
            
            # -按钮
            minus_btn_rect = pygame.Rect(minus_btn_x, btn_y, btn_size, btn_size)
            minus_surface = pygame.Surface((btn_size, btn_size), pygame.SRCALPHA)
            # 根据悬停状态改变按钮颜色
            if is_minus_hover:
                pygame.draw.rect(minus_surface, (100, 100, 120, 240), (0, 0, btn_size, btn_size), 0, 8)
                pygame.draw.rect(minus_surface, (120, 120, 140, 100), (0, 0, btn_size, btn_size//2), 0, 8)
            else:
                pygame.draw.rect(minus_surface, (80, 80, 100, 220), (0, 0, btn_size, btn_size), 0, 8)
                pygame.draw.rect(minus_surface, (100, 100, 120, 80), (0, 0, btn_size, btn_size//2), 0, 8)
            screen.blit(minus_surface, minus_btn_rect)
            pygame.draw.rect(screen, (200, 200, 200), minus_btn_rect, 2, 8)
            
            minus_text = font_large.render("-", True, (255, 255, 255))
            minus_text_x = minus_btn_x + btn_size // 2 - minus_text.get_width() // 2
            minus_text_y = btn_y + btn_size // 2 - minus_text.get_height() // 2
            # 添加文本阴影
            shadow_minus = font_large.render("-", True, (0, 0, 0, 150))
            screen.blit(shadow_minus, (minus_text_x + 1, minus_text_y + 1))
            screen.blit(minus_text, (minus_text_x, minus_text_y))
            
            # +按钮
            plus_btn_rect = pygame.Rect(plus_btn_x, btn_y, btn_size, btn_size)
            plus_surface = pygame.Surface((btn_size, btn_size), pygame.SRCALPHA)
            # 根据悬停状态改变按钮颜色
            if is_plus_hover:
                pygame.draw.rect(plus_surface, (90, 120, 90, 240), (0, 0, btn_size, btn_size), 0, 8)
                pygame.draw.rect(plus_surface, (110, 140, 110, 100), (0, 0, btn_size, btn_size//2), 0, 8)
            else:
                pygame.draw.rect(plus_surface, (80, 100, 80, 220), (0, 0, btn_size, btn_size), 0, 8)
                pygame.draw.rect(plus_surface, (100, 120, 100, 80), (0, 0, btn_size, btn_size//2), 0, 8)
            screen.blit(plus_surface, plus_btn_rect)
            pygame.draw.rect(screen, (200, 200, 200), plus_btn_rect, 2, 8)
            
            plus_text = font_large.render("+", True, (255, 255, 255))
            plus_text_x = plus_btn_x + btn_size // 2 - plus_text.get_width() // 2
            plus_text_y = btn_y + btn_size // 2 - plus_text.get_height() // 2
            # 添加文本阴影
            shadow_plus = font_large.render("+", True, (0, 0, 0, 150))
            screen.blit(shadow_plus, (plus_text_x + 1, plus_text_y + 1))
            screen.blit(plus_text, (plus_text_x, plus_text_y))
            
            # 绘制确认按钮
            confirm_width = 120
            confirm_height = 45
            confirm_x = input_x + input_width // 2 - confirm_width // 2
            confirm_y = input_y + input_height - 60
            
            # 检查鼠标是否悬停在确认按钮上
            is_confirm_hover = pygame.Rect(confirm_x, confirm_y, confirm_width, confirm_height).collidepoint(pygame.mouse.get_pos())
            
            confirm_btn_rect = pygame.Rect(confirm_x, confirm_y, confirm_width, confirm_height)
            confirm_surface = pygame.Surface((confirm_width, confirm_height), pygame.SRCALPHA)
            # 根据悬停状态改变按钮颜色
            if is_confirm_hover:
                pygame.draw.rect(confirm_surface, (90, 140, 90, 240), (0, 0, confirm_width, confirm_height), 0, 8)
                pygame.draw.rect(confirm_surface, (110, 160, 110, 100), (0, 0, confirm_width, confirm_height//2), 0, 8)
            else:
                pygame.draw.rect(confirm_surface, (80, 120, 80, 220), (0, 0, confirm_width, confirm_height), 0, 8)
                pygame.draw.rect(confirm_surface, (100, 140, 100, 80), (0, 0, confirm_width, confirm_height//2), 0, 8)
            screen.blit(confirm_surface, confirm_btn_rect)
            pygame.draw.rect(screen, (200, 200, 200), confirm_btn_rect, 2, 8)
            
            confirm_text = font_small.render("确认", True, (255, 255, 255))
            confirm_text_x = confirm_x + confirm_width // 2 - confirm_text.get_width() // 2
            confirm_text_y = confirm_y + confirm_height // 2 - confirm_text.get_height() // 2
            # 添加文本阴影
            shadow_confirm = font_small.render("确认", True, (0, 0, 0, 150))
            screen.blit(shadow_confirm, (confirm_text_x + 1, confirm_text_y + 1))
            screen.blit(confirm_text, (confirm_text_x, confirm_text_y))
            
            # 保存按钮矩形供点击检测
            if not hasattr(self, 'quantity_input_rect') or self.quantity_input_rect is None:
                self.quantity_input_rect = {}
            self.quantity_input_rect.update({
                "minus": minus_btn_rect,
                "plus": plus_btn_rect,
                "confirm": confirm_btn_rect,
                "background": input_bg_rect
            })
    
    def handle_creative_inventory_click(self, mx, my):
        """处理创造背包的点击事件"""
        # 检查是否显示了数量输入界面
        if self.show_quantity_input and hasattr(self, 'quantity_input_rect'):
            # 处理文本框点击
            if "input_box" in self.quantity_input_rect and self.quantity_input_rect["input_box"].collidepoint(mx, my):
                # 激活数量输入模式
                self.input_active = 'quantity'
                self.input_text = str(self.quantity_to_take)
                return
            # 处理-按钮点击
            if self.quantity_input_rect["minus"].collidepoint(mx, my):
                self.quantity_to_take = max(1, self.quantity_to_take - 1)
                # 如果正在输入，同步更新输入文本
                if self.input_active == 'quantity':
                    self.input_text = str(self.quantity_to_take)
                return
            # 处理+按钮点击
            elif self.quantity_input_rect["plus"].collidepoint(mx, my):
                self.quantity_to_take = min(64, self.quantity_to_take + 1)
                # 如果正在输入，同步更新输入文本
                if self.input_active == 'quantity':
                    self.input_text = str(self.quantity_to_take)
                return
            # 处理确认按钮点击
            elif self.quantity_input_rect["confirm"].collidepoint(mx, my):
                # 如果正在输入数量，先处理输入
                if self.input_active == 'quantity':
                    try:
                        # 将输入文本转换为数字
                        input_value = int(self.input_text)
                        # 限制范围在1-64之间
                        self.quantity_to_take = max(1, min(64, input_value))
                    except ValueError:
                        # 输入不是有效的数字，使用默认值1
                        self.quantity_to_take = 1
                    # 取消输入模式
                    self.input_active = None
                    self.input_text = ""
                
                # 给玩家添加指定数量的物品
                if self.selected_item_for_quantity:
                    # 检查是否为装备类物品，限制数量为1
                    item_info = ITEMS.get(self.selected_item_for_quantity, {})
                    if 'type' in item_info and item_info['type'] in ['weapon', 'pickaxe', 'axe', 'shovel', 'helmet', 'armor', 'boots', 'special']:
                        actual_quantity = 1  # 装备类物品强制数量为1
                    else:
                        actual_quantity = self.quantity_to_take
                    self.player.add_item(self.selected_item_for_quantity, actual_quantity)
                    print(f"[{time.strftime('%H:%M:%S')}] 玩家从创造背包获取了 {ITEMS.get(self.selected_item_for_quantity, {'name': '未知物品'})['name']} × {actual_quantity}")
                # 重置状态
                self.show_quantity_input = False
                self.selected_item_for_quantity = None
                self.quantity_to_take = 1
                return
            # 点击背景以外区域关闭
            elif not self.quantity_input_rect["background"].collidepoint(mx, my):
                # 如果正在输入，保存输入值
                if self.input_active == 'quantity':
                    try:
                        # 将输入文本转换为数字
                        input_value = int(self.input_text)
                        # 限制范围在1-64之间
                        self.quantity_to_take = max(1, min(64, input_value))
                    except ValueError:
                        # 输入不是有效的数字，保持原值
                        pass
                    # 取消输入模式
                    self.input_active = None
                    self.input_text = ""
                
                self.show_quantity_input = False
                self.selected_item_for_quantity = None
                self.quantity_to_take = 1
                return
        
        # 检查是否点击了快捷拿去按钮
        if hasattr(self, 'quick_take_button_rect') and self.quick_take_button_rect.collidepoint(mx, my):
            self.quick_take_enabled = not self.quick_take_enabled
            return
        
        # 检查是否点击了分类按钮
        for category, rect in self.creative_buttons.items():
            if rect.collidepoint(mx, my):
                self.selected_creative_category = category
                self.creative_scroll_offset = 0  # 重置滚动偏移量
                return
        
        # 计算物品网格的位置，与draw_creative_inventory函数保持一致
        item_size = 70
        grid_cols = 11
        grid_spacing = 10
        
        grid_width = grid_cols * (item_size + grid_spacing) - grid_spacing
        grid_height = HEIGHT - 320  # 与绘制函数保持一致
        grid_x = WIDTH // 2 - grid_width // 2
        grid_y = 200  # 网格Y位置
        
        # 检查是否点击了物品
        selected_items = self.creative_categories[self.selected_creative_category]
        for i, item_id in enumerate(selected_items):
            row = i // grid_cols
            col = i % grid_cols
            
            item_x = grid_x + col * (item_size + grid_spacing)
            item_y = grid_y + row * (item_size + 30) - self.creative_scroll_offset  # 与绘制函数保持一致，增加垂直间距
            
            item_rect = pygame.Rect(item_x, item_y, item_size, item_size)
            if item_rect.collidepoint(mx, my):
                if self.quick_take_enabled:
                    # 根据物品类型设置不同的堆叠数量
                    item_info = ITEMS.get(item_id, {})
                    # 检查是否为装备类物品（包括所有需要堆叠上限为1的物品类型）
                    if 'type' in item_info and item_info['type'] in ['weapon', 'pickaxe', 'axe', 'shovel', 'helmet', 'armor', 'boots', 'special']:
                        quantity = 1  # 装备类物品上限1
                    else:
                        quantity = 99  # 其他物品上限99
                    self.player.add_item(item_id, quantity)
                    print(f"[{time.strftime('%H:%M:%S')}] 玩家从创造背包获取了 {ITEMS.get(item_id, {'name': '未知物品'})['name']} × {quantity}")
                else:
                    # 非快捷拿去模式：显示数量输入界面
                    self.show_quantity_input = True
                    self.selected_item_for_quantity = item_id
                    # 检查是否为装备类物品，设置合适的默认数量
                    item_info = ITEMS.get(item_id, {})
                    if 'type' in item_info and item_info['type'] in ['weapon', 'pickaxe', 'axe', 'shovel', 'helmet', 'armor', 'boots', 'special']:
                        self.quantity_to_take = 1  # 装备类物品默认数量1
                    else:
                        self.quantity_to_take = 1
                return
    def draw_save_selection(self, screen):
        """存档选择界面（已移除，相关功能已整合到开始游戏页面）"""
        # 绘制半透明背景
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # 半透明黑色
        screen.blit(overlay, (0, 0))
        
        # 显示提示信息
        font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Heiti TC"], 36)
        message = font.render("存档功能已整合到开始游戏页面", True, (255, 255, 255))
        screen.blit(message, (WIDTH//2 - message.get_width()//2, HEIGHT//2 - message.get_height()//2))
        
        # 清空存档选择按钮字典
        self.save_selection_buttons = {}
  







# 启动游戏
if __name__ == "__main__":
    game = Game()
    game.run()