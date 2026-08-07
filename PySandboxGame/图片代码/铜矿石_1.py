from PIL import Image, ImageDraw
import random

def generate_copper_ore_block(output_path="铜矿石.png"):
    # 我的世界铜矿石特点：岩石基底+橙红色铜矿脉，矿脉随机分布且有自然纹理
    size = 32
    image = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(image)
    
    # 颜色定义（贴合我的世界原版铜矿石色调）
    # 岩石基底颜色（灰色系，带细微变化）
    stone_colors = [
        (120, 120, 120),  # 中灰
        (135, 135, 135),  # 浅灰
        (110, 110, 110),  # 中深灰
        (140, 140, 140),  # 亮灰
        (100, 100, 100)   # 深灰
    ]
    
    # 铜矿石颜色（橙红色系，区分不同矿脉深浅）
    copper_colors = [
        (200, 110, 50),   # 浅橙铜色（主矿脉）
        (180, 95, 40),    # 中橙铜色（次要矿脉）
        (160, 80, 30),    # 深橙铜色（矿脉边缘）
        (210, 120, 60)    # 亮橙铜色（高光部分）
    ]
    
    # 1. 绘制岩石基底
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
    
    # 2. 生成铜矿石矿脉（随机分布的簇状结构）
    # 先创建几个主要矿脉簇
    for _ in range(3, 5):  # 3-4个主要矿脉
        # 随机矿脉位置和大小
        start_x = random.randint(3, size - 8)
        start_y = random.randint(3, size - 8)
        width = random.randint(4, 8)
        height = random.randint(4, 8)
        
        # 填充矿脉簇
        for x in range(start_x, start_x + width):
            for y in range(start_y, start_y + height):
                if x < size - 2 and y < size - 2:
                    # 矿脉内部随机颜色变化
                    if random.random() < 0.7:  # 70%概率是铜矿
                        # 矿脉边缘颜色稍深
                        if x == start_x or x == start_x + width - 1 or \
                           y == start_y or y == start_y + height - 1:
                            color = random.choice(copper_colors[1:3])
                        else:
                            color = random.choice([copper_colors[0], copper_colors[3]])
                        
                        draw.point((x, y), color)
    
    # 3. 添加细小铜矿颗粒（增强自然感）
    for _ in range(15, 25):  # 15-25个小颗粒
        x = random.randint(2, size - 3)
        y = random.randint(2, size - 3)
        # 1-2像素大小的颗粒
        grain_size = random.randint(1, 2)
        
        for dx in range(grain_size):
            for dy in range(grain_size):
                if x + dx < size - 2 and y + dy < size - 2:
                    draw.point((x + dx, y + dy), random.choice(copper_colors))
    
    # 4. 绘制1像素黑色边框
    for x in range(size):
        draw.point((x, 0), (0, 0, 0))
        draw.point((x, size - 1), (0, 0, 0))
    
    for y in range(1, size - 1):
        draw.point((0, y), (0, 0, 0))
        draw.point((size - 1, y), (0, 0, 0))
    
    # 保存图片
    image.save(output_path)
    print(f"铜矿石图片已生成：{output_path} (32x32像素)")

if __name__ == "__main__":
    generate_copper_ore_block()
