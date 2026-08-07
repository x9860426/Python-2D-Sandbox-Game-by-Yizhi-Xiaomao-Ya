import pygame
import sys
import time
import random
import math
import os
import datetime

# 添加项目根目录及其子目录到Python搜索路径，使自定义模块可以被导入
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# 添加所有模块目录到Python搜索路径
sys.path.append(os.path.join(project_root, '6.资源管理'))
sys.path.append(os.path.join(project_root, '3.物品与背包'))
sys.path.append(os.path.join(project_root, '4.游戏界面'))
sys.path.append(os.path.join(project_root, '5.游戏系统'))
sys.path.append(os.path.join(project_root, '存档'))

# 导入音频管理器
from 音频输出 import audio_manager
# 导入图片管理器
from 图片加载 import 图片管理器
# 导入物品定义
from 物品定义 import *
# 导入公告系统
from 公告 import AnnouncementSystem
# 导入设置界面
from 设置 import 设置界面
# 导入创建世界界面
from 创建世界 import 创建世界界面
# 导入加载窗口
from 加载窗口 import 加载窗口
# 导入存档处理界面
from 存档处理 import 存档处理界面

# 初始化pygame
pygame.init()

# 设置中文字体
pygame.font.init()
try:
    大字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 72)
    中字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 36)
    小字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 24)
except:
    大字体 = pygame.font.SysFont('Arial', 72)
    中字体 = pygame.font.SysFont('Arial', 36)
    小字体 = pygame.font.SysFont('Arial', 24)

# 游戏窗口设置
窗口宽度, 窗口高度 = 1200, 800
# 创建可调节大小的窗口标志
窗口标志 = pygame.RESIZABLE  # 可调节大小
# 先不创建主窗口，在加载完成后创建
窗口 = None

# 游戏状态管理
class 游戏状态:
    开始界面 = 0
    游戏运行 = 1
    公告界面 = 2
    设置界面 = 3
    创建世界界面 = 4
    存档处理界面 = 5

# 颜色定义
白色 = (255, 255, 255)
黑色 = (0, 0, 0)
灰色 = (200, 200, 200)
浅灰色 = (230, 230, 230)
深灰色 = (150, 150, 150)
# 蓝色渐变相关颜色 - 历史版本配色方案
深蓝色 = (0, 50, 100)
浅蓝色 = (0, 255, 255)
# 按钮反馈颜色
按钮默认 = (100, 150, 100)
按钮悬停 = (130, 180, 130)
按钮按下 = (70, 120, 70)
按钮文字 = 白色
# 特殊按钮颜色
导入按钮默认 = (120, 100, 180)
导入按钮悬停 = (150, 130, 210)
导入按钮按下 = (90, 70, 150)
公告按钮默认 = (80, 100, 180)
设置按钮默认 = (180, 150, 80)

