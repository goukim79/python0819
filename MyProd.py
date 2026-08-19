import sqlite3
from contextlib import contextmanager


class ProductDB:
    """전자제품 데이터를 SQLite로 관리하는 클래스."""

    def __init__(self, db_name="MyProduct.db"):
        self.db_name = db_name
        self.create_table()

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def create_table(self):
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS Products (
                    productID INTEGER PRIMARY KEY,
                    productName TEXT NOT NULL,
                    productPrice INTEGER NOT NULL
                )
                """
            )

    def insert_product(self, product_id, product_name, product_price):
        """제품 1건을 입력하고 생성된 productID를 반환한다."""
        with self.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO Products (productID, productName, productPrice)
                VALUES (?, ?, ?)
                """,
                (product_id, product_name, product_price),
            )
            return cursor.lastrowid

    def insert_products(self, products):
        """제품 여러 건을 일괄 입력한다."""
        with self.connect() as conn:
            conn.executemany(
                """
                INSERT INTO Products (productID, productName, productPrice)
                VALUES (?, ?, ?)
                """,
                products,
            )

    def update_product(self, product_id, product_name, product_price):
        """productID에 해당하는 제품을 수정하고 수정된 행 수를 반환한다."""
        with self.connect() as conn:
            cursor = conn.execute(
                """
                UPDATE Products
                SET productName = ?, productPrice = ?
                WHERE productID = ?
                """,
                (product_name, product_price, product_id),
            )
            return cursor.rowcount

    def delete_product(self, product_id):
        """productID에 해당하는 제품을 삭제하고 삭제된 행 수를 반환한다."""
        with self.connect() as conn:
            cursor = conn.execute(
                "DELETE FROM Products WHERE productID = ?",
                (product_id,),
            )
            return cursor.rowcount

    def select_products(self, product_id=None):
        """제품 전체 또는 productID에 해당하는 제품을 조회한다."""
        with self.connect() as conn:
            if product_id is None:
                cursor = conn.execute(
                    """
                    SELECT productID, productName, productPrice
                    FROM Products
                    ORDER BY productID
                    """
                )
            else:
                cursor = conn.execute(
                    """
                    SELECT productID, productName, productPrice
                    FROM Products
                    WHERE productID = ?
                    """,
                    (product_id,),
                )
            return cursor.fetchall()

    def seed_sample_data(self, count=100_000):
        """기존 제품을 비우고 count건의 샘플 데이터를 입력한다."""
        products = [
            (product_id, f"전자제품_{product_id:06d}", 10_000 + (product_id % 100) * 1_000)
            for product_id in range(1, count + 1)
        ]
        with self.connect() as conn:
            conn.execute("DELETE FROM Products")
            conn.executemany(
                """
                INSERT INTO Products (productID, productName, productPrice)
                VALUES (?, ?, ?)
                """,
                products,
            )


if __name__ == "__main__":
    product_db = ProductDB()
    product_db.seed_sample_data()
    print(f"Products 테이블에 {len(product_db.select_products())}건의 샘플 데이터를 저장했습니다.")