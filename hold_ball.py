#!/usr/bin/env python
#coding=utf-8

'''
Brief : track deer for robot.  Ver : V1.0
Author : Sanson   Date : 2019/01/22
'''
from picamera.array import PiRGBArray
# 捕获’brg’格式的数据库
from picamera import PiCamera
from functools import partial
# functools模块用于高级函数：作用于或返回其他函数的函数，一般来说，任何可调用对象都可以作为这个模块的用途来处理。
# partial 函数的功能就是：把一个函数的某些参数给固定住，返回一个新的函数。


import cv2
import os
import time
import threading    
# 多线程库

import numpy as np
import multiprocessing as mp
# 多进程库

from socket import *
# 用于通讯的库

import RobotApi as api
import sys

# 分辨率
resX = 450
resY = 250

# 定义颜色范围数组
lower_red = np.array([160, 40, 40])
upper_red = np.array([179, 255, 255])
lower_green = np.array([30, 100, 100])
upper_green = np.array([80, 255, 255])
lower_blue = np.array([100, 100, 100])
upper_blue = np.array([125, 255, 255])
lower_yellow = np.array([20, 30, 30])
upper_yellow = np.array([70, 255, 255])
lower_purple = np.array([125, 50, 50])
upper_purple = np.array([150, 255, 255])

center_x = 0
center_y = 0
radius = 0
hold_flag = 0
release_flag = 0

# 相机设定
camera = PiCamera()
camera.resolution = (resX, resY)
# 分辨率
camera.framerate = 30
# 帧率

#使用此作为输出
rawCapture = PiRGBArray(camera, size=(resX, resY))

HOST = '127.0.0.1'
PORT = 20001
ADDR = (HOST, PORT) 
udp_client = socket(AF_INET, SOCK_DGRAM)
# 进程间的通讯，面向网络套字节AF_INET
# Python只支持AF_INET、AF_UNIX、AF_NETLINK和AF_TIPC家族use_video_port

class RobotMotion:
    def __init__(self):

	    pass
		
    def holding_deer(self):    
        #data = str("{\"cmd\":\"set\",\"type\":\"led\",\"para\":{\"type\":\"camera\",\"mode\":\"on\",\"color\":\"red\"}}")
        data = str("{\"cmd\":\"action\",\"type\":\"start\",\"para\":{\"name\":\"hold_deer_small\",\"repeat\":1 }}")
        udp_client.sendto(data ,ADDR)
        time.sleep(8)
    def forward_step(self,num): 
	    data_list = []
        data_list.append("{\"cmd\":\"action\",\"type\":\"start\",\"para\":{\"name\":\"step_forward\",\"repeat\":")
	    data_list.append(str(num))
	    data_list.append("}}")
	    data = ''.join(data_list)
        udp_client.sendto(data ,ADDR)
        time.sleep(2*num)
    def backward_step(self,num):
	    data_list = []
        data_list.append("{\"cmd\":\"action\",\"type\":\"start\",\"para\":{\"name\":\"step_backward\",\"repeat\":")
	    data_list.append(str(num))
	    data_list.append("}}")
	    data = ''.join(data_list)
        udp_client.sendto(data ,ADDR)
        time.sleep(2*num)
    def left_step(self,num):
	    data_list = []
        data_list.append("{\"cmd\":\"action\",\"type\":\"start\",\"para\":{\"name\":\"step_left\",\"repeat\":")
	    data_list.append(str(num))
	    data_list.append("}}")
	    data = ''.join(data_list)
        udp_client.sendto(data ,ADDR)
        time.sleep(num)
    def right_step(self,num):
	    data_list = []
        data_list.append("{\"cmd\":\"action\",\"type\":\"start\",\"para\":{\"name\":\"step_right\",\"repeat\":")
	    data_list.append(str(num))
	    data_list.append("}}")
	    data = ''.join(data_list)
        udp_client.sendto(data ,ADDR)
        time.sleep(num)
    def turn_left_step(self,num):
	    data_list = []
        data_list.append("{\"cmd\":\"action\",\"type\":\"start\",\"para\":{\"name\":\"step_turn_left\",\"repeat\":")
	    data_list.append(str(num))
	    data_list.append("}}")
	    data = ''.join(data_list)
        udp_client.sendto(data ,ADDR)
        time.sleep(num)
    def turn_right_step(self,num):
	    data_list = []
        data_list.append("{\"cmd\":\"action\",\"type\":\"start\",\"para\":{\"name\":\"step_turn_right\",\"repeat\":")
	    data_list.append(str(num))
	    data_list.append("}}")
	        data = ''.join(data_list)
        udp_client.sendto(data ,ADDR)
        time.sleep(num)
    def reset(self,num):
	    data_list = []
        data_list.append("{\"cmd\":\"action\",\"type\":\"start\",\"para\":{\"name\":\"reset\",\"repeat\":")
	    data_list.append(str(num))
	    data_list.append("}}")
	    data = ''.join(data_list)
        udp_client.sendto(data ,ADDR)
        time.sleep(0.5)

