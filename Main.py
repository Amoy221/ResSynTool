import AB
import ABCheck
import ResSyn
import DeleteABfile
import os

if __name__ == '__main__':
    if AB.is_abCommandToolsInstalled():
        if AB.logon("王爽","ws265231","TT Game","pig"):
            AB.Getlogoninfo()
            res_path = "Z:\\TT Game" # ab工作区
            target_path = "D:\\Projects" # 把这个路径换成plastic工作区----------------
            abpath = r"07Plot\Gacha"
            ablist,abfilelist,abdirtorylist = AB.ABfilepath(abpath) # 检索ab库所有文件(换成ab库路径)---------------
            # print(abfilelist)

            ab_path = os.path.join(target_path,abpath) # D:\\Projects\07Plot\Gacha
            ABCheck.ABFileDownload(ablist,'commitinfo.json',target_path,ab_path) #把ab文件下载到本地 
            res_path = "Z:\\TT Game" # ab工作区
            target_path = "D:\\Projects" # 把这个路径换成plastic工作区----------------
            files_to_add = ResSyn.resFolder(res_path,target_path) # 把文件移动到plastic工作区
            if len(files_to_add) > 0:
                ResSyn.add_tsa(res_path,target_path)
                is_deleteAbfile = ResSyn.commit_Repository()
                if is_deleteAbfile:
                    DeleteABfile.delete_contents(res_path) # 提交到plastic库后，删除ab本地文件


            

