import unittest
from io import StringIO
from contextlib import redirect_stdout

from Person import Employee, Manager, Person


class PersonTest(unittest.TestCase):
    # 테스트는 프로그램이 약속대로 일하는지 확인하는 작은 문제입니다.
    # 아래에는 Person, Manager, Employee를 확인하는 문제 10개가 있습니다.

    def test_01_person_has_id(self):
        person = Person(1, "민수")
        self.assertEqual(person.id, 1)

    def test_02_person_has_name(self):
        person = Person(1, "민수")
        self.assertEqual(person.name, "민수")

    def test_03_person_print_info(self):
        person = Person(1, "민수")
        output = StringIO()
        with redirect_stdout(output):
            person.printInfo()
        self.assertEqual(output.getvalue(), "id: 1, name: 민수\n")

    def test_04_manager_has_person_values(self):
        manager = Manager(2, "지영", "팀장")
        self.assertEqual((manager.id, manager.name), (2, "지영"))

    def test_05_manager_has_title(self):
        manager = Manager(2, "지영", "팀장")
        self.assertEqual(manager.title, "팀장")

    def test_06_manager_is_person(self):
        manager = Manager(2, "지영", "팀장")
        self.assertIsInstance(manager, Person)

    def test_07_manager_print_info(self):
        manager = Manager(2, "지영", "팀장")
        output = StringIO()
        with redirect_stdout(output):
            manager.printInfo()
        self.assertEqual(output.getvalue(), "id: 2, name: 지영\ntitle: 팀장\n")

    def test_08_employee_has_skill(self):
        employee = Employee(3, "철수", "파이썬")
        self.assertEqual(employee.skill, "파이썬")

    def test_09_employee_is_person(self):
        employee = Employee(3, "철수", "파이썬")
        self.assertIsInstance(employee, Person)

    def test_10_employee_print_info(self):
        employee = Employee(3, "철수", "파이썬")
        output = StringIO()
        with redirect_stdout(output):
            employee.printInfo()
        self.assertEqual(output.getvalue(), "id: 3, name: 철수\nskill: 파이썬\n")


if __name__ == "__main__":
    unittest.main()