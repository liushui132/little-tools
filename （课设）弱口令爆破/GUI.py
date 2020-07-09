import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
import time
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
import os
import sys
import optparse
from multiprocessing import Process,Manager
from tkinter import *
from tkinter import messagebox

flag = []

def GUI():
    global flag
    root = tkinter.Tk()
    root.geometry('600x500+200+200')
    root.title('弱口令爆破小工具')

    mesbox = ScrolledText(root, font=('宋体', 11))
    mesbox.place(x=90, y=225, width=420, height=100)
    mesbox.insert(tkinter.END, '                    使用教程\n', )
    mesbox.insert(tkinter.END, '-------------------------------------------------\n')
    mesbox.insert(tkinter.END, '               简单的弱口令爆破工具\n')
    mesbox.insert(tkinter.END, '           暂支持ftp,ssh,mysql弱口令爆破\n')

    label_1 = tkinter.Label(root, text='爆破方式')    #用户名
    label_1.place(x=20, y=30, width=100, height=20)
    entry_1 = tkinter.Entry(root, width=80)
    entry_1.place(x=120, y=30, width=130, height=20)


    label_2 = tkinter.Label(root, text='主机地址')    #密码
    label_2.place(x=30, y=60, width=80, height=20)
    entry_2 = tkinter.Entry(root, width=80)
    entry_2.place(x=120, y=60, width=130, height=20)

    label_3 = tkinter.Label(root, text='端口号')    #密码
    label_3.place(x=30, y=90, width=80, height=20)
    entry_3 = tkinter.Entry(root, width=80)
    entry_3.place(x=120, y=90, width=130, height=20)


    label_4 = tkinter.Label(root, text='用户名')       # 确认密码
    label_4.place(x=30, y=120, width=80, height=20)
    entry_4 = tkinter.Entry(root, width=80)
    entry_4.place(x=120, y=120, width=130, height=20)
        
    label_5 = tkinter.Label(root, text='密码字典路径')       #加密方式
    label_5.place(x=30, y=150, width=80, height=20)
    entry_5 = tkinter.Entry(root, width=80)
    entry_5.place(x=120, y=150, width=130, height=20)

    label_6 = tkinter.Label(root, text='爆破进程数')       #加密方式
    label_6.place(x=30, y=180, width=80, height=20)
    entry_6 = tkinter.Entry(root, width=80)
    entry_6.place(x=120, y=180, width=130, height=20)  


    def chick():
        
        kind = entry_1.get()             #爆破类型
        ip = entry_2.get()               #IP地址
        port = entry_3.get()             #端口号
        username = entry_4.get()         #用户名
        passwd_path = entry_5.get()      #密码路径
        process = entry_6.get()          #进程数
        flag.append(kind)
        flag.append(ip)
        flag.append(port)
        flag.append(username)
        flag.append(passwd_path)
        flag.append(process)
        app = Application(flag)

        root.mainloop() 
    chick = tkinter.Button(root, text='爆破', command=chick)
    chick.place(x=300, y=80, width=60, height=25)
    root.mainloop()



class Application(Frame):
    """一个经典的GUI程序的写法"""

    def __init__(self, args):
        global flag
        root1 = tkinter.Tk()
        root1.geometry('600x500+200+200')
        root1.title('弱口令爆破结果')

        self.mesbox1 = ScrolledText(root1, font=('宋体', 11))
        self.mesbox1.place(x=90, y=25, width=450, height=400)
        self.mesbox1.insert(tkinter.END, '                    爆破流程\n', )
        self.mesbox1.insert(tkinter.END, '---------------------------------------------------\n')        
        self.args = args
        self.passwd_load()
        kind = flag[0]
        if kind == 'FTP':
            self.FTP()
        elif kind == 'SSH':
            self.SSH()
        elif kind == 'MYSQL':
            self.MYSQL()
    def passwd_load(self):
        try:
            self.mesbox1.insert(tkinter.END, 'LOADING Passwd File..........\n')
            self.passwd_list=Manager().Queue()
            with open(flag[4],encoding='utf-8') as f:
                while True:
                    line=f.readline().strip()
                    if line!="":
                        self.passwd_list.put(line)
                    else:
                        break
        except Exception as e:
            self.mesbox1.insert(tkinter.END, "ERROT!!!.%s\n"%e)
    def FTP(self):
        print("FTP")
        self.mesbox1.insert(tkinter.END, "\n[+]Please Waiting .........\n")
        self.result = Manager().Queue()
        crackName='ftpcrack'
        moduleName=__import__(crackName)
        t=getattr(moduleName,crackName)(flag)
        plist=[]
        for i in range(0,int(flag[5])):
            p=Process(target=t.run,args=(self.passwd_list,self.result,flag[3]))
            plist.append(p)
            p.start()

        key=0
        while True:
            if key==int(flag[5]):
                self.mesbox1.insert(tkinter.END, '\n[-]not Found Password!\n')
                break
            data=self.result.get()
            if data==1:
                key+=1
            else:
                self.mesbox1.insert(tkinter.END, "\n[+]Found Passwd: %s/%s\n" %(data[0],data[1]))
                break
        for p in plist:
            p.terminate()

    def SSH(self):
        print("SSH")
        self.result = Manager().Queue()
        crackName='sshcrack'
        moduleName=__import__(crackName)
        t=getattr(moduleName,crackName)(flag)
        plist=[]
        for i in range(0,int(flag[5])):
            p=Process(target=t.run,args=(self.passwd_list,self.result,flag[3]))
            plist.append(p)
            p.start()

        key=0
        while True:
            if key==int(flag[5]):
                self.mesbox1.insert(tkinter.END, '\n[-]not Found Password!\n')
                break
            data=self.result.get()
            if data==1:
                key+=1
            else:
                self.mesbox1.insert(tkinter.END, "\n[+]Found Passwd: %s/%s\n" %(data[0],data[1]))
                break
        for p in plist:
            p.terminate()
    def MYSQL(self):
        print ("MYSQL")
        self.result = Manager().Queue()
        crackName='mysqlcrack'
        moduleName=__import__(crackName)
        t=getattr(moduleName,crackName)(flag)
        plist=[]
        for i in range(0,int(flag[5])):
            p=Process(target=t.run,args=(self.passwd_list,self.result,flag[3]))
            plist.append(p)
            p.start()

        key=0
        while True:
            if key==int(flag[5]):
                self.mesbox1.insert(tkinter.END, '\n[-]not Found Password!\n')
                break
            data=self.result.get()
            if data==1:
                key+=1
            else:
                self.mesbox1.insert(tkinter.END, "\n[+]Found Passwd: %s/%s\n" %(data[0],data[1]))
                break
        for p in plist:
            p.terminate()
        

if __name__ == "__main__":
	gui =GUI()
