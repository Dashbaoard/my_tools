# _*_ coding: utf-8 _*_
# .@FileName:HZrig_controllers
# .....:2022-09-13 : 23 :14
# .@Aurhor..:MingYu
# .@Contact.:1942598111@qq.com
"""
launch :
        import HZrig_controllers as kt_FileName
        reload(FileName)
        FileName.main()
"""
import maya.cmds as cmds
import maya.mel as mel

modulePath = cmds.getModulePath(moduleName='MY_Tools_2023')

mel.eval('source "{}/scripts/ScriptPackages/HZrig_controller/HZrig_controllers_UI.mel";'.format(modulePath))