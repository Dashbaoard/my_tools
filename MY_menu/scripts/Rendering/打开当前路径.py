import maya.cmds as cmds
import os
os.startfile(os.path.dirname(cmds.file(query=True,loc=True)))