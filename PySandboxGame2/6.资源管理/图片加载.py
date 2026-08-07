import pygame
import os
import sys
import zipfile
import random
import string

# 添加物品定义模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class 图片加载器:
    """图片加载器类，负责加载和管理游戏中的所有图片资源"""
    
    # 单例模式实现
    _instance = None
    
    def __new__(cls):
        """确保只有一个图片加载器实例"""
        if cls._instance is None:
            cls._instance = super(图片加载器, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """初始化图片加载器"""
        # 防止重复初始化
        if hasattr(self, '_initialized') and self._initialized:
            return
            
        self.图片字典 = {}
        # 存储已提示过的不存在图片，避免重复提示
        self.不存在图片记录 = set()
        # 获取当前脚本所在目录（相对路径）
        # 兼容EXE打包的路径获取
        if getattr(sys, 'frozen', False):
            # 打包为EXE后的路径，PyInstaller会将资源解压到_MEIPASS目录
            script_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        else:
            # 正常脚本运行时的路径：获取项目根目录（向上两级，因为图片加载.py在6.资源管理文件夹中）
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 设置图片目录为脚本目录下的"资源/图片"文件夹（相对路径）
        self.图片目录 = os.path.join(script_dir, "资源", "图片")
        # 支持的图片扩展名
        self.图片扩展名 = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        # 是否已加载所有图片的标志
        self._all_images_loaded = False
        # 标记初始化完成
        self._initialized = True
        
        print("图片加载器初始化完成")
    
    def 加载所有图片(self, 加载窗口=None):
        """加载所有图片资源
        
        参数:
            加载窗口: 可选，加载窗口实例，用于显示加载进度和具体文件名
        """
        # 检查是否已经加载过所有图片，如果是则直接返回
        if self._all_images_loaded and len(self.图片字典) > 0:
            print("图片资源已加载，无需重复加载")
            return True
            
        try:
            print("开始扫描并加载所有图片文件...")
            
            # 先获取所有图片文件列表以计算总数（用于实际加载）
            实际图片总数 = self._计算图片总数(self.图片目录)
            
            # 重置计数器用于进度计算
            self._已加载图片数 = 0
            # 使用实际计算的图片总数
            self._总图片数 = 实际图片总数
            
            # 自动扫描并加载所有图片文件（包括子目录）
            self.自动扫描加载图片(self.图片目录, 加载窗口=加载窗口)
            
            print(f"成功加载 {len(self.图片字典)} 张图片")
            # 标记已加载所有图片
            self._all_images_loaded = True
            return True
            
        except Exception as e:
            print(f"图片加载失败: {str(e)}")
            return False
    
    def _计算图片总数(self, 目录路径):
        """计算目录中图片文件的总数
        
        参数:
            目录路径: 要扫描的目录路径
        
        返回:
            int: 图片文件总数
        """
        if not os.path.exists(目录路径):
            return 0
        
        总数 = 0
        for 文件名 in os.listdir(目录路径):
            文件路径 = os.path.join(目录路径, 文件名)
            
            if os.path.isdir(文件路径):
                # 递归计算子目录中的图片数量
                总数 += self._计算图片总数(文件路径)
            else:
                # 检查是否为图片文件
                扩展名 = os.path.splitext(文件名)[1].lower()
                if 扩展名 in self.图片扩展名:
                    总数 += 1
        
        # 保存总数
        self._总图片数 = 总数
        return 总数
    
    def 自动扫描加载图片(self, 目录路径, 父路径="", 加载窗口=None):
        """自动扫描并加载目录中的所有图片文件
        
        参数:
            目录路径: 要扫描的目录路径
            父路径: 用于构建带有子目录前缀的图片名称
            加载窗口: 可选，加载窗口实例，用于显示加载进度和具体文件名
        """
        if not os.path.exists(目录路径):
            print(f"警告: 目录不存在 - {目录路径}")
            return
        
        for 文件名 in os.listdir(目录路径):
            文件路径 = os.path.join(目录路径, 文件名)
            
            if os.path.isdir(文件路径):
                # 如果是子目录，递归扫描
                子目录名 = os.path.basename(文件路径)
                新父路径 = f"{父路径}{子目录名}_" if 父路径 else f"{子目录名}_"
                self.自动扫描加载图片(文件路径, 新父路径, 加载窗口)
            else:
                # 检查是否为图片文件
                扩展名 = os.path.splitext(文件名)[1].lower()
                if 扩展名 in self.图片扩展名:
                    # 构建图片名称（去掉扩展名）
                    基础图片名 = os.path.splitext(文件名)[0]
                    
                    # 创建带前缀的图片名（用于唯一标识）
                    if 父路径:
                        图片名 = f"{父路径}{基础图片名}"
                    else:
                        图片名 = 基础图片名
                    
                    # 加载带前缀的图片
                    self.加载图片(图片名, 文件路径, 加载窗口=加载窗口)
                    
                    # 不再同时加载不带前缀的图片，避免重复加载
                    # 只保留带前缀的图片名，确保图片唯一
    
    # 注意：由于使用了自动扫描加载图片功能，以下方法已被替换
    # 保留方法签名以确保兼容性，但它们不再执行任何操作
    def 加载方块图片(self):
        """加载方块相关图片（已由自动扫描功能替代）"""
        print("提示: 方块图片加载已由自动扫描功能替代")
    
    def 加载物品图片(self):
        """加载物品相关图片（已由自动扫描功能替代）"""
        print("提示: 物品图片加载已由自动扫描功能替代")
    
    def 加载角色图片(self):
        """加载角色相关图片（已由自动扫描功能替代）"""
        print("提示: 角色图片加载已由自动扫描功能替代")
    
    def 加载背景图片(self):
        """加载背景相关图片（已由自动扫描功能替代）"""
        print("提示: 背景图片加载已由自动扫描功能替代")
    
    def 加载图片(self, 图片名, 图片路径, 加载窗口=None):
        """加载单张图片
        
        参数:
            图片名: 图片名称
            图片路径: 图片文件路径
            加载窗口: 可选，加载窗口实例，用于显示加载进度和具体文件名
        """
        try:
            if not os.path.exists(图片路径):
                # 只在图片不存在且之前未提示过时显示警告
                if 图片名 not in self.不存在图片记录:
                    self.不存在图片记录.add(图片名)
                    print(f"警告: 图片文件不存在 - {图片路径}")
                return False
            
            # 检查是否设置了视频模式
            if pygame.display.get_init():
                图片 = pygame.image.load(图片路径)
                # 转换为更高效的格式
                if 图片.get_alpha() is None:
                    图片 = 图片.convert()
                else:
                    图片 = 图片.convert_alpha()
                # 检查图片是否已存在，避免重复计数
                if 图片名 not in self.图片字典:
                    self.图片字典[图片名] = 图片
                    
                    # 只有新图片才更新计数器
                    self._已加载图片数 += 1
                
                # 获取文件名（带扩展名）
                文件名 = os.path.basename(图片路径)
                print(f"加载图片: {文件名} - 成功")
                
                # 更新加载窗口
                if 加载窗口 and hasattr(self, '_总图片数') and self._总图片数 > 0:
                    # 计算相对进度（0-100%）
                    相对进度 = (self._已加载图片数 / self._总图片数) * 100
                    # 映射到主程序中分配的图片加载进度范围（20-100%）
                    进度 = 20 + int((相对进度 / 100) * 80)
                    # 限制进度在20-100之间
                    进度 = max(20, min(100, 进度))
                    # 确保格式为：正在加载图片:??.png
                    加载窗口.update_progress(进度, f"正在加载图片:{文件名}")
                
                return True
            else:
                # 未设置视频模式时不显示过多警告
                if 图片名 not in self.不存在图片记录:
                    self.不存在图片记录.add(图片名)
                    print(f"跳过加载 {图片名}: 未设置视频模式")
                return False
        except Exception as e:
            # 错误只提示一次
            if 图片名 not in self.不存在图片记录:
                self.不存在图片记录.add(图片名)
                print(f"加载图片失败 {图片名}: {str(e)}")
            return False
    
    def 获取图片(self, 图片名):
        """获取已加载的图片
        
        参数:
            图片名: 要获取的图片名称
            
        返回:
            pygame.Surface: 图片表面，如果未找到则返回None
        """
        # 1. 首先尝试直接匹配
        图片 = self.图片字典.get(图片名)
        if 图片:
            return 图片
        
        # 2. 如果直接匹配失败，尝试搜索所有图片名中包含该图片名的图片
        for 字典中的图片名 in self.图片字典:
            if 字典中的图片名.endswith(f"_{图片名}") or 字典中的图片名 == 图片名:
                return self.图片字典[字典中的图片名]
        
        return None
    
    def 图片是否已加载(self, 图片名):
        """检查图片是否已加载
        
        参数:
            图片名: 要检查的图片名称
            
        返回:
            bool: 如果图片已加载则返回True，否则返回False
        """
        # 1. 首先检查直接匹配
        if 图片名 in self.图片字典:
            return True
        
        # 2. 如果直接匹配失败，尝试搜索所有图片名中包含该图片名的图片
        for 字典中的图片名 in self.图片字典:
            if 字典中的图片名.endswith(f"_{图片名}") or 字典中的图片名 == 图片名:
                return True
        
        return False
    
    def 缩放图片(self, 图片名, 新宽度, 新高度):
        """缩放指定图片"""
        if 图片名 in self.图片字典:
            try:
                原始图片 = self.图片字典[图片名]
                缩放后的图片 = pygame.transform.scale(原始图片, (新宽度, 新高度))
                return 缩放后的图片
            except Exception as e:
                print(f"缩放图片失败 {图片名}: {str(e)}")
                return None
        return None
    
    def 获取物品图片(self, 物品ID, 尺寸=None):
        """获取物品图片，作为游戏中唯一的图片获取接口
        
        参数:
            物品ID: 物品的唯一标识符（可以是数值ID或字符串名称）
            尺寸: 可选，图片的目标尺寸
            
        返回:
            pygame.Surface: 物品图片表面，如果未找到则返回None
        """
        # 1. 如果物品ID是字符串，直接作为纹理名称尝试获取
        if isinstance(物品ID, str):
            纹理名称 = 物品ID
            
            # 尝试多种方式查找图片
            # 1. 首先尝试直接使用纹理名称
            图片 = self.获取图片(纹理名称)
            
            # 2. 如果失败，尝试搜索所有图片名中包含纹理名称的图片
            if not 图片:
                for 图片名 in self.图片字典:
                    # 检查图片名是否以纹理名称结尾（去掉前缀）
                    if 图片名.endswith(f"_{纹理名称}") or 图片名 == 纹理名称:
                        图片 = self.获取图片(图片名)
                        break
            
            # 3. 如果找到纹理图片
            if 图片:
                # 根据需要缩放图片
                if 尺寸:
                    # 为了正确缩放，我们需要知道原始图片名
                    # 查找原始图片名
                    原始图片名 = 纹理名称
                    for 图片名 in self.图片字典:
                        if 图片名.endswith(f"_{纹理名称}") or 图片名 == 纹理名称:
                            原始图片名 = 图片名
                            break
                    return self.缩放图片(原始图片名, 尺寸[0], 尺寸[1])
                return 图片
            
            # 4. 如果纹理图片未加载，尝试直接从文件加载
            图片路径 = os.path.join(self.图片目录, f"{纹理名称}.png")
            if self.加载图片(纹理名称, 图片路径):
                图片 = self.获取图片(纹理名称)
                if 尺寸 and 图片:
                    return self.缩放图片(纹理名称, 尺寸[0], 尺寸[1])
                return 图片
            
            # 记录错误但不抛出异常
            if 物品ID not in self.不存在图片记录:
                self.不存在图片记录.add(物品ID)
                print(f"警告: 未能加载掉落物图片 (ID: {物品ID}), 使用默认色块")
            return None
        
        # 2. 物品ID是数值ID，正常处理流程
        # 首先尝试直接将物品ID作为图片名获取
        图片 = self.获取图片(物品ID)
        if 图片:
            if 尺寸:
                return self.缩放图片(物品ID, 尺寸[0], 尺寸[1])
            return 图片
        
        # 如果直接获取失败，尝试从物品定义获取纹理信息
        try:
            # 从物品定义获取物品信息
            from 物品定义 import 物品, 方块属性
            
            # 尝试获取物品信息
            物品信息 = None
            if 物品ID in 物品:
                物品信息 = 物品[物品ID]
            elif 物品ID in 方块属性:
                物品信息 = 方块属性[物品ID]
            
            # 如果找到物品信息，尝试获取纹理名称
            if 物品信息 and "纹理" in 物品信息:
                纹理名称 = 物品信息["纹理"]
                
                # 尝试多种方式查找图片
                # 1. 首先尝试直接使用纹理名称
                图片 = self.获取图片(纹理名称)
                
                # 2. 如果失败，尝试搜索所有图片名中包含纹理名称的图片
                if not 图片:
                    for 图片名 in self.图片字典:
                        # 检查图片名是否以纹理名称结尾（去掉前缀）
                        if 图片名.endswith(f"_{纹理名称}") or 图片名 == 纹理名称:
                            图片 = self.获取图片(图片名)
                            break
                
                # 3. 如果找到纹理图片
                if 图片:
                    # 根据需要缩放图片
                    if 尺寸:
                        # 为了正确缩放，我们需要知道原始图片名
                        # 查找原始图片名
                        原始图片名 = 纹理名称
                        for 图片名 in self.图片字典:
                            if 图片名.endswith(f"_{纹理名称}") or 图片名 == 纹理名称:
                                原始图片名 = 图片名
                                break
                        return self.缩放图片(原始图片名, 尺寸[0], 尺寸[1])
                    return 图片
                
                # 4. 如果纹理图片未加载，尝试直接从文件加载
                图片路径 = os.path.join(self.图片目录, f"{纹理名称}.png")
                if self.加载图片(纹理名称, 图片路径):
                    图片 = self.获取图片(纹理名称)
                    if 尺寸 and 图片:
                        return self.缩放图片(纹理名称, 尺寸[0], 尺寸[1])
                    return 图片
        except Exception as e:
            # 只在首次失败时显示错误信息
            if str(物品ID) not in self.不存在图片记录:
                self.不存在图片记录.add(str(物品ID))
                print(f"获取物品ID {物品ID} 图片时出错: {e}")
        
        # 如果所有尝试都失败，返回None
        return None
    
    def 清除所有图片(self):
        """清除所有已加载的图片"""
        self.图片字典.clear()
        print("已清除所有图片资源")

# 全局图片加载器实例
图片管理器 = 图片加载器()
# 初始化计数器属性
图片管理器._已加载图片数 = 0
图片管理器._总图片数 = 0

# 测试代码
if __name__ == "__main__":
    pygame.init()
    # 创建一个临时的显示窗口用于测试
    pygame.display.set_mode((1, 1))
    print("开始测试图片加载...")
    图片管理器.加载所有图片()
    pygame.quit()