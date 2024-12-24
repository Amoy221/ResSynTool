import ABRes
import ABCheck
import ResSyn

if __name__ == '__main__':
    if ABRes.is_abCommandToolsInstalled():
        if ABRes.logon("王爽","ws265231","TT Game","pig"):
            ABRes.Getlogoninfo()
            abfilelist = ABRes.ABfilepath(r"07Plot\Gacha")
            ABCheck.ABFileDownload(abfilelist,'commitinfo.json')

            res_path = "Z:\\TT Game" # ab工作区
            target_path = "D:\\Projects" # plastic工作区
            # resfile_list = []
            # files_to_add = []
            files_to_add = ResSyn.resFolder(res_path,target_path)
            # cl = type(files_to_add)
            # print(f"files_to_add:{files_to_add}，类型：{cl}")
            if len(files_to_add) > 0:
                ResSyn.add_tsa(res_path,target_path)
                ResSyn.commit_Repository()
