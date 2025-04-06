# _*_ coding: utf-8 _*_
# .@FileName:MY_Tools_2020
# .....:2022-09-17 : 10 :46
# .@Aurhor..:MingYu
# .@Contact.:1942598111@qq.com
"""
launch :
        import MY_Tools_2020 as kt_FileName
        import importlib.reload as relaad
        reload(FileName)
        FileName.main()
"""
import maya.cmds as cmds
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
import MY_MenuUI_2020
import importlib
#from importlib import reload
reload(MY_MenuUI_2020)

def load_MY_tools():
    MY_MenuUI_2020.MY_Menu_UI()

def unLoad_MY_tools():
    MY_MenuUI_2020.delete_MY_Menu_UI()

def initializePlugin(mobject):
    load_MY_tools()

def uninitializePlugin(mobject):
    load_MY_tools()