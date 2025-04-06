# _*_ coding: utf-8 _*_
# .@FileName:MY_MenuUI_2020
# .....:2022-09-17 : 14 :29
# .@Aurhor..:MingYu
# .@Contact.:1942598111@qq.com
"""
launch :
        import MY_MenuUI_2020 as kt_FileName
        import importlib.reload as relaad
        reload(FileName)
        FileName.main()
"""

import os
import sys
import maya.cmds as cmds
import maya.mel as mel


menuList = ['Rendering', 'Rigging', 'Animation', 'TD']#大文件夹名称
currentFilePath = r'{}'.format(os.path.dirname(__file__))#返回当前文件夹路径
scriptPackagesPath = r'{}\{}'.format(currentFilePath, 'ScriptPackages')#在路径中找到Scr文件夹
envPaths = [r'{}\{}'.format(currentFilePath, p) for p in menuList]#当前文件夹内的文件夹
envPaths.append(scriptPackagesPath)#加入Scr文件夹
#print(envPaths)
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
    path = r'{}\{}'.format(currentFilePath, item)#RAT文件夹
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


def MY_Menu_UI(*args):
    if cmds.menu('testMenu', ex=True):
        cmds.deleteUI('testMenu')
    gMainWindow = mel.eval('$tmpVar=$gMainWindow')
    mainMenu = cmds.menu('testMenu', label='MY', tearOff=True, p=gMainWindow)
    for m in commandItemList:
        cmds.menuItem('{}_MenuItem'.format(m[0]), label=m[0], subMenu=True, p=mainMenu)
        for commandI in m[1]:
            print(commandI)
            cmds.menuItem('{}_MenuItem'.format(commandI), label=commandI, p='{}_MenuItem'.format(m[0]),
                          c="import {0};import os; reload({0});os.system('python {0}')".format(commandI))


def delete_MY_Menu_UI(*args):
    if cmds.menu('testMenu', ex=True):
        cmds.deleteUI('testMenu')
