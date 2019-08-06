#  *_* coding:utf8 *_*
# pip install baidu-aip
import os
import time

import cv2
from aip import AipBodyAnalysis
from threading import Thread


""" 你的 APPID AK SK """
APP_ID = '16947698'
API_KEY = 'fN9yStlTEv1zkWoMDMQU7YKT'
SECRET_KEY = 'fqk4FfDRZp7fjk1ngcTeeaKtgWZxFh6H'

gesture_client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)


gesture_contrast = {
    "Ok": "1",
    "Thumb_up": "4",
    "Thumb_down": "5",
    "Insult": "2",
    "Six": "3",
    "Five": "6",
    "Fist": "7",
    "Honour": "8",
}


# 0指的是摄像头的编号。如果你电脑上有两个摄像头的话，访问第2个摄像头就可以传入1。
capture = cv2.VideoCapture(0)
def camera():

    while True:
        ret, frame = capture.read()
        # cv2.imshow(窗口名称, 窗口显示的图像)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

Thread(target=camera).start()


def gesture_recognition():
    ret, frame = capture.read()

    image = cv2.imencode(".png", frame)[1].tobytes()

    result = gesture_client.gesture(image)


    gesture=result['result']

    if gesture :
       gesture=gesture[0]['classname']
    else:
        print('未获取到手势指令')
        gesture='None'
    #gesture=result['result'][0]['classname']

    return gesture_contrast[gesture] if gesture in gesture_contrast else "指令未收录"
    #return gesture

# if __name__ == '__main__':
#
#     while True:
#         print(gesture_recognition())
#         print('=======================')



