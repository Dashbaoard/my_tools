import maya.cmds as cmds

l1='locator1'
l2='locator2'
modT=cmds.ls(sl=True,sn=True)
cmds.matchTransform(l1,modT[0])
cmds.matchTransform(l2,modT[1])
cmds.matchTransform(modT[1],l1)
cmds.matchTransform(modT[0],l2)