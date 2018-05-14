# -*- coding: utf-8 -*-
"""
Created on Mon May  7 23:03:26 2018

@author: LJY
"""
from selenium import webdriver
import csv
from time import sleep

url = 'http://music.163.com/#/discover/playlist/' \
    '?order=hot&cat=%E5%8D%8E%E8%AF%AD&limit=35&offset=0'

#driver = webdriver.PhantomJS()
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=options)

#csv_file = open("playlist.csv","w",newline='')
csv_file = open("playlist.csv","w",encoding='UTF-8',newline='')
writer = csv.writer(csv_file)
writer.writerow(['标题','播放量','链接'])
n = 1
while url != 'javascript:void(0)':
    driver.get(url)
    sleep(3)
    driver.switch_to.frame("contentFrame")
    data = driver.find_element_by_id("m-pl-container").\
        find_elements_by_tag_name("li")
    
    print("第"+str(n)+"页")
    n+=1
    
    for i in range(len(data)):
        nb = data[i].find_element_by_class_name("nb").text
        if'万'in nb and int(nb.split("万")[0]) > 500:
            msk = data[i].find_element_by_css_selector("a.msk")
            #writer.writerow([msk.get_attribute('title').encode('GBK','ignore').decode('GBk'),nb,msk.get_attribute('href').encode('GBK','ignore').decode('GBk')])
            writer.writerow([msk.get_attribute('title'),nb,msk.get_attribute('href')])
    url = driver.find_element_by_css_selector("a.zbtn.znxt").\
        get_attribute('href')
csv_file.close()
driver.quit()