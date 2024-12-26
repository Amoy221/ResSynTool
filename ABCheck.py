import json
import AB
import os
import DeleteABfile
import test


def ABFileDownload(abfilelist,jsonpath,target_path,ab_path):
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
            path, user, commitmessage, changedtime = AB.gethistory(filepath) # 获取每个文件的历史信息
            
            # 检查 path 是否在 existing_records 的键中
            if path in existing_entries.keys():
                    # 检查 changedtime 是否与 existing_records[path] 中的 changedtime 相匹配
                if existing_entries[path]['modifiedTime'] == changedtime:
                    print(f"Path: {path}, modifiedTime: {changedtime} 文件已存在，且修改时间没变.")
                    continue
                else:
                    print(f"Path: {path} 文件存在, 但 modifiedTime: {changedtime} 修改时间变化.")
                    
                    # print(f"target_path:{target_path},path:{path}")
                    # plasticfilepath = os.path.join(target_path,path) # 拼接plastic文件路径
                    plasticfilepath = target_path + path
                    # print(plasticfilepath)
                    plasticfilepath = plasticfilepath.replace('\\\\','\\')

                    if '.' in plasticfilepath.split("\\")[-1]:

                        DeleteABfile.deletePlasticfile(plasticfilepath) # 删除plastic文件
                        print(f"plastic工作区的同名文件{plasticfilepath}已删除。。。。")
                        existing_entries.pop(path)
                    # 将更新后的字典写回到JSON文件
                    with open(jsonpath, 'w', encoding='utf-8') as json_file:
                        json.dump(existing_entries, json_file, ensure_ascii=False, indent=4) 
                    print(f"缓存json文件{path}数据已移除。。。。")
                    directories = test.get_changetime_directories(plasticfilepath,ab_path)
                    for directory in directories:
                        directory = directory.split(target_path)[1] + "\\"
                        # print(directory)
                        existing_entries[directory]['modifiedTime'] = changedtime
                        print(f"文件{directory}时间已修改：{changedtime}")

            else:
                print(f"Path: {path} 文件不存在，可以下载.")

            if '.' in path.split('\\')[-1]:
                # print(f"{path}是文件。。")

                is_updateJson = AB.GetLatestABRes(path) # 下载资源文件到本地
            else:
                # print(f"{path}是文件夹。。")
                is_updateJson = True

            # CommitMessage.abfilejson(path,user,commitmessage,changedtime)
            if is_updateJson:
                new_entry = {
                    path: {
                        "commiter": user,
                        "modifiedTime": changedtime,
                        "commitmessage": commitmessage
                    }
                }
                existing_entries.update(new_entry) # 更新下载的信息  
        # 将更新后的 JSON 结构写回到文件中
        with open(jsonpath, 'w', encoding='utf-8') as json_file:
            json.dump(existing_entries, json_file, ensure_ascii=False, indent=4)
                
    except FileNotFoundError as e:
        # 如果文件不存在，就创建一个空列表
        existing_entries = {}
        # print("111")
        print(f"FileNotFoundError:{e}")
        print(f"FileNotFoundError:{str(e)}")

    except json.JSONDecodeError:
        # 如果文件不是有效的 JSON，打印错误并跳过
        print("Error decoding JSON in output.json")
        existing_entries = {}
    


