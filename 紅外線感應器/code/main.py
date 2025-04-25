#!/usr/bin/python3

import RPi.GPIO as GPIO
import threading
from threading import Timer
import time

#進入流程物件
class EntryFSM:
    def __init__(self):
        self.inState='idle'
        self.onway=0
        self.outState='idle'
        self.isRunning=False
        self.beginTimer=Timer(0,self.reset)
        self.lastTimer=Timer(0,self.reset)
        self.oddTimer=Timer(0,self.reset)
        self.beginTimer.cancel()
        self.lastTimer.cancel()
        self.oddTimer.cancel()

    #進入流程處理
    def process(self,pin,processlock):
        self.isRunning=True
        global laneVehicleCount

        if(self.inState=='idle'):
            if(pin==A1_sensor):
                self.inState='A1_first'                       
                self.beginTimer=Timer(firstTimer,self.reset,args=('in',))     
                self.beginTimer.start()
            elif(pin==A2_sensor):
                self.inState='A2_first'
                self.beginTimer=Timer(firstTimer,self.reset,args=('in',))     
                self.beginTimer.start()
        elif(self.inState=='A1_first'):
            if(pin==A2_sensor):
                self.onway+=1
                with laneVehicleCountLock:
                    laneVehicleCount+=1
                self.inState='idle'
                flash_control(B_WarningLight,True)
                traffic_control('B','Red')
                self.beginTimer.cancel();self.lastTimer.cancel()
                self.lastTimer=Timer(secondTimer,self.reset)
                self.lastTimer.start()
        elif(self.inState=='A2_first'):
            if(pin==A1_sensor):
                self.inState='idle'
                if(self.onway>0 and self.onway==laneVehicleCount and not(processlock[0])):
                    self.onway-=1
                    with laneVehicleCountLock:
                        laneVehicleCount-=1
                        processlock[0]=True
                self.beginTimer.cancel()

        if(self.outState=='idle'):
            if(pin==B2_sensor):
                self.outState='B2_Entry'
                self.lastTimer.cancel()
                self.lastTimer=Timer(thirdTimer,self.reset)
                self.lastTimer.start()
            elif(pin==B1_sensor):
                self.outState='B1_Entry'
                self.oddTimer=Timer(firstTimer,self.reset,args=('out',))     
                self.oddTimer.start()
        elif(self.outState=='B2_Entry'):
            if(pin==B1_sensor):
                self.outState='idle'
                if(self.onway>0 and laneVehicleCount>0 and not(processlock[0])):
                    self.onway-=1
                    with laneVehicleCountLock:
                        laneVehicleCount-=1
                        processlock[0]=True
                if(self.onway<=0):
                    self.onway=0
                    flash_control(B_WarningLight,False)
                    traffic_control('B','Green')
                    self.lastTimer.cancel()
        elif(self.outState=='B1_Entry'):
            if(pin==B2_sensor):
                self.outState='idle'
                self.oddTimer.cancel()

        self.isRunning=False
        
    #重置狀態
    def reset(self,part='All'):
        global laneVehicleCount

        if(part=='All'):
            self.inState='idle'
            self.outState='idle'
            with laneVehicleCountLock:
                laneVehicleCount-=self.onway
            self.onway=0
            flash_control(B_WarningLight,False)
            traffic_control('B','Green')
        elif(part=='in'):
            self.inState='idle'
        elif(part=='out'):
            self.outState='idle'

