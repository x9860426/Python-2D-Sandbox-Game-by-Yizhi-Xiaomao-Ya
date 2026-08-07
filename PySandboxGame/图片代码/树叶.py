from PIL import Image, ImageDraw
import random

def generate_minecraft_leaf_block(output_path="树叶.png"):
    # 我的世界树叶特点：绿色为主，随机分布，带有少量空隙和深色纹理
    size = 32
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))  # 使用透明背景
    draw = ImageDraw.Draw(image)
    
    # 树叶颜色（我的世界经典绿色调）
    leaf_colors = [
        (34, 139, 34, 255),    # 深绿
        (46, 139, 87, 255),    # 海绿
        (50, 205, 50, 255),    # 亮绿
        (37, 116, 36, 255),    # 暗绿
        (60, 179, 113, 255)    # 中绿
    ]
    
    # 深色纹理（叶脉和阴影）
    vein_colors = [
        (20, 100, 20, 255),    # 深暗绿
        (30, 110, 30, 255),    # 暗绿
        (25, 80, 25, 255)      # 极暗绿
    ]
    
    # 1. 绘制基础树叶（覆盖大部分区域）
    for x in range(1, size - 1):
        for y in range(1, size - 1):
            # 随机决定是否为树叶（留一些空隙模拟自然树叶）
            if random.random() > 0.15:  # 85%概率是树叶
                # 选择基础颜色
                color = random.choice(leaf_colors)
                
                # 随机添加叶脉纹理
                if random.random() < 0.2:  # 20%概率添加叶脉
                    color = random.choice(vein_colors)
                
                # 边缘区域随机减少密度
                if (x < 4 or x > size - 5 or y < 4 or y > size - 5) and random.random() < 0.3:
                    # 边缘部分透明化
                    color = (color[0], color[1], color[2], 100)
                
                draw.point((x, y), color)
    
    # 2. 添加随机叶片簇（增强自然感）
    for _ in range(8):
        # 随机位置生成小叶片簇
        x = random.randint(3, size - 4)
        y = random.randint(3, size - 4)
        cluster_size = random.randint(2, 3)
        
        for dx in range(cluster_size):
            for dy in range(cluster_size):
                if x + dx < size - 2 and y + dy < size - 2:
                    # 簇内颜色稍亮
                    color = random.choice(leaf_colors)
                    bright_color = (min(255, color[0]+10), min(255, color[1]+10), color[2], 255)
                    draw.point((x + dx, y + dy), bright_color)
    
    # 3. 添加深色阴影斑点（模拟树叶重叠）
    for _ in range(5):
        x = random.randint(2, size - 3)
        y = random.randint(2, size - 3)
        spot_size = random.randint(2, 4)
        
        for dx in range(spot_size):
            for dy in range(spot_size):
                if x + dx < size - 2 and y + dy < size - 2 and random.random() < 0.7:
                    draw.point((x + dx, y + dy), random.choice(vein_colors))
    
    # 4. 绘制1像素黑色边框
    for x in range(size):
        draw.point((x, 0), (0, 0, 0, 255))
        draw.point((x, size - 1), (0, 0, 0, 255))
    
    for y in range(1, size - 1):
        draw.point((0, y), (0, 0, 0, 255))
        draw.point((size - 1, y), (0, 0, 0, 255))
    
    # 保存图片（带透明通道）
    image.save(output_path)
    print(f"树叶方块图片已生成：{output_path} (32x32像素)")

if __name__ == "__main__":
    generate_minecraft_leaf_block()
