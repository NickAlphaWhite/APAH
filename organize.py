import os
import re
import json

# --- 配置 ---
IMG_DIR = 'img'  # 你的图片文件夹名字
OUTPUT_JS = 'img-list.js'  # 生成的 JS 文件
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}

def organize_images():
    if not os.path.exists(IMG_DIR):
        print(f"错误: 找不到文件夹 '{IMG_DIR}'")
        return

    image_map = {}
    files = os.listdir(IMG_DIR)
    
    print("开始处理图片重命名...")

    for filename in files:
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            continue

        # 使用正则匹配文件名开头的数字 (例如从 "237-Pisupo..." 中提取 "237")
        match = re.match(r'^(\d+)', filename)
        if match:
            item_id = match.group(1)
            padded_id = item_id.zfill(3)  # 统一补齐为三位数，如 001
            
            # 检查是否已经是纯编号格式，如果不是，则重命名
            new_filename = f"{padded_id}{ext}"
            old_path = os.path.join(IMG_DIR, filename)
            new_path = os.path.join(IMG_DIR, new_filename)

            if filename != new_filename:
                # 处理重名冲突（例如 008-1 和 008-2）
                count = 1
                while os.path.exists(new_path):
                    new_filename = f"{padded_id}-{count}{ext}"
                    new_path = os.path.join(IMG_DIR, new_filename)
                    count += 1
                
                os.rename(old_path, new_path)
                print(f"重命名: {filename} -> {new_filename}")
            
            # 记录到映射表中 (ID -> 文件名)
            image_map[int(item_id)] = new_filename

    # 生成 JS 文件内容
    js_content = f"// 自动生成的图片索引表\nconst APAH_IMG_LIST = {json.dumps(image_map, indent=2, sort_keys=True)};"
    
    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"\n成功！")
    print(f"- 图片已完成编号重命名")
    print(f"- 已生成 {OUTPUT_JS}")

if __name__ == "__main__":
    organize_images()
