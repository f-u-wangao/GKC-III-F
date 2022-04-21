#!/usr/bin/python
# -*- coding: utf-8 -*-

from driver import driver
import time
import cv2
import numpy as np
import argparse

from smart_car import sm,st,intrinsicMat, distortionCoe, birdView, perspective_transform,\
    line, lines_order, constraint,distance

global parking_back_stage
parking_back_stage = 0

# src_pts = np.float32([[279,109],[375,108],[402,160],[233,161]])/2
# dst_pts = np.float32([[130,70],[190,70],[190,150],[130,150]])
# M = cv2.getPerspectiveTransform(src_pts,dst_pts)

#### back
# src_pts = np.float32([[292,166],[377,165],[406,206],[267,207]])/2
# dst_pts = np.float32([[130,40],[190,40],[190,140],[130,140]])
# M = cv2.getPerspectiveTransform(src_pts,dst_pts)

# front
src_pts = np.float32([[293,239],[414,238],[460,277],[250,278]])/2
dst_pts = np.float32([[130,40],[190,40],[190,140],[130,140]])
M = cv2.getPerspectiveTransform(src_pts,dst_pts)

'''========================parameters=================================='''
parser = argparse.ArgumentParser(description='parking_parameters')
parser.add_argument('--parking_space', type=int,default = 0,choices = [0,1,2,3,4], help='parking_space')
parser.add_argument('--k1',type = float,default = 0.5,help = 'center_error control rate')
parser.add_argument('--k2',type = float,default = 0.5,help = 'angle control rate')
parser.add_argument('--done_dist',type = float,default = 220,help = 'parking done distance')
parser.add_argument('--k3',type = float,default = 0.1,help = 'over rate')
parser.add_argument('--show',type = bool,default = True, help = 'show images or not')
'''======================================================================='''


def filter_blue_light(image):
    img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_blue_light = np.array([85,100,90])
    upper_blue_light = np.array([98,255,255])
    mask = cv2.inRange(img,lower_blue_light,upper_blue_light)
    light_blue = cv2.bitwise_and(img,img,mask = mask)
    light_blue = cv2.cvtColor(light_blue, cv2.COLOR_HSV2BGR)
    return light_blue

def filter_blue_dark(image):
    img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_blue_dark = np.array([100, 80, 70])
    upper_blue_dark = np.array([130,255,255])
    mask = cv2.inRange(img,lower_blue_dark,upper_blue_dark)
    dark_blue = cv2.bitwise_and(img,img,mask = mask)
    dark_blue = cv2.cvtColor(dark_blue, cv2.COLOR_HSV2BGR)
    return dark_blue

def filter_yellow(image):
    img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([35,110,110])
    upper_yellow = np.array([60,255,255])
    mask = cv2.inRange(img,lower_yellow,upper_yellow)
    yellow = cv2.bitwise_and(img,img,mask = mask)
    yellow = cv2.cvtColor(yellow, cv2.COLOR_HSV2BGR)
    return yellow

def filter_red(image):
    img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_red = np.array([150,100,50])
    upper_red = np.array([175,255,255])
    mask = cv2.inRange(img,lower_red,upper_red)
    red = cv2.bitwise_and(img,img,mask = mask)
    red = cv2.cvtColor(red,cv2.COLOR_HSV2BGR)
    return red

def filter_white(image):
    img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_white = np.array([0,0,230])
    upper_white = np.array([350,350,350])
    mask = cv2.inRange(img,lower_white,upper_white)
    white = cv2.bitwise_and(img,img,mask = mask)
    white = cv2.cvtColor(white,cv2.COLOR_HSV2BGR)
    return white

