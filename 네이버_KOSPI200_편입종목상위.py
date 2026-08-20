import csv
import re
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup


URL = "https://finance.naver.com/sise/sise_index.naver?code=KPI200"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}


def clean_text(value):
    """셀 안의 줄바꿈과 연속 공백을 정리한다."""
    return re.sub(r"\s+", " ", value).strip()


def parse_constituents_page(html):
    soup = BeautifulSoup(html, "html.parser")
    expected_headers = {
        "종목별",
        "현재가",
        "전일비",
        "등락률",
        "거래량",
        "거래대금(백만)",
        "시가총액(억)",
    }
    normalized_expected_headers = {
        re.sub(r"\s+", "", header) for header in expected_headers
    }

    for table in soup.find_all("table"):
        rows = []
        for row in table.find_all("tr"):
            cells = [clean_text(cell.get_text(" ", strip=True)) for cell in row.find_all(["th", "td"])]
            if cells:
                rows.append(cells)

        if not rows:
            continue

        header_index = next(
            (
                index
                for index, row in enumerate(rows)
                if normalized_expected_headers.issubset(
                    {re.sub(r"\s+", "", cell) for cell in row}
                )
            ),
            None,
        )
        if header_index is None:
            continue

        headers = rows[header_index]
        data = [row for row in rows[header_index + 1 :] if len(row) == len(headers)]
        return [dict(zip(headers, row)) for row in data]

    return []


def get_constituents_page_url(url=URL):
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")
    iframe = soup.find("iframe", title=lambda title: title and "편입종목상위" in title)
    if iframe is None or not iframe.get("src"):
        raise RuntimeError("편입종목상위 iframe을 찾지 못했습니다.")

    return urljoin(url, iframe["src"])


def add_page_parameter(url, page):
    parsed_url = urlsplit(url)
    query = dict(parse_qsl(parsed_url.query))
    query["page"] = str(page)
    return urlunsplit(parsed_url._replace(query=urlencode(query)))


def get_top_constituents(url=URL, total_count=200):
    page_url = get_constituents_page_url(url)
    constituents = []
    seen_names = set()

    for page in range(1, 21):
        response = requests.get(
            add_page_parameter(page_url, page), headers=HEADERS, timeout=15
        )
        response.raise_for_status()
        response.encoding = response.apparent_encoding

        page_items = parse_constituents_page(response.text)
        if not page_items:
            break

        for item in page_items:
            name = item["종목별"]
            if name not in seen_names:
                constituents.append(item)
                seen_names.add(name)

        if len(constituents) >= total_count:
            break

    return constituents[:total_count]


def save_csv(items, filename="kospi200_top_constituents.csv"):
    if not items:
        return

    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=items[0].keys())
        writer.writeheader()
        writer.writerows(items)


if __name__ == "__main__":
    constituents = get_top_constituents()

    for number, item in enumerate(constituents, start=1):
        print(
            f"{number:2}. {item['종목별']} | "
            f"현재가: {item['현재가']} | "
            f"등락률: {item['등락률']} | "
            f"거래량: {item['거래량']}"
        )

    save_csv(constituents)
    print(f"총 {len(constituents)}개 종목을 CSV 파일에 저장했습니다.")