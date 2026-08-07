from PIL import Image, ImageDraw
import random

def generate_diamond_block(output_path="钻石块.png"):
    # 优化后的钻石块：更自然的晶体纹理，更协调的高光分布，提升视觉美感
    size = 32
    image = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(image)
    
    # 钻石颜色体系（更和谐的浅蓝色调，避免过饱和）
    diamond_colors = [
        (180, 220, 235),  # 柔和基础蓝（主色调，更自然）
        (150, 210, 240),  # 通透浅蓝色（用于过渡）
        (230, 250, 255),  # 柔和高光（不刺眼）
        (120, 190, 230)   # 深邃蓝（用于纹理边缘，增强层次）
    ]
    
    # 1. 填充基础底色（渐变过渡，增强立体感）
    for x in range(1, size - 1):
        for y in range(1, size - 1):
            # 中心区域更亮，边缘稍暗，形成自然过渡
            dist_from_center = abs(x - 15) + abs(y - 15)
            brightness_factor = 1 - (dist_from_center / 40)
            
            if random.random() < 0.6 + (brightness_factor * 0.2):
                color = diamond_colors[0]
            elif random.random() < 0.5:
                color = diamond_colors[1]
            else:
                color = diamond_colors[2]
                
            draw.point((x, y), color)
    
    # 2. 绘制优雅的晶体纹理（更自然的线条分布）
    # 主纹理线（更少但更流畅）
    for _ in range(3):
        # 随机起始点
        start_x = random.randint(3, 6)
        start_y = random.randint(3, 28)
        end_x = random.randint(25, 28)
        end_y = random.randint(3, 28)
        
        # 绘制平滑斜线
        for i in range(100):
            t = i / 100
            x = int(start_x + (end_x - start_x) * t)
            y = int(start_y + (end_y - start_y) * t)
            if 1 < x < size-2 and 1 < y < size-2:
                if random.random() < 0.8:  # 轻微断续，更自然
                    draw.point((x, y), diamond_colors[3])
                    # 线条一侧添加柔和高光
                    if random.random() < 0.5:
                        draw.point((x+1, y), diamond_colors[2])
                    else:
                        draw.point((x, y+1), diamond_colors[2])
    
    # 3. 交叉纹理（增强晶体结构感但不过于密集）
    for y in range(8, 24, 6):
        for x in range(1, size-1):
            if random.random() < 0.3:
                draw.point((x, y), diamond_colors[3])
                
    for x in range(8, 24, 6):
        for y in range(1, size-1):
            if random.random() < 0.3:
                draw.point((x, y), diamond_colors[3])
    
    # 4. 高品质高光效果（更协调的分布）
    # 中心高光区（最亮区域）
    center_glow_size = 5
    center_x, center_y = 15, 15
    for dx in range(-center_glow_size, center_glow_size+1):
        for dy in range(-center_glow_size, center_glow_size+1):
            x = center_x + dx
            y = center_y + dy
            if 1 < x < size-2 and 1 < y < size-2:
                dist = (dx**2 + dy**2)**0.5
                if dist < center_glow_size and random.random() < 1 - (dist/center_glow_size):
                    draw.point((x, y), diamond_colors[2])
    
    # 边缘反光点（模拟光线反射）
    edge_points = [
        (5, 5), (26, 5), (5, 26), (26, 26),
        (15, 5), (15, 26), (5, 15), (26, 15)
    ]
    for (x, y) in edge_points:
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                nx = x + dx
                ny = y + dy
                if 1 < nx < size-2 and 1 < ny < size-2:
                    if random.random() < 0.3:
                        draw.point((nx, ny), diamond_colors[2])
    
    # 5. 精致边框（稍细于之前，更协调）
    for x in range(size):
        draw.point((x, 0), (30, 30, 30))  # 深灰色边框，比纯黑更柔和
        draw.point((x, size - 1), (30, 30, 30))
    
    for y in range(1, size - 1):
        draw.point((0, y), (30, 30, 30))
        draw.point((size - 1, y), (30, 30, 30))
    
    # 保存图片
    image.save(output_path)
    print(f"钻石块图片已生成：{output_path} (32x32像素)")

if __name__ == "__main__":
    generate_diamond_block()
