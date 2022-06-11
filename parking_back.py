#!/usr/bin/python
# -*- coding: utf-8 -*-

from driver import driver
import time
import cv2
import numpy as np
import math
import os
from smart_car import flag_show_img, width, height, sm, st,\
    intrinsicMat, distortionCoe, birdView, perspective_transform,\
    line, lines_order, constraint,distance


# src_pts = np.float32([[240,240],[490,240],[630,390],[40,390]])/2
# dst_pts = np.float32([[160,40],[480,40],[480,440],[160,440]])

# src_pts = np.float32([[209,276],[468,274],[524,304],[154,321]])/2
# dst_pts = np.float32([[125,90],[515,90],[515,464],[125,464]])/2

src_pts = np.float32([[279,109],[375,108],[402,160],[233,161]])/2
dst_pts = np.float32([[130,70],[190,70],[190,150],[130,150]])

def go_double_lines(image):
    '''

    :param image:
    :return: sm;st
    '''
    global flag_show_img, sm, st, last_frame_line

    corr_img = cv2.undistort(image, intrinsicMat, distortionCoe, None, intrinsicMat)
    cv2.imshow('1',corr_img)
    img = cv2.resize(corr_img, (320, 240), interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # gray = cv2.GaussianBlur(gray, (3, 3), 0)
    # gray = cv2.medianBlur(gray, 3)
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    can = cv2.Canny(gray, 100, 400)
    add = can + binary

    transform_matrix = perspective_transform(src_pts, dst_pts)
    warped_image = add

    warped_image = birdView(warped_image, transform_matrix['M'])
    cv2.imshow('warped', warped_image)
    cv2.waitKey(20)
    warped_image = 255 - warped_image
    # warped_image = cv2.dilate(warped_image, np.ones((3, 3), np.uint8))
    warped_image = cv2.erode(warped_image, np.ones((3, 3), np.uint8))

    lines_raw = cv2.HoughLinesP(warped_image, 1, np.pi / 180, 100, 100, 100, 50)
    # cv2.imshow("bird", warped_image)
    # print(lines.shape)

    if lines_raw is not None:
        lines, angle_d = lines_order(lines_raw)
        lines = lines.astype(np.int32)
        n = lines.shape[0]

        for x in lines:
            if flag_show_img == 0:
                break
            cv2.line(warped_image, (x[0], x[1]), (x[2], x[3]), (255, 0, 255), 4)
            cv2.line(warped_image, (x[0], x[1]), (x[2], x[3]), (0, 0, 255), 1)
        flag_n = 0
        offset = 90

        if n == 1:
            c1 = float(lines[0, 2] - lines[0, 0]) / float(lines[0, 3] - lines[0, 1])
            bottomx = lines[0, 0] + float(240 - lines[0, 1]) * (c1 + 0.0001)
            print("bottom x :", bottomx)
            if bottomx < 160 and last_frame_line > -1:
                last_frame_line = 1
            elif bottomx > 160 and last_frame_line < 1:
                last_frame_line = -1
            if last_frame_line == 1:
                print('left line')
                if flag_show_img:
                    x_1 = lines[0, 0] + offset
                    x_2 = lines[0, 2] + offset
                    y_1 = lines[0, 1]
                    y_2 = lines[0, 3]
                    cv2.line(warped_image, (x_1, y_1), (x_2, y_2), (255, 0, 255), 6)
                    cv2.line(warped_image, (x_1, y_1), (x_2, y_2), (0, 0, 255), 2)

                d_x = (lines[0, 0] + lines[0, 2]) / 2.0 + offset - 160

                angle = angle_d[0, 0]
            elif last_frame_line == -1:
                if flag_show_img:
                    x_1 = lines[0, 0] - offset
                    x_2 = lines[0, 2] - offset
                    y_1 = lines[0, 1]
                    y_2 = lines[0, 3]
                    cv2.line(warped_image, (x_1, y_1), (x_2, y_2), (255, 0, 255), 6)
                    cv2.line(warped_image, (x_1, y_1), (x_2, y_2), (0, 0, 255), 2)
                d_x = (lines[0, 0] + lines[0, 2]) / 2.0 - offset - 160
                angle = angle_d[0, 0]
            flag_n = 1
        if n == 2:
            last_frame_line = 0
            x_1 = int((lines[0, 0] + lines[1, 0]) / 2.0)
            y_1 = int((lines[0, 1] + lines[1, 1]) / 2.0)
            x_2 = int((lines[0, 2] + lines[1, 2]) / 2.0)
            y_2 = int((lines[0, 3] + lines[1, 3]) / 2.0)
            if distance([x_1, y_1], [x_2, y_2]) < 50:
                x_1 = int((lines[0, 0] + lines[1, 2]) / 2.0)
                y_1 = int((lines[0, 1] + lines[1, 3]) / 2.0)
                x_2 = int((lines[0, 2] + lines[1, 0]) / 2.0)
                y_2 = int((lines[0, 3] + lines[1, 1]) / 2.0)
            if flag_show_img:
                cv2.line(warped_image, (x_1, y_1), (x_2, y_2), (255, 0, 255), 6)
                cv2.line(warped_image, (x_1, y_1), (x_2, y_2), (0, 0, 255), 2)
            d_x = (lines[0, 0] + lines[1, 0] + lines[0, 2] + lines[1, 2]) / 4.0 - 160
            angle = (angle_d[0, 0] + angle_d[1, 0]) / 2.0
            flag_n = 1

        if flag_n:
            k1 = -0.035
            k2 = 17
            print("d_x", k1 * d_x, "angle", k2 * angle)
            # steering_angle = constraint(-20,20,k1*d_x +k2*angle) -1.5
            st = constraint(-1, 1, (k1 * d_x + k2 * angle)/20)
            sm = constraint(-1, 1, 1.0 - abs(angle)/np.pi)
            print(st)

    if flag_show_img:
        cv2.imshow("bird_", warped_image)
        cv2.waitKey(10)

    return sm, st,warped_image

def filter_blue_light(image):
    img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_blue_light = np.array([85,100,90])
    upper_blue_light = np.array([98,255,255])
    mask = cv2.inRange(img,lower_blue_light,upper_blue_light)
    light_blue = cv2.bitwise_and(img,img,mask = mask)
    return light_blue

def filter_blue_dark(image):
    img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_blue_dark = np.array([100,80,70])
    upper_blue_dark = np.array([130,255,255])
    mask = cv2.inRange(img,lower_blue_dark,upper_blue_dark)
    dark_blue = cv2.bitwise_and(img,img,mask = mask)
    return dark_blue

def filter_yellow(image):
    img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([35,110,110])
    upper_yellow = np.array([60,255,255])
    mask = cv2.inRange(img,lower_yellow,upper_yellow)
    yellow = cv2.bitwise_and(img,img,mask = mask)
    print(yellow.shape)
    return yellow

def filter_red(image):
    img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_red = np.array([150,100,50])
    upper_red = np.array([175,255,255])
    mask = cv2.inRange(img,lower_red,upper_red)
    red = cv2.bitwise_and(img,img,mask = mask)

    return red

def get_parking_space(image, parking_space):
    '''
    :param image:
    :param parking_space:
    :return:
    '''
    corr_img = cv2.undistort(image, intrinsicMat, distortionCoe, None, intrinsicMat)
    img = cv2.resize(corr_img, (320, 240), interpolation=cv2.INTER_CUBIC)
    if parking_space == 1:
        img = filter_blue_dark(img)
    elif parking_space == 2:
        img = filter_red(img)
    elif parking_space == 3:
        img = filter_yellow(img)
    elif parking_space == 4:
        img = filter_blue_light(img)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # gray = cv2.GaussianBlur(gray, (3, 3), 0)
    # gray = cv2.medianBlur(gray, 3)
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    can = cv2.Canny(gray, 100, 400)
    add = can + binary
    return img


def parking_back(image,parking_space):
    '''

    :param image:
    :return: sm;st
    '''

    global flag_show_img, sm, st

    corr_img = cv2.undistort(image, intrinsicMat, distortionCoe, None, intrinsicMat)
    #cv2.imshow('1',corr_img)
    img = cv2.resize(corr_img, (320, 240), interpolation=cv2.INTER_CUBIC)
    if parking_space == 1:
        img = filter_blue_dark(img)
    elif parking_space == 2:
        img = filter_red(img)
    elif parking_space == 3:
        img = filter_yellow(img)
    elif parking_space == 4:
        img = filter_blue_light(img)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # gray = cv2.GaussianBlur(gray, (3, 3), 0)
    # gray = cv2.medianBlur(gray, 3)
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    can = cv2.Canny(gray, 100, 400)
    add = can + binary

    transform_matrix = perspective_transform(src_pts, dst_pts)
    warped_image = add

    warped_image = birdView(warped_image, transform_matrix['M'])
    cv2.imshow('warped', warped_image)
    cv2.waitKey(20)
    warped_image = 255 - warped_image
    # warped_image = cv2.dilate(warped_image, np.ones((3, 3), np.uint8))
    warped_image = cv2.erode(warped_image, np.ones((3, 3), np.uint8))

    lines_raw = cv2.HoughLinesP(warped_image, 1, np.pi / 180, 100, 100, 100, 50)


    if flag_show_img:
        cv2.imshow("bird_", warped_image)
        cv2.waitKey(10)

    return sm, st,warped_image

def get_bird_image(image):

    corr_img = cv2.undistort(image, intrinsicMat, distortionCoe, None, intrinsicMat)
    cv2.imshow('corr_img',corr_img)
    img = cv2.resize(corr_img, (320, 240), interpolation=cv2.INTER_CUBIC)
    transform_matrix = perspective_transform(src_pts, dst_pts)
    warped_image = birdView(img, transform_matrix['M'])

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    can = cv2.Canny(gray, 100, 400)
    add = can + binary
    return warped_image

def smart_car():
    print("==========piCar Client Start==========")
    print("=============stop mode================")
    print("Please select a parking space(1-4)")
    parking_space = input()
    while parking_space != '1' and parking_space != '2' and parking_space != '3' and parking_space != '4':
        print("This parking space does not exit.")
        print("please select again.")
        parking_space = input()
    print("parking space:", parking_space)
    d = driver()
    d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="stop")
    d.setStatus(mode="speed")

    while True:
        t1 = time.time()

        cap = cv2.VideoCapture(0)
        cap2 = cv2.VideoCapture(1)
        _, frame = cap.read()
        _, frame2 = cap2.read()
        cv2.imshow("image1", cv2.flip(frame, 1))
        cv2.imshow("image2", cv2.flip(frame2, -1))
        cv2.waitKey(3)

        sm, st = parking_back(frame2, parking_space)
        d.setStatus(motor=sm, servo=st)
        print("Motor: %0.2f, Servo: %0.2f" % (sm, st))
        # time.sleep(1)
        # # d.heartBeat()
        # d.getStatus(sensor=0, mode=0)
        # time.sleep(1)

        t2 = time.time()
        print("time:", t2-t1)

    d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="stop")
    d.close()
    del d
    print("==========piCar Client Fin==========")
    return 0

