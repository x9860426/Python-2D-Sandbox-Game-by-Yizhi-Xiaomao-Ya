from PIL import Image, ImageDraw
import random
import math

def generate_lava_style_water(output_path="水.png"):
    # 尺寸设置
    size = 32
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 水的颜色体系（蓝色调，借鉴岩浆的明暗对比风格）
    water_colors = [
        (0, 80, 255, 210),    # 深蓝（基础色）
        (0, 110, 255, 220),   # 亮蓝
        (0, 50, 255, 200),    # 暗蓝
        (0, 140, 255, 230),   # 高亮蓝（水花亮斑）
        (0, 30, 255, 190)     # 深暗蓝
    ]
    
    # 生成基础纹理（借鉴岩浆的流动模式）
    for x in range(size):
        for y in range(size):
            # 选择基础蓝色
            color = random.choice(water_colors)
            
            # 保持颜色连贯性，模拟流动感（与岩浆相同逻辑）
            if random.random() < 0.65:
                if x > 0:
                    left_color = image.getpixel((x-1, y))
                    # 固定蓝色通道为255，调整绿色通道控制深浅
                    color = (
                        0,  # 红色通道固定为0
                        max(30, min(150, (color[1] + left_color[1]) // 2)),  # 绿色通道控制明暗
                        255,  # 蓝色通道固定为最大值
                        color[3]
                    )
                elif y > 0:
                    top_color = image.getpixel((x, y-1))
                    color = (
                        0,
                        max(30, min(150, (color[1] + top_color[1]) // 2)),
                        255,
                        color[3]
                    )
            
            # 流动效果（使用岩浆同款正弦曲线算法）
            flow = int(18 * math.sin(x * 0.3 + y * 0.2 + random.random()))
            green = max(30, min(150, color[1] + flow))  # 调整绿色通道控制蓝色深浅
            
            # 上下明暗分布（借鉴岩浆的顶部亮底部暗）
            if y < size * 0.3:  # 顶部区域更亮
                green = min(150, green + 15)
            elif y > size * 0.7:  # 底部区域稍暗
                green = max(30, green - 15)
            
            # 绘制像素
            draw.point((x, y), (0, green, 255, color[3]))
    
    # 添加水花亮斑（对应岩浆的火焰亮斑）
    for _ in range(15):
        cx, cy = random.randint(2, size-3), random.randint(2, size-3)
        radius = random.randint(2, 4)
        
        for x in range(cx-radius, cx+radius+1):
            for y in range(cy-radius, cy+radius+1):
                if 0 <= x < size and 0 <= y < size:
                    dist = math.sqrt((x-cx)**2 + (y-cy)** 2)
                    if dist <= radius:
                        # 亮斑使用高亮蓝色（对应岩浆的高亮红色）
                        brightness = int(140 - (dist/radius)*50)
                        draw.point((x, y), (0, brightness, 255, random.randint(220, 250)))
    
    # 添加水流气泡（对应岩浆的气泡）
    for _ in range(6):
        bx, by = random.randint(3, size-4), random.randint(3, size-4)
        bubble_size = random.randint(1, 2)
        for dx in range(bubble_size):
            for dy in range(bubble_size):
                nx, ny = bx+dx, by+dy
                if 0 <= nx < size and 0 <= ny < size:
                    # 气泡使用高亮蓝色（水的气泡比岩浆更亮）
                    draw.point((nx, ny), (0, 160, 255, random.randint(200, 230)))
    
    # 保存图片
    image.save(output_path)
    print(f"岩浆风格水方块已生成：{output_path} (32x32像素，无边框)")

if __name__ == "__main__":
    generate_lava_style_water()
