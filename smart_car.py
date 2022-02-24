#!/usr/bin/python
# -*- coding: utf-8 -*-

from driver import driver
import time
import cv2
import numpy as np
import math
import os


global flag_show_img
flag_show_img = 1
global width, height
width = 640
height = 480
global sm,st
sm = 0
st = 0
global last_frame_line   # 1:left;0:double;-1:right
last_frame_line = 0

intrinsicMat = np.array([[489.3828, 0.8764, 297.5558],
                            [0, 489.8446, 230.0774],
                            [0, 0, 1]])
distortionCoe = np.array([-0.4119,0.1709,0,0.0011, 0.018])

# src_pts = np.float32([[150,277],[490,277],[620,360],[20,360]])
# dst_pts = np.float32([[105,176],[535,176],[535,434],[105,434]])
#
#
#

# intrinsicMat = np.array( [[4.6103702730752963e+02, 0., 3.5418630431854262e+02],
#                           [0.,4.6064503212814503e+02, 2.2282685137757812e+02],
#                           [0., 0., 1.]])
# distortionCoe = np.array([ -4.1165212539677309e-01, 2.2238052367908023e-01,
#                            9.4008882780610356e-04, -7.5876901718103422e-04, -6.2809466175509324e-02 ])

# src_pts = np.float32([[240,240],[490,240],[630,390],[40,390]])/2
# dst_pts = np.float32([[160,40],[480,40],[480,440],[160,440]])

src_pts = np.float32([[209,276],[468,274],[524,304],[154,321]])/2
dst_pts = np.float32([[125,90],[515,90],[515,464],[125,464]])/2
def birdView(img,M):
    '''
    Transform image to birdeye view
    img:binary image
    M:transformation matrix
    return a wraped image
    '''
    img_sz = (img.shape[1],img.shape[0])
    img_warped = cv2.warpPerspective(img,M,img_sz,flags = cv2.INTER_LINEAR)
    return img_warped

def perspective_transform(src_pts,dst_pts):
    '''
    perspective transform
    args:source and destiantion points
    return M and Minv
    '''
    M = cv2.getPerspectiveTransform(src_pts,dst_pts)
    Minv = cv2.getPerspectiveTransform(dst_pts,src_pts)
    return {'M':M,'Minv':Minv}

def line(x1, y1, x2, y2):
    '''
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return: (angle,d)
    '''
    x1 = float(x1)
    x2 = float(x2)
    y1 = float(y1)
    y2 = float(y2)
    if x1 == x2:
        return np.array([0, x1])
    elif y1 == y2:
        return np.array([np.pi/2, y2])
    else:
        k = (y1 - y2) / (x1 - x2)
        k_1 =  (x1 - x2) / (y1 - y2)
        b = y1 - (y1 - y2) * x1 / (x1 - x2)
        angle = np.arctan(k_1)
        d = b / math.sqrt(1 + k * k)
        return np.array([angle, d])

def lines_order(lines):
    '''
    :param lines: HoughLinesP [N,1,4]
    :return:  important lines [n,4]  x1,y1,x2,y2;[n,2]  angle，d
    '''
    N = lines.shape[0]
    line_angle_d = np.zeros((N, 2))
    for i in range(N):
        for x1, y1, x2, y2 in lines[i]:
            line_angle_d[i] = line(x1, y1, x2, y2)
    line_order_0 = line_angle_d[np.lexsort(line_angle_d.T)]
    line_order = lines[np.lexsort(line_angle_d.T), 0, :]
    num = 0
    important_line_point = []
    important_line = []
    for i in range(N - 1):
        # print(abs(line_order_0[i, 1] - line_order_0[i + 2, 1]))
        num += 1
        if abs(line_order_0[i, 1] - line_order_0[i + 1, 1]) > 100 or i == N - 2:
            #if abs(line_order_0[i - int(num / 2), 0]) < np.pi / 3:
                # print(i)
                average = line_order[i - int(num / 2)]
                important_line_point.append(list(average))
                important_line.append(list(line_order_0[i - int(num / 2)]))
                num = 0
    return np.array(important_line_point), np.array(important_line)   # angle_d

def constraint(low,high,value):
    '''
    :param:
    :return:
    '''
    if value < low:
        return low
    if value > high:
        return high
    else:
        return value

def distance(plot_0, plot_1):
    return math.sqrt(
        (plot_0[0] - plot_1[0]) * (plot_0[0] - plot_1[0]) +
        (plot_0[1] - plot_1[1]) * (plot_0[1] - plot_1[1]))



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

    return sm, st

def smart_car():
    print("==========piCar Client Start==========")
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

        sm, st = go_double_lines(frame)
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
    print("============================")
    print("1------go_double_lines")
    print("2------stop_back")
    print("============================")
    key = input()
    if key == 1:
        smart_car()