#退出流程物件
class ExitFSM:
    def __init__(self):      
        self.inState='idle'
        self.onway=0
        self.outState='idle'
        self.isRunning=False
        self.beginTimer=Timer(0,self.reset)
        self.lastTimer=Timer(0,self.reset)
        self.oddTimer=Timer(0,self.reset)
        self.beginTimer.cancel()
        self.lastTimer.cancel()
        self.oddTimer.cancel()

    #退出流程處理
    def process(self,pin,processlock):
        self.isRunning=True
        global laneVehicleCount

        if(self.inState=='idle'):
            if(pin==B1_sensor):
                self.inState='B1_first'                       
                self.beginTimer=Timer(firstTimer,self.reset,args=('in',))     
                self.beginTimer.start()
            elif(pin==B2_sensor):
                self.inState='B2_first'
                self.beginTimer=Timer(firstTimer,self.reset,args=('in',))     
                self.beginTimer.start()
        elif(self.inState=='B1_first'):
            if(pin==B2_sensor):
                self.onway+=1
                with laneVehicleCountLock:
                    laneVehicleCount+=1
                self.inState='idle'
                flash_control(A_WarningLight,True)
                traffic_control('A','Red')
                self.beginTimer.cancel();self.lastTimer.cancel()
                self.lastTimer=Timer(secondTimer,self.reset)
                self.lastTimer.start()
        elif(self.inState=='B2_first'):
            if(pin==B1_sensor):
                self.inState='idle'
                if(self.onway>0 and self.onway==laneVehicleCount and not(processlock[0])):
                    self.onway-=1
                    with laneVehicleCountLock:
                        laneVehicleCount-=1
                        processlock[0]=True
                self.beginTimer.cancel()

        if(self.outState=='idle'):
            if(pin==A2_sensor):
                self.outState='A2_Entry'
                self.lastTimer.cancel()
                self.lastTimer=Timer(thirdTimer,self.reset)
                self.lastTimer.start()
            elif(pin==A1_sensor):
                self.outState='A1_Entry'
                self.oddTimer=Timer(firstTimer,self.reset,args=('out',))     
                self.oddTimer.start()
        elif(self.outState=='A2_Entry'):
            if(pin==A1_sensor):
                self.outState='idle'
                if(self.onway>0 and laneVehicleCount>0 and not(processlock[0])):
                    self.onway-=1
                    with laneVehicleCountLock:
                        laneVehicleCount-=1
                        processlock[0]=True
                if(self.onway<=0):
                    self.onway=0
                    flash_control(A_WarningLight,False)
                    traffic_control('A','Green')
                    self.lastTimer.cancel()
        elif(self.outState=='A1_Entry'):
            if(pin==A2_sensor):
                self.outState='idle'
                self.oddTimer.cancel()

        self.isRunning=False

    #重置狀態
    def reset(self,part='All'):
        global laneVehicleCount

        if(part=='All'):
            self.inState='idle'
            self.outState='idle'
            with laneVehicleCountLock:
                laneVehicleCount-=self.onway
            self.onway=0
            flash_control(A_WarningLight,False)
            traffic_control('A','Green')
        elif(part=='in'):
            self.inState='idle'
        elif(part=='out'):
            self.outState='idle'

#腳位定義
A1_sensor=11
A2_sensor=13
A_WarningLight=36
A_RedLight=29
A_GreenLight=31
B1_sensor=16
B2_sensor=18
B_WarningLight=38
B_RedLight=33
B_GreenLight=35

#計時器秒數設定
firstTimer=5
secondTimer=30
thirdTimer=30

#紀錄車道內數量
laneVehicleCount=0
laneVehicleCountLock = threading.Lock()

#進出流程
Entry=EntryFSM()
Exit=ExitFSM()

#初始腳位設定
def setup():
    GPIO.setmode(GPIO.BOARD)
    
    #sensor
    GPIO.setup(A1_sensor,GPIO.IN)
    GPIO.setup(A2_sensor,GPIO.IN)
    GPIO.setup(B1_sensor,GPIO.IN)
    GPIO.setup(B2_sensor,GPIO.IN)
    #設定下拉電阻
    GPIO.setup(A1_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(A2_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(B1_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(B2_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #設定事件觸發
    GPIO.add_event_detect(A1_sensor,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(A2_sensor,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(B1_sensor,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(B2_sensor,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)

    #警示燈設定
    GPIO.setup(A_WarningLight,GPIO.OUT)
    GPIO.setup(B_WarningLight,GPIO.OUT)
    GPIO.output(A_WarningLight,GPIO.LOW)
    GPIO.output(B_WarningLight,GPIO.LOW)

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
    processlock=[False]

    #建立進入流程執行緒
    if(not(Entry.isRunning)):
        threadEntry=threading.Thread(target=Entry.process, args=(pin,processlock,))
        threadEntry.start()
        
    #建立退出流程執行緒
    if(not(Exit.isRunning)):
       threadExit=threading.Thread(target=Exit.process, args=(pin,processlock,))
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
