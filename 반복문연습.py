#반복문연습

value = 5
while value > 0 :
    print(value)
    value -= 1

print("form in 반복문")
d = {"apple":100, "kiwi" : 200}
for item in d.items():
    print(item)

lst = [100,200,300]
for item in lst:
    print(item)

#수열함수
print(list(range(0,10)))
print(list(range(2000,2017)))
print(list(range(1,32)))

#for루프없음
for i in range(10) :
    print(i)

#list 컴프리레션
lst = list(range(0,10))
print([i**2 for i in lst if i>5])
tp = ("apple", "kiwi")
print([v.upper() for v in tp])

#필터링함수
lst = [10,25,30]
itemL = filter(None, lst)
for item in itemL :
    print(item)

def getBiggerThan20(x):
    return x>20

lst = [10,25,30]
itemL = filter(getBiggerThan20, lst)
for item in itemL :
    print(item)

print("람다함수활용")
lst = [10,25,30]
itemL = filter(lambda x:x>20, lst)
for item in itemL :
    print(item)

