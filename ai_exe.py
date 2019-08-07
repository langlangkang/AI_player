import os
import time

from pygame import mixer
import cv2
from aip import AipBodyAnalysis
from threading import Thread



class ai():
    def __init__(self):
        """ 你的 APPID AK SK """
        APP_ID = '16947698'
        API_KEY = 'fN9yStlTEv1zkWoMDMQU7YKT'
        SECRET_KEY = 'fqk4FfDRZp7fjk1ngcTeeaKtgWZxFh6H'

        self.gesture_client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)

        self.gesture_contrast = {
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
        self.capture = cv2.VideoCapture(0)

        self.music_names = os.listdir('music')  # 列表歌


        self.music_source = []  # 音频播放路劲
        self.current_music_no = 0  # 音乐
        self.volume = 0.2  # 设置播放频道的音量



    def camera(self):

        while True:
            ret, frame = self.capture.read()
            # cv2.imshow(窗口名称, 窗口显示的图像)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break

    def gesture_recognition(self):
        ret, frame = self.capture.read()

        image = cv2.imencode(".png", frame)[1].tobytes()

        result = self.gesture_client.gesture(image)

        gesture = result['result']

        if gesture:
            gesture = gesture[0]['classname']
        else:
            print('未获取到手势指令')
            gesture = 'None'

        return self.gesture_contrast[gesture] if gesture in self.gesture_contrast else "指令未收录"

    def bofang(self):



        while True:
            print('* 1.播放\n'
                  '* 2.暂停\n'
                  '* 3.继续播放\n'
                  '* 4.上一首\n'
                  '* 5.下一首\n'
                  '* 6.音量增加\n'
                  '* 7.音量减少\n'
                  '* 8.退出\n'
                  )

            while True:
                command = self.gesture_recognition()  # 根据手势获取数字，结果为数字
                if command in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    print('接受的指令为：', command)
                    break

            if command == '1':
                mixer.music.load(self.music_source[self.current_music_no])  # Load a music file
                mixer.music.play()

            elif command == '2':
                mixer.music.pause()

            elif command == '3':
                mixer.music.unpause()

            # 4.上一首
            elif command == '4':
                if self.current_music_no > 0:
                    self.current_music_no -= 1
                else:
                    # len(music_source)=4  current_music_no=3   0,1,2,3
                    self.current_music_no = len(self.music_source) - 1

                mixer.music.load(self.music_source[self.current_music_no])
                mixer.music.play()

            # 5.下一首
            elif command == '5':
                # len(music_source)=4  0<3
                if self.current_music_no < len(self.music_source) - 1:
                    self.current_music_no += 1
                else:
                    self.current_music_no = 0  # 0,1,2,3   3-->0

                mixer.music.load(self.music_source[self.current_music_no])
                mixer.music.play()

            elif command == '6':
                if self.volume < 1:
                    self.volume += 0.1
                    mixer.music.set_volume(self.volume)
                else:
                    print('音量已经是最大了')

            elif command == '7':
                if self.volume > 0:
                    self.volume -= 0.1
                    mixer.music.set_volume(self.volume)
                else:
                    print('音量已经是最小了')

            elif command == '8':
                print('退出播放器')
                # kill主进程  getpid得到 进程 id    9绝杀，不管是否死机等，强制关闭
                os.kill(os.getpid(), 9)

            print('正在播放歌曲：', self.music_names[self.current_music_no])
            print('当前音量',self.volume)

    def shezhi(self):

        print(self.music_names)
        for name in self.music_names:
            path = 'music/' + name
            self.music_source.append(path)
        mixer.init()  # 初始化
        mixer.music.set_volume(self.volume)  # 设置播放频道的音量

    def run(self):

        self.shezhi()
        self.bofang()

if __name__ == '__main__':
    path = './music/'

    if not os.path.exists(path):
        os.mkdir(path)
        os.kill(os.getpid(), 9)
    musics = os.listdir(path=path)
    if not musics:
        print('文件夹里面没有东西')
    else:
        for i,music in enumerate(musics):
            if music.endswith('.mp3'):
                print('有{}首歌'.format(i+1))
            else:
                print('music目录下没有歌，请放入歌')

    AI=ai()
    Thread(target=AI.camera).start()
    AI.run()


