# _*_ coding: utf-8 _*_
# .@FileName:MY_Tools_2023
# .....:2022-09-12 : 16 :42
# .@Aurhor..:MingYu
# .@Contact.:1942598111@qq.com
"""
launch :
        import MY_Tools_2023 as kt_FileName
        reload(FileName)
        FileName.main()
"""
import maya.cmds as cmds
import MY_MenuUI

import importlib
from importlib import reload
reload(MY_MenuUI)

def load_MY_tools():
    MY_MenuUI.MY_Menu_UI()


def unLoad_MY_tools():
    MY_MenuUI.delete_MY_Menu_UI()

def initializePlugin(mobject):
    load_MY_tools()

def uninitializePlugin(mobject):
    load_MY_tools()


def execfile(file_path, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": file_path,
        "__name__": "__main__",
    })
    with open(file_path, 'rb') as file:
        exec(compile(file.read(), file_path, 'exec'), globals, locals)