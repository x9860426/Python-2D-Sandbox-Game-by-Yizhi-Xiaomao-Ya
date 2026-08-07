from PIL import Image, ImageDraw
import random
import math

# 创建32x32透明图像
image = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# 定义石子的颜色范围（更自然的灰色调）
def get_stone_color(type='normal'):
    if type == 'light':
        # 亮部颜色
        val = random.randint(130, 170)
        return (val, val, val, 255)
    elif type == 'dark':
        # 暗部颜色
        val = random.randint(50, 90)
        return (val, val, val, 255)
    else:
        # 普通颜色
        val = random.randint(80, 130)
        return (val, val, val, 255)

# 生成不规则多边形顶点
def generate_polygon_vertices(center_x, center_y, num_points, min_radius, max_radius, jaggedness=0.3):
    vertices = []
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        # 添加随机性使边缘更不规则
        radius = random.uniform(min_radius, max_radius)
        # 添加锯齿效果
        jitter = random.uniform(-jaggedness, jaggedness)
        adjusted_radius = radius * (1 + jitter)
        
        x = center_x + adjusted_radius * math.cos(angle)
        y = center_y + adjusted_radius * math.sin(angle)
        vertices.append((x, y))
    return vertices

# 绘制不规则多边形
def draw_irregular_shape(vertices, color):
    # 确保所有顶点在图像范围内
    valid_vertices = []
    for x, y in vertices:
        valid_x = max(0, min(31, x))
        valid_y = max(0, min(31, y))
        valid_vertices.append((valid_x, valid_y))
    
    # 只有当有足够的顶点时才绘制
    if len(valid_vertices) >= 3:
        draw.polygon(valid_vertices, fill=color)

# 绘制随机尖角
def draw_spike(base_x, base_y, direction, length, width, color):
    # 计算尖角的三个点
    tip_x = base_x + length * math.cos(direction)
    tip_y = base_y + length * math.sin(direction)
    
    # 计算两侧的点
    side_angle1 = direction + math.pi * 0.8
    side_angle2 = direction - math.pi * 0.8
    
    side1_x = base_x + width * math.cos(side_angle1)
    side1_y = base_y + width * math.sin(side_angle1)
    
    side2_x = base_x + width * math.cos(side_angle2)
    side2_y = base_y + width * math.sin(side_angle2)
    
    # 确保所有点在图像范围内
    points = [
        (max(0, min(31, tip_x)), max(0, min(31, tip_y))),
        (max(0, min(31, side1_x)), max(0, min(31, side1_y))),
        (max(0, min(31, side2_x)), max(0, min(31, side2_y)))
    ]
    
    draw.polygon(points, fill=color)

# 创建主要石头形状
center_x, center_y = 16, 16  # 固定中心点

# 主要形状：使用不规则多边形
main_points = random.randint(5, 7)  # 5-7个顶点
main_vertices = generate_polygon_vertices(center_x, center_y, main_points, 8, 14, 0.2)
main_color = get_stone_color()
draw_irregular_shape(main_vertices, main_color)

# 添加亮部细节（在主要形状上添加一些亮色区域）
for _ in range(2):
    light_points = random.randint(3, 4)
    # 亮部区域稍微小一些
    light_vertices = generate_polygon_vertices(center_x, center_y, light_points, 5, 10, 0.3)
    light_color = get_stone_color('light')
    draw_irregular_shape(light_vertices, light_color)

# 添加几个尖角
for _ in range(3):
    # 选择主要形状的一个顶点附近作为尖角的起点
    vertex_idx = random.randint(0, len(main_vertices) - 1)
    base_x, base_y = main_vertices[vertex_idx]
    
    # 计算从中心到顶点的方向
    direction = math.atan2(base_y - center_y, base_x - center_x)
    
    # 随机调整方向
    direction += random.uniform(-0.3, 0.3)
    
    # 绘制尖角
    length = random.randint(4, 8)
    width = random.randint(2, 3)
    spike_color = get_stone_color(random.choice(['normal', 'light']))
    draw_spike(base_x, base_y, direction, length, width, spike_color)

# 添加一些小的凹凸细节
for _ in range(4):
    detail_points = random.randint(3, 4)
    # 使用安全的范围值
    detail_center_x = random.randint(8, 24)
    detail_center_y = random.randint(8, 24)
    detail_vertices = generate_polygon_vertices(detail_center_x, detail_center_y, detail_points, 2, 4, 0.4)
    detail_color = get_stone_color(random.choice(['normal', 'dark']))
    draw_irregular_shape(detail_vertices, detail_color)

# 添加裂缝效果
for _ in range(2):
    # 使用安全的范围值
    start_x = random.randint(6, 26)
    start_y = random.randint(6, 26)
    
    direction = random.uniform(0, 2 * math.pi)
    length = random.randint(6, 12)
    
    end_x = start_x + length * math.cos(direction)
    end_y = start_y + length * math.sin(direction)
    
    # 确保终点在图像范围内
    end_x = max(0, min(31, end_x))
    end_y = max(0, min(31, end_y))
    
    # 绘制细裂缝
    crack_color = get_stone_color('dark')
    draw.line([(start_x, start_y), (end_x, end_y)], fill=crack_color, width=1)

# 添加高光点
for _ in range(3):
    # 使用安全的范围值
    highlight_x = random.randint(8, 24)
    highlight_y = random.randint(8, 24)
    highlight_radius = 1
    draw.ellipse([(highlight_x - highlight_radius, highlight_y - highlight_radius),
                  (highlight_x + highlight_radius, highlight_y + highlight_radius)],
                 fill=(200, 200, 200, 255))

# 保存图像到正确路径
image.save("d:\\py\\py文件\\2d游戏\\图片代码\\石子.png", "PNG")
print("美观的石子图像已生成并保存为PNG格式（透明背景）")