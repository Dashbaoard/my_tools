# _*_ coding: utf-8 _*_
# .@FileName:polySphere
# .@Date....:2023-09-03-17 : 29 : 15
# .@Aurhor..:冥羽
# .@Contact.:1942598111@qq.com
'''
launch:
        import pSphere as kt_FileName
        reload(FileName)
        FileName.main()
'''
# this text can be entered from the script editor and can be made into a button

import maya.cmds as cmds
import maya.mel as mel


class MainClassBadGeo:

    def __init__(self):

        self.bG_output = ""

        # C H E C K  W I N D O W

        # UI Width宽度
        sizeX = 240
        version = "v1.0"# 版本
        # 检查窗口，如果在程序在运行，关闭它
        if cmds.window("igEzRenameWin", exists=True):
            cmds.deleteUI("igEzRenameWin", window=True)
            cmds.windowPref("igEzRenameWin", r=True)  # 删除窗口首选项

        # 创建 UI 标题tool  宽 高   最小化  最大化  调整大小
        igEzRenamWin = cmds.window("igEzRenameWin", title="ig Easy Rename Tool " + version, width=sizeX * 2.5, height=385,
                                   mnb=True, mxb=False, sizeable=True)

        # 创建接口元素   布局  高度  跟随大小   两边边缘
        mainLayout = cmds.columnLayout("mainColumnLayout", width=sizeX, adjustableColumn=True, co=["both", 2])

        # 选择所有的表单按钮
        cmds.separator(h=5, style="none", parent=mainLayout)# 分隔符   高度   样式   父布局
        cmds.button(label=u"选择所有", w=sizeX, h=25, c=self.SelectAll, ann="Select ALL objects in scene")#按钮  宽度  高度    命令    注释
        cmds.separator(h=5, style="none", parent=mainLayout)# 分隔符   高度   样式   父布局

        # 按名称选择   球
        cmds.rowColumnLayout(numberOfRows=1, w=sizeX, parent=mainLayout, rowHeight=[(1, 25), (2, 60)], cs=[(5, 5), (5, 5)])# 布局   行数    宽度   父布局    行高度   列间距
        cmds.button(label=u"球", w=sizeX / 3, h=25, c=self.PSphere, align="center", ann="Select objects by name")#按钮  宽度   高度   命令    居中     注释
        cmds.text(label=u"半径：", font="boldLabelFont", w=sizeX / 6, align="center")
        self.radius = cmds.textField(w=sizeX * 0.2,
                                    ann="Select by Name \n Use * after and/or before the text to select by prefix/suffix \n Example: *_grp")#文本控件   宽度    注释
        cmds.text(label=u"轴向细分：", font="boldLabelFont", w=sizeX / 4, align="center")
        self.SubdivisionsX = cmds.textField(w=sizeX * 0.2,
                                            ann="Select by Name \n Use * after and/or before the text to select by prefix/suffix \n Example: *_grp")  # 文本控件   宽度    注释
        cmds.text(label=u"高度细分：", font="boldLabelFont", w=sizeX / 4, align="center")
        self.SubdivisionsY = cmds.textField(w=sizeX * 0.2,
                                         ann="Select by Name \n Use * after and/or before the text to select by prefix/suffix \n Example: *_grp")  # 文本控件   宽度    注释
        cmds.text(label=u"创建UV：", font="boldLabelFont", w=sizeX / 4, align="center")

        cmds.separator(w=sizeX, h=15, style="in", parent=mainLayout)# 横线



        cmds.rowColumnLayout(numberOfRows=1, w=sizeX, parent=mainLayout, rowHeight=[(1, 25), (2, 60)],
                             cs=[(5, 5), (5, 5)])  # 布局   行数    宽度   父布局    行高度   列间距
        cmds.button(label=u"纹理贴图", w=sizeX / 3, h=25, c=self.ConSolidTx, align="center",
                    ann="Select objects by name")  # 按钮  宽度   高度   命令    居中     注释
        cmds.text(label=u"尺寸：", font="boldLabelFont", w=sizeX / 6, align="center")
        self.SizeTest = cmds.textField(w=sizeX * 0.2,
                                     ann="Select by Name \n Use * after and/or before the text to select by prefix/suffix \n Example: *_grp")  # 文本控件   宽度    注释
        cmds.text(label=u"UV：", font="boldLabelFont", w=sizeX / 4, align="center")
        self.BackgroundModeTest = cmds.textField(w=sizeX * 0.2,
                                            ann="Select by Name \n Use * after and/or before the text to select by prefix/suffix \n Example: *_grp")  # 文本控件   宽度    注释
        cmds.text(label=u"格式：", font="boldLabelFont", w=sizeX / 4, align="center")
        self.FileFormatTest = cmds.textField(w=sizeX * 0.2,
                                            ann="Select by Name \n Use * after and/or before the text to select by prefix/suffix \n Example: *_grp")  # 文本控件   宽度    注释

        cmds.separator(w=sizeX, h=15, style="in", parent=mainLayout)  # 横线
        # Show UI:
        cmds.showWindow(igEzRenamWin)# 显示窗口

    def SelectAll(*args):
        cmds.select(ado=True, hi=True)  # 选择所有不能删除的对象，和他的子集
        selection = cmds.ls(selection=True, sn=True)  # 列出所有选中的，简单的名字
        selectionAdd = []  # 创建一个空列表

    def PSphere(self, *args):
        Sphere_radius = cmds.textField(self.radius, tx=1, q=True)
        SubdivisionsX = cmds.textField(self.SubdivisionsX, tx=1, q=True)
        SubdivisionsY = cmds.textField(self.SubdivisionsY, text=1, q=True)
        SY_digits = SubdivisionsY.isdigit()
    #    while not SY_digits:
    #        print("输入的文本不是一个有效的数字，请重新输入。")
    #        SubdivisionsY = cmds.textField(SelectName, text=1, q=True)
    #        SY_digits = SubdivisionsY.isdigit()

    #    if SY_digits == True:
    #        cmds.polySphere(sx=10, sy=int(SubdivisionsY), r=20)
    #    else:
    #        print("输入的文本不是一个有效的数字，请重新输入。")
        if Sphere_radius == "":
            Sphere_radius = 1
        if SubdivisionsX == "":
            SubdivisionsX = 20
        if SubdivisionsY == "":
            SubdivisionsY = 20
        try:
            cmds.polySphere(sx=int(SubdivisionsX), sy=int(SubdivisionsY), r=int(Sphere_radius))
        except:
            print("输入的文本不是一个有效的数字，请重新输入。")

    def ConSolidTx(self, *args):

        TxSize = cmds.textField(self.SizeTest, tx=1, q=True)
        TxSize_digits = TxSize.isdigit()

        FilFormat = cmds.textField(self.FileFormatTest, tx=1, q=True)
        FilFormat_digits = FilFormat.isdigit()

        UVBm = cmds.textField(self.BackgroundModeTest, tx=1, q=True)
        UVBM_digits = UVBm.isdigit()

        selection = cmds.ls(selection=True, sn=True)
        if TxSize_digits == False:
            TxSize = 2048

        if UVBM_digits == False:
            UVBm = 3

        if FilFormat_digits == False:
            FilFormat ="tif"

        try:
            cmds.convertSolidTx(selection[0], selection[1], rx=int(TxSize), ry=int(TxSize), bm=int(UVBm), fil=str(FilFormat))

        except:
            print("输入的文本不是一个有效的数字，请重新输入。")

MCBG = MainClassBadGeo()
#MCBG.badGeoUI()