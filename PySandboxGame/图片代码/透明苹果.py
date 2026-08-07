from PIL import Image, ImageDraw
import math

def generate_transparent_apple(output_path="透明苹果.png"):
    # 基础设置：32x32像素，RGBA模式确保背景透明
    size = 32
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))  # 初始全透明背景
    draw = ImageDraw.Draw(image)
    
    # 苹果颜色体系（卡通风格，色彩鲜明）
    apple_colors = {
        "body_main": (220, 0, 0, 255),    # 苹果主体红色（不透明）
        "body_light": (255, 50, 50, 255), # 主体亮部（增强立体感）
        "body_dark": (180, 0, 0, 255),    # 主体暗部
        "leaf_main": (0, 180, 0, 255),    # 叶子绿色
        "leaf_light": (50, 220, 50, 255), # 叶子亮部
        "stem": (100, 60, 20, 255),       # 果柄棕色
        "highlight": (255, 255, 255, 230) # 高光（半透明）
    }
    
    # 1. 绘制苹果主体（圆形，避免边缘生硬）
    apple_center = (size//2, size//2 + 2)  # 苹果中心（稍向下偏移，更自然）
    apple_radius = 12                      # 主体半径（适配32x32尺寸）
    
    for x in range(size):
        for y in range(size):
            # 计算到中心的距离
            dx = x - apple_center[0]
            dy = y - apple_center[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            # 在圆形范围内绘制苹果主体
            if distance <= apple_radius:
                # 顶部稍亮，底部稍暗，增强立体感
                brightness_factor = 1 - (dy / (apple_radius * 2))
                
                # 确定颜色（根据位置变化）
                if brightness_factor > 1.1:
                    color = apple_colors["body_light"]
                elif brightness_factor < 0.9:
                    color = apple_colors["body_dark"]
                else:
                    color = apple_colors["body_main"]
                
                # 边缘稍透明，避免生硬
                edge_factor = 1 - (distance / apple_radius)
                if edge_factor < 0.2:
                    # 边缘渐变透明
                    alpha = int(255 * (edge_factor / 0.2))
                    color = (color[0], color[1], color[2], alpha)
                
                draw.point((x, y), color)
    
    # 2. 绘制果柄
    # 果柄位置（苹果顶部中心偏左）
    stem_start = (apple_center[0] - 1, apple_center[1] - apple_radius)
    stem_end = (apple_center[0] - 3, apple_center[1] - apple_radius - 4)
    
    # 绘制果柄线条
    for i in range(5):
        x = stem_start[0] - (i // 2)
        y = stem_start[1] - i
        if 0 <= x < size and 0 <= y < size:
            draw.point((x, y), apple_colors["stem"])
            # 果柄右侧添加亮边
            draw.point((x + 1, y), (130, 90, 50, 255))
    
    # 3. 绘制叶子
    # 叶子位置（果柄顶部）
    leaf_center = (stem_end[0] - 2, stem_end[1] - 1)
    
    for x in range(leaf_center[0] - 3, leaf_center[0] + 2):
        for y in range(leaf_center[1] - 2, leaf_center[1] + 3):
            # 叶子形状（简单椭圆）
            dx = x - leaf_center[0]
            dy = y - leaf_center[1]
            if (dx*dx)*2 + (dy*dy) <= 9:  # 横向椭圆
                # 叶子左侧亮部，右侧暗部
                if dx < -1:
                    draw.point((x, y), apple_colors["leaf_light"])
                else:
                    draw.point((x, y), apple_colors["leaf_main"])
    
    # 4. 添加高光（增强光泽感）
    # 高光位置（右上侧）
    highlight_center = (apple_center[0] + 4, apple_center[1] - 4)
    
    for x in range(highlight_center[0] - 3, highlight_center[0] + 2):
        for y in range(highlight_center[1] - 2, highlight_center[1] + 2):
            dx = x - highlight_center[0]
            dy = y - highlight_center[1]
            if dx*dx + dy*dy <= 4:  # 小圆形高光
                draw.point((x, y), apple_colors["highlight"])
    
    # 保存图片
    image.save(output_path)
    print(f"透明背景苹果已生成：{output_path} (32x32像素)")

if __name__ == "__main__":
    generate_transparent_apple()
