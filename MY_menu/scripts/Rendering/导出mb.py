import maya.app.renderSetup.model.renderSetup as renderSetup
import json
import maya.cmds as cmds
import subprocess
import os
import shutil

username = os.getlogin()

FP="C:/Users/{}/Documents/maya/projects/default/scenes/a.mb".format(username)
cmds.file(FP, force=True, options="v=0", typ="mayaBinary", es=True, pr=True)



# 指定你想要保存的JSON文件路径
json_file_path = r'C:\Users\{}\Documents\maya\RSTemplates\a.json'.format(username)

# 调用renderSetup API来导出所有渲染设置
renderSetupData = renderSetup.instance().encode()
with open(json_file_path, 'w') as json_file:
    json.dump(renderSetupData, json_file, indent=4)

print("Render settings have been exported to: " + json_file_path)