import os
import hashlib
import json

commit_file = []

def calculate_file_hash(file_path, hash_function=hashlib.sha256):
    """计算文件哈希值"""
    hash_obj = hash_function()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def load_hashes_from_json(json_file_path):
    """读取json文件的哈希值"""
    try:
        with open(json_file_path, "r") as f:
            hashes = json.load(f)
    except FileNotFoundError:
        hashes = {}
    return hashes

def save_hashes_to_json(json_file_path, hashes):
    """把哈希值保存到json文件中"""
    with open(json_file_path, "w") as f:
        json.dump(hashes, f, indent=4)

def calculate_directory_hash(directory_path, hash_function=hashlib.sha256):
    """基于子目录下文件的哈希值变化，计算子目录的哈希值"""
    directory_hasher = hash_function()
    contents_hashes = []

    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = calculate_file_hash(file_path)
            contents_hashes.append(file_hash)

    # Sort the hashes to ensure consistent hashing of the directory contents
    contents_hashes.sort()

    # Hash the concatenated hashes of the contents
    for content_hash in contents_hashes:
        directory_hasher.update(content_hash.encode('utf-8'))

    return directory_hasher.hexdigest()

def process_directory(directory, json_file_path):
    """计算哈希，更新json"""
    hashes = load_hashes_from_json(json_file_path)
    updated_hashes = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_file_hash(file_path)

            if file_path in hashes:
                if hashes[file_path] == file_hash:
                    print(f"{file_path}没有修改！跳过")  # Key and value (hash) both match
                    continue
                else:
                    # Update the hash if it has changed
                    updated_hashes[file_path] = file_hash
                    print(f"修改：{file_path}，更新json")
                    commit_file.append(file_path)
            else:
                # Add the new file and its hash to the dictionary
                updated_hashes[file_path] = file_hash
                print(f"新增：{file_path}，更新json")
                commit_file.append(file_path)
        
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            dir_hash = calculate_directory_hash(dir_path)
            if dir_path in hashes:
                if hashes[dir_path] == dir_hash:
                    print(f"{dir_path}没有修改！跳过")  # Key and value (hash) both match
                    continue
                else:
                    # Update the hash if it has changed
                    updated_hashes[dir_path] = dir_hash
                    print(f"修改：{dir_path}，更新json")
                    commit_file.append(dir_path)
            else:
                # Add the new file and its hash to the dictionary
                updated_hashes[dir_path] = dir_hash
                print(f"新增：{dir_path}，更新json")
                commit_file.append(dir_path)


    # Update the JSON file with any changes
    hashes.update(updated_hashes)
    save_hashes_to_json(json_file_path, hashes)
    return commit_file