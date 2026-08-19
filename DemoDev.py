#DemoDev.py
#Developers라는 클래스를 정의하는데
#멤버변수로 id, name, skill이 있고 printInfo라는 메서드가 필요
class Developers:
    def __init__(self, id, name, skill):
        self.id = id
        self.name = name
        self.skill = skill

    def printInfo(self):
        print("id: {0}, name: {1}, skill: {2}".format(self.id, self.name, self.skill))      

#인스턴스를 생성
dev1 = Developers(100, "전우치", "Python")
dev2 = Developers(200, "이순신", "Java") 
dev1.printInfo()
dev2.printInfo()