import os
import subprocess
import time
import texthelper
from datetime import datetime
import CommitMessage
import json
import ABCheck

def is_abCommandToolsInstalled():
    cmd = f'ab'
    # 是否安装ab库命令行工具
    result = subprocess.getoutput(cmd)
    if "'ab' 不是内部或外部命令" not in result:
        return True
    else:
        print("未安装ab命令行工具(NXNCommandLineTool.exe),请安装后再试")
        return False
    
def is_login():
    # 是否登录ab库
    result = subprocess.getoutput('ab logoninfo')
    if result != 'Invalid session please logon!\n':
        print("已经登录！！！")
        return True
    else:
        print("没有登录。请先登录！！！")
        return False
    
def setconfigproperty(name, value):
    # 设置配置项
    cmd = f'ab setconfigproperty -name {name} -value {value}'
    result = subprocess.getoutput(cmd)
    if result == '' or 'has been set to' in result:
        print("配置成功")
        return True
    else:
        # logger.error("设置配置项错误! 错误信息:" + result)
        print("配置失败")
        return False


def logon(user, password, database, server):
    """
    使用指定的用户、密码、数据库和服务器信息登录AB系统。

    参数:
    - user: 用户名
    - password: 用户密码
    - database: 数据库名称
    - server: 服务器地址

    输出:
    - 登录操作的输出结果
    """
    # logger.info(f"[{database}]登陆中")
    # 登录前退出JXDK桥
    cmd = 'ab shutdown -force'
    subprocess.getoutput(cmd)
    time.sleep(2)

    # 开始登录
    cmd = f'ab logon -u {user} -p {password} -d "{database}" -s {server}'
    result = subprocess.getoutput(cmd)
    if (result == '' or 'connecting to JXDK Bridge...' in result) and 'Username or password are invalid.' not in result:
        # logger.info(f"[{database}]登录成功")
        print("登录成功！！")
        setconfigproperty('VerboseLevel', '2')  # 设置输出详细程度
        setconfigproperty('SessionTimeout', '0')  # 设置会话永不过期
        return True
    else:
        # logger.error(f"[{database}]登录失败! 错误信息:" + result.replace('\n', '').replace('connecting to JXDK Bridge...', ''))
        print("登录失败！！！")
        return False


def Getlogoninfo():
    cmd = f'ab logoninfo'
    result = subprocess.getoutput(cmd)
    print(result)

def GetLatestABRes(abpath):
    '''
    参数：'-nosmartget' 关闭智能获取功能.get_date.dat表
    '''
    print(f'下载ab库文件到本地z盘中....')
    downloadfaild_list = []
    cmd = ['ab', 'getlatest', abpath, '-overwritewritable', 'replace', '-overwritecheckedout', 'replace','-nosmartget']
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # print(result)
    output = []
    for line in result.stdout:
        output.append(line)
        print(line)
    result.wait()
    print(f"output:{output}")
    # 判断最后一行输出是否包含'successfully'
    if f'successfully' in output[-1]:
        # logger.info(f"更新成功[{path}]")
        print(f"{abpath}更新成功------------------------")
        return True
    else:
        print(f'{abpath}:更新失败')
        # logger.error(f"[{path}]更新失败! 错误信息:" + output[-1].replace('\n', ''))
        if "Error message from the server: ''" in output[-1]:
            # logger.error(f"[{path}]错误信息为服务器错误,重试中")
            return GetLatestABRes(abpath)  # 递归调用并返回结果
        else:
            downloadfaild_list.append(abpath)
            print(f'ab库下载失败的文件：{downloadfaild_list}')
            return False


def gethistory(path):
    cmd = f'ab history -format "user:#Changed By#|commitmessage:#CheckInComment#|time:#Changed At#|created time:#Created At#|" "{path}"'
    result = subprocess.getoutput(cmd)
    # print(f"result:{result}")
    data = [line for line in subprocess.getoutput(cmd).splitlines() if line != '|' and 'user' in line]
    # print(f"data:{data}")
    if len(data) >= 1:
        index = 0
        while index<len(data):
            result = data[index]
            # print(result)
            user = texthelper.get_middle_text(result,'user:', '|')
            # if len(data) == 1 and user in whitelist:
            #     return None,None,None
            # #  找到并只输出 白名单中存在的user的内容
            # if not user or user in whitelist:
            #     index+=1
            #     if index==len(data):
            #         return None,None,None
            #     continue
            commitmessage = texthelper.get_middle_text(result,'commitmessage:', '|')
            timestamp = texthelper.get_middle_text(result,'time:', '|')
            createdtime = result.split("created time:")[1].split('|')[0].strip()
            # print(f"createdtime:{createdtime}")
            if timestamp == '':
                # 解析时间字符串为 datetime 对象
                parsed_time = datetime.strptime(createdtime, "%a %b %d %H:%M:%S %Y")
                # 格式化为指定的时间格式
                changedtime = parsed_time.strftime("%Y-%m-%d %H:%M:%S")
                # print(f"changedtime:{changedtime}")
            else:
                changedtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(timestamp)))
                # print(f"changedtime2:{changedtime}")
            print(f'[{path}]提交信息为[{user}|{commitmessage}|{changedtime}]')
            return path,user,commitmessage,changedtime
        else:
            return False



def ABfilepath(path):
    print("正在检索AB库所有文件....")
    # ab enumobjects -format "Name of Object:#Name#,Local-Path=#LocalPath#" -recursive "Z:\TT Game\07Plot\Gacha"
    # cmd = ['ab','enumobjects','-format', '"Name of Object:#Name#,Local-Path=#LocalPath#"', '-recursive', path]
    cmd = f'ab enumobjects -format "Name of Object:#Name#,Local-Path=#LocalPath#" -recursive "{path}"'
    result = subprocess.getoutput(cmd)
    # print(type(result))
    local_paths = []
    lines = result.split('\n')
    for line in lines:
        if 'Local-Path=' in line:
            parts = line.split('Local-Path=')
            local_path = parts[1].strip()
            local_path = local_path.split(r'Z:\TT Game')[1]
            print(local_path)
            local_paths.append(local_path)
    # print(local_paths)
    return local_paths


# if __name__ == '__main__':
#     if is_abCommandToolsInstalled():
#         if logon("王爽","ws265231","TT Game","pig"):
#             Getlogoninfo()
#             # GetLatestABRes(r"07Plot\Gacha")
#             # file_list = Getlocalrespath(r'Z:\TT Game') # 可以不用了
#             # for abfilepath in file_list:
#             #     path,user,commitmessage,changedtime = gethistory(abfilepath)
#             #     CommitMessage.abfilejson(path,user,commitmessage,changedtime)
#             abfilelist = ABfilepath(r"07Plot\Gacha") # 获取ab库下所有文件的路径
#             # for filepath in abfilelist:
#             #     path,user,commitmessage,changedtime = gethistory(filepath) # 获取每个文件的提交信息
#             ABCheck.ABFileDownload(abfilelist,'commitinfo.json')






