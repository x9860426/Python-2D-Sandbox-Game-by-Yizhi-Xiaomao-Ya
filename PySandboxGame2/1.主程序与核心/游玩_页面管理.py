import pygame
import importlib.util
import os

class PageManager:
    """页面管理器，统一管理游戏中所有页面的打开、关闭和切换"""
    
    def __init__(self, game):
        self.game = game
        self.屏幕 = game.屏幕
        
        # 页面状态字典，记录每个页面的打开状态
        self.page_states = {
            'f1': False,  # 帮助页面
            'f2': False,  # 属性提升页面
            'f3': False,  # 创造背包页面
            'f4': False,  # 开发者调试页面
            'c': False,   # 合成页面
            'v': False,   # 熔炉页面
            'esc': False,  # ESC菜单页面
            'chest': False  # 箱子页面
        }
        
        # 页面实例字典
        self.pages = {
            'f1': None,
            'f2': None,
            'f3': None,
            'f4': None,
            'c': None,
            'v': None,
            'esc': None,
            'chest': None
        }
        
        # 初始化所有页面
        self._initialize_pages()
    
    def _initialize_pages(self):
        """初始化所有页面实例"""
        # 动态导入并初始化各个页面
        
        # F1帮助页面
        self.pages['f1'] = None  # f1页面是静态内容，不需要实例化
        
        # F2属性提升页面
        try:
            from 属性提升 import 属性提升页面
            self.pages['f2'] = 属性提升页面(self.game)
        except ImportError as e:
            print(f"导入属性提升页面失败: {e}")
        
        # F3创造背包页面
        try:
            from 创造背包 import CreativeBackpack
            self.pages['f3'] = CreativeBackpack(self.game)
        except ImportError as e:
            print(f"导入创造背包页面失败: {e}")
        
        # F4开发者调试页面
        try:
            from 开发者调试 import DeveloperDebugPanel
            self.pages['f4'] = DeveloperDebugPanel(self.game)
        except ImportError as e:
            print(f"导入开发者调试页面失败: {e}")
        
        # C合成页面
        try:
            from 合成页面 import CraftingPage
            self.pages['c'] = CraftingPage(self.game)
        except ImportError as e:
            print(f"导入合成页面失败: {e}")
        
        # V熔炉页面
        try:
            from 熔炉 import FurnaceManager
            from 物品定义 import 物品 as 物品定义
            self.pages['v'] = FurnaceManager(self.game, 物品定义)
        except ImportError as e:
            print(f"导入熔炉页面失败: {e}")
        
        # 箱子页面
        try:
            from 箱子 import 箱子管理器
            self.pages['chest'] = 箱子管理器(self.game, {})
        except ImportError as e:
            print(f"导入箱子页面失败: {e}")
        

    
    def handle_key_event(self, event):
        """处理键盘事件，管理页面的打开和关闭"""
        if event.type != pygame.KEYDOWN:
            return False
        
        key = event.key
        handled = False
        
        # 检查是否有页面处于打开状态
        any_page_open = any(self.page_states.values())
        
        # ESC键处理：如果没有页面打开，打开ESC菜单；否则关闭当前所有页面
        if key == pygame.K_ESCAPE:
            if not any_page_open:
                # 没有页面打开，打开ESC菜单
                self._open_page('esc')
            else:
                # 有页面打开，关闭所有页面
                self._close_all_pages()
            handled = True
        
        # F1帮助页面
        elif key == pygame.K_F1:
            self._toggle_page('f1')
            handled = True
        
        # F2属性提升页面
        elif key == pygame.K_F2:
            self._toggle_page('f2')
            handled = True
        
        # F3创造背包页面
        elif key == pygame.K_F3:
            self._toggle_page('f3')
            handled = True
        
        # F4开发者调试页面
        elif key == pygame.K_F4:
            self._toggle_page('f4')
            handled = True
        
        # C合成页面
        elif key == pygame.K_c:
            self._toggle_page('c')
            handled = True
        

        
        return handled
    
    def _toggle_page(self, page_key):
        """切换指定页面的状态 - 只在页面未打开时打开，关闭只能通过ESC键或关闭按钮"""
        # 关闭其他所有页面
        for key in self.page_states:
            if key != page_key:
                self._close_page(key)
        
        # 只在页面未打开时打开，不允许通过快捷键关闭
        if not self.page_states[page_key]:
            self._open_page(page_key)
    
    def _open_page(self, page_key, *args, **kwargs):
        """打开指定页面，支持传递额外参数给页面的打开方法"""
        self.page_states[page_key] = True
        
        # 特殊处理F1帮助页面
        if page_key == 'f1':
            self.game.show_controls = True
            self.game.help_scroll_offset = 0  # 重置滚动位置
        else:
            # 调用页面的打开方法
            page = self.pages[page_key]
            if page:
                if hasattr(page, 'toggle'):
                    page.toggle()
                elif hasattr(page, 'open'):
                    page.open()
                elif hasattr(page, 'open_page'):
                    # 传递额外参数给open_page方法
                    page.open_page(*args, **kwargs)
    
    def _close_page(self, page_key):
        """关闭指定页面"""
        self.page_states[page_key] = False
        
        # 特殊处理F1帮助页面
        if page_key == 'f1':
            self.game.show_controls = False
        else:
            # 调用页面的关闭方法，优先使用close或close_page，避免使用toggle
            page = self.pages[page_key]
            if page:
                if hasattr(page, 'close'):
                    page.close()
                elif hasattr(page, 'close_page'):
                    page.close_page()
                elif hasattr(page, 'toggle'):
                    # 只有在没有close方法时才使用toggle，确保关闭页面
                    if page.is_open:
                        page.toggle()
    
    def _close_all_pages(self):
        """关闭所有页面"""
        for key in self.page_states:
            self._close_page(key)
    
    def draw(self):
        """绘制所有打开的页面"""
        for page_key, is_open in self.page_states.items():
            if is_open:
                # 特殊处理F1帮助页面
                if page_key == 'f1':
                    # F1页面由游戏主类绘制，这里不需要额外处理
                    pass
                else:
                    page = self.pages[page_key]
                    if page:
                        if hasattr(page, '绘制'):
                            page.绘制(self.屏幕)
                        elif hasattr(page, 'draw'):
                            page.draw(self.屏幕)
    
    def update(self, delta_time):
        """更新所有页面的状态"""
        for page_key, is_open in self.page_states.items():
            if is_open:
                page = self.pages[page_key]
                if page and hasattr(page, 'update'):
                    try:
                        # 尝试传递delta_time参数
                        page.update(delta_time)
                    except TypeError:
                        # 如果方法不接受delta_time参数，只传递self
                        try:
                            page.update()
                        except Exception as e:
                            print(f"更新页面 {page_key} 时出错: {e}")
    
    def handle_mouse_event(self, event):
        """处理鼠标事件，传递给当前打开的页面
        
        当有页面打开时，无论点击的是页面内还是页面外，都阻止事件继续传递到游戏世界
        """
        # 检查是否有任何页面处于打开状态
        any_page_open = any(self.page_states.values())
        
        # 如果有页面打开，先尝试让页面处理事件
        if any_page_open:
            for page_key, is_open in self.page_states.items():
                if is_open:
                    page = self.pages[page_key]
                    if page:
                        if hasattr(page, 'handle_event'):
                            if page.handle_event(event):
                                # 检查页面是否已经关闭
                                if hasattr(page, '是否打开') and not page.是否打开:
                                    self.page_states[page_key] = False
                                elif hasattr(page, 'is_open') and not page.is_open:
                                    self.page_states[page_key] = False
                        elif hasattr(page, '处理事件'):
                            if page.处理事件(event):
                                # 检查页面是否已经关闭
                                if hasattr(page, '是否打开') and not page.是否打开:
                                    self.page_states[page_key] = False
                                elif hasattr(page, 'is_open') and not page.is_open:
                                    self.page_states[page_key] = False
                        else:
                            # 根据事件类型调用相应的处理方法
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if hasattr(page, 'handle_mouse_click'):
                                    page.handle_mouse_click(event)
                                elif hasattr(page, '处理点击'):
                                    鼠标x, 鼠标y = event.pos
                                    page.处理点击(鼠标x, 鼠标y, event.button)
                                    # 检查页面是否已经关闭
                                    if hasattr(page, '是否打开') and not page.是否打开:
                                        self.page_states[page_key] = False
                                    elif hasattr(page, 'is_open') and not page.is_open:
                                        self.page_states[page_key] = False
                                elif hasattr(page, 'handle_click'):
                                    鼠标x, 鼠标y = event.pos
                                    page.handle_click(鼠标x, 鼠标y, event.button)
                                    # 检查页面是否已经关闭
                                    if hasattr(page, 'is_open') and not page.is_open:
                                        self.page_states[page_key] = False
                                elif hasattr(page, 'handle_mouse_down'):
                                    page.handle_mouse_down(event)
                            elif event.type == pygame.MOUSEBUTTONUP:
                                if hasattr(page, 'handle_mouse_up'):
                                    page.handle_mouse_up(event)
                            elif event.type == pygame.MOUSEMOTION:
                                if hasattr(page, 'handle_mouse_motion'):
                                    page.handle_mouse_motion(event)
                                elif hasattr(page, 'handle_mouse_drag'):
                                    page.handle_mouse_drag(event)
            # 当有页面打开时，无论页面是否处理了事件，都阻止事件继续传递到游戏世界
            return True
        
        return False
    
    def handle_keyboard_event(self, event):
        """处理键盘事件，传递给当前打开的页面
        
        当有页面打开时，无论键盘事件是否被页面处理，都阻止事件继续传递到游戏世界
        """
        # 检查是否有任何页面处于打开状态
        any_page_open = any(self.page_states.values())
        
        # 如果有页面打开，先尝试让页面处理事件
        if any_page_open:
            for page_key, is_open in self.page_states.items():
                if is_open:
                    page = self.pages[page_key]
                    if page:
                        if hasattr(page, 'handle_keyboard'):
                            if page.handle_keyboard(event):
                                # 检查页面是否已经关闭
                                if hasattr(page, '是否打开') and not page.是否打开:
                                    self.page_states[page_key] = False
                                elif hasattr(page, 'is_open') and not page.is_open:
                                    self.page_states[page_key] = False
                        elif hasattr(page, '处理键盘'):
                            if page.处理键盘(event):
                                # 检查页面是否已经关闭
                                if hasattr(page, '是否打开') and not page.是否打开:
                                    self.page_states[page_key] = False
                                elif hasattr(page, 'is_open') and not page.is_open:
                                    self.page_states[page_key] = False
                        elif hasattr(page, '处理事件'):
                            if page.处理事件(event):
                                # 检查页面是否已经关闭
                                if hasattr(page, '是否打开') and not page.是否打开:
                                    self.page_states[page_key] = False
                                elif hasattr(page, 'is_open') and not page.is_open:
                                    self.page_states[page_key] = False
            # 当有页面打开时，无论页面是否处理了事件，都阻止事件继续传递到游戏世界
            return True
        
        return False
    
    def is_any_page_open(self):
        """检查是否有任何页面处于打开状态"""
        return any(self.page_states.values())
    
    def get_open_page(self):
        """获取当前打开的页面键"""
        for page_key, is_open in self.page_states.items():
            if is_open:
                return page_key
        return None