def parking(parking_space):
    while parking_space != '1' and parking_space != '2' and parking_space != '3' and parking_space != '4':
        print("This parking space does not exit.")
        print("please select again.")
        parking_space = input()
    print("parking space:", parking_space)
    d = driver()
    d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="stop")
    d.setStatus(mode="speed")

    while True:
        t1 = time.time()

        cap = cv2.VideoCapture(0)
        cap2 = cv2.VideoCapture(1)
        _, frame = cap.read()
        _, frame2 = cap2.read()
        cv2.imshow("image1", cv2.flip(frame, 1))
        cv2.imshow("image2", cv2.flip(frame2, -1))
        cv2.waitKey(3)

        sm, st = parking_back(frame2, parking_space)
        d.setStatus(motor=sm, servo=st)
        print("Motor: %0.2f, Servo: %0.2f" % (sm, st))
        # time.sleep(1)
        # # d.heartBeat()
        # d.getStatus(sensor=0, mode=0)
        # time.sleep(1)

        t2 = time.time()
        print("time:", t2-t1)

    d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="stop")
    d.close()
    del d
    print("==========piCar Client Fin==========")
    return 0


if __name__ == '__main__':
    # smart_car()
    img = cv2.imread('./stop/back/009.jpg')
    cv2.imshow("raw",img)
    img = cv2.undistort(img, intrinsicMat, distortionCoe, None, intrinsicMat)

    cv2.imshow('corr_img',img)
    t1 = time.time()
    img = cv2.resize(img, (320, 240), interpolation=cv2.INTER_CUBIC)
    #cv2.imshow('resize', img)

    transform_matrix = perspective_transform(src_pts, dst_pts)
    img = birdView(img, transform_matrix['M'])
    cv2.imshow('bird',img)
    img_yellow = filter_yellow(img)
    img_red = filter_red(img)
    img_light_blue = filter_blue_light(img)
    img_dark_blue = filter_blue_dark(img)
    t2 = time.time()
    print(t2-t1)
    cv2.imshow('yellow', img_yellow)
    cv2.imshow('red', img_red)
    cv2.imshow("light_blue", img_light_blue)
    cv2.imshow("dark_blue", img_dark_blue)

    # gray = cv2.cvtColor(img_light_blue, cv2.COLOR_RGB2GRAY)
    # ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # can = cv2.Canny(gray, 100, 400)
    # cv2.imshow("binary",binary)
    # cv2.imshow("can", can)
    cv2.waitKey(100000)


