from PIL import Image
import random
import math

# 创建透明底的小煤块图像（RGBA模式）
width, height = 32, 32  # 32x32像素的小煤块
image = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # 透明背景
pixels = image.load()

# 定义煤块的黑色调颜色列表
BLACK_COLORS = [
    (30, 30, 30, 255),   # 浅黑色
    (20, 20, 20, 255),   # 中黑色
    (15, 15, 15, 255),   # 深黑色
    (10, 10, 10, 255),   # 更深黑色
    (5, 5, 5, 255),      # 接近纯黑
    (0, 0, 0, 255)       # 纯黑色
]

# 定义煤块的基本形状（不规则的多边形）
def is_inside_coal(x, y):
    # 创建一个不规则的形状，模拟煤块的自然外观
    # 使用简单的距离公式和随机性来创建不规则边界
    center_x, center_y = width // 2, height // 2
    distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
    # 基础半径为12-14像素，加上一些随机变化使其更自然
    base_radius = random.uniform(12, 14)
    # 添加一些不规则性
    irregularity = random.uniform(-1, 1)
    # 根据位置调整不规则性，使边缘更加自然
    angle_factor = (x + y) % 360
    irregularity += 0.5 * math.sin(angle_factor)
    
    # 判断是否在煤块内部
    return distance < base_radius + irregularity

# 填充煤块的基本形状
for x in range(width):
    for y in range(height):
        if is_inside_coal(x, y):
            # 为煤块内部填充不同深浅的黑色
            color = random.choice(BLACK_COLORS)
            pixels[x, y] = color

# 添加一些高光和纹理效果，使煤块看起来更自然
for x in range(width):
    for y in range(height):
        if pixels[x, y][3] > 0:  # 如果该像素不是透明的
            # 20%的概率添加一些亮斑，增加纹理
            if random.random() < 0.2:
                # 选择一个稍亮的颜色
                brightness = random.randint(25, 60)
                pixels[x, y] = (brightness, brightness, brightness, 255)
            # 10%的概率添加一些更深的斑块
            elif random.random() < 0.1:
                # 选择一个更深的颜色
                dark = random.randint(0, 15)
                pixels[x, y] = (dark, dark, dark, 255)

# 添加一些边缘细节，使煤块看起来更立体
for x in range(width):
    for y in range(height):
        # 检查边缘像素
        if pixels[x, y][3] > 0:  # 如果该像素不是透明的
            # 检查相邻像素是否有透明的（表示这是边缘）
            is_edge = False
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if pixels[nx, ny][3] == 0:
                            is_edge = True
                            break
                if is_edge:
                    break
            
            # 如果是边缘像素，根据位置调整亮度
            if is_edge:
                # 为边缘添加一些变化
                if random.random() < 0.4:
                    # 稍微提亮边缘
                    r, g, b, a = pixels[x, y]
                    new_brightness = min(255, r + random.randint(10, 30))
                    pixels[x, y] = (new_brightness, new_brightness, new_brightness, a)

# 保存图像为透明底PNG
image.save("d:\\py\\py文件\\2d游戏\\图片代码\\小煤块.png", "PNG")
print("小煤块图像已生成并保存为PNG格式（透明背景）")