from PIL import Image
import random
import os

# 创建32x32像素的图像，初始颜色为中深灰
image_size = 32
EDGE_GRAY = (0, 0, 0)  # 中深灰边缘颜色
img = Image.new('RGB', (image_size, image_size), color=EDGE_GRAY)
pixels = img.load()

# 定义颜色
BLACK = (0, 0, 0)
# 灰色调 - 使用用户提供的颜色列表（去重后）
GRAY_COLORS = [
    (120, 120, 120),    # 深灰
    (130, 130, 130),    # 深灰
    (100, 100, 100), # 深灰
    (107, 107, 107), # 中深灰
    (110, 110, 110), # 中深灰
    (116, 116, 116), # 中深灰
    (132, 132, 132), # 中灰
    (135, 135, 135), # 中灰
    (140, 140, 140), # 中灰
    (142, 142, 142), # 浅灰
    (143, 143, 143), # 浅灰
    (145, 145, 145)  # 浅灰
]
# 蓝色调 - 使用不同深浅的蓝色
BLUE_COLORS = [
    (0, 0, 255),      # 纯蓝
    (0, 0, 240),      # 深蓝
    (0, 0, 220),      # 深蓝色
    (20, 20, 200),    # 深灰蓝
]

# 让用户输入蓝色像素的数量
try:
        blue_pixels_count = int(input("请输入蓝色像素的数量（建议80-800之间）: "))
        # 限制蓝色像素的范围，避免过多或过少
        blue_pixels_count = max(20, min(800, blue_pixels_count))
except ValueError:
    print("输入无效，使用默认值700个蓝色像素")
    blue_pixels_count = 700  # 使用默认值为700个蓝色像素

# 填充内部区域为随机灰色（最外层1像素保持中深灰边缘）
for x in range(1, image_size - 1):
    for y in range(1, image_size - 1):
        pixels[x, y] = random.choice(GRAY_COLORS)

# 计算集中区域和分散区域的蓝色像素数量
# 92%在集中区域，8%随机分散
concentrated_count = int(blue_pixels_count * 0.92)
dispersed_count = blue_pixels_count - concentrated_count

# 1. 生成集中区域的红色像素（直径6像素的区域）
vein_centers_count = random.randint(3, 6)  # 3-6个矿脉中心
vein_centers = []

# 随机选择矿脉中心点
for _ in range(vein_centers_count):
    x = random.randint(3, image_size - 4)  # 确保在内部区域
    y = random.randint(3, image_size - 4)
    vein_centers.append((x, y))

# 从每个中心点向外扩散形成矿脉（直径6像素，半径3像素）
blue_placed = 0
max_attempts = concentrated_count * 10  # 增加最大尝试次数，确保能填充足够的红色像素
attempt = 0

# 首先确保矿脉中心没有灰色杂质，100%填充中心像素
for center_x, center_y in vein_centers:
    if 1 <= center_x < image_size - 1 and 1 <= center_y < image_size - 1:
        pixels[center_x, center_y] = random.choice(BLUE_COLORS)
        blue_placed += 1
        if blue_placed >= concentrated_count:
            break

# 然后从中心向外扩散形成矿脉（半径3像素，直径6像素）
while blue_placed < concentrated_count and attempt < max_attempts:
    attempt += 1
    
    # 随机选择一个矿脉中心
    if vein_centers:
        center_x, center_y = random.choice(vein_centers)
        
        # 限制扩散距离为1.5像素（直径3像素）
        max_spread = 1.5
        
        # 从中心向外扩散
        # 直接遍历所有可能的dx和dy值，覆盖半径约1.5像素的范围
        # 直径3像素意味着从中心向各方向最多延伸1.5像素
        for dx in range(-2, 3):  # 覆盖-1.5到1.5的范围
            for dy in range(-2, 3):
                if blue_placed >= concentrated_count:
                    break
                    
                x = center_x + dx
                y = center_y + dy
                # 计算欧几里得距离，使矿脉更圆形化
                euclidean_distance = (dx**2 + dy**2)**0.5
                # 确保在内部区域且在合适的距离范围内（直径3像素，半径约1.5像素）
                if euclidean_distance <= max_spread and 1 <= x < image_size - 1 and 1 <= y < image_size - 1:
                    # 设置圆形区域内的填充概率为70%，提高填充效率
                    probability = 0.7  # 提高概率确保能填充更多红色像素
                    if random.random() < probability:
                                        # 只在非蓝色像素上填充，避免重复计算
                        if pixels[x, y] not in BLUE_COLORS:
                            pixels[x, y] = random.choice(BLUE_COLORS)
                            blue_placed += 1

# 2. 生成随机分散的蓝色像素（占20%）
dispersed_placed = 0
max_dispersed_attempts = dispersed_count * 5  # 更多尝试机会确保放置足够的分散像素
dispersed_attempt = 0

# 记录已经是黑色的像素位置，避免重复
# 收集所有非蓝色且非边缘颜色的像素位置作为候选
non_blue_pixels = []
for x in range(1, image_size - 1):
    for y in range(1, image_size - 1):
        if pixels[x, y] not in BLUE_COLORS and pixels[x, y] != EDGE_GRAY:
            non_blue_pixels.append((x, y))

# 随机选择分散的蓝色像素位置
if non_blue_pixels and dispersed_count > 0:
    # 打乱候选列表
    random.shuffle(non_blue_pixels)
    # 选择前dispersed_count个位置
    for x, y in non_blue_pixels[:dispersed_count]:
        pixels[x, y] = random.choice(BLUE_COLORS)
        dispersed_placed += 1

# 确保总蓝色像素数量达到要求
total_blue_placed = blue_placed + dispersed_placed
if total_blue_placed < blue_pixels_count:
    # 如果还不够，在任何位置补充
    remaining = blue_pixels_count - total_blue_placed
    for _ in range(remaining):
        x = random.randint(1, image_size - 2)
        y = random.randint(1, image_size - 2)
        pixels[x, y] = random.choice(BLUE_COLORS)

# 保存图像 - 使用原始字符串避免转义字符问题
output_dir = r"d:\py\py文件\2d游戏\图片代码"
# 实际上目录应该已经存在，我们可以直接保存文件
output_path = os.path.join(output_dir, "煤矿.png")
img.save(output_path)
print(f"蓝煤矿图片已保存至: {output_path}")

# 不再自动显示图像，如需查看请手动打开文件
# img.show()