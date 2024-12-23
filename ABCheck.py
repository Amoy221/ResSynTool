import json
import ABRes
import os


def ABFileDownload(abfilelist,jsonpath):
    try:
        default_data = {}
        # 尝试读取现有的 JSON 文件
        file_exists = os.path.isfile(jsonpath)
        if not file_exists:
            # 文件不存在，创建新文件并写入默认数据
            with open(jsonpath, 'w', encoding='utf-8') as jsonfile:
                json.dump(default_data, jsonfile, ensure_ascii=False, indent=4)
            print(f"{jsonpath} 文件不存在，已创建并写入默认数据。")
        with open(jsonpath, 'r', encoding='utf-8') as jsonfile:
            existing_entries = json.load(jsonfile)
        for filepath in abfilelist:
            path, user, commitmessage, changedtime = ABRes.gethistory(filepath)
            new_entry = {
                path: {
                    "commiter": user,
                    "modifiedTime": changedtime,
                    "commitmessage": commitmessage
                }
            }
            # print(f"path:{path},changedtime:{changedtime}")
            # 检查 path 是否在 existing_records 的键中
            if path in existing_entries.keys():
                    # 检查 changedtime 是否与 existing_records[path] 中的 changedtime 相匹配
                if existing_entries[path]['modifiedTime'] == changedtime:
                    print(f"Path: {path}, modifiedTime: {changedtime} 文件已存在，且修改时间没变.")
                else:
                    print(f"Path: {path} 文件存在, 但 modifiedTime: {changedtime} 修改时间变化.")
            else:
                print(f"Path: {path} 文件不存在，可以下载.")
                ABRes.GetLatestABRes(path) # 下载资源文件
                # CommitMessage.abfilejson(path,user,commitmessage,changedtime)
                existing_entries.update(new_entry) # 更新下载的信息  
        # 将更新后的 JSON 结构写回到文件中
        with open(jsonpath, 'w', encoding='utf-8') as json_file:
            json.dump(existing_entries, json_file, ensure_ascii=False, indent=4)
                
    except FileNotFoundError:
        # 如果文件不存在，就创建一个空列表
        existing_entries = {}
        print("111")
    except json.JSONDecodeError:
        # 如果文件不是有效的 JSON，打印错误并跳过
        print("Error decoding JSON in output.json")
        existing_entries = {}
    
 
