import json
import os
import random
import shutil
from collections import defaultdict

def process_json(json_file_path, image_base_path, target_image_base_path, output_json_path):
    data_list = []
    print('加载JSON数据...')
    with open(json_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:  # 跳过空行
                item = json.loads(line)
                data_list.append(item)
    
    # 依据数据集名称对数据项进行分组
    dataset_groups = defaultdict(list)
    print('按照数据集分组...')
    for item in data_list:
        # 获取图像相对路径
        actual_path = item['image']
        image_filename = os.path.basename(actual_path)
        image_name, ext = os.path.splitext(image_filename)
        name_parts = image_name.split('_')

        dataset_name = '_'.join(name_parts[:-1])
        dataset_groups[dataset_name].append(item)
    
    print('处理每个数据集...')
    all_items = []
    for dataset_name, items in dataset_groups.items():
        print(f'处理数据集：{dataset_name}')
        
        dataset_dir = os.path.join(target_image_base_path, dataset_name)
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)
        
        for idx, item in enumerate(items):
            # 生成新的ID，从1开始
            new_id = str(idx + 1).zfill(12)
            item['id'] = new_id
            
            # 更新图像路径，保持相对路径不变
            image_rel_path_list = item['image'].split('/')[-3:]
            image_rel_path = '/'.join(image_rel_path_list)

            # 把图片名字改成新的ID
            image_filename = os.path.basename(image_rel_path)
            # image_name, ext = os.path.splitext(image_filename)
            new_image_name = f'{new_id}.jpg'
            image_rel_path_new = os.path.join(image_rel_path.split(image_filename)[0], new_image_name)

            # 构建源图像和目标图像的完整路径
            old_full_image_path = os.path.join(image_base_path, image_rel_path)
            new_full_image_path = os.path.join(target_image_base_path, image_rel_path_new)
            
            # 确保目标目录存在
            new_image_dir = os.path.dirname(new_full_image_path)
            if not os.path.exists(new_image_dir):
                os.makedirs(new_image_dir)
            
            if os.path.exists(old_full_image_path):
                shutil.copy2(old_full_image_path, new_full_image_path)
            else:
                print(f"警告！图像文件不存在：{old_full_image_path}")
            
            # 更新图像路径为相对于目标图像基路径的相对路径
            item['image'] = image_rel_path_new
        
        # 对每个数据集内部进行shuffle
        random.shuffle(items)

        # 将处理后的数据集添加到总列表中
        all_items.extend(items)
    
    # 将所有数据写入输出JSON文件，数据集按顺序排列
    print('写入输出JSON文件...')
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
    
    print(f"处理完成，结果已保存到：{output_json_path}")

# 调用函数
json_file_path = '/data/jcy/data/openx_part/llava/test.json'          # 原始JSON文件路径
image_base_path = '/data/jcy/data/openx_part/llava/images'           # 图像文件所在目录
target_image_base_path = '/data/jcy/data/openx_part/llava_shuffled/images'  # 图像文件目标目录
output_json_path = '/data/jcy/data/openx_part/llava_shuffled/llavadata.json'       # 输出的JSON文件路径


target_dir = os.path.dirname(target_image_base_path)
if not os.path.exists(target_dir):
    os.makedirs(target_dir)
if not os.path.exists(target_image_base_path):
    os.makedirs(target_image_base_path)

process_json(json_file_path, image_base_path, target_image_base_path, output_json_path)