from PIL import Image
import random
import os

# 创建32x32像素的图像
image_size = 32

# 定义颜色
EDGE_LIGHT_BLUE = (120, 160, 255)  # 纯蓝色边缘

# 定义不同深浅的蓝色（中心区域使用）
LIGHT_BLUE_COLORS = [
     (160, 180, 255),    # 亮蓝色
     (140, 160, 240),    # 蓝色
     (180, 200, 255),    # 很亮的蓝色
     (150, 170, 245),    # 蓝色
     (130, 150, 230),    # 较深的蓝色
]

# 创建图像并设置边缘为浅蓝色
img = Image.new('RGB', (image_size, image_size), color=EDGE_LIGHT_BLUE)
pixels = img.load()

# 填充内部区域为随机黑色（最外层1像素保持微黑色边缘）
for x in range(1, image_size - 1):
    for y in range(1, image_size - 1):
        # 随机选择一种浅蓝色
        pixels[x, y] = random.choice(LIGHT_BLUE_COLORS)

# 可以选择添加一些随机性变化，让煤块看起来更自然
# 1. 随机添加一些稍微亮一点的像素（模拟煤块的纹理）
for _ in range(int(image_size * image_size * 0.05)):  # 5%的像素有亮斑
    x = random.randint(1, image_size - 2)
    y = random.randint(1, image_size - 2)
    # 添加一些稍微亮一点的蓝色像素（模拟蓝色方块的纹理）
    blue_brightness = random.randint(230, 255)
    # 直接使用LIGHT_BLUE_COLORS中类似色调的值，避免引入额外绿色
    pixels[x, y] = (210, 220, blue_brightness)

# 2. 随机添加一些暗黑色斑块，增加煤块的层次感
for _ in range(int(image_size * image_size * 0.1)):  # 10%的像素有暗斑块
    x = random.randint(1, image_size - 2)
    y = random.randint(1, image_size - 2)
    # 添加更深的蓝色像素
    dark_blue = random.randint(80, 120)
    # 使用与LIGHT_BLUE_COLORS协调的颜色值
    pixels[x, y] = (100, 140, dark_blue)

# 保存图像
output_dir = r"d:\py\py文件\2d游戏\图片代码"
output_path = os.path.join(output_dir, "浅蓝色块.png")
img.save(output_path)
print(f"浅蓝色块图片已保存至: {output_path}")

# 不再自动显示图像，如需查看请手动打开文件