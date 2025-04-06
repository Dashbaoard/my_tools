import maya.app.renderSetup.model.renderSetup as renderSetup
import json
import maya.cmds as cmds
import subprocess
import os
import shutil

username = os.getlogin()

FP="C:/Users/{}/Documents/maya/projects/default/scenes/a.mb".format(username)
cmds.file(FP, open=True, force=True)




def importRenderSetup(filename):
    # 打开JSON文件并加载数据
    with open(filename, "r") as file:
        renderSetupData = json.load(file)
    
    # 使用renderSetup API导入渲染设置
    renderSetup.instance().decode(renderSetupData, renderSetup.DECODE_AND_OVERWRITE, None)

# 调用函数并传入你的JSON文件路径
importRenderSetup(r'C:\Users\{}\Documents\maya\RSTemplates\a.json'.format(username))



cmds.shadingNode("cryptomatte", asShader=True, n="cryptomatte1")
cmds.shadingNode("aiAmbientOcclusion", asShader=True, n="AO5")
try:
    cmds.defaultNavigation(ce=True, s='AO5', d='aiAOV_AO.defaultValue')
except:
    pass
cmds.defaultNavigation(ce=True, s='cryptomatte1', d='aiAOV_crypto_asset.defaultValue')
cmds.defaultNavigation(ce=True, s='cryptomatte1', d='aiAOV_crypto_material.defaultValue')
cmds.defaultNavigation(ce=True, s='cryptomatte1', d='aiAOV_crypto_object.defaultValue')
