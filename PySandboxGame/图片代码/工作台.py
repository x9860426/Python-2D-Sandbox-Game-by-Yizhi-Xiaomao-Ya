from PIL import Image, ImageDraw
import random
import os

# 创建32x32像素的图像，初始为透明背景
image_size = 32
img = Image.new('RGBA', (image_size, image_size), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 根据ASCII示意图重新设计工作台的简约风格颜色方案
# 采用更鲜明、更简约的色彩
PLANK_TOP = (180, 130, 80, 255)      # 顶部木板颜色
PLANK_TOP_DARK = (160, 110, 60, 255) # 顶部木板深色边缘
FRAME_SIDE = (130, 90, 50, 255)      # 框架侧面颜色
FRAME_DARK = (100, 60, 30, 255)      # 框架深色线条
PLANK_LINE = (120, 80, 40, 255)      # 木板线条
CRAFT_GRID = (100, 70, 30, 255)      # 合成格子线
METAL_SILVER = (170, 170, 170, 255)  # 金属色
METAL_HIGHLIGHT = (210, 210, 210, 255) # 金属高光

# 1. 绘制工作台顶部木板 - 对应ASCII中的 == 部分（扩大尺寸）
# 顶部第一层木板
top_plank1 = [(3, 5), (28, 11)]
draw.rectangle(top_plank1, fill=PLANK_TOP)
# 顶部第二层木板 (略微偏移，更有层次感)
top_plank2 = [(4, 11), (27, 17)]
draw.rectangle(top_plank2, fill=PLANK_TOP)

# 顶部木板的深色边缘线，增强立体感
draw.line([(3, 5), (28, 5)], fill=PLANK_TOP_DARK, width=1)  # 上边缘
draw.line([(3, 17), (27, 17)], fill=PLANK_TOP_DARK, width=1) # 下边缘
draw.line([(3, 5), (3, 17)], fill=PLANK_TOP_DARK, width=1)   # 左边缘
draw.line([(28, 5), (28, 11)], fill=PLANK_TOP_DARK, width=1) # 右边缘上层
draw.line([(27, 11), (27, 17)], fill=PLANK_TOP_DARK, width=1) # 右边缘下层

# 2. 绘制工作台框架 - 四个独立凳角（扩大并靠近边缘）
# 左上凳角
left_top_leg = [(5, 17), (8, 28)]
draw.rectangle(left_top_leg, fill=FRAME_SIDE)
# 右上凳角
right_top_leg = [(23, 17), (26, 28)]
draw.rectangle(right_top_leg, fill=FRAME_SIDE)
# 左下凳角
left_bottom_leg = [(9, 20), (12, 30)]
draw.rectangle(left_bottom_leg, fill=FRAME_SIDE)
# 右下凳角
right_bottom_leg = [(19, 20), (22, 30)]
draw.rectangle(right_bottom_leg, fill=FRAME_SIDE)

# 凳角的深色边缘线
# 左上凳角边缘
draw.line([(5, 17), (5, 28)], fill=FRAME_DARK, width=1)   # 左边缘
draw.line([(8, 17), (8, 28)], fill=FRAME_DARK, width=1)   # 右边缘
# 右上凳角边缘
draw.line([(23, 17), (23, 28)], fill=FRAME_DARK, width=1) # 左边缘
draw.line([(26, 17), (26, 28)], fill=FRAME_DARK, width=1) # 右边缘
# 左下凳角边缘
draw.line([(9, 20), (9, 30)], fill=FRAME_DARK, width=1)   # 左边缘
draw.line([(12, 20), (12, 30)], fill=FRAME_DARK, width=1) # 右边缘
# 右下凳角边缘
draw.line([(19, 20), (19, 30)], fill=FRAME_DARK, width=1) # 左边缘
draw.line([(22, 20), (22, 30)], fill=FRAME_DARK, width=1) # 右边缘

# 凳角底部线条
draw.line([(5, 28), (8, 28)], fill=FRAME_DARK, width=1)   # 左上凳角底部
draw.line([(23, 28), (26, 28)], fill=FRAME_DARK, width=1) # 右上凳角底部
draw.line([(9, 30), (12, 30)], fill=FRAME_DARK, width=1)   # 左下凳角底部
draw.line([(19, 30), (22, 30)], fill=FRAME_DARK, width=1) # 右下凳角底部

# 3. 添加凳角之间的细微连接 (可选，不连接脚尖)
# 顶部横向连接条（在凳角上方）
top_connect = [(8, 17), (23, 18)]
draw.rectangle(top_connect, fill=FRAME_SIDE)
draw.line([(8, 17), (23, 17)], fill=FRAME_DARK, width=1)

# 4. 添加工作台顶部的4格合成界面（扩大尺寸）
# 中心分割线
vertical_line = [(15, 6), (15, 16)]
horizontal_line = [(7, 11), (24, 11)]
draw.line(vertical_line, fill=CRAFT_GRID, width=1)
draw.line(horizontal_line, fill=CRAFT_GRID, width=1)

# 强化4个格子的边框
for i in range(2):
    for j in range(2):
        x1 = 7 + i * 8
        y1 = 6 + j * 5
        x2 = 15 + i * 8
        y2 = 11 + j * 5
        draw.rectangle([(x1, y1), (x2, y2)], outline=CRAFT_GRID, width=1)

# 5. 添加简单的木纹纹理（覆盖更大区域）
# 顶部木板的木纹线
for y in range(6, 17, 2):
    for _ in range(5):
        x = random.randint(4, 26)
        # 轻微的木纹点
        draw.point((x, y), fill=PLANK_LINE)

# 凳角上的木纹线
for leg in [left_top_leg, right_top_leg, left_bottom_leg, right_bottom_leg]:
    for y in range(leg[0][1] + 2, leg[1][1] - 2, 3):
        # 在凳角上添加木纹线
        length = random.randint(1, 2)
        draw.line([(leg[0][0], y), (leg[0][0] + length, y)], 
                 fill=FRAME_DARK, width=1)

# 6. 添加工具 - 更大更明显的设计
# 锤子 (放在左上格子)
# 锤子头部
hammer_head = [(8, 7), (14, 11)]
draw.rectangle(hammer_head, fill=METAL_SILVER)
# 锤子手柄
hammer_handle = [(10, 11), (12, 15)]
draw.rectangle(hammer_handle, fill=FRAME_SIDE)
# 锤子高光
draw.line([(8, 7), (14, 7)], fill=METAL_HIGHLIGHT, width=1)

# 锯子 (放在右上格子)
# 锯子手柄
锯_handle = [(18, 7), (23, 11)]
draw.rectangle(锯_handle, fill=FRAME_SIDE)
# 锯片
锯_blade = [(17, 8), (24, 13)]
draw.rectangle(锯_blade, fill=METAL_SILVER)
# 锯齿效果
for i in range(17, 24, 1):
    # 简化的锯齿
    draw.point((i, 13), fill=METAL_SILVER)
# 锯片高光
draw.line([(17, 8), (24, 8)], fill=METAL_HIGHLIGHT, width=1)

# 7. 添加简单的阴影效果（扩大范围）
# 顶部木板在框架上的阴影
for x in range(6, 25):
    draw.point((x, 17), fill=(FRAME_DARK[0], FRAME_DARK[1], FRAME_DARK[2], 120))

# 8. 增强工作台顶部的木板效果
# 在顶部木板之间添加分隔线
draw.line([(4, 11), (27, 11)], fill=PLANK_LINE, width=1)

# 9. 添加更多随机高光点增强质感
for _ in range(8):
    # 顶部木板的高光
    x = random.randint(5, 26)
    y = random.randint(7, 16)
    draw.point((x, y), fill=(200, 160, 110, 200))

# 10. 添加工作台底部的支撑细节
# 在凳角底部添加一些木纹点
for leg in [left_top_leg, right_top_leg]:
    draw.point((leg[0][0] + 1, leg[1][1]), fill=(80, 50, 20, 200))
for leg in [left_bottom_leg, right_bottom_leg]:
    draw.point((leg[0][0] + 1, leg[1][1]), fill=(80, 50, 20, 200))

# 保存图像
output_dir = r"d:\py\py文件\2d游戏\图片代码"
output_path = os.path.join(output_dir, "工作台.png")
img.save(output_path)

print(f"扩大尺寸并充满像素空间的工作台图像已保存至: {output_path}")

# 不再自动显示图像，如需查看请手动打开文件
# img.show()