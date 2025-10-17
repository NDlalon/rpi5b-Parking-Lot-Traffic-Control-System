#!/usr/bin/python3

import RPi.GPIO as GPIO
import threading
from threading import Timer
import time

#進入流程物件
class EntryFSM:
    def __init__(self):
        self.isRunning=False
        self.WarningLightTimer=Timer(0,self.reset)
        self.WarningLightTimer.cancel()

    #進入流程處理
    def process(self,pin):
        self.isRunning=True
        global FenceToken

        if(pin==remote):
            self.WarningLightTimer.cancel()
            self.WarningLightTimer=Timer(EntryTimer,self.FenceClose)
            self.WarningLightTimer.start()

            with FenceTokenLock:
                FenceToken='EntryFSM'
                fence_control('up')

            flash_control(Entry_WarningLight,True)
            traffic_control('B','Red')
            
        self.isRunning=False

    #關閉柵欄機
    def FenceClose(self):
        global FenceToken
        
        if(FenceToken=='EntryFSM'):
            with FenceTokenLock:
                FenceToken='EntryFSM_now'

        start_time=time.time()
        while(time.time()-start_time<FenceTimer):
            if(FenceToken=='EntryFSM'):
                return 
            elif(GPIO.input(pressureSensor)==GPIO.HIGH):
                fence_control('up')
                start_time=time.time()
            elif(GPIO.input(pressureSensor)==GPIO.LOW and FenceToken=='EntryFSM_now'):
                fence_control('down')
            time.sleep(0.01)

        if(FenceToken=='EntryFSM_now'):  
            fence_control('idle')
        self.reset()

    #重置狀態
    def reset(self):
        flash_control(Entry_WarningLight,False)
        traffic_control('B','Green')


#退出流程物件
class ExitFSM:
    def __init__(self):
        self.isRunning=False
        self.WarningLightTimer=Timer(0,self.reset)
        self.WarningLightTimer.cancel()
    
    #退出流程處理
    def process(self,pin):
        self.isRunning=True
        global FenceToken

        if(pin==coil_sensor):
            self.WarningLightTimer.cancel()
            self.WarningLightTimer=Timer(ExitTimer,self.FenceClose)
            self.WarningLightTimer.start()

            with FenceTokenLock:
                FenceToken='ExitFSM'
                fence_control('up')
                
            flash_control(Exit_WarningLight,True)
            traffic_control('A','Red')                

        self.isRunning=False

    #關閉柵欄機
    def FenceClose(self):
        global FenceToken
        
        if(FenceToken=='ExitFSM'):
            with FenceTokenLock:
                FenceToken='ExitFSM_now'

        start_time=time.time()
        while(time.time()-start_time<FenceTimer):
            if(FenceToken=='ExitFSM'):
                return
            elif(GPIO.input(pressureSensor)==GPIO.HIGH):
                fence_control('up')
                start_time=time.time()
            elif(GPIO.input(pressureSensor)==GPIO.LOW and FenceToken=='ExitFSM_now'):
                fence_control('down')
            time.sleep(0.01)

        if(FenceToken=='ExitFSM_now'):
            fence_control('idle')
        self.reset()

    #重置狀態
    def reset(self,part='ALL'):
        if(part=='ALL'):
            flash_control(Exit_WarningLight,False)
            traffic_control('A','Green')
        elif(part=='coilA'):
            self.coilAState='idle'
        elif(part=='coilB'):
            self.coilBState='idle'
        elif(part=='infrared'):
            self.infraredState='idle'

#腳位定義
coil_sensor=7
remote=22

pressureSensor=32

TimerMSB=19
TimerLSB=21

Entry_WarningLight=35 
Exit_WarningLight=38
A_trafficLight=33
B_trafficLight=36

FenceUP=29
FenceDOWN=31
FenceToken=''
FenceTokenLock=threading.Lock()

#計時器秒數設定
EntryTimer=0 #由程式啟動時設定
ExitTimer=0 #由程式啟動時設定
stateTimer=5
FenceTimer=5

