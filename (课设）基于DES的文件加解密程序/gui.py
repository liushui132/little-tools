import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
import time
import json
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
import os
from edtor import *





# 登录界面
flag1 = tkinter.Tk()
flag1.title('DES加解密')
flag1['height'] = 400
flag1['width'] = 500

flag1.resizable(0, 0)  # 限制窗口大小


mesbox = ScrolledText(flag1, font=('宋体', 11))
mesbox.place(x=30, y=205, width=420, height=100)
mesbox.insert(tkinter.END, '                    使用教程\n', )
mesbox.insert(tkinter.END, '-------------------------------------------------\n')
mesbox.insert(tkinter.END, '     功能支持DES对文件的加密，解密，修改密钥\n')
mesbox.insert(tkinter.END, '        支持ECB,CBC,CFB三种密码分组模式\n')

###################################################################################################################################
'''
加密部分
'''
###################################################################################################################################

 
def encrypt(*args):                         # 加密

    
    flag2 = tkinter.Tk()
    flag2.title('DES加密')
    flag2['height'] = 500
    flag2['width'] = 600
    flag2.resizable(0, 0)  # 限制窗口大小


    label_1 = tkinter.Label(flag2, text='加密文件名')    # 用户名
    label_1.place(x=20, y=30, width=100, height=20)
    entry_1 = tkinter.Entry(flag2, width=80)
    entry_1.place(x=120, y=30, width=130, height=20)

    label_2 = tkinter.Label(flag2, text='加密密码')    # 密码
    label_2.place(x=30, y=60, width=80, height=20)
    entry_2 = tkinter.Entry(flag2, width=80)
    entry_2.place(x=120, y=60, width=130, height=20)

    label_3 = tkinter.Label(flag2, text='输出文件名')       # 确认密码
    label_3.place(x=30, y=90, width=80, height=20)
    entry_3 = tkinter.Entry(flag2, width=80)
    entry_3.place(x=120, y=90, width=130, height=20)

    label_4 = tkinter.Label(flag2, text='分组方式')       #加密方式
    label_4.place(x=30, y=120, width=80, height=20)
    entry_4 = tkinter.Entry(flag2, width=80)
    entry_4.place(x=120, y=120, width=130, height=20)
    
    def chick():
        file_path = entry_1.get()
        password = entry_2.get()
        print(password)
        out_path = entry_3.get()
        kind = entry_4.get()
        iv ="0101010101010101010101010101010101010101010101010101010101010101"   #初始VI向量
        str_message =  Base64_read(file_path)  #读取明文，并转成base64
        binary_message = STRtoBIN(str_message)  #将base64明文转成二进制
        password = STRtoBIN(password)   #密钥转成二进制
        binary_password = padding_password(password)   #得到密钥得二进制比特流 64的倍数
        binary_message = padding_message(binary_message) #得到明文的二进制比特流  64的倍数
        if kind == "ECB" :
            reslut = ECB_encrypt(binary_message,password)      #ECB模式加密 
        elif kind == "CBC" :
            reslut = CBC_encrypt(binary_message,binary_password,iv)    #CBC模式加密
        elif kind == "CFB":
            reslut = CFB_encrypt(binary_message,binary_password,iv)    #CFB模式加密
        str_message = BINtoSTR(reslut)     #加密后二进制转成ascii字符
        write(str_message,out_path)    #加密后的密文写入文件
        print(str_message)    #输出测试
        mesbox1 = ScrolledText(flag2, font=('宋体', 11))
        mesbox1.place(x=30, y=205, width=420, height=100)
        mesbox1.insert(tkinter.END, '                    加密成功！\n', )
        mesbox1.insert(tkinter.END, '-------------------------------------------------\n')
        mesbox1.insert(tkinter.END, "加密后文件内容为：\n")
        mesbox1.insert(tkinter.END, str_message)


    chick = tkinter.Button(flag2, text='加密', command=chick)
    chick.place(x=270, y=100, width=60, height=25)

    flag2.mainloop()



###################################################################################################################################
'''
解密部分
'''
###################################################################################################################################

def decrypt(*args):                            #解密

    flag3 = tkinter.Tk()
    flag3.title('DES加解密')
    flag3['height'] = 500
    flag3['width'] = 600
    flag3.resizable(0, 0)  # 限制窗口大小

    label_1 = tkinter.Label(flag3, text='解密文件名')    #用户名
    label_1.place(x=20, y=30, width=100, height=20)
    entry_1 = tkinter.Entry(flag3, width=80)
    entry_1.place(x=120, y=30, width=130, height=20)

    label_2 = tkinter.Label(flag3, text='文件密钥')    # 密码
    label_2.place(x=30, y=60, width=80, height=20)
    entry_2 = tkinter.Entry(flag3, width=80)
    entry_2.place(x=120, y=60, width=130, height=20)

    label_3 = tkinter.Label(flag3, text='输出文件名')       # 确认密码
    label_3.place(x=30, y=90, width=80, height=20)
    entry_3 = tkinter.Entry(flag3, width=80)
    entry_3.place(x=120, y=90, width=130, height=20)

    label_4 = tkinter.Label(flag3, text='分组方式')       #加密方式
    label_4.place(x=30, y=120, width=80, height=20)
    entry_4 = tkinter.Entry(flag3, width=80)
    entry_4.place(x=120, y=120, width=130, height=20)


    def chick():
        file_path = entry_1.get()
        password = entry_2.get()
        out_path = entry_3.get()
        kind = entry_4.get()
        iv ="0101010101010101010101010101010101010101010101010101010101010101"   #初始VI向量
        str_message =  read(file_path)  #读取密文，并转成二进制
        binary_message = STRtoBIN(str_message)  #将b密文转成二进制
        password = STRtoBIN(password)   #密钥转成二进制
        binary_password = padding_password(password)   #得到密钥得二进制比特流 64的倍数
        binary_message = padding_message(binary_message) #得到明文的二进制比特流  64的倍数
        if kind == 'ECB':
            reslut = ECB_decrypt(binary_message,binary_password)      #ECB模式解密  
        elif kind == 'CBC':
            reslut = CBC_decrypt(binary_message,binary_password,iv)      #CBC模式解密  
        elif kind == 'CFB':
            reslut = CFB_decrypt(binary_message,binary_password,iv)     #CFB模式解密 
              
        str_message = Base64_BINtoSTR(reslut)     #解密后二进制转成ascii字符，并base64解码
        write(str_message,out_path)    #加密后的密文写入文件
        #print(str_message)    #输出测试
        mesbox2 = ScrolledText(flag3, font=('宋体', 11))
        mesbox2.place(x=30, y=205, width=420, height=100)
        mesbox2.insert(tkinter.END, '                    解密成功！\n', )
        mesbox2.insert(tkinter.END, '-------------------------------------------------\n')
        mesbox2.insert(tkinter.END, "解密后文件内容为：\n")
        mesbox2.insert(tkinter.END, str_message)

    signinbut = tkinter.Button(flag3, text='解密', command=chick)
    signinbut.place(x=270, y=110, width=60, height=25)

    flag3.mainloop()

###################################################################################################################################
'''
更换密钥部分
'''
###################################################################################################################################

def change_password():                            #更换密钥

    flag4 = tkinter.Tk()
    flag4.title('更换密钥')
    flag4['height'] = 500
    flag4['width'] = 600
    flag4.resizable(0, 0)  # 限制窗口大小


    label_1 = tkinter.Label(flag4, text='文件名称')    #用户名
    label_1.place(x=20, y=30, width=100, height=20)
    entry_1 = tkinter.Entry(flag4, width=80)
    entry_1.place(x=120, y=30, width=130, height=20)

    label_2 = tkinter.Label(flag4, text='分组方式')    # 密码
    label_2.place(x=30, y=60, width=80, height=20)
    entry_2 = tkinter.Entry(flag4, width=80)
    entry_2.place(x=120, y=60, width=130, height=20)

    label_3 = tkinter.Label(flag4, text='旧密钥')       # 确认密码
    label_3.place(x=30, y=90, width=80, height=20)
    entry_3 = tkinter.Entry(flag4, width=80)
    entry_3.place(x=120, y=90, width=130, height=20)

    label_4 = tkinter.Label(flag4, text='新密钥')       #加密方式
    label_4.place(x=30, y=120, width=80, height=20)
    entry_4 = tkinter.Entry(flag4, width=80)
    entry_4.place(x=120, y=120, width=130, height=20)

    label_5 = tkinter.Label(flag4, text='输出文件名')       #加密方式
    label_5.place(x=30, y=150, width=80, height=20)
    entry_5 = tkinter.Entry(flag4, width=80)
    entry_5.place(x=120, y=150, width=130, height=20)


    def chick():
        tmp = 'tmp.txt'
        file_path = entry_1.get()
        kind = entry_2.get()
        old_password = entry_3.get()
        new_password = entry_4.get()
        out_path = entry_5.get()
        iv ="0101010101010101010101010101010101010101010101010101010101010101"   #初始VI向量
        str_message =  read(file_path)  #读取密文，并转成二进制
        binary_message = STRtoBIN(str_message)  #将b密文转成二进制
        password_old = STRtoBIN(old_password)   #密钥转成二进制
        binary_password_old = padding_password(password_old)   #得到密钥得二进制比特流 64的倍数
        binary_message = padding_message(binary_message) #得到明文的二进制比特流  64的倍数
        if kind == 'ECB':
            reslut = ECB_decrypt(binary_message,binary_password_old)      #ECB模式解密  
        elif kind == 'CBC':
            reslut = CBC_decrypt(binary_message,binary_password_old,iv)      #CBC模式解密  
        elif kind == 'CFB':
            reslut = CFB_decrypt(binary_message,binary_password_old,iv)     #CFB模式解密 
              
        str_message = Base64_BINtoSTR(reslut)     #解密后二进制转成ascii字符，并base64解码
        write(str_message,tmp)    #加密后的密文写入文件
        #print(str_message)    #输出测试
        str_message_new =  Base64_read(tmp)  #读取明文，并转成base64
        binary_message_new = STRtoBIN(str_message_new)  #将base64明文转成二进制
        password_new = STRtoBIN(new_password)   #密钥转成二进制
        binary_password_new = padding_password(password_new)   #得到密钥得二进制比特流 64的倍数
        binary_message_new = padding_message(binary_message_new) #得到明文的二进制比特流  64的倍数
        if kind == "ECB" :
            reslut = ECB_encrypt(binary_message_new,binary_password_new)      #ECB模式加密 
        elif kind == "CBC" :
            reslut = CBC_encrypt(binary_message_new,binary_password_new,iv)    #CBC模式加密
        elif kind == "CFB":
            reslut = CFB_encrypt(binary_message_new,binary_password_new,iv)    #CFB模式加密
        str_message_new = BINtoSTR(reslut)     #加密后二进制转成ascii字符
        write(str_message_new,out_path)    #加密后的密文写入文件
        print(str_message_new)    #输出测试
        mesbox2 = ScrolledText(flag4, font=('宋体', 11))
        mesbox2.place(x=30, y=205, width=420, height=100)
        mesbox2.insert(tkinter.END, '                    密钥更换成功！\n', )
        mesbox2.insert(tkinter.END, '-------------------------------------------------\n')
        mesbox2.insert(tkinter.END, "更换后密文为：\n")
        mesbox2.insert(tkinter.END, str_message_new)


    signinbut = tkinter.Button(flag4, text='更换', command=chick)
    signinbut.place(x=270, y=110, width=60, height=25)

    flag4.mainloop()




loginbut = tkinter.Button(flag1, text='加密', command=encrypt)
loginbut.place(x=70, y=110, width=60, height=25)
signinbut = tkinter.Button(flag1, text='解密', command=decrypt)
signinbut.place(x=160, y=110, width=60, height=25)
loginbut = tkinter.Button(flag1, text='更换密码', command=change_password)
loginbut.place(x=250, y=110, width=60, height=25)

flag1.mainloop()

