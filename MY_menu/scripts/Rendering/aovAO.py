import maya.cmds as cmds
cmds.shadingNode("cryptomatte", asShader=True, n="cryptomatte1")
cmds.shadingNode("aiAmbientOcclusion", asShader=True, n="AO5")

cmds.defaultNavigation(ce=True, s='AO5', d='aiAOV_AO.defaultValue')
cmds.defaultNavigation(ce=True, s='cryptomatte1', d='aiAOV_crypto_asset.defaultValue')
cmds.defaultNavigation(ce=True, s='cryptomatte1', d='aiAOV_crypto_material.defaultValue')
cmds.defaultNavigation(ce=True, s='cryptomatte1', d='aiAOV_crypto_object.defaultValue')
