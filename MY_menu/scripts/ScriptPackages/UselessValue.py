# _*_ coding: utf-8 _*_
# .@FileName:UselessValue
# .@Date....:2023-09-10-11 : 28 : 01
# .@Aurhor..:冥羽
# .@Contact.:1942598111@qq.com
'''
launch:
        import UselessValue as kt_FileName
        reload(FileName)
        FileName.main()
'''

from PySide2.QtWidgets import QApplication, QWidget
from UselessValueUI import Ui_UselessValueTool


class MyWindow(QWidget, Ui_UselessValueTool):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


#if __name__ == '__main__':

app = QApplication([])
window = MyWindow()
window.show()
app.exec_()


