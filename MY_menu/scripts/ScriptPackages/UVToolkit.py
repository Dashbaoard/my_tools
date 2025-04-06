'''
UVToolkit v1.3
Author: Erik Lehmann
Copyright (c) 2020 Erik Lehmann
Email: contact(at)eriklehmann.com
'''
import maya.cmds as mc
import maya.mel as mm
import maya.OpenMaya as om
from math import sqrt, trunc, atan2, degrees
from functools import partial
import os
class MainClassUVKit:    
    def __init__(self):
        self.uvKitWinID = "uvKitWin"
        self.uvKitLayoutSizeWinID = "uvKitLayoutArrangeSizeWin"
        self.uvKitLSSliderWinID = "uvKitLSSliderWin"
        self.uvKitGreen = (0.3, 0.50, 0.40)
        self.uvKitGrey = (0.3, 0.3, 0.3)
        self.uvKitDark = (0.22, 0.22, 0.22)
        self.uvKitTransSourceObject = []
        self.uvKitTransTargetObject = []
        self.uvKitTransSampleSpace = 0
        self.uvKitProgressControl = ""
        self.uvKitProgressBooleanCheck = False
        self.uvKitLSBase = 1.0
        self.uvKitLSScale = 1.0
        self.uvKitLayPercentageSpace = 2.0
        self.uvKitLayArrangeSizeVal = 0.2
        self.uvKitLayStackSizeVal = 0.2
        self.uvKitLaySpreadSizeVal = 0.1
        self.uvKitLayFloatPositions = 3
        self.uvKitRotateAngleValues = [15, 45, 90, 180]
        self.uvKitModAlignRefPivot = []
        self.uvKitEGetVal = 10.0
        self.uvKitEMapSize = 1024
        self.uvKitEActiveRatio = 0
        self.uvKitEActiveObject = []
        self.uvKitMayaVersion = mc.about(q=True, v=True)
        if '2017' in self.uvKitMayaVersion:
            self.uvKitArrowUp = 'nodeGrapherArrowUp.png'
            self.uvKitArrowDown = 'nodeGrapherArrowDown.png'
        else:
            self.uvKitArrowUp = 'moveUVUp.png'
            self.uvKitArrowDown = 'moveUVDown.png'
        self.uvKitUI()
    def uvKitUI(self, _=False):    
        if (mc.window(self.uvKitWinID, exists=True)):
            mc.deleteUI(self.uvKitWinID, wnd=True)
            mc.windowPref(self.uvKitWinID, r=True)
        mc.window(self.uvKitWinID, t="UV Toolkit v1.3")
        mc.columnLayout(adj=True)
        mc.rowLayout(nc=6)
        mc.text(l='', w=90, h=20)
        mc.symbolButton(image='%s' % self.uvKitArrowUp, w=25, h=25,
        ann='Collapse all tabs', 
        c=lambda *_:self.uvKitCollapseTabs(uvKitCollapseTabsVal=True, uvKitTabWinSize=139))
        mc.symbolButton(image='%s' % self.uvKitArrowDown, w=25, h=25,
        ann='Expand all tabs',
        c=lambda *_:self.uvKitCollapseTabs(uvKitCollapseTabsVal=False, uvKitTabWinSize=633))
        mc.symbolButton(image='textureEditor.png', w=25, h=25,
        ann = 'LMB: Open UV Editor // MMB: Open UV Set Editor',
        c = lambda *_:mc.TextureViewWindow(),
        dgc = lambda *_:mc.UVSetEditor() )
        mc.symbolButton(image='help.png', w=25, h=25,
        ann="Open online documentation",
        c=lambda *_:self.uvKitOpenDocs())
        mc.symbolButton(image='nodeGrapherModeAllLarge.png', w=25, h=25,
        ann="Open 'About' window with information about the toolkit", 
        c=lambda *_:UvKitAboutClass())
        mc.setParent(top=True)
        self.uvKitUFO = mc.frameLayout(l="Unfold", la="top", bgc=self.uvKitGrey, cll=True, cl=True,
        cc = partial(self.uvKitResWin, uvKitClValue=66), ec=partial(self.uvKitResWin, uvKitClValue=(-66)))
        mc.columnLayout(adj=True)
        mc.rowLayout(nc=2)
        self.uvKitUnfoldBtn = mc.button(l="Unfold", al="center", bgc=self.uvKitGreen, h=30, w=110, c = self.uvKitUFOUnfold,
        ann='LMB: Cuts selected edges, 3D unfolds and packs shells // RMB: Option Menu')
        mc.popupMenu(p = self.uvKitUnfoldBtn)
        mc.menuItem(d=True, dl='Options')
        self.uvKitUnfoldOMEdges = mc.menuItem(cb=True, l='Cut selected Edges')
        self.uvKitUnfoldOMPack = mc.menuItem(cb=True, l='Pack shells')
        self.uvKitUFOProjBtn = mc.button(l="Projection", al="center", w=110, h=30,
        ann='LMB: Camera // ALT: X // CTRL: Y // SHIFT: Z', c = lambda *_:self.uvKitUFOProjection() )
        mc.setParent('..')
        mc.rowLayout(nc=3)
        self.uvKitUVUnfoldBtn = mc.button(l="U / V", al="center", w=70, h=30,
        ann='LMB: Horizontal // ALT: Vertical // CTRL: Free // + SHIFT: Pins selected UVs during unfold',
        c = lambda *_:self.uvKitUFOAxis(uvKitUFOPsVal=False))
        mc.button(l="Straighten", al="center", h=30, w=78, c = self.uvKitUFOStraighten,
        ann='LMB: Straighten UVs // ALT: Straighten Shell (Select Edge Loop)')
        mc.button(l="Gridify", al="center", h=30, w=70, c = self.uvKitUFOGridify,
        ann='Unfolds cylindrical shapes into a grid shell, based on the selected edges')
        mc.setParent(top=True)
        self.uvKitTMUVLayout = mc.frameLayout(l="Layout", la="top", bgc=self.uvKitGrey, cll=True, cl=True, 
        cc=partial(self.uvKitResWin, uvKitClValue=66), ec=partial(self.uvKitResWin, uvKitClValue=(-66)))
        mc.columnLayout(adj=True)
        mc.rowLayout(nc=2)
        self.uvKitLayoutBtn = mc.button(l="Layout", al="center", bgc=self.uvKitGreen, w=110, h=30, c = self.uvKitLayStandard,
        ann='LMB: Layout UVs // ALT: Layout each object individually // MMB: Set map space // RMB: Option menu',
        dgc = lambda *_:self.uvKitLayoutSizeWindow("Layout"))
        mc.popupMenu(p = self.uvKitLayoutBtn)
        self.uvKitLayoutRBC = mc.radioMenuItemCollection()
        mc.menuItem(d=True, dl='Shell Rotation')
        self.uvKitLayoutRBNone = mc.menuItem(rb=True, cl=self.uvKitLayoutRBC, l='None')
        self.uvKitLayoutRBFree = mc.menuItem(rb=False, cl=self.uvKitLayoutRBC, l='Free')
        self.uvKitLayoutRB90 = mc.menuItem(rb=False, cl=self.uvKitLayoutRBC, l='90 Degree')
        self.uvKitGridArrangeBtn = mc.button(l="Grid Arrange", al="center", w=110, h=30, 
        ann='LMB: Grid arrange (Object based) // ALT: Sort by Polygon count // MMB: Set size', c = self.uvKitLayArrange,
        dgc = lambda *_:self.uvKitLayoutSizeWindow("Grid") )
        mc.setParent('..')
        mc.rowLayout(nc=3)
        self.uvKitLayStackBtn = mc.button(l="Stack", al="center", w=72, h=30, 
        ann='LMB: Stack UV layouts in default range // ALT: Stack with uniform scale // CTRL: Stack Shells // MMB: Set uniform scale size', 
        c = self.uvKitLayStack, dgc = lambda *_:self.uvKitLayoutSizeWindow("Stack") )
        mc.button(l="Align", al="center", w=74, h=30, 
        ann='Align UV Shells - LMB: Horizontal // ALT: Vertical // CTRL: Match Position // MMB: Set Reference', 
        c = self.uvKitModAlign, dgc = lambda *_:self.uvKitModAlignRef() )
        self.uvKitLaySpreadBtn = mc.button(l="Spread", al="center", w=72, h=30, 
        c = lambda *_:self.uvKitDistribute(), dgc = lambda *_:self.uvKitLayoutSizeWindow("Spread"),
        ann='Spread Layouts (Object based) // LMB: Right // ALT: Up // add SHIFT: opposite direction (left, down) // MMB: Set move value')
        mc.setParent(top=True)
        self.uvKitTMUVModify = mc.frameLayout(l="Modify", la="top", bgc=self.uvKitGrey, cll=True, cl=True, 
        cc=partial(self.uvKitResWin, uvKitClValue=66), ec=partial(self.uvKitResWin, uvKitClValue=(-66)))
        mc.columnLayout(adj=True)
        mc.rowLayout(nc=3)
        self.uvKitModRotBtn = mc.button(l="Rotate", al="center", w=72, h=30, 
        c = self.uvKitModRotateUV,ann="LMB: Clockwise // ALT: Counterclockwise // +SHIFT: Individual Shell // RMB: Option menu")
        mc.popupMenu(p = self.uvKitModRotBtn)
        self.uvKitModRotRBC = mc.radioMenuItemCollection()
        mc.menuItem(d=True, dl='Rotation value')
        mc.menuItem("uvKitModRot15RB", rb=False, cl=self.uvKitModRotRBC, l='15')
        mc.menuItem("uvKitModRot45RB", rb=True, cl=self.uvKitModRotRBC, l='45')
        mc.menuItem("uvKitModRot90RB", rb=False, cl=self.uvKitModRotRBC, l='90')
        mc.menuItem("uvKitModRot180RB", rb=False, cl=self.uvKitModRotRBC, l='180')
        self.uvKitModFlipBtn = mc.button(l="Flip", al="center", w=74, h=30, c = self.uvKitModFlipUV, 
        ann="LMB: Flip all // ALT: Flip individual // SHIFT: Flip automatically")
        mc.button(l="Orient", al="center", w=72, h=30, c = self.uvKitModOrient, 
        ann="LMB: Orient to closest U or V // ALT: Align to X // CTRL: Align to Y // SHIFT: Align to Z")
        mc.setParent('..')
        mc.rowLayout(nc=2)
        mc.button(l="Local Scale", al="center", w=110, h=30, c = self.uvKitLSStart, 
        ann='LMB: Start the local scale process (Select only 1 UV from each target shell)')
        mc.button(l="Equalize", al="center", w=110, h=30, c = self.uvKitEqualizeCall,  
        ann='LMB: Equalize UV layout scale // ALT: Set source')
        mc.setParent(top=True)
        self.uvKitTMUVCP = mc.frameLayout(l="UV Shader", bgc=self.uvKitGrey, cll=True, cl=True, 
        cc=partial(self.uvKitResWin, uvKitClValue=98), ec=partial(self.uvKitResWin, uvKitClValue=(-98)))
        mc.columnLayout(adj=True)
        mc.rowLayout(nc=2)
        mc.button(l="Create / Del", w=110, h=30, bgc=self.uvKitGreen, ann='LMB: Create Shaders // SHIFT: Delete Shaders',
        c = lambda *_:self.uvKitCPCall("Create / Del") )
        mc.button(l="Un / Assign", w=110, h=30, ann='LMB: Assign Checker Pattern // ALT: Assign UV Direction // SHIFT: Unassign Shader', 
        c = lambda *_:self.uvKitCPCall("Un / Assign") )
        mc.setParent('..')
        mc.rowLayout(nc=3)
        mc.button(l='1 K', w=73, h=30, c = lambda *_:self.uvKitCPsetK(1), ann='Set texture map size to 1K')
        mc.button(l='2 K', w=73, h=30, c = lambda *_:self.uvKitCPsetK(2), ann='Set texture map size to 2K')
        mc.button(l='4 K', w=72, h=30, c = lambda *_:self.uvKitCPsetK(4), ann='Set texture map size to 4K')
        mc.setParent('..')
        mc.rowLayout(nc=3)
        mc.button(l='8 K', w=73, h=30, c = lambda *_:self.uvKitCPsetK(8), ann='Set texture map size to 8K')
        mc.button(l='16 K', w=73, h=30, c = lambda *_:self.uvKitCPsetK(16), ann='Set texture map size to 16K')
        mc.button(l='32 K', w=72, h=30, c = lambda *_:self.uvKitCPsetK(32), ann='Set texture map size to 32K')
        mc.setParent(top=True)
        self.uvKitTMUVTrans = mc.frameLayout(l="Transfer", la="top", bgc=self.uvKitGrey, cll=True, cl=True, 
        cc=partial(self.uvKitResWin, uvKitClValue=198), ec=partial(self.uvKitResWin, uvKitClValue=(-198)))
        mc.columnLayout(adj=True)
        mc.rowLayout(nc=2)
        mc.textScrollList("uvKitTransSourceList", h=120, w=110, ams=False)
        mc.textScrollList("uvKitTransTargetList", h=120, w=110, ams=False)
        mc.setParent('..')
        mc.rowLayout(nc=2)
        mc.button(label="Set Source", c = self.uvKitTransSetSource, h=30, w=110,
        ann='Set one or multiple source objects')
        mc.button(label="Set Target(s)", c = self.uvKitTransSetTarget, h=30, w=110,
        ann='Set one or multiple target objects')
        mc.setParent('..')
        mc.rowLayout(nc=1)
        self.uvKitTransCopyBtn = mc.button(label="Copy UVs", ann = "LMB: Copy UVs // RMB: Option Menu",
        h=40, w=222, bgc=self.uvKitGreen, c = self.uvKitTransCopyUVs)
        mc.popupMenu(p = self.uvKitTransCopyBtn)
        self.uvKitTransOMSpaceRBC = mc.radioMenuItemCollection()
        mc.menuItem(d=True, dl='Sample Space')
        self.uvKitTopoRB = mc.menuItem(rb=True, cl = self.uvKitTransOMSpaceRBC, l='Topology')
        self.uvKitWorldRB = mc.menuItem(rb=False, cl = self.uvKitTransOMSpaceRBC, l='World')
        self.uvKitLocalRB = mc.menuItem(rb=False, cl = self.uvKitTransOMSpaceRBC, l='Local')
        self.uvKitCmptRB = mc.menuItem(rb=False, cl = self.uvKitTransOMSpaceRBC, l='Component')
        self.uvKitTransOMScopeRBC = mc.radioMenuItemCollection()
        mc.menuItem(d=True, dl='Layout Scope')
        self.uvKitTransRBScopeAll = mc.menuItem(rb=True, cl = self.uvKitTransOMScopeRBC, l='All')
        self.uvKitTransRBScopeCurrent = mc.menuItem(rb=False, cl = self.uvKitTransOMScopeRBC, l='Current')
        mc.setParent(top=True)
        mc.showWindow(self.uvKitWinID)
        mc.window(self.uvKitWinID, e=True, w=228, h=139)
    def uvKitResWin(self, uvKitClValue, _=False):
        uvKitWinSize = mc.window(self.uvKitWinID, q=True, h=True)
        mc.window(self.uvKitWinID, e=True, h=(uvKitWinSize-uvKitClValue))
    def uvKitCollapseTabs(self, uvKitCollapseTabsVal, uvKitTabWinSize, _=False):
        mc.frameLayout(self.uvKitUFO, e=True, cl=uvKitCollapseTabsVal)
        mc.frameLayout(self.uvKitTMUVLayout, e=True, cl=uvKitCollapseTabsVal)
        mc.frameLayout(self.uvKitTMUVModify, e=True, cl=uvKitCollapseTabsVal)
        mc.frameLayout(self.uvKitTMUVCP, e=True, cl=uvKitCollapseTabsVal)
        mc.frameLayout(self.uvKitTMUVTrans, e=True, cl=uvKitCollapseTabsVal)
        mc.window(self.uvKitWinID, e=True, h=uvKitTabWinSize)
    def uvKitOpenDocs(self, _=False):
        mc.launch(web="https://www.eriklehmann.com/documentation/")
    def uvKitProgressCheck(self, maxProVal, _=False):
        self.uvKitProgressCancel = False
        if maxProVal > 50:
            self.uvKitProgressControl = mc.progressWindow(t="In progress...", ii=True, maxValue = maxProVal)
            self.uvKitProgressBooleanCheck = True
    def uvKitProgressStep(self, _=False):
        if self.uvKitProgressBooleanCheck == True:
            mc.progressWindow(self.uvKitProgressControl, edit=True, step=1)
    def uvKitProgressEnd(self, _=False):
        mc.progressWindow(self.uvKitProgressControl, edit=True, ep=True)
    def uvKitGetUVShells(self, uvKitGUVSList, _=False):
        uvKitLayRotTmpList = []
        uvKitGUVSCheck = []
        for i in uvKitGUVSList:
            if i in uvKitGUVSCheck:
                continue
            else:
                mc.select(i)
                mm.eval('polySelectBorderShell 0;')
                uvKitTmpObj = mc.ls(sl=True)
                uvKitLayRotTmpList.append(uvKitTmpObj)
                uvKitTmpObjFlat = mc.ls(sl=True, fl=True)
                for i in uvKitTmpObjFlat:
                    uvKitGUVSCheck.append(i)
        return uvKitLayRotTmpList
    def uvKitGetBoundingBox(self, uvKitGetBBInput, _=False):
        mc.select(uvKitGetBBInput)
        uvKitGetBBBB = mc.polyEvaluate(bc2=True)
        uvKitGetBBPivot = [0,0]
        uvKitGetBBPivot[0] = ((uvKitGetBBBB[0][0] + uvKitGetBBBB[0][1]) /2 )
        uvKitGetBBPivot[1] = ((uvKitGetBBBB[1][0] + uvKitGetBBBB[1][1]) /2 )
        return uvKitGetBBPivot
    def uvKitUFOUnfold(self, uvKitUFOPack, _=False):
        if mc.menuItem(self.uvKitUnfoldOMPack, q=True, cb=True):
            uvKitUFOPack = True
        else:
            uvKitUFOPack = False
        uvKitUFOTemp = mc.ls(sl=True)
        if mc.menuItem(self.uvKitUnfoldOMEdges, q=True, cb=True):
            if '.e' in str(uvKitUFOTemp):
                uvKitUFOEdgeTemp = uvKitUFOTemp
                uvKitUFOTemp = mc.listRelatives(p=True)
                mc.polyMapCut(uvKitUFOEdgeTemp, ch=True)
        mc.u3dUnfold(uvKitUFOTemp, ite=10, p=uvKitUFOPack, bi=True, tf=False, ms=512, rs=1)
    def uvKitUFOProjection(self, _=False):
        uvKitModifier = mc.getModifiers()
        if uvKitModifier == 0:
            uvKitUFOProVal = 'c'
        if (uvKitModifier & 8) > 0:
            uvKitUFOProVal = 'x'    
        if (uvKitModifier & 4) > 0:
            uvKitUFOProVal = 'y'
        if (uvKitModifier & 1) > 0:
            uvKitUFOProVal = 'z'
        uvKitUFOProRe = uvKitUFOProSel = mc.ls(sl=True)
        if '.' not in str(uvKitUFOProRe):
            uvKitUFOProTempList = []
            for i in uvKitUFOProSel:
                uvKitUFOProFaceCount = mc.polyEvaluate(i, f=True)
                mc.select('%s.f[0:%s]' % (i, uvKitUFOProFaceCount), r=True)
                uvKitUFOProTemp = mc.ls(sl=True)
                uvKitUFOProTempList.append(uvKitUFOProTemp[0])
            uvKitUFOProSel = uvKitUFOProTempList
        mc.polyProjection(uvKitUFOProSel, ch=True, type='Planar', ibd=True, kir=True, md=('%s' % uvKitUFOProVal))
        mc.select(uvKitUFOProRe)
    def uvKitUFOAxis(self, uvKitUFOPsVal, _=False):
        uvKitModifier = mc.getModifiers()
        uvKitUFOPsVal = False
        if (uvKitModifier & 1) > 0:
            if not (uvKitModifier & 8) > 0 or (uvKitModifier & 4) > 0:
                uvKitUFOAxisVal=2
            uvKitUFOPsVal = True
        if uvKitModifier == 0:
            uvKitUFOAxisVal=2
        if (uvKitModifier & 8) > 0:
            uvKitUFOAxisVal=1
        if (uvKitModifier & 4) > 0:
            uvKitUFOAxisVal=0
        mc.unfold(i=10000, ss=0.001, gb=0, gmb=0.5, pub=False, ps=uvKitUFOPsVal, oa=uvKitUFOAxisVal, us=False)
    def uvKitUFOGridify(self, _=False):
        uvKitUCCutEdge = mc.ls(sl=True)
        mc.polySelectSp(ring=True)
        mm.eval('PolySelectConvert 1;')
        uvKitUCFaceSel = mc.ls(sl=True)
        mm.eval('PolySelectConvert 20;')
        for i in uvKitUCCutEdge:
            mc.select(i, d=True)
        uvKitUCEdgeSel = mc.ls(sl=True)
        mc.select(uvKitUCFaceSel)
        mc.UnitizeUVs()
        mc.select(uvKitUCEdgeSel)
        mc.polyMapSewMove(nf=(len(uvKitUCFaceSel)), lps=False, ch=True)
        mc.select(uvKitUCFaceSel)
        mm.eval('PolySelectConvert 4;')
        mc.unfold(i=10000, ss=0.001, gb=0, gmb=0.5, pub=False, ps=False, oa=2, us=False)
        mc.polyLayoutUV(lm=1, sc=1, se=0, rbf=2, fr=False, ps=1.0, gu=1, gv=1, ch=True)    
    def uvKitUFOStraighten(self, _=False):
        uvKitModifier = mc.getModifiers()
        if uvKitModifier == 0:
            mc.UVStraighten()
        if (uvKitModifier & 8) > 0:
            mm.eval("texStraightenShell;")
    def uvKitLayStandard(self, _=False):
        uvKitModifier = mc.getModifiers()
        uvKitLAYtemp = mc.ls(sl=True)
        if mc.menuItem(self.uvKitLayoutRBFree, q=True, rb=True) == True:
            uvKitLayRotation = 2
        if mc.menuItem(self.uvKitLayoutRB90, q=True, rb=True) == True:
            uvKitLayRotation = 1
        if mc.menuItem(self.uvKitLayoutRBNone, q=True, rb=True) == True:
            uvKitLayRotation = 0
        if uvKitModifier == 0:  
            mc.polyMultiLayoutUV(uvKitLAYtemp, l=2, lm=0, sc=1, rbf=uvKitLayRotation, fr=True, ps=self.uvKitLayPercentageSpace, gu=1, psc=2, gv=1, su=1, sv=1)
        if (uvKitModifier & 8) > 0:
            for i in uvKitLAYtemp:
                mc.polyMultiLayoutUV(i, l=2, lm=0, sc=1, rbf=uvKitLayRotation, fr=True, ps=self.uvKitLayPercentageSpace, gu=1, psc=2, gv=1, su=1, sv=1) 
    def uvKitLayoutSizeWindow(self, uvKitCheckSizeCall, _=False):
        if uvKitCheckSizeCall == "Layout":
            uvKitLayoutTmpSize = self.uvKitLayPercentageSpace
            uvKitLayoutSetSizeMax = 10.00
            uvKitLayoutSetSizeMin = 0.01
            self.uvKitLayFloatPositions = 4
        if uvKitCheckSizeCall == "Grid":
            uvKitLayoutTmpSize = self.uvKitLayArrangeSizeVal
            uvKitLayoutSetSizeMax = 0.99
            uvKitLayoutSetSizeMin = 0.01
            self.uvKitLayFloatPositions = 3
        if uvKitCheckSizeCall == "Stack":
            uvKitLayoutTmpSize = self.uvKitLayStackSizeVal
            uvKitLayoutSetSizeMax = 0.99
            uvKitLayoutSetSizeMin = 0.01
            self.uvKitLayFloatPositions = 3
        if uvKitCheckSizeCall == "Spread":
            uvKitLayoutTmpSize = self.uvKitLaySpreadSizeVal
            uvKitLayoutSetSizeMax = 1
            uvKitLayoutSetSizeMin = 0
            self.uvKitLayFloatPositions = 3
        if (mc.window(self.uvKitLayoutSizeWinID, exists=True)):
            mc.deleteUI(self.uvKitLayoutSizeWinID, wnd=True)
            mc.windowPref(self.uvKitLayoutSizeWinID, r=True)
        mc.window(self.uvKitLayoutSizeWinID, s=False, tlb=True, t="Options")
        mc.columnLayout(adj=True)
        mc.rowLayout(nc=1)
        mc.text(l="", h=10)
        mc.setParent('..')
        mc.rowLayout(nc=2)
        mc.text(l=" Set value: ", w = 95)
        self.uvKitLayChangeSizeFF = mc.floatField(min=uvKitLayoutSetSizeMin, max=uvKitLayoutSetSizeMax, 
        pre=self.uvKitLayFloatPositions, v=uvKitLayoutTmpSize, w=55, h=30)
        mc.setParent('..')
        mc.rowLayout(nc=1)
        mc.text(l="", h=10)
        mc.setParent('..')
        mc.rowLayout(nc=5)
        mc.text(l="", w=25)
        mc.button(l='OK', h=30, w=35, c = lambda *_:self.uvKitLayRunSetSize(uvKitCheckSizeCall) )
        mc.text(l="", w=20)
        mc.button(l='Cancel', h=30, w=65, c = lambda *_:self.uvKitLayoutSizeCloseWin() )
        mc.text(l="", w=25)      
        mc.setParent(top=True)
        mc.showWindow(self.uvKitLayoutSizeWinID)
        mc.window(self.uvKitLayoutSizeWinID, e=True, w=180, h=100)
    def uvKitLayRunSetSize(self, uvKitCheckSizeCall, _=False): 
        if uvKitCheckSizeCall == "Layout":
            self.uvKitLayPercentageSpace = mc.floatField(self.uvKitLayChangeSizeFF, q=True, v=True)
        if uvKitCheckSizeCall == "Grid":
            self.uvKitLayArrangeSizeVal = mc.floatField(self.uvKitLayChangeSizeFF, q=True, v=True)
        if uvKitCheckSizeCall == "Stack":
            self.uvKitLayStackSizeVal = mc.floatField(self.uvKitLayChangeSizeFF, q=True, v=True)
        if uvKitCheckSizeCall == "Spread":
            self.uvKitLaySpreadSizeVal = mc.floatField(self.uvKitLayChangeSizeFF, q=True, v=True)
        self.uvKitLayoutSizeCloseWin()
    def uvKitLayoutSizeCloseWin(self, _=False):
        mc.deleteUI(self.uvKitLayoutSizeWinID, wnd=True)
    def uvKitLayArrange(self, _=False):
        uvKitModifier = mc.getModifiers()
        objs = mc.ls(sl=True)
        objSel = mc.ls(sl=True)
        scaleInput = self.uvKitLayArrangeSizeVal
        gridRows = int( 1 / scaleInput )
        if gridRows > 2 or self.uvKitLayArrangeSizeVal > 0.48 :
            gridRows = gridRows - 1
        offsetTemp = ((1 / float(gridRows)) - scaleInput) / 2
        udimUMove = udimVMove = 0
        moveU = moveV = 0.0
        maxU = maxV = gridRows
        countToMaxU = countToMaxV = 1
        moveUBase = scaleInput + (float("%.3f" % offsetTemp) * 2)
        offsetUTemp = offsetVTemp = float("%.3f" % offsetTemp)
        self.uvKitProgressCheck(len(objs))
        while len(objs) > 0:
            if (uvKitModifier & 8) > 0:
                tmpList = []
                tmpSource = objs[0]
                polyCount = mc.polyEvaluate(tmpSource, f=True)
                vertexCount = mc.polyEvaluate(tmpSource, v=True)
                for i in objs:
                    if (mc.polyEvaluate(i, f=True)) == polyCount and (mc.polyEvaluate(i, v=True)) == vertexCount:
                        tmpList.append(i)
            else:
                tmpList = objs
            for i in tmpList:
                self.uvKitProgressStep()
                if self.uvKitProgressBooleanCheck == True and mc.progressWindow(self.uvKitProgressControl, q=True, ic=True):
                    break
                mc.polyMultiLayoutUV(i, l=0, lm=0, sc=1, rbf=0, fr=False,
                ps=0.5, gu=1, psc=0, gv=1, su=scaleInput, sv=scaleInput,
                ou=offsetUTemp, ov=offsetVTemp)
                mc.select(i)
                mm.eval('PolySelectConvert 4;')
                mc.polyEditUV(u=moveU, v=moveV)
                mc.polyEditUV(u=udimUMove, v=udimVMove)
                if countToMaxU == maxU:
                    countToMaxU = 1
                    moveU = 0
                    countToMaxV = countToMaxV + 1
                    moveV = (moveV + moveUBase)
                else:
                    moveU = (moveU + moveUBase)
                    countToMaxU = countToMaxU + 1
                if countToMaxV > maxV:
                    udimUMove = udimUMove + 1
                    moveV = 0
                    countToMaxV = 1
                if udimUMove > 9:
                    udimUMove = 0
                    udimVMove = udimVMove + 1
                if (uvKitModifier & 8) > 0:
                    continue
                else:
                    objs.remove(i)
            if (uvKitModifier & 8) > 0:
                if (countToMaxU == 1) and (countToMaxV == 1):
                    pass
                else:
                    udimUMove = udimUMove + 1
                moveU = 0
                moveV = 0
                countToMaxU = 1
                countToMaxV = 1
                for i in tmpList:
                    objs.remove(i)
        mc.select(objSel)
        self.uvKitProgressEnd()
    def uvKitLayStack(self, _=False):
        uvKitModifier = mc.getModifiers()
        if uvKitModifier == 0:
            self.uvKitLayStack()
        if (uvKitModifier & 8) > 0:
            self.uvKitLayGatherShells()
    def uvKitLayStack(self, _=False):
        uvKitModifier = mc.getModifiers()
        uvKitLayStackSel = mc.ls(sl=True, typ="transform")
        if uvKitModifier == 0 or (uvKitModifier & 8) > 0:
            if uvKitLayStackSel == []:
                print("Please select an object!")
            else:
                self.uvKitProgressCheck(len(uvKitLayStackSel))
                for i in uvKitLayStackSel:
                    if uvKitModifier == 0:
                        mc.select(i)
                        testVal = self.uvKitEqualizerGet(1)
                    mc.polyMultiLayoutUV(i, l=0, lm=0, sc=1, rbf=0, fr=False,
                       ps=0.5, gu=1, psc=0, gv=1, ou=0.005, ov=0.005, su=self.uvKitLayStackSizeVal, sv=self.uvKitLayStackSizeVal)
                    if uvKitModifier == 0:
                        mc.select(i)
                        self.uvKitEqualizerSet(1, "Stack")
                    self.uvKitProgressStep()
                    if self.uvKitProgressBooleanCheck == True and mc.progressWindow(self.uvKitProgressControl, q=True, ic=True):
                        break
        else:
            mm.eval("texStackShells({});")
        self.uvKitProgressEnd()
        mc.select(uvKitLayStackSel)   
    def uvKitModAlignRef(self, _=False):
        uvKitModAlignRefSel = mc.ls(sl=True, fl=True)
        self.uvKitModAlignRefPivot = self.uvKitGetBoundingBox(uvKitModAlignRefSel)
    def uvKitModAlign(self, _=False):
        uvKitModifier = mc.getModifiers()
        if self.uvKitModAlignRefPivot:
            uvKitModAlignSel = mc.ls(sl=True, fl=True)
            uvKitModAlignShells = self.uvKitGetUVShells( uvKitModAlignSel )
            for i in uvKitModAlignShells:
                uvKitModAlignPivot = self.uvKitGetBoundingBox(i)
                uvKitModAlignUValue = self.uvKitModAlignRefPivot[0] - uvKitModAlignPivot[0]
                uvKitModAlignVValue = self.uvKitModAlignRefPivot[1] - uvKitModAlignPivot[1]
                mc.select(i, r=True)
                if uvKitModifier == 0:                  
                    mc.polyEditUV(u=0, v=uvKitModAlignVValue, r=True, s=False)
                if (uvKitModifier & 8) > 0:
                    mc.polyEditUV(u=uvKitModAlignUValue, v=0, r=True, s=False)
                if (uvKitModifier & 4) > 0:
                    mc.polyEditUV(u=uvKitModAlignUValue, v=uvKitModAlignVValue, r=True, s=False)
        else:
            mc.warning("Please set a Reference (Use the Middle Mouse Button)")
    def uvKitDistribute(self, _=False):
        uvKitModifier = mc.getModifiers()
        if uvKitModifier == 0:
            uvKitDisUVal = self.uvKitLaySpreadSizeVal
            uvKitDisVVal = 0
        if (uvKitModifier & 1) > 0:
            uvKitDisUVal = -(self.uvKitLaySpreadSizeVal)
            uvKitDisVVal = 0
        if (uvKitModifier & 8) > 0:
            if (uvKitModifier & 1) > 0:
                uvKitDisUVal = 0
                uvKitDisVVal = -(self.uvKitLaySpreadSizeVal)
            else:
                uvKitDisUVal = 0
                uvKitDisVVal = self.uvKitLaySpreadSizeVal   
        uvKitDisSelList = mc.ls(sl=True)
        uvKitDisGrowVal = 0
        for i in uvKitDisSelList:
            mc.select(i)
            mm.eval('PolySelectConvert 4;')
            mc.polyEditUV(u=(uvKitDisUVal*uvKitDisGrowVal), v=(uvKitDisVVal*uvKitDisGrowVal))
            uvKitDisGrowVal = uvKitDisGrowVal + 1
        mc.select(uvKitDisSelList)
    def uvKitModRotateUV(self, uvKitModRotClock, _=False):
        uvKitModifier = mc.getModifiers()
        for i in self.uvKitRotateAngleValues:
            if mc.menuItem("uvKitModRot%sRB" % i, q=True, rb=True):
                if (uvKitModifier & 8) > 0: uvKitModRotVal = i
                else:
                    uvKitModRotVal = -i
        uvKitModRotSel = mc.ls(sl=True, fl=True)
        uvKitModRotSelTmp = mc.ls(sl=True, fl=True)
        if (uvKitModifier & 1) > 0:
            uvKitModRotTmpList = self.uvKitGetUVShells( uvKitModRotSelTmp )
            for i in uvKitModRotTmpList:
                uvKitModRotPivot = self.uvKitGetBoundingBox(i)
                mc.polyEditUV(i, pu=uvKitModRotPivot[0], pv=uvKitModRotPivot[1], a = uvKitModRotVal)
            mc.select(uvKitModRotSel)
        else:
            if '2017' in self.uvKitMayaVersion:
                mm.eval('polyRotateUVs %s;' % uvKitModRotVal)                
            else:
                mm.eval('polyRotateUVs %s 1' % uvKitModRotVal)
    def uvKitModFlipUV(self, _=False):
        uvKitModifier = mc.getModifiers()
        uvKitModFlipSel = mc.ls(sl=True, fl=True)
        uvKitModFlipSelTmp = mc.ls(sl=True, fl=True)
        if uvKitModifier == 0:
            mc.FlipUVs()
        if (uvKitModifier & 8) > 0: 
            uvKitModFlipTmpList = self.uvKitGetUVShells( uvKitModFlipSelTmp )
            for i in uvKitModFlipTmpList:
                uvKitModFlipPivot = self.uvKitGetBoundingBox(i)
                mc.polyFlipUV(ft=0, l=True, up=True, pu=uvKitModFlipPivot[0], pv=uvKitModFlipPivot[1])
        if (uvKitModifier & 1) > 0:
            for i in (mc.ls(sl=True)):
                mc.polyMultiLayoutUV(fr=True, l=0, rbf=0, sc=0, psc=0)
        mc.select(uvKitModFlipSel)
    def uvKitModOrient(self, _=False):
        uvKitModifier = mc.getModifiers()
        if uvKitModifier == 0:
            mc.UVOrientShells()
        if (uvKitModifier & 8) > 0:
            mc.u3dLayout(rot=3, trs=False, ls=0)
        if (uvKitModifier & 4) > 0:
            mc.u3dLayout(rot=4, trs=False, ls=0) 
        if (uvKitModifier & 1) > 0:
            mc.u3dLayout(rot=5, trs=False, ls=0)     
    def uvKitEqualizeCall(self, _=False):
        uvKitModifier = mc.getModifiers()
        if uvKitModifier == 0:
            if self.uvKitEActiveRatio:
                self.uvKitEqualizerSet(1, "Equalize")
            else:
                mc.warning("Please set a source")
        if (uvKitModifier & 8) > 0:
            self.uvKitEqualizerGet(1)
    def uvKitEqualizerGet(self, set_active):
        uvKitEUVArea = 0
        uvKitEFaceArea = 0
        uvKitEqSel = mc.ls(sl=True, fl=True)
        if len(uvKitEqSel) == 1:
            util = om.MScriptUtil()
            util.createFromDouble(0.0)
            areaPtr = util.asDoublePtr() 
            mm.eval("PolySelectConvert 1")      
            uvKitEomSel = om.MSelectionList()
            om.MGlobal.getActiveSelectionList(uvKitEomSel)
            it = om.MItSelectionList(uvKitEomSel)
            while not it.isDone():
                uvKitEPath = om.MDagPath()
                uvKitEElement = om.MObject()
                it.getDagPath(uvKitEPath,uvKitEElement)
                fn = om.MFnDependencyNode(uvKitEPath.node())
                if not uvKitEElement.isNull():
                    if uvKitEElement.apiType() == om.MFn.kMeshPolygonComponent:
                        itPoly = om.MItMeshPolygon(uvKitEPath,uvKitEElement)
                        while not itPoly.isDone():
                            itPoly.getUVArea(areaPtr)
                            uvKitEqArea = om.MScriptUtil.getDouble(areaPtr)
                            uvKitEUVArea += uvKitEqArea
                            itPoly.getArea(areaPtr,om.MSpace.kWorld)
                            uvKitEqArea = om.MScriptUtil.getDouble(areaPtr)
                            uvKitEFaceArea += uvKitEqArea
                            itPoly.next()
                it.next()
            uvKitEUVRatio = uvKitEUVArea / uvKitEFaceArea
            if set_active == 1:
                self.uvKitEActiveRatio = uvKitEUVRatio
                self.uvKitEActiveObject = uvKitEqSel[0]
            mc.select(uvKitEqSel)
            om.MGlobal.displayInfo("The current source is: %s" % self.uvKitEActiveObject)
            return uvKitEUVRatio
        else:
            print('Please select only one object.')
    def uvKitEqualizerSet(self, obj, uvKitEqPivCheck):
        uvKitEqSel = mc.ls(sl=True, fl=True)
        for i in uvKitEqSel:
            mc.select(i)
            uvKitECurrentRatio = self.uvKitEqualizerGet(0)
            if uvKitECurrentRatio == 0:
                uvKitECurrentRatio = 1
            uvKitEScaleRatio = self.uvKitEActiveRatio / uvKitECurrentRatio
            uvKitEScaleRatio = sqrt(uvKitEScaleRatio)
            mm.eval("PolySelectConvert 4")  
            uvKitEqBB = mc.polyEvaluate(bc2=True)
            uvKitEqPivot = [0,0]
            if uvKitEqPivCheck == "Equalize":
                uvKitEqPivot[0] = ((uvKitEqBB[0][0] + uvKitEqBB[0][1]) /2 )
                uvKitEqPivot[1] = ((uvKitEqBB[1][0] + uvKitEqBB[1][1]) /2 )
            mc.polyEditUV(pu=uvKitEqPivot[0], pv=uvKitEqPivot[1], su=uvKitEScaleRatio, sv=uvKitEScaleRatio)
        mc.select(uvKitEqSel)
    def uvKitLSStart(self, _=False):
        self.uvKitLSSliderWindow()
        self.uvKitLSRun()
    def uvKitLSRun(self, _=False):
        uvKitLSList = mc.ls(sl=True, fl=True)
        uvKitLSSliderVal = mc.floatSliderGrp('uvKitLSSlider', q=True, v=True)
        self.uvKitLSScale = uvKitLSSliderVal / self.uvKitLSBase
        self.uvKitLSBase = self.uvKitLSBase * self.uvKitLSScale
        for i in uvKitLSList:
            mc.select(i, r=True)
            mm.eval('textureWindowSelectConvert 4;')
            mm.eval('polySelectBorderShell 0;')
            uvKitBBVal = mc.polyEvaluate(bc2=True, ae=True)
            uvKitLSPivot = [0,0]
            uvKitLSPivot[0] = ((uvKitBBVal[0][0] + uvKitBBVal[0][1]) /2 )
            uvKitLSPivot[1] = ((uvKitBBVal[1][0] + uvKitBBVal[1][1]) /2 )
            mc.polyEditUVShell(pu=uvKitLSPivot[0], pv=uvKitLSPivot[1], su=self.uvKitLSScale, sv=self.uvKitLSScale)
        mc.select(uvKitLSList, r=True)
    def uvKitLSDone(self, uvKitLSList, _=False):
        self.uvKitLSBase = 1.0
        self.uvKitLSScale = 1.0
        if (mc.window(self.uvKitLSSliderWinID, exists=True)):
            mc.deleteUI(self.uvKitLSSliderWinID, wnd=True)
            mc.windowPref(self.uvKitLSSliderWinID, r=True)
    def uvKitLSSliderWindow(self, _=False):
        if (mc.window(self.uvKitLSSliderWinID, exists=True)):
            mc.deleteUI(self.uvKitLSSliderWinID, wnd=True)
            mc.windowPref(self.uvKitLSSliderWinID, r=True)
        mc.window(self.uvKitLSSliderWinID, s=False, tlb=True, t="Local Scale")
        mc.columnLayout(adj=True)
        mc.rowLayout(nc=2)
        mc.floatSliderGrp('uvKitLSSlider', en=True, field=True, cw2=(70, 150), ss=0.01, 
        min=0.01, max=10.0, fmn=0.01, fmx=1.0, value=1.0, h=30, cc=self.uvKitLSRun)
        mc.button('uvKitLSDoneBtn', label="Done", en=True, h=30, w=100, c = self.uvKitLSDone,
        ann='Finish the local scale process')
        mc.setParent(top=True)
        mc.showWindow(self.uvKitLSSliderWinID)
        mc.window(self.uvKitLSSliderWinID, e=True, w=336, h=37)
    def uvKitCPCall(self, uvKitCPButton, _=False):
        uvKitModifier = mc.getModifiers()
        if uvKitModifier == 0:
            if uvKitCPButton == "Create / Del":
                self.uvKitCPcreateShader("MAT_checkerPattern", "UVCheckerPattern_1K.tga")
                self.uvKitCPcreateShader("MAT_uvDirection", "UVDirection_1K.tga")
            if uvKitCPButton == "Un / Assign":
                self.uvKitCPassignShader("MAT_checkerPattern")
        if (uvKitModifier & 1) > 0:
            if uvKitCPButton == "Create / Del":
                self.uvKitCPdeleteShader("MAT_checkerPattern")
                self.uvKitCPdeleteShader("MAT_uvDirection")
            if uvKitCPButton == "Un / Assign":
                self.uvKitCPremoveShader()
        if (uvKitModifier & 8) > 0:
            if uvKitCPButton == "Un / Assign":
                self.uvKitCPassignShader("MAT_uvDirection")
    def uvKitCPcreateShader(self, uvKitCPCreateName, uvKitTextureFile, _=False):
        uvKitCPshader = mc.shadingNode('surfaceShader', asShader=True, n=("%s" % uvKitCPCreateName) )
        uvKitCPfileNode = mc.shadingNode('file', asTexture=True, n=("%sTex" % uvKitCPCreateName) )
        uvKitCPnode = mc.shadingNode('place2dTexture', asUtility=True, n=("%s_place2D" % uvKitCPCreateName) )
        uvKitCPSG = mc.sets(r=True, nss=True, em=True, n=("%sSG" % uvKitCPCreateName) )
        mc.connectAttr(uvKitCPshader + '.outColor', uvKitCPSG + '.surfaceShader', f=True)
        mc.connectAttr(uvKitCPfileNode + '.outColor', uvKitCPshader + '.outColor', f=True)
        mc.connectAttr(uvKitCPnode + ".coverage", uvKitCPfileNode + ".coverage", f=True)
        mc.connectAttr(uvKitCPnode + ".translateFrame", uvKitCPfileNode + ".translateFrame", f=True)
        mc.connectAttr(uvKitCPnode + ".rotateFrame", uvKitCPfileNode + ".rotateFrame", f=True)
        mc.connectAttr(uvKitCPnode + ".mirrorU", uvKitCPfileNode + ".mirrorU", f=True)
        mc.connectAttr(uvKitCPnode + ".mirrorV", uvKitCPfileNode + ".mirrorV", f=True)
        mc.connectAttr(uvKitCPnode + ".stagger", uvKitCPfileNode + ".stagger", f=True)
        mc.connectAttr(uvKitCPnode + ".wrapU", uvKitCPfileNode + ".wrapU", f=True)
        mc.connectAttr(uvKitCPnode + ".wrapV", uvKitCPfileNode + ".wrapV", f=True)
        mc.connectAttr(uvKitCPnode + ".repeatUV", uvKitCPfileNode + ".repeatUV", f=True) 
        mc.connectAttr(uvKitCPnode + ".offset", uvKitCPfileNode + ".offset", f=True)
        mc.connectAttr(uvKitCPnode + ".rotateUV", uvKitCPfileNode + ".rotateUV", f=True)
        mc.connectAttr(uvKitCPnode + ".noiseUV", uvKitCPfileNode + ".noiseUV", f=True) 
        mc.connectAttr(uvKitCPnode + ".vertexUvOne", uvKitCPfileNode + ".vertexUvOne", f=True)
        mc.connectAttr(uvKitCPnode + ".vertexUvTwo", uvKitCPfileNode + ".vertexUvTwo", f=True)
        mc.connectAttr(uvKitCPnode + ".vertexUvThree", uvKitCPfileNode + ".vertexUvThree", f=True)
        mc.connectAttr(uvKitCPnode + ".vertexCameraOne", uvKitCPfileNode + ".vertexCameraOne", f=True)
        mc.connectAttr(uvKitCPnode + ".outUV", uvKitCPfileNode + ".uv", f=True)
        mc.connectAttr(uvKitCPnode + ".outUvFilterSize", uvKitCPfileNode + ".uvFilterSize", f=True)
        uvKitCPscriptPath = os.path.dirname(os.path.realpath(__file__))
        uvKitCPtexturePath = uvKitCPscriptPath + ('/%s' % uvKitTextureFile)
        mc.setAttr("%sTex.fileTextureName" % uvKitCPCreateName, uvKitCPtexturePath, type='string')
    def uvKitCPassignShader(self, uvKitCPAssignName, _=False):
        mc.sets(e=True, fe='%sSG' % uvKitCPAssignName)
    def uvKitCPremoveShader(self, _=False):
        mc.sets(e=True, fe='initialShadingGroup')
    def uvKitCPdeleteShader(self, uvKitCPDelShaName, _=False):
        mc.hyperShade(objects="%s" % uvKitCPDelShaName)
        mc.sets(e=True, fe='initialShadingGroup')
        mc.select('%s' % uvKitCPDelShaName, '%sTex' % uvKitCPDelShaName, '%s_place2D' % uvKitCPDelShaName, '%sSG' % uvKitCPDelShaName, r=True, ne=True)
        mc.delete()
    def uvKitCPsetK(self, uvKitSetKNum, _=False):
        mc.setAttr("MAT_checkerPattern_place2D.repeatU", uvKitSetKNum)
        mc.setAttr("MAT_checkerPattern_place2D.repeatV", uvKitSetKNum)
        mc.setAttr("MAT_uvDirection_place2D.repeatU", uvKitSetKNum)
        mc.setAttr("MAT_uvDirection_place2D.repeatV", uvKitSetKNum)
    def uvKitTransSetSource(self, _=False):
        self.uvKitTransSourceObject = mc.ls(sl=True)
        mc.textScrollList("uvKitTransSourceList", e=True, ra=True)
        for i in self.uvKitTransSourceObject:
            mc.textScrollList("uvKitTransSourceList", e=True, a=(i))
    def uvKitTransSetTarget(self, _=False):
        self.uvKitTransTargetObject = mc.ls(sl=True)
        mc.textScrollList("uvKitTransTargetList", e=True, ra=True)
        for i in self.uvKitTransTargetObject:
            mc.textScrollList("uvKitTransTargetList", e=True, a=(i))
    def uvKitTransCopyUVs(self, _=False):
        if mc.menuItem(self.uvKitWorldRB, q=True, rb=True):
            self.uvKitTransSampleSpace = 0
        if mc.menuItem(self.uvKitLocalRB, q=True, rb=True):
            self.uvKitTransSampleSpace = 1    
        if mc.menuItem(self.uvKitCmptRB, q=True, rb=True):
            self.uvKitTransSampleSpace = 4
        if mc.menuItem(self.uvKitTopoRB, q=True, rb=True):
            self.uvKitTransSampleSpace = 5
        if mc.menuItem(self.uvKitTransRBScopeAll, q=True, rb=True):
            self.uvKitTransOMScope = 2
        if mc.menuItem(self.uvKitTransRBScopeCurrent, q=True, rb=True):
            self.uvKitTransOMScope = 1
        if len(self.uvKitTransTargetObject) > 50:
            self.uvKitProgressCheck(len(self.uvKitTransTargetObject))
        uvKitTransSourcePos = 0
        for i in self.uvKitTransTargetObject:
            if len(self.uvKitTransSourceObject) == uvKitTransSourcePos:
                break
            uvKitSourceUVSet = mc.polyUVSet(self.uvKitTransSourceObject[uvKitTransSourcePos], q=True, currentUVSet=True)
            uvKitTargetUVSet = mc.polyUVSet(i, q=True, currentUVSet=True)
            mc.transferAttributes(self.uvKitTransSourceObject[uvKitTransSourcePos], i, uvs=self.uvKitTransOMScope,
            pos=0, nml=0, col=0, spa=self.uvKitTransSampleSpace, sus=("%s" % uvKitSourceUVSet), 
            tus=("%s" % uvKitTargetUVSet), sm=3, fuv=0, clb=1)
            mc.DeleteHistory()
            self.uvKitProgressStep()
            if self.uvKitProgressBooleanCheck == True and mc.progressWindow(self.uvKitProgressControl, q=True, ic=True):
                break
            if len(self.uvKitTransSourceObject) > 1:
                uvKitTransSourcePos = uvKitTransSourcePos + 1
        self.uvKitProgressEnd()
