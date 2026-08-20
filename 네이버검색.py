import re

from openpyxl import Workbook
import requests
from bs4 import BeautifulSoup


URL = "https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query=%EB%B0%98%EB%8F%84%EC%B2%B4"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def get_article_titles(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    title_links = soup.select('a[data-heatmap-target=".tit"]')

    # 구형 네이버 뉴스 결과 페이지와도 호환
    if not title_links:
        title_links = soup.select("a.news_tit")

    articles = [
        (
            re.sub(
                r"\s+",
                " ",
                title_link.get_text("", strip=False).replace("새 창 열림", ""),
            ).strip(),
            title_link.get("href", ""),
        )
        for title_link in title_links
        if title_link.get("href")
    ]

    # 같은 기사에 여러 네이버뉴스 링크가 있을 수 있으므로 중복 제거
    unique_articles = []
    seen_urls = set()
    for title, article_url in articles:
        if article_url not in seen_urls:
            unique_articles.append((title, article_url))
            seen_urls.add(article_url)

    return unique_articles


def save_to_excel(articles, filename):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "네이버 뉴스"
    worksheet.append(["번호", "기사 제목", "기사 링크"])

    for number, (title, article_url) in enumerate(articles, start=1):
        worksheet.append([number, title, article_url])

    worksheet.freeze_panes = "A2"
    worksheet.column_dimensions["A"].width = 10
    worksheet.column_dimensions["B"].width = 70
    worksheet.column_dimensions["C"].width = 100
    workbook.save(filename)


if __name__ == "__main__":
    articles = get_article_titles(URL)
    for number, (title, article_url) in enumerate(articles, start=1):
        print(f"{number}. {title}")
        print(f"   {article_url}")

    save_to_excel(articles, "naver_result.xlsx")
    print("크롤링 결과를 naver_result.xlsx 파일에 저장했습니다.")