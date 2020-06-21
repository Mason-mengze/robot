#!/usr/bin/python
#coding=utf-8

from picamera.array import PiRGBArray
from picamera import PiCamera
from functools import partial

from socket import *
import multiprocessing as mp
import cv2
import os
import time
import httplib, urllib, base64, json
import threading

##############################
#Version = "V1.0"
#Author = "Sanson"
#Date = "2017/12/29"
##############################

resX = 500
resY = 300

avg = None
es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))

# Setup the camera
camera = PiCamera()
camera.resolution = (resX, resY)
camera.framerate = 30

# Use this as our output
rawCapture = PiRGBArray(camera, size=(resX, resY))

time.sleep(5)

rawCapture.truncate(0)

for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = f.array

    # 调整帧尺寸，转换为灰阶图像并进行模糊
    #frame = cv2.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # 如果平均帧是None，初始化它
    if avg is None:
        print "[INFO] starting background model..."
        avg = gray.copy().astype("float")
        rawCapture.truncate(0)
        continue
 
    # accumulate the weighted average between the current frame and
    # previous frames, then compute the difference between the current
    # frame and running average

    cv2.accumulateWeighted(gray, avg, 0.5)
    # 对于每个从背景之后读取的帧都会计算其与背景之间的差异，并得到一个差分图（different map）。  
    # 还需要应用阈值来得到一幅黑白图像，并通过下面代码来膨胀（dilate）图像，从而对孔（hole）和缺陷（imperfection）进行归一化处理  
    diff = cv2.absdiff(gray, cv2.convertScaleAbs(avg))  

    diff = cv2.threshold(diff, 5, 255, cv2.THRESH_BINARY)[1] # 二值化阈值处理  
    diff = cv2.dilate(diff, None, iterations=2) # 形态学膨胀  
    # 显示矩形框
    (contours, _) = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 该函数计算一幅图像中目标的轮廓  
    for c in contours:  
        if cv2.contourArea(c) < 5000: # 对于矩形区域，只显示大于给定阈值的轮廓，所以一些微小的变化不会显示。对于光照不变和噪声低的摄像头可不设定轮廓最小尺寸的阈值  
            continue  
        (x, y, w, h) = cv2.boundingRect(c) # 该函数计算矩形的边界框  
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        print"x=%d y=%d w=%d h=%d " %(x,y,w,h)
  
    cv2.imshow('contours', frame)  
    cv2.imshow('dis', diff)
	
    key = cv2.waitKey(1) & 0xFF  
    # 按'q'健退出循环  
    if key == ord('q'):  
        break
		
    rawCapture.truncate(0)
	
# When everything done, release the capture  
camera.release()
cv2.destroyAllWindows()
