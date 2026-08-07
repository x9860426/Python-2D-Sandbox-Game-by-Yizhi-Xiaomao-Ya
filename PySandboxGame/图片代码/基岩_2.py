from PIL import Image, ImageDraw
import random
import os

def generate_bedrock_block(output_path="基岩.png"):
    """由土块代码修改而来的基岩生成函数"""
    try:
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        size = 32
        image = Image.new("RGB", (size, size))
        draw = ImageDraw.Draw(image)
        
        # 基岩颜色体系（深灰色调，替代土块的棕色系）
        bedrock_colors = {
            "base": (40, 40, 40),    # 基础深灰色（替代土块基础棕色）
            "light": (60, 60, 60),   # 浅灰色（替代土块浅棕色）
            "dark": (20, 20, 20),    # 近黑色（替代土块深棕色）
            "crack": (70, 70, 70)    # 裂缝亮色（替代土块沙质色）
        }
        
        # 1. 填充基础底色（将土块的棕色替换为基岩的深灰色）
        for x in range(1, size - 1):
            for y in range(1, size - 1):
                if random.random() < 0.6:
                    color = bedrock_colors["base"]
                elif random.random() < 0.5:
                    color = bedrock_colors["light"]
                else:
                    color = bedrock_colors["dark"]
                draw.point((x, y), color)
        
        # 2. 添加基岩纹理（将土块的色块改为基岩的裂缝结构）
        for _ in range(5, 8):
            start_x = random.randint(3, size - 8)
            start_y = random.randint(3, size - 8)
            width = random.randint(5, 9)
            height = random.randint(5, 9)
            
            for x in range(start_x, start_x + width):
                for y in range(start_y, start_y + height):
                    if 1 < x < size - 2 and 1 < y < size - 2:
                        # 提高填充概率，让裂缝更密集（修改自土块的0.7）
                        if random.random() < 0.85:
                            color = random.choice([
                                bedrock_colors["dark"],
                                bedrock_colors["crack"],
                                bedrock_colors["base"]
                            ])
                            draw.point((x, y), color)
        
        # 3. 基岩的坚硬颗粒（替代土块的沙粒）
        for _ in range(40, 50):  # 增加颗粒数量
            x = random.randint(2, size - 3)
            y = random.randint(2, size - 3)
            if random.random() < 0.5:  # 提高出现概率
                grain_size = random.randint(1, 2)
                for dx in range(grain_size):
                    for dy in range(grain_size):
                        nx, ny = x + dx, y + dy
                        if 2 <= nx < size - 3 and 2 <= ny < size - 3:
                            # 随机深色或浅色颗粒，体现岩石质感
                            color = random.choice([bedrock_colors["dark"], bedrock_colors["crack"]])
                            draw.point((nx, ny), color)
        
        # 4. 绘制更粗的边框（基岩特性，修改自土块的1像素边框）
        border_color = (10, 10, 10)
        # 边框厚度改为2像素
        for t in range(2):
            for x in range(size):
                draw.point((x, t), border_color)
                draw.point((x, size - 1 - t), border_color)
            for y in range(2, size - 2):
                draw.point((t, y), border_color)
                draw.point((size - 1 - t, y), border_color)
        
        # 保存图片
        image.save(output_path)
        print(f"✅ 基岩生成成功！已保存至: {os.path.abspath(output_path)}")
        return True
        
    except Exception as e:
        print(f"❌ 生成失败: {str(e)}")
        return False

if __name__ == "__main__":
    generate_bedrock_block()
    # 自定义路径示例：generate_bedrock_block("资源包/基岩.png")