# 增强的按钮类
class 按钮:
    def __init__(self, x, y, 宽度, 高度, 文字, 字体, 默认颜色=按钮默认, 悬停颜色=按钮悬停, 
                 按下颜色=按钮按下, 文字颜色=按钮文字, 边框颜色=深灰色):
        self.矩形 = pygame.Rect(x, y, 宽度, 高度)
        self.原始矩形 = pygame.Rect(x, y, 宽度, 高度)  # 存储原始位置用于窗口调整
        self.文字 = 文字
        self.字体 = 字体
        self.默认颜色 = 默认颜色
        self.悬停颜色 = 悬停颜色
        self.按下颜色 = 按下颜色
        self.文字颜色 = 文字颜色
        self.边框颜色 = 边框颜色
        self.是否悬停 = False
        self.是否按下 = False
    
    def 绘制(self, 窗口, 当前窗口宽度=窗口宽度, 当前窗口高度=窗口高度):
        # 根据按钮状态选择颜色
        if self.是否按下:
            颜色 = self.按下颜色
            边框宽度 = 3
        elif self.是否悬停:
            颜色 = self.悬停颜色
            边框宽度 = 2
            # 添加发光效果
            发光表面 = pygame.Surface((self.矩形.width, self.矩形.height), pygame.SRCALPHA)
            pygame.draw.rect(发光表面, (*颜色, 100), 发光表面.get_rect(), border_radius=5)
            窗口.blit(发光表面, (self.矩形.x - 3, self.矩形.y - 3))
        else:
            颜色 = self.默认颜色
            边框宽度 = 2
        
        # 绘制圆角按钮
        pygame.draw.rect(窗口, 颜色, self.矩形, border_radius=5)
        pygame.draw.rect(窗口, self.边框颜色, self.矩形, 边框宽度, border_radius=5)
        
        # 渲染文本
        文本表面 = self.字体.render(self.文字, True, self.文字颜色)
        文本矩形 = 文本表面.get_rect(center=self.矩形.center)
        窗口.blit(文本表面, 文本矩形)
    
    def 更新(self, 鼠标位置, 当前窗口宽度=窗口宽度, 当前窗口高度=窗口高度):
        # 主按钮居中显示
        if self.原始矩形.width > 120:  # 主按钮(导入存档和开始游戏)
            self.矩形.x = (当前窗口宽度 - self.矩形.width) // 2  # 始终居中
            # 主按钮宽度根据窗口宽度缩放，但保持最小尺寸
            self.矩形.width = max(self.原始矩形.width, int(当前窗口宽度 * 0.2))
        else:  # 小按钮(公告和设置)
            # 小按钮仍然使用相对位置
            相对_x = self.原始矩形.x / 窗口宽度
            相对_y = self.原始矩形.y / 窗口高度
            self.矩形.x = int(当前窗口宽度 * 相对_x)
            self.矩形.y = int(当前窗口高度 * 相对_y)
        
        # 更新悬停状态
        self.是否悬停 = self.矩形.collidepoint(鼠标位置)
    
    def 设置按下状态(self, 是否按下):
        # 设置按下状态
        self.是否按下 = 是否按下
    
    def 被点击(self, 位置):
        return self.矩形.collidepoint(位置)

# 初始化按钮 - 新的尺寸和样式
按钮宽度 = 350
按钮高度 = 70
间距 = 40

# 计算按钮位置使其居中
起始_y = 窗口高度 // 2 + 30
导入按钮 = 按钮(
    (窗口宽度 - 按钮宽度) // 2,
    起始_y,
    按钮宽度,
    按钮高度,
    "导入存档",
    中字体,
    默认颜色=导入按钮默认,
    悬停颜色=导入按钮悬停,
    按下颜色=导入按钮按下,
    文字颜色=按钮文字
)

游戏按钮 = 按钮(
    (窗口宽度 - 按钮宽度) // 2,
    起始_y + 按钮高度 + 间距,
    按钮宽度,
    按钮高度,
    "开始游戏",
    中字体,
    文字颜色=按钮文字
)

# 小按钮设置
小按钮宽度 = 120
小按钮高度 = 45

公告按钮 = 按钮(
    窗口宽度 - 小按钮宽度 - 25,
    窗口高度 - 小按钮高度 - 25,
    小按钮宽度,
    小按钮高度,
    "公告",
    小字体,
    默认颜色=公告按钮默认,
    文字颜色=按钮文字
)

设置按钮 = 按钮(
    窗口宽度 - 小按钮宽度 * 2 - 40,
    窗口高度 - 小按钮高度 - 25,
    小按钮宽度,
    小按钮高度,
    "设置",
    小字体,
    默认颜色=设置按钮默认,
    文字颜色=按钮文字
)

# 绘制装饰性方块图案
def 绘制方块图案(窗口, 宽度, 高度):
    # 绘制背景方块图案作为装饰
    方块大小 = 20
    方块间距 = 100
    
    for x in range(-方块大小, 宽度 + 方块大小, 方块间距):
        for y in range(-方块大小, 高度 + 方块大小, 方块间距):
            # 随机决定是否绘制方块
            if (x + y) % (方块间距 * 2) == 0:
                # 方块颜色 - 比背景稍亮
                方块颜色 = (50, 180, 50, 50)
                方块表面 = pygame.Surface((方块大小, 方块大小), pygame.SRCALPHA)
                pygame.draw.rect(方块表面, 方块颜色, (0, 0, 方块大小, 方块大小))
                窗口.blit(方块表面, (x, y))

# 处理按钮点击
import datetime

