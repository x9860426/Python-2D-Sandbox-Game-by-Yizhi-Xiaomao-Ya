from PIL import Image, ImageDraw
import random
import os
import math

def generate_light_wooden_plank_block(output_path="浅色木板方块.png"):
    """生成浅色方块风格木板，带自然木纹和1像素边框"""
    try:
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        size = 32  # 方块尺寸：32x32像素
        image = Image.new("RGB", (size, size))
        draw = ImageDraw.Draw(image)
        
        # 浅色木板颜色体系（温暖浅棕色系）
        wood_colors = {
            "base": (210, 180, 140),   # 基础浅棕色（主底色）
            "light_base": (230, 200, 160), # 更浅的棕色（底色亮部）
            "dark_grain": (160, 120, 80),  # 深一些的木纹色（主木纹）
            "light_grain": (190, 150, 110),# 浅木纹色（细木纹）
            "highlight": (240, 220, 190)   # 高光色（木材反光）
        }
        
        # 1. 填充木板基础底色（带轻微渐变）
        for x in range(1, size - 1):  # 预留1像素边框
            for y in range(1, size - 1):
                # 横向轻微渐变：顶部更亮，底部稍暗
                brightness_factor = 1 - (y / (size - 2)) * 0.1
                if random.random() < 0.65:
                    color = wood_colors["base"]
                else:
                    color = wood_colors["light_base"]
                
                # 应用亮度变化
                r = int(color[0] * brightness_factor)
                g = int(color[1] * brightness_factor)
                b = int(color[2] * brightness_factor)
                draw.point((x, y), (r, g, b))
        
        # 2. 绘制主要木纹（水平方向，模拟年轮）
        for y in range(3, size - 3, 5):  # 间距稍大，避免过于密集
            grain_width = random.randint(1, 2)
            for dy in range(grain_width):
                current_y = y + dy
                if 1 < current_y < size - 2:
                    for x in range(1, size - 1):
                        # 木纹自然弯曲
                        curve = int(2 * math.sin(x * 0.2 + random.random()))
                        if random.random() < 0.8:  # 适当断续
                            draw.point((x, current_y + curve), wood_colors["dark_grain"])
        
        # 3. 绘制细小木纹（纵向纹理，更稀疏）
        for _ in range(12):  # 数量比深色木板少，保持浅色清爽感
            start_x = random.randint(2, size - 3)
            length = random.randint(7, 18)
            start_y = random.randint(2, size - length - 2)
            
            for y in range(start_y, start_y + length):
                offset = int(1 * math.sin(y * 0.3))
                x = start_x + offset
                if 1 < x < size - 2:
                    if random.random() < 0.85:
                        draw.point((x, y), wood_colors["light_grain"])
                        # 少量分支
                        if random.random() < 0.08:
                            for dx in range(1, 3):
                                if x + dx < size - 2:
                                    draw.point((x + dx, y), wood_colors["light_grain"])
        
        # 4. 添加高光点（更明显，体现浅色木材反光）
        for _ in range(25):  # 高光点更多
            x = random.randint(2, size - 3)
            y = random.randint(2, size - 3)
            if random.random() < 0.35:
                draw.point((x, y), wood_colors["highlight"])
                if random.random() < 0.5 and x + 1 < size - 2:
                    draw.point((x + 1, y), wood_colors["light_base"])
        
        # 5. 绘制1像素边框（浅棕色边框，与浅色木材协调）
        border_color = (130, 100, 70)  # 比木纹色稍深
        for x in range(size):
            draw.point((x, 0), border_color)
            draw.point((x, size - 1), border_color)
        for y in range(1, size - 1):
            draw.point((0, y), border_color)
            draw.point((size - 1, y), border_color)
        
        # 保存图片
        image.save(output_path)
        print(f"浅色木板方块已生成：{os.path.abspath(output_path)} (32x32像素)")
        return True
        
    except Exception as e:
        print(f"生成失败: {str(e)}")
        return False

if __name__ == "__main__":
    generate_light_wooden_plank_block()
    # 自定义路径示例：generate_light_wooden_plank_block("资源包/浅色木板.png")
