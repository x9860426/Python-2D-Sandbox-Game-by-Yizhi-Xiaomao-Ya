import pygame
import sys

# 物品类，支持存储多种变量（如耐久等）
class 物品:
    """物品类，用于背包系统中的物品表示"""
    def __init__(self, 物品_id, 数量=1, **kwargs):
        self.物品_id = 物品_id
        self.数量 = 数量
        # 从物品定义获取信息
        from 物品定义 import 物品 as 物品定义
        self.物品信息 = 物品定义.get(物品_id, {})
        # 存储额外变量（如耐久等）
        self.额外属性 = kwargs
        
        # 初始化耐久度
        self._初始化耐久度()
        
        # 为手枪、步枪、狙击枪、喷子、冲锋枪和机甲系列武器添加弹匣属性
        物品名称 = self.物品信息.get("名称", "")
        if "手枪" in 物品名称 or "步枪" in 物品名称 or "狙击枪" in 物品名称 or "喷子" in 物品名称 or "冲锋枪" in 物品名称 or "机甲" in 物品名称:
            # 从物品定义获取弹匣容量
            弹匣容量 = self.物品信息.get("弹夹", 0)
            # 如果额外属性中没有指定当前弹匣子弹数量，默认设置为满弹夹
            if "当前弹匣子弹" not in self.额外属性:
                self.额外属性["当前弹匣子弹"] = 弹匣容量
            # 保存弹匣容量到额外属性
            self.额外属性["弹匣容量"] = 弹匣容量
    
    def _初始化耐久度(self):
        """初始化物品的耐久度属性"""
        # 首先检查是否直接设置了耐久度属性（用于无限耐久武器）
        direct_durability = self.物品信息.get("耐久度", 0)
        if direct_durability > 0:
            # 直接使用物品定义中的耐久度属性
            max_durability = direct_durability
        else:
            # 从物品信息获取最大耐久度
            max_durability = self.物品信息.get("最大耐久", 0)
            
            # 如果物品信息中没有最大耐久度，根据物品类型和品质设置
            if max_durability == 0:
                物品名称 = self.物品信息.get("名称", "")
                物品类型 = self.物品信息.get("类型", "")
                
                # 根据物品类型和名称中的品质词设置耐久度
                if 物品类型 in ["weapon", "pickaxe", "axe", "shovel", "剑", "镐", "斧", "铲"] or any(工具 in 物品名称 for 工具 in ["弓", "弩", "手枪", "狙击枪"]):
                    # 木品质
                    if "木" in 物品名称:
                        max_durability = 25
                    # 石品质
                    elif "石" in 物品名称:
                        max_durability = 50
                    # 铜品质
                    elif "铜" in 物品名称:
                        max_durability = 75
                    # 铁品质
                    elif "铁" in 物品名称:
                        max_durability = 100
                    # 金品质
                    elif "金" in 物品名称:
                        max_durability = 150
                    # 钻石品质
                    elif "钻石" in 物品名称:
                        max_durability = 200
                    # 特殊武器
                    elif "弓" in 物品名称:
                        max_durability = 100
                    elif "弩" in 物品名称:
                        max_durability = 250
                    elif "手枪" in 物品名称:
                        max_durability = 250
                    elif "步枪" in 物品名称:
                        max_durability = 750
                    elif "狙击枪" in 物品名称:
                        max_durability = 75
        
        # 如果有最大耐久度，设置当前耐久度
        if max_durability > 0:
            # 如果额外属性中没有指定当前耐久度，默认设置为最大耐久度
            if "当前耐久度" not in self.额外属性:
                self.额外属性["当前耐久度"] = max_durability
            # 保存最大耐久度到额外属性
            self.额外属性["耐久度"] = max_durability
        
        # 为手枪和冲锋枪添加弹匣属性
        物品名称 = self.物品信息.get("名称", "")
        if "手枪" in 物品名称:
            # 如果额外属性中没有指定当前弹匣子弹数量，默认设置为0发
            if "当前弹匣子弹" not in self.额外属性:
                self.额外属性["当前弹匣子弹"] = 0
            # 保存弹匣容量到额外属性
            self.额外属性["弹匣容量"] = 15
        elif "冲锋枪" in 物品名称:
            # 如果额外属性中没有指定当前弹匣子弹数量，默认设置为0发
            if "当前弹匣子弹" not in self.额外属性:
                self.额外属性["当前弹匣子弹"] = 0
            # 保存弹匣容量到额外属性
            self.额外属性["弹匣容量"] = 25
    
    def 获取名称(self):
        """获取物品名称"""
        return self.物品信息.get("名称", "未知物品")
    
    def 获取最大堆叠(self):
        """获取物品最大堆叠数量"""
        return self.物品信息.get("堆叠上限", 99)
    
    def 可以堆叠(self, 其他物品):
        """检查是否可以与其他物品堆叠"""
        return self.物品_id == 其他物品.物品_id and self.数量 < self.获取最大堆叠()
    
    def 获取属性(self, 属性名, 默认值=None):
        """获取物品的属性，先检查额外属性，再检查物品信息"""
        # 先从额外属性中获取
        if 属性名 in self.额外属性:
            return self.额外属性[属性名]
        # 再从物品信息中获取
        if 属性名 in self.物品信息:
            return self.物品信息[属性名]
        # 如果都没有，返回默认值
        return 默认值
    
    def 设置属性(self, 属性名, 值):
        """设置物品的额外属性"""
        self.额外属性[属性名] = 值
    
    def 获取颜色(self):
        """获取物品颜色"""
        return self.物品信息.get("颜色", (200, 200, 200))
    
    def 获取图像(self, 尺寸=None):
        """获取物品图像，使用图片加载模块加载"""
        try:
            from 图片加载 import 图片管理器
            return 图片管理器.获取物品图片(self.物品_id, 尺寸)
        except ImportError:
            print("错误: 无法导入图片加载模块")
        except Exception as e:
            print(f"获取物品图像失败: {e}")
        return None
    
    def 拆分一半(self):
        """拆分一半物品，返回新物品实例"""
        if self.数量 <= 1:
            return None  # 无法再拆分
        一半 = self.数量 // 2
        self.数量 -= 一半
        return 物品(self.物品_id, 一半)
    
    def 增加数量(self, 数量):
        """增加物品数量，返回实际增加的数量"""
        剩余空间 = self.获取最大堆叠() - self.数量
        实际增加 = min(数量, 剩余空间)
        self.数量 += 实际增加
        return 实际增加
    
    def take_damage(self, damage_amount=1):
        """处理物品耐久度消耗
        
        参数:
            damage_amount: 消耗的耐久度
            
        返回:
            bool: 如果物品损坏返回True，否则返回False
        """
        max_durability = self.获取属性("耐久度", 0)
        if max_durability <= 0:
            return False
        
        current_durability = self.获取属性("当前耐久度", max_durability)
        new_durability = current_durability - damage_amount
        
        # 更新当前耐久度
        self.设置属性("当前耐久度", new_durability)
        
        # 检查物品是否损坏
        if new_durability <= 0:
            return True
        
        return False

