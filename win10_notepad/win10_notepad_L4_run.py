# coding = utf-8
"""
查看帮助
关于记事本
新建
新窗口
"""

import sys
from PySide6.QtGui import QFontDatabase,QFont,QTextCursor
from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QMainWindow,QApplication,QFontDialog,QFileDialog,QLabel
from PySide6.QtPrintSupport import QPrintDialog
from win10_notepad_L4_ui import Ui_MainWindow


class WinRun(QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
        """
        super().__init__()
        self.setupUi(self)
        # Setup the QTextEdit editor configuration
        self.fixedfont = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        self.fixedfont.setPointSize(12)
        self.plainTextEdit.setFont(self.fixedfont)



        # 自定义状态栏
        # 添加位置监测
        postion = QLabel("第1行，第1列")
        self.statusbar.addWidget(postion)
        self.plainTextEdit.cursorPositionChanged.connect(lambda: self.get_cursor(postion))

        #  添加缩放监测
        zoom_label = QLabel("100%")
        self.statusbar.addWidget(zoom_label)


        # 添加风格监测

        # 添加编码格式监测 不同系统使用其对应默认编码
        
        # 插入日期
        self.action_D.triggered.connect(self.insert_date_to_plainTextEdit)
        # 取消自动换行
        self.action_W.triggered.connect(self.reset_warp)


        # 添加字体设置 需要定义一个自己的 FontDialog 继续Dialog
        self.action_F_2.triggered.connect(self.get_fontdialog)
        # 添加打印支持
        self.action_P.triggered.connect(self.file_print)
        # 新建文件
        self.action_N.triggered.connect(self.new_file)
        # 打开文件
        self.action_O.triggered.connect(self.open_file)
        # 保存
        self.action_S.triggered.connect(self.save_file)
        # 另存为
        self.action_A.triggered.connect(self.save_file_as)
        # 恢复默认缩放
        self.action_2.triggered.connect(self.reset_font)

    def get_cursor(self,postion):
        cursor = self.plainTextEdit.textCursor()
        line = cursor.blockNumber()+1
        column = cursor.columnNumber()+1
        postion.setText(f"第{line}行，第{column}列")


    # if you edit in desinger use as follows!
    def insert_date_to_plainTextEdit(self):
        current_datetime = QDateTime.currentDateTime()
        formatted_time = current_datetime.toString("hh:mm yyyy/M/d")
        self.plainTextEdit.insertPlainText(formatted_time)

    def reset_warp(self, checked: bool):
        """
        根据复选框状态设置自动换行
        :param checked: 是否勾选（True: 关闭换行, False: 启用换行）
        """
        if checked:
            self.plainTextEdit.setLineWrapMode(self.plainTextEdit.LineWrapMode.WidgetWidth)
        else:
            self.plainTextEdit.setLineWrapMode(self.plainTextEdit.LineWrapMode.NoWrap)

    

    def get_fontdialog(self):
        # 获取当前字体作为初始值
        current_font = self.plainTextEdit.font()
        
        # 打开字体对话框
        font, ok = QFontDialog.getFont(current_font, self, "选择字体")
        
        # 只有用户点击 "OK" 并且 font 是 QFont 对象时才设置
        if ok and isinstance(font, QFont):
            self.plainTextEdit.setFont(font)

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec():
            self.plainTextEdit.print_(dlg.printer())


    def new_file(self):
        self.plainTextEdit.clear()
        self.setWindowTitle("Untitled")
        self.current_path = None
        # self.plainTextEdit.setFontPointSize(12)
        self.fixedfont.setPointSize(12)
      
    def open_file(self):
        open_file = QFileDialog().getOpenFileName(self, '打开', '~','文本文档(*.txt);;所有文件(*.*)')
        if open_file:
            self.recentlyOpen = True
            try:
                self.initialTitle = open_file[0]
                self.setWindowTitle(self.initialTitle)
                #self.setWindowTitle(open_file[0])
                with open(open_file[0], 'r') as f:
                    file_text = f.read()
                    self.plainTextEdit.setPlainText(file_text)
                self.current_path = open_file[0]
                self.recentlyOpen = False
            except FileNotFoundError:
                print("File not found")
        else:
            print("No file selected")

    def save_file(self):
        if self.current_path is not None:
            fileTextContent = self.plainTextEdit.toPlainText()
            with open(self.current_path, 'w') as f:
                f.write(fileTextContent)
                self.initialTitle = str(self.current_path)
                self.setWindowTitle(self.initialTitle)
        else:
            self.save_file_as()

    def save_file_as(self):
        pathName = QFileDialog.getSaveFileName(self, '另存为', '', '文本文档(*.txt)')
        fileTextContent = self.plainTextEdit.toPlainText()
        with open(pathName[0], 'w') as f:
            f.write(fileTextContent)
        self.current_path = pathName[0]
        self.initialTitle = pathName[0]
        self.setWindowTitle(pathName[0])     

    def reset_font(self):
        self.plainTextEdit.setFont( self.fixedfont)

    def create_new_instance(self):
        """
        槽函数：创建 MainWindow 类的一个新实例并显示它。
        这就是“自己调用自己”——当前实例创建了另一个同类型的实例。
        """
        # 创建一个新的 MainWindow 实例
        new_window = Ui_MainWindow("窗口") # 你可以传递不同的参数
        
        # 将新窗口存储在列表或字典中，防止被 Python 垃圾回收器回收
        # 如果你不保存引用，窗口可能在创建后立即被关闭或消失。
        # 这里我们简单地将它作为主窗口的一个属性保存。
        if not hasattr(self, 'child_windows'):
            self.child_windows = []
        self.child_windows.append(new_window)
        
        # 显示新窗口
        new_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WinRun()
    win.show()
    sys.exit(app.exec())