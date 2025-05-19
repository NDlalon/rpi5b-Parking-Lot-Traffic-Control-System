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
        self.coilAState='idle'
        self.coilBState='idle'
        self.infraredState='idle'
        self.coilATimer=Timer(0,self.reset)
        self.coilATimer.cancel()
        self.coilBTimer=Timer(0,self.reset)
        self.coilBTimer.cancel()
        self.infraredTimer=Timer(0,self.reset)
        self.infraredTimer.cancel()

        self.WarningLightTimer=Timer(0,self.reset)
        self.WarningLightTimer.cancel()
    
    #退出流程處理
    def process(self,pin):
        self.isRunning=True
        global FenceToken

        #coilA1,coilA2 senser
        if(pin==coil_sensorA1):
            if(self.coilAState=='idle'):
                self.coilAState='coilA1_Entry'
                self.coilATimer.cancel()
                self.coilATimer=Timer(stateTimer,self.reset,args=('coilA',))
                self.coilATimer.start()
            elif(self.coilAState=='coilA2_Entry'):
                self.coilAState='idle'
                self.coilATimer.cancel()
        elif(pin==coil_sensorA2):
            if(self.coilAState=='idle'):
                self.coilAState='coilA2_Entry'
                self.coilATimer.cancel()
                self.coilATimer=Timer(stateTimer,self.reset,args=('coilA',))
                self.coilATimer.start()
            elif(self.coilAState=='coilA1_Entry'):
                self.coilATimer.cancel()
                self.WarningLightTimer.cancel()
                self.WarningLightTimer=Timer(ExitTimer,self.FenceClose)
                self.WarningLightTimer.start()
                self.coilAState='idle'
                with FenceTokenLock:
                    FenceToken='ExitFSM'
                    fence_control('up')
                flash_control(Exit_WarningLight,True)
                traffic_control('A','Red')
                

        #coilB1,coilB2 senser
        elif(pin==coil_sensorB1):
            if(self.coilBState=='idle'):
                self.coilBState='coilB1_Entry'
                self.coilBTimer.cancel()
                self.coilBTimer=Timer(stateTimer,self.reset,args=('coilB',))
                self.coilBTimer.start()
            elif(self.coilBState=='coilB2_Entry'):
                self.coilBState='idle'
                self.coilBTimer.cancel()
        elif(pin==coil_sensorB2):
            if(self.coilBState=='idle'):
                self.coilBState='coilB2_Entry'
                self.coilBTimer.cancel()
                self.coilBTimer=Timer(stateTimer,self.reset,args=('coilB',))
                self.coilBTimer.start()
            elif(self.coilBState=='coilB1_Entry'):
                self.coilBTimer.cancel()
                self.WarningLightTimer.cancel()
                self.WarningLightTimer=Timer(ExitTimer,self.FenceClose)
                self.WarningLightTimer.start()
                self.coilBState='idle'
                with FenceTokenLock:
                    FenceToken='ExitFSM'
                    fence_control('up')
                flash_control(Exit_WarningLight,True)
                traffic_control('A','Red')

        #infrared senser
        elif(pin==infrared_sensorA1):
            if(self.infraredState=='idle'):
                self.infraredState='infraredA1_Entry'
                self.infraredTimer.cancel()
                self.infraredTimer=Timer(stateTimer,self.reset,args=('infrared',))
                self.infraredTimer.start()
            elif(self.infraredState=='infraredA2_Entry'):
                self.infraredState='idle'
                self.infraredTimer.cancel()
        elif(pin==infrared_sensorA2):
            if(self.infraredState=='idle'):
                self.infraredState='infraredA2_Entry'
                self.infraredTimer.cancel()
                self.infraredTimer=Timer(stateTimer,self.reset,args=('infrared',))
                self.infraredTimer.start()
            elif(self.infraredState=='infraredA1_Entry'):
                self.infraredTimer.cancel()
                self.WarningLightTimer.cancel()
                self.WarningLightTimer=Timer(ExitTimer,self.FenceClose)
                self.WarningLightTimer.start()
                self.infraredState='idle'
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
coil_sensorA1=7
coil_sensorA2=11
coil_sensorB1=13
coil_sensorB2=15
infrared_sensorA1=16
infrared_sensorA2=18
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

#進出流程
Entry=EntryFSM()
Exit=ExitFSM()

#初始腳位設定
def setup():
    GPIO.setmode(GPIO.BOARD)
    
    #設定sensor與下拉電阻
    GPIO.setup(coil_sensorA1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(coil_sensorA2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(coil_sensorB1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(coil_sensorB2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(infrared_sensorA1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(infrared_sensorA2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(remote, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(pressureSensor,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    #計時器秒數設定腳位與下拉電阻
    GPIO.setup(TimerMSB,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(TimerLSB,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    #設定事件觸發
    GPIO.add_event_detect(coil_sensorA1,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorA2,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorB1,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorB2,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(infrared_sensorA1,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(infrared_sensorA2,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(remote,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    #警示燈設定
    GPIO.setup(Entry_WarningLight,GPIO.OUT)
    GPIO.setup(Exit_WarningLight,GPIO.OUT)
    GPIO.output(Entry_WarningLight,GPIO.LOW)
    GPIO.output(Exit_WarningLight,GPIO.LOW)
    #紅綠燈設定
    GPIO.setup(A_trafficLight,GPIO.OUT)
    GPIO.setup(B_trafficLight,GPIO.OUT)
    GPIO.output(A_trafficLight,GPIO.LOW)
    GPIO.output(B_trafficLight,GPIO.LOW)
    #柵欄機設定
    GPIO.setup(FenceUP,GPIO.OUT)
    GPIO.setup(FenceDOWN,GPIO.OUT)
    GPIO.output(FenceUP,GPIO.LOW)
    GPIO.output(FenceDOWN,GPIO.LOW)
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
        GPIO.output(Light,GPIO.HIGH)
    else:
        GPIO.output(Light,GPIO.LOW)

#=====紅綠燈控制=====
def traffic_control(traffic,light):
    trafficLight=0

    if(traffic=='A'):
        trafficLight=A_trafficLight
    elif(traffic=='B'):
        trafficLight=B_trafficLight

    if(light=='Red'):
        GPIO.output(trafficLight,GPIO.HIGH)
    elif(light=='Green'):
        GPIO.output(trafficLight,GPIO.LOW)

#=====柵欄機控制=====
def fence_control(state=''):
    if(state=='up'):
        GPIO.output(FenceDOWN,GPIO.LOW)
        GPIO.output(FenceUP,GPIO.HIGH)
    elif(state=='down'):
        GPIO.output(FenceUP,GPIO.LOW)
        GPIO.output(FenceDOWN,GPIO.HIGH)
    elif(state=='idle'):
        GPIO.output(FenceUP,GPIO.LOW)
        GPIO.output(FenceDOWN,GPIO.LOW)

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
