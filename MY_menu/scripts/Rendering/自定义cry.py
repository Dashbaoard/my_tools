# _*_ coding: utf-8 _*_
# .@FileName:ReplaceMaterial
# .@Date....:2023-12-10-14 : 30 : 20
# .@Aurhor..:冥羽
# .@Contact.:1942598111@qq.com
'''
launch:
        import ReplaceMaterial as kt_FileName
        reload(FileName)
        FileName.main()
'''
import maya.cmds as cmds
import mtoa.aovs as tio
import os
import re

tioq=tio.AOVInterface()
class MyWindow(object):

    def __init__(self):

        # C H E C K  W I N D O W

        # UI Width宽度
        sizeX = 500
        version = "v1.0"# 版本
        # 检查窗口，如果在程序在运行，关闭它
        if cmds.window("CustomCrypomatte", exists=True):
            cmds.deleteUI("CustomCrypomatte", window=True)
            cmds.windowPref("CustomCrypomatte", r=True)  # 删除窗口首选项

        # 创建 UI 标题tool  宽 高   最小化  最大化  调整大小
        ReplaceMaterial = cmds.window("CustomCrypomatte", title="Custom Crypomatte Tool " + version, width=sizeX, 
                                   mnb=True, mxb=False, sizeable=True)

        # 创建接口元素   布局  高度  跟随大小   两边边缘
        mainLayout = cmds.columnLayout("mainColumnLayout", width=sizeX/4, adjustableColumn=True, co=["both", 10])


        cmds.text(label=u"自定义crypotmatte", font="boldLabelFont", h=30, align="center")
        cmds.text(l="  ", h=20)
        
        cmds.button(l='创建aov层',w=20,h=40,parent=mainLayout,c=self.creatAov)
        cmds.text(l="  ", h=10)
        cmds.button(l='选择物体增加属性',w=20,h=40,parent=mainLayout,c=self.addAttUserid)
        cmds.text(l="  ", h=20)
        self.folder3 = cmds.optionMenu(ann='格式',h=50, p=mainLayout)
        cmds.menuItem(label='all')
        cmds.menuItem(label='mesh')
        cmds.menuItem(label='ass')
        cmds.menuItem(label='usd')
        cmds.text(l="  ", h=10)
        cmds.button(l='每一个物体',w=20,h=40,parent=mainLayout,c=self.differCry)
        self.textCry = cmds.textFieldGrp(adj=1,cw2=(500,200),h=60)
        cmds.button(l='相同的cry', w=300,h=50,p=self.textCry,c=self.equalCry)



        # Show UI:
        cmds.showWindow(ReplaceMaterial)# 显示窗口
        
        
    def creatAov(self, *args):
        getAovC=tioq.getAOVs(include='crypto_userid')
        if getAovC == []:
            tioq.addAOV('crypto_userid')
            cmds.shadingNode("cryptomatte", asShader=True, n="customCrypomatte")
            cmds.defaultNavigation(ce=True, s='customCrypomatte', d='aiAOV_crypto_userid.defaultValue')
            cmds.setAttr('customCrypomatte.userCryptoAov0','crypto_userid',type="string")
            cmds.setAttr('customCrypomatte.userCryptoSrc0','userid',type="string")
        else:
            cmds.error('存在crypto_userid')
    def addAttUserid(self, *args):
        Shapes=cmds.ls(sl=True,dag=True,sn=True)
        G=cmds.ls(sl=True,dag=True,sn=True,typ='transform')
        Shapes=list(set(Shapes)-set(G))
        for Shape in Shapes:
            try:
                cmds.addAttr(Shape,ln='mtoa_constant_userid',nn='userid',dt='string')
            except RuntimeError:
                pass
            continue
        
    def differCry(self, *args):
        GeShiNum = cmds.optionMenu(self.folder3,sl=True,q=True)
        if GeShiNum == 1:
            Shapes=cmds.ls(sl=True,dag=True,sn=True)
            G=cmds.ls(sl=True,dag=True,sn=True,typ='transform')
            Shapes=list(set(Shapes)-set(G))
        elif GeShiNum == 2:
            Shapes=cmds.ls(sl=True,dag=True,sn=True,typ='mesh')
        elif GeShiNum == 3:
            Shapes=cmds.ls(sl=True,dag=True,sn=True,typ='aiStandIn')
        elif GeShiNum == 4:
            Shapes=cmds.ls(sl=True,dag=True,sn=True,typ='mayaUsdProxyShape')
        
        for Shape in Shapes:
            cmds.setAttr('{}.mtoa_constant_userid'.format(Shape),Shape,typ='string')
    
    def equalCry(self, *args):
        GeShiNum = cmds.optionMenu(self.folder3,sl=True,q=True)
        if GeShiNum == 1:
            Shapes=cmds.ls(sl=True,dag=True,sn=True)
            G=cmds.ls(sl=True,dag=True,sn=True,typ='transform')
            Shapes=list(set(Shapes)-set(G))
        elif GeShiNum == 2:
            Shapes=cmds.ls(sl=True,dag=True,sn=True,typ='mesh')
        elif GeShiNum == 3:
            Shapes=cmds.ls(sl=True,dag=True,sn=True,typ='aiStandIn')
        elif GeShiNum == 4:
            Shapes=cmds.ls(sl=True,dag=True,sn=True,typ='mayaUsdProxyShape')
        
        cryName = cmds.textFieldGrp(self.textCry,q=True,tx=True)
        if cryName == '':
            for Shape in Shapes:
                cmds.setAttr('{}.mtoa_constant_userid'.format(Shape),Shapes[0],typ='string')
        else :
            for Shape in Shapes:
                cmds.setAttr('{}.mtoa_constant_userid'.format(Shape),cryName,typ='string')
    
    
MyWindow()