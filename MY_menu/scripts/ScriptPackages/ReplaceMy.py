# _*_ coding: utf-8 _*_
# .@FileName:ReplaceMy
# .@Date....:2023-09-16-17 : 29 : 15
# .@Aurhor..:冥羽
# .@Contact.:1942598111@qq.com

import maya.cmds as cmds
import maya.mel as mel


class MyWindow(object):

    def __init__(self):

        # C H E C K  W I N D O W

        # UI Width宽度
        sizeX = 240
        version = "v1.0"# 版本
        # 检查窗口，如果在程序在运行，关闭它
        if cmds.window("ReplaceMy", exists=True):
            cmds.deleteUI("ReplaceMy", window=True)
            cmds.windowPref("ReplaceMy", r=True)  # 删除窗口首选项

        # 创建 UI 标题tool  宽 高   最小化  最大化  调整大小
        ReplaceMy = cmds.window("ReplaceMy", title="ReplaceMyTool " + version, width=sizeX, height=200,
                                   mnb=True, mxb=False, sizeable=True)

        # 创建接口元素   布局  高度  跟随大小   两边边缘
        mainLayout = cmds.columnLayout("mainColumnLayout", width=sizeX, adjustableColumn=True, co=["both", 2])

        cmds.text(label=u"使用前先保存文件", font="boldLabelFont", h=30, align="center")

        cmds.button(label=u"mod", w=sizeX, h=25, c=self.GetNewMod, ann=u"选择新的模型")
        self.NewModSumTest = cmds.textField(w=sizeX * 0.5, en=False, ann=u"新模型的数量", tx=0)

        cmds.button(l=u"lay", w=sizeX, h=25, c=self.GetOldMod, ann=u"选择旧的模型")
        self.OldModSumTest = cmds.textField(w=sizeX * 0.5, en=False, ann=u"旧模型的数量", tx=0)

        cmds.button(l=u"移动", w=sizeX, h=25, c=self.MatchTransformCnn, ann=u"先保存文件，然后点就完了")
        
        cmds.button(l=u"1对1", w=sizeX, h=25, c=self.MatchTransOneCnn, ann=u"先选原点的，再选择位置上的")
        
        # Show UI:
        cmds.showWindow(ReplaceMy)# 显示窗口

        self.NewMod = []
        self.OldMod = []
        self.SunMod = 0

    def GetNewMod(self, *args):
        self.NewMod = cmds.ls(selection=True, sn=True)
        NewModSum = len(self.NewMod)
        NewModSumTest = cmds.textField(self.NewModSumTest, tx=NewModSum, e=True)

        return self.NewMod

    def GetOldMod(self, *args):
        self.OldMod = cmds.ls(selection=True, sn=True)
        OldModSum = len(self.OldMod)
        self.SunMod = OldModSum

        NewModSumTest = cmds.textField(self.OldModSumTest, tx=OldModSum, e=True)

        return self.OldMod

    def MatchTransformCnn(self, *args):
        Sub = 0
        i = 1
        while i <= self.SunMod:
            cmds.matchTransform(self.NewMod[Sub], self.OldMod[Sub])
            Sub = Sub + 1
            i += 1

    def MatchTransOneCnn(self, *args):
        cmds.matchTransform()


MCBG = MyWindow()