class UvKitAboutClass:    
    def __init__(self):
        self.uvKitAboutWinID = "uvKitWinAbout"
        self.uvKitAboutUI()
    def uvKitAboutUI(self, _=False):    
        if (mc.window(self.uvKitAboutWinID, exists=True)):
            mc.deleteUI(self.uvKitAboutWinID, wnd=True)
            mc.windowPref(self.uvKitAboutWinID, r=True)
        mc.window(self.uvKitAboutWinID, s=False, tlb=True, t="About")
        mc.columnLayout(adj=True)
        mc.rowLayout(nc=1)
        mc.text(l='', h=10)
        mc.setParent('..')
        mc.rowLayout(nc=1)
        mc.text(l='<font color=#3cb777><h3>UV Toolkit v1.3</h3></font>', al='center', w=196, h=20)
        mc.setParent('..')
        mc.rowLayout(nc=1)
        mc.text(l='Author: Erik Lehmann \nCopyright 2020 Erik Lehmann', al='center', w=196, h=40)
        mc.setParent('..')
        mc.rowLayout(nc=1)
        mc.text(l='<font color=#3cb777><h3>Feedback Or Questions?</h3></font>', al='center', w=196, h=35)
        mc.setParent('..')
        mc.rowLayout(nc=3)
        mc.text(l='', w=21)
        mc.textField(tx='contact@eriklehmann.com', ebg=False, ed=False, w=154, h=30)
        mc.text(l='', w=21)
        mc.setParent('..')
        mc.rowLayout(nc=1)
        mc.text(l='<font color=#3cb777><h3>More About My Work</h3></font>', al='center', w=196, h=35)
        mc.setParent('..')
        mc.rowLayout(nc=4)
        mc.text(l='', w=10)
        mc.button(l='Website', ann='Explore the work of Filmmaker and Build TD Erik Lehmann', w=85, h=30,
        c=lambda *_:self.uvKitAboutOpenBrowser(uvKitAboutSiteCode='Website'))
        mc.button(l='Gumroad', ann="Find more useful resources for Maya on Gumroad.", w=85, h=30, 
        c=lambda *_:self.uvKitAboutOpenBrowser(uvKitAboutSiteCode='Gumroad'))
        mc.text(l='', w=10)
        mc.setParent('..')
        mc.rowLayout(nc=4)
        mc.text(l='', w=10)
        mc.button(l='Artstation', ann="Erik Lehmann's Artstation Profile", w=85, h=30,
        c=lambda *_:self.uvKitAboutOpenBrowser(uvKitAboutSiteCode='Artstation'))
        mc.button(l='Facebook', ann='Art Of Erik Lehmann on Facebook', w=85, h=30,
        c=lambda *_:self.uvKitAboutOpenBrowser(uvKitAboutSiteCode='Facebook'))
        mc.text(l='', w=10)
        mc.setParent(top=True)
        mc.showWindow(self.uvKitAboutWinID)
        mc.window(self.uvKitAboutWinID, e=True, w=200, h=260)
    def uvKitAboutOpenBrowser(self, uvKitAboutSiteCode, _=False):
        if uvKitAboutSiteCode == 'Website':
            mc.launch(web="http://www.eriklehmann.com/")
        elif uvKitAboutSiteCode == 'Gumroad':
            mc.launch(web="https://gumroad.com/eriklehmann")    
        elif uvKitAboutSiteCode == 'Artstation':
            mc.launch(web="https://www.artstation.com/eriklehmann")
        elif uvKitAboutSiteCode == 'Facebook':
            mc.launch(web="https://www.facebook.com/ArtOfErikLehmann/")