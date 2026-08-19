# 문자열연습.py

strA ="파이썬은 강력해"
strB = "python"
strC = """ 이문자열은
다중 라인으로
저장됩니다.
"""
print(strA)
print(len(strB))
print(strC)

#슬라이싱
print(strB[0:3])
print(strB[:3])
print(strB[-3:])

#list
colors = ["red", "blue", "green"]
print(len(colors))
print(type(colors))
colors.append("white")
colors.insert(1, "pink")
print(colors)
colors.remove("blue")
print(colors)

#set
a = {1,2,3,3}
b = {3,4,4,5}
print(a)
print(type(a))
print(a.union(b))
print(a.intersection(b))
print(a.difference(b))

#tuble
tp = (100,200,300)
print(len(tp))

#함수
def time(a,b) :
    return a+b, a*b

result = time(5,6)
print(result)

print("id : %s name : %s" % ("kim", "김유신"))

args = (3,4)
print(time(*args))