#輸出方式
#此處正緣觸發與負緣觸發所指為RPi Relay Board (B)的relay觸發方式
edge=False   #(True為正緣觸發 False為負緣觸發)
gpioPotential={
    True:GPIO.HIGH,
    False:GPIO.LOW
}

#進出流程
Entry=EntryFSM()
Exit=ExitFSM()

#初始腳位設定
def setup():
    GPIO.setmode(GPIO.BOARD)
    
    #設定sensor與下拉電阻
    GPIO.setup(coil_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(remote, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(pressureSensor,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    #計時器秒數設定腳位與下拉電阻
    GPIO.setup(TimerMSB,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(TimerLSB,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    #設定事件觸發
    GPIO.add_event_detect(coil_sensor,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(remote,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    #警示燈設定
    GPIO.setup(Entry_WarningLight,GPIO.OUT)
    GPIO.setup(Exit_WarningLight,GPIO.OUT)
    GPIO.output(Entry_WarningLight,gpioPotential[not edge])
    GPIO.output(Exit_WarningLight,gpioPotential[not edge])
    #紅綠燈設定
    GPIO.setup(A_trafficLight,GPIO.OUT)
    GPIO.setup(B_trafficLight,GPIO.OUT)
    GPIO.output(A_trafficLight,gpioPotential[not edge])
    GPIO.output(B_trafficLight,gpioPotential[not edge])
    #柵欄機設定
    GPIO.setup(FenceUP,GPIO.OUT)
    GPIO.setup(FenceDOWN,GPIO.OUT)
    GPIO.output(FenceUP,GPIO.LOW) #柵欄機上須保持正緣觸發
    GPIO.output(FenceDOWN,gpioPotential[not edge])
    #計時器秒數設定 
    timerSetting()
    
#按鈕中斷執行程序
def SensorCallBack(pin):
    
    #建立進入流程執行緒
    if(pin==remote):
        if(not(Entry.isRunning)):
            threadEntry=threading.Thread(target=Entry.process, args=(pin,))
            threadEntry.start()
        
    #建立退出流程執行緒
    else:
        if(not(Exit.isRunning)):
            threadExit=threading.Thread(target=Exit.process, args=(pin,))
            threadExit.start()
    
#=====警示燈控制=====
def flash_control(Light,activ=False):
    if(activ):
        GPIO.output(Light,gpioPotential[edge])
    else:
        GPIO.output(Light,gpioPotential[not edge])

#=====紅綠燈控制=====
def traffic_control(traffic,light):
    trafficLight=0

    if(traffic=='A'):
        trafficLight=A_trafficLight
    elif(traffic=='B'):
        trafficLight=B_trafficLight

    if(light=='Red'):
        GPIO.output(trafficLight,gpioPotential[edge])
    elif(light=='Green'):
        GPIO.output(trafficLight,gpioPotential[not edge])

#=====柵欄機控制=====
#柵欄機上保持正緣觸發，確保樹莓派異常時能正常開啟
def fence_control(state=''):
    if(state=='up'):
        GPIO.output(FenceDOWN,gpioPotential[not edge])
        GPIO.output(FenceUP,GPIO.HIGH)
    elif(state=='down'):
        GPIO.output(FenceUP,GPIO.LOW)
        GPIO.output(FenceDOWN,gpioPotential[edge])
    elif(state=='idle'):
        GPIO.output(FenceUP,GPIO.LOW)
        GPIO.output(FenceDOWN,gpioPotential[not edge])

#柵欄機時間設定
def timerSetting():
    global ExitTimer
    global EntryTimer
    second=10

    if(GPIO.input(TimerMSB)==GPIO.HIGH):
        second+=20
    if(GPIO.input(TimerLSB)==GPIO.HIGH):
        second+=10

    EntryTimer=second
    ExitTimer=second

if __name__ == '__main__':
    setup()
    
    while True:
        time.sleep(1)