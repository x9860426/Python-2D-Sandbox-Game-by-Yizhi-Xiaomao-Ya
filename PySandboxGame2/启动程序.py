import sys
import os

# 获取当前启动程序所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将所有中文文件夹添加到Python路径中
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "1.主程序与核心"))
sys.path.insert(0, os.path.join(current_dir, "2.生物与NPC"))
sys.path.insert(0, os.path.join(current_dir, "3.物品与背包"))
sys.path.insert(0, os.path.join(current_dir, "4.游戏界面"))
sys.path.insert(0, os.path.join(current_dir, "5.游戏系统"))
sys.path.insert(0, os.path.join(current_dir, "6.资源管理"))
sys.path.insert(0, os.path.join(current_dir, "存档"))

# 设置工作目录为启动程序所在目录
os.chdir(current_dir)

# 直接运行主程序文件
try:
    # 使用exec执行主程序
    # 首先检查是否是打包环境
    if hasattr(sys, '_MEIPASS'):
        # 打包环境
        # 在PyInstaller打包后，所有文件都会被放在_MEIPASS目录下
        # 我们需要确保主程序.py在打包时被正确添加
        # 这里我们直接导入主程序模块，因为它应该已经被打包进可执行文件
        import 主程序
    else:
        # 开发环境
        # 构建主程序文件路径
        main_program = os.path.join(current_dir, "1.主程序与核心", "主程序.py")
        
        # 使用exec执行主程序
        with open(main_program, 'r', encoding='utf-8') as f:
            exec(f.read(), globals())
            
except Exception as e:
    print(f"启动程序时出错: {str(e)}")
    import traceback
    traceback.print_exc()
    # 避免在打包后尝试使用input，因为stdin可能不可用
    import time
    time.sleep(5)