#!/usr/bin/python
# -*- coding: utf-8 -*-


import RobotApi

# Connect robot SDK
RobotApi.ubtRobotInitialize()
ret = RobotApi.ubtRobotConnect("SDK", "1", "127.0.0.1")
if (0 != ret):
    print ("Can not connect to robot sdk")
    exit(1)

isSetLed = False

if __name__ == '__main__':
    try:
        # block program start here
        #--------------------------


        if (RobotApi.ubtVisionDetect("face", "0",10) == 0): 

            #show_tts.
            RobotApi.ubtVoiceTTS(0, "你好，很高兴认识你，人类朋友，非常感谢你的到来。")

            #show_chest.
            RobotApi.ubtSetRobotLED("button", "red", "blink")
            isSetLed = True

            #moves_walk.
            RobotApi.ubtSetRobotMotion("walk", "front", 2, 1)

            #Bow.
            RobotApi.ubtSetRobotMotion("bow", "", 1, 1)
            RobotApi.ubtStartRobotAction("reset", 1)
        else:

            #show_tts.
            RobotApi.ubtVoiceTTS(0, "你好朋友，请让我看到你们的脸。")

            #show_chest.
            RobotApi.ubtSetRobotLED("button", "yellow", "blink")
            isSetLed = True

            #moves_wave_hand.
            RobotApi.ubtSetRobotMotion("wave", "left", 3, 1)

            #moves_walk.
            #RobotApi.ubtSetRobotMotion("walk", "back", 2, 1)
            RobotApi.ubtStartRobotAction("reset", 1)

        #--------------------------
        # block program end
        print "Run blockly complete!"
    except:
        print "runError"

    if isSetLed:
        RobotApi.ubtSetRobotLED("button", "blue", "breath")

    # Reset robot servo
    RobotApi.ubtStartRobotAction("reset", 1)
    # Disconnect robot SDK
    RobotApi.ubtRobotDisconnect("SDK", "1", "127.0.0.1")
    RobotApi.ubtRobotDeinitialize()