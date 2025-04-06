# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UselessValue.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide2.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_UselessValueTool(object):
    def setupUi(self, UselessValueTool):
        if not UselessValueTool.objectName():
            UselessValueTool.setObjectName(u"UselessValueTool")
        UselessValueTool.resize(550, 639)
        self.horizontalLayout = QHBoxLayout(UselessValueTool)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.pushButton = QPushButton(UselessValueTool)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QFont.PreferDefault)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QCursor(Qt.ArrowCursor))
        self.pushButton.setMouseTracking(False)
        self.pushButton.setTabletTracking(False)
        self.pushButton.setFocusPolicy(Qt.StrongFocus)
        self.pushButton.setAcceptDrops(False)
        self.pushButton.setLayoutDirection(Qt.LeftToRight)
        self.pushButton.setAutoFillBackground(False)

        self.verticalLayout.addWidget(self.pushButton)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(UselessValueTool)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 3, 1, 1)

        self.label = QLabel(UselessValueTool)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.pushButton_2 = QPushButton(UselessValueTool)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 0, 0, 1, 1)

        self.comboBox = QComboBox(UselessValueTool)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 0, 8, 1, 1)

        self.listWidget = QListWidget(UselessValueTool)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.listWidget, 0, 4, 1, 1)

        self.listWidget_2 = QListWidget(UselessValueTool)
        self.listWidget_2.setObjectName(u"listWidget_2")
        self.listWidget_2.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.listWidget_2, 0, 2, 1, 1)

        self.label_3 = QLabel(UselessValueTool)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 5, 1, 1)

        self.label_4 = QLabel(UselessValueTool)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 7, 1, 1)

        self.listWidget_3 = QListWidget(UselessValueTool)
        self.listWidget_3.setObjectName(u"listWidget_3")
        self.listWidget_3.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.listWidget_3, 0, 6, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 4, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(UselessValueTool)

        self.comboBox.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(UselessValueTool)
    # setupUi

    def retranslateUi(self, UselessValueTool):
        UselessValueTool.setWindowTitle(QCoreApplication.translate("UselessValueTool", u"UselessValue", None))
#if QT_CONFIG(tooltip)
        self.pushButton.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pushButton.setText(QCoreApplication.translate("UselessValueTool", u"\u9009\u62e9\u6240\u6709", None))
        self.label_2.setText(QCoreApplication.translate("UselessValueTool", u"\u8f74\u5411\u7ec6\u5206\uff1a", None))
        self.label.setText(QCoreApplication.translate("UselessValueTool", u"\u534a\u5f84\uff1a", None))
        self.pushButton_2.setText(QCoreApplication.translate("UselessValueTool", u"\u7403", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("UselessValueTool", u"None", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("UselessValueTool", u"Pinched at pole", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("UselessValueTool", u"Sawtooth at pole", None))

        self.comboBox.setCurrentText(QCoreApplication.translate("UselessValueTool", u"Sawtooth at pole", None))
        self.label_3.setText(QCoreApplication.translate("UselessValueTool", u"\u9ad8\u5ea6\u7ec6\u5206\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("UselessValueTool", u"\u521b\u5efaUV\uff1a", None))
    # retranslateUi


