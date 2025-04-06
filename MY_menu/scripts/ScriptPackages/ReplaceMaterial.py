# _*_ coding: utf-8 _*_
# .@FileName:ReplaceMaterial
# .@Date....:2023-10-14-14 : 30 : 20
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
        sizeX = 240
        version = "v1.0"# 版本
        # 检查窗口，如果在程序在运行，关闭它
        if cmds.window("ReplaceMaterial", exists=True):
            cmds.deleteUI("ReplaceMaterial", window=True)
            cmds.windowPref("ReplaceMaterial", r=True)  # 删除窗口首选项

        # 创建 UI 标题tool  宽 高   最小化  最大化  调整大小
        ReplaceMaterial = cmds.window("ReplaceMaterial", title="Replace material Tool " + version, width=sizeX, height=200,
                                   mnb=True, mxb=False, sizeable=True)

        # 创建接口元素   布局  高度  跟随大小   两边边缘
        mainLayout = cmds.columnLayout("mainColumnLayout", width=sizeX, adjustableColumn=True, co=["both", 2])

        cmds.text(label=u"需要一样的模型内容", font="boldLabelFont", h=30, align="center")
        cmds.text(label=u"先选择对的材质模型组", font="boldLabelFont", h=30, align="center")
        cmds.text(label=u"后选择对的动画模型组", font="boldLabelFont", h=30, align="center")

        cmds.button(label=u"替换材质", w=sizeX, h=25, c=self.ReplaceSder, ann=u"先选择对的材质模型，后选择对的动画模型")

        # Show UI:
        cmds.showWindow(ReplaceMaterial)# 显示窗口

    def ReplaceSder(self, *args):
        aaa = cmds.ls(selection=True, sn=True)
        cmds.select(aaa[0])
        mod = cmds.ls(sl=1, dag=1, type="mesh")
        Pshader = cmds.listConnections(mod, type="shadingEngine")
        PShaderList = list(set(Pshader))
        PShaderList = [x for x in PShaderList if x != 'initialShadingGroup']
        for PShaderLs in PShaderList:
            rrr = []
            PShader = cmds.select(PShaderLs)
            facename = cmds.ls(selection=True, sn=True)
            print(facename)
            for Oldname in facename:
                Newname = Oldname.replace(aaa[0], aaa[1])
                print(Newname)
                rrr.append(Newname)
            print(rrr)
            cmds.select(rrr)
            cmds.hyperShade(assign=PShaderLs)
MyWindow()