def 处理按钮点击(按钮对象):
    global 设置界面实例
    global 创建世界界面实例
    # 获取当前系统时间
    当前时间 = datetime.datetime.now().strftime("%H:%M:%S")
    # 确定当前页面
    当前页面 = "开始游戏页面"
    # 按照指定格式输出终端提示
    print(f"[{当前时间}]用户在  [{当前页面}]  按下  [{按钮对象.文字}]  ")
    # 播放点击音效
    audio_manager.play_click_sound()
    # 处理按钮功能
    if 按钮对象.文字 == "开始游戏":
        # 开始游戏时应用当前设置
        if hasattr(设置界面, '_instance') and 设置界面._instance:
            # 使用当前设置
            print(f"游戏开始时的设置 - 音乐: {设置界面._instance.音乐开关}, 音效: {设置界面._instance.音效开关}, 音量: {设置界面._instance.音量}, 帧率: {设置界面._instance.帧率选择}")
    elif 按钮对象.文字 == "设置":
        # 切换到设置界面时不重新创建实例，使用已有的全局实例
        pass

# 游戏主循环
def 主函数():
    global 窗口
    global 设置界面实例
    global 创建世界界面实例
    时钟 = pygame.time.Clock()
    运行中 = True
    当前状态 = 游戏状态.开始界面
    
    # 1. 先创建主游戏窗口（统一窗口）
    窗口 = pygame.display.set_mode((窗口宽度, 窗口高度), 窗口标志)
    pygame.display.set_caption("方块世界")
    
    # 窗口尺寸变量，用于跟踪调整后的大小
    当前宽度, 当前高度 = 窗口.get_size()
    
    # 2. 将主窗口传递给加载窗口，实现统一窗口
    加载窗口实例 = 加载窗口(screen=窗口, width=当前宽度, height=当前高度)
    加载窗口实例.update_progress(0, "准备加载资源...")
    time.sleep(0.1)  # 模拟加载延迟
    
    # 3. 加载设置和配置 - 0%到10%
    加载窗口实例.update_progress(5, "加载游戏设置...")
    time.sleep(0.1)  # 模拟加载延迟
    
    # 4. 加载音频文件 - 10%到20%（占据10%进度）
    加载窗口实例.update_progress(10, "加载音频文件...")
    audio_manager.load_all_audio(loading_window=加载窗口实例)
    time.sleep(0.1)  # 模拟加载延迟
    
    # 5. 加载图片资源 - 20%到100%（占据80%进度）
    加载窗口实例.update_progress(20, "加载图片资源...")
    图片管理器.加载所有图片(加载窗口=加载窗口实例)
    time.sleep(0.5)  # 模拟加载延迟
    
    # 6. 初始化游戏系统和准备启动游戏 - 100%
    加载窗口实例.update_progress(100, "初始化游戏系统...")
    time.sleep(0.1)  # 模拟加载延迟
    
    # 7. 加载完成
    加载窗口实例.update_progress(100, "所有资源加载完成！")
    time.sleep(0.1)
    
    # 8. 不需要关闭加载窗口，因为它使用的是主窗口
    # 加载窗口实例.close()
    
    # 9. 初始化设置界面（加载设置配置）
    设置界面实例 = 设置界面(窗口)
    # 初始化公告系统
    公告系统 = AnnouncementSystem(窗口)
    # 初始化创建世界界面
    创建世界界面实例 = 创建世界界面(窗口)
    # 初始化存档处理界面
    存档处理界面实例 = 存档处理界面(窗口)
    
    while 运行中:
        # 使用设置界面中的帧率设置，默认为60fps
        帧率 = 60
        if hasattr(设置界面实例, '帧率选择'):
            帧率 = 设置界面实例.帧率选择
        时钟.tick(帧率)
        鼠标位置 = pygame.mouse.get_pos()
        
        # 更新按钮状态 - 传入当前窗口尺寸
        导入按钮.更新(鼠标位置, 当前宽度, 当前高度)
        游戏按钮.更新(鼠标位置, 当前宽度, 当前高度)
        公告按钮.更新(鼠标位置, 当前宽度, 当前高度)
        设置按钮.更新(鼠标位置, 当前宽度, 当前高度)
        
        # 处理事件
        for 事件 in pygame.event.get():
            # 在公告界面时处理公告系统事件
            if 当前状态 == 游戏状态.公告界面:
                if not 公告系统.handle_event(事件):
                    当前状态 = 游戏状态.开始界面
            # 在设置界面时处理设置界面事件
            elif 当前状态 == 游戏状态.设置界面:
                if not 设置界面实例.handle_event(事件):
                    当前状态 = 游戏状态.开始界面
            # 在创建世界界面时处理界面事件
            elif 当前状态 == 游戏状态.创建世界界面:
                if not 创建世界界面实例.handle_event(事件):
                    当前状态 = 游戏状态.开始界面
            # 在存档处理界面时处理界面事件
            elif 当前状态 == 游戏状态.存档处理界面:
                if not 存档处理界面实例.handle_event(事件):
                    当前状态 = 游戏状态.开始界面
            
            # 通用事件处理
            if 事件.type == pygame.QUIT:
                运行中 = False
            elif 事件.type == pygame.VIDEORESIZE:
                # 窗口大小改变
                当前宽度, 当前高度 = 事件.w, 事件.h
                # 更新窗口大小 - 最小尺寸限制
                最小宽度, 最小高度 = 800, 600
                当前宽度 = max(当前宽度, 最小宽度)
                当前高度 = max(当前高度, 最小高度)
                窗口 = pygame.display.set_mode((当前宽度, 当前高度), pygame.RESIZABLE)
                # 更新设置界面尺寸
                if 当前状态 == 游戏状态.设置界面:
                    设置界面实例 = 设置界面(窗口)
                elif 当前状态 == 游戏状态.创建世界界面:
                    创建世界界面实例 = 创建世界界面(窗口)
                elif 当前状态 == 游戏状态.存档处理界面:
                    存档处理界面实例 = 存档处理界面(窗口)
            elif 事件.type == pygame.MOUSEBUTTONDOWN:
                if 事件.button == 1:  # 左键点击
                    # 设置按钮按下状态
                    if 导入按钮.被点击(鼠标位置):
                        导入按钮.设置按下状态(True)
                    if 游戏按钮.被点击(鼠标位置):
                        游戏按钮.设置按下状态(True)
                    if 公告按钮.被点击(鼠标位置):
                        公告按钮.设置按下状态(True)
                    if 设置按钮.被点击(鼠标位置):
                        设置按钮.设置按下状态(True)
            elif 事件.type == pygame.MOUSEBUTTONUP:
                if 事件.button == 1:  # 左键释放
                    # 根据当前状态处理不同界面的按钮点击
                    if 当前状态 == 游戏状态.开始界面:
                        # 只有在开始界面才处理开始界面的按钮点击
                        if 导入按钮.被点击(鼠标位置) and 导入按钮.是否按下:
                            处理按钮点击(导入按钮)
                            当前状态 = 游戏状态.存档处理界面
                        if 游戏按钮.被点击(鼠标位置) and 游戏按钮.是否按下:
                            处理按钮点击(游戏按钮)
                            当前状态 = 游戏状态.创建世界界面
                        if 公告按钮.被点击(鼠标位置) and 公告按钮.是否按下:
                            处理按钮点击(公告按钮)
                            当前状态 = 游戏状态.公告界面
                            公告系统.is_open = True
                        if 设置按钮.被点击(鼠标位置) and 设置按钮.是否按下:
                            处理按钮点击(设置按钮)
                            当前状态 = 游戏状态.设置界面
                            # 更新音频设置，确保设置界面的更改能够立即生效
                            audio_manager.update_settings()
                    # 其他状态下，让对应界面自己处理按钮点击
                    # （设置界面和创建世界界面已经在各自的handle_event中处理）
                    
                    # 重置所有按钮的按下状态
                    导入按钮.设置按下状态(False)
                    游戏按钮.设置按下状态(False)
                    公告按钮.设置按下状态(False)
                    设置按钮.设置按下状态(False)
            elif 事件.type == pygame.KEYDOWN:
                if 事件.key == pygame.K_ESCAPE:
                    if 当前状态 == 游戏状态.设置界面 or 当前状态 == 游戏状态.创建世界界面:
                        当前状态 = 游戏状态.开始界面  # ESC键关闭设置界面或创建世界界面
                    else:
                        # 开始游戏界面和其他状态下，ESC键不执行任何操作
                        # 这样可以防止在开始游戏页面意外关闭游戏
                        pass
                elif 事件.key == pygame.K_F1:
                    # F1键快速切换到设置界面
                    if 当前状态 == 游戏状态.设置界面:
                        当前状态 = 游戏状态.开始界面
                    else:
                        当前状态 = 游戏状态.设置界面
                        # 更新音频设置
                        audio_manager.update_settings()
                elif 事件.key == pygame.K_F2:
                    # F2键打开设置界面
                    当前状态 = 游戏状态.设置界面
                    # 更新音频设置
                    audio_manager.update_settings()
        
        # 根据当前状态绘制不同内容
        if 当前状态 == 游戏状态.游戏运行:
            # 游戏运行状态，等待游戏结束
            # 实际上，游戏是通过创建世界界面或存档处理界面启动的
            # 当游戏结束时，它会自动返回主程序的主循环
            pass
        elif 当前状态 == 游戏状态.开始界面:
            # 在绘制开始界面之前，确保当前宽度和高度反映窗口的实际大小
            当前宽度, 当前高度 = 窗口.get_size()
            # 尝试使用图片加载器获取背景图片 - 添加pygame显示检查
            try:
                # 检查pygame显示是否仍处于活动状态
                if not pygame.display.get_init():
                    continue
                    
                # 使用图片加载器获取背景图1
                背景图片 = 图片管理器.获取图片("背景图1")
                if 背景图片 is not None:
                    # 计算缩放比例，保持图片的原始宽高比
                    图片宽度 = 背景图片.get_width()
                    图片高度 = 背景图片.get_height()
                    
                    # 计算缩放后的尺寸，保持原始宽高比
                    缩放比例 = max(当前宽度 / 图片宽度, 当前高度 / 图片高度)
                    新宽度 = int(图片宽度 * 缩放比例)
                    新高度 = int(图片高度 * 缩放比例)
                    
                    # 缩放图片
                    缩放背景图 = pygame.transform.scale(背景图片, (新宽度, 新高度))
                    
                    # 计算居中位置
                    x = (当前宽度 - 新宽度) // 2
                    y = (当前高度 - 新高度) // 2
                    
                    # 绘制背景图
                    窗口.blit(缩放背景图, (x, y))
                else:
                    # 如果图片加载失败，使用蓝色渐变
                    渐变表面 = pygame.Surface((当前宽度, 当前高度))
                    for y in range(当前高度):
                        # 从深蓝到浅蓝的垂直渐变
                        r = 0
                        g = 50 + int(y * 205 / 当前高度)
                        b = 100 + int(y * 155 / 当前高度)
                        pygame.draw.line(渐变表面, (r, g, b), (0, y), (当前宽度, y))
                    窗口.blit(渐变表面, (0, 0))
            except Exception as e:
                # 捕获所有异常，确保程序不会崩溃
                try:
                    if not pygame.display.get_init():
                        continue
                    print(f"背景图片处理失败: {e}，使用蓝色渐变背景")
                    # 使用蓝色渐变作为最终备选
                    渐变表面 = pygame.Surface((当前宽度, 当前高度))
                    for y in range(当前高度):
                        r = 0
                        g = 50 + int(y * 205 / 当前高度)
                        b = 100 + int(y * 155 / 当前高度)
                        pygame.draw.line(渐变表面, (r, g, b), (0, y), (当前宽度, y))
                    窗口.blit(渐变表面, (0, 0))
                except Exception as inner_e:
                    print(f"绘制渐变背景失败: {inner_e}")
                    continue
            
            # 绘制装饰性元素
            绘制方块图案(窗口, 当前宽度, 当前高度)
            
            # 绘制半透明遮罩以确保文字清晰可见
            遮罩层 = pygame.Surface((当前宽度, 当前高度), pygame.SRCALPHA)
            遮罩层.fill((0, 0, 0, 40))  # 半透明黑色
            窗口.blit(遮罩层, (0, 0))
            
            # 绘制'方块世界'文字 - 使用加粗字体
            粗体大字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 72, bold=True)
            
            # 文字阴影
            阴影表面 = 粗体大字体.render("方块世界", True, (0, 0, 0))
            阴影矩形 = 阴影表面.get_rect(center=(当前宽度 // 2, 当前高度 // 4))
            窗口.blit(阴影表面, (阴影矩形.x + 3, 阴影矩形.y + 3))
            
            # 主文字
            标题文字 = 粗体大字体.render("方块世界", True, 白色)
            标题矩形 = 标题文字.get_rect(center=(当前宽度 // 2, 当前高度 // 4))
            窗口.blit(标题文字, 标题矩形) 
            
            # 绘制副标题
            副标题字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 24)
            副标题文字 = 副标题字体.render("探索、建造、生存", True, 白色)
            副标题矩形 = 副标题文字.get_rect(center=(当前宽度 // 2, 标题矩形.bottom + 30))
            窗口.blit(副标题文字, 副标题矩形)
            
            # 确保按钮始终居中显示
            导入按钮.矩形.x = (当前宽度 - 导入按钮.矩形.width) // 2
            游戏按钮.矩形.x = (当前宽度 - 游戏按钮.矩形.width) // 2
            
            # 绘制按钮 - 传入当前窗口尺寸
            导入按钮.绘制(窗口, 当前宽度, 当前高度)
            游戏按钮.绘制(窗口, 当前宽度, 当前高度)
            公告按钮.绘制(窗口, 当前宽度, 当前高度)
            设置按钮.绘制(窗口, 当前宽度, 当前高度)
            
            # 在右下角显示分辨率提示文字
            提示字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 16)
            提示文字 = 提示字体.render("游戏由1920*1080(125%)页面开发可能有不兼容问题", True, (255, 255, 255))
            # 计算左下角位置，留出边距
            文字_x = 20
            文字_y = 当前高度 - 提示文字.get_height() - 20
            # 添加半透明背景以提高可读性
            文字背景 = pygame.Surface((提示文字.get_width() + 10, 提示文字.get_height() + 6), pygame.SRCALPHA)
            文字背景.fill((0, 0, 0, 100))
            窗口.blit(文字背景, (文字_x - 5, 文字_y - 3))
            # 绘制文字
            窗口.blit(提示文字, (文字_x, 文字_y))
        
        # 公告界面
        elif 当前状态 == 游戏状态.公告界面:
            # 保持开始界面背景
            渐变表面 = pygame.Surface((当前宽度, 当前高度))
            for y in range(当前高度):
                r = 0
                g = 50 + int(y * 205 / 当前高度)
                b = 100 + int(y * 155 / 当前高度)
                pygame.draw.line(渐变表面, (r, g, b), (0, y), (当前宽度, y))
            窗口.blit(渐变表面, (0, 0))
            
            # 绘制公告界面
            公告系统.draw()
            
            # 如果公告系统关闭，返回开始界面
            if not 公告系统.is_open:
                当前状态 = 游戏状态.开始界面
        
        # 设置界面
        elif 当前状态 == 游戏状态.设置界面:
            # 保持开始界面背景
            渐变表面 = pygame.Surface((当前宽度, 当前高度))
            for y in range(当前高度):
                r = 0
                g = 50 + int(y * 205 / 当前高度)
                b = 100 + int(y * 155 / 当前高度)
                pygame.draw.line(渐变表面, (r, g, b), (0, y), (当前宽度, y))
            窗口.blit(渐变表面, (0, 0))
            
            # 绘制设置界面
            设置界面实例.绘制()
        
        # 创建世界界面
        elif 当前状态 == 游戏状态.创建世界界面:
            # 保持开始界面背景
            渐变表面 = pygame.Surface((当前宽度, 当前高度))
            for y in range(当前高度):
                r = 0
                g = 50 + int(y * 205 / 当前高度)
                b = 100 + int(y * 155 / 当前高度)
                pygame.draw.line(渐变表面, (r, g, b), (0, y), (当前宽度, y))
            窗口.blit(渐变表面, (0, 0))
            
            # 绘制创建世界界面
            创建世界界面实例.绘制()
        
        # 存档处理界面
        elif 当前状态 == 游戏状态.存档处理界面:
            # 保持开始界面背景
            渐变表面 = pygame.Surface((当前宽度, 当前高度))
            for y in range(当前高度):
                r = 0
                g = 50 + int(y * 205 / 当前高度)
                b = 100 + int(y * 155 / 当前高度)
                pygame.draw.line(渐变表面, (r, g, b), (0, y), (当前宽度, y))
            窗口.blit(渐变表面, (0, 0))
            
            # 绘制存档处理界面
            存档处理界面实例.绘制()
        
        # 更新显示
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    主函数()