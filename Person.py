# Person.py


class Person:
    # Person은 사람 한 명을 표현하는 기본 설계도입니다.
    # id와 name은 Person을 만든 모든 사람이 꼭 가지는 정보입니다.
    def __init__(self, id, name):
        # self는 지금 만들고 있는 사람 한 명을 가리킵니다.
        # id는 사람을 찾기 위한 번호이고, name은 사람의 이름입니다.
        self.id = id
        self.name = name

    def printInfo(self):
        # print는 화면에 글자를 보여주는 명령입니다.
        # 부모 클래스의 공통 정보인 id와 name을 출력합니다.
        print("id: {0}, name: {1}".format(self.id, self.name))


class Manager(Person):
    # Manager는 Person의 기능을 물려받은 관리자입니다.
    # 관리자에게만 필요한 title(직책) 정보를 하나 더 가집니다.
    def __init__(self, id, name, title):
        # super().__init__은 부모 Person의 준비 작업을 먼저 해 줍니다.
        # 그래서 id와 name을 여기서 다시 쓰지 않아도 됩니다.
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        # 먼저 부모의 id와 name을 출력합니다.
        super().printInfo()
        # 그 다음 관리자만 가진 title을 출력합니다.
        print("title: {0}".format(self.title))


class Employee(Person):
    # Employee는 Person의 기능을 물려받은 직원입니다.
    # 직원에게만 필요한 skill(기술) 정보를 하나 더 가집니다.
    def __init__(self, id, name, skill):
        # 부모에게 id와 name을 맡기고, 직원의 skill만 여기서 준비합니다.
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        # 먼저 부모의 id와 name을 출력합니다.
        super().printInfo()
        # 그 다음 직원만 가진 skill을 출력합니다.
        print("skill: {0}".format(self.skill))
