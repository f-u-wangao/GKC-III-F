import cv2

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

while True:
    _, frame = cap.read()
    _, frame2 = cap2.read()
    cv2.imshow("image1", cv2.flip(frame, 1))
    cv2.imshow("image2", cv2.flip(frame2, -1))
    cv2.waitKey(3)
