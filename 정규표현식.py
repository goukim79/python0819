#정규표현식.py
import re

result = re.search("[0-9]*th", "  35th")
print(result)
print(result.group())

# result = re.match("[0-9]*th", "  35th")
# print(result)
# print(result.group())

#패턴 단어검색
result = re.search("apple", "I like apple")
print(result)
print(result.group())

result = re.search("\d{4}", "올해는 2026년입니다.")
print(result)
print(result.group())

result = re.search("\d{5}", "우리 동네는 51200입니다.")
print(result)
print(result.group())