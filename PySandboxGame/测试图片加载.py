import pygame
import sys

# 初始化pygame
pygame.init()

# 屏幕设置
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("武器图片加载测试")

# 定义与主程序相同的颜色常量
WOOD_BROWN = (139, 69, 19)
ORE_SILVER = (192, 192, 192)

# 需要测试的武器图片列表
weapons = [
    "木弓箭",
    "木箭",
    "步枪",
    "手枪",
    "狙击枪",
    "子弹"
]

# 加载图片的函数
loaded_images = {}
def load_image(name):
    try:
        img = pygame.image.load(f"{name}.png").convert_alpha()
        return pygame.transform.scale(img, (64, 64))  # 放大显示以便查看
    except FileNotFoundError:
        print(f"警告: 无法加载图像 {name}.png: 文件未找到。创建替代颜色块。")
        # 创建替代颜色块
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        # 根据名称返回相应的颜色
        color_map = {
            "木弓箭": WOOD_BROWN,
            "木箭": WOOD_BROWN,
            "步枪": ORE_SILVER,
            "手枪": ORE_SILVER,
            "狙击枪": ORE_SILVER,
            "子弹": ORE_SILVER
        }
        color = color_map.get(name, (128, 128, 128))
        surf.fill(color)
        return surf
    except Exception as e:
        print(f"警告: 加载图像 {name}.png 时出错: {e}")
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        surf.fill((255, 0, 255))  # 紫色作为错误颜色
        return surf

# 加载所有武器图片
for weapon in weapons:
    loaded_images[weapon] = load_image(weapon)

# 字体设置
try:
    font = pygame.font.Font(None, 36)
except:
    font = pygame.font.SysFont(None, 36)

# 主循环
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 填充背景色
    screen.fill((240, 240, 240))
    
    # 绘制标题
    title = font.render("武器图片加载测试", True, (0, 0, 0))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))
    
    # 绘制所有武器图片和名称
    start_x = 50
    start_y = 100
    gap = 80
    
    for i, weapon in enumerate(weapons):
        row = i % 3
        col = i // 3
        
        x = start_x + row * gap
        y = start_y + col * gap
        
        # 绘制图片
        screen.blit(loaded_images[weapon], (x, y))
        
        # 绘制名称
        text = font.render(weapon, True, (0, 0, 0))
        screen.blit(text, (x, y + 70))
    
    # 刷新屏幕
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(60)

# 退出游戏
pygame.quit()
sys.exit()