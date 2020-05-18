import requests
import time
import random
from bs4 import BeautifulSoup
from urllib import parse
import argparse

def get_parser():
    parser = argparse.ArgumentParser(description="Demo of argparse")
    parser.add_argument('-u','--url_key', required=True,help = 'the key_words you spider')
    parser.add_argument('-n','--number', default=1,type=int,help = 'the number of page that you spider')
    parser.add_argument('-f','--filename', default="result" ,help = 'the file name of the result')
    parser.add_argument('-t','--sleeptime', default=30,type=int ,help = 'the sleep time after you spider a page,you.d better set it more 10s')
    parser.add_argument('-v','--verify', default=True,type=bool ,help = 'if choose spider with the https')
    parser.add_argument('-k', '--kind',default='', choices=['https://', 'http://'])
    return parser

def read_agents():
    dk=open('user_agents.txt','r',encoding='utf-8')
    for r in dk.readlines():
        agents="".join(r.split('\n'))
        yield agents

def read_google():
    dk=open('google.txt','r',encoding='utf-8')
    for r in dk.readlines():
        googles="".join(r.split('\n'))
        yield googles

def config_agents():
    user_agents=[]    
    for ua in read_agents():
        user_agents.append(ua)
    return random.choice(user_agents)
def config_google():
    google_searchs=[]
    for domain in read_google():
        google_searchs.append(domain)
    return random.choice(google_searchs)
def write(value,save_file):
    value=value.split('=')[1].split('&s')[0]
    value=parse.unquote(value)
    value=parse.unquote(value)
    f = str(save_file)+".txt"
    with open(f,"a") as file:  
        file.write(str(value)+"\n")
    print("网址 {} 存入{}.txt成功".format(value,save_file))

def domain(num,key_word,save_file,sleep,verify,kind):
    kind='/url?q='+str(kind)
    for page in range(0,num):       
        agent = config_agents()
        google = config_google()
        url='https://www.google.com/search?hl=zh-CN&q={}&btnG=Search&gbv=1&start={}'.format(key_word,page*10)
        header = {'user-agent':agent,'Content-type':"text/html;charset=utf-8"}
        response =requests.get(url=url,headers=header,timeout=30,allow_redirects=False,verify=verify)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser'); 
        for target in soup.find_all('a'): 
            try:
                value = target.get('href') 
            except: 
                value = '' 
            
            if value.startswith(kind):
                if value.startswith("/url?q=https://accounts.google.com/"):
                        pass
                else:
                    write(value,save_file)
        time.sleep(sleep)
    
if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    num = args.number
    key_word = args.url_key
    save_file = args.filename
    sleep = args.sleeptime
    verify = args.verify 
    kind = args.kind
    domain(num,key_word,save_file,sleep,verify,kind)
