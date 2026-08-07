from PIL import Image, ImageDraw
import random

def generate_gold_ore_block(output_path="金矿石.png"):
    # 金矿石含量约15%，比铁更稀有
    size = 32
    image = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(image)
    
    # 颜色定义 - 金矿石为金黄色
    stone_colors = [
        (120, 120, 120),  # 中灰
        (135, 135, 135),  # 浅灰
        (110, 110, 110),  # 中深灰
        (140, 140, 140),  # 亮灰
        (100, 100, 100)   # 深灰
    ]
    
    gold_colors = [
        (218, 165, 32),   # 金色
        (238, 201, 0),    # 亮金色
        (205, 153, 0),    # 深金色
        (255, 215, 0)     # 高亮金色
    ]
    
    # 绘制岩石基底
    for x in range(1, size - 1):
        for y in range(1, size - 1):
            color = random.choice(stone_colors)
            
            # 岩石纹理
            if random.random() < 0.3:
                variation = random.randint(-8, 8)
                color = (
                    max(0, min(255, color[0] + variation)),
                    max(0, min(255, color[1] + variation)),
                    max(0, min(255, color[2] + variation))
                )
            
            draw.point((x, y), color)
    
    # 生成金矿脉（约15%含量，更稀有）
    for _ in range(1, 3):  # 更少的矿脉簇
        start_x = random.randint(4, size - 8)
        start_y = random.randint(4, size - 8)
        width = random.randint(3, 5)  # 更小的矿脉
        height = random.randint(3, 5)
        
        for x in range(start_x, start_x + width):
            for y in range(start_y, start_y + height):
                if x < size - 2 and y < size - 2 and random.random() < 0.5:  # 更低的填充率
                    if x == start_x or x == start_x + width - 1 or \
                       y == start_y or y == start_y + height - 1:
                        color = random.choice(gold_colors[2:3])
                    else:
                        color = random.choice([gold_colors[0], gold_colors[1], gold_colors[3]])
                    
                    draw.point((x, y), color)
    
    # 添加细小金矿颗粒（更少）
    for _ in range(5, 8):
        x = random.randint(2, size - 3)
        y = random.randint(2, size - 3)
        grain_size = random.randint(1, 2)
        
        for dx in range(grain_size):
            for dy in range(grain_size):
                if x + dx < size - 2 and y + dy < size - 2:
                    draw.point((x + dx, y + dy), random.choice(gold_colors))
    
    # 绘制边框
    for x in range(size):
        draw.point((x, 0), (0, 0, 0))
        draw.point((x, size - 1), (0, 0, 0))
    
    for y in range(1, size - 1):
        draw.point((0, y), (0, 0, 0))
        draw.point((size - 1, y), (0, 0, 0))
    
    image.save(output_path)
    print(f"金矿石图片已生成：{output_path}")

if __name__ == "__main__":
    generate_gold_ore_block()
