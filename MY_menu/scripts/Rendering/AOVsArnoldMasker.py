# _*_ coding: utf-8 _*_
# .@FileName:重命名
# 
# .@Aurhor..:MingYu
# .@Contact.:1942598111@qq.com
"""
launch :
        import AOVsArnoldMasker as kt_FileName
        import importlib.reload as relaad
        reload(FileName)
        FileName.main()
"""
import maya.cmds as cmds
import maya.mel as mel

modulePath = cmds.getModulePath(moduleName='MY_Tools_2023')

mel.eval('source "{}/scripts/ScriptPackages/AOVsArnoldMasker.mel";'.format(modulePath))