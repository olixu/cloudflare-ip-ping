#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import ctypes
import  subprocess
from multiprocessing.pool import ThreadPool
import logging
import time
import re
import msvcrt
from tqdm import tqdm

# 设置日志
def set_logging_format():
    logging.basicConfig(level=logging.INFO,
        format='%(message)s',
        filename="ping_host.log",
        filemode='w'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.FATAL)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

# 获得所有待测试ip
def get_all_ips(hosts_list_path):
    ips = []
    with open(hosts_list_path, "r") as f:
        for host in f.readlines():
            ips.append(host.strip())
    return ips

#多线程调用ping
def ping_host(ip):
    global finish
    popen = subprocess.Popen('ping -c 1 -w 1 %s' %ip, stdout=subprocess.PIPE,shell=True)
    popen.wait()
    res = popen.stdout.read().decode('gbk').strip('\n')
    if "平均" in res:
        try:
            latency = re.findall("平均 = \d+ms", res)[0]
            latency = re.findall(r"\d+", latency)[0]
            loss = re.findall("\d+% 丢失", res)[0]
            loss = re.findall(r"\d+", loss)[0]
            if int(latency)<THRESHOLD:
                logging.info("{}, 延迟:{}ms, 丢包:{}%".format(ip, latency, loss))
        except Exception as e:
            print(e) 
    finish += 1  

# 判断是否为管理员
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    if is_admin() == False:
        print("请以管理员权限运行")
        sys.exit()
    # 线程数：为200时候，我本地测试179秒。
    # 不同配置和网络的电脑结果有差异。线程不是越大越好，设置成不超过300。
    # 超过300后丢包测试的结果不准。
    WORD_THREAD_NUM = int(input("线程数(一般设置为200)范围为0-2000："))
    assert 0<WORD_THREAD_NUM<2000
    # 移动连接香港，一般设置100ms，电信联通连接美西，一般设置200
    THRESHOLD = int(input("阈值(移动设置为100，电信联通设置200)范围为0-300:"))
    assert 0<THRESHOLD<300
    now = time.time()
    set_logging_format()
    hosts_list_path  = "./input.txt"
    ips = get_all_ips(hosts_list_path)
    total = len(ips)
    finish = 1
    finish_temp = 1
    pool = ThreadPool(WORD_THREAD_NUM)
    pool.map_async(ping_host,ips)
    pool.close()
    with tqdm(total=total) as pbar:
        while(True):
            # 更新bar
            time.sleep(1.0)
            pbar.update(finish-finish_temp)  
            finish_temp = finish
            if (total<=finish or msvcrt.kbhit()):
                pool.terminate()
                print("正在退出")
                break
    print("总共耗时：",time.time()-now, 's')