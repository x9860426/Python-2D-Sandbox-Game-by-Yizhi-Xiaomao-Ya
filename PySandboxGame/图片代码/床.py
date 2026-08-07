from PIL import Image, ImageDraw
import os

# 设置输出目录
output_dir = r"d:\py\py文件\2d游戏\图片代码"

# 定义颜色
BED_WOOD = (139, 69, 19, 255)        # 床腿和床架的棕色
BED_WOOD_DARK = (101, 67, 33, 255)    # 深色木纹
BED_BLANKET = (205, 92, 92, 255)      # 床罩红色
BED_BLANKET_LIGHT = (220, 120, 120, 255)  # 浅色床罩
PILLOW = (255, 250, 240, 255)         # 枕头颜色
PILLOW_DETAIL = (245, 245, 245, 255)  # 枕头细节

# 创建左右两半的32x32床图像
def create_bed_halves():
    # 左半部分
    left_bed = Image.new('RGBA', (32, 32), color=(0, 0, 0, 0))
    left_draw = ImageDraw.Draw(left_bed)
    
    # 绘制左半部分床腿
    left_draw.rectangle([(2, 22), (4, 31)], fill=BED_WOOD)
    left_draw.rectangle([(10, 22), (12, 31)], fill=BED_WOOD)
    
    # 绘制床架
    left_draw.rectangle([(2, 22), (31, 24)], fill=BED_WOOD)
    
    # 添加床头板
    left_draw.rectangle([(2, 8), (4, 22)], fill=BED_WOOD)
    left_draw.rectangle([(10, 8), (12, 22)], fill=BED_WOOD)
    left_draw.rectangle([(2, 8), (12, 10)], fill=BED_WOOD)
    
    # 绘制枕头（只在左半部分，放在床头板后面）
    left_draw.rectangle([(14, 10), (31, 18)], fill=PILLOW)
    left_draw.rectangle([(16, 12), (29, 16)], fill=PILLOW_DETAIL)
    
    # 绘制床罩
    left_draw.rectangle([(2, 18), (31, 22)], fill=BED_BLANKET)
    left_draw.line([(2, 20), (31, 20)], fill=BED_BLANKET_LIGHT, width=1)
    
    # 添加木纹细节
    for x in range(2, 32, 4):
        left_draw.line([(x, 22), (x, 24)], fill=BED_WOOD_DARK, width=1)
    
    # 右半部分
    right_bed = Image.new('RGBA', (32, 32), color=(0, 0, 0, 0))
    right_draw = ImageDraw.Draw(right_bed)
    
    # 绘制右半部分床腿
    right_draw.rectangle([(20, 22), (22, 31)], fill=BED_WOOD)
    right_draw.rectangle([(28, 22), (30, 31)], fill=BED_WOOD)
    
    # 绘制床架
    right_draw.rectangle([(0, 22), (30, 24)], fill=BED_WOOD)
    
    # 绘制床罩
    right_draw.rectangle([(0, 18), (30, 22)], fill=BED_BLANKET)
    right_draw.line([(0, 20), (30, 20)], fill=BED_BLANKET_LIGHT, width=1)
    
    # 添加床罩装饰线条
    for y in range(18, 22, 1):
        for x in range(4, 30, 5):
            right_draw.point((x, y), fill=BED_BLANKET_LIGHT)
    
    # 添加木纹细节
    for x in range(0, 30, 4):
        right_draw.line([(x, 22), (x, 24)], fill=BED_WOOD_DARK, width=1)
    
    # 保存左右半部分
    left_path = os.path.join(output_dir, "床_左.png")
    right_path = os.path.join(output_dir, "床_右.png")
    left_bed.save(left_path)
    right_bed.save(right_path)
    
    print(f"床的左半部分已保存至: {left_path}")
    print(f"床的右半部分已保存至: {right_path}")
    
    return left_bed, right_bed

# 创建64x32的完整床图像
def create_full_bed(left_bed, right_bed):
    full_bed = Image.new('RGBA', (64, 32), color=(0, 0, 0, 0))
    # 粘贴左半部分到0,0位置
    full_bed.paste(left_bed, (0, 0))
    # 粘贴右半部分到32,0位置
    full_bed.paste(right_bed, (32, 0))
    
    # 保存完整床图像
    full_path = os.path.join(output_dir, "床_完整.png")
    full_bed.save(full_path)
    print(f"完整床图像已保存至: {full_path}")
    
    return full_bed

# 创建64x64的放大床图像（合并版本）
def create_merged_bed(full_bed):
    # 创建64x64图像
    merged_bed = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(merged_bed)
    
    # 绘制放大版床腿
    draw.rectangle([(5, 45), (8, 63)], fill=BED_WOOD)
    draw.rectangle([(18, 45), (22, 63)], fill=BED_WOOD)
    draw.rectangle([(42, 45), (46, 63)], fill=BED_WOOD)
    draw.rectangle([(55, 45), (58, 63)], fill=BED_WOOD)
    
    # 绘制床架
    draw.rectangle([(5, 45), (58, 49)], fill=BED_WOOD)
    
    # 添加床头板
    draw.rectangle([(5, 15), (8, 45)], fill=BED_WOOD)
    draw.rectangle([(18, 15), (22, 45)], fill=BED_WOOD)
    draw.rectangle([(5, 15), (22, 19)], fill=BED_WOOD)
    
    # 绘制枕头（放在床头板后面）
    draw.rectangle([(26, 20), (63, 36)], fill=PILLOW)
    draw.rectangle([(30, 24), (59, 32)], fill=PILLOW_DETAIL)
    
    # 绘制床罩
    draw.rectangle([(5, 36), (58, 45)], fill=BED_BLANKET)
    draw.line([(5, 40), (58, 40)], fill=BED_BLANKET_LIGHT, width=2)
    
    # 添加床罩装饰
    for y in range(36, 45, 2):
        for x in range(10, 58, 8):
            draw.point((x, y), fill=BED_BLANKET_LIGHT)
    
    # 添加木纹细节
    for x in range(5, 58, 8):
        draw.line([(x, 45), (x, 49)], fill=BED_WOOD_DARK, width=1)
    
    # 保存合并的64x64床图像
    merged_path = os.path.join(output_dir, "床_合并_64x64.png")
    merged_bed.save(merged_path)
    print(f"合并的64x64床图像已保存至: {merged_path}")

# 主函数
if __name__ == "__main__":
    # 创建左右两半
    left_bed, right_bed = create_bed_halves()
    # 创建完整的64x32床
    full_bed = create_full_bed(left_bed, right_bed)
    # 创建64x64的合并床
    create_merged_bed(full_bed)
    
    print("所有床图像已成功生成！")

# 不再自动显示图像，如需查看请手动打开文件
# left_bed.show()
# right_bed.show()
# full_bed.show()