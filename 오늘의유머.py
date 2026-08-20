# web2.py
# 크롤링에 필요
from bs4 import BeautifulSoup
# 웹서버에 요청
import urllib.request
# 정규표현식 검색
import re

with open("humor.txt", "wt", encoding="utf-8") as f:
    for i in range(0, 10):
        url = "https://www.todayhumor.co.kr/board/list.php?table=humorbest&page={0}".format(i)
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
        titles = soup.find_all("td", attrs={"class": "subject"})
        for title_tag in titles:
            title = title_tag.get_text(strip=True)
            print(title)
            f.write(title + "\n")


