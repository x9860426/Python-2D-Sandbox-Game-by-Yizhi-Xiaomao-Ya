from PIL import Image, ImageDraw
import random

def generate_copper_block(output_path="铜块2.png"):
    # 我的世界铜块特点：纯铜色金属质感，有细微纹理，无岩石基底
    size = 32
    image = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(image)
    
    # 铜块颜色（比铜矿石更均匀，金属感更强）
    copper_base = [
        (184, 115, 51),   # 铜色主色调
        (196, 123, 55),   # 稍亮铜色
        (172, 107, 47),   # 稍暗铜色
        (205, 133, 60)    # 高光铜色
    ]
    
    # 金属纹理线条颜色（略深于主色）
    line_colors = [
        (160, 95, 40),    # 深铜色线条
        (170, 102, 45)    # 中深铜色线条
    ]
    
    # 1. 填充铜块基底（全块都是铜材质）
    for x in range(1, size - 1):
        for y in range(1, size - 1):
            # 基础铜色
            color = random.choice(copper_base)
            
            # 细微的明暗变化，体现金属质感
            if random.random() < 0.4:
                var = random.randint(-5, 5)
                color = (
                    max(0, min(255, color[0] + var)),
                    max(0, min(255, color[1] + var)),
                    max(0, min(255, color[2] + var))
                )
            
            draw.point((x, y), color)
    
    # 2. 添加金属纹理线条（横向和纵向）
    # 横向线条
    for y in range(3, size - 3, 4):  # 每隔4像素一条
        for x in range(2, size - 2):
            if random.random() < 0.7:  # 70%概率绘制线条
                # 线条颜色稍深
                draw.point((x, y), random.choice(line_colors))
                # 线条下方1像素稍亮，增强立体感
                if y + 1 < size - 2 and random.random() < 0.5:
                    draw.point((x, y + 1), copper_base[3])
    
    # 纵向线条
    for x in range(3, size - 3, 5):  # 每隔5像素一条
        for y in range(2, size - 2):
            if random.random() < 0.6:  # 60%概率绘制线条
                draw.point((x, y), random.choice(line_colors))
                # 线条右侧1像素稍亮，增强立体感
                if x + 1 < size - 2 and random.random() < 0.5:
                    draw.point((x + 1, y), copper_base[3])
    
    # 3. 添加随机金属亮点（增强金属光泽）
    for _ in range(15, 25):
        x = random.randint(2, size - 3)
        y = random.randint(2, size - 3)
        # 1像素亮点
        if random.random() < 0.6:
            draw.point((x, y), copper_base[3])
        # 偶尔出现2x2的亮点簇
        elif random.random() < 0.2:
            for dx in range(2):
                for dy in range(2):
                    if x + dx < size - 2 and y + dy < size - 2:
                        draw.point((x + dx, y + dy), copper_base[3])
    
    # 4. 绘制1像素黑色边框（与矿石系列保持一致）
    for x in range(size):
        draw.point((x, 0), (0, 0, 0))
        draw.point((x, size - 1), (0, 0, 0))
    
    for y in range(1, size - 1):
        draw.point((0, y), (0, 0, 0))
        draw.point((size - 1, y), (0, 0, 0))
    
    # 保存图片
    image.save(output_path)
    print(f"铜块图片已生成：{output_path} (32x32像素)")

if __name__ == "__main__":
    generate_copper_block()
