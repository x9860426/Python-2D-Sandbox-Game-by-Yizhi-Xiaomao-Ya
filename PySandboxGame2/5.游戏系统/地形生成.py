import random
import math

# 导入方块常量
from 物品定义 import (
    空气, 土块, 草方块, 岩石, 木头, 树叶, 沙子, 黑土块, 水, 岩浆,
    红花, 草, 仙人掌, 枯草, 乔木, 乔木叶, 灌木, 基岩,
    煤矿, 铁矿石, 铜矿石, 金矿石, 钻石矿石,
    乔木果
)

# 地形类型枚举
地形类型 = {
    '森林': 1,
    '草原': 2,
    '高山': 3,
    '沙漠': 4,
    '雨林': 5
}

class 地形生成器:
    """地形生成器类，负责生成各种类型的地形"""
    
    def __init__(self, 世界宽度, 世界高度, 地形_type, 无限世界=False):
        self.世界宽度 = 世界宽度
        self.世界高度 = 世界高度
        self.地形_type = 地形_type
        self.无限世界 = 无限世界
        
        # 根据地形类型设置参数
        self.设置地形参数()
        
    def 设置地形参数(self):
        """根据地形类型设置生成参数"""
        # 地形基础参数
        self.地形参数 = {
            '森林': {
                '起伏': 20,
                '起伏间隔': random.randint(10, 100),
                '地形大小': random.randint(100, 500),
                '木头数量': '中',  # 4-8高，宽1
                '草数量': '少',
                '花数量': '较少',
                '生成乔木': False
            },
            '草原': {
                '起伏': 5,
                '起伏间隔': random.randint(10, 100),
                '地形大小': random.randint(100, 600),
                '木头数量': '较少',  # 4-8高，宽1
                '草数量': '中',
                '花数量': '少',
                '生成乔木': False
            },
            '高山': {
                '起伏': 30,
                '起伏间隔': random.randint(10, 100),
                '地形大小': random.randint(150, 400),
                '木头数量': '较少',  # 4-8高，宽1
                '草数量': '少',
                '花数量': '多',
                '生成乔木': False
            },
            '沙漠': {
                '起伏': 10,
                '起伏间隔': random.randint(10, 100),
                '地形大小': random.randint(200, 600),
                '仙人掌数量': '较多',  # 1-3高
                '枯草数量': '多',
                '生成乔木': False
            },
            '雨林': {
                '起伏': 10,
                '起伏间隔': random.randint(10, 100),
                '地形大小': random.randint(300, 600),
                '乔木数量': '较多',  # 5-12高3-5粗
                '灌木数量': '中',
                '草数量': '少',
                '花数量': '非常少',
                '生成乔木': True
            }
        }
        
        self.当前参数 = self.地形参数.get(self.地形_type, self.地形参数['森林'])
        
        # 将数量描述转换为概率值
        self.数量_prob = {
            '非常少': 0.05,
            '少': 0.1,
            '中': 0.2,
            '较多': 0.3,
            '多': 0.4,
            '非常多': 0.5
        }
    
    def 生成高度图(self, 地形区域=None, 初始高度=None):
        """生成地形高度图，所有地形从世界高度的2/5开始生成
        
        参数：
            地形区域：列表，包含多个(开始x, 结束x, 地形类型)的元组，用于混合地形生成
            初始高度：上一个区块的结束高度，用于无限世界的连续地形生成
        """
        高度图 = [0] * self.世界宽度
        
        # 从世界高度的2/5开始生成，如果提供了初始高度则使用初始高度
        基础高度 = int(self.世界高度 * 2 / 5)
        目标高度 = 基础高度  # 用于从高山地形切换到其他地形时的目标高度
        
        # 初始高度（整数）
        current_height = 初始高度 if 初始高度 is not None else 基础高度
        
        # 为每个x位置生成高度
        for x in range(self.世界宽度):
            # 确定当前位置的地形类型
            当前地形类型 = self.地形_type
            if 地形区域:
                # 查找当前x位置所在的地形区域
                for (start_x, end_x, 区域地形类型) in 地形区域:
                    if start_x <= x < end_x:
                        当前地形类型 = 区域地形类型
                        break
            
            # 随机决定高度变化
            rand = random.random()
            if 当前地形类型 == '高山':
                # 高山地形：40%向上，14%向下，46%不变
                if rand < 0.4:  # 40%向上
                    current_height += 1
                elif rand < 0.54:  # 14%向下
                    current_height -= 1
                # 剩下的46%保持当前高度
            else:
                # 其他地形：14%向上，14%向下，74%不变
                # 如果之前是高山地形，现在切换到其他地形，需要强行下降到2/5正确起伏区
                if x > 0:
                    # 检查前一个位置的地形类型
                    前一个地形类型 = self.地形_type
                    if 地形区域:
                        for (start_x, end_x, 区域地形类型) in 地形区域:
                            if start_x <= x-1 < end_x:
                                前一个地形类型 = 区域地形类型
                                break
                    
                    # 如果前一个是高山地形，现在不是，需要强行调整到目标高度
                    if 前一个地形类型 == '高山' and 当前地形类型 != '高山':
                        # 强行下降到目标高度
                        if current_height > 目标高度:
                            current_height = max(current_height - 2, 目标高度)  # 每次最多下降2格
                    
                # 正常地形的高度变化
                if rand < 0.14:  # 14%向上
                    current_height += 1
                elif rand < 0.28:  # 14%向下
                    current_height -= 1
                # 剩下的74%保持当前高度
            
            # 限制高度范围，确保不超出合理范围
            min_height = int(self.世界高度 * 1 / 5)  # 最低高度为世界高度的1/5
            max_height = int(self.世界高度 * 4 / 5)  # 最高高度为世界高度的4/5
            current_height = max(min_height, min(current_height, max_height))
            
            # 保存当前高度
            高度图[x] = current_height
        
        return 高度图
    
    def 生成_草方块地形(self, 方块数组, 高度图, x, 地表_y):
        """生成草方块地表的地形"""
        # 地表草方块
        方块数组[地表_y][x] = 草方块
        
        # 泥土层 (3层)
        for y in range(地表_y + 1, 地表_y + 4):
            if y < self.世界高度:
                方块数组[y][x] = 土块
        
        # 黑土层 (3层)
        for y in range(地表_y + 4, 地表_y + 7):
            if y < self.世界高度:
                方块数组[y][x] = 黑土块
    
    def 生成_沙子地形(self, 方块数组, 高度图, x, 地表_y):
        """生成沙子地表的地形"""
        # 地表沙子 (1层)
        方块数组[地表_y][x] = 沙子
        
        # 沙子层 (3层)
        for y in range(地表_y + 1, 地表_y + 4):
            if y < self.世界高度:
                方块数组[y][x] = 沙子
        
        # 土块层 (3层)
        for y in range(地表_y + 4, 地表_y + 7):
            if y < self.世界高度:
                方块数组[y][x] = 土块
    
    def 生成矿石层(self, 方块数组, 高度图, x):
        """生成矿石层"""
        地表_y = 高度图[x]
        
        # 低级矿石层 (黑土层下，少量)
        for y in range(地表_y + 7, 地表_y + 15):
            if y < self.世界高度:
                if random.random() < 0.05:
                    矿石类型 = random.choice([煤矿, 铜矿石])
                    方块数组[y][x] = 矿石类型
                else:
                    方块数组[y][x] = 岩石
        
        # 中级矿石层 (中级深度，中等数量)
        for y in range(地表_y + 15, 地表_y + 25):
            if y < self.世界高度:
                if random.random() < 0.1:
                    矿石类型 = random.choice([铁矿石, 铜矿石])
                    方块数组[y][x] = 矿石类型
                else:
                    方块数组[y][x] = 岩石
        
        # 高级矿石层 (深层，较多数量)
        for y in range(地表_y + 25, self.世界高度 - 3):
            if y < self.世界高度:
                if random.random() < 0.15:
                    矿石类型 = random.choice([金矿石, 钻石矿石, 铁矿石])
                    方块数组[y][x] = 矿石类型
                else:
                    方块数组[y][x] = 岩石
    
    def 生成基岩层(self, 方块数组):
        """生成基岩层"""
        for x in range(self.世界宽度):
            for y in range(self.世界高度 - 3, self.世界高度):
                if y < self.世界高度:
                    方块数组[y][x] = 基岩
    
    def 生成_普通树木(self, 方块数组, 高度图, x):
        """生成普通树木（4-8高，宽1）"""
        地表_y = 高度图[x]
        
        # 检查是否在草方块上
        if 方块数组[地表_y][x] != 草方块:
            return False
        
        # 生成树干
        树高 = random.randint(4, 8)
        
        # 只检查树干和树叶要生成的位置是否有空间
        # 检查树干空间（1x树高）
        for y in range(地表_y - 树高, 地表_y):
            if y >= 0 and y < self.世界高度:
                if 方块数组[y][x] != 空气:
                    return False
        
        # 生成树干
        for y in range(地表_y - 树高, 地表_y):
            if y >= 0:
                方块数组[y][x] = 木头
        
        # 生成树叶（顶部和周围）
        树叶范围 = 3  # 增加树叶范围到3，生成5x5的树冠
        for dx in range(-树叶范围, 树叶范围 + 1):
            for dy in range(-树叶范围, 3):  # 增加dy范围，生成3层树叶
                leaf_x = x + dx
                leaf_y = 地表_y - 树高 + dy
                if 0 <= leaf_x < self.世界宽度 and leaf_y >= 0:
                    # 计算树叶到树干的距离，距离越近，生成概率越高
                    distance = abs(dx) + abs(dy)
                    if distance <= 4:  # 只在树干周围4格内生成树叶
                        # 距离越近，生成概率越高
                        leaf_prob = 0.95  # 95%概率生成树叶，几乎全覆盖
                        if random.random() < leaf_prob:
                            方块数组[leaf_y][leaf_x] = 树叶
        
        return True
    
    def 生成_乔木(self, 方块数组, 高度图, x):
        """生成乔木（5-12高，3-5粗）"""
        地表_y = 高度图[x]
        
        # 检查是否在草方块上
        if 方块数组[地表_y][x] != 草方块:
            return False
        
        # 生成树干
        树高 = random.randint(5, 12)
        树粗 = random.randint(3, 5)
        
        # 检查周围是否有空间
        half_width = 树粗 // 2
        for dx in range(-half_width, half_width + 1):
            for dy in range(0, 树高 + 5):
                check_x = x + dx
                check_y = 地表_y - dy
                if 0 <= check_x < self.世界宽度 and 0 <= check_y < self.世界高度:
                    if 方块数组[check_y][check_x] != 空气 and check_y < 地表_y:
                        return False
        
        # 生成树干（3-5粗）
        half_width = 树粗 // 2
        for dx in range(-half_width, half_width + 1):
            for y in range(地表_y - 树高, 地表_y):
                if y >= 0 and 0 <= x + dx < self.世界宽度:
                    方块数组[y][x + dx] = 乔木
        
        # 生成乔木叶（大量）
        树叶范围 = 3
        for dx in range(-树叶范围, 树叶范围 + 1):
            for dy in range(-树叶范围, 2):
                leaf_x = x + dx
                leaf_y = 地表_y - 树高 + dy
                if 0 <= leaf_x < self.世界宽度 and leaf_y >= 0:
                    if random.random() < 0.9:  # 90%概率生成树叶
                        方块数组[leaf_y][leaf_x] = 乔木叶
                    elif random.random() < 0.1:  # 10%概率生成乔木果
                        方块数组[leaf_y][leaf_x] = 乔木果
        
        return True
    
    def 生成_仙人掌(self, 方块数组, 高度图, x):
        """生成仙人掌（1-3高）"""
        地表_y = 高度图[x]
        
        # 检查是否在沙子上
        if 方块数组[地表_y][x] != 沙子:
            return False
        
        # 检查上方是否有空间（只检查仙人掌要生成的位置）
        高度 = random.randint(1, 3)
        for dy in range(1, 高度 + 1):
            check_y = 地表_y - dy
            if check_y >= 0:
                if 方块数组[check_y][x] != 空气:
                    return False
        
        # 生成仙人掌
        for y in range(地表_y - 高度, 地表_y):
            if y >= 0:
                方块数组[y][x] = 仙人掌
        
        return True
    
    def 生成_植物(self, 方块数组, 高度图):
        """生成植物（草、花、灌木等）"""
        for x in range(self.世界宽度):
            地表_y = 高度图[x]
            
            # 根据地形类型生成不同植物
            if self.地形_type in ['森林', '草原', '高山']:
                # 生成草
                if 方块数组[地表_y][x] == 草方块:
                    概率 = self.数量_prob.get(self.当前参数['草数量'], 0.1)
                    if random.random() < 概率:
                        if 方块数组[地表_y - 1][x] == 空气:
                            方块数组[地表_y - 1][x] = 草
                
                # 生成花
                概率 = self.数量_prob.get(self.当前参数['花数量'], 0.05)
                if random.random() < 概率:
                    if 方块数组[地表_y][x] == 草方块 and 方块数组[地表_y - 1][x] == 空气:
                        方块数组[地表_y - 1][x] = 红花
                
                # 生成树木
                概率 = self.数量_prob.get(self.当前参数['木头数量'], 0.1)
                if random.random() < 概率:
                    self.生成_普通树木(方块数组, 高度图, x)
            
            elif self.地形_type == '沙漠':
                # 生成仙人掌
                概率 = self.数量_prob.get(self.当前参数['仙人掌数量'], 0.1)
                if random.random() < 概率:
                    self.生成_仙人掌(方块数组, 高度图, x)
                
                # 生成枯草
                概率 = self.数量_prob.get(self.当前参数['枯草数量'], 0.2)
                if random.random() < 概率:
                    if 方块数组[地表_y][x] == 沙子 and 方块数组[地表_y - 1][x] == 空气:
                        方块数组[地表_y - 1][x] = 枯草
            
            elif self.地形_type == '雨林':
                # 生成灌木
                概率 = self.数量_prob.get(self.当前参数['灌木数量'], 0.1)
                if random.random() < 概率:
                    if 方块数组[地表_y][x] == 草方块 and 方块数组[地表_y - 1][x] == 空气:
                        方块数组[地表_y - 1][x] = 灌木
                
                # 生成草
                概率 = self.数量_prob.get(self.当前参数['草数量'], 0.05)
                if random.random() < 概率:
                    if 方块数组[地表_y][x] == 草方块 and 方块数组[地表_y - 1][x] == 空气:
                        方块数组[地表_y - 1][x] = 草
                
                # 生成花
                概率 = self.数量_prob.get(self.当前参数['花数量'], 0.02)
                if random.random() < 概率:
                    if 方块数组[地表_y][x] == 草方块 and 方块数组[地表_y - 1][x] == 空气:
                        方块数组[地表_y - 1][x] = 红花
                
                # 生成乔木
                概率 = self.数量_prob.get(self.当前参数['乔木数量'], 0.1)
                if random.random() < 概率:
                    self.生成_乔木(方块数组, 高度图, x)
    
    def 生成地形(self):
        """生成完整地形"""
        # 初始化方块数组
        方块数组 = [[空气 for _ in range(self.世界宽度)] for _ in range(self.世界高度)]
        
        # 生成高度图
        高度图 = self.生成高度图()
        
        # 生成基础地形
        for x in range(self.世界宽度):
            地表_y = 高度图[x]
            
            if self.地形_type == '沙漠':
                # 沙漠地形：沙子地表
                self.生成_沙子地形(方块数组, 高度图, x, 地表_y)
            else:
                # 其他地形：草方块地表
                self.生成_草方块地形(方块数组, 高度图, x, 地表_y)
            
            # 生成矿石层
            self.生成矿石层(方块数组, 高度图, x)
        
        # 生成基岩层
        self.生成基岩层(方块数组)
        
        # 生成水和岩浆
        self.生成_水和岩浆(方块数组, 高度图)
        
        # 生成植物
        self.生成_植物(方块数组, 高度图)
        
        return 方块数组
    
    def 生成_水和岩浆(self, 方块数组, 高度图):
        """生成水和岩浆"""
        for x in range(self.世界宽度):
            地表_y = 高度图[x]
            
            # 生成水
            # 在低洼地区生成水，概率较低
            if random.random() < 0.03:  # 3%概率生成水
                # 查找低洼地区
                # 检查当前位置是否低于左右两侧
                left_height = 地表_y
                right_height = 地表_y
                if x > 0:
                    left_height = 高度图[x - 1]
                if x < self.世界宽度 - 1:
                    right_height = 高度图[x + 1]
                
                # 如果当前位置低于左右两侧，且不是在高山上，生成水
                if 地表_y < left_height and 地表_y < right_height and 地表_y < int(self.世界高度 * 3 / 5):
                    # 生成水，从地表向下填充
                    water_height = 地表_y - random.randint(1, 3)  # 水的高度比地表低1-3格
                    # 填充水
                    for y in range(water_height, 地表_y):
                        if 0 <= y < self.世界高度:
                            方块数组[y][x] = 水
                            # 向左右扩展水
                            for dx in range(-2, 3):
                                nx = x + dx
                                if 0 <= nx < self.世界宽度:
                                    # 检查是否在合理范围内
                                    if 0 <= y < self.世界高度:
                                        # 有一定概率向左右扩展
                                        if random.random() < 0.7:  # 70%概率扩展
                                            方块数组[y][nx] = 水
            
            # 生成岩浆
            # 在深层地下生成岩浆，概率很低
            if random.random() < 0.01:  # 1%概率生成岩浆
                # 岩浆生成在地下深处
                lava_y = 地表_y + random.randint(10, 30)  # 岩浆在地表下10-30格
                if lava_y < self.世界高度 - 5:  # 确保在基岩上方
                    # 生成岩浆池
                    for dy in range(0, 5):  # 岩浆池深度5格
                        for dx in range(-3, 4):  # 岩浆池宽度7格
                            ny = lava_y + dy
                            nx = x + dx
                            if 0 <= nx < self.世界宽度 and 0 <= ny < self.世界高度:
                                # 有一定概率生成岩浆
                                if random.random() < 0.8:  # 80%概率生成岩浆
                                    方块数组[ny][nx] = 岩浆
    
    def 生成区块地形(self, chunk_x, chunk_y):
        """生成区块地形（用于无限世界）"""
        # 此方法用于无限世界的区块生成
        # 实现逻辑类似，但是针对单个区块
        pass
    
    def 生成_混合地形(self, 初始高度=None):
        """生成混合地形，包含多种地形类型，共享同一个高度图
        
        参数：
            初始高度：上一个区块的结束高度，用于无限世界的连续地形生成
        """
        # 初始化方块数组
        方块数组 = [[空气 for _ in range(self.世界宽度)] for _ in range(self.世界高度)]
        
        # 地形类型列表
        地形类型列表 = ['森林', '草原', '高山', '沙漠', '雨林']
        
        # 将世界划分为多个地形区域
        区域大小 = random.randint(150, 300)  # 每个地形区域的大小
        区域列表 = []
        
        x = 0
        while x < self.世界宽度:
            # 随机选择一个地形类型
            地形类型 = random.choice(地形类型列表)
            # 随机选择区域大小
            current_size = random.randint(区域大小 // 2, 区域大小)
            # 添加到区域列表
            区域列表.append((x, min(x + current_size, self.世界宽度), 地形类型))
            x += current_size
        
        # 生成统一的高度图（所有区域共享），传入地形区域信息和初始高度
        高度图 = self.生成高度图(区域列表, 初始高度)
        
        # 为每个区域生成地形
        for start_x, end_x, 地形类型 in 区域列表:
            # 区域宽度
            区域宽度 = end_x - start_x
            
            # 初始化区域方块数组
            区域方块 = [[空气 for _ in range(区域宽度)] for _ in range(self.世界高度)]
            
            # 为区域内的每个x位置生成地形
            for local_x in range(区域宽度):
                world_x = start_x + local_x
                地表_y = 高度图[world_x]
                
                # 根据地形类型生成不同的地表和地下结构
                if 地形类型 == '沙漠':
                    # 沙漠地形：沙子地表
                    # 地表沙子 (1层)
                    区域方块[地表_y][local_x] = 沙子
                    # 沙子层 (3层)
                    for y in range(地表_y + 1, 地表_y + 4):
                        if y < self.世界高度:
                            区域方块[y][local_x] = 沙子
                    # 土块层 (3层)
                    for y in range(地表_y + 4, 地表_y + 7):
                        if y < self.世界高度:
                            区域方块[y][local_x] = 土块
                else:
                    # 其他地形：草方块地表
                    # 地表草方块
                    区域方块[地表_y][local_x] = 草方块
                    # 泥土层 (3层)
                    for y in range(地表_y + 1, 地表_y + 4):
                        if y < self.世界高度:
                            区域方块[y][local_x] = 土块
                    # 黑土层 (3层)
                    for y in range(地表_y + 4, 地表_y + 7):
                        if y < self.世界高度:
                            区域方块[y][local_x] = 黑土块
                
                # 生成矿石层
                # 低级矿石层 (黑土层下，少量)
                for y in range(地表_y + 7, 地表_y + 15):
                    if y < self.世界高度:
                        if random.random() < 0.05:
                            矿石类型 = random.choice([煤矿, 铜矿石])
                            区域方块[y][local_x] = 矿石类型
                        else:
                            区域方块[y][local_x] = 岩石
                # 中级矿石层 (中级深度，中等数量)
                for y in range(地表_y + 15, 地表_y + 25):
                    if y < self.世界高度:
                        if random.random() < 0.1:
                            矿石类型 = random.choice([铁矿石, 铜矿石])
                            区域方块[y][local_x] = 矿石类型
                        else:
                            区域方块[y][local_x] = 岩石
                # 高级矿石层 (深层，较多数量)
                for y in range(地表_y + 25, self.世界高度 - 3):
                    if y < self.世界高度:
                        if random.random() < 0.15:
                            矿石类型 = random.choice([金矿石, 钻石矿石, 铁矿石])
                            区域方块[y][local_x] = 矿石类型
                        else:
                            区域方块[y][local_x] = 岩石
            
            # 生成基岩层
            for local_x in range(区域宽度):
                for y in range(self.世界高度 - 3, self.世界高度):
                    if y < self.世界高度:
                        区域方块[y][local_x] = 基岩
            
            # 生成植物
            # 创建临时生成器，用于生成植物
            临时生成器 = 地形生成器(区域宽度, self.世界高度, 地形类型, self.无限世界)
            # 为区域生成植物
            临时生成器.生成_植物(区域方块, 高度图[start_x:end_x])
            
            # 将区域方块数据复制到主方块数组
            for x in range(start_x, end_x):
                local_x = x - start_x
                for y in range(self.世界高度):
                    方块数组[y][x] = 区域方块[y][local_x]
        
        # 生成水和岩浆
        self.生成_水和岩浆(方块数组, 高度图)
        
        # 保存高度图的结束高度，用于下一个区块的地形生成
        self.结束高度 = 高度图[-1] if 高度图 else int(self.世界高度 * 2 / 5)
        
        return 方块数组


def 生成地形(世界宽度, 世界高度, 地形类型="森林", 无限世界=False, 初始高度=None):
    """生成地形的主函数
    
    参数：
        世界宽度：地形宽度
        世界高度：地形高度
        地形类型：地形类型，"混合"表示混合地形，"平坦世界"表示平坦地形
        无限世界：是否为无限世界
        初始高度：上一个区块的结束高度，用于无限世界的连续地形生成
    
    返回：
        方块数组：生成的地形方块数组
        结束高度：当前地形的结束高度，用于下一个区块的地形生成
    """
    if 地形类型 == "混合":
        # 生成混合地形
        生成器 = 地形生成器(世界宽度, 世界高度, "森林", 无限世界)
        方块数组 = 生成器.生成_混合地形(初始高度)
        结束高度 = 生成器.结束高度
        return 方块数组, 结束高度
    elif 地形类型 == "平坦世界":
        # 生成平坦地形
        方块数组 = [[空气 for _ in range(世界宽度)] for _ in range(世界高度)]
        
        # 平坦世界的固定高度（世界高度的3/5）
        平坦高度 = int(世界高度 * 3 / 5)
        
        for x in range(世界宽度):
            # 地表草方块
            方块数组[平坦高度][x] = 草方块
            
            # 泥土层 (3层)
            for y in range(平坦高度 + 1, 平坦高度 + 4):
                if y < 世界高度:
                    方块数组[y][x] = 土块
            
            # 石头层
            for y in range(平坦高度 + 4, 世界高度 - 3):
                if y < 世界高度:
                    方块数组[y][x] = 岩石
            
            # 基岩层 (3层)
            for y in range(世界高度 - 3, 世界高度):
                if y < 世界高度:
                    方块数组[y][x] = 基岩
        
        # 平坦世界的结束高度就是平坦高度
        结束高度 = 平坦高度
        return 方块数组, 结束高度
    else:
        # 生成单一地形
        生成器 = 地形生成器(世界宽度, 世界高度, 地形类型, 无限世界)
        方块数组 = 生成器.生成地形()
        # 计算结束高度
        结束高度 = int(世界高度 * 2 / 5)  # 单一地形的结束高度默认为基础高度
        return 方块数组, 结束高度
