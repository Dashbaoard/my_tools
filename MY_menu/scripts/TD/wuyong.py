# _*_ coding: utf-8 _*_
# .@FileName:重命名
# .....:2022-09-16 : 23 :10
# .@Aurhor..:MingYu
# .@Contact.:1942598111@qq.com
"""
launch :
        import pSphere as kt_FileName
        reload(FileName)
        FileName.main()
"""
import maya.cmds as cmds
import pSphere
import importlib
importlib.reload(pSphere)
