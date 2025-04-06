# _*_ coding: utf-8 _*_
# .@FileName:ReplaceMaterial
# .@Date....:2023-12-16-14 : 30 : 20
# .@Aurhor..:冥羽
# .@Contact.:1942598111@qq.com
'''
launch:
        import ReplaceMaterial as kt_FileName
        reload(FileName)
        FileName.main()
'''
import maya.cmds as cmds


class MyWindow(object):

    def __init__(self):

        # C H E C K  W I N D O W

        # UI Width宽度
        sizeX = 250
        version = "v1.0"# 版本
        # 检查窗口，如果在程序在运行，关闭它
        if cmds.window("ReplaceCam", exists=True):
            cmds.deleteUI("ReplaceCam", window=True)
            cmds.windowPref("ReplaceCam", r=True)  # 删除窗口首选项

        # 创建 UI 标题tool  宽 高   最小化  最大化  调整大小
        ReplaceCam = cmds.window("ReplaceCam", title="Replace Cam Tool " + version, width=sizeX, 
                                   mnb=True, mxb=False, sizeable=True)

        # 创建接口元素   布局  高度  跟随大小   两边边缘
        mainLayout = cmds.columnLayout("mainColumnLayout", width=sizeX/4, adjustableColumn=True, co=["both", 2])


        cmds.text(label=u"复制相机", font="boldLabelFont", h=30, align="center")
        cmds.text(l="  ", h=30)

        cmds.button(l='复制相机', c=self.reload, w=170, ann='选择要复制的相机')
        
        # Show UI:
        cmds.showWindow(ReplaceCam)# 显示窗口


    def reload(self,*args):
        CamSl=cmds.ls(selection=True, sn=True)
        cmds.duplicate()
        cmds.Unparent()
        CamNew=cmds.ls(selection=True, sn=True)
        cmds.parentConstraint(CamSl,CamNew, n='CamNewAA')
        cmds.BakeSimulation(CamNew)
        cmds.delete('CamNewAA')
        if cmds.findKeyframe(CamSl,at='focalLength',c=True) != None:
            cmds.copyKey( CamSl, attribute='focalLength', option="curve" )
            cmds.pasteKey(CamNew, attribute='focalLength')
MyWindow()