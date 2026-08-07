from PIL import Image
import random
import os

# 创建32x32像素的图像
image_size = 32

# 定义颜色
EDGE_BLACK = (120, 120, 120)  # 微黑色边缘

# 定义不同深浅的黑色（中心区域使用）
BLACK_COLORS = [
    (50, 50, 50),        # 纯黑
    (0, 0, 0),        # 几乎黑色
    (10, 10, 10),     # 深黑色
    (30, 30, 30),     # 深黑色
    (20, 20, 20),     # 深灰色（接近微黑色，用于渐变）
]

# 创建图像并设置边缘为微黑色
img = Image.new('RGB', (image_size, image_size), color=EDGE_BLACK)
pixels = img.load()

# 填充内部区域为随机黑色（最外层1像素保持微黑色边缘）
for x in range(1, image_size - 1):
    for y in range(1, image_size - 1):
        # 随机选择一种黑色
        pixels[x, y] = random.choice(BLACK_COLORS)

# 可以选择添加一些随机性变化，让煤块看起来更自然
# 1. 随机添加一些稍微亮一点的像素（模拟煤块的纹理）
for _ in range(int(image_size * image_size * 0.05)):  # 5%的像素有亮斑
    x = random.randint(1, image_size - 2)
    y = random.randint(1, image_size - 2)
    # 添加一些稍微亮一点的像素，但仍然保持在黑色范围内
    brightness = random.randint(25, 40)
    pixels[x, y] = (brightness, brightness, brightness)

# 2. 随机添加一些暗黑色斑块，增加煤块的层次感
for _ in range(int(image_size * image_size * 0.1)):  # 10%的像素有暗斑块
    x = random.randint(1, image_size - 2)
    y = random.randint(1, image_size - 2)
    # 添加更暗的黑色像素
    darkness = random.randint(0, 8)
    pixels[x, y] = (darkness, darkness, darkness)

# 保存图像
output_dir = r"d:\py\py文件\2d游戏\图片代码"
output_path = os.path.join(output_dir, "煤块.png")
img.save(output_path)
print(f"煤块图片已保存至: {output_path}")

# 不再自动显示图像，如需查看请手动打开文件