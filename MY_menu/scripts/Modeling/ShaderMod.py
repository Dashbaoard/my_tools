from functools import partial


import maya.cmds as cmds
class ShaderModWin(object):
    def __init__(self):
        sizeX=250
        if cmds.window("ShaderModWin", exists=True):
            cmds.deleteUI("ShaderModWin", window=True)
            
        ShaderModWin = cmds.window("ShaderModWin", title="ShaderMod " + '1', width=sizeX + 6, height=200,
                                   mnb=True, mxb=False, sizeable=True)
        mainLayout = cmds.columnLayout("mainColumnLayout", width=sizeX, adjustableColumn=True, co=["both", 2])
        #cmds.text(label=u"")
        cmds.text(label=u"选择要拆分的模型", font="boldLabelFont", ann="Write the suffix", h=40)
        #cmds.text(label=u"")
        cmds.button(label=u'材质模型', parent=mainLayout, command=self.report)
        cmds.showWindow()
    def report(self,*arge):
        modLongname=cmds.ls(sl=True,l=True)
        modname=cmds.ls(sl=True,sn=True)
        mod=cmds.ls(sl=1,dag=1,type="mesh")

        cmds.ConvertSelectionToFaces()

        PShaderList=cmds.listConnections(mod,type="shadingEngine")

        PShaderList = list(set(PShaderList))
        #PShaderList.remove('initialShadingGroup')
        PShaderList = [x for x in PShaderList if x != 'initialShadingGroup']

        for PShaderLs in PShaderList:
            PShader=cmds.select(PShaderLs)
            facename=cmds.ls(selection=True, l=True)

            faceSlList=[]
            for faceSlet in facename:
                #faceSS = faceSlet.split('.')[0]
                if modLongname[0] in faceSlet:
                    faceSlList.append(faceSlet)
                elif modLongname[0] not in faceSlet:
                    pass
            cmds.select(faceSlList)
            cmds.polyChipOff(dup=False)
        cmds.polySeparate(mod)
        
        PUList=[]
        for PShaderLs in PShaderList:
            cmds.hyperShade(o=PShaderLs)

            ShaderFaceLs=cmds.ls(selection=True, l=True)
            print(ShaderFaceLs)

            facePList=[]
            for ShaderFaceSl in ShaderFaceLs:
                integer_part = ShaderFaceSl.split('.')[0]
                if modLongname[0] in integer_part:
                    facePList.append(integer_part)
                else:
                    pass
            if len(facePList) == 1:
                cmds.select(facePList[0])
                ea=cmds.Unparent()
            else:
                ea=cmds.polyUnite(facePList)

            PUName=cmds.ls(sl=True,sn=True)

            NewName=modname[0]+'_001'
            cmds.rename(PUName,NewName)
            NewNameSl = cmds.ls(sl=True,sn=True)
            PUList.append(NewNameSl[0])
            
            cmds.DeleteHistory(ea)

            cmds.hyperShade( assign=PShaderLs )
        cmds.group(PUList,n = "{}".format(modname[0]))

