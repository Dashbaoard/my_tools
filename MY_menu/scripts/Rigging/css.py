# _*_ coding: utf-8 _*_
# .@FileName:css
# .....:2022-09-22 : 00 :48
# .@Aurhor..:MingYu
# .@Contact.:1942598111@qq.com
"""
launch :
        import css as kt_FileName
        import importlib.reload as reload
        reload(FileName)
        FileName.main()
"""
import maya.cmds as cmds
import maya.mel as mel

modulePath = cmds.getModulePath(moduleName='MY_Tools_2023')

mel.eval('source "{}/scripts/ScriptPackages/css.mel";'.format(modulePath))