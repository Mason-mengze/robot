#!/usr/bin/python
# _*_ coding: utf-8 -*-
import time
import RobotApi
RobotApi.ubtRobotInitialize()
#------------------------------Connect----------------------------------
gIPAddr = ""
robotinfo = RobotApi.UBTEDU_ROBOTINFO_T()
#The robot name you want to connect
robotinfo.acName="Yanshee_369E"
ret = RobotApi.ubtRobotDiscovery("SDK", 15, robotinfo)
if (0 != ret):
print ("Return value: %d" % ret)
exit(1)
gIPAddr = robotinfo.acIPAddr
ret = RobotApi.ubtRobotConnect("SDK", "1", gIPAddr)
if (0 != ret):
print ("Can not connect to robot %s" % robotinfo.acName)
exit(1)

 #-----------------------↓ block program start here ↓----------------------


    if (getRobotSensorValue("obstacle") <= 10):
      #lights_chest.
      api.ubtSetRobotLED("button", "red", "blink")
      ubtinit.isSetLed = True

      #sound_tts.
      api.ubtVoiceTTS(0, "距离太近了，请离远点")



    elif (getRobotSensorValue("obstacle") <= 20):
      #lights_chest.
      api.ubtSetRobotLED("button", "yellow", "blink")
      ubtinit.isSetLed = True

      #sound_tts.
      api.ubtVoiceTTS(0, "谢谢")

    #-----------------------↑     block program end    ↑----------------------
RobotApi.ubtRobotDisconnect("SDK","1",gIPAddr)
RobotApi.ubtRobotDeinitialize()