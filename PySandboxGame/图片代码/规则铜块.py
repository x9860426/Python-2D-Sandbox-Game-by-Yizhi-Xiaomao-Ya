from PIL import Image, ImageDraw
import random

def generate_regular_copper_block(output_path="规则铜块.png"):
    # 规则纹理铜块：更整齐的网格图案，减少随机性
    size = 32
    image = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(image)
    
    # 铜块基础颜色（更统一的色调）
    copper_colors = [
        (184, 115, 51),   # 标准铜色
        (195, 122, 54),   # 亮铜色（用于高光区域）
        (173, 108, 48)    # 暗铜色（用于线条）
    ]
    
    # 1. 填充基础底色（更均匀的基础）
    for x in range(1, size - 1):
        for y in range(1, size - 1):
            # 基础色占比更高，减少随机变化
            if random.random() < 0.8:
                color = copper_colors[0]  # 主要使用标准铜色
            else:
                color = copper_colors[1]  # 少量高光
            
            draw.point((x, y), color)
    
    # 2. 绘制规则网格线条（主要特征）
    grid_size = 8  # 网格大小，控制规则程度
    
    # 横向线条（每grid_size像素一条）
    for y in range(grid_size, size - 1, grid_size):
        for x in range(1, size - 1):
            # 线条连续无断裂，增强规则感
            draw.point((x, y), copper_colors[2])
            # 线条下方添加细微高光，增强立体感
            if y + 1 < size - 1:
                draw.point((x, y + 1), copper_colors[1])
    
    # 纵向线条（每grid_size像素一条）
    for x in range(grid_size, size - 1, grid_size):
        for y in range(1, size - 1):
            # 线条连续无断裂
            draw.point((x, y), copper_colors[2])
            # 线条右侧添加细微高光
            if x + 1 < size - 1:
                draw.point((x + 1, y), copper_colors[1])
    
    # 3. 网格内添加次要纹理（保持规则性）
    sub_grid = grid_size // 2  # 子网格大小
    
    # 子网格线条（更细的辅助线）
    for y in range(sub_grid, size - 1, sub_grid):
        for x in range(1, size - 1):
            # 辅助线更淡且有规律
            if random.random() < 0.3:  # 30%透明度的辅助线
                draw.point((x, y), (
                    copper_colors[2][0] + 10,
                    copper_colors[2][1] + 5,
                    copper_colors[2][2] + 5
                ))
    
    for x in range(sub_grid, size - 1, sub_grid):
        for y in range(1, size - 1):
            if random.random() < 0.3:
                draw.point((x, y), (
                    copper_colors[2][0] + 10,
                    copper_colors[2][1] + 5,
                    copper_colors[2][2] + 5
                ))
    
    # 4. 添加规则分布的高光点（每个网格内固定位置）
    for x in range(grid_size//2, size - 1, grid_size):
        for y in range(grid_size//2, size - 1, grid_size):
            # 每个主网格中心添加高光
            draw.point((x, y), copper_colors[1])
            # 周围4个点也添加高光
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if 1 <= x + dx < size - 1 and 1 <= y + dy < size - 1:
                    draw.point((x + dx, y + dy), copper_colors[1])
    
    # 5. 绘制1像素黑色边框
    for x in range(size):
        draw.point((x, 0), (0, 0, 0))
        draw.point((x, size - 1), (0, 0, 0))
    
    for y in range(1, size - 1):
        draw.point((0, y), (0, 0, 0))
        draw.point((size - 1, y), (0, 0, 0))
    
    # 保存图片
    image.save(output_path)
    print(f"规则铜块图片已生成：{output_path} (32x32像素)")

if __name__ == "__main__":
    generate_regular_copper_block()
