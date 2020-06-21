#!/usr/bin/python
# _*_ coding: utf-8 -*-

import time
import RobotApi as api

api.ubtRobotInitialize()
#------------------------------Connect----------------------------------------
ret = api.ubtRobotConnect("SDK", "1", "127.0.0.1")
if (0 != ret):
        print ("Can not connect to robot %s" % robotinfo.acName)
        exit(1)
#---------------------------Read Sensor Value-------------------------------
isInterrputed = 1
infrared_sensor = api.UBTEDU_ROBOTINFRARED_SENSOR_T()
while True:
        time.sleep(3)
	ret = api.ubtReadSensorValue("infrared",infrared_sensor,4)
	if ret != 0:
	    print("Can not read Sensor value. Error code: %d" % (ret))  
	else:
    	    print("Read Sensor Value: %d mm" % (infrared_sensor.iValue))
	    infrared_int = infrared_sensor.iValue/10
	    infrared_str = str("距离障碍物")+str(infrared_int)+str("cm")
	    ret = api.ubtVoiceTTS(isInterrputed, infrared_str)
	    if ret != 0:
		print("Can not play TTS voice. Error code: %d" % ret)

#---------------------------Disconnect--------------------------------------
api.ubtRobotDisconnect("SDK","1","127.0.0.1")
api.ubtRobotDeinitialize()