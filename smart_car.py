#!/usr/bin/python
# -*- coding: utf-8 -*-

from driver import driver
import time
import cv2


def go_double_lines(image):
    sm = 0
    st = 0
    return sm, st

def run_picar():
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
        time.sleep(1)
        # d.heartBeat()
        d.getStatus(sensor=0, mode=0)
        time.sleep(1)

        t2 = time.time()
        print("time:", t2-t1)

    d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="stop")
    d.close()
    del d
    print("==========piCar Client Fin==========")
    return 0


if __name__ == '__main__':
    run_picar()

