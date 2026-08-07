import pygame
import random
import math
import sys
import time
import json
import os
import importlib.util
from f1页面 import help_manager
# 导入音频管理器
from 音频输出 import audio_manager
# 导入箱子模块
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from 箱子 import 箱子管理器
# 导入合成页面
from 合成页面 import CraftingPage

# 导入物品定义
from 物品定义 import (
    空气, 土块, 草方块, 岩石, 木头, 树叶, 水, 方块属性, 基岩,
    批量加载物品图片,
    # 方块
    铁矿石, 金矿石, 钻石矿石, 岩浆, 箱子, 火把, 黑土块, 红花, 草,
    木板, 铜矿石, 金块, 铁块, 钻石块, 铜块, 沙子, 枯草, 仙人掌,
    乔木, 乔木叶, 灌木, 岩石底, 床左, 床右, 床整体, 工作台,
    红方块, 红矿石, 红石块, 蓝方块, 蓝矿石, 蓝石块, 煤块, 煤矿,
    紫石块, 熔炉, 玻璃,
    # 植物生长阶段
    土豆发芽, 土豆幼年, 土豆成年,
    小麦发芽, 小麦幼年, 小麦成年,
    水稻发芽, 水稻幼年, 水稻成熟,
    玉米发芽, 玉米幼年, 玉米成年,
    甘蔗幼年, 甘蔗成年,
    番薯发芽, 番薯幼年, 番薯成年,
    白菜发芽, 白菜幼年, 白菜成年,
    # 物品材料
    红石, 金锭, 蓝石, 石子, 铁锭, 铜锭, 小煤块, 钻石, 木炭,
    # 工具武器
    木剑, 石剑, 铜剑, 铁剑, 金剑, 钻石剑,
    木弓箭, 木箭, 木箭发射, 弩, 未来弩, 激光炮,
    步枪, 手枪, 狙击枪, 子弹, 子弹发射,
    火箭筒, 火箭弹, 火箭弹发射,
    龙息暗雷, 龙息沧蓝, 龙息蓝核,
    木镐, 石镐, 铜镐, 铁镐, 金镐, 钻石镐,
    木斧, 石斧, 铜斧, 铁斧, 金斧, 钻石斧头,
    木铲, 石铲, 铜铲, 铁铲, 金铲, 钻石铲,
    # 食物
    苹果, 肉块, 乔木果,
    # 药水
    一级回血瓶, 二级回血瓶, 三级回血瓶, 四级回血瓶,
    # 装备
    头盔1级, 头盔2级, 头盔3级, 头盔4级, 头盔5级,
    盔甲1级, 盔甲2级, 盔甲3级, 盔甲4级, 盔甲5级,
    靴子1级, 靴子2级, 靴子3级, 靴子4级, 靴子5级,
    斗篷1级, 披风2级, 灵服3级, 披风4级, 腰带5级,
    # 生物
    史莱姆, 土拨鼠, 幽灵, 蝙蝠, 火焰精灵, 蘑菇怪, 岩石怪,
    猴子, 三角龙, 丧尸, 企鹅, 僵尸, 刺球, 双角骷髅, 变形怪, 可爱幽灵,
    吸血鬼, 夜魔, 大史莱姆, 奶龙, 小恶魔, 小熊猫, 小霸王龙, 小鸡, 岩浆怪,
    幽灵人, 建龙, 异变者, 异变骷髅, 异形眼, 异形球体, 异形蛇, 异形蜘蛛,
    恶魔球, 普通骷髅, 松鼠, 母鸡, 灰兔, 牧羊人, 狗, 独眼人, 狼人,
    猪, 白兔, 章鱼, 章鱼怪, 红眼粘液怪, 老虎, 萌刺, 蓝怪, 蚂蚁怪物,
    贝利亚, 超异变者, 邪恶粘液怪, 邪恶蜘蛛, 邪恶蝙蝠, 金怪, 问灵, 霸王龙,
    骷髅球, 鸟, 肥胖Boss, 死神, 死神祝福,
    # 生物蛋
    史莱姆蛋, 土拨鼠蛋, 幽灵蛋, 蝙蝠蛋, 火焰精灵蛋, 蘑菇怪蛋, 岩石怪蛋,
    猴子蛋, 三角龙蛋, 丧尸蛋, 企鹅蛋, 僵尸蛋, 刺球蛋, 双角骷髅蛋, 变形怪蛋,
    可爱幽灵蛋, 吸血鬼蛋, 夜魔蛋, 大史莱姆蛋, 奶龙蛋, 小恶魔蛋, 小熊猫蛋,
    小霸王龙蛋, 小鸡蛋, 岩浆怪蛋, 幽灵人蛋, 建龙蛋, 异变者蛋, 异变骷髅蛋,
    异形眼蛋, 异形球体蛋, 异形蛇蛋, 异形蜘蛛蛋, 恶魔球蛋, 普通骷髅蛋,
    松鼠蛋, 母鸡蛋, 灰兔蛋, 牧羊人蛋, 狗蛋, 独眼人蛋, 狼人蛋, 猪蛋, 白兔蛋,
    章鱼蛋, 章鱼怪蛋, 红眼粘液怪蛋, 老虎蛋, 萌刺蛋, 蓝怪蛋, 蚂蚁怪物蛋,
    贝利亚蛋, 超异变者蛋, 邪恶粘液怪蛋, 邪恶蜘蛛蛋, 邪恶蝙蝠蛋, 金怪蛋,
    问灵蛋, 霸王龙蛋, 骷髅球蛋, 鸟蛋, 肥胖蛋, 死神蛋, 死神祝福蛋
)

# 导入图片管理器
from 图片加载 import 图片管理器
# 导入武器处理模块
from 武器处理 import 武器技能管理器实例
from 武器处理 import handle_player_attack

# 游戏设置
宽度, 高度 = 1200, 800
方块大小 = 32

# 区块设置
CHUNK_SIZE = 64  # 区块大小（方块数）

# 出生点设置
出生点_x = 500
出生点_y = 0

# 初始化pygame（只在直接运行该文件时执行）
if __name__ == "__main__":
    pygame.init()
    pygame.font.init()  # 初始化字体模块
    
    # 加载所有音频文件
    audio_manager.load_all_audio()
    
    # 创建pygame窗口（确保在加载图片前创建）
    pygame.display.set_mode((宽度, 高度), pygame.RESIZABLE)
    
    # 现在窗口已创建，可以安全地加载图片了
    图片管理器.加载所有图片()

class DamageText:
    """伤害数字类，用于显示伤害数值"""
    def __init__(self, x, y, damage, is_player=False, color=None):
        self.x = x
        self.y = y
        self.damage = damage
        self.is_player = is_player  # 是否是玩家受到的伤害
        self.lifetime = 1.0  # 显示时间（秒）
        self.alpha = 255  # 透明度
        self.velocity_y = -2  # 向上移动速度
        self.velocity_x = random.uniform(-1, 1)  # 随机水平速度
        
        # 根据伤害类型选择颜色，如果提供了自定义颜色则使用自定义颜色
        if color:
            self.color = color  # 使用自定义颜色
        elif is_player:
            self.color = (255, 0, 0)  # 玩家受伤显示红色
        else:
            self.color = (255, 255, 0)  # 生物受伤显示黄色
    
    def update(self, dt):
        """更新伤害数字位置和透明度"""
        self.lifetime -= dt
        self.y += self.velocity_y
        self.x += self.velocity_x
        self.alpha = max(0, int(self.lifetime * 255))
    
    def is_finished(self):
        """检查是否需要移除"""
        return self.lifetime <= 0
    
    def draw(self, screen, camera_x, camera_y):
        """绘制伤害数字"""
        # 创建字体，将大小从36缩小20%变为28
        font = pygame.font.Font(None, 28)
        # 在伤害数字前面添加"-"符号
        text = font.render(f"-{self.damage}", True, self.color)
        
        # 设置透明度
        text.set_alpha(self.alpha)
        
        # 计算绘制位置
        draw_x = self.x - camera_x - text.get_width() // 2
        draw_y = self.y - camera_y - text.get_height() // 2
        
        # 绘制文字
        screen.blit(text, (draw_x, draw_y))

class Arrow:
    """箭矢类，处理箭矢的物理运动和碰撞检测"""
    def __init__(self, x, y, direction_x, direction_y, damage=10, owner=None, weapon_type='arrow'):
        self.x = x
        self.y = y
        # 记录初始位置，用于计算飞行距离
        self.initial_x = x
        self.initial_y = y
        # 根据武器类型设置不同的大小
        if weapon_type == 'bullet':
            # 子弹大小：10*10像素（减小50%）
            self.width = 10
            self.height = 10
        elif weapon_type == 'rocket_launcher':
            # 火箭发射器（救世主榴弹炮）大小：12*12像素，比默认小20%
            self.width = int(12 * 0.8)  # 9像素
            self.height = int(12 * 0.8)  # 9像素
        else:
            # 其他武器类型保持默认大小
            self.width = 12
            self.height = 6
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.damage = damage
        self.owner = owner  # 箭矢所有者，通常是玩家
        self.lifetime = 5.0  # 箭矢存在时间（秒）
        self.explosion_radius = 3  # 爆炸半径（以方块为单位）
        self.explosion_damage = 400  # 爆炸伤害
        
        # 根据武器类型设置不同的速度
        if weapon_type == 'arrow':
            # 弓箭速度：500
            speed = 500
        elif weapon_type == '弩':
            # 弩速度：400
            speed = 400
        elif weapon_type == '未来弩':
            # 未来弩速度：800
            speed = 800
        elif weapon_type == 'bullet':
            # 手枪、步枪、狙击枪使用子弹类型，根据武器名称区分速度
            speed = 800  # 默认子弹速度
            
            # 通过玩家对象的game属性获取当前手持工具
            if hasattr(owner, 'game') and owner.game:
                game = owner.game
                工具实例, 当前工具 = game.获取当前手持工具()
                if 当前工具:
                    武器名称 = 当前工具.get('名称', '')
                    if '手枪' in 武器名称:
                        # 手枪速度：800
                        speed = 800
                    elif '步枪' in 武器名称 or '齐天' in 武器名称:
                        # 步枪和齐天系列枪械速度：1000
                        speed = 1000
                    elif '狙击枪' in 武器名称:
                        # 狙击枪速度：2000
                        speed = 1200
        else:
            # 默认速度：500
            speed = 500
        
        # 计算速度向量
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
        self.mirror_y = False  # 初始化Y轴镜像标记
        
        # 尾迹效果相关属性
        self.尾迹点 = []  # 存储尾迹点的列表
        self.尾迹最大长度 = 5  # 尾迹最大点数量
        self.尾迹更新间隔 = 0.05  # 尾迹点更新间隔（秒）
        self.尾迹存在时间 = 0.5  # 尾迹点存在时间（秒）
        self.尾迹上次更新时间 = 0  # 上次更新尾迹的时间
        self.尾迹点持续时间 = []  # 每个尾迹点的持续时间
        
        # 爆炸特效相关属性
        self.is_rocket = False  # 是否为火箭弹
        self.explosion_effect = None  # 爆炸特效实例
        self.has_exploded = False  # 是否已爆炸
        
        # 五子棋子弹随机图片类型（只在初始化时选择一次）
        self.五子棋图片类型 = None
        if weapon_type == '五子棋':
            import random
            self.五子棋图片类型 = random.choice(["白字五子棋", "黑字五子棋"])
    
    def update(self, dt, world, mobs, game):
        """更新箭矢位置和状态"""
        # 减少生命周期
        self.lifetime -= dt
        
        if self.stuck:
            # 如果箭矢已插入，只更新插入时间
            self.stuck_time += dt
            return
        
        # 检查飞行距离，激光炮子弹限制600像素
        if hasattr(self, 'weapon_type') and self.weapon_type == 'laser_cannon':
            distance = math.sqrt((self.x - self.initial_x)**2 + (self.y - self.initial_y)**2)
            if distance > 600:
                self.lifetime = 0
                return
        
        # 更新尾迹效果 - 五子棋子弹无拖尾特效
        if not hasattr(self, 'weapon_type') or self.weapon_type != '五子棋':
            # 更新尾迹上次更新时间
            self.尾迹上次更新时间 += dt
            
            # 当达到更新间隔时，添加新的尾迹点
            # 标准渲染模式下调整尾迹参数，平衡长度和性能
            update_interval = self.尾迹更新间隔
            max_trail_length = self.尾迹最大长度
            
            # 获取游戏实例的特效渲染设置
            effect_setting = "标准"  # 默认标准渲染
            if hasattr(self, 'owner') and hasattr(self.owner, 'game'):
                effect_setting = getattr(self.owner.game, '特效渲染设置', "标准")
            elif hasattr(self, 'game'):
                effect_setting = getattr(self.game, '特效渲染设置', "标准")
            
            if effect_setting == "标准":
                # 标准渲染模式下：减少更新白线时间，设置为0.2秒
                update_interval = 0.2  # 0.2秒更新一次
                max_trail_length = 2# 保持5个尾迹点
            
            if self.尾迹上次更新时间 >= update_interval:
                # 计算箭矢尾部的位置，增加额外的10像素偏移
                # 箭矢长度的一半，用于计算尾部位置
                arrow_length = self.width / 2
                # 额外超出图片10像素的偏移量
                # 标准渲染模式下extra_offset为10，其他模式为30
                extra_offset = 30
                if effect_setting == "标准":
                    extra_offset = 10
                # 总偏移量 = 箭矢长度的一半 + 额外偏移量
                total_offset = arrow_length + extra_offset
                # 根据当前角度计算尾部偏移量
                tail_offset_x = -math.cos(math.radians(self.angle)) * total_offset
                tail_offset_y = -math.sin(math.radians(self.angle)) * total_offset
                # 计算尾部位置
                tail_x = self.x + tail_offset_x
                tail_y = self.y + tail_offset_y
                # 添加尾部位置作为尾迹点
                self.尾迹点.append((tail_x, tail_y))
                self.尾迹点持续时间.append(0)
                
                # 限制尾迹点数量
                if len(self.尾迹点) > max_trail_length:
                    self.尾迹点.pop(0)
                    self.尾迹点持续时间.pop(0)
                
                # 重置更新时间
                self.尾迹上次更新时间 = 0
            
            # 更新所有尾迹点的持续时间
            for i in range(len(self.尾迹点持续时间)):
                self.尾迹点持续时间[i] += dt
            
            # 删除超过存在时间的尾迹点
            while self.尾迹点持续时间 and self.尾迹点持续时间[0] >= self.尾迹存在时间:
                self.尾迹点.pop(0)
                self.尾迹点持续时间.pop(0)
        else:
            # 五子棋子弹清空尾迹点，禁用拖尾特效
            self.尾迹点 = []
            self.尾迹点持续时间 = []
        
        # 更新位置
        new_x = self.x + self.velocity_x * dt
        new_y = self.y + self.velocity_y * dt
        
        # 根据武器类型决定是否应用重力效果
        if not hasattr(self, 'weapon_type') or self.weapon_type != 'bullet' or self.weapon_type == '五子棋':
            # 根据是否为救世主榴弹炮决定重力强度
            if hasattr(self, 'is_savior_grenade') and self.is_savior_grenade:
                # 救世主榴弹炮：抛物线增强250%，重力350
                self.velocity_y += 350 * dt
            else:
                # 其他武器：默认重力100
                self.velocity_y += 100 * dt
            # 更新角度，根据当前速度向量计算，实现抛物线角度调整
            self.angle = math.degrees(math.atan2(self.velocity_y, self.velocity_x))
        # 普通子弹不应用重力，保持初始角度，实现直线飞行
        
        # 检查与世界的碰撞
        hit_block = False
        # 反弹次数计数
        if not hasattr(self, '反弹次数'):
            self.反弹次数 = 0
        
        # 先检查X方向的碰撞
        tile_x = int((new_x + self.width // 2) // 方块大小)
        tile_y = int((self.y + self.height // 2) // 方块大小)
        
        if 0 <= tile_y < world.高度 and 0 <= tile_x < world.宽度:
            block_id = world.get_block(tile_x, tile_y)
            if block_id != 空气:
                from 物品定义 import 方块属性
                if 方块属性.get(block_id, {}).get("固体", False):
                    if hasattr(self, 'weapon_type') and self.weapon_type == 'laser_cannon':
                        # 激光炮子弹破坏方块
                        world.set_block(tile_x, tile_y, 空气)
                        # 生成掉落物
                        try:
                            from 掉落物 import 掉落物管理器实例
                            掉落物管理器实例.生成掉落物(world, tile_x, tile_y, block_id)
                        except Exception as e:
                            print(f"生成掉落物失败: {e}")
                    elif hasattr(self, 'weapon_type') and self.weapon_type == '未来弩':
                        # X方向碰撞，反转X速度
                        self.velocity_x = -self.velocity_x * 0.8
                        # 重新计算旋转角度
                        self.angle = math.degrees(math.atan2(self.velocity_y, self.velocity_x))
                        self.反弹次数 += 1
                        if self.反弹次数 >= 3:
                            self.stuck = True
                            self.stuck_position = (self.x, self.y)
                            self.尾迹点 = []
                            self.尾迹点持续时间 = []
                        hit_block = True
                    else:
                        self.stuck = True
                        self.stuck_position = (self.x, self.y)
                        self.尾迹点 = []
                        self.尾迹点持续时间 = []
                        hit_block = True
        
        # 再检查Y方向的碰撞
        if not hit_block:
            tile_x = int((self.x + self.width // 2) // 方块大小)
            tile_y = int((new_y + self.height // 2) // 方块大小)
            
            if 0 <= tile_y < world.高度 and 0 <= tile_x < world.宽度:
                block_id = world.get_block(tile_x, tile_y)
                if block_id != 空气:
                    from 物品定义 import 方块属性
                    if 方块属性.get(block_id, {}).get("固体", False):
                        if hasattr(self, 'weapon_type') and self.weapon_type == 'laser_cannon':
                            # 激光炮子弹破坏方块
                            world.set_block(tile_x, tile_y, 空气)
                            # 生成掉落物
                            try:
                                from 掉落物 import 掉落物管理器实例
                                掉落物管理器实例.生成掉落物(world, tile_x, tile_y, block_id)
                            except Exception as e:
                                print(f"生成掉落物失败: {e}")
                        elif hasattr(self, 'weapon_type') and self.weapon_type == '未来弩':
                            # Y方向碰撞，反转Y速度
                            self.velocity_y = -self.velocity_y * 0.8
                            # 重新计算旋转角度
                            self.angle = math.degrees(math.atan2(self.velocity_y, self.velocity_x))
                            self.反弹次数 += 1
                            if self.反弹次数 >= 3:
                                self.stuck = True
                                self.stuck_position = (self.x, self.y)
                                self.尾迹点 = []
                                self.尾迹点持续时间 = []
                            hit_block = True
                        else:
                            self.stuck = True
                            self.stuck_position = (self.x, self.y)
                            self.尾迹点 = []
                            self.尾迹点持续时间 = []
                            hit_block = True
        
        # 检查是否超出世界边界
        if not hit_block:
            if new_x < 0 or new_x + self.width > world.宽度 * 方块大小 or \
               new_y < 0 or new_y + self.height > world.高度 * 方块大小:
                if hasattr(self, 'weapon_type') and self.weapon_type == '未来弩':
                    # 边界碰撞处理
                    if new_x < 0 or new_x + self.width > world.宽度 * 方块大小:
                        self.velocity_x = -self.velocity_x * 0.8
                    if new_y < 0 or new_y + self.height > world.高度 * 方块大小:
                        self.velocity_y = -self.velocity_y * 0.8
                    # 重新计算旋转角度
                    self.angle = math.degrees(math.atan2(self.velocity_y, self.velocity_x))
                    self.反弹次数 += 1
                    if self.反弹次数 >= 3:
                        self.stuck = True
                        self.stuck_position = (self.x, self.y)
                        self.尾迹点 = []
                        self.尾迹点持续时间 = []
                else:
                    self.stuck = True
                    self.stuck_position = (self.x, self.y)
                    self.尾迹点 = []
                    self.尾迹点持续时间 = []
                hit_block = True
        
        if not hit_block:
            # 检查与生物的碰撞
            all_mobs = mobs.copy()
            # 添加当前boss到检查列表
            try:
                from boos生物处理 import boss_manager
                if boss_manager.current_boss and boss_manager.current_boss.is_alive():
                    all_mobs.append(boss_manager.current_boss)
            except Exception as e:
                pass
            
            for mob in all_mobs:
                # 不击中自己
                if self.owner == mob:
                    continue
                
                mob_rect = pygame.Rect(mob.x, mob.y, mob.width, mob.height)
                
                # 创建箭矢的碰撞箱
                arrow_rect = pygame.Rect(new_x, new_y, self.width, self.height)
                
                if arrow_rect.colliderect(mob_rect):
                    # 箭矢击中生物
                    # 确保mob.game存在
                    mob.game = game
                    
                    # 计算子弹飞行距离
                    distance = math.sqrt((new_x - self.initial_x)**2 + (new_y - self.initial_y)**2)
                    
                    # 根据武器类型和距离调整伤害
                    adjusted_damage = self.damage
                    
                    # 检查是否为冲锋枪子弹
                    if self.weapon_type == 'bullet' and hasattr(self.owner, 'game') and self.owner.game:
                        game = self.owner.game
                        工具实例, 当前工具 = game.获取当前手持工具()
                        if 当前工具 and '冲锋枪' in 当前工具.get('名称', ''):
                            # 冲锋枪：9格内（约144像素）13伤害，9格外6伤害
                            nine_grid_pixels = 9 * 16  # 假设每格16像素
                            if distance > nine_grid_pixels:
                                adjusted_damage = 6
                            else:
                                adjusted_damage = 13
                    
                    # 调用take_damage方法，创建伤害数字
                    死亡 = mob.take_damage(adjusted_damage)
                    # 创建伤害文本
                    game.damage_texts.append(DamageText(mob.x + mob.width // 2, mob.y - 10, adjusted_damage))
                    # 播放击中生物的音效
                    from 音频输出 import audio_manager
                    audio_manager.play_sound("受击1")
                    
                    # 如果生物死亡，生成掉落物和经验
                    if 死亡:
                        # 根据生物掉落物配置生成掉落物
                        try:
                            from 掉落物 import 掉落物管理器实例
                            from 生物系统 import 生物掉落物配置
                            掉落物管理器实例.生成生物掉落物(world, 
                                                           int(mob.x // 方块大小), 
                                                           int(mob.y // 方块大小), 
                                                           mob.name, 
                                                           getattr(mob, 'mob_id', 0), 
                                                           生物掉落物配置)
                        except Exception as e:
                            print(f"生成生物掉落物失败: {e}")
                            # 备用方案
                            from 物品定义 import 肉块
                            world.spawn_item(int(mob.x // 方块大小), int(mob.y // 方块大小), 肉块, random.randint(1, 3))
                        # 生成经验球
                        if hasattr(self.owner, 'game'):
                            self.owner.game.spawn_exp_orbs(mob.x // 方块大小, mob.y // 方块大小)
                    
                    self.lifetime = 0  # 箭矢消失
                    break
            
            # 检查与吸血鬼召唤生物的碰撞
            for mob in mobs:
                # 只处理吸血鬼的召唤生物
                if hasattr(mob, 'mob_id') and mob.mob_id == 20016:  # 20016是吸血鬼的ID
                    # 检查邪恶蝙蝠
                    if hasattr(mob, 'summoned_bats'):
                        for bat in mob.summoned_bats[:]:
                            bat_rect = pygame.Rect(bat['x'], bat['y'], bat['width'], bat['height'])
                            if arrow_rect.colliderect(bat_rect):
                                # 击中邪恶蝙蝠，减少血量
                                bat['health'] -= self.damage
                                if bat['health'] <= 0:
                                    # 蝙蝠死亡，移除
                                    mob.summoned_bats.remove(bat)
                                self.lifetime = 0  # 箭矢消失
                                break
                    
                    # 检查治愈蝙蝠
                    if hasattr(mob, 'healing_bats'):
                        for bat in mob.healing_bats[:]:
                            bat_rect = pygame.Rect(bat['x'], bat['y'], bat['width'], bat['height'])
                            if arrow_rect.colliderect(bat_rect):
                                # 击中治愈蝙蝠，减少血量
                                bat['health'] -= self.damage
                                if bat['health'] <= 0:
                                    # 蝙蝠死亡，移除
                                    mob.healing_bats.remove(bat)
                                self.lifetime = 0  # 箭矢消失
                                break
                    
                    # 检查刺球
                    if hasattr(mob, 'spike_balls'):
                        for ball in mob.spike_balls[:]:
                            ball_rect = pygame.Rect(ball['x'], ball['y'], ball['width'], ball['height'])
                            if arrow_rect.colliderect(ball_rect):
                                # 击中刺球，减少血量
                                ball['health'] -= self.damage
                                if ball['health'] <= 0:
                                    # 刺球死亡，移除
                                    mob.spike_balls.remove(ball)
                                self.lifetime = 0  # 箭矢消失
                                break
                    
                    # 检查异变骷髅
                    if hasattr(mob, 'mutant_skulls'):
                        for skull in mob.mutant_skulls[:]:
                            skull_rect = pygame.Rect(skull['x'], skull['y'], skull['width'], skull['height'])
                            if arrow_rect.colliderect(skull_rect):
                                # 击中异变骷髅，减少血量
                                skull['health'] -= self.damage
                                if skull['health'] <= 0:
                                    # 骷髅死亡，移除
                                    mob.mutant_skulls.remove(skull)
                                self.lifetime = 0  # 箭矢消失
                                break
                    
                    # 检查死神召唤的幽灵
                    if hasattr(mob, 'summoned_souls'):
                        for soul in mob.summoned_souls[:]:
                            soul_rect = pygame.Rect(soul['x'], soul['y'], soul['width'], soul['height'])
                            if arrow_rect.colliderect(soul_rect):
                                # 击中幽灵，减少血量
                                soul['health'] -= self.damage
                                if soul['health'] <= 0:
                                    # 幽灵死亡，移除
                                    mob.summoned_souls.remove(soul)
                                self.lifetime = 0  # 箭矢消失
                                break
                    
                    # 如果箭矢已经消失，跳出循环
                    if self.lifetime <= 0:
                        break
        
        if not self.stuck and not hit_block:
            # 没有击中任何物体，更新位置
            self.x = new_x
            self.y = new_y
            self.rect.x = self.x
            self.rect.y = self.y
        
        # 检查是否需要爆炸（火箭弹击中目标或生命周期结束）
        if self.is_rocket and not self.has_exploded:
            if self.stuck or self.lifetime <= 0:
                # 触发爆炸
                self.explode(world, mobs, game)
                self.has_exploded = True
                self.lifetime = 0  # 爆炸后销毁火箭弹
    
    def explode(self, world, mobs, game):
        """实现爆炸效果"""
        import math
        
        # 计算爆炸中心坐标
        explode_x = self.x + self.width // 2
        explode_y = self.y + self.height // 2
        
        # 获取爆炸半径
        radius = self.explosion_radius
        
        # 1. 破坏爆炸范围内的方块
        # 确保radius为整数，避免range()函数出错
        radius_int = int(radius)
        for dx in range(-radius_int, radius_int + 1):
            for dy in range(-radius_int, radius_int + 1):
                # 计算距离，实现圆形爆炸范围
                distance = math.sqrt(dx*dx + dy*dy)
                if distance <= radius:
                    tile_x = int(explode_x // 方块大小) + dx
                    tile_y = int(explode_y // 方块大小) + dy
                    
                    # 检查方块是否在世界范围内
                    if 0 <= tile_y < world.高度 and 0 <= tile_x < world.宽度:
                        block_id = world.get_block(tile_x, tile_y)
                        if block_id != 空气:
                            # 破坏方块
                            world.set_block(tile_x, tile_y, 空气)
                            # 生成掉落物
                            try:
                                from 掉落物 import 掉落物管理器实例
                                掉落物管理器实例.生成掉落物(world, tile_x, tile_y, block_id)
                            except Exception as e:
                                print(f"生成掉落物失败: {e}")
        
        # 2. 伤害爆炸范围内的生物
        all_mobs = mobs.copy()
        # 添加当前boss到检查列表
        try:
            from boos生物处理 import boss_manager
            if boss_manager.current_boss and boss_manager.current_boss.is_alive():
                all_mobs.append(boss_manager.current_boss)
        except Exception as e:
            pass
        
        for mob in all_mobs:
            mob_center_x = mob.x + mob.width // 2
            mob_center_y = mob.y + mob.height // 2
            
            # 计算生物到爆炸中心的距离
            distance = math.sqrt((mob_center_x - explode_x)**2 + (mob_center_y - explode_y)**2)
            
            if distance <= radius * 方块大小:
                # 根据距离计算伤害（中心伤害最高，边缘最低）
                damage_multiplier = max(0.3, 1 - (distance / (radius * 方块大小)))
                final_damage = int(self.explosion_damage * damage_multiplier)
                
                # 伤害生物
                mob.game = game
                死亡 = mob.take_damage(final_damage)
                # 创建伤害文本
                game.damage_texts.append(DamageText(mob.x + mob.width // 2, mob.y - 10, final_damage))
                
                # 如果生物死亡，生成掉落物和经验
                if 死亡:
                    # 根据生物掉落物配置生成掉落物
                    try:
                        from 掉落物 import 掉落物管理器实例
                        from 生物系统 import 生物掉落物配置
                        掉落物管理器实例.生成生物掉落物(world, 
                                                       int(mob.x // 方块大小), 
                                                       int(mob.y // 方块大小), 
                                                       mob.name, 
                                                       getattr(mob, 'mob_id', 0), 
                                                       生物掉落物配置)
                    except Exception as e:
                        print(f"生成生物掉落物失败: {e}")
                        # 备用方案
                        from 物品定义 import 肉块
                        world.spawn_item(int(mob.x // 方块大小), int(mob.y // 方块大小), 肉块, random.randint(1, 3))
                    # 生成经验球
                    game.spawn_exp_orbs(mob.x // 方块大小, mob.y // 方块大小)
            
            # 检查吸血鬼召唤生物是否在爆炸范围内
            if hasattr(mob, 'mob_id') and mob.mob_id == 20016:  # 20016是吸血鬼的ID
                # 检查邪恶蝙蝠
                if hasattr(mob, 'summoned_bats'):
                    for bat in mob.summoned_bats[:]:
                        bat_center_x = bat['x'] + bat['width'] // 2
                        bat_center_y = bat['y'] + bat['height'] // 2
                        distance = math.sqrt((bat_center_x - explode_x)**2 + (bat_center_y - explode_y)**2)
                        
                        if distance <= radius * 方块大小:
                            # 根据距离计算伤害
                            damage_multiplier = max(0.3, 1 - (distance / (radius * 方块大小)))
                            final_damage = int(self.explosion_damage * damage_multiplier)
                            
                            # 伤害蝙蝠
                            bat['health'] -= final_damage
                            if bat['health'] <= 0:
                                # 蝙蝠死亡，移除
                                mob.summoned_bats.remove(bat)
                
                # 检查治愈蝙蝠
                if hasattr(mob, 'healing_bats'):
                    for bat in mob.healing_bats[:]:
                        bat_center_x = bat['x'] + bat['width'] // 2
                        bat_center_y = bat['y'] + bat['height'] // 2
                        distance = math.sqrt((bat_center_x - explode_x)**2 + (bat_center_y - explode_y)**2)
                        
                        if distance <= radius * 方块大小:
                            # 根据距离计算伤害
                            damage_multiplier = max(0.3, 1 - (distance / (radius * 方块大小)))
                            final_damage = int(self.explosion_damage * damage_multiplier)
                            
                            # 伤害蝙蝠
                            bat['health'] -= final_damage
                            if bat['health'] <= 0:
                                # 蝙蝠死亡，移除
                                mob.healing_bats.remove(bat)
                
                # 检查刺球
                if hasattr(mob, 'spike_balls'):
                    for ball in mob.spike_balls[:]:
                        ball_center_x = ball['x'] + ball['width'] // 2
                        ball_center_y = ball['y'] + ball['height'] // 2
                        distance = math.sqrt((ball_center_x - explode_x)**2 + (ball_center_y - explode_y)**2)
                        
                        if distance <= radius * 方块大小:
                            # 根据距离计算伤害
                            damage_multiplier = max(0.3, 1 - (distance / (radius * 方块大小)))
                            final_damage = int(self.explosion_damage * damage_multiplier)
                            
                            # 伤害刺球
                            ball['health'] -= final_damage
                            if ball['health'] <= 0:
                                # 刺球死亡，移除
                                mob.spike_balls.remove(ball)
                
                # 检查异变骷髅
                if hasattr(mob, 'mutant_skulls'):
                    for skull in mob.mutant_skulls[:]:
                        skull_center_x = skull['x'] + skull['width'] // 2
                        skull_center_y = skull['y'] + skull['height'] // 2
                        distance = math.sqrt((skull_center_x - explode_x)**2 + (skull_center_y - explode_y)**2)
                        
                        if distance <= radius * 方块大小:
                            # 根据距离计算伤害
                            damage_multiplier = max(0.3, 1 - (distance / (radius * 方块大小)))
                            final_damage = int(self.explosion_damage * damage_multiplier)
                            
                            # 伤害骷髅
                            skull['health'] -= final_damage
                            if skull['health'] <= 0:
                                # 骷髅死亡，移除
                                mob.mutant_skulls.remove(skull)
        
        # 3. 创建爆炸特效
        class ExplosionEffect:
            def __init__(self, x, y, radius, game):
                self.x = x
                self.y = y
                self.radius = radius
                self.game = game
                self.lifetime = 0.5  # 爆炸效果持续时间
                self.frame = 0  # 用于动画效果
                
                # 获取特效渲染设置
                self.effect_setting = getattr(game, '特效渲染设置', "标准")
            
            def update(self, dt):
                self.lifetime -= dt
                self.frame += dt * 20  # 动画播放速度
                return self.lifetime <= 0
            
            def draw(self, screen, camera_x, camera_y):
                # 计算屏幕坐标
                screen_x = self.x - camera_x
                screen_y = self.y - camera_y
                
                # 根据特效设置绘制不同效果
                if self.effect_setting == "最佳":
                    # 最佳特效：多层彩色爆炸效果
                    import random
                    
                    # 绘制外层火焰环
                    for i in range(3):
                        current_radius = int(self.radius * 方块大小 * (0.5 + (self.frame % 10) / 10))
                        color = [(255, 0, 0), (255, 165, 0), (255, 255, 0)][i]
                        alpha = 255 - int((self.frame % 10) * 25)
                        
                        # 创建带透明度的表面
                        explosion_surface = pygame.Surface((current_radius * 2, current_radius * 2), pygame.SRCALPHA)
                        pygame.draw.circle(explosion_surface, (*color, alpha), (current_radius, current_radius), current_radius)
                        screen.blit(explosion_surface, (screen_x - current_radius, screen_y - current_radius))
                    
                    # 添加火花效果
                    for _ in range(10):
                        spark_angle = random.uniform(0, 2 * math.pi)
                        spark_distance = random.uniform(0, self.radius * 方块大小)
                        spark_x = screen_x + math.cos(spark_angle) * spark_distance
                        spark_y = screen_y + math.sin(spark_angle) * spark_distance
                        spark_size = random.randint(1, 3)
                        spark_color = (255, 255, 255)
                        pygame.draw.circle(screen, spark_color, (int(spark_x), int(spark_y)), spark_size)
                
                elif self.effect_setting == "标准":
                    # 标准特效：升级为动态脉冲爆炸效果
                    import random
                    current_radius = int(self.radius * 方块大小 * (0.5 + (self.frame % 10) / 10))
                    
                    # 绘制主爆炸圈，使用渐变效果
                    for i in range(3):
                        # 从中心向外的三层不同粗细和透明度的圆环
                        ring_radius = current_radius * (0.7 + i * 0.15)
                        # 确保alpha值在0-255范围内
                        alpha = max(0, 200 - int((self.frame % 10) * 15) - i * 30)
                        ring_width = 3 - i
                        
                        # 使用橙红色渐变
                        if i == 0:
                            color = (255, 50, 0)
                        elif i == 1:
                            color = (255, 100, 0)
                        else:
                            color = (255, 150, 0)
                        
                        pygame.draw.circle(screen, (*color, alpha), (int(screen_x), int(screen_y)), int(ring_radius), ring_width)
                    
                    # 添加简单的火花效果，增强视觉冲击力
                    for _ in range(5):
                        spark_angle = random.uniform(0, 2 * math.pi)
                        spark_distance = random.uniform(0, current_radius * 0.8)
                        spark_x = screen_x + math.cos(spark_angle) * spark_distance
                        spark_y = screen_y + math.sin(spark_angle) * spark_distance
                        spark_size = random.randint(1, 2)
                        spark_color = (255, 200, 100)
                        pygame.draw.circle(screen, spark_color, (int(spark_x), int(spark_y)), spark_size)
                
                else:  # 关闭特效
                    # 关闭特效：升级为简洁的动态波纹效果
                    current_radius = int(self.radius * 方块大小)
                    
                    # 绘制扩散的波纹效果
                    for i in range(2):
                        # 两个向外扩散的圆环
                        wave_radius = int(current_radius * (0.6 + i * 0.2 + (self.frame % 10) / 50))
                        # 确保alpha值在0-255范围内
                        alpha = max(0, 150 - int((self.frame % 10) * 15) - i * 50)
                        
                        # 使用深灰色调，保持简洁但有层次感
                        if i == 0:
                            color = (150, 150, 150)
                        else:
                            color = (100, 100, 100)
                        
                        pygame.draw.circle(screen, (*color, alpha), (int(screen_x), int(screen_y)), wave_radius, 1)
                    
                    # 中心添加一个简单的白色亮点
                    center_radius = int(current_radius * 0.1)
                    # 确保alpha值在0-255范围内
                    center_alpha = max(0, 200 - int((self.frame % 10) * 20))
                    pygame.draw.circle(screen, (255, 255, 255, center_alpha), (int(screen_x), int(screen_y)), center_radius)
        
        # 创建爆炸特效实例并添加到游戏中
        explosion = ExplosionEffect(explode_x, explode_y, radius, game)
        if not hasattr(game, 'explosion_effects'):
            game.explosion_effects = []
        game.explosion_effects.append(explosion)
        
        # 播放爆炸音效
        from 音频输出 import audio_manager
        try:
            audio_manager.play_sound("爆炸")
        except Exception as e:
            print(f"播放爆炸音效失败: {e}")
    
    def is_finished(self):
        """检查箭矢是否应被移除"""
        # 子弹击中方块后直接消失，不需要停留
        if hasattr(self, 'weapon_type') and self.weapon_type == 'bullet' and self.stuck:
            return True
        return self.lifetime <= 0 or (self.stuck and self.stuck_time > 2.0)
    
    def draw(self, screen, camera_x, camera_y):
        """绘制箭矢"""
        # 激光炮绘制粗白线
        if hasattr(self, 'weapon_type') and self.weapon_type == 'laser_cannon':
            # 绘制从初始位置到当前位置的粗白线
            screen_x1 = self.initial_x - camera_x
            screen_y1 = self.initial_y - camera_y
            screen_x2 = self.x - camera_x
            screen_y2 = self.y - camera_y
            # 绘制5像素宽的白色激光线
            pygame.draw.line(screen, (255, 255, 255), 
                           (screen_x1, screen_y1), (screen_x2, screen_y2), 5)
            return
            
        # 绘制尾迹效果 - 根据特效渲染设置
        # 获取游戏实例的特效渲染设置
        effect_setting = "标准"  # 默认标准渲染
        if hasattr(self, 'owner') and hasattr(self.owner, 'game'):
            effect_setting = getattr(self.owner.game, '特效渲染设置', "标准")
        elif hasattr(self, 'game'):
            effect_setting = getattr(self.game, '特效渲染设置', "标准")
        
        # 根据特效渲染设置决定是否绘制尾迹以及绘制方式
        if effect_setting != "关闭" and len(self.尾迹点) >= 2:
            # 创建尾迹表面，支持透明度
            trail_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            
            # 绘制连续的尾迹线
            if effect_setting == "标准":
                # 标准渲染：单独设计，绘制所有尾迹线，但降低透明度和线宽
                for i in range(len(self.尾迹点) - 1):
                    # 获取当前和下一个尾迹点
                    x1, y1 = self.尾迹点[i]
                    x2, y2 = self.尾迹点[i+1]
                    
                    # 转换为屏幕坐标
                    screen_x1 = x1 - camera_x
                    screen_y1 = y1 - camera_y
                    screen_x2 = x2 - camera_x
                    screen_y2 = y2 - camera_y
                    
                    # 计算透明度（根据尾迹点的持续时间，越旧的点越透明）
                    alpha = 255 - int((self.尾迹点持续时间[i] / self.尾迹存在时间) * 255)
                    # 标准渲染模式下固定透明度为100%
                    alpha = 255  # 标准渲染模式下透明度固定为100%
                    
                    # 绘制白色尾迹线，标准渲染模式下线宽为1
                    pygame.draw.line(trail_surface, (255, 255, 255, alpha), 
                                   (screen_x1, screen_y1), (screen_x2, screen_y2), 1)
            else:
                # 最佳渲染模式：绘制所有尾迹线
                for i in range(len(self.尾迹点) - 1):
                    # 获取当前和下一个尾迹点
                    x1, y1 = self.尾迹点[i]
                    x2, y2 = self.尾迹点[i+1]
                    
                    # 转换为屏幕坐标
                    screen_x1 = x1 - camera_x
                    screen_y1 = y1 - camera_y
                    screen_x2 = x2 - camera_x
                    screen_y2 = y2 - camera_y
                    
                    # 计算透明度（根据尾迹点的持续时间，越旧的点越透明）
                    alpha = 255 - int((self.尾迹点持续时间[i] / self.尾迹存在时间) * 255)
                    
                    # 绘制白色尾迹线
                    pygame.draw.line(trail_surface, (255, 255, 255, alpha), 
                                   (screen_x1, screen_y1), (screen_x2, screen_y2), 2)
            
            # 将尾迹表面绘制到屏幕上
            screen.blit(trail_surface, (0, 0))
        
        # 计算屏幕位置
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # 使用图片管理器加载木箭发射图片
        from 图片加载 import 图片管理器
        
        # 检查是否有所有者和选中的武器
        use_texture = False
        
        # 五子棋武器特殊处理
        if hasattr(self, 'weapon_type') and self.weapon_type == '五子棋':
            # 为五子棋子弹设置20*20像素大小
            self.width = 20
            self.height = 20
            
            # 使用初始化时选择的图片类型
            arrow_texture = self.五子棋图片类型
            
            if 图片管理器.图片是否已加载(arrow_texture):
                # 获取原始图片
                original_image = 图片管理器.获取图片(arrow_texture)
                
                # 五子棋子弹使用1:1缩放，保持20*20像素大小
                scaled_width = 20
                scaled_height = 20
                scaled_image = pygame.transform.scale(original_image, (scaled_width, scaled_height))
                
                # 五子棋子弹不旋转，保持原始方向
                image_rect = scaled_image.get_rect(center=(screen_x + self.width // 2, screen_y + self.height // 2))
                screen.blit(scaled_image, image_rect.topleft)
                use_texture = True
            else:
                # 如果图片未加载，使用初始化时选择的颜色绘制圆形
                circle_color = (255, 255, 255) if self.五子棋图片类型 == "白字五子棋" else (0, 0, 0)
                pygame.draw.circle(screen, circle_color, (int(screen_x + self.width // 2), int(screen_y + self.height // 2)), 10)
                use_texture = True
        else:
            # 根据武器类型选择正确的发射纹理
            arrow_texture = "木箭发射"
            if hasattr(self, 'weapon_type'):
                if self.weapon_type == 'bullet':
                    # 检查是否是齐天系列武器
                    is_qitian_weapon = False
                    # 检查是否是机甲系列武器或特殊武器
                    is_mecha_weapon = False
                    is_savior_weapon = False
                    if hasattr(self.owner, 'game') and self.owner.game:
                        工具实例, 当前工具 = self.owner.game.获取当前手持工具()
                        if 当前工具 and '齐天' in 当前工具.get('名称', ''):
                            is_qitian_weapon = True
                        if 当前工具 and '机甲' in 当前工具.get('名称', ''):
                            is_mecha_weapon = True
                        if 当前工具 and '救世主' in 当前工具.get('名称', ''):
                            is_savior_weapon = True
                    # 机甲系列武器使用机甲弹发射.png
                    if is_mecha_weapon:
                        arrow_texture = "机甲弹发射"
                    # 齐天系列武器使用15子弹橙.png
                    elif is_qitian_weapon:
                        arrow_texture = "15子弹橙"
                    # 所有救世主系列武器使用11子弹橙.png
                    elif is_savior_weapon:
                        arrow_texture = "11子弹橙"
                    # 普通枪械使用子弹发射.png
                    else:
                        arrow_texture = "子弹发射"
                elif self.weapon_type == 'arrow':
                    # 检查是否是救世主弩
                    is_savior_crossbow = False
                    if hasattr(self.owner, 'game') and self.owner.game:
                        工具实例, 当前工具 = self.owner.game.获取当前手持工具()
                        if 当前工具 and '救世主弩' in 当前工具.get('名称', ''):
                            is_savior_crossbow = True
                    # 救世主弩使用22箭橙.png
                    if is_savior_crossbow:
                        arrow_texture = "22箭橙"
                    else:
                        arrow_texture = "木箭发射"
                elif self.weapon_type == '未来弩':
                    arrow_texture = "木箭发射"
                elif self.weapon_type == 'rocket_launcher':
                    arrow_texture = "火箭弹发射"
            if 图片管理器.图片是否已加载(arrow_texture):
                # 获取原始图片
                original_image = 图片管理器.获取图片(arrow_texture)
                
                # 根据武器类型设置缩放比例
                scale_factor = 5
                if hasattr(self, 'weapon_type') and self.weapon_type == 'bullet':
                    scale_factor = 2.5  # 子弹缩小50%
                scaled_width = int(self.width * scale_factor)
                scaled_height = int(self.height * scale_factor)
                scaled_image = pygame.transform.scale(original_image, (scaled_width, scaled_height))
                
                # 如果需要上下镜像反转
                if hasattr(self, 'mirror_y') and self.mirror_y:
                    scaled_image = pygame.transform.flip(scaled_image, False, True)
                
                # 然后旋转缩放后的图片
                rotated_image = pygame.transform.rotate(scaled_image, -self.angle)
                image_rect = rotated_image.get_rect(center=(screen_x + self.width // 2, screen_y + self.height // 2))
                screen.blit(rotated_image, image_rect.topleft)
                use_texture = True
            
            # 如果没有使用纹理图片，则使用默认矩形绘制
            if not use_texture:
                # 创建一个简单的箭矢图形
                arrow_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                pygame.draw.rect(arrow_surface, (139, 69, 19), (0, 0, self.width, self.height))  # 棕色箭矢
                
                # 旋转箭矢
                rotated_surface = pygame.transform.rotate(arrow_surface, -self.angle)
                rotated_rect = rotated_surface.get_rect(center=(self.x - camera_x + self.width // 2, 
                                                               self.y - camera_y + self.height // 2))
                
                screen.blit(rotated_surface, rotated_rect.topleft)

from 图片加载 import 图片管理器

# 导入掉落物管理器并同步方块属性
from 掉落物 import 掉落物管理器实例, 从方块属性同步掉落物
# 同步方块属性到掉落物管理器
从方块属性同步掉落物(方块属性)

# 颜色定义
天空_白天 = (135, 206, 235)
天空_夜晚 = (25, 25, 112)
草地_绿 = (60, 180, 75)
泥土_棕 = (139, 69, 19)
石头_灰 = (105, 105, 105)
木头_棕 = (150, 75, 0)
树叶_绿 = (34, 139, 34)
水_蓝 = (65, 105, 225)
玩家_皮肤 = (240, 184, 160)
玩家_衬衫 = (220, 20, 60)
玩家_裤子 = (30, 144, 255)

class Player:
    """玩家类 - 核心移动功能"""
    
    def __init__(self, 坐标_x, 坐标_y, 世界宽度, 世界高度, 目标帧率=60, game=None):
        self.game = game  # 引用Game实例，用于访问当前选中格子和背包管理器
        self.坐标_x = 坐标_x
        self.坐标_y = 坐标_y
        self.宽 = 28
        self.高 = 56
        self.速度_x = 0
        self.速度_y = 0
        self.移动速度 = 5
        # 根据不同帧率设置不同的跳跃力度
        if 目标帧率 == 60:
            self.跳跃力度 = -10  # 60帧时跳跃力度为-10
        elif 目标帧率 in (120, 240):
            self.跳跃力度 = -13  # 120帧和240帧时跳跃力度为-13
        self.在地面上 = False
        self.朝向右 = True
        self.世界宽度 = 世界宽度
        self.世界高度 = 世界高度
        self.目标帧率 = 目标帧率  # 存储目标帧率用于调整物理参数
        # 加载角色外观设置
        self.角色外观 = 1  # 默认外观
        self.加载外观设置()
        # 角色图片缓存
        self.角色图片 = {}
        self.跳跃图片计时器 = 0  # 跳跃图片显示计时器
        self.需要使用跳跃图片 = False
        self.空格上次按下 = False  # 记录上次空格状态
        self.正在行走 = False  # 记录是否正在行走
        # 添加下落高度记录
        self.下落起始位置 = 0  # 记录开始下落时的y坐标
        self.方块大小 = 32  # 方块大小，用于计算下落高度
        # 水相关状态
        self.在水中 = False  # 玩家是否在水中
        self.上一帧在水中 = False  # 上一帧是否在水中，用于检测离开水的瞬间
        self.在水附近 = False  # 玩家是否在水方块附近
        # Star系统相关属性
        self.star_count = 0  # star数量
        self.star_progress = 0  # star进度(0-100)
        # 待机图片相关属性
        self.移动或跳跃时间 = 0  # 记录玩家移动或跳跃后的时间
        self.是否在移动或跳跃 = False  # 记录玩家是否在移动或跳跃
        self.需要使用待机图片 = False  # 是否需要使用待机图片
        # 冲刺相关属性
        self.正在冲刺 = False  # 记录玩家是否正在冲刺
        self.冲刺计时器 = 0  # 冲刺持续时间计时器
        self.冲刺持续时间 = 0.15  # 冲刺持续时间（秒）- 调整为适合80速度的持续时间
        
        # 生命值和饥饿值系统
        self.base_max_health = 100  # 本命生命值
        self.equipment_health = 0  # 装备生命值
        self.upgrade_health = 0  # 升级生命值
        self.max_health = self.base_max_health + self.equipment_health + self.upgrade_health  # 总生命值
        self.current_health = self.max_health  # 当前生命值
        self.max_hunger = 100  # 最大饥饿值
        self.current_hunger = 100  # 当前饥饿值
        self.extra_health = 0  # 额外生命值
        self.max_extra_health = 100  # 额外生命值参考最大值，用于进度条显示，实际无上限
        self.曾经最大额外生命值 = 0  # 曾经获得的最大额外生命值，用于进度条最大值
        # 护盾系统
        self.current_shield = 0  # 当前护盾值
        self.max_shield = 100  # 最大护盾值
        
        # 装备属性
        self.equipment_attack = 0  # 装备攻击力
        self.equipment_defense = 0  # 装备防御力
        self.equipment_speed = 0  # 装备移速
        self.equipment_jump = 0  # 装备跳跃力
        self.equipment_fall_safety = 0  # 装备摔落安全格数
        self.upgrade_fall_safety = 0  # 属性提升带来的摔落安全格数
        
        # 防御属性
        self.base_defense = 0  # 基础防御力
        self.upgrade_defense = 0  # 属性提升带来的防御力
        
        # 飞行模式
        self.fly_mode = False  # 飞行模式状态，默认关闭
        
        # 饥饿值减少计时器（游戏时间小时）
        self.hunger_timer = 0  # 单位：秒
        self.hunger_reduction_interval = 10  # 饥饿值减少间隔（秒），缩短为10秒以便明显观察
        
        # 饥饿值恢复生命值计时器
        self.health_regen_timer = 0  # 单位：秒
        self.health_regen_interval = 1  # 恢复间隔（秒）
        
        # 丢弃物品计时器 - 用于限制按G键丢弃物品的频率
        self.drop_item_timer = 0  # 单位：秒
        self.drop_item_interval = 0.2  # 丢弃间隔（秒）
        
        # 攻击力属性
        self.base_attack = 5  # 玩家默认攻击力
        
        # 近战攻击间隔相关属性
        self.近战攻击间隔 = 0.4  # 近战攻击间隔，单位：秒
        self.上次攻击时间 = 0  # 上次攻击时间，单位：秒
        
        # 受伤和攻击动画相关属性
        self.正在受伤 = False  # 标记是否正在受伤，用于播放受伤动画
        self.正在攻击 = False  # 标记是否正在攻击，用于播放攻击动画
        self.受伤动画时间 = 0  # 受伤动画持续时间，单位：秒
        # 齐天金箍棒形态属性
        self.齐天金箍棒形态 = 0  # 齐天金箍棒当前形态，默认0（正常形态）
        self.攻击动画时间 = 0  # 攻击动画持续时间，单位：秒
        self.受伤动画持续时间 = 0.5  # 受伤动画总持续时间，单位：秒
        self.攻击动画持续时间 = 0.3  # 攻击动画总持续时间，单位：秒
        
        self.load角色图片()
    
    def move(self, 世界, 时间增量):
        """移动玩家并处理碰撞 - 优化版"""
        # 飞行模式下不应用重力
        if self.fly_mode:
            重力 = 0
        else:
            # 重力设置：默认1，不再与帧率绑定
            if hasattr(self, '重力值'):
                # 确保重力值不低于最小值0.1
                重力 = max(0.1, self.重力值)
            else:
                # 如果没有重力值属性，使用默认值1
                重力 = 1
        
        # 记录是否正在下落
        正在下落 = self.速度_y > 0 and not self.在地面上
        
        # 记录下落起始位置（当开始下落时）
        if not self.在地面上 and self.速度_y > 0 and self.下落起始位置 == 0:
            self.下落起始位置 = self.坐标_y
        
        # 如果在地面上，重置下落起始位置
        if self.在地面上:
            self.下落起始位置 = 0
        
        if not self.在地面上:
            self.速度_y += 重力
        
        # 限制最大下落速度
        最大下落速度 = 10
        self.速度_y = min(self.速度_y, 最大下落速度)
        
        # 小步移动以避免碰撞穿透
        水平移动量 = self.速度_x * 时间增量 * 60
        小步大小 = min(abs(水平移动量), 2)  # 水平小步大小
        步数 = max(1, int(abs(水平移动量) / 小步大小) if 小步大小 > 0 else 1)
        
        # 分步处理水平移动
        水平移动成功 = True
        for i in range(步数):
            移动方向 = 1 if 水平移动量 > 0 else -1
            小步dx = 移动方向 * min(小步大小, abs(水平移动量) - i * 小步大小)
            新坐标_x = self.坐标_x + 小步dx
            
            # 检查水平碰撞
            if not self.check_collision(新坐标_x, self.坐标_y, 世界):
                self.坐标_x = 新坐标_x
            else:
                # 碰到方块，停止水平移动
                水平移动成功 = False
                break
        
        # 垂直移动也使用小步移动
        垂直移动量 = self.速度_y * 时间增量 * 60
        垂直小步大小 = min(abs(垂直移动量), 2)  # 垂直小步大小
        垂直步数 = max(1, int(abs(垂直移动量) / 垂直小步大小) if 垂直小步大小 > 0 else 1)
        
        碰撞 = False
        for i in range(垂直步数):
            移动方向 = 1 if 垂直移动量 > 0 else -1
            小步dy = 移动方向 * min(垂直小步大小, abs(垂直移动量) - i * 垂直小步大小)
            新坐标_y = self.坐标_y + 小步dy
            
            if not self.check_collision(self.坐标_x, 新坐标_y, 世界):
                self.坐标_y = 新坐标_y
            else:
                碰撞 = True
                break
        
        if not 碰撞:
            self.在地面上 = False
        else:
            if self.速度_y > 0:
                # 计算下落高度（以方块数为单位）
                下落高度 = 0
                if self.下落起始位置 > 0:
                    下落高度 = (self.坐标_y - self.下落起始位置) / self.方块大小
                
                # 处理摔落伤害和音效
                # 计算实际触发伤害的高度：5格 + 装备提供的摔落安全格数 + 属性提升带来的摔落安全格数
                总摔落安全格数 = self.equipment_fall_safety + self.upgrade_fall_safety
                触发伤害高度 = 5 - 总摔落安全格数
                if 正在下落 and 下落高度 >= 触发伤害高度:
                    # 计算伤害：(实际下落高度 - 4 - 总摔落安全格数) * 5
                    伤害值 = int((下落高度 - 4 - 总摔落安全格数) * 5)
                    # 确保伤害值不小于0
                    伤害值 = max(0, 伤害值)
                    # 使用take_damage方法处理伤害，自动处理无敌状态和额外生命值
                    self.take_damage(伤害值)
                    
                    # 播放跌落音效
                    try:
                        audio_manager.play_sound("跌落")
                    except:
                        pass
                
                self.在地面上 = True
                self.下落起始位置 = 0  # 重置下落起始位置
            self.速度_y = 0
        
        # 斜向移动脱困 - 当斜向移动被卡住时，尝试单独移动水平或垂直方向
        if not 水平移动成功 and self.在地面上 and abs(self.速度_x) > 0:
            # 尝试向上微调以脱困
            if not self.check_collision(self.坐标_x, self.坐标_y - 1, 世界):
                self.坐标_y -= 1  # 向上微调1像素
        
        # 边界检查 - 限制玩家在世界范围内
        # 限制x坐标不小于0
        if self.坐标_x < 0:
            self.坐标_x = 0
        
        # 限制x坐标不大于世界宽度
        世界宽度_像素 = self.世界宽度 * 方块大小
        if self.坐标_x > 世界宽度_像素:
            self.坐标_x = 世界宽度_像素
        
        # 限制y坐标不小于0
        if self.坐标_y < 0:
            self.坐标_y = 0
        
        # 当玩家y坐标超过世界高度+3时，重置到y=0
        世界高度_像素 = self.世界高度 * 方块大小
        if self.坐标_y > 世界高度_像素 + 3:
            self.坐标_y = 0
    
    def check_collision(self, 坐标_x, 坐标_y, 世界):
        """检查与世界方块的碰撞 - 优化版"""
        # 减少碰撞检测点数量，只检查必要的点
        填充 = 2
        点列表 = [
            # 四个角（最关键的碰撞点）
            (坐标_x + 填充, 坐标_y + 填充),
            (坐标_x + self.宽 - 填充, 坐标_y + 填充),
            (坐标_x + 填充, 坐标_y + self.高 - 填充),
            (坐标_x + self.宽 - 填充, 坐标_y + self.高 - 填充)
        ]
        
        # 只在非斜向移动时添加额外点（优化斜向移动性能）
        if not (abs(self.速度_x) > 0 and abs(self.速度_y) > 0):
            点列表.extend([
                # 中心
                (坐标_x + self.宽 // 2, 坐标_y + self.高 // 2),
                # 左右边中点
                (坐标_x + 填充, 坐标_y + self.高 // 2),
                (坐标_x + self.宽 - 填充, 坐标_y + self.高 // 2),
                # 上下边中点
                (坐标_x + self.宽 // 2, 坐标_y + 填充),
                (坐标_x + self.宽 // 2, 坐标_y + self.高 - 填充)
            ])
        
        # 缓存方块属性访问，避免重复查找
        solid_blocks = set()
        
        for px, py in 点列表:
            方块_x = int(px // 方块大小)
            方块_y = int(py // 方块大小)
            
            # 检查坐标是否有效，根据世界类型处理不同情况
            if (世界.无限世界 or 0 <= 方块_x < self.世界宽度) and 0 <= 方块_y < self.世界高度:
                # 使用get_block方法获取方块，兼容无限世界
                方块 = 世界.get_block(方块_x, 方块_y)
                
                # 快速判断：空气直接跳过
                if 方块 == 空气:
                    continue
                
                # 检查是否为固体方块
                if 方块 in solid_blocks:
                    return True
                
                # 缓存固体方块判断结果
                if 方块属性.get(方块, {}).get("固体", False):
                    solid_blocks.add(方块)
                    return True
        return False
    
    def _check_single_point_collision(self, 坐标_x, 坐标_y, 世界, 点列表):
        """内部方法：检查单个点集的碰撞 - 优化版"""
        # 简化实现，直接返回False，减少不必要的计算
        # 这个方法主要用于斜向移动微调，在优化后的碰撞检测中不再需要复杂计算
        return False
    
    def check_water_status(self, 世界):
        """检查玩家在水中和水方块附近的状态"""
        from 状态管理 import 状态管理器实例  # 导入状态管理器实例
        
        # 保存上一帧的水中状态
        self.上一帧在水中 = self.在水中
        
        self.在水中 = False
        self.在水附近 = False
        
        # 获取玩家占据的方块坐标范围
        左方块_x = int(self.坐标_x // 方块大小)
        右方块_x = int((self.坐标_x + self.宽) // 方块大小)
        上方块_y = int(self.坐标_y // 方块大小)
        下方块_y = int((self.坐标_y + self.高) // 方块大小)
        
        # 检查玩家是否在水中（玩家碰撞盒内有水方块）
        for x in range(左方块_x, 右方块_x + 1):
            for y in range(上方块_y, 下方块_y + 1):
                # 检查坐标是否有效，根据世界类型处理不同情况
                if (世界.无限世界 or 0 <= x < self.世界宽度) and 0 <= y < self.世界高度:
                    # 使用get_block方法获取方块，兼容无限世界
                    方块 = 世界.get_block(x, y)
                    if 方块 == 水:
                        self.在水中 = True
                        
                        # 当玩家在水中时，关闭燃烧状态
                        if 状态管理器实例.是否燃烧():
                            状态管理器实例.关闭燃烧状态()
                        
                        break
            if self.在水中:
                break
        
        # 如果不在水中，检查是否在水方块附近（5格范围内）
        if not self.在水中:
            # 检查玩家周围5格范围内的方块
            for x in range(左方块_x - 5, 右方块_x + 6):
                for y in range(上方块_y - 5, 下方块_y + 6):
                    # 检查坐标是否有效，根据世界类型处理不同情况
                    if (世界.无限世界 or 0 <= x < self.世界宽度) and 0 <= y < self.世界高度:
                        # 使用get_block方法获取方块，兼容无限世界
                        方块 = 世界.get_block(x, y)
                        if 方块 == 水:
                            self.在水附近 = True
                            break
                if self.在水附近:
                    break
        
        # 检测玩家离开水的瞬间
        if not self.在水中 and self.上一帧在水中:
            # 生成蓝色颗粒效果
            # 生成随机数量的蓝色颗粒（5-10个）
            for _ in range(random.randint(5, 10)):
                # 在玩家周围随机位置生成
                粒子_x = self.坐标_x + random.randint(0, self.宽)
                粒子_y = self.坐标_y + random.randint(0, self.高)
                # 蓝色颗粒
                粒子颜色 = (0, 100, 255)  # 蓝色
                # 添加到世界粒子列表
                if hasattr(世界, '粒子'):
                    世界.粒子.append({
                        'x': 粒子_x,
                        'y': 粒子_y,
                        'vx': random.uniform(-2, 2),
                        'vy': random.uniform(-2, 2),
                        'color': 粒子颜色,
                        'life': 1.0,  # 持续1秒
                        'size': random.uniform(2, 5)
                    })
    
    def jump(self):
        """跳跃"""
        if self.在地面上:
            # 播放跳跃音效
            audio_manager.play_sound("跳跃")
            # 计算实际跳跃力度（基础跳跃力度 + 装备跳跃力百分比加成）
            # 跳跃力度是负值，所以装备跳跃力加成（百分比）应该从跳跃力度中减去
            跳跃力加成百分比 = self.equipment_jump / 100.0
            实际跳跃力度 = self.跳跃力度 - abs(self.跳跃力度) * 跳跃力加成百分比
            self.速度_y = 实际跳跃力度
            self.在地面上 = False
    
    def update(self, 按键状态, 世界, 时间增量):
        """更新玩家状态"""
        # 计算实际移动速度（基础速度 + 装备速度百分比加成）
        移速加成百分比 = self.equipment_speed / 100.0
        实际移动速度 = self.移动速度 * (1 + 移速加成百分比)
        
        # 更新冲刺状态
        if self.正在冲刺:
            self.冲刺计时器 += 时间增量
            if self.冲刺计时器 >= self.冲刺持续时间:
                self.正在冲刺 = False
                self.冲刺计时器 = 0
        
        # 水平移动控制
        if 按键状态[pygame.K_a] or 按键状态[pygame.K_LEFT]:
            self.速度_x = -实际移动速度
            self.朝向右 = False
            self.正在行走 = True
            self.正在冲刺 = False  # 有按键输入时取消冲刺状态
        elif 按键状态[pygame.K_d] or 按键状态[pygame.K_RIGHT]:
            self.速度_x = 实际移动速度
            self.朝向右 = True
            self.正在行走 = True
            self.正在冲刺 = False  # 有按键输入时取消冲刺状态
        else:
            self.正在行走 = False
            # 只有在冲刺状态下才应用减速机制，普通移动时立即停止
            if self.正在冲刺:
                # 冲刺时慢慢减速
                if abs(self.速度_x) > 1:
                    # 根据当前速度方向减速
                    减速系数 = 0.9
                    self.速度_x *= 减速系数
                else:
                    self.速度_x = 0
                    self.正在冲刺 = False
            else:
                # 普通移动时立即停止
                self.速度_x = 0
        
        # 飞行模式控制
        if self.fly_mode:
            if 按键状态[pygame.K_w] or 按键状态[pygame.K_UP]:
                self.速度_y = -实际移动速度
            elif 按键状态[pygame.K_s] or 按键状态[pygame.K_DOWN]:
                self.速度_y = 实际移动速度
            else:
                self.速度_y = 0
        else:
            # 跳跃控制
            if 按键状态[pygame.K_SPACE] and self.在地面上:
                self.jump()
        
        # 岩浆检测和伤害处理
        self.检测岩浆(世界, 时间增量)
        
        # 处理空格按下和跳跃图片切换 - 使用状态变化触发
        当前空格状态 = 按键状态[pygame.K_SPACE]
        
        # 如果空格键刚刚被按下（从释放到按下）
        if 当前空格状态 and not self.空格上次按下:
            # 触发跳跃图片显示
            self.需要使用跳跃图片 = True
            # 设置计时器为1秒（根据帧率转换）
            self.跳跃图片计时器 = 60  # 假设60fps，60帧就是1秒
        
        # 更新计时器
        if self.跳跃图片计时器 > 0:
            # 使用时间增量来更新计时器，确保在不同帧率下都保持1秒
            self.跳跃图片计时器 -= 60 * 时间增量
            if self.跳跃图片计时器 <= 0:
                self.跳跃图片计时器 = 0
                self.需要使用跳跃图片 = False
        
        # 保存当前空格状态
        self.空格上次按下 = 当前空格状态
        
        # 更新丢弃物品计时器
        self.drop_item_timer += 时间增量
        
        # 处理G键丢弃物品 - 限制1秒一次
        if 按键状态[pygame.K_g] and self.drop_item_timer >= self.drop_item_interval:
            # 检查游戏实例是否存在以及是否有背包管理器
            if hasattr(self, 'game') and self.game and hasattr(self.game, '背包管理器'):
                背包管理器 = self.game.背包管理器
                # 获取当前选中的快捷栏格子
                当前格子 = self.game.当前选中格子
                # 获取快捷栏物品列表
                hotbar_items = 背包管理器.快捷栏物品
                # 检查当前格子是否有效且有物品
                if 0 <= 当前格子 < len(hotbar_items) and hotbar_items[当前格子] is not None:
                    当前物品 = hotbar_items[当前格子]
                    # 检查物品数量是否大于0
                    if 当前物品.数量 > 0:
                        # 创建掉落物
                        物品_id = 当前物品.物品_id
                        # 计算掉落位置：根据玩家朝向，在玩家前方生成
                        # 向右30像素，向左50像素
                        距离 = 30 if self.朝向右 else 50
                        掉落_x = self.坐标_x + self.宽 // 2 + 距离 * (1 if self.朝向右 else -1)
                        掉落_y = self.坐标_y + self.高 // 2
                        # 根据玩家朝向设置水平速度
                        水平速度 = 3 if self.朝向右 else -3
                        # 创建掉落物实体
                        掉落物 = ItemEntity(self.game.世界, 掉落_x, 掉落_y, 物品_id, 1)
                        # 设置掉落物的初始速度
                        掉落物.velocity_x = 水平速度
                        掉落物.velocity_y = -2  # 向上抛出
                        # 将掉落物添加到世界的掉落物列表中
                        self.game.世界.items.append(掉落物)
                        # 减少物品数量
                        当前物品.数量 -= 1
                        # 如果物品数量为0，从快捷栏中移除
                        if 当前物品.数量 <= 0:
                            hotbar_items[当前格子] = None
                        # 重置丢弃物品计时器
                        self.drop_item_timer = 0
        
        # 检测玩家是否在移动或跳跃
        当前是否在移动或跳跃 = self.正在行走 or self.需要使用跳跃图片 or abs(self.速度_x) > 0 or abs(self.速度_y) > 0
        
        # 如果玩家正在移动或跳跃
        if 当前是否在移动或跳跃:
            # 重置移动或跳跃时间
            self.移动或跳跃时间 = 0
            self.是否在移动或跳跃 = True
            self.需要使用待机图片 = False
        else:
            # 玩家没有移动或跳跃，增加时间
            self.移动或跳跃时间 += 时间增量
            self.是否在移动或跳跃 = False
            
            # 如果超过10秒没有移动或跳跃，切换到待机图片
            if self.移动或跳跃时间 >= 10:
                self.需要使用待机图片 = True
        
        # 更新生命值和饥饿值系统
        self._update_health_and_hunger(时间增量)
        
        # 更新受伤动画时间
        if self.正在受伤:
            self.受伤动画时间 += 时间增量
            if self.受伤动画时间 >= self.受伤动画持续时间:
                self.正在受伤 = False
                self.受伤动画时间 = 0
        
        # 更新攻击动画时间
        if self.正在攻击:
            self.攻击动画时间 += 时间增量
            if self.攻击动画时间 >= self.攻击动画持续时间:
                self.正在攻击 = False
                self.攻击动画时间 = 0
        
        self.move(世界, 时间增量)
        
    def _update_health_and_hunger(self, 时间增量):
        """更新生命值和饥饿值系统"""
        # 更新饥饿值计时器
        self.hunger_timer += 时间增量
        
        # 检查是否需要减少饥饿值（游戏时间每小时减少1饥饿值）
        if self.hunger_timer >= self.hunger_reduction_interval:
            # 减少饥饿值
            self.current_hunger -= 1  # 恢复为每次减少1点饥饿值
            # 确保饥饿值不低于0
            self.current_hunger = max(0, self.current_hunger)
            # 重置计时器
            self.hunger_timer = 0
            # 移除调试输出
        
        # 更新生命值恢复计时器
        self.health_regen_timer += 时间增量
        
        # 检查是否可以恢复生命值（饥饿值大于20%，生命值不满95，且达到恢复间隔）
        if (self.current_hunger > self.max_hunger * 0.2 and 
            self.health_regen_timer >= 3 and  # 修改为3秒间隔
            self.current_health < 95):  # 修改为生命值不满95时
            
            # 消耗饥饿值
            self.current_hunger -= 1
            # 确保饥饿值不低于0
            self.current_hunger = max(0, self.current_hunger)
            
            # 恢复生命值
            self.current_health += 5
            # 确保生命值不超过最大值
            self.current_health = min(self.current_health, self.max_health)
            
            # 重置生命值恢复计时器
            self.health_regen_timer = 0
            
            # 移除调试输出
        
        # 当饥饿值为0时，激活饥饿状态并扣除生命值
        if self.current_hunger == 0:
            from 状态管理 import 状态管理器实例
            # 激活饥饿状态（无限时间）
            状态管理器实例.激活饥饿状态()
            
            # 每秒扣除10点生命值
            if self.health_regen_timer >= 1:  # 每秒扣除一次
                self.take_damage(10)  # 每次扣除10点生命值
                self.health_regen_timer = 0
        else:
            # 当饥饿值大于0时，关闭饥饿状态
            from 状态管理 import 状态管理器实例
            if 状态管理器实例.是否饥饿():
                状态管理器实例.关闭饥饿状态()
    
    def 检测岩浆(self, 世界, 时间增量):
        """检测玩家是否接触岩浆并处理伤害和燃烧状态
        
        参数:
            世界: 游戏世界实例
            时间增量: 上次更新到现在的时间间隔（秒）
        """
        from 状态管理 import 状态管理器实例
        import random
        
        # 初始化计时器属性（如果不存在）
        if not hasattr(self, '岩浆伤害计时器'):
            self.岩浆伤害计时器 = 0
        if not hasattr(self, '燃烧伤害计时器'):
            self.燃烧伤害计时器 = 0
        if not hasattr(self, '在岩浆中'):
            self.在岩浆中 = False
        
        # 重置在岩浆中状态
        新的在岩浆中状态 = False
        
        # 获取玩家碰撞盒覆盖的方块范围
        方块大小 = 32
        左方块_x = int(self.坐标_x // 方块大小)
        右方块_x = int((self.坐标_x + self.宽) // 方块大小)
        上方块_y = int(self.坐标_y // 方块大小)
        下方块_y = int((self.坐标_y + self.高) // 方块大小)
        
        # 检测玩家是否在岩浆中
        for x in range(左方块_x, 右方块_x + 1):
            for y in range(上方块_y, 下方块_y + 1):
                # 检查坐标是否有效，根据世界类型处理不同情况
                if (世界.无限世界 or 0 <= x < 世界.宽度) and 0 <= y < 世界.高度:
                    方块 = 世界.get_block(x, y)
                    if 方块 == 岩浆:
                        新的在岩浆中状态 = True
                        break
            if 新的在岩浆中状态:
                break
        
        # 处理岩浆接触伤害
        if 新的在岩浆中状态:
            self.在岩浆中 = True
            # 增加岩浆伤害计时器
            self.岩浆伤害计时器 += 时间增量
            
            # 每秒造成15点伤害
            if self.岩浆伤害计时器 >= 1:
                self.take_damage(15)
                self.岩浆伤害计时器 = 0
            
            # 在岩浆中时，清除燃烧状态
            if 状态管理器实例.是否燃烧():
                状态管理器实例.关闭燃烧状态()
        else:
            # 如果离开岩浆，激活燃烧状态
            if self.在岩浆中 and not 状态管理器实例.是否燃烧():
                状态管理器实例.激活燃烧状态(10)  # 10秒燃烧时间
            self.在岩浆中 = False
        
        # 处理燃烧状态伤害
        if 状态管理器实例.是否燃烧():
            # 增加燃烧伤害计时器
            self.燃烧伤害计时器 += 时间增量
            
            # 每秒造成5点伤害
            if self.燃烧伤害计时器 >= 1:
                self.take_damage(5)
                self.燃烧伤害计时器 = 0
        
        # 生成红色粒子效果（在岩浆中或燃烧时）
        if 新的在岩浆中状态 or 状态管理器实例.是否燃烧():
            # 生成随机数量的粒子（1-3个）
            for _ in range(random.randint(1, 3)):
                # 在玩家周围随机位置生成
                粒子_x = self.坐标_x + random.randint(0, self.宽)
                粒子_y = self.坐标_y + random.randint(0, self.高)
                # 红色粒子
                粒子颜色 = (255, random.randint(0, 100), random.randint(0, 50))
                # 添加到世界粒子列表
                if hasattr(世界, '粒子'):
                    世界.粒子.append({
                        'x': 粒子_x,
                        'y': 粒子_y,
                        'vx': random.uniform(-2, 2),
                        'vy': random.uniform(-2, 2),
                        'color': 粒子颜色,
                        'life': random.uniform(0.5, 1.5),
                        'size': random.uniform(2, 5)
                    })
        
        # 生成棕色颗粒效果（当处于饥饿状态时）
        if 状态管理器实例.是否饥饿():
            # 生成随机数量的颗粒（1-2个）
            for _ in range(random.randint(1, 2)):
                # 在玩家周围随机位置生成
                粒子_x = self.坐标_x + random.randint(0, self.宽)
                粒子_y = self.坐标_y + random.randint(0, self.高)
                # 棕色颗粒
                粒子颜色 = (139, 69, 19)  # 棕色
                # 添加到世界粒子列表
                if hasattr(世界, '粒子'):
                    世界.粒子.append({
                        'x': 粒子_x,
                        'y': 粒子_y,
                        'vx': random.uniform(-0.5, 0.5),  # 速度减半，飘的距离减少50%
                        'vy': random.uniform(-0.5, 0.5),  # 速度减半，飘的距离减少50%
                        'color': 粒子颜色,
                        'life': random.uniform(1.0, 2.0),
                        'size': random.uniform(1, 3)  # 颗粒较小
                    })
    
    def 加载外观设置(self):
        """加载角色外观设置"""
        try:
            # 获取脚本所在目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # 获取项目根目录（向上一级，因为游玩.py在1.主程序与核心文件夹中）
            project_root = os.path.dirname(script_dir)
            # 设置文件现在位于存档文件夹中
            设置文件路径 = os.path.join(project_root, "存档", "设置_数据库.json")
            if os.path.exists(设置文件路径):
                with open(设置文件路径, "r", encoding="utf-8") as f:
                    设置数据 = json.load(f)
                    if "当前选择外观" in 设置数据:
                        self.角色外观 = 设置数据["当前选择外观"]
        except Exception as e:
            # 输出错误信息，方便调试
            print(f"加载外观设置时出错: {str(e)}")
            # 静默处理错误，保持默认外观
            pass
    
    def load角色图片(self):
        """加载角色图片"""
        try:
            # 获取脚本所在目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # 获取项目根目录（向上一级，因为游玩.py在1.主程序与核心文件夹中）
            project_root = os.path.dirname(script_dir)
            # 使用项目根目录下的资源/图片/角色路径
            图片_dir = os.path.join(project_root, "资源", "图片", "角色")
            
            # 加载玩家上传文件 - 对应外观1
            # 首先尝试从设置文件中获取上传文件路径
            上传文件路径 = None
            # 设置文件现在位于存档文件夹中
            设置文件路径 = os.path.join(project_root, "存档", "设置_数据库.json")
            if os.path.exists(设置文件路径):
                try:
                    with open(设置文件路径, "r", encoding="utf-8") as f:
                        设置数据 = json.load(f)
                        if "玩家上传图片路径" in 设置数据:
                            上传文件路径 = 设置数据["玩家上传图片路径"]
                except Exception as e:
                    print(f"读取设置文件时出错: {str(e)}")
            
            # 确保上传文件目录存在
            if not os.path.exists(图片_dir):
                os.makedirs(图片_dir, exist_ok=True)
            
            # 如果没有指定路径或文件不存在，使用默认路径
            if 上传文件路径 is None or not os.path.exists(上传文件路径):
                上传文件路径 = os.path.join(图片_dir, "玩家上传.png")
            
            # 计算基础角色尺寸：1:1比例，放大75%（用于骑士3和小骑士）
            基础角色尺寸 = int(32 * 1.75)  # 32 * 1.75 = 56
            # 骑士1和骑士2的尺寸：2:1比例（高:宽），不增加75%大小
            骑士1_2宽度 = 32  # 基础32像素宽度
            骑士1_2高度 = 32 * 2  # 2:1比例高度
            # 骑士3和小骑士的尺寸：1:1比例，放大75%
            角色尺寸 = 基础角色尺寸
            
            # 加载玩家上传图片
            if os.path.exists(上传文件路径):
                try:
                    图片 = pygame.image.load(上传文件路径).convert_alpha()
                    # 缩放到1:1比例，放大75%
                    图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                    self.角色图片["玩家上传"] = 图片
                except Exception as e:
                    print(f"加载玩家上传图片时出错: {str(e)}")
            
            # 从图片管理器加载骑士1站立图片 - 对应外观3
            图片 = 图片管理器.获取图片("骑士1_站立")
            if 图片:
                # 缩放到2:1比例（高:宽）
                图片 = pygame.transform.scale(图片, (骑士1_2宽度, 骑士1_2高度))
                self.角色图片["骑士1_站立"] = 图片
            else:
                # 尝试备选名称
                图片 = 图片管理器.获取图片("骑士1")
                if 图片:
                    # 缩放到2:1比例（高:宽）
                    图片 = pygame.transform.scale(图片, (骑士1_2宽度, 骑士1_2高度))
                    self.角色图片["骑士1_站立"] = 图片
            
            # 从图片管理器加载骑士1跳跃图片
            图片 = 图片管理器.获取图片("骑士1_跳跃")
            if 图片:
                # 缩放到2:1比例（高:宽）
                图片 = pygame.transform.scale(图片, (骑士1_2宽度, 骑士1_2高度))
                self.角色图片["骑士1_跳跃"] = 图片
            
            # 从图片管理器加载骑士1行走图片
            图片 = 图片管理器.获取图片("骑士1_行走")
            if 图片:
                # 缩放到2:1比例（高:宽）
                图片 = pygame.transform.scale(图片, (骑士1_2宽度, 骑士1_2高度))
                self.角色图片["骑士1_行走"] = 图片
            
            # 从图片管理器加载骑士2站立图片 - 对应外观2和4
            图片 = 图片管理器.获取图片("骑士2_站立")
            if 图片:
                # 缩放到2:1比例（高:宽）
                图片 = pygame.transform.scale(图片, (骑士1_2宽度, 骑士1_2高度))
                self.角色图片["骑士2_站立"] = 图片
            else:
                # 尝试备选名称
                图片 = 图片管理器.获取图片("骑士2")
                if 图片:
                    # 缩放到2:1比例（高:宽）
                    图片 = pygame.transform.scale(图片, (骑士1_2宽度, 骑士1_2高度))
                    self.角色图片["骑士2_站立"] = 图片
            
            # 从图片管理器加载骑士2跳跃图片
            图片 = 图片管理器.获取图片("骑士2_跳跃")
            if 图片:
                # 缩放到2:1比例（高:宽）
                图片 = pygame.transform.scale(图片, (骑士1_2宽度, 骑士1_2高度))
                self.角色图片["骑士2_跳跃"] = 图片
            
            # 从图片管理器加载骑士2行走图片
            图片 = 图片管理器.获取图片("骑士2_行走")
            if 图片:
                # 缩放到2:1比例（高:宽）
                图片 = pygame.transform.scale(图片, (骑士1_2宽度, 骑士1_2高度))
                self.角色图片["骑士2_行走"] = 图片
            
            # 从图片管理器加载骑士3站立图片 - 对应外观5
            图片 = 图片管理器.获取图片("骑士3")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["骑士3_站立"] = 图片
            
            # 从图片管理器加载骑士3跳跃图片
            图片 = 图片管理器.获取图片("骑士3_跳跃")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["骑士3_跳跃"] = 图片
            
            # 从图片管理器加载骑士3行走图片
            图片 = 图片管理器.获取图片("骑士3_行走")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["骑士3_行走"] = 图片
            
            # 从图片管理器加载小骑士站立图片 - 对应外观6
            图片 = 图片管理器.获取图片("小骑士")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["小骑士_站立"] = 图片
            
            # 从图片管理器加载小骑士跳跃图片
            图片 = 图片管理器.获取图片("小骑士_跳跃")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["小骑士_跳跃"] = 图片
            
            # 从图片管理器加载小骑士行走图片
            图片 = 图片管理器.获取图片("小骑士_行走")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["小骑士_行走"] = 图片
            
            # 从图片管理器加载猫猫1站立图片 - 对应外观7
            图片 = 图片管理器.获取图片("猫猫1")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫1_站立"] = 图片
            
            # 从图片管理器加载猫猫1跳跃图片
            图片 = 图片管理器.获取图片("猫猫1_跳跃")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫1_跳跃"] = 图片
            
            # 从图片管理器加载猫猫1行走图片
            图片 = 图片管理器.获取图片("猫猫1_行走")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫1_行走"] = 图片
            
            # 从图片管理器加载猫猫1待机图片
            图片 = 图片管理器.获取图片("猫猫1_待机")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫1_待机"] = 图片
            
            # 从图片管理器加载猫猫1受伤图片（生气）
            图片 = 图片管理器.获取图片("猫猫1_生气")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫1_受伤"] = 图片
            
            # 从图片管理器加载猫猫1攻击图片
            图片 = 图片管理器.获取图片("猫猫1_攻击")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫1_攻击"] = 图片
            
            # 从图片管理器加载猫猫2站立图片 - 对应外观8
            图片 = 图片管理器.获取图片("猫猫2")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫2_站立"] = 图片
            
            # 从图片管理器加载猫猫2跳跃图片
            图片 = 图片管理器.获取图片("猫猫2_跳跃")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫2_跳跃"] = 图片
            
            # 从图片管理器加载猫猫2行走图片
            图片 = 图片管理器.获取图片("猫猫2_行走")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫2_行走"] = 图片
            
            # 从图片管理器加载猫猫2待机图片
            图片 = 图片管理器.获取图片("猫猫2_待机")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫2_待机"] = 图片
            
            # 从图片管理器加载猫猫2受伤图片（生气）
            图片 = 图片管理器.获取图片("猫猫2_生气")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫2_受伤"] = 图片
            
            # 从图片管理器加载猫猫2攻击图片
            图片 = 图片管理器.获取图片("猫猫2_攻击")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫2_攻击"] = 图片
            
            # 从图片管理器加载猫猫3站立图片 - 对应外观9
            图片 = 图片管理器.获取图片("猫猫3")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫3_站立"] = 图片
            
            # 从图片管理器加载猫猫3跳跃图片
            图片 = 图片管理器.获取图片("猫猫3_跳跃")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫3_跳跃"] = 图片
            
            # 从图片管理器加载猫猫3行走图片
            图片 = 图片管理器.获取图片("猫猫3_行走")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫3_行走"] = 图片
            
            # 从图片管理器加载猫猫3待机图片
            图片 = 图片管理器.获取图片("猫猫3_待机")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫3_待机"] = 图片
            
            # 从图片管理器加载猫猫3受伤图片（生气）
            图片 = 图片管理器.获取图片("猫猫3_生气")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫3_受伤"] = 图片
            
            # 从图片管理器加载猫猫3攻击图片
            图片 = 图片管理器.获取图片("猫猫3_攻击")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫3_攻击"] = 图片
            
            # 从图片管理器加载猫猫4站立图片 - 对应外观10
            图片 = 图片管理器.获取图片("猫猫4")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫4_站立"] = 图片
            
            # 从图片管理器加载猫猫4跳跃图片
            图片 = 图片管理器.获取图片("猫猫4_跳跃")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫4_跳跃"] = 图片
            
            # 从图片管理器加载猫猫4行走图片
            图片 = 图片管理器.获取图片("猫猫4_行走")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫4_行走"] = 图片
            
            # 从图片管理器加载猫猫4待机图片
            图片 = 图片管理器.获取图片("猫猫4_待机")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫4_待机"] = 图片
            
            # 从图片管理器加载猫猫4受伤图片（生气）
            图片 = 图片管理器.获取图片("猫猫4_生气")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫4_受伤"] = 图片
            
            # 从图片管理器加载猫猫4攻击图片
            图片 = 图片管理器.获取图片("猫猫4_攻击")
            if 图片:
                # 缩放到1:1比例，放大75%
                图片 = pygame.transform.scale(图片, (角色尺寸, 角色尺寸))
                self.角色图片["猫猫4_攻击"] = 图片
        except Exception as e:
            # 静默处理错误
            pass
    
    def draw(self, 屏幕, 相机_x, 相机_y):
        """绘制玩家"""
        绘制_x = self.坐标_x - 相机_x
        绘制_y = self.坐标_y - 相机_y
        
        # 确保字典键名正确
        玩家上传键 = "玩家上传"
        骑士1站立键 = "骑士1_站立" if "骑士1_站立" in self.角色图片 else "骑士1"
        骑士1跳跃键 = "骑士1_跳跃"
        骑士1行走键 = "骑士1_行走"
        骑士2站立键 = "骑士2_站立" if "骑士2_站立" in self.角色图片 else "骑士2"
        骑士2跳跃键 = "骑士2_跳跃"
        骑士2行走键 = "骑士2_行走"
        骑士3站立键 = "骑士3_站立" if "骑士3_站立" in self.角色图片 else "骑士3"
        骑士3跳跃键 = "骑士3_跳跃"
        骑士3行走键 = "骑士3_行走"
        小骑士站立键 = "小骑士_站立" if "小骑士_站立" in self.角色图片 else "小骑士"
        小骑士跳跃键 = "小骑士_跳跃"
        小骑士行走键 = "小骑士_行走"
        # 猫猫角色键名定义
        猫猫1站立键 = "猫猫1_站立" if "猫猫1_站立" in self.角色图片 else "猫猫1"
        猫猫1跳跃键 = "猫猫1_跳跃"
        猫猫1行走键 = "猫猫1_行走"
        猫猫1待机键 = "猫猫1_待机" if "猫猫1_待机" in self.角色图片 else "猫猫1_站立"
        猫猫2站立键 = "猫猫2_站立" if "猫猫2_站立" in self.角色图片 else "猫猫2"
        猫猫2跳跃键 = "猫猫2_跳跃"
        猫猫2行走键 = "猫猫2_行走"
        猫猫2待机键 = "猫猫2_待机" if "猫猫2_待机" in self.角色图片 else "猫猫2_站立"
        猫猫3站立键 = "猫猫3_站立" if "猫猫3_站立" in self.角色图片 else "猫猫3"
        猫猫3跳跃键 = "猫猫3_跳跃"
        猫猫3行走键 = "猫猫3_行走"
        猫猫3待机键 = "猫猫3_待机" if "猫猫3_待机" in self.角色图片 else "猫猫3_站立"
        猫猫4站立键 = "猫猫4_站立" if "猫猫4_站立" in self.角色图片 else "猫猫4"
        猫猫4跳跃键 = "猫猫4_跳跃"
        猫猫4行走键 = "猫猫4_行走"
        猫猫4待机键 = "猫猫4_待机" if "猫猫4_待机" in self.角色图片 else "猫猫4_站立"
        
        # 玩家上传文件处理 - 外观1
        if self.角色外观 == 1:
            # 使用玩家上传图片
            if 玩家上传键 in self.角色图片:
                try:
                    图片 = self.角色图片[玩家上传键]
                    # 翻转图片以匹配朝向
                    if not self.朝向右:
                        图片 = pygame.transform.flip(图片, True, False)
                    # 计算图片位置使其居中
                    图片_x = 绘制_x + (self.宽 - 图片.get_width()) // 2
                    图片_y = 绘制_y + (self.高 - 图片.get_height())
                    屏幕.blit(图片, (图片_x, 图片_y))
                    return
                except Exception as e:
                    print(f"渲染玩家上传图片时出错: {str(e)}")
        
        # 骑士1处理 - 外观3
        elif self.角色外观 == 3:
            # 根据状态决定使用跳跃、行走还是站立图片（优先级：跳跃 > 行走 > 站立）
            if self.需要使用跳跃图片 and 骑士1跳跃键 in self.角色图片:
                # 使用跳跃图片
                图片 = self.角色图片[骑士1跳跃键]
            elif self.正在行走 and 骑士1行走键 in self.角色图片:
                # 使用行走图片
                图片 = self.角色图片[骑士1行走键]
            elif 骑士1站立键 in self.角色图片:
                # 使用站立图片
                图片 = self.角色图片[骑士1站立键]
            else:
                图片 = None
                
            if 图片:
                # 翻转图片以匹配朝向
                if not self.朝向右:
                    图片 = pygame.transform.flip(图片, True, False)
                # 计算图片位置使其居中
                图片_x = 绘制_x + (self.宽 - 图片.get_width()) // 2
                图片_y = 绘制_y + (self.高 - 图片.get_height())
                屏幕.blit(图片, (图片_x, 图片_y))
                return
        
        # 骑士2处理 - 外观4
        elif self.角色外观 == 4:
            # 根据状态决定使用跳跃、行走还是站立图片（优先级：跳跃 > 行走 > 站立）
            if self.需要使用跳跃图片 and 骑士2跳跃键 in self.角色图片:
                # 使用跳跃图片
                图片 = self.角色图片[骑士2跳跃键]
            elif self.正在行走 and 骑士2行走键 in self.角色图片:
                # 使用行走图片
                图片 = self.角色图片[骑士2行走键]
            elif 骑士2站立键 in self.角色图片:
                # 使用站立图片
                图片 = self.角色图片[骑士2站立键]
            else:
                图片 = None
                
            if 图片:
                # 翻转图片以匹配朝向
                if not self.朝向右:
                    图片 = pygame.transform.flip(图片, True, False)
                # 计算图片位置使其居中
                图片_x = 绘制_x + (self.宽 - 图片.get_width()) // 2
                图片_y = 绘制_y + (self.高 - 图片.get_height())
                屏幕.blit(图片, (图片_x, 图片_y))
                return
        
        # 骑士3处理 - 外观5
        elif self.角色外观 == 5:
            # 根据状态决定使用跳跃、行走还是站立图片（优先级：跳跃 > 行走 > 站立）
            if self.需要使用跳跃图片 and 骑士3跳跃键 in self.角色图片:
                # 使用跳跃图片
                图片 = self.角色图片[骑士3跳跃键]
            elif self.正在行走 and 骑士3行走键 in self.角色图片:
                # 使用行走图片
                图片 = self.角色图片[骑士3行走键]
            elif 骑士3站立键 in self.角色图片:
                # 使用站立图片
                图片 = self.角色图片[骑士3站立键]
            else:
                图片 = None
                
            if 图片:
                # 翻转图片以匹配朝向
                if not self.朝向右:
                    图片 = pygame.transform.flip(图片, True, False)
                # 计算图片位置使其居中，底部对齐
                图片_x = 绘制_x + (self.宽 - 图片.get_width()) // 2
                # 1:1比例角色，底部对齐玩家底部
                图片_y = 绘制_y + (self.高 - 图片.get_height())
                屏幕.blit(图片, (图片_x, 图片_y))
                return
        
        # 小骑士处理 - 外观6
        elif self.角色外观 == 6:
            # 根据状态决定使用跳跃、行走还是站立图片（优先级：跳跃 > 行走 > 站立）
            if self.需要使用跳跃图片 and 小骑士跳跃键 in self.角色图片:
                # 使用跳跃图片
                图片 = self.角色图片[小骑士跳跃键]
            elif self.正在行走 and 小骑士行走键 in self.角色图片:
                # 使用行走图片
                图片 = self.角色图片[小骑士行走键]
            elif 小骑士站立键 in self.角色图片:
                # 使用站立图片
                图片 = self.角色图片[小骑士站立键]
            else:
                图片 = None
                
            if 图片:
                # 翻转图片以匹配朝向
                if not self.朝向右:
                    图片 = pygame.transform.flip(图片, True, False)
                # 计算图片位置使其居中，底部对齐
                图片_x = 绘制_x + (self.宽 - 图片.get_width()) // 2
                # 1:1比例角色，底部对齐玩家底部
                图片_y = 绘制_y + (self.高 - 图片.get_height())
                屏幕.blit(图片, (图片_x, 图片_y))
                return
        
        # 猫猫1处理 - 外观7
        elif self.角色外观 == 7:
            # 根据状态决定使用受伤、攻击、跳跃、行走、待机还是站立图片（优先级：受伤 > 攻击 > 跳跃 > 行走 > 待机 > 站立）
            if self.正在受伤 and "猫猫1_受伤" in self.角色图片:
                # 使用受伤图片
                图片 = self.角色图片["猫猫1_受伤"]
            elif self.正在攻击 and "猫猫1_攻击" in self.角色图片:
                # 使用攻击图片
                图片 = self.角色图片["猫猫1_攻击"]
            elif self.需要使用跳跃图片 and 猫猫1跳跃键 in self.角色图片:
                # 使用跳跃图片
                图片 = self.角色图片[猫猫1跳跃键]
            elif self.正在行走 and 猫猫1行走键 in self.角色图片:
                # 使用行走图片
                图片 = self.角色图片[猫猫1行走键]
            elif self.需要使用待机图片 and 猫猫1待机键 in self.角色图片:
                # 使用待机图片
                图片 = self.角色图片[猫猫1待机键]
            elif 猫猫1站立键 in self.角色图片:
                # 使用站立图片
                图片 = self.角色图片[猫猫1站立键]
            else:
                图片 = None
                
            if 图片:
                # 翻转图片以匹配朝向
                if not self.朝向右:
                    图片 = pygame.transform.flip(图片, True, False)
                # 计算图片位置使其居中，底部对齐
                图片_x = 绘制_x + (self.宽 - 图片.get_width()) // 2
                # 1:1比例角色，底部对齐玩家底部
                图片_y = 绘制_y + (self.高 - 图片.get_height())
                屏幕.blit(图片, (图片_x, 图片_y))
                return
        
        # 猫猫2处理 - 外观8
        elif self.角色外观 == 8:
            # 根据状态决定使用受伤、攻击、跳跃、行走、待机还是站立图片（优先级：受伤 > 攻击 > 跳跃 > 行走 > 待机 > 站立）
            if self.正在受伤 and "猫猫2_受伤" in self.角色图片:
                # 使用受伤图片
                图片 = self.角色图片["猫猫2_受伤"]
            elif self.正在攻击 and "猫猫2_攻击" in self.角色图片:
                # 使用攻击图片
                图片 = self.角色图片["猫猫2_攻击"]
            elif self.需要使用跳跃图片 and 猫猫2跳跃键 in self.角色图片:
                # 使用跳跃图片
                图片 = self.角色图片[猫猫2跳跃键]
            elif self.正在行走 and 猫猫2行走键 in self.角色图片:
                # 使用行走图片
                图片 = self.角色图片[猫猫2行走键]
            elif self.需要使用待机图片 and 猫猫2待机键 in self.角色图片:
                # 使用待机图片
                图片 = self.角色图片[猫猫2待机键]
            elif 猫猫2站立键 in self.角色图片:
                # 使用站立图片
                图片 = self.角色图片[猫猫2站立键]
            else:
                图片 = None
                
            if 图片:
                # 翻转图片以匹配朝向
                if not self.朝向右:
                    图片 = pygame.transform.flip(图片, True, False)
                # 计算图片位置使其居中，底部对齐
                图片_x = 绘制_x + (self.宽 - 图片.get_width()) // 2
                # 1:1比例角色，底部对齐玩家底部
                图片_y = 绘制_y + (self.高 - 图片.get_height())
                屏幕.blit(图片, (图片_x, 图片_y))
                return
        
        # 猫猫3处理 - 外观9
        elif self.角色外观 == 9:
            # 根据状态决定使用受伤、攻击、跳跃、行走、待机还是站立图片（优先级：受伤 > 攻击 > 跳跃 > 行走 > 待机 > 站立）
            if self.正在受伤 and "猫猫3_受伤" in self.角色图片:
                # 使用受伤图片
                图片 = self.角色图片["猫猫3_受伤"]
            elif self.正在攻击 and "猫猫3_攻击" in self.角色图片:
                # 使用攻击图片
                图片 = self.角色图片["猫猫3_攻击"]
            elif self.需要使用跳跃图片 and 猫猫3跳跃键 in self.角色图片:
                # 使用跳跃图片
                图片 = self.角色图片[猫猫3跳跃键]
            elif self.正在行走 and 猫猫3行走键 in self.角色图片:
                # 使用行走图片
                图片 = self.角色图片[猫猫3行走键]
            elif self.需要使用待机图片 and 猫猫3待机键 in self.角色图片:
                # 使用待机图片
                图片 = self.角色图片[猫猫3待机键]
            elif 猫猫3站立键 in self.角色图片:
                # 使用站立图片
                图片 = self.角色图片[猫猫3站立键]
            else:
                图片 = None
                
            if 图片:
                # 翻转图片以匹配朝向
                if not self.朝向右:
                    图片 = pygame.transform.flip(图片, True, False)
                # 计算图片位置使其居中，底部对齐
                图片_x = 绘制_x + (self.宽 - 图片.get_width()) // 2
                # 1:1比例角色，底部对齐玩家底部
                图片_y = 绘制_y + (self.高 - 图片.get_height())
                屏幕.blit(图片, (图片_x, 图片_y))
                return
        
        # 猫猫4处理 - 外观10
        elif self.角色外观 == 10:
            # 根据状态决定使用受伤、攻击、跳跃、行走、待机还是站立图片（优先级：受伤 > 攻击 > 跳跃 > 行走 > 待机 > 站立）
            if self.正在受伤 and "猫猫4_受伤" in self.角色图片:
                # 使用受伤图片
                图片 = self.角色图片["猫猫4_受伤"]
            elif self.正在攻击 and "猫猫4_攻击" in self.角色图片:
                # 使用攻击图片
                图片 = self.角色图片["猫猫4_攻击"]
            elif self.需要使用跳跃图片 and 猫猫4跳跃键 in self.角色图片:
                # 使用跳跃图片
                图片 = self.角色图片[猫猫4跳跃键]
            elif self.正在行走 and 猫猫4行走键 in self.角色图片:
                # 使用行走图片
                图片 = self.角色图片[猫猫4行走键]
            elif self.需要使用待机图片 and 猫猫4待机键 in self.角色图片:
                # 使用待机图片
                图片 = self.角色图片[猫猫4待机键]
            elif 猫猫4站立键 in self.角色图片:
                # 使用站立图片
                图片 = self.角色图片[猫猫4站立键]
            else:
                图片 = None
                
            if 图片:
                # 翻转图片以匹配朝向
                if not self.朝向右:
                    图片 = pygame.transform.flip(图片, True, False)
                # 计算图片位置使其居中，底部对齐
                图片_x = 绘制_x + (self.宽 - 图片.get_width()) // 2
                # 1:1比例角色，底部对齐玩家底部
                图片_y = 绘制_y + (self.高 - 图片.get_height())
                屏幕.blit(图片, (图片_x, 图片_y))
                return
        
        # 外观2或没有找到对应图片：使用系统绘制
        # 身体
        pygame.draw.rect(屏幕, 玩家_皮肤, (绘制_x, 绘制_y, self.宽, self.高))
        
        # 衣服
        pygame.draw.rect(屏幕, 玩家_衬衫, 
                        (绘制_x, 绘制_y + self.高 // 3, self.宽, self.高 // 3))
        pygame.draw.rect(屏幕, 玩家_裤子,
                        (绘制_x, 绘制_y + self.高 * 2 // 3, self.宽, self.高 // 3))
        
        # 头部
        头部晃动 = math.sin(time.time() * 5) * 2 if abs(self.速度_x) > 0.1 else 0
        pygame.draw.circle(屏幕, 玩家_皮肤, 
                          (绘制_x + self.宽 // 2, 绘制_y - 5 + 头部晃动), 12)
        
        # 眼睛
        眼睛偏移 = 3 if self.朝向右 else -3
        pygame.draw.circle(屏幕, (255, 255, 255),
                          (绘制_x + self.宽 // 2 + 眼睛偏移, 绘制_y - 8 + 头部晃动), 3)
    
    def take_damage(self, 伤害值, attacker=None):
        """玩家受到伤害
        
        参数:
            伤害值: 受到的伤害数值
            attacker: 攻击者对象（可选）
        """
        # 如果有攻击者，通知所有召唤的死神祝福攻击这个攻击者
        if attacker and hasattr(self, 'game') and self.game:
            from 武器处理 import handle_player_attack, 武器技能管理器实例
            handle_player_attack(attacker, 武器技能管理器实例)
        # 检查是否有无敌状态
        from 状态管理 import 状态管理器实例
        是否无敌, _, _ = 状态管理器实例.获取无敌状态()
        
        if not 是否无敌:
            # 保存初始生命值和额外生命值，用于打印日志
            初始额外生命值 = self.extra_health
            初始当前生命值 = self.current_health
            初始护盾值 = getattr(self, 'current_shield', 0)
            
            # 计算总防御力
            总防御力 = getattr(self, 'equipment_defense', 0) + getattr(self, 'upgrade_defense', 0) + getattr(self, 'base_defense', 0)
            
            # 计算免伤百分比（曲线加成：1防御=1%，40防御=30%，最大80%）
            import math
            # 使用 logistic 函数实现曲线加成：免伤百分比 = 0.8 / (1 + e^(-0.109*(防御值 - 44.5)))
            免伤百分比 = 0.8 / (1 + math.exp(-0.109 * (总防御力 - 44.5)))
            # 转换为百分比
            免伤百分比 *= 100
            
            # 应用免伤效果，计算最终伤害
            最终伤害值 = int(伤害值 * (1 - 免伤百分比 / 100))
            # 确保最终伤害至少为1
            最终伤害值 = max(1, 最终伤害值)
            
            # 先消耗护盾值（如果有）
            if hasattr(self, 'current_shield') and self.current_shield > 0:
                if self.current_shield >= 最终伤害值:
                    # 护盾足够承受全部伤害
                    self.current_shield -= 最终伤害值
                    最终伤害值 = 0
                else:
                    # 护盾不足以承受全部伤害，消耗完所有护盾
                    最终伤害值 -= self.current_shield
                    self.current_shield = 0
            
            # 再消耗额外生命值
            if 最终伤害值 > 0 and self.extra_health > 0:
                if self.extra_health >= 最终伤害值:
                    # 额外生命值足够承受全部伤害
                    self.extra_health -= 最终伤害值
                    最终伤害值 = 0
                else:
                    # 额外生命值不足以承受全部伤害，消耗完所有额外生命值
                    最终伤害值 -= self.extra_health
                    self.extra_health = 0
            
            # 最后消耗当前生命值
            if 最终伤害值 > 0:
                self.current_health -= 最终伤害值
                # 确保生命值不低于0
                self.current_health = max(0, self.current_health)
                
                # 创建伤害数字（只在实际受到伤害时显示）
                if hasattr(self, 'game') and self.game:
                    damage_text = DamageText(
                        self.坐标_x + self.宽 // 2,
                        self.坐标_y,
                        最终伤害值,
                        is_player=True
                    )
                    self.game.damage_texts.append(damage_text)
            
            # 播放受伤音效
            from 音频输出 import audio_manager
            try:
                audio_manager.play_sound("受击1")
            except:
                pass
            
            # 生成受伤粒子效果
            if hasattr(self, '世界') and hasattr(self.世界, '粒子'):
                for _ in range(5):
                    粒子_x = self.坐标_x + random.randint(0, self.宽)
                    粒子_y = self.坐标_y + random.randint(0, self.高)
                    粒子颜色 = (255, 0, 0)  # 红色
                    self.世界.粒子.append({
                        'x': 粒子_x,
                        'y': 粒子_y,
                        'vx': random.uniform(-3, 3),
                        'vy': random.uniform(-3, 3),
                        'color': 粒子颜色,
                        'life': random.uniform(0.5, 1.0),
                        'size': random.uniform(2, 4)
                    })
            
            # 设置受伤状态，用于播放受伤动画
            self.正在受伤 = True
            self.受伤动画时间 = 0
            
            # 打印伤害处理日志
            print(f"玩家受到伤害: 原始伤害={伤害值}, 总防御力={总防御力}, 免伤百分比={免伤百分比:.2f}%, 最终伤害={最终伤害值}, 初始额外生命值={初始额外生命值}, 初始当前生命值={初始当前生命值}, 最终额外生命值={self.extra_health}, 最终当前生命值={self.current_health}")
            
            # 如果生命值为0，触发死亡逻辑
            if self.current_health <= 0:
                self.die()
                return True  # 返回True表示死亡
        
        return False  # 返回False表示未死亡
    
    def die(self):
        """玩家死亡处理"""
        # 这里可以添加死亡动画、游戏结束逻辑等
        print("玩家死亡！")
        # 播放死亡音效
        from 音频输出 import audio_manager
        try:
            audio_manager.play_sound("死亡")
        except:
            pass


class ExpOrb:  # 经验小球类
    def __init__(self, world, x, y, exp_type):
        self.world = world
        self.x = x
        self.y = y
        self.size = 8
        self.type = exp_type  # 'green', 'blue', 'gold'
        self.life_time = 0
        self.max_life_time = 600  # 10秒后消失
        self.vel_x = random.uniform(-1, 1)
        self.vel_y = random.uniform(-2, -1)
        self.gravity = 0.1
        self.can_pickup = False  # 是否可以被拾取
        self.can_pickup_time = 50  # 生成后多久可以被拾取（帧数）
        
        # 设置颜色和经验值
        if exp_type == 'green':
            self.color = (0, 255, 0)
            self.value = 5
        elif exp_type == 'blue':
            self.color = (0, 0, 255)
            self.value = 10
        elif exp_type == 'gold':
            self.color = (255, 215, 0)
            self.value = 20
    
    def update(self, dt, player):
        # 更新生命周期
        self.life_time += 1
        
        # 检查是否可以被拾取
        if self.life_time >= self.can_pickup_time:
            self.can_pickup = True
        
        # 吸引到玩家
        if self.life_time > 100:  # 1.5秒后开始吸引
            player_center_x = player.坐标_x + player.宽 // 2
            player_center_y = player.坐标_y + player.高 // 2
            orb_center_x = self.x + self.size // 2
            orb_center_y = self.y + self.size // 2
            
            dx = player_center_x - orb_center_x
            dy = player_center_y - orb_center_y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # 使用与掉落物相同的碰撞检测方法
            if self.can_pickup and self.collides_with_player(player.坐标_x, player.坐标_y, player.宽, player.高):
                # 收集经验
                self.add_exp_to_player(player)
                return True  # 移除这个经验球
            elif distance < 100 and self.can_pickup:  # 100像素范围内开始吸引（只有可拾取时才吸引）
                attract_force = 0.2
                self.vel_x += (dx / distance) * attract_force
                self.vel_y += (dy / distance) * attract_force
        
        # 应用重力
        self.vel_y += self.gravity
        
        # 检查当前位置是否被方块占据（卡进方块） - 与掉落物系统一致的处理逻辑
        current_block_x = int(self.x // 方块大小)
        current_block_y = int(self.y // 方块大小)
        # 安全检查：确保世界高度和宽度不是None
        if hasattr(self.world, '高度') and hasattr(self.world, '宽度'):
            if self.world.高度 is not None and self.world.宽度 is not None:
                if 0 <= current_block_y < self.world.高度 and 0 <= current_block_x < self.world.宽度:
                    block_id = self.world.get_block(current_block_x, current_block_y)
                    if block_id != 空气:
                        # 经验球卡进了方块，向上推出
                        self.vel_y = -3  # 向上的速度
                        self.y = current_block_y * 方块大小 - self.size  # 直接放在方块上方
        
        # 垂直移动和方块碰撞检测
        # 计算底部位置
        bottom_y = self.y + self.size + self.vel_y
        # 检查底部是否碰到方块
        block_x = int((self.x + self.size // 2) // 方块大小)
        block_y = int(bottom_y // 方块大小)
        
        # 检查是否在世界范围内且方块不是空气
        if 0 <= block_y < self.world.高度:
            if self.world.get_block(block_x, block_y) != 空气:
                # 碰撞处理
                self.y = block_y * 方块大小 - self.size  # 设置位置在方块上方
                self.vel_y = -self.vel_y * 0.2  # 轻微反弹
                
                # 如果垂直速度很小，停止垂直移动
                if abs(self.vel_y) < 0.5:
                    self.vel_y = 0
        
        # 水平移动和方块碰撞检测
        next_x = self.x + self.vel_x
        left_block_x = int(next_x // 方块大小)
        right_block_x = int((next_x + self.size) // 方块大小)
        block_y_mid = int((self.y + self.size // 2) // 方块大小)
        
        # 检查左右是否碰到方块
        collision_left = (0 <= block_y_mid < self.world.高度 and 
                         self.world.get_block(left_block_x, block_y_mid) != 空气)
        collision_right = (0 <= block_y_mid < self.world.高度 and 
                          self.world.get_block(right_block_x, block_y_mid) != 空气)
        
        if collision_left:
            self.x = (left_block_x + 1) * 方块大小
            self.vel_x = -self.vel_x * 0.2
        elif collision_right:
            self.x = right_block_x * 方块大小 - self.size
            self.vel_x = -self.vel_x * 0.2
        else:
            # 应用水平速度
            self.x += self.vel_x
        
        # 应用垂直速度
        if self.vel_y != 0:
            self.y += self.vel_y
        
        # 添加摩擦力
        self.vel_x *= 0.95
        
        # 检查是否过期
        if self.life_time > self.max_life_time:
            return True
        
        return False
    
    def collides_with_player(self, player_x, player_y, player_width=32, player_height=64):
        """检查是否与玩家碰撞，与掉落物使用相同的碰撞检测方式"""
        return (self.x < player_x + player_width and
                self.x + self.size > player_x and
                self.y < player_y + player_height and
                self.y + self.size > player_y)
    
    def add_exp_to_player(self, player):
        # 添加经验到玩家
        player.star_progress += self.value
        # 检查是否升级
        while player.star_progress >= 100:
            player.star_count += 1
            player.star_progress -= 100
    
    def draw(self, surface, camera_x, camera_y):
        # 绘制经验球
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # 基础圆形
        pygame.draw.circle(surface, self.color, 
                          (int(screen_x + self.size // 2), 
                           int(screen_y + self.size // 2)), 
                          self.size // 2)
        
        # 闪光效果
        flash_size = max(1, int(self.size / 4))
        flash_offset = self.size // 4
        pygame.draw.circle(surface, (255, 255, 255), 
                          (int(screen_x + flash_offset), 
                           int(screen_y + flash_offset)), 
                          flash_size)

class ItemEntity:  # 掉落物实体类
    """掉落物实体，用于处理物品在世界中的物理行为"""
    def __init__(self, world, x, y, item_id, count=1, is_special=False, special_type=None):
        self.world = world
        self.x = x  # 世界坐标x
        self.y = y  # 世界坐标y
        self.item_id = item_id  # 物品ID
        self.count = count  # 物品数量
        self.velocity_x = 0  # 初始水平速度为0，不左右移动
        self.velocity_y = random.uniform(0, 1)  # 初始垂直速度（直接向下）
        self.gravity = 0.2  # 重力加速度
        self.friction = 0.9  # 摩擦力
        self.bounce = 0.4  # 弹性系数
        self.lifetime = 0  # 存活时间
        self.max_lifetime = 60  # 最大存活时间（秒）
        self.can_pickup = False  # 是否可以被拾取
        self.can_pickup_time = 0.5  # 生成后多久可以被拾取（秒）
        self.animation_offset = 0  # 动画偏移量
        self.animation_speed = 0.1  # 动画速度
        self.is_special = is_special  # 是否是特殊掉落物
        self.special_type = special_type  # 特殊掉落物类型
        self.target_player = None  # 目标玩家
        self.special_speed = 0.5  # 特殊掉落物移动速度
        # 特效相关属性
        self.trail = []  # 拖尾效果
        self.max_trail_length = 10  # 最大拖尾长度
        self.glow_color = (255, 0, 0)  # 发光颜色
        self.glow_intensity = 1.0  # 发光强度
    
    def update(self, dt):
        """更新掉落物状态"""
        self.lifetime += dt
        
        # 更新动画
        self.animation_offset = math.sin(self.lifetime * 5) * 3  # 上下浮动动画
        
        # 检查是否可以被拾取
        if self.lifetime >= self.can_pickup_time:
            self.can_pickup = True
        
        # 如果是特殊掉落物，使用特殊移动逻辑
        if self.is_special and self.special_type == "death_sickle" and self.target_player:
            # 无视重力和碰撞，直接向玩家移动
            # 计算到玩家的方向
            dx = self.target_player.坐标_x + self.target_player.宽 // 2 - (self.x + 8)
            dy = self.target_player.坐标_y + self.target_player.高 // 2 - (self.y + 8)
            distance = math.hypot(dx, dy)
            
            if distance > 0:
                # 归一化方向向量
                dir_x = dx / distance
                dir_y = dy / distance
                
                # 向玩家移动
                self.x += dir_x * self.special_speed
                self.y += dir_y * self.special_speed
            
            # 更新拖尾效果
            self.trail.append((self.x, self.y))
            if len(self.trail) > self.max_trail_length:
                self.trail.pop(0)
            return  # 跳过普通物理逻辑
        
        # 更新速度（应用重力）
        self.velocity_y += self.gravity
        
        # 检查当前位置是否被方块占据（卡进方块）
        current_block_x = int(self.x // 方块大小)
        current_block_y = int(self.y // 方块大小)
        # 安全检查：确保世界高度和宽度不是None
        if hasattr(self.world, '高度') and hasattr(self.world, '宽度'):
            if self.world.高度 is not None and self.world.宽度 is not None:
                if 0 <= current_block_y < self.world.高度 and 0 <= current_block_x < self.world.宽度:
                    if self.world.get_block(current_block_x, current_block_y) != 空气:
                        # 掉落物卡进了方块，向上推出
                        self.velocity_y = -3  # 向上的速度
                        self.y = current_block_y * 方块大小 - 16  # 直接放在方块上方
        
        # 水平移动和碰撞检测
        # 计算水平位置
        next_x = self.x + self.velocity_x
        # 检查左右是否碰到方块
        left_block_x = int(next_x // 方块大小)
        right_block_x = int((next_x + 16) // 方块大小)
        block_y_mid = int((self.y + 8) // 方块大小)
        
        # 检查左侧碰撞
        if hasattr(self.world, '高度') and self.world.高度 is not None:
            if 0 <= block_y_mid < self.world.高度:
                if self.world.get_block(left_block_x, block_y_mid) != 空气:
                    self.x = (left_block_x + 1) * 方块大小
                    self.velocity_x = -self.velocity_x * self.bounce
        # 检查右侧碰撞（使用if而不是elif，确保两边都检查）
        if hasattr(self.world, '高度') and self.world.高度 is not None:
            if 0 <= block_y_mid < self.world.高度:
                if self.world.get_block(right_block_x, block_y_mid) != 空气:
                    self.x = right_block_x * 方块大小 - 16
                    self.velocity_x = -self.velocity_x * self.bounce
        else:
            # 应用水平速度
            self.x += self.velocity_x
        
        # 垂直移动和碰撞检测
        # 计算底部位置
        bottom_y = self.y + 16 + self.velocity_y
        # 检查底部是否碰到方块
        block_x = int(self.x // 方块大小)
        block_y = int(bottom_y // 方块大小)
        
        # 检查是否在世界范围内且方块不是空气
        if hasattr(self.world, '高度') and self.world.高度 is not None:
            if 0 <= block_y < self.world.高度:
                if self.world.get_block(block_x, block_y) != 空气:
                    # 碰撞处理
                    self.y = block_y * 方块大小 - 16  # 设置位置在方块上方
                    self.velocity_y = -self.velocity_y * self.bounce  # 反弹
                    
                    # 如果垂直速度很小，停止垂直移动
                    if abs(self.velocity_y) < 0.5:
                        self.velocity_y = 0
        
        # 应用垂直速度
        self.y += self.velocity_y
    
    def draw(self, surface, camera_x, camera_y):
        """绘制掉落物"""
        # 计算屏幕位置
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y + self.animation_offset)
        
        # 如果是特殊掉落物，绘制特效
        if self.is_special and self.special_type == "death_sickle":
            # 绘制拖尾效果
            for i, pos in enumerate(self.trail):
                trail_screen_x = int(pos[0] - camera_x)
                trail_screen_y = int(pos[1] - camera_y + self.animation_offset)
                # 拖尾透明度逐渐降低
                alpha = 255 * (i + 1) / len(self.trail)
                # 拖尾大小逐渐减小
                scale = (i + 1) / len(self.trail)
                trail_size = int(18 * scale)
                
                # 绘制拖尾
                pygame.draw.circle(surface, (*self.glow_color, int(alpha)), 
                                 (trail_screen_x + 9, trail_screen_y + 9), trail_size // 2)
            
            # 绘制发光效果
            glow_surface = pygame.Surface((36, 36), pygame.SRCALPHA)
            # 绘制外圈发光
            for i in range(5, 0, -1):
                alpha = 50 / i
                radius = 18 + i * 2
                pygame.draw.circle(glow_surface, (*self.glow_color, int(alpha)), 
                                 (18, 18), radius)
            # 绘制内圈发光
            pygame.draw.circle(glow_surface, (*self.glow_color, 100), (18, 18), 18)
            # 绘制到主表面
            surface.blit(glow_surface, (screen_x - 9, screen_y - 9))
        
        # 从图片加载器获取物品图片
        item_image = None
        try:
            # 尝试使用图片加载器加载图片（通过全局图片管理器）
            if 图片管理器 is not None:
                # 使用图片加载器的获取物品图片方法，指定尺寸为18x18（缩小25%）
                item_image = 图片管理器.获取物品图片(self.item_id, 尺寸=(18, 18))
                
                # 如果图片管理器未能提供图片，尝试直接从字典获取
                if item_image is None and hasattr(图片管理器, '图片字典'):
                    # 尝试将item_id转换为字符串作为图片名
                    item_id_str = str(self.item_id)
                    if item_id_str in 图片管理器.图片字典:
                        item_image = 图片管理器.图片字典[item_id_str]
                        # 手动缩放图片，缩小25%
                        item_image = pygame.transform.scale(item_image, (18, 18))
        except Exception as e:
            # 记录错误但不中断程序
            print(f"加载掉落物图片失败 (ID: {self.item_id}): {str(e)}")
        
        # 绘制掉落物（尺寸为18x18，缩小25%）
        if item_image:
            # 有图片时直接绘制
            surface.blit(item_image, (screen_x, screen_y))
        else:
            # 只有在图片加载失败时才使用色块作为备用方案
            print(f"警告: 未能加载掉落物图片 (ID: {self.item_id}), 使用默认色块")
            item_id_str = str(self.item_id)
            color = (hash(self.item_id) % 256, hash(item_id_str + "1") % 256, hash(item_id_str + "2") % 256)
            pygame.draw.rect(surface, color, (screen_x, screen_y, 18, 18))
        
        # 绘制物品数量（如果大于1）在右上角
        if self.count > 0:
            font = pygame.font.SysFont(None, 14)  # 字体大小也适当缩小
            text = font.render(str(self.count), True, (255, 255, 255))  # 白色文字
            # 计算右上角位置（适配新尺寸）
            text_x = screen_x + 18 - text.get_width() - 2
            text_y = screen_y + 2
            # 只显示数字，不显示背景
            surface.blit(text, (text_x, text_y))
    
    def collides_with_player(self, player_x, player_y, player_width=32, player_height=64):
        """检查是否与玩家碰撞"""
        return (self.x < player_x + player_width and
                self.x + 16 > player_x and
                self.y < player_y + player_height and
                self.y + 16 > player_y)
    
    def should_despawn(self):
        """检查是否应该消失"""
        return self.lifetime > self.max_lifetime

# 区块类，用于存储单个区块的地形数据
class Chunk:
    def __init__(self, chunk_x, chunk_y, world):
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.world = world
        self.宽度 = CHUNK_SIZE
        self.高度 = world.高度
        self.方块 = [[空气 for _ in range(self.宽度)] for _ in range(self.高度)]
        self.generated = False  # 标记是否已生成地形
        
    def generate_terrain(self):
        """生成此区块的地形"""
        if self.generated:
            return
        
        # 导入地形生成器
        from 地形生成 import 生成地形
        
        # 获取上一个区块的结束高度作为初始高度
        初始高度 = None
        if self.chunk_x > 0 and (self.chunk_x - 1) in self.world.区块结束高度:
            初始高度 = self.world.区块结束高度[self.chunk_x - 1]
        
        # 根据世界类型生成不同的地形
        if self.world.世界类型 == "平坦世界":
            # 平坦世界，生成平坦地形
            区块方块数组, 结束高度 = 生成地形(self.宽度, self.高度, "平坦世界", self.world.无限世界, 初始高度)
        else:
            # 随机世界，生成混合地形
            区块方块数组, 结束高度 = 生成地形(self.宽度, self.高度, "混合", self.world.无限世界, 初始高度)
        
        # 将生成的地形复制到区块方块数组中
        for y in range(self.高度):
            for local_x in range(self.宽度):
                self.方块[y][local_x] = 区块方块数组[y][local_x]
        
        # 保存当前区块的结束高度，供下一个区块使用
        self.world.区块结束高度[self.chunk_x] = 结束高度
        
        self.generated = True

# 世界类 - 核心地形生成
class World:
    """世界类 - 核心地形生成"""
    def __init__(self, 宽度, 高度, 世界类型="随机世界", 无限世界=False):
        self.高度 = 高度
        self.世界类型 = 世界类型
        self.无限世界 = 无限世界
        self.时间_of_day = 600  # 早上6点
        self.时间更新系数 = 10  # 这个系数决定了游戏一天的时长为3600秒
        self.神秘音乐已播放 = False  # 标记当天是否已播放神秘音乐
        self.今天已保存 = False  # 标记当天是否已保存数据
        self.items = []  # 存储掉落物实体列表
        self.exp_orbs = []  # 存储经验小球列表
        self.粒子 = []  # 存储粒子效果列表
        self.mobs = []  # 存储生物列表
        
        # 初始化区块数据
        self.chunks = {}  # 存储区块数据的字典，键为(chunk_x, chunk_y)
        self.区块结束高度 = {}  # 存储每个区块的结束高度，键为chunk_x
        
        # 生成初始地形
        if not 无限世界:
            # 限制世界大小，生成固定宽度的地形
            self.宽度 = 宽度
            self.generate_limited_terrain()
        else:
            # 无限世界，宽度设置为None
            self.宽度 = None
        
        # 初始化云数据
        self.clouds = []
        # 不在这里生成云群，而是在update_clouds方法中生成，这样可以使用玩家的实际位置
        
    def get_chunk_key(self, x, y):
        """获取区块坐标的键"""
        chunk_x = x // CHUNK_SIZE
        chunk_y = y // CHUNK_SIZE
        return (chunk_x, chunk_y)
    
    def get_chunk(self, chunk_x, chunk_y):
        """获取指定区块，如果不存在则创建 - 优化版"""
        chunk_key = (chunk_x, chunk_y)
        if chunk_key not in self.chunks:
            # 优化1：限制同时生成的区块数量，避免一次性生成过多区块
            if len(self.chunks) >= 50:  # 限制最多50个区块，减少内存占用和生成负担
                # 返回空气区块，不生成新地形
                chunk = Chunk(chunk_x, chunk_y, self)
                # 不生成地形，直接返回空区块
                self.chunks[chunk_key] = chunk
                return chunk
            
            # 创建新区块
            chunk = Chunk(chunk_x, chunk_y, self)
            
            # 优化2：只有在玩家附近的区块才生成完整地形
            if hasattr(self, '玩家') and self.玩家 is not None:
                player_chunk_x = int(self.玩家.坐标_x // (CHUNK_SIZE * 方块大小))
                # 只在玩家周围6个区块范围内生成完整地形
                if abs(chunk_x - player_chunk_x) <= 6:
                    # 生成地形
                    chunk.generate_terrain()
                # 否则不生成地形，直接使用空区块
            else:
                # 没有玩家时，生成完整地形
                chunk.generate_terrain()
                
            self.chunks[chunk_key] = chunk
        return self.chunks[chunk_key]
    
    def get_block(self, x, y):
        """获取指定位置的方块"""
        # 如果是有限世界，检查坐标是否超出范围
        if not self.无限世界:
            if x < 0 or x >= self.宽度 or y < 0 or y >= self.高度:
                return 空气
        else:
            if y < 0 or y >= self.高度:
                return 空气
        
        # 获取区块
        chunk_x = x // CHUNK_SIZE
        chunk_y = 0  # y轴方向只有一个区块
        chunk = self.get_chunk(chunk_x, chunk_y)
        
        # 获取区块内的本地坐标
        local_x = x % CHUNK_SIZE
        
        # 返回方块
        return chunk.方块[y][local_x]
    
    def set_block(self, x, y, block_type):
        """设置指定位置的方块"""
        # 如果是有限世界，检查坐标是否超出范围
        if not self.无限世界:
            if x < 0 or x >= self.宽度 or y < 0 or y >= self.高度:
                return
            # 同时更新有限世界的self.方块数据
            self.方块[y][x] = block_type
        else:
            if y < 0 or y >= self.高度:
                return
        
        # 获取区块
        chunk_x = x // CHUNK_SIZE
        chunk_y = 0  # y轴方向只有一个区块
        chunk = self.get_chunk(chunk_x, chunk_y)
        
        # 获取区块内的本地坐标
        local_x = x % CHUNK_SIZE
        
        # 设置区块内的方块数据
        chunk.方块[y][local_x] = block_type
    
    def check_and_remove_floating_grass(self):
        """检查并删除悬空的植物，包括各种植物的生长阶段"""
        # 定义需要检查的植物类型列表，包括所有植物生长阶段
        plants_to_check = [
            # 基础植物
            草, 红花, 灌木, 枯草, 仙人掌,
            # 土豆植物
            土豆发芽, 土豆幼年, 土豆成年,
            # 小麦植物
            小麦发芽, 小麦幼年, 小麦成年,
            # 水稻植物
            水稻发芽, 水稻幼年, 水稻成熟,
            # 玉米植物
            玉米发芽, 玉米幼年, 玉米成年,
            # 甘蔗植物
            甘蔗幼年, 甘蔗成年,
            # 番薯植物
            番薯发芽, 番薯幼年, 番薯成年,
            # 白菜植物
            白菜发芽, 白菜幼年, 白菜成年
        ]
        
        # 定义允许的支撑方块类型（土块和草方块）
        allowed_support_blocks = [土块, 草方块]
        
        # 定义水稻植物类型列表
        rice_plants = [水稻发芽, 水稻幼年, 水稻成熟]
        
        # 定义沙漠植物类型列表（仙人掌和枯草）
        desert_plants = [枯草, 仙人掌]
        
        # 遍历所有已生成的区块
        for chunk_key, chunk in self.chunks.items():
            chunk_x, chunk_y = chunk_key
            # 遍历区块内的所有方块
            for y in range(self.高度):
                for x in range(CHUNK_SIZE):
                    # 计算世界坐标
                    world_x = chunk_x * CHUNK_SIZE + x
                    # 获取当前方块类型
                    current_block = chunk.方块[y][x]
                    # 处理所有需要检查的植物类型
                    if current_block in plants_to_check:
                        # 检查正下方是否有支撑方块
                        has_support = False
                        if y + 1 < self.高度:
                            # 获取下方方块
                            below_block = self.get_block(world_x, y + 1)
                            
                            # 检查当前植物是否为水稻
                            if current_block in rice_plants:
                                # 水稻必须生长在水面上
                                if below_block == 水:
                                    has_support = True
                            # 检查当前植物是否为沙漠植物（仙人掌和枯草）
                            elif current_block in desert_plants:
                                # 沙漠植物可以生长在土块、草方块、沙子上，或者同类型的沙漠植物上
                                if below_block in allowed_support_blocks or below_block == 沙子 or below_block == current_block:
                                    has_support = True
                            else:
                                # 其他植物必须生长在土块或草方块上
                                if below_block in allowed_support_blocks:
                                    has_support = True
                        
                        # 如果没有支撑，删除植物
                        if not has_support:
                            self.set_block(world_x, y, 空气)
    
    def generate_limited_terrain(self):
        """生成有限大小的地形"""
        # 初始化方块数据，用于有限世界
        self.方块 = [[空气 for _ in range(self.宽度)] for _ in range(self.高度)]
        
        # 生成地形
        if self.世界类型 == "平坦世界":
            # 平坦世界
            self.generate_flat_terrain()
        else:  # 随机世界
            self.generate_random_terrain()
        
        # 同时将有限世界的数据转换为区块，以便后续可以无缝切换到无限世界逻辑
        chunks_needed = (self.宽度 + CHUNK_SIZE - 1) // CHUNK_SIZE
        for chunk_x in range(chunks_needed):
            chunk = self.get_chunk(chunk_x, 0)
            # 将有限世界的方块数据复制到对应区块
            for local_x in range(CHUNK_SIZE):
                world_x = chunk_x * CHUNK_SIZE + local_x
                if world_x < self.宽度:
                    for y in range(self.高度):
                        chunk.方块[y][local_x] = self.方块[y][world_x]
            chunk.generated = True
    
    def generate_clouds(self):
        """生成初始云群，在玩家附近生成 - 优化版"""
        # 根据时间生成不同密度的云
        cloud_density = self.get_cloud_density()
        
        # 优化：大幅减少云的数量，降低性能消耗
        cloud_count = int(3 + (cloud_density * 10))  # 基础3朵云，根据密度最多增加10朵
        
        # 获取玩家位置
        player_x = getattr(self, '玩家', None) and getattr(self.玩家, '坐标_x', 0) or 0
        
        # 生成云的位置、大小和移动速度
        for i in range(cloud_count):
            # 优化：限制最大云数量为20朵，大幅降低渲染负担
            if len(self.clouds) >= 20:  # 减少最大云数量
                break
                
            # 云在玩家附近生成，范围为玩家左侧500px到右侧1500px
            cloud_x = random.randint(int(player_x - 500), int(player_x + 1500))
                
            cloud = {
                'x': cloud_x,  # 在玩家附近生成
                'y': random.randint(30, 280),  # 扩大Y轴分布范围
                'width': random.randint(60, 120),  # 减小云的宽度
                'height': random.randint(30, 70),   # 减小云的高度
                'speed': random.uniform(0.08, 0.35) * cloud_density,  # 调整速度范围
                'opacity': random.uniform(0.65, 0.9)  # 稍微降低透明度，让云更明显
            }
            self.clouds.append(cloud)
        

    
    def get_cloud_density(self):
        """根据时间获取云的密度（0.0-1.0）"""
        小时 = self.时间_of_day // 100
        分钟 = self.时间_of_day % 100
        
        # 不同时间段的云密度 - 全面提高云密度
        if 6 <= 小时 < 9:  # 早晨 - 增加云量
            return 0.85
        elif 9 <= 小时 < 12:  # 上午 - 较多云量
            return 0.7
        elif 12 <= 小时 < 15:  # 中午 - 中等云量
            return 0.6
        elif 15 <= 小时 < 18:  # 下午 - 较多云量
            return 0.75
        elif 18 <= 小时 < 20:  # 傍晚 - 很多云量
            return 0.9
        else:  # 晚上和深夜 - 增加夜间云量
            return 0.4
    
    def update_clouds(self, dt):
        """更新云的位置和动态生成，只在玩家附近生成和保留云 - 优化版"""
        # 检查云密度是否需要更新
        current_density = self.get_cloud_density()
        
        # 优化：大幅减少目标云数量，降低性能消耗
        target_count = int(3 + (current_density * 10))
        
        # 获取玩家位置
        player_x = getattr(self, '玩家', None) and getattr(self.玩家, '坐标_x', 0) or 0
        
        # 如果云太少，添加新云，在玩家左侧生成
        while len(self.clouds) < target_count and len(self.clouds) < 20:  # 减少最大云数量到20朵
            cloud = {
                'x': player_x - random.randint(500, 800),  # 从玩家左侧500-800px进入
                'y': random.randint(30, 280),  # 扩大Y轴分布范围
                'width': random.randint(60, 120),  # 减小云的宽度
                'height': random.randint(30, 70),   # 减小云的高度
                'speed': random.uniform(0.08, 0.35) * current_density,  # 调整速度范围
                'opacity': random.uniform(0.65, 0.9)  # 调整透明度
            }
            self.clouds.append(cloud)
        
        # 更新云的位置并移除距离玩家太远的云
        new_clouds = []
        for cloud in self.clouds:
            cloud['x'] += cloud['speed'] * dt * 60  # 更新云的位置
            
            # 只保留在玩家附近范围内的云
            # 玩家左侧3000px到右侧3000px范围内
            if player_x - 3000 <= cloud['x'] <= player_x + 3000:
                new_clouds.append(cloud)
        
        self.clouds = new_clouds
    
    def draw_clouds(self, 屏幕, 相机_x, 相机_y):
        """绘制云群"""
        # 获取当前屏幕的实际大小
        current_width, current_height = 屏幕.get_size()
        
        # 创建透明表面用于绘制云，使用当前屏幕大小
        cloud_surface = pygame.Surface((current_width, current_height), pygame.SRCALPHA)
        
        # 如果没有云，生成一些调试云
        if not self.clouds:
            # 生成5朵调试云
            for i in range(5):
                cloud = {
                    'x': self.玩家.坐标_x + (i - 2) * 200,  # 在玩家附近生成
                    'y': random.randint(50, 200),
                    'width': 100,
                    'height': 50,
                    'speed': 0.1,
                    'opacity': 0.8
                }
                self.clouds.append(cloud)
        
        # 绘制每朵云
        for cloud in self.clouds:
            # 计算云在屏幕上的位置
            draw_x = cloud['x'] - 相机_x
            draw_y = cloud['y'] - 相机_y
            
            # 如果云在屏幕范围内，使用当前屏幕大小
            if -cloud['width'] <= draw_x <= current_width and -cloud['height'] <= draw_y <= current_height:
                # 绘制多层椭圆来模拟云的形状
                # 基础层
                pygame.draw.ellipse(cloud_surface, 
                                   (255, 255, 255, int(255 * cloud['opacity'])), 
                                   (draw_x, draw_y, cloud['width'], cloud['height']))
                
                # 增加云朵的层次感
                pygame.draw.ellipse(cloud_surface, 
                                   (255, 255, 255, int(255 * cloud['opacity'] * 0.8)), 
                                   (draw_x + cloud['width'] * 0.2, draw_y - cloud['height'] * 0.3, 
                                    cloud['width'] * 0.6, cloud['height'] * 0.8))
                
                pygame.draw.ellipse(cloud_surface, 
                                   (255, 255, 255, int(255 * cloud['opacity'] * 0.7)), 
                                   (draw_x - cloud['width'] * 0.1, draw_y - cloud['height'] * 0.1, 
                                    cloud['width'] * 0.5, cloud['height'] * 0.7))
        
        # 将云表面绘制到主屏幕
        屏幕.blit(cloud_surface, (0, 0))
    
    def draw_sun_moon(self, 屏幕):
        """绘制太阳和月亮"""
        # 绘制太阳
        sun_pos = (self.时间_of_day - 600) / 1200 * 宽度  # 太阳从早上6点到晚上6点移动
        
        # 根据时间调整太阳位置和颜色
        if 600 <= self.时间_of_day < 1800:  # 白天显示太阳
            # 太阳颜色在日落时会变成橙黄色
            if 1500 <= self.时间_of_day < 1800:  # 日落时段
                color_intensity = 1.0 - (self.时间_of_day - 1500) / 300
                sun_color = (255, int(255 * color_intensity), 0)
                # 太阳周围的光晕
                halo_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
                pygame.draw.circle(halo_surface, (255, 220, 100, 50), (100, 100), 50)
                pygame.draw.circle(halo_surface, (255, 230, 150, 30), (100, 100), 70)
                屏幕.blit(halo_surface, (sun_pos - 100, 50))
            else:
                sun_color = (255, 255, 0)
            
            pygame.draw.circle(屏幕, sun_color, (int(sun_pos), 100), 30)
        
        # 绘制月亮
        moon_pos = ((self.时间_of_day + 600) % 2400) / 2400 * 宽度  # 月亮从晚上6点到早上6点移动
        
        # 只有在夜晚才显示月亮
        if self.时间_of_day < 600 or self.时间_of_day >= 1800:
            # 月亮颜色
            moon_color = (220, 220, 240)
            
            # 月亮的光晕
            if self.时间_of_day >= 1800:  # 刚入夜时
                intensity = min(1.0, (self.时间_of_day - 1800) / 200)
            else:  # 黎明前
                intensity = min(1.0, (600 - self.时间_of_day) / 200)
            
            if intensity > 0:
                halo_surface = pygame.Surface((150, 150), pygame.SRCALPHA)
                pygame.draw.circle(halo_surface, (220, 220, 240, int(30 * intensity)), (75, 75), 40)
                屏幕.blit(halo_surface, (int(moon_pos) - 75, 75))
            
            # 绘制月亮
            pygame.draw.circle(屏幕, moon_color, (int(moon_pos), 100), 25)
            
            # 添加月亮上的灰色区域，模拟月海
            pygame.draw.circle(屏幕, (200, 200, 220), (int(moon_pos) + 3, 100 - 3), 10)
            pygame.draw.circle(屏幕, (200, 200, 220), (int(moon_pos) - 5, 105), 8)
    
    def generate_terrain(self):
        """生成基础地形"""
        if self.世界类型 == "平坦世界":
            self.generate_flat_terrain()
        else:  # 随机世界
            self.generate_random_terrain()
    
    def save_terrain_data(self, 存档名称):
        """保存地形数据到指定存档文件夹
        
        参数:
            存档名称: 存档的名称，用于创建文件夹路径
        """
        try:
            # 获取代码文件所在目录
            import os
            代码目录 = os.path.dirname(os.path.abspath(__file__))
            # 构建存档文件夹路径：代码目录/存档/存档名称/主世界地形数据/
            存档根目录 = os.path.join(代码目录, "存档")
            存档文件夹 = os.path.join(存档根目录, 存档名称)
            地形数据文件夹 = os.path.join(存档文件夹, "主世界地形数据")
            
            # 确保文件夹存在
            os.makedirs(地形数据文件夹, exist_ok=True)
            
            # 构建地形数据文件路径
            地形数据文件 = os.path.join(地形数据文件夹, "地形数据.json")
            
            # 准备要保存的数据
            地形数据 = {
                "世界宽度": self.宽度,
                "世界高度": self.高度,
                "世界类型": self.世界类型,
                "无限世界": self.无限世界,
                "地形数据": []
            }
            
            # 根据世界类型保存不同格式的数据
            if self.无限世界:
                # 无限世界，保存区块数据
                区块列表 = []
                for chunk_key, chunk in self.chunks.items():
                    chunk_x, chunk_y = chunk_key
                    # 只保存已生成的区块
                    if chunk.generated:
                        区块数据 = {
                            "chunk_x": chunk_x,
                            "chunk_y": chunk_y,
                            "方块数据": chunk.方块
                        }
                        区块列表.append(区块数据)
                地形数据["区块数据"] = 区块列表
            else:
                # 有限世界，直接保存方块数据
                地形数据["方块数据"] = self.方块
            
            # 保存数据到JSON文件
            with open(地形数据文件, "w", encoding="utf-8") as f:
                json.dump(地形数据, f, ensure_ascii=False, indent=4)
            
            print(f"地形数据已成功保存到: {地形数据文件}")
        except Exception as e:
            print(f"保存地形数据时出错: {str(e)}")
    
    def save_game_data(self, 存档名称, 玩家对象, 游戏实例):
        """保存所有游戏数据到指定存档文件夹
        
        参数:
            存档名称: 存档的名称，用于创建文件夹路径
            玩家对象: 玩家实例，包含玩家数据
            游戏实例: 游戏主实例，包含背包、箱子等数据
        """
        try:
            # 检查是否处于创建存档模式
            if not getattr(游戏实例, '世界参数', {}).get('创建存档', False):
                print("=== 无存档模式，不保存游戏数据 ===")
                return True
                
            # 获取代码文件所在目录
            import os
            代码目录 = os.path.dirname(os.path.abspath(__file__))
            # 构建存档文件夹路径：代码目录/存档/存档名称/
            存档根目录 = os.path.join(代码目录, "存档")
            存档文件夹 = os.path.join(存档根目录, 存档名称)
            
            # 确保文件夹存在
            os.makedirs(存档文件夹, exist_ok=True)
            
            # 1. 保存地形数据（已实现）
            self.save_terrain_data(存档名称)
            
            # 2. 保存玩家数据
            玩家数据文件夹 = os.path.join(存档文件夹, "玩家数据")
            os.makedirs(玩家数据文件夹, exist_ok=True)
            
            # 准备玩家数据
            玩家数据 = {
                "坐标_x": 玩家对象.坐标_x,
                "坐标_y": 玩家对象.坐标_y,
                "生命值": 玩家对象.current_health,
                "最大生命值": 玩家对象.max_health,
                "饥饿值": 玩家对象.current_hunger,
                "最大饥饿值": 玩家对象.max_hunger,
                "经验值": getattr(玩家对象, '经验值', 0),
                "等级": getattr(玩家对象, '等级', 1),
                "角色外观": 玩家对象.角色外观,
                "飞行模式": 玩家对象.fly_mode,
                "创造模式": getattr(游戏实例, '创造模式', False)
            }
            
            # 保存玩家数据到JSON文件
            玩家数据文件 = os.path.join(玩家数据文件夹, "玩家数据.json")
            with open(玩家数据文件, "w", encoding="utf-8") as f:
                json.dump(玩家数据, f, ensure_ascii=False, indent=4)
            print(f"玩家数据已成功保存到: {玩家数据文件}")
            
            # 3. 保存背包数据
            if hasattr(玩家对象, '背包'):
                背包数据文件夹 = os.path.join(存档文件夹, "背包数据")
                os.makedirs(背包数据文件夹, exist_ok=True)
                
                背包数据 = {
                    "物品栏": getattr(玩家对象.背包, '物品栏', []),
                    "快捷栏": getattr(玩家对象.背包, '快捷栏', []),
                    "当前选中格子": getattr(游戏实例, '当前选中格子', 0)
                }
                
                背包数据文件 = os.path.join(背包数据文件夹, "背包数据.json")
                with open(背包数据文件, "w", encoding="utf-8") as f:
                    json.dump(背包数据, f, ensure_ascii=False, indent=4)
                print(f"背包数据已成功保存到: {背包数据文件}")
            
            # 4. 保存世界通用数据
            世界通用数据文件夹 = os.path.join(存档文件夹, "世界通用数据")
            os.makedirs(世界通用数据文件夹, exist_ok=True)
            
            世界通用数据 = {
                "时间_of_day": self.时间_of_day,
                "时间更新系数": self.时间更新系数,
                "神秘音乐已播放": self.神秘音乐已播放,
                "世界类型": self.世界类型,
                "无限世界": self.无限世界
            }
            
            世界通用数据文件 = os.path.join(世界通用数据文件夹, "世界通用数据.json")
            with open(世界通用数据文件, "w", encoding="utf-8") as f:
                json.dump(世界通用数据, f, ensure_ascii=False, indent=4)
            print(f"世界通用数据已成功保存到: {世界通用数据文件}")
            
            # 5. 保存生物数据
            生物数据文件夹 = os.path.join(存档文件夹, "生物数据")
            os.makedirs(生物数据文件夹, exist_ok=True)
            
            生物列表 = []
            for mob in self.mobs:
                生物数据 = {
                    "类型": getattr(mob, '类型', 'unknown'),
                    "坐标_x": mob.x,
                    "坐标_y": mob.y,
                    "生命值": getattr(mob, 'current_health', 100),
                    "最大生命值": getattr(mob, 'max_health', 100),
                    "方向": getattr(mob, 'direction', 'right'),
                    "是否在地面上": getattr(mob, '在地面上', True)
                }
                生物列表.append(生物数据)
            
            生物数据文件 = os.path.join(生物数据文件夹, "生物数据.json")
            with open(生物数据文件, "w", encoding="utf-8") as f:
                json.dump(生物列表, f, ensure_ascii=False, indent=4)
            print(f"生物数据已成功保存到: {生物数据文件}")
            
            # 6. 保存箱子数据
            if hasattr(游戏实例, '箱子'):
                箱子数据文件夹 = os.path.join(存档文件夹, "箱子数据")
                os.makedirs(箱子数据文件夹, exist_ok=True)
                
                箱子列表 = []
                for 箱子 in getattr(游戏实例, '箱子', []):
                    箱子数据 = {
                        "坐标_x": getattr(箱子, 'x', 0),
                        "坐标_y": getattr(箱子, 'y', 0),
                        "物品栏": getattr(箱子, '物品栏', [])
                    }
                    箱子列表.append(箱子数据)
                
                箱子数据文件 = os.path.join(箱子数据文件夹, "箱子数据.json")
                with open(箱子数据文件, "w", encoding="utf-8") as f:
                    json.dump(箱子列表, f, ensure_ascii=False, indent=4)
                print(f"箱子数据已成功保存到: {箱子数据文件}")
            
            # 7. 保存熔炉数据
            if hasattr(游戏实例, '熔炉'):
                熔炉数据文件夹 = os.path.join(存档文件夹, "熔炉数据")
                os.makedirs(熔炉数据文件夹, exist_ok=True)
                
                熔炉列表 = []
                for 熔炉 in getattr(游戏实例, '熔炉', []):
                    熔炉数据 = {
                        "坐标_x": getattr(熔炉, 'x', 0),
                        "坐标_y": getattr(熔炉, 'y', 0),
                        "燃料": getattr(熔炉, '燃料', 0),
                        "物品": getattr(熔炉, '物品', None),
                        "进度": getattr(熔炉, '进度', 0)
                    }
                    熔炉列表.append(熔炉数据)
                
                熔炉数据文件 = os.path.join(熔炉数据文件夹, "熔炉数据.json")
                with open(熔炉数据文件, "w", encoding="utf-8") as f:
                    json.dump(熔炉列表, f, ensure_ascii=False, indent=4)
                print(f"熔炉数据已成功保存到: {熔炉数据文件}")
            
            # 8. 保存投掷物数据
            投掷物数据文件夹 = os.path.join(存档文件夹, "投掷物数据")
            os.makedirs(投掷物数据文件夹, exist_ok=True)
            
            # 保存玩家箭矢数据
            箭矢列表 = []
            if hasattr(游戏实例, 'arrows'):
                for arrow in getattr(游戏实例, 'arrows', []):
                    箭矢数据 = {
                        "x": arrow.x,
                        "y": arrow.y,
                        "width": arrow.width,
                        "height": arrow.height,
                        "damage": arrow.damage,
                        "owner": getattr(arrow, 'owner', None),
                        "weapon_type": arrow.weapon_type,
                        "velocity_x": arrow.velocity_x,
                        "velocity_y": arrow.velocity_y,
                        "angle": arrow.angle,
                        "lifetime": arrow.lifetime
                    }
                    箭矢列表.append(箭矢数据)
            
            箭矢数据文件 = os.path.join(投掷物数据文件夹, "箭矢数据.json")
            with open(箭矢数据文件, "w", encoding="utf-8") as f:
                json.dump(箭矢列表, f, ensure_ascii=False, indent=4)
            print(f"箭矢数据已成功保存到: {箭矢数据文件}")
            
            # 9. 保存状态管理器数据
            状态数据文件夹 = os.path.join(存档文件夹, "状态数据")
            os.makedirs(状态数据文件夹, exist_ok=True)
            
            try:
                from 状态管理 import 状态管理器实例
                状态数据 = {
                    "是否无敌": 状态管理器实例.是否无敌(),
                    "无敌剩余时间": 状态管理器实例.获取无敌状态()[1],
                    "是否燃烧": 状态管理器实例.是否燃烧(),
                    "燃烧剩余时间": 状态管理器实例.获取燃烧状态()[1],
                    "是否饥饿": 状态管理器实例.是否饥饿(),
                    "饥饿剩余时间": 状态管理器实例.获取饥饿状态()[1]
                }
                
                状态数据文件 = os.path.join(状态数据文件夹, "状态数据.json")
                with open(状态数据文件, "w", encoding="utf-8") as f:
                    json.dump(状态数据, f, ensure_ascii=False, indent=4)
                print(f"状态数据已成功保存到: {状态数据文件}")
            except Exception as e:
                print(f"保存状态数据失败: {str(e)}")
            
            # 10. 保存武器技能管理器数据
            技能数据文件夹 = os.path.join(存档文件夹, "技能数据")
            os.makedirs(技能数据文件夹, exist_ok=True)
            
            try:
                from 武器处理 import 武器技能管理器实例
                技能数据 = {
                    "技能冷却时间": 武器技能管理器实例.cooldowns,
                    "已解锁技能": getattr(武器技能管理器实例, 'unlocked_skills', []),
                    "技能使用次数": getattr(武器技能管理器实例, 'skill_usage_count', {})
                }
                
                技能数据文件 = os.path.join(技能数据文件夹, "技能数据.json")
                with open(技能数据文件, "w", encoding="utf-8") as f:
                    json.dump(技能数据, f, ensure_ascii=False, indent=4)
                print(f"技能数据已成功保存到: {技能数据文件}")
            except Exception as e:
                print(f"保存技能数据失败: {str(e)}")
            
            # 11. 保存背包管理器数据
            背包管理器数据文件夹 = os.path.join(存档文件夹, "背包管理器数据")
            os.makedirs(背包管理器数据文件夹, exist_ok=True)
            
            if hasattr(游戏实例, '背包管理器'):
                背包管理器实例 = getattr(游戏实例, '背包管理器')
                背包管理器数据 = {
                    "物品栏": getattr(背包管理器实例, '物品栏', []),
                    "快捷栏": getattr(背包管理器实例, '快捷栏', []),
                    "当前选中格子": getattr(背包管理器实例, '当前选中格子', 0)
                }
                
                背包管理器数据文件 = os.path.join(背包管理器数据文件夹, "背包管理器数据.json")
                with open(背包管理器数据文件, "w", encoding="utf-8") as f:
                    json.dump(背包管理器数据, f, ensure_ascii=False, indent=4)
                print(f"背包管理器数据已成功保存到: {背包管理器数据文件}")
            
            # 12. 保存合成页面数据
            合成页面数据文件夹 = os.path.join(存档文件夹, "合成页面数据")
            os.makedirs(合成页面数据文件夹, exist_ok=True)
            
            if hasattr(游戏实例, 'crafting_system'):
                合成页面实例 = getattr(游戏实例, 'crafting_system')
                合成页面数据 = {
                    "已解锁配方": getattr(合成页面实例, '已解锁配方', []),
                    "当前选中分类": getattr(合成页面实例, '当前选中分类', "武器")
                }
                
                合成页面数据文件 = os.path.join(合成页面数据文件夹, "合成页面数据.json")
                with open(合成页面数据文件, "w", encoding="utf-8") as f:
                    json.dump(合成页面数据, f, ensure_ascii=False, indent=4)
                print(f"合成页面数据已成功保存到: {合成页面数据文件}")
            
            print(f"\n游戏数据已全部成功保存到存档: {存档名称}")
            return True
        except Exception as e:
            print(f"保存游戏数据时出错: {str(e)}")
            import traceback
            print(f"错误详情: {traceback.format_exc()}")
            return False
    
    def auto_save(self, 存档名称, 上次保存时间, 自动保存间隔=300):
        """自动保存世界数据
        
        参数:
            存档名称: 存档的名称
            上次保存时间: 上次保存的时间戳
            自动保存间隔: 自动保存的间隔时间（秒），默认5分钟
        
        返回:
            更新后的上次保存时间
        """
        当前时间 = time.time()
        if 当前时间 - 上次保存时间 >= 自动保存间隔:
            self.save_terrain_data(存档名称)
            return 当前时间
        return 上次保存时间
    
    def generate_flat_terrain(self):
        """生成平坦地形"""
        地表高度 = self.高度 // 2
        
        # 生成地表层
        for x in range(self.宽度):
            # 地表草方块
            self.方块[地表高度][x] = 草方块
            
            # 泥土层 (3层)
            for y in range(地表高度 + 1, 地表高度 + 4):
                if y < self.高度:
                    self.方块[y][x] = 土块
            
            # 石头层
            for y in range(地表高度 + 4, self.高度):
                if y < self.高度:
                    self.方块[y][x] = 岩石
        
        # 在平坦地形上随机生成一些树木
        for x in range(50, self.宽度 - 50, random.randint(15, 25)):
            if random.random() < 0.7:
                self.generate_tree(x, 地表高度)
    
    def generate_random_terrain(self):
        """使用新的地形生成器生成地形"""
        from 地形生成 import 生成地形
        
        # 随机选择地形类型
        地形类型列表 = ['森林', '草原', '高山', '沙漠', '雨林']
        选择的地形类型 = random.choice(地形类型列表)
        
        # 使用新的地形生成器生成地形
        区块方块数组, 结束高度 = 生成地形(self.宽度, self.高度, 选择的地形类型)
        # 只取方块数组部分
        self.方块 = 区块方块数组
    def generate_tree(self, x, 地表_y, tree_type="normal"):
        """生成树木，支持不同地形类型的树木生成
        
        参数:
            x: 树的x坐标
            地表_y: 地表的y坐标
            tree_type: 树木类型 (normal/rainforest)
        """
        
        # 根据树木类型调整树高度
        if tree_type == "rainforest":
            树高度 = random.randint(5, 7)  # 雨林树木更高
            树叶密度 = 0.9  # 更高的树叶密度
            树叶半径 = 3    # 更大的树冠
        else:  # 普通树木
            树高度 = random.randint(4, 6)
            树叶密度 = 0.8
            树叶半径 = 2
        
        # 树干
        for y in range(地表_y - 树高度, 地表_y):
            if 0 <= y < self.高度:
                self.方块[y][x] = 木头
        
        # 树叶
        中心_y = 地表_y - 树高度
        
        # 雨林树木有更大的树冠
        if tree_type == "rainforest":
            # 更大的树冠，底部有额外的树叶
            for dy in range(-树叶半径, 树叶半径 + 1):
                for dx in range(-树叶半径, 树叶半径 + 1):
                    # 更复杂的树叶形状，底部更广
                    distance = abs(dx) + abs(dy)
                    if distance <= 4 + min(0, dy):  # 底部更宽
                        nx, ny = x + dx, 中心_y + dy
                        # 额外的树叶层
                        if random.random() < 0.7 and 0 <= nx < self.宽度 and 0 <= ny < self.高度:
                            if self.方块[ny][nx] == 空气:  # 不覆盖已有方块
                                self.方块[ny][nx] = 树叶
            
            # 树干上方添加额外的树叶
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx, ny = x + dx, 地表_y - 1 + dy
                    if 0 <= nx < self.宽度 and 0 <= ny < self.高度:
                        if self.方块[ny][nx] == 空气 and random.random() < 0.6:
                            self.方块[ny][nx] = 树叶
        else:
            # 普通树木的菱形树叶形状
            for dy in range(-树叶半径, 树叶半径 + 1):
                for dx in range(-树叶半径, 树叶半径 + 1):
                    if abs(dx) + abs(dy) <= 3:  # 菱形树叶形状
                        nx, ny = x + dx, 中心_y + dy
                        if 0 <= nx < self.宽度 and 0 <= ny < self.高度:
                            if random.random() < 树叶密度 and self.方块[ny][nx] == 空气:
                                self.方块[ny][nx] = 树叶
    
    def get_sky_color(self):
        """根据时间获取天空颜色，每小时不同的背景色"""
        小时 = self.时间_of_day // 100
        分钟 = self.时间_of_day % 100
        
        # 为24小时中的每个小时定义不同的天空颜色
        小时颜色 = {
            0: (20, 20, 80),    # 深夜 - 深蓝色
            1: (18, 18, 70),    # 深夜 - 更深的蓝色
            2: (15, 15, 60),    # 深夜 - 最深的蓝色
            3: (15, 15, 70),    # 深夜 - 开始变亮
            4: (30, 30, 100),   # 黎明前 - 深蓝色带紫调
            5: (180, 160, 130), # 晨光 - 橙黄色调（类似黄昏但过渡更快）
            6: (120, 140, 200), # 早晨 - 淡蓝色
            7: (135, 180, 235), # 早晨 - 亮蓝色
            8: (145, 190, 240), # 上午 - 明亮蓝色
            9: (150, 200, 245), # 上午 - 浅蓝色
            10: (155, 210, 250), # 上午 - 亮蓝色
            11: (160, 215, 250), # 中午前 - 明亮蓝天
            12: (160, 215, 240), # 中午 - 略暗的蓝色
            13: (155, 210, 245), # 午后 - 类似上午
            14: (150, 200, 245), # 下午 - 保持明亮
            15: (145, 190, 240), # 下午 - 开始略微变暗
            16: (135, 180, 235), # 傍晚前 - 开始变化
            17: (210, 160, 110), # 傍晚 - 自然的橙黄色调
            18: (190, 120, 80),  # 黄昏 - 温暖的橙金色调
            19: (120, 80, 120),  # 黄昏 - 紫橙色过渡
            20: (80, 60, 100),   # 夜晚开始 - 蓝紫色调
            21: (30, 25, 90),    # 夜晚 - 深蓝色
            22: (25, 22, 85),    # 夜晚 - 深蓝色
            23: (22, 20, 80)     # 夜晚 - 接近深夜
        }
        
        # 确保小时在0-23范围内
        小时 = 小时 % 24
        
        # 获取当前小时和下一个小时的颜色
        当前颜色 = 小时颜色[小时]
        下一小时 = (小时 + 1) % 24
        下一小时颜色 = 小时颜色[下一小时]
        
        # 计算分钟在小时中的比例（0.0-1.0）
        分钟比例 = 分钟 / 100.0
        
        # 在当前小时和下一小时颜色之间进行线性插值
        r = int(当前颜色[0] + (下一小时颜色[0] - 当前颜色[0]) * 分钟比例)
        g = int(当前颜色[1] + (下一小时颜色[1] - 当前颜色[1]) * 分钟比例)
        b = int(当前颜色[2] + (下一小时颜色[2] - 当前颜色[2]) * 分钟比例)
        
        # 确保颜色值在0-255范围内
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        return (r, g, b)
    
    def __init__(self, 宽度, 高度, 世界类型="随机世界", 无限世界=False):
        self.高度 = 高度
        self.世界类型 = 世界类型
        self.无限世界 = 无限世界
        self.时间_of_day = 600  # 早上6点
        self.时间更新系数 = 10  # 这个系数决定了游戏一天的时长为3600秒
        self.神秘音乐已播放 = False  # 标记当天是否已播放神秘音乐
        self.items = []  # 存储掉落物实体列表
        self.exp_orbs = []  # 存储经验小球列表
        self.粒子 = []  # 存储粒子效果列表
        self.mobs = []  # 存储生物列表
        
        # 植物生长相关
        self.植物生长阶段 = {
            # 土豆生长阶段
            土豆发芽: 土豆幼年,
            土豆幼年: 土豆成年,
            # 小麦生长阶段
            小麦发芽: 小麦幼年,
            小麦幼年: 小麦成年,
            # 水稻生长阶段
            水稻发芽: 水稻幼年,
            水稻幼年: 水稻成熟,
            # 玉米生长阶段
            玉米发芽: 玉米幼年,
            玉米幼年: 玉米成年,
            # 甘蔗生长阶段
            甘蔗幼年: 甘蔗成年,
            # 番薯生长阶段
            番薯发芽: 番薯幼年,
            番薯幼年: 番薯成年,
            # 白菜生长阶段
            白菜发芽: 白菜幼年,
            白菜幼年: 白菜成年
        }
        # 记录上次生长检查的小时
        self.上次生长检查小时 = -1
        
        # 初始化区块数据
        self.chunks = {}  # 存储区块数据的字典，键为(chunk_x, chunk_y)
        self.区块结束高度 = {}  # 存储每个区块的结束高度，键为chunk_x
        
        # 生成初始地形
        if not 无限世界:
            # 限制世界大小，生成固定宽度的地形
            self.宽度 = 宽度
            self.generate_limited_terrain()
        else:
            # 无限世界，宽度设置为None
            self.宽度 = None
        
        # 初始化云数据
        self.clouds = []
        # 生成更多初始云
        self.generate_clouds()
        # 再次生成一批云，确保初始云量充足
        self.generate_clouds()
    
    def update_plant_growth(self):
        """更新植物生长状态 - 每天8到18点每小时3%概率将植物生长一次"""
        当前小时 = int(self.时间_of_day // 100)
        
        # 优化：只有20%的概率执行植物生长更新，减少CPU负担
        if random.random() > 0.2:
            return
            
        # 检查是否在生长时间段内（8:00-18:00）
        if 8 <= 当前小时 <= 18:
            # 检查是否是新的小时（防止每帧都检查）
            if 当前小时 != self.上次生长检查小时:
                self.上次生长检查小时 = 当前小时
                
                # 优化：只检查玩家附近的区块，减少遍历的区块数量
                if hasattr(self, '玩家') and self.玩家 is not None:
                    # 获取玩家所在的区块
                    player_chunk_x = int(self.玩家.坐标_x // (CHUNK_SIZE * 方块大小))
                    
                    # 只检查玩家周围3个区块范围内的植物，大幅减少计算量
                    for chunk_x in range(player_chunk_x - 3, player_chunk_x + 4):
                        chunk_key = (chunk_x, 0)
                        if chunk_key in self.chunks:
                            chunk = self.chunks[chunk_key]
                            # 遍历区块内的所有方块
                            for y in range(self.高度):
                                for x in range(CHUNK_SIZE):
                                    # 计算世界坐标
                                    world_x = chunk_x * CHUNK_SIZE + x
                                    # 获取当前方块类型
                                    current_block = chunk.方块[y][x]
                                    
                                    # 检查当前方块是否是可生长的植物
                                    if current_block in self.植物生长阶段:
                                        # 3%概率生长
                                        if random.random() < 0.03:
                                            # 生长到下一个阶段
                                            next_stage = self.植物生长阶段[current_block]
                                            self.set_block(world_x, y, next_stage)
    
    def update(self, 时间增量):
        """更新时间 - 60单位=1小时，一天=3600秒（1小时）"""
        旧时间 = self.时间_of_day
        # 使用实例属性时间更新系数
        self.时间_of_day = (self.时间_of_day + 时间增量 * self.时间更新系数) % 2400
        
        # 更新掉落物
        self.update_items(时间增量)
        
        # 更新云
        self.update_clouds(时间增量)
        
        # 每天12:00自动保存游戏数据（只有在有存档的情况下）
        current_hour = int(self.时间_of_day // 100)
        current_minute = int(self.时间_of_day % 100)
        
        # 检查是否是12:00且当天尚未保存
        if current_hour == 12 and current_minute == 0 and not self.今天已保存:
            # 只有在有玩家和游戏实例的情况下才保存
            if hasattr(self, '玩家') and self.玩家 is not None:
                # 获取游戏实例
                game_instance = getattr(self.玩家, 'game', None)
                if game_instance is not None:
                    # 获取存档名称
                    存档名称 = getattr(game_instance, '世界参数', {}).get('存档名称', '未知存档')
                    # 只有在有有效存档名称的情况下才保存数据
                    if 存档名称 and 存档名称 != '未知' and 存档名称 != '测试世界':
                        print("=== 游戏时间12:00，开始自动保存游戏数据 ===")
                        # 保存所有游戏数据
                        self.save_game_data(存档名称, self.玩家, game_instance)
                        print("=== 游戏数据自动保存完成 ===")
                        # 标记当天已保存
                        self.今天已保存 = True
                    else:
                        print("=== 无有效存档名称，跳过自动保存 ===")
        # 如果不是12:00，重置保存标记
        elif current_hour != 12:
            self.今天已保存 = False
        
        # 更新植物生长
        self.update_plant_growth()
        
        # 检查是否到达20:00并播放神秘音乐
        # 当时间从19:59左右过渡到20:00左右时播放
        if 1990 <= 旧时间 < 2000 and not self.神秘音乐已播放:
            from 音频输出 import audio_manager
            audio_manager.play_sound("神秘音乐")
            self.神秘音乐已播放 = True
        
        # 当时间重置到0点时，重置播放标志
        if 旧时间 >= 2350 and self.时间_of_day < 50:
            self.神秘音乐已播放 = False
            # 重置上次生长检查小时，确保第二天能正常检查
            self.上次生长检查小时 = -1
    
    def spawn_mobs(self, count, player, game=None):
        """生成指定数量的生物"""
        from 生物系统 import Mob
        from 物品定义 import (
            史莱姆, 土拨鼠, 幽灵, 蝙蝠, 火焰精灵, 蘑菇怪, 岩石怪,
            猴子
        )
        
        # 生物类型列表
        mob_types = [史莱姆, 土拨鼠, 幽灵, 蝙蝠, 火焰精灵, 蘑菇怪, 岩石怪, 猴子]
        
        # 飞行生物类型列表
        flying_mobs = [幽灵, 蝙蝠, 火焰精灵]
        
        for _ in range(count):
            # 随机选择生物类型
            mob_id = random.choice(mob_types)
            
            # 在玩家附近生成
            spawn_x = random.randint(int(player.坐标_x - 500), int(player.坐标_x + 500))
            spawn_y = 0
            
            if mob_id in flying_mobs:
                # 飞行生物：生成在玩家附近的合理高度（±50像素）
                spawn_y = player.坐标_y + random.randint(-50, 50)
                # 确保飞行生物不会生成在地下或太高的地方
                spawn_y = max(0, min(spawn_y, self.高度 * 32 - 100))
            else:
                # 非飞行生物：找到地面位置
                for y in range(5, self.高度):
                    if self.get_block(int(spawn_x // 方块大小), y) != 0:
                        spawn_y = (y - 3) * 方块大小
                        break
            
            mob = Mob(spawn_x, spawn_y, mob_id)
            # 设置game属性，用于显示伤害数字
            if game:
                mob.game = game
            self.mobs.append(mob)
    
    def remove_dead_mobs(self):
        """移除死亡的生物"""
        self.mobs = [mob for mob in self.mobs if mob.is_alive()]
    
    def spawn_exp_orbs(self, x, y):
        """
        在指定坐标生成经验小球
        """
        import random
        from 游玩 import ExpOrb
        # 计算生成位置
        orb_x = x * 方块大小 + random.randint(8, 24)
        orb_y = y * 方块大小 + random.randint(8, 24)
        
        # 决定生成哪种经验球
        rand = random.random()
        if rand < 0.2:  # 20%概率生成金色经验球
            self.exp_orbs.append(ExpOrb(self, orb_x, orb_y, 'gold'))
        elif rand < 0.4:  # 20%概率生成蓝色经验球
            self.exp_orbs.append(ExpOrb(self, orb_x, orb_y, 'blue'))
        else:  # 60%概率生成绿色经验球
            self.exp_orbs.append(ExpOrb(self, orb_x, orb_y, 'green'))
    
    def update_mobs(self, dt, player):
        """更新所有生物"""
        for mob in self.mobs:
            # 设置game属性，用于显示伤害数字和召唤生物
            mob.game = self
            mob.update(self, player)
        # 移除死亡的生物
        self.remove_dead_mobs()
    
    def draw_mobs(self, 屏幕, 相机_x, 相机_y):
        """绘制所有生物"""
        for mob in self.mobs:
            mob.draw(屏幕, 相机_x, 相机_y)
    
    def update_items(self, dt):
        """更新所有掉落物的状态"""
        # 创建一个新列表来存储需要保留的掉落物
        remaining_items = []
        
        for item in self.items:
            # 更新掉落物
            item.update(dt)
            
            # 只保留不需要消失的掉落物
            if not item.should_despawn():
                remaining_items.append(item)
        
        # 更新掉落物列表
        self.items = remaining_items
    
    def spawn_item(self, x, y, item_id, count=1, is_special=False, special_type=None, target_player=None):
        """在指定位置生成掉落物"""
        new_item_x = x * 方块大小 + 8
        new_item_y = y * 方块大小
        
        # 特殊处理：死神的镰刀不合并，总是生成新的
        from 物品定义 import 死神的镰刀
        if item_id == 死神的镰刀:
            # 直接创建新的掉落物实体，数量固定为1
            new_item = ItemEntity(self, new_item_x, new_item_y, item_id, 1, is_special=is_special, special_type=special_type)
            # 设置目标玩家
            if target_player:
                new_item.target_player = target_player
            self.items.append(new_item)
            # 调试信息
            print(f"创建新掉落物: {item_id} 数量: 1，位置: ({x}, {y})，特殊类型: {special_type}，不合并")
            return
        
        # 普通物品：检查附近是否有相同类型的掉落物，如果有则合并
        merge_distance = 64  # 合并距离阈值（像素），增加距离以提高合并成功率
        # 遍历现有掉落物，查找可合并的
        for item in self.items:
            # 检查是否是相同类型的物品
            if item.item_id == item_id:
                # 计算距离
                distance = math.hypot(new_item_x - item.x, new_item_y - item.y)
                # 如果在合并距离内
                if distance <= merge_distance:
                    # 合并数量
                    item.count += count
                    # 调试信息
                    print(f"掉落物合并: {item_id} 数量增加到 {item.count}，位置: ({x}, {y})")
                    return  # 直接返回，不创建新掉落物
        
        # 如果没有找到可合并的掉落物，创建新的掉落物实体
        new_item = ItemEntity(self, new_item_x, new_item_y, item_id, count, is_special=is_special, special_type=special_type)
        # 设置目标玩家
        if target_player:
            new_item.target_player = target_player
        self.items.append(new_item)
        # 调试信息
        print(f"创建新掉落物: {item_id} 数量: {count}，位置: ({x}, {y})，特殊类型: {special_type}")
    
    def draw_items(self, surface, camera_x, camera_y):
        """绘制所有掉落物"""
        for item in self.items:
            item.draw(surface, camera_x, camera_y)
    
    def update_particles(self, dt):
        """更新所有粒子效果
        
        参数:
            dt: 时间增量（秒）
        """
        new_particles = []
        
        for particle in self.粒子:
            # 更新粒子位置
            particle['x'] += particle['vx'] * dt * 60
            particle['y'] += particle['vy'] * dt * 60
            
            # 减少粒子生命值
            particle['life'] -= dt
            
            # 只保留生命值大于0的粒子
            if particle['life'] > 0:
                new_particles.append(particle)
        
        # 限制粒子数量，最多100个
        self.粒子 = new_particles[:100]
    
    def draw_particles(self, surface, camera_x, camera_y):
        """绘制所有粒子效果
        
        参数:
            surface: 绘制表面
            camera_x: 相机X坐标
            camera_y: 相机Y坐标
        """
        for particle in self.粒子:
            # 计算粒子在屏幕上的位置
            draw_x = particle['x'] - camera_x
            draw_y = particle['y'] - camera_y
            
            # 计算粒子大小（随生命值减小而变小）
            particle_size = int(particle['size'] * (particle['life'] / (0.5 + 1.5)))
            particle_size = max(1, particle_size)  # 确保粒子大小至少为1
            
            # 绘制粒子
            pygame.draw.circle(surface, particle['color'], 
                              (int(draw_x), int(draw_y)), particle_size)
    
    def draw(self, 屏幕, 相机_x, 相机_y):
        """绘制世界 - 优化版"""
        # 绘制天空
        屏幕.fill(self.get_sky_color())
        
        # 绘制太阳和月亮
        self.draw_sun_moon(屏幕)
        
        # 绘制云群
        self.draw_clouds(屏幕, 相机_x, 相机_y)
        
        # 获取当前屏幕实际大小
        当前屏幕宽度, 当前屏幕高度 = 屏幕.get_size()
        
        # 计算可见区域
        起始_x = max(0, int(相机_x // 方块大小) - 1)
        if self.无限世界:
            # 无限世界，不限制x轴的结束位置
            结束_x = int((相机_x + 当前屏幕宽度) // 方块大小) + 1
        else:
            # 有限世界，限制x轴的结束位置
            结束_x = min(self.宽度, int((相机_x + 当前屏幕宽度) // 方块大小) + 1)
        起始_y = max(0, int(相机_y // 方块大小) - 1)
        结束_y = min(self.高度, int((相机_y + 当前屏幕高度) // 方块大小) + 1)
        
        # 优化1：预计算可见区域的方块数量，限制最大渲染方块数
        max_blocks = 5000  # 限制最多渲染5000个方块
        block_count = 0
        
        # 优化2：预加载常用方块的图片和属性，避免重复查找
        方块缓存 = {}
        
        # 植物生长阶段缩放比例配置
        生长阶段缩放 = {
            # 发芽阶段：大小不变
            土豆发芽: 1.0,
            小麦发芽: 1.0,
            水稻发芽: 1.0,
            玉米发芽: 1.0,
            番薯发芽: 1.0,
            白菜发芽: 1.0,
            # 幼苗/幼年阶段：放大30%
            土豆幼年: 1.3,
            小麦幼年: 1.3,
            水稻幼年: 1.3,
            玉米幼年: 1.3,
            甘蔗幼年: 2.0,  # 甘蔗放大100%
            番薯幼年: 1.3,
            白菜幼年: 1.3,
            # 成年/成熟阶段：放大70%
            土豆成年: 1.7,
            小麦成年: 1.7,
            水稻成熟: 1.7,
            玉米成年: 1.7,
            甘蔗成年: 2.0,  # 甘蔗放大100%
            番薯成年: 1.7,
            白菜成年: 1.7
        }
        
        # 统一使用get_block方法获取方块，确保有限世界和无限世界行为一致
        for y in range(起始_y, 结束_y):
            for x in range(起始_x, 结束_x):
                # 优化3：限制最大渲染方块数
                block_count += 1
                if block_count > max_blocks:
                    break
                
                方块_id = self.get_block(x, y)
                if 方块_id == 空气:
                    continue
                
                绘制_x = x * 方块大小 - 相机_x
                绘制_y = y * 方块大小 - 相机_y
                
                # 优化4：使用缓存的方块信息，避免重复查找
                if 方块_id not in 方块缓存:
                    # 获取方块信息
                    方块_info = 方块属性.get(方块_id, {})
                    方块名称 = 方块_info.get("名称", "")
                    纹理名称 = 方块_info.get("纹理", "")
                    颜色 = 方块_info.get("颜色")
                    
                    # 获取当前方块的缩放比例，默认1.0
                    缩放比例 = 生长阶段缩放.get(方块_id, 1.0)
                    
                    # 计算缩放后的大小
                    缩放后的宽度 = int(方块大小 * 缩放比例)
                    缩放后的高度 = int(方块大小 * 缩放比例)
                    
                    # 计算绘制位置的偏移量，使植物居中显示
                    偏移_x = (方块大小 - 缩放后的宽度) // 2
                    偏移_y = (方块大小 - 缩放后的高度) // 2
                    
                    # 尝试获取方块图片
                    方块图片 = None
                    
                    # 1. 优先使用纹理名称查找图片
                    if 纹理名称:
                        方块图片 = 图片管理器.获取图片(纹理名称)
                    # 2. 如果纹理名称找不到图片，尝试使用方块名称
                    if not 方块图片 and 方块名称:
                        方块图片 = 图片管理器.获取图片(方块名称)
                    
                    # 缓存方块信息
                    方块缓存[方块_id] = {
                        "方块名称": 方块名称,
                        "纹理名称": 纹理名称,
                        "颜色": 颜色,
                        "缩放比例": 缩放比例,
                        "缩放后的宽度": 缩放后的宽度,
                        "缩放后的高度": 缩放后的高度,
                        "偏移_x": 偏移_x,
                        "偏移_y": 偏移_y,
                        "方块图片": 方块图片
                    }
                
                # 获取缓存的方块信息
                缓存数据 = 方块缓存[方块_id]
                方块名称 = 缓存数据["方块名称"]
                纹理名称 = 缓存数据["纹理名称"]
                颜色 = 缓存数据["颜色"]
                缩放比例 = 缓存数据["缩放比例"]
                缩放后的宽度 = 缓存数据["缩放后的宽度"]
                缩放后的高度 = 缓存数据["缩放后的高度"]
                偏移_x = 缓存数据["偏移_x"]
                偏移_y = 缓存数据["偏移_y"]
                方块图片 = 缓存数据["方块图片"]
                
                if 方块图片:
                    # 优化5：缓存缩放后的图片，避免每次绘制都重新缩放
                    缓存键 = f"{纹理名称 or 方块名称}_{缩放比例}"
                    
                    # 检查是否已有缓存的缩放图片
                    if not hasattr(图片管理器, "缩放图片缓存"):
                        图片管理器.缩放图片缓存 = {}
                    
                    # 如果缓存中没有，创建并缓存
                    if 缓存键 not in 图片管理器.缩放图片缓存:
                        缩放后的图片 = pygame.transform.scale(方块图片, (缩放后的宽度, 缩放后的高度))
                        图片管理器.缩放图片缓存[缓存键] = 缩放后的图片
                    else:
                        缩放后的图片 = 图片管理器.缩放图片缓存[缓存键]
                    
                    # 绘制缩放后的图片
                    屏幕.blit(缩放后的图片, (绘制_x + 偏移_x, 绘制_y + 偏移_y))
                else:
                    # 如果没有图片，使用颜色绘制
                    if 颜色:
                        pygame.draw.rect(屏幕, 颜色, 
                                       (绘制_x + 偏移_x, 绘制_y + 偏移_y, 缩放后的宽度, 缩放后的高度))
            
            if block_count > max_blocks:
                break

class Game:
    """游戏主类，处理游戏逻辑和循环"""
    
    def __init__(self, 世界参数, screen=None):
        # 初始化游戏窗口
        if screen is None:
            # 如果没有传入屏幕，创建新窗口（兼容旧代码）
            # 添加硬件加速标志，启用GPU加速
            self.屏幕 = pygame.display.set_mode((宽度, 高度), 
                                             pygame.RESIZABLE | 
                                             pygame.HWSURFACE |  # 硬件表面加速
                                             pygame.DOUBLEBUF |  # 双缓冲，减少闪烁
                                             pygame.SCALED)      # 硬件缩放加速
            pygame.display.set_caption("方块世界")
        else:
            # 使用传入的屏幕，实现统一窗口
            self.屏幕 = screen
        
        # 加载图片资源
        print("正在加载图片资源...")
        图片管理器.加载所有图片()
        
        self.时钟 = pygame.time.Clock()
        self.帧率 = 60
        # 帧率相关变量初始化
        self.fps_timer = 0
        self.current_fps = 0
        self.frame_count = 0
        
        # 导入json模块用于读取设置
        import json
        import os
        
        # 从相对路径的设置_数据库.json加载最大帧数
        self.target_fps = self._加载最大帧数(json, os)
        
        # 加载特效渲染设置
        self.特效渲染设置 = self._加载特效渲染设置(json, os)
        
        # 存储世界参数
        self.世界参数 = 世界参数
        
        # 初始化游戏世界
        self.世界 = World(
            宽度=世界参数['世界宽度'],
            高度=世界参数['世界高度'],
            世界类型=世界参数['世界类型'],
            无限世界=世界参数.get('无限世界', False)
        )
        
        # 保存地形数据到存档文件夹
        if 世界参数.get('创建存档', False):
            print(f"正在保存地形数据到存档: {世界参数['存档名称']}")
            self.世界.save_terrain_data(世界参数['存档名称'])
        
        # 初始化页面管理器（确保在世界参数和世界实例初始化之后）
        from 游玩_页面管理 import PageManager
        self.page_manager = PageManager(self)
        
        # 获取安全的出生位置
        self.玩家 = self.spawn_player()
        
        # 将玩家对象关联到世界对象，并重新生成云群
        self.世界.玩家 = self.玩家
        # 使用玩家的实际位置生成云群
        print(f"玩家位置: x={self.玩家.坐标_x}, y={self.玩家.坐标_y}")
        print(f"生成云群前的云数量: {len(self.世界.clouds)}")
        self.世界.generate_clouds()
        print(f"第一次生成云群后的云数量: {len(self.世界.clouds)}")
        self.世界.generate_clouds()
        print(f"第二次生成云群后的云数量: {len(self.世界.clouds)}")
        
        # 近战攻击间隔相关属性
        self.近战攻击间隔 = 0.4  # 近战攻击间隔，单位：秒
        self.上次攻击时间 = 0  # 上次攻击时间，单位：秒
        
        # 玩家创建时激活30秒无敌状态
        from 状态管理 import 状态管理器实例
        状态管理器实例.激活无敌状态(30)
        
        # 游戏状态
        self.运行中 = True
        self.创造模式 = 世界参数['创造模式']
        self.显示调试 = True
        
        # 挖掘相关属性
        self.正在挖掘 = False
        self.挖掘位置 = None  # (x, y) 方块坐标
        self.挖掘开始时间 = 0
        self.挖掘进度 = 0
        self.当前挖掘方块 = None
        self.is_instant_dig = False  # 秒挖掘状态（无时间限制挖掘）
        self.has_max_permission = False  # 最高权限（可挖掘基岩）
        self.enable_3x3_place = False  # 3*3放置（快捷栏物品只减少1个）
        self.enable_3x3_dig = False  # 3*3范围挖掘
        self.enable_fullscreen_click = False  # 全屏点击任意位置挖掘放置
        
        # 确保创造模式下秒挖掘默认关闭，以便体验挖掘效率差异
        if self.创造模式:
            self.is_instant_dig = False
        
        # 快捷栏相关属性
        self.当前选中格子 = 0  # 默认选中第一个格子（格1）
        
        # 草悬空检测相关属性
        self.草检查计时器 = 0  # 草悬空检测计时器
        self.草检查间隔 = 5  # 草悬空检测间隔（秒）
        
        # 初始化帮助页面相关属性
        self.show_controls = False  # 控制操作提示页面显示状态
        self.help_scroll_offset = 0  # 帮助页面滚动偏移量
        self.help_max_scroll_offset = 0  # 最大滚动偏移量
        self.scroll_speed = 40  # 滚动速度
        
        # 长按Q键使用物品相关属性
        self.q_pressed = False  # Q键是否被按下
        self.q_press_time = 0  # Q键按下的时间
        self.q_holding_time = 0  # Q键长按的累计时间
        self.required_hold_time = 2  # 长按Q键所需的时间（秒）
        self.q_sound_played = False  # 是否已播放吃东西音效
        # 物品使用进度相关属性
        self.物品使用进度 = 0  # 物品使用进度（0-1）
        self.显示物品使用进度 = False  # 是否显示物品使用进度条
        
        # 弓箭冷却相关属性
        self.弓箭冷却时间 = 1.0  # 弓箭射击间隔，单位：秒
        self.弓箭上次射击时间 = 0  # 上次射击的时间戳
        
        # 鼠标左键状态属性
        self.mouse_left_pressed = False  # 鼠标左键是否被按下
        self.mouse_press_time = 0  # 鼠标按下的时间
        self.mouse_holding_time = 0  # 鼠标长按的累计时间
        
        # 弹药数量相关属性
        self.当前武器弹药 = 15  # 当前弹夹子弹数（手枪弹夹容量15发）
        self.背包弹药 = 9999  # 背包弹药数量
        
        # 弹夹系统属性
        self.换弹中 = False  # 换弹中状态
        self.换弹剩余时间 = 0  # 换弹剩余时间
        self.换弹总时间 = 3  # 换弹总时间（秒）
        
        # 换弹进度条属性
        self.显示换弹进度条 = False  # 换弹进度条显示状态
        self.换弹进度 = 0  # 换弹进度（0-1）
        self.换弹开始时间 = 0  # 换弹开始时间
        
        # 换弹按钮动画相关属性
        self.换弹按钮按下 = False  # 按钮是否被按下
        self.换弹按钮动画时间 = 0  # 动画持续时间
        self.换弹按钮动画时长 = 0.2  # 动画总时长（秒）
        
        # ESC菜单相关属性
        self.show_esc_menu = False
        self.esc_page = None
        
        # 伤害数字相关属性
        self.damage_texts = []  # 存储伤害数字对象的列表
        self.DamageText = DamageText  # 将DamageText类赋值给游戏对象，供生物系统使用
        # 预先导入ESC页面模块，避免运行时重复导入
        import importlib.util
        # 获取当前目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 漂浮文字通知系统
        self.notifications = []  # 存储当前显示的漂浮文字列表
        self.提示移动速度 = 50  # 文字向上移动速度（像素/秒）
        self.提示显示时间 = 3.0  # 文字显示总时间（秒）
        self.当前时间 = 0  # 当前时间记录
        self.提示字体 = pygame.font.SysFont("Microsoft YaHei", 20, True)  # 漂浮文字字体
        # 静态导入模块，便于PyInstaller打包

        
        # 自动保存相关属性
        self.上次保存时间 = time.time()
        self.自动保存间隔 = 300  # 自动保存间隔时间（秒），默认5分钟
        
        
        
        # 批量加载物品图片
        print("开始预加载物品图片...")
        批量加载物品图片()
        # 背包测试完毕，不再随机生成初始物品
        
        # 初始化创造背包（按F3键打开）
        from 创造背包 import CreativeBackpack
        self.creative_backpack = CreativeBackpack(self)
        
        # 初始化合成页面
        from 合成页面 import CraftingPage
        self.crafting_system = CraftingPage(self)
        
        # 初始化背包（按B键打开）
        from 背包 import 背包管理器
        self.背包管理器 = 背包管理器(self)
        
        # 箭矢列表
        self.arrows = []
        # 伤害数字列表
        self.damage_texts = []
        
        # 初始化返回主程序按钮（设置图标）
        # 先设置临时位置，在draw方法中会动态调整为靠右
        self.return_to_main_button = pygame.Rect(0, 0, 20, 20)
        # 加载返回主程序按钮图片
        self.return_button_image = 图片管理器.获取图片("设置按钮ui") if 图片管理器.图片是否已加载("设置按钮ui") else None
        # 初始化关机按钮
        self.关机按钮 = pygame.Rect(0, 0, 20, 20)
        # 加载关机按钮图片
        self.关机按钮_image = 图片管理器.获取图片("关机按钮") if 图片管理器.图片是否已加载("关机按钮") else None
        # 添加直接返回主程序按钮
        self.直接返回主程序按钮 = pygame.Rect(0, 0, 120, 40)
        # 设置按钮文字
        self.直接返回主程序文字 = "返回主菜单"
        # 控制直接返回主程序按钮的显示状态
        self.显示直接返回主程序按钮 = False
        # 添加隐藏按钮，修改文字为"取消"
        self.隐藏按钮 = pygame.Rect(0, 0, 120, 40)
        self.隐藏按钮文字 = "取消"
        # 添加提示窗口相关属性
        self.显示退出提示 = False  # 是否显示退出提示窗口
        self.提示窗口宽度 = 700  # 提示窗口宽度
        self.提示窗口高度 = 700  # 提示窗口高度
        # 提示窗口按钮
        self.确认按钮_rect = pygame.Rect(0, 0, 100, 40)  # 确认按钮
        self.取消按钮_rect = pygame.Rect(0, 0, 100, 40)  # 取消按钮
        # 提示窗口标题和内容
        self.退出提示标题 = "设置"
        self.退出提示内容 = "确定要退出并保存存档吗？"
        # 提示窗口字体 - 使用支持中文的字体
        try:
            self.提示窗口字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 28)
            self.提示窗口标题字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 36, bold=True)
        except:
            self.提示窗口字体 = pygame.font.Font(None, 28)
            self.提示窗口标题字体 = pygame.font.Font(None, 36)
        # 音效和音乐开关状态 - 从设置文件同步
        self.音效开关 = True  # 音效开关状态
        self.音乐开关 = True  # 音乐开关状态
        # 音量进度条值 - 从设置文件同步
        self.音量值 = 100  # 音量百分比（0-100）
        # 特效渲染设置 - 从设置文件同步
        self.特效渲染设置 = "标准"  # 特效渲染设置：最佳、标准、关闭
        # 显示距离设置 - 从设置文件同步
        self.显示攻击距离 = False  # 显示攻击距离
        self.显示受伤距离 = False  # 显示受伤距离
        # 加载设置数据
        self._load_settings_from_file()
    
    def spawn_player(self):
        """找到合适的出生点并生成玩家，确保y坐标为0"""
        出生_x, 出生_y = 0, 0
        
        # 根据世界类型处理不同的出生点逻辑
        if self.世界.无限世界:
            # 无限世界，使用固定的出生位置
            中心_x = 1000  # 固定中心位置
            搜索范围 = 100  # 固定搜索范围
            
            # 查找合适的x坐标，但固定y坐标为0
            for x in range(中心_x - 搜索范围, 中心_x + 搜索范围):
                # 检查该位置上方有足够空间
                出生_x = x * 方块大小
                break
        else:
            # 有限世界，使用传统的中心位置搜索
            中心_x = self.世界.宽度 // 2
            搜索范围 = min(100, self.世界.宽度 // 4)
            
            # 查找合适的x坐标，但固定y坐标为0
            for x in range(中心_x - 搜索范围, 中心_x + 搜索范围):
                # 检查x坐标是否有效且该位置上方有足够空间
                if 0 <= x < self.世界.宽度:
                    出生_x = x * 方块大小
                    break
            
            # 如果没找到合适的x位置，使用中心位置
            if 出生_x == 0:
                出生_x = 中心_x * 方块大小
        
        # 固定y坐标为0
        出生_y = 0
        
        return Player(出生_x, 出生_y, self.世界.宽度 if not self.世界.无限世界 else 2000, self.世界.高度, self.target_fps, self)
    
    def handle_events(self):
        """处理游戏事件"""
        for 事件 in pygame.event.get():
            if 事件.type == pygame.QUIT:
                # 只有在有存档的情况下才保存数据
                存档名称 = self.世界参数.get('存档名称', '')
                if 存档名称 and 存档名称 != '未知' and 存档名称 != '测试世界':
                    # 关闭窗口前保存一次游戏数据
                    print("=== 关闭窗口，开始保存游戏数据 ===")
                    self.世界.save_game_data(存档名称, self.玩家, self)
                    print("=== 游戏数据保存完成 ===")
                else:
                    print("=== 无存档，关闭窗口时不保存数据 ===")
                # 设置运行中为False，退出游戏主循环
                self.运行中 = False
            # 处理ESC键，切换设置页面显示/隐藏
            elif 事件.type == pygame.KEYDOWN:
                if 事件.key == pygame.K_ESCAPE:
                    if self.显示退出提示:
                        print("按ESC键，关闭设置页面")
                        # 隐藏退出提示窗口
                        self.显示退出提示 = False
                    else:
                        # 检查是否有其他页面打开，如果有则不显示设置页面
                        有其他页面打开 = False
                        # 检查帮助页面
                        if self.show_controls:
                            有其他页面打开 = True
                        # 检查创造背包
                        elif hasattr(self, 'creative_backpack') and self.creative_backpack.is_open:
                            有其他页面打开 = True
                        # 检查合成页面
                        elif hasattr(self, 'crafting_system') and self.crafting_system.is_open:
                            有其他页面打开 = True
                        # 检查熔炉页面
                        elif hasattr(self, 'furnace_manager') and self.furnace_manager.是否打开:
                            有其他页面打开 = True
                        # 检查属性提升页面
                        elif hasattr(self, '属性提升页面') and self.属性提升页面.is_open:
                            有其他页面打开 = True
                        # 检查开发者调试页面
                        elif hasattr(self, 'dev_debug_page') and self.dev_debug_page.is_open:
                            有其他页面打开 = True
                        # 检查背包页面
                        elif hasattr(self, '背包管理器') and self.背包管理器.是否打开:
                            有其他页面打开 = True
                        # 检查页面管理器是否有任何页面打开
                        elif hasattr(self, 'page_manager') and self.page_manager.is_any_page_open():
                            有其他页面打开 = True
                        
                        if not 有其他页面打开:
                            print("按ESC键，打开设置页面")
                            # 显示退出提示窗口前，加载最新的设置数据
                            self._load_settings_from_file()
                            # 显示退出提示窗口
                            self.显示退出提示 = True
            elif 事件.type == pygame.KEYUP:
                # 处理键盘释放事件
                if 事件.key == pygame.K_q:
                    # 检查当前是否手持远程武器（弓、弩、手枪、步枪或狙击枪）
                    工具实例, 当前工具 = self.获取当前手持工具()
                    手持远程武器 = False
                    if 当前工具:
                        武器名称 = 当前工具['名称']
                        # 齐天金箍棒是近战武器，排除在远程武器之外
                        手持远程武器 = ('弓' in 武器名称 or '弩' in 武器名称 or '手枪' in 武器名称 or '步枪' in 武器名称 or '狙击枪' in 武器名称 or '火箭筒' in 武器名称 or 'RPG' in 武器名称 or '激光炮' in 武器名称 or '喷子' in 武器名称 or '冲锋枪' in 武器名称 or '龙息' in 武器名称 or '机甲' in 武器名称 or '榴弹炮' in 武器名称 or '加特林' in 武器名称 or ('齐天' in 武器名称 and '金箍棒' not in 武器名称) or '救世主' in 武器名称)
                    
                    # 重置Q键状态
                    self.q_pressed = False
                    self.q_holding_time = 0
                    self.物品使用进度 = 0
                    self.显示物品使用进度 = False
                    
                    # 调用武器技能管理器处理Q键释放
                    weapon_name = 当前工具['名称'] if 当前工具 else ""
                    武器技能管理器实例.handle_input(事件, self.玩家, weapon_name)
                    
                    # 只有非远程武器时，才停止所有音频
                    if not 手持远程武器:
                        # 按Q键停止播放所有音频
                        from 音频输出 import audio_manager
                        audio_manager.stop_all_sounds()
            
            # 处理自定义事件
            elif 事件.type >= pygame.USEREVENT + 1000:
                # 检查是否是灵火剑持续伤害事件
                if hasattr(self, 'timed_damage_events'):
                    event_id = 事件.type
                    if event_id in self.timed_damage_events:
                        # 获取事件数据
                        event_data = self.timed_damage_events[event_id]
                        mob = event_data['mob']
                        damage = event_data['damage']
                        color = event_data['color']
                        
                        # 检查生物是否还活着
                        if hasattr(mob, 'health') and mob.health > 0:
                            # 造成伤害
                            死亡 = mob.take_damage(damage)
                            # 创建蓝色伤害文本
                            if not 死亡 or mob.health > 0:
                                self.damage_texts.append(self.DamageText(
                                    mob.x + mob.width // 2, 
                                    mob.y - 10, 
                                    damage, 
                                    color=color
                                ))
                        
                        # 从事件字典中移除已处理的事件
                        del self.timed_damage_events[event_id]
                # 检查是否是亡灵斧头伤害事件
                elif hasattr(事件, 'player_x') and hasattr(事件, 'player_y') and hasattr(事件, 'half_range'):
                    # 获取事件数据
                    player_x = 事件.player_x
                    player_y = 事件.player_y
                    half_range = 事件.half_range
                    tile_size = 事件.tile_size
                    damage = 事件.damage
                    game = 事件.game
                    
                    # 1. 获取所有生物
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
                    
                    # 2. 计算伤害范围矩形
                    damage_rect = pygame.Rect(
                        player_x - half_range * tile_size, 
                        player_y - half_range * tile_size, 
                        (half_range * 2 + 1) * tile_size, 
                        (half_range * 2 + 1) * tile_size
                    )
                    
                    # 3. 对范围内的生物造成伤害
                    for mob in all_mobs:
                        mob_rect = pygame.Rect(mob.x, mob.y, mob.width, mob.height)
                        if damage_rect.colliderect(mob_rect):
                            # 对生物造成伤害
                            mob.game = game
                            死亡 = mob.take_damage(damage)
                            
                            # 创建伤害文本
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
            
            # 处理鼠标点击事件（换弹按钮和返回主程序按钮）
            if 事件.type == pygame.MOUSEBUTTONDOWN:
                if 事件.button == 1:  # 左键点击
                    # 检查是否显示退出提示窗口
                    if self.显示退出提示:
                        # 检查是否点击了关闭按钮
                        if hasattr(self, '关闭按钮_rect') and self.关闭按钮_rect.collidepoint(事件.pos):
                            print("点击关闭按钮，取消退出")
                            # 隐藏退出提示窗口
                            self.显示退出提示 = False
                        # 检查是否点击了音效开关
                        elif hasattr(self, '音效开关_rect') and self.音效开关_rect.collidepoint(事件.pos):
                            print("点击音效开关")
                            # 切换音效开关状态
                            self.音效开关 = not self.音效开关
                            print(f"音效开关状态: {self.音效开关}")
                            # 保存设置到文件
                            self._save_settings_to_file()
                        # 检查是否点击了音乐开关
                        elif hasattr(self, '音乐开关_rect') and self.音乐开关_rect.collidepoint(事件.pos):
                            print("点击音乐开关")
                            # 切换音乐开关状态
                            self.音乐开关 = not self.音乐开关
                            print(f"音乐开关状态: {self.音乐开关}")
                            # 保存设置到文件
                            self._save_settings_to_file()
                        # 检查是否点击了音量进度条
                        elif hasattr(self, '进度条_rect') and self.进度条_rect.collidepoint(事件.pos):
                            print("点击音量进度条")
                            # 计算点击位置对应的音量值
                            轨道_x = self.进度条_rect.x
                            轨道_width = self.进度条_rect.width
                            点击_x = 事件.pos[0]
                            # 计算音量百分比
                            音量百分比 = (点击_x - 轨道_x) / 轨道_width
                            # 限制在0-100之间
                            self.音量值 = max(0, min(100, int(音量百分比 * 100)))
                            print(f"音量调整为: {self.音量值}%")
                            # 保存设置到文件
                            self._save_settings_to_file()
                        # 检查是否点击了显示攻击距离按钮
                        elif hasattr(self, '显示攻击距离按钮_rect') and self.显示攻击距离按钮_rect.collidepoint(事件.pos):
                            print("点击显示攻击距离按钮")
                            # 切换显示攻击距离状态
                            self.显示攻击距离 = not self.显示攻击距离
                            print(f"显示攻击距离状态: {self.显示攻击距离}")
                            # 保存设置到文件
                            self._save_settings_to_file()
                        # 检查是否点击了显示受伤距离按钮
                        elif hasattr(self, '显示受伤距离按钮_rect') and self.显示受伤距离按钮_rect.collidepoint(事件.pos):
                            print("点击显示受伤距离按钮")
                            # 切换显示受伤距离状态
                            self.显示受伤距离 = not self.显示受伤距离
                            print(f"显示受伤距离状态: {self.显示受伤距离}")
                            # 保存设置到文件
                            self._save_settings_to_file()
                        # 检查是否点击了特效选项
                        elif hasattr(self, '特效选项_rects'):
                            特效选项 = ["最佳", "标准", "关闭"]
                            for i, 选项_rect in enumerate(self.特效选项_rects):
                                if 选项_rect.collidepoint(事件.pos):
                                    print(f"点击特效选项: {特效选项[i]}")
                                    # 更新特效渲染设置
                                    self.特效渲染设置 = 特效选项[i]
                                    print(f"特效设置已更新为: {self.特效渲染设置}")
                                    # 保存设置到文件
                                    self._save_settings_to_file()
                                    break
                        # 检查是否点击了保存世界按钮
                        elif hasattr(self, '保存世界按钮_rect') and self.保存世界按钮_rect.collidepoint(事件.pos):
                            print("点击保存世界按钮")
                            # 只有在有存档的情况下才保存数据
                            存档名称 = self.世界参数.get('存档名称', '')
                            if 存档名称 and 存档名称 != '未知' and 存档名称 != '测试世界':
                                # 保存游戏数据
                                print("=== 点击保存世界，开始保存游戏数据 ===")
                                self.世界.save_game_data(存档名称, self.玩家, self)
                                print("=== 游戏数据保存完成 ===")
                                # 可以添加保存成功提示
                                self._show_notification("世界已保存")
                            else:
                                print("=== 无存档，无法保存世界 ===")
                                self._show_notification("无存档，无法保存")
                            # 不隐藏退出提示窗口，继续显示
                        # 点击其他区域不处理
                        return
                    # 检查是否点击了返回主程序按钮（设置图标）
                    elif self.return_to_main_button.collidepoint(事件.pos):
                        # 显示退出提示窗口
                        self.显示退出提示 = True
                        print("显示退出提示窗口")
                    # 检查是否点击了关机按钮
                    elif self.关机按钮.collidepoint(事件.pos):
                        print("点击关机按钮")
                        # 显示返回主菜单确认对话框
                        self.显示直接返回主程序按钮 = True
                        print("显示返回主菜单确认对话框")
                    # 检查是否点击了直接返回主程序按钮
                    elif hasattr(self, '直接返回主程序按钮') and self.显示直接返回主程序按钮 and self.直接返回主程序按钮.collidepoint(事件.pos):
                        print("点击直接返回主程序按钮")
                        # 先保存游戏数据，再返回主程序
                        存档名称 = self.世界参数.get('存档名称', '')
                        if 存档名称 and 存档名称 != '未知' and 存档名称 != '测试世界':
                            print("=== 返回主菜单前，开始保存游戏数据 ===")
                            self.世界.save_game_data(存档名称, self.玩家, self)
                            print("=== 游戏数据保存完成 ===")
                        else:
                            print("=== 无存档，返回主菜单时不保存数据 ===")
                        
                        # 清理BOSS实例
                        print("=== 清理游戏数据，准备返回主菜单 ===")
                        from boos生物处理 import boss_manager
                        boss_manager.clear_bosses()
                        
                        # 清理世界中的生物
                        if hasattr(self.世界, 'creatures'):
                            self.世界.creatures = []
                        
                        # 保存完成后返回主程序
                        self.运行中 = False
                        print("保存数据后返回主程序")
                    # 检查是否点击了取消按钮
                    elif hasattr(self, '隐藏按钮') and self.显示直接返回主程序按钮 and self.隐藏按钮.collidepoint(事件.pos):
                        print("点击取消按钮")
                        # 关闭返回主菜单确认对话框
                        self.显示直接返回主程序按钮 = False
                        print("关闭返回主菜单确认对话框")
                    # 检查是否点击了换弹按钮
                    elif hasattr(self, '换弹按钮_rect'):
                        if self.换弹按钮_rect.collidepoint(事件.pos):
                            # 按下了换弹按钮，在终端显示
                            print("按下换弹")
                            # 设置按钮按下状态，启动动画
                            self.换弹按钮按下 = True
                            self.换弹按钮动画时间 = 0
                            # 调用开始换弹方法
                            self._开始换弹()
            
            # 处理背包事件
            if hasattr(self, '背包管理器') and self.背包管理器.是否打开:
                if self.背包管理器.处理事件(事件):
                    continue
            
            # 使用页面管理器处理所有页面相关事件
            if self.page_manager.handle_key_event(事件):
                continue
            
            # 处理鼠标事件
            if self.page_manager.handle_mouse_event(事件):
                continue
            
            # 处理键盘事件
            if self.page_manager.handle_keyboard_event(事件):
                continue
            
            # 处理合成页面键盘事件
            if hasattr(self, 'crafting_system') and self.crafting_system.is_open:
                if self.crafting_system.handle_keyboard(事件):
                    continue
            
            # 只处理键盘按下事件
            if 事件.type == pygame.KEYDOWN:
                
                # ESC键优先级：1. 关闭帮助页面 2. 关闭创造背包 3. 关闭普通背包 4. 关闭合成页面 5. 关闭箱子页面 6. 关闭熔炉页面 7. 关闭属性提升页面 8. 关闭开发者调试页面 9. 打开/关闭ESC菜单
                if 事件.key == pygame.K_ESCAPE:
                    if self.show_controls:
                        self.show_controls = False
                    elif hasattr(self, 'creative_backpack') and self.creative_backpack.is_open:
                        # 优先关闭创造背包
                        self.creative_backpack.toggle()
                    # 关闭合成页面 - 无论通过何种方式打开
                    elif hasattr(self, 'crafting_system') and self.crafting_system.is_open:
                        self.crafting_system.close()
                        # 同时更新页面管理器的状态，确保状态同步
                        if hasattr(self, 'page_manager'):
                            self.page_manager.page_states['c'] = False
                    # 关闭箱子页面由页面管理器统一处理，这里不需要单独处理
                    # 关闭熔炉页面
                    elif hasattr(self, 'furnace_manager') and self.furnace_manager.是否打开:
                        # 处理熔炉页面的键盘事件
                        if self.furnace_manager.handle_keyboard(事件):
                            pass  # 熔炉页面已处理ESC键事件
                    # 关闭属性提升页面
                    elif hasattr(self, '属性提升页面') and self.属性提升页面.is_open:
                        self.属性提升页面.toggle()
                    # 关闭开发者调试页面
                    elif hasattr(self, 'dev_debug_page') and self.dev_debug_page.is_open:
                        self.dev_debug_page.toggle()
                    else:
                        # 切换ESC菜单显示状态
                        # 关闭ESC菜单功能
                        self.show_esc_menu = False
                # F1键切换帮助页面
                elif 事件.key == pygame.K_F1:
                    self.show_controls = not self.show_controls
                    self.help_scroll_offset = 0  # 重置滚动位置
                # F2键打开/关闭属性提升页面
                elif 事件.key == pygame.K_F2:
                    # 如果当前显示ESC菜单或帮助页面，先关闭它们
                    if self.show_esc_menu:
                        self.show_esc_menu = False
                    elif self.show_controls:
                        self.show_controls = False
                    elif hasattr(self, 'creative_backpack') and self.creative_backpack.is_open:
                        # 如果创造背包打开，先关闭它
                        self.creative_backpack.toggle()
                    else:
                        # 切换属性提升页面状态
                        if hasattr(self, '属性提升页面'):
                            self.属性提升页面.toggle()
                        else:
                            # 动态导入属性提升模块并创建实例
                            import 属性提升
                            self.属性提升页面 = 属性提升.属性提升页面(self)
                # F3键打开/关闭创造背包
                elif 事件.key == pygame.K_F3:
                    # 如果当前显示ESC菜单或帮助页面，先关闭它们
                    if self.show_esc_menu:
                        self.show_esc_menu = False
                    elif self.show_controls:
                        self.show_controls = False
                        # 如果普通背包打开，先关闭它
                    else:
                        # 切换创造背包状态
                        self.creative_backpack.toggle()
                # F4键打开/关闭开发者调试页面
                elif 事件.key == pygame.K_F4:
                    # 如果当前显示ESC菜单或帮助页面，先关闭它们
                    if self.show_esc_menu:
                        self.show_esc_menu = False
                    elif self.show_controls:
                        self.show_controls = False
                    elif hasattr(self, 'creative_backpack') and self.creative_backpack.is_open:
                        # 如果创造背包打开，先关闭它
                        self.creative_backpack.toggle()
                    else:
                        # 切换开发者调试页面状态
                        if hasattr(self, 'dev_debug_page'):
                            self.dev_debug_page.toggle()
                        else:
                            # 动态导入开发者调试模块并创建实例
                            import 开发者调试
                            self.dev_debug_page = 开发者调试.DeveloperDebugPanel(self)
                # F5键切换创造模式
                elif 事件.key == pygame.K_F5:
                    self.创造模式 = not self.创造模式
                    print(f"创造模式: {'开启' if self.创造模式 else '关闭'}")
                # C键打开/关闭合成页面
                elif 事件.key == pygame.K_c:
                    # 如果当前显示ESC菜单或帮助页面，先关闭它们
                    if self.show_esc_menu:
                        self.show_esc_menu = False
                    elif self.show_controls:
                        self.show_controls = False
                    elif hasattr(self, 'creative_backpack') and self.creative_backpack.is_open:
                        # 如果创造背包打开，先关闭它
                        self.creative_backpack.toggle()
                    else:
                        # 切换合成系统状态，指定打开方式为键盘
                        self.crafting_system.toggle('keyboard')
                # B键切换背包
                elif 事件.key == pygame.K_b:
                    # 如果当前显示ESC菜单或帮助页面，先关闭它们
                    if self.show_esc_menu:
                        self.show_esc_menu = False
                    elif self.show_controls:
                        self.show_controls = False
                    else:
                        # 切换背包显示状态
                        self.背包管理器.切换()
                # 检查开发者调试页面是否有输入框处于激活状态
                dev_input_active = False
                if hasattr(self, 'dev_debug_page') and self.dev_debug_page.is_open:
                    dev_input_active = self.dev_debug_page.is_input_active or self.dev_debug_page.active_input is not None
                
                # 处理数字键1-8切换快捷栏格子（无论是否在创造模式下都应该生效）
                # 但当开发者调试页面输入框激活时，不执行快捷栏切换
                if not dev_input_active:
                    # 数字键切换快捷栏格子逻辑
                    旧格子 = self.当前选中格子
                    if 事件.key == pygame.K_1:
                        self.当前选中格子 = 0  # 切换到格1
                    elif 事件.key == pygame.K_2:
                        self.当前选中格子 = 1  # 切换到格2
                    elif 事件.key == pygame.K_3:
                        self.当前选中格子 = 2  # 切换到格3
                    elif 事件.key == pygame.K_4:
                        self.当前选中格子 = 3  # 切换到格4
                    elif 事件.key == pygame.K_5:
                        self.当前选中格子 = 4  # 切换到格5
                    elif 事件.key == pygame.K_6:
                        self.当前选中格子 = 5  # 切换到格6
                    elif 事件.key == pygame.K_7:
                        self.当前选中格子 = 6  # 切换到格7
                    elif 事件.key == pygame.K_8:
                        self.当前选中格子 = 7  # 切换到格8
                    
                    # 只有在实际更换了物品时才取消换弹
                    if hasattr(self, '换弹中') and self.换弹中 and 旧格子 != self.当前选中格子:
                        self.换弹中 = False
                        self.显示换弹进度条 = False
                        self._show_notification("换弹取消")
                
                # 处理Q键按下事件（无论开发者调试页面是否激活都可以使用）
                if 事件.key == pygame.K_q:
                    print(f"Q键按下，正在处理...")
                    # 检查当前是否手持远程武器（弓、弩、手枪、步枪、狙击枪或喷子）
                    工具实例, 当前工具 = self.获取当前手持工具()
                    print(f"获取当前手持工具：工具实例={工具实例}，当前工具={当前工具}")
                    手持远程武器 = 当前工具 and ('弓' in 当前工具['名称'] or '弩' in 当前工具['名称'] or '手枪' in 当前工具['名称'] or '步枪' in 当前工具['名称'] or '狙击枪' in 当前工具['名称'] or '火箭筒' in 当前工具['名称'] or 'RPG' in 当前工具['名称'] or '激光炮' in 当前工具['名称'] or '喷子' in 当前工具['名称'] or '冲锋枪' in 当前工具['名称'] or '龙息' in 当前工具['名称'] or '机甲' in 当前工具['名称'] or '榴弹炮' in 当前工具['名称'] or '加特林' in 当前工具['名称'] or ('齐天' in 当前工具['名称'] and '金箍棒' not in 当前工具['名称']) or '五子棋' in 当前工具['名称'] or '救世主' in 当前工具['名称']) if 当前工具 else False
                    
                    # 检查是否手持特殊武器（死神的镰刀或灵火剑）
                    手持特殊武器 = False
                    if 当前工具:
                        武器名称 = 当前工具['名称']
                        print(f"当前武器名称={武器名称}")
                        手持特殊武器 = '死神的镰刀' in 武器名称 or '灵火剑' in 武器名称 or '超暗黑刺刀' in 武器名称 or '亡灵斧头' in 武器名称 or '火焰三叉戟' in 武器名称 or '齐天金箍棒' in 武器名称
                        print(f"手持特殊武器={手持特殊武器}")
                    
                    # 调用武器技能管理器处理Q键按下事件
                    if 当前工具:
                        weapon_name = 当前工具['名称']
                        print(f"调用武器技能管理器，武器名称={weapon_name}")
                        武器技能管理器实例.handle_input(事件, self.玩家, weapon_name)
                    else:
                        print("当前工具为空，无法调用武器技能管理器")
                    
                    if 手持远程武器:
                        # 手持远程武器时，按Q键直接发射，不执行长按逻辑
                        # 获取鼠标当前位置
                        鼠标位置 = pygame.mouse.get_pos()
                        # 射箭/发射子弹
                        self.射箭(鼠标位置)
                    elif not 手持特殊武器:
                        # 非远程武器且非特殊武器，执行长按逻辑
                        # 记录Q键按下状态和时间
                        self.q_pressed = True
                        self.q_press_time = time.time()
                        self.q_holding_time = 0
                        self.q_sound_played = False
                    else:
                        # 手持死神的镰刀，不执行长按逻辑，避免与技能冲突
                        pass
                elif 事件.key == pygame.K_x and hasattr(self, '属性提升页面') and self.属性提升页面.is_open:
                    # X键关闭属性提升页面
                    self.属性提升页面.toggle()
                elif 事件.key == pygame.K_x and hasattr(self, 'dev_debug_page') and self.dev_debug_page.is_open:
                    # X键关闭开发者调试页面
                    self.dev_debug_page.toggle()
                # R键换弹功能
                elif 事件.key == pygame.K_r:
                    # 获取当前手持工具
                    工具实例, 当前工具 = self.获取当前手持工具()
                    if 当前工具:
                        武器名称 = 当前工具.get('名称', '')
                    是否手枪 = '手枪' in 武器名称
                    是否步枪 = '步枪' in 武器名称
                    是否狙击枪 = '狙击枪' in 武器名称
                    是否喷子 = '喷子' in 武器名称
                    是否冲锋枪 = '冲锋枪' in 武器名称
                    是否齐天武器 = '齐天' in 武器名称
                    if 是否手枪 or 是否步枪 or 是否狙击枪 or 是否喷子 or 是否冲锋枪 or 是否齐天武器:
                            # 开始换弹
                            self._开始换弹()
                elif self.创造模式:
                    # 创造模式：快速放置方块（示例）
                    pass
            # 禁用窗口大小调整功能，使用统一窗口
            # elif 事件.type == pygame.VIDEORESIZE:
            #     global 宽度, 高度
            #     宽度, 高度 = 事件.w, 事件.h
            #     self.屏幕 = pygame.display.set_mode((宽度, 高度), pygame.RESIZABLE)
            elif 事件.type == pygame.MOUSEMOTION:
                # 如果死亡页面已打开，将鼠标事件传递给死亡页面处理
                if hasattr(self, 'death_page_open') and self.death_page_open and hasattr(self, 'death_page'):
                    self.death_page.handle_mouse_motion(事件)
                elif self.show_esc_menu:
                    # 将鼠标事件传递给ESC菜单处理
                    self.esc_page.handle_mouse_motion(事件)
                    # 处理拖拽事件
                    self.esc_page.handle_mouse_drag(事件)
                elif hasattr(self, 'creative_backpack') and self.creative_backpack.is_open:
                    # 如果创造背包打开，处理其鼠标移动事件
                    self.creative_backpack.handle_mouse_motion(事件)
                elif hasattr(self, '属性提升页面') and self.属性提升页面.is_open:
                    # 如果属性提升页面打开，处理其鼠标事件
                    self.属性提升页面.handle_event(事件)
                elif hasattr(self, 'dev_debug_page') and self.dev_debug_page.is_open:
                    # 如果开发者调试页面打开，处理其鼠标事件
                    self.dev_debug_page.handle_event(事件)
                    # 如果背包打开，不处理游戏内的挖掘逻辑
                    pass
                # 箱子页面的处理由页面管理器统一处理，这里不需要单独处理
                elif self.正在挖掘:
                    # 如果鼠标移动到其他方块，停止当前挖掘
                    新的挖掘位置 = self.获取鼠标指向的方块(事件.pos)
                    if 新的挖掘位置 != self.挖掘位置:
                        self.停止挖掘()
            elif 事件.type == pygame.MOUSEBUTTONDOWN:
                # 如果死亡页面已打开，处理死亡页面的鼠标点击
                if hasattr(self, 'death_page_open') and self.death_page_open and hasattr(self, 'death_page'):
                    self.death_page.handle_mouse_click(事件)
                elif self.show_esc_menu:
                    # 将鼠标点击事件传递给ESC菜单处理
                    result = self.esc_page.handle_mouse_click(事件)
                    if result is not None:
                        self.show_esc_menu = False
                        if result == "退出存档":
                            # 退出存档，关闭游戏
                            print("正在退出存档，返回开始游戏页面...")
                            self.运行中 = False
                        elif not result:
                            self.运行中 = False
                    # 处理鼠标按下事件（用于拖拽滑块）
                    self.esc_page.handle_mouse_down(事件)
                elif hasattr(self, 'creative_backpack') and self.creative_backpack.is_open:
                    # 如果创造背包打开，处理其鼠标点击事件
                    self.creative_backpack.handle_mouse_click(事件)
                elif hasattr(self, 'dev_debug_page') and self.dev_debug_page.is_open:
                    # 如果开发者调试页面打开，处理其鼠标点击事件
                    self.dev_debug_page.handle_event(事件)
                    # 将鼠标点击事件传递给背包管理器处理
                # 箱子页面的鼠标点击事件由页面管理器统一处理，这里不需要单独处理
                elif hasattr(self, 'crafting_system') and self.crafting_system.is_open:
                    # 将所有鼠标事件传递给合成系统处理
                    if 事件.type == pygame.MOUSEBUTTONDOWN:
                        # 鼠标按下事件
                        self.crafting_system.handle_click(事件.pos[0], 事件.pos[1], 事件.button)
                    elif 事件.type == pygame.MOUSEMOTION:
                        # 鼠标移动事件，用于悬停检测
                        self.crafting_system._update_hovered_slot()
                    elif 事件.type == pygame.MOUSEBUTTONUP:
                        # 鼠标释放事件
                        pass
                else:
                    # 正常游戏状态下的鼠标按下处理
                    if 事件.button == 1:  # 左键按下
                        # 设置鼠标左键按下状态
                        self.mouse_left_pressed = True
                        self.mouse_press_time = time.time()
                        self.mouse_holding_time = 0
                        # 检查是否点击了快捷栏格子
                        格子索引 = self.检查快捷栏点击(事件.pos)
                        if 格子索引 != -1:
                            # 如果点击了不同的格子，切换当前选中格子
                            if 格子索引 != self.当前选中格子:
                                # 如果正在换弹，取消换弹
                                if hasattr(self, '换弹中') and self.换弹中:
                                    self.换弹中 = False
                                    self.显示换弹进度条 = False
                                    self._show_notification("换弹取消")
                            self.当前选中格子 = 格子索引
                        else:
                            # 检查当前是否手持远程武器（弓、弩或手枪）
                            工具实例, 当前工具 = self.获取当前手持工具()
                            手持远程武器 = False
                            手持工具 = False
                            if 当前工具:
                                武器名称 = 当前工具.get('名称', '')
                                手持远程武器 = ('弓' in 武器名称 or '弩' in 武器名称 or '手枪' in 武器名称 or '步枪' in 武器名称 or '狙击枪' in 武器名称 or '火箭筒' in 武器名称 or 'RPG' in 武器名称 or '激光炮' in 武器名称 or '喷子' in 武器名称 or '冲锋枪' in 武器名称 or '龙息' in 武器名称 or '机甲' in 武器名称 or '榴弹炮' in 武器名称 or '加特林' in 武器名称 or ('齐天' in 武器名称 and '金箍棒' not in 武器名称) or '五子棋' in 武器名称 or '救世主' in 武器名称)
                                手持工具 = ('镐' in 武器名称 or '斧' in 武器名称 or '铲' in 武器名称)
                            
                            if 手持远程武器:
                                # 手持远程武器时，禁用近战攻击和挖掘，改为射箭/发射子弹
                                self.射箭(事件.pos)
                            elif 手持工具:
                                # 手持工具（斧、镐、铲），根据鼠标指向目标类型决定行为
                                # 获取鼠标指向的方块坐标
                                方块坐标 = self.获取鼠标指向的方块(事件.pos)
                                if 方块坐标:
                                    方块_x, 方块_y = 方块坐标
                                    # 获取当前方块ID
                                    当前方块_id = self.世界.get_block(方块_x, 方块_y)
                                    
                                    from 物品定义 import 空气
                                    if 当前方块_id != 空气 and 当前方块_id != "空气":
                                        # 鼠标指向非空气方块，开始挖掘
                                        self.开始挖掘(事件.pos)
                                    else:
                                        # 鼠标指向空气或生物，尝试攻击生物
                                        self.攻击生物(事件.pos)
                            else:
                                # 手持其他物品，先检测是否点击到了生物
                                if not self.攻击生物(事件.pos):
                                    # 如果没有点击到生物，再开始挖掘
                                    self.开始挖掘(事件.pos)
                    elif 事件.button == 3:  # 右键按下，处理放置方块或箱子交互
                        # 先检查当前是否手持远程武器，如果是则发射子弹
                        工具实例, 当前工具 = self.获取当前手持工具()
                        手持远程武器 = False
                        if 当前工具:
                            武器名称 = 当前工具.get('名称', '')
                            手持远程武器 = ('弓' in 武器名称 or '弩' in 武器名称 or '手枪' in 武器名称 or '步枪' in 武器名称 or '狙击枪' in 武器名称 or '火箭筒' in 武器名称 or 'RPG' in 武器名称 or '激光炮' in 武器名称 or '喷子' in 武器名称 or '冲锋枪' in 武器名称 or '龙息' in 武器名称 or '机甲' in 武器名称 or '榴弹炮' in 武器名称 or '加特林' in 武器名称 or ('齐天' in 武器名称 and '金箍棒' not in 武器名称) or '五子棋' in 武器名称 or '救世主' in 武器名称)
                        
                        if 手持远程武器:
                            # 手持远程武器时，右键也发射子弹
                            self.射箭(事件.pos)
                        else:
                            # 不是远程武器，处理放置方块或箱子交互
                            # 获取鼠标指向的方块坐标
                            方块坐标 = self.获取鼠标指向的方块(事件.pos)
                            放置_x, 放置_y = None, None  # 初始化放置位置为None
                            if 方块坐标:
                                方块_x, 方块_y = 方块坐标
                                # 检查是否点击的是箱子方块
                                # 从物品定义中获取箱子的方块ID和空气方块ID
                                from 物品定义 import 物品 as 物品定义
                                from 物品定义 import 空气
                                # 获取箱子的方块ID
                                箱子 = None
                                for 物品_id, 物品_info in 物品定义.items():
                                    if 物品_info.get("名称") == "箱子" and 物品_info.get("类型") == "block":
                                        箱子 = 物品_id
                                        break
                                # 获取当前方块ID，兼容无限世界
                                当前方块_id = self.世界.get_block(方块_x, 方块_y)
                                
                                # 检查是否点击的是箱子方块
                                if 当前方块_id == "箱子" or 当前方块_id == 箱子:
                                    # 使用页面管理器打开箱子页面
                                    # 设置箱子位置并加载对应数据
                                    self.page_manager.pages['chest'].设置箱子坐标(方块_x, 方块_y)
                                    # 打开箱子页面
                                    self.page_manager._open_page('chest')
                                # 检查是否点击的是熔炉方块
                                elif 当前方块_id == "熔炉" or 当前方块_id == 熔炉:
                                    # 使用页面管理器打开熔炉页面，直接传递坐标
                                    self.page_manager._open_page('v', 方块_x, 方块_y)
                                elif 当前方块_id == "工作台" or 当前方块_id == 工作台:
                                    # 使用页面管理器打开合成页面，确保状态统一管理
                                    # 先关闭可能打开的其他页面
                                    if self.show_esc_menu:
                                        self.show_esc_menu = False
                                    elif self.show_controls:
                                        self.show_controls = False
                                    elif hasattr(self, 'creative_backpack') and self.creative_backpack.is_open:
                                        self.creative_backpack.toggle()
                                    # 使用页面管理器打开合成页面，指定打开方式为工作台
                                    self.crafting_system.open('workbench')
                                    # 同时更新页面管理器的状态，确保ESC键能正确处理
                                    self.page_manager.page_states['c'] = True
                                    self.page_manager.pages['c'] = self.crafting_system
                                else:
                                    # 计算放置位置：如果点击的是空方块，直接放置；否则尝试放置在旁边
                                    放置_x, 放置_y = self.计算放置位置(方块_x, 方块_y)
                                
                                if 放置_x is not None and 放置_y is not None:
                                    # 检查放置位置是否为空且在世界范围内 - 兼容无限世界
                                    放置位置有效 = False
                                    if self.世界.无限世界:
                                        # 无限世界，只检查y坐标和方块是否为空
                                        if 0 <= 放置_y < self.世界.高度 and self.世界.get_block(放置_x, 放置_y) == 空气:
                                            放置位置有效 = True
                                    else:
                                        # 有限世界，检查x和y坐标以及方块是否为空
                                        if 0 <= 放置_x < self.世界.宽度 and 0 <= 放置_y < self.世界.高度 and self.世界.get_block(放置_x, 放置_y) == 空气:
                                            放置位置有效 = True
                                    
                                    if 放置位置有效:
                                        # 检查与玩家的碰撞（防止放在自己身上）
                                        if not self.check_placement_collision(放置_x, 放置_y):
                                            # 从背包管理器获取当前选中格子的物品
                                            if hasattr(self, '背包管理器'):
                                                当前选中格子 = self.当前选中格子
                                                物品 = self.背包管理器.快捷栏物品[当前选中格子]
                                                if 物品:
                                                    from 物品定义 import 方块属性
                                                    from 物品定义 import 物品 as 物品定义
                                                    物品_id = 物品.物品_id
                                                    
                                                    # 获取物品信息
                                                    物品_info = 物品定义.get(物品_id, {})
                                                    物品类型 = 物品_info.get("类型", "")
                                                    
                                                    if 物品类型 == "生物蛋":
                                                        # 生物蛋：生成对应的生物
                                                        from 生物系统 import Mob
                                                        # 获取生物蛋对应的生物ID
                                                        生物_id_map = {
                                                        史莱姆蛋: 史莱姆,
                                                        土拨鼠蛋: 土拨鼠,
                                                        幽灵蛋: 幽灵,
                                                        蝙蝠蛋: 蝙蝠,
                                                        火焰精灵蛋: 火焰精灵,
                                                        蘑菇怪蛋: 蘑菇怪,
                                                        岩石怪蛋: 岩石怪,
                                                        猴子蛋: 猴子,
                                                        三角龙蛋: 三角龙,
                                                        丧尸蛋: 丧尸,
                                                        企鹅蛋: 企鹅,
                                                        僵尸蛋: 僵尸,
                                                        刺球蛋: 刺球,
                                                        双角骷髅蛋: 双角骷髅,
                                                        变形怪蛋: 变形怪,
                                                        可爱幽灵蛋: 可爱幽灵,
                                                        吸血鬼蛋: 吸血鬼,
                                                        夜魔蛋: 夜魔,
                                                        大史莱姆蛋: 大史莱姆,
                                                        奶龙蛋: 奶龙,
                                                        小恶魔蛋: 小恶魔,
                                                        小熊猫蛋: 小熊猫,
                                                        小霸王龙蛋: 小霸王龙,
                                                        小鸡蛋: 小鸡,
                                                        岩浆怪蛋: 岩浆怪,
                                                        幽灵人蛋: 幽灵人,
                                                        建龙蛋: 建龙,
                                                        异变者蛋: 异变者,
                                                        异变骷髅蛋: 异变骷髅,
                                                        异形眼蛋: 异形眼,
                                                        异形球体蛋: 异形球体,
                                                        异形蛇蛋: 异形蛇,
                                                        异形蜘蛛蛋: 异形蜘蛛,
                                                        恶魔球蛋: 恶魔球,
                                                        普通骷髅蛋: 普通骷髅,
                                                        松鼠蛋: 松鼠,
                                                        母鸡蛋: 母鸡,
                                                        灰兔蛋: 灰兔,
                                                        牧羊人蛋: 牧羊人,
                                                        狗蛋: 狗,
                                                        独眼人蛋: 独眼人,
                                                        狼人蛋: 狼人,
                                                        猪蛋: 猪,
                                                        白兔蛋: 白兔,
                                                        章鱼蛋: 章鱼,
                                                        章鱼怪蛋: 章鱼怪,
                                                        红眼粘液怪蛋: 红眼粘液怪,
                                                        老虎蛋: 老虎,
                                                        萌刺蛋: 萌刺,
                                                        蓝怪蛋: 蓝怪,
                                                        蚂蚁怪物蛋: 蚂蚁怪物,
                                                        贝利亚蛋: 贝利亚,
                                                        超异变者蛋: 超异变者,
                                                        邪恶粘液怪蛋: 邪恶粘液怪,
                                                        邪恶蜘蛛蛋: 邪恶蜘蛛,
                                                        邪恶蝙蝠蛋: 邪恶蝙蝠,
                                                        金怪蛋: 金怪,
                                                        问灵蛋: 问灵,
                                                        霸王龙蛋: 霸王龙,
                                                        骷髅球蛋: 骷髅球,
                                                        鸟蛋: 鸟,
                                                        死神祝福蛋: 死神祝福,
                                                        肥胖蛋: 肥胖Boss,
                                                        死神蛋: 死神
                                                    }
                                                        
                                                        对应生物_id = 生物_id_map.get(物品_id)
                                                        if 对应生物_id:
                                                            # 计算生物生成位置（方块中心）
                                                            生物_x = 放置_x * 方块大小 + 方块大小 // 2
                                                            生物_y = 放置_y * 方块大小
                                                            # 创建生物实例
                                                            新生物 = Mob(生物_x, 生物_y, 对应生物_id)
                                                            # 将生物添加到世界
                                                            self.世界.mobs.append(新生物)
                                                            # 检查是否是BOSS生物，进行特殊处理
                                                            # 减少物品数量
                                                            物品.数量 -= 1
                                                            if 物品.数量 <= 0:
                                                                # 物品数量为0，从快捷栏移除
                                                                self.背包管理器.快捷栏物品[当前选中格子] = None
                                                            # 播放放置音效
                                                            try:
                                                                audio_manager.play_sound("放置")
                                                            except:
                                                                pass
                                                    elif 物品_id in 方块属性:
                                                        # 普通方块：放置方块
                                                        # 检查是否启用了3*3放置
                                                        if self.enable_3x3_place:
                                                            # 3*3放置：以目标位置为中心，放置3x3区域的方块
                                                            for dx in range(-1, 2):
                                                                for dy in range(-1, 2):
                                                                    nx, ny = 放置_x + dx, 放置_y + dy
                                                                    # 边界检查 - 兼容无限世界
                                                                    if (self.世界.无限世界 and 0 <= ny < self.世界.高度) or (not self.世界.无限世界 and 0 <= nx < self.世界.宽度 and 0 <= ny < self.世界.高度):
                                                                        # 检查放置位置是否为空 - 兼容无限世界
                                                                        if self.世界.get_block(nx, ny) == 空气:
                                                                            # 检查放置位置是否与玩家碰撞
                                                                            if not self.check_placement_collision(nx, ny):
                                                                                # 放置方块 - 兼容无限世界
                                                                                self.世界.set_block(nx, ny, 物品_id)
                                                        else:
                                                            # 普通放置：只放置目标位置的方块
                                                            # 放置方块 - 兼容无限世界
                                                            self.世界.set_block(放置_x, 放置_y, 物品_id)
                                                         
                                                        # 只减少一次物品数量，无论放置了多少个方块
                                                        物品.数量 -= 1
                                                        if 物品.数量 <= 0:
                                                            # 物品数量为0，从快捷栏移除
                                                            self.背包管理器.快捷栏物品[当前选中格子] = None
                                                        # 播放放置方块音效
                                                        try:
                                                            audio_manager.play_sound("放置方块")
                                                        except:
                                                            pass
                                                    else:
                                                        # 检查是否为可种植的种子物品
                                                        # 种子到发芽方块的映射关系
                                                        from 物品定义 import 物品 as 物品定义
                                                        from 物品定义 import 土块, 草方块, 水
                                                        
                                                        from 物品定义 import 空气
                                                        # 定义种子物品到发芽方块的映射
                                                        种子映射 = {
                                                            17035: 10045,  # 土豆 -> 土豆发芽
                                                            17041: 10054,  # 玉米 -> 玉米发芽
                                                            17043: 10051,  # 生米 -> 水稻发芽
                                                            17042: 10057,  # 甘蔗 -> 甘蔗幼年
                                                            17045: 10059,  # 番薯 -> 番薯发芽
                                                            17046: 10062   # 白菜 -> 白菜发芽
                                                        }
                                                        
                                                        if 物品_id in 种子映射:
                                                            # 检查点击的方块是否为土块、草方块或水
                                                            点击的方块_id = self.世界.get_block(方块_x, 方块_y)
                                                            可种植表面 = [土块, 草方块, 水]
                                                            
                                                            if 点击的方块_id in 可种植表面:
                                                                # 获取对应的发芽方块ID
                                                                发芽方块_id = 种子映射[物品_id]
                                                                
                                                                # 检查放置位置是否为空且在世界范围内
                                                                放置位置有效 = False
                                                                if self.世界.无限世界:
                                                                    # 无限世界，只检查y坐标和方块是否为空
                                                                    if 0 <= 放置_y < self.世界.高度 and self.世界.get_block(放置_x, 放置_y) == 空气:
                                                                        放置位置有效 = True
                                                                else:
                                                                    # 有限世界，检查x和y坐标以及方块是否为空
                                                                    if 0 <= 放置_x < self.世界.宽度 and 0 <= 放置_y < self.世界.高度 and self.世界.get_block(放置_x, 放置_y) == 空气:
                                                                        放置位置有效 = True
                                                                    
                                                                if 放置位置有效:
                                                                    # 放置发芽方块
                                                                    self.世界.set_block(放置_x, 放置_y, 发芽方块_id)
                                                                    # 减少物品数量
                                                                    物品.数量 -= 1
                                                                    if 物品.数量 <= 0:
                                                                        # 物品数量为0，从快捷栏移除
                                                                        self.背包管理器.快捷栏物品[当前选中格子] = None
                                                                    # 播放放置音效
                                                                    try:
                                                                        audio_manager.play_sound("放置")
                                                                    except:
                                                                        pass
                    elif 事件.button == 4 or 事件.button == 5:
                        if self.show_controls:
                            # 在帮助页面显示时，处理滚动
                            if 事件.button == 4:  # 向上滚动
                                self.help_scroll_offset = max(0, self.help_scroll_offset - self.scroll_speed)
                            elif 事件.button == 5:  # 向下滚动
                                self.help_scroll_offset = min(self.help_max_scroll_offset, self.help_scroll_offset + self.scroll_speed)
                        else:
                            # 不在帮助页面时，切换快捷栏格子
                            旧格子 = self.当前选中格子
                            if 事件.button == 4:  # 滚轮向上滚动
                                self.当前选中格子 = (self.当前选中格子 - 1) % 8
                            elif 事件.button == 5:  # 滚轮向下滚动
                                self.当前选中格子 = (self.当前选中格子 + 1) % 8
                            # 只有在实际更换了物品时才取消换弹
                            if hasattr(self, '换弹中') and self.换弹中 and 旧格子 != self.当前选中格子:
                                self.换弹中 = False
                                self.显示换弹进度条 = False
                                self._show_notification("换弹取消")
            elif 事件.type == pygame.MOUSEBUTTONUP:
                if self.show_esc_menu:
                    # 将鼠标释放事件传递给ESC菜单处理（用于结束拖拽滑块）
                    self.esc_page.handle_mouse_up(事件)
                elif 事件.button == 1:  # 左键释放
                    # 重置鼠标左键状态
                    self.mouse_left_pressed = False
                    self.mouse_holding_time = 0
                    self.停止挖掘()
            # 处理鼠标滚轮滚动事件（更现代的方式）
            elif 事件.type == pygame.MOUSEWHEEL:
                if self.show_controls:
                    # 使用滚轮增量进行滚动，更加流畅
                    scroll_amount = 事件.y * self.scroll_speed
                    if scroll_amount > 0:
                        # 向上滚动
                        self.help_scroll_offset = max(0, self.help_scroll_offset - scroll_amount)
                    else:
                        # 向下滚动
                        self.help_scroll_offset = min(self.help_max_scroll_offset, self.help_scroll_offset + abs(scroll_amount))
                else:
                    # 不在帮助页面时，切换快捷栏格子
                    旧格子 = self.当前选中格子
                    if 事件.y > 0:  # 滚轮向上滚动
                        self.当前选中格子 = (self.当前选中格子 - 1) % 8
                    elif 事件.y < 0:  # 滚轮向下滚动
                        self.当前选中格子 = (self.当前选中格子 + 1) % 8
                    # 只有在实际更换了物品时才取消换弹
                    if hasattr(self, '换弹中') and self.换弹中 and 旧格子 != self.当前选中格子:
                        self.换弹中 = False
                        self.显示换弹进度条 = False
                        self._show_notification("换弹取消")
    
    def update(self, 时间增量):
        """更新游戏状态"""
        # 更新换弹按钮动画时间
        if hasattr(self, '换弹按钮按下') and self.换弹按钮按下:
            self.换弹按钮动画时间 += 时间增量
            if self.换弹按钮动画时间 > self.换弹按钮动画时长:
                self.换弹按钮动画时间 = self.换弹按钮动画时长
        
        # 检查玩家是否死亡
        if self.玩家.current_health <= 0 and not hasattr(self, 'death_page_open'):
            self.death_page_open = True
            from 死亡页面 import DeathPage
            self.death_page = DeathPage(self)
        
        # 如果死亡页面已打开，直接返回，不更新游戏状态
        if hasattr(self, 'death_page_open') and self.death_page_open:
            return
        
        # 更新状态管理器
        from 状态管理 import 状态管理器实例
        状态管理器实例.更新(时间增量)
        
        # 获取按键状态
        按键状态 = pygame.key.get_pressed()
        
        # 处理长按Q键使用物品的逻辑
        self._handle_q_key_hold(时间增量)
        
        # 更新玩家和世界
        self.玩家.update(按键状态, self.世界, 时间增量)
        self.世界.update(时间增量)
        
        # 草悬空检测和删除
        self.草检查计时器 += 时间增量
        if self.草检查计时器 >= self.草检查间隔:
            self.世界.check_and_remove_floating_grass()
            self.草检查计时器 = 0
        
        # 更新武器技能管理器
        武器技能管理器实例.update(时间增量, self.世界, self.玩家, self)
        
        # 更新挖掘进度
        self.更新挖掘进度(时间增量)
        
        # 更新漂浮文字
        self._update_notifications(时间增量)
        
        # 更新激光效果
        if hasattr(self, 'laser_effects'):
            self.laser_effects = [laser for laser in self.laser_effects if not laser.update(时间增量)]
        
        # 更新龙息激光效果
        if hasattr(self, '龙息激光效果列表'):
            self.龙息激光效果列表 = [laser for laser in self.龙息激光效果列表 if not laser.update(时间增量)]
        
        # 更新爆炸效果
        if hasattr(self, 'explosion_effects'):
            self.explosion_effects = [explosion for explosion in self.explosion_effects if not explosion.update(时间增量)]
        
        # 更新弧线劈砍效果
        if hasattr(self, 'slash_effects'):
            # 更新每个特效的位置为玩家当前位置，使特效跟随玩家移动
            for slash in self.slash_effects:
                # 计算玩家中心位置 - 使用正确的中文属性名
                player_center_x = self.玩家.坐标_x + self.玩家.宽 // 2
                player_center_y = self.玩家.坐标_y + self.玩家.高 // 2
                # 更新特效位置
                slash.x = player_center_x
                slash.y = player_center_y
            # 然后更新特效状态
            self.slash_effects = [slash for slash in self.slash_effects if not slash.update(时间增量)]
        
        # 更新灵火剑持续伤害效果
        if hasattr(self, 'linghuo_sword_effects'):
            self.linghuo_sword_effects = [effect for effect in self.linghuo_sword_effects if not effect.update(时间增量, self)]
        
        # 更新技能效果（如亡灵法杖的持续召唤效果）
        if hasattr(self, 'skill_effects'):
            self.skill_effects = [effect for effect in self.skill_effects if not effect.update(时间增量)]
        
        # 处理延迟伤害事件（如电磁发射器的额外伤害）
        if hasattr(self, 'timed_damage_events'):
            当前时间 = pygame.time.get_ticks()
            # 创建一个列表来存储需要移除的事件ID
            events_to_remove = []
            
            # 遍历所有延迟伤害事件
            for event_id, event_data in self.timed_damage_events.items():
                # 检查事件是否到了触发时间
                if 当前时间 >= event_id:
                    # 获取事件数据
                    mob = event_data['mob']
                    damage = event_data['damage']
                    color = event_data['color']
                    
                    # 检查生物是否还活着
                    if hasattr(mob, 'health') and mob.health > 0:
                        # 确保mob.game存在
                        mob.game = self
                        # 造成伤害
                        死亡 = mob.take_damage(damage)
                        
                        # 创建伤害文本
                        if hasattr(self, 'damage_texts'):
                            damage_text = self.DamageText(
                                mob.x + mob.width // 2, 
                                mob.y - 10, 
                                damage, 
                                color=color
                            )
                            self.damage_texts.append(damage_text)
                        
                        # 如果目标死亡，生成经验球和掉落物
                        if 死亡:
                            # 生成经验球
                            self.spawn_exp_orbs(mob.x // 32, mob.y // 32)
                            
                            # 尝试生成掉落物
                            try:
                                from 掉落物 import 掉落物管理器实例
                                from 生物系统 import 生物掉落物配置
                                掉落物管理器实例.生成生物掉落物(
                                    self.世界,
                                    int(mob.x // 32),
                                    int(mob.y // 32),
                                    getattr(mob, 'name', ''),
                                    getattr(mob, 'mob_id', 0),
                                    生物掉落物配置
                                )
                            except Exception as e:
                                print(f"生成生物掉落物失败: {e}")
                                # 备用方案
                                from 物品定义 import 肉块
                                self.世界.spawn_item(int(mob.x // 32), int(mob.y // 32), 肉块, 1)
                    
                    # 将事件标记为需要移除
                    events_to_remove.append(event_id)
            
            # 移除已触发的事件
            for event_id in events_to_remove:
                if event_id in self.timed_damage_events:
                    del self.timed_damage_events[event_id]
        
        # 检查水状态并控制音频播放
        self.玩家.check_water_status(self.世界)
        
        # 更新火焰三叉戟buff效果
        if hasattr(self.玩家, '火焰三叉戟_buff_active') and self.玩家.火焰三叉戟_buff_active:
            self.玩家.火焰三叉戟_buff_timer += 时间增量
            
            # 检查buff是否过期
            if self.玩家.火焰三叉戟_buff_timer >= self.玩家.火焰三叉戟_buff_duration:
                # buff过期，恢复原始属性
                self.玩家.火焰三叉戟_buff_active = False
                if hasattr(self.玩家, '原始攻击间隔'):
                    delattr(self.玩家, '原始攻击间隔')
                if hasattr(self.玩家, '原始伤害加成'):
                    delattr(self.玩家, '原始伤害加成')
                if hasattr(self.玩家, '原始攻击范围'):
                    delattr(self.玩家, '原始攻击范围')
        
        # 更新闪电三叉戟buff效果
        if hasattr(self.玩家, '闪电三叉戟_buff_active') and self.玩家.闪电三叉戟_buff_active:
            self.玩家.闪电三叉戟_buff_timer += 时间增量
            
            # 检查buff是否过期
            if self.玩家.闪电三叉戟_buff_timer >= self.玩家.闪电三叉戟_buff_duration:
                # buff过期，恢复原始属性
                self.玩家.闪电三叉戟_buff_active = False
                if hasattr(self.玩家, '原始攻击间隔'):
                    delattr(self.玩家, '原始攻击间隔')
                if hasattr(self.玩家, '原始伤害加成'):
                    delattr(self.玩家, '原始伤害加成')
                if hasattr(self.玩家, '原始攻击范围'):
                    delattr(self.玩家, '原始攻击范围')
        
        # 处理玩家捡取掉落物
        self.handle_item_pickup()
        
        # 更新经验小球
        if hasattr(self.世界, 'exp_orbs'):
            # 创建一个新列表来存储需要保留的经验小球
            remaining_orbs = []
            for orb in self.世界.exp_orbs:
                # 更新经验小球
                if not orb.update(时间增量, self.玩家):
                    remaining_orbs.append(orb)
            # 更新经验小球列表
            self.世界.exp_orbs = remaining_orbs
        
        # 更新粒子效果
        self.世界.update_particles(时间增量)
        
        # 更新生物
        self.世界.update_mobs(时间增量, self.玩家)
        
        # 更新Boss
        from boos生物处理 import boss_manager
        boss_manager.update(self.世界, self.玩家)
        
        # 定期生成生物
        
        # 定期生成生物
        if hasattr(self, 'mob_spawn_timer'):
            self.mob_spawn_timer += 时间增量
        else:
            self.mob_spawn_timer = 0
        
        # 每10秒生成一个生物，最多10个
        if self.mob_spawn_timer >= 10 and len(self.世界.mobs) < 10:
            self.世界.spawn_mobs(1, self.玩家, self)
            self.mob_spawn_timer = 0
        
        # 控制音频播放
        from 音频输出 import audio_manager     
        try:
            # 处理水中音效
            if self.玩家.在水中:
                # 在水中：播放游泳音效（播放完再播放），停止水滴音效
                audio_manager.stop_sound("水滴")
                audio_manager.play_sound_loop_when_finished("游泳")
            else:
                # 不在水中：停止游泳音效
                audio_manager.stop_sound("游泳")
                
                # 处理水附近音效
                if self.玩家.在水附近:
                    # 在水附近：播放水滴音效（播放完再播放）
                    audio_manager.play_sound_loop_when_finished("水滴")
                else:
                     # 不在水附近：停止水滴音效
                     audio_manager.stop_sound("水滴")
        except Exception as e:
            print(f"音频控制错误: {e}")
        
        # 更新合成系统
        if hasattr(self, 'crafting_system'):
            self.crafting_system.update(时间增量)
        
        # 更新创造背包
        if hasattr(self, 'creative_backpack') and self.creative_backpack.is_open:
            self.creative_backpack.update()
        
        # 更新熔炉管理器 - 无论页面是否打开，熔炉都要继续燃烧
        if hasattr(self, 'furnace_manager'):
            self.furnace_manager.update(时间增量)
        # 或者通过页面管理器更新熔炉
        if hasattr(self, 'page_manager') and hasattr(self.page_manager, 'pages'):
            furnace_page = self.page_manager.pages.get('v')
            if furnace_page:
                furnace_page.update(时间增量)
        
        # 更新箭矢
        for arrow in self.arrows[:]:
            arrow.update(时间增量, self.世界, self.世界.mobs, self)
            if arrow.is_finished():
                self.arrows.remove(arrow)
        
        # 更新伤害数字
        for text in self.damage_texts[:]:
            text.update(时间增量)
            if text.is_finished():
                self.damage_texts.remove(text)
        
        # 更新换弹状态
        if hasattr(self, '换弹中') and self.换弹中:
            from 物品定义 import 子弹
            
            # 计算换弹进度
            已过时间 = self.当前时间 - self.换弹开始时间
            self.换弹进度 = min(已过时间 / self.换弹总时间, 1.0)
            
            # 检查换弹是否完成
            if self.换弹进度 >= 1.0:
                # 换弹完成
                self.换弹中 = False
                self.显示换弹进度条 = False
                
                # 检查是否有正在换弹的武器实例
                if hasattr(self, '正在换弹的武器') and self.正在换弹的武器:
                    武器实例 = self.正在换弹的武器
                    
                    # 获取当前手持工具信息，判断是否为齐天武器
                    工具实例, 当前工具 = self.获取当前手持工具()
                    is_qitian_weapon = False
                    if 当前工具 and '齐天' in 当前工具.get('名称', ''):
                        is_qitian_weapon = True
                    
                    # 从物品实例获取当前弹匣子弹数，从当前工具获取弹匣容量
                    当前弹匣子弹 = 武器实例.获取属性("当前弹匣子弹", 0)
                    弹匣容量 = 当前工具.get("弹夹", 15)  # 优先使用武器定义的弹夹属性
                    
                    if is_qitian_weapon:
                        # 齐天武器：无限子弹，直接填满弹夹，不消耗背包弹药
                        武器实例.设置属性("当前弹匣子弹", 弹匣容量)
                    else:
                        # 特殊处理所有救世主武器：消耗救世能源，不消耗常规弹药
                        if 当前工具 and '救世主' in 当前工具.get('名称', ''):
                            # 直接填满弹夹
                            武器实例.设置属性("当前弹匣子弹", 弹匣容量)
                            
                            # 消耗救世能源的耐久
                            救世能源实例列表 = []
                            # 遍历背包物品（5x6二维列表）
                            for 行 in self.背包管理器.背包物品:
                                for 背包格子 in 行:
                                    if 背包格子:
                                        from 物品定义 import 物品 as 物品定义
                                        物品_info = 物品定义.get(背包格子.物品_id, {})
                                        if 物品_info.get('名称') == '救世能源':
                                            救世能源实例列表.append(背包格子)
                            # 遍历快捷栏物品
                            for 背包格子 in self.背包管理器.快捷栏物品:
                                if 背包格子:
                                    from 物品定义 import 物品 as 物品定义
                                    物品_info = 物品定义.get(背包格子.物品_id, {})
                                    if 物品_info.get('名称') == '救世能源':
                                        救世能源实例列表.append(背包格子)
                            
                            # 根据武器类型确定消耗的耐久度
                            消耗耐久度 = 30  # 默认消耗30耐久
                            武器名称 = 当前工具.get('名称', '')
                            if '救世主加特林' in 武器名称:
                                消耗耐久度 = 150  # 救世主加特林消耗150耐久
                            elif '救世主喷子' in 武器名称 or '救世主S686' in 武器名称:
                                消耗耐久度 = 20  # 救世主喷子消耗20耐久
                            elif '救世主RPG' in 武器名称:
                                消耗耐久度 = 10  # 救世主RPG消耗10耐久
                            elif '救世主弩' in 武器名称:
                                消耗耐久度 = 1  # 救世主弩每发射消耗1耐久
                            elif '榴弹炮' in 武器名称:
                                消耗耐久度 = 30  # 救世主榴弹炮消耗30耐久
                            
                            # 找到第一个有足够耐久的救世能源并消耗
                            for 能源实例 in 救世能源实例列表:
                                当前耐久 = 能源实例.获取属性("耐久", 能源实例.物品信息.get("最大耐久", 1000))
                                if 当前耐久 >= 消耗耐久度:
                                    # 消耗对应的耐久度
                                    能源损坏 = 能源实例.take_damage(消耗耐久度)
                                    # 如果救世能源损坏，显示提示并从背包中移除
                                    if 能源损坏:
                                        # 播放物品破碎音效
                                        try:
                                            from 音频输出 import audio_manager
                                            audio_manager.play_sound("道具破碎")
                                        except Exception as e:
                                            print(f"播放破碎音效失败: {e}")
                                        # 显示损坏通知
                                        self._show_notification("救世能源 已耗尽")
                                        
                                        # 从背包中移除损坏的救世能源
                                        for i, 行 in enumerate(self.背包管理器.背包物品):
                                            for j, 背包格子 in enumerate(行):
                                                if 背包格子 == 能源实例:
                                                    self.背包管理器.背包物品[i][j] = None
                                                    break
                                        for i, 快捷栏格子 in enumerate(self.背包管理器.快捷栏物品):
                                            if 快捷栏格子 == 能源实例:
                                                self.背包管理器.快捷栏物品[i] = None
                                                break
                                    break
                        else:
                            # 检查是否是机甲武器
                            is_mecha_weapon = False
                            if 当前工具 and '机甲' in 当前工具.get('名称', ''):
                                is_mecha_weapon = True
                            
                            # 根据武器类型选择弹药类型
                            from 物品定义 import 子弹, 机甲弹
                            ammo_type = 机甲弹 if is_mecha_weapon else 子弹
                            
                            # 其他武器：计算需要补充的弹药数量（取背包弹药和剩余空间的最小值）
                            补充弹药数量 = min(弹匣容量 - 当前弹匣子弹, self.背包管理器.获取物品总数量(ammo_type))
                            
                            # 消耗背包中的弹药
                            self.背包管理器.减少物品数量(ammo_type, 补充弹药数量)
                            
                            # 更新物品实例的弹匣子弹数量
                            武器实例.设置属性("当前弹匣子弹", 当前弹匣子弹 + 补充弹药数量)
                    
                    # 清除正在换弹的武器实例
                    self.正在换弹的武器 = None
                
                # 显示换弹完成提示
                self._show_notification("换弹完成！")
                
                # 播放换弹完成音效
                try:
                    from 音频输出 import audio_manager
                    audio_manager.play_sound("换弹")
                except Exception as e:
                    print(f"播放换弹音效失败: {e}")
        
        # 处理长按鼠标左键或长按Q键连续发射
        工具实例, 当前工具 = self.获取当前手持工具()
        是否步枪 = False
        是否喷子 = False
        是否冲锋枪 = False
        是否齐天武器 = False
        是否龙息武器 = False
        是否五子棋 = False
        是否加特林 = False
        武器名称 = ''
        是齐天金箍棒 = False
        if 当前工具:
            武器名称 = 当前工具.get('名称', '')
            是否步枪 = '步枪' in 武器名称
            是否喷子 = '喷子' in 武器名称
            是否冲锋枪 = '冲锋枪' in 武器名称
            是否齐天武器 = '齐天' in 武器名称
            是否龙息武器 = '龙息' in 武器名称
            是否五子棋 = '五子棋' in 武器名称
            是否加特林 = '加特林' in 武器名称
            # 检查是否是齐天金箍棒（近战武器，不发射子弹）
            是齐天金箍棒 = '齐天金箍棒' in 武器名称
        
        if (是否步枪 or 是否喷子 or 是否冲锋枪 or 是否齐天武器 or 是否龙息武器 or 是否五子棋 or 是否加特林 or ('救世主' in 武器名称 and not '弩' in 武器名称)) and not 是齐天金箍棒:
            # 步枪、喷子、冲锋枪、齐天武器、龙息武器、五子棋、加特林和所有救世主武器（除了弩）支持全自动连续发射
            # 检查是否长按鼠标左键或长按Q键
            if self.mouse_left_pressed or self.q_pressed:
                # 获取鼠标当前位置
                鼠标位置 = pygame.mouse.get_pos()
                # 发射子弹或激光
                self.射箭(鼠标位置)
    
    def _handle_q_key_hold(self, 时间增量):
        """处理长按Q键使用物品的逻辑"""
        if self.q_pressed:
            # 检查当前手持物品
            工具实例, 当前工具 = self.获取当前手持工具()
            
            # 如果没有手持物品，直接返回
            if not 工具实例 or not 当前工具:
                return
            
            # 获取物品ID和类型
            item_id = 工具实例.物品_id
            from 物品定义 import 物品 as 物品定义
            物品_info = 物品定义.get(item_id, {})
            物品类型 = 物品_info.get("类型")
            
            # 定义药水的物品ID列表
            from 物品定义 import 一级回血瓶, 二级回血瓶, 三级回血瓶, 四级回血瓶
            potion_items = [一级回血瓶, 二级回血瓶, 三级回血瓶, 四级回血瓶]
            
            # 检查物品是否为食物或药水
            is_food = 物品类型 == "food"
            is_potion = item_id in potion_items
            
            # 只有食物和药水类物品才允许长按Q键使用
            if not (is_food or is_potion):
                return
            
            # 计算长按时间
            self.q_holding_time = time.time() - self.q_press_time
            
            # 播放吃东西音效（仅在开始按住时播放一次）
            if not self.q_sound_played:
                try:
                    from 音频输出 import audio_manager
                    audio_manager.play_sound("吃")
                    self.q_sound_played = True
                except Exception as e:
                    print(f"播放吃食物音效错误: {e}")
            
            # 计算并更新物品使用进度
            self.物品使用进度 = min(self.q_holding_time / self.required_hold_time, 1.0)
            self.显示物品使用进度 = True
            
            # 当长按时间达到要求时，使用物品
            if self.q_holding_time >= self.required_hold_time:
                self._use_hotbar_item()
                # 重置状态
                self.q_pressed = False
                self.q_holding_time = 0
                self.物品使用进度 = 0
                self.显示物品使用进度 = False
    
    def _use_hotbar_item(self):
        """使用快捷栏中的当前选中物品（食物或药水）"""
        # 检查背包管理器是否存在
        if not hasattr(self, '背包管理器'):
            return
        
        # 获取当前选中格子和快捷栏物品列表
        当前格子 = self.当前选中格子
        hotbar_items = self.背包管理器.快捷栏物品
        
        # 检查当前格子索引是否有效且有物品
        if 当前格子 < 0 or 当前格子 >= len(hotbar_items) or hotbar_items[当前格子] is None:
            return
        
        # 获取选中的物品
        选中物品 = hotbar_items[当前格子]
        item_id = 选中物品.物品_id
        
        # 从物品定义中获取物品信息，判断物品类型
        from 物品定义 import 物品 as 物品定义
        物品_info = 物品定义.get(item_id, {})
        物品类型 = 物品_info.get("类型")
        
        # 定义药水的物品ID列表
        potion_items = [一级回血瓶, 二级回血瓶, 三级回血瓶, 四级回血瓶]
        
        # 检查物品是否为食物或药水
        is_food = 物品类型 == "food"
        is_potion = item_id in potion_items
        is_food_or_potion = is_food or is_potion
        
        if is_food_or_potion:
            # 应用物品效果
            self._apply_item_effect(item_id)
            
            # 减少物品数量
            if 选中物品.数量 > 1:
                选中物品.数量 -= 1
            else:
                hotbar_items[当前格子] = None
            
            # 输出使用物品的信息
            print(f"使用了物品: {物品_info.get('名称', '未知物品')} (ID: {item_id})")
    
    def _apply_item_effect(self, item_id):
        """应用物品效果"""
        from 物品定义 import 物品 as 物品定义
        物品_info = 物品定义.get(item_id, {})
        
        # 根据物品类型应用不同效果
        if item_id == 一级回血瓶:
            使用前生命值 = self.玩家.current_health
            self.玩家.current_health = min(self.玩家.current_health + 20, self.玩家.max_health)
            增加后生命值 = self.玩家.current_health
            print(f"使用一级回血瓶：添加前:生命值={使用前生命值}, 增加后:生命值={增加后生命值}")
        elif item_id == 二级回血瓶:
            使用前生命值 = self.玩家.current_health
            self.玩家.current_health = min(self.玩家.current_health + 40, self.玩家.max_health)
            增加后生命值 = self.玩家.current_health
            print(f"使用二级回血瓶：添加前:生命值={使用前生命值}, 增加后:生命值={增加后生命值}")
        elif item_id == 三级回血瓶:
            使用前生命值 = self.玩家.current_health
            self.玩家.current_health = min(self.玩家.current_health + 60, self.玩家.max_health)
            增加后生命值 = self.玩家.current_health
            print(f"使用三级回血瓶：添加前:生命值={使用前生命值}, 增加后:生命值={增加后生命值}")
        elif item_id == 四级回血瓶:
            # 获取物品定义中的效果数据
            生命值恢复 = 物品_info.get("生命值", 100)
            额外生命值恢复 = 物品_info.get("额外生命值", 50)
            
            # 应用普通生命值恢复
            使用前生命值 = self.玩家.current_health
            self.玩家.current_health = min(self.玩家.current_health + 生命值恢复, self.玩家.max_health)
            增加后生命值 = self.玩家.current_health
            
            # 应用额外生命值恢复
            使用前额外生命值 = self.玩家.extra_health
            self.玩家.extra_health += 额外生命值恢复  # 移除最大值限制，允许无限叠加
            增加后额外生命值 = self.玩家.extra_health
            
            # 更新曾经最大额外生命值
            if self.玩家.extra_health > self.玩家.曾经最大额外生命值:
                self.玩家.曾经最大额外生命值 = self.玩家.extra_health
            
            print(f"使用四级回血瓶：添加前:生命值={使用前生命值}, 增加后:生命值={增加后生命值}")
            print(f"使用四级回血瓶：添加前:额外生命值={使用前额外生命值}, 增加后:额外生命值={增加后额外生命值}")
        elif 物品_info.get("类型") == "food":
            # 食物效果 - 恢复饥饿值和生命值
            使用前饥饿值 = self.玩家.current_hunger
            使用前生命值 = self.玩家.current_health
            
            # 从物品定义中获取饥饿值和生命值恢复量
            饥饿值恢复 = 物品_info.get("饥饿值", 20)
            生命值恢复 = 物品_info.get("生命值", 5)
            
            # 应用效果
            self.玩家.current_hunger = min(self.玩家.current_hunger + 饥饿值恢复, self.玩家.max_hunger)
            self.玩家.current_health = min(self.玩家.current_health + 生命值恢复, self.玩家.max_health)
            
            增加后饥饿值 = self.玩家.current_hunger
            增加后生命值 = self.玩家.current_health
            食物名称 = 物品_info.get("名称", "未知食物")
            
            print(f"使用{食物名称}：添加前:饥饿值={使用前饥饿值}, 增加后:饥饿值={增加后饥饿值}")
            print(f"使用{食物名称}：添加前:生命值={使用前生命值}, 增加后:生命值={增加后生命值}")
        else:
            # 检查物品是否有生命值或额外生命值属性
            生命值恢复 = 物品_info.get("生命值", 0)
            额外生命值恢复 = 物品_info.get("额外生命值", 0)
            
            if 生命值恢复 > 0 or 额外生命值恢复 > 0:
                # 应用普通生命值恢复
                if 生命值恢复 > 0:
                    使用前生命值 = self.玩家.current_health
                    self.玩家.current_health = min(self.玩家.current_health + 生命值恢复, self.玩家.max_health)
                    增加后生命值 = self.玩家.current_health
                    print(f"使用{物品_info.get('名称', '未知物品')}：添加前:生命值={使用前生命值}, 增加后:生命值={增加后生命值}")
                
                # 应用额外生命值恢复
                if 额外生命值恢复 > 0:
                    使用前额外生命值 = self.玩家.extra_health
                    self.玩家.extra_health += 额外生命值恢复  # 移除最大值限制，允许无限叠加
                    增加后额外生命值 = self.玩家.extra_health
                    
                    # 更新曾经最大额外生命值
                    if self.玩家.extra_health > self.玩家.曾经最大额外生命值:
                        self.玩家.曾经最大额外生命值 = self.玩家.extra_health
                    
                    print(f"使用{物品_info.get('名称', '未知物品')}：添加前:额外生命值={使用前额外生命值}, 增加后:额外生命值={增加后额外生命值}")
    
    def draw(self, 相机_x, 相机_y):
        """绘制游戏画面"""
        # 绘制世界
        self.世界.draw(self.屏幕, 相机_x, 相机_y)
        
        # 绘制掉落物
        self.世界.draw_items(self.屏幕, 相机_x, 相机_y)
        
        # 绘制经验小球
        if hasattr(self.世界, 'exp_orbs'):
            for orb in self.世界.exp_orbs:
                orb.draw(self.屏幕, 相机_x, 相机_y)
        
        # 绘制生物
        self.世界.draw_mobs(self.屏幕, 相机_x, 相机_y)
        
        # 绘制生物攻击距离红线（如果显示攻击距离设置为开启）
        if self.显示攻击距离:
            for mob in self.世界.mobs:
                # 获取生物的屏幕坐标
                screen_x = mob.x - 相机_x + mob.width // 2
                screen_y = mob.y - 相机_y + mob.height // 2
                # 绘制红色攻击距离圆圈
                pygame.draw.circle(self.屏幕, (255, 0, 0), (screen_x, screen_y), mob.attack_range, 2)  # 红色，线宽2
        
        # 绘制生物受伤距离橙线（如果显示受伤距离设置为开启）
        if self.显示受伤距离:
            for mob in self.世界.mobs:
                # 获取生物的屏幕坐标和体积大小
                screen_x = mob.x - 相机_x
                screen_y = mob.y - 相机_y
                # 绘制橙色体积矩形（表示受伤距离）
                mob_rect = pygame.Rect(screen_x, screen_y, mob.width, mob.height)
                pygame.draw.rect(self.屏幕, (255, 165, 0), mob_rect, 2)  # 橙色，线宽2
        
        # 绘制玩家
        self.玩家.draw(self.屏幕, 相机_x, 相机_y)
        
        # 在玩家中心绘制红色半透明扇形，角度150°，跟随鼠标，半径根据武器变化
        import math
        # 获取当前手持工具
        工具实例, 当前工具 = self.获取当前手持工具()
        
        # 检查是否手持远程武器或投掷物，如果是则不绘制扇形
        手持远程武器或投掷物 = False
        if 当前工具:
            武器名称 = 当前工具.get('名称', '')
            武器类型 = 当前工具.get('类型', '')
            
            # 远程武器关键词列表：包括所有远程攻击武器
            远程武器关键词 = ['弓', '弩', '手枪', '步枪', '狙击枪', '喷子', '冲锋枪', '枪', 
                             '火箭筒', '激光炮', '电磁发射器', '法杖', '炮', '加特林', '榴弹炮', '龙息', '机甲', '齐天', '五子棋']
            
            # 投掷物判断：堆叠上限大于1的武器通常是投掷物，或者名称包含投掷物关键词
            堆叠上限 = 当前工具.get('堆叠上限', 1)
            投掷物关键词 = ['投掷', '燃烧瓶', '手榴弹', '炸弹']
            
            # 远程武器判断：名称包含远程关键词，或者类型为远程类型
            是远程武器 = any(关键词 in 武器名称 for 关键词 in 远程武器关键词) or 武器类型 in ['weapon'] and any(关键词 in 武器名称 for 关键词 in ['远程', '发射', '弹'])
            是投掷物 = 堆叠上限 > 1 or any(关键词 in 武器名称 for 关键词 in 投掷物关键词)
            
            手持远程武器或投掷物 = 是远程武器 or 是投掷物
        
        # 如果手持远程武器或投掷物，则不绘制扇形
        if 手持远程武器或投掷物:
            pass  # 不绘制扇形
        # 攻击扇区绘制代码已注释，暂时隐藏
        # else:
        #     # 根据武器类型计算真实攻击范围（与攻击生物方法使用相同逻辑）
        #     攻击范围 = 1.5  # 默认为空手范围
        #     武器名称 = ''  # 初始化武器名称变量，避免未定义错误
        #     
        #     # 正确处理获取当前手持工具的返回值
        #     if 工具实例 and 当前工具:
        #         # 工具实例是物品对象，当前工具是工具信息字典
        #         武器名称 = 当前工具.get('名称', '')
        #         
        #         # 检查是否是火焰三叉戟且有buff
        #         是火焰三叉戟 = '火焰三叉戟' in 武器名称
        #         火焰三叉戟_buff = hasattr(self.玩家, '火焰三叉戟_buff_active') and self.玩家.火焰三叉戟_buff_active
        #         
        #         # 检查是否是闪电三叉戟且有buff
        #         是闪电三叉戟 = '闪电三叉戟' in 武器名称
        #         闪电三叉戟_buff = hasattr(self.玩家, '闪电三叉戟_buff_active') and self.玩家.闪电三叉戟_buff_active
        #         
        #         # 根据武器类型设置攻击范围
        #         # 空手: 1.5*1.5, 拿工具: 使用工具距离属性, 拿近战武器: 使用工具距离属性, 死神的镰刀: 3.5*3.5
        #         # 合并条件判断，让死神的镰刀也使用通用的图片特效
        #         if 工具实例.获取属性('伤害', 0) > 0 or '死神的镰刀' in 武器名称:
        #             攻击范围 = 3.5
        #         # 检查是否为火焰三叉戟且有buff
        #         elif 是火焰三叉戟 and 火焰三叉戟_buff:
        #             # 火焰三叉戟buff激活时，攻击范围提升到6*6
        #             攻击范围 = 6.0
        #         # 检查是否为闪电三叉戟且有buff
        #         elif 是闪电三叉戟 and 闪电三叉戟_buff:
        #             # 闪电三叉戟buff激活时，攻击范围提升到5*5
        #             攻击范围 = 5.0
        #         # 检查是否为近战武器（根据伤害属性判断）
        #         elif hasattr(工具实例, '获取属性') and 工具实例.获取属性('伤害', 0) > 0:
        #             # 从物品属性中获取工具距离
        #             攻击范围 = 工具实例.获取属性('工具距离', 2.5)
        #         # 其他工具
        #         else:
        #             # 从物品属性中获取工具距离
        #             攻击范围 = 工具实例.获取属性('工具距离', 2.0)
        #     
        #     # 使用真实攻击范围作为扇形半径格数
        #     半径格数 = 攻击范围
        #     
        #     # 计算玩家中心屏幕坐标
        #     玩家中心_x = self.玩家.坐标_x - 相机_x + self.玩家.宽 // 2
        #     玩家中心_y = self.玩家.坐标_y - 相机_y + self.玩家.高 // 2
        #     
        #     # 获取鼠标位置
        #     鼠标_x, 鼠标_y = pygame.mouse.get_pos()
        #     
        #     # 计算玩家中心到鼠标的角度（弧度）
        #     方向角度 = math.atan2(鼠标_y - 玩家中心_y, 鼠标_x - 玩家中心_x)
        #     
        #     # 根据武器类型设置扇形角度
        #     # 只有闪电三叉戟、火焰三叉戟和骨矛使用30°角度，其他武器使用150°
        #     if 武器名称 in ['火焰三叉戟', '闪电三叉戟', '骨矛']:
        #         # 这三种武器使用30°角度（15°向左 + 15°向右）
        #         角度偏移 = math.radians(15)
        #     else:
        #         # 其他武器使用150°角度（75°向左 + 75°向右）
        #         角度偏移 = math.radians(75)
        #     
        #     # 计算扇形的起始和结束角度
        #     起始角度 = 方向角度 - 角度偏移
        #     结束角度 = 方向角度 + 角度偏移
        #     
        #     # 计算半径（格数 * 方块大小）
        #     半径 = 半径格数 * 32  # 32是方块大小
        #     
        #     # 创建半透明表面
        #     扇形表面 = pygame.Surface((半径 * 2, 半径 * 2), pygame.SRCALPHA)
        #     
        #     # 计算扇形的顶点坐标
        #     扇形顶点 = [(半径, 半径)]  # 中心顶点
        #     
        #     # 添加扇形边缘的顶点（使用50个点来绘制平滑的扇形）
        #     点数 = 50
        #     for i in range(点数 + 1):
        #         # 计算当前角度
        #         当前角度 = 起始角度 + (结束角度 - 起始角度) * i / 点数
        #         # 计算顶点坐标
        #         x = 半径 + math.cos(当前角度) * 半径
        #         y = 半径 + math.sin(当前角度) * 半径
        #         扇形顶点.append((x, y))
        #     
        #     # 绘制红色半透明扇形（RGB: 255, 0, 0; Alpha: 100）
        #     pygame.draw.polygon(扇形表面, (255, 0, 0, 100), 扇形顶点)
        #     
        #     # 在玩家中心绘制扇形
        #     self.屏幕.blit(扇形表面, 
        #                   (玩家中心_x - 半径, 玩家中心_y - 半径))
        
        # 绘制粒子效果
        self.世界.draw_particles(self.屏幕, 相机_x, 相机_y)
        
        # 绘制箭矢
        for arrow in self.arrows:
            arrow.draw(self.屏幕, 相机_x, 相机_y)
        
        # 绘制激光效果
        if hasattr(self, 'laser_effects'):
            for laser in self.laser_effects:
                laser.draw(self.屏幕, 相机_x, 相机_y)
        
        # 绘制龙息激光效果
        if hasattr(self, '龙息激光效果列表'):
            for laser in self.龙息激光效果列表:
                laser.draw(self.屏幕, 相机_x, 相机_y)
        
        # 绘制爆炸效果
        if hasattr(self, 'explosion_effects'):
            for explosion in self.explosion_effects:
                explosion.draw(self.屏幕, 相机_x, 相机_y)
        
        # 绘制弧线劈砍效果
        if hasattr(self, 'slash_effects'):
            for slash in self.slash_effects:
                slash.draw(self.屏幕, 相机_x, 相机_y)
        
        # 绘制武器技能相关元素
        武器技能管理器实例.draw(self.屏幕, 相机_x, 相机_y)
        
        # 绘制伤害数字
        for text in self.damage_texts:
            text.draw(self.屏幕, 相机_x, 相机_y)
        
        # 绘制漂浮文字
        self._draw_notifications(self.屏幕)
        
        # 绘制挖掘进度条
        self.绘制挖掘进度条(相机_x, 相机_y)
        
        # 绘制BOSS血量条
        self.绘制BOSS血量条()
        
        # 显示调试信息
        if self.显示调试:
            self.draw_debug_info(相机_x, 相机_y)
        
        # 绘制狙击枪红线辅助参考
        # 获取当前手持工具
        工具实例, 当前工具 = self.获取当前手持工具()
        if 当前工具:
            武器名称 = 当前工具.get('名称', '')
            是否狙击枪 = '狙击枪' in 武器名称
            if 是否狙击枪:
                # 检查是否在可射击状态（不在冷却中）
                当前时间 = time.time()
                冷却时间 = 2.0  # 狙击枪冷却时间
                if 当前时间 - self.弓箭上次射击时间 >= 冷却时间:
                    # 获取玩家中心位置（屏幕坐标）
                    玩家屏幕_x = self.玩家.坐标_x - 相机_x + self.玩家.宽 // 2
                    玩家屏幕_y = self.玩家.坐标_y - 相机_y + self.玩家.高 // 2
                    
                    # 获取鼠标位置
                    鼠标_x, 鼠标_y = pygame.mouse.get_pos()
                    
                    # 计算方向向量
                    dx = 鼠标_x - 玩家屏幕_x
                    dy = 鼠标_y - 玩家屏幕_y
                    
                    # 计算向量长度
                    length = math.sqrt(dx*dx + dy*dy)
                    
                    # 归一化方向向量
                    if length > 0:
                        dir_x = dx / length
                        dir_y = dy / length
                    else:
                        dir_x = 0
                        dir_y = 1
                    
                    # 计算延伸100像素后的终点位置
                    延伸距离 = 300
                    
                    终点_x = 鼠标_x + dir_x * 延伸距离
                    终点_y = 鼠标_y + dir_y * 延伸距离
                    
                    # 绘制3像素宽的红线，从玩家中心到延伸后的终点
                    pygame.draw.line(self.屏幕, (255, 0, 0), (玩家屏幕_x, 玩家屏幕_y), (终点_x, 终点_y), 3)
        
        
        # 绘制左上角生命值和饥饿值进度条
        # 检查是否显示UI - 如果合成页面打开则隐藏
        if not (hasattr(self, 'crafting_system') and self.crafting_system.is_open):
            self.绘制状态进度条()
            
            # 在屏幕底部中心绘制长方形和正方形
            self.绘制底部图形()
        
        # 如果显示帮助页面，则绘制帮助内容
        if self.show_controls:
            self.draw_help_page()
        
        # 如果显示ESC菜单，则绘制菜单
        if self.show_esc_menu and self.esc_page:
            self.esc_page.draw(self.屏幕)
        
        
        # 箱子页面的绘制由页面管理器统一处理，这里不需要单独处理
        
        # 如果合成页面打开，则绘制合成界面
        if hasattr(self, 'crafting_system') and self.crafting_system.is_open:
            self.crafting_system.draw(self.屏幕)
        
        # 如果背包打开，则绘制背包界面
        if hasattr(self, '背包管理器') and self.背包管理器.是否打开:
            self.背包管理器.绘制(self.屏幕)
        
        # 绘制返回主程序按钮（设置图标）
        # 动态调整按钮位置为靠右
        screen_width, screen_height = self.屏幕.get_size()
        self.return_to_main_button.x = screen_width - 30  # 距离右侧10像素
        self.return_to_main_button.y = 10  # 距离顶部10像素
        
        if self.return_button_image:
            # 使用图片绘制按钮，缩放到20*20
            scaled_image = pygame.transform.scale(self.return_button_image, (20, 20))
            self.屏幕.blit(scaled_image, self.return_to_main_button)
        else:
            # 如果图片加载失败，使用默认矩形绘制
            pygame.draw.rect(self.屏幕, (100, 100, 100), self.return_to_main_button)
            pygame.draw.rect(self.屏幕, (200, 200, 200), self.return_to_main_button, 1)
        
        # 绘制关机按钮，位置在设置图标下方
        self.关机按钮.x = screen_width - 30  # 距离右侧10像素，与设置图标对齐
        self.关机按钮.y = self.return_to_main_button.y + self.return_to_main_button.height + 10  # 设置图标下方10像素
        
        if self.关机按钮_image:
            # 使用图片绘制关机按钮，缩放到20*20
            scaled_shutdown_image = pygame.transform.scale(self.关机按钮_image, (20, 20))
            self.屏幕.blit(scaled_shutdown_image, self.关机按钮)
        else:
            # 如果图片加载失败，使用默认矩形绘制
            pygame.draw.rect(self.屏幕, (150, 50, 50), self.关机按钮)
            pygame.draw.rect(self.屏幕, (200, 200, 200), self.关机按钮, 1)
        
        # 绘制直接返回主程序按钮
        if self.显示直接返回主程序按钮:
            # 添加背景遮罩
            背景_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            pygame.draw.rect(背景_surface, (0, 0, 0, 120), (0, 0, screen_width, screen_height))
            self.屏幕.blit(背景_surface, (0, 0))
            
            # 添加标题文字：是否返回主菜单
            标题字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 24, bold=True)
            标题文字 = 标题字体.render("是否返回主菜单", True, (255, 255, 255))
            标题_rect = 标题文字.get_rect(center=(screen_width // 2, screen_height // 2 - 60))
            self.屏幕.blit(标题文字, 标题_rect)
            
            # 将按钮放置在屏幕中间，垂直排列
            start_x = (screen_width - self.直接返回主程序按钮.width) // 2  # 水平居中
            # 返回主菜单按钮位置
            self.直接返回主程序按钮.x = start_x
            self.直接返回主程序按钮.y = screen_height // 2 - 30  # 屏幕垂直居中偏上30像素
            
            # 设置取消按钮位置，垂直排列在下方，间距20像素
            self.隐藏按钮.x = start_x  # 水平居中，与返回主菜单按钮对齐
            self.隐藏按钮.y = screen_height // 2 + 30  # 屏幕垂直居中偏下30像素，与上方按钮间距60像素
            
            # 获取鼠标位置
            鼠标_pos = pygame.mouse.get_pos()
            
            # 绘制返回主程序按钮
            if self.直接返回主程序按钮.collidepoint(鼠标_pos):
                按钮_color = (50, 120, 170)
            else:
                按钮_color = (40, 100, 150)
            pygame.draw.rect(self.屏幕, 按钮_color, self.直接返回主程序按钮, border_radius=6)
            pygame.draw.rect(self.屏幕, (60, 140, 190), self.直接返回主程序按钮, 2, border_radius=6)
            
            # 绘制取消按钮
            if self.隐藏按钮.collidepoint(鼠标_pos):
                按钮_color = (50, 170, 50)
            else:
                按钮_color = (40, 150, 40)
            pygame.draw.rect(self.屏幕, 按钮_color, self.隐藏按钮, border_radius=6)
            pygame.draw.rect(self.屏幕, (60, 190, 60), self.隐藏按钮, 2, border_radius=6)
            
            # 绘制按钮文字
            按钮字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 18, bold=True)
            
            # 返回主菜单按钮文字
            按钮文字 = 按钮字体.render(self.直接返回主程序文字, True, (255, 255, 255))
            文字_rect = 按钮文字.get_rect(center=self.直接返回主程序按钮.center)
            self.屏幕.blit(按钮文字, 文字_rect)
            
            # 取消按钮文字
            按钮文字 = 按钮字体.render(self.隐藏按钮文字, True, (255, 255, 255))
            文字_rect = 按钮文字.get_rect(center=self.隐藏按钮.center)
            self.屏幕.blit(按钮文字, 文字_rect)
        
        # 如果死亡页面已打开，则绘制死亡页面
        if hasattr(self, 'death_page_open') and self.death_page_open and hasattr(self, 'death_page'):
            self.death_page.draw(self.屏幕)
        
        # 绘制退出提示窗口
        if self.显示退出提示:
            self._绘制退出提示窗口()
    
    def calculate_total_content_height(self, 内容):
        """计算帮助页面内容的总高度"""
        total_height = 0
        for section in 内容:
            # 章节标题高度
            total_height += 40
            # 章节内容高度
            for item in section[1]:
                total_height += 30
        return total_height
    
    def draw_scrollbar(self, 容器高度, 内容总高度):
        """绘制滚动条"""
        if 内容总高度 <= 容器高度:
            return  # 内容未超出容器，不需要滚动条
        
        # 计算滚动条参数
        滚动条_width = 10
        滚动条_height = max(20, int((容器高度 / 内容总高度) * 容器高度))
        滚动条_x = self.屏幕.get_width() - 30
        滚动条_y = 60 + int((self.help_scroll_offset / (内容总高度 - 容器高度)) * (容器高度 - 滚动条_height))
        
        # 绘制滚动条背景
        pygame.draw.rect(self.屏幕, (50, 50, 50), (滚动条_x, 60, 滚动条_width, 容器高度))
        # 绘制滚动条
        pygame.draw.rect(self.屏幕, (150, 150, 150), (滚动条_x, 滚动条_y, 滚动条_width, 滚动条_height))
    
    def _绘制退出提示窗口(self):
        """绘制退出提示窗口"""
        # 获取屏幕尺寸
        屏幕宽度, 屏幕高度 = self.屏幕.get_size()
        
        # 计算提示窗口位置（居中）
        窗口_x = (屏幕宽度 - self.提示窗口宽度) // 2
        窗口_y = (屏幕高度 - self.提示窗口高度) // 2
        
        # 绘制半透明背景遮罩，添加模糊效果
        背景表面 = pygame.Surface((屏幕宽度, 屏幕高度), pygame.SRCALPHA)
        pygame.draw.rect(背景表面, (0, 0, 0, 180), (0, 0, 屏幕宽度, 屏幕高度))
        self.屏幕.blit(背景表面, (0, 0))
        
        # 绘制窗口阴影效果
        阴影宽度 = 10
        阴影表面 = pygame.Surface((self.提示窗口宽度 + 2*阴影宽度, self.提示窗口高度 + 2*阴影宽度), pygame.SRCALPHA)
        pygame.draw.rect(阴影表面, (0, 0, 0, 120), (0, 0, self.提示窗口宽度 + 2*阴影宽度, self.提示窗口高度 + 2*阴影宽度), border_radius=15)
        self.屏幕.blit(阴影表面, (窗口_x - 阴影宽度, 窗口_y - 阴影宽度))
        
        # 绘制提示窗口背景，使用圆角和渐变效果
        窗口表面 = pygame.Surface((self.提示窗口宽度, self.提示窗口高度), pygame.SRCALPHA)
        # 渐变背景 - 使用更明亮的颜色，不那么灰
        for y in range(self.提示窗口高度):
            # 从上到下颜色渐变，使用更明亮的蓝灰色调
            alpha = 220 + int(y * 35 / self.提示窗口高度)
            color = (85, 90, 100)  # 使用更明亮的颜色，减少灰色调
            pygame.draw.line(窗口表面, (*color, alpha), (0, y), (self.提示窗口宽度, y))
        # 圆角矩形
        pygame.draw.rect(窗口表面, (85, 90, 100), (0, 0, self.提示窗口宽度, self.提示窗口高度), border_radius=15)
        # 窗口边框 - 使用更柔和的颜色
        pygame.draw.rect(窗口表面, (105, 110, 120), (0, 0, self.提示窗口宽度, self.提示窗口高度), 2, border_radius=15)
        self.屏幕.blit(窗口表面, (窗口_x, 窗口_y))
        
        # 绘制标题栏
        标题栏高度 = 60
        标题栏_rect = pygame.Rect(窗口_x, 窗口_y, self.提示窗口宽度, 标题栏高度)
        # 使用更明亮的标题栏颜色
        pygame.draw.rect(self.屏幕, (95, 100, 110), 标题栏_rect, border_radius=15, border_bottom_left_radius=0, border_bottom_right_radius=0)
        # 标题栏底部边框
        pygame.draw.line(self.屏幕, (115, 120, 130), (窗口_x, 窗口_y + 标题栏高度), (窗口_x + self.提示窗口宽度, 窗口_y + 标题栏高度), 2)
        
        # 绘制窗口标题，使用更好的位置和颜色
        # 减小标题字体大小，使用原来的字体大小
        标题表面 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 28, bold=True).render(self.退出提示标题, True, (255, 255, 255))
        标题_rect = 标题表面.get_rect(center=(窗口_x + self.提示窗口宽度 // 2, 窗口_y + 标题栏高度 // 2))
        # 添加标题文字阴影 - 使用更柔和的阴影
        阴影表面 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 28, bold=True).render(self.退出提示标题, True, (0, 0, 0, 120))
        self.屏幕.blit(阴影表面, (标题_rect.x + 3, 标题_rect.y + 3))
        self.屏幕.blit(标题表面, 标题_rect)
        
        # 绘制右上角关闭按钮（x）
        关闭按钮_size = 32
        self.关闭按钮_rect = pygame.Rect(窗口_x + self.提示窗口宽度 - 45, 窗口_y + 14, 关闭按钮_size, 关闭按钮_size)
        鼠标_pos = pygame.mouse.get_pos()
        关闭按钮_hover = self.关闭按钮_rect.collidepoint(鼠标_pos)
        
        # 关闭按钮样式 - 使用更美观的设计
        if 关闭按钮_hover:
            # 悬停状态：使用红色渐变
            pygame.draw.circle(self.屏幕, (230, 80, 80), self.关闭按钮_rect.center, 18)
        else:
            # 正常状态：使用更柔和的颜色
            pygame.draw.circle(self.屏幕, (90, 95, 105), self.关闭按钮_rect.center, 18)
        
        # 绘制x符号 - 使用更粗的字体和更好的样式
        关闭_x = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 34, bold=True).render("×", True, (255, 255, 255))
        关闭_x_rect = 关闭_x.get_rect(center=self.关闭按钮_rect.center)
        self.屏幕.blit(关闭_x, 关闭_x_rect)
        
        # 添加第一行：左侧图片和右侧文字
        第一行_y = 窗口_y + 标题栏高度 + 20  # 标题栏下方20像素，增加间距
        
        # 计算第一行内容的居中位置
        第一行总宽度 = 160 + 30 + 200  # 图片宽度 + 中间间距 + 文字宽度
        第一行_start_x = 窗口_x + (self.提示窗口宽度 - 第一行总宽度) // 2
        
        # 左侧4:3比例图片 - 使用更好的边框设计
        图片宽度 = 160
        图片高度 = 120  # 4:3比例
        图片_x = 第一行_start_x
        图片_y = 第一行_y
        
        # 绘制图片背景 - 使用更柔和的颜色
        pygame.draw.rect(self.屏幕, (245, 245, 245), (图片_x, 图片_y, 图片宽度, 图片高度), border_radius=12)
        # 绘制图片边框 - 使用更细的边框和更好的颜色
        pygame.draw.rect(self.屏幕, (120, 125, 135), (图片_x, 图片_y, 图片宽度, 图片高度), 2, border_radius=12)
        
        # 右侧文字：存档名称 - 使用合适的字体大小
        存档名称文字 = self.提示窗口字体.render("存档名称", True, (230, 230, 230))
        # 文字与图片顶部对齐
        存档名称_y = 第一行_y + 20  # 图片上方20像素间距，让文字居中对齐
        存档名称_rect = 存档名称文字.get_rect(left=第一行_start_x + 160 + 30, y=存档名称_y)  # 增加中间间距到30像素
        self.屏幕.blit(存档名称文字, 存档名称_rect)
        
        # 添加第二行：可交互控件
        第二行_y = 第一行_y + 图片高度 + 30  # 第一行图片下方30像素，增加间距
        元素_height = 40
        间隔 = 15
        
        # 计算第二行总宽度和居中位置
        第二行总宽度 = 110 + 间隔 + 110 + 间隔 + 240
        第二行_start_x = 窗口_x + (self.提示窗口宽度 - 第二行总宽度) // 2
        
        # 1. 第一个控件：音效开关
        音效开关_x = 第二行_start_x
        音效开关_y = 第二行_y
        音效开关_width = 110
        
        # 绘制音效开关背景 - 使用更明亮的颜色
        pygame.draw.rect(self.屏幕, (100, 105, 115), (音效开关_x, 音效开关_y, 音效开关_width, 元素_height), border_radius=15)
        pygame.draw.rect(self.屏幕, (120, 125, 135), (音效开关_x, 音效开关_y, 音效开关_width, 元素_height), 2, border_radius=15)
        
        # 绘制音效文字 - 减小文字大小50%
        小字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 14)
        音效文字 = 小字体.render("音效", True, (230, 230, 230))
        音效文字_rect = 音效文字.get_rect(left=音效开关_x + 15, centery=音效开关_y + 元素_height // 2)
        self.屏幕.blit(音效文字, 音效文字_rect)
        
        # 绘制开关圆圈 - 优化设计
        开关_radius = 12
        开关_x = 音效开关_x + 音效开关_width - 30
        开关_y = 音效开关_y + 元素_height // 2
        
        # 绘制开关轨道 - 使用更好的颜色
        轨道_rect = pygame.Rect(开关_x - 25, 开关_y - 15, 40, 30)
        if self.音效开关:
            # 开启状态：轨道使用绿色
            pygame.draw.rect(self.屏幕, (60, 180, 80), 轨道_rect, border_radius=15)
            # 圆圈位置
            开关_center = (开关_x + 5, 开关_y)
        else:
            # 关闭状态：轨道使用灰色
            pygame.draw.rect(self.屏幕, (120, 125, 135), 轨道_rect, border_radius=15)
            # 圆圈位置
            开关_center = (开关_x - 15, 开关_y)
        
        # 绘制开关圆圈 - 使用更美观的设计
        pygame.draw.circle(self.屏幕, (255, 255, 255), 开关_center, 开关_radius)
        # 添加内圈效果
        pygame.draw.circle(self.屏幕, (180, 185, 195), 开关_center, 5)
        
        # 保存音效开关矩形，用于交互
        self.音效开关_rect = pygame.Rect(音效开关_x, 音效开关_y, 音效开关_width, 元素_height)
        
        # 2. 第二个控件：音乐开关
        音乐开关_x = 第二行_start_x + 110 + 间隔
        音乐开关_y = 第二行_y
        音乐开关_width = 110
        
        # 绘制音乐开关背景 - 使用更明亮的颜色
        pygame.draw.rect(self.屏幕, (100, 105, 115), (音乐开关_x, 音乐开关_y, 音乐开关_width, 元素_height), border_radius=15)
        pygame.draw.rect(self.屏幕, (120, 125, 135), (音乐开关_x, 音乐开关_y, 音乐开关_width, 元素_height), 2, border_radius=15)
        
        # 绘制音乐文字 - 减小文字大小50%
        音乐文字 = 小字体.render("音乐", True, (230, 230, 230))
        音乐文字_rect = 音乐文字.get_rect(left=音乐开关_x + 15, centery=音乐开关_y + 元素_height // 2)
        self.屏幕.blit(音乐文字, 音乐文字_rect)
        
        # 绘制音乐开关圆圈 - 优化设计
        音乐开关_radius = 12
        音乐开关_x_pos = 音乐开关_x + 音乐开关_width - 30
        音乐开关_y_pos = 音乐开关_y + 元素_height // 2
        
        # 绘制开关轨道 - 使用更好的颜色
        音乐轨道_rect = pygame.Rect(音乐开关_x_pos - 25, 音乐开关_y_pos - 15, 40, 30)
        if self.音乐开关:
            # 开启状态：轨道使用蓝色
            pygame.draw.rect(self.屏幕, (60, 130, 200), 音乐轨道_rect, border_radius=15)
            # 圆圈位置
            音乐开关_center = (音乐开关_x_pos + 5, 音乐开关_y_pos)
        else:
            # 关闭状态：轨道使用灰色
            pygame.draw.rect(self.屏幕, (120, 125, 135), 音乐轨道_rect, border_radius=15)
            # 圆圈位置
            音乐开关_center = (音乐开关_x_pos - 15, 音乐开关_y_pos)
        
        # 绘制开关圆圈 - 使用更美观的设计
        pygame.draw.circle(self.屏幕, (255, 255, 255), 音乐开关_center, 音乐开关_radius)
        # 添加内圈效果
        pygame.draw.circle(self.屏幕, (180, 185, 195), 音乐开关_center, 5)
        
        # 保存音乐开关矩形，用于交互
        self.音乐开关_rect = pygame.Rect(音乐开关_x, 音乐开关_y, 音乐开关_width, 元素_height)
        
        # 3. 第三个控件：音量进度条
        进度条_x = 第二行_start_x + 110 + 间隔 + 110 + 间隔
        进度条_y = 第二行_y
        进度条_width = 240
        进度条_height = 25
        
        # 绘制进度条背景 - 使用更明亮的颜色
        pygame.draw.rect(self.屏幕, (100, 105, 115), (进度条_x, 进度条_y, 进度条_width, 元素_height), border_radius=15)
        pygame.draw.rect(self.屏幕, (120, 125, 135), (进度条_x, 进度条_y, 进度条_width, 元素_height), 2, border_radius=15)
        
        # 绘制音量文字 - 减小文字大小50%
        音量文字 = 小字体.render(f"音量: {self.音量值}%", True, (230, 230, 230))
        音量文字_rect = 音量文字.get_rect(left=进度条_x + 15, centery=进度条_y + 元素_height // 2)
        self.屏幕.blit(音量文字, 音量文字_rect)
        
        # 绘制进度条轨道
        轨道_x = 进度条_x + 110
        轨道_y = 进度条_y + (元素_height - 进度条_height) // 2
        轨道_width = 120
        # 使用更美观的轨道颜色
        pygame.draw.rect(self.屏幕, (120, 125, 135), (轨道_x, 轨道_y, 轨道_width, 进度条_height), border_radius=12)
        
        # 绘制进度条填充 - 使用更美观的颜色
        填充_width = int((self.音量值 / 100) * 轨道_width)
        pygame.draw.rect(self.屏幕, (60, 160, 220), (轨道_x, 轨道_y, 填充_width, 进度条_height), border_radius=12)
        
        # 绘制进度条滑块 - 优化设计
        滑块_x = 轨道_x + 填充_width - 13
        滑块_y = 轨道_y + 进度条_height // 2
        # 主滑块
        pygame.draw.circle(self.屏幕, (255, 255, 255), (滑块_x, 滑块_y), 13)
        # 滑块内圈
        pygame.draw.circle(self.屏幕, (180, 185, 195), (滑块_x, 滑块_y), 6)
        
        # 保存进度条矩形，用于交互
        self.进度条_rect = pygame.Rect(轨道_x, 轨道_y, 轨道_width, 进度条_height)
        
        # 添加第三行：特效选项
        第三行_y = 第二行_y + 元素_height + 20  # 第二行控件下方20像素
        特效元素_height = 35
        特效间隔 = 10
        
        # 计算第三行总宽度和居中位置，向左移动30像素
        特效总宽度 = 200  # 特效文字 + 三个选项的总宽度
        第三行_start_x = 窗口_x + (self.提示窗口宽度 - 特效总宽度) // 2 - 30  # 向左移动30像素
        
        # 特效文字标签
        特效文字 = 小字体.render("特效：", True, (230, 230, 230))
        特效文字_rect = 特效文字.get_rect(left=第三行_start_x, centery=第三行_y + 特效元素_height // 2)
        self.屏幕.blit(特效文字, 特效文字_rect)
        
        # 特效选项按钮
        特效选项 = ["最佳", "标准", "关闭"]
        选项_width = 60
        选项_x = 第三行_start_x + 50  # 特效文字右侧50像素
        
        # 保存特效选项矩形，用于交互
        self.特效选项_rects = []
        
        for i, 选项 in enumerate(特效选项):
            # 计算选项位置
            当前选项_x = 选项_x + i * (选项_width + 特效间隔)
            选项_rect = pygame.Rect(当前选项_x, 第三行_y, 选项_width, 特效元素_height)
            self.特效选项_rects.append(选项_rect)
            
            # 根据是否选中绘制不同的背景色
            if self.特效渲染设置 == 选项:
                # 选中状态：使用高亮颜色
                pygame.draw.rect(self.屏幕, (60, 130, 200), 选项_rect, border_radius=10)
            else:
                # 未选中状态：使用普通背景色
                pygame.draw.rect(self.屏幕, (100, 105, 115), 选项_rect, border_radius=10)
            
            # 绘制选项边框
            pygame.draw.rect(self.屏幕, (120, 125, 135), 选项_rect, 2, border_radius=10)
            
            # 绘制选项文字
            选项文字 = 小字体.render(选项, True, (230, 230, 230))
            选项文字_rect = 选项文字.get_rect(center=选项_rect.center)
            self.屏幕.blit(选项文字, 选项文字_rect)
        
        # 添加第四行：显示攻击距离和显示受伤距离按钮
        第四行_y = 第三行_y + 特效元素_height + 20  # 特效选项下方20像素
        新按钮_width = 150
        新按钮_height = 35
        新按钮_spacing = 50
        
        # 计算按钮总宽度和居中位置
        新按钮_total_width = 新按钮_width * 2 + 新按钮_spacing
        第四行_start_x = 窗口_x + (self.提示窗口宽度 - 新按钮_total_width) // 2
        
        # 绘制显示攻击距离按钮
        显示攻击距离按钮_rect = pygame.Rect(第四行_start_x, 第四行_y, 新按钮_width, 新按钮_height)
        # 根据状态设置按钮颜色
        显示攻击距离按钮_color = (60, 160, 220) if self.显示攻击距离 else (100, 105, 115)  # 开启时显示蓝色，关闭时显示灰色
        pygame.draw.rect(self.屏幕, 显示攻击距离按钮_color, 显示攻击距离按钮_rect, border_radius=10)
        pygame.draw.rect(self.屏幕, (120, 125, 135), 显示攻击距离按钮_rect, 2, border_radius=10)
        显示攻击距离文本 = 小字体.render("显示攻击距离", True, (230, 230, 230))
        显示攻击距离文本_rect = 显示攻击距离文本.get_rect(center=显示攻击距离按钮_rect.center)
        self.屏幕.blit(显示攻击距离文本, 显示攻击距离文本_rect)
        # 保存按钮引用，用于交互
        self.显示攻击距离按钮_rect = 显示攻击距离按钮_rect
        
        # 绘制显示受伤距离按钮
        显示受伤距离按钮_rect = pygame.Rect(第四行_start_x + 新按钮_width + 新按钮_spacing, 第四行_y, 新按钮_width, 新按钮_height)
        # 根据状态设置按钮颜色
        显示受伤距离按钮_color = (60, 160, 220) if self.显示受伤距离 else (100, 105, 115)  # 开启时显示蓝色，关闭时显示灰色
        pygame.draw.rect(self.屏幕, 显示受伤距离按钮_color, 显示受伤距离按钮_rect, border_radius=10)
        pygame.draw.rect(self.屏幕, (120, 125, 135), 显示受伤距离按钮_rect, 2, border_radius=10)
        显示受伤距离文本 = 小字体.render("显示受伤距离", True, (230, 230, 230))
        显示受伤距离文本_rect = 显示受伤距离文本.get_rect(center=显示受伤距离按钮_rect.center)
        self.屏幕.blit(显示受伤距离文本, 显示受伤距离文本_rect)
        # 保存按钮引用，用于交互
        self.显示受伤距离按钮_rect = 显示受伤距离按钮_rect
        
        # 计算按钮位置，优化布局
        按钮_y = 窗口_y + self.提示窗口高度 - 70  # 距离窗口底部70像素，向下移动30像素
        按钮_width = 140
        按钮_height = 50
        按钮间距 = 20
        
        # 更新按钮尺寸和位置 - 移动到存档名称文字下面
        # 修改按钮大小为宽90，高38
        保存世界按钮_width = 90
        保存世界按钮_height = 38
        self.保存世界按钮_rect = pygame.Rect(0, 0, 保存世界按钮_width, 保存世界按钮_height)
        
        # 保存世界按钮位置：存档名称文字下方
        self.保存世界按钮_rect.x = 第一行_start_x + 160 + 30  # 与存档名称文字左对齐
        self.保存世界按钮_rect.y = 存档名称_y + 存档名称文字.get_height() + 25  # 存档名称文字下方25像素（向下移动15像素）
        
        # 绘制保存世界按钮，添加悬停和点击效果，更改色调
        保存世界按钮_color = (60, 160, 220)  # 修改色调为明亮的蓝色
        保存世界按钮_hover = (80, 180, 240)  # 悬停色调
        保存世界按钮_click = (40, 140, 200)  # 点击色调
        保存世界_button_color = 保存世界按钮_color
        
        if self.保存世界按钮_rect.collidepoint(鼠标_pos):
            保存世界_button_color = 保存世界按钮_hover
            # 检查是否按下
            if pygame.mouse.get_pressed()[0]:
                保存世界_button_color = 保存世界按钮_click
        
        pygame.draw.rect(self.屏幕, 保存世界_button_color, self.保存世界按钮_rect, border_radius=8)  # 恢复圆角大小
        pygame.draw.rect(self.屏幕, (60, 140, 190), self.保存世界按钮_rect, 2, border_radius=8)  # 恢复边框颜色
        
        # 绘制按钮文字，因为按钮尺寸足够大
        # 文字大小减少40%（原28像素，减少后约17像素）
        小字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 17)
        保存世界文本 = 小字体.render("保存世界", True, (255, 255, 255))
        保存世界文本_rect = 保存世界文本.get_rect(center=self.保存世界按钮_rect.center)
        self.屏幕.blit(保存世界文本, 保存世界文本_rect)
    
    def draw_help_page(self):
        """绘制帮助页面内容"""
        # 创建半透明背景
        半透明背景 = pygame.Surface((self.屏幕.get_width(), self.屏幕.get_height()), pygame.SRCALPHA)
        半透明背景.fill((0, 0, 0, 200))  # 半透明黑色
        self.屏幕.blit(半透明背景, (0, 0))
        
        # 创建字体
        try:
            标题字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 28, bold=True)
            章节字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 24, bold=True)
            内容字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 18)
            提示字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 16)
        except:
            标题字体 = pygame.font.Font(None, 28)
            章节字体 = pygame.font.Font(None, 24)
            内容字体 = pygame.font.Font(None, 18)
            提示字体 = pygame.font.Font(None, 16)
        
        # 帮助页面标题
        标题 = 标题字体.render("游戏帮助说明", True, (255, 255, 255))
        self.屏幕.blit(标题, (self.屏幕.get_width() // 2 - 标题.get_width() // 2, 20))
        
        # 从帮助管理器获取帮助内容
        帮助内容 = help_manager.get_help_content()
        
        # 计算内容区域
        容器宽度 = self.屏幕.get_width() - 60
        容器高度 = self.屏幕.get_height() - 120
        内容_x = 30
        内容_y = 60
        
        # 计算总内容高度并设置最大滚动偏移
        内容总高度 = self.calculate_total_content_height(帮助内容)
        self.help_max_scroll_offset = max(0, 内容总高度 - 容器高度)
        
        # 绘制帮助内容
        current_y = 内容_y - self.help_scroll_offset
        
        for section in 帮助内容:
            章节标题, 章节内容 = section
            
            # 绘制章节标题（如果在可见区域内）
            if 0 <= current_y < 内容_y + 容器高度:
                标题颜色 = (255, 215, 0)  # 金色
                章节文本 = 章节字体.render(章节标题, True, 标题颜色)
                self.屏幕.blit(章节文本, (内容_x, current_y))
            
            current_y += 40  # 标题高度
            
            # 绘制章节内容（如果在可见区域内）
            for item in 章节内容:
                if 0 <= current_y < 内容_y + 容器高度:
                    内容文本 = 内容字体.render(item, True, (255, 255, 255))
                    self.屏幕.blit(内容文本, (内容_x + 20, current_y))
                current_y += 30  # 每行内容高度
        
        # 绘制滚动条
        self.draw_scrollbar(容器高度, 内容总高度)
        
        # 底部提示
        底部提示 = 提示字体.render("按F1或ESC关闭指南", True, (255, 255, 255))
        self.屏幕.blit(底部提示, (self.屏幕.get_width() // 2 - 底部提示.get_width() // 2, self.屏幕.get_height() - 40))
        
        # 滚动提示
        滚动提示 = 提示字体.render("使用鼠标滚轮上下滚动", True, (200, 200, 200))
        self.屏幕.blit(滚动提示, (self.屏幕.get_width() // 2 - 滚动提示.get_width() // 2, self.屏幕.get_height() - 20))
    
    def 绘制状态进度条(self):
        """在左上角绘制生命值和饥饿值进度条 - UI优化版"""
        # 创建字体对象 - 加粗
        try:
            字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 16, bold=True)
            标签字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 14, bold=True)
        except:
            字体 = pygame.font.Font(None, 16)
            标签字体 = pygame.font.Font(None, 14)
        
        # 进度条配置 - UI优化
        进度条宽度 = 180   # 增加宽度
        进度条高度 = 22   # 增加高度
        进度条间隔 = 8    # 调整间隔
        左侧边距 = 25
        顶部边距 = 25
        圆角半径 = 6       # 添加圆角效果
        边框宽度 = 2       # 边框宽度
        边框颜色 = (70, 70, 70)  # 边框颜色
        
        # 棕色背景色 (RGB: 139, 69, 19) - 略微亮一点
        背景颜色 = (150, 79, 29)
        
        # 定义颜色 - 更鲜艳的颜色
        生命值颜色 = (230, 50, 50)  # 更鲜艳的红色
        额外生命值颜色 = (65, 105, 225)  # 皇家蓝色
        饥饿值颜色 = (255, 215, 0)  # 金色保持不变
        护盾颜色 = (0, 191, 255)  # 深天蓝色
        
        # 从玩家对象获取实际数值
        生命值百分比 = int((self.玩家.current_health / self.玩家.max_health) * 100)
        # 获取护盾值（如果没有则默认为0）
        护盾值 = getattr(self.玩家, 'current_shield', 0)
        最大护盾值 = getattr(self.玩家, 'max_shield', 100)
        护盾百分比 = int((护盾值 / 最大护盾值) * 100) if 最大护盾值 > 0 else 0
        
        # 计算额外生命值百分比，基于曾经最大额外生命值
        # 当额外生命值为0时，重置曾经最大额外生命值
        if self.玩家.extra_health <= 0:
            self.玩家.曾经最大额外生命值 = 0
            额外生命值百分比 = 0
        else:
            # 使用曾经最大额外生命值作为进度条最大值，如果曾经最大额外生命值为0则使用当前额外生命值
            进度条最大值 = max(self.玩家.曾经最大额外生命值, self.玩家.extra_health, 1)  # 确保至少为1，避免除零错误
            额外生命值百分比 = int((self.玩家.extra_health / 进度条最大值) * 100)
        饥饿值百分比 = int((self.玩家.current_hunger / self.玩家.max_hunger) * 100)
        
        # 计算位置
        生命值_y = 顶部边距
        
        # 绘制生命值进度条
        # 进度条背景带圆角
        pygame.draw.rect(self.屏幕, 背景颜色, 
                        (左侧边距, 生命值_y, 进度条宽度, 进度条高度),
                        border_radius=圆角半径)
        # 绘制边框
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (左侧边距, 生命值_y, 进度条宽度, 进度条高度),
                        边框宽度, border_radius=圆角半径)
        # 绘制生命值进度带圆角
        pygame.draw.rect(self.屏幕, 生命值颜色, 
                        (左侧边距 + 边框宽度, 生命值_y + 边框宽度, 
                         (进度条宽度 - 2 * 边框宽度) * 生命值百分比 / 100, 
                         进度条高度 - 2 * 边框宽度),
                        border_radius=圆角半径 - 2)
        
        # 在生命值进度条中心绘制文字
        if self.玩家.extra_health > 0:
            生命值文字 = 字体.render(f"{self.玩家.current_health}+{self.玩家.extra_health}/{self.玩家.max_health}", True, (255, 255, 255))  # 白色文字更醒目，只有有额外生命值时显示+额外生命值
        else:
            生命值文字 = 字体.render(f"{self.玩家.current_health}/{self.玩家.max_health}", True, (255, 255, 255))  # 白色文字更醒目
        文字_x = 左侧边距 + (进度条宽度 - 生命值文字.get_width()) // 2
        文字_y = 生命值_y + (进度条高度 - 生命值文字.get_height()) // 2
        self.屏幕.blit(生命值文字, (文字_x, 文字_y))
        
        # 额外生命值高度（细条）
        额外生命值高度 = 8
        
        # 只有当护盾值大于0时才绘制护盾值进度条
        if 护盾值 > 0:
            护盾_y = 生命值_y + 进度条高度 + 进度条间隔
            # 进度条背景带圆角
            pygame.draw.rect(self.屏幕, 背景颜色, 
                            (左侧边距, 护盾_y, 进度条宽度, 进度条高度),
                            border_radius=圆角半径)
            # 绘制边框
            pygame.draw.rect(self.屏幕, 边框颜色, 
                            (左侧边距, 护盾_y, 进度条宽度, 进度条高度),
                            边框宽度, border_radius=圆角半径)
            # 绘制护盾进度带圆角
            pygame.draw.rect(self.屏幕, 护盾颜色, 
                            (左侧边距 + 边框宽度, 护盾_y + 边框宽度, 
                             (进度条宽度 - 2 * 边框宽度) * 护盾百分比 / 100, 
                             进度条高度 - 2 * 边框宽度),
                            border_radius=圆角半径 - 2)
            
            # 在护盾进度条中心绘制文字
            护盾文字 = 字体.render(f"护盾: {护盾值}/{最大护盾值}", True, (255, 255, 255))  # 白色文字更醒目
            文字_x = 左侧边距 + (进度条宽度 - 护盾文字.get_width()) // 2
            文字_y = 护盾_y + (进度条高度 - 护盾文字.get_height()) // 2
            self.屏幕.blit(护盾文字, (文字_x, 文字_y))
            
            # 计算额外生命值位置：在护盾进度条下方
            额外生命值_y = 护盾_y + 进度条高度 + 3
        else:
            # 没有护盾值，额外生命值直接放在生命值进度条下方
            额外生命值_y = 生命值_y + 进度条高度 + 3
        
        # 只有当有额外生命值时才绘制额外生命值进度条
        if self.玩家.max_extra_health > 0 and self.玩家.extra_health > 0:
            # 绘制额外生命值进度条背景
            pygame.draw.rect(self.屏幕, 背景颜色, 
                            (左侧边距, 额外生命值_y, 进度条宽度, 额外生命值高度),
                            border_radius=额外生命值高度 // 2)
            # 绘制边框
            pygame.draw.rect(self.屏幕, 边框颜色, 
                            (左侧边距, 额外生命值_y, 进度条宽度, 额外生命值高度),
                            边框宽度, border_radius=额外生命值高度 // 2)
            # 绘制额外生命值进度，基于额外生命值实际值和曾经最大额外生命值
            pygame.draw.rect(self.屏幕, 额外生命值颜色, 
                            (左侧边距 + 边框宽度, 额外生命值_y + 边框宽度, 
                             (进度条宽度 - 2 * 边框宽度) * 额外生命值百分比 / 100, 
                             额外生命值高度 - 2 * 边框宽度),
                            border_radius=(额外生命值高度 - 2 * 边框宽度) // 2)
            # 有额外生命值，饥饿值放在额外生命值进度条下方
            饥饿值_y = 额外生命值_y + 额外生命值高度 + 进度条间隔
        else:
            # 没有额外生命值，饥饿值位置取决于是否有护盾
            if 护盾值 > 0:
                # 有护盾时，饥饿值在护盾下方
                饥饿值_y = 护盾_y + 进度条高度 + 进度条间隔
            else:
                # 没有护盾时，饥饿值直接在生命值下方
                饥饿值_y = 生命值_y + 进度条高度 + 进度条间隔
        
        # 绘制饥饿值进度条
        pygame.draw.rect(self.屏幕, 背景颜色, 
                        (左侧边距, 饥饿值_y, 进度条宽度, 进度条高度),
                        border_radius=圆角半径)
        # 绘制边框
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (左侧边距, 饥饿值_y, 进度条宽度, 进度条高度),
                        边框宽度, border_radius=圆角半径)
        # 绘制饥饿值进度带圆角
        pygame.draw.rect(self.屏幕, 饥饿值颜色, 
                        (左侧边距 + 边框宽度, 饥饿值_y + 边框宽度, 
                         (进度条宽度 - 2 * 边框宽度) * 饥饿值百分比 / 100, 
                         进度条高度 - 2 * 边框宽度),
                        border_radius=圆角半径 - 2)
        
        # 在饥饿值进度条中心绘制文字
        饥饿值文字 = 字体.render(f"{self.玩家.current_hunger}/{self.玩家.max_hunger}", True, (255, 255, 255))  # 白色文字更醒目
        文字_x = 左侧边距 + (进度条宽度 - 饥饿值文字.get_width()) // 2
        文字_y = 饥饿值_y + (进度条高度 - 饥饿值文字.get_height()) // 2
        self.屏幕.blit(饥饿值文字, (文字_x, 文字_y))
        
        # 绘制状态指示器 - 在饥饿值下方绘制
        状态指示器_y = 饥饿值_y + 进度条高度 + 进度条间隔
        指示器大小 = 35  # 图标大小
        指示器_x = 左侧边距  # 与进度条左对齐
        指示器间隔 = 30  # 增加状态指示器之间的间隔，避免文字重叠
        
        # 从状态管理器获取状态信息
        from 状态管理 import 状态管理器实例
        是否无敌, 剩余无敌时间, 最大无敌时间 = 状态管理器实例.获取无敌状态()
        是否燃烧, 剩余燃烧时间, 最大燃烧时间 = 状态管理器实例.获取燃烧状态()
        是否饥饿, 剩余饥饿时间, 最大饥饿时间 = 状态管理器实例.获取饥饿状态()
        
        # 当前绘制位置
        当前_x = 指示器_x
        
        # 绘制无敌状态指示器
        if 是否无敌:
            # 金色边框颜色
            金色边框颜色 = (255, 215, 0)
            # 白色背景颜色
            白色背景颜色 = (255, 255, 255)
            # 圆角半径
            圆角半径 = 8  # 更圆润的边框
            
            # 绘制白色背景（带圆角）
            pygame.draw.rect(self.屏幕, 白色背景颜色, 
                            (当前_x, 状态指示器_y, 指示器大小, 指示器大小),
                            border_radius=圆角半径)
            
            # 绘制金色边框（带圆角）
            pygame.draw.rect(self.屏幕, 金色边框颜色, 
                            (当前_x, 状态指示器_y, 指示器大小, 指示器大小),
                            3,  # 金色边框宽度为3
                            border_radius=圆角半径)  # 圆角边框
            
            # 尝试获取无敌图片
            无敌图片 = 图片管理器.获取图片("无敌")
            
            if 无敌图片:
                # 缩放图片到指示器大小（考虑边框宽度）
                图片内部大小 = 指示器大小 - 8  # 减去边框和边距
                缩放后的图片 = pygame.transform.scale(无敌图片, (图片内部大小, 图片内部大小))
                
                # 计算图片位置（居中放置）
                图片_x = 当前_x + (指示器大小 - 图片内部大小) // 2
                图片_y = 状态指示器_y + (指示器大小 - 图片内部大小) // 2
                
                # 绘制无敌图片
                self.屏幕.blit(缩放后的图片, (图片_x, 图片_y))
            
            # 绘制剩余时间文字（外黑里白效果，底部对齐）
            剩余时间 = int(剩余无敌时间)
            时间文字内容 = f"{剩余时间}s"
            
            # 绘制黑色描边
            时间文字 = 字体.render(时间文字内容, True, (0, 0, 0))
            # 减小图标和文字之间的距离（从10改为5）
            时间文字_x = 当前_x + 指示器大小 + 5
            # 调整为底部对齐：文字底部与正方形底部对齐
            时间文字_y = 状态指示器_y + 指示器大小 - 时间文字.get_height()
            
            # 绘制4个方向的黑色描边
            self.屏幕.blit(时间文字, (时间文字_x - 1, 时间文字_y - 1))  # 左上
            self.屏幕.blit(时间文字, (时间文字_x + 1, 时间文字_y - 1))  # 右上
            self.屏幕.blit(时间文字, (时间文字_x - 1, 时间文字_y + 1))  # 左下
            self.屏幕.blit(时间文字, (时间文字_x + 1, 时间文字_y + 1))  # 右下
            
            # 绘制白色文字
            时间文字 = 字体.render(时间文字内容, True, (255, 255, 255))
            self.屏幕.blit(时间文字, (时间文字_x, 时间文字_y))
            
            # 更新当前绘制位置
            当前_x += 指示器大小 + 指示器间隔
        
        # 绘制燃烧状态指示器
        if 是否燃烧:
            # 橙色边框颜色
            橙色边框颜色 = (255, 165, 0)
            # 白色背景颜色
            白色背景颜色 = (255, 255, 255)
            # 圆角半径
            圆角半径 = 8  # 更圆润的边框
            
            # 绘制白色背景（带圆角）
            pygame.draw.rect(self.屏幕, 白色背景颜色, 
                            (当前_x, 状态指示器_y, 指示器大小, 指示器大小),
                            border_radius=圆角半径)
            
            # 绘制橙色边框（带圆角）
            pygame.draw.rect(self.屏幕, 橙色边框颜色, 
                            (当前_x, 状态指示器_y, 指示器大小, 指示器大小),
                            3,  # 橙色边框宽度为3
                            border_radius=圆角半径)  # 圆角边框
            
            # 尝试获取火焰图片
            火焰图片 = 图片管理器.获取图片("火焰")
            
            if 火焰图片:
                # 缩放图片到指示器大小（考虑边框宽度）
                图片内部大小 = 指示器大小 - 8  # 减去边框和边距
                缩放后的图片 = pygame.transform.scale(火焰图片, (图片内部大小, 图片内部大小))
                
                # 计算图片位置（居中放置）
                图片_x = 当前_x + (指示器大小 - 图片内部大小) // 2
                图片_y = 状态指示器_y + (指示器大小 - 图片内部大小) // 2
                
                # 绘制火焰图片
                self.屏幕.blit(缩放后的图片, (图片_x, 图片_y))
            
            # 绘制剩余时间文字（外黑里白效果，底部对齐）
            剩余时间 = int(剩余燃烧时间)
            时间文字内容 = f"{剩余时间}s"
            
            # 绘制黑色描边
            时间文字 = 字体.render(时间文字内容, True, (0, 0, 0))
            # 减小图标和文字之间的距离（从10改为5）
            时间文字_x = 当前_x + 指示器大小 + 5
            # 调整为底部对齐：文字底部与正方形底部对齐
            时间文字_y = 状态指示器_y + 指示器大小 - 时间文字.get_height()
            
            # 绘制4个方向的黑色描边
            self.屏幕.blit(时间文字, (时间文字_x - 1, 时间文字_y - 1))  # 左上
            self.屏幕.blit(时间文字, (时间文字_x + 1, 时间文字_y - 1))  # 右上
            self.屏幕.blit(时间文字, (时间文字_x - 1, 时间文字_y + 1))  # 左下
            self.屏幕.blit(时间文字, (时间文字_x + 1, 时间文字_y + 1))  # 右下
            
            # 绘制白色文字
            时间文字 = 字体.render(时间文字内容, True, (255, 255, 255))
            self.屏幕.blit(时间文字, (时间文字_x, 时间文字_y))
            
            # 更新当前绘制位置
            当前_x += 指示器大小 + 指示器间隔
        
        # 绘制饥饿状态指示器
        if 是否饥饿:
            # 棕色边框颜色
            棕色边框颜色 = (139, 69, 19)  # 棕色
            # 白色背景颜色
            白色背景颜色 = (255, 255, 255)
            # 圆角半径
            圆角半径 = 8  # 更圆润的边框
            
            # 绘制白色背景（带圆角）
            pygame.draw.rect(self.屏幕, 白色背景颜色, 
                            (当前_x, 状态指示器_y, 指示器大小, 指示器大小),
                            border_radius=圆角半径)
            
            # 绘制棕色边框（带圆角）
            pygame.draw.rect(self.屏幕, 棕色边框颜色, 
                            (当前_x, 状态指示器_y, 指示器大小, 指示器大小),
                            3,  # 棕色边框宽度为3
                            border_radius=圆角半径)  # 圆角边框
            
            # 尝试获取饥饿图片
            饥饿图片 = 图片管理器.获取图片("饥饿")
            
            if 饥饿图片:
                # 缩放图片到指示器大小（考虑边框宽度）
                图片内部大小 = 指示器大小 - 8  # 减去边框和边距
                缩放后的图片 = pygame.transform.scale(饥饿图片, (图片内部大小, 图片内部大小))
                
                # 计算图片位置（居中放置）
                图片_x = 当前_x + (指示器大小 - 图片内部大小) // 2
                图片_y = 状态指示器_y + (指示器大小 - 图片内部大小) // 2
                
                # 绘制饥饿图片
                self.屏幕.blit(缩放后的图片, (图片_x, 图片_y))
            
            # 绘制剩余时间文字（外黑里白效果，底部对齐）
            # 饥饿状态显示-1s表示无限时间
            时间文字内容 = f"-1s"
            
            # 绘制黑色描边
            时间文字 = 字体.render(时间文字内容, True, (0, 0, 0))
            # 减小图标和文字之间的距离（从10改为5）
            时间文字_x = 当前_x + 指示器大小 + 5
            # 调整为底部对齐：文字底部与正方形底部对齐
            时间文字_y = 状态指示器_y + 指示器大小 - 时间文字.get_height()
            
            # 绘制4个方向的黑色描边
            self.屏幕.blit(时间文字, (时间文字_x - 1, 时间文字_y - 1))  # 左上
            self.屏幕.blit(时间文字, (时间文字_x + 1, 时间文字_y - 1))  # 右上
            self.屏幕.blit(时间文字, (时间文字_x - 1, 时间文字_y + 1))  # 左下
            self.屏幕.blit(时间文字, (时间文字_x + 1, 时间文字_y + 1))  # 右下
            
            # 绘制白色文字
            时间文字 = 字体.render(时间文字内容, True, (255, 255, 255))
            self.屏幕.blit(时间文字, (时间文字_x, 时间文字_y))
            
            # 更新当前绘制位置
            当前_x += 指示器大小 + 指示器间隔
                        
    def draw_debug_info(self, 相机_x, 相机_y):
        """绘制调试信息"""
        字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 24)
        
        # 位置信息
        位置文本 = 字体.render(
            f"X:{int(self.玩家.坐标_x//方块大小)}   Y:{int(self.玩家.坐标_y//方块大小)}", 
            True, (255, 255, 255)
        )
        
        # 时间信息
        小时 = int(self.世界.时间_of_day // 100)
        分钟 = int((self.世界.时间_of_day % 100) * 0.6)
        时间文本 = 字体.render(
            f"时间:{小时:02d}:{分钟:02d}", 
            True, (255, 255, 255)
        )
        
        # 已删除世界信息、模式信息和控制提示的显示代码
        
        # 绘制位置文本在屏幕左下角
        屏幕高度 = self.屏幕.get_height()
        文本边距 = 10
        self.屏幕.blit(位置文本, (文本边距, 屏幕高度 - 位置文本.get_height() - 文本边距))
        
        # 绘制时间文本在屏幕右上角，与返回主程序按钮保持适当间距
        屏幕宽度 = self.屏幕.get_width()
        # 时间文本显示在返回按钮左侧，间距10像素
        时间文本_x = 屏幕宽度 - self.return_to_main_button.width - 时间文本.get_width() - 20
        时间文本_y = 10
        self.屏幕.blit(时间文本, (时间文本_x, 时间文本_y))
    
    def _加载最大帧数(self, json_module, os_module):
        """从相对路径的设置_数据库.json加载最大帧数设置"""
        default_fps = 240  # 默认帧率设置为240，避免限制GPU加速后的高帧率，保持游戏速度正常
        try:
            # 获取当前脚本所在目录
            script_dir = os_module.path.dirname(os_module.path.abspath(__file__))
            # 获取项目根目录（向上一级）
            project_root = os_module.path.dirname(script_dir)
            # 设置文件的正确路径：存档文件夹中的设置_数据库.json
            settings_path = os_module.path.join(project_root, "存档", "设置_数据库.json")
            
            # 检查文件是否存在
            if os_module.path.exists(settings_path):
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings = json_module.load(f)
                    # 尝试获取最大帧数或帧率选择设置
                    if isinstance(settings, dict):
                        # 优先检查"最大帧数"键
                        if '最大帧数' in settings:
                            target_fps = int(settings['最大帧数'])
                            print(f"已从设置文件加载最大帧数: {target_fps}")
                            return target_fps
                        # 然后检查"帧率选择"键
                        elif '帧率选择' in settings:
                            target_fps = int(settings['帧率选择'])
                            print(f"已从设置文件加载帧率选择: {target_fps}")
                            return target_fps
            
            print(f"未找到设置_数据库.json或帧率设置，使用默认值: {default_fps}")
        except Exception as e:
            print(f"加载设置_数据库.json时出错: {e}，使用默认值: {default_fps}")
        
        return default_fps
    
    def _加载特效渲染设置(self, json_module, os_module):
        """从相对路径的设置_数据库.json加载特效渲染设置"""
        default_effect = "标准"  # 默认标准渲染
        try:
            # 获取当前脚本所在目录
            script_dir = os_module.path.dirname(os_module.path.abspath(__file__))
            # 获取项目根目录（向上一级）
            project_root = os_module.path.dirname(script_dir)
            # 设置文件的正确路径：存档文件夹中的设置_数据库.json
            settings_path = os_module.path.join(project_root, "存档", "设置_数据库.json")
            
            # 检查文件是否存在
            if os_module.path.exists(settings_path):
                with open(settings_path, 'r', encoding='utf-8') as f:
                    settings = json_module.load(f)
                    # 尝试获取特效渲染设置
                    if isinstance(settings, dict) and '特效渲染' in settings:
                        effect_setting = settings['特效渲染']
                        print(f"已从设置文件加载特效渲染设置: {effect_setting}")
                        return effect_setting
            
            print(f"未找到设置_数据库.json或特效渲染设置，使用默认值: {default_effect}")
        except Exception as e:
            print(f"加载设置_数据库.json时出错: {e}，使用默认值: {default_effect}")
        
        return default_effect
    
    def 绘制底部图形(self):
        """在屏幕底部中心绘制快捷栏，包含8个间隔5像素的正方形，并在上方绘制进度条 - UI优化版"""
        屏幕宽度 = self.屏幕.get_width()
        屏幕高度 = self.屏幕.get_height()
        
        # 设置图形参数
        正方形大小 = 45  # 增加大小，更易于点击
        正方形间距 = 8
        长方形高度 = 正方形大小 + 20  # 长方形比正方形高10像素的边距
        长方形宽度 = 8 * 正方形大小 + 7 * 正方形间距 + 40  # 8个正方形和7个间距，额外增加40像素
        
        # 定义颜色
        背景颜色 = (80, 80, 80)  # 深灰色背景
        边框颜色 = (120, 120, 120)  # 边框颜色
        选中边框颜色 = (255, 215, 0)  # 金色选中边框
        进度条背景 = (150, 79, 29)  # 稍微亮一点的棕色
        进度条颜色 = (255, 215, 0)  # 金色
        
        # 计算长方形位置（底部中心）
        长方形_x = (屏幕宽度 - 长方形宽度) // 2
        长方形_y = 屏幕高度 - 长方形高度 - 10  # 距离底部10像素
        
        # 绘制进度条（UI优化）
        进度条_height = 10
        进度条_y = 长方形_y - 15  # 在长方形上方15像素处
        圆角半径 = 5
        
        # 绘制进度条背景带圆角
        pygame.draw.rect(self.屏幕, 进度条背景, 
                        (长方形_x, 进度条_y, 长方形宽度, 进度条_height),
                        border_radius=圆角半径)
        # 绘制进度条边框
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (长方形_x, 进度条_y, 长方形宽度, 进度条_height),
                        2, border_radius=圆角半径)
        # 从玩家对象获取star相关属性
        if hasattr(self.玩家, 'star_count') and hasattr(self.玩家, 'star_progress'):
            star_count = self.玩家.star_count
            star_progress = self.玩家.star_progress
        else:
            star_count = 0
            star_progress = 0
        
        # 确保进度值在有效范围内
        # 修复进度条逻辑：如果star_progress是0-1范围的值，直接使用；否则才做0-100限制
        if star_progress <= 1:  # 检查是否已经是0-1范围
            normalized_progress = star_progress
        else:
            normalized_progress = min(max(star_progress, 0), 100) / 100
        
        # 绘制动态进度条
        进度_width = int(长方形宽度 * normalized_progress)
        pygame.draw.rect(self.屏幕, 进度条颜色, 
                        (长方形_x + 2, 进度条_y + 2, 进度_width - 4, 进度条_height - 4),
                        border_radius=圆角半径 - 2)
        
        # 在进度条上方中心显示动态star文字
        try:
            # 创建字体对象
            try:
                font = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 20, bold=True)
                fps_font = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 18, bold=True)
                item_count_font = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 16, bold=True)
            except:
                font = pygame.font.Font(None, 20)
                fps_font = pygame.font.Font(None, 18)
                item_count_font = pygame.font.Font(None, 16)
            
            text = font.render(f'star : {star_count}', True, (255, 255, 255))  # 白色文字
            # 计算文字位置，放在进度条上方中心
            text_rect = text.get_rect(center=(长方形_x + 长方形宽度 // 2, 进度条_y - 12))
            self.屏幕.blit(text, text_rect)
            
            # 更新帧率计数
            self.frame_count += 1
            # 使用目标帧率限制游戏循环
            dt = self.时钟.tick(self.target_fps) / 1000.0  # 转换为秒
            
            # 使用pygame的get_fps方法获取实际帧率
            pygame_fps = self.时钟.get_fps()
            # 四舍五入到整数并确保至少为0
            self.current_fps = max(0, int(round(pygame_fps)))
            
            # 在右下角显示动态FPS - 使用更好的样式
            fps_display = f"FPS：{self.current_fps:02d}"
            fps_text = fps_font.render(fps_display, True, (255, 255, 255))  # 白色文字
            # 计算右下角位置
            fps_rect = fps_text.get_rect(bottomright=(self.屏幕.get_width() - 15, self.屏幕.get_height() - 15))
            # 添加半透明背景
            pygame.draw.rect(self.屏幕, (0, 0, 0, 128), 
                            (fps_rect.x - 5, fps_rect.y - 5, fps_rect.width + 10, fps_rect.height + 10))
            self.屏幕.blit(fps_text, fps_rect)
            
        except Exception as e:
            print(f"绘制文字时出错: {e}")
        
        # 绘制长方形（深灰色背景）
        pygame.draw.rect(self.屏幕, 背景颜色, 
                        (长方形_x, 长方形_y, 长方形宽度, 长方形高度))
        # 绘制边框
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (长方形_x, 长方形_y, 长方形宽度, 长方形高度), 2)
        
        # 绘制8个正方形，间隔5像素 - 添加边框和选中效果
        第一个正方形_x = 长方形_x + (长方形宽度 - (8 * 正方形大小 + 7 * 正方形间距)) // 2
        正方形_y = 长方形_y + (长方形高度 - 正方形大小) // 2
        
        # 获取快捷栏物品数据
        hotbar_items = []
        # 从背包管理器获取快捷栏物品
        if hasattr(self, '背包管理器'):
            hotbar_items = self.背包管理器.快捷栏物品[:8]  # 只取前8个快捷栏物品
        for i in range(8):
            正方形_x = 第一个正方形_x + i * (正方形大小 + 正方形间距)
            
            # 绘制正方形背景（稍微深一点的颜色）
            pygame.draw.rect(self.屏幕, (60, 60, 60), 
                            (正方形_x, 正方形_y, 正方形大小, 正方形大小))
            # 绘制正方形边框
            pygame.draw.rect(self.屏幕, 边框颜色, 
                            (正方形_x, 正方形_y, 正方形大小, 正方形大小), 2)
            
            # 根据当前选中格子显示选中状态
            if i == self.当前选中格子:
                pygame.draw.rect(self.屏幕, 选中边框颜色, 
                                (正方形_x - 2, 正方形_y - 2, 正方形大小 + 4, 正方形大小 + 4), 3)
                
                # 绘制物品使用进度条（当显示进度条且进度大于0时）
                if self.显示物品使用进度 and self.物品使用进度 > 0:
                    # 进度条参数
                    progress_bar_height = 5
                    progress_bar_width = 正方形大小 - 8  # 进度条宽度比物品格小8像素
                    progress_bar_x = 正方形_x + 4  # 居中显示
                    progress_bar_y = 正方形_y - progress_bar_height - 2  # 位于物品格上方
                    
                    # 绘制进度条背景（半透明）
                    s = pygame.Surface((progress_bar_width, progress_bar_height), pygame.SRCALPHA)
                    s.fill((0, 0, 0, 128))
                    self.屏幕.blit(s, (progress_bar_x, progress_bar_y))
                    
                    # 计算进度条长度
                    progress_length = int(progress_bar_width * self.物品使用进度)
                    
                    # 绘制进度条（白色）
                    if progress_length > 0:
                        pygame.draw.rect(self.屏幕, (255, 255, 255, 200), 
                                        (progress_bar_x, progress_bar_y, progress_length, progress_bar_height))
            
            # 显示快捷栏物品
            if i < len(hotbar_items) and hotbar_items[i] is not None:
                item = hotbar_items[i]
                try:
                    # 尝试使用图片管理器获取物品图片
                    from 图片加载 import 图片管理器
                    # 获取物品图片，尺寸设为正方形大小的80%（需要传递元组）
                    图片尺寸 = int(正方形大小 * 0.8)
                    item_image = 图片管理器.获取物品图片(item.物品_id, (图片尺寸, 图片尺寸))
                    
                    # 如果获取到图片，绘制到格子中心
                    if item_image:
                        # 计算图片位置，使其居中
                        image_x = 正方形_x + (正方形大小 - item_image.get_width()) // 2
                        image_y = 正方形_y + (正方形大小 - item_image.get_height()) // 2
                        self.屏幕.blit(item_image, (image_x, image_y))
                    
                    # 显示物品数量（如果大于1）
                    if item.数量 > 1:
                        # 使用item_count_font字体
                        count_text = item_count_font.render(str(item.数量), True, (255, 255, 255))
                        # 在格子右下角显示数量
                        text_x = 正方形_x + 正方形大小 - count_text.get_width() - 2
                        text_y = 正方形_y + 正方形大小 - count_text.get_height() - 2
                        self.屏幕.blit(count_text, (text_x, text_y))
                    
                    # 显示技能冷却时间（所有武器都显示）
                    物品名称 = item.获取名称()
                    # 获取剩余冷却时间
                    remaining_cooldown = 武器技能管理器实例.get_remaining_cooldown(物品名称)
                    if remaining_cooldown > 0:
                        # 格式化冷却时间：最后1秒显示1位小数，否则显示整数
                        if remaining_cooldown < 1:
                            cooldown_text_str = f"{remaining_cooldown:.1f}"
                        else:
                            cooldown_text_str = f"{int(remaining_cooldown)}"
                        # 在物品中心显示冷却时间
                        cooldown_text = item_count_font.render(cooldown_text_str, True, (255, 255, 255))
                        # 添加白边效果
                        outline_text = item_count_font.render(cooldown_text_str, True, (0, 0, 0))
                        # 计算中心位置
                        center_x = 正方形_x + 正方形大小 // 2
                        center_y = 正方形_y + 正方形大小 // 2
                        # 绘制白边
                        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                            self.屏幕.blit(outline_text, (center_x - outline_text.get_width() // 2 + dx, 
                                                          center_y - outline_text.get_height() // 2 + dy))
                        # 绘制文字
                        self.屏幕.blit(cooldown_text, (center_x - cooldown_text.get_width() // 2, 
                                                      center_y - cooldown_text.get_height() // 2))
                    
                    # 显示齐天金箍棒形态
                    if '齐天金箍棒' in 物品名称:
                        # 获取当前形态
                        from 武器处理 import 齐天金箍棒形态数据
                        当前形态 = getattr(self.玩家, '齐天金箍棒形态', 0) + 1
                        # 显示形态文字
                        form_text = item_count_font.render(f"形态{当前形态}", True, (255, 215, 0))
                        # 添加黑边效果
                        form_outline_text = item_count_font.render(f"形态{当前形态}", True, (0, 0, 0))
                        # 在物品格左上角显示
                        form_x = 正方形_x + 2
                        form_y = 正方形_y + 2
                        # 绘制黑边
                        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                            self.屏幕.blit(form_outline_text, (form_x + dx, form_y + dy))
                        # 绘制文字
                        self.屏幕.blit(form_text, (form_x, form_y))
                    
                    # 绘制耐久度进度条
                    max_durability = item.获取属性("耐久度", 0)
                    if max_durability > 0:
                        current_durability = item.获取属性("当前耐久度", max_durability)
                        durability_percent = (current_durability / max_durability) * 100
                        
                        # 满95%+不显示耐久进度条
                        if durability_percent < 95:
                            # 快捷栏显示5像素高的耐久条
                            progress_bar_height = 5
                            progress_bar_width = 正方形大小 - 8  # 进度条宽度比物品格小8像素
                            progress_bar_x = 正方形_x + 4  # 居中显示
                            progress_bar_y = 正方形_y + 正方形大小 - progress_bar_height - 2  # 距离底部2像素
                            
                            # 根据耐久度百分比连续变化颜色
                            # 从红色(低耐久)到黄色(中耐久)再到绿色(高耐久)
                            if durability_percent <= 50:
                                # 红色到黄色的渐变 (0-50%)
                                ratio = durability_percent / 50
                                red = 255
                                green = int(255 * ratio)
                                blue = 0
                            else:
                                # 黄色到绿色的渐变 (50-100%)
                                ratio = (durability_percent - 50) / 50
                                red = int(255 * (1 - ratio))
                                green = 255
                                blue = 0
                            color = (red, green, blue)
                            
                            # 计算进度条长度
                            progress_length = int(progress_bar_width * (durability_percent / 100))
                            # 绘制耐久度背景
                            pygame.draw.rect(self.屏幕, (0, 0, 0, 128), 
                                            (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
                            # 绘制耐久度进度
                            if progress_length > 0:
                                pygame.draw.rect(self.屏幕, color, 
                                                (progress_bar_x, progress_bar_y, progress_length, progress_bar_height))
                except Exception as e:
                    # 静默失败，不影响游戏运行
                    pass
            
            # 不显示格子标签
        
        # 检查当前是否手持手枪、步枪、狙击枪、喷子、冲锋枪、机甲武器或齐天武器，只有手持这些武器时才显示换弹按钮和文字
        工具实例, 当前工具 = self.获取当前手持工具()
        是否手枪 = 当前工具 and '手枪' in 当前工具['名称'] if 当前工具 else False
        是否步枪 = 当前工具 and '步枪' in 当前工具['名称'] if 当前工具 else False
        是否狙击枪 = 当前工具 and '狙击枪' in 当前工具['名称'] if 当前工具 else False
        是否喷子 = 当前工具 and '喷子' in 当前工具['名称'] if 当前工具 else False
        是否冲锋枪 = 当前工具 and '冲锋枪' in 当前工具['名称'] if 当前工具 else False
        是否机甲武器 = 当前工具 and '机甲' in 当前工具['名称'] if 当前工具 else False
        是否齐天武器 = 当前工具 and '齐天' in 当前工具['名称'] if 当前工具 else False
        # 检查是否是齐天金箍棒（近战武器，不显示换弹按钮）
        是齐天金箍棒 = 当前工具 and '齐天金箍棒' in 当前工具['名称'] if 当前工具 else False
        武器名称 = 当前工具.get('名称', '') if 当前工具 else ''
        是否显示换弹按钮 = (是否手枪 or 是否步枪 or 是否狙击枪 or 是否喷子 or 是否冲锋枪 or 是否机甲武器 or 是否齐天武器 or '救世主' in 武器名称) and not 是齐天金箍棒
        
        if 是否显示换弹按钮:
            # 统一将换弹按钮显示在第8个格子（索引7）上方，不管手枪实际位置
            第8个格子索引 = 7
            第8个格子_x = 第一个正方形_x + 第8个格子索引 * (正方形大小 + 正方形间距)
            第8个格子_y = 正方形_y
            
            # 计算圆圈位置（第8个格子中心上方40像素）
            圆圈中心_x = 第8个格子_x + 正方形大小 // 2 - 25
            圆圈中心_y = 第8个格子_y - 40
            圆圈半径 = 12
            
            # 处理换弹按钮动画
            动画缩放因子 = 1.0
            if hasattr(self, '换弹按钮按下') and self.换弹按钮按下:
                # 计算动画进度
                动画进度 = self.换弹按钮动画时间 / self.换弹按钮动画时长
                if 动画进度 < 1.0:
                    # 按钮按下动画：先缩小后恢复
                    if 动画进度 < 0.5:
                        # 前半段缩小
                        动画缩放因子 = 1.0 - 动画进度 * 0.3
                    else:
                        # 后半段恢复
                        动画缩放因子 = 0.85 + (动画进度 - 0.5) * 0.3
                else:
                    # 动画结束
                    self.换弹按钮按下 = False
                    self.换弹按钮动画时间 = 0
                    动画缩放因子 = 1.0
            
            # 应用动画缩放
            动画圆圈半径 = int(圆圈半径 * 动画缩放因子)
            
            # 绘制圆圈：先绘制白色实心内圈，再绘制黑色外圈边框
            # 保存圆圈矩形区域，用于点击检测
            圆圈_rect = pygame.Rect(
                圆圈中心_x - 圆圈半径, 
                圆圈中心_y - 圆圈半径, 
                圆圈半径 * 2, 
                圆圈半径 * 2
            )
            # 将圆圈矩形保存为实例属性，以便点击检测时使用
            self.换弹按钮_rect = 圆圈_rect
            
            # 绘制白色实心内圈，考虑动画缩放
            pygame.draw.circle(self.屏幕, (255, 255, 255), (圆圈中心_x, 圆圈中心_y), 动画圆圈半径)
            # 绘制黑色外圈边框，线宽为2，考虑动画缩放
            pygame.draw.circle(self.屏幕, (0, 0, 0), (圆圈中心_x, 圆圈中心_y), 动画圆圈半径, 2)
            
            # 在圆圈中心显示文字：<->
            # 创建中心文字专用字体，调整字体大小以确保"R"居中显示
            center_font = None
            try:
                center_font = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 16, bold=True)
            except:
                center_font = pygame.font.Font(None, 16)
        else:
            # 清除换弹按钮矩形，防止点击检测
            if hasattr(self, '换弹按钮_rect'):
                delattr(self, '换弹按钮_rect')
        
        if 是否显示换弹按钮:
            # 要显示的中心文字，修改为R
            center_text = "R"
            # 渲染中心文字，颜色改为黑色
            center_text_surface = center_font.render(center_text, True, (0, 0, 0))
            # 计算中心文字位置：圆圈中心
            center_text_x = 圆圈中心_x - center_text_surface.get_width() // 2
            center_text_y = 圆圈中心_y - center_text_surface.get_height() // 2
            # 绘制中心文字
            self.屏幕.blit(center_text_surface, (center_text_x, center_text_y))
            
            # 在圆圈右边显示文字：弹夹子弹/无限
            # 创建右侧文字专用字体
            right_font = None
            try:
                right_font = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 18, bold=True)
            except:
                right_font = pygame.font.Font(None, 18)
            
            # 获取当前手持工具
            工具实例, 当前工具 = self.获取当前手持工具()
            
            # 从物品实例获取当前弹匣子弹数
            当前弹匣子弹 = 0
            if 工具实例 and 当前工具 and ('手枪' in 当前工具.get('名称', '') or '步枪' in 当前工具.get('名称', '') or '狙击枪' in 当前工具.get('名称', '') or '喷子' in 当前工具.get('名称', '') or '冲锋枪' in 当前工具.get('名称', '') or '齐天' in 当前工具.get('名称', '') or '机甲' in 当前工具.get('名称', '') or '救世主' in 当前工具.get('名称', '')):
                当前弹匣子弹 = 工具实例.获取属性("当前弹匣子弹", 0)
            
            # 检查是否为齐天武器（无限子弹）
            is_qitian_weapon = False
            if 当前工具 and '齐天' in 当前工具.get('名称', ''):
                is_qitian_weapon = True
            
            # 检查是否为救世主系列特殊武器
            is_savior_special = False
            if 当前工具 and '救世主' in 当前工具.get('名称', '') and ('弩' not in 当前工具.get('名称', '')):
                is_savior_special = True
            
            # 根据武器类型显示不同的弹药信息
            if is_qitian_weapon:
                # 齐天武器：显示弹夹数量/无限
                right_text = f"{当前弹匣子弹}/无限"
            elif is_savior_special:
                # 救世主特殊武器：显示弹夹数量/未知
                right_text = f"{当前弹匣子弹}/未知"
            else:
                # 其他武器：显示弹夹数量/背包子弹数
                from 物品定义 import 子弹, 机甲弹
                # 根据武器类型选择弹药类型
                is_mecha_weapon = False
                if 当前工具 and '机甲' in 当前工具.get('名称', ''):
                    is_mecha_weapon = True
                ammo_type = 机甲弹 if is_mecha_weapon else 子弹
                背包子弹数 = self.背包管理器.获取物品总数量(ammo_type)
                right_text = f"{当前弹匣子弹}/{背包子弹数}"
            # 渲染右侧文字，颜色改为白色
            right_text_surface = right_font.render(right_text, True, (255, 255, 255))
            # 计算右侧文字位置：圆圈右边，垂直居中对齐
            right_text_x = 圆圈中心_x + 圆圈半径 + 5  # 圆圈右边5像素
            right_text_y = 圆圈中心_y - right_text_surface.get_height() // 2  # 垂直居中
            # 绘制右侧文字
            self.屏幕.blit(right_text_surface, (right_text_x, right_text_y))
            
            # 绘制换弹进度条（如果正在换弹）
            if self.换弹中 and self.显示换弹进度条:
                # 进度条参数
                progress_bar_height = 5
                progress_bar_width = 正方形大小 - 8  # 进度条宽度比物品格小8像素
                
                # 计算当前选中格子的位置，进度条显示在当前手持手枪的快捷栏格子上方
                当前选中格子_x = 第一个正方形_x + self.当前选中格子 * (正方形大小 + 正方形间距)
                当前选中格子_y = 正方形_y
                
                progress_bar_x = 当前选中格子_x + 4  # 居中显示
                progress_bar_y = 当前选中格子_y - progress_bar_height - 5  # 距离顶部5像素
                
                # 绘制进度条背景（半透明）
                s = pygame.Surface((progress_bar_width, progress_bar_height), pygame.SRCALPHA)
                s.fill((0, 0, 0, 128))
                self.屏幕.blit(s, (progress_bar_x, progress_bar_y))
                
                # 计算进度条长度
                progress_length = int(progress_bar_width * self.换弹进度)
                
                # 绘制进度条（白色）
                if progress_length > 0:
                    pygame.draw.rect(self.屏幕, (255, 255, 255, 200), 
                                    (progress_bar_x, progress_bar_y, progress_length, progress_bar_height))
    
    def handle_item_pickup(self):
        """处理玩家捡取掉落物的逻辑"""
        # 创建一个新列表来存储未被捡取的掉落物
        remaining_items = []
        
        for item in self.世界.items:
            # 检查掉落物是否可以被拾取且与玩家碰撞
            if item.can_pickup and item.collides_with_player(
                self.玩家.坐标_x, self.玩家.坐标_y,
                self.玩家.宽, self.玩家.高
            ):
                # 尝试将物品添加到玩家背包
                success = False
                if hasattr(self, '背包管理器'):
                    success = self.背包管理器.添加物品到背包(item.item_id, item.count)
                
                if success:
                    print(f"玩家捡取了 {item.count} 个 物品{item.item_id}")
                    
                    # 尝试播放捡取音效
                    try:
                        from 音频输出 import audio_manager
                        audio_manager.play_sound("物品拾取")
                    except:
                        pass
                    
                    # 不将这个物品添加回remaining_items列表，相当于移除它
                else:
                    # 如果背包已满，保留物品
                    remaining_items.append(item)
                    print(f"背包已满，无法捡取物品{item.item_id}")
            else:
                # 保留未被捡取的物品
                remaining_items.append(item)
        
        # 更新世界中的掉落物列表
        self.世界.items = remaining_items
    
    def 检查快捷栏点击(self, 鼠标位置):
        """检查鼠标点击是否在快捷栏格子上，如果是返回格子索引，否则返回-1"""
        屏幕宽度 = self.屏幕.get_width()
        屏幕高度 = self.屏幕.get_height()
        
        # 快捷栏参数（与绘制底部图形方法保持一致）
        正方形大小 = 45
        正方形间距 = 8
        长方形高度 = 正方形大小 + 20
        长方形宽度 = 8 * 正方形大小 + 7 * 正方形间距 + 40
        
        # 计算长方形位置
        长方形_x = (屏幕宽度 - 长方形宽度) // 2
        长方形_y = 屏幕高度 - 长方形高度 - 10
        
        # 计算第一个正方形位置
        第一个正方形_x = 长方形_x + (长方形宽度 - (8 * 正方形大小 + 7 * 正方形间距)) // 2
        正方形_y = 长方形_y + (长方形高度 - 正方形大小) // 2
        
        # 检查鼠标是否在某个格子内
        for i in range(8):
            正方形_x = 第一个正方形_x + i * (正方形大小 + 正方形间距)
            # 检查鼠标位置是否在当前格子内
            if 正方形_x <= 鼠标位置[0] <= 正方形_x + 正方形大小 and \
               正方形_y <= 鼠标位置[1] <= 正方形_y + 正方形大小:
                return i
        
        return -1  # 没有点击到任何格子
    
    def 绘制BOSS血量条(self):
        """在屏幕上方绘制BOSS血量条"""
        # 尝试导入boss_manager
        try:
            from boos生物处理 import boss_manager
            current_boss = boss_manager.get_current_boss()
            
            if current_boss and current_boss.is_alive():
                # 计算玩家与贝利亚的距离
                player_x, player_y = self.玩家.坐标_x, self.玩家.坐标_y
                boss_x, boss_y = current_boss.x, current_boss.y
                
                # 计算欧几里得距离
                dx = player_x - boss_x
                dy = player_y - boss_y
                distance = math.sqrt(dx * dx + dy * dy)
                
                # 只有在600*600范围内才显示BOSS血量条
                if distance <= 600:
                    # 计算血量条位置和尺寸
                    screen_width, screen_height = self.屏幕.get_size()
                    
                    # 大升级：增加血量条尺寸和视觉效果
                    bar_width = screen_width * 0.49  # 宽度缩小30%，变为屏幕的49%
                    bar_height = 30  # 高度增加到30像素
                    bar_x = (screen_width - bar_width) // 2
                    bar_y = 40
                    
                    # 计算血量百分比
                    health_ratio = current_boss.health / current_boss.max_health
                    
                    # 大升级：添加发光效果
                    glow_radius = 8
                    health_color = (255, 0, 0)  # 玩家要求：使用红色
                    
                    # 绘制发光效果
                    for i in range(glow_radius, 0, -1):
                        alpha = 255 - (i * 20)
                        glow_surface = pygame.Surface((bar_width + i*2, bar_height + i*2), pygame.SRCALPHA)
                        pygame.draw.rect(glow_surface, (*health_color, alpha), (i, i, bar_width, bar_height), border_radius=8)
                        self.屏幕.blit(glow_surface, (bar_x - i, bar_y - i))
                    
                    # 绘制血量条背景（带圆角）
                    pygame.draw.rect(self.屏幕, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height), border_radius=8)
                    pygame.draw.rect(self.屏幕, (60, 60, 60), (bar_x + 2, bar_y + 2, bar_width - 4, bar_height - 4), border_radius=6)
                    
                    # 绘制血量条前景（带圆角和渐变效果）
                    # 主血量条
                    pygame.draw.rect(self.屏幕, (*health_color, 255), (bar_x + 4, bar_y + 4, bar_width * health_ratio - 8, bar_height - 8), border_radius=4)
                    
                    # 绘制高光效果
                    highlight_surface = pygame.Surface((bar_width * health_ratio - 8, bar_height - 8), pygame.SRCALPHA)
                    pygame.draw.rect(highlight_surface, (255, 255, 255, 40), (0, 0, bar_width * health_ratio - 8, (bar_height - 8) // 2), border_radius=4)
                    self.屏幕.blit(highlight_surface, (bar_x + 4, bar_y + 4))
                    
                    # 绘制边框（双层边框）
                    pygame.draw.rect(self.屏幕, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 3, border_radius=8)
                    pygame.draw.rect(self.屏幕, (100, 100, 100), (bar_x + 1, bar_y + 1, bar_width - 2, bar_height - 2), 1, border_radius=7)
                    
                    # 绘制BOSS名称和血量文字
                    # 尝试使用系统自带的中文字体
                    # 根据BOSS类型动态获取名称
                    boss_name = "未知BOSS"
                    # 检查BOSS的mob_id属性来确定名称
                    if hasattr(current_boss, 'mob_id'):
                        try:
                            from 生物系统 import 贝利亚, 吸血鬼, 肥胖Boss
                            if current_boss.mob_id == 贝利亚:
                                boss_name = "贝利亚"
                            elif current_boss.mob_id == 吸血鬼:
                                boss_name = "吸血鬼"
                            elif current_boss.mob_id == 肥胖Boss:
                                boss_name = "肥胖Boss"
                        except ImportError:
                            pass
                    # 或者检查BOSS的name属性
                    elif hasattr(current_boss, 'name'):
                        boss_name = current_boss.name
                    # 或者检查BOSS的类名来确定名称
                    elif hasattr(current_boss, '__class__'):
                        if current_boss.__class__.__name__ == 'BelialBoss':
                            boss_name = "贝利亚"
                        elif current_boss.__class__.__name__ == 'VampireBoss':
                            boss_name = "吸血鬼"
                        elif "肥胖" in current_boss.__class__.__name__:
                            boss_name = "肥胖Boss"
                    # 减小字体大小并调整显示格式
                    try:
                        # 使用系统中文字体（优先使用黑体，然后微软雅黑），字体大小调整为18
                        font = pygame.font.SysFont(["SimHei", "Microsoft YaHei", "黑体", "微软雅黑"], 18)
                        # 计算血量百分比并格式化为整数
                        health_percentage = int(health_ratio * 100)
                        # 获取贝利亚上次使用的技能
                        last_skill = getattr(current_boss, 'last_skill', '未使用技能')
                        # 调整显示格式为"贝利亚:100%-技能"
                        health_text = f"{boss_name}: {health_percentage}%-{last_skill}"
                        text_surface = font.render(health_text, True, (255, 255, 255))
                    except Exception as e:
                        # 使用默认字体，保持中文显示
                        font = pygame.font.Font(None, 18)
                        # 计算血量百分比并格式化为整数
                        health_percentage = int(health_ratio * 100)
                        # 获取贝利亚上次使用的技能
                        last_skill = getattr(current_boss, 'last_skill', '未使用技能')
                        # 调整显示格式为"贝利亚:100%-技能"
                        health_text = f"{boss_name}: {health_percentage}%-{last_skill}"
                        text_surface = font.render(health_text, True, (255, 255, 255))
                    text_x = (screen_width - text_surface.get_width()) // 2
                    text_y = bar_y + bar_height + 5
                    self.屏幕.blit(text_surface, (text_x, text_y))
        except Exception as e:
            # 如果导入失败或没有BOSS，忽略错误
            pass

    def run(self):
        """游戏主循环"""
        上一次时间 = time.time()
        
        print("游戏已启动！")
        print(f"世界名称: {self.世界参数['存档名称']}")
        print(f"世界大小: {self.世界.宽度}x{self.世界.高度}")
        print(f"世界类型: {self.世界参数['世界类型']}")
        print(f"创造模式: {'开启' if self.创造模式 else '关闭'}")
        print("\n游戏控制:")
        print("A/左箭头: 向左移动")
        print("D/右箭头: 向右移动")
        print("空格: 跳跃")
        print("鼠标左键长按: 挖掘方块")
        print("鼠标右键: 放置方块")
        
        # 初始化相机位置
        self.相机_x = self.玩家.坐标_x - 宽度 // 2
        self.相机_y = self.玩家.坐标_y - 高度 // 2
        
        # 检查初始云数量
        print(f"\n初始云数量: {len(self.世界.clouds)}")
        print(f"玩家初始位置: x={self.玩家.坐标_x}, y={self.玩家.坐标_y}")
        print(f"相机初始位置: x={self.相机_x}, y={self.相机_y}")
        
        while self.运行中:
            # 计算delta时间
            当前时间 = time.time()
            时间增量 = 当前时间 - 上一次时间
            上一次时间 = 当前时间
            
            # 限制时间增量，防止大延迟
            时间增量 = min(时间增量, 0.1)
            
            # 处理事件
            self.handle_events()
            
            # 更新游戏状态
            self.update(时间增量)
            # 更新页面状态
            self.page_manager.update(时间增量)
            
            # 自动保存功能已替换为每天12:00自动保存，不再使用时间间隔自动保存
            # 自动保存逻辑已移至World类的update方法中实现
            
            # 更新相机位置（支持平滑跟随和非绑定玩家）
            self.update_camera()
            
            # 绘制
            self.draw(self.相机_x, self.相机_y)
            
            # 使用页面管理器绘制所有打开的页面
            self.page_manager.draw()
            
            # 更新屏幕
            pygame.display.flip()
            
            # 控制帧率，使用从设置加载的目标帧率
            self.时钟.tick(self.target_fps)
        
        # 游戏结束，返回主程序
        print("游戏结束，返回主菜单")

    def 获取鼠标指向的方块(self, 鼠标位置):
        """根据鼠标位置获取指向的方块坐标 - 优化版，支持距离限制和全屏点击"""
        # 获取相机位置（支持非绑定玩家）
        相机_x, 相机_y = self.get_camera_position()
        
        # 转换为世界坐标
        世界_x = 鼠标位置[0] + 相机_x
        世界_y = 鼠标位置[1] + 相机_y
        
        # 转换为方块坐标
        方块_x = int(世界_x // 方块大小)
        方块_y = int(世界_y // 方块大小)
        
        # 检查是否在世界范围内
        if (self.世界.无限世界 and 0 <= 方块_y < self.世界.高度) or (not self.世界.无限世界 and 0 <= 方块_x < self.世界.宽度 and 0 <= 方块_y < self.世界.高度):
            # 检查是否启用了全屏点击功能
            if not self.enable_fullscreen_click:
                # 普通模式：限制在玩家坐标±5个方块范围内
                玩家方块_x = int(self.玩家.坐标_x // 方块大小)
                玩家方块_y = int(self.玩家.坐标_y // 方块大小)
                
                # 最大交互距离：5个方块
                if abs(方块_x - 玩家方块_x) > 5 or abs(方块_y - 玩家方块_y) > 5:
                    return None
            
            return (方块_x, 方块_y)
        return None
    
    def 计算放置位置(self, 点击_x, 点击_y):
        """计算方块的实际放置位置
        根据点击的方块是否为空，决定是直接放置还是放在旁边"""
        # 如果点击的位置是空的，直接返回该位置
        if self.世界.get_block(点击_x, 点击_y) == 空气:
            # 检查是否启用了全屏点击功能
            if not self.enable_fullscreen_click:
                # 检查该位置是否在玩家交互范围内
                玩家方块_x = int(self.玩家.坐标_x // 方块大小)
                玩家方块_y = int(self.玩家.坐标_y // 方块大小)
                
                # 最大交互距离：5个方块
                if abs(点击_x - 玩家方块_x) > 5 or abs(点击_y - 玩家方块_y) > 5:
                    return None, None
            return 点击_x, 点击_y
        
        # 否则尝试放在周围的四个方向
        方向 = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # 上、下、左、右
        
        for dx, dy in 方向:
            new_x, new_y = 点击_x + dx, 点击_y + dy
            # 检查是否在世界范围内且为空 - 兼容无限世界
            位置有效 = False
            if self.世界.无限世界:
                # 无限世界，只检查y坐标是否在范围内且方块为空
                if 0 <= new_y < self.世界.高度 and self.世界.get_block(new_x, new_y) == 空气:
                    位置有效 = True
            else:
                # 有限世界，检查x和y坐标是否在范围内且方块为空
                if 0 <= new_x < self.世界.宽度 and 0 <= new_y < self.世界.高度 and self.世界.get_block(new_x, new_y) == 空气:
                    位置有效 = True
            
            if 位置有效:
                # 检查是否启用了全屏点击功能
                if not self.enable_fullscreen_click:
                    # 检查该位置是否在玩家交互范围内
                    玩家方块_x = int(self.玩家.坐标_x // 方块大小)
                    玩家方块_y = int(self.玩家.坐标_y // 方块大小)
                    
                    # 最大交互距离：5个方块
                    if abs(new_x - 玩家方块_x) > 5 or abs(new_y - 玩家方块_y) > 5:
                        continue
                return new_x, new_y
        
        return None, None  # 无法放置
    
    def check_placement_collision(self, 方块_x, 方块_y):
        """检查放置方块是否会与玩家碰撞"""
        # 计算方块的世界坐标
        block_world_x = 方块_x * 方块大小
        block_world_y = 方块_y * 方块大小
        
        # 检查玩家是否与方块重叠
        player_left = self.玩家.坐标_x
        player_right = self.玩家.坐标_x + self.玩家.宽
        player_top = self.玩家.坐标_y
        player_bottom = self.玩家.坐标_y + self.玩家.高
        
        # 方块的边界
        block_left = block_world_x
        block_right = block_world_x + 方块大小
        block_top = block_world_y
        block_bottom = block_world_y + 方块大小
        
        # 检查是否重叠
        if (player_right > block_left and player_left < block_right and 
            player_bottom > block_top and player_top < block_bottom):
            return True  # 会碰撞
        
        return False  # 不会碰撞
    
    def update_camera(self):
        """更新相机位置 - 支持非绑定玩家和相机跟随"""
        # 获取当前屏幕实际大小
        当前屏幕宽度, 当前屏幕高度 = self.屏幕.get_size()
        
        # 平滑相机跟随，确保玩家始终在屏幕中心
        target_x = self.玩家.坐标_x - 当前屏幕宽度 // 2
        target_y = self.玩家.坐标_y - 当前屏幕高度 // 2
        
        # 相机平滑因子
        平滑因子 = 0.1
        
        # 初始化相机位置（如果不存在）
        if not hasattr(self, '相机_x'):
            self.相机_x = target_x
            self.相机_y = target_y
        else:
            # 平滑移动相机
            self.相机_x += (target_x - self.相机_x) * 平滑因子
            self.相机_y += (target_y - self.相机_y) * 平滑因子
        
        # 限制相机范围
        if self.世界.无限世界:
            # 无限世界，只限制y坐标，不限制x坐标
            self.相机_x = self.相机_x
            self.相机_y = max(0, min(self.相机_y, self.世界.高度 * 方块大小 - 当前屏幕高度))
        else:
            # 有限世界，限制x和y坐标
            self.相机_x = max(0, min(self.相机_x, self.世界.宽度 * 方块大小 - 当前屏幕宽度))
            self.相机_y = max(0, min(self.相机_y, self.世界.高度 * 方块大小 - 当前屏幕高度))
    
    def get_camera_position(self):
        """获取当前相机位置"""
        # 获取当前屏幕实际大小
        当前屏幕宽度, 当前屏幕高度 = self.屏幕.get_size()
        
        if hasattr(self, '相机_x'):
            相机_x = self.相机_x
            相机_y = self.相机_y
        else:
            # 默认相机位置（玩家居中）
            相机_x = self.玩家.坐标_x - 当前屏幕宽度 // 2
            相机_y = self.玩家.坐标_y - 当前屏幕高度 // 2
        
        # 应用屏幕震动效果
        if hasattr(self, 'screen_shake') and self.screen_shake > 0:
            # 随机震动偏移
            shake_offset_x = random.randint(-self.screen_shake, self.screen_shake)
            shake_offset_y = random.randint(-self.screen_shake, self.screen_shake)
            相机_x += shake_offset_x
            相机_y += shake_offset_y
            
            # 减少震动强度
            self.screen_shake -= 1
        
        return 相机_x, 相机_y
    
    def 开始挖掘(self, 鼠标位置):
        """开始挖掘方块"""
        方块坐标 = self.获取鼠标指向的方块(鼠标位置)
        if 方块坐标:
            方块_x, 方块_y = 方块坐标
            # 使用get_block方法获取方块，兼容无限世界
            方块_id = self.世界.get_block(方块_x, 方块_y)
            
            # 只有非空气方块才能挖掘
            if 方块_id != 空气:
                self.正在挖掘 = True
                self.挖掘位置 = 方块坐标
                self.挖掘开始时间 = time.time()
                self.挖掘进度 = 0
                self.当前挖掘方块 = 方块_id
    
    def 停止挖掘(self):
        """停止挖掘方块"""
        self.正在挖掘 = False
        self.挖掘位置 = None
        self.挖掘进度 = 0
        self.当前挖掘方块 = None
    
    def 获取当前手持工具(self):
        """获取玩家当前手持的工具"""
        try:
            # 检查是否有背包管理器和当前选中格子
            if hasattr(self, '背包管理器'):
                当前选中格子 = self.当前选中格子
                # 获取当前选中格子的物品
                if 0 <= 当前选中格子 < len(self.背包管理器.快捷栏物品):
                    物品 = self.背包管理器.快捷栏物品[当前选中格子]
                    if 物品:
                        # 从物品定义中获取完整的物品信息
                        from 物品定义 import 物品 as 物品定义
                        物品_id = 物品.物品_id
                        完整物品信息 = 物品定义.get(物品_id, {})
                        
                        # 确保返回的是完整的物品定义信息
                        return (物品, 完整物品信息)
            return (None, None)
        except Exception as e:
            # 如果获取工具失败，返回None
            print(f"获取当前手持工具时出错: {e}")
            return (None, None)
    
    def _开始换弹(self):
        """开始换弹过程"""
        from 物品定义 import 子弹, 机甲弹
        
        # 检查是否正在换弹
        if self.换弹中:
            return
        
        # 获取当前手持工具
        工具实例, 当前工具 = self.获取当前手持工具()
        
        # 检查是否手持手枪、步枪、狙击枪、喷子、冲锋枪、机甲武器或齐天系列武器（除了齐天金箍棒）或救世主系列武器
        武器名称 = 当前工具.get('名称', '') if 当前工具 else ''
        # 检查是否是齐天金箍棒（近战武器，不需要换弹）
        是齐天金箍棒 = '齐天金箍棒' in 武器名称
        if not 当前工具 or ('手枪' not in 武器名称 and '步枪' not in 武器名称 and '狙击枪' not in 武器名称 and '喷子' not in 武器名称 and '冲锋枪' not in 武器名称 and '机甲' not in 武器名称 and '救世主' not in 武器名称 and ('齐天' not in 武器名称 or 是齐天金箍棒)):
            return
        
        # 检查是否是齐天系列武器
        是齐天武器 = '齐天' in 武器名称
        # 检查是否是机甲系列武器
        是机甲武器 = '机甲' in 武器名称
        
        # 非齐天武器需要检查背包中是否有弹药或能源
        if not 是齐天武器:
            # 特殊处理所有救世主武器：需要救世能源才能换弹
            if '救世主' in 武器名称:
                # 检查背包中是否有救世能源
                救世能源实例列表 = []
                # 遍历背包物品（5x6二维列表）
                for 行 in self.背包管理器.背包物品:
                    for 背包格子 in 行:
                        if 背包格子:
                            from 物品定义 import 物品 as 物品定义
                            物品_info = 物品定义.get(背包格子.物品_id, {})
                            if 物品_info.get('名称') == '救世能源':
                                救世能源实例列表.append(背包格子)
                # 遍历快捷栏物品
                for 背包格子 in self.背包管理器.快捷栏物品:
                    if 背包格子:
                        from 物品定义 import 物品 as 物品定义
                        物品_info = 物品定义.get(背包格子.物品_id, {})
                        if 物品_info.get('名称') == '救世能源':
                            救世能源实例列表.append(背包格子)
                
                # 检查是否有救世能源
                if not 救世能源实例列表:
                    # 没有救世能源，显示提示
                    self._show_notification("需要<救世能源>才能换弹")
                    return
                
                # 根据武器类型确定消耗的耐久度
                消耗耐久度 = 30  # 默认消耗30耐久
                if '救世主加特林' in 武器名称:
                    消耗耐久度 = 150  # 救世主加特林消耗150耐久
                elif '救世主喷子' in 武器名称 or '救世主S686' in 武器名称:
                    消耗耐久度 = 20  # 救世主喷子消耗20耐久
                elif '救世主RPG' in 武器名称:
                    消耗耐久度 = 10  # 救世主RPG消耗10耐久
                elif '救世主弩' in 武器名称:
                    消耗耐久度 = 1  # 救世主弩每发射消耗1耐久，不需要换弹
                elif '榴弹炮' in 武器名称:
                    消耗耐久度 = 30  # 救世主榴弹炮消耗30耐久
                else:
                    # 其他救世主枪械消耗30耐久
                    消耗耐久度 = 30
                
                # 找到第一个有足够耐久的救世能源
                可用救世能源 = None
                for 能源实例 in 救世能源实例列表:
                    当前耐久 = 能源实例.获取属性("耐久", 能源实例.物品信息.get("最大耐久", 1000))
                    if 当前耐久 >= 消耗耐久度:
                        可用救世能源 = 能源实例
                        break
                
                if not 可用救世能源:
                    # 没有足够耐久的救世能源，显示提示
                    self._show_notification("救世能源耐久不足")
                    return
            else:
                # 其他武器需要检查背包中是否有弹药
                # 根据武器类型选择弹药类型
                当前弹药类型 = 机甲弹 if 是机甲武器 else 子弹
                # 检查背包中是否有弹药
                背包弹药数量 = self.背包管理器.获取物品总数量(当前弹药类型)
                if 背包弹药数量 <= 0:
                    # 显示没有弹药的提示
                    弹药名称 = "机甲弹" if 是机甲武器 else "子弹"
                    self._show_notification(f"没有{弹药名称}可换！")
                    return
        
        # 从物品实例获取当前弹匣子弹数，从当前工具获取弹匣容量
        当前弹匣子弹 = 工具实例.获取属性("当前弹匣子弹", 0)
        弹匣容量 = 当前工具.get("弹夹", 30)  # 优先使用武器定义的弹夹属性
        
        # 检查弹夹是否已满
        if 当前弹匣子弹 >= 弹匣容量:
            # 弹夹已满，不需要换弹
            self._show_notification("弹夹已满！")
            return
        
        # 开始换弹，保存当前武器实例
        self.换弹中 = True
        self.换弹剩余时间 = self.换弹总时间
        self.换弹开始时间 = self.当前时间
        # 保存正在换弹的武器实例
        self.正在换弹的武器 = 工具实例
        # 初始化换弹进度条
        self.显示换弹进度条 = True
        self.换弹进度 = 0
        
        # 显示换弹提示
        self._show_notification("换弹中...")
        
        # 播放换弹音效
        try:
            from 音频输出 import audio_manager
            audio_manager.play_sound("换弹")
        except Exception as e:
            print(f"播放换弹音效失败: {e}")
    
    def _load_settings_from_file(self):
        """从设置文件加载设置数据"""
        import json
        import os
        # 设置文件路径
        设置文件路径 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../存档/设置_数据库.json')
        
        try:
            if os.path.exists(设置文件路径):
                with open(设置文件路径, 'r', encoding='utf-8') as f:
                    设置数据 = json.load(f)
                    # 更新音效开关
                    if '音效开关' in 设置数据:
                        self.音效开关 = 设置数据['音效开关']
                    # 更新音乐开关
                    if '音乐开关' in 设置数据:
                        self.音乐开关 = 设置数据['音乐开关']
                    # 更新音量
                    if '音量' in 设置数据:
                        self.音量值 = 设置数据['音量']
                    # 更新特效渲染设置
                    if '特效渲染' in 设置数据:
                        self.特效渲染设置 = 设置数据['特效渲染']
                    # 更新显示攻击距离设置
                    if '显示攻击距离' in 设置数据:
                        self.显示攻击距离 = 设置数据['显示攻击距离']
                    # 更新显示受伤距离设置
                    if '显示受伤距离' in 设置数据:
                        self.显示受伤距离 = 设置数据['显示受伤距离']
                    print(f"从设置文件加载设置成功: 音效={self.音效开关}, 音乐={self.音乐开关}, 音量={self.音量值}, 特效={self.特效渲染设置}, 显示攻击距离={self.显示攻击距离}, 显示受伤距离={self.显示受伤距离}")
        except Exception as e:
            print(f"从设置文件加载设置失败: {str(e)}")
    
    def _save_settings_to_file(self):
        """将设置数据保存到设置文件"""
        import json
        import os
        # 设置文件路径
        设置文件路径 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../存档/设置_数据库.json')
        
        try:
            # 确保存档目录存在
            存档目录 = os.path.dirname(设置文件路径)
            if not os.path.exists(存档目录):
                os.makedirs(存档目录)
            
            # 准备要保存的设置数据
            设置数据 = {
                '音效开关': self.音效开关,
                '音乐开关': self.音乐开关,
                '音量': self.音量值,
                '特效渲染': self.特效渲染设置,
                '显示攻击距离': self.显示攻击距离,
                '显示受伤距离': self.显示受伤距离
            }
            
            # 保存设置数据到文件
            with open(设置文件路径, 'w', encoding='utf-8') as f:
                json.dump(设置数据, f, ensure_ascii=False, indent=2)
            print(f"设置数据已保存到文件: {设置文件路径}")
        except Exception as e:
            print(f"保存设置数据到文件失败: {str(e)}")
    
    def _show_notification(self, text, 玩家=None):
        """显示漂浮文字通知"""
        # 根据是否有玩家参数决定显示位置
        if 玩家 is not None:
            # 在玩家位置显示
            x = 玩家.坐标_x + 玩家.宽 // 2
            y = 玩家.坐标_y
        else:
            # 在屏幕中心显示
            x = self.屏幕.get_width() // 2
            y = self.屏幕.get_height() // 2 - 250
        
        # 添加新的漂浮文字到列表
        self.notifications.append({
            "text": text,
            "x": x,  # 显示位置
            "y": y,  # 显示位置
            "alpha": 255,  # 完全不透明
            "start_time": self.当前时间,  # 开始显示时间
            "duration": self.提示显示时间  # 显示持续时间
        })
    
    def _draw_notifications(self, screen):
        """绘制所有漂浮文字"""
        for notification in self.notifications:
            # 创建文字表面
            text_surface = self.提示字体.render(notification["text"], True, (255, 255, 255))
            # 设置透明度
            text_surface.set_alpha(notification["alpha"])
            # 计算文字位置
            # 如果是玩家位置的通知，需要转换为屏幕坐标
            screen_x = notification["x"] - self.相机_x
            screen_y = notification["y"] - self.相机_y
            # 计算文字居中位置
            text_rect = text_surface.get_rect(center=(screen_x, screen_y))
            # 绘制文字
            screen.blit(text_surface, text_rect)
    
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
        

    
    def 射箭(self, 鼠标位置):
        """发射箭矢或子弹"""
        import time
        import random
        
        # 获取当前手持工具
        工具实例, 当前工具 = self.获取当前手持工具()
        
        # 检查是否手持远程武器
        if not 当前工具:
            return
        
        武器名称 = 当前工具.get('名称', '')
        
        # 检查武器类型
        是否未来弩 = '未来弩' in 武器名称
        是否手枪 = '手枪' in 武器名称
        是否步枪 = '步枪' in 武器名称
        是否狙击枪 = '狙击枪' in 武器名称
        是否喷子 = '喷子' in 武器名称
        是否冲锋枪 = '冲锋枪' in 武器名称
        是否弩 = '弩' in 武器名称
        是否弓箭 = '弓箭' in 武器名称
        是否激光炮 = '激光炮' in 武器名称
        是否火箭筒 = '火箭筒' in 武器名称 or '救世主RPG' in 武器名称
        # 检查是否是机甲系列武器
        是否机甲武器 = '机甲' in 武器名称
        # 检查是否是齐天系列武器
        是齐天武器 = '齐天' in 武器名称
        # 检查是否是齐天金箍棒（近战武器，不发射子弹/箭矢）
        是齐天金箍棒 = '齐天金箍棒' in 武器名称
        # 检查是否是龙息系列武器
        是龙息武器 = '龙息' in 武器名称
        # 检查是否是五子棋武器
        是否五子棋 = '五子棋' in 武器名称
        
        # 如果是齐天金箍棒，直接返回，不发射任何东西
        if 是齐天金箍棒:
            return
        
        # 根据武器类型设置冷却时间，优先使用武器定义中的间隔属性
        冷却时间 = 当前工具.get('间隔', 1.0)  # 优先使用武器定义的间隔属性
        
        # 特殊武器类型的冷却时间设置
        if 是否未来弩 or 是否激光炮 or 是龙息武器:
            冷却时间 = 0.0  # 未来弩、激光炮和龙息武器无冷却
        elif 是否火箭筒:
            冷却时间 = 1.0  # 火箭筒冷却时间，1秒
        
        # 新机甲武器专属加成：射速+20%（减少20%冷却时间）
        if 是否机甲武器 and 冷却时间 > 0:
            冷却时间 *= 0.8
        
        # 检查冷却时间
        当前时间 = time.time()
        if 当前时间 - self.弓箭上次射击时间 < 冷却时间:
            # 冷却时间未结束，步枪、冲锋枪、机甲武器和齐天武器不显示等待提示，直接返回
            if 是否机甲武器 or 是否步枪 or 是否冲锋枪 or 是齐天武器:
                return
            # 手枪和狙击枪显示等待提示
            if 是否手枪 or 是否狙击枪:
                self._show_notification("等待中...")
                return
            # 其他武器显示等待提示
            self._show_notification("等待中...")
            return
        
        # 导入物品定义
        from 物品定义 import 木箭, 子弹, 机甲弹
        
        # 根据武器类型选择弹药
        from 物品定义 import 子弹, 木箭, 火箭弹, 机甲弹
        
        弹药类型 = 机甲弹 if 是否机甲武器 else (子弹 if 是否手枪 or 是否步枪 or 是否狙击枪 or 是否喷子 or 是否冲锋枪 or 是齐天武器 or 是否五子棋 else (火箭弹 if 是否火箭筒 else 木箭))
        弹药名称 = '机甲弹' if 是否机甲武器 else ('子弹' if 是否手枪 or 是否步枪 or 是否狙击枪 or 是否喷子 or 是否冲锋枪 or 是齐天武器 or 是否五子棋 else ('火箭弹' if 是否火箭筒 else '木箭'))
        
        # 检查是否有弹药（未来弩、激光炮和龙息武器不消耗弹药）
        弹药数量 = 1  # 未来弩、激光炮和齐天武器默认有弹药
        
        # 检查并消耗弹药（未来弩、激光炮、龙息武器、五子棋和救世主弩不消耗弹药）
        if 是否未来弩 or 是否激光炮 or 是龙息武器 or 是否五子棋 or '救世主弩' in 武器名称:
            # 未来弩、激光炮、龙息武器、五子棋和救世主弩不消耗弹药，无需特殊处理
            pass
        else:
            if 是否机甲武器 or 是否手枪 or 是否步枪 or 是否狙击枪 or 是否喷子 or 是否冲锋枪 or 是齐天武器 or '救世主' in 武器名称:
                # 机甲武器、手枪、步枪、狙击枪、喷子、冲锋枪、齐天武器使用物品实例的独立弹夹系统
                # 检查是否正在换弹
                if self.换弹中:
                    return
                
                # 从物品实例获取当前弹匣子弹数
                当前弹匣子弹 = 工具实例.获取属性("当前弹匣子弹", 当前工具.get("弹夹", 30))
                
                # 检查弹夹中是否有子弹
                if 当前弹匣子弹 <= 0:
                    # 弹夹为空，自动开始换弹
                    self._开始换弹()
                    return
                
                # 消耗弹夹中的子弹
                工具实例.设置属性("当前弹匣子弹", 当前弹匣子弹 - 1)
            else:
                # 其他武器直接使用背包弹药
                弹药数量 = self.背包管理器.获取物品总数量(弹药类型)
                
                if 弹药数量 <= 0:
                    # 显示需要弹药的提示
                    self._show_notification(f"需要<{弹药名称}>弹药")
                    return
                
                # 消耗一个弹药
                self.背包管理器.减少物品数量(弹药类型, 1)
        
        # 特殊处理救世主弩和救世主RPG：需要救世能源才能发射，消耗救世能源的耐久
        救世能源工具实例 = None
        if '救世主弩' in 武器名称 or '救世主RPG' in 武器名称:
            # 检查背包中是否有救世能源
            from 物品定义 import 物品 as 物品定义
            救世能源_id = 16097  # 救世能源的物品ID
            
            # 获取背包中所有救世能源的工具实例
            救世能源实例列表 = []
            # 遍历背包物品（5x6二维列表）
            for 行 in self.背包管理器.背包物品:
                for 背包格子 in 行:
                    if 背包格子:
                        物品_info = 物品定义.get(背包格子.物品_id, {})
                        if 物品_info.get('名称') == '救世能源':
                            救世能源实例列表.append(背包格子)
            # 遍历快捷栏物品
            for 背包格子 in self.背包管理器.快捷栏物品:
                if 背包格子:
                    物品_info = 物品定义.get(背包格子.物品_id, {})
                    if 物品_info.get('名称') == '救世能源':
                        救世能源实例列表.append(背包格子)
            
            # 检查是否有救世能源
            if not 救世能源实例列表:
                # 没有救世能源，显示提示
                self._show_notification("需要<救世能源>才能发射")
                return
            
            # 找到第一个有耐久的救世能源
            for 能源实例 in 救世能源实例列表:
                当前耐久 = 能源实例.获取属性("耐久", 能源实例.物品信息.get("最大耐久", 1000))
                if 当前耐久 > 0:
                    救世能源工具实例 = 能源实例
                    break
            
            # 检查是否找到可用的救世能源
            if not 救世能源工具实例:
                # 所有救世能源都没有耐久，显示提示
                self._show_notification("救世能源耐久不足")
                return
        
        # 消耗武器耐久度（未来弩、激光炮和龙息武器除外）
        if 工具实例 and not 是否未来弩 and not 是否激光炮 and not 是龙息武器:
            if '救世主弩' in 武器名称 or '救世主RPG' in 武器名称:
                # 救世主弩和RPG消耗救世能源的耐久，而不是自身耐久
                if 救世能源工具实例:
                    # 根据武器类型确定消耗的耐久度
                    消耗耐久 = 1 if '救世主弩' in 武器名称 else 10  # 救世主弩消耗1点，RPG消耗10点
                    能源损坏 = 救世能源工具实例.take_damage(消耗耐久)
                    # 如果救世能源损坏，显示提示并从背包中移除
                    if 能源损坏:
                        # 播放物品破碎音效
                        try:
                            audio_manager.play_sound("道具破碎")
                        except Exception as e:
                            print(f"播放破碎音效失败: {e}")
                        # 显示损坏通知
                        self._show_notification("救世能源 已耗尽")
                        
                        # 从背包中移除损坏的救世能源
                        for i, 背包格子 in enumerate(self.背包管理器.物品):
                            if 背包格子 == 救世能源工具实例:
                                self.背包管理器.物品[i] = None
                                break
                        for i, 快捷栏格子 in enumerate(self.背包管理器.快捷栏物品):
                            if 快捷栏格子 == 救世能源工具实例:
                                self.背包管理器.快捷栏物品[i] = None
                                break
            else:
                # 其他武器消耗自身耐久
                # 发射一次消耗1点耐久度
                武器损坏 = 工具实例.take_damage(1)
                # 如果武器损坏，显示提示并从快捷栏中移除
                if 武器损坏:
                    # 播放物品破碎音效
                    try:
                        audio_manager.play_sound("道具破碎")
                    except Exception as e:
                        print(f"播放破碎音效失败: {e}")
                    # 显示损坏通知
                    self._show_notification(f"{武器名称} 已损坏")
                    
                    # 手枪、步枪、狙击枪、喷子、机甲短枪和其他机甲武器损坏时弹出弹夹中剩余的子弹作为掉落物
                    if 是否手枪 or 是否步枪 or 是否狙击枪 or 是否喷子 or ('机甲短枪' in 武器名称) or 是否机甲武器:
                        # 获取弹夹中剩余的子弹数
                        剩余子弹数 = 工具实例.获取属性("当前弹匣子弹", 0)
                        if 剩余子弹数 > 0:
                            # 生成掉落物
                            from 物品定义 import 子弹, 机甲弹
                            # 根据武器类型选择掉落的弹药类型
                            掉落弹药类型 = 机甲弹 if 是否机甲武器 else 子弹
                            for _ in range(剩余子弹数):
                                # 计算掉落位置，在玩家前方
                                掉落_x = self.玩家.坐标_x + self.玩家.宽 // 2 + (30 if self.玩家.朝向右 else -50)
                                掉落_y = self.玩家.坐标_y + self.玩家.高 // 2
                                # 创建掉落物实体
                                掉落物 = ItemEntity(self.世界, 掉落_x, 掉落_y, 掉落弹药类型, 1)
                                # 设置掉落物的初始速度
                                掉落物.velocity_x = 3 if self.玩家.朝向右 else -3
                                掉落物.velocity_y = -2  # 向上抛出
                                # 将掉落物添加到世界的掉落物列表中
                                self.世界.items.append(掉落物)
                    
                    # 从快捷栏中移除损坏的武器
                    当前选中格子 = self.当前选中格子
                    if hasattr(self, '背包管理器') and 0 <= 当前选中格子 < len(self.背包管理器.快捷栏物品):
                        self.背包管理器.快捷栏物品[当前选中格子] = None
        
        # 计算箭矢发射方向
        鼠标_x, 鼠标_y = 鼠标位置
        世界_x = 鼠标_x + self.相机_x
        世界_y = 鼠标_y + self.相机_y
        
        # 玩家位置
        玩家_x = self.玩家.坐标_x + self.玩家.宽 // 2
        玩家_y = self.玩家.坐标_y + self.玩家.高 // 2
        
        # 计算方向向量
        dx = 世界_x - 玩家_x
        dy = 世界_y - 玩家_y
        
        # 默认伤害值
        伤害值 = 18  # 默认伤害
        
        # 如果有工具实例，尝试从工具获取伤害值
        if 工具实例:
            伤害值 = 工具实例.获取属性('伤害', 18)
        
        # 加上装备攻击力加成
        伤害值 += self.玩家.equipment_attack
        
        # 新机甲武器专属加成：伤害+20%
        if 是否机甲武器:
            伤害值 = int(伤害值 * 1.2)
        
        # 处理龙息系列武器的特殊激光效果 - 跟随鼠标的持续伤害激光
        if 是龙息武器:
            import math
            # 计算方向向量的单位向量
            magnitude = math.sqrt(dx*dx + dy*dy)
            if magnitude == 0:
                magnitude = 1
            unit_dx = dx / magnitude
            unit_dy = dy / magnitude
            
            # 设置龙息激光长度为600像素
            laser_length = 600
            
            # 龙息武器的伤害值
            龙息伤害 = 当前工具.get('龙息伤害', 10)
            
            # 计算激光终点
            laser_end_x = 玩家_x + unit_dx * laser_length
            laser_end_y = 玩家_y + unit_dy * laser_length
            
            # 检查激光路径上的方块，不可穿透方块
            实际终点_x = laser_end_x
            实际终点_y = laser_end_y
            
            # 分段检查方块碰撞
            step = 10  # 每10像素检查一次
            for i in range(1, int(laser_length / step) + 1):
                check_x = 玩家_x + unit_dx * i * step
                check_y = 玩家_y + unit_dy * i * step
                
                # 转换为方块坐标
                tile_x = int(check_x // 方块大小)
                tile_y = int(check_y // 方块大小)
                
                # 检查是否在世界范围内
                if 0 <= tile_y < self.世界.高度 and 0 <= tile_x < self.世界.宽度:
                    block_id = self.世界.get_block(tile_x, tile_y)
                    if block_id != 空气:
                        from 物品定义 import 方块属性
                        if 方块属性.get(block_id, {}).get("固体", False):
                            # 遇到固体方块，设置激光终点
                            实际终点_x = check_x
                            实际终点_y = check_y
                            break
            
            # 创建龙息激光效果对象
            class 龙息激光效果:
                def __init__(self, start_x, start_y, end_x, end_y, damage, color1, color2, owner, game):
                    self.start_x = start_x
                    self.start_y = start_y
                    self.end_x = end_x
                    self.end_y = end_y
                    self.damage = damage
                    self.color1 = color1  # 主要颜色
                    self.color2 = color2  # 次要颜色
                    self.owner = owner
                    self.game = game
                    self.lifetime = 0.1  # 激光持续时间
                    self.frame = 0  # 用于闪烁效果
                
                def update(self, dt):
                    # 更新激光状态
                    self.lifetime -= dt
                    self.frame += dt * 1  # 控制闪烁频率 - 进一步降低到1秒更新1次
                    return self.is_finished()
                
                def is_finished(self):
                    # 检查激光是否结束
                    return self.lifetime <= 0
                
                def draw(self, screen, camera_x, camera_y):
                    # 绘制龙息激光
                    screen_x1 = self.start_x - camera_x
                    screen_y1 = self.start_y - camera_y
                    screen_x2 = self.end_x - camera_x
                    screen_y2 = self.end_y - camera_y
                    
                    # 获取游戏实例的特效渲染设置
                    effect_setting = getattr(self.game, '特效渲染设置', "标准")
                    
                    # 计算当前颜色（闪烁效果）
                    if int(self.frame) % 2 == 0:
                        current_color = self.color1
                    else:
                        current_color = self.color2
                    
                    # 根据特效设置绘制不同质量的激光效果
                    if effect_setting == "最佳":
                        # 最佳特效：增强的多层彩色激光效果
                        import random
                        import math
                        
                        # 1. 绘制外层彩色光晕（动态效果）
                        for i in range(5):  # 增加到5层光晕
                            # 动态透明度和宽度
                            alpha = 200 - i * 35
                            width = 20 - i * 3
                            # 动态颜色变化
                            hue_shift = int(self.frame * 2)  # 随时间变化的色调偏移
                            r = (current_color[0] + hue_shift) % 256
                            g = (current_color[1] + hue_shift) % 256
                            b = (current_color[2] + hue_shift) % 256
                            glow_color = (r, g, b, alpha)
                            # 创建透明表面绘制光晕
                            glow_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                            pygame.draw.line(glow_surface, glow_color, 
                                          (screen_x1, screen_y1), (screen_x2, screen_y2), width)
                            screen.blit(glow_surface, (0, 0))
                        
                        # 2. 绘制主激光线（带内部渐变效果）
                        # 创建带渐变的激光表面
                        laser_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                        # 主激光线
                        pygame.draw.line(laser_surface, current_color, 
                                      (screen_x1, screen_y1), (screen_x2, screen_y2), 5)
                        # 激光内部高亮
                        pygame.draw.line(laser_surface, (255, 255, 255), 
                                      (screen_x1, screen_y1), (screen_x2, screen_y2), 2)
                        screen.blit(laser_surface, (0, 0))
                        
                        # 3. 添加粒子效果
                        particle_count = 15  # 粒子数量
                        for _ in range(particle_count):
                            # 计算粒子位置（沿激光线随机分布）
                            t = random.uniform(0, 1)
                            particle_x = screen_x1 + t * (screen_x2 - screen_x1)
                            particle_y = screen_y1 + t * (screen_y2 - screen_y1)
                            # 添加随机偏移，使粒子围绕激光线分布
                            offset = random.uniform(-10, 10)
                            angle = math.atan2(screen_y2 - screen_y1, screen_x2 - screen_x1) + math.pi / 2
                            particle_x += math.cos(angle) * offset
                            particle_y += math.sin(angle) * offset
                            # 随机粒子大小和透明度
                            particle_size = random.uniform(1, 4)
                            particle_alpha = random.randint(100, 255)
                            # 粒子颜色
                            particle_color = (current_color[0], current_color[1], current_color[2], particle_alpha)
                            # 绘制粒子
                            pygame.draw.circle(screen, particle_color, (int(particle_x), int(particle_y)), int(particle_size))
                        
                        # 4. 激光末端能量聚集效果
                        # 激光起点（玩家位置）的能量聚集
                        start_glow_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
                        for i in range(3):
                            radius = 30 - i * 10
                            alpha = 150 - i * 50
                            pygame.draw.circle(start_glow_surface, (*current_color, alpha), (30, 30), radius)
                        screen.blit(start_glow_surface, (screen_x1 - 30, screen_y1 - 30))
                        
                        # 激光终点的能量爆炸效果
                        end_glow_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
                        for i in range(4):
                            radius = 40 - i * 10
                            alpha = 200 - i * 40
                            pygame.draw.circle(end_glow_surface, (*current_color, alpha), (40, 40), radius)
                        screen.blit(end_glow_surface, (screen_x2 - 40, screen_y2 - 40))
                        
                        # 5. 能量流动效果（沿激光线移动的亮点）
                        flow_count = 3  # 流动亮点数量
                        for i in range(flow_count):
                            # 计算流动位置（随时间变化）
                            flow_t = (self.frame * 0.5 + i * 0.3) % 1
                            flow_x = screen_x1 + flow_t * (screen_x2 - screen_x1)
                            flow_y = screen_y1 + flow_t * (screen_y2 - screen_y1)
                            # 绘制流动亮点
                            pygame.draw.circle(screen, (255, 255, 255, 255), (int(flow_x), int(flow_y)), 4)
                            pygame.draw.circle(screen, current_color, (int(flow_x), int(flow_y)), 6, 2)
                    elif effect_setting == "标准":
                        # 标准特效：单层激光带简单光晕
                        # 创建透明表面绘制光晕
                        glow_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                        pygame.draw.line(glow_surface, (*current_color, 100), 
                                      (screen_x1, screen_y1), (screen_x2, screen_y2), 8)
                        screen.blit(glow_surface, (0, 0))
                        # 绘制主激光线
                        pygame.draw.line(screen, current_color, 
                                      (screen_x1, screen_y1), (screen_x2, screen_y2), 4)
                    else:  # 特效关闭时
                        # 特效关闭：绘制简单的白色激光线
                        pygame.draw.line(screen, (255, 255, 255), 
                                      (screen_x1, screen_y1), (screen_x2, screen_y2), 3)
                
                def check_damage(self, mobs):
                    # 检查激光对生物的伤害
                    import math
                    import time
                    
                    # 获取激光线段
                    x1, y1 = self.start_x, self.start_y
                    x2, y2 = self.end_x, self.end_y
                    
                    # 遍历所有生物
                    for mob in mobs:
                        # 跳过自己
                        if mob == self.owner:
                            continue
                        
                        # 生物中心坐标
                        mob_x = mob.x + mob.width // 2
                        mob_y = mob.y + mob.height // 2
                        
                        # 计算生物到激光线段的最短距离
                        dx = x2 - x1
                        dy = y2 - y1
                        
                        # 如果激光线段长度为0，直接计算距离
                        if dx == 0 and dy == 0:
                            distance = math.sqrt((mob_x - x1)**2 + (mob_y - y1)**2)
                        else:
                            t = max(0, min(1, ((mob_x - x1)*dx + (mob_y - y1)*dy) / (dx*dx + dy*dy)))
                            closest_x = x1 + t * dx
                            closest_y = y1 + t * dy
                            distance = math.sqrt((mob_x - closest_x)**2 + (mob_y - closest_y)**2)
                        
                        # 如果生物在激光范围内，造成伤害
                        if distance <= mob.width // 2 + 10:
                            # 获取当前时间
                            current_time = time.time()
                            
                            # 检查是否已经有伤害时间记录，如果没有则创建
                            if not hasattr(mob, 'last_damage_time_by_laser'):
                                mob.last_damage_time_by_laser = 0
                            
                            # 根据武器类型获取不同的伤害间隔
                            damage_interval = 0.15  # 默认间隔
                            if '龙息暗雷' in self.game.获取当前手持工具()[1].get('名称', ''):
                                damage_interval = 0.15
                            elif '龙息沧蓝' in self.game.获取当前手持工具()[1].get('名称', ''):
                                damage_interval = 0.20
                            elif '龙息蓝核' in self.game.获取当前手持工具()[1].get('名称', ''):
                                damage_interval = 0.25
                            
                            # 检查是否达到伤害间隔
                            if current_time - mob.last_damage_time_by_laser >= damage_interval:
                                mob.take_damage(self.damage)
                                mob.last_damage_time_by_laser = current_time
                                # 创建伤害文本
                                self.game.damage_texts.append(DamageText(mob.x + mob.width // 2, mob.y - 10, self.damage))
            
            # 获取龙息武器的色调
            龙息色调 = 当前工具.get('龙息色调', [(255, 255, 255), (255, 0, 0)])
            color1 = 龙息色调[0]
            color2 = 龙息色调[1]
            
            # 确保龙息激光效果列表存在
            if not hasattr(self, '龙息激光效果列表'):
                self.龙息激光效果列表 = []
            
            # 移除所有已结束的激光效果
            self.龙息激光效果列表 = [laser for laser in self.龙息激光效果列表 if not laser.is_finished()]
            
            # 只保留一个激光效果实例，实现跟随鼠标的效果
            if len(self.龙息激光效果列表) > 0:
                # 更新现有激光效果的位置和颜色
                龙息激光 = self.龙息激光效果列表[0]
                龙息激光.start_x = 玩家_x
                龙息激光.start_y = 玩家_y
                龙息激光.end_x = 实际终点_x
                龙息激光.end_y = 实际终点_y
                龙息激光.damage = 龙息伤害
                龙息激光.color1 = color1
                龙息激光.color2 = color2
                龙息激光.lifetime = 0.1  # 重置生命周期
            else:
                # 创建龙息激光效果
                龙息激光 = 龙息激光效果(玩家_x, 玩家_y, 实际终点_x, 实际终点_y, 龙息伤害, color1, color2, self.玩家, self)
                self.龙息激光效果列表.append(龙息激光)
            
            # 检查并伤害激光路径上的生物
            all_mobs = self.世界.mobs.copy()
            try:
                from boos生物处理 import boss_manager
                if boss_manager.current_boss and boss_manager.current_boss.is_alive():
                    all_mobs.append(boss_manager.current_boss)
            except Exception as e:
                pass
            龙息激光.check_damage(all_mobs)
            
            # 龙息武器不消耗耐久度
            
            # 播放射击音效（仅首次创建激光时播放）
            if len(self.龙息激光效果列表) == 1:
                try:
                    from 音频输出 import audio_manager
                    audio_manager.play_sound("射箭")
                except Exception as e:
                    print(f"播放射箭音效失败: {e}")
            
            # 更新冷却时间
            self.弓箭上次射击时间 = 当前时间
            return
            
            # 将龙息激光添加到游戏的激光效果列表中
            if not hasattr(self, '龙息激光效果列表'):
                self.龙息激光效果列表 = []
            self.龙息激光效果列表.append(龙息激光)
            
            # 检查龙息激光对生物的伤害
            all_mobs = self.世界.mobs.copy()
            # 添加当前boss到检查列表
            try:
                from boos生物处理 import boss_manager
                if boss_manager.current_boss and boss_manager.current_boss.is_alive():
                    all_mobs.append(boss_manager.current_boss)
            except Exception as e:
                pass
            
            龙息激光.check_damage(all_mobs)
            
            # 消耗武器耐久度
            if 工具实例:
                武器损坏 = 工具实例.take_damage(1)
                # 如果武器损坏，显示提示并从快捷栏中移除
                if 武器损坏:
                    try:
                        from 音频输出 import audio_manager
                        audio_manager.play_sound("道具破碎")
                    except Exception as e:
                        print(f"播放破碎音效失败: {e}")
                    self._show_notification(f"{武器名称} 已损坏")
                    # 从快捷栏中移除损坏的武器
                    当前选中格子 = self.当前选中格子
                    if hasattr(self, '背包管理器') and 0 <= 当前选中格子 < len(self.背包管理器.快捷栏物品):
                        self.背包管理器.快捷栏物品[当前选中格子] = None
            
            # 播放射击音效
            try:
                from 音频输出 import audio_manager
                audio_manager.play_sound("射箭")
            except Exception as e:
                print(f"播放射箭音效失败: {e}")
            
            # 更新冷却时间
            self.弓箭上次射击时间 = 当前时间
            return
        
        # 处理激光炮的特殊效果 - 瞬间破坏600像素内的方块和生物
        elif 是否激光炮:
            import math
            # 计算方向向量的单位向量
            magnitude = math.sqrt(dx*dx + dy*dy)
            if magnitude == 0:
                magnitude = 1
            unit_dx = dx / magnitude
            unit_dy = dy / magnitude
            
            # 设置激光长度为600像素
            laser_length = 600
            
            # 计算激光终点
            laser_end_x = 玩家_x + unit_dx * laser_length
            laser_end_y = 玩家_y + unit_dy * laser_length
            
            # 创建激光效果对象，用于绘制
            class LaserEffect:
                def __init__(self, start_x, start_y, end_x, end_y, damage, owner, game):
                    self.start_x = start_x
                    self.start_y = start_y
                    self.end_x = end_x
                    self.end_y = end_y
                    self.damage = damage
                    self.owner = owner
                    self.game = game
                    self.lifetime = 1.0  # 激光效果持续时间，停留1秒
                    
                    # 初始化时根据特效设置选择颜色，只选择一次，避免每秒变化
                    import random
                    self.color = (255, 255, 255)  # 默认白色
                    self.frame_count = 0  # 用于闪烁效果的帧计数器
                    effect_setting = getattr(self.game, '特效渲染设置', "标准")
                    
                    if effect_setting == "最佳":
                        # 最佳特效：使用更丰富的颜色组合
                        self.colors = [(255, 255, 255), (255, 0, 255), (0, 255, 255), (255, 255, 0), (255, 165, 0)]
                    elif effect_setting == "标准":
                        # 标准特效：从5种颜色中随机选择一种，固定使用
                        colors = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
                        self.color = random.choice(colors)
                    else:  # 关闭特效
                        # 关闭特效：固定为白色
                        self.color = (255, 255, 255)
                    
                def update(self, dt):
                    self.lifetime -= dt
                    self.frame_count += 1  # 增加帧计数器，用于闪烁效果
                    return self.lifetime <= 0
                
                def draw(self, screen, camera_x, camera_y):
                    # 获取游戏的特效渲染设置
                    effect_setting = getattr(self.game, '特效渲染设置', "标准")
                    
                    # 计算屏幕坐标
                    screen_x1 = self.start_x - camera_x
                    screen_y1 = self.start_y - camera_y
                    screen_x2 = self.end_x - camera_x
                    screen_y2 = self.end_y - camera_y
                    
                    # 根据特效设置绘制激光效果
                    if effect_setting == "最佳":
                        # 最佳特效：五彩缤纷的闪烁激光效果
                        # 确保colors属性存在，如果不存在则动态创建
                        if not hasattr(self, 'colors'):
                            self.colors = [(255, 255, 255), (255, 0, 255), (0, 255, 255), (255, 255, 0), (255, 165, 0)]
                        
                        # 添加闪烁效果：根据帧计数动态改变线宽和透明度
                        import random
                        flash_intensity = (self.frame_count % 5) / 4  # 0.0 到 1.0 之间的闪烁强度
                        
                        # 绘制多层彩色激光，每层有不同的颜色和动态线宽
                        for i in range(len(self.colors)):
                            color = self.colors[i]
                            # 动态线宽，随闪烁强度变化
                            base_width = 12 - i * 2
                            dynamic_width = max(2, int(base_width * (0.7 + flash_intensity * 0.3)))
                            
                            # 绘制主激光线
                            pygame.draw.line(screen, color, 
                                           (screen_x1, screen_y1), (screen_x2, screen_y2), dynamic_width)
                            
                            # 随机添加一些火花效果
                            if random.random() < 0.3:
                                # 将浮点数坐标转换为整数
                                min_x = int(min(screen_x1, screen_x2))
                                max_x = int(max(screen_x1, screen_x2))
                                min_y = int(min(screen_y1, screen_y2))
                                max_y = int(max(screen_y1, screen_y2))
                                
                                # 确保范围有效
                                if min_x <= max_x and min_y <= max_y:
                                    spark_x = random.randint(min_x, max_x)
                                    spark_y = random.randint(min_y, max_y)
                                    spark_size = random.randint(1, 3)
                                    pygame.draw.circle(screen, color, (spark_x, spark_y), spark_size)
                    elif effect_setting == "标准":
                        # 标准特效：使用固定的随机颜色
                        pygame.draw.line(screen, self.color, 
                                       (screen_x1, screen_y1), (screen_x2, screen_y2), 10)
                    else:  # 关闭特效
                        # 关闭特效：使用固定白色，简略效果
                        pygame.draw.line(screen, self.color, 
                                       (screen_x1, screen_y1), (screen_x2, screen_y2), 5)
            
            # 创建并添加激光效果
            laser = LaserEffect(玩家_x, 玩家_y, laser_end_x, laser_end_y, 伤害值, self.玩家, self)
            # 添加激光效果到游戏对象（需要确保游戏对象有laser_effects属性）
            if not hasattr(self, 'laser_effects'):
                self.laser_effects = []
            self.laser_effects.append(laser)
            
            # 瞬间破坏600像素内的所有方块
            # 计算激光线经过的所有方块
            # 使用Bresenham算法计算激光线经过的所有点
            def bresenham_line(x0, y0, x1, y1):
                points = []
                dx = abs(x1 - x0)
                dy = abs(y1 - y0)
                sx = 1 if x0 < x1 else -1
                sy = 1 if y0 < y1 else -1
                err = dx - dy
                
                while True:
                    points.append((x0, y0))
                    if x0 == x1 and y0 == y1:
                        break
                    e2 = 2 * err
                    if e2 > -dy:
                        err -= dy
                        x0 += sx
                    if e2 < dx:
                        err += dx
                        y0 += sy
                return points
            
            # 转换为方块坐标
            start_tile_x = int(玩家_x // 方块大小)
            start_tile_y = int(玩家_y // 方块大小)
            end_tile_x = int(laser_end_x // 方块大小)
            end_tile_y = int(laser_end_y // 方块大小)
            
            # 获取激光线经过的所有方块
            tiles = bresenham_line(start_tile_x, start_tile_y, end_tile_x, end_tile_y)
            
            # 破坏每个方块
            for tile_x, tile_y in tiles:
                # 检查方块是否在世界范围内
                if 0 <= tile_y < self.世界.高度 and 0 <= tile_x < self.世界.宽度:
                    block_id = self.世界.get_block(tile_x, tile_y)
                    if block_id != 空气:
                        # 破坏方块
                        self.世界.set_block(tile_x, tile_y, 空气)
                        # 生成掉落物
                        try:
                            from 掉落物 import 掉落物管理器实例
                            掉落物管理器实例.生成掉落物(self.世界, tile_x, tile_y, block_id)
                        except Exception as e:
                            print(f"生成掉落物失败: {e}")
            
            # 伤害600像素内的所有生物
            for mob in self.世界.mobs:
                # 计算生物到激光起点的距离
                mob_center_x = mob.x + mob.width // 2
                mob_center_y = mob.y + mob.height // 2
                
                # 计算生物到激光线的最短距离
                # 向量AB：激光线
                # 向量AP：从起点到生物
                AB = (laser_end_x - 玩家_x, laser_end_y - 玩家_y)
                AP = (mob_center_x - 玩家_x, mob_center_y - 玩家_y)
                
                # 计算AP在AB上的投影长度
                AB_length_squared = AB[0]**2 + AB[1]**2
                if AB_length_squared == 0:
                    # 激光线长度为0，直接计算距离
                    distance = math.hypot(mob_center_x - 玩家_x, mob_center_y - 玩家_y)
                else:
                    projection = (AP[0] * AB[0] + AP[1] * AB[1]) / AB_length_squared
                    projection = max(0, min(1, projection))  # 限制在0到1之间
                    
                    # 计算投影点
                    closest_x = 玩家_x + projection * AB[0]
                    closest_y = 玩家_y + projection * AB[1]
                    
                    # 计算生物到激光线的最短距离
                    distance = math.hypot(mob_center_x - closest_x, mob_center_y - closest_y)
                
                # 检查生物是否在激光范围内（距离<10像素，激光宽度）
                if distance < 10:
                    # 伤害生物
                    mob.game = self
                    死亡 = mob.take_damage(伤害值)
                    # 创建伤害文本
                    text_x = mob.x + mob.width // 2
                    text_y = mob.y - 10
                    self.damage_texts.append(DamageText(text_x, text_y, 伤害值))
                    
                    # 如果生物死亡，生成掉落物
                    if 死亡:
                        # 根据生物掉落物配置生成掉落物
                        try:
                            from 掉落物 import 掉落物管理器实例
                            from 生物系统 import 生物掉落物配置
                            掉落物管理器实例.生成生物掉落物(self.世界, 
                                                           int(mob.x // 方块大小), 
                                                           int(mob.y // 方块大小), 
                                                           mob.name, 
                                                           getattr(mob, 'mob_id', 0), 
                                                           生物掉落物配置)
                        except Exception as e:
                            print(f"生成生物掉落物失败: {e}")
                            # 备用方案
                            from 物品定义 import 肉块
                            self.世界.spawn_item(int(mob.x // 方块大小), int(mob.y // 方块大小), 肉块, random.randint(1, 3))
        else:
            # 检查是否是齐天系列武器
            是齐天武器 = '齐天' in 武器名称
            # 检查是否是齐天金箍棒（近战武器，不发射子弹）
            是齐天金箍棒 = '齐天金箍棒' in 武器名称
            
            # 检查是否是五子棋武器
            是否五子棋 = '五子棋' in 武器名称
            # 检查是否是救世主弩
            是否救世主弩 = '救世主弩' in 武器名称
            # 检查是否是救世主榴弹炮
            是否救世主榴弹炮 = '救世主榴弹炮' in 武器名称
            # 检查是否是救世主加特林
            是否救世主加特林 = '救世主加特林' in 武器名称
            
            # 创建箭矢或子弹对象，传递正确的伤害值和武器类型
            # 检查是否是救世主系列武器（除了弩和榴弹炮）
            是否救世主武器 = '救世主' in 武器名称 and not 是否救世主弩 and not 是否救世主榴弹炮
            weapon_type = '未来弩' if 是否未来弩 else ('rocket_launcher' if 是否火箭筒 or 是否救世主榴弹炮 else ('五子棋' if 是否五子棋 else ('bullet' if 是否手枪 or 是否步枪 or 是否狙击枪 or 是否喷子 or 是否冲锋枪 or 是否机甲武器 or (是齐天武器 and not 是齐天金箍棒) or 是否救世主加特林 or 是否救世主武器 else 'arrow')))
            
            # 计算原始方向的角度（弧度）
            import math
            original_angle = math.atan2(dy, dx)
            # 计算方向向量的大小
            magnitude = math.sqrt(dx*dx + dy*dy)
            
            # 特殊处理救世主弩：一次性发射3发子弹（3°、0°、-3°）
            if 是否救世主弩:
                # 救世主弩发射3发子弹，角度分别为3°、0°、-3°
                angle_deviations = [3, 0, -3]  # 以度为单位的角度偏差
                for dev_deg in angle_deviations:
                    # 将角度偏差转换为弧度
                    angle_deviation = dev_deg * math.pi / 180
                    new_angle = original_angle + angle_deviation
                    
                    # 计算新的方向向量
                    new_dx = math.cos(new_angle) * magnitude
                    new_dy = math.sin(new_angle) * magnitude
                    
                    # 创建箭对象，使用原始伤害值和武器类型
                    arrow = Arrow(玩家_x, 玩家_y, new_dx, new_dy, damage=伤害值, owner=self.玩家, weapon_type=weapon_type)
                    self.arrows.append(arrow)
                
                # 播放射箭音效
                try:
                    from 音频输出 import audio_manager
                    audio_manager.play_sound("射箭")
                except Exception as e:
                    pass
            # 手枪、步枪、狙击枪、喷子、冲锋枪、机甲武器、齐天系列武器（除了齐天金箍棒）、五子棋武器和所有救世主武器发射子弹时添加角度偏差
            elif 是否手枪 or 是否步枪 or 是否狙击枪 or 是否喷子 or 是否冲锋枪 or 是否机甲武器 or (是齐天武器 and not 是齐天金箍棒) or 是否五子棋 or 是否救世主加特林 or 是否救世主武器:
                import random
                
                # 根据武器类型设置不同的角度偏差和发射数量
                if 是否喷子 or ('机甲短枪' in 武器名称):
                    # 喷子和机甲短枪发射8颗子弹，每颗子弹有不同的角度偏差，模拟霰弹效果
                    子弹数量 = 8
                    for _ in range(子弹数量):
                        # 喷子和机甲短枪添加-20到+20度的随机角度偏差（转换为弧度），散射效果
                        angle_deviation = random.randint(-20, 20) * math.pi / 180
                        new_angle = original_angle + angle_deviation
                        
                        # 计算新的方向向量
                        new_dx = math.cos(new_angle) * magnitude
                        new_dy = math.sin(new_angle) * magnitude
                        
                        # 喷子和机甲短枪每颗子弹的伤害在3-8之间随机
                        喷子子弹伤害 = random.randint(3, 8)
                        
                        # 加上装备攻击力加成
                        喷子子弹伤害 += self.玩家.equipment_attack
                        
                        # 创建子弹对象，使用原始位置、新的方向向量和随机伤害
                        arrow = Arrow(玩家_x, 玩家_y, new_dx, new_dy, damage=喷子子弹伤害, owner=self.玩家, weapon_type=weapon_type)
                        self.arrows.append(arrow)
                else:
                    # 其他枪械发射单颗子弹
                    if 是否五子棋:
                        # 五子棋武器：使用武器定义中的偏差幅度属性
                        偏差幅度 = 当前工具.get("偏差幅度", 5)  # 从当前工具获取偏差幅度，默认5度
                        angle_deviation = random.randint(-偏差幅度, 偏差幅度) * math.pi / 180
                    elif 是否手枪:
                        # 使用武器定义中的偏差幅度属性
                        偏差幅度 = 当前工具.get("偏差幅度", 15)  # 从当前工具获取偏差幅度，默认15度
                        # 新机甲武器专属加成：射击幅度减少40%
                        if 是否机甲武器:
                            偏差幅度 = int(偏差幅度 * 0.6)
                        angle_deviation = random.randint(-偏差幅度, 偏差幅度) * math.pi / 180
                    elif 是否步枪:
                        # 使用武器定义中的偏差幅度属性
                        偏差幅度 = 当前工具.get("偏差幅度", 5)  # 从当前工具获取偏差幅度，默认5度
                        # 新机甲武器专属加成：射击幅度减少40%
                        if 是否机甲武器:
                            偏差幅度 = int(偏差幅度 * 0.6)
                        angle_deviation = random.randint(-偏差幅度, 偏差幅度) * math.pi / 180
                    elif 是否狙击枪:
                        # 狙击枪无角度偏差
                        angle_deviation = 0
                    elif 是否冲锋枪:
                        # 使用武器定义中的偏差幅度属性
                        偏差幅度 = 当前工具.get("偏差幅度", 5)  # 从当前工具获取偏差幅度，默认5度
                        # 新机甲武器专属加成：射击幅度减少40%
                        if 是否机甲武器:
                            偏差幅度 = int(偏差幅度 * 0.6)
                        angle_deviation = random.randint(-偏差幅度, 偏差幅度) * math.pi / 180
                    elif 是否机甲武器:
                        # 使用武器定义中的偏差幅度属性
                        偏差幅度 = 当前工具.get("偏差幅度", 10)  # 从当前工具获取偏差幅度，默认10度
                        # 新机甲武器专属加成：射击幅度减少40%
                        偏差幅度 = int(偏差幅度 * 0.6)
                        angle_deviation = random.randint(-偏差幅度, 偏差幅度) * math.pi / 180
                    elif 是齐天武器:
                        # 使用武器定义中的偏差幅度属性
                        偏差幅度 = 当前工具.get("偏差幅度", 10)  # 从当前工具获取偏差幅度，默认10度
                        # 添加-偏差幅度到+偏差幅度度的随机角度偏差（转换为弧度）
                        angle_deviation = random.randint(-偏差幅度, 偏差幅度) * math.pi / 180
                    elif 是否救世主加特林:
                        # 使用武器定义中的偏差幅度属性
                        偏差幅度 = 当前工具.get("偏差幅度", 12)  # 从当前工具获取偏差幅度，默认12度
                        # 添加-偏差幅度到+偏差幅度度的随机角度偏差（转换为弧度）
                        angle_deviation = random.randint(-偏差幅度, 偏差幅度) * math.pi / 180
                    elif 是否救世主武器:
                        # 所有其他救世主武器使用武器定义中的偏差幅度属性
                        偏差幅度 = 当前工具.get("偏差幅度", 5)  # 从当前工具获取偏差幅度，默认5度
                        # 添加-偏差幅度到+偏差幅度度的随机角度偏差（转换为弧度）
                        angle_deviation = random.randint(-偏差幅度, 偏差幅度) * math.pi / 180
                    else:
                        # 默认情况，无角度偏差
                        angle_deviation = 0
                    
                    new_angle = original_angle + angle_deviation
                    
                    # 计算新的方向向量
                    new_dx = math.cos(new_angle) * magnitude
                    new_dy = math.sin(new_angle) * magnitude
                    
                    # 创建子弹对象，使用原始位置和新的方向向量
                    arrow = Arrow(玩家_x, 玩家_y, new_dx, new_dy, damage=伤害值, owner=self.玩家, weapon_type=weapon_type)
                    self.arrows.append(arrow)
                    
                    # 播放射击音效
                    try:
                        from 音频输出 import audio_manager
                        if 是否救世主加特林 or 是否救世主武器:
                            audio_manager.play_sound("枪声5")  # 救世主枪械使用枪声5
                        else:
                            audio_manager.play_sound("射击")  # 其他枪械使用默认射击音效
                    except Exception as e:
                        pass
            else:
                # 其他远程武器发射单颗子弹
                arrow = Arrow(玩家_x, 玩家_y, dx, dy, damage=伤害值, owner=self.玩家, weapon_type=weapon_type)
                
                # 为火箭筒、救世主RPG和救世主榴弹炮设置爆炸属性
                if 是否火箭筒 or 是否救世主榴弹炮:
                    if 是否火箭筒:
                        if '救世主RPG' in 武器名称:
                            # 救世主RPG爆炸半径5方块（比火箭筒大30%，4 * 1.3 = 5.2，取整为5）
                            arrow.explosion_radius = 5
                        else:
                            # 普通火箭筒爆炸半径4方块
                            arrow.explosion_radius = 4
                    elif 是否救世主榴弹炮:
                        # 救世主榴弹炮爆炸半径2方块（比火箭筒小50%）
                        arrow.explosion_radius = 2
                        # 救世主榴弹炮子弹添加特殊标识，用于增强抛物线效果
                        arrow.is_savior_grenade = True
                    arrow.explosion_damage = 100  # 爆炸伤害
                    arrow.is_rocket = True  # 添加火箭弹标识
                
                self.arrows.append(arrow)
        
        # 机甲武器使用后有概率获得10点护盾，伤害高的枪越容易获得
        if 是否机甲武器 and 当前工具:
            import random
            # 获取武器伤害值
            weapon_damage = 工具实例.获取属性('伤害', 18) if 工具实例 else 18
            # 计算获得护盾的概率（伤害越高概率越高，范围0-100%）
            shield_probability = min(1.0, weapon_damage / 50.0)  # 伤害50时概率100%
            # 随机判断是否获得护盾
            if random.random() < shield_probability:
                # 为玩家添加10点护盾值，不超过最大护盾值
                self.玩家.current_shield = min(self.玩家.max_shield, self.玩家.current_shield + 10)
                # 显示获得护盾的提示
                self._show_notification("获得10点护盾")
        
        # 更新上次射击时间
        self.弓箭上次射击时间 = 当前时间
        
        # 播放射击音效
        from 音频输出 import audio_manager
        try:
            if 是否机甲武器 or 是否手枪 or 是否步枪 or 是否喷子 or 是否冲锋枪 or 是齐天武器 or 是否救世主加特林 or 是否救世主武器:
                # 救世主枪械使用枪声5，其他枪械使用相应的枪声
                if 是否救世主加特林 or 是否救世主武器:
                    audio_manager.play_sound("枪声5")  # 救世主枪械播放枪声5
                else:
                    audio_manager.play_sound("枪声1")  # 其他枪械播放枪声1
            elif 是否狙击枪:
                # 狙击枪播放指定的枪声2.mp3
                audio_manager.play_sound("枪声2")
            elif 是否激光炮:
                # 激光炮播放枪声4.mp3
                audio_manager.play_sound("枪声4")
            elif 是否火箭筒:
                # 火箭筒播放爆炸音效
                if '救世主RPG' in 武器名称:
                    audio_manager.play_sound("枪声5")  # 救世主RPG使用枪声5
                else:
                    audio_manager.play_sound("爆炸")  # 普通火箭筒使用爆炸音效
            elif 是否救世主榴弹炮:
                # 救世主榴弹炮使用枪声5
                audio_manager.play_sound("枪声5")
            elif 是否五子棋:
                # 五子棋播放弓箭发射音效
                audio_manager.play_sound("弓箭发射")
            else:
                # 其他远程武器播放弓箭发射音效
                audio_manager.play_sound("弓箭发射")
        except Exception as e:
            # 播放失败时尝试其他音效
            try:
                if 是否机甲武器 or 是否手枪 or 是否步枪 or 是否喷子 or 是否冲锋枪 or 是否激光炮 or 是否火箭筒 or 是齐天武器 or 是否救世主加特林:
                    audio_manager.play_sound("枪声2")
                else:
                    audio_manager.play_sound("射箭")
            except:
                pass
    
    def 攻击生物(self, 鼠标位置):
        """攻击生物 - 根据不同武器类型检测不同范围的生物"""
        # 获取当前手持工具，计算伤害和攻击范围
        工具实例, 当前工具 = self.获取当前手持工具()
        
        # 检查是否是火焰三叉戟且有buff
        是火焰三叉戟 = 当前工具 and 工具实例 and '火焰三叉戟' in 当前工具.get('名称', '')
        火焰三叉戟_buff = hasattr(self.玩家, '火焰三叉戟_buff_active') and self.玩家.火焰三叉戟_buff_active
        
        # 检查是否是闪电三叉戟且有buff
        是闪电三叉戟 = 当前工具 and 工具实例 and '闪电三叉戟' in 当前工具.get('名称', '')
        闪电三叉戟_buff = hasattr(self.玩家, '闪电三叉戟_buff_active') and self.玩家.闪电三叉戟_buff_active
        
        # 检查近战攻击间隔
        当前时间 = pygame.time.get_ticks() / 1000  # 转换为秒
        # 根据武器类型和buff状态设置攻击间隔
        攻击间隔 = self.玩家.近战攻击间隔  # 默认攻击间隔
        
        # 检查是否是齐天金箍棒
        是齐天金箍棒 = 当前工具 and '齐天金箍棒' in 当前工具.get('名称', '')
        
        # 初始化形态数据
        当前形态 = 0
        形态_攻击间隔 = 0.45
        形态_伤害 = 90
        形态_攻击范围 = 3
        
        if 是齐天金箍棒:
            # 导入形态数据
            from 武器处理 import 齐天金箍棒形态数据
            # 获取当前形态，默认0
            当前形态 = getattr(self.玩家, '齐天金箍棒形态', 0)
            # 获取当前形态的属性
            形态_攻击间隔 = 齐天金箍棒形态数据[当前形态][0]
            形态_伤害 = 齐天金箍棒形态数据[当前形态][1]
            形态_攻击范围 = 齐天金箍棒形态数据[当前形态][2]
            # 设置攻击间隔
            攻击间隔 = 形态_攻击间隔
        elif 是火焰三叉戟 and 火焰三叉戟_buff:
            攻击间隔 = 0.2  # 火焰三叉戟buff：0.2秒攻击间隔
        elif 是闪电三叉戟 and 闪电三叉戟_buff:
            攻击间隔 = 0.15  # 闪电三叉戟buff：0.15秒攻击间隔
        
        if 当前时间 - self.玩家.上次攻击时间 < 攻击间隔:
            return False  # 攻击间隔未到，无法攻击
        
        # 更新上次攻击时间
        self.玩家.上次攻击时间 = 当前时间
        
        # 设置攻击状态，用于播放攻击动画
        self.玩家.正在攻击 = True
        self.玩家.攻击动画时间 = 0
        
        # 计算玩家周围范围（根据武器类型确定范围）
        玩家方块_x = int(self.玩家.坐标_x // 方块大小)
        玩家方块_y = int(self.玩家.坐标_y // 方块大小)
        
        # 遍历所有生物，检测是否在范围内
        all_mobs = self.世界.mobs.copy()
        # 添加当前boss到检查列表
        try:
            from boos生物处理 import boss_manager
            if boss_manager.current_boss and boss_manager.current_boss.is_alive():
                all_mobs.append(boss_manager.current_boss)
        except Exception as e:
            pass
        
        命中生物 = False
        已攻击的幽灵 = []  # 用于记录已攻击的幽灵，避免重复攻击
        
        # 根据武器类型设置攻击范围
        # 空手: 1.5*1.5, 拿工具: 使用工具距离属性, 拿近战武器: 使用工具距离属性, 死神的镰刀: 3.5*3.5
        攻击范围 = 1.5  # 默认为空手范围
        
        if 当前工具 and 工具实例:
            武器名称 = 当前工具.get('名称', '')
            
            # 检查是否为齐天金箍棒
            if 是齐天金箍棒:
                # 使用形态攻击范围
                攻击范围 = 形态_攻击范围
            # 检查是否为死神的镰刀
            elif 工具实例.获取属性('伤害', 0) > 0 or '死神的镰刀' in 武器名称:
                攻击范围 = 3.5
            # 检查是否为火焰三叉戟且有buff
            elif 是火焰三叉戟 and 火焰三叉戟_buff:
                # 火焰三叉戟buff激活时，攻击范围提升到6*6
                攻击范围 = 6.0
            # 检查是否为闪电三叉戟且有buff
            elif 是闪电三叉戟 and 闪电三叉戟_buff:
                # 闪电三叉戟buff激活时，攻击范围提升到5*5
                攻击范围 = 5.0
            # 检查是否为近战武器（根据伤害属性判断）
            elif 工具实例.获取属性('伤害', 0) > 0:
                # 从物品属性中获取工具距离
                攻击范围 = 工具实例.获取属性('工具距离', 2.5)
            # 其他工具
            else:
                # 从物品属性中获取工具距离
                攻击范围 = 工具实例.获取属性('工具距离', 2.0)
        
        # 使用玩家的默认攻击力
        基础伤害 = self.玩家.base_attack  # 玩家默认攻击力5点
        
        if 当前工具 and 工具实例:
            # 有工具时，加上武器的攻击力
            武器伤害 = 工具实例.获取属性('伤害', 0)
            
            # 检查是否是电磁发射器
            是电磁发射器 = '电磁发射器' in 当前工具.get('名称', '')
            
            if 是齐天金箍棒:
                # 使用形态伤害
                武器伤害 = 形态_伤害
            elif 是电磁发射器:
                # 电磁发射器：随机10-23伤害
                import random
                武器伤害 = random.randint(10, 23)
            else:
                # 其他武器：根据buff状态调整伤害
                if 是火焰三叉戟 and 火焰三叉戟_buff:
                    武器伤害 *= 1.5  # 火焰三叉戟技能：+50%伤害（在已减少50%的基础上）
                elif 是闪电三叉戟 and 闪电三叉戟_buff:
                    武器伤害 *= 1.4  # 闪电三叉戟技能：+40%伤害（在已减少60%的基础上）
            
            基础伤害 += 武器伤害
        
        # 加上装备攻击力加成
        基础伤害 += self.玩家.equipment_attack
        
        # 播放近战攻击音效（只播放一次）
        from 音频输出 import audio_manager
        try:
            audio_manager.play_sound("近战攻击")
        except:
            pass
        
        # 导入math模块用于特效计算
        import math
        
        # 生成攻击特效
        玩家中心_x = self.玩家.坐标_x + self.玩家.宽 // 2
        玩家中心_y = self.玩家.坐标_y + self.玩家.高 // 2
        
        # 根据武器类型生成不同特效
        if 当前工具 and 工具实例:
            武器名称 = 当前工具.get('名称', '')
            
            # 获取玩家朝向
            玩家朝向右 = self.玩家.朝向右
            
            if 工具实例.获取属性('伤害', 0) > 0 or '死神的镰刀' in 武器名称:
                # 基础近战劈砍特效：蓝色彩色劈砍动画
                # 清空现有特效列表，强行结束之前的特效
                self.slash_effects = []
                
                # 彩色劈砍特效类
                class SwordSlashEffect:
                    def __init__(self, x, y, facing_right=True, flip_vertical=False, reverse_frames=False, weapon_name="", player=None, tool_instance=None):
                        self.x = x
                        self.y = y
                        self.facing_right = facing_right
                        self.flip_vertical = flip_vertical  # 控制是否上下镜像翻转
                        self.reverse_frames = reverse_frames  # 控制是否相反顺序播放帧
                        self.duration = 0.3  # 动画持续时间，从0.7秒改为0.3秒
                        self.lifetime = self.duration
                        self.frame = 0  # 当前帧
                        self.total_frames = 6  # 总帧数
                        self.frame_duration = self.duration / self.total_frames  # 每帧持续时间
                        self.frame_timer = 0  # 帧计时器初始化
                        self.size = 75  # 特效大小（放大到75x75像素，比原来小50%）
                        
                        # 暗黑系列武器列表
                        dark_weapons = [
                            "死神的镰刀", "骨刀", "骨弯刀", "超暗黑刺刀", "精美骨刀",
                            "亡灵斧头", "骨矛", "骨头狼牙棒", "尖锐骨头狼牙棒", "普通骨锤"
                        ]
                        
                        # 火焰系列武器列表
                        fire_weapons = [
                            "火焰斧头", "火焰三叉戟"
                        ]
                        
                        # 齐天金箍棒特殊处理
                        is_golden_cudgel = "齐天金箍棒" in weapon_name
                        
                        # 判断武器类型
                        is_dark_weapon = any(weapon in weapon_name for weapon in dark_weapons)
                        is_fire_weapon = any(weapon in weapon_name for weapon in fire_weapons)
                        
                        # 获取武器攻击距离
                        attack_range = tool_instance.获取属性('工具距离', 3.0) if tool_instance else 3.0  # 默认攻击距离为3.0
                        
                        # 根据武器类型选择特效图片前缀和颜色
                        if is_golden_cudgel:
                            prefix = "4劈砍"
                            color = "橙"
                            # 根据形态调整特效大小
                            # 从player对象获取当前形态
                            from 武器处理 import 齐天金箍棒形态数据
                            # 尝试获取当前形态，默认0
                            current_form = getattr(player, '齐天金箍棒形态', 0) if player and hasattr(player, '齐天金箍棒形态') else 0
                            # 根据形态调整特效大小
                            if current_form == 0:  # 形态1：正常形态
                                self.size = 75  # 标准大小
                            elif current_form == 1:  # 形态2：快速形态
                                self.size = 60  # 稍小
                            elif current_form == 2:  # 形态3：强力形态
                                self.size = 300  # 放大
                        elif is_dark_weapon:
                            prefix = "1劈砍"
                            color = "黑"
                            # 根据攻击距离调整特效大小
                            calculated_size = 75 + (attack_range - 3.0) * 30  # 基础大小75，每增加1攻击距离，大小增加30
                            self.size = max(64, calculated_size)  # 最小64像素
                        elif is_fire_weapon:
                            prefix = "3劈砍"
                            color = "红"
                            # 根据攻击距离调整特效大小
                            calculated_size = 75 + (attack_range - 3.0) * 30  # 基础大小75，每增加1攻击距离，大小增加30
                            self.size = max(64, calculated_size)  # 最小64像素
                        else:
                            prefix = "2劈砍"
                            color = "蓝"
                            # 根据攻击距离调整特效大小
                            calculated_size = 75 + (attack_range - 3.0) * 30  # 基础大小75，每增加1攻击距离，大小增加30
                            self.size = max(64, calculated_size)  # 最小64像素
                        
                        # 加载图片
                        from 图片加载 import 图片管理器
                        self.images = []
                        try:
                            # 尝试加载所有劈砍图片（带扩展名）
                            # 先尝试带扩展名的图片名
                            self.images.append(图片管理器.获取图片(f"{prefix}1{color}.png"))
                            self.images.append(图片管理器.获取图片(f"{prefix}1{color}.png"))
                            self.images.append(图片管理器.获取图片(f"{prefix}2{color}.png"))
                            self.images.append(图片管理器.获取图片(f"{prefix}3{color}.png"))
                            self.images.append(图片管理器.获取图片(f"{prefix}3{color}.png"))
                            self.images.append(图片管理器.获取图片(f"{prefix}3{color}.png"))
                            
                            # 检查是否有图片加载成功
                            if all(img is None for img in self.images):
                                # 如果带扩展名的图片加载失败，尝试不带扩展名的图片名
                                self.images = []
                                self.images.append(图片管理器.获取图片(f"{prefix}1{color}"))
                                self.images.append(图片管理器.获取图片(f"{prefix}1{color}"))
                                self.images.append(图片管理器.获取图片(f"{prefix}2{color}"))
                                self.images.append(图片管理器.获取图片(f"{prefix}3{color}"))
                                self.images.append(图片管理器.获取图片(f"{prefix}3{color}"))
                                self.images.append(图片管理器.获取图片(f"{prefix}3{color}"))
                                
                            # 打印图片加载结果
                            print(f"特效图片加载结果: {sum(1 for img in self.images if img is not None)}/{len(self.images)} 张图片加载成功")
                        except Exception as e:
                            # 如果图片加载失败，使用默认图片
                            self.images = [None] * self.total_frames
                            print(f"特效图片加载失败: {e}")
                    
                    def update(self, dt):
                        """更新特效状态，返回是否应该移除"""
                        self.lifetime -= dt
                        self.frame_timer += dt
                        
                        # 更新帧
                        if self.frame_timer >= self.frame_duration:
                            self.frame += 1
                            self.frame_timer = 0
                        
                        # 限制帧范围
                        self.frame = min(self.frame, self.total_frames - 1)
                        
                        # 返回是否应该移除（生命周期结束）
                        return self.lifetime <= 0
                    
                    def draw(self, screen, camera_x, camera_y):
                        """绘制劈砍特效"""
                        if not self.images or all(img is None for img in self.images):
                            return
                        
                        # 计算屏幕坐标
                        screen_x = self.x - camera_x
                        screen_y = self.y - camera_y
                        
                        # 获取当前帧索引，支持反向播放
                        if self.reverse_frames:
                            # 相反顺序播放帧
                            current_frame = self.total_frames - 1 - self.frame
                        else:
                            # 正常顺序播放帧
                            current_frame = self.frame
                        
                        # 获取当前帧图片
                        current_img = self.images[current_frame]
                        if current_img is None:
                            return
                        
                        # 调整图片大小
                        resized_img = pygame.transform.scale(current_img, (self.size, self.size))
                        
                        # 计算透明度
                        if self.frame == 0:
                            alpha = 0.7  # 70%透明度
                        elif self.frame == 1:
                            alpha = 1.0  # 100%透明度
                        elif self.frame == 2:
                            alpha = 1.0  # 100%透明度
                        elif self.frame == 3:
                            alpha = 1.0  # 100%透明度
                        elif self.frame == 4:
                            alpha = 0.7  # 70%透明度
                        else:  # frame == 5
                            alpha = 0.5  # 50%透明度
                        
                        # 创建一个更大的表面，确保旋转时有足够空间
                        max_size = int(self.size * math.sqrt(2))
                        temp_surface = pygame.Surface((max_size, max_size), pygame.SRCALPHA)
                        temp_surface.fill((0, 0, 0, 0))
                        
                        # 计算旋转角度（从上到下劈砍，总旋转90度，初始角度+40度）
                        rotation_progress = self.frame / (self.total_frames - 1)
                        total_rotation = 90  # 总旋转角度，从60度提高到90度
                        initial_offset = 40  # 初始偏移角度+40度
                        
                        # 根据玩家朝向和flip_vertical参数调整图片和旋转
                        if self.facing_right:
                            # 朝向右：
                            # 1. 根据flip_vertical决定是否上下镜像翻转
                            # 2. 根据flip_vertical决定旋转方向（第二段攻击旋转方向相反）
                            # 3. 旋转中心在图片左侧中点，对应玩家中心右侧
                            if self.flip_vertical:
                                final_img = pygame.transform.flip(resized_img, False, True)  # 上下镜像翻转
                                # 第二段攻击：顺时针旋转（与第一段相反）
                                rotation = rotation_progress * total_rotation + initial_offset  # 顺时针旋转+初始偏移
                            else:
                                final_img = resized_img  # 不翻转
                                # 第一段攻击：逆时针旋转
                                rotation = -rotation_progress * total_rotation + initial_offset  # 逆时针旋转+初始偏移
                            # 图片绘制在临时表面的右侧
                            blit_x = max_size - resized_img.get_width()
                            blit_y = (max_size // 2) - (resized_img.get_height() // 2)
                        else:
                            # 朝向左：
                            # 1. 左右翻转，根据flip_vertical决定是否上下镜像翻转
                            # 2. 根据flip_vertical决定旋转方向（第二段攻击旋转方向相反）
                            # 3. 旋转中心在图片右侧中点，对应玩家中心左侧
                            if self.flip_vertical:
                                final_img = pygame.transform.flip(resized_img, True, False)  # 左右翻转+不上下镜像翻转（第二段攻击不翻转）
                                # 第二段攻击：顺时针旋转（与第一段相反）
                                rotation = rotation_progress * total_rotation + initial_offset  # 顺时针旋转+初始偏移
                            else:
                                final_img = pygame.transform.flip(resized_img, True, True)  # 左右翻转+上下镜像翻转（第一段攻击翻转）
                                # 第一段攻击：逆时针旋转
                                rotation = -rotation_progress * total_rotation + initial_offset  # 逆时针旋转+初始偏移
                            # 图片绘制在临时表面的左侧
                            blit_x = 0
                            blit_y = (max_size // 2) - (resized_img.get_height() // 2)
                        
                        # 绘制图片到临时表面
                        temp_surface.blit(final_img, (blit_x, blit_y))
                        
                        # 旋转临时表面
                        rotated_surface = pygame.transform.rotate(temp_surface, rotation)
                        
                        # 应用透明度
                        rotated_surface.set_alpha(int(alpha * 255))
                        
                        # 计算绘制位置，使旋转中心更靠近玩家中心
                        rotated_rect = rotated_surface.get_rect()
                        
                        # 减小旋转中心与玩家中心的距离，让特效更靠拢玩家
                        offset = self.size // 4  # 从原来的size//2改为size//4，使特效更靠近玩家
                        
                        if self.facing_right:
                            # 朝向右：旋转中心在玩家中心右侧，但更靠近
                            rotation_center_x = screen_x + offset
                        else:
                            # 朝向左：旋转中心在玩家中心左侧，但更靠近
                            rotation_center_x = screen_x - offset
                        
                        rotation_center_y = screen_y
                        
                        # 旋转后表面的中心应该位于旋转中心位置
                        rotated_rect.center = (rotation_center_x, rotation_center_y)
                        
                        # 绘制到屏幕
                        screen.blit(rotated_surface, rotated_rect)
                
                # 初始化攻击计数，如果不存在
                if not hasattr(self, 'attack_count'):
                    self.attack_count = 0
                
                # 计算当前攻击模式
                flip_vertical = self.attack_count % 2 == 1  # 第2次攻击上下镜像翻转
                reverse_frames = self.attack_count % 2 == 1  # 第2次攻击帧数相反旋转播放
                
                # 创建并添加劈砍特效
                slash = SwordSlashEffect(玩家中心_x, 玩家中心_y, 玩家朝向右, flip_vertical, reverse_frames, 武器名称, self.玩家, 工具实例)
                self.slash_effects.append(slash)
                
                # 攻击计数递增
                self.attack_count += 1
                
                # 简化粒子效果，减少数量
                import random
                if not hasattr(self, 'particles'):
                    self.particles = []
                
                # 根据玩家朝向设置基础角度
                base_angle = 0 if 玩家朝向右 else 180
                
                for _ in range(3):  # 减少到3个粒子
                    angle = random.uniform(-60, 60) + base_angle
                    speed = random.uniform(2, 6)
                    particle = {
                        'x': 玩家中心_x,
                        'y': 玩家中心_y,
                        'vx': math.cos(math.radians(angle)) * speed,
                        'vy': math.sin(math.radians(angle)) * speed,
                        'life': 25,
                        'max_life': 25,
                        'size': 3,
                        'color': (255, 150, 50)
                    }
                    self.particles.append(particle)
        
        for mob in all_mobs:
            # 计算生物方块位置
            生物方块_x = int(mob.x // 方块大小)
            生物方块_y = int(mob.y // 方块大小)
            
            # 检查生物是否在玩家攻击范围内
            if abs(生物方块_x - 玩家方块_x) <= 攻击范围 and abs(生物方块_y - 玩家方块_y) <= 攻击范围:
                # 先检查生物是否有召唤的幽灵（如死神的灵魂护盾技能）
                if hasattr(mob, 'summoned_souls'):
                    for soul in mob.summoned_souls[:]:
                        # 检查幽灵是否已被攻击过
                        if soul in 已攻击的幽灵:
                            continue
                        
                        # 计算幽灵方块位置
                        幽灵方块_x = int(soul['x'] // 方块大小)
                        幽灵方块_y = int(soul['y'] // 方块大小)
                        
                        # 检查幽灵是否在范围内
                        if abs(幽灵方块_x - 玩家方块_x) <= 攻击范围 and abs(幽灵方块_y - 玩家方块_y) <= 攻击范围:
                            # 幽灵受到伤害
                            soul['health'] -= 基础伤害
                            
                            # 创建伤害文本
                            # 根据buff状态设置伤害颜色
                            if 是火焰三叉戟 and 火焰三叉戟_buff:
                                damage_color = (255, 0, 0)  # 火焰三叉戟：红色伤害文字
                            elif 是闪电三叉戟 and 闪电三叉戟_buff:
                                damage_color = (0, 0, 255)  # 闪电三叉戟：蓝色伤害文字
                            else:
                                damage_color = (255, 255, 0)  # 默认：黄色伤害文字
                            damage_text = DamageText(soul['x'] + soul['width'] // 2, soul['y'] - 10, 基础伤害, color=damage_color)
                            self.damage_texts.append(damage_text)
                            
                            # 标记为已攻击
                            已攻击的幽灵.append(soul)
                            命中生物 = True
                            
                            # 如果幽灵死亡，移除它
                            if soul['health'] <= 0:
                                mob.summoned_souls.remove(soul)
                
                # 攻击生物本身
                # 生物受到伤害
                死亡 = mob.take_damage(基础伤害)
                
                # 创建伤害文本
                # 根据buff状态设置伤害颜色
                if 是火焰三叉戟 and 火焰三叉戟_buff:
                    damage_color = (255, 0, 0)  # 火焰三叉戟：红色伤害文字
                elif 是闪电三叉戟 and 闪电三叉戟_buff:
                    damage_color = (0, 0, 255)  # 闪电三叉戟：蓝色伤害文字
                else:
                    damage_color = (255, 255, 0)  # 默认：黄色伤害文字
                damage_text = DamageText(mob.x + mob.width // 2, mob.y - 10, 基础伤害, color=damage_color)
                self.damage_texts.append(damage_text)
                
                # 检查是否是电磁发射器，添加额外伤害
                if 当前工具 and 工具实例 and '电磁发射器' in 当前工具.get('名称', ''):
                    # 电磁发射器：0.2秒后造成5-9点额外伤害
                    import random
                    额外伤害 = random.randint(5, 9)
                    
                    # 创建延迟伤害事件
                    if not hasattr(self, 'timed_damage_events'):
                        self.timed_damage_events = {}
                    
                    event_id = pygame.time.get_ticks() + 200  # 200毫秒后触发
                    self.timed_damage_events[event_id] = {
                        'mob': mob,
                        'damage': 额外伤害,
                        'color': (0, 255, 255)  # 青色伤害文字
                    }
                
                # 通知所有召唤的死神祝福攻击这个生物
                handle_player_attack(mob, 武器技能管理器实例)
                
                命中生物 = True
                
                # 如果生物死亡，生成掉落物和经验
                if 死亡:
                    # 根据生物掉落物配置生成掉落物
                    try:
                        from 掉落物 import 掉落物管理器实例
                        from 生物系统 import 生物掉落物配置
                        掉落物管理器实例.生成生物掉落物(self.世界, 
                                                       int(mob.x // 方块大小), 
                                                       int(mob.y // 方块大小), 
                                                       mob.name, 
                                                       getattr(mob, 'mob_id', 0), 
                                                       生物掉落物配置)
                    except Exception as e:
                        print(f"生成生物掉落物失败: {e}")
                        # 备用方案
                        from 物品定义 import 肉块
                        self.世界.spawn_item(int(mob.x // 方块大小), int(mob.y // 方块大小), 肉块, random.randint(1, 3))
                    # 生成经验球
                    self.spawn_exp_orbs(mob.x // 方块大小, mob.y // 方块大小)
        
        # 每次攻击都消耗武器耐久度
        if 工具实例 and hasattr(工具实例, 'take_damage'):
            # 攻击一次消耗1点耐久
            damage_amount = 1
            is_broken = 工具实例.take_damage(damage_amount)
            # 如果工具损坏
            if is_broken:
                # 播放物品破碎音效
                try:
                    audio_manager.play_sound("道具破碎")
                except Exception as e:
                    print(f"播放破碎音效失败: {e}")
                # 从快捷栏中移除损坏的物品
                当前选中格子 = self.当前选中格子
                if hasattr(self, '背包管理器') and 0 <= 当前选中格子 < len(self.背包管理器.快捷栏物品):
                    # 获取武器名称
                    武器名称 = 当前工具.get('名称', '武器')
                    # 显示损坏通知
                    self._show_notification(f"{武器名称} 已损坏")
                    # 从快捷栏移除
                    self.背包管理器.快捷栏物品[当前选中格子] = None
        
        return 命中生物  # 返回是否命中任何生物
    
    def 更新挖掘进度(self, 时间增量):
        """更新挖掘进度"""
        if not self.正在挖掘 or not self.挖掘位置:
            return
        
        方块_x, 方块_y = self.挖掘位置
        方块_id = self.当前挖掘方块
        
        # 特殊处理：水方块不可挖掘
        if 方块_id == "水":
            self.停止挖掘()
            return
        
        # 获取当前手持工具（无论是否秒挖掘都需要获取，用于后续工具耐久度减少）
        工具实例, 当前工具 = self.获取当前手持工具()
        
        # 获取方块信息
        方块信息 = 方块属性.get(方块_id, {})
        方块名称 = 方块信息.get("名称", "")
        不可破坏 = 方块信息.get("不可破坏", False)
        
        # 检查是否可以挖掘：不可破坏的方块只有在玩家有最高权限时才能挖掘
        if 不可破坏 and not self.has_max_permission:
            # 不可破坏的方块，直接停止挖掘
            self.停止挖掘()
            return
        
        # 秒挖掘处理：如果开启秒挖掘，直接设置进度为1.0
        if self.is_instant_dig:
            self.挖掘进度 = 1.0
        else:
            # 获取方块硬度
            硬度 = 方块信息.get("硬度", 1.0)  # 默认硬度为1.0
            
            # 计算挖掘时间（基于硬度）
            基础挖掘时间 = 1.0  # 基础挖掘时间1秒
            总挖掘时间 = 基础挖掘时间 * 硬度
            
            # 初始化挖掘加成：空手固定1.0
            挖掘加成 = 1.0
            
            # 如果有工具且工具实例有效
            if 当前工具 and 工具实例:
                工具名称 = 当前工具.get('名称', '')
                挖掘效率值 = 当前工具.get('挖掘效率', 1.0)
                
                # 根据工具类型和方块类型判断是否为正确工具
                正确工具 = False
                
                if '镐' in 工具名称:
                    # 镐类工具对矿石、石头、方块类有加成
                    if any(类型 in 方块名称 for 类型 in ['岩石', '矿石', '块', '红石', '蓝石', '紫石', '熔炉', '煤矿', '铁矿石', '金矿石', '钻石矿石', '铜矿石', '红矿石', '蓝矿石', '金块', '铁块', '钻石块', '铜块', '红方块', '蓝方块', '煤块', '紫石块', '玻璃', '岩石底']):
                        正确工具 = True
                elif '斧' in 工具名称:
                    # 斧类工具对木材、树叶、植物、家具类方块有加成
                    if any(类型 in 方块名称 for 类型 in ['木头', '乔木', '木板', '树叶', '仙人掌', '灌木', '乔木叶', '床左', '床右', '床整体', '工作台']):
                        正确工具 = True
                elif '铲' in 工具名称:
                    # 铲类工具对泥土、沙子、草类方块有加成
                    if any(类型 in 方块名称 for 类型 in ['土块', '沙子', '泥土', '草方块', '黑土块', '枯草', '草', '红花']):
                        正确工具 = True
                
                # 只有正确工具才获得挖掘效率加成
                if 正确工具:
                    # 正确工具：挖掘加成 = 1.0 + (挖掘效率值 × 1.0)
                    挖掘加成 = 1.0 + (挖掘效率值 * 1.0)
                else:
                    # 错误工具：挖掘加成 = 1.0
                    挖掘加成 = 1.0
            
            # 应用挖掘加成
            总挖掘时间 /= 挖掘加成
            
            # 防止除以零错误
            if 总挖掘时间 <= 0:
                总挖掘时间 = 0.1
            
            # 计算当前进度
            当前时间 = time.time()
            已挖掘时间 = 当前时间 - self.挖掘开始时间
            self.挖掘进度 = min(已挖掘时间 / 总挖掘时间, 1.0)
        
        # 检查是否挖掘完成
        if self.挖掘进度 >= 1.0:
            # 计算挖掘完成时间
            挖掘完成时间 = time.time()
            挖掘耗时 = 挖掘完成时间 - self.挖掘开始时间
            
            # 获取挖掘工具名称
            挖掘工具名称 = "空手"
            if 当前工具:
                挖掘工具名称 = 当前工具.get('名称', '未知工具')
            
            # 输出挖掘信息到终端
            print(f"[挖掘完成] 挖掘工具: {挖掘工具名称}, 挖掘完成时间: {挖掘耗时:.2f}秒")
            
            self.破坏方块(方块_x, 方块_y)
            # 挖掘完成后减少工具耐久度
            if 工具实例 and hasattr(工具实例, 'take_damage'):
                # 每次挖掘固定减少1点耐久
                damage_amount = 1
                is_broken = 工具实例.take_damage(damage_amount)
                # 如果工具损坏
                if is_broken:
                    # 播放物品破碎音效
                    try:
                        audio_manager.play_sound("道具破碎")
                    except Exception as e:
                        print(f"播放破碎音效失败: {e}")
                    # 从快捷栏中移除损坏的物品
                    if hasattr(self, '背包管理器'):
                        当前选中格子 = self.当前选中格子
                        if 0 <= 当前选中格子 < len(self.背包管理器.快捷栏物品):
                            self.背包管理器.快捷栏物品[当前选中格子] = None
            self.停止挖掘()
    
    def 破坏方块(self, x, y):
        """破坏方块"""
        # 定义要破坏的方块坐标列表
        blocks_to_destroy = []
        
        # 检查是否启用了3*3范围挖掘
        if self.enable_3x3_dig:
            # 3*3范围挖掘：以目标位置为中心，破坏周围3x3区域的方块
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    # 边界检查 - 兼容无限世界
                    if (self.世界.无限世界 and 0 <= ny < self.世界.高度) or (not self.世界.无限世界 and 0 <= nx < self.世界.宽度 and 0 <= ny < self.世界.高度):
                        # 使用get_block方法获取方块，兼容无限世界
                        方块_id = self.世界.get_block(nx, ny)
                        # 跳过空气和水方块
                        if 方块_id != 空气 and 方块_id != "水":
                            方块信息 = 方块属性.get(方块_id, {})
                            # 检查是否可以破坏
                            if self.创造模式 or not 方块信息.get("不可破坏", False) or self.has_max_permission:
                                blocks_to_destroy.append((nx, ny, 方块_id, 方块信息))
        else:
            # 普通挖掘：只破坏目标位置的方块
            # 边界检查 - 兼容无限世界
            if (self.世界.无限世界 and 0 <= y < self.世界.高度) or (not self.世界.无限世界 and 0 <= x < self.世界.宽度 and 0 <= y < self.世界.高度):
                # 使用get_block方法获取方块，兼容无限世界
                方块_id = self.世界.get_block(x, y)
                方块信息 = 方块属性.get(方块_id, {})
                方块名称 = 方块信息.get("名称", "")
                
                # 特殊方块处理：水方块不可破坏
                if 方块_id != "水":
                    # 如果是创造模式、方块不是不可破坏的，或者玩家有最高权限
                    if self.创造模式 or not 方块信息.get("不可破坏", False) or self.has_max_permission:
                        blocks_to_destroy.append((x, y, 方块_id, 方块信息))
        
        # 破坏所有选中的方块
        if blocks_to_destroy:
            # 播放一次破坏方块音效
            try:
                from 音频输出 import audio_manager
                audio_manager.play_sound("破坏方块")
            except Exception as e:
                print(f"播放破坏音效失败: {e}")
            
            # 破坏每个方块
            for nx, ny, 方块_id, 方块信息 in blocks_to_destroy:
                # 替换为空气 - 兼容无限世界
                self.世界.set_block(nx, ny, 空气)
                
                # 使用掉落物管理器生成掉落物
                try:
                    from 掉落物 import 掉落物管理器实例
                    掉落物管理器实例.生成掉落物(self.世界, nx, ny, 方块_id)
                except Exception as e:
                    print(f"生成掉落物失败: {e}")
                    # 备用掉落物生成逻辑
                    try:
                        from 掉落物 import DropItem
                        新的掉落物 = DropItem(nx * 方块大小 + 方块大小 // 2, ny * 方块大小 + 方块大小 // 2, 方块_id, 1)
                        if hasattr(self.世界, 'items'):
                            self.世界.items.append(新的掉落物)
                    except:
                        pass
                
                # 生成经验小球（只有矿石才会掉落）
                方块名称 = 方块信息.get("名称", "")
                if '矿石' in 方块名称 or 方块_id in ['煤矿', '铁矿石', '金矿石', '钻石矿石', '铜矿石', '红矿石', '蓝矿石']:
                    self.spawn_exp_orbs(nx, ny)
                
    def spawn_exp_orbs(self, x, y):
        """
        在指定坐标生成经验小球
        """
        # 计算生成位置
        orb_x = x * 方块大小 + random.randint(8, 24)
        orb_y = y * 方块大小 + random.randint(8, 24)
        
        # 决定生成哪种经验球
        rand = random.random()
        if rand < 0.2:  # 20%概率生成金色经验球
            if hasattr(self.世界, 'exp_orbs'):
                self.世界.exp_orbs.append(ExpOrb(self.世界, orb_x, orb_y, 'gold'))
        elif rand < 0.4:  # 20%概率生成蓝色经验球
            if hasattr(self.世界, 'exp_orbs'):
                self.世界.exp_orbs.append(ExpOrb(self.世界, orb_x, orb_y, 'blue'))
        elif rand < 0.6:  # 20%概率生成绿色经验球
            if hasattr(self.世界, 'exp_orbs'):
                self.世界.exp_orbs.append(ExpOrb(self.世界, orb_x, orb_y, 'green'))
    
    def 绘制挖掘进度条(self, 相机_x, 相机_y):
        """绘制挖掘进度条"""
        if not self.正在挖掘 or not self.挖掘位置:
            return
        
        方块_x, 方块_y = self.挖掘位置
        
        # 计算屏幕上的绘制位置
        绘制_x = 方块_x * 方块大小 - 相机_x
        绘制_y = 方块_y * 方块大小 - 相机_y - 10  # 进度条在方块上方
        
        # 绘制进度条背景
        pygame.draw.rect(self.屏幕, (0, 0, 0), (绘制_x, 绘制_y, 方块大小, 5))
        
        # 检查是否使用了正确的工具
        使用正确工具 = False
        if hasattr(self, '当前挖掘方块'):
            方块_id = self.当前挖掘方块
            方块信息 = 方块属性.get(方块_id, {})
            方块名称 = 方块信息.get("名称", "")
            
            # 获取当前手持工具
            工具实例, 当前工具 = self.获取当前手持工具()
            if 当前工具:
                工具名称 = 当前工具.get('名称', '')
                
                # 判断工具是否适合当前方块
                if '镐' in 工具名称 and any(类型 in 方块名称 for 类型 in ['岩石', '矿石', '块']):
                    使用正确工具 = True
                elif '斧' in 工具名称 and any(类型 in 方块名称 for 类型 in ['木头', '乔木', '木板']):
                    使用正确工具 = True
                elif '铲' in 工具名称 and any(类型 in 方块名称 for 类型 in ['土块', '沙子', '泥土']):
                    使用正确工具 = True
        
        # 根据是否使用正确工具和挖掘进度设置进度条颜色
        if 使用正确工具:
            # 使用正确工具时，颜色从绿色逐渐变为金色
            if self.挖掘进度 < 0.33:
                进度条颜色 = (0, 255, 0)  # 绿色
            elif self.挖掘进度 < 0.66:
                进度条颜色 = (255, 255, 0)  # 黄色
            else:
                进度条颜色 = (255, 215, 0)  # 金色
        else:
            # 使用错误工具时，颜色从红色逐渐变为白色
            if self.挖掘进度 < 0.33:
                进度条颜色 = (255, 0, 0)  # 红色
            elif self.挖掘进度 < 0.66:
                进度条颜色 = (255, 128, 0)  # 橙色
            else:
                进度条颜色 = (255, 255, 255)  # 白色
        
        # 绘制进度条
        进度宽度 = int(方块大小 * self.挖掘进度)
        pygame.draw.rect(self.屏幕, 进度条颜色, (绘制_x, 绘制_y, 进度宽度, 5))
        
        # 绘制一个边框高亮正在挖掘的方块
        pygame.draw.rect(self.屏幕, 进度条颜色, 
                        (绘制_x, 绘制_y + 10, 方块大小, 方块大小), 2)

def start_game(世界参数, screen=None):
    """从创建世界界面启动游戏的入口函数"""
    # 创建并运行游戏实例，传递屏幕参数实现统一窗口
    游戏实例 = Game(世界参数, screen=screen)
    游戏实例.run()

# 直接运行此文件时的测试代码
if __name__ == "__main__":
    # 测试用的默认参数
    default_params = {
        '存档名称': '测试世界',
        '世界宽度': 2000,
        '世界高度': 100,
        '世界类型': '随机世界',
        '创造模式': True,
        '创建存档': False,
        '无限世界': False,
    }
    print(f"测试参数 - 无限世界: {default_params['无限世界']}")
    start_game(default_params)