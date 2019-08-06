# encoding: utf-8
import os
import shutil
#import time


class SEARCH():
    def __init__(self):
        self.path = r'D:'
        self.save_music_path = './musicfiles/'
        self.files=[]
        self.mp3files=[]

    def traverse(self,f):

        fs = os.listdir(f)  # 列表 当前路径下的文件
        for f1 in fs:
            tmp_path = os.path.join(f, f1)  # 拼起来，形成当前 根目录
            if not os.path.isdir(tmp_path):  # isdir函数用于判断判断某一路径是否为目录
                print('文件: %s' % tmp_path)
                self.files.append(tmp_path)
            else:
                print('文件夹：%s' % tmp_path)
                self.traverse(tmp_path)  # 如果是目录，则继续用这个方法遍历里面的文件，直到都没有根目录，只有子目录

    def search_mp3(self):

        print('总共扫出来{}个文件'.format(len(self.files)))

        for i in self.files:
            if i.endswith('.mp3'):
                self.mp3files.append(i)
            else:
                continue

        #print(self.mp3files)

        print('总共有{}首音乐'.format(len(self.mp3files)))
        self.mp3files = list(set(self.mp3files))
        print('去重后总共有{}首音乐'.format(len(self.mp3files)))

    def copyfile(self):
        if not os.path.exists(self.save_music_path):
            os.mkdir(self.save_music_path)
        musiclist=os.listdir(self.save_music_path)
        if ''.join(musiclist) :
            print('收集了以下歌曲',''.join(musiclist))
        musiclists=[]
        for i in musiclist:
            musicname = i.split('\\')[-1]
            musiclists.append(musicname)


        for file in self.mp3files:
            filename=file.split('\\')[-1]
            if filename in musiclists:
                print('\r已存在{}'.format(filename),end='')
                #time.sleep(0.5)
                continue
            shutil.copy(file, self.save_music_path)
        print('保存路径为：',self.save_music_path,'请查看')

    def run(self):
        self.traverse(self.path)

        self.search_mp3()

        self.copyfile()

if __name__ == '__main__':
    search=SEARCH()
    search.run()