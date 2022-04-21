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
    line, lines_order, constraint,distance,go_double_lines,smart_car



if __name__ == '__main__':


     print("============================")
    # print("1------go_double_lines")
    # print("2------stop_back")
    # key = input()
    # if key == 1:
    #     smart_car()
    # image = cv2.imread('./front/020.jpg')
    # cv2.imshow("raw",image)
    # t1 = time.time()
    # sm,st,img = go_double_lines(image)
    # t2 = time.time()
    # print('t',t2-t1)
    # cv2.imshow("ra",img)
    # cv2.waitKey(1000000)
    #print(sm)
    # pathDir = os.listdir('./front')
    # n = 0
    # print(pathDir)
    # for file in pathDir:
    #     img = cv2.imread('./front/' + file)

        # img = get_cleaned_image(img)
        # squares, img = find_squares(img)
        # cv2.drawContours(img, squares, -1, (255, 0, 0), 2)
        # print(squares)
        #
        # display( img,'squares',0)
        # #ch = cv2.waitKey(0)
        # img = image_process_0(img)
        # squares, img = find_squares(img)
        # cv2.drawContours(img, squares, -1, (255, 0, 0), 2)
        #print(img.shape)
        # cv2.imshow('1',img)
        # cv2.waitKey(10)
        # sm,st,img_ = go_double_lines(img)
        # a = format(sm, '.4f')
        # b = format(st, '.4f')
        # # 调用cv.putText()添加文字
        # text = "sm:"+str(a)+";"+"st:"+str(b)
        # AddText = img.copy()
        # cv2.putText(AddText, text, (100, 100), cv2.FONT_HERSHEY_COMPLEX, 1.0, (100, 200, 200), 2)
        #
        # # res = np.hstack([img, AddText])
        #
        # cv2.imwrite('./image/' + str(n) + '.jpg', AddText)
        # cv2.imwrite('./image/' + str(n) + 'a.jpg', img_)
        # n += 1
        # print('Done')


