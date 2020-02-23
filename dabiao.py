# coding=utf-8
from tkinter import *
from PIL import Image, ImageTk
import os, shutil

#/Users/apple/Desktop/picturetrain
class WidgetsDemo:
    def __init__(self):
        self.image_list = []
        self.index = 0
        #移动到的位置
        self.image_new = '/Users/apple/Desktop/after/'
        window = Tk()
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        ww = 400
        wh = 200
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
        window.title("我是小小工具人")
        frame1 = Frame(window)
        frame1.pack(side=TOP)
        self.E1 = Entry(frame1, bd=2, width=40)
        self.E1.pack(side=LEFT)
        self.b1 = Button(frame1, text='开始', command=self.get_image_list)
        self.b1.pack(side=RIGHT)

        frame2 = Frame(window)
        frame2.pack()
        self.label1 = Label(frame2)
        self.label1.pack(side=TOP)
        self.E2 = Entry(frame2, bd=2)
        self.E2.pack(side=BOTTOM)
        self.E2.bind('<Key-Return>', self.rename)

        window.mainloop()

    # 将所有文件名放在self.image_list中
    def get_image_list(self):
        self.index = 0
        path = self.get_image_dir()
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            self.image_list.append(file_path)

        self.pilImage = Image.open(self.image_list[self.index])
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.label1.configure(image=self.tkImage)

    def get_image_dir(self):
        image_dir = self.E1.get()
        return image_dir
    
    def rename(self, event):
        name = self.E2.get()
        self.E2.delete(0, END)
        new_file_path = self.image_new + name + '.jpg'
        shutil.move(self.image_list[self.index], new_file_path)
        self.index = self.index + 1
        self.pilImage = Image.open(self.image_list[self.index])
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.label1.configure(image=self.tkImage)

WidgetsDemo()

