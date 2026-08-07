from PIL import Image, ImageDraw
import random

def generate_long_blade_wooden_sword(output_path="长刀刃木剑.png"):
    # 基础设置：32x32像素，透明背景（刀刃占比提升至2/3）
    size = 32
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 木剑颜色体系（贴近真实木材质感，增强明暗对比）
    colors = {
        "blade_base": (190, 150, 110, 255),   # 刀刃基础木色
        "blade_grain": (160, 120, 80, 255),   # 刀刃木纹
        "blade_highlight": (230, 190, 150, 255), # 刀刃高光（增强反光）
        "blade_dark": (150, 110, 70, 255),    # 刀刃暗部
        "handle_main": (130, 90, 50, 255),    # 握柄主色
        "handle_dark": (100, 60, 20, 255),    # 握柄深色纹理
        "guard": (110, 70, 30, 255)           # 护手（连接刀刃与握柄）
    }
    
    # 1. 绘制加长刀刃（占比提升：纵向22像素，约占总高度2/3）
    blade_total_height = 22  # 刀刃总长度（增加约40%）
    for y in range(0, blade_total_height):
        # 刀刃宽度变化：顶部极窄，逐渐加宽至底部
        if y <= 5:
            width = 1 + int(y / 5 * 2)  # 顶部0-5像素：1→3像素
        elif y <= 15:
            width = 3 + int((y - 5) / 10 * 1)  # 中部5-15像素：3→4像素
        else:
            width = 4 + int((y - 15) / 7 * 1)  # 底部15-22像素：4→5像素
        
        half_width = width // 2
        center_x = 16  # 水平居中
        
        # 填充刀刃
        for x in range(center_x - half_width, center_x + half_width + 1):
            if 0 <= x < size and 0 <= y < size:
                # 左侧高光区，右侧暗部区，中间基础色
                if x == center_x - half_width:
                    draw.point((x, y), colors["blade_highlight"])
                elif x == center_x + half_width:
                    draw.point((x, y), colors["blade_dark"])
                else:
                    draw.point((x, y), colors["blade_base"])
    
    # 2. 绘制刀刃细节（纵向木纹+锋利边缘）
    # 纵向木纹（沿刀刃长度方向）
    for x_offset in [-1, 0, 1]:
        x = 16 + x_offset
        for y in range(3, blade_total_height - 2, random.choice([3, 4])):
            draw.point((x, y), colors["blade_grain"])
            # 木纹轻微分支
            if y > 8 and y < 18 and random.random() < 0.5:
                branch_dir = random.choice([-1, 1])
                draw.point((x + branch_dir, y), colors["blade_grain"])
    
    # 3. 刀刃反光条纹（增强锋利感）
    for y in range(2, blade_total_height - 3, 5):
        # 左侧高光条纹
        draw.point((15, y), colors["blade_highlight"])
        if y > 5:
            draw.point((15, y + 1), colors["blade_highlight"])
    
    # 4. 绘制护手（连接刀刃与握柄）
    guard_y = blade_total_height - 1  # 护手位置与刀刃底部衔接
    for y in range(guard_y, guard_y + 2):
        for x in range(13, 20):  # 护手宽度大于刀刃底部
            draw.point((x, y), colors["guard"])
            # 护手边缘加深
            if x == 13 or x == 19 or y == guard_y:
                draw.point((x, y), (90, 50, 10, 255))
    
    # 5. 绘制握柄（缩短以配合长刀刃）
    # 握柄长度调整为10像素（原13像素）
    for y in range(guard_y + 2, 32):
        for x in range(14, 19):  # 握柄宽度
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
    print(f"长刀刃木剑图片已生成：{output_path} (32x32像素，透明背景)")

if __name__ == "__main__":
    generate_long_blade_wooden_sword()
