#내부라이브러리 연습
import random

print(random.random())
print(random.random())
print(random.uniform(2.0, 5.0))
print(random.choice(['apple', 'banana', 'cherry']))
print([random.randrange(20) for i in range(5)])
print([random.randrange(20) for i in range(5)])
print([random.sample(range(20), 10)])
print([random.sample(range(20), 10)])
#로또번호 만들기
lotto = random.sample(range(1, 46), 6)
print("이번주 로또번호는", sorted(lotto))

#파일명 다루기
from os.path import *
#raw string notation
filename = r"C:\python313\python.exe"

print(basename(filename))
print(dirname(filename))
print(split(filename))
print(abspath(filename))

if exists(filename):
    print("파일이 존재합니다.")
else:
    print("파일이 존재하지 않습니다.")

#운영체제 다루기
import os
print(os.name) 
print(os.environ) 
print(os.getcwd())
#특정 폴더의 파일 리스트
import glob
print(glob.glob("C:\\python313\\*.*"))

