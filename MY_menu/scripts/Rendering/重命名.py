# _*_ coding: utf-8 _*_
# .@FileName:重命名
# .....:2022-09-16 : 23 :10
# .@Aurhor..:MingYu
# .@Contact.:1942598111@qq.com
"""
launch :
        import 重命名 as kt_FileName
        reload(FileName)
        FileName.main()
"""
import maya.cmds as cmds
import ig_EzRename
import sys
import importlib

if int((sys.version)[0]) >= 3:
    from importlib import reload
    
reload(ig_EzRename)
ig_EzRename.UI()