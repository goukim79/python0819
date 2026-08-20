#web1.py
#웹크롤링을 연습
from bs4 import BeautifulSoup

#페이지를 로딩
page = open("Chap09_test.html", "rt", encoding="utf-8").read()

soup = BeautifulSoup(page, "html.parser")

# print(soup.prettify())

#<p> 몽땅 검색
#print(soup.find_all("p"))
# 첫번째 <p>만 검색
# print(soup.find("p"))
#반복문: .text 속성으로 <p>태그의 텍스트만 출력. 
# 빈줄을 삭제

f = open("Chap09_test.txt", "wt", encoding="utf-8")
for item in soup.find_all("p"):
    title = item.text.strip().replace("\n", "")
    print(title)
    f.write(title + "\n")
f.close()
