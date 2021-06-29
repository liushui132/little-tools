import time
import time
import socket
import sys
import os
import gevent
from gevent.pool import Pool
from gevent import monkey
import argparse
import platform
from netaddr import *
#


def get_parser():
    parser = argparse.ArgumentParser(description="Demo of argparse")
    parser.add_argument('-u','--host', required=True,help = 'the host you scan')
    parser.add_argument('-n','--number', default=3000,type=int,help = 'the number of page that you spider')
    return parser



class Port_scan:      #探测端口开放
    def port_scan(host,T):  #  扫描主体   耗时任务或者阻塞任务，异步执行的或者需要并发的就是它了
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                server.connect((host,T))
                server.settimeout(2)
                print("{}:{}".format(host,T),"--开放")
            except:
                pass
                #print("{}".format(T),"--没有开放")
            finally:
                server.close()    

    def main(host,thread,ip_list):      
        for host in ip_list:
            print(host)
        p=Pool(int(thread))
        monkey.patch_all()
        for host in ip_list:
            host =str(host)
            prot_threads=[p.spawn(Port_scan.port_scan,host,i) for i in range(65535)]
        gevent.joinall(prot_threads)         # 五，在此阻塞，等所有协程全部完成退出，这一步才执行完


class ip_alive:               #探测存活主机
    IPList = []                     
    def ip(ip):                 #将ip块解析
        ip = IPNetwork(ip)
        ip_list = list(ip)
        return ip_list

    def my_os():      #获取本机操作系统名称
        return platform.system()

    def ping_check(ip):                          #ping指定IP判断主机是否存活
        if ip_alive.my_os() == 'Windows':
            p_w = 'n'
        elif ip_alive.my_os() == 'Linux':
            p_w = 'c'
        else:
            print('不支持此操作系统')
        output = os.popen('ping -%s 1 %s'%(p_w,ip)).readlines()
        for w in output:
            if str(w).upper().find('TTL')>=0:
                print("{}".format(ip),"--存活")
                ip_alive.IPList.append(ip)
                break
    #def main(host,thread):  
    def main(host,thread):      
        ip_list = ip_alive.ip(host)
        print((len(ip_list)))
        p=Pool(300)
        monkey.patch_all()
        threads=[p.spawn(ip_alive.ping_check,str(host)) for host in ip_list]
        gevent.joinall(threads)
        Port_scan.main(host,thread,ip_alive.IPList)
        print(ip_alive.IPList)
        

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    host = args.host
    num = args.number
    t1 = time.time()
    ip_alive.main(host,num)
    t2 = time.time()
    print("扫描结束******用时",(t2-t1))