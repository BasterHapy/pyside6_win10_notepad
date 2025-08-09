# coding = utf-8
"""
    自定义个一个QFontListView 继承子 QListView
    未在Windows上测试
"""

from PySide6.QtWidgets import QApplication,QListView
from PySide6.QtCore import QStringListModel
from PySide6.QtGui import QFontDatabase
import sys
# 首先来显示一下
class QFontListView(QListView):
    def __init__(self):
        super().__init__()
        self.model = QStringListModel(QFontDatabase.families())
        self.setModel(self.model)

