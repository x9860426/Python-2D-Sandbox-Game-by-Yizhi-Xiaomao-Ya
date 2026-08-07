import pygame
import sys
import os
from 音频输出 import audio_manager
from 图片加载 import 图片管理器



# 深色主题配色方案
主背景色 = (26, 27, 29)      # 更深灰色主背景
次级背景色 = (39, 40, 40)    # 深灰色次级背景
边框颜色 = (70, 70, 70)      # 中灰色边框
标题颜色 = (220, 220, 220)   # 浅色标题
文本颜色 = (0, 0, 0)   # 100%黑色文本
阴影颜色 = (0, 0, 0, 80)     # 更明显的半透明黑色阴影

class 设置界面:
    # 类变量，用于存储单例实例
    _instance = None
    
    def __init__(self, 屏幕):
        self.屏幕 = 屏幕
        self.屏幕宽度 = 屏幕.get_width()
        self.屏幕高度 = 屏幕.get_height()
        # 输入框编辑状态
        self.当前编辑输入框 = None  # None表示无编辑，'宽渲染'或'高渲染'表示正在编辑
        
        # 使用图片加载器获取背景图片
        self.background_image = None
        
        # 底1尺寸：宽160*高600
        self.底1宽度 = 160
        self.底1高度 = 600
        
        # 底2尺寸：宽700*高600
        self.底2宽度 = 700
        self.底2高度 = 600
        
        # 间隔：20
        self.间隔 = 20
        
        # 计算居中位置 - 使用实际尺寸进行计算
        self.底1_x = (self.屏幕宽度 - self.底1宽度 - self.间隔 - self.底2宽度) // 2
        self.底2_x = self.底1_x + self.底1宽度 + self.间隔
        self.底_y = (self.屏幕高度 - max(self.底1高度, self.底2高度)) // 2
        
        # 圆角半径和字体设置
        self.圆角半径 = 10
        self.标题字体 = pygame.font.SysFont("Microsoft YaHei", 24, True)
        self.文本字体 = pygame.font.SysFont("Microsoft YaHei", 18)
        self.按钮字体 = pygame.font.SysFont("Microsoft YaHei", 16, bold=True)
        
        # 按钮相关属性
        self.按钮高度 = 40
        self.按钮宽度 = self.底1宽度 - 30
        self.按钮间隔 = 15
        
        # 当前选中的选项
        self.当前选中 = "基础设置"
        # 当前选中的小底索引（1-4，默认为1）
        self.当前选中的小底 = 2
        
        # 按钮颜色设置（95%白色）
        self.按钮颜色 = (242, 242, 242)      # 正常按钮颜色（95%白色）
        self.按钮悬停颜色 = (250, 250, 250)   # 悬停按钮颜色（比95%白色更亮）
        self.按钮选中颜色 = (255, 255, 255)   # 选中按钮颜色（100%白色）
        self.按钮边框颜色 = (220, 220, 220)   # 按钮边框颜色（比95%白色稍暗）
        
        # 滑动容器相关属性
        self.滑动偏移 = 0  # 当前滑动偏移量（垂直方向）
        self.滑动速度 = 20  # 滚轮滑动速度
        self.最大滑动偏移 = 0  # 最大滑动偏移量
        self.滑动容器高度 = 0  # 滑动容器实际高度
        self.显示区域高度 = 0  # 显示区域高度
        
        # 音乐和音效设置 - 使用单例模式确保设置一致
        if not hasattr(self.__class__, '_instance') or self.__class__._instance is None:
            # 第一次创建实例，初始化默认设置
            self.音乐开关 = True  # 默认开启音乐
            self.音效开关 = True  # 默认开启音效
            self.音量 = 100       # 默认音量100%
            self.帧率选择 = 60    # 默认帧率60FPS
            # 渲染设置默认值
            self.宽渲染 = 100    # 默认宽渲染
            self.高渲染 = 50     # 默认高渲染
            # 特效渲染设置
            self.特效渲染 = "标准"  # 默认标准渲染
            # 显示距离设置
            self.显示攻击距离 = False  # 默认关闭显示攻击距离
            self.显示受伤距离 = False  # 默认关闭显示受伤距离
            # 帧率选项列表
            self.帧率选项 = [60, 120, 240]
            # 存档默认保存路径
            import os
            self.存档路径 = os.path.join(os.getcwd(), "存档")  # 默认路径：程序同级的存档文件夹
            # 玩家上传的图片路径
            self.玩家上传图片路径 = ""  # 默认为空字符串
            # 加载保存的设置
            self.加载设置()
            # 保存实例引用
            self.__class__._instance = self
        else:
            # 后续创建实例，使用已有设置
            existing = self.__class__._instance
            self.音乐开关 = existing.音乐开关
            self.音效开关 = existing.音效开关
            self.音量 = existing.音量
            self.帧率选择 = existing.帧率选择
            self.宽渲染 = getattr(existing, '宽渲染', 100)  # 获取宽渲染，默认100
            self.高渲染 = getattr(existing, '高渲染', 50)   # 获取高渲染，默认50
            self.特效渲染 = getattr(existing, '特效渲染', "标准")  # 获取特效渲染，默认标准
            self.显示攻击距离 = getattr(existing, '显示攻击距离', False)  # 获取显示攻击距离，默认关闭
            self.显示受伤距离 = getattr(existing, '显示受伤距离', False)  # 获取显示受伤距离，默认关闭
            self.帧率选项 = existing.帧率选项
            self.存档路径 = existing.存档路径
            self.玩家上传图片路径 = existing.玩家上传图片路径  # 添加这一行，确保复制玩家上传图片路径属性
            # 更新实例引用
            self.__class__._instance = self
        
        # 开关和滑块的尺寸和位置
        self.开关宽度 = 60
        self.开关高度 = 30
        self.滑块轨道高度 = 10
        self.滑块宽度 = 250
        self.滑块手柄宽度 = 20
        self.滑块手柄高度 = 20
        
        self.更新尺寸()
        self.更新按钮位置()
        # 应用设置
        self.应用设置()
    
    def 更新尺寸(self):
        """更新屏幕尺寸和位置信息"""
        self.屏幕宽度 = self.屏幕.get_width()
        self.屏幕高度 = self.屏幕.get_height()
        # 重新计算居中位置
        self.底1_x = (self.屏幕宽度 - self.底1宽度 - self.间隔 - self.底2宽度) // 2
        self.底2_x = self.底1_x + self.底1宽度 + self.间隔
        self.底_y = (self.屏幕高度 - max(self.底1高度, self.底2高度)) // 2
        # 更新按钮位置
        self.更新按钮位置()
    
    def draw_gradient_background(self):
        """绘制渐变背景"""
        # 从深蓝到浅蓝的垂直渐变
        start_color = (100, 100, 255)
        end_color = (150, 150, 255)
        
        for y in range(self.屏幕高度):
            # 计算当前行的颜色插值
            ratio = y / self.屏幕高度
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            # 绘制一行像素
            pygame.draw.line(self.屏幕, (r, g, b), (0, y), (self.屏幕宽度, y))
    
    def 更新按钮位置(self):
        """更新按钮位置信息"""
        # 按钮起始Y坐标（标题下方一定距离）
        起始_y = self.底_y + 80
        
        # 计算基础设置按钮位置
        self.基础设置按钮 = pygame.Rect(
            self.底1_x + 15, 起始_y,
            self.按钮宽度, self.按钮高度
        )
        
        # 计算存储设置按钮位置
        self.存储设置按钮 = pygame.Rect(
            self.底1_x + 15, 起始_y + self.按钮高度 + self.按钮间隔,
            self.按钮宽度, self.按钮高度
        )
        
        # 计算外观设置按钮位置（存储设置下方）
        self.按钮外观设置按钮 = pygame.Rect(
            self.底1_x + 15, 起始_y + (self.按钮高度 + self.按钮间隔) * 2,
            self.按钮宽度, self.按钮高度
        )
        
        # 计算底关闭按钮位置（靠近底部）
        self.关闭按钮 = pygame.Rect(
            self.底1_x + 15, self.底_y + self.底1高度 - 60,
            self.按钮宽度, self.按钮高度
        )
    
    def 绘制(self):
        # 首先更新尺寸
        self.更新尺寸()
        
        # 绘制背景：尝试使用图片加载器获取背景图1，失败则使用渐变
        背景图片 = 图片管理器.获取图片("背景图1")
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
            # 使用渐变背景
            self.draw_gradient_background()
        
        # 创建整个设置面板的外框（用于绘制阴影）
        总宽度 = self.底1宽度 + self.间隔 + self.底2宽度
        总高度 = max(self.底1高度, self.底2高度)
        总_x = (self.屏幕宽度 - 总宽度) // 2
        总_y = (self.屏幕高度 - 总高度) // 2
        
        # 绘制整个面板的阴影
        阴影表面 = pygame.Surface((总宽度 + 10, 总高度 + 10), pygame.SRCALPHA)
        pygame.draw.rect(阴影表面, 阴影颜色, (
            5, 5, 总宽度, 总高度), border_radius=self.圆角半径)
        self.屏幕.blit(阴影表面, (总_x - 5, 总_y - 5))
        
        # 绘制底1（左侧面板）带圆角
        pygame.draw.rect(self.屏幕, 次级背景色, 
                        (self.底1_x, self.底_y, self.底1宽度, self.底1高度), 
                        border_radius=self.圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (self.底1_x, self.底_y, self.底1宽度, self.底1高度), 
                        2, border_radius=self.圆角半径)
        
        # 绘制底2（右侧面板）带圆角
        pygame.draw.rect(self.屏幕, 主背景色, 
                        (self.底2_x, self.底_y, self.底2宽度, self.底2高度), 
                        border_radius=self.圆角半径)
        pygame.draw.rect(self.屏幕, 边框颜色, 
                        (self.底2_x, self.底_y, self.底2宽度, self.底2高度), 
                        2, border_radius=self.圆角半径)
        
        # 绘制左侧面板标题
        左侧标题 = self.标题字体.render("设置选项", True, 标题颜色)
        左侧标题_rect = 左侧标题.get_rect(center=(self.底1_x + self.底1宽度//2, self.底_y + 30))
        # 标题阴影
        左侧标题阴影 = self.标题字体.render("设置选项", True, (0, 0, 0, 50))
        self.屏幕.blit(左侧标题阴影, (左侧标题_rect.x + 1, 左侧标题_rect.y + 1))
        self.屏幕.blit(左侧标题, 左侧标题_rect)
        
        # 绘制右侧面板标题
        右侧标题 = self.标题字体.render("设置详情", True, 标题颜色)
        右侧标题_rect = 右侧标题.get_rect(center=(self.底2_x + self.底2宽度//2, self.底_y + 30))
        # 标题阴影
        右侧标题阴影 = self.标题字体.render("设置详情", True, (0, 0, 0, 50))
        self.屏幕.blit(右侧标题阴影, (右侧标题_rect.x + 1, 右侧标题_rect.y + 1))
        self.屏幕.blit(右侧标题, 右侧标题_rect)
        
        # 在底2标题下方添加95%白色区域（向下增加15像素）
        白色区域_y = self.底_y + 60  # 标题下方30像素
        白色区域_height = self.底2高度 - 75  # 留出底部空间，向下增加15像素
        白色区域_color = (242, 242, 242)  # 95%白色
        pygame.draw.rect(self.屏幕, 白色区域_color, 
                        (self.底2_x + 20, 白色区域_y, self.底2宽度 - 40, 白色区域_height), 
                        border_radius=8)
        # 添加边框
        pygame.draw.rect(self.屏幕, (220, 220, 220), 
                        (self.底2_x + 20, 白色区域_y, self.底2宽度 - 40, 白色区域_height), 
                        1, border_radius=8)
        
        # 根据当前选中的页面绘制相应内容
        if self.当前选中 == "基础设置":
            self.绘制基础设置()
        elif self.当前选中 == "存储设置":
            self.绘制存储设置()
        elif self.当前选中 == "外观设置":
            self.绘制按钮外观设置()
        
        # 绘制按钮
        self.绘制按钮()
    
    def 绘制基础设置(self):
        """绘制基础设置内容"""
        if self.当前选中 != "基础设置":
            return
        
        # 计算中心位置
        中心_x = self.底2_x + self.底2宽度 // 2
        内容_y = self.底_y + 120  # 白色区域内的起始位置
        
        # 第一行：音乐开关和音效开关（中心左右对称间隔10像素）
        开关行_y = 内容_y
        
        # 音乐标签和开关
        音乐文本 = self.文本字体.render("音乐", True, 文本颜色)
        音乐文本_rect = 音乐文本.get_rect(center=(中心_x - 120, 开关行_y))
        self.屏幕.blit(音乐文本, 音乐文本_rect)
        
        音乐开关_rect = pygame.Rect(中心_x - 90, 开关行_y - 15, self.开关宽度, self.开关高度)
        self.绘制开关(音乐开关_rect, self.音乐开关)
        
        # 音效标签和开关
        音效文本 = self.文本字体.render("音效", True, 文本颜色)
        音效文本_rect = 音效文本.get_rect(center=(中心_x + 90, 开关行_y))
        self.屏幕.blit(音效文本, 音效文本_rect)
        
        音效开关_rect = pygame.Rect(中心_x + 120, 开关行_y - 15, self.开关宽度, self.开关高度)
        self.绘制开关(音效开关_rect, self.音效开关)
        
        # 第二行：音量控制（250长）
        音量行_y = 内容_y + 60
        音量文本 = self.文本字体.render(f"{self.音量}%音量大小", True, 文本颜色)
        音量文本_rect = 音量文本.get_rect(center=(中心_x, 音量行_y - 10))
        self.屏幕.blit(音量文本, 音量文本_rect)
        
        滑块轨道_rect = pygame.Rect(中心_x - 125, 音量行_y + 15, self.滑块宽度, self.滑块轨道高度)
        # 计算滑块手柄位置（使用圆形手柄，中心位置）
        滑块_handle_x = 中心_x - 125 + (self.音量 / 100) * self.滑块宽度
        滑块_handle_rect = pygame.Rect(滑块_handle_x - 10, 音量行_y + 15 - 5, 20, 20)
        
        # 绘制滑块轨道（浅灰色背景）
        pygame.draw.rect(self.屏幕, (200, 200, 200), 滑块轨道_rect, border_radius=5)
        
        # 绘制滑块已填充部分（蓝色渐变效果）
        # 根据音量值动态调整填充颜色深度
        填充_color = (100 - self.音量 // 2, 149, 237)
        pygame.draw.rect(self.屏幕, 填充_color, 
                        (中心_x - 125, 音量行_y + 15, (self.音量 / 100) * self.滑块宽度, self.滑块轨道高度), 
                        border_radius=5)
        
        # 获取鼠标位置，用于交互效果
        鼠标位置 = pygame.mouse.get_pos()
        鼠标悬停 = 滑块_handle_rect.collidepoint(鼠标位置)
        
        # 绘制滑块手柄（更圆润、更现代的设计）
        # 手柄颜色根据交互状态变化
        if 鼠标悬停:
            手柄_color = (70, 130, 180)  # 蓝色
            # 添加阴影效果
            pygame.draw.circle(self.屏幕, (0, 0, 0, 30), (滑块_handle_rect.center[0] + 1, 滑块_handle_rect.center[1] + 1), 10)
        else:
            手柄_color = (100, 149, 237)  # 浅蓝色
        
        # 绘制圆形手柄
        pygame.draw.circle(self.屏幕, 手柄_color, 滑块_handle_rect.center, 10)
        # 添加高光效果
        pygame.draw.circle(self.屏幕, (255, 255, 255, 150), (滑块_handle_rect.center[0] - 3, 滑块_handle_rect.center[1] - 3), 4)
        
        # 第三行：帧率设置
        帧率行_y = 音量行_y + 70  # 向上移动10像素
        帧率文本 = self.文本字体.render("帧率设置", True, 文本颜色)
        帧率文本_rect = 帧率文本.get_rect(center=(中心_x, 帧率行_y - 20))  # 再向上移动10像素
        self.屏幕.blit(帧率文本, 帧率文本_rect)
        
        # 绘制帧率选项按钮
        按钮间距 = 10
        按钮宽度 = 80
        按钮高度 = 35
        
        for i, 帧率 in enumerate(self.帧率选项):
            # 计算按钮位置
            按钮_x = 中心_x - (len(self.帧率选项) * 按钮宽度 + (len(self.帧率选项) - 1) * 按钮间距) // 2 + i * (按钮宽度 + 按钮间距)
            按钮_y = 帧率行_y + 0  # 按钮y坐标也相应调整
            
            # 绘制帧率按钮
            按钮_rect = pygame.Rect(按钮_x, 按钮_y, 按钮宽度, 按钮高度)
            
            # 根据是否选中和鼠标状态设置按钮颜色
            if 帧率 == self.帧率选择:
                按钮_color = (144, 238, 144)  # 选中颜色（绿色）
            elif 按钮_rect.collidepoint(鼠标位置):
                按钮_color = (240, 240, 240)  # 悬停颜色
            else:
                按钮_color = (230, 230, 230)  # 正常颜色
            
            pygame.draw.rect(self.屏幕, 按钮_color, 按钮_rect, border_radius=6)
            pygame.draw.rect(self.屏幕, (200, 200, 200), 按钮_rect, 1, border_radius=6)
            
            # 绘制帧率按钮文本
            帧率按钮文本 = self.文本字体.render(f"{帧率}FPS", True, 文本颜色)
            帧率按钮文本_rect = 帧率按钮文本.get_rect(center=按钮_rect.center)
            self.屏幕.blit(帧率按钮文本, 帧率按钮文本_rect)
        
        # 第四行：渲染设置 - 宽渲染和高渲染放在同一行
        渲染行_y = 帧率行_y + 70
        
        # 宽渲染部分
        宽渲染文本 = self.文本字体.render("宽渲染：", True, 文本颜色)
        宽渲染文本_x = 中心_x - 200
        self.屏幕.blit(宽渲染文本, (宽渲染文本_x, 渲染行_y - 15))
        
        # 绘制宽渲染输入框（文字右侧10像素）
        输入框宽度 = 100
        输入框高度 = 30
        宽渲染输入框_rect = pygame.Rect(宽渲染文本_x + 宽渲染文本.get_width() + 10, 渲染行_y - 15, 输入框宽度, 输入框高度)
        
        # 绘制输入框背景
        pygame.draw.rect(self.屏幕, (255, 255, 255), 宽渲染输入框_rect, border_radius=4)
        pygame.draw.rect(self.屏幕, (200, 200, 200), 宽渲染输入框_rect, 1, border_radius=4)
        
        # 绘制宽渲染值
        宽渲染值文本 = self.文本字体.render(str(self.宽渲染), True, 文本颜色)
        宽渲染值_rect = 宽渲染值文本.get_rect(center=宽渲染输入框_rect.center)
        self.屏幕.blit(宽渲染值文本, 宽渲染值_rect)
        
        # 如果正在编辑宽渲染，添加光标效果
        if hasattr(self, '当前编辑输入框') and self.当前编辑输入框 == '宽渲染':
            # 闪烁光标
            if pygame.time.get_ticks() % 1000 < 500:
                光标_x = 宽渲染值_rect.right + 5
                光标_y1 = 宽渲染输入框_rect.top + 5
                光标_y2 = 宽渲染输入框_rect.bottom - 5
                pygame.draw.line(self.屏幕, 文本颜色, (光标_x, 光标_y1), (光标_x, 光标_y2), 2)
        
        # 高渲染部分（与宽渲染输入框间隔10像素）
        高渲染文本 = self.文本字体.render("高渲染：", True, 文本颜色)
        高渲染文本_x = 宽渲染输入框_rect.right + 10
        self.屏幕.blit(高渲染文本, (高渲染文本_x, 渲染行_y - 15))
        
        # 绘制高渲染输入框（文字右侧10像素）
        高渲染输入框_rect = pygame.Rect(高渲染文本_x + 高渲染文本.get_width() + 10, 渲染行_y - 15, 输入框宽度, 输入框高度)
        
        # 绘制输入框背景
        pygame.draw.rect(self.屏幕, (255, 255, 255), 高渲染输入框_rect, border_radius=4)
        pygame.draw.rect(self.屏幕, (200, 200, 200), 高渲染输入框_rect, 1, border_radius=4)
        
        # 绘制高渲染值
        高渲染值文本 = self.文本字体.render(str(self.高渲染), True, 文本颜色)
        高渲染值_rect = 高渲染值文本.get_rect(center=高渲染输入框_rect.center)
        self.屏幕.blit(高渲染值文本, 高渲染值_rect)
        
        # 如果正在编辑高渲染，添加光标效果
        if hasattr(self, '当前编辑输入框') and self.当前编辑输入框 == '高渲染':
            # 闪烁光标
            if pygame.time.get_ticks() % 1000 < 500:
                光标_x = 高渲染值_rect.right + 5
                光标_y1 = 高渲染输入框_rect.top + 5
                光标_y2 = 高渲染输入框_rect.bottom - 5
                pygame.draw.line(self.屏幕, 文本颜色, (光标_x, 光标_y1), (光标_x, 光标_y2), 2)
        
        # 特效渲染设置 - 在渲染坐标下方添加
        特效渲染行_y = 渲染行_y + 60
        
        # 特效渲染标题
        特效渲染文本 = self.文本字体.render("特效渲染：", True, 文本颜色)
        特效渲染文本_rect = 特效渲染文本.get_rect(center=(中心_x, 特效渲染行_y))
        self.屏幕.blit(特效渲染文本, 特效渲染文本_rect)
        
        # 特效渲染按钮设置
        特效渲染按钮_width = 80
        特效渲染按钮_height = 30
        特效渲染按钮_spacing = 15
        特效渲染按钮_y = 特效渲染行_y + 30
        
        # 计算按钮总宽度
        特效渲染按钮_total_width = 特效渲染按钮_width * 3 + 特效渲染按钮_spacing * 2
        特效渲染按钮_start_x = 中心_x - 特效渲染按钮_total_width // 2
        
        # 绘制最佳渲染按钮
        最佳按钮_rect = pygame.Rect(特效渲染按钮_start_x, 特效渲染按钮_y, 特效渲染按钮_width, 特效渲染按钮_height)
        最佳按钮_color = (144, 238, 144) if self.特效渲染 == "最佳" else (230, 230, 230)
        if 最佳按钮_rect.collidepoint(鼠标位置):
            最佳按钮_color = (240, 240, 240)
        pygame.draw.rect(self.屏幕, 最佳按钮_color, 最佳按钮_rect, border_radius=6)
        pygame.draw.rect(self.屏幕, (200, 200, 200), 最佳按钮_rect, 1, border_radius=6)
        最佳按钮文本 = self.文本字体.render("最佳", True, 文本颜色)
        最佳按钮文本_rect = 最佳按钮文本.get_rect(center=最佳按钮_rect.center)
        self.屏幕.blit(最佳按钮文本, 最佳按钮文本_rect)
        
        # 绘制标准渲染按钮
        标准按钮_rect = pygame.Rect(特效渲染按钮_start_x + 特效渲染按钮_width + 特效渲染按钮_spacing, 特效渲染按钮_y, 特效渲染按钮_width, 特效渲染按钮_height)
        标准按钮_color = (144, 238, 144) if self.特效渲染 == "标准" else (230, 230, 230)
        if 标准按钮_rect.collidepoint(鼠标位置):
            标准按钮_color = (240, 240, 240)
        pygame.draw.rect(self.屏幕, 标准按钮_color, 标准按钮_rect, border_radius=6)
        pygame.draw.rect(self.屏幕, (200, 200, 200), 标准按钮_rect, 1, border_radius=6)
        标准按钮文本 = self.文本字体.render("标准", True, 文本颜色)
        标准按钮文本_rect = 标准按钮文本.get_rect(center=标准按钮_rect.center)
        self.屏幕.blit(标准按钮文本, 标准按钮文本_rect)
        
        # 绘制关闭按钮
        关闭按钮_rect = pygame.Rect(特效渲染按钮_start_x + (特效渲染按钮_width + 特效渲染按钮_spacing) * 2, 特效渲染按钮_y, 特效渲染按钮_width, 特效渲染按钮_height)
        关闭按钮_color = (144, 238, 144) if self.特效渲染 == "关闭" else (230, 230, 230)
        if 关闭按钮_rect.collidepoint(鼠标位置):
            关闭按钮_color = (240, 240, 240)
        pygame.draw.rect(self.屏幕, 关闭按钮_color, 关闭按钮_rect, border_radius=6)
        pygame.draw.rect(self.屏幕, (200, 200, 200), 关闭按钮_rect, 1, border_radius=6)
        关闭按钮文本 = self.文本字体.render("关闭", True, 文本颜色)
        关闭按钮文本_rect = 关闭按钮文本.get_rect(center=关闭按钮_rect.center)
        self.屏幕.blit(关闭按钮文本, 关闭按钮文本_rect)
        
        # 保存按钮引用，用于点击检测
        self.特效渲染按钮_rects = {
            "最佳": 最佳按钮_rect,
            "标准": 标准按钮_rect,
            "关闭": 关闭按钮_rect
        }
        
        # 显示攻击距离和显示受伤距离按钮
        新按钮行_y = 特效渲染按钮_y + 50
        新按钮_width = 150
        新按钮_height = 35
        新按钮_spacing = 50
        
        # 计算按钮总宽度
        新按钮_total_width = 新按钮_width * 2 + 新按钮_spacing
        新按钮_start_x = 中心_x - 新按钮_total_width // 2
        
        # 绘制显示攻击距离按钮
        显示攻击距离按钮_rect = pygame.Rect(新按钮_start_x, 新按钮行_y, 新按钮_width, 新按钮_height)
        # 根据状态设置按钮颜色
        显示攻击距离按钮_color = (144, 238, 144) if self.显示攻击距离 else (230, 230, 230)  # 开启时显示绿色，关闭时显示灰色
        pygame.draw.rect(self.屏幕, 显示攻击距离按钮_color, 显示攻击距离按钮_rect, border_radius=6)
        pygame.draw.rect(self.屏幕, (200, 200, 200), 显示攻击距离按钮_rect, 1, border_radius=6)
        显示攻击距离文本 = self.文本字体.render("显示攻击距离", True, 文本颜色)
        显示攻击距离文本_rect = 显示攻击距离文本.get_rect(center=显示攻击距离按钮_rect.center)
        self.屏幕.blit(显示攻击距离文本, 显示攻击距离文本_rect)
        # 保存按钮引用，用于点击检测
        self.显示攻击距离按钮_rect = 显示攻击距离按钮_rect
        
        # 绘制显示受伤距离按钮
        显示受伤距离按钮_rect = pygame.Rect(新按钮_start_x + 新按钮_width + 新按钮_spacing, 新按钮行_y, 新按钮_width, 新按钮_height)
        # 根据状态设置按钮颜色
        显示受伤距离按钮_color = (144, 238, 144) if self.显示受伤距离 else (230, 230, 230)  # 开启时显示绿色，关闭时显示灰色
        pygame.draw.rect(self.屏幕, 显示受伤距离按钮_color, 显示受伤距离按钮_rect, border_radius=6)
        pygame.draw.rect(self.屏幕, (200, 200, 200), 显示受伤距离按钮_rect, 1, border_radius=6)
        显示受伤距离文本 = self.文本字体.render("显示受伤距离", True, 文本颜色)
        显示受伤距离文本_rect = 显示受伤距离文本.get_rect(center=显示受伤距离按钮_rect.center)
        self.屏幕.blit(显示受伤距离文本, 显示受伤距离文本_rect)
        # 保存按钮引用，用于点击检测
        self.显示受伤距离按钮_rect = 显示受伤距离按钮_rect
    
    def 创建圆角矩形(self, x1, y1, x2, y2, 圆角半径, color):
        """使用更简单的方法绘制圆角矩形"""
        # 绘制主体矩形（去掉圆角部分）
        pygame.draw.rect(self.屏幕, color, (x1 + 圆角半径, y1, x2 - x1 - 2 * 圆角半径, y2 - y1))
        pygame.draw.rect(self.屏幕, color, (x1, y1 + 圆角半径, x2 - x1, y2 - y1 - 2 * 圆角半径))
        
        # 绘制四个圆角（圆形）
        pygame.draw.circle(self.屏幕, color, (x1 + 圆角半径, y1 + 圆角半径), 圆角半径)
        pygame.draw.circle(self.屏幕, color, (x2 - 圆角半径, y1 + 圆角半径), 圆角半径)
        pygame.draw.circle(self.屏幕, color, (x1 + 圆角半径, y2 - 圆角半径), 圆角半径)
        pygame.draw.circle(self.屏幕, color, (x2 - 圆角半径, y2 - 圆角半径), 圆角半径)
    
    def 绘制开关(self, rect, is_on):
        """绘制开关按钮"""
        # 绘制开关背景
        if is_on:
            # 开启状态：绿色背景
            背景色 = (76, 175, 80)
        else:
            # 关闭状态：灰色背景
            背景色 = (200, 200, 200)
            
        # 绘制圆角矩形背景
        圆角半径 = rect[3] // 2
        self.创建圆角矩形(rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3], 圆角半径, 背景色)
        
        # 绘制开关圆点
        if is_on:
            # 开启状态：圆点在右侧
            圆点_x = rect[0] + rect[2] - rect[3] // 2
            圆点_y = rect[1] + rect[3] // 2
        else:
            # 关闭状态：圆点在左侧
            圆点_x = rect[0] + rect[3] // 2
            圆点_y = rect[1] + rect[3] // 2
            
        pygame.draw.circle(self.屏幕, (255, 255, 255), (圆点_x, 圆点_y), rect[3] // 2 - 2)
    
    def 绘制存储设置(self):
        """绘制存储设置内容"""
        if self.当前选中 != "存储设置":
            return
        
        # 计算中心位置
        中心_x = self.底2_x + self.底2宽度 // 2
        内容_y = self.底_y + 120  # 白色区域内的起始位置
        
        # 绘制标题
        存储设置标题 = self.标题字体.render("存档路径设置", True, 文本颜色)
        存储设置标题_rect = 存储设置标题.get_rect(center=(中心_x, 内容_y))
        self.屏幕.blit(存储设置标题, 存储设置标题_rect)
        
        # 存档路径显示和更换按钮
        路径行_y = 内容_y + 60
        
        # 绘制路径显示框
        路径框宽度 = self.底2宽度 - 200  # 留出更换按钮的空间
        路径框_x = 中心_x - (路径框宽度 + 100) // 2  # 路径框和按钮之间间隔10像素
        路径框_y = 路径行_y - 20
        路径框_height = 40
        
        # 绘制路径框背景
        pygame.draw.rect(self.屏幕, (255, 255, 255), 
                        (路径框_x, 路径框_y, 路径框宽度, 路径框_height), 
                        border_radius=6)
        pygame.draw.rect(self.屏幕, (200, 200, 200), 
                        (路径框_x, 路径框_y, 路径框宽度, 路径框_height), 
                        1, border_radius=6)
        
        # 绘制路径文本（限制长度，超出部分显示省略号）
        路径文本 = self.文本字体.render(self.存档路径, True, 文本颜色)
        # 如果文本太长，需要截断显示
        if 路径文本.get_width() > 路径框宽度 - 20:
            # 逐渐减少文本长度直到适合
            temp_path = self.存档路径
            while len(temp_path) > 0 and self.文本字体.render(temp_path + "...", True, 文本颜色).get_width() > 路径框宽度 - 20:
                temp_path = temp_path[:-1]
            路径文本 = self.文本字体.render(temp_path + "...", True, 文本颜色)
        
        路径文本_rect = 路径文本.get_rect(center=(路径框_x + 路径框宽度//2, 路径框_y + 路径框_height//2))
        self.屏幕.blit(路径文本, 路径文本_rect)
        
        # 绘制更换按钮
        更换按钮_width = 90
        更换按钮_height = 40
        更换按钮_x = 路径框_x + 路径框宽度 + 10
        更换按钮_y = 路径框_y
        
        # 绘制按钮背景
        鼠标位置 = pygame.mouse.get_pos()
        按钮_rect = pygame.Rect(更换按钮_x, 更换按钮_y, 更换按钮_width, 更换按钮_height)
        
        if 按钮_rect.collidepoint(鼠标位置):
            按钮_color = (240, 240, 240)  # 悬停颜色
        else:
            按钮_color = (230, 230, 230)  # 正常颜色
        
        pygame.draw.rect(self.屏幕, 按钮_color, 按钮_rect, border_radius=6)
        pygame.draw.rect(self.屏幕, (200, 200, 200), 按钮_rect, 1, border_radius=6)
        
        # 绘制按钮文本
        更换按钮文本 = self.按钮字体.render("更换", True, 文本颜色)
        更换按钮文本_rect = 更换按钮文本.get_rect(center=按钮_rect.center)
        self.屏幕.blit(更换按钮文本, 更换按钮文本_rect)
        
        # 保存按钮引用，用于点击检测
        self.更换路径按钮 = 按钮_rect
        
    def 绘制按钮(self):
        """绘制所有按钮"""
        # 获取鼠标位置
        鼠标位置 = pygame.mouse.get_pos()
        
        # 绘制基础设置按钮
        基础设置颜色 = self.按钮颜色
        if self.基础设置按钮.collidepoint(鼠标位置):
            基础设置颜色 = self.按钮悬停颜色
        if self.当前选中 == "基础设置":
            基础设置颜色 = self.按钮选中颜色
        
        pygame.draw.rect(self.屏幕, 基础设置颜色, self.基础设置按钮, border_radius=6)
        pygame.draw.rect(self.屏幕, self.按钮边框颜色, self.基础设置按钮, 1, border_radius=6)
        
        基础设置文本 = self.按钮字体.render("基础设置", True, 文本颜色)
        基础设置文本_rect = 基础设置文本.get_rect(center=self.基础设置按钮.center)
        self.屏幕.blit(基础设置文本, 基础设置文本_rect)
        
        # 绘制存储设置按钮
        存储设置颜色 = self.按钮颜色
        if self.存储设置按钮.collidepoint(鼠标位置):
            存储设置颜色 = self.按钮悬停颜色
        if self.当前选中 == "存储设置":
            存储设置颜色 = self.按钮选中颜色
        
        pygame.draw.rect(self.屏幕, 存储设置颜色, self.存储设置按钮, border_radius=6)
        pygame.draw.rect(self.屏幕, self.按钮边框颜色, self.存储设置按钮, 1, border_radius=6)
        
        存储设置文本 = self.按钮字体.render("存储设置", True, 文本颜色)
        存储设置文本_rect = 存储设置文本.get_rect(center=self.存储设置按钮.center)
        self.屏幕.blit(存储设置文本, 存储设置文本_rect)
        
        # 绘制外观设置按钮
        按钮外观设置颜色 = self.按钮颜色
        if self.按钮外观设置按钮.collidepoint(鼠标位置):
            按钮外观设置颜色 = self.按钮悬停颜色
        if self.当前选中 == "外观设置":
            按钮外观设置颜色 = self.按钮选中颜色
        
        pygame.draw.rect(self.屏幕, 按钮外观设置颜色, self.按钮外观设置按钮, border_radius=6)
        pygame.draw.rect(self.屏幕, self.按钮边框颜色, self.按钮外观设置按钮, 1, border_radius=6)
        
        按钮外观设置文本 = self.按钮字体.render("外观设置", True, 文本颜色)
        按钮外观设置文本_rect = 按钮外观设置文本.get_rect(center=self.按钮外观设置按钮.center)
        self.屏幕.blit(按钮外观设置文本, 按钮外观设置文本_rect)
        
        # 绘制关闭按钮
        关闭按钮颜色 = self.按钮颜色
        if self.关闭按钮.collidepoint(鼠标位置):
            关闭按钮颜色 = self.按钮悬停颜色
        
        pygame.draw.rect(self.屏幕, 关闭按钮颜色, self.关闭按钮, border_radius=6)
        pygame.draw.rect(self.屏幕, self.按钮边框颜色, self.关闭按钮, 1, border_radius=6)
        
        关闭按钮文本 = self.按钮字体.render("关闭", True, 文本颜色)
        关闭按钮文本_rect = 关闭按钮文本.get_rect(center=self.关闭按钮.center)
        self.屏幕.blit(关闭按钮文本, 关闭按钮文本_rect)
    
    def 处理上传按钮点击(self):
        """处理上传按钮点击事件"""
        import tkinter as tk
        from tkinter import filedialog
        from PIL import Image
        import os
        
        # 隐藏tkinter主窗口
        root = tk.Tk()
        root.withdraw()
        
        # 打开文件选择对话框，限制为png格式
        文件路径 = filedialog.askopenfilename(
            title="选择PNG图片文件",
            filetypes=[("PNG图片", "*.png")],
            initialdir=os.getcwd()
        )
        
        # 销毁tkinter窗口
        root.destroy()
        
        if 文件路径:
            try:
                # 检查文件是否为png格式
                if not 文件路径.lower().endswith(".png"):
                    print("请选择PNG格式的图片文件")
                    return
                
                # 使用PIL打开图片
                with Image.open(文件路径) as img:
                    # 计算新的尺寸，保持宽高比为1:2
                    新宽度 = 100  # 可以根据需要调整
                    新高度 = 新宽度 * 2
                    
                    # 调整图片大小
                    调整后的图片 = img.resize((新宽度, 新高度), Image.LANCZOS)
                    
                    # 保存调整后的图片到本地
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    保存目录 = os.path.join(script_dir, "图片", "上传")
                    if not os.path.exists(保存目录):
                        os.makedirs(保存目录)
                    
                    # 使用原文件名保存
                    文件名 = os.path.basename(文件路径)
                    保存路径 = os.path.join(保存目录, 文件名)
                    调整后的图片.save(保存路径, "PNG")
                    
                    # 更新设置中的路径
                    self.玩家上传图片路径 = 保存路径
                    
                    # 保存设置
                    self.保存设置()
                    print(f"图片已上传并调整大小，保存到: {保存路径}")
                    print(f"路径已保存到设置数据库")
            except Exception as e:
                print(f"处理图片时出错: {e}")
    
    def handle_event(self, 事件):
        # 处理ESC键关闭设置界面
        if 事件.type == pygame.KEYDOWN:
            if 事件.key == pygame.K_ESCAPE:
                # 退出前自动保存设置
                self.保存设置()
                return False  # 返回False表示关闭设置界面
            # 处理输入框编辑
            elif self.当前编辑输入框 is not None:
                # 处理回车键确认
                if 事件.key == pygame.K_RETURN:
                    # 应用数值限制
                    if self.当前编辑输入框 == '宽渲染':
                        # 宽渲染限制：10-10000
                        if self.宽渲染 < 10:
                            self.宽渲染 = 10
                        elif self.宽渲染 > 10000:
                            self.宽渲染 = 10000
                    else:
                        # 高渲染限制：10-600
                        if self.高渲染 < 10:
                            self.高渲染 = 10
                        elif self.高渲染 > 600:
                            self.高渲染 = 600
                    self.当前编辑输入框 = None
                    self.保存设置()
                    self.显示设置信息()
                # 处理退格键
                elif 事件.key == pygame.K_BACKSPACE:
                    if self.当前编辑输入框 == '宽渲染':
                        self.宽渲染 = int(str(self.宽渲染)[:-1] or '0')
                    else:
                        self.高渲染 = int(str(self.高渲染)[:-1] or '0')
                # 处理数字输入
                elif pygame.K_0 <= 事件.key <= pygame.K_9:
                    数字 = 事件.key - pygame.K_0
                    if self.当前编辑输入框 == '宽渲染':
                        new_value = int(str(self.宽渲染) + str(数字))
                        # 宽渲染限制：10-10000
                        if new_value <= 10000:
                            self.宽渲染 = new_value
                    else:
                        new_value = int(str(self.高渲染) + str(数字))
                        # 高渲染限制：10-600
                        if new_value <= 600:
                            self.高渲染 = new_value
                return True
            # 处理数字键1-10切换选中小底（带图片存在性检查）
            elif pygame.K_1 <= 事件.key <= pygame.K_9 or 事件.key == pygame.K_0:
                if 事件.key == pygame.K_0:
                    选中的小底 = 10  # 0键对应外观10
                else:
                    选中的小底 = 事件.key - pygame.K_0  # 转换为数字1-9
                
                # 检查是否可以切换到选中的小底
                can_switch = False
                if 选中的小底 == 1:
                    # 小底1：检查玩家上传图片是否存在
                    can_switch = bool(self.玩家上传图片路径 and os.path.exists(self.玩家上传图片路径))
                    if not can_switch:
                        print("无法选中小底1：未检测到上传图片")
                elif 选中的小底 == 2:
                    # 小底2：系统绘制，总是可以切换
                    can_switch = True
                elif 选中的小底 == 3:
                    # 小底3：检查骑士1_站立图片是否存在
                    can_switch = 图片管理器.图片是否已加载("骑士1_站立")
                    if not can_switch:
                        print("无法选中小底3：未检测到骑士1_站立图片")
                elif 选中的小底 == 4:
                    # 小底4：检查骑士2_站立图片是否存在
                    can_switch = 图片管理器.图片是否已加载("骑士2_站立")
                    if not can_switch:
                        print("无法选中小底4：未检测到骑士2_站立图片")
                elif 选中的小底 == 5:
                    # 小底5：检查骑士3图片是否存在
                    can_switch = 图片管理器.图片是否已加载("骑士3")
                    if not can_switch:
                        print("无法选中小底5：未检测到骑士3图片")
                elif 选中的小底 == 6:
                    # 小底6：检查小骑士图片是否存在
                    can_switch = 图片管理器.图片是否已加载("小骑士")
                    if not can_switch:
                        print("无法选中小底6：未检测到小骑士图片")
                elif 选中的小底 == 7:
                    # 小底7：检查猫猫1图片是否存在
                    can_switch = 图片管理器.图片是否已加载("猫猫1")
                    if not can_switch:
                        print("无法选中小底7：未检测到猫猫1图片")
                elif 选中的小底 == 8:
                    # 小底8：检查猫猫2图片是否存在
                    can_switch = 图片管理器.图片是否已加载("猫猫2")
                    if not can_switch:
                        print("无法选中小底8：未检测到猫猫2图片")
                elif 选中的小底 == 9:
                    # 小底9：检查猫猫3图片是否存在
                    can_switch = 图片管理器.图片是否已加载("猫猫3")
                    if not can_switch:
                        print("无法选中小底9：未检测到猫猫3图片")
                elif 选中的小底 == 10:
                    # 小底10：检查猫猫4图片是否存在
                    can_switch = 图片管理器.图片是否已加载("猫猫4")
                    if not can_switch:
                        print("无法选中小底10：未检测到猫猫4图片")
                
                # 特殊情况：如果再次选择小底1但图片不存在，强制切换到小底2
                if 选中的小底 == 1 and self.当前选中的小底 == 1 and not can_switch:
                    self.当前选中的小底 = 2
                    print("检测到小底1图片不存在，已自动切换到小底2")
                
                # 如果可以切换，则执行切换
                elif can_switch and 选中的小底 != self.当前选中的小底:
                    self.当前选中的小底 = 选中的小底
                    print(f"已选中小底{选中的小底}")
        # 处理窗口调整事件
        elif 事件.type == pygame.VIDEORESIZE:
            self.更新尺寸()
        # 处理鼠标点击事件
        elif 事件.type == pygame.MOUSEBUTTONDOWN:
            if 事件.button == 1:  # 左键点击
                return self.处理鼠标点击(事件.pos)
        # 处理鼠标滚轮事件（用于滚动角色列表）
        elif 事件.type == pygame.MOUSEWHEEL:
            if self.当前选中 == "外观设置":
                # 向下滚动（正数）：增加滑动偏移，向上滚动（负数）：减少滑动偏移
                self.滑动偏移 -= 事件.y * self.滑动速度
                # 限制滑动偏移范围
                self.滑动偏移 = max(0, min(self.滑动偏移, self.最大滑动偏移))
        # 处理鼠标拖拽事件（用于音量滑块）
        elif 事件.type == pygame.MOUSEMOTION:
            if 事件.buttons[0]:  # 左键按住拖动
                self.处理鼠标拖拽(事件.pos)
        return True  # 继续显示设置界面
    
    def 显示设置信息(self):
        """显示当前设置信息到终端"""
        import datetime
        当前时间 = datetime.datetime.now().strftime("%H:%M:%S")
        音乐状态 = "开" if self.音乐开关 else "关"
        音效状态 = "开" if self.音效开关 else "关"
        print(f"[{当前时间}]   [音乐:{音乐状态}]  [音效:{音效状态}]  [总音量:{self.音量}%]  [帧率:{self.帧率选择}FPS]  [存档路径:{self.存档路径}]")
    
    def 处理鼠标点击(self, 鼠标位置):
        """处理鼠标点击事件，增强交互体验"""
        # 检查外观设置中的小底透明按钮点击
        if self.当前选中 == "外观设置" and hasattr(self, '小底透明按钮_rects'):
            for i, 按钮_rect in enumerate(self.小底透明按钮_rects):
                if 按钮_rect and 按钮_rect.collidepoint(鼠标位置):
                    选中的小底 = i + 1  # 索引0-9对应小底1-10
                    
                    # 检查是否可以切换到选中的小底（和数字键切换逻辑相同）
                    can_switch = False
                    if 选中的小底 == 1:
                        # 小底1：检查玩家上传图片是否存在
                        can_switch = bool(self.玩家上传图片路径 and os.path.exists(self.玩家上传图片路径))
                        if not can_switch:
                            print("无法选中小底1：未检测到上传图片")
                    elif 选中的小底 == 2:
                        # 小底2：系统绘制，总是可以切换
                        can_switch = True
                    elif 选中的小底 == 3:
                        # 小底3：检查骑士1_站立图片是否存在
                        can_switch = 图片管理器.图片是否已加载("骑士1_站立")
                        if not can_switch:
                            print("无法选中小底3：未检测到骑士1_站立图片")
                    elif 选中的小底 == 4:
                        # 小底4：检查骑士2_站立图片是否存在
                        can_switch = 图片管理器.图片是否已加载("骑士2_站立")
                        if not can_switch:
                            print("无法选中小底4：未检测到骑士2_站立图片")
                    elif 选中的小底 == 5:
                        # 小底5：检查骑士3图片是否存在
                        can_switch = 图片管理器.图片是否已加载("骑士3")
                        if not can_switch:
                            print("无法选中小底5：未检测到骑士3图片")
                    elif 选中的小底 == 6:
                        # 小底6：检查小骑士图片是否存在
                        can_switch = 图片管理器.图片是否已加载("小骑士")
                        if not can_switch:
                            print("无法选中小底6：未检测到小骑士图片")
                    elif 选中的小底 == 7:
                        # 小底7：检查猫猫1图片是否存在
                        can_switch = 图片管理器.图片是否已加载("猫猫1")
                        if not can_switch:
                            print("无法选中小底7：未检测到猫猫1图片")
                    elif 选中的小底 == 8:
                        # 小底8：检查猫猫2图片是否存在
                        can_switch = 图片管理器.图片是否已加载("猫猫2")
                        if not can_switch:
                            print("无法选中小底8：未检测到猫猫2图片")
                    elif 选中的小底 == 9:
                        # 小底9：检查猫猫3图片是否存在
                        can_switch = 图片管理器.图片是否已加载("猫猫3")
                        if not can_switch:
                            print("无法选中小底9：未检测到猫猫3图片")
                    elif 选中的小底 == 10:
                        # 小底10：检查猫猫4图片是否存在
                        can_switch = 图片管理器.图片是否已加载("猫猫4")
                        if not can_switch:
                            print("无法选中小底10：未检测到猫猫4图片")
                    
                    # 特殊情况：如果再次选择小底1但图片不存在，强制切换到小底2
                    if 选中的小底 == 1 and self.当前选中的小底 == 1 and not can_switch:
                        self.当前选中的小底 = 2
                        print("检测到小底1图片不存在，已自动切换到小底2")
                        return True
                    
                    # 如果可以切换，则执行切换
                    if can_switch and 选中的小底 != self.当前选中的小底:
                        self.当前选中的小底 = 选中的小底
                        print(f"已选中小底{选中的小底}")
                        return True
                    
                    # 即使不能切换，也返回True以避免后续处理
                    return True
        
        # 检查外观设置中的上传按钮点击
        if self.当前选中 == "外观设置" and hasattr(self, '上传按钮_rects'):
            for i, 按钮_rect in enumerate(self.上传按钮_rects):
                if 按钮_rect and 按钮_rect.collidepoint(鼠标位置):
                    if i == 0:  # 上传按钮
                        self.处理上传按钮点击()
                        return True
        
        # 检查基础设置按钮
        if self.基础设置按钮.collidepoint(鼠标位置):
            audio_manager.play_click_sound()
            self.当前选中 = "基础设置"
            self.显示设置信息()
            return True
        # 检查存储设置按钮
        elif self.存储设置按钮.collidepoint(鼠标位置):
            audio_manager.play_click_sound()
            # 保存设置到文件
            self.保存设置()
            self.当前选中 = "存储设置"
            self.显示设置信息()
            return True
        # 检查外观设置按钮
        elif self.按钮外观设置按钮.collidepoint(鼠标位置):
            audio_manager.play_click_sound()
            # 保存设置到文件
            self.保存设置()
            self.当前选中 = "外观设置"
            print("已进入外观设置")
            self.显示设置信息()
            return True
        # 检查关闭按钮
        elif self.关闭按钮.collidepoint(鼠标位置):
            audio_manager.play_click_sound()
            # 退出前自动保存设置
            self.保存设置()
            self.显示设置信息()
            return False  # 返回False表示关闭设置界面
        
        # 如果当前选中的是基础设置，处理设置内容的点击
        if self.当前选中 == "基础设置":
            中心_x = self.底2_x + self.底2宽度 // 2
            内容_y = self.底_y + 120
            
            # 计算渲染设置输入框位置（同一行显示）
            输入框宽度 = 100
            输入框高度 = 30
            帧率行_y = 内容_y + 60 + 70  # 在音量下方70像素（向上移动10像素）
            渲染行_y = 帧率行_y + 70
            
            # 宽渲染部分位置计算
            宽渲染文本 = self.文本字体.render("宽渲染：", True, (0, 0, 0))
            宽渲染文本_x = 中心_x - 200
            宽渲染输入框_rect = pygame.Rect(宽渲染文本_x + 宽渲染文本.get_width() + 10, 渲染行_y - 15, 输入框宽度, 输入框高度)
            
            # 高渲染部分位置计算
            高渲染文本 = self.文本字体.render("高渲染：", True, (0, 0, 0))
            高渲染文本_x = 宽渲染输入框_rect.right + 10
            高渲染输入框_rect = pygame.Rect(高渲染文本_x + 高渲染文本.get_width() + 10, 渲染行_y - 15, 输入框宽度, 输入框高度)
            
            # 特效渲染按钮位置计算
            特效渲染行_y = 渲染行_y + 60
            特效渲染按钮_width = 80
            特效渲染按钮_height = 30
            特效渲染按钮_spacing = 15
            特效渲染按钮_y = 特效渲染行_y + 30
            特效渲染按钮_total_width = 特效渲染按钮_width * 3 + 特效渲染按钮_spacing * 2
            特效渲染按钮_start_x = 中心_x - 特效渲染按钮_total_width // 2
            
            # 计算特效渲染按钮矩形
            最佳按钮_rect = pygame.Rect(特效渲染按钮_start_x, 特效渲染按钮_y, 特效渲染按钮_width, 特效渲染按钮_height)
            标准按钮_rect = pygame.Rect(特效渲染按钮_start_x + 特效渲染按钮_width + 特效渲染按钮_spacing, 特效渲染按钮_y, 特效渲染按钮_width, 特效渲染按钮_height)
            关闭按钮_rect = pygame.Rect(特效渲染按钮_start_x + (特效渲染按钮_width + 特效渲染按钮_spacing) * 2, 特效渲染按钮_y, 特效渲染按钮_width, 特效渲染按钮_height)
            
            # 检查特效渲染按钮点击
            if 最佳按钮_rect.collidepoint(鼠标位置):
                self.特效渲染 = "最佳"
                self.保存设置()
                self.显示设置信息()
                return True
            elif 标准按钮_rect.collidepoint(鼠标位置):
                self.特效渲染 = "标准"
                self.保存设置()
                self.显示设置信息()
                return True
            elif 关闭按钮_rect.collidepoint(鼠标位置):
                self.特效渲染 = "关闭"
                self.保存设置()
                self.显示设置信息()
                return True
            
            # 检查渲染设置输入框点击
            elif 宽渲染输入框_rect.collidepoint(鼠标位置):
                self.当前编辑输入框 = '宽渲染'
                return True
            elif 高渲染输入框_rect.collidepoint(鼠标位置):
                self.当前编辑输入框 = '高渲染'
                return True
            # 检查显示攻击距离按钮点击
            elif hasattr(self, '显示攻击距离按钮_rect') and self.显示攻击距离按钮_rect.collidepoint(鼠标位置):
                self.显示攻击距离 = not self.显示攻击距离
                self.保存设置()
                self.显示设置信息()
                return True
            # 检查显示受伤距离按钮点击
            elif hasattr(self, '显示受伤距离按钮_rect') and self.显示受伤距离按钮_rect.collidepoint(鼠标位置):
                self.显示受伤距离 = not self.显示受伤距离
                self.保存设置()
                self.显示设置信息()
                return True
            elif self.当前编辑输入框 is not None:
                # 点击其他地方，结束编辑
                self.当前编辑输入框 = None
                self.保存设置()
                self.显示设置信息()
            
            # 检查音乐开关点击
            音乐开关_rect = pygame.Rect(中心_x - 90, 内容_y - 15, self.开关宽度, self.开关高度)
            if 音乐开关_rect.collidepoint(鼠标位置):
                self.音乐开关 = not self.音乐开关
                self.应用设置()
                self.显示设置信息()
                # 播放点击音效
                audio_manager.play_click_sound()
                return True
            
            # 检查音效开关点击
            音效开关_rect = pygame.Rect(中心_x + 120, 内容_y - 15, self.开关宽度, self.开关高度)
            if 音效开关_rect.collidepoint(鼠标位置):
                self.音效开关 = not self.音效开关
                self.应用设置()
                self.显示设置信息()
                # 播放点击音效（仅当关闭音效前）
                if not self.音效开关:
                    audio_manager.play_click_sound()
                return True
            
            # 检查音量滑块点击
            音量行_y = 内容_y + 60
            滑块轨道_rect = pygame.Rect(中心_x - 125, 音量行_y + 15, self.滑块宽度, self.滑块轨道高度)
            
            # 计算滑块手柄位置，用于检测点击
            滑块_handle_x = 中心_x - 125 + (self.音量 / 100) * self.滑块宽度
            滑块_handle_rect = pygame.Rect(滑块_handle_x - 10, 音量行_y + 15 - 5, 20, 20)
            
            if 滑块轨道_rect.collidepoint(鼠标位置) or 滑块_handle_rect.collidepoint(鼠标位置):
                # 计算点击位置对应的音量值
                相对位置 = (鼠标位置[0] - 滑块轨道_rect.x) / self.滑块宽度
                新音量 = max(0, min(100, int(相对位置 * 100)))
                
                # 仅当音量变化时才更新
                if 新音量 != self.音量:
                    self.音量 = 新音量
                    self.应用设置()
                    self.显示设置信息()
                    # 播放音量调节音效
                    audio_manager.play_click_sound()
                return True
            
            # 检查帧率选项点击
            帧率行_y = 内容_y + 60 + 70  # 在音量下方70像素（向上移动10像素）
            按钮间距 = 10
            按钮宽度 = 80
            按钮高度 = 35
            
            for 帧率 in self.帧率选项:
                按钮_x = 中心_x - (len(self.帧率选项) * 按钮宽度 + (len(self.帧率选项) - 1) * 按钮间距) // 2 + self.帧率选项.index(帧率) * (按钮宽度 + 按钮间距)
                按钮_y = 帧率行_y + 0  # 按钮y坐标也相应调整
                按钮_rect = pygame.Rect(按钮_x, 按钮_y, 按钮宽度, 按钮高度)
                
                if 按钮_rect.collidepoint(鼠标位置):
                    if 帧率 != self.帧率选择:
                        self.帧率选择 = 帧率
                        self.应用设置()
                        self.显示设置信息()
                        # 播放点击音效
                        audio_manager.play_click_sound()
                    return True
        # 如果当前选中的是存储设置，处理设置内容的点击
        elif self.当前选中 == "存储设置":
            # 检查更换路径按钮点击
            if hasattr(self, '更换路径按钮') and self.更换路径按钮.collidepoint(鼠标位置):
                # 打开文件夹选择对话框
                import tkinter as tk
                from tkinter import filedialog
                # 隐藏tkinter主窗口
                root = tk.Tk()
                root.withdraw()
                # 打开文件夹选择对话框
                新路径 = filedialog.askdirectory(title="选择存档文件夹", initialdir=self.存档路径)
                # 如果用户选择了文件夹
                if 新路径:
                    self.存档路径 = 新路径
                    self.保存设置()  # 立即保存新路径
                    self.显示设置信息()
                    # 播放点击音效
                    audio_manager.play_click_sound()
                # 销毁tkinter窗口
                root.destroy()
                return True
        
        return True  # 继续显示设置界面
    
    def 保存设置(self):
        """保存设置到文件，按优先级规则：当前目录 > C盘备用路径"""
        import json
        import os
        设置数据 = {
            "音乐开关": self.音乐开关,
            "音效开关": self.音效开关,
            "音量": self.音量,
            "帧率选择": self.帧率选择,
            "宽渲染": self.宽渲染,
            "高渲染": self.高渲染,
            "存档路径": self.存档路径,
            "玩家上传图片路径": self.玩家上传图片路径,
            "当前选择外观": self.当前选中的小底,
            "特效渲染": self.特效渲染,
            "显示攻击距离": self.显示攻击距离,
            "显示受伤距离": self.显示受伤距离
        }
        
        # 1. 优先保存到脚本目录的 "设置_数据库.json"
        try:
            # 获取脚本所在目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            主设置文件路径 = os.path.join(script_dir, "设置_数据库.json")
            with open(主设置文件路径, "w", encoding="utf-8") as f:
                json.dump(设置数据, f, ensure_ascii=False, indent=2)
            print(f"设置已保存到脚本目录: {主设置文件路径}")
            return True
        except Exception as e:
            print(f"保存设置到脚本目录失败: {e}")
            # 2. 如果脚本目录保存失败，尝试在备用设置目录下创建文件
            try:
                # 获取脚本所在目录
                script_dir = os.path.dirname(os.path.abspath(__file__))
                备用路径 = os.path.join(script_dir, "备用设置")  # 使用脚本目录的绝对路径
                if not os.path.exists(备用路径):
                    os.makedirs(备用路径)
                备用文件路径 = os.path.join(备用路径, "设置_数据库.json")
                with open(备用文件路径, "w", encoding="utf-8") as f:
                    json.dump(设置数据, f, ensure_ascii=False, indent=2)
                print(f"设置已保存到备用路径: {备用文件路径}")
                return True
            except Exception as e2:
                print(f"保存设置到备用路径也失败: {e2}")
                return False
    
    def 加载设置(self):
        """从文件加载设置，按优先级规则：当前目录 > C盘备用路径 > 创建默认设置"""
        import json
        import os
        已加载 = False
        
        # 1. 优先从脚本目录加载 "设置_数据库.json"
        try:
            # 获取脚本所在目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            主设置文件路径 = os.path.join(script_dir, "设置_数据库.json")
            if os.path.exists(主设置文件路径):
                with open(主设置文件路径, "r", encoding="utf-8") as f:
                    设置数据 = json.load(f)
                    if "音乐开关" in 设置数据:
                        self.音乐开关 = 设置数据["音乐开关"]
                    if "音效开关" in 设置数据:
                        self.音效开关 = 设置数据["音效开关"]
                    if "音量" in 设置数据:
                        self.音量 = 设置数据["音量"]
                    if "帧率选择" in 设置数据:
                        self.帧率选择 = 设置数据["帧率选择"]
                    if "宽渲染" in 设置数据:
                        # 宽渲染限制：100-5000
                        self.宽渲染 = 设置数据["宽渲染"]
                        if self.宽渲染 < 100:
                            self.宽渲染 = 100
                        elif self.宽渲染 > 5000:
                            self.宽渲染 = 5000
                    if "高渲染" in 设置数据:
                        # 高渲染限制：100-600
                        self.高渲染 = 设置数据["高渲染"]
                        if self.高渲染 < 100:
                            self.高渲染 = 100
                        elif self.高渲染 > 600:
                            self.高渲染 = 600
                    if "存档路径" in 设置数据:
                        # 验证存档路径是否存在，如果不存在则使用默认路径
                        if os.path.exists(设置数据["存档路径"]):
                            self.存档路径 = 设置数据["存档路径"]
                        else:
                            print(f"加载的存档路径不存在: {设置数据['存档路径']}，使用默认路径")
                    if "玩家上传图片路径" in 设置数据:
                        self.玩家上传图片路径 = 设置数据["玩家上传图片路径"]
                    # 加载当前选择外观设置
                    if "当前选择外观" in 设置数据:
                        self.当前选中的小底 = 设置数据["当前选择外观"]
                    # 加载特效渲染设置
                    if "特效渲染" in 设置数据:
                        self.特效渲染 = 设置数据["特效渲染"]
                    # 加载显示距离设置
                    if "显示攻击距离" in 设置数据:
                        self.显示攻击距离 = 设置数据["显示攻击距离"]
                    if "显示受伤距离" in 设置数据:
                        self.显示受伤距离 = 设置数据["显示受伤距离"]
                print("设置已从当前目录加载")
                已加载 = True
        except Exception as e:
            print(f"从当前目录加载设置失败: {e}")
        
        # 2. 若脚本目录文件不存在，尝试从备用设置目录加载
        if not 已加载:
            try:
                # 获取脚本所在目录
                script_dir = os.path.dirname(os.path.abspath(__file__))
                备用文件路径 = os.path.join(script_dir, "备用设置", "设置_数据库.json")  # 使用脚本目录的绝对路径
                if os.path.exists(备用文件路径):
                    with open(备用文件路径, "r", encoding="utf-8") as f:
                        设置数据 = json.load(f)
                        if "音乐开关" in 设置数据:
                            self.音乐开关 = 设置数据["音乐开关"]
                        if "音效开关" in 设置数据:
                            self.音效开关 = 设置数据["音效开关"]
                        if "音量" in 设置数据:
                            self.音量 = 设置数据["音量"]
                        if "帧率选择" in 设置数据:
                            self.帧率选择 = 设置数据["帧率选择"]
                        # 添加宽渲染和高渲染设置的加载
                        if "宽渲染" in 设置数据:
                            # 宽渲染限制：100-5000
                            self.宽渲染 = 设置数据["宽渲染"]
                            if self.宽渲染 < 100:
                                self.宽渲染 = 100
                            elif self.宽渲染 > 5000:
                                self.宽渲染 = 5000
                        if "高渲染" in 设置数据:
                            # 高渲染限制：100-600
                            self.高渲染 = 设置数据["高渲染"]
                            if self.高渲染 < 100:
                                self.高渲染 = 100
                            elif self.高渲染 > 600:
                                self.高渲染 = 600
                        if "存档路径" in 设置数据:
                            # 验证存档路径是否存在，如果不存在则使用默认路径
                            if os.path.exists(设置数据["存档路径"]):
                                self.存档路径 = 设置数据["存档路径"]
                            else:
                                print(f"加载的存档路径不存在: {设置数据['存档路径']}，使用默认路径")
                        # 加载玩家上传图片路径
                        if "玩家上传图片路径" in 设置数据:
                            self.玩家上传图片路径 = 设置数据["玩家上传图片路径"]
                        # 备用路径也需要加载当前选择外观设置
                        if "当前选择外观" in 设置数据:
                            self.当前选中的小底 = 设置数据["当前选择外观"]
                        # 备用路径加载特效渲染设置
                        if "特效渲染" in 设置数据:
                            self.特效渲染 = 设置数据["特效渲染"]
                        # 备用路径加载显示距离设置
                        if "显示攻击距离" in 设置数据:
                            self.显示攻击距离 = 设置数据["显示攻击距离"]
                        if "显示受伤距离" in 设置数据:
                            self.显示受伤距离 = 设置数据["显示受伤距离"]
                    print(f"设置已从备用路径加载: {备用文件路径}")
                    已加载 = True
            except Exception as e:
                print(f"从备用路径加载设置失败: {e}")
        
        # 3. 确保默认存档路径存在
        默认存档路径 = os.path.join(os.getcwd(), "存档")
        if not os.path.exists(self.存档路径):
            print(f"存档路径不存在，设置为默认路径: {默认存档路径}")
            self.存档路径 = 默认存档路径
            # 尝试创建默认存档文件夹
            if not os.path.exists(self.存档路径):
                try:
                    os.makedirs(self.存档路径)
                    print(f"已创建默认存档文件夹: {self.存档路径}")
                except Exception as e:
                    print(f"创建默认存档文件夹失败: {e}")
        
        # 4. 若两个文件均不存在，尝试创建默认设置
        if not 已加载:
            print("未找到设置文件，开始按优先级创建默认设置")
            self.保存设置()  # 保存设置方法会按优先级尝试创建文件
    
    def 应用设置(self):
        """应用当前设置到pygame"""
        # 更新单例实例中的值
        if hasattr(self.__class__, '_instance'):
            self.__class__._instance.音乐开关 = self.音乐开关
            self.__class__._instance.音效开关 = self.音效开关
            self.__class__._instance.音量 = self.音量
            self.__class__._instance.帧率选择 = self.帧率选择
            self.__class__._instance.存档路径 = self.存档路径
        
        # 应用音量设置
        volume_level = self.音量 / 100.0
        pygame.mixer.music.set_volume(volume_level if self.音乐开关 else 0)
        # 注意：音效的音量需要在播放时单独设置
        
        # 帧率设置会在主循环中使用
        # 确保存档路径存在
        import os
        if not os.path.exists(self.存档路径):
            try:
                os.makedirs(self.存档路径)
                print(f"已创建存档文件夹: {self.存档路径}")
            except Exception as e:
                print(f"创建存档文件夹失败: {e}")
    
    def 绘制按钮外观设置(self):
        """绘制外观设置内容"""
        if self.当前选中 != "外观设置":
            return
        
        # 绘制5个小底（微灰底），比例宽1高2
        白色区域_x = self.底2_x + 20
        白色区域_y = self.底_y + 60
        白色区域_width = self.底2宽度 - 40
        白色区域_height = self.底2高度 - 75
        
        # 显示区域高度
        self.显示区域高度 = 白色区域_height
        
        # 计算每个小底的尺寸和位置
        小底_width = int(白色区域_width * 0.15)  # 小底宽度为白色区域宽度的15%
        小底_height = 小底_width * 2  # 高度为宽度的2倍
        间距 = 30  # 固定间隔10像素
        行间距 = 80  # 行间距
        
        # 计算起始X坐标，使其居中排列
        每行数量 = 5
        总宽度 = 每行数量 * 小底_width + (每行数量 - 1) * 间距
        起始_x = 白色区域_x + (白色区域_width - 总宽度) // 2
        
        # 微灰色背景色
        微灰底颜色 = (220, 220, 220)
        边框颜色 = (200, 200, 200)
        
        # 角色列表，包含10个角色（索引0-9对应角色1-10）
        角色列表 = [
            {"名称": "上传角色", "类型": "upload"},
            {"名称": "系统角色", "类型": "system"},
            {"名称": "骑士1", "类型": "knight", "图片前缀": "骑士1", "图片列表": ["骑士1_站立", "骑士1_行走", "骑士1_跳跃"]},
            {"名称": "骑士2", "类型": "knight", "图片前缀": "骑士2", "图片列表": ["骑士2_站立", "骑士2_行走", "骑士2_跳跃"]},
            {"名称": "骑士3", "类型": "knight", "图片前缀": "骑士3", "图片列表": ["骑士3", "骑士3_跳跃", "骑士3_行走"]},
            {"名称": "小骑士", "类型": "knight", "图片前缀": "小骑士", "图片列表": ["小骑士", "小骑士_跳跃", "小骑士_行走"]},
            {"名称": "猫猫1", "类型": "cat", "图片前缀": "猫猫1", "图片列表": ["猫猫1", "猫猫1_行走", "猫猫1_跳跃"]},
            {"名称": "猫猫2", "类型": "cat", "图片前缀": "猫猫2", "图片列表": ["猫猫2", "猫猫2_行走", "猫猫2_跳跃"]},
            {"名称": "猫猫3", "类型": "cat", "图片前缀": "猫猫3", "图片列表": ["猫猫3", "猫猫3_行走", "猫猫3_跳跃"]},
            {"名称": "猫猫4", "类型": "cat", "图片前缀": "猫猫4", "图片列表": ["猫猫4", "猫猫4_行走", "猫猫4_跳跃"]}
        ]
        
        # 计算滑动容器相关参数
        角色数量 = len(角色列表)
        行数 = (角色数量 + 每行数量 - 1) // 每行数量  # 计算需要的行数
        self.滑动容器高度 = 行数 * (小底_height + 行间距) - 行间距
        
        # 计算最大滑动偏移
        self.最大滑动偏移 = max(0, self.滑动容器高度 - self.显示区域高度 + 50)  # +50是为了底部留些空间
        
        # 应用滑动偏移，计算起始Y坐标
        起始_y = 白色区域_y - self.滑动偏移 + 20  # +20是为了顶部留些空间
        
        # 绘制角色小底，支持多行显示
        for i, 角色 in enumerate(角色列表):
            # 计算行号和列号
            行号 = i // 每行数量
            列号 = i % 每行数量
            
            # 计算小底位置
            小底_x = 起始_x + 列号 * (小底_width + 间距)
            小底_y = 起始_y + 行号 * (小底_height + 行间距)
            
            # 小骑士（索引5）和猫猫1-4（索引6-9）的底向上移动20像素
            if i in [5, 6, 7, 8, 9]:
                小底_y -= 20
            小底_rect = pygame.Rect(小底_x, 小底_y, 小底_width, 小底_height)
            
            # 绘制微灰色背景
            pygame.draw.rect(self.屏幕, 微灰底颜色, 小底_rect, border_radius=4)
            
            # 为每个小底添加透明覆盖按钮
            # 初始化透明按钮矩形列表
            if not hasattr(self, '小底透明按钮_rects'):
                self.小底透明按钮_rects = []
            # 确保列表长度足够
            while len(self.小底透明按钮_rects) <= i:
                self.小底透明按钮_rects.append(None)
            # 存储小底的矩形区域作为透明按钮
            self.小底透明按钮_rects[i] = 小底_rect.copy()
            
            # 绘制边框：如果是选中的小底，则边框变绿
            if (i + 1) == self.当前选中的小底:
                选中边框颜色 = (0, 255, 0)  # 绿色边框
                pygame.draw.rect(self.屏幕, 选中边框颜色, 小底_rect, 3, border_radius=4)  # 更粗的边框
            else:
                pygame.draw.rect(self.屏幕, 边框颜色, 小底_rect, 1, border_radius=4)
            
            # 在小底内部加载图片
            if 角色["类型"] in ["knight", "cat"]:
                try:
                    # 导入random和time模块
                    import random
                    import time
                    
                    # 获取当前时间秒数，用于每1秒更新一次
                    current_time = int(time.time())
                    
                    # 为每个角色实例存储上次更新时间和当前图片
                    if not hasattr(self, '角色更新时间'):
                        self.角色更新时间 = {}
                        self.角色当前图片 = {}
                    
                    # 检查是否需要更新图片（每1秒）
                    角色_key = 角色["图片前缀"]
                    if 角色_key not in self.角色更新时间 or current_time - self.角色更新时间[角色_key] >= 1:
                        # 随机选择一张图片
                        selected_image = random.choice(角色["图片列表"])
                        # 从图片管理器获取图片
                        self.角色当前图片[角色_key] = 图片管理器.获取图片(selected_image)
                        # 更新时间戳
                        self.角色更新时间[角色_key] = current_time
                    
                    # 只有当图片获取成功时才绘制
                    if self.角色当前图片.get(角色_key):
                        # 对于1:1比例角色（骑士3、小骑士和猫猫1-4），使用1:1比例并增加50%大小
                        if 角色_key in ["骑士3", "小骑士", "猫猫1", "猫猫2", "猫猫3", "猫猫4"]:
                            # 计算1:1尺寸，取小底宽度和高度中的较小值，然后增加50%
                            基础尺寸 = min(小底_width - 10, 小底_height - 10)
                            尺寸 = int(基础尺寸 * 1.5)  # 增加50%大小
                            # 缩放图片为1:1比例
                            缩放后的图片 = pygame.transform.scale(self.角色当前图片[角色_key], (尺寸, 尺寸))
                            # 居中显示
                            绘制_x = 小底_x + (小底_width - 尺寸) // 2
                            绘制_y = 小底_y + (小底_height - 尺寸) // 2
                            self.屏幕.blit(缩放后的图片, (绘制_x, 绘制_y))
                        else:
                            # 其他角色保持原有比例
                            缩放后的图片 = pygame.transform.scale(self.角色当前图片[角色_key], (小底_width - 10, 小底_height - 10))
                            # 居中显示
                            self.屏幕.blit(缩放后的图片, (小底_x + 5, 小底_y + 5))
                except Exception as e:
                    print(f"加载{角色['名称']}图片失败: {e}")
            
            # 在小底下方添加内容
            if i == 0:  # 第1个小底（索引为0）：生成上传按钮
                # 按钮尺寸
                按钮宽度 = 80
                按钮高度 = 30
                # 按钮位置（在小底下方居中）
                按钮_x = 小底_x + (小底_width - 按钮宽度) // 2
                按钮_y = 起始_y + 小底_height + 20 - 12  # 向上移动12像素
                # 创建按钮矩形用于检测点击
                上传按钮_rect = pygame.Rect(按钮_x, 按钮_y, 按钮宽度, 按钮高度)
                # 绘制按钮背景
                pygame.draw.rect(self.屏幕, (200, 200, 200), 上传按钮_rect, border_radius=4)
                # 绘制按钮边框
                pygame.draw.rect(self.屏幕, (150, 150, 150), 上传按钮_rect, 2, border_radius=4)
                # 按钮文字
                按钮_font = pygame.font.SysFont("Microsoft YaHei", 20)
                按钮文本 = 按钮_font.render("上传", True, (0, 0, 0))
                按钮文本_rect = 按钮文本.get_rect(center=(按钮_x + 按钮宽度 // 2, 按钮_y + 按钮高度 // 2))
                self.屏幕.blit(按钮文本, 按钮文本_rect)
                # 存储按钮矩形供点击检测使用
                if not hasattr(self, '上传按钮_rects'):
                    self.上传按钮_rects = []
                # 确保列表长度足够
                while len(self.上传按钮_rects) <= i:
                    self.上传按钮_rects.append(None)
                self.上传按钮_rects[i] = 上传按钮_rect
                
                # 如果有玩家上传的图片路径，在小底内显示图片
                if self.玩家上传图片路径 and os.path.exists(self.玩家上传图片路径):
                    try:
                        上传图片 = pygame.image.load(self.玩家上传图片路径)
                        # 缩放图片以适应小底大小
                        缩放后的图片 = pygame.transform.scale(上传图片, (小底_width - 10, 小底_height - 10))
                        # 居中显示
                        self.屏幕.blit(缩放后的图片, (小底_x + 5, 起始_y + 5))
                    except Exception as e:
                        print(f"加载玩家上传图片失败: {e}")
            else:  # 其他小底显示文本
                文本_font = pygame.font.SysFont("Microsoft YaHei", 24)
                if i == 1:  # 第2个小底（索引为1）
                    文本内容 = "系统绘制"
                    # 系统绘制玩家图像
                    if i == 1:  # 在第2个小底中绘制玩家
                        try:
                            # 设置玩家颜色常量
                            PLAYER_SKIN = (255, 223, 186)  # 皮肤色
                            PLAYER_SHIRT = (70, 130, 180)   # 蓝色衣服
                            PLAYER_PANTS = (30, 30, 100)    # 深蓝色裤子
                            
                            # 计算绘制区域，缩小40%（乘以0.6）
                            scale_factor = 0.6
                            original_width = 小底_width - 10
                            original_height = 小底_height - 10
                            player_width = int(original_width * scale_factor)
                            player_height = int(original_height * scale_factor)
                            
                            # 居中显示并整体向下移动50像素
                            draw_x = 小底_x + 5 + (original_width - player_width) // 2
                            draw_y = 起始_y + 5 + (original_height - player_height) // 2 + 35
                            
                            # 身体
                            pygame.draw.rect(self.屏幕, PLAYER_SKIN, (draw_x, draw_y, player_width, player_height))
                            
                            # 衣服
                            pygame.draw.rect(self.屏幕, PLAYER_SHIRT, 
                                            (draw_x, draw_y + player_height // 3, player_width, player_height // 3))
                            pygame.draw.rect(self.屏幕, PLAYER_PANTS,
                                            (draw_x, draw_y + player_height * 2 // 3, player_width, player_height // 3))
                            
                            # 头部（向上移动15像素）
                            head_size = int(min(player_width // 2, player_height // 3))
                            head_x = draw_x + player_width // 2
                            head_y = draw_y - head_size // 3 - 15
                            pygame.draw.circle(self.屏幕, PLAYER_SKIN, (head_x, head_y), head_size)
                            
                            # 眼睛 - 只绘制右眼（不绘制黑点）
                            eye_size = head_size // 5
                            eye_offset = head_size // 3
                            pygame.draw.circle(self.屏幕, (255, 255, 255), 
                                            (head_x + eye_offset, head_y - eye_size), eye_size)
                        except Exception as e:
                            print(f"绘制玩家图像失败: {e}")
                elif i == 2:  # 第3个小底（索引为2）
                    文本内容 = "骑士1"
                elif i == 3:  # 第4个小底（索引为3）
                    文本内容 = "骑士2"
                elif i == 4:  # 第5个小底（索引为4）
                    文本内容 = "骑士3"
                elif i == 5:  # 第6个小底（索引为5）
                    文本内容 = "小骑士"
                elif i == 6:  # 第7个小底（索引为6）
                    文本内容 = "猫猫1"
                elif i == 7:  # 第8个小底（索引为7）
                    文本内容 = "猫猫2"
                elif i == 8:  # 第9个小底（索引为8）
                    文本内容 = "猫猫3"
                elif i == 9:  # 第10个小底（索引为9）
                    文本内容 = "猫猫4"
                文本_surface = 文本_font.render(文本内容, True, (0, 0, 0))
                # 计算每个小底下方的文本位置，确保文本显示在对应小底下方
                文本_y = 小底_y + 小底_height + 25
                文本_rect = 文本_surface.get_rect(center=(小底_x + 小底_width/2, 文本_y))
                self.屏幕.blit(文本_surface, 文本_rect)
    
    def 处理鼠标拖拽(self, 鼠标位置):
        """处理鼠标拖拽事件（用于音量滑块）"""
        if self.当前选中 == "基础设置":
            中心_x = self.底2_x + self.底2宽度 // 2
            内容_y = self.底_y + 120
            音量行_y = 内容_y + 60
            滑块轨道_rect = pygame.Rect(中心_x - 125, 音量行_y + 15, self.滑块宽度, self.滑块轨道高度)
            
            # 只有当鼠标在滑块轨道上时才处理音量变化
            if 滑块轨道_rect.collidepoint(鼠标位置):
                # 计算拖拽位置对应的音量值
                相对位置 = max(0, min(1, (鼠标位置[0] - 滑块轨道_rect.x) / self.滑块宽度))
                新音量 = int(相对位置 * 100)
                
                # 检查音量是否有变化
                if 新音量 != self.音量:
                    变化量 = abs(新音量 - self.音量)
                    self.音量 = 新音量
                    self.应用设置()
                    
                    # 显示设置信息
                    self.显示设置信息()
                    
                    # 播放音量调节音效（如果音效开启）
                    if self.音效开关:
                        # 这里可以添加音量调节音效的代码
                        pass

# 示例使用方法
def 主函数():
    # 创建一个适合展示设置界面的窗口
    屏幕 = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    # 初始化设置界面
    设置界面实例 = 设置界面(屏幕)
    
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
                # 传递事件给设置界面处理
                if not 设置界面实例.handle_event(事件):
                    运行中 = False
                    
            # 处理窗口调整事件
            if 事件.type == pygame.VIDEORESIZE:
                # 更新屏幕尺寸
                屏幕 = pygame.display.set_mode((事件.w, 事件.h), pygame.RESIZABLE)
                # 重新初始化设置界面以适应新尺寸
                设置界面实例 = 设置界面(屏幕)
        
        # 绘制设置界面
        设置界面实例.绘制()
        
        # 刷新屏幕
        pygame.display.flip()
        
        # 控制帧率
        clock.tick(60)
    
    # 退出pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    主函数()