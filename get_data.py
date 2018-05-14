# -*- coding: utf-8 -*-
"""
Created on Mon May  7 23:03:26 2018

@author: LJY
"""
from selenium import webdriver
import csv
from time import sleep

#网易云音乐华语歌单第一页url
url = 'http://music.163.com/#/discover/playlist/' \
    '?order=hot&cat=%E5%8D%8E%E8%AF%AD&limit=35&offset=0'

#用Chrome接口来创建一个Selenium的WebDriver
#浏览器窗口最大化
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=options)

#准备好存储歌单的csv文件，指定文件编码格式'UTF-8'
csv_file = open("playlist.csv","w",encoding='UTF-8',newline='')
writer = csv.writer(csv_file)
writer.writerow(['标题','播放量','链接'])
n = 1
#解析每一页，直到'下一页'为空
while url != 'javascript:void(0)':
    #用WebDriver加载页面
    driver.get(url)
    #加入等待：为了使页面完全加载完成
    sleep(3)
    #切换到内容的iframe
    driver.switch_to.frame("contentFrame")
    #定位歌单标签
    data = driver.find_element_by_id("m-pl-container").\
        find_elements_by_tag_name("li")
    
    print("正在爬取第"+str(n)+"页")
    n+=1
    
    #解析一页中的所有歌单
    for i in range(len(data)):
        #获取播放量
        nb = data[i].find_element_by_class_name("nb").text
        if'万'in nb and int(nb.split("万")[0]) > 500:
            #获取播放量大于500万的歌单的封面
            msk = data[i].find_element_by_css_selector("a.msk")
            #把封面上的标题和链接连同播放数一起写到文件中
            writer.writerow([msk.get_attribute('title'),nb,msk.get_attribute('href')])
    #定位'下一页'的url
    url = driver.find_element_by_css_selector("a.zbtn.znxt").\
        get_attribute('href')
#关闭文件。文件关闭后不能再进行读写操作
csv_file.close()
#关闭浏览器并退出驱动程序
driver.quit()