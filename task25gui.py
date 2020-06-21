#!/usr/bin/python
# _*_ coding: utf-8 -*-

 
import sys, Tkinter 
import time
import RobotApi

RobotApi.ubtRobotInitialize()
#------------------------------Connect----------------------------------------
ret = RobotApi.ubtRobotConnect("SDK", "1", "127.0.0.1")
if (0 != ret):
        print ("Can not connect to robot %s" % robotinfo.acName)
        exit(1)

root = Tkinter.Tk()

root.title("RobotPanel"),

root.minsize(300,370)

 
def callback():

    print "OK ByeBye!"

    sys.exit()

 
Tkinter.Label(root, text="农工商机器人团队").pack()


Tkinter.Button(root, text="Exit", command=callback).pack()

def button_led1():
    RobotApi.ubtSetRobotLED("button", "red", "on")
    print'ok turn on led'
Tkinter.Button(root, text="红灯", command=button_led1).pack()
    
def button_led2():    
    RobotApi.ubtSetRobotLED("button", "blue", "breath")
    print'ok turn off led'
Tkinter.Button(root, text="蓝灯", command=button_led2).pack()

def robot_control1():
    RobotApi.ubtSetRobotMotion("walk", "front", 4,1)
    RobotApi.ubtStartRobotAction("reset",1)
    print'ok robot move forward'
Tkinter.Button(root, text="前行", command=robot_control1).pack()
    
def robot_control2():
    RobotApi.ubtSetRobotMotion("walk", "back", 2,1)
    RobotApi.ubtStartRobotAction("reset",1)
    print'ok robot backward'
Tkinter.Button(root, text="后退", command=robot_control2).pack()
    
def robot_control3():
    RobotApi.ubtSetRobotMotion("walk", "left", 3,1)
    RobotApi.ubtStartRobotAction("reset",1)
    print'ok robot move left'
Tkinter.Button(root, text="左走", command=robot_control3).pack()
    
def robot_control4():
    RobotApi.ubtSetRobotMotion("walk", "right", 3,1)
    RobotApi.ubtStartRobotAction("reset",1)
    print'ok robot move right'
Tkinter.Button(root, text="右走", command=robot_control4).pack()
    
def robot_control5():
    RobotApi.ubtSetRobotMotion("raise", "both", 3, 1)
    RobotApi.ubtStartRobotAction("reset",1)
    print'ok robot raise both hand'
Tkinter.Button(root, text="举手", command=robot_control5).pack()

def robot_control6():
    RobotApi.ubtSetRobotMotion("bow", "", 1, 1)
    RobotApi.ubtStartRobotAction("reset",1)
    print'ok robot bow'
Tkinter.Button(root, text="鞠躬", command=robot_control6).pack()

def robot_control7():
    RobotApi.ubtVoiceTTS(1,"你好，我是农工商智能教学机器人")
    print'ok robot say something'
Tkinter.Button(root, text="说话", command=robot_control7).pack()

def robot_control8():
    RobotApi.ubtStopRobotAction()
    print'ok robot stop motion'
Tkinter.Button(root, text="复位", command=robot_control8).pack()

def robot_photo():
    RobotApi.ubtTakeAPhoto("",5)
    print'ok take a photo'
Tkinter.Button(root, text="拍照", command=robot_photo).pack()

root.mainloop()