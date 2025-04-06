# _*_ coding: utf-8 _*_
# .@FileName:ReplaceMaterial
# .@Date....:2024-01-12-23 : 21 : 20
# .@Aurhor..:冥羽
# .@Contact.:1942598111@qq.com
'''
launch:
        import ReplaceMaterial as kt_FileName
        reload(FileName)
        FileName.main()
'''
import maya.cmds as cmds
import random

class MyWindow(object):

    def __init__(self):

        # C H E C K  W I N D O W

        # UI Width宽度
        sizeX = 250
        version = "v1.0"# 版本
        # 检查窗口，如果在程序在运行，关闭它
        if cmds.window("LgtTy", exists=True):
            cmds.deleteUI("LgtTy", window=True)
            cmds.windowPref("LgtTy", r=True)  # 删除窗口首选项

        # 创建 UI 标题tool  宽 高   最小化  最大化  调整大小
        ReplaceCam = cmds.window("LgtTy", title="LgtTy Tool " + version, width=sizeX*4, 
                                   mnb=True, mxb=False, sizeable=True)

        # 创建接口元素   布局  高度  跟随大小   两边边缘
        mainLayout = cmds.columnLayout("LgtTy", width=sizeX, adjustableColumn=True, co=["both", 2])


        cmds.text(label=u"灯光", font="boldLabelFont", h=30, align="center")
        cmds.text(l="  ", h=30)
        
        #LgtColor=cmds.getAttr("directionalLightShape1.color",type=True)
        #print(LgtColor)
        cmds.colorSliderGrp( 'colorU',label='Color', rgb=(1,1,1),cc=self.colorZ,dc=self.colorZ)
        cmds.floatSliderGrp( 'intensitylabeU',l='intensity', field=True, pre=3,v=0.000,dc=self.IntensityZ,cc=self.IntensityZ )
        cmds.floatSliderGrp( 'ExposureU', label='Exposure', field=True,minValue=0,maxValue=10,fieldMinValue=-100.0, fieldMaxValue=100.0,v=0.000, pre=3,dc=self.ExposureZ,cc=self.ExposureZ )
        cmds.intSliderGrp('SamplesU', field=True, label='Samples', minValue=1,maxValue=10, value=1,dc=self.SamplesZ,cc=self.SamplesZ )
        
        cmds.floatSliderGrp( 'coneAngleU',l='coneAngle', field=True, fieldMaxValue=180.0,minValue=0.006, maxValue=179.994, pre=4,v=0.000,dc=self.coneAngleZ,cc=self.coneAngleZ )
        cmds.floatSliderGrp( 'penumbraAngleU',l='penumbraAngle', field=True,minValue=-10, maxValue=10, fieldMaxValue=10.0, pre=3,v=0.000,dc=self.penumbraAngleZ,cc=self.penumbraAngleZ )
        cmds.floatSliderGrp( 'dropoffU',l='dropoff', field=True, fieldMaxValue=255.0, maxValue=255.0, pre=4,v=0.000,dc=self.dropoffZ,cc=self.dropoffZ )
        
        
        cmds.textFieldGrp( 'AovU',label='Aov',adj=2,cc=self.AovZ)
        cmds.button(l='Light Visible(on)', w=170, ann='可见切换',c=self.LVZON)
        cmds.button(l='Light Visible(off)', w=170, ann='可见切换',c=self.LVZOff)
        cmds.paneLayout( configuration='vertical2')
        cmds.button(label=u"mesh", w=sizeX/100, h=40, c=self.MeshZ, ann=u"选择要导出动画的大组")
        cmds.button(label=u"mesh_light", w=sizeX/100, h=40, c=self.MeshLgtZ, ann=u"选择要导入动画的大组")
        
        cmds.columnLayout("LgtTyR", width=sizeX, adjustableColumn=True, co=["both", 2],p=mainLayout)

        cmds.button(l='刷新', w=170, ann='刷新',c=self.BuZ)
        cmds.textFieldGrp( 'IRandU',label='随机intensity')
        cmds.textField('IMaxU',p='IRandU' )
        cmds.button(l='随机', w=170, ann='随机',p='IRandU',c=self.RandIZ)
        cmds.textFieldGrp( 'ERandU',label='随机Exposure')
        cmds.textField('EMaxU',p='ERandU' )
        cmds.button(l='随机', w=170, ann='随机',p='ERandU',c=self.RandEZ)
        
        # Show UI:
        cmds.showWindow(ReplaceCam)# 显示窗口
        
    def colorZ(self,*args):
        Shapes=cmds.ls(sl=True,dag=True,sn=True)
        G=cmds.ls(sl=True,dag=True,sn=True,typ='transform')
        Shapes=list(set(Shapes)-set(G))
        colorV=cmds.colorSliderGrp('colorU',q=True,rgb=True )
        #colorV=colorV[1,-1]
        for Shape in Shapes:
            cmds.setAttr("{}.color".format(Shape),colorV[0],colorV[1],colorV[2],type="double3")
            
            
    def IntensityZ(self,*args):
        #Mesh=cmds.ls(sl=True,dag=True,sn=True,type='mesh')
        Shapes=cmds.ls(sl=True,dag=True,sn=True)
        G=cmds.ls(sl=True,dag=True,sn=True,typ='transform')
        Shapes=list(set(Shapes)-set(G))
        
        #Shapes=Lgt
        IntensityV=cmds.floatSliderGrp( 'intensitylabeU',q=True,v=True )
        for Shape in Shapes:
            cmds.setAttr("{}.intensity".format(Shape),IntensityV)
            
    def ExposureZ(self,*args):
        Shapes=cmds.ls(sl=True,dag=True,sn=True)
        G=cmds.ls(sl=True,dag=True,sn=True,typ='transform')
        Shapes=list(set(Shapes)-set(G))
        ExposureV=cmds.floatSliderGrp( 'ExposureU',q=True,v=True )
        for Shape in Shapes:
            cmds.setAttr("{}.aiExposure".format(Shape),ExposureV)
            
    def SamplesZ(self,*args):
        Shapes=cmds.ls(sl=True,dag=True,sn=True)
        G=cmds.ls(sl=True,dag=True,sn=True,typ='transform')
        Shapes=list(set(Shapes)-set(G))
        SamplesV=cmds.intSliderGrp('SamplesU',q=True,v=True )
        for Shape in Shapes:
            cmds.setAttr("{}.aiSamples".format(Shape),SamplesV)
            
    def AovZ(self,*args):
        Shapes=cmds.ls(sl=True,dag=True,sn=True)
        G=cmds.ls(sl=True,dag=True,sn=True,typ='transform')
        Shapes=list(set(Shapes)-set(G))
        AovV=cmds.textFieldGrp('AovU',q=True,tx=True )
        for Shape in Shapes:
            cmds.setAttr("{}.aiAov".format(Shape),AovV,typ="string")
            
    def coneAngleZ(self,*args):
        Shapes=cmds.ls(sl=True,dag=True,sn=True)
        G=cmds.ls(sl=True,dag=True,sn=True,typ='transform')
        Shapes=list(set(Shapes)-set(G))
        coneAngleV=cmds.floatSliderGrp( 'coneAngleU',q=True,v=True )
        for Shape in Shapes:
            cmds.setAttr("{}.coneAngle".format(Shape),coneAngleV)
            
    def penumbraAngleZ(self,*args):
        Shapes=cmds.ls(sl=True,dag=True,sn=True)
        G=cmds.ls(sl=True,dag=True,sn=True,typ='transform')
        Shapes=list(set(Shapes)-set(G))
        penumbraAngleV=cmds.floatSliderGrp( 'penumbraAngleU',q=True,v=True )
        for Shape in Shapes:
            cmds.setAttr("{}.penumbraAngle".format(Shape),penumbraAngleV)

    def dropoffZ(self,*args):
        Shapes=cmds.ls(sl=True,dag=True,sn=True)
        G=cmds.ls(sl=True,dag=True,sn=True,typ='transform')
        Shapes=list(set(Shapes)-set(G))
        dropoffV=cmds.floatSliderGrp( 'dropoffU',q=True,v=True )
        for Shape in Shapes:
            cmds.setAttr("{}.dropoff".format(Shape),dropoffV)
        
    def LVZON(self,*args):
        Shapes=cmds.ls(sl=True,dag=True,sn=True,typ='mesh')
        for Shape in Shapes:
            cmds.setAttr("{}.lightVisible".format(Shape),1)
            
    def LVZOff(self,*args):
        Shapes=cmds.ls(sl=True,dag=True,sn=True,typ='mesh')

        for Shape in Shapes:
            cmds.setAttr("{}.lightVisible".format(Shape),0)
    
    def MeshZ(self,*args):
        Shapes=cmds.ls(sl=True,dag=True,sn=True,typ='mesh')
        for Shape in Shapes:
            cmds.setAttr("{}.aiTranslator".format(Shape),"polymesh",typ="string")
            
    def MeshLgtZ(self,*args):
        Shapes=cmds.ls(sl=True,dag=True,sn=True,typ='mesh')
        for Shape in Shapes:
            cmds.setAttr("{}.aiTranslator".format(Shape),"mesh_light",typ="string")
            
    def BuZ(self,*args):
        Shapes=cmds.ls(sl=True,dag=True,sn=True)
        G=cmds.ls(sl=True,dag=True,sn=True,typ='transform')
        Shapes=list(set(Shapes)-set(G))
        Shapes=Shapes[0]
        colorQV=cmds.getAttr("{}.color".format(Shapes))
        cmds.colorSliderGrp('colorU',e=True,rgb=(colorQV[0]))
        
        intensityQV=cmds.getAttr("{}.intensity".format(Shapes))
        cmds.floatSliderGrp('intensitylabeU',e=True,v=intensityQV)
        
        ExposureQV=cmds.getAttr("{}.aiExposure".format(Shapes))
        cmds.floatSliderGrp('ExposureU',e=True,v=ExposureQV)
        
        SamplesQV=cmds.getAttr("{}.aiSamples".format(Shapes))
        cmds.intSliderGrp('SamplesU',e=True,v=SamplesQV)
        
        AovQV=cmds.getAttr("{}.aiAov".format(Shapes))
        cmds.textFieldGrp('AovU',e=True,tx=AovQV)
        
    def RandIZ(self,*args):
        Shapes=cmds.ls(sl=True,dag=True,sn=True)
        G=cmds.ls(sl=True,dag=True,sn=True,typ='transform')
        Shapes=list(set(Shapes)-set(G))
        MinV=cmds.textFieldGrp( 'IRandU',q=True,tx=True)
        MaxV=cmds.textField('IMaxU',q=True,tx=True)
        
        
        for Shape in Shapes:
            ExposureRV=random.uniform(float(MinV),float(MaxV))
            cmds.setAttr("{}.intensity".format(Shape),ExposureRV)
            
    def RandEZ(self,*args):
        Shapes=cmds.ls(sl=True,dag=True,sn=True)
        G=cmds.ls(sl=True,dag=True,sn=True,typ='transform')
        Shapes=list(set(Shapes)-set(G))
        MinV=cmds.textFieldGrp( 'ERandU',q=True,tx=True)
        MaxV=cmds.textField('EMaxU',q=True,tx=True)
        
        
        for Shape in Shapes:
            ExposureRV=random.uniform(float(MinV),float(MaxV))
            cmds.setAttr("{}.aiExposure".format(Shape),ExposureRV)
        
MyWindow()