def parking_front(image,args):
    '''
    :param image: raw image
    :param args:
    :return:sm, st
    '''
    global parking_back_stage,sm,st
    corr_img = cv2.undistort(image, intrinsicMat, distortionCoe, None, intrinsicMat)
    img = cv2.resize(corr_img, (320, 240), interpolation=cv2.INTER_CUBIC)
    img = birdView(img, M)
    # cv2.imshow('bird',img)

    if args.parking_space == 1:
        img = filter_blue_dark(img)
    elif args.parking_space == 2:
        img = filter_red(img)
    elif args.parking_space == 3:
        img = filter_yellow(img)
    elif args.parking_space == 4:
        img = filter_blue_light(img)
    elif args.parking_space == 0:
        img = filter_white(img)

    # cv2.imshow('filter', img)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.erode(gray, np.ones((3, 3), np.uint8))
    contours,hierarchy = cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    area = []
    for c in contours:
        area.append(cv2.contourArea(c))
    if area:
        max_idx = np.argmax(np.array(area))
        max = contours[max_idx]
        rect = cv2.minAreaRect(max)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        cv2.drawContours(gray,[box],0,(255,255,255),1)
        if args.show:
            cv2.imshow("parking_space",gray)
        center = np.mean(box,axis = 0)
        # print(center)
        center_error = -1*np.arctan2(center[0]-160,240-center[1])
        box = box[np.lexsort(box.T)]
        print(box)
        angle_d_0 = line(box[0,0],box[0,1],box[2,0],box[2,1])
        angle_error = angle_d_0[0]
        if box[2,1] == box[3,1]:
            angle_d_1 = line(box[0, 0], box[0, 1], box[2, 0], box[2, 1])
            if abs(angle_d_0[0]) < abs(angle_d_1[0]):
                angle_error = angle_d_0[0]
            else:
                angle_error = angle_d_1[0]

        dist = distance(center,[160,240])
        print("center_error",center_error)
        print("angle_error",angle_error)
        print("dist",dist)

        if parking_back_stage == 0 :
            if abs(center_error) < 0.1 and abs(angle_error)<0.1:
                parking_back_stage = 2
            else:
                parking_back_stage = 1
            first_center_error = center_error
        if parking_back_stage == 1:
            st = args.k1 * center_error +args.k2*angle_error
            if abs(center_error) < abs(first_center_error) *args.k3 and center_error * first_center_error < 0:
                parking_back_stage = 2
        if parking_back_stage == 2:
            st = args.k1 * center_error + args.k2 * angle_error
            if center[1] > args.done_dist:
                st = 0
                parking_back_stage = 3
    return sm,st


def smart_car():
    print("==========piCar Client Start==========")
    print("=============stop mode================")
    global parking_back_stage
    args = parser.parse_args()
    d = driver()
    d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="stop")
    d.setStatus(mode="speed")
    time_c = 0
    while True:
        t1 = time.time()
        cap = cv2.VideoCapture(0)
        cap2 = cv2.VideoCapture(1)
        _, frame = cap.read()
        _, frame2 = cap2.read()
        cv2.imshow("image1", cv2.flip(frame, 1))
        cv2.imshow("image2", cv2.flip(frame2, -1))
        cv2.waitKey(3)
        sm, st = parking_front(frame2, args)
        d.setStatus(motor=sm, servo=st)
        print("Motor: %0.2f, Servo: %0.2f" % (sm, st))
        t2 = time.time()
        if time_c + t2 - t1 < 0.5:
            time_c += t2 - t1
        else:
            d.setStatus(motor=sm * 0.1, servo=st)
            print("Motor: %0.2f, Servo: %0.2f" % (sm, st))
            print("time:", time_c + t2 - t1)
            time_c = 0
        if parking_back_stage == 3:
            print("parking done")
            break
    d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="stop")
    d.close()
    del d
    print("==========piCar Client Fin==========")
    return 0

if __name__ == '__main__':
    smart_car()
    # # img = cv2.imread('./stop/back/008.jpg')
    # img = cv2.imread('./wwh/front/002.jpg')
    # # img = cv2.imread('./wwh/back/003.jpg')
    # cv2.imshow("raw",img)
    # args = parser.parse_args()
    # parking_front(img,args)
    # cv2.waitKey(100000)


