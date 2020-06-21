#!/usr/bin/python
# -*- coding: utf-8 -*-                                                                                

import time
import RobotApi as api

api.ubtRobotInitialize()
    #-----------------------↓ block program start here ↓----------------------


    if (getRobotSensorValue("obstacle") < 10):
      #raise_hand
      api.ubtSetRobotMotion("raise", "left", 3, 1)

      #lights_chest.
      api.ubtSetRobotLED("button", "red", "blink")
      ubtinit.isSetLed = True

      #sound_tts.
      api.ubtVoiceTTS(0, "距离太近，请靠远点")



    if (getRobotSensorValue("obstacle") > 10):
      #lights_chest.
      api.ubtSetRobotLED("button", "yellow", "blink")
      ubtinit.isSetLed = True

      #sound_tts.
      api.ubtVoiceTTS(0, "谢谢")

    #-----------------------↑     block program end    ↑----------------------
api.ubtRobotDisconnect("SDK","1","127.0.0.1")
api.ubtRobotDeinitialize()
