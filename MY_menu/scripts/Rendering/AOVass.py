# -*- coding: utf-8 -*-
import os, sys, functools
from PySide2 import QtCore, QtGui, QtWidgets
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from maya import cmds, mel

rendersetup_static = True
try:
    import maya.app.renderSetup.model.override as override
    import maya.app.renderSetup.model.plug as plug
    import maya.app.renderSetup.model.utils as utils
    import maya.app.renderSetup.model.typeIDs as typeIDs
    import maya.app.renderSetup.model.selector as selector
    import maya.app.renderSetup.model.collection as collection
    import maya.app.renderSetup.model.renderLayer as renderLayer
    import maya.app.renderSetup.model.renderSetup as renderSetup
    import maya.app.renderSetup.model.connectionOverride as connectionOverride
except:
    cmds.confirmDialog(title=u'警告!!', icon='question', message=u'未找到Render Setup库\n可能Maya版本过低\n将禁用Render Setup',
                       button=[u'关闭'])
    rendersetup_static = False


def mayaMainWindows():
    mainWindowsPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindowsPtr), QtWidgets.QWidget)


class Ui_Aov_Management_Tool(object):
    ############################################################################################################################
    #
    #         UI
    #
    ############################################################################################################################
    def setupUi(self, Aov_Management_Tool):
        Aov_Management_Tool.setObjectName("Aov_Management_Tool")# 窗口名称
        Aov_Management_Tool.resize(300, 600)# 窗口尺寸
        self.verticalLayout = QtWidgets.QVBoxLayout(Aov_Management_Tool)#垂直布局
        self.verticalLayout.setObjectName("verticalLayout")#布局名称
        self.widget = QtWidgets.QWidget(Aov_Management_Tool)#创建一个部件
        self.widget.setMaximumSize(QtCore.QSize(16777215, 30))#部件最大尺寸
        self.widget.setObjectName("widget")#部件名称
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)#水平布局 在部件里面
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)#布局的目录边缘大小（默认值）
        self.horizontalLayout.setObjectName("horizontalLayout")#布局名称
        self.label = QtWidgets.QLabel(self.widget)#创建一个标签 在部件里面
        self.label.setMaximumSize(QtCore.QSize(16777215, 30))#标签最大尺寸
        self.label.setObjectName("label")#标签名称
        self.horizontalLayout.addWidget(self.label)
        self.renderlayer_radiobutton = QtWidgets.QRadioButton(self.widget)#创建一个单选按钮 在部件里面
        self.renderlayer_radiobutton.setMaximumSize(QtCore.QSize(16777215, 30))#按钮的最大尺寸
        self.renderlayer_radiobutton.setChecked(True)#按钮默认打开
        self.renderlayer_radiobutton.setObjectName("renderlayer_radiobutton")#按钮名称
        self.horizontalLayout.addWidget(self.renderlayer_radiobutton)
        self.rendersetup_radiobutton = QtWidgets.QRadioButton(self.widget)#创建一个单选按钮 在部件里面
        self.rendersetup_radiobutton.setMaximumSize(QtCore.QSize(16777215, 30))#按钮的最大尺寸
        self.rendersetup_radiobutton.setObjectName("rendersetup_radiobutton")#按钮名称
        self.horizontalLayout.addWidget(self.rendersetup_radiobutton)#
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(Aov_Management_Tool)#创建一个部件
        self.widget_2.setMaximumSize(QtCore.QSize(16777215, 30))#部件最大尺寸
        self.widget_2.setObjectName("widget_2")#部件名称
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)#水平布局 在部件里面
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)#布局的目录边缘大小（默认值）
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")#布局名称
        self.label_2 = QtWidgets.QLabel(self.widget_2)#创建一个标签 在部件里面
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 30))#标签最大尺寸
        self.label_2.setObjectName("label_2")#标签名称
        self.horizontalLayout_2.addWidget(self.label_2)
        self.arnold_radiobutton = QtWidgets.QRadioButton(self.widget_2)#创建一个单选按钮 在部件里面
        self.arnold_radiobutton.setMaximumSize(QtCore.QSize(16777215, 30))#按钮的最大尺寸
        self.arnold_radiobutton.setChecked(True)#按钮默认打开
        self.arnold_radiobutton.setObjectName("arnold_radiobutton")#按钮名称
        self.horizontalLayout_2.addWidget(self.arnold_radiobutton)#
        self.redshift_radiobutton = QtWidgets.QRadioButton(self.widget_2)#创建一个单选按钮 在部件里面
        self.redshift_radiobutton.setMaximumSize(QtCore.QSize(16777215, 30))#按钮的最大尺寸
        self.redshift_radiobutton.setObjectName("redshift_radiobutton")#按钮名称
        self.horizontalLayout_2.addWidget(self.redshift_radiobutton)#
        self.verticalLayout.addWidget(self.widget_2)#
        self.refresh_button = QtWidgets.QPushButton(Aov_Management_Tool)#创建一个按钮
        self.refresh_button.setMaximumSize(QtCore.QSize(16777215, 50))#按钮的最大尺寸
        self.refresh_button.setObjectName("refresh_button")#按钮名称
        self.verticalLayout.addWidget(self.refresh_button)#按钮放入垂直布局
        self.listWidget = QtWidgets.QListWidget(Aov_Management_Tool)#创建一个显示框
        self.listWidget.setObjectName("listWidget")#显示框名称
        self.verticalLayout.addWidget(self.listWidget)#显示框放入垂直布局

        ####################################################
        # 是否禁用rendersetup
        self.rendersetup_radiobutton.setEnabled(rendersetup_static)#不禁用第二个按钮
        # 设置窗口flags
        self.setWindowFlags(QtCore.Qt.Window)#表示这个一个独立的窗口
        # 右键
        self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)#可以右击
        self.listWidget.customContextMenuRequested.connect(self.showChrMenu)#右击链接窗口
        self.createRightMenu()#右击菜单
        # 多选
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # icon
        iconwh = self.listWidget.iconSize()#显示框图标大小
        iconwh.setWidth(50)#显示框图标宽
        iconwh.setHeight(50)#显示框图标高
        self.listWidget.setIconSize(iconwh)#指认上

        ####################################################
        self.ui_ctrl()#
        self.retranslateUi(Aov_Management_Tool)
        QtCore.QMetaObject.connectSlotsByName(Aov_Management_Tool)

    ############################################################################################################################
    #
    #         UI文字设置
    #
    ############################################################################################################################
    def retranslateUi(self, Aov_Management_Tool):
        Aov_Management_Tool.setWindowTitle(u"Aov管理工具--小静")#窗口命名
        self.label.setText(u"渲染模式：")#标签内容
        self.rendersetup_radiobutton.setText(u"Render Setup")#按钮命名
        self.renderlayer_radiobutton.setText(u"Render Layer")#按钮命名
        self.label_2.setText(u"渲染器：")#标签内容
        self.arnold_radiobutton.setText(u"Arnold")#按钮命名
        self.redshift_radiobutton.setText(u"Redshift")#按钮命名
        self.refresh_button.setText(u"刷新")#按钮命名

    ############################################################################################################################
    #
    # 控制函数
    #
    ############################################################################################################################
    def ui_ctrl(self):
        self.refresh_button.clicked.connect(self.refresh_aov)#大按钮链接方法
        self.listWidget.itemDoubleClicked.connect(self.select_aov_nodes)#显示框链接用法

    ############################################################################################################################
    #
    # 右键菜单
    #
    ############################################################################################################################
    def createRightMenu(self):
        '''''
        创建右键菜单
        '''
        self.ChrMenu = QtWidgets.QMenu(self)#创建一个菜单
        self.menuitemA = self.ChrMenu.addAction(u'Select')#创建一个行为和命名
        self.ChrMenu.addSeparator()#加一个横条
        self.menuitemB = self.ChrMenu.addAction(u'On')#创建一个行为和命名
        self.menuitemC = self.ChrMenu.addAction(u'Off')#创建一个行为和命名
        self.ChrMenu.addSeparator()#加一个横条
        self.menuitemD = self.ChrMenu.addAction(u'Overrides_On')#创建一个行为和命名
        self.menuitemE = self.ChrMenu.addAction(u'Overrides_Off')#创建一个行为和命名
        self.ChrMenu.addSeparator()#加一个横条
        self.menuitemF = self.ChrMenu.addAction(u'Delete_Overrides')#创建一个行为和命名
        self.menuitemG = self.ChrMenu.addAction(u'Delete_Aov')#创建一个行为和命名
        self.ChrMenu.addSeparator()#加一个横条
        #
        self.menuitemA.triggered.connect(self.select_aov_nodes)#选择选中的aov
        self.menuitemB.triggered.connect(functools.partial(self.set_aov_state, True))
        self.menuitemC.triggered.connect(functools.partial(self.set_aov_state, False))
        self.menuitemD.triggered.connect(functools.partial(self.set_overrides_aov, True, True))
        self.menuitemE.triggered.connect(functools.partial(self.set_overrides_aov, False, True))
        self.menuitemF.triggered.connect(self.delete_overrides)
        self.menuitemG.triggered.connect(self.delete_aov)

    def showChrMenu(self):
        self.ChrMenu.exec_(QtGui.QCursor().pos())

    ############################################################################################################################
    #
    # 回调函数
    #
    ############################################################################################################################

    ############################################################################################################################
    #
    # 执行函数
    #
    ############################################################################################################################
    # Refresh_Aov
    def refresh_aov(self):
        # 类型
        render_type = ""
        if self.arnold_radiobutton.isChecked():
            render_type = "aiAOV"
        elif self.redshift_radiobutton.isChecked():
            render_type = "RedshiftAOV"
        # 清除listwidget
        Oldlist = self.listWidget.count()
        if Oldlist:
            self.listWidget.clear()
        # refresh
        if self.renderlayer_radiobutton.isChecked():
            for aov_node in cmds.ls(type=render_type):
                icon = QtGui.QIcon()
                item = QtWidgets.QListWidgetItem(self.listWidget)
                item.setText(cmds.getAttr(aov_node + '.name'))
                # icon
                if cmds.getAttr(aov_node + '.enabled') == 1:
                    icon.addPixmap(QtGui.QPixmap(":\hyper_s_ON.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                else:
                    icon.addPixmap(QtGui.QPixmap(":\hyper_s_OFF.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item.setIcon(icon)
                # bgc
                all_override_attr = cmds.editRenderLayerAdjustment(cmds.editRenderLayerGlobals(q=1, crl=1), q=1, lyr=1)
                if all_override_attr and (aov_node + ".enabled") in all_override_attr:  # 如果属性在层覆盖属性中
                    item.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 0, a=50)))  # 255,255,0,a=50
                # add
                self.listWidget.addItem(item)
        elif self.rendersetup_radiobutton.isChecked():
            sel_renderlayer = renderSetup.instance().getVisibleRenderLayer().name()
            # 所有renderlayer
            all_renderlayer_obj = renderSetup.instance().getRenderLayers()
            all_renderlayer_list = []
            for i in all_renderlayer_obj:
                all_renderlayer_list.append(i.name())

            for aov_node in cmds.ls(type=render_type):
                icon = QtGui.QIcon()
                item = QtWidgets.QListWidgetItem(self.listWidget)
                item.setText(cmds.getAttr(aov_node + '.name'))
                # icon
                if cmds.getAttr(aov_node + '.enabled') == 1:
                    icon.addPixmap(QtGui.QPixmap(":\hyper_s_ON.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                else:
                    icon.addPixmap(QtGui.QPixmap(":\hyper_s_OFF.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

                # bgc
                if sel_renderlayer in all_renderlayer_list:  # 如果切换了renderlayer
                    aovs_collection_on = sel_renderlayer + '_Aov_overrides_On'
                    aovs_collection_off = sel_renderlayer + '_Aov_overrides_Off'
                    # 获取当前renderlayer所有collection
                    all_collection_list = []
                    all_collection_obj = renderSetup.instance().getRenderLayer(sel_renderlayer).getCollections()
                    for i in all_collection_obj:
                        all_collection_list.append(i.name())
                    if aovs_collection_on in all_collection_list:  # 如果有Aov_overrides_On
                        target_collection = renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                            aovs_collection_on)
                        aovs_in_collection = target_collection.getSelector().staticSelection.asList()
                        if aov_node in aovs_in_collection:
                            icon.addPixmap(QtGui.QPixmap(":\hyper_s_ON.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                            item.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 0, a=50)))
                    if aovs_collection_off in all_collection_list:  # 如果有Aov_overrides_Off
                        target_collection = renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                            aovs_collection_off)
                        aovs_in_collection = target_collection.getSelector().staticSelection.asList()
                        if aov_node in aovs_in_collection:
                            icon.addPixmap(QtGui.QPixmap(":\hyper_s_OFF.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                            item.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 0, a=50)))

                item.setIcon(icon)
                # add
                self.listWidget.addItem(item)

    def set_listwidgetitem_style(self, line_num, bgc_bool):
        if bgc_bool:
            self.listWidget.item(line_num).setBackground(
                QtGui.QBrush(QtGui.QColor(255, 255, 0, a=50)))  # 255,255,0,a=50
        else:
            self.listWidget.item(line_num).setBackground(QtGui.QBrush(QtGui.QColor(0, 0, 0, a=0)))

    def set_listwidgetitem_icon(self, line_num, icon_bool):
        icon = QtGui.QIcon()
        if icon_bool:
            icon.addPixmap(QtGui.QPixmap(":\hyper_s_ON.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.listWidget.item(line_num).setIcon(icon)
        else:
            icon.addPixmap(QtGui.QPixmap(":\hyper_s_OFF.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.listWidget.item(line_num).setIcon(icon)

    def select_aov_nodes(self):
        select_node_list = []#创建一个空的选择的节点列表
        # 类型
        render_type = ""#创建一个空的类型
        if self.arnold_radiobutton.isChecked():
            render_type = "aiAOV"#如果按钮选择为aiAov，类型就为aiAov
        elif self.redshift_radiobutton.isChecked():
            render_type = "RedshiftAOV"#如果按钮选择为RedshiftAOV，类型就为RedshiftAOV

        for item in self.listWidget.selectedItems():#在选中的项目里循环
            for aov_node in cmds.ls(type=render_type):#选中的aov为当前的aov类型，进行循环
                if cmds.getAttr(aov_node + '.name') == item.text():
                    select_node_list.append(aov_node)#节点列表添加选中的aov类型
        cmds.select(select_node_list, r=1)#选择aov类型列表，替换之前的选择

    def set_aov_state(self, on_off):
        render_type = ""#创建一个空的类型
        if self.arnold_radiobutton.isChecked():
            render_type = "aiAOV"#如果按钮选择为aiAov，类型就为aiAov
        elif self.redshift_radiobutton.isChecked():
            render_type = "RedshiftAOV"#如果按钮选择为RedshiftAOV，类型就为RedshiftAOV

        for item in self.listWidget.selectedItems():
            line_num = self.listWidget.row(item)
            for aov_node in cmds.ls(type=render_type):
                if cmds.getAttr(aov_node + '.name') == item.text():
                    cmds.setAttr((aov_node + '.enabled'), on_off)
            self.set_listwidgetitem_icon(line_num, on_off)
            self.set_listwidgetitem_style(line_num, False)

    def set_overrides_aov(self, on_off, bgc_bool):
        render_type = ""
        if self.arnold_radiobutton.isChecked():
            render_type = "aiAOV"
        elif self.redshift_radiobutton.isChecked():
            render_type = "RedshiftAOV"

        if self.renderlayer_radiobutton.isChecked():
            for item in self.listWidget.selectedItems():
                line_num = self.listWidget.row(item)
                for aov_node in cmds.ls(type=render_type):
                    if cmds.getAttr(aov_node + '.name') == item.text():
                        cmds.editRenderLayerAdjustment(aov_node + '.enabled')
                        cmds.setAttr((aov_node + '.enabled'), on_off)
                self.set_listwidgetitem_icon(line_num, on_off)
                self.set_listwidgetitem_style(line_num, bgc_bool)
        elif self.rendersetup_radiobutton.isChecked():
            sel_renderlayer = renderSetup.instance().getVisibleRenderLayer().name()

            if sel_renderlayer == "defaultRenderLayer":
                cmds.confirmDialog(title=u'警告!!', icon='question', message=u'Render Setup不支持在defaultRenderLayer设置层覆盖',
                                   button=[u'关闭'])
                return

            # 所有renderlayer
            all_renderlayer_obj = renderSetup.instance().getRenderLayers()
            all_renderlayer_list = []
            for i in all_renderlayer_obj:
                all_renderlayer_list.append(i.name())
            # 创建collection
            aovs_collection_on = sel_renderlayer + '_Aov_overrides_On'
            aovs_collection_off = sel_renderlayer + '_Aov_overrides_Off'
            # 获取当前renderlayer所有collection
            all_collection_list = []
            all_collection_obj = renderSetup.instance().getRenderLayer(sel_renderlayer).getCollections()
            for i in all_collection_obj:
                all_collection_list.append(i.name())
            if not aovs_collection_on in all_collection_list:
                _cl = renderSetup.instance().getRenderLayer(sel_renderlayer).createCollection(aovs_collection_on)
                _cl.getSelector().setFilterType(8)
                _cl.getSelector().setCustomFilterValue(render_type)
                ov = _cl.createOverride("enable_on", typeIDs.absOverride)
                if cmds.ls(type=render_type):
                    ov.finalize(cmds.ls(type=render_type)[0] + ".enabled")
                    ov.setAttrValue(True)
                    cmds.setAttr("enable_on.atv", l=1)
            if not aovs_collection_off in all_collection_list:
                _cl = renderSetup.instance().getRenderLayer(sel_renderlayer).createCollection(aovs_collection_off)
                _cl.getSelector().setFilterType(8)
                _cl.getSelector().setCustomFilterValue(render_type)
                ov = _cl.createOverride("enable_off", typeIDs.absOverride)
                if cmds.ls(type=render_type):
                    ov.finalize(cmds.ls(type=render_type)[0] + ".enabled")
                    ov.setAttrValue(False)
                    cmds.setAttr("enable_off.atv", l=1)
            # 获取两个collection的所有aov
            aov_on_cllection = renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                aovs_collection_on)
            aov_on_list = aov_on_cllection.getSelector().staticSelection.asList()
            aov_off_cllection = renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                aovs_collection_off)
            aov_off_list = aov_off_cllection.getSelector().staticSelection.asList()
            # 查看collection的设置是否符合要求
            # aov on
            ov_list = aov_on_cllection.getOverrides()
            for ov in ov_list:
                if ov.typeName() == "absOverride" and ov.attributeName() == "enabled":
                    if not ov.getAttrValue():
                        cmds.setAttr("enable_on.atv", l=0)
                        cmds.setAttr("enable_on.atv", True)
                        cmds.setAttr("enable_on.atv", l=1)
                # aov off
            ov_list = aov_off_cllection.getOverrides()
            for ov in ov_list:
                if ov.typeName() == "absOverride" and ov.attributeName() == "enabled":
                    if ov.getAttrValue():
                        cmds.setAttr("enable_off.atv", l=0)
                        cmds.setAttr("enable_off.atv", False)
                        cmds.setAttr("enable_off.atv", l=1)
            # 移动aov所在的collection
            if on_off:
                for item in self.listWidget.selectedItems():
                    line_num = self.listWidget.row(item)
                    for aov_node in cmds.ls(type=render_type):
                        if cmds.getAttr(aov_node + '.name') == item.text():
                            if aov_node in aov_off_list:
                                # 移除collection  Off
                                renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                                    aovs_collection_off).getSelector().staticSelection.remove([aov_node])
                                # 添加collection   on
                                renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                                    aovs_collection_on).getSelector().staticSelection.add([aov_node])
                            else:
                                # 添加collection   on
                                renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                                    aovs_collection_on).getSelector().staticSelection.add([aov_node])
                    self.set_listwidgetitem_icon(line_num, on_off)
                    self.set_listwidgetitem_style(line_num, bgc_bool)
            else:
                for item in self.listWidget.selectedItems():
                    line_num = self.listWidget.row(item)
                    for aov_node in cmds.ls(type=render_type):
                        if cmds.getAttr(aov_node + '.name') == item.text():
                            if aov_node in aov_on_list:
                                # 移除collection  on
                                renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                                    aovs_collection_on).getSelector().staticSelection.remove([aov_node])
                                # 添加collection   off
                                renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                                    aovs_collection_off).getSelector().staticSelection.add([aov_node])
                            else:
                                # 添加collection   off
                                renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                                    aovs_collection_off).getSelector().staticSelection.add([aov_node])
                    self.set_listwidgetitem_icon(line_num, on_off)
                    self.set_listwidgetitem_style(line_num, bgc_bool)

    def delete_overrides(self):
        render_type = ""
        if self.arnold_radiobutton.isChecked():
            render_type = "aiAOV"
        elif self.redshift_radiobutton.isChecked():
            render_type = "RedshiftAOV"

        if self.renderlayer_radiobutton.isChecked():
            for item in self.listWidget.selectedItems():
                line_num = self.listWidget.row(item)
                for aov_node in cmds.ls(type=render_type):
                    if cmds.getAttr(aov_node + '.name') == item.text():
                        cmds.editRenderLayerAdjustment((aov_node + '.enabled'), remove=True)
                self.set_listwidgetitem_style(line_num, False)
        elif self.rendersetup_radiobutton.isChecked():
            sel_renderlayer = renderSetup.instance().getVisibleRenderLayer().name()
            # 所有renderlayer
            all_renderlayer_obj = renderSetup.instance().getRenderLayers()
            all_renderlayer_list = []
            for i in all_renderlayer_obj:
                all_renderlayer_list.append(i.name())
            # 创建collection
            aovs_collection_on = sel_renderlayer + '_Aov_overrides_On'
            aovs_collection_off = sel_renderlayer + '_Aov_overrides_Off'
            # 获取当前renderlayer所有collection
            all_collection_list = []
            all_collection_obj = renderSetup.instance().getRenderLayer(sel_renderlayer).getCollections()
            for i in all_collection_obj:
                all_collection_list.append(i.name())
            if not aovs_collection_on in all_collection_list:
                _cl = renderSetup.instance().getRenderLayer(sel_renderlayer).createCollection(aovs_collection_on)
                _cl.getSelector().setFilterType(8)
                _cl.getSelector().setCustomFilterValue(render_type)
                ov = _cl.createOverride("enable_on", typeIDs.absOverride)
                if cmds.ls(type=render_type):
                    ov.finalize(cmds.ls(type=render_type)[0] + ".enabled")
                    cmds.setAttr("enable_on.atv", l=1)
            if not aovs_collection_off in all_collection_list:
                _cl = renderSetup.instance().getRenderLayer(sel_renderlayer).createCollection(aovs_collection_off)
                _cl.getSelector().setFilterType(8)
                _cl.getSelector().setCustomFilterValue(render_type)
                ov = _cl.createOverride("enable_off", typeIDs.absOverride)
                if cmds.ls(type=render_type):
                    ov.finalize(cmds.ls(type=render_type)[0] + ".enabled")
                    ov.setAttrValue(False)
                    cmds.setAttr("enable_off.atv", l=1)
            # 获取两个collection的所有aov
            aov_on_cllection = renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                aovs_collection_on)
            aov_on_list = aov_on_cllection.getSelector().staticSelection.asList()
            aov_off_cllection = renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                aovs_collection_off)
            aov_off_list = aov_off_cllection.getSelector().staticSelection.asList()

            # 移动aov所在的collection
            for item in self.listWidget.selectedItems():
                line_num = self.listWidget.row(item)
                for aov_node in cmds.ls(type=render_type):
                    if cmds.getAttr(aov_node + '.name') == item.text():
                        if aov_node in aov_on_list:
                            renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                                aovs_collection_on).getSelector().staticSelection.remove([aov_node])
                        if aov_node in aov_off_list:
                            renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                                aovs_collection_off).getSelector().staticSelection.remove([aov_node])
                self.set_listwidgetitem_style(line_num, False)

    def delete_aov(self):
        render_type = ""
        if self.arnold_radiobutton.isChecked():
            render_type = "aiAOV"
        elif self.redshift_radiobutton.isChecked():
            render_type = "RedshiftAOV"

        for item in self.listWidget.selectedItems():
            line_num = self.listWidget.row(item)
            for aov_node in cmds.ls(type=render_type):
                if cmds.getAttr(aov_node + '.name') == item.text():
                    cmds.delete(aov_node)
            self.listWidget.takeItem(line_num)
        if self.rendersetup_radiobutton.isChecked():
            sel_renderlayer = renderSetup.instance().getVisibleRenderLayer().name()

            if sel_renderlayer == "defaultRenderLayer":
                cmds.confirmDialog(title=u'警告!!', icon='question', message=u'Render Setup不支持在defaultRenderLayer设置层覆盖',
                                   button=[u'关闭'])
                return

            # 所有renderlayer
            all_renderlayer_obj = renderSetup.instance().getRenderLayers()
            all_renderlayer_list = []
            for i in all_renderlayer_obj:
                all_renderlayer_list.append(i.name())
            # 创建collection
            aovs_collection_on = sel_renderlayer + '_Aov_overrides_On'
            aovs_collection_off = sel_renderlayer + '_Aov_overrides_Off'
            # 获取当前renderlayer所有collection
            all_collection_list = []
            all_collection_obj = renderSetup.instance().getRenderLayer(sel_renderlayer).getCollections()
            for i in all_collection_obj:
                all_collection_list.append(i.name())
            if not aovs_collection_on in all_collection_list:
                _cl = renderSetup.instance().getRenderLayer(sel_renderlayer).createCollection(aovs_collection_on)
                _cl.getSelector().setFilterType(8)
                _cl.getSelector().setCustomFilterValue(render_type)
                ov = _cl.createOverride("enable_on", typeIDs.absOverride)
                if cmds.ls(type=render_type):
                    ov.finalize(cmds.ls(type=render_type)[0] + ".enabled")
                    cmds.setAttr("enable_on.atv", l=1)
            if not aovs_collection_off in all_collection_list:
                _cl = renderSetup.instance().getRenderLayer(sel_renderlayer).createCollection(aovs_collection_off)
                _cl.getSelector().setFilterType(8)
                _cl.getSelector().setCustomFilterValue(render_type)
                ov = _cl.createOverride("enable_off", typeIDs.absOverride)
                if cmds.ls(type=render_type):
                    ov.finalize(cmds.ls(type=render_type)[0] + ".enabled")
                    ov.setAttrValue(False)
                    cmds.setAttr("enable_off.atv", l=1)
            # 获取两个collection的所有aov
            aov_on_cllection = renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                aovs_collection_on)
            aov_on_missinglist = aov_on_cllection.getSelector().staticSelection.asList()
            aov_off_cllection = renderSetup.instance().getRenderLayer(sel_renderlayer).getCollectionByName(
                aovs_collection_off)
            aov_off_missinglist = aov_off_cllection.getSelector().staticSelection.asList()
            for aovnode in aov_on_missinglist:
                if aov_on_cllection.getSelector().staticSelection.isMissing(aovnode):
                    aov_on_cllection.getSelector().staticSelection.remove([aovnode])


class Download_This_Script():
    def __init__(self):
        self.this_file = unicode(os.path.dirname(os.path.dirname(__file__))).replace("\\", "/")
        self.run()

    def run(self):
        print(self.this_file)


class MainWindow(Ui_Aov_Management_Tool, QtWidgets.QWidget):
    def __init__(self, parent=mayaMainWindows()):
        Ui_Aov_Management_Tool.__init__(self)
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.retranslateUi(self)


if __name__ == "__main__":
    try:
        AovManagementToolWin.close()
        AovManagementToolWin.deleteLater()
    except:
        pass
    AovManagementToolWin = MainWindow()
    AovManagementToolWin.show()
