#클래스 정의.py

#1. 클래스정의
class Person:
    #초기화
    def __init__(self):
        self.name = "default name"
    def printInfo(self):
        print("My name is {0}".format(self.name))

p1 = Person()
p1.name = "홍길동"
p2 = Person()
p1.printInfo()