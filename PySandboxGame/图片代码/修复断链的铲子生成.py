from PIL import Image, ImageDraw
import random

def gen_material_shovel(material, output="%s铲.png"):
    mat_colors = {
        '石': {'base': (160,160,160,255), 'grain': (130,130,130,255), 'high': (190,190,190,255), 'dark': (100,100,100,255)},
        '铜': {'base': (184,115,51,255), 'grain': (164,95,31,255), 'high': (204,135,71,255), 'dark': (154,85,21,255)},
        '铁': {'base': (200,200,200,255), 'grain': (170,170,170,255), 'high': (230,230,230,255), 'dark': (140,140,140,255)},
        '金': {'base': (255,215,0,255), 'grain': (235,195,0,255), 'high': (255,235,100,255), 'dark': (215,175,0,255)},
        '钻石': {'base': (175,238,238,255), 'grain': (145,208,208,255), 'high': (224,255,255,255), 'dark': (127,204,204,255)}
    }
    c = mat_colors.get(material)
    if not c:
        print(f"错误：不支持的材质 {material}")
        return
        
    img = Image.new("RGBA", (32,32), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    cx = 16  # 中心x坐标

    # 铲头绘制（增加与连接部的过渡处理）
    blade_h, blade_bw = 10, 16
    for y in range(blade_h):
        w = blade_bw - int((y/blade_h)*(blade_bw-8))
        hw = w//2
        for x in range(cx-hw, cx+hw+1):
            if 0<=x<32 and 0<=y<32:
                # 底部边缘（加深）
                if y == blade_h-1:
                    draw.point((x,y), c['dark'])
                # 左侧高光
                elif x == cx - hw:
                    draw.point((x,y), c['high'])
                # 右侧暗部
                elif x == cx + hw:
                    draw.point((x,y), c['dark'])
                # 内部基础色+纹理
                else:
                    draw.point((x,y), c['base'])
                    if material == '石' and random.random()<0.3:
                        draw.point((x,y), c['dark'])
                    if material in ['铜','铁'] and y%3==0:
                        draw.point((x,y), c['grain'])
                    if material == '金' and random.random()<0.2:
                        draw.point((x,y), c['high'])
                    if material == '钻石' and (x+y)%4==0:
                        draw.point((x,y), c['high'])

    # 连接部（重点修复：增加与铲头和握柄的渐变过渡，解决断链问题）
    conn_h, conn_w = 3, 5
    # 铲头底部最后一行的宽度（用于衔接）
    blade_last_row_width = blade_bw - int(((blade_h-1)/blade_h)*(blade_bw-8))
    blade_last_hw = blade_last_row_width // 2
    
    for y in range(blade_h, blade_h+conn_h):
        if y >=32: break
        # 连接部高度比例（0-1），用于渐变过渡
        conn_ratio = (y - blade_h) / (conn_h - 1) if conn_h > 1 else 0
        
        # 宽度从铲头底部宽度平滑过渡到连接部宽度
        current_width = int(blade_last_row_width - conn_ratio * (blade_last_row_width - conn_w))
        hw = current_width // 2
        
        for x in range(cx-hw, cx+hw+1):
            if 0<=x<32:
                # 颜色从铲头底部颜色渐变到连接部木色
                r = int(c['dark'][0] * (1 - conn_ratio) + 120 * conn_ratio)
                g = int(c['dark'][1] * (1 - conn_ratio) + 80 * conn_ratio)
                b = int(c['dark'][2] * (1 - conn_ratio) + 40 * conn_ratio)
                draw.point((x,y), (r, g, b, 255))
                
                # 连接部边缘（随高度变化）
                if x in [cx-hw, cx+hw]:
                    edge_r = int(c['dark'][0] * (1 - conn_ratio) + 100 * conn_ratio)
                    edge_g = int(c['dark'][1] * (1 - conn_ratio) + 60 * conn_ratio)
                    edge_b = int(c['dark'][2] * (1 - conn_ratio) + 20 * conn_ratio)
                    draw.point((x,y), (edge_r, edge_g, edge_b, 255))

    # 握柄（增加与连接部的衔接处理）
    handle_start = blade_h + conn_h
    # 连接部最后一行的宽度（用于衔接）
    conn_last_width = conn_w
    conn_last_hw = conn_last_width // 2
    
    for y_idx, y in enumerate(range(handle_start, 32)):
        if y >=32: break
        # 握柄起始阶段的过渡比例
        handle_ratio = min(y_idx / 3, 1)  # 前3行完成过渡
        
        # 宽度从连接部宽度平滑过渡到握柄宽度
        w = int(conn_last_width - handle_ratio * (conn_last_width - 5) + 
               (y_idx / (31-handle_start)) * 2 if (31-handle_start)!=0 else 3)
        hw = w//2
        
        # 握柄颜色（从连接部颜色渐变到握柄色）
        hc_r = int(120 * (1 - handle_ratio) + (130 - 20 * (y_idx / 19)) * handle_ratio)
        hc_g = int(80 * (1 - handle_ratio) + (90 - 20 * (y_idx / 19)) * handle_ratio)
        hc_b = int(40 * (1 - handle_ratio) + (50 - 20 * (y_idx / 19)) * handle_ratio)
        hc = (int(hc_r), int(hc_g), int(hc_b), 255)
        
        for x in range(cx-hw, cx+hw+1):
            if 0<=x<32:
                draw.point((x,y), hc)
                if x in [cx-hw, cx+hw]:
                    draw.point((x,y), (100,60,20,255))
        
        # 防滑纹理
        if y_idx%2==0 and y<30:
            for x in range(cx-hw, cx+hw+1):
                if 0<=x<32:
                    draw.point((x,y), (100,60,20,255))

    try:
        img.save(output % material)
        print(f"{material}铲生成：{output % material}")
    except Exception as e:
        print(f"保存{material}铲失败：{str(e)}")

if __name__ == "__main__":
    for mat in ['石','铜','铁','金','钻石']:
        gen_material_shovel(mat)
