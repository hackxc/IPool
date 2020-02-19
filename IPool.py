#!/usr/bin/python
#-*- coding:utf-8 -*-
import requests,re,time
import threading
import os,sys
import urllib3
urllib3.disable_warnings()


ips = []
successip = []

def ip():
    try:
        url = 'http://www.89ip.cn/'
        headers = {
          'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'
        }
        req = requests.get(url,headers=headers)
        html = req.text
        #获取ip
        ipr = r'<tr>.*?<td>(.*?)</td>'
        iplist = re.findall(ipr,html,re.S)
        #获取端口
        portr = r'<tr>.*?<td>.*?</td>.*?<td>(.*?)</td>'
        portlist = re.findall(portr,html,re.S)
        #拼接ip 端口
        for ip,port in zip(iplist,portlist):
            ip = ip.strip()
            port = port.strip()
            ips.append(str(ip+":"+port))
    except:
        pass

def ip3():
    try:
        url = 'http://www.66ip.cn/areaindex_35/1.html'
        req = requests.get(url)
        html = req.content
        ipr = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        portr = r'</td><td>(\d{1,5})</td><td>'
        iplist = re.findall(ipr, html)
        portlist = re.findall(portr, html)
        for ip, port in zip(iplist, portlist):
            ips.append(str(ip + ":" + port))
    except:
        pass


def ipnn():
    try:
        url = 'https://www.xicidaili.com/nn/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'
        }
        req = requests.get(url, headers=headers)
        ipr = r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>'
        iplist = re.findall(ipr, req.content)

        portr = r'<td>(\d{1,5})</td>'
        portlist = re.findall(portr, req.content)
        for ip, port in zip(iplist, portlist):
            successip.append(str(ip + ":" + port))
    except:
        pass


def test(ip,url):
    try:
        req = requests.get('%s'%url, proxies={"http": ip}, timeout=1)
    except:
        lock.acquire()
        print 'false',ip
        lock.release()
    else:
        lock.acquire()
        if req.status_code==200:
            print 'success',ip
            if ip not in successip:
                successip.append(ip)
        lock.release()

if __name__ == '__main__':
    os.popen('title IPool        By: www.hackxc.cc')
    lock = threading.Lock()
    IE1 = '''reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f'''
    os.popen(IE1)
    print u'''
  ___ ____             _ 
 |_ _|  _ \ ___   ___ | |
  | || |_) / _ \ / _ \| |
  | ||  __/ (_) | (_) | |
 |___|_|   \___/ \___/|_|  
                          — 自动化IP池
    '''
    url = raw_input("\nVerification url: ")
    if 'http' not in url:
        url = 'http://'+url
    print u"\n开始自动采集IP　数据来源：互联网"
    ip()
    ip3()
    ipnn()
    print u"\nIP已采集完成"
    print u"\n开始验证代理\n"
    time.sleep(1)
    for ip in ips:
        t = threading.Thread(target=test,args=(ip,url))
        t.start()
    #判断线程是否结束
    while True:
        if threading.activeCount()==1:
            os.system('cls')
            print u'''\nby：小陈      Blog：www.hackxc.cc'''
            print u"\n可用ip列表如下 (Save as success_ip.txt)：\n"
            n = 1
            f = open('success_ip.txt','a+')
            for x in successip:
                print str(u"%s - %s"%(n,x))
                f.write(x+"\n")
                n+=1
            f.close()
            break
    #设置代理
    while True:
        try:
            n = input("\nSerial number set proxy IP (0 exit):")
            if n==0:
                sys.exit(1)
            IE1 = '''reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f'''
            IE2 = '''reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "%s" /f''' %successip[n - 1]
            os.popen(IE1)
            os.popen(IE2)
            print u"设置成功，重启浏览器 开启IE代理即可使用"
        except:
            if n==0:
                sys.exit(1)
            print u"IP序号错误"
