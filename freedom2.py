#!usr/bin/python
#coding=utf-8

import RobotApi as api
import RobotApi
import RestfulAPI as api2
import flask
import sys, Tkinter
import time

api.ubtRobotInitialize()
#------------------------------------------------------
ret = api.ubtRobotConnect('SDK', '1', '127.0.0.1')
if (0 != ret):
    print('连接机器人%s失败' % robotinfo.acName)
    exit(1)
#------------------------------------------------------

def go_face():

    if (api.ubtVisionDetect ( 'face', '0', 10)==0):
        api.ubtVoiceTTS ( 1, '我看到你了,正在向你走来')
        length = RobotApi.UBTEDU_ROBOTINFRARED_SENSOR_T()
        while True:
            
            RobotApi.ubtReadSensorValue('infrared', length, 5)
            time.sleep(3)
            print(length.iValue)
            if length.iValue >20:
                
                api.ubtStartRobotAction('walk', 0)

            else :
                api.ubtSetRobotMotion('bow', 'front', 2, 1)
    else:
        api.ubtVoiceTTS(1, '没找到人脸')
        
go_face()
#--------------------------------------------------------
api.ubtRobotDisconnect('SDK', '1', '127.0.0.1')
api.ubtRobotDeinitialize()

            


        


