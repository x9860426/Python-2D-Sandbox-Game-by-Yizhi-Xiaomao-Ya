import pygame
import os
# 导入图片管理器全局实例
from 图片加载 import 图片管理器

class 存档处理界面:
    def __init__(self, 窗口):
        self.窗口 = 窗口
        self.宽度 = 窗口.get_width()
        self.高度 = 窗口.get_height()
        
        # 初始化中文字体
        try:
            self.中字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 29)  # 减小20% (36*0.8=28.8≈29)
            self.小字体 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 19)  # 减小20% (24*0.8=19.2≈19)
        except:
            self.中字体 = pygame.font.SysFont('Arial', 29)
            self.小字体 = pygame.font.SysFont('Arial', 19)
        
        # 颜色定义
        self.白色 = (255, 255, 255)
        self.黑色 = (0, 0, 0)
        self.灰色 = (200, 200, 200)
        self.浅灰色 = (230, 230, 230)
        self.深灰色 = (150, 150, 150)
        self.按钮默认 = (100, 150, 100)
        self.按钮悬停 = (130, 180, 130)
        self.按钮按下 = (70, 120, 70)
        self.按钮文字 = self.白色
        self.导入按钮默认 = (120, 100, 180)
        self.导入按钮悬停 = (150, 130, 210)
        self.导入按钮按下 = (90, 70, 150)
        
        # 按钮尺寸和位置
        self.按钮宽度 = 200
        self.按钮高度 = 60
        self.按钮间距 = 30
        
        # 创建返回按钮，下降20像素
        self.返回按钮 = pygame.Rect(
            (self.宽度 - self.按钮宽度 * 2 - self.按钮间距) // 2,
            self.高度 - self.按钮高度 - 30,
            self.按钮宽度,
            self.按钮高度
        )
        
        # 创建创建新世界按钮，下降20像素
        self.创建新世界按钮 = pygame.Rect(
            (self.宽度 + self.按钮间距) // 2,
            self.高度 - self.按钮高度 - 30,
            self.按钮宽度,
            self.按钮高度
        )
        
        # 中心底的位置和尺寸
        self.中心底_width = self.宽度 * 0.8
        self.中心底_height = self.高度 * 0.7 + 100  # 增加100像素高度
        # 向上移动50像素
        self.中心底 = pygame.Rect(
            (self.宽度 - self.中心底_width) // 2,
            (self.高度 - self.中心底_height) // 2 - 50,
            self.中心底_width,
            self.中心底_height
        )
        
        # 按钮状态
        self.返回按钮_悬停 = False
        self.返回按钮_按下 = False
        self.创建新世界按钮_悬停 = False
        self.创建新世界按钮_按下 = False
        
        # 存档列表
        self.存档列表 = []
        self.加载存档列表()
        
        # 滚动功能相关变量
        self.滚动偏移量 = 0  # 存档列表的滚动偏移量
        self.存档_height = 60  # 每个存档项的高度
        self.选中存档_height = self.存档_height + 100  # 选中存档项的高度（增加20像素）
        self.存档间距 = 10  # 存档项之间的间距
        # 可滚动区域，调整高度以一次显示6个存档项，向下移动50像素
        self.可滚动区域 = pygame.Rect(
            self.中心底.x + 20,
            self.中心底.y + 150,
            self.中心底_width - 40,
            6 * self.存档_height + 5 * self.存档间距  # 6个存档项的总高度
        )
        self.滚动条_width = 8  # 滚动条宽度
        self.滚动条_height = 0  # 滚动条高度
        self.滚动条_pos = 0  # 滚动条位置
        self.滚动条_hover = False  # 滚动条是否被悬停
        self.滚动条_dragging = False  # 滚动条是否被拖动
        self.鼠标_hover_可滚动区域 = False  # 鼠标是否悬停在可滚动区域
        
        # 选中状态相关变量
        self.选中存档索引 = None  # 当前选中的存档索引
        
        # 删除存档确认相关变量
        self.删除确认状态 = 0  # 0: 未确认, 1: 第一次确认, 2: 第二次确认, 3: 第三次确认
        self.删除确认目标索引 = None  # 要删除的存档索引
        self.删除确认倒计时 = 0  # 确认倒计时，防止快速点击
        self.删除确认位置 = None  # 确认提示的位置
        
        # 更改存档名称相关变量
        self.更改名称状态 = 0  # 0: 未更改, 1: 正在更改
        self.更改名称目标索引 = None  # 要更改名称的存档索引
        self.新存档名称 = ""  # 新的存档名称
        self.输入框焦点 = False  # 输入框是否获得焦点
        
        # 更改存档图片相关变量
        self.更改图片状态 = 0  # 0: 未更改, 1: 正在更改
        self.更改图片目标索引 = None  # 要更改图片的存档索引
        self.上次选择路径 = os.path.expanduser("~")  # 上次选择的图片路径，默认为用户主目录
        self.图片底_color = (255, 255, 255)  # 图片底颜色，默认为白色
        
        # 背景图片将在绘制时通过图片加载器获取
        
        # 初始更新滚动条（必须在选中存档索引初始化之后）
        self.更新滚动条()
    
    def 加载存档列表(self):
        """加载所有存档"""
        # 这里可以实现加载存档的逻辑
        # 暂时添加一些测试数据，从3个增加到20个
        self.存档列表 = [
            {
                "名称": f"测试存档{i}", 
                "日期": f"2025-12-{28 - (i-1) % 30:02d}", 
                "大小": f"{1.0 + (i-1) * 0.1:.1f}MB",
                "上次游玩时间": f"2025-12-{28 - (i-1) % 30:02d} 14:{30 + i % 30:02d}",
                "文件夹大小": f"{1.5 + (i-1) * 0.2:.1f}MB",
                "文件路径": f"存档/测试存档{i}"
            }
            for i in range(1, 21)
        ]
    
    def 绘制(self):
        """绘制导入存档界面"""
        # 绘制背景图片：尝试使用图片加载器获取背景图2，失败则使用默认背景
        背景图片 = 图片管理器.获取图片("背景图2")
        if 背景图片 is not None:
            # 计算缩放比例，保持图片的原始宽高比
            图片宽度 = 背景图片.get_width()
            图片高度 = 背景图片.get_height()
            
            # 计算缩放后的尺寸，保持原始宽高比
            缩放比例 = max(self.宽度 / 图片宽度, self.高度 / 图片高度)
            新宽度 = int(图片宽度 * 缩放比例)
            新高度 = int(图片高度 * 缩放比例)
            
            # 缩放图片
            缩放背景图 = pygame.transform.scale(背景图片, (新宽度, 新高度))
            
            # 计算居中位置
            x = (self.宽度 - 新宽度) // 2
            y = (self.高度 - 新高度) // 2
            
            # 绘制背景图
            self.窗口.blit(缩放背景图, (x, y))
        
        # 绘制中心底（保持固定大小）
        pygame.draw.rect(self.窗口, self.浅灰色, self.中心底, border_radius=10)
        pygame.draw.rect(self.窗口, self.深灰色, self.中心底, 2, border_radius=10)
        
        # 绘制标题，向上移动8像素
        标题文字 = self.中字体.render("导入存档", True, self.黑色)
        标题_rect = 标题文字.get_rect(center=(self.宽度 // 2, self.中心底.y + 32))
        self.窗口.blit(标题文字, 标题_rect)
        
        # 绘制存档列表
        累积_y = 0
        可见存档列表 = []
        
        # 首先计算所有存档项的位置和可见性
        for i, 存档 in enumerate(self.存档列表):
            # 确定当前存档项的高度
            current_height = self.选中存档_height if i == self.选中存档索引 else self.存档_height
            
            # 计算当前存档项的y位置
            存档_y = self.可滚动区域.y + 累积_y - self.滚动偏移量
            
            # 保存可见的存档项信息
            if 存档_y + current_height > self.可滚动区域.y and 存档_y < self.可滚动区域.y + self.可滚动区域.height:
                可见存档列表.append((i, 存档, 存档_y, current_height))
            
            # 累积y坐标，加上当前高度和间距
            累积_y += current_height + self.存档间距
        
        # 绘制可见的存档项
        for i, 存档, 存档_y, current_height in 可见存档列表:
            存档_rect = pygame.Rect(
                self.可滚动区域.x,
                存档_y,
                self.可滚动区域.width - self.滚动条_width - 10,  # 留出滚动条的空间
                current_height
            )
            
            # 绘制存档项背景，选中状态使用不同颜色
            if i == self.选中存档索引:
                pygame.draw.rect(self.窗口, self.浅灰色, 存档_rect, border_radius=5)
                pygame.draw.rect(self.窗口, self.深灰色, 存档_rect, 2, border_radius=5)  # 绘制选项底边框
                
                # 在选中的存档项中绘制详细信息，各项间距减小3像素
                # 绘制存档名称
                名称文字 = self.中字体.render(f"存档名称: {存档['名称']}", True, self.黑色)
                self.窗口.blit(名称文字, (存档_rect.x + 20, 存档_rect.y + 15))
                
                # 绘制上次游玩时间（间距27像素）
                上次游玩时间文字 = self.小字体.render(f"上次游玩时间: {存档['上次游玩时间']}", True, self.深灰色)
                self.窗口.blit(上次游玩时间文字, (存档_rect.x + 20, 存档_rect.y + 42))
                
                # 绘制文件夹大小（间距27像素）
                文件夹大小文字 = self.小字体.render(f"文件夹大小: {存档['文件夹大小']}", True, self.深灰色)
                self.窗口.blit(文件夹大小文字, (存档_rect.x + 20, 存档_rect.y + 69))
                
                # 绘制文件路径（间距27像素）
                文件路径文字 = self.小字体.render(f"文件路径: {存档['文件路径']}", True, self.深灰色)
                self.窗口.blit(文件路径文字, (存档_rect.x + 20, 存档_rect.y + 96))
                
                # 绘制4:3图片底
                图片底_width = 160
                图片底_height = 120  # 4:3比例
                图片底 = pygame.Rect(
                    存档_rect.right - 图片底_width - 20,
                    存档_rect.y + 15,
                    图片底_width,
                    图片底_height
                )
                pygame.draw.rect(self.窗口, self.白色, 图片底, border_radius=5)
                pygame.draw.rect(self.窗口, self.深灰色, 图片底, 1, border_radius=5)
                
                # 绘制功能按钮（间距27像素）
                按钮_width = 90
                按钮_height = 30
                按钮_start_x = 存档_rect.x + 20
                按钮_y = 存档_rect.y + 123
                按钮_spacing = 10
                
                # 进入存档按钮
                进入存档按钮 = pygame.Rect(按钮_start_x, 按钮_y, 按钮_width, 按钮_height)
                pygame.draw.rect(self.窗口, self.按钮默认, 进入存档按钮, border_radius=5)
                进入存档文字 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 16).render("进入存档", True, self.按钮文字)
                进入存档文字_rect = 进入存档文字.get_rect(center=进入存档按钮.center)
                self.窗口.blit(进入存档文字, 进入存档文字_rect)
                
                # 删除存档按钮
                删除存档按钮 = pygame.Rect(按钮_start_x + 按钮_width + 按钮_spacing, 按钮_y, 按钮_width, 按钮_height)
                # 根据确认状态改变按钮颜色
                if self.删除确认状态 > 0 and self.删除确认目标索引 == i:
                    # 确认过程中，按钮变红
                    pygame.draw.rect(self.窗口, (255, 50, 50), 删除存档按钮, border_radius=5)
                    删除存档文字 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 16).render(f"确认删除({self.删除确认状态}/3)", True, self.按钮文字)
                else:
                    pygame.draw.rect(self.窗口, (200, 100, 100), 删除存档按钮, border_radius=5)
                    删除存档文字 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 16).render("删除存档", True, self.按钮文字)
                删除存档文字_rect = 删除存档文字.get_rect(center=删除存档按钮.center)
                self.窗口.blit(删除存档文字, 删除存档文字_rect)
                
                # 更改存档名称按钮
                更改存档名称按钮 = pygame.Rect(按钮_start_x + (按钮_width + 按钮_spacing) * 2, 按钮_y, 按钮_width, 按钮_height)
                pygame.draw.rect(self.窗口, self.导入按钮默认, 更改存档名称按钮, border_radius=5)
                更改存档名称文字 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 16).render("更改名称", True, self.按钮文字)
                更改存档名称文字_rect = 更改存档名称文字.get_rect(center=更改存档名称按钮.center)
                self.窗口.blit(更改存档名称文字, 更改存档名称文字_rect)
                
                # 更改存档图片按钮
                更改存档图片按钮 = pygame.Rect(按钮_start_x + (按钮_width + 按钮_spacing) * 3, 按钮_y, 按钮_width, 按钮_height)
                pygame.draw.rect(self.窗口, self.导入按钮默认, 更改存档图片按钮, border_radius=5)
                更改存档图片文字 = pygame.font.SysFont(['SimHei', 'Microsoft YaHei', 'Arial'], 16).render("更改图片", True, self.按钮文字)
                更改存档图片文字_rect = 更改存档图片文字.get_rect(center=更改存档图片按钮.center)
                self.窗口.blit(更改存档图片文字, 更改存档图片文字_rect)
            else:
                pygame.draw.rect(self.窗口, self.白色, 存档_rect, border_radius=5)
                pygame.draw.rect(self.窗口, self.深灰色, 存档_rect, 1, border_radius=5)
                
                # 绘制存档名称
                名称文字 = self.中字体.render(存档["名称"], True, self.黑色)
                名称_rect = 名称文字.get_rect(midleft=(存档_rect.x + 20, 存档_rect.centery))
                self.窗口.blit(名称文字, 名称_rect)
                
                # 绘制存档信息
                信息文字 = self.小字体.render(f"日期: {存档['日期']} | 大小: {存档['大小']}", True, self.深灰色)
                信息_rect = 信息文字.get_rect(midright=(存档_rect.right - 20, 存档_rect.centery))
                self.窗口.blit(信息文字, 信息_rect)
        
        # 绘制滚动条
        if self.滚动条_height > 0:
            # 绘制滚动轨道
            滚动轨道_rect = pygame.Rect(
                self.可滚动区域.right - self.滚动条_width - 5,
                self.可滚动区域.y,
                self.滚动条_width,
                self.可滚动区域.height
            )
            pygame.draw.rect(self.窗口, self.灰色, 滚动轨道_rect, border_radius=4)
            
            # 绘制滚动滑块
            滚动滑块_rect = pygame.Rect(
                self.可滚动区域.right - self.滚动条_width - 5,
                self.滚动条_pos,
                self.滚动条_width,
                self.滚动条_height
            )
            if self.滚动条_hover or self.滚动条_dragging:
                pygame.draw.rect(self.窗口, self.深灰色, 滚动滑块_rect, border_radius=4)
            else:
                pygame.draw.rect(self.窗口, self.浅灰色, 滚动滑块_rect, border_radius=4)
        
        # 绘制返回按钮
        if self.返回按钮_按下:
            按钮颜色 = self.按钮按下
        elif self.返回按钮_悬停:
            按钮颜色 = self.按钮悬停
        else:
            按钮颜色 = self.按钮默认
        pygame.draw.rect(self.窗口, 按钮颜色, self.返回按钮, border_radius=5)
        pygame.draw.rect(self.窗口, self.深灰色, self.返回按钮, 2, border_radius=5)
        
        返回文字 = self.中字体.render("返回", True, self.按钮文字)
        返回文字_rect = 返回文字.get_rect(center=self.返回按钮.center)
        self.窗口.blit(返回文字, 返回文字_rect)
        
        # 绘制创建新世界按钮
        if self.创建新世界按钮_按下:
            按钮颜色 = self.导入按钮按下
        elif self.创建新世界按钮_悬停:
            按钮颜色 = self.导入按钮悬停
        else:
            按钮颜色 = self.导入按钮默认
        pygame.draw.rect(self.窗口, 按钮颜色, self.创建新世界按钮, border_radius=5)
        pygame.draw.rect(self.窗口, self.深灰色, self.创建新世界按钮, 2, border_radius=5)
        
        创建新世界文字 = self.中字体.render("创建新世界", True, self.按钮文字)
        创建新世界文字_rect = 创建新世界文字.get_rect(center=self.创建新世界按钮.center)
        self.窗口.blit(创建新世界文字, 创建新世界文字_rect)
        
        # 绘制删除确认提示
        if self.删除确认状态 > 0:
            # 创建半透明黑色背景
            确认背景 = pygame.Surface((self.宽度, self.高度), pygame.SRCALPHA)
            pygame.draw.rect(确认背景, (0, 0, 0, 150), (0, 0, self.宽度, self.高度))
            self.窗口.blit(确认背景, (0, 0))
            
            # 确认框尺寸
            确认框_width = 400
            确认框_height = 200
            确认框_rect = pygame.Rect(
                (self.宽度 - 确认框_width) // 2,
                (self.高度 - 确认框_height) // 2,
                确认框_width,
                确认框_height
            )
            
            # 绘制确认框
            pygame.draw.rect(self.窗口, self.白色, 确认框_rect, border_radius=10)
            pygame.draw.rect(self.窗口, self.深灰色, 确认框_rect, 2, border_radius=10)
            
            # 绘制确认标题
            确认标题 = self.中字体.render("删除存档确认", True, self.黑色)
            确认标题_rect = 确认标题.get_rect(center=(确认框_rect.centerx, 确认框_rect.y + 40))
            self.窗口.blit(确认标题, 确认标题_rect)
            
            # 绘制确认提示文字
            if self.删除确认状态 == 1:
                确认文字 = self.小字体.render("您确定要删除这个存档吗？", True, self.黑色)
            elif self.删除确认状态 == 2:
                确认文字 = self.小字体.render("这是第二次确认！确定要删除吗？", True, self.黑色)
            else:
                确认文字 = self.小字体.render("最后一次确认！确定删除该存档？", True, self.黑色)
            
            确认文字_rect = 确认文字.get_rect(center=(确认框_rect.centerx, 确认框_rect.centery))
            self.窗口.blit(确认文字, 确认文字_rect)
            
            # 绘制存档名称
            存档名称文字 = self.小字体.render(f"存档名称: {self.存档列表[self.删除确认目标索引]['名称']}", True, self.深灰色)
            存档名称_rect = 存档名称文字.get_rect(center=(确认框_rect.centerx, 确认框_rect.centery + 30))
            self.窗口.blit(存档名称文字, 存档名称_rect)
            
            # 绘制确认和取消按钮
            按钮_width = 120
            按钮_height = 40
            按钮_spacing = 40
            按钮_y = 确认框_rect.y + 确认框_height - 60
            
            # 取消按钮
            取消按钮 = pygame.Rect(
                (self.宽度 - 按钮_width * 2 - 按钮_spacing) // 2,
                按钮_y,
                按钮_width,
                按钮_height
            )
            pygame.draw.rect(self.窗口, self.灰色, 取消按钮, border_radius=5)
            取消文字 = self.小字体.render("取消", True, self.按钮文字)
            取消文字_rect = 取消文字.get_rect(center=取消按钮.center)
            self.窗口.blit(取消文字, 取消文字_rect)
            
            # 确认按钮
            确认按钮 = pygame.Rect(
                (self.宽度 + 按钮_spacing) // 2,
                按钮_y,
                按钮_width,
                按钮_height
            )
            # 根据确认状态改变按钮颜色
            if self.删除确认状态 == 3:
                确认按钮_color = (255, 50, 50)  # 最后一次确认，红色
            else:
                确认按钮_color = (200, 100, 100)  # 前两次确认，橙色
            pygame.draw.rect(self.窗口, 确认按钮_color, 确认按钮, border_radius=5)
            确认文字 = self.小字体.render("确认", True, self.按钮文字)
            确认文字_rect = 确认文字.get_rect(center=确认按钮.center)
            self.窗口.blit(确认文字, 确认文字_rect)
        
        # 绘制更改存档名称输入框
        if self.更改名称状态 == 1:
            # 创建半透明黑色背景
            背景 = pygame.Surface((self.宽度, self.高度), pygame.SRCALPHA)
            pygame.draw.rect(背景, (0, 0, 0, 150), (0, 0, self.宽度, self.高度))
            self.窗口.blit(背景, (0, 0))
            
            # 输入框背景尺寸
            输入框_width = 400
            输入框_height = 150
            输入框_rect = pygame.Rect(
                (self.宽度 - 输入框_width) // 2,
                (self.高度 - 输入框_height) // 2,
                输入框_width,
                输入框_height
            )
            
            # 绘制输入框背景
            pygame.draw.rect(self.窗口, self.白色, 输入框_rect, border_radius=10)
            pygame.draw.rect(self.窗口, self.深灰色, 输入框_rect, 2, border_radius=10)
            
            # 绘制标题
            标题文字 = self.中字体.render("更改存档名称", True, self.黑色)
            标题_rect = 标题文字.get_rect(center=(输入框_rect.centerx, 输入框_rect.y + 30))
            self.窗口.blit(标题文字, 标题_rect)
            
            # 绘制输入框
            输入框内_rect = pygame.Rect(
                输入框_rect.x + 50,
                输入框_rect.y + 60,
                输入框_rect.width - 100,
                40
            )
            # 根据焦点状态改变边框颜色
            输入框颜色 = self.深灰色 if self.输入框焦点 else self.灰色
            pygame.draw.rect(self.窗口, self.浅灰色, 输入框内_rect, border_radius=5)
            pygame.draw.rect(self.窗口, 输入框颜色, 输入框内_rect, 2, border_radius=5)
            
            # 绘制输入的文字
            输入文字 = self.小字体.render(self.新存档名称, True, self.黑色)
            self.窗口.blit(输入文字, (输入框内_rect.x + 10, 输入框内_rect.y + 10))
            
            # 绘制光标
            if self.输入框焦点 and int(pygame.time.get_ticks() / 500) % 2 == 0:
                光标_x = 输入框内_rect.x + 10 + self.小字体.size(self.新存档名称)[0]
                光标_rect = pygame.Rect(光标_x, 输入框内_rect.y + 10, 2, self.小字体.size("A")[1])
                pygame.draw.rect(self.窗口, self.黑色, 光标_rect)
            
            # 绘制提示文字
            提示文字 = self.小字体.render("按Enter确认，按ESC取消", True, self.深灰色)
            提示_rect = 提示文字.get_rect(center=(输入框_rect.centerx, 输入框_rect.y + 110))
            self.窗口.blit(提示文字, 提示_rect)
    
    def handle_event(self, 事件):
        """处理事件"""
        鼠标位置 = pygame.mouse.get_pos()
        
        # 更新按钮悬停状态
        self.返回按钮_悬停 = self.返回按钮.collidepoint(鼠标位置)
        self.创建新世界按钮_悬停 = self.创建新世界按钮.collidepoint(鼠标位置)
        
        # 更新鼠标悬停可滚动区域状态
        self.鼠标_hover_可滚动区域 = self.可滚动区域.collidepoint(鼠标位置)
        
        # 更新滚动条悬停状态
        if self.滚动条_height > 0:
            滚动滑块_rect = pygame.Rect(
                self.可滚动区域.right - self.滚动条_width - 5,
                self.滚动条_pos,
                self.滚动条_width,
                self.滚动条_height
            )
            self.滚动条_hover = 滚动滑块_rect.collidepoint(鼠标位置)
        
        if 事件.type == pygame.MOUSEBUTTONDOWN:
            if 事件.button == 1:  # 左键点击
                # 如果正在删除确认状态，先处理确认框按钮
                if self.删除确认状态 > 0:
                    # 确认框按钮位置
                    确认框_width = 400
                    确认框_height = 200
                    确认框_x = (self.宽度 - 确认框_width) // 2
                    确认框_y = (self.高度 - 确认框_height) // 2
                    
                    # 按钮尺寸
                    按钮_width = 120
                    按钮_height = 40
                    按钮_spacing = 40
                    按钮_y = 确认框_y + 确认框_height - 60
                    
                    # 取消按钮
                    取消按钮 = pygame.Rect(
                        (self.宽度 - 按钮_width * 2 - 按钮_spacing) // 2,
                        按钮_y,
                        按钮_width,
                        按钮_height
                    )
                    
                    # 确认按钮
                    确认按钮 = pygame.Rect(
                        (self.宽度 + 按钮_spacing) // 2,
                        按钮_y,
                        按钮_width,
                        按钮_height
                    )
                    
                    # 检查是否点击了取消按钮
                    if 取消按钮.collidepoint(鼠标位置):
                        # 播放点击音效
                        from 音频输出 import audio_manager
                        audio_manager.play_click_sound()
                        # 取消删除确认
                        self.删除确认状态 = 0
                        self.删除确认目标索引 = None
                        return True
                    
                    # 检查是否点击了确认按钮
                    elif 确认按钮.collidepoint(鼠标位置):
                        # 播放点击音效
                        from 音频输出 import audio_manager
                        audio_manager.play_click_sound()
                        
                        if self.删除确认状态 < 3:
                            # 继续确认流程
                            self.删除确认状态 += 1
                        else:
                            # 第三次确认，执行删除
                            if 0 <= self.删除确认目标索引 < len(self.存档列表):
                                存档 = self.存档列表[self.删除确认目标索引]
                                print(f"删除存档: {存档['名称']}")
                                # 执行删除存档的逻辑
                                self.存档列表.pop(self.删除确认目标索引)
                                # 如果删除的是当前选中的存档，取消选中状态
                                if self.选中存档索引 == self.删除确认目标索引:
                                    self.选中存档索引 = None
                                # 如果删除的是前面的存档，调整选中索引
                                elif self.选中存档索引 > self.删除确认目标索引:
                                    self.选中存档索引 -= 1
                                # 重置删除确认状态
                                self.删除确认状态 = 0
                                self.删除确认目标索引 = None
                                # 更新滚动条
                                self.更新滚动条()
                        return True
                # 如果正在更改名称状态，处理点击事件
                elif self.更改名称状态 == 1:
                    # 输入框背景尺寸
                    输入框_width = 400
                    输入框_height = 150
                    输入框_x = (self.宽度 - 输入框_width) // 2
                    输入框_y = (self.高度 - 输入框_height) // 2
                    
                    # 输入框内框尺寸
                    输入框内_x = 输入框_x + 50
                    输入框内_y = 输入框_y + 60
                    输入框内_width = 输入框_width - 100
                    输入框内_height = 40
                    
                    # 检查是否点击了输入框内
                    输入框内_rect = pygame.Rect(输入框内_x, 输入框内_y, 输入框内_width, 输入框内_height)
                    if 输入框内_rect.collidepoint(鼠标位置):
                        # 获得焦点
                        self.输入框焦点 = True
                    else:
                        # 失去焦点
                        self.输入框焦点 = False
                    return True
                
                # 检查是否点击了滚动条
                if self.滚动条_height > 0:
                    滚动滑块_rect = pygame.Rect(
                        self.可滚动区域.right - self.滚动条_width - 5,
                        self.滚动条_pos,
                        self.滚动条_width,
                        self.滚动条_height
                    )
                    if 滚动滑块_rect.collidepoint(鼠标位置):
                        self.滚动条_dragging = True
                        self.拖动起始位置 = 鼠标位置[1] - self.滚动条_pos
                        return True
                
                # 检查是否点击了存档项
                累积_y = 0
                for i, 存档 in enumerate(self.存档列表):
                    # 确定当前存档项的高度
                    current_height = self.选中存档_height if i == self.选中存档索引 else self.存档_height
                    
                    # 计算当前存档项的y位置
                    存档_y = self.可滚动区域.y + 累积_y - self.滚动偏移量
                    
                    # 创建存档项矩形
                    存档_rect = pygame.Rect(
                        self.可滚动区域.x,
                        存档_y,
                        self.可滚动区域.width - self.滚动条_width - 10,
                        current_height
                    )
                    
                    # 检查是否点击了当前存档项
                    if 存档_rect.collidepoint(鼠标位置):
                        # 播放点击音效
                        from 音频输出 import audio_manager
                        audio_manager.play_click_sound()
                        
                        # 如果是选中状态，检查是否点击了功能按钮
                        if self.选中存档索引 == i:
                            # 计算功能按钮的位置
                            按钮_width = 90
                            按钮_height = 30
                            按钮_start_x = 存档_rect.x + 20
                            按钮_y = 存档_rect.y + 123
                            按钮_spacing = 10
                            
                            # 进入存档按钮
                            进入存档按钮 = pygame.Rect(按钮_start_x, 按钮_y, 按钮_width, 按钮_height)
                            # 删除存档按钮
                            删除存档按钮 = pygame.Rect(按钮_start_x + 按钮_width + 按钮_spacing, 按钮_y, 按钮_width, 按钮_height)
                            # 更改存档名称按钮
                            更改存档名称按钮 = pygame.Rect(按钮_start_x + (按钮_width + 按钮_spacing) * 2, 按钮_y, 按钮_width, 按钮_height)
                            # 更改存档图片按钮
                            更改存档图片按钮 = pygame.Rect(按钮_start_x + (按钮_width + 按钮_spacing) * 3, 按钮_y, 按钮_width, 按钮_height)
                            
                            # 检查是否点击了进入存档按钮
                            if 进入存档按钮.collidepoint(鼠标位置):
                                print(f"进入存档: {存档['名称']}")
                                # 这里可以添加进入存档的逻辑
                                return False  # 返回游戏界面
                            
                            # 检查是否点击了删除存档按钮
                            elif 删除存档按钮.collidepoint(鼠标位置):
                                # 如果还没有开始确认流程，或者确认的是其他存档
                                if self.删除确认状态 == 0 or self.删除确认目标索引 != i:
                                    # 开始第一次确认
                                    self.删除确认状态 = 1
                                    self.删除确认目标索引 = i
                                    self.删除确认位置 = 删除存档按钮.center
                                elif self.删除确认状态 < 3:
                                    # 继续确认流程
                                    self.删除确认状态 += 1
                                else:
                                    # 第三次确认，执行删除
                                    print(f"删除存档: {存档['名称']}")
                                    # 这里可以添加删除存档的逻辑
                                    self.存档列表.pop(i)
                                    self.选中存档索引 = None
                                    self.删除确认状态 = 0
                                    self.删除确认目标索引 = None
                                    self.更新滚动条()
                                return True
                            
                            # 检查是否点击了更改存档名称按钮
                            elif 更改存档名称按钮.collidepoint(鼠标位置):
                                print(f"开始更改存档名称: {存档['名称']}")
                                # 开始更改存档名称
                                self.更改名称状态 = 1
                                self.更改名称目标索引 = i
                                self.新存档名称 = 存档['名称']  # 初始化为当前名称
                                self.输入框焦点 = True  # 自动获得焦点
                                return True
                            
                            # 检查是否点击了更改存档图片按钮
                            elif 更改存档图片按钮.collidepoint(鼠标位置):
                                print(f"开始更改存档图片: {存档['名称']}")
                                # 使用tkinter打开系统图片选择器
                                try:
                                    import tkinter as tk
                                    from tkinter import filedialog
                                    # 隐藏tk窗口
                                    root = tk.Tk()
                                    root.withdraw()
                                    # 打开文件选择对话框，允许选择图片文件，从上次选择的路径开始
                                    文件路径 = filedialog.askopenfilename(
                                        title="选择存档图片",
                                        initialdir=self.上次选择路径,
                                        filetypes=[("图片文件", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
                                    )
                                    if 文件路径:
                                        # 保存上次选择的路径
                                        self.上次选择路径 = os.path.dirname(文件路径)
                                        # 加载并处理图片
                                        try:
                                            新图片 = pygame.image.load(文件路径).convert_alpha()
                                            # 调整图片大小为160x120（4:3比例）
                                            新图片 = pygame.transform.scale(新图片, (160, 120))
                                            # 这里可以添加图片底处理逻辑
                                            # 创建带底的图片
                                            带底图片 = pygame.Surface((160, 120), pygame.SRCALPHA)
                                            # 填充背景色
                                            带底图片.fill(self.图片底_color)
                                            # 绘制图片
                                            带底图片.blit(新图片, (0, 0))
                                            # 更新存档图片
                                            # 这里可以根据需要保存图片到文件系统
                                            # 目前只是在内存中更新，实际项目中需要保存到文件
                                            print(f"存档图片已更改为: {文件路径}")
                                        except Exception as e:
                                            print(f"加载图片失败: {str(e)}")
                                except ImportError:
                                    print("tkinter未安装，无法打开文件选择器")
                                return True
                            
                            # 如果没有点击任何功能按钮，则取消选中
                            else:
                                self.选中存档索引 = None  # 取消选中
                        else:
                            self.选中存档索引 = i  # 选中当前存档项
                        
                        # 初始化变量，确保在所有情况下都能正常访问
                        选中存档_y = 0
                        选中存档_height = self.存档_height  # 默认高度
                        
                        # 更新滚动条，因为存档列表总高度可能发生变化
                        self.更新滚动条()
                        
                        # 只有在有选中存档项的情况下，才调整滚动偏移量
                        if self.选中存档索引 is not None:
                            # 重新计算选中存档项的位置和高度
                            调整后_累积_y = 0
                            # 使用不同的变量名，避免与外部循环冲突
                            找到选中项 = False
                            for j in range(len(self.存档列表)):
                                内部_current_height = self.选中存档_height if j == self.选中存档索引 else self.存档_height
                                if j == self.选中存档索引:
                                    选中存档_y = self.可滚动区域.y + 调整后_累积_y - self.滚动偏移量
                                    选中存档_height = 内部_current_height
                                    找到选中项 = True
                                    break
                                调整后_累积_y += 内部_current_height + self.存档间距
                            
                            # 只有在找到选中项的情况下，才进行滚动调整
                            if 找到选中项:
                                # 检查选中存档项是否超出可滚动区域底部
                                选中存档_bottom = 选中存档_y + 选中存档_height
                                可滚动区域_bottom = self.可滚动区域.y + self.可滚动区域.height
                                
                                if 选中存档_bottom > 可滚动区域_bottom:
                                    # 计算需要向上滚动的距离
                                    需要滚动距离 = 选中存档_bottom - 可滚动区域_bottom
                                    # 调整滚动偏移量
                                    self.滚动偏移量 += 需要滚动距离
                                    # 更新滚动条位置
                                    self.更新滚动条()
                                
                                # 检查选中存档项是否超出可滚动区域顶部
                                可滚动区域_top = self.可滚动区域.y
                                
                                if 选中存档_y < 可滚动区域_top:
                                    # 计算需要向下滚动的距离
                                    需要滚动距离 = 可滚动区域_top - 选中存档_y
                                    # 调整滚动偏移量
                                    self.滚动偏移量 = max(0, self.滚动偏移量 - 需要滚动距离)
                                    # 更新滚动条位置
                                    self.更新滚动条()
                        
                        return True
                    
                    # 累积y坐标
                    累积_y += current_height + self.存档间距
                
                # 检查返回按钮
                if self.返回按钮_悬停:
                    self.返回按钮_按下 = True
                # 检查创建新世界按钮
                if self.创建新世界按钮_悬停:
                    self.创建新世界按钮_按下 = True
            
            # 鼠标滚轮滚动（按钮4：向上，按钮5：向下）
            elif 事件.button == 4 or 事件.button == 5:
                if self.鼠标_hover_可滚动区域 or self.滚动条_hover:
                    # 计算滚动步长
                    滚动步长 = 50
                    
                    # 计算存档列表的总高度，考虑选中状态下的存档项高度
                    存档总高度 = 0
                    for i in range(len(self.存档列表)):
                        current_height = self.选中存档_height if i == self.选中存档索引 else self.存档_height
                        存档总高度 += current_height + self.存档间距
                    # 减去最后一个存档项的间距
                    if self.存档列表:
                        存档总高度 -= self.存档间距
                    
                    # 计算最大滚动偏移量
                    最大滚动偏移量 = max(0, 存档总高度 - self.可滚动区域.height)
                    
                    # 更新滚动偏移量
                    if 事件.button == 4:  # 向上滚动
                        self.滚动偏移量 = max(0, self.滚动偏移量 - 滚动步长)
                    elif 事件.button == 5:  # 向下滚动
                        self.滚动偏移量 = min(最大滚动偏移量, self.滚动偏移量 + 滚动步长)
                    
                    # 更新滚动条位置
                    self.更新滚动条()
        
        elif 事件.type == pygame.MOUSEBUTTONUP:
            if 事件.button == 1:  # 左键释放
                # 停止拖动滚动条
                self.滚动条_dragging = False
                
                if self.返回按钮_按下 and self.返回按钮_悬停:
                    # 播放点击音效
                    from 音频输出 import audio_manager
                    audio_manager.play_click_sound()
                    return False  # 返回开始界面
                
                if self.创建新世界按钮_按下 and self.创建新世界按钮_悬停:
                    # 播放点击音效
                    from 音频输出 import audio_manager
                    audio_manager.play_click_sound()
                    # 这里可以添加创建新世界的逻辑
                    return False  # 返回开始界面
                
                # 重置按钮状态
                self.返回按钮_按下 = False
                self.创建新世界按钮_按下 = False
        
        # 处理鼠标拖动滚动条
        elif 事件.type == pygame.MOUSEMOTION:
            if self.滚动条_dragging:
                # 计算新的滚动条位置
                新位置 = 鼠标位置[1] - self.拖动起始位置
                
                # 限制滚动条在轨道内
                新位置 = max(self.可滚动区域.y, 新位置)
                新位置 = min(self.可滚动区域.y + self.可滚动区域.height - self.滚动条_height, 新位置)
                
                # 更新滚动条位置
                self.滚动条_pos = 新位置
                
                # 计算滚动偏移量
                轨道高度 = self.可滚动区域.height - self.滚动条_height
                相对位置 = self.滚动条_pos - self.可滚动区域.y
                滚动比例 = 相对位置 / 轨道高度
                
                # 计算存档列表的总高度
                存档总高度 = len(self.存档列表) * (self.存档_height + self.存档间距)
                
                # 计算最大滚动偏移量
                最大滚动偏移量 = max(0, 存档总高度 - self.可滚动区域.height)
                
                # 更新滚动偏移量
                self.滚动偏移量 = 滚动比例 * 最大滚动偏移量
        
        elif 事件.type == pygame.KEYDOWN:
            if 事件.key == pygame.K_ESCAPE:
                # 如果正在更改名称状态，取消更改
                if self.更改名称状态 == 1:
                    self.更改名称状态 = 0
                    self.更改名称目标索引 = None
                    self.新存档名称 = ""
                    self.输入框焦点 = False
                    return True
                return False  # 返回开始界面
            
            # 处理更改名称状态下的键盘事件
            if self.更改名称状态 == 1 and self.输入框焦点:
                if 事件.key == pygame.K_RETURN:
                    # 确认更改存档名称
                    if 0 <= self.更改名称目标索引 < len(self.存档列表):
                        if self.新存档名称.strip() != "":
                            旧名称 = self.存档列表[self.更改名称目标索引]['名称']
                            self.存档列表[self.更改名称目标索引]['名称'] = self.新存档名称.strip()
                            print(f"存档名称已从 '{旧名称}' 更改为 '{self.新存档名称.strip()}'")
                    # 重置状态
                    self.更改名称状态 = 0
                    self.更改名称目标索引 = None
                    self.新存档名称 = ""
                    self.输入框焦点 = False
                    return True
                elif 事件.key == pygame.K_BACKSPACE:
                    # 删除最后一个字符
                    self.新存档名称 = self.新存档名称[:-1]
                    return True
                elif 事件.key == pygame.K_TAB:
                    # 忽略Tab键
                    return True
                elif 事件.unicode.isprintable():
                    # 只允许可打印字符
                    self.新存档名称 += 事件.unicode
                    return True
        
        return True  # 继续显示当前界面
    
    def 更新滚动条(self):
        """更新滚动条的高度和位置"""
        # 计算存档列表的总高度，考虑选中状态下的存档项高度
        存档总高度 = 0
        for i in range(len(self.存档列表)):
            current_height = self.选中存档_height if i == self.选中存档索引 else self.存档_height
            存档总高度 += current_height + self.存档间距
        # 减去最后一个存档项的间距
        if self.存档列表:
            存档总高度 -= self.存档间距
        
        # 计算可滚动区域的高度
        可滚动区域高度 = self.可滚动区域.height
        
        # 只有当存档总高度超过可滚动区域高度时才显示滚动条
        if 存档总高度 <= 可滚动区域高度:
            self.滚动条_height = 0  # 不显示滚动条
            # 确保滚动偏移量为0，防止内容显示异常
            self.滚动偏移量 = 0
            return
        
        # 计算滚动条高度（根据内容比例）
        self.滚动条_height = max(20, (可滚动区域高度 / 存档总高度) * 可滚动区域高度)
        
        # 计算最大滚动偏移量
        最大滚动偏移量 = max(0, 存档总高度 - 可滚动区域高度)
        
        # 确保滚动偏移量在有效范围内
        self.滚动偏移量 = max(0, min(self.滚动偏移量, 最大滚动偏移量))
        
        # 计算滚动条的位置
        滚动比例 = self.滚动偏移量 / 最大滚动偏移量 if 最大滚动偏移量 > 0 else 0
        self.滚动条_pos = self.可滚动区域.y + 滚动比例 * (可滚动区域高度 - self.滚动条_height)
    
    def update_size(self, 宽度, 高度):
        """更新界面尺寸"""
        self.宽度 = 宽度
        self.高度 = 高度
        
        # 调整背景图片大小
        if self.背景图片:
            try:
                self.背景图片 = pygame.transform.scale(self.背景图片, (self.宽度, self.高度))
            except Exception as e:
                print(f"无法调整背景图片大小: {e}")
        
        # 更新中心底的位置和尺寸
        self.中心底_width = self.宽度 * 0.8
        self.中心底_height = self.高度 * 0.7 + 100  # 增加100像素高度
        # 向上移动50像素
        self.中心底 = pygame.Rect(
            (self.宽度 - self.中心底_width) // 2,
            (self.高度 - self.中心底_height) // 2 - 50,
            self.中心底_width,
            self.中心底_height
        )
        
        # 更新可滚动区域，调整高度以一次显示6个存档项，向下移动50像素
        self.可滚动区域 = pygame.Rect(
            self.中心底.x + 20,
            self.中心底.y + 150,
            self.中心底_width - 40,
            6 * self.存档_height + 5 * self.存档间距  # 6个存档项的总高度
        )
        
        # 更新按钮位置，两个按钮都下降20像素
        self.返回按钮 = pygame.Rect(
            (self.宽度 - self.按钮宽度 * 2 - self.按钮间距) // 2,
            self.高度 - self.按钮高度 - 30,
            self.按钮宽度,
            self.按钮高度
        )
        
        self.创建新世界按钮 = pygame.Rect(
            (self.宽度 + self.按钮间距) // 2,
            self.高度 - self.按钮高度 - 30,
            self.按钮宽度,
            self.按钮高度
        )
        
        # 更新滚动条
        self.更新滚动条()