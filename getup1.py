#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import RobotApi as api

api.ubtRobotInitialize()
#------------------------------Connect----------------------------------------
ret = api.ubtRobotConnect("SDK", "1", "127.0.0.1")
if (0 != ret):
    print ("Can not connect to robot %s" % robotinfo.acName)
    exit(1)
#---------------------------Read Sensor Value-------------------------------
while True:
    time.sleep(3)   
    if (getRobotSensorValue("obstacle") <= 10):
      #lights_chest.
      api.ubtSetRobotLED("button", "red", "blink")
      ubtinit.isSetLed = True

      #sound_tts.
      api.ubtVoiceTTS(0, "距离太近了，请离远点")



    elif (getRobotSensorValue("obstacle") > 20):
      #lights_chest.
      api.ubtSetRobotLED("button", "yellow", "blink")
      ubtinit.isSetLed = True

      #sound_tts.
      api.ubtVoiceTTS(0, "谢谢")

#---------------------------Disconnect--------------------------------------
api.ubtRobotDisconnect("SDK","1","127.0.0.1")
api.ubtRobotDeinitialize()
