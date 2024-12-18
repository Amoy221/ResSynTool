import os
import shutil
import subprocess
# import hash1
import hash3

def resFolder(resPath,targetPath):

    # for root, dirs, files in os.walk(resPath):
    #     for dir_name in dirs:
    #         resfile_list.append(os.path.join(root, dir_name))
    #     for file_name in files:
    #         resfile_list.append(os.path.join(root, file_name))
    # print(f"原目录下文件：{resfile_list}")
    # 获取当前脚本文件的完整路径
    # script_path = os.path.abspath(__file__)
    
    # # 获取当前脚本文件所在的目录
    # script_dir = os.path.join(os.path.dirname(script_path),"hash3.json")
    # print
    resfile_list = hash3.process_directory(resPath,"E:\\art_tool\\SynRes\\hashes3.json")


    print(f"有修改或新增的文件：{resfile_list}")
    # print(hash1.process_directory(resPath,"E:\\art_tool\\SynRes\\hashes1.json"))

    if len(resfile_list) > 0:
        for file in resfile_list:
            print(file)
            split_list = file.split(res_path)
            file_name = split_list[1]
            # print(file_name)
            target_file = target_path+file_name
            # if os.path.exists(target_file):
            #     print(f"文件 {target_file} 存在，无法重复提交。")
            #     continue
            files_to_add.append(target_file)
            print(f"准备要提交的文件：{files_to_add}")
    else:
        print("没有需要提交的文件")
    
    if len(files_to_add) > 0:
        # 复制源目录下的所有内容到目标目录，忽略同名文件夹，同名文件内容不同则文件为修改状态
        shutil.copytree(resPath, targetPath, dirs_exist_ok=True)


def add_tsa(res_path,target_path):

    print(f"要添加到工作区的文件：{files_to_add}")
    # 构造cm add命令
    command = ['cm', 'add'] + files_to_add
    # 执行命令
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("文件已成功添加到暂存区:")
        for file in files_to_add:
            print(file)
        # 如果需要，可以打印命令的输出
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"添加文件时出错: {e}")
        # 打印错误输出以帮助调试
        print(e.stderr)



def commit_Repository():
    # 提交信息
    commit_message = "这是通过Python脚本提交的更改"
    for file in files_to_add:
        # 确保文件存在于工作区中
        if not os.path.exists(file):
            print(f"文件 {file} 不存在，无法提交。")
            exit(1)
    # 构造cm ci命令及其参数
    # -m后面跟的是提交信息
    command = ['cm', 'ci', '-m', commit_message ,"--all"] + files_to_add
    try: 
        # 执行命令并等待其完成
        # check=True表示如果命令返回非零退出码，则引发CalledProcessError异常
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 如果命令成功执行，打印提交信息
        print("更改已成功提交到Plastic SCM存储库:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，打印错误信息
        print(f"提交更改时出错: {e}")
        print(e.stderr)


if __name__ == '__main__':
    res_path = "D:\\project_res"
    target_path = "D:\\Projects"
    resfile_list = []
    files_to_add = []
    resFolder(res_path,target_path)
    if len(files_to_add) > 0:
        add_tsa(res_path,target_path)
        commit_Repository()




