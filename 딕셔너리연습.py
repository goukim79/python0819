#딕셔너리연습.py

#형식변환
a = list((1,2,3))
print(a)
a.append(10)
print(2)

#딕셔너리 연습
device = {"아이폰" : 5, "아이패드" : 10, "태블릿" : "15"}

device["맥북"] = 20
print(device)
print(len(device))
#삭제
del device["아이폰"]

for item in device.items():
    print(item)

for k,v in device.items():
    print(k,v)