from PIL import Image, ImageDraw
import random
import math

# 创建32x32透明图像
width, height = 32, 32
image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# 定义钻石的颜色
class DiamondColors:
    # 主要钻石色（浅蓝色）
    PRIMARY = (173, 216, 230, 255)
    # 亮部
    LIGHT = (224, 255, 255, 255)
    # 暗部
    DARK = (135, 206, 235, 255)
    # 深暗部
    DEEPER = (70, 130, 180, 255)
    # 高光
    HIGHLIGHT = (255, 255, 255, 255)

# 生成钻石形状的顶点（八面体形状）
def generate_diamond_shape(center_x, center_y):
    points = []
    # 钻石通常是八面体形状，这里使用8个顶点
    num_points = 8
    
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        # 钻石的水平和垂直直径略有不同，呈现菱形效果
        if i % 2 == 0:
            # 对角线方向
            radius = random.uniform(10, 12)
        else:
            # 边的方向
            radius = random.uniform(8, 10)
        
        variation = random.uniform(-0.1, 0.1)  # 轻微变化使形状更自然
        final_radius = radius * (1 + variation)
        
        x = center_x + final_radius * math.cos(angle)
        y = center_y + final_radius * math.sin(angle)
        points.append((x, y))
    
    return points

# 绘制基础形状
def draw_base_shape(draw, points, color):
    draw.polygon(points, fill=color)

# 添加晶体结构的线条细节
def add_crystal_details(draw, center_x, center_y):
    # 添加钻石的晶体质感线条
    for _ in range(8):
        # 随机起始角度
        angle = random.uniform(0, 2 * math.pi)
        
        # 线条长度和宽度
        length = random.uniform(8, 16)
        thickness = random.randint(1, 2)
        
        # 计算线条的起点和终点
        start_x = center_x + random.uniform(-4, 4)
        start_y = center_y + random.uniform(-4, 4)
        end_x = start_x + length * math.cos(angle)
        end_y = start_y + length * math.sin(angle)
        
        # 50%概率使用亮部，50%概率使用暗部
        if random.random() < 0.5:
            color = DiamondColors.LIGHT
        else:
            color = DiamondColors.DARK
        
        # 绘制线条
        draw.line([(start_x, start_y), (end_x, end_y)], fill=color, width=thickness)

# 添加高光效果
def add_highlights(draw, points):
    # 钻石的高光通常在边缘和尖角处
    highlight_count = 4
    
    # 选择几个顶点添加高光
    selected_points = random.sample(points, min(highlight_count, len(points)))
    
    for point in selected_points:
        x, y = point
        # 高光大小
        size = random.uniform(2, 4)
        
        # 绘制高光椭圆
        draw.ellipse([
            (x - size/2, y - size/2),
            (x + size/2, y + size/2)
        ], fill=DiamondColors.HIGHLIGHT)
    
    # 添加一些内部高光点
    for _ in range(3):
        # 在形状内部随机位置
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(3, 8)
        
        x = 16 + distance * math.cos(angle)
        y = 16 + distance * math.sin(angle)
        size = random.uniform(1, 2)
        
        draw.ellipse([
            (x - size/2, y - size/2),
            (x + size/2, y + size/2)
        ], fill=DiamondColors.HIGHLIGHT)

# 添加钻石特有的光泽线
def add_diamond_shine(draw, center_x, center_y):
    # 钻石有强烈的方向性光泽
    for _ in range(6):
        # 随机方向
        shine_angle = random.uniform(0, 2 * math.pi)
        
        # 光泽线的长度和位置
        start_dist = random.uniform(0, 6)
        end_dist = random.uniform(12, 18)
        
        start_x = center_x + start_dist * math.cos(shine_angle)
        start_y = center_y + start_dist * math.sin(shine_angle)
        end_x = center_x + end_dist * math.cos(shine_angle)
        end_y = center_y + end_dist * math.sin(shine_angle)
        
        # 绘制半透明的光泽线
        # 创建临时图像用于半透明效果
        temp_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_image)
        
        # 半透明高光色
        semi_transparent_highlight = (255, 255, 255, 128)
        
        # 在临时图像上绘制线条
        temp_draw.line([(start_x, start_y), (end_x, end_y)], 
                      fill=semi_transparent_highlight, 
                      width=1)
        
        # 将临时图像合并到主图像
        image.paste(temp_image, (0, 0), temp_image)

# 生成钻石形状
center_x, center_y = width // 2, height // 2
diamond_shape = generate_diamond_shape(center_x, center_y)

# 绘制基础形状（使用主要钻石色）
draw_base_shape(draw, diamond_shape, DiamondColors.PRIMARY)

# 添加晶体结构细节
add_crystal_details(draw, center_x, center_y)

# 添加钻石特有的光泽
add_diamond_shine(draw, center_x, center_y)

# 添加高光效果
add_highlights(draw, diamond_shape)

# 保存图像为透明底PNG
image.save("D:\\py\\py文件\\2d游戏\\图片代码\\钻石.png", "PNG")
print("钻石图像已生成并保存为PNG格式（透明背景）")