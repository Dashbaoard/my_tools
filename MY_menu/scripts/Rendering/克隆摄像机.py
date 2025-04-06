# _*_ coding: utf-8 _*_
# .@FileName:克隆摄像机
# .....:2022-09-24 : 07 :30
# .@Aurhor..:MingYu
# .@Contact.:1942598111@qq.com
"""
launch :
        import 克隆摄像机 as kt_FileName
        import importlib.reload as relaad
        reload(FileName)
        FileName.main()
"""
import maya.cmds as cmds
import maya.mel as mel

modulePath = cmds.getModulePath(moduleName='MY_Tools_2023')

mel.eval('source "{}/scripts/ScriptPackages/克隆摄像机.mel";'.format(modulePath))

#mel.eval('D:\zjd\maya\chajian\hezi\MY_menu\scripts\Rendering\克隆摄像机.mel')