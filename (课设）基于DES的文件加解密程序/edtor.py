

from DES_BOX import *
import re
import base64

###################################################################################################################################
'''
文件/进制转换/填充操作: 文件的读取，写入，明文，密钥，明文补全为64的整数倍
'''
###################################################################################################################################

def write(str_message,out_path):         ##############################写入文件，将明文，密文写入文件中
    try:
        f = open(out_path,'w',encoding='utf-8')
        f.write(str_message)
        f.close()
        print("文件输出成功！")
    except IOError:
        print('文件加解密出错！！！')

def read(file_path):                  ########################################读取密文文件，不需要转成base64,
    try:
        f = open(file_path,'r',encoding = 'utf-8')
        message = f.read()
        f.close()

        return message
    except IOError:
        print('文件打开出错')

def Base64_read(file_path):            ##############################读取明文文件，编码转成base64,
    try:
        f = open(file_path,'r',encoding = 'utf-8')
        message = f.read()
        f.close()
        message = base64.b64encode(message.encode('utf-8')).decode("utf-8")
        return message
    except IOError:
        print('文件打开出错')

def STRtoBIN(message):         ################## 将从文件中读取到的字符串先转成ascii,再转化为二进制，每个字符占8个byte,不足补全，
    binary = ""
    for i in message:  #对每个字符进行二进制转化
        tmp = bin(ord(i))[2:]  #字符转成ascii，再转成二进制，并去掉前面的0b
        for j in range(0,8-len(tmp)):   #补齐8位,每组64位，即8位字符
            tmp = '0'+ tmp  
        binary += tmp
    return binary





def BINtoSTR(binary_str):         #################### 二进制转化为字符，不需要base64解码   （写入密文时）
    str_message= ""
    tmp = re.findall(r'.{8}',binary_str)  #每8位表示一个字符
    for i in tmp:
        str_message += chr(int(i,2))  #base参数的意思，将该字符串视作2进制转化为10进制
    return str_message

def Base64_BINtoSTR(binary_str):         ################## 二进制转化为字符，需要base64解码   （写入明文时）
    str_message= ""
    tmp = re.findall(r'.{8}',binary_str)  #每8位表示一个字符
    for i in tmp:
        str_message += chr(int(i,2))      
    str_message = base64.b64decode(str_message.encode('utf-8')).decode("utf-8")
    return str_message



def padding_message(binary_message):    #明文/密文 二进制比特流填充为64的整数倍
    dig = len(binary_message)

    while (dig % 64 != 0):
        binary_message += '0'
        dig = len(binary_message)
    return binary_message



def padding_password(binary_password):            #密钥的二进制比特流填充为64位

    dig = len(binary_password)
    if dig > 64:
        binary_password = binary_password[0:64]
    while (dig != 64):
        binary_password += '0'
        dig = len(binary_password)
    return binary_password                                                                                                                     

###################################################################################################################################
'''
DES算法操作
'''
###################################################################################################################################






#IP盒处理
def ip_change(binary_message):
    reslut = ""
    for i in IP_table:
        reslut += binary_message[i-1]     #数组下标i-1
    return reslut


#IP逆盒处理
def ip_re_change(binary_message):
    res = ""
    for i in IP_re_table:
        res += binary_message[i-1]
    return res

#E盒置换
def e_str(binary_message):
    res = ""
    for i in E:
        res += binary_message[i-1]
    return res


#字符串异或操作
def str_xor(my_str1,my_str2): 
    res = ""
    for i in range(0,len(my_str1)):
        xor_res = int(my_str1[i],10)^int(my_str2[i],10) #变成10进制是转化成字符串 2进制与10进制异或结果一样，都是1,0
        if xor_res == 1:
            res += '1'
        if xor_res == 0:
            res += '0'

    return res


#循环左移操作
def left_turn(str_1,num):
    left_res = str_1[num:len(str_1)]
    left_res =  left_res+str_1[0:num]
    return left_res


#秘钥的PC-1置换
def change_key1(password):
    res = ""
    for i in PC_1:  #PC_1盒上的元素表示位置    只循环64次
        res += password[i-1]     #将密钥按照PC_1的位置顺序排列，
    return res

#秘钥的PC-2置换
def change_key2(password):
    res  = ""
    for i in PC_2:
        res += password[i-1]
    return res


# S盒过程
def s_box(str_1):
    res = ""
    c = 0
    for i in range(0,len(str_1),6):#6为一组
        now_str = str_1[i:i+6]    #第i个分组
        row = int(now_str[0]+now_str[5],2)   #b1b6 =r   第r行
        col = int(now_str[1:5],2)   #第c列
        num = bin(S[c][row*16 + col])[2:]   #利用了bin输出有可能不是4位str类型的值，所以才有下面的循环并且加上字符0
        for gz in range(0,4-len(num)):
            num = '0'+ num
        res += num
        c  += 1
    return res


#P盒置换
def p_box(binary_message):
    res = ""
    for i in  P:
        res += binary_message[i-1]
    return res



# F函数的实现
def function_f(binary_message,key):
    first_output = e_str(binary_message)   #位选择函数将32位待加密str拓展位48位
    second_output = str_xor(first_output,key)  #将48位结果与子密钥Ki按位模2加    得到的结果分为8组（6*8）
    third_output = s_box(second_output)    #每组6位缩减位4位   S盒置换
    last_output = p_box(third_output)     #P盒换位处理  得到f函数的最终值
    return last_output


def gen_key(key):
    key_list = []
    divide_output = change_key1(key)
    key_C0 = divide_output[0:28]
    key_D0 = divide_output[28:]
    for i in SHIFT:   #shift左移位数
        key_c = left_turn(key_C0,i)
        key_d = left_turn(key_D0,i)
        key_output = change_key2(key_c + key_d)
        key_list.append(key_output)
    return key_list



#DES加密函数

def encrypt(bin_message,binary_password): 
    message_ip_bin = ip_change(bin_message)  #ip转换
    password_lst = gen_key(binary_password)   #子密钥
    message_left = message_ip_bin[0:32]
    message_right = message_ip_bin[32:]
    for i in range(0,15):
        message_tmp = message_right  #暂存右边32位
        f_result = function_f(message_tmp,password_lst[i])   #右32位与k的f函数值
        message_right = str_xor(f_result,message_left)  #f函数的结果与左边32位异或   作为下次右边32位
        message_left = message_tmp   #上一次的右边直接放到左边
    f_result = function_f(message_right,password_lst[15])  #第16次不用换位
    message_finally_left = str_xor(message_left,f_result)
    message_finally_right = message_right
    finally_message = ip_re_change(message_finally_left + message_finally_right)   #ip逆转换
    return finally_message   #单一分组的加密结果

##des解密函数                #和加密流程反过来
def decrypt(bin_message,binary_password):
    message_ip_bin = ip_change(bin_message)     #IP转换
    password_list = gen_key(binary_password)     #子密钥
    list_num = range(1,16)                 #循环15次
    cipher_left = message_ip_bin[0:32]
    cipher_right = message_ip_bin[32:]
    for i in list_num[::-1]:   #表示逆转列表调用
        message_tmp = cipher_right
        cipher_right = str_xor(cipher_left,function_f(cipher_right,password_list[i]))
        cipher_left = message_tmp
    finally_left = str_xor(cipher_left,function_f(cipher_right,password_list[0]))
    finally_right = cipher_right
    finally_output  = finally_left + finally_right
    reslut = ip_re_change(finally_output)                     #IP逆置换
    return reslut




########################################################################################################################################
'''
ECB式下的加解密
'''
########################################################################################################################################

def ECB_encrypt(binary_message,binary_password):

        reslut = ""
        tmp = re.findall(r'.{64}',binary_message)    #在字符串中查找和匹配长度为64位任意字符的结果，并返回这些结果的列表。
        for i in tmp:
            print(i)
            reslut += encrypt(i,binary_password)  #将每个字符加密后的结果再连接起来
        return reslut



def ECB_decrypt(binary_message,binary_password):
    reslut = ""
    tmp = re.findall(r'.{64}',binary_message)
    for i in tmp:
        reslut += decrypt(i,binary_password)
    return reslut

########################################################################################################################################
'''
CBC模式下的加解密
'''
########################################################################################################################################


def CBC_encrypt(binary_message,binary_password,iv):
    reslut = ""        #最终输出的密文
    key = []           #列表中存放用来异或的密钥
    num = 0
    key.append(iv)  
    tmp = re.findall(r'.{64}',binary_message)    #在字符串中查找和匹配长度为64位任意字符的结果，并返回这些结果的列表。
    for i in tmp:
        i = str_xor(i,key[num])

        miwen = encrypt(i,binary_password)
        key.append(miwen)
        reslut += miwen  #将每个字符加密后的结果再连接起来
        num = num +1 
    return reslut


def CBC_decrypt(binary_message,binary_password,iv):
    reslut = ""
    key = []
    num = 0
    byte_num = 0    #密文段数
    key.append(iv)  
    tmp = re.findall(r'.{64}',binary_message) #把密文分成64字节的列表
    byte_num = len(tmp) -1                     #密文组数 
    for j in tmp:                              #解密将所需异或的提前写入列表
        key.append(j)
    for i in reversed(tmp):                    #倒叙遍历列表
        mingwen = decrypt(i,binary_password)
        mingwen = str_xor(mingwen,key[byte_num])
        print(mingwen)
        byte_num =byte_num -1
        reslut = mingwen + reslut
    return reslut


########################################################################################################################################
'''
CFB模式下的加解密
'''
########################################################################################################################################


def CFB_encrypt(binary_message,binary_password,iv):
    reslut = ""        #最终输出的密文
    key = []           #列表中存放用来异或的密钥
    num = 0
    iv = encrypt(iv,binary_password)
    key.append(iv)  
    tmp = re.findall(r'.{64}',binary_message)    #在字符串中查找和匹配长度为64位任意字符的结果，并返回这些结果的列表。
    for i in tmp:
        miwen = str_xor(i,key[num])   #xor,生成密文分组
        reslut += miwen  #将每个字符加密后的结果连接起来
        miwen = encrypt(miwen ,binary_password)   #密文分组加密生成向量
        key.append(miwen)
        num = num +1 
    return reslut


def CFB_decrypt(binary_message,binary_password,iv):
    reslut = ""
    key = []
    num = 0
    iv = encrypt(iv,binary_password)  #初始向量加密放入，放入向量列表
    key.append(iv)  
    tmp = re.findall(r'.{64}',binary_message) #把密文分成64字节的列表
    for i in tmp:                    #正序遍历列表
        mingwen = str_xor(i,key[num])
        num = num +1
        miwen  = encrypt(i,binary_password)
        key.append(miwen)
        reslut += mingwen 
    return reslut

