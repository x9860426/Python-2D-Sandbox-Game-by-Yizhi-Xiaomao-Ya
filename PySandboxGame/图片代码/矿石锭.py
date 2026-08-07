from PIL import Image, ImageDraw
import random
import math

# 创建32x32透明图像
width, height = 32, 32
image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# 定义蓝色矿石锭的颜色
class BlueColors:
    # 主要蓝色
    PRIMARY = (0, 102, 204, 255)
    # 亮部
    LIGHT = (51, 153, 255, 255)
    # 暗部
    DARK = (0, 76, 153, 255)
    # 深暗部
    DEEPER = (0, 51, 102, 255)
    # 高光
    HIGHLIGHT = (102, 204, 255, 255)

# 生成不规则多边形作为矿石锭基础形状
def generate_ingot_shape(center_x, center_y):
    # 矿石锭通常是不规则的多边形
    points = []
    num_points = random.randint(6, 8)  # 6-8个顶点
    
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        # 基础半径和变化
        base_radius = random.uniform(10, 13)
        variation = random.uniform(-0.2, 0.2)
        radius = base_radius * (1 + variation)
        
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    
    return points

# 绘制基础形状
def draw_base_shape(draw, points, color):
    draw.polygon(points, fill=color)

# 添加不规则的凹凸纹理
def add_texture(draw, center_x, center_y, main_radius):
    # 添加一些小的凸起和凹陷
    for _ in range(15):
        # 随机位置
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0.5, 1.0) * main_radius
        
        x = center_x + distance * math.cos(angle)
        y = center_y + distance * math.sin(angle)
        
        # 随机大小和形状
        size = random.uniform(1, 3)
        is_highlight = random.random() < 0.3  # 30%概率是亮部
        
        if is_highlight:
            # 亮部纹理
            color = BlueColors.LIGHT
            if random.random() < 0.1:  # 10%概率是更强的高光
                color = BlueColors.HIGHLIGHT
        else:
            # 暗部纹理
            color = BlueColors.DARK
        
        # 绘制小椭圆作为纹理
        draw.ellipse([
            (x - size, y - size * 0.5),
            (x + size, y + size * 0.5)
        ], fill=color)

# 添加金属光泽效果
def add_metal_shine(draw, center_x, center_y, main_radius):
    # 金属通常有方向性的光泽
    for _ in range(5):
        # 选择一个方向
        shine_angle = random.uniform(0, 2 * math.pi)
        
        # 光泽的起始和结束点
        start_dist = random.uniform(0.3, 0.7) * main_radius
        end_dist = random.uniform(0.7, 1.1) * main_radius
        
        start_x = center_x + start_dist * math.cos(shine_angle)
        start_y = center_y + start_dist * math.sin(shine_angle)
        end_x = center_x + end_dist * math.cos(shine_angle)
        end_y = center_y + end_dist * math.sin(shine_angle)
        
        # 绘制光泽线
        draw.line(
            [(start_x, start_y), (end_x, end_y)],
            fill=BlueColors.HIGHLIGHT,
            width=1
        )

# 添加边缘细节
def add_edge_details(draw, points):
    # 为边缘添加一些变化
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        
        # 50%的概率在边缘添加细节
        if random.random() < 0.5:
            # 随机选择边缘上的点
            t = random.uniform(0.2, 0.8)
            mid_x = x1 + t * (x2 - x1)
            mid_y = y1 + t * (y2 - y1)
            
            # 随机偏移量
            offset = random.uniform(-1, 1)
            
            # 计算垂直于边缘的方向
            dx, dy = x2 - x1, y2 - y1
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                perp_x, perp_y = -dy/length, dx/length
                
                # 计算新点
                new_x = mid_x + perp_x * offset
                new_y = mid_y + perp_y * offset
                
                # 绘制边缘细节
                draw.line(
                    [(mid_x, mid_y), (new_x, new_y)],
                    fill=random.choice([BlueColors.DARK, BlueColors.DEEPER]),
                    width=1
                )

# 生成主要矿石锭形状
center_x, center_y = width // 2, height // 2
main_shape = generate_ingot_shape(center_x, center_y)

# 绘制基础形状（使用主要金色）
draw_base_shape(draw, main_shape, BlueColors.PRIMARY)

# 添加纹理细节
add_texture(draw, center_x, center_y, 13)  # 13是最大可能的半径

# 添加金属光泽
add_metal_shine(draw, center_x, center_y, 13)

# 添加边缘细节
add_edge_details(draw, main_shape)

# 添加几个亮点增强金属感
for _ in range(3):
    # 随机位置（偏向矿石锭的上方）
    angle = random.uniform(-math.pi/4, math.pi/4)
    distance = random.uniform(0.6, 0.9) * 13
    
    x = center_x + distance * math.cos(angle)
    y = center_y + distance * math.sin(angle)
    
    # 绘制小的高亮圆点
    draw.ellipse(
        [(x - 1, y - 1), (x + 1, y + 1)],
        fill=BlueColors.HIGHLIGHT
    )

# 保存图像为透明底PNG
image.save("d:\\py\\py文件\\2d游戏\\图片代码\\蓝矿石锭.png", "PNG")
print("蓝矿石锭图像已生成并保存为PNG格式（透明背景）")