#!usr/bin/python3
# -*- coding: utf-8 -*-

#导入库
import RobotApi
import time

#初始化 RobotApi.ubtRobotinitialize() RobotApi.ubtrobotinitialize()
#RobotApi.ubtRobotinitialize() RobotApi.ubtrobotinitialize()
RobotApi.ubtRobotInitialize()

#连接机器人
ret = RobotApi.ubtRobotConnect("SDK", "1", "127.0.0.1")
#ret = RobotApi.ubtRobotConnect("SDK", "1", "127.0.0.1")
#ret = RobotApi.ubtRobotConnect("SDK", "1", "127.0.0.1")
if 0 != ret:
    # 测返回值
    print('连接失败，错误代码：%s' % robotinfo.acName)
    exit(1)

#主程序
#机器人检测到红外（超声波）传感器距离障碍物小于10cm时举左手、闪红灯、
#建立循环
infrared_sensor = RobotApi.UBTEDU_ROBOTINFRARED_SENSOR_T()
while True:
#延时执行
    time.sleep(3)
    ret = RobotApi.ubtReadSensorValue('infrared', infrared_sensor, 4)
    #ret = RobotApi.ubtReadSensorValue("infrared", infrared_sensor, 4)
    if ret!= 0:
        print('读取不到传感器，错误代码：%d' % ret)
    else:
        print('传感器读取得数值为：%d mm' % infrared_sensor.iValue)
        #print("Read Sensor Value: %d mm" % infrared_sensor.iValue)
        #转换距离单位
        infrared_int = infrared_sensor.iValue/10

        if infrared_int < 10:
            #导入api执行动作
            RobotApi.ubtSetRobotMotion('raise', 'left', 3, 1)
            #api.ubtSetRobotMotion("raise", "left", 3, 1)
            #控制灯光
            RobotApi.ubtSetRobotLED('button', 'red', 'breath')
            #将文字实例化
            infrared_str = str('距离太近，请远离一点') + str('距离障碍物') + str(infrared_int) + str('厘米')

            #infrared_str = str("距离太近，请远离一点") + str("距离障碍物") + str(infrared_int) + str("cm")
            ## 定义一个用于阅读的字符对象
            #ret = api.ubtVoiceTTS(isInterrputed, infrared_str)
            #调用TTs语音输出
            ret = RobotApi.ubtVioceTTS(1, infrared_str)

            # api.ubtSetRobotLED("button", "red", "breath")
#并通过语音模块说：“距离太近，请远离一点”，
#检测到红外（超声波）传感器距离障碍物大于20cm时做鞠躬动作、闪黄灯，并说：“谢谢！”。
        elif infrsred_int >20:
            RobotApi.ubtSetRobotMotion('bow', 'front', 2, 1)
            RobotApi.ubtSetRobotLED('button', 'yellow', 'breath')
            infrared_str = str('谢谢') + str('距离障碍物') + str(infrared_int) + str('厘米')
            ret= RobotApi.ubtVioceTTS(1, infrared_str)
        if ret != 0:

            #TTS返回值
            print('调用TTS失败，返回错误代码：%d' % ret)

# 断开连接关闭实例化
RobotApi.ubtRobotDisconnect("SDK","1","127.0.0.1")
RobotApi.ubtRobotDeinitialize()

# api.ubtRobotDisconnect("SDK","1","127.0.0.1")
# #断开连接
# api.ubtRobotDeinitialize()


# RobotApi.UBTEDU_ROBOTINFRARED_SENAOR_T() 这句话好难打多打几次练熟


# !/usr/bin/python
# _*_ coding: utf-8 -*-

import time
import RobotApi

RobotApi.ubtRobotInitialize()
# ------------------------------Connect---------------------------------
RobotApi.ubtRobotInitialize()

# 连接机器人
ret = RobotApi.ubtRobotConnect("SDK", "1", "127.0.0.1")
# ret = RobotApi.ubtRobotConnect("SDK", "1", "127.0.0.1")
# ret = RobotApi.ubtRobotConnect("SDK", "1", "127.0.0.1")
if 0 != ret:
    # 测返回值
    print('连接失败，错误代码：%s' % robotinfo.acName)
    exit(1)

# ---------------------------Read Sensor Value--------------------------
touch_sensor = RobotApi.UBTEDU_ROBOTTOUCH_SENSOR_T()
# RobotApi.ubtSetRobotMotion("raise", "left", 3, 1)
while True:
    time.sleep(1)
    ret = RobotApi.ubtReadSensorValue("touch", touch_sensor, 4)
    if ret != 0:
        print("Can not read Sensor value. Error code: %d" % (ret))
    else:
        print("Read Touch Sensor Value: %d " % (touch_sensor.iValue))
    if touch_sensor.iValue > 0:
        ret = RobotApi.ubtVoiceTTS(1, "很高兴认识你，人类朋友，我是人工智能教育机器人 偃师！ ")
        RobotApi.ubtSetRobotLED("button", "red", "blink")
        time.sleep(2)
        RobotApi.ubtSetRobotMotion("raise", "left", 3, 1)

        RobotApi.ubtSetRobotLED("button", "blue", "breath")

# ---------------------------Disconnect---------------------------------
RobotApi.ubtRobotDisconnect("SDK", "1", '127.0.0.1')
RobotApi.ubtRobotDeinitialize()





















