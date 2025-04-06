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
import maya.mel as mel
import mtoa.aovs as tio
import os
import re
import maya.app.renderSetup.views.renderSetupWindow as re_Wind

tioq = tio.AOVInterface()


class MyWindow(object):

    def __init__(self):

        # C H E C K  W I N D O W

        # UI Width宽度
        sizeX = 500
        version = "v1.0"  # 版本
        # 检查窗口，如果在程序在运行，关闭它
        if cmds.window("xrsz", exists=True):
            cmds.deleteUI("xrsz", window=True)
            cmds.windowPref("xrsz", r=True)  # 删除窗口首选项

        # 创建 UI 标题tool  宽 高   最小化  最大化  调整大小
        ReplaceMaterial = cmds.window("xrsz", title="渲染设置" + version, width=sizeX,
                                      mnb=True, mxb=False, sizeable=True)

        # 创建接口元素   布局  高度  跟随大小   两边边缘
        mainLayout = cmds.columnLayout("mainColumnLayout", width=sizeX / 4, adjustableColumn=True, co=["both", 10])

        cmds.text(label=u"渲染基础设置", font="boldLabelFont", h=30, align="center")
        cmds.text(label=u"使用前请把文件保存在项目中", font="boldLabelFont", h=30, align="center")
        cmds.text(l="  ", h=20)

        cmds.button(l='删除摄像机贴图', w=20, h=40, parent=mainLayout, c=self.delCamTex)
        cmds.button(l='关闭渲染报错和生成tx贴图', w=20, h=40, parent=mainLayout, c=self.deTxError)
        cmds.button(l='高质量', w=20, h=40, parent=mainLayout, c=self.higSam)
        #cmds.button(l='中质量', w=20, h=40, parent=mainLayout, c=self.midSam)
        cmds.button(l='低质量', w=20, h=40, parent=mainLayout, c=self.lowSam)
        cmds.button(l='灯光aov', w=20, h=40, parent=mainLayout, c=self.lgtAov)
        cmds.button(l='基础设置', w=20, h=40, parent=mainLayout, c=self.RenderSetting)
        cmds.button(l='基础设置（独立）', w=20, h=40, parent=mainLayout, c=self.RenderSettingIndependent)
        # self.textCry = cmds.textFieldGrp(adj=1,cw2=(500,200),h=60)
        # cmds.button(l='相同的cry', w=300,h=50,p=self.textCry)

        if cmds.getAttr('defaultRenderGlobals.ren') != 'arnold':
            cmds.setAttr('defaultRenderGlobals.ren', 'arnold', typ='string')

        # Show UI:
        cmds.showWindow(ReplaceMaterial)  # 显示窗口

    def find_files_with_substring(directory, substring):
        matching_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if substring in file:
                    matching_files.append(os.path.join(root, file))
        return matching_files

    def delCamTex(self, *args):
        tu = cmds.ls(typ='imagePlane')
        cmds.delete(tu)

    def deTxError(self, *args):
        cmds.setAttr('defaultArnoldRenderOptions.autotx', 0)
        cmds.setAttr('defaultArnoldRenderOptions.abortOnError', 0)

    def higSam(self, *args):
        cmds.setAttr("defaultArnoldRenderOptions.AASamples", 5)
        cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", 4)
        cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", 5)
        cmds.setAttr("defaultArnoldRenderOptions.motion_blur_enable", 1)
        cmds.setAttr("defaultArnoldRenderOptions.range_type", 0)
        cameras = cmds.ls(typ='camera')
        for camera in cameras:
            cmds.setAttr('{}.aiUseGlobalShutter'.format(camera), 0)

    def midSam(self, *args):
        pass

    def lowSam(self, *args):
            cmds.setAttr("defaultArnoldRenderOptions.AASamples", 3)
            cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", 2)
            cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", 2)
            cmds.setAttr("defaultArnoldRenderOptions.motion_blur_enable", 0)

    def lgtAov(self, *args):
        aovPath = r'U:\temp\zjd\jichuAov.json'
        if not os.path.exists(aovPath):
            cmds.confirmDialog(title="提示", message="<span style = 'font-size:20pt;'>文件不存在啊！</span>",
                               button=['Yes'])
        try:
            re_Wind._importAOVsFromPath(aovPath)
        except TypeError:
            cmds.confirmDialog(title="提示",
                               message="<span style = 'font-size:20pt;'>预设可能坏了吧，再查查看看瞅一瞅looklook</span>",
                               button=['Yes'])
        if tioq.getAOVs(include='crypto_asset'):
            cmds.shadingNode("cryptomatte", asShader=True, n="cryptomatte1")
            cmds.defaultNavigation(ce=True, s='cryptomatte1', d='aiAOV_crypto_asset.defaultValue')
            cmds.defaultNavigation(ce=True, s='cryptomatte1', d='aiAOV_crypto_material.defaultValue')
            cmds.defaultNavigation(ce=True, s='cryptomatte1', d='aiAOV_crypto_object.defaultValue')
        if tioq.getAOVs(include='AO'):
            cmds.shadingNode("aiAmbientOcclusion", asShader=True, n="AO5")
            cmds.defaultNavigation(ce=True, s='AO5', d='aiAOV_AO.defaultValue')
        if tioq.getAOVs(include='crypto_userid'):
            cmds.shadingNode("cryptomatte", asShader=True, n="customCrypomatte")
            cmds.defaultNavigation(ce=True, s='customCrypomatte', d='aiAOV_crypto_userid.defaultValue')
            cmds.setAttr('customCrypomatte.userCryptoAov0', 'crypto_userid', type="string")
            cmds.setAttr('customCrypomatte.userCryptoSrc0', 'userid', type="string")



    def RenderSetting(self, *args):
        FileLJ = cmds.file(query=True, loc=True)
        FileDir = os.path.dirname(FileLJ)
        FileDirSplit = os.path.normpath(FileDir).split(os.sep)
        #if len(cmds.ls(typ='renderLayer')) >= 1:
        cmds.setAttr('defaultRenderGlobals.imageFilePrefix',
                    r'W:\{}\renders\{}\{}\3d\lgt\lgt\<RenderLayer>\v001\<RenderPass>\{}_{}_{}_<RenderLayer>_<RenderPass>_v001'.format(FileDirSplit[1], FileDirSplit[2], FileDirSplit[3], FileDirSplit[1], FileDirSplit[2], FileDirSplit[3]),
                    type='string')

        mel.eval('setMayaSoftwareFrameExt(3,0)')

        minKeyVr=cmds.playbackOptions(q=True, min=True)
        cmds.setAttr('defaultRenderGlobals.startFrame', minKeyVr)
        maxKeyVr=cmds.playbackOptions(q=True, max=True)
        cmds.setAttr('defaultRenderGlobals.endFrame', maxKeyVr)

    def RenderSettingIndependent(self, *args):
        FileLJ = cmds.file(query=True, loc=True)
        FileDir = os.path.dirname(FileLJ)
        FileDirSplit = os.path.normpath(FileDir).split(os.sep)
        #if len(cmds.ls(typ='renderLayer')) >= 1:
        cmds.setAttr('defaultRenderGlobals.imageFilePrefix',
                    r'V:\myth\Chr\wenZhongArmyF1\tex\render\<Scene>\v001\myth_Chr_wenZhongArmyF1_<Scene>_v001',
                    type='string')

        mel.eval('setMayaSoftwareFrameExt(3,0)')

        cmds.setAttr('camera1.renderable', 1)
        cmds.setAttr('persp.renderable', 0)
        cmds.setAttr('defaultResolution.width', 2048)
        cmds.setAttr('defaultResolution.height', 1152)

        cmds.setAttr('defaultArnoldRenderOptions.AASamples', 4)
        cmds.setAttr('defaultArnoldRenderOptions.GIDiffuseSamples', 3)
        cmds.setAttr('defaultArnoldRenderOptions.GISpecularSamples', 3)

        minKeyVr=cmds.playbackOptions(q=True, min=True)
        cmds.setAttr('defaultRenderGlobals.startFrame', 1001)
        maxKeyVr=cmds.playbackOptions(q=True, max=True)
        cmds.setAttr('defaultRenderGlobals.endFrame', 1150)

MyWindow()


