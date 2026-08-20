#DemoForm2.py
#DemoFrom2.ui 화면단 + DemoForm2.py 조작단
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
# 크롤링에 필요
from bs4 import BeautifulSoup
# 웹서버에 요청
import urllib.request
# 정규표현식 검색
import re




#미리 준비한 ui 화면단과 조작단을 연결
form_class = uic.loadUiType("DemoForm2.ui")[0]

#DemoForm 클래스 정의
class DemoForm2(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    def firstClick(self):
        
        with open("clien1.txt", "wt", encoding="utf-8") as f:
            for i in range(0, 10):
                url = "https://www.clien.net/service/board/sold?&od=T31&po={0}".format(i)
                request = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": (
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/131.0.0.0 Safari/537.36"
                        )
                    },
                )
                page = urllib.request.urlopen(request, timeout=10)
                soup = BeautifulSoup(page, "html.parser")

                titles = soup.find_all("span", attrs={"data-role": "list-title-text"})
                for tag in titles:
                    title = tag.text.strip()
                    print(title)
                    f.write(title + "\n")
        self.label1.setText("중고장터 크롤링 완료")
    def secondClick(self):
        self.label1.setText("두번째 버튼 클릭")
    def thirdClick(self):
        self.label1.setText("세번째 버튼 클릭")
    
#진입점을 체크해서 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = DemoForm2()
    dialog.show()
    sys.exit(app.exec())