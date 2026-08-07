from PIL import Image, ImageDraw
import random

def generate_regular_iron_block(output_path="规则铁块.png"):
    # 规则铁块核心：对称网格纹理+统一金属色，减少随机性，增强整齐感
    size = 32
    image = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(image)
    
    # 铁块颜色体系（金属银灰色，区分基础色、线条色、高光色）
    iron_colors = [
        (160, 160, 160),  # 基础银灰色（占比最高，保证统一性）
        (140, 140, 140),  # 暗灰色（用于网格线条，增强轮廓）
        (180, 180, 180)   # 亮灰色（用于高光，体现金属质感）
    ]
    
    # 1. 填充基础底色（高度统一，减少随机变化）
    for x in range(1, size - 1):
        for y in range(1, size - 1):
            # 85%使用基础色，15%使用轻微高光，避免单调
            if random.random() < 0.85:
                color = iron_colors[0]
            else:
                color = iron_colors[2]
            draw.point((x, y), color)
    
    # 2. 绘制主网格线条（核心规则元素，连续无断裂）
    main_grid = 8  # 主网格尺寸（32x32分为4x4网格）
    
    # 横向主线条
    for y in range(main_grid, size - 1, main_grid):
        for x in range(1, size - 1):
            draw.point((x, y), iron_colors[1])
            # 线条下方1像素添加高光，增强立体感
            if y + 1 < size - 1:
                draw.point((x, y + 1), iron_colors[2])
    
    # 纵向主线条
    for x in range(main_grid, size - 1, main_grid):
        for y in range(1, size - 1):
            draw.point((x, y), iron_colors[1])
            # 线条右侧1像素添加高光
            if x + 1 < size - 1:
                draw.point((x + 1, y), iron_colors[2])
    
    # 3. 绘制次级网格（增强规则感，主网格的1/2大小）
    sub_grid = main_grid // 2
    
    # 横向次线条（更细，颜色稍浅）
    for y in range(sub_grid, size - 1, sub_grid):
        for x in range(1, size - 1):
            # 次级线条不连续，形成更细致的纹理
            if random.random() < 0.6:
                draw.point((x, y), (150, 150, 150))  # 中间色调
    
    # 纵向次线条
    for x in range(sub_grid, size - 1, sub_grid):
        for y in range(1, size - 1):
            if random.random() < 0.6:
                draw.point((x, y), (150, 150, 150))
    
    # 4. 添加规则高光点（每个主网格内固定位置）
    for x in range(main_grid//2, size - 1, main_grid):
        for y in range(main_grid//2, size - 1, main_grid):
            # 主网格中心高光
            draw.point((x, y), iron_colors[2])
            # 中心周围形成小高光簇
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                if 1 <= x + dx < size - 1 and 1 <= y + dy < size - 1:
                    draw.point((x + dx, y + dy), iron_colors[2])
    
    # 5. 绘制1像素黑色边框（与其他方块保持一致）
    for x in range(size):
        draw.point((x, 0), (0, 0, 0))
        draw.point((x, size - 1), (0, 0, 0))
    
    for y in range(1, size - 1):
        draw.point((0, y), (0, 0, 0))
        draw.point((size - 1, y), (0, 0, 0))
    
    # 保存图片
    image.save(output_path)
    print(f"规则铁块图片已生成：{output_path} (32x32像素)")

if __name__ == "__main__":
    generate_regular_iron_block()
