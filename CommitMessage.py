import json
import os

def abfilejson(path, user, commitmessage, changedtime):
    '''记录提交的文件缓存'''
    # 定义要追加的数据
    new_entry = {
        path: {
            "commiter": user,
            "modifiedTime": changedtime,
            "commitmessage": commitmessage
        }
    }
    
    # 尝试读取现有的 JSON 文件
    file_exists = os.path.isfile('output.json')
    if file_exists:
        with open('output.json', 'r', encoding='utf-8') as json_file:
            try:
                # 读取并解析现有的 JSON 内容
                existing_data = json.load(json_file)
            except json.JSONDecodeError:
                # 如果文件不是有效的 JSON，则创建一个空的结构
                existing_data = {}
    else:
        # 如果文件不存在，则创建一个空的结构
        existing_data = {}
    
    # 更新 JSON 结构
    # 注意：如果 'path' 键已经存在，这将覆盖旧数据
    # 如果需要处理键冲突，您需要实现额外的逻辑
    existing_data.update(new_entry)
    
    # 将更新后的 JSON 结构写回到文件中
    with open('output.json', 'w', encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
    
    print("JSON 文件已更新")
