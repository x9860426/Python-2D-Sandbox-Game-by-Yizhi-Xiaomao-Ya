from PIL import Image, ImageDraw
import random
import os

# 创建32x32像素的图像，初始为透明背景
image_size = 32
img = Image.new('RGBA', (image_size, image_size), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 定义熔炉的颜色
DARK_GRAY = (60, 60, 60, 255)    # 深灰色主体
MEDIUM_GRAY = (80, 80, 80, 255)  # 中灰色
LIGHT_GRAY = (100, 100, 100, 255) # 浅灰色
ORANGE = (255, 140, 0, 255)      # 橙色火焰
YELLOW = (255, 230, 0, 255)      # 黄色火焰
BROWN = (139, 69, 19, 255)       # 棕色细节
BLACK = (30, 30, 30, 255)        # 黑色细节

# 绘制熔炉主体
# 底部矩形
lower_part = [(5, 16), (26, 30)]
draw.rectangle(lower_part, fill=DARK_GRAY)

# 上部矩形
upper_part = [(7, 5), (24, 18)]
draw.rectangle(upper_part, fill=MEDIUM_GRAY)

# 添加纹理和细节
# 横向金属条
draw.rectangle([(4, 15), (27, 17)], fill=BLACK)  # 分隔条

# 左右边缘细节
for i in range(3):
    # 左侧边缘
    draw.rectangle([(3, 6 + i*8), (5, 10 + i*8)], fill=LIGHT_GRAY)
    # 右侧边缘
    draw.rectangle([(26, 6 + i*8), (28, 10 + i*8)], fill=LIGHT_GRAY)

# 底部细节线条
for i in range(3):
    draw.rectangle([(6 + i*7, 29), (11 + i*7, 30)], fill=BLACK)

# 顶部边缘细节
for i in range(3):
    draw.rectangle([(8 + i*6, 4), (12 + i*6, 5)], fill=LIGHT_GRAY)

# 火焰部分（在下部矩形中间）
# 内部空洞
draw.rectangle([(12, 20), (19, 28)], fill=(0, 0, 0, 100))

# 绘制火焰效果
for x in range(12, 20):
    for y in range(20, 28):
        # 使用渐变效果
        intensity = 1 - (y - 20) / 8.0
        if random.random() < intensity * 0.7:
            # 越靠近顶部，黄色越多
            if y < 22:
                color = YELLOW
            elif y < 25:
                # 中间部分随机橙黄混合
                if random.random() < 0.5:
                    color = ORANGE
                else:
                    color = YELLOW
            else:
                color = ORANGE
            
            # 设置透明度渐变
            alpha = int(200 + 55 * intensity)
            color_with_alpha = (color[0], color[1], color[2], alpha)
            draw.point((x, y), fill=color_with_alpha)

# 添加一些随机的金属亮点
for _ in range(8):
    x = random.randint(6, 25)
    y = random.randint(6, 29)
    # 避免在火焰区域添加亮点
    if not (12 <= x <= 19 and 20 <= y <= 28):
        draw.point((x, y), fill=(200, 200, 200, 255))

# 保存图像
output_dir = r"d:\py\py文件\2d游戏\图片代码"
output_path = os.path.join(output_dir, "熔炉.png")
img.save(output_path)

print(f"熔炉图像已保存至: {output_path}")

# 不再自动显示图像，如需查看请手动打开文件
# img.show()