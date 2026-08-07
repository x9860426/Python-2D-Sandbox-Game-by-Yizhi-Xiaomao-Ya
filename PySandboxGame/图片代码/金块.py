from PIL import Image, ImageDraw
import random

def generate_gold_block(output_path="金块.png"):
    # 金块特点：金黄色金属质感，带有自然纹理和光泽，保持方块特性
    size = 32
    image = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(image)
    
    # 金块颜色体系（金黄色调，区分基础色、纹理色和高光色）
    gold_colors = [
        (255, 215, 0),    # 基础金色（主色调）
        (240, 190, 0),    # 暗金色（用于纹理线条）
        (255, 230, 50),   # 亮金色（用于高光）
        (255, 220, 20)    # 暖金色（用于过渡）
    ]
    
    # 1. 填充基础底色（以金色为主，保持统一性）
    for x in range(1, size - 1):
        for y in range(1, size - 1):
            # 基础色占比高，保证整体金色基调
            if random.random() < 0.75:
                color = gold_colors[0]
            elif random.random() < 0.6:
                color = gold_colors[3]  # 少量暖金色过渡
            else:
                color = gold_colors[2]  # 少量高光
            draw.point((x, y), color)
    
    # 2. 绘制自然金属纹理（非严格网格，更自然的线条）
    # 横向纹理
    for y in range(2, size - 2, random.randint(3, 5)):
        for x in range(1, size - 1):
            # 线条有自然断续，避免过于规则
            if random.random() < 0.7:
                draw.point((x, y), gold_colors[1])
                # 线条下方添加轻微高光
                if y + 1 < size - 2 and random.random() < 0.4:
                    draw.point((x, y + 1), gold_colors[2])
    
    # 纵向纹理
    for x in range(2, size - 2, random.randint(4, 6)):
        for y in range(1, size - 1):
            if random.random() < 0.6:
                draw.point((x, y), gold_colors[1])
                # 线条右侧添加轻微高光
                if x + 1 < size - 2 and random.random() < 0.4:
                    draw.point((x + 1, y), gold_colors[2])
    
    # 3. 添加金属光泽高光（随机分布但不过于密集）
    # 小高光点
    for _ in range(30, 40):
        x = random.randint(1, size - 2)
        y = random.randint(1, size - 2)
        if random.random() < 0.5:
            draw.point((x, y), gold_colors[2])
    
    # 稍大的高光簇
    for _ in range(5, 8):
        x = random.randint(2, size - 4)
        y = random.randint(2, size - 4)
        for dx in range(2):
            for dy in range(2):
                draw.point((x + dx, y + dy), gold_colors[2])
    
    # 4. 绘制1像素黑色边框（保持方块特性）
    for x in range(size):
        draw.point((x, 0), (0, 0, 0))
        draw.point((x, size - 1), (0, 0, 0))
    
    for y in range(1, size - 1):
        draw.point((0, y), (0, 0, 0))
        draw.point((size - 1, y), (0, 0, 0))
    
    # 保存图片
    image.save(output_path)
    print(f"金块图片已生成：{output_path} (32x32像素)")

if __name__ == "__main__":
    generate_gold_block()
