from PIL import Image, ImageDraw
import random
import math

def generate_lava_block(output_path="岩浆.png"):
    # 尺寸设置
    size = 32
    # 使用RGBA模式支持透明边缘
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 岩浆颜色体系（纯红色调，无其他杂色）
    lava_colors = [
        (255, 60, 0, 210),    # 深红（基础色）
        (255, 90, 0, 220),    # 亮红
        (255, 30, 0, 200),    # 暗红
        (255, 120, 0, 230),   # 高亮红（岩浆亮斑）
        (255, 10, 0, 190)     # 深暗红
    ]
    
    # 生成岩浆基础纹理
    for x in range(size):
        for y in range(size):
            # 只使用纯红色系
            color = random.choice(lava_colors)
            
            # 保持颜色连贯性，模拟岩浆流动
            if random.random() < 0.65:
                if x > 0:
                    left_color = image.getpixel((x-1, y))
                    # 固定红色通道为255，调整绿色通道控制深浅
                    color = (
                        255,  # 红色通道最大值
                        max(10, min(130, (color[1] + left_color[1]) // 2)),  # 绿色通道控制明暗
                        0,  # 蓝色通道固定为0
                        color[3]
                    )
                elif y > 0:
                    top_color = image.getpixel((x, y-1))
                    color = (
                        255,
                        max(10, min(130, (color[1] + top_color[1]) // 2)),
                        0,
                        color[3]
                    )
            
            # 岩浆流动效果（使用正弦曲线模拟起伏）
            flow = int(18 * math.sin(x * 0.3 + y * 0.2 + random.random()))
            green = max(10, min(130, color[1] + flow))  # 只调整绿色通道
            
            # 边缘处理（底部稍暗，顶部稍亮，模拟自然流动）
            alpha = color[3]
            if y < size * 0.3:  # 顶部区域
                green = min(130, green + 15)
            elif y > size * 0.7:  # 底部区域
                green = max(10, green - 15)
            
            # 绘制像素（确保纯红色调）
            draw.point((x, y), (255, green, 0, alpha))
    
    # 添加岩浆火焰纹理（亮斑）
    for _ in range(15):
        cx, cy = random.randint(2, size-3), random.randint(2, size-3)
        radius = random.randint(2, 4)
        
        for x in range(cx-radius, cx+radius+1):
            for y in range(cy-radius, cy+radius+1):
                if 0 <= x < size and 0 <= y < size:
                    dist = math.sqrt((x-cx)**2 + (y-cy)** 2)
                    if dist <= radius:
                        # 亮斑使用高亮红色
                        brightness = int(120 - (dist/radius)*50)
                        draw.point((x, y), (255, brightness, 0, random.randint(220, 250)))
    
    # 添加岩浆气泡（暗色空洞）
    for _ in range(6):
        bx, by = random.randint(3, size-4), random.randint(3, size-4)
        bubble_size = random.randint(1, 2)
        for dx in range(bubble_size):
            for dy in range(bubble_size):
                nx, ny = bx+dx, by+dy
                if 0 <= nx < size and 0 <= ny < size:
                    # 气泡使用暗红色
                    draw.point((nx, ny), (255, 20, 0, random.randint(150, 180)))
    
    # 保存图片
    image.save(output_path)
    print(f"岩浆方块已生成：{output_path} (32x32像素，无边框)")

if __name__ == "__main__":
    generate_lava_block()
