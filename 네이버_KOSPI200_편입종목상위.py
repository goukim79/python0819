import csv
import re
import sys
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


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


class ConstituentWorker(QObject):
    """네트워크 요청을 GUI 스레드와 분리해 실행한다."""

    finished = pyqtSignal(list)
    failed = pyqtSignal(str)

    def __init__(self, url, total_count):
        super().__init__()
        self.url = url
        self.total_count = total_count

    def run(self):
        try:
            self.finished.emit(get_top_constituents(self.url, self.total_count))
        except Exception as error:
            self.failed.emit(str(error))


class ConstituentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.items = []
        self.thread = None
        self.worker = None
        self.setWindowTitle("KOSPI200 편입종목 조회")
        self.resize(1_100, 650)
        self.build_ui()

    def build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        title = QLabel("KOSPI200 편입종목 상위 조회")
        title.setObjectName("titleLabel")
        description = QLabel("네이버 금융에서 편입종목을 조회하고 CSV 파일로 저장합니다.")
        description.setObjectName("descriptionLabel")

        self.url_input = QLineEdit(URL)
        self.count_input = QSpinBox()
        self.count_input.setRange(1, 200)
        self.count_input.setValue(200)
        self.fetch_button = QPushButton("종목 조회")
        self.save_button = QPushButton("CSV 저장")
        self.save_button.setEnabled(False)

        settings = QGridLayout()
        settings.addWidget(QLabel("조회 URL"), 0, 0)
        settings.addWidget(self.url_input, 0, 1, 1, 3)
        settings.addWidget(QLabel("종목 수"), 1, 0)
        settings.addWidget(self.count_input, 1, 1)
        settings.addWidget(self.fetch_button, 1, 2)
        settings.addWidget(self.save_button, 1, 3)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setVisible(False)
        self.status_label = QLabel("조회할 URL과 종목 수를 확인한 뒤 조회하세요.")

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(
            ["순번", "종목별", "현재가", "전일비", "등락률", "거래량", "시가총액(억)"]
        )
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        for column in (0, 2, 3, 4, 5, 6):
            self.table.horizontalHeader().setSectionResizeMode(
                column, QHeaderView.ResizeMode.ResizeToContents
            )

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(28, 24, 28, 28)
        layout.setSpacing(12)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addLayout(settings)
        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)
        layout.addWidget(self.table)

        self.fetch_button.clicked.connect(self.start_fetch)
        self.save_button.clicked.connect(self.save_results)
        central_widget.setStyleSheet(
            """
            QWidget { background: #f4f7f8; color: #1f2933; font-family: 'Malgun Gothic'; font-size: 13px; }
            QLabel#titleLabel { color: #0b5963; font-size: 25px; font-weight: 700; }
            QLabel#descriptionLabel { color: #62727b; margin-bottom: 6px; }
            QLineEdit, QSpinBox { background: white; border: 1px solid #c8d3d8; border-radius: 4px; padding: 7px; }
            QPushButton { background: #0b5963; color: white; border: 0; border-radius: 4px; padding: 8px 18px; font-weight: 600; }
            QPushButton:disabled { background: #aab8bd; }
            QTableWidget { background: white; border: 1px solid #d5dfe2; gridline-color: #e5ebed; }
            QHeaderView::section { background: #dcebed; color: #17434a; padding: 7px; font-weight: 600; border: 0; }
            """
        )

    def start_fetch(self):
        if self.thread is not None and self.thread.isRunning():
            return

        self.fetch_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.progress.setVisible(True)
        self.status_label.setText("네이버 금융에서 종목을 조회하는 중입니다...")
        self.table.setRowCount(0)

        self.thread = QThread(self)
        self.worker = ConstituentWorker(self.url_input.text().strip(), self.count_input.value())
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.fetch_finished)
        self.worker.failed.connect(self.fetch_failed)
        self.worker.finished.connect(self.thread.quit)
        self.worker.failed.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.thread_finished)
        self.thread.start()

    def fetch_finished(self, items):
        self.items = items
        self.table.setRowCount(len(items))
        columns = ["종목별", "현재가", "전일비", "등락률", "거래량", "시가총액(억)"]
        for row, item in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            for column, name in enumerate(columns, start=1):
                self.table.setItem(row, column, QTableWidgetItem(item.get(name, "")))
        self.status_label.setText(f"총 {len(items)}개 종목을 조회했습니다.")
        self.save_button.setEnabled(bool(items))

    def fetch_failed(self, message):
        self.items = []
        self.status_label.setText("조회에 실패했습니다.")
        QMessageBox.critical(self, "조회 오류", message)

    def thread_finished(self):
        self.progress.setVisible(False)
        self.fetch_button.setEnabled(True)
        self.thread = None
        self.worker = None

    def save_results(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "CSV 파일 저장", "kospi200_top_constituents.csv", "CSV 파일 (*.csv)"
        )
        if not filename:
            return
        try:
            save_csv(self.items, filename)
            self.status_label.setText(f"CSV 파일을 저장했습니다: {filename}")
        except OSError as error:
            QMessageBox.critical(self, "저장 오류", str(error))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConstituentWindow()
    window.show()
    sys.exit(app.exec())