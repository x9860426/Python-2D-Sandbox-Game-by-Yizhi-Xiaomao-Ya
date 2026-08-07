from PIL import Image, ImageDraw
import math

# 创建一个32x32的RGBA图像
image = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# 玻璃主体颜色
base_color = (220, 240, 255)  # 浅蓝色的玻璃
edge_color = (100, 255, 255)   # 浅青色边缘

# 计算中心点
center_x, center_y = 15.5, 15.5  # 32x32图像的中心点(从0开始计数)

# 玻璃效果参数
max_alpha = 180  # 最大透明度（中心）
min_alpha = 80   # 最小透明度（边缘）

# 绘制渐变玻璃效果
for x in range(32):
    for y in range(32):
        # 检查是否为边缘1圈1像素
        if x == 0 or x == 31 or y == 0 or y == 31:
            # 边缘1像素设置为浅青色，使用稍高的透明度
            draw.point((x, y), fill=(edge_color[0], edge_color[1], edge_color[2], 220))
            continue
        
        # 计算当前像素到中心的距离
        distance = math.sqrt((x - center_x) **2 + (y - center_y)** 2)
        
        # 最大距离（从中心到角落）
        max_distance = math.sqrt(center_x** 2 + center_y** 2)
        
        # 计算透明度渐变：边缘透明，中心半透明
        # 使用平滑的曲线而不是线性渐变
        alpha_factor = 1 - (distance / max_distance)** 0.7
        alpha = int(min_alpha + (max_alpha - min_alpha) * alpha_factor)
        
        # 确保alpha在0-255范围内
        alpha = max(0, min(255, alpha))
        
        # 修复可能存在的瑕疵，确保过渡平滑
        # 为靠近边缘的第二层像素添加轻微调整
        if (x == 1 or x == 30 or y == 1 or y == 30):
            # 稍微降低透明度，使过渡更自然
            alpha = int(alpha * 0.9)
        
        # 为边缘像素添加更亮的高光效果
        if distance > max_distance * 0.8:
            highlight_factor = (distance / max_distance - 0.8) * 5
            color = (
                min(255, int(base_color[0] + highlight_factor * 35)),
                min(255, int(base_color[1] + highlight_factor * 35)),
                min(255, int(base_color[2] + highlight_factor * 35))
            )
        else:
            color = base_color
        
        # 绘制像素
        draw.point((x, y), fill=(color[0], color[1], color[2], alpha))

# 添加一点反光效果
# 左上角到右下角的对角线高光
for i in range(8):
    if 4+i < 32 and 4+i < 32:
        highlight_alpha = 60 - i * 6
        draw.point((4+i, 4+i), fill=(255, 255, 255, highlight_alpha))

# 保存图像 - 使用原始字符串避免转义字符问题
output_path = r"D:\py\py文件\2d游戏\1\图片\玻璃.png"
# 确保目录存在
import os
dir_path = os.path.dirname(output_path)
print(f"正在确保目录存在: {dir_path}")
os.makedirs(dir_path, exist_ok=True)
print("目录已准备就绪")

# 保存图像
print("正在保存图像...")
image.save(output_path, "PNG")
print(f"成功! 玻璃图片已生成并保存到: {output_path}")

# 验证文件是否存在
if os.path.exists(output_path):
    print(f"验证成功: 文件已创建，大小为 {os.path.getsize(output_path)} 字节")
else:
    print("错误: 文件未创建")

# 显示图像（可选）
# image.show()