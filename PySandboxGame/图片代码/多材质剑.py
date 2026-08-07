from PIL import Image, ImageDraw
import random

def generate_sword_by_material(material, output_path=None):
    """
    生成不同材质的剑，保持相同的刀柄设计
    material: 材质类型，可选 'stone', 'copper', 'iron', 'gold', 'diamond'
    """
    # 默认输出路径
    if output_path is None:
        output_path = f"{material}_sword.png"
    
    # 基础设置：32x32像素，透明背景
    size = 32
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 材质颜色配置（保持刀柄颜色一致）
    material_colors = {
        'stone': {          # 石剑
            'blade_base': (160, 160, 160, 255),
            'blade_grain': (130, 130, 130, 255),
            'blade_highlight': (190, 190, 190, 255),
            'blade_dark': (100, 100, 100, 255)
        },
        'copper': {         # 铜剑
            'blade_base': (184, 115, 51, 255),
            'blade_grain': (164, 95, 31, 255),
            'blade_highlight': (204, 135, 71, 255),
            'blade_dark': (154, 85, 21, 255)
        },
        'iron': {           # 铁剑
            'blade_base': (200, 200, 200, 255),
            'blade_grain': (170, 170, 170, 255),
            'blade_highlight': (230, 230, 230, 255),
            'blade_dark': (140, 140, 140, 255)
        },
        'gold': {           # 金剑
            'blade_base': (255, 215, 0, 255),
            'blade_grain': (235, 195, 0, 255),
            'blade_highlight': (255, 235, 100, 255),
            'blade_dark': (215, 175, 0, 255)
        },
        'diamond': {        # 钻石剑
            'blade_base': (175, 238, 238, 255),
            'blade_grain': (145, 208, 208, 255),
            'blade_highlight': (224, 255, 255, 255),
            'blade_dark': (127, 204, 204, 255)
        }
    }
    
    # 统一的刀柄颜色（保持不变）
    handle_colors = {
        "handle_main": (130, 90, 50, 255),
        "handle_dark": (100, 60, 20, 255),
        "guard": (110, 70, 30, 255),
        "guard_dark": (90, 50, 10, 255)
    }
    
    # 获取当前材质的颜色
    colors = {** material_colors[material], **handle_colors}
    
    # 1. 绘制加长刀刃（统一长度）
    blade_total_height = 22
    for y in range(0, blade_total_height):
        # 刀刃宽度变化规律（所有材质保持一致）
        if y <= 5:
            width = 1 + int(y / 5 * 2)
        elif y <= 15:
            width = 3 + int((y - 5) / 10 * 1)
        else:
            width = 4 + int((y - 15) / 7 * 1)
        
        half_width = width // 2
        center_x = 16  # 水平居中
        
        # 填充刀刃
        for x in range(center_x - half_width, center_x + half_width + 1):
            if 0 <= x < size and 0 <= y < size:
                if x == center_x - half_width:
                    draw.point((x, y), colors["blade_highlight"])
                elif x == center_x + half_width:
                    draw.point((x, y), colors["blade_dark"])
                else:
                    draw.point((x, y), colors["blade_base"])
    
    # 2. 绘制刀刃细节（根据材质调整纹理）
    if material in ['stone']:
        # 石质纹理：更粗糙，随机分布
        for _ in range(15):
            x = random.randint(14, 18)
            y = random.randint(3, blade_total_height - 3)
            draw.point((x, y), colors["blade_dark"])
            if random.random() < 0.3:
                draw.point((x + random.choice([-1, 1]), y), colors["blade_dark"])
    elif material in ['copper', 'iron']:
        # 金属纹理：纵向条纹
        for x_offset in [-1, 0, 1]:
            x = 16 + x_offset
            for y in range(3, blade_total_height - 2, random.choice([3, 4])):
                draw.point((x, y), colors["blade_grain"])
    elif material == 'gold':
        # 黄金纹理：更少纹理，更多高光
        for x_offset in [0]:
            x = 16 + x_offset
            for y in range(5, blade_total_height - 2, 5):
                draw.point((x, y), colors["blade_grain"])
        # 额外高光点
        for _ in range(8):
            x = random.randint(15, 17)
            y = random.randint(4, blade_total_height - 4)
            draw.point((x, y), colors["blade_highlight"])
    elif material == 'diamond':
        # 钻石纹理：锐利的反光线条
        for angle in [30, 150]:
            rad = angle * 3.14 / 180
            for i in range(10):
                x = int(16 + i * math.cos(rad))
                y = int(5 + i * math.sin(rad))
                if 0 <= x < size and 0 <= y < blade_total_height:
                    draw.point((x, y), colors["blade_highlight"])
    
    # 3. 刀刃反光条纹（所有材质通用）
    for y in range(2, blade_total_height - 3, 5):
        draw.point((15, y), colors["blade_highlight"])
        if y > 5:
            draw.point((15, y + 1), colors["blade_highlight"])
    
    # 4. 绘制护手（所有材质保持一致）
    guard_y = blade_total_height - 1
    for y in range(guard_y, guard_y + 2):
        for x in range(13, 20):
            draw.point((x, y), colors["guard"])
            if x == 13 or x == 19 or y == guard_y:
                draw.point((x, y), colors["guard_dark"])
    
    # 5. 绘制握柄（所有材质保持完全一致）
    for y in range(guard_y + 2, 32):
        for x in range(14, 19):
            draw.point((x, y), colors["handle_main"])
    
    # 握柄防滑纹理
    for y in range(guard_y + 4, 30, 2):
        for x in range(14, 19):
            draw.point((x, y), colors["handle_dark"])
    
    # 握柄边缘
    for y in range(guard_y + 2, 32):
        draw.point((14, y), colors["handle_dark"])
        draw.point((18, y), colors["handle_dark"])
    
    # 握柄底部
    for x in range(13, 20):
        draw.point((x, 31), colors["handle_dark"])
    
    # 保存图片
    image.save(output_path)
    print(f"{material}剑已生成：{output_path} (32x32像素，透明背景)")
    return image

# 生成所有材质的剑
if __name__ == "__main__":
    import math  # 钻石剑需要用到math库
    materials = ['stone', 'copper', 'iron', 'gold', 'diamond']
    for material in materials:
        generate_sword_by_material(material)
