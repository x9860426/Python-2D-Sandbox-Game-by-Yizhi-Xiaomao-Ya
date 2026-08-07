from PIL import Image, ImageDraw
import random

def generate_minecraft_log_side(output_path="树干.png"):
    # 核心调整：去掉明显棕色边缘，纹理覆盖整个方块（除黑色边框）
    size = 32
    image = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(image)
    
    # 我的世界木材主色调（无单独树皮色，用颜色深浅区分纹理）
    wood_base = [
        (139, 69, 19),  # 中等棕（主色）
        (150, 75, 25),  # 稍浅棕
        (125, 62, 16),  # 稍深棕
        (165, 83, 32)   # 最浅棕
    ]
    
    # 1. 全区域绘制木材纹理（无单独边缘层）
    for x in range(1, size - 1):  # 仅留1像素黑色边框位置
        for y in range(1, size - 1):
            # 垂直木纹核心逻辑（我的世界风格）
            # 用x坐标分组，形成垂直纹理带
            group = x // 4  # 每4像素一组
            
            # 基础颜色选择
            if group % 3 == 0:
                color = wood_base[1]  # 稍浅
            elif group % 3 == 1:
                color = wood_base[0]  # 中等
            else:
                color = wood_base[2]  # 稍深
            
            # 随机微调，打破绝对规律
            if random.random() < 0.4:
                color = (
                    min(255, color[0] + random.randint(-5, 5)),
                    min(255, color[1] + random.randint(-3, 3)),
                    min(255, color[2] + random.randint(-2, 2))
                )
            
            # 横向细微纹理（随机出现）
            if y % 7 == 0 and random.random() < 0.3:
                color = (
                    min(255, color[0] + 4),
                    min(255, color[1] + 2),
                    color[2]
                )
            
            draw.point((x, y), color)
    
    # 2. 添加随机深色木纹线条（增强自然感）
    for _ in range(12):
        # 随机垂直线条
        x = random.randint(2, size - 3)
        length = random.randint(6, 22)
        start_y = random.randint(2, size - 3 - length)
        
        # 深色线条
        line_color = (
            wood_base[2][0] - 5,
            wood_base[2][1] - 3,
            wood_base[2][2] - 2
        )
        
        for y in range(start_y, start_y + length):
            draw.point((x, y), line_color)
    
    # 3. 添加随机浅色斑点（模拟木材结疤）
    for _ in range(8):
        x = random.randint(3, size - 4)
        y = random.randint(3, size - 4)
        size_spot = random.randint(1, 2)
        
        # 浅色斑点
        spot_color = wood_base[3]
        for dx in range(size_spot):
            for dy in range(size_spot):
                if x + dx < size - 2 and y + dy < size - 2:
                    draw.point((x + dx, y + dy), spot_color)
    
    # 4. 绘制1像素黑色边框
    for x in range(size):
        draw.point((x, 0), (0, 0, 0))
        draw.point((x, size - 1), (0, 0, 0))
    
    for y in range(1, size - 1):
        draw.point((0, y), (0, 0, 0))
        draw.point((size - 1, y), (0, 0, 0))
    
    # 保存图片
    image.save(output_path)
    print(f"树干侧面方块已生成：{output_path} (32x32像素)")

if __name__ == "__main__":
    generate_minecraft_log_side()
