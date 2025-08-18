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
    def process(self):
        self.isRunning=True
        isPass=False
        global entryOn,exitOn

        if(GPIO.input(coil_sensorA1)==GPIO.HIGH and GPIO.input(coil_sensorA2)==GPIO.HIGH):
            isPass=True
            self.WarningLightTimer.cancel()
            self.WarningLightTimer=Timer(EntryTimer,self.reset)
            self.WarningLightTimer.start()
        elif(GPIO.input(coil_sensorB1)==GPIO.HIGH and GPIO.input(coil_sensorB2)==GPIO.HIGH):
            isPass=True
            self.WarningLightTimer.cancel()
            self.WarningLightTimer=Timer(EntryTimer,self.reset)
            self.WarningLightTimer.start()
        elif(GPIO.input(coil_sensorC1)==GPIO.HIGH and GPIO.input(coil_sensorC2)==GPIO.HIGH):
            isPass=True
            self.WarningLightTimer.cancel()
            self.WarningLightTimer=Timer(EntryTimer,self.reset)
            self.WarningLightTimer.start()
        elif(GPIO.input(infrared_sensorA1)==GPIO.HIGH and GPIO.input(infrared_sensorA2)==GPIO.HIGH):
            isPass=True
            self.WarningLightTimer.cancel()
            self.WarningLightTimer=Timer(EntryTimer,self.reset)
            self.WarningLightTimer.start()

        if(isPass and not exitOn):
            flash_control(Exit_WarningLight,True)
            traffic_control('Exit','Red')
            entryOn=True
             
        self.isRunning=False

    #重置狀態
    def reset(self):
        global entryOn

        flash_control(Exit_WarningLight,False)
        traffic_control('Exit','Green')
        entryOn=False

#退出流程物件
class ExitFSM:
    def __init__(self):
        self.isRunning=False
        self.WarningLightTimer=Timer(0,self.reset)
        self.WarningLightTimer.cancel()
    
    #退出流程處理
    def process(self):
        self.isRunning=True
        isPass=False
        global entryOn,exitOn

        if(GPIO.input(coil_sensorD1)==GPIO.HIGH and GPIO.input(coil_sensorD2)==GPIO.HIGH):
            isPass=True
            self.WarningLightTimer.cancel()
            self.WarningLightTimer=Timer(ExitTimer,self.reset)
            self.WarningLightTimer.start()
        elif(GPIO.input(coil_sensorE1)==GPIO.HIGH and GPIO.input(coil_sensorE2)==GPIO.HIGH):
            isPass=True
            self.WarningLightTimer.cancel()
            self.WarningLightTimer=Timer(ExitTimer,self.reset)
            self.WarningLightTimer.start()
        elif(GPIO.input(coil_sensorF1)==GPIO.HIGH and GPIO.input(coil_sensorF2)==GPIO.HIGH):
            isPass=True
            self.WarningLightTimer.cancel()
            self.WarningLightTimer=Timer(ExitTimer,self.reset)
            self.WarningLightTimer.start()
        elif(GPIO.input(infrared_sensorB1)==GPIO.HIGH and GPIO.input(infrared_sensorB2)==GPIO.HIGH):
            isPass=True
            self.WarningLightTimer.cancel()
            self.WarningLightTimer=Timer(ExitTimer,self.reset)
            self.WarningLightTimer.start()  

        if(isPass and not entryOn):
            flash_control(Entry_WarningLight,True)
            traffic_control('Entry','Red')
            exitOn=True

        self.isRunning=False

    #重置狀態
    def reset(self):
        global exitOn

        flash_control(Entry_WarningLight,False)
        traffic_control('Entry','Green')
        exitOn=False

#腳位定義
coil_sensorA1=33
coil_sensorA2=35
coil_sensorB1=19
coil_sensorB2=21
coil_sensorC1=15
coil_sensorC2=23
coil_sensorD1=16
coil_sensorD2=18
coil_sensorE1=8
coil_sensorE2=10
coil_sensorF1=22
coil_sensorF2=24
infrared_sensorA1=36
infrared_sensorA2=38
infrared_sensorB1=26
infrared_sensorB2=32

TimerMSB=37
TimerLSB=40

Entry_WarningLight=13
Exit_WarningLight=31
Entry_trafficLight=11
Exit_trafficLight=29

entryOn=False
exitOn=False

#計時器秒數設定
EntryTimer=0 #由程式啟動時設定
ExitTimer=0 #由程式啟動時設定

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
    GPIO.setup(coil_sensorC1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(coil_sensorC2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(coil_sensorD1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(coil_sensorD2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(coil_sensorE1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(coil_sensorE2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(coil_sensorF1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(coil_sensorF2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(infrared_sensorA1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(infrared_sensorA2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(infrared_sensorB1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(infrared_sensorB2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #計時器秒數設定腳位與下拉電阻
    GPIO.setup(TimerMSB,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(TimerLSB,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    #設定事件觸發
    GPIO.add_event_detect(coil_sensorA1,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorA2,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorB1,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorB2,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorC1,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorC2,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorD1,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorD2,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorE1,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorE2,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorF1,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(coil_sensorF2,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(infrared_sensorA1,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(infrared_sensorA2,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(infrared_sensorB1,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    GPIO.add_event_detect(infrared_sensorB2,GPIO.RISING,callback=SensorCallBack ,bouncetime=200)
    #警示燈設定
    GPIO.setup(Entry_WarningLight,GPIO.OUT)
    GPIO.setup(Exit_WarningLight,GPIO.OUT)
    GPIO.output(Entry_WarningLight,GPIO.LOW)
    GPIO.output(Exit_WarningLight,GPIO.LOW)
    #紅綠燈設定
    GPIO.setup(Entry_trafficLight,GPIO.OUT)
    GPIO.setup(Exit_trafficLight,GPIO.OUT)
    GPIO.output(Entry_trafficLight,GPIO.LOW)
    GPIO.output(Exit_trafficLight,GPIO.LOW)
    #計時器秒數設定 
    timerSetting()

#按鈕中斷執行程序
def SensorCallBack(pin):
    #建立進入流程執行緒
    if(pin in [coil_sensorA1,coil_sensorA2,coil_sensorB1,coil_sensorB2,coil_sensorC1,coil_sensorC2,infrared_sensorA1,infrared_sensorA2]):
        if(not(Entry.isRunning)):
            threadEntry=threading.Thread(target=Entry.process, args=())
            threadEntry.start()
        
    #建立退出流程執行緒
    elif(pin in [coil_sensorD1,coil_sensorD2,coil_sensorE1,coil_sensorE2,coil_sensorF1,coil_sensorF2,infrared_sensorB1,infrared_sensorB2]):
        if(not(Exit.isRunning)):
            threadExit=threading.Thread(target=Exit.process, args=())
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

    if(traffic=='Entry'):
        trafficLight=Entry_trafficLight
    elif(traffic=='Exit'):
        trafficLight=Exit_trafficLight

    if(light=='Red'):
        GPIO.output(trafficLight,GPIO.HIGH)
    elif(light=='Green'):
        GPIO.output(trafficLight,GPIO.LOW)

#警示燈時間設定
def timerSetting():
    global ExitTimer
    global EntryTimer
    second=10

    if(GPIO.input(TimerMSB)==GPIO.HIGH):
        second+=10
    if(GPIO.input(TimerLSB)==GPIO.HIGH):
        second+=5

    EntryTimer=second
    ExitTimer=second

if __name__ == '__main__':
    setup()
    
    while True:
        time.sleep(1)