# 背包管理器类
class 背包管理器:
    """背包管理器，处理背包的显示、交互和物品管理"""
    def __init__(self, 游戏):
        self.游戏 = 游戏
        self.是否打开 = False
        
        # UI尺寸参数
        self.宽度 = 500  # 页面宽度
        self.高度 = 450  # 页面高度
        
        # 物品槽相关参数
        self.物品槽大小 = 44  # 物品槽大小
        self.物品槽间距 = 5  # 物品槽间距
        self.物品槽边框宽度 = 1  # 物品槽边框宽度
        self.物品槽边框颜色 = (150, 150, 150)  # 物品槽边框颜色
        
        # 计算背包位置（居中显示）
        try:
            # 尝试获取屏幕尺寸
            if hasattr(游戏, 'get_width') and hasattr(游戏, 'get_height'):
                屏幕宽度 = 游戏.get_width()
                屏幕高度 = 游戏.get_height()
            elif hasattr(游戏, '屏幕') and hasattr(游戏.屏幕, 'get_width') and hasattr(游戏.屏幕, 'get_height'):
                屏幕宽度 = 游戏.屏幕.get_width()
                屏幕高度 = 游戏.屏幕.get_height()
            else:
                屏幕宽度 = 800
                屏幕高度 = 600
            
            # 计算居中位置
            self.位置_x = (屏幕宽度 - self.宽度) // 2
            self.位置_y = (屏幕高度 - self.高度) // 2
        except Exception as e:
            print(f"计算背包位置失败: {e}")
            # 使用默认位置
            self.位置_x = 150
            self.位置_y = 100
        
        # 颜色配置
        self.颜色 = {
            '背景暗': (50, 50, 55),
            '背景中': (70, 70, 75),
            '背景亮': (90, 90, 95),
            '边框暗': (120, 120, 125),
            '边框中': (150, 150, 155),
            '边框亮': (180, 180, 185),
            '文本主色': (255, 255, 255),
            '文本次色': (200, 200, 200),
            '格子普通': (60, 60, 65),
            '格子悬停': (80, 80, 85),
            '关闭按钮': (0, 0, 0),  # 黑色关闭按钮
            '关闭按钮悬停': (50, 50, 50)  # 悬停时稍亮的黑色
        }
        
        # 物品存储
        self.背包物品 = [[None for _ in range(6)] for _ in range(5)]  # 5x6的背包格子
        self.装备物品 = [None] * 4  # 4个装备槽
        self.快捷栏物品 = [None] * 9  # 9个快捷栏槽
        
        # 字体
        self.标题字体 = pygame.font.SysFont("SimHei", 24)
        self.普通字体 = pygame.font.SysFont("SimHei", 20)
        self.悬停字体 = pygame.font.SysFont("SimHei", 16)
        
        # 当前悬停物品
        self.当前悬停物品 = None
        self.当前悬停物品_rect = None
        
        # 拖拽状态
        self.拖拽中的物品 = None  # (物品, 来源类型, 来源位置)
        self.右键拆分的物品 = None  # 用于处理右键拆分跟随鼠标的物品
        
        # 不再随机填充背包，根据游玩.py中的注释："背包测试完毕，不再随机生成初始物品"
    
    def 切换(self):
        """切换背包的打开/关闭状态"""
        self.是否打开 = not self.是否打开
        return self.是否打开
    
    def 打开(self):
        """打开背包"""
        self.是否打开 = True
        return True
    
    def 关闭(self):
        """关闭背包"""
        self.是否打开 = False
        return False
    
    def 处理点击(self, x, y, 按钮=1):
        """处理背包界面的点击事件"""
        # 这里可以添加点击逻辑
        if not self.是否打开:
            return False
        
        # 检查是否点击了关闭按钮
        关闭按钮_rect = self._获取关闭按钮_rect()
        if 关闭按钮_rect and 关闭按钮_rect.collidepoint(x, y):
            print("点击了关闭按钮")
            self.关闭()
            return True
        
        # 处理右键点击
        if 按钮 == 3:
            return self.处理右键点击(x, y)
        
        # 检查是否点击了装备栏(2*2区域)======================================================================================================================================================
        if self._是否在装备栏区域(x, y):
            行, 列 = self._获取装备槽(x, y)
            if 行 is not None and 列 is not None:
                print(f"点击了装备栏(2*2) 位置: ({行+1},{列+1})")
                self.处理装备栏点击(行, 列)
                return True
                
        # 检查是否点击了物品栏(5*6区域)=====================================================================================================================================================
        if self._是否在物品栏区域(x, y):
            行, 列 = self._获取物品栏槽(x, y)
            if 行 is not None and 列 is not None:
                print(f"点击了物品栏(5*6) 位置: ({行+1},{列+1})")
                self.处理物品栏点击(行, 列)
                return True
                
        # 检查是否点击了快捷栏(1*9区域)=====================================================================================================================================================
        '重点注意:1-8是快捷栏位，9是丢弃按钮'
        if self._是否在快捷栏区域(x, y):
            槽位 = self._获取快捷栏槽(x, y)
            if 槽位 is not None:
                if 槽位 == 8:  # 丢弃按钮
                    print("点击了丢弃按钮")
                    self.处理丢弃按钮点击()
                else:  # 快捷栏位
                    print(f"点击了快捷栏位 位置: {槽位+1}")
                    self.处理快捷栏点击(槽位)
                return True
        
        # 如果点击了背包外，取消拖拽
        if self.拖拽中的物品:
            self.取消拖拽()
        
        return False
    

    
    def 处理左键点击(self, x, y):
        """处理左键点击物品"""
        pass
    
    def 处理右键点击(self, x, y):
        """处理右键点击物品"""
        # 如果已经有拖拽中的物品，将其放回原位置
        if self.拖拽中的物品:
            self.取消拖拽()
            return True
        
        # 检查是否点击了物品栏
        if self._是否在物品栏区域(x, y):
            行, 列 = self._获取物品栏槽(x, y)
            if 行 is not None and 列 is not None:
                self.拆分物品('背包', (行, 列))
                return True
        
        # 检查是否点击了快捷栏
        if self._是否在快捷栏区域(x, y):
            槽位 = self._获取快捷栏槽(x, y)
            if 槽位 is not None and 槽位 < 8:  # 只处理前8个快捷栏位
                self.拆分物品('快捷栏', (0, 槽位))
                return True
        
        return False
    
    def 处理物品栏点击(self, 行, 列):
        """处理物品栏点击"""
        # 获取当前槽位的物品
        当前物品 = self.背包物品[行][列]
        
        if self.拖拽中的物品:
            # 正在拖拽物品，尝试放置
            # 检查是否是拆分物品
            if len(self.拖拽中的物品) == 4:
                被拖拽物品, 来源类型, 来源位置, 是拆分物品 = self.拖拽中的物品
            else:
                被拖拽物品, 来源类型, 来源位置 = self.拖拽中的物品
                是拆分物品 = False
            
            # 检查是否是回到原位置
            是原位置 = False
            if 来源类型 == '背包':
                来源行, 来源列 = 来源位置
                if 行 == 来源行 and 列 == 来源列:
                    是原位置 = True
            
            if 是原位置:
                # 回到原位置，直接放回物品
                if not 是拆分物品:
                    self.背包物品[行][列] = 被拖拽物品
                self.拖拽中的物品 = None
                return
            
            if 当前物品:
                # 目标槽位有物品
                if 当前物品.可以堆叠(被拖拽物品):
                    # 可以堆叠，合并物品
                    可堆叠数量 = 当前物品.获取最大堆叠() - 当前物品.数量
                    实际堆叠数量 = min(被拖拽物品.数量, 可堆叠数量)
                    当前物品.数量 += 实际堆叠数量
                    被拖拽物品.数量 -= 实际堆叠数量
                    
                    if 被拖拽物品.数量 <= 0:
                        # 所有物品都堆叠了，取消拖拽
                        self.拖拽中的物品 = None
                    else:
                        # 还有剩余物品，更新拖拽物品数量
                        if 是拆分物品:
                            self.拖拽中的物品 = (被拖拽物品, 来源类型, 来源位置, True)
                        else:
                            self.拖拽中的物品 = (被拖拽物品, 来源类型, 来源位置)
                else:
                    # 不能堆叠，检查是否是拆分物品
                    if 是拆分物品:
                        # 拆分物品不能与其他物品交换，取消拖拽并合并回原物品
                        self.取消拖拽()
                    else:
                        # 普通物品，交换物品
                        self.背包物品[行][列] = 被拖拽物品
                        来源物品 = 当前物品
                        
                        # 将来源物品放回原位置
                        if 来源类型 == '背包':
                            来源行, 来源列 = 来源位置
                            self.背包物品[来源行][来源列] = 来源物品
                        elif 来源类型 == '快捷栏':
                            来源行, 来源列 = 来源位置
                            self.快捷栏物品[来源列] = 来源物品
                        
                        # 取消拖拽
                        self.拖拽中的物品 = None
            else:
                # 目标槽位为空，放置物品
                self.背包物品[行][列] = 被拖拽物品
                
                # 拆分物品不需要清空原位置，普通物品需要
                if not 是拆分物品:
                    # 清空原位置
                    if 来源类型 == '背包':
                        来源行, 来源列 = 来源位置
                        self.背包物品[来源行][来源列] = None
                    elif 来源类型 == '快捷栏':
                        来源行, 来源列 = 来源位置
                        self.快捷栏物品[来源列] = None
                
                # 取消拖拽
                self.拖拽中的物品 = None
        else:
            # 没有拖拽物品，尝试拿起物品
            if 当前物品:
                self.拖拽中的物品 = (当前物品, '背包', (行, 列))
                self.背包物品[行][列] = None
    
    def 处理快捷栏点击(self, 槽位):
        """处理快捷栏点击"""
        # 获取当前槽位的物品
        当前物品 = self.快捷栏物品[槽位]
        
        if self.拖拽中的物品:
            # 正在拖拽物品，尝试放置
            # 检查是否是拆分物品
            if len(self.拖拽中的物品) == 4:
                被拖拽物品, 来源类型, 来源位置, 是拆分物品 = self.拖拽中的物品
            else:
                被拖拽物品, 来源类型, 来源位置 = self.拖拽中的物品
                是拆分物品 = False
            
            # 检查是否是回到原位置
            是原位置 = False
            if 来源类型 == '快捷栏':
                来源行, 来源列 = 来源位置
                if 槽位 == 来源列:
                    是原位置 = True
            
            if 是原位置:
                # 回到原位置，直接放回物品
                if not 是拆分物品:
                    self.快捷栏物品[槽位] = 被拖拽物品
                self.拖拽中的物品 = None
                return
            
            if 当前物品:
                # 目标槽位有物品
                if 当前物品.可以堆叠(被拖拽物品):
                    # 可以堆叠，合并物品
                    可堆叠数量 = 当前物品.获取最大堆叠() - 当前物品.数量
                    实际堆叠数量 = min(被拖拽物品.数量, 可堆叠数量)
                    当前物品.数量 += 实际堆叠数量
                    被拖拽物品.数量 -= 实际堆叠数量
                    
                    if 被拖拽物品.数量 <= 0:
                        # 所有物品都堆叠了，取消拖拽
                        self.拖拽中的物品 = None
                    else:
                        # 还有剩余物品，更新拖拽物品数量
                        if 是拆分物品:
                            self.拖拽中的物品 = (被拖拽物品, 来源类型, 来源位置, True)
                        else:
                            self.拖拽中的物品 = (被拖拽物品, 来源类型, 来源位置)
                else:
                    # 不能堆叠，检查是否是拆分物品
                    if 是拆分物品:
                        # 拆分物品不能与其他物品交换，取消拖拽并合并回原物品
                        self.取消拖拽()
                    else:
                        # 普通物品，交换物品
                        self.快捷栏物品[槽位] = 被拖拽物品
                        来源物品 = 当前物品
                        
                        # 将来源物品放回原位置
                        if 来源类型 == '背包':
                            来源行, 来源列 = 来源位置
                            self.背包物品[来源行][来源列] = 来源物品
                        elif 来源类型 == '快捷栏':
                            来源行, 来源列 = 来源位置
                            self.快捷栏物品[来源列] = 来源物品
                        
                        # 取消拖拽
                        self.拖拽中的物品 = None
            else:
                # 目标槽位为空，放置物品
                self.快捷栏物品[槽位] = 被拖拽物品
                
                # 拆分物品不需要清空原位置，普通物品需要
                if not 是拆分物品:
                    # 清空原位置
                    if 来源类型 == '背包':
                        来源行, 来源列 = 来源位置
                        self.背包物品[来源行][来源列] = None
                    elif 来源类型 == '快捷栏':
                        来源行, 来源列 = 来源位置
                        self.快捷栏物品[来源列] = None
                
                # 取消拖拽
                self.拖拽中的物品 = None
        else:
            # 没有拖拽物品，尝试拿起物品
            if 当前物品:
                self.拖拽中的物品 = (当前物品, '快捷栏', (0, 槽位))
                self.快捷栏物品[槽位] = None
    
    def 处理装备栏点击(self, 行, 列):
        """处理装备栏点击"""
        # 获取装备槽索引
        装备槽索引 = 行 * 2 + 列
        当前物品 = self.装备物品[装备槽索引]
        
        # 装备类型与装备槽的对应关系
        装备槽类型对应 = {
            0: 'helmet',  # 槽1：头盔
            1: 'armor',   # 槽2：盔甲
            2: 'boots',   # 槽3：靴子
            3: 'special'  # 槽4：特殊装备
        }
        
        if self.拖拽中的物品:
            # 正在拖拽物品，尝试装备
            # 检查是否是拆分物品
            if len(self.拖拽中的物品) == 4:
                被拖拽物品, 来源类型, 来源位置, 是拆分物品 = self.拖拽中的物品
            else:
                被拖拽物品, 来源类型, 来源位置 = self.拖拽中的物品
                是拆分物品 = False
            
            # 拆分物品不能装备，取消拖拽并合并回原物品
            if 是拆分物品:
                self.取消拖拽()
                return
            
            # 检查装备类型是否匹配当前装备槽
            被拖拽物品类型 = 被拖拽物品.物品信息.get('类型', '')
            当前槽允许类型 = 装备槽类型对应.get(装备槽索引, '')
            
            # 检查装备类型是否匹配
            if 当前槽允许类型 and 被拖拽物品类型 != 当前槽允许类型:
                # 类型不匹配，不能装备
                return
            
            if 当前物品:
                # 目标槽位有装备，交换
                self.装备物品[装备槽索引] = 被拖拽物品
                来源物品 = 当前物品
                
                # 将来源物品放回原位置
                if 来源类型 == '背包':
                    来源行, 来源列 = 来源位置
                    self.背包物品[来源行][来源列] = 来源物品
                elif 来源类型 == '快捷栏':
                    来源行, 来源列 = 来源位置
                    self.快捷栏物品[来源列] = 来源物品
                
                # 取消拖拽
                self.拖拽中的物品 = None
                
                # 更新玩家装备属性
                self._更新玩家装备属性()
            else:
                # 目标槽位为空，装备物品
                self.装备物品[装备槽索引] = 被拖拽物品
                
                # 清空原位置
                if 来源类型 == '背包':
                    来源行, 来源列 = 来源位置
                    self.背包物品[来源行][来源列] = None
                elif 来源类型 == '快捷栏':
                    来源行, 来源列 = 来源位置
                    self.快捷栏物品[来源列] = None
                
                # 取消拖拽
                self.拖拽中的物品 = None
                
                # 更新玩家装备属性
                self._更新玩家装备属性()
        else:
            # 没有拖拽物品，尝试拿起装备
            if 当前物品:
                self.拖拽中的物品 = (当前物品, '装备', (行, 列))
                self.装备物品[装备槽索引] = None
        
        # 更新玩家装备属性
        self._更新玩家装备属性()
    
    def 处理丢弃按钮点击(self):
        """处理丢弃按钮点击，生成掉落物实体（使用抛物线物理效果）"""
        if self.拖拽中的物品:
            # 获取被拖拽物品信息
            if len(self.拖拽中的物品) == 4:
                被拖拽物品, 来源类型, 来源位置, 是拆分物品 = self.拖拽中的物品
            else:
                被拖拽物品, 来源类型, 来源位置 = self.拖拽中的物品
                是拆分物品 = False
            
            # 生成掉落物
            if 被拖拽物品:
                # 获取玩家位置和朝向
                玩家_x = self.游戏.玩家.坐标_x
                玩家_y = self.游戏.玩家.坐标_y
                玩家朝向 = getattr(self.游戏.玩家, '朝向右', True)
                玩家宽度 = getattr(self.游戏.玩家, '宽', 32)
                玩家高度 = getattr(self.游戏.玩家, '高', 64)
                
                # 计算掉落位置：根据玩家朝向，在玩家前方生成
                # 向右30像素，向左50像素
                距离 = 30 if 玩家朝向 else 50
                掉落_x = 玩家_x + 玩家宽度 // 2 + 距离 * (1 if 玩家朝向 else -1)
                掉落_y = 玩家_y + 玩家高度 // 2
                
                # 根据玩家朝向设置水平速度和向上的垂直速度，实现抛物线效果
                水平速度 = 3 if 玩家朝向 else -3
                垂直速度 = -2  # 向上抛出，与按G键丢弃保持一致
                
                # 创建掉落物实体
                from 游玩 import ItemEntity
                掉落物 = ItemEntity(self.游戏.世界, 掉落_x, 掉落_y, 被拖拽物品.物品_id, 被拖拽物品.数量)
                
                # 设置掉落物的初始速度，实现抛物线运动
                掉落物.velocity_x = 水平速度
                掉落物.velocity_y = 垂直速度
                
                # 将掉落物添加到世界的掉落物列表中
                if hasattr(self.游戏.世界, 'items'):
                    self.游戏.世界.items.append(掉落物)
                else:
                    # 如果世界没有items属性，创建一个
                    self.游戏.世界.items = [掉落物]
            
            # 清空拖拽状态
            self.拖拽中的物品 = None
    
    def 拆分物品(self, 来源类型, 来源位置):
        """拆分物品，拆分后的物品跟随鼠标移动"""
        # 获取来源物品
        来源物品 = None
        if 来源类型 == '背包':
            行, 列 = 来源位置
            来源物品 = self.背包物品[行][列]
        elif 来源类型 == '快捷栏':
            行, 列 = 来源位置
            来源物品 = self.快捷栏物品[列]
        
        if not 来源物品 or 来源物品.数量 <= 1:
            return
        
        # 计算拆分数量（一半）
        拆分数量 = 来源物品.数量 // 2
        来源物品.数量 -= 拆分数量
        
        # 创建新物品
        新物品 = 物品(来源物品.物品_id, 拆分数量)
        
        # 将拆分后的物品放入拖拽状态，跟随鼠标移动
        self.拖拽中的物品 = (新物品, 来源类型, 来源位置, True)  # 最后一个参数表示是拆分物品
    
    def 取消拖拽(self):
        """取消拖拽，将物品放回原位置"""
        if self.拖拽中的物品:
            # 检查是否是拆分物品
            if len(self.拖拽中的物品) == 4:
                物品, 来源类型, 来源位置, 是拆分物品 = self.拖拽中的物品
                # 如果是拆分物品，将其数量合并回原物品
                if 是拆分物品:
                    if 来源类型 == '背包':
                        行, 列 = 来源位置
                        原物品 = self.背包物品[行][列]
                        if 原物品:
                            原物品.数量 += 物品.数量
                    elif 来源类型 == '快捷栏':
                        行, 列 = 来源位置
                        原物品 = self.快捷栏物品[列]
                        if 原物品:
                            原物品.数量 += 物品.数量
            else:
                物品, 来源类型, 来源位置 = self.拖拽中的物品
                # 普通拖拽物品，放回原位置
                if 来源类型 == '背包':
                    行, 列 = 来源位置
                    self.背包物品[行][列] = 物品
                elif 来源类型 == '快捷栏':
                    行, 列 = 来源位置
                    self.快捷栏物品[列] = 物品
                elif 来源类型 == '装备':
                    行, 列 = 来源位置
                    装备槽索引 = 行 * 2 + 列
                    self.装备物品[装备槽索引] = 物品
            
            self.拖拽中的物品 = None
    
    def 绘制拖拽物品(self, 屏幕, 鼠标位置):
        """绘制拖拽中的物品"""
        if self.拖拽中的物品:
            # 处理不同长度的拖拽状态
            if len(self.拖拽中的物品) == 4:
                物品, 来源类型, 来源位置, 是拆分物品 = self.拖拽中的物品
            else:
                物品, 来源类型, 来源位置 = self.拖拽中的物品
                是拆分物品 = False
            
            # 计算绘制位置（鼠标中心）
            物品_x = 鼠标位置[0] - self.物品槽大小 // 2
            物品_y = 鼠标位置[1] - self.物品槽大小 // 2
            
            # 绘制物品
            self._绘制物品(屏幕, 物品_x, 物品_y, 物品)
    

    
    def 处理事件(self, 事件):
        """处理各种事件
        
        当背包打开时，无论点击的是背包内还是背包外，都阻止事件继续传递到游戏世界
        """
        # 如果背包未打开，不处理事件
        if not self.是否打开:
            return False
        
        # 调用键盘事件处理
        if self.处理键盘(事件):
            return True
        
        # 处理鼠标点击
        if 事件.type == pygame.MOUSEBUTTONDOWN:
            if 事件.button == 1:  # 左键点击
                x, y = pygame.mouse.get_pos()
                # 无论点击的是背包内还是背包外，都返回True
                self.处理点击(x, y, 1)
                return True
            elif 事件.button == 3:  # 右键点击
                x, y = pygame.mouse.get_pos()
                # 无论点击的是背包内还是背包外，都返回True
                self.处理点击(x, y, 3)
                return True
        
        # 当背包打开时，其他事件也返回True，阻止继续传递
        return True
    
    def _是否在装备栏区域(self, x, y):
        """判断点是否在装备栏区域内"""
        标题栏高度 = 45
        装备栏_x = self.位置_x + 15
        装备栏_y = self.位置_y + 标题栏高度 + 20
        装备栏宽度 = 150
        装备栏高度 = 300
        
        物品槽大小 = self.物品槽大小
        物品槽间距 = self.物品槽间距
        装备槽起始_x = 装备栏_x + (装备栏宽度 - (2 * 物品槽大小 + 物品槽间距)) // 2
        装备槽起始_y = 装备栏_y + 60
        
        # 装备栏区域矩形
        区域_rect = pygame.Rect(
            装备槽起始_x,
            装备槽起始_y,
            2 * 物品槽大小 + 物品槽间距,
            2 * 物品槽大小 + 物品槽间距
        )
        return 区域_rect.collidepoint(x, y)
    
    def _获取装备槽(self, x, y):
        """获取装备栏中点击的格子坐标"""
        标题栏高度 = 45
        装备栏_x = self.位置_x + 15
        装备栏_y = self.位置_y + 标题栏高度 + 20
        装备栏宽度 = 150
        
        物品槽大小 = self.物品槽大小
        物品槽间距 = self.物品槽间距
        装备槽起始_x = 装备栏_x + (装备栏宽度 - (2 * 物品槽大小 + 物品槽间距)) // 2
        装备槽起始_y = 装备栏_y + 60
        
        # 计算点击的行列
        for i in range(2):
            for j in range(2):
                槽位_x = 装备槽起始_x + j * (物品槽大小 + 物品槽间距)
                槽位_y = 装备槽起始_y + i * (物品槽大小 + 物品槽间距)
                槽位_rect = pygame.Rect(槽位_x, 槽位_y, 物品槽大小, 物品槽大小)
                if 槽位_rect.collidepoint(x, y):
                    return (i, j)
        return (None, None)
    
    def _是否在物品栏区域(self, x, y):
        """判断点是否在物品栏区域内"""
        标题栏高度 = 45
        物品栏_x = self.位置_x + 170
        物品栏_y = self.位置_y + 标题栏高度 + 20
        
        物品槽大小 = self.物品槽大小
        物品槽间距 = self.物品槽间距
        物品栏槽起始_x = 物品栏_x + 15
        物品栏槽起始_y = 物品栏_y + 50
        
        # 物品栏区域矩形
        区域_rect = pygame.Rect(
            物品栏槽起始_x,
            物品栏槽起始_y,
            6 * 物品槽大小 + 5 * 物品槽间距,  # 6列
            5 * 物品槽大小 + 4 * 物品槽间距   # 5行
        )
        return 区域_rect.collidepoint(x, y)
    
    def _获取物品栏槽(self, x, y):
        """获取物品栏中点击的格子坐标"""
        标题栏高度 = 45
        物品栏_x = self.位置_x + 170
        物品栏_y = self.位置_y + 标题栏高度 + 20
        
        物品槽大小 = self.物品槽大小
        物品槽间距 = self.物品槽间距
        物品栏槽起始_x = 物品栏_x + 15
        物品栏槽起始_y = 物品栏_y + 50
        
        # 计算点击的行列
        for i in range(5):
            for j in range(6):
                槽位_x = 物品栏槽起始_x + j * (物品槽大小 + 物品槽间距)
                槽位_y = 物品栏槽起始_y + i * (物品槽大小 + 物品槽间距)
                槽位_rect = pygame.Rect(槽位_x, 槽位_y, 物品槽大小, 物品槽大小)
                if 槽位_rect.collidepoint(x, y):
                    return (i, j)
        return (None, None)
    
    def _是否在快捷栏区域(self, x, y):
        """判断点是否在快捷栏区域内"""
        快捷栏_y = self.位置_y + self.高度 - 70
        快捷栏宽度 = 550
        快捷栏_x = self.位置_x + (self.宽度 - 快捷栏宽度) // 2
        
        物品槽大小 = self.物品槽大小
        物品槽间距 = self.物品槽间距
        快捷栏槽起始_x = 快捷栏_x + (快捷栏宽度 - (9 * 物品槽大小 + 8 * 物品槽间距)) // 2
        快捷栏槽_y = 快捷栏_y + 7
        
        # 快捷栏区域矩形
        区域_rect = pygame.Rect(
            快捷栏槽起始_x,
            快捷栏槽_y,
            9 * 物品槽大小 + 8 * 物品槽间距,  # 9列
            物品槽大小
        )
        return 区域_rect.collidepoint(x, y)
    
    def _获取快捷栏槽(self, x, y):
        """获取快捷栏中点击的格子索引"""
        快捷栏_y = self.位置_y + self.高度 - 70
        快捷栏宽度 = 550
        快捷栏_x = self.位置_x + (self.宽度 - 快捷栏宽度) // 2
        
        物品槽大小 = self.物品槽大小
        物品槽间距 = self.物品槽间距
        快捷栏槽起始_x = 快捷栏_x + (快捷栏宽度 - (9 * 物品槽大小 + 8 * 物品槽间距)) // 2
        快捷栏槽_y = 快捷栏_y + 7
        
        # 计算点击的槽位索引
        for i in range(9):
            槽位_x = 快捷栏槽起始_x + i * (物品槽大小 + 物品槽间距)
            槽位_rect = pygame.Rect(槽位_x, 快捷栏槽_y, 物品槽大小, 物品槽大小)
            if 槽位_rect.collidepoint(x, y):
                return i
        return None
    
    def 处理键盘(self, 事件):
        """处理键盘事件
        支持ESC键和X键关闭背包
        """
        if 事件.type == pygame.KEYDOWN:
            # 检查是否按了ESC键或X键
            if 事件.key == pygame.K_ESCAPE or 事件.key == pygame.K_x:
                if self.是否打开:
                    self.关闭()
                    return True
        return False
    

    
    def _获取关闭按钮_rect(self):
        """获取关闭按钮的矩形区域"""
        if not self.是否打开:
            return None
        
        标题栏高度 = 45
        关闭按钮大小 = 28
        关闭按钮_rect = pygame.Rect(
            self.位置_x + self.宽度 - 关闭按钮大小 - 10,
            self.位置_y + (标题栏高度 - 关闭按钮大小) // 2,
            关闭按钮大小,
            关闭按钮大小
        )
        return 关闭按钮_rect
    
    def _绘制物品提示(self, 屏幕):
        """绘制物品提示信息，包括装备属性"""
        if not self.当前悬停物品:
            return
        
        # 绘制物品提示
        if self.当前悬停物品 and self.当前悬停物品_rect:
            # 获取物品信息
            物品名称 = self.当前悬停物品.get("名称", "未知物品")
            物品介绍 = self.当前悬停物品.get("说明", "无说明")
            
            # 创建提示文本
            名称文本 = f"物品:{物品名称}"
            介绍文本前缀 = "介绍:"
            介绍文本内容 = 物品介绍
            
            # 渲染名称文本
            名称表面 = self.悬停字体.render(名称文本, True, (255, 255, 255))
            
            # 文本换行处理
            def wrap_text(text, font, max_width_chars=20):
                lines = []
                current_line = ""
                for char in text:
                    current_line += char
                    if len(current_line) >= max_width_chars:
                        lines.append(current_line)
                        current_line = ""
                if current_line:
                    lines.append(current_line)
                return lines
            
            # 处理名称和介绍文本的换行
            名称_lines = wrap_text(物品名称, self.悬停字体, 20)
            名称_full_lines = [f"物品:{line}" for line in 名称_lines]
            介绍_lines = wrap_text(介绍文本内容, self.悬停字体, 20)
            if 介绍_lines:
                介绍_lines[0] = 介绍文本前缀 + 介绍_lines[0]
            
            # 从物品说明中提取属性加成
            属性_lines = []
            import re
            
            # 查找最大生命值加成
            hp_match = re.search(r'最大生命值\+?(\d+)', 物品介绍)
            if hp_match:
                属性_lines.append(f"最大生命值+{hp_match.group(1)}")
            
            # 查找攻击力加成
            attack_match = re.search(r'攻击力\+?(\d+)', 物品介绍)
            if attack_match:
                属性_lines.append(f"攻击力+{attack_match.group(1)}")
            
            # 查找防御力加成
            defense_match = re.search(r'防御\+?(\d+)', 物品介绍)
            if defense_match:
                属性_lines.append(f"防御力+{defense_match.group(1)}")
            
            # 查找移速加成
            speed_match = re.search(r'移速\+?(\d+(?:\.\d+)?)', 物品介绍)
            if speed_match:
                属性_lines.append(f"移速+{speed_match.group(1)}")
            
            # 查找跳跃力加成
            jump_match = re.search(r'(?:跳跃力|跳跃|跳跃加成)\+?(\d+(?:\.\d+)?)', 物品介绍)
            if jump_match:
                属性_lines.append(f"跳跃力+{jump_match.group(1)}")
            
            # 渲染所有文本行
            文本_surfaces = []
            for line in 名称_full_lines:
                文本_surfaces.append(self.悬停字体.render(line, True, (255, 255, 255)))
            if 属性_lines:
                # 添加属性标题
                属性_lines.insert(0, "装备属性:")
                for line in 属性_lines:
                    文本_surfaces.append(self.悬停字体.render(line, True, (0, 255, 0)))
            for line in 介绍_lines:
                文本_surfaces.append(self.悬停字体.render(line, True, (255, 255, 255)))
            
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
            pygame.draw.rect(屏幕, (0, 0, 0, 220), 提示框_rect, border_radius=5)
            pygame.draw.rect(屏幕, (100, 100, 100), 提示框_rect, 1, border_radius=5)
            
            # 绘制所有文本行
            current_y = 提示框_y + 6
            for surface in 文本_surfaces:
                屏幕.blit(surface, (提示框_x + 8, current_y))
                current_y += 行高
    
    def 随机填充背包(self, 填充百分比: int):
        """随机填充背包，用于测试"""
        import random
        # 获取所有物品ID
        from 物品定义 import 物品 as 物品定义
        所有物品ID = list(物品定义.keys())
        if not 所有物品ID:
            return
        
        # 计算要填充的格子数量
        背包总格子数 = 5 * 6  # 5行6列
        快捷栏总格子数 = 8  # 1-8为快捷栏
        总格子数 = 背包总格子数 + 快捷栏总格子数
        要填充的格子数 = int(总格子数 * 填充百分比 / 100)
        
        # 随机填充背包
        for _ in range(要填充的格子数):
            # 随机选择物品ID
            物品_id = random.choice(所有物品ID)
            # 随机选择数量（1到最大堆叠）
            最大堆叠 = 物品定义[物品_id].get("堆叠上限", 99)
            数量 = random.randint(1, 最大堆叠)
            # 随机选择位置（背包或快捷栏）
            if random.choice([True, False]) and 快捷栏总格子数 > 0:
                # 填充快捷栏
                位置 = random.randint(0, 7)  # 0-7对应快捷栏1-8
                self.添加物品到快捷栏(物品_id, 数量)
            else:
                # 填充背包
                self.添加物品到背包(物品_id, 数量)
    
    def 添加物品到背包(self, 物品_id, 数量=1, **kwargs):
        """将物品添加到背包"""
        # 先检查是否可以堆叠到现有物品上
        for 行 in range(5):
            for 列 in range(6):
                当前物品 = self.背包物品[行][列]
                if 当前物品 and 当前物品.物品_id == 物品_id:
                    可堆叠数量 = 当前物品.获取最大堆叠() - 当前物品.数量
                    if 可堆叠数量 > 0:
                        实际添加数量 = min(数量, 可堆叠数量)
                        当前物品.数量 += 实际添加数量
                        数量 -= 实际添加数量
                        if 数量 <= 0:
                            return True
        
        # 寻找空格子
        for 行 in range(5):
            for 列 in range(6):
                if self.背包物品[行][列] is None:
                    self.背包物品[行][列] = 物品(物品_id, 数量, **kwargs)
                    return True
        
        return False  # 背包已满
    
    def 添加物品到快捷栏(self, 物品_id, 数量=1, **kwargs):
        """将物品添加到快捷栏"""
        # 先检查是否可以堆叠到现有物品上
        for i in range(8):  # 0-7对应快捷栏1-8
            当前物品 = self.快捷栏物品[i]
            if 当前物品 and 当前物品.物品_id == 物品_id:
                可堆叠数量 = 当前物品.获取最大堆叠() - 当前物品.数量
                if 可堆叠数量 > 0:
                    实际添加数量 = min(数量, 可堆叠数量)
                    当前物品.数量 += 实际添加数量
                    数量 -= 实际添加数量
                    if 数量 <= 0:
                        return True
        
        # 寻找空格子
        for i in range(8):  # 0-7对应快捷栏1-8
            if self.快捷栏物品[i] is None:
                self.快捷栏物品[i] = 物品(物品_id, 数量, **kwargs)
                return True
        
        # 快捷栏已满，尝试添加到背包
        return self.添加物品到背包(物品_id, 数量, **kwargs)
    
    def 查找物品(self, 物品_id):
        """在所有存储中查找指定ID的物品"""
        # 检查背包物品（二维列表）
        for 行, 行物品 in enumerate(self.背包物品):
            for 列, 物品 in enumerate(行物品):
                if 物品 and 物品.物品_id == 物品_id:
                    return ('背包', (行, 列), 物品)
        
        # 检查装备物品（一维列表）
        for i, 物品 in enumerate(self.装备物品):
            if 物品 and 物品.物品_id == 物品_id:
                return ('装备', i, 物品)
        
        # 检查快捷栏物品（一维列表）
        for i, 物品 in enumerate(self.快捷栏物品):
            if 物品 and 物品.物品_id == 物品_id:
                return ('快捷栏', i, 物品)
        
        return None
    
    def 获取物品总数量(self, 物品_id):
        """计算背包中所有指定物品ID的总数量"""
        总数量 = 0
        
        # 检查背包物品（二维列表）
        for 行, 行物品 in enumerate(self.背包物品):
            for 列, 物品 in enumerate(行物品):
                if 物品 and 物品.物品_id == 物品_id:
                    总数量 += 物品.数量
        
        # 检查装备物品（一维列表）
        for i, 物品 in enumerate(self.装备物品):
            if 物品 and 物品.物品_id == 物品_id:
                总数量 += 物品.数量
        
        # 检查快捷栏物品（一维列表）
        for i, 物品 in enumerate(self.快捷栏物品):
            if 物品 and 物品.物品_id == 物品_id:
                总数量 += 物品.数量
        
        return 总数量
    
    def 减少物品数量(self, 物品_id, 数量):
        """从背包中减少指定数量的物品，返回实际减少的数量
        如果物品数量减到0或以下，自动删除该物品，并重复执行检查"""
        实际减少数量 = 0
        剩余需要减少数量 = 数量
        
        # 检查背包物品（二维列表）
        for 行, 行物品 in enumerate(self.背包物品):
            for 列, 物品 in enumerate(行物品):
                if 物品 and 物品.物品_id == 物品_id:
                    if 物品.数量 >= 剩余需要减少数量:
                        物品.数量 -= 剩余需要减少数量
                        实际减少数量 += 剩余需要减少数量
                        # 检查物品数量是否为0，如果是则删除物品
                        if 物品.数量 <= 0:
                            self.背包物品[行][列] = None
                        return 实际减少数量
                    else:
                        # 物品数量不足，减少全部
                        实际减少数量 += 物品.数量
                        剩余需要减少数量 -= 物品.数量
                        # 删除物品，因为数量已经减到0
                        self.背包物品[行][列] = None
                        if 剩余需要减少数量 <= 0:
                            return 实际减少数量
        
        # 检查快捷栏物品（一维列表）
        for i, 物品 in enumerate(self.快捷栏物品):
            if 物品 and 物品.物品_id == 物品_id:
                if 物品.数量 >= 剩余需要减少数量:
                    物品.数量 -= 剩余需要减少数量
                    实际减少数量 += 剩余需要减少数量
                    # 检查物品数量是否为0，如果是则删除物品
                    if 物品.数量 <= 0:
                        self.快捷栏物品[i] = None
                    return 实际减少数量
                else:
                    # 物品数量不足，减少全部
                    实际减少数量 += 物品.数量
                    剩余需要减少数量 -= 物品.数量
                    # 删除物品，因为数量已经减到0
                    self.快捷栏物品[i] = None
                    if 剩余需要减少数量 <= 0:
                        return 实际减少数量
        
    def 清空背包(self):
        """清空所有背包、装备栏和快捷栏中的物品"""
        print("清空背包")
        # 清空背包物品
        self.背包物品 = [[None for _ in range(6)] for _ in range(5)]
        # 清空装备物品
        self.装备物品 = [None] * 4
        # 清空快捷栏物品
        self.快捷栏物品 = [None] * 9
    
    def 计算装备总属性(self):
        """计算所有装备的总属性
        
        返回:
            dict: 包含各项装备属性总和的字典
        """
        # 初始化属性总和
        属性总和 = {
            '生命值': 0,
            '攻击力': 0,
            '防御力': 0,
            '移速': 0,
            '跳跃力': 0,
            '摔落安全格数': 0
        }
        
        # 遍历所有装备物品
        for 装备 in self.装备物品:
            if 装备:
                # 获取装备的物品信息
                装备信息 = 装备.物品信息
                
                # 从物品说明中提取属性加成
                说明 = 装备信息.get('说明', '')
                import re
                # 查找最大生命值加成，例如：最大生命值+10
                hp_match = re.search(r'最大生命值\+?(\d+)', 说明)
                if hp_match:
                    属性总和['生命值'] += int(hp_match.group(1))
                
                # 查找攻击力/伤害加成，例如：伤害加成+1、攻击力+10、伤害加成：8或攻击力：5
                attack_match = re.search(r'(?:攻击力|伤害加成)[：+]?(\d+)', 说明)
                if attack_match:
                    属性总和['攻击力'] += int(attack_match.group(1))
                
                # 查找防御力加成，例如：防御：1、防御力+10、防御：1或防御力：10
                defense_match = re.search(r'防御(?:力)?[：+]?(\d+)', 说明)
                if defense_match:
                    属性总和['防御力'] += int(defense_match.group(1))
                
                # 查找移速加成，例如：移速+5、移速：5、移速+5%或速度加成+10
                speed_match = re.search(r'(?:移速|速度加成)[：+]?(\d+(?:\.\d+)?)', 说明)
                if speed_match:
                    属性总和['移速'] += float(speed_match.group(1))
                
                # 查找跳跃力加成，例如：跳跃力+5、跳跃：5、跳跃力：5或跳跃加成：5
                jump_match = re.search(r'(?:跳跃力|跳跃|跳跃加成)[：+]?(\d+(?:\.\d+)?)', 说明)
                if jump_match:
                    属性总和['跳跃力'] += float(jump_match.group(1))
                
                # 查找靴子等级，计算摔落安全格数加成
                装备名称 = 装备信息.get('名称', '')
                # 从名称中提取等级数字
                level_match = re.search(r'(\d+)级', 装备名称)
                if level_match and 装备信息.get('类型') == 'boots':
                    等级 = int(level_match.group(1))
                    # 根据等级计算摔落安全格数：1级1格，2级1.5格，3级2格，4级2.5格，5级3格
                    if 等级 == 1:
                        属性总和['摔落安全格数'] += 1.0
                    elif 等级 == 2:
                        属性总和['摔落安全格数'] += 1.5
                    elif 等级 == 3:
                        属性总和['摔落安全格数'] += 2.0
                    elif 等级 == 4:
                        属性总和['摔落安全格数'] += 2.5
                    elif 等级 == 5:
                        属性总和['摔落安全格数'] += 3.0
        
        return 属性总和
    
    def _更新玩家装备属性(self):
        """更新玩家的装备属性，包括生命值、攻击力等"""
        # 计算装备总属性
        装备属性 = self.计算装备总属性()
        
        # 调试输出：装备属性
        print(f"装备属性总和：{装备属性}")
        
        # 获取游戏实例和玩家对象
        if hasattr(self, '游戏') and hasattr(self.游戏, '玩家'):
            玩家 = self.游戏.玩家
            
            # 更新玩家的装备生命值
            if hasattr(玩家, 'equipment_health'):
                玩家.equipment_health = 装备属性['生命值']
                # 重新计算总生命值
                玩家.max_health = 玩家.base_max_health + 玩家.equipment_health + 玩家.upgrade_health
                
                # 如果当前生命值超过新的最大生命值，调整当前生命值
                if hasattr(玩家, 'current_health') and 玩家.current_health > 玩家.max_health:
                    玩家.current_health = 玩家.max_health
            
            # 更新玩家的装备攻击力
            if hasattr(玩家, 'equipment_attack'):
                玩家.equipment_attack = 装备属性['攻击力']
                # 调试输出：装备攻击力
                print(f"玩家装备攻击力更新为：{玩家.equipment_attack}")
            
            # 更新玩家的装备防御力
            if hasattr(玩家, 'equipment_defense'):
                玩家.equipment_defense = 装备属性['防御力']
            
            # 更新玩家的装备移速
            if hasattr(玩家, 'equipment_speed'):
                玩家.equipment_speed = 装备属性['移速']
            
            # 更新玩家的装备跳跃力
            if hasattr(玩家, 'equipment_jump'):
                玩家.equipment_jump = 装备属性['跳跃力']
            
            # 更新玩家的装备摔落安全格数
            if hasattr(玩家, 'equipment_fall_safety'):
                玩家.equipment_fall_safety = 装备属性['摔落安全格数']
    
    def 绘制(self, 屏幕):
        """绘制背包界面"""
        if not self.是否打开:
            return
        
        # 更新屏幕尺寸
        屏幕宽度 = 屏幕.get_width()
        屏幕高度 = 屏幕.get_height()
        
        # 重新计算居中位置，确保背包页面始终居中
        self.位置_x = (屏幕宽度 - self.宽度) // 2
        self.位置_y = (屏幕高度 - self.高度) // 2
        
        # 获取鼠标位置
        鼠标位置 = pygame.mouse.get_pos()
        
        # 绘制半透明背景覆盖层
        覆盖层 = pygame.Surface((屏幕宽度, 屏幕高度), pygame.SRCALPHA)
        覆盖层.fill((0, 0, 0, 180))
        屏幕.blit(覆盖层, (0, 0))
        
        # 绘制主界面背景 - 多层边框效果
        # 底层阴影
        pygame.draw.rect(屏幕, (0, 0, 0, 100), 
                         (self.位置_x + 3, self.位置_y + 3, self.宽度, self.高度), 0, 8)
        # 主背景
        pygame.draw.rect(屏幕, self.颜色['背景暗'], 
                         (self.位置_x, self.位置_y, self.宽度, self.高度), 0, 8)
        # 三层边框效果
        pygame.draw.rect(屏幕, self.颜色['边框暗'], 
                         (self.位置_x, self.位置_y, self.宽度, self.高度), 3, 8)
        pygame.draw.rect(屏幕, self.颜色['边框中'], 
                         (self.位置_x + 3, self.位置_y + 3, self.宽度 - 6, self.高度 - 6), 1, 6)
        
        # 绘制标题栏
        标题栏高度 = 45
        pygame.draw.rect(屏幕, self.颜色['背景中'], 
                         (self.位置_x, self.位置_y, self.宽度, 标题栏高度), 0, 8)
        pygame.draw.rect(屏幕, self.颜色['边框中'], 
                         (self.位置_x, self.位置_y, self.宽度, 标题栏高度), 1, 8)
        pygame.draw.rect(屏幕, self.颜色['边框暗'], 
                         (self.位置_x, self.位置_y + 标题栏高度 - 2, self.宽度, 2))
        
        # 绘制标题 - 背包图标和文字
        标题文本 = self.标题字体.render("背包", True, self.颜色['文本主色'])
        标题_x = self.位置_x + 20
        屏幕.blit(标题文本, (标题_x, self.位置_y + 10))
        
        # 绘制关闭按钮
        关闭按钮_rect = self._获取关闭按钮_rect()
        关闭按钮悬停 = 关闭按钮_rect and 关闭按钮_rect.collidepoint(鼠标位置)
        
        # 关闭按钮多层效果
        pygame.draw.rect(屏幕, self.颜色['关闭按钮悬停'] if 关闭按钮悬停 else self.颜色['关闭按钮'], 
                         关闭按钮_rect, 0, 5)
        pygame.draw.rect(屏幕, self.颜色['边框亮'], 关闭按钮_rect, 2, 5)
        pygame.draw.rect(屏幕, (0, 0, 0, 50), 
                         (关闭按钮_rect.x + 1, 关闭按钮_rect.y + 1, 
                          关闭按钮_rect.width - 2, 关闭按钮_rect.height - 2), 0, 4)
        
        # 绘制关闭符号
        关闭文本 = self.普通字体.render("×", True, self.颜色['文本主色'])
        关闭文本_x = 关闭按钮_rect.x + (关闭按钮_rect.width - 关闭文本.get_width()) // 2
        关闭文本_y = 关闭按钮_rect.y + (关闭按钮_rect.height - 关闭文本.get_height()) // 2 - 2
        屏幕.blit(关闭文本, (关闭文本_x, 关闭文本_y))
        
        # 重置当前悬停物品
        self.当前悬停物品 = None
        self.当前悬停物品_rect = None
        
        # 绘制装备栏
        self._绘制装备栏区域(屏幕, 鼠标位置)
        
        # 绘制物品栏
        self._绘制物品栏区域(屏幕, 鼠标位置)
        
        # 绘制快捷栏
        self._绘制快捷栏区域(屏幕, 鼠标位置)
        
        # 绘制物品提示
        self._绘制物品提示(屏幕)
        
        # 绘制拖拽中的物品
        鼠标位置 = pygame.mouse.get_pos()
        self.绘制拖拽物品(屏幕, 鼠标位置)
    
    def 检测物品悬停(self, x, y):
        """检测鼠标位置是否悬停在物品上"""
        # 重置当前悬停物品
        self.当前悬停物品 = None
        self.当前悬停物品_rect = None
        
        # 检测装备栏物品悬停
        if self._是否在装备栏区域(x, y):
            行, 列 = self._获取装备槽(x, y)
            if 行 is not None and 列 is not None:
                装备槽索引 = 行 * 2 + 列
                当前物品 = self.装备物品[装备槽索引]
                if 当前物品:
                    # 获取装备槽位置
                    标题栏高度 = 45
                    装备栏_x = self.位置_x + 15
                    装备栏_y = self.位置_y + 标题栏高度 + 20
                    物品槽大小 = self.物品槽大小
                    物品槽间距 = self.物品槽间距
                    装备槽起始_x = 装备栏_x + (装备栏宽度 - (2 * 物品槽大小 + 物品槽间距)) // 2
                    装备槽起始_y = 装备栏_y + 60
                    槽位_x = 装备槽起始_x + 列 * (物品槽大小 + 物品槽间距)
                    槽位_y = 装备槽起始_y + 行 * (物品槽大小 + 物品槽间距)
                    
                    # 设置当前悬停物品
                    self.当前悬停物品 = 当前物品.物品信息
                    self.当前悬停物品_rect = pygame.Rect(槽位_x, 槽位_y, 物品槽大小, 物品槽大小)
        
        # 检测物品栏物品悬停
        elif self._是否在物品栏区域(x, y):
            行, 列 = self._获取物品栏槽(x, y)
            if 行 is not None and 列 is not None:
                当前物品 = self.背包物品[行][列]
                if 当前物品:
                    # 获取物品槽位置
                    标题栏高度 = 45
                    物品栏_x = self.位置_x + 170
                    物品栏_y = self.位置_y + 标题栏高度 + 20
                    物品槽大小 = self.物品槽大小
                    物品槽间距 = self.物品槽间距
                    物品栏槽起始_x = 物品栏_x + 15
                    物品栏槽起始_y = 物品栏_y + 50
                    槽位_x = 物品栏槽起始_x + 列 * (物品槽大小 + 物品槽间距)
                    槽位_y = 物品栏槽起始_y + 行 * (物品槽大小 + 物品槽间距)
                    
                    # 设置当前悬停物品
                    self.当前悬停物品 = 当前物品.物品信息
                    self.当前悬停物品_rect = pygame.Rect(槽位_x, 槽位_y, 物品槽大小, 物品槽大小)
        
        # 检测快捷栏物品悬停
        elif self._是否在快捷栏区域(x, y):
            槽位 = self._获取快捷栏槽(x, y)
            if 槽位 is not None and 槽位 < 8:
                当前物品 = self.快捷栏物品[槽位]
                if 当前物品:
                    # 获取快捷栏槽位置
                    快捷栏_y = self.位置_y + self.高度 - 70
                    快捷栏宽度 = 550
                    快捷栏_x = self.位置_x + (self.宽度 - 快捷栏宽度) // 2
                    物品槽大小 = self.物品槽大小
                    物品槽间距 = self.物品槽间距
                    快捷栏槽起始_x = 快捷栏_x + (快捷栏宽度 - (9 * 物品槽大小 + 8 * 物品槽间距)) // 2
                    快捷栏槽_y = 快捷栏_y + 7
                    槽位_x = 快捷栏槽起始_x + 槽位 * (物品槽大小 + 物品槽间距)
                    
                    # 设置当前悬停物品
                    self.当前悬停物品 = 当前物品.物品信息
                    self.当前悬停物品_rect = pygame.Rect(槽位_x, 快捷栏槽_y, 物品槽大小, 物品槽大小)
    
    def _绘制装备栏区域(self, 屏幕, 鼠标位置):
        """绘制装备栏区域"""
        标题栏高度 = 45
        装备栏_x = self.位置_x + 15
        装备栏_y = self.位置_y + 标题栏高度 + 20
        装备栏宽度 = 150
        装备栏高度 = 300
        
        # 绘制装备栏背景
        pygame.draw.rect(屏幕, self.颜色['背景中'], 
                         (装备栏_x, 装备栏_y, 装备栏宽度, 装备栏高度), 0, 6)
        pygame.draw.rect(屏幕, self.颜色['边框中'], 
                         (装备栏_x, 装备栏_y, 装备栏宽度, 装备栏高度), 2, 6)
        
        # 装备栏标题
        装备栏标题 = self.普通字体.render("装备栏", True, self.颜色['文本主色'])
        标题_bg_rect = pygame.Rect(装备栏_x + 10, 装备栏_y + 10,
                                  装备栏宽度 - 20, 25)
        pygame.draw.rect(屏幕, self.颜色['背景暗'], 标题_bg_rect, 0, 3)
        pygame.draw.rect(屏幕, self.颜色['边框暗'], 标题_bg_rect, 1, 3)
        屏幕.blit(装备栏标题, (装备栏_x + 20, 装备栏_y + 12))
        
        # 绘制装备格子
        物品槽大小 = self.物品槽大小
        物品槽间距 = self.物品槽间距
        装备槽起始_x = 装备栏_x + (装备栏宽度 - (2 * 物品槽大小 + 物品槽间距)) // 2
        装备槽起始_y = 装备栏_y + 60
        
        for i in range(2):
            for j in range(2):
                x = 装备槽起始_x + j * (物品槽大小 + 物品槽间距)
                y = 装备槽起始_y + i * (物品槽大小 + 物品槽间距)
                
                # 检查鼠标悬停
                鼠标悬停 = x <= 鼠标位置[0] <= x + 物品槽大小 and y <= 鼠标位置[1] <= y + 物品槽大小
                
                # 绘制格子
                self._绘制物品槽(屏幕, x, y, 鼠标悬停)
                
                # 绘制物品
                当前物品 = self.装备物品[i * 2 + j]
                if 当前物品:
                    self._绘制物品(屏幕, x, y, 当前物品)
                    
                    # 检查鼠标是否悬停在物品上
                    if 鼠标悬停:
                        # 设置当前悬停物品
                        self.当前悬停物品 = 当前物品.物品信息
                        self.当前悬停物品_rect = pygame.Rect(x, y, 物品槽大小, 物品槽大小)
                        物品悬停 = True
        
        # 绘制属性信息
        self._绘制装备属性(屏幕, 装备栏_x, 装备栏_y, 装备栏宽度, 装备栏高度)
    
    def _绘制物品栏区域(self, 屏幕, 鼠标位置):
        """绘制物品栏区域"""
        标题栏高度 = 45
        物品栏_x = self.位置_x + 170
        物品栏_y = self.位置_y + 标题栏高度 + 20
        物品栏宽度 = 320
        物品栏高度 = 300
        
        # 绘制物品栏背景
        pygame.draw.rect(屏幕, self.颜色['背景中'], 
                         (物品栏_x, 物品栏_y, 物品栏宽度, 物品栏高度), 0, 6)
        pygame.draw.rect(屏幕, self.颜色['边框中'], 
                         (物品栏_x, 物品栏_y, 物品栏宽度, 物品栏高度), 2, 6)
        
        # 物品栏标题
        物品栏标题 = self.普通字体.render("物品栏", True, self.颜色['文本主色'])
        标题_bg_rect = pygame.Rect(物品栏_x + 10, 物品栏_y + 10,
                                  物品栏宽度 - 20, 25)
        pygame.draw.rect(屏幕, self.颜色['背景暗'], 标题_bg_rect, 0, 3)
        pygame.draw.rect(屏幕, self.颜色['边框暗'], 标题_bg_rect, 1, 3)
        屏幕.blit(物品栏标题, (物品栏_x + 20, 物品栏_y + 12))
        
        # 绘制物品格子
        物品槽大小 = self.物品槽大小
        物品槽间距 = self.物品槽间距
        物品栏槽起始_x = 物品栏_x + 15
        物品栏槽起始_y = 物品栏_y + 50
        
        # 重置当前悬停物品
        物品悬停 = False
        
        for i in range(5):
            for j in range(6):
                x = 物品栏槽起始_x + j * (物品槽大小 + 物品槽间距)
                y = 物品栏槽起始_y + i * (物品槽大小 + 物品槽间距)
                
                # 检查鼠标悬停
                鼠标悬停 = x <= 鼠标位置[0] <= x + 物品槽大小 and y <= 鼠标位置[1] <= y + 物品槽大小
                
                # 绘制格子
                self._绘制物品槽(屏幕, x, y, 鼠标悬停)
                
                # 绘制物品
                当前物品 = self.背包物品[i][j]
                if 当前物品:
                    self._绘制物品(屏幕, x, y, 当前物品)
                    
                    # 检查鼠标是否悬停在物品上
                    if 鼠标悬停:
                        # 设置当前悬停物品
                        self.当前悬停物品 = 当前物品.物品信息
                        self.当前悬停物品_rect = pygame.Rect(x, y, 物品槽大小, 物品槽大小)
                        物品悬停 = True
    
    def _绘制快捷栏区域(self, 屏幕, 鼠标位置):
        """绘制快捷栏区域"""
        快捷栏_y = self.位置_y + self.高度 - 70
        快捷栏宽度 = 550
        快捷栏_x = self.位置_x + (self.宽度 - 快捷栏宽度) // 2
        
        # 绘制快捷栏格子
        物品槽大小 = self.物品槽大小
        物品槽间距 = self.物品槽间距
        快捷栏槽起始_x = 快捷栏_x + (快捷栏宽度 - (9 * 物品槽大小 + 8 * 物品槽间距)) // 2
        快捷栏槽_y = 快捷栏_y + 7
        
        for i in range(9):
            x = 快捷栏槽起始_x + i * (物品槽大小 + 物品槽间距)
            y = 快捷栏槽_y
            
            # 检查鼠标悬停
            鼠标悬停 = x <= 鼠标位置[0] <= x + 物品槽大小 and y <= 鼠标位置[1] <= y + 物品槽大小
            
            # 第9个格子为丢弃按钮
            槽位类型 = "discard" if i == 8 else "normal"
            
            # 绘制格子
            self._绘制物品槽(屏幕, x, y, 鼠标悬停, 槽位类型)
            
            # 绘制物品（前8个槽位）
            if i < 8:  # 0-7对应快捷栏1-8
                当前物品 = self.快捷栏物品[i]
                if 当前物品:
                    self._绘制物品(屏幕, x, y, 当前物品)
                    
                    # 检查鼠标是否悬停在物品上
                    if 鼠标悬停:
                        # 设置当前悬停物品
                        self.当前悬停物品 = 当前物品.物品信息
                        self.当前悬停物品_rect = pygame.Rect(x, y, 物品槽大小, 物品槽大小)
                        物品悬停 = True
    
    def _绘制物品槽(self, 屏幕, x, y, 鼠标悬停=False, 槽位类型="normal"):
        """绘制单个物品槽"""
        物品槽大小 = self.物品槽大小
        
        # 根据槽类型设置颜色
        if 槽位类型 == "input":
            槽位背景 = (70, 60, 40)
            槽位边框 = (160, 140, 100)
        elif 槽位类型 == "fuel":
            槽位背景 = (70, 40, 40)
            槽位边框 = (160, 100, 100)
        elif 槽位类型 == "output":
            槽位背景 = (40, 70, 50)
            槽位边框 = (100, 160, 120)
        elif 槽位类型 == "discard":
            # 丢弃按钮：红色背景
            槽位背景 = (180, 60, 60)
            槽位边框 = (220, 80, 80)
        else:
            槽位背景 = self.颜色['格子悬停'] if 鼠标悬停 else self.颜色['格子普通']
            槽位边框 = self.颜色['边框亮'] if 鼠标悬停 else self.颜色['边框中']
        
        # 绘制格子
        pygame.draw.rect(屏幕, 槽位背景, (x, y, 物品槽大小, 物品槽大小), 0, 4)
        pygame.draw.rect(屏幕, 槽位边框, (x, y, 物品槽大小, 物品槽大小), 2, 4)
        pygame.draw.rect(屏幕, (0, 0, 0, 30), 
                         (x + 2, y + 2, 物品槽大小 - 4, 物品槽大小 - 4), 1, 3)
        
        # 丢弃按钮显示文字
        if 槽位类型 == "discard":
            丢弃文本 = self.悬停字体.render("丢弃", True, (255, 255, 255))
            文本_x = x + (物品槽大小 - 丢弃文本.get_width()) // 2
            文本_y = y + (物品槽大小 - 丢弃文本.get_height()) // 2
            屏幕.blit(丢弃文本, (文本_x, 文本_y))
    
    def _绘制物品(self, 屏幕, x, y, 物品):
        """绘制物品，包括图像和数量"""
        物品槽大小 = self.物品槽大小
        
        # 计算物品绘制位置（居中）
        物品_x = x + 5
        物品_y = y + 5
        物品绘制大小 = 物品槽大小 - 10
        
        # 获取物品图像，直接传入尺寸
        物品图像 = 物品.获取图像((物品绘制大小, 物品绘制大小))
        if 物品图像:
            # 绘制物品图像
            屏幕.blit(物品图像, (物品_x, 物品_y))
        else:
            # 没有图像时，绘制物品颜色块
            pygame.draw.rect(屏幕, 物品.获取颜色(), 
                           (物品_x, 物品_y, 物品绘制大小, 物品绘制大小), 
                           border_radius=3)
        
        # 绘制物品数量（如果大于1）
        if 物品.数量 > 1:
            数量文本 = self.悬停字体.render(str(物品.数量), True, (255, 255, 255))
            # 数量文本位置（右下角）
            数量_x = x + 物品槽大小 - 数量文本.get_width() - 3
            数量_y = y + 物品槽大小 - 数量文本.get_height() - 3
            # 绘制数量背景
            背景_rect = pygame.Rect(数量_x - 2, 数量_y - 2, 
                                  数量文本.get_width() + 4, 数量文本.get_height() + 4)
            pygame.draw.rect(屏幕, (0, 0, 0, 180), 背景_rect, border_radius=3)
            # 绘制数量文本
            屏幕.blit(数量文本, (数量_x, 数量_y))
        
        # 绘制耐久度进度条（3像素高）
        max_durability = 物品.获取属性("耐久度", 0)
        if max_durability > 0:
            current_durability = 物品.获取属性("当前耐久度", max_durability)
            durability_percent = (current_durability / max_durability) * 100
            
            # 满95%+不显示耐久进度条
            if durability_percent < 95:
                # 背包显示3像素高的耐久条
                progress_bar_height = 3
                progress_bar_width = 物品槽大小 - 10  # 进度条宽度比物品槽小10像素
                progress_bar_x = x + 5  # 居中显示
                progress_bar_y = y + 物品槽大小 - progress_bar_height - 5  # 距离底部5像素
                
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
                pygame.draw.rect(屏幕, (0, 0, 0, 128), 
                                (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height),
                                border_radius=1)
                # 绘制耐久度进度
                if progress_length > 0:
                    pygame.draw.rect(屏幕, color, 
                                    (progress_bar_x, progress_bar_y, progress_length, progress_bar_height),
                                    border_radius=1)
    
    def _绘制装备属性(self, 屏幕, x, y, 宽度, 高度):
        """绘制装备属性统计"""
        # 获取装备总属性
        属性总和 = self.计算装备总属性()
        
        # 创建属性文字列表
        属性列表 = [
            f"最大生命值+{属性总和['生命值']}",
            f"攻击力+{属性总和['攻击力']}",
            f"防御力+{属性总和['防御力']}",
            f"移速+{属性总和['移速']}",
            f"跳跃力+{属性总和['跳跃力']}"
        ]
        
        # 文字位置
        文字起始_y = y + 高度 - 120
        文字中心_x = x + 宽度 // 2
        
        # 绘制属性文字
        for i, 属性文本 in enumerate(属性列表):
            文本表面 = self.悬停字体.render(属性文本, True, self.颜色['文本主色'])
            文本_x = 文字中心_x - 文本表面.get_width() // 2
            文本_y = 文字起始_y + i * 20
            
            # 绘制背景
            背景宽度 = 文本表面.get_width() + 20
            背景高度 = 文本表面.get_height() + 6
            背景_x = 文字中心_x - 背景宽度 // 2
            背景_y = 文本_y - 3
            
            pygame.draw.rect(屏幕, (65, 65, 70), (背景_x, 背景_y, 背景宽度, 背景高度), 0, 3)
            pygame.draw.rect(屏幕, self.颜色['边框暗'], (背景_x, 背景_y, 背景宽度, 背景高度), 1, 3)
            
            # 绘制文字
            屏幕.blit(文本表面, (文本_x, 文本_y))
