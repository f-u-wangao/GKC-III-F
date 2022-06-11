from takePic import takePicture
from voiceControl import voiceControl
from rasp_mask_detect.rasp_fast import MaskDetection
from smart_car import smart_car
from parking_back import parking
from multiprocessing import Process, Queue
import keyboard


def voiceControl_packaged(qTakePic, qMaskRec, qRunning):
    while True:
        if keyboard.read_key() == 'v':
            word = voiceControl()
            if word:
                if word == "采集图像":
                    qTakePic.put(1)
                elif word == "停止采集图像":
                    qTakePic.put(0)
                elif word == "口罩识别":
                    qMaskRec.put(1)
                elif word == "停止口罩识别":
                    qMaskRec.put(0)
                elif word == "巡线":
                    qRunning.put(5)
                elif word == "停一号位":
                    qRunning.put(1)
                elif word == "停二号位":
                    qRunning.put(2)
                elif word == "停三号位":
                    qRunning.put(3)
                elif word == "停四号位":
                    qRunning.put(4)
                elif word == "停车":
                    qRunning.put(0)


def takePicture_packaged(qTakePic):
    while True:
        msg = qTakePic.get()
        if msg == 1:
            takePicture()


def maskDetect_packaged(qMaskRec):
    while True:
        msg = qMaskRec.get()
        if msg == 1:
            mask_detection = MaskDetection()
            mask_detection.detect()


def running_packaged(qRunning):
    while True:
        msg = qRunning.get()
        if msg == 5:
            smart_car()
        elif 1 <= msg <= 4:
            parking(msg)


if __name__ == '__main__':

    qTakePic = Queue()
    qMaskRec = Queue()
    qRunning = Queue()

    process_for_voice_control = Process(
        target=voiceControl_packaged, args=(qTakePic, qMaskRec, qRunning))
    process_for_picture_capture = Process(
        target=takePicture_packaged, args=(qTakePic, ))
    process_for_mask_recognition = Process(
        target=maskDetect_packaged, args=(qMaskRec, ))
    process_for_running = Process(
        target=running_packaged, args=(qRunning, ))

    processes = [process_for_voice_control,
                 process_for_picture_capture,
                 process_for_mask_recognition,
                 process_for_running]

    for process in processes:
        process.start()
    for process in processes:
        process.join()
