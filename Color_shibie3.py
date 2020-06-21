#!usr/bin/python
#coding=utf-8

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RobotApi as api

#下面定义颜色上下限，用的是hsv颜色而不是rgb颜色

red1 = np.array([170, 100, 100])  
red2 = np.array([179, 255, 255]) 
camera = PiCamera()
win, camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(1)

for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = image.array
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, red1, red2) #二值化，去除背景部分，参数一：erode_hsv原图像，参数二：color_dist[ball_color]['Lower']颜色的下限，参数三：color_dist[ball_color]['Upper']颜色的上限
    mask = cv2.erode(mask, None, iterations=2)   # 腐蚀 粗的变细，参数一：hsv原图像，参数三：iterations=2腐蚀的宽度
    mask = cv2.dilate(mask, None, iterations=2)  #膨胀 由细再 变粗参数和上面差不多
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  #找到边框 cv2.RETR_EXTERNAL表示只检测外轮廓 cv2.CHAIN_APPROX_SIMPLE：只保留终点坐标（没有线段）[2]:去倒数第二个返回值也就是轮廓

    if len(cnts) > 0:
        c = max(cnts, key = cv2.contourArea)    #在边界中找出面积最大的区域

        ((x, y), r) = cv2.minEnclosingCircle(c)    #用圆形圈最小圆形出轮廓,并返回圆心坐标，半径
        

        M = cv2.moments(c)

        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))   #计算圆心（m00)即为轮廓的面积。
        print("坐标：%d,%d 半径：%d" % (x, y, r))
        if r > 10: 

            cv2.circle(frame, (int(x), int(y)), int(r), (0, 255, 255), 2)   #用红线圈出物体
            if int(x) < win.shape[0] / 2 - 20:
                api.ubtSetRobotLED("button", "yellow", "breath")
                print("在左边")
            elif int(x) > win.shape[0] / 2 + 20:win
                api.ubtSetRobotLED("button", "green", "breath")
                print("在右边")
            else:
                api.ubtSetRobotLED("button", "blue", "breath")
                print("在中间")

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):

        break