'''
To save the image, you just need to press the "space" botton
To exit the program, you need to press the "esc" button
The images will be saved in two directories: front and back
Name of images will follow the ascending order
'''
import cv2
import os


def findProperFileNumber(folder):
    all_files = os.listdir(folder)
    max_count = 1
    for file in all_files:
        ext = os.path.splitext(file)  # get the name and suffix of each file
        if ext[1] == '.jpg' and int(ext[0]) >= max_count:
            max_count = int(ext[0]) + 1
    return max_count


def takePicture():
    # define the folder to save the pictures
    SAVE_FOLDER1 = "./pic/back"
    SAVE_FOLDER2 = "./pic/front"

    # get video streams
    cap1 = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(1)

    # count proper file number in the folder or directly define index
    # index1 = index2 = 1;
    index1 = findProperFileNumber(SAVE_FOLDER1)
    index2 = findProperFileNumber(SAVE_FOLDER2)

    # get return-successfully read or not, frame
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    # transform frames
    frame1 = cv2.flip(frame1, 1)
    frame2 = cv2.flip(frame2, -1)

    # show the images on the screen
    cv2.imshow("image1", frame1)
    cv2.imshow("image2", frame2)

    # capture the images, then save
    save_path1 = "{}/{:>03d}.jpg".format(SAVE_FOLDER1, index1)
    save_path2 = "{}/{:>03d}.jpg".format(SAVE_FOLDER2, index2)
    cv2.imwrite(save_path1, frame1)
    cv2.imwrite(save_path2, frame2)
    print("Caught front {:>03d} and back {:>03d}").format(index1, index2)


if __name__ == '__main__':
    # define the folder to save the pictures
    SAVE_FOLDER1 = "./pic/back"
    SAVE_FOLDER2 = "./pic/front"

    # get video streams
    cap1 = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(1)

    # count proper file number in the folder or directly define index
    # index1 = index2 = 1;
    index1 = findProperFileNumber(SAVE_FOLDER1)
    index2 = findProperFileNumber(SAVE_FOLDER2)

    while True:
        # get return-successfully read or not, frame
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        # transfrom frames
        frame1 = cv2.flip(frame1, 1)
        frame2 = cv2.flip(frame2, -1)

        # show the images on the screen
        cv2.imshow("image1", frame1)
        cv2.imshow("image2", frame2)

        # wait and read the key pressed on the keyboard
        input = cv2.waitKey(10) & 0xFF

        # press space and capture the images, then save
        if input == ord(' '):
            save_path1 = "{}/{:>03d}.jpg".format(SAVE_FOLDER1, index1)
            save_path2 = "{}/{:>03d}.jpg".format(SAVE_FOLDER2, index2)
            cv2.imwrite(save_path1, frame1)
            cv2.imwrite(save_path2, frame2)
            print("Caught front {:>03d} and back {:>03d}").format(
                index1, index2)
            index1 += 1
            index2 += 1

        # press esc and quit the program
        elif input == 27:
            break
