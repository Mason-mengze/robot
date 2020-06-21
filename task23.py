#!/usr/bin/python
# _*_ coding: utf-8 -*-

import time
import RobotApi

RobotApi.ubtRobotInitialize()
#------------------------------Connect---------------------------------
gIPAddr=""

robotinfo=RobotApi.UBTEDU_ROBOTINFO_T()
#The robot name you want to connect
robotinfo.acName="Yanshee_369E"
ret=RobotApi.ubtRobotDiscovery("SDK",1,robotinfo)
if(0!=ret):
    print("Return value: %d"%ret)
    exit(1)

gIPAddr=robotinfo.acIPAddr
ret=RobotApi.ubtRobotConnect("SDK","1",gIPAddr)
if(0!=ret):
    print("Can not connect to robot %s"%robotinfo.acName)
    exit(1)

#---------------------------Read Sensor Value--------------------------
touch_sensor=RobotApi.UBTEDU_ROBOTTOUCH_SENSOR_T()
#RobotApi.ubtSetRobotMotion("raise", "left", 3, 1)
while True:
    time.sleep(1)
    ret=RobotApi.ubtReadSensorValue("touch",touch_sensor,4)
    if ret!=0:
        print("Can not read Sensor value. Error code: %d"%(ret))
    else:
        print("Read Touch Sensor Value: %d "%(touch_sensor.iValue))
    if touch_sensor.iValue > 0 : 
        ret = RobotApi.ubtVoiceTTS(1,"很高兴认识你，人类朋友，我是人工智能教育机器人 偃师！ ")
        RobotApi.ubtSetRobotLED("button", "red", "blink")
        time.sleep(2)
        RobotApi.ubtSetRobotMotion("raise", "left", 3, 1)
        
        RobotApi.ubtSetRobotLED("button", "blue", "breath")

#---------------------------Disconnect---------------------------------
RobotApi.ubtRobotDisconnect("SDK","1",gIPAddr)
RobotApi.ubtRobotDeinitialize()
