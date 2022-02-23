import cv2
import numpy as np
import matplotlib.pyplot as plt  # plt 用于显示图片

mtx = np.array([[5.01084713e+03, 0.00000000e+00, 3.15478990e+02],
       [0.00000000e+00, 8.85802435e+02, 2.28687992e+02],
       [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

dist = np.array([[
    1.13773850e+02,
    -6.45391282e+03,
    2.76185119e+00,
    7.10477644e-02,
    1.27737000e+05,
]])


def undistortion(image, camera_matrix, dist_coeff):
    undistortion_image = cv2.undistort(image, camera_matrix, dist_coeff)

    return undistortion_image

img_path = "./back/018.jpg"
img = cv2.imread(img_path)
cv2.imshow("original", img)
undistortion_img = undistortion(img, mtx, dist)
cv2.imshow("undistortion", undistortion_img)
cv2.waitKey(0)