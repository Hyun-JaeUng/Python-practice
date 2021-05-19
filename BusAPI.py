# 라이브러리
import requests, xmltodict, json
import pandas as pd
import time

# 공공 API 활용 KEY
key = 'kNSQvU5WeosgTXwCx1mTthdz93%2BlLXHKA7ZtzbuNArBuUVVP4akW5xsfp6R5JYuMH106DwcuJRTqXJHI4q%2BNjA%3D%3D'

# id, latitude, longitude, busNum
# ===================================================================================================

# 사용자의 위치를 받아서 tmX, tmY 변수에 지정 우선 임시 지정)
tmX = 126.9233021 # 경도(double) = longitude
tmY = 37.55639751 # 위도(double) = latitude
radius = 100 # 범위 (넓히면 여러 정류장 인식 됨.)

def position(x, y, r):
    url = f'http://ws.bus.go.kr/api/rest/stationinfo/getStationByPos?ServiceKey={key}&tmX={x}&tmY={y}&radius={r}' # 서울특별시_정류소정보조회 서비스 中 7_getStaionsByPosList
    content = requests.get(url).content
    dict = xmltodict.parse(content)

    # 첫번째 정류장이라 설정 ("음성으로 "현재 인식된 정류장은 A 정류장 입니다." 라고 전해주기)
    target_stId = int(dict['ServiceResult']['msgBody']['itemList'][0]['stationId'])
    target_stationName = str(dict['ServiceResult']['msgBody']['itemList'][0]['stationNm'])
    target_arsId = str(dict['ServiceResult']['msgBody']['itemList'][0]['arsId'])
    msgStation = "현재 인식된 정류장은 " + target_stationName + " 입니다." # 질문) 이렇게 메시지 형태로 구현해야 하나요?

    return (target_stId, target_stationName, target_arsId, msgStation)

station = position(tmX,tmY,radius) # 튜플

target_stId = station[0] # 밑 함수에서 쓰임.
target_stationName = station[1]
target_arsId = station[2]
target_msgStation = station[3]

print(target_stId) # 정류장 ID
print(target_stationName) # 정류장 이름
print(target_arsId) #정류장 고유번호
print(target_msgStation) # 사용자에게 주는 메시지

# ===================================================================================================
data1 = pd.read_csv('data/busnumber_to_busRouteid.csv')

# 음성인식을 통해 사용자가 5714번 탄다고 가정했음.
target_bus = '5714' # busNum, str 형태로 해야됨. -> 엑셀이 str 형태

def arriveMessage(target_bus):
    target_busRouteId = data1[data1['busNumber'] == target_bus].iloc[0]['busRouteId']
    url = f'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?ServiceKey={key}&busRouteId={target_busRouteId}' # 서울특별시_노선정보조회 서비스 中 1_getStaionsByRouteList
    content = requests.get(url).content
    dict = xmltodict.parse(content)

    # target_arsId = arsId 넘버가 일치하는 버스의 seq(=ord) 구하기
    alist = []
    for i in range(0, len(dict['ServiceResult']['msgBody']['itemList'])):
        alist.append(dict['ServiceResult']['msgBody']['itemList'][i]['arsId'])

    # 인덱스 값이 곧 seq 값
    target_ord = alist.index(target_arsId) + 1

    # 서울특별시_버스도착정보조회 서비스 中 2_getArrInfoByRouteList
    url = f'http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRoute?ServiceKey=' \
          f'{key}&stId={target_stId}&busRouteId={target_busRouteId}&ord={target_ord}'
    content = requests.get(url).content
    dict = xmltodict.parse(content)

    arrival = dict['ServiceResult']['msgBody']['itemList']['arrmsg1']
    arrival2 = dict['ServiceResult']['msgBody']['itemList']['arrmsg2']
    busplainnum = dict['ServiceResult']['msgBody']['itemList']['plainNo1']
    nextstation = dict['ServiceResult']['msgBody']['itemList']['stationNm1']

    return (arrival, arrival2, busplainnum, nextstation)

result_arriveMsg = arriveMessage(target_bus)
arrival = result_arriveMsg[0]
arrival2 = result_arriveMsg[1]
busplainnum = result_arriveMsg[2]
nextstation = result_arriveMsg[3]

print(arrival) # 첫 번째 버스 도착 예정 시간
print(arrival2) # 두 번째 버스 도착 예정 시간
print(busplainnum) # 버스 차량 번호
print(nextstation) # 다음 정류장

# 분이랑 초가 없는 경우도 있음 -> 고려해서 수정해야 함!
indexMinute = arrival.find('분')
indexSecond = arrival.find('초')
freeTime = 60 # 스마트 글래스 켜지기 시작하는 시간 (협의하여 결정, 실제 코드가 돌아가고 사용자에게 전달될때까지 시스템에서 소요되는 시간이 어느정도인지 고려해야 할듯)
k = int(arrival[0:indexMinute]) * 60 + int(arrival[indexMinute+1:indexSecond]) - freeTime

def NoticeOneMinute(k):
    time.sleep(k)
    finalResult = arriveMessage(target_bus)
    finalArrival = finalResult[0]
    print(finalArrival)

    return finalArrival







# ===================================================================================================