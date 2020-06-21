#!/usr/bin/python
# _*_ coding: utf-8 -*-

import time
import RobotApi as api

api.ubtRobotInitialize()
# 用RobotApi.ubtRobotInitialize()对机器人进行初始化
# RobotApi.ubtRobotDeinitialize() RobotApi

# ------------------------------Connect----------------------------------------
ret = api.ubtRobotConnect("SDK", "1", "127.0.0.1")
# 连接到机器人，其中这里的127.0.0.1为创造一个本地回环，也可以输入机器人当前的IP地址
if (0!= ret):
# 如果返回值不为0则连接错误
        print ("Can not connect to robot %s" % robotinfo.acName)
        #打印连接错误返回信息
        exit(1)
        # 错误退出
# ---------------------------Read Sensor Value-------------------------------
isInterrputed = 1
infrared_sensor = api.UBTEDU_ROBOTINFRARED_SENSOR_T()
# 声明传感器所读取的数据api.UBTEDU_ROBOTINFRARED_SENSOR_T() # RobotApi.UBTEDU_ROBOTINFRARED_SENAOR_T()
while True:
    	time.sleep(3)
    # 延时执行3秒
	ret = api.ubtReadSensorValue("infrared",infrared_sensor, 4)
	#参数选择红外，返回红外的返回传感器的值，返回最大数值的长度
	if ret != 0:
            #如果返回值不为0则打印传感器的值
	    print("Can not read Sensor value. Error code: %d" % ret)
	    #格式化打印ret的值
	else:
    	    print("Read Sensor Value: %d mm" % infrared_sensor.iValue)
    	    #打印传感器所获取到的信息
	    infrared_int = infrared_sensor.iValue/10
	    #单位毫米除与10转换为厘米
	    
	    if infrared_int < 10:
	         api.ubtSetRobotMotion("raise", "left", 3, 1)
	         # 根据API文档 raise左手，left选定左手，3为速度，1为重复次数
	         api.ubtSetRobotLED("button", "red", "breath")
	         #根据API文档 ，控制灯光，buntton选定机器人胸口按钮灯光，red为将灯光调为红色，将灯光调为呼吸灯
	         infrared_str = str("距离太近，请远离一点")+str("距离障碍物")+str(infrared_int)+str("cm")
	         #定义一个用于阅读的字符对象
	         ret = api.ubtVoiceTTS(isInterrputed, infrared_str)
	         #根据API文档,调用TTS语音播放定义的字符
	        
	    elif infrared_int >20:
                 api.ubtSetRobotMotion("bow", "front", 2, 1)
                 #根据API文档 bow为鞠躬，font选定向前，2为速度，1为重复次数
	         api.ubtSetRobotLED("button", "yellow", "breath")
	         ##根据API文档 ，控制灯光，buntton选定机器人胸口按钮灯光，yellow为将灯光调为黄色，将灯光调为呼吸灯
	    	 infrared_str = str ("谢谢")+str("距离障碍物")+str(infrared_int)+str("cm")
	    	 #定义一个用于阅读的字符对象
	         ret = api.ubtVoiceTTS(isInterrputed, infrared_str)
	         #根据API文档,调用TTS语音播放定义的字符
	    if ret != 0:
			print("Can not play TTS voice. Error code: %d" % ret)
		#如果调用TTS语音失败，则打印返回的错误信息

#---------------------------Disconnect--------------------------------------
api.ubtRobotDisconnect("SDK","1","127.0.0.1")
#断开连接
api.ubtRobotDeinitialize()
#关闭初始化