#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
_____ _____  ______           _____ ______     
/ ____|  __ \|  ____|   /\    / ____|  ____|_   
| |    | |__) | |__     /  \  | (___ | |__ _| |_ 
| |    |  _  /|  __|   / /\ \  \___ \|  __|_   _|
| |____| | \ \| |____ / ____ \ ____) | |____|_|  
\_____|_|  \_\______/_/    \_\_____/|______|    

"""

import maya.cmds as mc
import maya.api.OpenMaya as om

# uses python maya 2

maya_useNewAPI = True

# 版本号
class MayaVerObj():
    def __init__(self):
        self.num = None 
        self.extnum = 0


def cPwhatmayaversion():
    verstring = mc.about(v=True)
    
    splited = verstring.split()
    num = None 
    extnum = 0
    
    for r in splited:
        if "20" in r:
            num = int(r)
            break
    
    i = -1
    for r in splited:
        i += 1
        if r.lower() == "extension" or r.lower() == "ext":
            j = i+1
            for j in range(len(splited)):
                if splited[j].isdigit():
                    extnum = int(splited[j])
                    break
            break
    
    if not num:
        raise Exception("can't get maya version")
    
    mayavobj = MayaVerObj()
    mayavobj.num = num 
    mayavobj.extnum = extnum 
    return mayavobj

global_creasePlus_mayaver = cPwhatmayaversion()

def getmayaver():
    global global_creasePlus_mayaver
    return global_creasePlus_mayaver


class CpMsg:

    kNoSel = 'nothing is selected'
    kNoSelCurve = 'no curve(s) selected'
    kNoSelMesh = 'no mesh(es) selected'
    kNoSelEdge = 'no edge(s) selected'
    kNoSelVert = 'no vertice(s) selected'
    kNoSelFace = 'no face(s) selected'

    kSelOneMesh = 'select one mesh'
    kSelMesh = 'mesh(es) must be selected'
    kSelEdge = 'edge(s) must be selected'
    kSelFace = 'face(s) must be selected'
    kSelVert = 'vertice(s) must be selected'

    kSelEdgeOrOneMesh = 'select edge(s) or a mesh'

    kSelCurveCv = 'curve cv(s) must be selected'
    kWorksForOne = 'works just for one entity'

    kNoHardEdges = 'no hard edge(s) were found'

    kSelLeastTwoMesh = 'select at least two meshes'
    kSelLeastTwoCurve = 'select at least two curves'

    kInvalidFuncArgs = 'function called with invalid arguments'

    kRequModelView = 'you are required to be in a modeling view/pan'
    kWrongSel = 'wrong selection'

    kcPnodePluginNotLoaded = \
        'creasePlus nodes plugin must be loaded to use this command'


# obj assumed to be a parent

def cPgotoChild(obj, mfntyp):
    dagn = om.MFnDagNode(obj)
    for i in range(dagn.childCount()):
        cur = dagn.child(i)
        if cur.hasFn(mfntyp):
            return cur
    return om.MObject.kNullObj


def cPshapeDagPath(obj):
    dagn = om.MFnDagNode(obj)
    return dagn.getPath()


def cPhardEdgesStrings(shape):

    sel = om.MSelectionList()
    sel.add(shape)

    dagp = sel.getDagPath(0)

    edgeIter = om.MItMeshEdge(dagp)
    selStrings = []
    shapeString = dagp.partialPathName()
    while not edgeIter.isDone():
        if edgeIter.isSmooth == False:
            selStrings.append(shapeString + '.e['
                              + str(edgeIter.index()) + ']')

        edgeIter.next()

    return selStrings


def cPgetShapeStringsFromSel(mfntyp):

    sel = om.MGlobal.getActiveSelectionList()
    selIt = om.MItSelectionList(sel)

    selStrings = []
    dagFn = om.MFnDagNode()
    while not selIt.isDone():

        if selIt.itemType() != selIt.kDagSelectionItem:
            selIt.next()
            continue

        obj = selIt.getDependNode()

        if not obj.hasFn(mfntyp):

            obj = cPgotoChild(obj, mfntyp)

            if not obj.hasFn(mfntyp):
                selIt.next()
                continue

        dagFn.setObject(obj)
        selStrings.append(dagFn.partialPathName())
        selIt.next()

    return selStrings


def cPcameraDominantPlane():

    activePan = mc.getPanel(wf=True)

    if mc.getPanel(to=activePan) != 'modelPanel':
        mc.error(CpMsg.kRequModelView)

    camPos = mc.camera(mc.modelEditor(activePan, q=True, cam=True),
                       q=True, p=True)
    camTarget = mc.camera(mc.modelEditor(activePan, q=True, cam=True),
                          q=True, wci=True)

    camDir = om.MVector(abs(camTarget[0] - camPos[0]), abs(camTarget[1]
                        - camPos[1]), abs(camTarget[2] - camPos[2]))

    maxv = 0
    ddir = 'x'
    if maxv < camDir.x:
        maxv = camDir.x
        ddir = 'x'
    if maxv < camDir.y:
        maxv = camDir.y
        ddir = 'y'
    if maxv < camDir.z:
        maxv = camDir.z
        ddir = 'z'

    return ddir


# mc.ls(sl=True)
# get shape + v, e, f comps in a tuple

def cPgetShapeAndCoStrings(mselit):

    shape = None
    v = None
    e = None
    f = None

    if mselit.itemType() != mselit.kDagSelectionItem:
        return (shape, v, e, f)

    hasComp = mselit.hasComponents()

    if hasComp == True:

        comp = mselit.getComponent()

        if comp[0].node().hasFn(om.MFn.kMesh):
            shape = comp[0]

        if comp[1].hasFn(om.MFn.kMeshPolygonComponent):
            f = comp[1]
        elif comp[1].hasFn(om.MFn.kMeshEdgeComponent):

            e = comp[1]
        elif comp[1].hasFn(om.MFn.kMeshVertComponent):

            v = comp[1]
    else:

        obj = mselit.getDependNode()

        if not obj.hasFn(om.MFn.kMesh):
            obj = cPgotoChild(obj, om.MFn.kMesh)

        if obj.hasFn(om.MFn.kMesh):
            shape = cPshapeDagPath(obj)

    return (shape, v, e, f)


def cPfaceToHardEdgeStrings(dagp, faceComps):

    edgeIds = set()

    faceIt = om.MItMeshPolygon(dagp, faceComps)
    meshFn = om.MFnMesh(dagp.node())

    while not faceIt.isDone():

        fEdges = faceIt.getEdges()

        for idx in fEdges:
            if not meshFn.isEdgeSmooth(idx):
                edgeIds.add(idx)

        faceIt.next(None)  # maya api bug

    shapeString = dagp.partialPathName()
    return [shapeString + '.e[' + str(idx) + ']' for idx in edgeIds]


def cPedgeToStrings(dagp, edgeComps):

    edgeStrings = []
    edgeIt = om.MItMeshEdge(dagp, edgeComps)
    shapeString = dagp.partialPathName()
    while not edgeIt.isDone():

        edgeStrings.append(shapeString + '.e[' + str(edgeIt.index())
                           + ']')
        edgeIt.next()

    return edgeStrings


################################  CONTEXTS

# draw curve ctx

try:
    global_cPcurveCtxStr
except:
    global_cPcurveCtxStr = mc.curveCVCtx('cPcurveCtx', degree=1)

#

# booleanop context

try:
    global_cPboolOpCtxStr
except:
    global_cPboolOpCtxStr = mc.dragAttrContext('cPboolOpCtx')

global_cPboolOpAttrCnt = 3
global_cPboolOpAttrIter = 0


def cPboolOpIterSetVal(val):
    global global_cPboolOpAttrIter
    global_cPboolOpAttrIter = val
    return global_cPboolOpAttrIter % global_cPboolOpAttrCnt


def cPboolOpIterVal():
    global global_cPboolOpAttrIter
    return global_cPboolOpAttrIter % global_cPboolOpAttrCnt


def cPboolOpIterIncVal():
    global global_cPboolOpAttrIter
    global_cPboolOpAttrIter += 1
    return global_cPboolOpAttrIter % global_cPboolOpAttrCnt


#

# mirror context

try:
    global_cPmirrorCtxStr
except:
    global_cPmirrorCtxStr = mc.dragAttrContext('cPmirrorCtx')

global_cPmirrorAttrCnt = None
if getmayaver().num > 2016:
    global_cPmirrorAttrCnt = 1
else:
    global_cPmirrorAttrCnt = 3

global_cPmirrorAttrIter = 0


def cPmirrorIterSetVal(val):
    global global_cPmirrorAttrIter
    global_cPmirrorAttrIter = val
    return global_cPmirrorAttrIter % global_cPmirrorAttrCnt


def cPmirrorIterVal():
    global global_cPmirrorAttrIter
    return global_cPmirrorAttrIter % global_cPmirrorAttrCnt


def cPmirrorIterIncVal():
    global global_cPmirrorAttrIter
    global_cPmirrorAttrIter += 1
    return global_cPmirrorAttrIter % global_cPmirrorAttrCnt


#

# hbevel context

try:
    global_hBevelCtxStr
except:
    global_hBevelCtxStr = mc.dragAttrContext('hBevelCtx')

global_hBevelAttrCnt = 2
global_hBevelAttrIter = 0


def cPhBevelIterSetVal(val):
    global global_hBevelAttrIter
    global_hBevelAttrIter = val
    return global_hBevelAttrIter % global_hBevelAttrCnt


def cPhBevelIterVal():
    global global_hBevelAttrIter
    return global_hBevelAttrIter % global_hBevelAttrCnt


def cPhBevelIterIncVal():
    global global_hBevelAttrIter
    global_hBevelAttrIter += 1
    return global_hBevelAttrIter % global_hBevelAttrCnt


#

# curvebevel context

try:
    global_cPcurveBevelCtxStr
except:
    global_cPcurveBevelCtxStr = mc.dragAttrContext('cPcurveBvlCtx')

global_cPcurveBevelAttrCnt = 2
global_cPcurveBevelAttrIter = 0


def cPcurveBevelIterSetVal(val):
    global global_cPcurveBevelAttrIter
    global_cPcurveBevelAttrIter = val
    return global_cPcurveBevelAttrIter % global_cPcurveBevelAttrCnt


def cPcurveBevelIterVal():
    global global_cPcurveBevelAttrIter
    return global_cPcurveBevelAttrIter % global_cPcurveBevelAttrCnt


def cPcurveBevelIterIncVal():
    global global_cPcurveBevelAttrIter
    global_cPcurveBevelAttrIter += 1
    return global_cPcurveBevelAttrIter % global_cPcurveBevelAttrCnt


#

# crease tool context

try:
    global_cPcreaseCtxStr
except:
    global_cPcreaseCtxStr = mc.polyCreaseCtx('cPcreaseCtx', es=True,
            r=True)

#

# physical crease context

try:
    global_pCreaseCtxStr
except:
    global_pCreaseCtxStr = mc.dragAttrContext('pCreaseCtx')

global_pCreaseAttrCnt = 2
global_pCreaseAttrIter = 0


def cPpCreaseIterSetVal(val):
    global global_pCreaseAttrIter
    global_pCreaseAttrIter = val
    return global_pCreaseAttrIter % global_pCreaseAttrCnt


def cPpCreaseIterVal():
    global global_pCreaseAttrIter
    return global_pCreaseAttrIter % global_pCreaseAttrCnt


def cPpCreaseIterIncVal():
    global global_pCreaseAttrIter
    global_pCreaseAttrIter += 1
    return global_pCreaseAttrIter % global_pCreaseAttrCnt


#
def cPcontextUndo():
    if mc.currentCtx() == global_cPboolOpCtxStr:
        # mc.setToolTo('moveSuperContext')
        mc.dragAttrContext(global_cPboolOpCtxStr, e=True, reset=True)
        mc.setToolTo(global_cPboolOpCtxStr)
    elif mc.currentCtx() == global_hBevelCtxStr:

        # mc.setToolTo('moveSuperContext')
        mc.dragAttrContext(global_hBevelCtxStr, e=True, reset=True)
        mc.setToolTo(global_hBevelCtxStr)
    elif mc.currentCtx() == global_cPmirrorCtxStr:

        # mc.setToolTo('moveSuperContext')
        mc.dragAttrContext(global_cPmirrorCtxStr, e=True, reset=True)
        mc.setToolTo(global_cPmirrorCtxStr)
    elif mc.currentCtx() == global_cPcurveBevelCtxStr:

        # mc.setToolTo('moveSuperContext')
        mc.dragAttrContext(global_cPcurveBevelCtxStr, e=True, reset=True)
        mc.setToolTo(global_cPcurveBevelCtxStr)
    elif mc.currentCtx() == global_pCreaseCtxStr:

        # mc.setToolTo('moveSuperContext')
        mc.dragAttrContext(global_pCreaseCtxStr, e=True, reset=True)
        mc.setToolTo(global_pCreaseCtxStr)


try:
    global_creasePlusCtxUndoJob
except:
    global_creasePlusCtxUndoJob = mc.scriptJob(event=['Undo',
            cPcontextUndo])


############

def main():
    return None


if __name__ == '__main__':
    main()

