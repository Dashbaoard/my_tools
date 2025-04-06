from PySide2.QtWidgets import QApplication
for one in QApplication.topLevelWidgets():
	try:
		one.move(0,0)
	except:
		pass

for win in cmds.lsUI(type='window'):
	cmds.window(win,e=1,tlc=[0,0])