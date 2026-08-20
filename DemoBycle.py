import sqlite3
import sys
from contextlib import contextmanager
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ProductDatabase:
    def __init__(self, database_path="MyProduct.db"):
        self.database_path = Path(database_path)
        self.create_table()

    @contextmanager
    def connect(self):
        connection = sqlite3.connect(self.database_path)
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def create_table(self):
        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS MyProduct (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price INTEGER NOT NULL
                )
                """
            )

    def add_product(self, name, price):
        with self.connect() as connection:
            connection.execute(
                "INSERT INTO MyProduct (name, price) VALUES (?, ?)",
                (name, price),
            )

    def update_product(self, product_id, name, price):
        with self.connect() as connection:
            cursor = connection.execute(
                "UPDATE MyProduct SET name = ?, price = ? WHERE id = ?",
                (name, price, product_id),
            )
            return cursor.rowcount

    def delete_product(self, product_id):
        with self.connect() as connection:
            cursor = connection.execute(
                "DELETE FROM MyProduct WHERE id = ?", (product_id,)
            )
            return cursor.rowcount

    def find_products(self, keyword=""):
        with self.connect() as connection:
            if keyword:
                cursor = connection.execute(
                    """
                    SELECT id, name, price FROM MyProduct
                    WHERE name LIKE ? OR CAST(id AS TEXT) = ?
                    ORDER BY id
                    """,
                    (f"%{keyword}%", keyword),
                )
            else:
                cursor = connection.execute(
                    "SELECT id, name, price FROM MyProduct ORDER BY id"
                )
            return cursor.fetchall()


class BicycleProductWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.database = ProductDatabase()
        self.setWindowTitle("자전거용품 관리")
        self.resize(650, 500)
        self.build_ui()
        self.load_products()

    def build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setObjectName("centralWidget")

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("수정/삭제할 ID")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("예: 자전거 헬멧")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("예: 59000")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("제품명 또는 ID 검색")

        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(18)
        form_layout.setVerticalSpacing(12)
        form_layout.addRow(QLabel("ID"), self.id_input)
        form_layout.addRow(QLabel("제품명"), self.name_input)
        form_layout.addRow(QLabel("가격"), self.price_input)

        button_layout = QHBoxLayout()
        add_button = QPushButton("입력")
        update_button = QPushButton("수정")
        delete_button = QPushButton("삭제")
        search_button = QPushButton("검색")
        clear_button = QPushButton("전체보기")
        add_button.setObjectName("addButton")
        update_button.setObjectName("updateButton")
        delete_button.setObjectName("deleteButton")
        search_button.setObjectName("searchButton")
        clear_button.setObjectName("clearButton")
        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(search_button)
        button_layout.addWidget(clear_button)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "제품명", "가격"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.table.cellDoubleClicked.connect(self.select_product)

        search_button.clicked.connect(self.search_products)
        clear_button.clicked.connect(self.load_products)
        add_button.clicked.connect(self.add_product)
        update_button.clicked.connect(self.update_product)
        delete_button.clicked.connect(self.delete_product)
        self.search_input.returnPressed.connect(self.search_products)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(34, 28, 34, 34)
        layout.setSpacing(16)

        title = QLabel("BIKE GEAR  /  자전거용품 관리")
        title.setObjectName("titleLabel")
        subtitle = QLabel("라이딩을 위한 장비를 한 곳에서 관리하세요")
        subtitle.setObjectName("subtitleLabel")
        input_title = QLabel("제품 정보")
        input_title.setObjectName("sectionLabel")
        search_title = QLabel("제품 찾기")
        search_title.setObjectName("sectionLabel")
        list_title = QLabel("등록된 용품")
        list_title.setObjectName("sectionLabel")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(input_title)
        layout.addLayout(form_layout)
        layout.addWidget(search_title)
        layout.addWidget(self.search_input)
        layout.addLayout(button_layout)
        layout.addWidget(list_title)
        layout.addWidget(self.table)

        central_widget.setStyleSheet(
            """
            QWidget#centralWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #e9fbf7, stop: 0.55 #f7fbff, stop: 1 #fff2ec);
                color: #17324d;
                font-family: 'Malgun Gothic';
                font-size: 13px;
            }
            QLabel#titleLabel {
                color: #0c6570;
                font-size: 25px;
                font-weight: 800;
                padding-bottom: 0;
            }
            QLabel#subtitleLabel {
                color: #658093;
                font-size: 13px;
                padding-bottom: 8px;
            }
            QLabel#sectionLabel {
                color: #e26d52;
                font-size: 14px;
                font-weight: 700;
                padding-top: 5px;
            }
            QLineEdit {
                background: rgba(255, 255, 255, 220);
                border: 1px solid #b8d8dc;
                border-radius: 8px;
                padding: 10px 12px;
                color: #17324d;
                selection-background-color: #16a6a0;
            }
            QLineEdit:focus {
                border: 2px solid #16a6a0;
                background: #ffffff;
            }
            QPushButton {
                background: #ffffff;
                border: 1px solid #b8d8dc;
                border-radius: 8px;
                color: #245268;
                font-weight: 700;
                min-height: 38px;
                padding: 0 18px;
            }
            QPushButton:hover {
                background: #dff7f2;
                border-color: #16a6a0;
            }
            QPushButton:pressed {
                background: #b9ebe3;
            }
            QPushButton#addButton {
                background: #16a6a0;
                border-color: #16a6a0;
                color: white;
            }
            QPushButton#addButton:hover, QPushButton#searchButton:hover {
                background: #0c817f;
                color: white;
            }
            QPushButton#deleteButton {
                background: #e26d52;
                border-color: #e26d52;
                color: white;
            }
            QPushButton#deleteButton:hover {
                background: #bd503d;
            }
            QTableWidget {
                background: rgba(255, 255, 255, 235);
                alternate-background-color: #eef9f7;
                border: 1px solid #b8d8dc;
                border-radius: 10px;
                gridline-color: #d9ecec;
                selection-background-color: #bcece5;
                selection-color: #17324d;
                outline: none;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background: #0c6570;
                color: white;
                border: none;
                font-weight: 700;
                padding: 10px;
            }
            """
        )

    def product_values(self, require_id=False):
        product_id = self.id_input.text().strip()
        name = self.name_input.text().strip()
        price_text = self.price_input.text().strip().replace(",", "")

        if require_id and not product_id.isdigit():
            raise ValueError("ID는 숫자로 입력하세요.")
        if not name:
            raise ValueError("제품명을 입력하세요.")
        if not price_text.isdigit():
            raise ValueError("가격은 0 이상의 숫자로 입력하세요.")
        return int(product_id) if product_id else None, name, int(price_text)

    def add_product(self):
        try:
            _, name, price = self.product_values()
            self.database.add_product(name, price)
            self.load_products()
            self.clear_inputs()
        except ValueError as error:
            self.show_error(str(error))

    def update_product(self):
        try:
            product_id, name, price = self.product_values(require_id=True)
            if self.database.update_product(product_id, name, price) == 0:
                raise ValueError("해당 ID의 제품을 찾을 수 없습니다.")
            self.load_products()
            self.clear_inputs()
        except ValueError as error:
            self.show_error(str(error))

    def delete_product(self):
        product_id = self.id_input.text().strip()
        if not product_id.isdigit():
            self.show_error("삭제할 제품의 ID를 입력하세요.")
            return
        if self.database.delete_product(int(product_id)) == 0:
            self.show_error("해당 ID의 제품을 찾을 수 없습니다.")
            return
        self.load_products()
        self.clear_inputs()

    def search_products(self):
        self.load_products(self.search_input.text().strip())

    def load_products(self, keyword=""):
        products = self.database.find_products(keyword)
        self.table.setRowCount(len(products))
        for row, (product_id, name, price) in enumerate(products):
            id_item = QTableWidgetItem(str(product_id))
            price_item = QTableWidgetItem(f"{price:,}")
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, price_item)

    def select_product(self, row, _column):
        self.id_input.setText(self.table.item(row, 0).text())
        self.name_input.setText(self.table.item(row, 1).text())
        self.price_input.setText(self.table.item(row, 2).text().replace(",", ""))

    def clear_inputs(self):
        self.id_input.clear()
        self.name_input.clear()
        self.price_input.clear()

    def show_error(self, message):
        QMessageBox.warning(self, "입력 확인", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BicycleProductWindow()
    window.show()
    sys.exit(app.exec())