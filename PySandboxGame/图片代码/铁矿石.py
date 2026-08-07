from PIL import Image, ImageDraw
import random

def generate_iron_ore_block(output_path="铁矿石.png"):
    # 基于铜矿石代码修改，生成铁矿石（保持相同结构和20%含量）
    size = 32
    image = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(image)
    
    # 颜色定义（将铜色替换为铁的银灰色系）
    stone_colors = [
        (120, 120, 120),  # 中灰
        (135, 135, 135),  # 浅灰
        (110, 110, 110),  # 中深灰
        (140, 140, 140),  # 亮灰
        (100, 100, 100)   # 深灰
    ]
    
    # 铁矿石颜色（替换铜的橙红色为银灰色）
    iron_colors = [
        (160, 160, 160),  # 浅灰铁色（主矿脉）
        (140, 140, 140),  # 中灰铁色（次要矿脉）
        (120, 120, 120),  # 深灰铁色（矿脉边缘）
        (180, 180, 180)   # 亮灰铁色（高光部分）
    ]
    
    # 1. 绘制岩石基底（保持与铜矿石相同的逻辑）
    for x in range(1, size - 1):
        for y in range(1, size - 1):
            # 基础岩石颜色
            color = random.choice(stone_colors)
            
            # 岩石纹理（细微明暗变化）
            if random.random() < 0.3:
                variation = random.randint(-8, 8)
                color = (
                    max(0, min(255, color[0] + variation)),
                    max(0, min(255, color[1] + variation)),
                    max(0, min(255, color[2] + variation))
                )
            
            draw.point((x, y), color)
    
    # 2. 生成铁矿石矿脉（保持铜矿石的分布逻辑，约20%含量）
    # 主要矿脉簇（数量和大小与铜矿石一致）
    for _ in range(3, 5):  # 3-4个主要矿脉
        start_x = random.randint(3, size - 8)
        start_y = random.randint(3, size - 8)
        width = random.randint(4, 8)
        height = random.randint(4, 8)
        
        # 填充矿脉簇
        for x in range(start_x, start_x + width):
            for y in range(start_y, start_y + height):
                if x < size - 2 and y < size - 2:
                    # 矿脉内部随机颜色变化（保持与铜矿石相同的填充率）
                    if random.random() < 0.7:  # 70%概率是铁矿
                        # 矿脉边缘颜色稍深
                        if x == start_x or x == start_x + width - 1 or \
                           y == start_y or y == start_y + height - 1:
                            color = random.choice(iron_colors[1:3])
                        else:
                            color = random.choice([iron_colors[0], iron_colors[3]])
                        
                        draw.point((x, y), color)
    
    # 3. 添加细小铁矿颗粒（保持与铜矿石相同的密度）
    for _ in range(15, 25):  # 15-25个小颗粒
        x = random.randint(2, size - 3)
        y = random.randint(2, size - 3)
        # 1-2像素大小的颗粒
        grain_size = random.randint(1, 2)
        
        for dx in range(grain_size):
            for dy in range(grain_size):
                if x + dx < size - 2 and y + dy < size - 2:
                    draw.point((x + dx, y + dy), random.choice(iron_colors))
    
    # 4. 绘制1像素黑色边框（与铜矿石保持一致）
    for x in range(size):
        draw.point((x, 0), (0, 0, 0))
        draw.point((x, size - 1), (0, 0, 0))
    
    for y in range(1, size - 1):
        draw.point((0, y), (0, 0, 0))
        draw.point((size - 1, y), (0, 0, 0))
    
    # 保存图片
    image.save(output_path)
    print(f"铁矿石图片已生成：{output_path} (32x32像素)")

if __name__ == "__main__":
    generate_iron_ore_block()
