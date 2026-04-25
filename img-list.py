import os
import json

IMG_DIR = 'img'
OUTPUT_JS = 'img-list.js'

def generate_img_list():
    img_map = {}
    if not os.path.exists(IMG_DIR):
        print("找不到 img 文件夹")
        return

    # 遍历文件夹
    for filename in os.listdir(IMG_DIR):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            # 提取开头的数字部分，例如 "008-Stonehenge-1.jpg" 提取出 "8" 或 "008"
            parts = filename.split('-')
            if parts[0].isdigit():
                item_id = int(parts[0]) # 转为整数作为 Key
                
                if item_id not in img_map:
                    img_map[item_id] = []
                
                # 将该图片加入对应 ID 的列表
                img_map[item_id].append(filename)

    # 排序图片名，确保像 -1, -2 这种顺序排列
    for key in img_map:
        img_map[key].sort()

    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write(f"const APAH_IMG_LIST = {json.dumps(img_map, indent=2)};")
    
    print(f"成功生成 {OUTPUT_JS}，共记录 {len(img_map)} 个作品的图片。")

generate_img_list()
