import time
arrival = '3분55초후[1번째 전]'
indexMinute = arrival.find('분')
indexSecond = arrival.find('초')

print(indexMinute)
print(indexSecond)
freeTime = 60 # 스마트 글래스 켜지기 시작하는 시간 (협의하여 결정, 실제 코드가 돌아가고 사용자에게 전달될때까지 시스템에서 소요되는 시간이 어느정도인지 고려해야 할듯)
k = int(arrival[0:indexMinute]) * 60 + int(arrival[indexMinute+1:indexSecond]) - freeTime
print(k)


a = time.time()
print(a)