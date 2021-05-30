import threading
from time import sleep

def hello_1():
    while True:
        print("1")
        sleep(1)

def hello_2():
    while True:
        print("2")
        sleep(1)

def hello_1_thread():
    thread=threading.Thread(target=hello_1) #thread를 동작시킬 함수를 target 에 대입해줍니다
    thread.daemon=True #프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
    thread.start() #thread를 시작합니다

if __name__ == "__main__":
    hello_1_thread()
    hello_2()

# a = hello_1()
# print(a)
#
# b = hello_2()
# print(b)