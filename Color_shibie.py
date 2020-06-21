#usr/bin/python
#_*_coding: utf-8 _*_
import cv2
import numpy as np
import io
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import RobotApi as api

api.ubtRobotInitialize()
ret = api.ubtRobotConnect("SDK", "1", "127.0.0.1")
if (0!= ret):
    print ("Can not connect to robot %s" % robotinfo.acName)
        #打印连接错误返回信息
    exit(1)

ball_color = 'red'
color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},#Lower颜色的下限,Upper颜色的上限
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              }

camera = PiCamera()
camera.resolution = (640, 480)
# 分辨率
camera.framerate = 32
# 帧率

#使用此作为输出 src
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(1)

while True:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        if frame is not None:
            gs_frame = cv2.GaussianBlur(image, (5, 5), 0)                     # 高斯模糊，参数一：frame需要高斯模糊的图像参数二：(5, 5)高斯矩阵的长与宽都是5参数三：0标准差是0
            hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)                 # 转化成HSV图像，参数一：gs_frame原图像，参数二：cv2.COLOR_BGR2HSV颜色转换方式，从BGR to HSV
            erode_hsv = cv2.erode(hsv, None, iterations=2)                   # 腐蚀 粗的变细，参数一：hsv原图像，参数三：iterations=2腐蚀的宽度
            inRange_hsv = cv2.inRange(erode_hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])  #二值化，去除背景部分，参数一：erode_hsv原图像，参数二：color_dist[ball_color]['Lower']颜色的下限，参数三：color_dist[ball_color]['Upper']颜色的上限
            cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] #使用该函数找出方框外边界，并存储在cnts中

            c = max(cnts, key=cv2.contourArea)#在边界中找出面积最大的区域
            (x, y), r = cv2.minEnclosingCircle(c)#读取边缘的外包圆（最小的封闭圆），返回坐标及半径（都是返回float类型）
            if r > 10:
                cv2.circle(inRange_hsv, (int(x), int(y)), int(r), (0, 0, 255), 3)#在frame画出圆，中心为（x，y），半径：r，颜色：red，线宽：3
                print("坐标：%d,%d 半径：%d" % (x, y, r))
            if int(x) < inRange_hsv.shape[0] / 2 - 20:
                api.ubtSetRobotLED("button", "yellow", "breath")
                print("在左边")
            elif int(x) > inRange_hsv.shape[0] / 2 + 20:
                api.ubtSetRobotLED("button", "green", "breath")
                print("在右边")
            else:
                api.ubtSetRobotLED("button", "blue", "breath")
                print("在中间")
            
            cv2.imshow('camera', inRange_hsv)
            cv2.waitKey(1)
        else:
            print("无画面")

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
