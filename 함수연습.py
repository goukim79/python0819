# 함수연습.py

#1)함수를 정의
def times(a=10, b=20):
    return a,b

#2) 호출
print(times())
print(times(5))
print(times(5,6))

#키워드 인자방식
def connectURI(server, port) :
    url = "https://" + server + ":" + port
    return url

#호출
print(connectURI("naver.com", "80"))
print(connectURI(port="80", server="test.com"))

#가변인자를 받는 함수
def union(*ar) : 
    result =[]
    for item in ar :
        for x in item :
            if x not in result:
                result.append(x)
    return result

#호출
print(union("HAM", "EGG"))
print(union("HAM", "EGG", "SPAM"))

#전역변수 지역변수 차이
x = 5
def func(a):
    return a+x

# 호출
print(func(1))

def func2(a) :
    x = 10
    return a + x

# 호출
print(func2(1))

#람다함수
g = lambda x,y:x*y
print(g(3,4))
print((lambda x:x*x)(3))

print(dir())
print(globals())
