# coding = utf-8

from PySide6.QtWidgets import QDialog,QApplication,QVBoxLayout,QLabel,QLineEdit,QFontComboBox,QLis
import sys

class MyFontDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setSizeGripEnabled(True)
        self.setWindowTitle("字体")
        layout = QVBoxLayout()
        family_accel = QLabel("字体(&F)")
        
        
        family_edit = QLineEdit()
        family_edit.setReadOnly(True)
        family_list = QFontComboBox()
        # familyEdit->setFocusProxy(familyList);
        family_edit.setFocusProxy(family_list)
        
        family_accel.setBuddy(family_list)
        family_accel.setIndent(2)
        
        layout.addWidget(family_accel)
        layout.addWidget(family_edit)
        layout.addWidget(family_list)


        self.setLayout(layout)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myfont =  MyFontDialog()
    myfont.show()
    sys.exit(app.exec())

