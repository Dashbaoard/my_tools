# _*_ coding: utf-8 _*_
# .@FileName:快速打开工程目录
# .....:2022-09-24 : 08 :29
# .@Aurhor..:MingYu
# .@Contact.:1942598111@qq.com
"""
launch :
        import 快速打开工程目录 as kt_FileName
        import importlib.reload as relaad
        reload(FileName)
        FileName.main()
"""
import maya.cmds as cmds
import maya.mel as mel

modulePath = cmds.getModulePath(moduleName='MY_Tools_2023')

mel.eval('source "{}/scripts/ScriptPackages/快速打开工程目录.mel";'.format(modulePath))