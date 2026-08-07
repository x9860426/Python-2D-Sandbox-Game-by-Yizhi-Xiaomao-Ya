import pygame
import sys
import os
# 导入游玩模块
import 游玩
# 导入音频管理器
from 音频输出 import audio_manager
# 导入加载窗口
from 加载窗口 import 加载窗口
# 导入图片管理器全局实例
from 图片加载 import 图片管理器

class 创建世界界面:
    def __init__(self, 屏幕):
        # 单例模式实现
        if hasattr(self.__class__, '_instance'):
            self.__class__._instance = self
        else:
            self.__class__._instance = self
            
        self.屏幕 = 屏幕
        
        # 使用图片加载器获取背景图片
        self.background_image = None
        
        # 主题配色方案
        self.背景颜色 = (240, 240, 240)
        self.面板背景颜色 = (250, 250, 250)
        self.面板边框颜色 = (200, 200, 200)
        
        # 按钮配置
        self.按钮颜色 = (230, 230, 230)
        self.按钮悬停颜色 = (240, 240, 240)
        self.按钮选中颜色 = (220, 220, 220)
        self.按钮边框颜色 = (200, 200, 200)
        # 绿色按钮配色 - 用于创建世界按钮
        self.创建世界按钮正常颜色 = (61, 245, 84)  # 绿色
        self.创建世界按钮悬停颜色 = (81, 255, 104)  # 亮绿色（悬停）
        self.创建世界按钮按下颜色 = (41, 225, 64)  # 暗绿色（按下）
        self.创建世界按钮边框颜色 = (31, 205, 54)  # 深绿色边框
        
        # 按钮按下状态变量（用于动画效果）
        self.存档按钮被按下 = False
        self.世界宽度按钮被按下 = False
        self.世界高度按钮被按下 = False
        # 创建世界按钮状态
        self.创建世界按钮悬停 = False
        self.创建世界按钮按下 = False
        self.按钮按下时间 = 0
        self.按钮按下持续时间 = 100  # 按钮按下动画持续时间（毫秒）
        
        # 字体设置 - 使用与主程序一致的字体（大字体），大小增加5
        pygame.font.init()
        try:
            # 使用与方块世界相同的字体样式，但大小增加5
            self.标题字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 45, bold=True)  
            self.按钮字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 20)
            self.文本字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 20)  # 存档名称字体增加2
        except:
            self.标题字体 = pygame.font.SysFont('Arial', 72 + 5, bold=True)
            self.按钮字体 = pygame.font.SysFont('Arial', 20)
            self.文本字体 = pygame.font.SysFont('Arial', 18)
        
        # 初始化存档名称相关属性
        self.存档名称 = self._get_default_save_name()  # 自动检测并设置默认存档名称
        self.原始存档名称 = self.存档名称  # 保存原始存档名称用于恢复
        self.输入框处于焦点 = False  # 输入框焦点状态
        
        # 初始化世界宽度相关属性
        self.世界宽度 = 2000  # 默认宽度为2000
        self.世界宽度输入框处于焦点 = False  # 世界宽度输入框焦点状态
        self.世界宽度输入文本 = str(self.世界宽度)
        
        # 初始化世界高度相关属性
        self.世界高度 = 250  # 默认高度为250
        self.世界高度输入框处于焦点 = False  # 世界高度输入框焦点状态
        self.世界高度输入文本 = str(self.世界高度)
        
        # 初始化世界类型相关属性
        self.世界类型选项 = ["随机世界", "平坦世界"]  # 世界类型选项
        self.当前世界类型 = self.世界类型选项[0]  # 默认选择第一个选项
        self.下拉框处于焦点 = False  # 下拉框焦点状态
        self.下拉框展开 = False  # 下拉框展开状态
        
        # 开关按钮状态常量定义
        self.开关_关闭 = False
        self.开关_开启 = True
        
        # 初始化三个开关按钮状态
        self.创造模式开关 = self.开关_开启  # 创造模式开关状态（默认为开启）
        self.创建存档开关 = self.开关_关闭  # 创建存档开关状态（默认为关闭）
        self.无限世界开关 = self.开关_关闭  # 无限世界开关状态（默认为关闭）
        
        # 开关按钮样式参数
        self.开关样式参数 = {
            "背景": {
                "关闭": (213, 213, 213),  # 灰色
                "开启": (84, 245, 61)   # 绿色
            },
            "圆形": {
                "半径": 15,
                "圆心_y": 20,
                "颜色": (255, 255, 255)
            },
            "背景形状": {
                "宽度": 85,
                "高度": 40,
                "圆角半径": 18
            }
        }
        
        # 先更新尺寸，然后初始化UI元素
        self.更新尺寸()
    
    def 更新尺寸(self):
        # 获取屏幕尺寸
        self.屏幕宽度, self.屏幕高度 = self.屏幕.get_size()
        
        # 计算底1（左侧面板）和底2（右侧面板）的位置和尺寸
        self.底1宽度 = max(200, int(self.屏幕宽度 * 0.2))  # 左侧面板宽度
        self.底2宽度 = self.屏幕宽度 - self.底1宽度 - 30  # 右侧面板宽度
        self.底高度 = self.屏幕高度 - 50  # 面板高度
        self.底_x = 20  # 左侧面板x坐标
        self.底1_x = self.底_x  # 左侧面板x坐标
        self.底2_x = self.底_x + self.底1宽度 + 10  # 右侧面板x坐标
        self.底_y = 25  # 面板y坐标
        
        # 初始化输入框和按钮位置
        self.初始化输入框()
        self.初始化按钮()
    
    def _get_default_save_name(self):
        """检测存档文件夹中现有文件，返回合适的默认存档名称"""
        # 获取代码文件所在目录
        import os
        代码目录 = os.path.dirname(os.path.abspath(__file__))
        # 存档文件夹路径：代码目录/存档
        存档文件夹 = os.path.join(代码目录, "存档")
        
        # 检查存档文件夹是否存在，不存在则创建
        if not os.path.exists(存档文件夹):
            os.makedirs(存档文件夹)
            return "New World 1"
        
        # 获取存档文件夹中的所有文件和文件夹
        现有文件 = os.listdir(存档文件夹)
        
        # 找出所有符合"New World X"格式的存档
        存档编号 = []
        基础名称 = "New World "
        
        for 文件 in 现有文件:
            # 检查文件名是否以"New World "开头并且后面是数字
            if 文件.startswith(基础名称):
                # 尝试提取数字部分
                数字部分 = 文件[len(基础名称):]
                if 数字部分.isdigit():
                    存档编号.append(int(数字部分))
        
        # 如果没有找到匹配的存档，返回"New World 1"
        if not 存档编号:
            return "New World 1"
        
        # 找到最大的编号并加1
        最大编号 = max(存档编号)
        return f"New World {最大编号 + 1}"
            
    def 初始化输入框(self):
        # 存档名称输入框位置和尺寸
        self.输入框_x = (self.屏幕宽度 - 275) // 2  # 水平居中
        self.输入框_y = 120  # 在标题文字下方
        self.输入框宽度 = 275  # 输入框缩短15像素
        self.输入框高度 = 35
        self.输入框_rect = pygame.Rect(self.输入框_x, self.输入框_y, self.输入框宽度, self.输入框高度)
        
        # 存档名称标签位置
        self.标签_x = self.输入框_x - 100
        self.标签_y = self.输入框_y + 5
        
        # 世界宽度输入框位置和尺寸 - 在存档名称下方
        self.世界宽度输入框_x = (self.屏幕宽度 - 275) // 2  # 水平居中
        self.世界宽度输入框_y = self.输入框_y + 60  # 在存档名称下方60像素
        self.世界宽度输入框_width = 275
        self.世界宽度输入框_height = 35
        self.世界宽度输入框_rect = pygame.Rect(
            self.世界宽度输入框_x, 
            self.世界宽度输入框_y, 
            self.世界宽度输入框_width, 
            self.世界宽度输入框_height
        )
        
        # 世界宽度标签位置
        self.世界宽度标签_x = self.世界宽度输入框_x - 100
        self.世界宽度标签_y = self.世界宽度输入框_y + 5
        
        # +按钮位置 - 在世界宽度输入框右侧
        self.增加宽度按钮_rect = pygame.Rect(
            self.世界宽度输入框_x + 290,  # 在输入框右侧
            self.世界宽度输入框_y,  # 与输入框同一行
            35,  # 按钮宽度（改为正方形）
            35   # 按钮高度
        )
        
        # 世界高度输入框位置和尺寸 - 在世界宽度下方
        self.世界高度输入框_x = (self.屏幕宽度 - 275) // 2  # 水平居中
        self.世界高度输入框_y = self.世界宽度输入框_y + 60  # 在世界宽度下方60像素
        self.世界高度输入框_width = 275
        self.世界高度输入框_height = 35
        self.世界高度输入框_rect = pygame.Rect(
            self.世界高度输入框_x, 
            self.世界高度输入框_y, 
            self.世界高度输入框_width, 
            self.世界高度输入框_height
        )
        
        # 世界高度标签位置
        self.世界高度标签_x = self.世界高度输入框_x - 100
        self.世界高度标签_y = self.世界高度输入框_y + 5
        
        # +按钮位置 - 在世界高度输入框右侧
        self.增加高度按钮_rect = pygame.Rect(
            self.世界高度输入框_x + 290,  # 在输入框右侧
            self.世界高度输入框_y,  # 与输入框同一行
            35,  # 按钮宽度（改为正方形）
            35   # 按钮高度
        )
        
        # 世界类型标签位置
        self.世界类型标签_x = self.世界宽度输入框_x - 100
        self.世界类型标签_y = self.世界高度输入框_y + 60  # 在世界高度下方60像素
        
        # 世界类型下拉框位置和尺寸
        self.世界类型下拉框_x = (self.屏幕宽度 - 275) // 2  # 水平居中
        self.世界类型下拉框_y = self.世界类型标签_y  # 与标签同一行
        self.世界类型下拉框_width = 275
        self.世界类型下拉框_height = 35
        self.世界类型下拉框_rect = pygame.Rect(
            self.世界类型下拉框_x, 
            self.世界类型下拉框_y, 
            self.世界类型下拉框_width, 
            self.世界类型下拉框_height
        )
        
        # 下拉选项区域位置和尺寸
        self.下拉选项区域_rect = pygame.Rect(
            self.世界类型下拉框_x, 
            self.世界类型下拉框_y + self.世界类型下拉框_height, 
            self.世界类型下拉框_width, 
            len(self.世界类型选项) * self.世界类型下拉框_height
        )
        
        # 开关按钮位置和尺寸 - 在世界类型下面一行，三个按钮水平排列
        self.开关按钮_y = self.世界类型下拉框_y + 80  # 在世界类型下拉框下方，向下移动10像素
        self.开关按钮_width = 64  # 按钮再减小20%
        self.开关按钮_height = 32  # 按钮再减小20%
        self.开关按钮间距 = 40  # 按钮间距
        
        # 计算总宽度，使三个按钮居中显示
        总宽度 = 3 * self.开关按钮_width + 2 * self.开关按钮间距
        起始_x = (self.屏幕宽度 - 总宽度) // 2
        
        # 创造模式开关按钮
        self.创造模式开关_rect = pygame.Rect(
            起始_x, 
            self.开关按钮_y,
            self.开关按钮_width,
            self.开关按钮_height
        )
        self.创造模式标签_x = 起始_x + self.开关按钮_width // 2  # 文字左右中心对齐按钮
        self.创造模式标签_y = self.开关按钮_y - 37  # 标签向上移动15像素
        
        # 创建存档开关按钮
        self.创建存档开关_rect = pygame.Rect(
            起始_x + self.开关按钮_width + self.开关按钮间距,
            self.开关按钮_y,
            self.开关按钮_width,
            self.开关按钮_height
        )
        self.创建存档标签_x = 起始_x + self.开关按钮_width + self.开关按钮间距 + self.开关按钮_width // 2  # 文字左右中心对齐按钮
        self.创建存档标签_y = self.开关按钮_y - 37  # 标签向上移动15像素
        
        # 无限世界开关按钮
        self.无限世界开关_rect = pygame.Rect(
            起始_x + 2 * (self.开关按钮_width + self.开关按钮间距),
            self.开关按钮_y,
            self.开关按钮_width,
            self.开关按钮_height
        )
        self.无限世界标签_x = 起始_x + 2 * (self.开关按钮_width + self.开关按钮间距) + self.开关按钮_width // 2  # 文字左右中心对齐按钮
        self.无限世界标签_y = self.开关按钮_y - 37  # 标签向上移动15像素
    
    def 初始化按钮(self):
        # 按钮尺寸
        self.按钮宽度 = self.底1宽度 - 40  # 按钮宽度
        self.按钮高度 = 40  # 按钮高度
        self.按钮间距 = 10  # 按钮间距
        
        # 左上角返回按钮
        self.左上角返回按钮 = pygame.Rect(
            20,  # 距离左侧20px
            20,  # 距离顶部20px
            80,  # 宽度
            40  # 高度
        )
        
        # 创建世界按钮
        self.创建世界按钮 = pygame.Rect(
            self.底2_x + (self.底2宽度 - 200) // 2,  # 水平居中
            self.底_y + self.底高度 - 80,  # 底部上方
            200,  # 宽度
            45  # 高度
        )
        
        # 存档相关按钮 - 调整到输入框右侧，改为正方形
        self.保存存档按钮 = pygame.Rect(
            (self.屏幕宽度 - 275) // 2 + 290,  # 在输入框右侧，根据新的输入框宽度调整
            120,  # 与输入框同一行
            35,  # 宽度 - 改为正方形，与高度相同
            35  # 高度 - 与输入框高度一致
        )
        
        # 新的创建世界按钮 - 左右居中，位置在创建存档下面
        self.新创建世界按钮_y = self.开关按钮_y + 100  # 在创建存档下面，距离开关按钮y坐标100像素
        self.新创建世界按钮 = pygame.Rect(
            (self.屏幕宽度 - 200) // 2,  # 水平居中
            self.新创建世界按钮_y,  # 垂直位置由变量控制
            200,  # 宽度
            45  # 高度
        )
    
    def 创建圆角矩形(self, x1, y1, x2, y2, 圆角半径):
        """创建圆角矩形的顶点列表，用于pygame.draw.polygon"""
        # 修正顶点计算，确保形成平滑的圆角矩形
        顶点 = []
        
        # 上边框
        顶点.append((x1 + 圆角半径, y1))
        顶点.append((x2 - 圆角半径, y1))
        
        # 右上圆角
        for i in range(1, 圆角半径):
            顶点.append((x2 - i, y1 + i))
        
        # 右边框
        顶点.append((x2, y1 + 圆角半径))
        顶点.append((x2, y2 - 圆角半径))
        
        # 右下圆角
        for i in range(圆角半径, 0, -1):
            顶点.append((x2 - i, y2 - i))
        
        # 下边框
        顶点.append((x2 - 圆角半径, y2))
        顶点.append((x1 + 圆角半径, y2))
        
        # 左下圆角
        for i in range(1, 圆角半径):
            顶点.append((x1 + i, y2 - i))
        
        # 左边框
        顶点.append((x1, y2 - 圆角半径))
        顶点.append((x1, y1 + 圆角半径))
        
        # 左上圆角
        for i in range(圆角半径, 0, -1):
            顶点.append((x1 + i, y1 + i))
        
        return 顶点
    
    def 绘制开关按钮(self, x, y, 状态, 变暗=False):
        """绘制单个开关按钮，参考历史程序文件中的形状
        参数:
            x, y: 按钮位置
            状态: 按钮状态
            变暗: 是否将按钮色调加30%黑
        """
        # 获取样式参数
        背景形状 = self.开关样式参数["背景形状"]
        圆形 = self.开关样式参数["圆形"]
        
        # 计算背景位置
        背景_x1 = x + (self.开关按钮_width - 背景形状["宽度"]) // 2
        背景_y1 = y + (self.开关按钮_height - 背景形状["高度"]) // 2
        背景_x2 = 背景_x1 + 背景形状["宽度"]
        背景_y2 = 背景_y1 + 背景形状["高度"]
        
        # 获取背景颜色
        背景颜色 = self.开关样式参数["背景"]["开启"] if 状态 else self.开关样式参数["背景"]["关闭"]
        
        # 如果需要变暗，将颜色各通道减少30%
        if 变暗:
            背景颜色 = tuple(max(0, int(c * 0.7)) for c in 背景颜色)
        
        # 绘制圆角背景（使用pygame的draw.rect代替polygon以确保更平滑的圆角）
        pygame.draw.rect(self.屏幕, 背景颜色, (背景_x1, 背景_y1, 背景_x2 - 背景_x1, 背景_y2 - 背景_y1), border_radius=背景形状["圆角半径"])
        
        # 绘制边框
        pygame.draw.rect(self.屏幕, (0, 0, 0), (背景_x1, 背景_y1, 背景_x2 - 背景_x1, 背景_y2 - 背景_y1), 1, border_radius=背景形状["圆角半径"])
        
        # 计算圆形位置
        圆心_y = 背景_y1 + (背景_y2 - 背景_y1) // 2
        目标_x坐标 = 背景_x2 - 圆形["半径"] - 5 if 状态 else 背景_x1 + 圆形["半径"] + 5
        
        # 绘制圆形滑块
        pygame.draw.circle(self.屏幕, 圆形["颜色"], (int(目标_x坐标), int(圆心_y)), 圆形["半径"])
        
        # 绘制滑块边框
        pygame.draw.circle(self.屏幕, (100, 100, 100), (int(目标_x坐标), int(圆心_y)), 圆形["半径"], 1)
    
    def 绘制(self):
        # 绘制背景：尝试使用图片加载器获取背景图2，失败则使用蓝色渐变
        背景图片 = 图片管理器.获取图片("背景图2")
        if 背景图片 is not None:
            # 计算缩放比例，保持图片的原始宽高比
            图片宽度 = 背景图片.get_width()
            图片高度 = 背景图片.get_height()
            
            # 计算缩放后的尺寸，保持原始宽高比
            缩放比例 = max(self.屏幕宽度 / 图片宽度, self.屏幕高度 / 图片高度)
            新宽度 = int(图片宽度 * 缩放比例)
            新高度 = int(图片高度 * 缩放比例)
            
            # 缩放图片
            缩放背景图 = pygame.transform.scale(背景图片, (新宽度, 新高度))
            
            # 计算居中位置
            x = (self.屏幕宽度 - 新宽度) // 2
            y = (self.屏幕高度 - 新高度) // 2
            
            # 绘制背景图
            self.屏幕.blit(缩放背景图, (x, y))
        else:
            # 如果图片加载失败，使用与开始游戏页面相同的蓝色渐变
            渐变表面 = pygame.Surface((self.屏幕宽度, self.屏幕高度))
            for y in range(self.屏幕高度):
                # 从深蓝到浅蓝的垂直渐变
                r = 0
                g = 50 + int(y * 205 / self.屏幕高度)
                b = 100 + int(y * 155 / self.屏幕高度)
                pygame.draw.line(渐变表面, (r, g, b), (0, y), (self.屏幕宽度, y))
            self.屏幕.blit(渐变表面, (0, 0))
        
        # 绘制左上角返回按钮（红底）
        pygame.draw.rect(self.屏幕, (200, 50, 50), self.左上角返回按钮)  # 红色背景
        pygame.draw.rect(self.屏幕, (150, 20, 20), self.左上角返回按钮, 2)  # 深红色边框
        返回文本 = self.按钮字体.render("返回", True, (255, 255, 255))  # 白色文字
        文本_rect = 返回文本.get_rect(center=self.左上角返回按钮.center)
        self.屏幕.blit(返回文本, 文本_rect)
        
        # 绘制中心上方的"创建世界"文本 - 与方块世界相同的样式，带阴影效果
        文本中心_y = 80  # 适当调整垂直位置
        
        # 文字阴影
        阴影表面 = self.标题字体.render("创建世界", True, (0, 0, 0))
        阴影矩形 = 阴影表面.get_rect(center=(self.屏幕宽度 // 2, 文本中心_y))
        self.屏幕.blit(阴影表面, (阴影矩形.x + 3, 阴影矩形.y + 3))
        
        # 主文字
        
        # 在左下角显示分辨率提示文字
        提示字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 16)
        提示文字 = 提示字体.render("游戏由1920*1080(125%)页面开发可能有不兼容问题", True, (255, 255, 255))
        # 计算左下角位置，留出边距
        文字_x = 20
        文字_y = self.屏幕高度 - 提示文字.get_height() - 20
        # 添加半透明背景以提高可读性
        文字背景 = pygame.Surface((提示文字.get_width() + 10, 提示文字.get_height() + 6), pygame.SRCALPHA)
        文字背景.fill((0, 0, 0, 100))
        self.屏幕.blit(文字背景, (文字_x - 5, 文字_y - 3))
        # 绘制文字
        self.屏幕.blit(提示文字, (文字_x, 文字_y))
        创建世界文本 = self.标题字体.render("创建世界", True, (255, 255, 255))
        创建世界文本_rect = 创建世界文本.get_rect(center=(self.屏幕宽度 // 2, 文本中心_y))
        self.屏幕.blit(创建世界文本, 创建世界文本_rect)
        
        # 绘制存档名称标签
        存档标签 = self.文本字体.render("存档名称:", True, (255, 255, 255))
        self.屏幕.blit(存档标签, (self.标签_x, self.标签_y))
        
        # 绘制存档名称输入框
        # 输入框背景 - 焦点时为浅金色
        输入框颜色 = (255, 246, 143) if self.输入框处于焦点 else (230, 230, 230)
        pygame.draw.rect(self.屏幕, 输入框颜色, self.输入框_rect)
        # 输入框边框
        边框颜色 = (100, 150, 200) if self.输入框处于焦点 else (200, 200, 200)
        pygame.draw.rect(self.屏幕, 边框颜色, self.输入框_rect, 2)
        # 输入框文本
        存档名称_text = self.文本字体.render(self.存档名称, True, (0, 0, 0))
        # 绘制文本，添加一些内边距
        self.屏幕.blit(存档名称_text, (self.输入框_x + 5, self.输入框_y + 5))
        
        # 处理按钮动画状态
        current_time = pygame.time.get_ticks()
        if self.存档按钮被按下 and current_time - self.按钮按下时间 > self.按钮按下持续时间:
            self.存档按钮被按下 = False
        if self.世界宽度按钮被按下 and current_time - self.按钮按下时间 > self.按钮按下持续时间:
            self.世界宽度按钮被按下 = False
        if self.世界高度按钮被按下 and current_time - self.按钮按下时间 > self.按钮按下持续时间:
            self.世界高度按钮被按下 = False
        
        # 绘制存档名称+按钮
        存档按钮颜色 = (150, 150, 150) if self.存档按钮被按下 else self.按钮颜色
        pygame.draw.rect(self.屏幕, 存档按钮颜色, self.保存存档按钮)
        pygame.draw.rect(self.屏幕, self.按钮边框颜色, self.保存存档按钮, 2)
        按钮文本 = self.按钮字体.render("+", True, (0, 0, 0))
        按钮文本_rect = 按钮文本.get_rect(center=self.保存存档按钮.center)
        self.屏幕.blit(按钮文本, 按钮文本_rect)
        
        # 绘制世界宽度标签
        世界宽度标签 = self.文本字体.render("世界宽度:", True, (255, 255, 255))
        self.屏幕.blit(世界宽度标签, (self.世界宽度标签_x, self.世界宽度标签_y))
        
        # 绘制世界宽度输入框
        # 输入框背景 - 焦点时为浅金色
        世界宽度输入框颜色 = (255, 246, 143) if self.世界宽度输入框处于焦点 else (230, 230, 230)
        pygame.draw.rect(self.屏幕, 世界宽度输入框颜色, self.世界宽度输入框_rect)
        # 输入框边框
        世界宽度边框颜色 = (100, 150, 200) if self.世界宽度输入框处于焦点 else (200, 200, 200)
        pygame.draw.rect(self.屏幕, 世界宽度边框颜色, self.世界宽度输入框_rect, 2)
        # 输入框文本
        世界宽度_text = self.文本字体.render(self.世界宽度输入文本, True, (0, 0, 0))
        # 绘制文本，添加一些内边距
        self.屏幕.blit(世界宽度_text, (self.世界宽度输入框_x + 5, self.世界宽度输入框_y + 5))
        
        # 绘制世界宽度+按钮
        宽度按钮颜色 = (150, 150, 150) if self.世界宽度按钮被按下 else self.按钮颜色
        pygame.draw.rect(self.屏幕, 宽度按钮颜色, self.增加宽度按钮_rect)
        pygame.draw.rect(self.屏幕, self.按钮边框颜色, self.增加宽度按钮_rect, 2)
        增加宽度按钮文本 = self.按钮字体.render("+", True, (0, 0, 0))
        增加宽度按钮文本_rect = 增加宽度按钮文本.get_rect(center=self.增加宽度按钮_rect.center)
        self.屏幕.blit(增加宽度按钮文本, 增加宽度按钮文本_rect)
        
        # 绘制世界高度标签
        世界高度标签 = self.文本字体.render("世界高度:", True, (255, 255, 255))
        self.屏幕.blit(世界高度标签, (self.世界高度标签_x, self.世界高度标签_y))
        
        # 绘制世界高度输入框
        # 输入框背景 - 焦点时为浅金色
        世界高度输入框颜色 = (255, 246, 143) if self.世界高度输入框处于焦点 else (230, 230, 230)
        pygame.draw.rect(self.屏幕, 世界高度输入框颜色, self.世界高度输入框_rect)
        # 输入框边框
        世界高度边框颜色 = (100, 150, 200) if self.世界高度输入框处于焦点 else (200, 200, 200)
        pygame.draw.rect(self.屏幕, 世界高度边框颜色, self.世界高度输入框_rect, 2)
        # 输入框文本
        世界高度_text = self.文本字体.render(self.世界高度输入文本, True, (0, 0, 0))
        # 绘制文本，添加一些内边距
        self.屏幕.blit(世界高度_text, (self.世界高度输入框_x + 5, self.世界高度输入框_y + 5))
        
        # 绘制世界高度+按钮
        高度按钮颜色 = (150, 150, 150) if self.世界高度按钮被按下 else self.按钮颜色
        pygame.draw.rect(self.屏幕, 高度按钮颜色, self.增加高度按钮_rect)
        pygame.draw.rect(self.屏幕, self.按钮边框颜色, self.增加高度按钮_rect, 2)
        增加高度按钮文本 = self.按钮字体.render("+", True, (0, 0, 0))
        增加高度按钮文本_rect = 增加高度按钮文本.get_rect(center=self.增加高度按钮_rect.center)
        self.屏幕.blit(增加高度按钮文本, 增加高度按钮文本_rect)
        
        # 绘制开关按钮标签
        创造模式标签 = self.文本字体.render("创造模式", True, (0, 0, 0))  # 100%黑色
        创造模式标签_width = 创造模式标签.get_width()
        self.屏幕.blit(创造模式标签, (self.创造模式标签_x - 创造模式标签_width // 2, self.创造模式标签_y))

        创建存档标签 = self.文本字体.render("创建存档", True, (0, 0, 0))  # 100%黑色
        创建存档标签_width = 创建存档标签.get_width()
        self.屏幕.blit(创建存档标签, (self.创建存档标签_x - 创建存档标签_width // 2, self.创建存档标签_y))

        # 根据存档模式状态决定无限世界文字颜色
        无限世界文字颜色 = (100, 100, 100) if not self.创建存档开关 else (0, 0, 0)
        无限世界标签 = self.文本字体.render("无限世界", True, 无限世界文字颜色)
        无限世界标签_width = 无限世界标签.get_width()
        self.屏幕.blit(无限世界标签, (self.无限世界标签_x - 无限世界标签_width // 2, self.无限世界标签_y))
        
        # 绘制三个开关按钮
        self.绘制开关按钮(self.创造模式开关_rect.x, self.创造模式开关_rect.y, self.创造模式开关)
        self.绘制开关按钮(self.创建存档开关_rect.x, self.创建存档开关_rect.y, self.创建存档开关)
        # 当存档模式关闭时，无限世界按钮变暗
        self.绘制开关按钮(self.无限世界开关_rect.x, self.无限世界开关_rect.y, self.无限世界开关, 变暗=not self.创建存档开关)
        
        # 绘制世界类型标签（移到开关按钮之后，提高优先级）
        世界类型标签 = self.文本字体.render("世界类型:", True, (255, 255, 255))
        self.屏幕.blit(世界类型标签, (self.世界类型标签_x, self.世界类型标签_y + 5))
        
        # 绘制世界类型下拉框（移到开关按钮之后，提高优先级）
        # 下拉框背景 - 焦点时为浅金色
        下拉框颜色 = (255, 246, 143) if self.下拉框处于焦点 else (230, 230, 230)
        pygame.draw.rect(self.屏幕, 下拉框颜色, self.世界类型下拉框_rect)
        # 下拉框边框
        下拉框边框颜色 = (100, 150, 200) if self.下拉框处于焦点 else (200, 200, 200)
        pygame.draw.rect(self.屏幕, 下拉框边框颜色, self.世界类型下拉框_rect, 2)
        # 下拉框文本
        世界类型文本 = self.文本字体.render(self.当前世界类型, True, (0, 0, 0))
        # 绘制文本，添加一些内边距
        self.屏幕.blit(世界类型文本, (self.世界类型下拉框_x + 5, self.世界类型下拉框_y + 5))
        # 绘制下拉箭头
        箭头文本 = self.文本字体.render("▼", True, (0, 0, 0))
        箭头_rect = 箭头文本.get_rect(right=self.世界类型下拉框_x + self.世界类型下拉框_width - 5, 
                                      centery=self.世界类型下拉框_y + self.世界类型下拉框_height // 2)
        self.屏幕.blit(箭头文本, 箭头_rect)
        
        # 绘制下拉选项（如果展开）
        if self.下拉框展开:
            # 绘制选项区域背景
            pygame.draw.rect(self.屏幕, (230, 230, 230), self.下拉选项区域_rect)
            pygame.draw.rect(self.屏幕, (200, 200, 200), self.下拉选项区域_rect, 2)
            
            # 绘制每个选项
            for i, 选项 in enumerate(self.世界类型选项):
                选项_rect = pygame.Rect(
                    self.世界类型下拉框_x,
                    self.世界类型下拉框_y + (i + 1) * self.世界类型下拉框_height,
                    self.世界类型下拉框_width,
                    self.世界类型下拉框_height
                )
                
                # 如果是当前选中的选项，使用不同背景色
                if 选项 == self.当前世界类型:
                    pygame.draw.rect(self.屏幕, (255, 246, 143), 选项_rect)
                
                # 绘制选项文本
                选项文本 = self.文本字体.render(选项, True, (0, 0, 0))
                self.屏幕.blit(选项文本, (选项_rect.x + 5, 选项_rect.y + 5))
        
        # 绘制新的创建世界按钮 - 绿色调，带动画效果
        # 根据按钮状态选择颜色
        if self.创建世界按钮按下:
            按钮颜色 = self.创建世界按钮按下颜色
        elif self.创建世界按钮悬停:
            按钮颜色 = self.创建世界按钮悬停颜色
        else:
            按钮颜色 = self.创建世界按钮正常颜色
        
        # 绘制按钮背景和边框
        pygame.draw.rect(self.屏幕, 按钮颜色, self.新创建世界按钮)
        pygame.draw.rect(self.屏幕, self.创建世界按钮边框颜色, self.新创建世界按钮, 2)
        
        # 绘制按钮文本
        新创建世界按钮文本 = self.按钮字体.render("创建世界", True, (0, 0, 0))
        新创建世界按钮文本_rect = 新创建世界按钮文本.get_rect(center=self.新创建世界按钮.center)
        self.屏幕.blit(新创建世界按钮文本, 新创建世界按钮文本_rect)
    
    def 验证世界宽度输入(self):
        """验证并处理世界宽度输入，确保在有效范围内"""
        try:
            # 尝试将输入文本转换为整数
            输入宽度 = int(self.世界宽度输入文本)
            # 限制最小值为1000，最大值为10000
            self.世界宽度 = max(1000, min(10000, 输入宽度))
            # 更新输入文本以反映实际值
            self.世界宽度输入文本 = str(self.世界宽度)
        except ValueError:
            # 如果输入无效，重置为当前世界宽度
            self.世界宽度输入文本 = str(self.世界宽度)
    
    def 增加世界宽度(self):
        """增加世界宽度500，但不超过上限10000"""
        self.世界宽度 = min(10000, self.世界宽度 + 500)
        self.世界宽度输入文本 = str(self.世界宽度)
        print(f"世界宽度已增加到：{self.世界宽度}")
    
    def 验证世界高度输入(self):
        """验证并处理世界高度输入，确保在有效范围内"""
        try:
            # 尝试将输入文本转换为整数
            输入高度 = int(self.世界高度输入文本)
            # 限制最小值为100，最大值为600
            self.世界高度 = max(100, min(600, 输入高度))
            # 更新输入文本以反映实际值
            self.世界高度输入文本 = str(self.世界高度)
        except ValueError:
            # 如果输入无效，重置为当前世界高度
            self.世界高度输入文本 = str(self.世界高度)
    
    def 增加世界高度(self):
        """增加世界高度25，但不超过上限1000"""
        self.世界高度 = min(600, self.世界高度 + 25)
        self.世界高度输入文本 = str(self.世界高度)
        print(f"世界高度已增加到：{self.世界高度}")
    
    def 切换开关状态(self, 开关属性):
        """切换指定开关的状态"""
        当前状态 = getattr(self, 开关属性)
        新状态 = self.开关_开启 if 当前状态 == self.开关_关闭 else self.开关_关闭
        setattr(self, 开关属性, 新状态)
        
        # 输出状态变化信息
        开关名称 = {"创造模式开关": "创造模式", "创建存档开关": "创建存档", "无限世界开关": "无限世界"}.get(开关属性, 开关属性)
        print(f"{开关名称}状态: {'开启' if 新状态 else '关闭'}")
    
    def handle_event(self, 事件):
        # 处理鼠标移动事件，检测按钮悬停状态
        if 事件.type == pygame.MOUSEMOTION:
            # 检测创建世界按钮悬停状态
            self.创建世界按钮悬停 = self.新创建世界按钮.collidepoint(事件.pos)
        # 处理鼠标松开事件，重置按下状态
        elif 事件.type == pygame.MOUSEBUTTONUP:
            if 事件.button == 1:  # 左键松开
                self.创建世界按钮按下 = False
        # 处理ESC键关闭界面
        if 事件.type == pygame.KEYDOWN:
            if 事件.key == pygame.K_ESCAPE:
                return False  # 返回False表示关闭界面
            elif self.输入框处于焦点:
                # 处理存档名称输入框输入
                if 事件.key == pygame.K_BACKSPACE:
                    self.存档名称 = self.存档名称[:-1]  # 删除最后一个字符
                elif 事件.key == pygame.K_RETURN:
                    # 验证存档名称，如果为空则恢复原始值
                    if self.存档名称.strip() == "":
                        self.存档名称 = self.原始存档名称
                    self.输入框处于焦点 = False
                else:
                    # 添加新字符（限制长度，避免输入过多）
                    if len(self.存档名称) < 20:
                        # 只允许输入英文字符、数字和一些基本符号
                        if 事件.unicode.isalnum() or 事件.unicode in ' _-':
                            self.存档名称 += 事件.unicode
            elif self.世界宽度输入框处于焦点:
                # 处理世界宽度输入框输入
                if 事件.key == pygame.K_BACKSPACE:
                    self.世界宽度输入文本 = self.世界宽度输入文本[:-1]  # 删除最后一个字符
                elif 事件.key == pygame.K_RETURN:
                    # 回车键确认输入
                    self.验证世界宽度输入()
                else:
                    # 只允许输入数字
                    if 事件.unicode.isdigit():
                        self.世界宽度输入文本 += 事件.unicode
            elif self.世界高度输入框处于焦点:
                # 处理世界高度输入框输入
                if 事件.key == pygame.K_BACKSPACE:
                    self.世界高度输入文本 = self.世界高度输入文本[:-1]  # 删除最后一个字符
                elif 事件.key == pygame.K_RETURN:
                    # 回车键确认输入
                    self.验证世界高度输入()
                else:
                    # 只允许输入数字
                    if 事件.unicode.isdigit():
                        self.世界高度输入文本 += 事件.unicode
        # 处理窗口调整事件
        elif 事件.type == pygame.VIDEORESIZE:
            self.更新尺寸()
            self.初始化按钮()
        # 处理鼠标点击事件
        elif 事件.type == pygame.MOUSEBUTTONDOWN:
            if 事件.button == 1:  # 左键点击
                # 检查是否点击了存档名称输入框
                if self.输入框_rect.collidepoint(事件.pos):
                    # 如果之前在世界宽度或高度输入框，先验证它们
                    if self.世界宽度输入框处于焦点:
                        self.验证世界宽度输入()
                    elif self.世界高度输入框处于焦点:
                        self.验证世界高度输入()
                    self.输入框处于焦点 = True
                    self.世界宽度输入框处于焦点 = False
                    self.世界高度输入框处于焦点 = False
                # 检查是否点击了世界宽度输入框
                elif self.世界宽度输入框_rect.collidepoint(事件.pos):
                    # 如果之前在其他输入框，先验证它们
                    if self.输入框处于焦点:
                        # 检查存档名称是否为空，如果为空则恢复原始值
                        if self.存档名称.strip() == "":
                            self.存档名称 = self.原始存档名称
                        self.输入框处于焦点 = False
                    elif self.世界高度输入框处于焦点:
                        self.验证世界高度输入()
                    self.世界宽度输入框处于焦点 = True
                    self.世界高度输入框处于焦点 = False
                # 检查是否点击了世界高度输入框
                elif self.世界高度输入框_rect.collidepoint(事件.pos):
                    # 如果之前在其他输入框，先验证它们
                    if self.输入框处于焦点:
                        # 检查存档名称是否为空，如果为空则恢复原始值
                        if self.存档名称.strip() == "":
                            self.存档名称 = self.原始存档名称
                        self.输入框处于焦点 = False
                    elif self.世界宽度输入框处于焦点:
                        self.验证世界宽度输入()
                    elif self.下拉框处于焦点:
                        self.下拉框处于焦点 = False
                        self.下拉框展开 = False
                    self.世界高度输入框处于焦点 = True
                    self.世界宽度输入框处于焦点 = False
                # 检查是否点击了世界类型下拉框
                elif self.世界类型下拉框_rect.collidepoint(事件.pos):
                    # 播放点击音效
                    audio_manager.play_click_sound()
                    # 如果之前在其他输入框，先验证它们
                    if self.输入框处于焦点:
                        # 检查存档名称是否为空，如果为空则恢复原始值
                        if self.存档名称.strip() == "":
                            self.存档名称 = self.原始存档名称
                        self.输入框处于焦点 = False
                    elif self.世界宽度输入框处于焦点:
                        self.验证世界宽度输入()
                    elif self.世界高度输入框处于焦点:
                        self.验证世界高度输入()
                    # 切换下拉框焦点和展开状态
                    self.下拉框处于焦点 = True
                    self.下拉框展开 = not self.下拉框展开
                    self.世界宽度输入框处于焦点 = False
                    self.世界高度输入框处于焦点 = False
                    self.输入框处于焦点 = False
                # 检查是否点击了下拉选项
                elif self.下拉框展开 and self.下拉选项区域_rect.collidepoint(事件.pos):
                    # 播放点击音效
                    audio_manager.play_click_sound()
                    # 计算点击的是哪个选项
                    选项索引 = (事件.pos[1] - self.世界类型下拉框_y - self.世界类型下拉框_height) // self.世界类型下拉框_height
                    if 0 <= 选项索引 < len(self.世界类型选项):
                        self.当前世界类型 = self.世界类型选项[选项索引]
                        print(f"世界类型已选择：{self.当前世界类型}")
                    # 关闭下拉框
                    self.下拉框展开 = False
                else:
                    # 如果点击了其他地方，验证输入并失去焦点
                    self.验证世界宽度输入()
                    self.验证世界高度输入()
                    self.输入框处于焦点 = False
                    self.世界宽度输入框处于焦点 = False
                    self.世界高度输入框处于焦点 = False
                    self.下拉框处于焦点 = False
                    self.下拉框展开 = False
                    
                    # 检查是否点击了+按钮
                    if self.增加宽度按钮_rect.collidepoint(事件.pos):
                        audio_manager.play_click_sound()
                        self.增加世界宽度()
                        self.世界宽度按钮被按下 = True
                        self.按钮按下时间 = pygame.time.get_ticks()
                    elif self.增加高度按钮_rect.collidepoint(事件.pos):
                        audio_manager.play_click_sound()
                        self.增加世界高度()
                        self.世界高度按钮被按下 = True
                        self.按钮按下时间 = pygame.time.get_ticks()
                    elif self.保存存档按钮.collidepoint(事件.pos):
                        audio_manager.play_click_sound()
                        self.递增存档编号()
                        self.存档按钮被按下 = True
                        self.按钮按下时间 = pygame.time.get_ticks()
                    # 检查是否点击了开关按钮
                    elif self.创造模式开关_rect.collidepoint(事件.pos):
                        audio_manager.play_click_sound()
                        self.切换开关状态("创造模式开关")
                    elif self.创建存档开关_rect.collidepoint(事件.pos):
                        audio_manager.play_click_sound()
                        # 切换存档模式状态
                        self.切换开关状态("创建存档开关")
                        # 如果存档模式关闭，强制关闭无限世界
                        if not self.创建存档开关 and self.无限世界开关:
                            self.无限世界开关 = self.开关_关闭
                            print("无限世界状态: 关闭 (因存档模式关闭)")
                    elif self.无限世界开关_rect.collidepoint(事件.pos):
                        audio_manager.play_click_sound()
                        # 只有在存档模式开启时才能切换无限世界状态
                        if self.创建存档开关:
                            self.切换开关状态("无限世界开关")
                        else:
                            print("请先开启存档模式才能开启无限世界")
                    
                    # 调用处理鼠标点击方法，但只有在点击了返回按钮或创建世界按钮时才返回结果
                    result = self.处理鼠标点击(事件.pos)
                    # 只有明确点击了返回按钮或创建世界按钮才返回False（关闭界面）
                    if result is False:
                        return False
        return True  # 继续显示界面
    
    def 递增存档编号(self):
        """递增存档名称中的数字部分，例如：New World 1 修改为 New World 2"""
        # 定义基础名称
        基础名称 = "New World "
        
        # 检查存档名称是否以基础名称开头
        if self.存档名称.startswith(基础名称):
            # 提取数字部分
            数字部分 = self.存档名称[len(基础名称):]
            if 数字部分.isdigit():
                # 增加数字并更新存档名称
                新编号 = int(数字部分) + 1
                self.存档名称 = f"{基础名称}{新编号}"
                print(f"存档编号已递增：{self.存档名称}")
                return
        
        # 如果不符合标准格式，设置为New World 1
        self.存档名称 = "New World 1"
        print(f"存档名称格式不符合标准，已重置为：{self.存档名称}")
    
    def 处理鼠标点击(self, 鼠标位置):
        # 检查左上角返回按钮点击
        if self.左上角返回按钮.collidepoint(鼠标位置):
            audio_manager.play_click_sound()
            print("返回主菜单")
            return False  # 返回False表示关闭界面
        
        # 检查创建世界按钮点击
        if self.创建世界按钮.collidepoint(鼠标位置):
            audio_manager.play_click_sound()
            print(f"创建新的世界 - 存档名称: {self.存档名称}, 世界宽度: {self.世界宽度}, 世界高度: {self.世界高度}, 世界类型: {self.当前世界类型}")
            print(f"创造模式: {'开启' if self.创造模式开关 else '关闭'}")
            print(f"创建存档: {'开启' if self.创建存档开关 else '关闭'}")
            print(f"无限世界: {'开启' if self.无限世界开关 else '关闭'}")
            # 准备世界参数
            世界参数 = {
                '存档名称': self.存档名称,
                '世界宽度': self.世界宽度,
                '世界高度': self.世界高度,
                '世界类型': self.当前世界类型,
                '创造模式': self.创造模式开关,
                '创建存档': self.创建存档开关,
                '无限世界': self.无限世界开关
            }
            # 启动游戏
            self.启动游戏(世界参数)
            return False  # 关闭创建世界界面
        
        # 检查新的创建世界按钮点击
        if self.新创建世界按钮.collidepoint(鼠标位置):
            audio_manager.play_click_sound()
            # 设置按钮按下状态
            self.创建世界按钮按下 = True
            print(f"新按钮点击 - 创建新的世界: 存档名称: {self.存档名称}, 世界宽度: {self.世界宽度}, 世界高度: {self.世界高度}, 世界类型: {self.当前世界类型}")
            print(f"创造模式: {'开启' if self.创造模式开关 else '关闭'}")
            print(f"创建存档: {'开启' if self.创建存档开关 else '关闭'}")
            print(f"无限世界: {'开启' if self.无限世界开关 else '关闭'}")
            # 准备世界参数
            世界参数 = {
                '存档名称': self.存档名称,
                '世界宽度': self.世界宽度,
                '世界高度': self.世界高度,
                '世界类型': self.当前世界类型,
                '创造模式': self.创造模式开关,
                '创建存档': self.创建存档开关,
                '无限世界': self.无限世界开关
            }
            # 启动游戏
            self.启动游戏(世界参数)
            return False  # 关闭创建世界界面
        
        # 默认情况下不返回任何值，这样就不会关闭界面（修复点击空白处返回问题）
    
    def 启动游戏(self, 世界参数):
        """启动游戏并传递世界参数，显示加载窗口"""
        print(f"正在启动游戏，进入世界: {世界参数['存档名称']}")
        # 保存窗口尺寸
        width = 800
        height = 600
        if hasattr(self, '屏幕') and self.屏幕 is not None:
            try:
                width = self.屏幕.get_width()
                height = self.屏幕.get_height()
            except pygame.error:
                pass
        
        # 创建并显示加载窗口 - 传递当前屏幕，实现统一窗口
        加载窗口实例 = 加载窗口(screen=self.屏幕, width=width, height=height)
        加载窗口实例.update_progress(10, "准备创建世界")
        pygame.event.pump()  # 处理事件，防止界面冻结
        pygame.display.flip()
        
        # 步骤1: 加载游戏资源 - 图片
        加载窗口实例.update_progress(20, "正在加载游戏资源")
        pygame.event.pump()
        pygame.display.flip()
        
        # 使用全局的图片管理器实例加载所有图片
        # 这里传递加载窗口实例，让图片加载过程能够更新加载窗口显示具体文件名
        图片管理器.加载所有图片(加载窗口=加载窗口实例)
        
        # 步骤2: 加载音频资源
        加载窗口实例.update_progress(60, "正在加载音频资源")
        pygame.event.pump()
        pygame.display.flip()
        
        # 使用音频管理器加载所有音频，传递加载窗口实例
        audio_manager.load_all_audio(loading_window=加载窗口实例)
        
        # 步骤3: 生成地形和游戏初始化
        加载窗口实例.update_progress(80, "生成地形和游戏初始化")
        pygame.event.pump()
        pygame.display.flip()
        pygame.time.delay(300)  # 短暂延迟，让用户看到进度
        
        # 完成加载
        加载窗口实例.update_progress(100, "加载完成！")
        pygame.display.flip()
        pygame.time.delay(500)  # 显示完成状态一小段时间
        
        # 不需要关闭加载窗口，因为它使用的是当前屏幕
        # 加载窗口实例.close()
        
        # 启动游戏，传递当前屏幕实现统一窗口
        游玩.start_game(世界参数, screen=self.屏幕)
        
        # 游戏结束后，检查pygame是否还在运行
        try:
            # 检查pygame是否还在运行
            pygame.display.get_init()
            # 不重新创建窗口，保持当前窗口大小
            # 只更新界面尺寸和重绘
            self.屏幕_width, self.屏幕_height = self.屏幕.get_size()
            self.更新尺寸()
            self.绘制()
        except pygame.error:
            # 如果pygame显示已关闭，重新初始化
            pygame.init()
            pygame.font.init()
            # 使用当前屏幕大小重新创建窗口
            try:
                self.屏幕 = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                try:
                    # 使用与方块世界相同的字体样式，但大小增加5
                    self.标题字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 45, bold=True)
                    self.按钮字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 20)
                    self.文本字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 20)
                except:
                    self.标题字体 = pygame.font.SysFont('Arial', 72 + 5, bold=True)
                    self.按钮字体 = pygame.font.SysFont('Arial', 20)
                    self.文本字体 = pygame.font.SysFont('Arial', 18)
                self.屏幕_width = width
                self.屏幕_height = height
                self.更新尺寸()
                self.绘制()
            except Exception as inner_e:
                print(f"创建默认窗口时出错: {inner_e}")
        
        return True  # 继续显示界面

# 示例使用方法
def 主函数():
    # 创建一个适合展示创建世界界面的窗口
    屏幕 = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("创建世界")
    clock = pygame.time.Clock()
    
    # 初始化创建世界界面
    创建世界界面实例 = 创建世界界面(屏幕)
    
    # 主循环
    运行中 = True
    while 运行中:
        # 清空屏幕
        屏幕.fill((240, 240, 240))
        
        # 处理事件
        for 事件 in pygame.event.get():
            if 事件.type == pygame.QUIT:
                运行中 = False
            else:
                # 传递事件给创建世界界面处理
                if not 创建世界界面实例.handle_event(事件):
                    运行中 = False
                    
            # 处理窗口调整事件
            if 事件.type == pygame.VIDEORESIZE:
                # 更新屏幕尺寸
                屏幕 = pygame.display.set_mode((事件.w, 事件.h), pygame.RESIZABLE)
                # 重新初始化界面以适应新尺寸
                创建世界界面实例 = 创建世界界面(屏幕)
        
        # 绘制界面
        创建世界界面实例.绘制()
        
        # 刷新屏幕
        pygame.display.flip()
        
        # 控制帧率
        clock.tick(60)
    
    # 退出pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    主函数()