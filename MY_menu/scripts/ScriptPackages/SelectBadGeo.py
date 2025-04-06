# SelectBadGeo v1.1
# License: MIT Licence (See LICENSE.txt or https://choosealicense.com/licenses/mit/)
# Copyright (c) 2017 Erik Lehmann
# Date: 01/16/18
#
# Description: 
#	Select Triangles, Quads, N-Gons, Concave, Hole, Lamina and Non Manifold geometry.
# 
# How to use:
#	1. Select object(s).
#	2. Choose geometry type.
#
# Installation: 
# 	1. 	Copy BadGeo.py to '\Users\[USER]\Documents\maya\[MAYAVERSION]\prefs\scripts'
# 	2. 	Launch / Restart Maya
#	3.	Type into 'Script Editor' (Python tab) and execute:
#       import SelectBadGeo as BG
#       MCBG = BG.MainClassBadGeo()
#       MCBG.badGeoUI()


import maya.cmds as cmds
import maya.mel as mel


class MainClassBadGeo:

    def __init__(self):
        self.bG_output = ""

    def badGeoUI(self):

        # C H E C K  W I N D O W

        if (cmds.window("bGWin", exists=True)):  # 如果窗口存在
            cmds.deleteUI("bGWin", wnd=True)  # 关闭窗口
            cmds.windowPref("bGWin", r=True)  # 删除窗口首选项

        # C R E A T E  U I

        cmds.window("bGWin", s=False, tlb=True, rtf=True, t="Select Bad Geometry",
                    w=145)  # 创建窗口， 名字    不可交互     样式    正好包裹    标题文本   宽度
        cmds.columnLayout(adj=True)  # 布局   单列   子工具在两侧

        # B A D  G E O M E T R Y 不利几何条件
        # 框架布局   标签   背景色     不可折叠    折叠状态   宽度
        cmds.frameLayout(label=("Geometry Type"), bgc=(0.3, 0.3, 0.3), collapsable=False, collapse=False, w=120)

        cmds.columnLayout(adj=True)  # 布局   单列   子工具在两侧

        cmds.button(label="Triangles", h=25, c=self.bGTriangles)  # 按钮    标签    高度    命令
        cmds.button(label="Quads", h=25, c=self.bGQuads)  # 按钮    标签     高度    命令
        cmds.button(label="N-Gons", h=25, c=self.bGNGons)  # 按钮    标签     高度    命令
        cmds.button(label="Concave", h=25, c=self.bGConcave)  # 按钮    标签     高度    命令
        cmds.button(label="Lamina", h=25, c=self.bGLamina)  # 按钮    标签     高度    命令
        cmds.button(label="Holes", h=25, c=self.bGHole)  # 按钮    标签     高度    命令
        cmds.button(label="Non-Manifold", h=25, c=self.bGNonM)  # 按钮    标签     高度    命令

        cmds.setParent("..")  # 在层次结构中向上移动一级。
        cmds.setParent("..")  # 在层次结构中向上移动一级。

        # O U T P U T

        cmds.frameLayout(label='Output', bgc=(0.3, 0.3, 0.3), collapsable=False,
                         collapse=True)  # 框架布局   标签   背景色     不可折叠    折叠状态

        self.bG_output = cmds.textField(h=25, bgc=(0.16, 0.16, 0.16), en=True, ed=False)  # 文本框  高度   背景色    启用    只读

        cmds.setParent("..")
        cmds.setParent("..")

        # S H O W  W I N D O W

        cmds.showWindow("bGWin")  # 显示窗口

    # M E T H O D S 方法

    # T R I A N G L E S

    def bGTriangles(self, _=False):
        bGsel = cmds.ls(sl=True)  # 选择的物体

        # Change to Component mode to retain object highlighting for better visibility  更改为组件模式以保留对象高亮显示以获得更好的可见性
        cmds.selectMode(q=True, co=True)  # 组件模式

        # Select Object/s and Run Script to highlight Triangles
        cmds.polySelectConstraint(m=3, t=0x0008, sz=1)  # 所有满足约束条件的项目都会被选中。     类型为面    三角面          只能选择这个
        cmds.polySelectConstraint(dis=True)  # 取消约束

        # Update Textfield  
        bGPolys = cmds.polyEvaluate(fc=True)  # 返回选择的面数

        try:
            cmds.textField(self.bG_output, e=True, tx=("{} Triangle(s)".format(int(bGPolys))))  # 文本框  编辑    文本为数值面数   # Triangle
        except:
            cmds.textField(self.bG_output, e=True, tx=("Nothing is selected."))  # 否则

    # Q U A D S  四边面

    def bGQuads(self, _=False):
        bGsel = cmds.ls(sl=True)

        cmds.selectMode(q=True, co=True)

        cmds.polySelectConstraint(m=3, t=0x0008, sz=2)
        cmds.polySelectConstraint(dis=True)

        bGPolys = cmds.polyEvaluate(fc=True)

        try:
            cmds.textField(self.bG_output, e=True, tx=("%s Quad(s)" % int(bGPolys)))
        except:
            cmds.textField(self.bG_output, e=True, tx=("Nothing is selected."))

    # N - G O N S   多边面

    def bGNGons(self, _=False):
        bGsel = cmds.ls(sl=True)

        cmds.selectMode(q=True, co=True)

        cmds.polySelectConstraint(m=3, t=0x0008, sz=3)
        cmds.polySelectConstraint(dis=True)

        bGPolys = cmds.polyEvaluate(fc=True)

        try:
            cmds.textField(self.bG_output, e=True, tx=("%s N-Gon(s)" % int(bGPolys)))
        except:
            cmds.textField(self.bG_output, e=True, tx=("Nothing is selected."))

    # C O N C A V E

    def bGConcave(self, _=False):

        bGsel = cmds.ls(sl=True)

        cmds.selectMode(q=True, co=True)

        cmds.polySelectConstraint(m=3, t=0x0008, c=1)
        cmds.polySelectConstraint(dis=True)

        bGPolys = cmds.polyEvaluate(fc=True)

        try:
            cmds.textField(self.bG_output, e=True, tx=("%s Concave(s)" % int(bGPolys)))
        except:
            cmds.textField(self.bG_output, e=True, tx=("Nothing is selected."))

    # L A M I N A

    def bGLamina(self, _=False):
        bGsel = cmds.ls(sl=True)

        cmds.selectMode(q=True, co=True)

        p = cmds.polyInfo(lf=True)

        if p == None:
            bGPolys = 0
            cmds.select(d=True)
        else:
            cmds.select(p)
            bGPolys = cmds.polyEvaluate(fc=True)

        try:
            cmds.textField(self.bG_output, e=True, tx=("%s Lamina" % int(bGPolys)))
        except:
            cmds.textField(self.bG_output, e=True, tx=("Nothing is selected."))

    # H O L E S

    def bGHole(self, _=False):
        bGsel = cmds.ls(sl=True)

        cmds.selectMode(q=True, co=True)

        cmds.polySelectConstraint(m=3, t=0x0008, h=1)
        cmds.polySelectConstraint(dis=True)

        bGPolys = cmds.polyEvaluate(fc=True)

        try:
            cmds.textField(self.bG_output, e=True, tx=("%s Hole(s)" % int(bGPolys)))
        except:
            cmds.textField(self.bG_output, e=True, tx=("Nothing is selected."))

    # N O N - M A N I F O L D

    def bGNonM(self, _=False):
        bGsel = cmds.ls(sl=True)

        cmds.selectMode(q=True, co=True)

        bGPolys = mel.eval(
            'polyCleanupArgList 4 { "0","2","1","0","0","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","1","0","0" };')

        bGCount = 0

        for i in bGPolys:
            bGCount = bGCount + 1

        cmds.select(bGPolys)

        try:
            cmds.textField(self.bG_output, e=True, tx=("%s Non-Manifold(s)" % bGCount))
        except:
            cmds.textField(self.bG_output, e=True, tx=("Nothing is selected."))

# MCBG = MainClassBadGeo()
# MCBG.badGeoUI()
