import os

def deleteFolder():
    list = os.listdir()
    for item in list:
        try:
            os.remove(item)
            print(item)
        except:
            os.chdir(item)
            deleteFolder(item)
            os.chdir("..")
            os.rmdir(item)
    