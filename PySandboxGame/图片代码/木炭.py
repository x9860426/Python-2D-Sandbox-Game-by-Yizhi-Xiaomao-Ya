from PIL import Image, ImageDraw
import os

# 设置输出目录
output_dir = r"D:\py\py文件\2d游戏\图片代码"

# 定义颜色
CHARCOAL_DARK = (20, 20, 20, 255)    # 深黑色
CHARCOAL_MEDIUM = (40, 40, 40, 255)  # 中黑色
CHARCOAL_LIGHT = (60, 60, 60, 255)   # 浅黑色
HIGHLIGHT = (80, 80, 80, 255)        # 高光色

# 创建32x32像素的透明背景图像
def create_charcoal():
    # 创建透明背景
    charcoal = Image.new('RGBA', (32, 32), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(charcoal)
    
    # 绘制主要木炭块
    # 主体形状
    draw.ellipse([(8, 8), (24, 24)], fill=CHARCOAL_DARK)
    
    # 添加不规则形状变化
    draw.ellipse([(10, 6), (22, 22)], fill=CHARCOAL_MEDIUM)
    draw.ellipse([(7, 10), (25, 26)], fill=CHARCOAL_DARK)
    
    # 添加木炭裂纹和纹理
    # 主要裂纹
    draw.line([(10, 10), (22, 22)], fill=CHARCOAL_LIGHT, width=1)
    draw.line([(12, 18), (20, 10)], fill=CHARCOAL_LIGHT, width=1)
    draw.line([(16, 10), (16, 22)], fill=CHARCOAL_LIGHT, width=1)
    
    # 次要裂纹
    draw.line([(9, 14), (15, 10)], fill=HIGHLIGHT, width=1)
    draw.line([(17, 16), (23, 12)], fill=HIGHLIGHT, width=1)
    draw.line([(13, 20), (19, 24)], fill=HIGHLIGHT, width=1)
    
    # 添加一些小点和纹理细节
    for x, y in [(11, 11), (14, 17), (18, 13), (21, 19), (10, 20), (22, 11)]:
        draw.point((x, y), fill=HIGHLIGHT)
    
    # 添加边缘不规则效果
    draw.ellipse([(14, 7), (18, 9)], fill=CHARCOAL_LIGHT)
    draw.ellipse([(21, 16), (23, 18)], fill=CHARCOAL_LIGHT)
    draw.ellipse([(9, 20), (11, 22)], fill=CHARCOAL_LIGHT)
    
    # 添加一些空洞效果
    draw.ellipse([(15, 15), (17, 17)], fill=CHARCOAL_MEDIUM)
    draw.ellipse([(12, 12), (14, 14)], fill=CHARCOAL_MEDIUM)
    
    # 保存图像
    output_path = os.path.join(output_dir, "木炭.png")
    charcoal.save(output_path)
    print(f"木炭图像已保存至: {output_path}")
    
    return charcoal

# 主函数
if __name__ == "__main__":
    charcoal = create_charcoal()
    print("木炭图像已成功生成！")

# 不再自动显示图像，如需查看请手动打开文件
# charcoal.show()