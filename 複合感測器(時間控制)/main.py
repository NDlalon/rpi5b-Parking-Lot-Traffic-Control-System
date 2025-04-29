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

        if(pin==remote):
            flash_control(Entry1_WarningLight,True)
            flash_control(Entry2_WarningLight,True)
            flash_control(Entry3_WarningLight,True)
            flash_control(Entry4_WarningLight,True)
            flash_control(Entry5_WarningLight,True)
            traffic_control('B','Red')
            
            self.WarningLightTimer.cancel()
            self.WarningLightTimer=Timer(EntryTimer,self.reset)
            self.WarningLightTimer.start()

        self.isRunning=False
    #重置狀態
    def reset(self):
        flash_control(Entry1_WarningLight,False)
        flash_control(Entry2_WarningLight,False)
        flash_control(Entry3_WarningLight,False)
        flash_control(Entry4_WarningLight,False)
        flash_control(Entry5_WarningLight,False)
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
            print('coilAState:',self.coilAState)
        elif(pin==coil_sensorA2):
            if(self.coilAState=='idle'):
                self.coilAState='coilA2_Entry'
                self.coilATimer.cancel()
                self.coilATimer=Timer(stateTimer,self.reset,args=('coilA',))
                self.coilATimer.start()
            elif(self.coilAState=='coilA1_Entry'):
                self.coilAState='idle'
                flash_control(Exit1_WarningLight,True)
                flash_control(Exit2_WarningLight,True)
                traffic_control('A','Red')
                self.coilATimer.cancel()
                self.WarningLightTimer.cancel()
                self.WarningLightTimer=Timer(ExitTimer,self.reset)
                self.WarningLightTimer.start()
            print('coilAState:',self.coilAState)
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
            print('coilBState:',self.coilBState)
        elif(pin==coil_sensorB2):
            if(self.coilBState=='idle'):
                self.coilBState='coilB2_Entry'
                self.coilBTimer.cancel()
                self.coilBTimer=Timer(stateTimer,self.reset,args=('coilB',))
                self.coilBTimer.start()
            elif(self.coilBState=='coilB1_Entry'):
                self.coilBState='idle'
                flash_control(Exit1_WarningLight,True)
                flash_control(Exit2_WarningLight,True)
                traffic_control('A','Red')
                self.coilBTimer.cancel()
                self.WarningLightTimer.cancel()
                self.WarningLightTimer=Timer(ExitTimer,self.reset)
                self.WarningLightTimer.start()
            print('coilBState:',self.coilBState)    
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
            print('infraredState:',self.infraredState)
        elif(pin==infrared_sensorA2):
            if(self.infraredState=='idle'):
                self.infraredState='infraredA2_Entry'
                self.infraredTimer.cancel()
                self.infraredTimer=Timer(stateTimer,self.reset,args=('infrared',))
                self.infraredTimer.start()
            elif(self.infraredState=='infraredA1_Entry'):
                self.infraredState='idle'
                flash_control(Exit1_WarningLight,True)
                flash_control(Exit2_WarningLight,True)
                traffic_control('A','Red')
                self.infraredTimer.cancel()
                self.WarningLightTimer.cancel()
                self.WarningLightTimer=Timer(ExitTimer,self.reset)
                self.WarningLightTimer.start()
            print('infraredState:',self.infraredState)

        self.isRunning=False

    #重置狀態
    def reset(self,part='ALL'):
        if(part=='ALL'):
            flash_control(Exit1_WarningLight,False)
            flash_control(Exit2_WarningLight,False)
            traffic_control('A','Green')
        elif(part=='coilA'):
            self.coilAState='idle'
            print('reset coilAState:',self.coilAState)
        elif(part=='coilB'):
            self.coilBState='idle'
            print('reset coilBState:',self.coilBState)
        elif(part=='infrared'):
            self.infraredState='idle'
            print('reset infraredState:',self.infraredState)

#腳位定義
coil_sensorA1=7
coil_sensorA2=11
coil_sensorB1=13
coil_sensorB2=15
infrared_sensorA1=16
infrared_sensorA2=18
remote=22

Entry1_WarningLight=29
Entry2_WarningLight=31
Entry3_WarningLight=33
Entry4_WarningLight=35
Entry5_WarningLight=36
Exit1_WarningLight=38
Exit2_WarningLight=40
A_RedLight=37
A_GreenLight=24
B_RedLight=26
B_GreenLight=32

#計時器秒數設定
EntryTimer=30
ExitTimer=30
stateTimer=5

#進出流程
Entry=EntryFSM()
Exit=ExitFSM()

#初始腳位設定
def setup():
    GPIO.setmode(GPIO.BOARD)
    
    #sensor
    GPIO.setup(coil_sensorA1,GPIO.IN)
    GPIO.setup(coil_sensorA2,GPIO.IN)
    GPIO.setup(coil_sensorB1,GPIO.IN)
    GPIO.setup(coil_sensorB2,GPIO.IN)
    GPIO.setup(infrared_sensorA1,GPIO.IN)
    GPIO.setup(infrared_sensorA2,GPIO.IN)
    GPIO.setup(remote,GPIO.IN)
    #設定下拉電阻
    GPIO.setup(coil_sensorA1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(coil_sensorA2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(coil_sensorB1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(coil_sensorB2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(infrared_sensorA1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(infrared_sensorA2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(remote, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #設定事件觸發
    GPIO.add_event_detect(coil_sensorA1,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorA2,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorB1,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorB2,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(infrared_sensorA1,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(infrared_sensorA2,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(remote,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    #警示燈設定
    GPIO.setup(Entry1_WarningLight,GPIO.OUT)
    GPIO.setup(Entry2_WarningLight,GPIO.OUT)
    GPIO.setup(Entry3_WarningLight,GPIO.OUT)
    GPIO.setup(Entry4_WarningLight,GPIO.OUT)
    GPIO.setup(Entry5_WarningLight,GPIO.OUT)
    GPIO.setup(Exit1_WarningLight,GPIO.OUT)
    GPIO.setup(Exit2_WarningLight,GPIO.OUT)
    GPIO.output(Entry1_WarningLight,GPIO.LOW)
    GPIO.output(Entry2_WarningLight,GPIO.LOW)
    GPIO.output(Entry3_WarningLight,GPIO.LOW)
    GPIO.output(Entry4_WarningLight,GPIO.LOW)
    GPIO.output(Entry5_WarningLight,GPIO.LOW)
    GPIO.output(Exit1_WarningLight,GPIO.LOW)
    GPIO.output(Exit2_WarningLight,GPIO.LOW)
    #紅綠燈設定
    GPIO.setup(A_RedLight,GPIO.OUT)
    GPIO.setup(A_GreenLight,GPIO.OUT)
    GPIO.setup(B_RedLight,GPIO.OUT)
    GPIO.setup(B_GreenLight,GPIO.OUT)
    GPIO.output(A_RedLight,GPIO.LOW)
    GPIO.output(A_GreenLight,GPIO.HIGH)
    GPIO.output(B_RedLight,GPIO.LOW)
    GPIO.output(B_GreenLight,GPIO.HIGH)


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
    red=0
    green=0

    if(traffic=='A'):
        red=A_RedLight
        green=A_GreenLight
    elif(traffic=='B'):
        red=B_RedLight
        green=B_GreenLight

    if(light=='Red'):
        GPIO.output(red,GPIO.HIGH)
        GPIO.output(green,GPIO.LOW)
    elif(light=='Green'):
        GPIO.output(red,GPIO.LOW)
        GPIO.output(green,GPIO.HIGH)

if __name__ == '__main__':
    setup()
    
    while True:
        time.sleep(1)
