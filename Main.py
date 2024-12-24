import AB
import ABCheck
import ResSyn

if __name__ == '__main__':
    if AB.is_abCommandToolsInstalled():
        if AB.logon("王爽","ws265231","TT Game","pig"):
            AB.Getlogoninfo()
            abfilelist = AB.ABfilepath(r"07Plot\Gacha")
            ABCheck.ABFileDownload(abfilelist,'commitinfo.json')
            res_path = "Z:\\TT Game" # ab工作区
            target_path = "D:\\Projects" # plastic工作区
            files_to_add = ResSyn.resFolder(res_path,target_path)
            if len(files_to_add) > 0:
                ResSyn.add_tsa(res_path,target_path)
                is_deleteAbfile = ResSyn.commit_Repository()
                # if is_deleteAbfile:

            

