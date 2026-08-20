# web2.py
# 크롤링에 필요
from bs4 import BeautifulSoup
# 웹서버에 요청
import urllib.request
# 정규표현식 검색
import re

with open("clien.txt", "wt", encoding="utf-8") as f:
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


