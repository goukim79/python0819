# db2.py
import sqlite3

#연결객체 파일에 저장
conn = sqlite3.connect(r"c:\work\phonebook1.db") #파일에 DB를 생성
cursor = conn.cursor()
#테이블 생성
cursor.execute("CREATE TABLE PhoneBook (name text, phoneNum text)")
#입력 파라메터 처리
name = "이순신"
phoneNum = "010-9876-5432"
cursor.execute("INSERT INTO PhoneBook VALUES (?, ?)", (name, phoneNum))
#1건 입력
cursor.execute("INSERT INTO PhoneBook VALUES ('전우치', '010-1234-5678')")
#여러건 입력
data = [("홍길동", "010-1111-2222"), ("강감찬", "010-3333-4444"), ("을지문덕", "010-5555-6666")]
cursor.executemany("INSERT INTO PhoneBook VALUES (?, ?)", data)
#조회
cursor.execute("SELECT * FROM PhoneBook")
for row in cursor:
    print(row)
conn.commit() #변경내용을 DB에 반영
print(cursor.fetchall())
