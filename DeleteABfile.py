import os
import win32api
import win32con

def delete_contents(directory_path):
    """
    遍历指定目录下的所有文件和子目录，取消它们的只读属性，并删除所有内容。

    :param directory_path: 要遍历并删除内容的目录路径
    """
    # 定义一个辅助函数来递归删除目录
    def delete_dir_contents(path):
        # 遍历目录内容
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                # 如果是目录，递归调用自己
                delete_dir_contents(item_path)
                # 删除空目录（注意：如果目录不是空的，到这里时应该已经被递归删除了）
                os.rmdir(item_path)
                print(f"Deleted directory: {item_path}")
            else:
                # 如果是文件，尝试删除
                try:
                    # 检查文件是否为只读，如果是则更改权限
                    if not os.access(item_path, os.W_OK):
                        os.chmod(item_path, os.stat(item_path).st_mode | 0o222)
                    # 删除文件
                    os.remove(item_path)
                    print(f"Deleted file: {item_path}")
                except Exception as e:
                    print(f"Failed to delete file {item_path}: {e}")

    # 调用辅助函数开始删除过程
    delete_dir_contents(directory_path)
    # 尝试删除最外层的目录（如果它是空的，到现在为止应该已经被递归删除了所有内容）
    try:
        os.rmdir(directory_path)
        print(f"Deleted outermost directory: {directory_path}")
    except OSError:
        # 如果目录不是空的（可能是因为权限问题或其他原因导致的文件删除失败），则忽略这个错误
        # 注意：在实际应用中，您可能想要更详细地处理这个错误
        print(f"Failed to delete outermost directory {directory_path}: It may not be empty.")

def deletePlasticfile(file_path):
    """删除plastic文件"""
    if os.path.exists(file_path):
        # 取消文件的只读属性
        win32api.SetFileAttributes(file_path, win32con.FILE_ATTRIBUTE_NORMAL)
        
        # 删除文件
        os.remove(file_path)
        print(f"文件 {file_path} 已成功删除。")
    else:
        print(f"文件 {file_path} 不存在。")