def get_circles(img):
    x = 0
    y = 0
    z = 0
    blurred = cv2.GaussianBlur(img, (11, 11), 0)
    # 高斯滤波
    # 参数：
    # src: 原图像
	# dst: 目标图像
	# ksize: 高斯核的大小；(width, height)；两者都是正奇数；如果设为0，则可以根据sigma得到；
	# sigmaX: X方向的高斯核标准差；
	# sigmaY: Y方向的高斯核标准差；
	# 	如果sigmaY设为0，则与sigmaX相等；
	# 	如果两者都为0，则可以根据ksize来计算得到；
	# （推荐指定ksize，sigmaX，sigmaY）
	# borderType: pixel extrapolation method
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # 色彩空间转化函数，将目标blurred格式转换为RGB转到HSV

    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    # 第一个参数：hsv指的是原图
    # 第二个参数：lower_purple指的是图像中低于这个lower_purple的值，图像值变为0
    # 第三个参数：upper_purple指的是图像中高于这个upper_purple的值，图像值变为0
    # 而在lower_red～upper_red之间的值变成255
    mask = cv2.erode(mask, None, iterations=2)
    # cv2.erode腐蚀函数
    # kernel:核的大小,none为默认大小
    # iteration:膨胀和腐蚀次数；叠代iteration的值越高，模糊程度(腐蚀程度)就越高 呈正相关关系
    mask = cv2.dilate(mask, None, iterations=2)
    # 膨胀函数与腐蚀函数相似
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    # cv2.findContours轮廓检测
    # cv2.RETR_EXTERNAL表示只检测外轮廓
    # cv2.CHAIN_APPROX_SIMPLE压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需4个点来保存轮廓信息
    # -2不懂是什么鬼
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        # max函数返回最大值
        # cv2.contourArea轮廓面积
        # 意思是返回一个最大的轮廓，其他不要
        ((x, y), z) = cv2.minEnclosingCircle(c)
        # cv2.minEnclosingCircle：可以帮我们找到一个对象的外切圆。它是所有能够包括对象的圆中面积最小的一个
        
    return int(x),int(y),int(z),img

def draw_frame(img,x,y,z):
    # 函数的参数优点：可以随时变换，不是规定死的
    if(z > 15):
        cv2.circle(img,(x,y),z,(0,255,0),5)
        # cv2.circle(img, center, radius, color[, thickness=None[, lineType=None[, shift=None]]])
        # 作用
        # 根据给定的圆心和半径等画圆
        # 参数说明
        # img：输入的图片data
        # center：圆心位置
        # radius：圆的半径
        # color：圆的颜色
        # thickness：圆形轮廓的粗细（如果为正）。负厚度表示要绘制实心圆。
        # lineType： 圆边界的类型。
        # shift：中心坐标和半径值中的小数位数
        print("circle_center is : ",x,y)
        # 打印出圆心
        print("radius is : ",z)
        # 打印半径
    cv2.imshow('Color_tracking', img)
    # 显示画图圆后的图

def     (x,y,z):
    global hold_flag
    # global可以在函数体中修改全局变量中已经赋值的变量
    global release_flag
    if z > 20 :
	if(x < 150):
            print"ok left"
            my_robot.left_step(1)
            my_robot.reset(1)
	if(x > 300):
            print"ok right"
            my_robot.right_step(1)
            my_robot.reset(1)
	if x > 200 and x < 260:
            if z > 100 :
                my_robot.holding_deer()
                my_robot.forward_step(2)
                time.sleep(5)
                my_robot.reset(1)
                release_flag = 1

def camera_thread():
    global center_x,center_y,radius
    global release_flag
    print "camera_thread run."

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        x,y,z,l = get_circles(image)
        center_x = x
        center_y = y
        radius = z
        draw_frame(l,x,y,z)
        rawCapture.truncate(0)
        key = cv2.waitKey(1) & 0xFF  
        # 按'q'健退出循环
        if key == ord('q'):
            break
        if release_flag == 1 :
            break
    # When everything done, release the capture
    #camera.release()
    cv2.destroyAllWindows()

def track_thread():
    global center_x,center_y,radius
    print "track_thread run."
    while True :
        walk_track(center_x,center_y,radius)
        time.sleep(0.1)

if __name__ == '__main__':
    my_robot = RobotMotion()
    my_robot.reset(1)
    threads = []
    t1 = threading.Thread(target=camera_thread,args=()) 
    threads.append(t1) 
    t2 = threading.Thread(target=track_thread,args=())                             
    threads.append(t2)                                                                                                                       

    for t in threads:
        t.setDaemon(True) 
        t.start()
    for t in threads:
        t.join()
    print "exit all task."


