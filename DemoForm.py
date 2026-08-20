#DemoForm.py
#DemoFrom.ui 화면단 + DemoForm.py 조작단
import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic

#미리 준비한 ui 화면단과 조작단을 연결
form_class = uic.loadUiType("DemoForm.ui")[0]

#DemoForm 클래스 정의
class DemoForm(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label.setText("Hello PyQt")

#진입점을 체크해서 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = DemoForm()
    dialog.show()
    sys.exit(app.exec())