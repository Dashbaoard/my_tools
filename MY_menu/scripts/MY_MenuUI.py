# _*_ coding: utf-8 _*_
# .@FileName:MY_MenuUI
# .....:2022-09-12 : 16 :21
# .@Aurhor..:MingYu
# .@Contact.:1942598111@qq.com
"""
launch :
        import MY_MenuUI as kt_FileName
        reload(FileName)
        FileName.main()
"""
import os, shutil, codecs
import sys
import maya.cmds as cmds
import maya.mel as mel


menuList = ['Rendering', 'Rigging', 'Animation','Modeling', 'TD']#大文件夹名称
currentFilePath = r'{}'.format(os.path.dirname(__file__))#返回当前文件夹路径
currentFilePath = currentFilePath.replace('\\', '/')
scriptPackagesPath = r'{}/{}'.format(currentFilePath, 'ScriptPackages')#在路径中找到Scr文件夹
envPaths = [r'{}/{}'.format(currentFilePath, p) for p in menuList]#当前文件夹内的文件夹
envPaths.append(scriptPackagesPath)#加入Scr文件夹
print(scriptPackagesPath)

def writeNewFileCodeUTF(path, string):
    file = codecs.open(path, 'w', 'utf-8')
    file.write(string)
    file.close


def copyTreeToPath(sourceFolder, targetPath):
    targetPath = targetPath.decode('gbk')
    sourceFolder = sourceFolder.decode('gbk')
    getAllFiles = []
    getAllDirs = []
    for root, dirs, files in os.walk(sourceFolder, topdown=False):
        for name in files:
            getAllFiles.append(os.path.join(root, name).replace('\\', '/'))
        for name in dirs:
            getAllDirs.append(os.path.join(root, name).replace('\\', '/'))

    for one in getAllDirs:
        getPathTarget = targetPath + one.replace(sourceFolder, '')

        cmds.sysFile(getPathTarget, md=True)
    allNum = getAllFiles.__len__()

    for i, one in enumerate(getAllFiles):
        getPathTarget = targetPath + one.replace(sourceFolder, '')
        try:
            cmds.sysFile(one, copy=getPathTarget)
        except:
            pass


for path in envPaths:
    if path in sys.path:
        print('The python Env Path Already there')
    else:
        sys.path.append(path)

for path in envPaths:
    if path in os.environ['MAYA_SCRIPT_PATH']:
        print('The MEL Env Path Already there')
    else:
        os.environ['MAYA_SCRIPT_PATH'] = '{};{}'.format(path, os.getenv('MAYA_SCRIPT_PATH'))

menuItemList = []
for item in menuList:
    path = r'{}/{}'.format(currentFilePath, item)#RAT文件夹
    for parent, dirnames, filenames in os.walk(path):
        dirnames[:] = [d for d in dirnames if d not in "__pycache__"]
        #print(parent, dirnames, filenames)
        if filenames:
            itemList = []
            for f in filenames:
                itemList.append(f.split('.')[0])
            menuItemList.append([item, itemList])

commandItemList = []
for item in menuItemList:
    commandItem = list(set(item[1]))
    commandItemList.append([item[0], commandItem])
#print(menuItemList)
#print(commandItemList)


def execfile(file_path, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": file_path,
        "__name__": "__main__",
    })
    with open(file_path, 'rb') as file:
        exec(compile(file.read(), file_path, 'exec'), globals, locals)


def MY_Menu_UI(*args):
    if cmds.menu('testMenu', ex=True):
        cmds.deleteUI('testMenu')
    gMainWindow = mel.eval('$tmpVar=$gMainWindow')
    mainMenu = cmds.menu('testMenu', label='MY', tearOff=True, p=gMainWindow)
    for m in menuItemList:
        cmds.menuItem('{}_MenuItem'.format(m[0]), label=m[0], subMenu=True, p=mainMenu)
        for commandI in m[1]:
            #print(commandI)
            #print(currentFilePath)
            #print(m[0])
            cmds.menuItem('{}_MenuItem'.format(commandI), label=commandI, p='{}_MenuItem'.format(m[0]),
                          c="from MY_MenuUI import execfile;execfile('{}/{}/{}.py')".format(currentFilePath, m[0], commandI))
#"import {0};from importlib import reload;import os; reload({0});os.system('

def delete_MY_Menu_UI(*args):
    if cmds.menu('testMenu', ex=True):
        cmds.deleteUI('testMenu')

