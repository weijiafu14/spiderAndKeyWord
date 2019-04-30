#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 14:53:28 2017

@author: Ming JIN
"""
#import re
import importlib
#import string
import sys
#import os
import time
#import urllib3
#from bs4 import BeautifulSoup
import requests
from lxml import etree
import pymysql
importlib.reload(sys)

cookie = {"Cookie":"SINAGLOBAL=1325102616317.948.1553568822015; UM_distinctid=16a23dfd27d3cd-0e45d3fd7afb09-3e7e045d-15f900-16a23dfd27e511; UOR=,,caibaojian.com; Ugrow-G0=56862bac2f6bf97368b95873bc687eef; login_sid_t=399b0f25e6a810ebd1fabe622f8fc4c3; cross_origin_proto=SSL; YF-V5-G0=572595c78566a84019ac3c65c1e95574; WBStorage=201904231321|undefined; _s_tentry=passport.weibo.com; wb_view_log=1600*9001; Apache=3780507203171.857.1555996874725; ULV=1555996874732:3:2:1:3780507203171.857.1555996874725:1555339862956; WBtopGlobal_register_version=edef3632d17f5fb3; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWQ8N0RxO.0K48nLH-Z1Eif5JpX5KzhUgL.Foq0S0e0S0MRSh22dJLoIf2LxKqL1-BL12-LxK-LBKBL1K-LxKqL1--L1KMLxKML1-2L1hBLxK-L1heLBo-LxK-LBo5LBonLxKnL1hBL1K2LxKqLB--L12zLxKMLBozL1h.t; SUHB=0bt8ltjsGA1XYy; ALF=1587532938; SSOLoginState=1555996938; wvr=6; YF-Page-G0=b9004652c3bb1711215bacc0d9b6f2b5|1555996940|1555996940; wb_view_log_6373377841=1600*9001; webim_unReadCount=%7B%22time%22%3A1555997216230%2C%22dm_pub_total%22%3A0%2C%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A39%2C%22msgbox%22%3A0%7D"}
password = "123456"
def get_url(index):
    print("连接Mysql数据库读入数据...")

    db1 = pymysql.connect(host='127.0.0.1',port=3306,user='root',password= password,db='URL_database',charset='utf8mb4',cursorclass = pymysql.cursors.DictCursor)
 
    cursor1 = db1.cursor()
    
    #str_index = 'id' + str(index)
    str_index = str(index)
    
    sql_1 = "select url from weibo_full_url where weibo_id ="+ "'" + str_index + "'" ""
 
    cursor1.execute(sql_1)
    
    result1 = cursor1.fetchall()
    
    result = result1[0]['url']
    
    db1.close()
    
    return result


def create_table(index):
    
    db3 = pymysql.connect(host='127.0.0.1',port=3306,user='root',password= password,db='2017_database',charset='utf8mb4',cursorclass = pymysql.cursors.DictCursor)
    
    cursor3 = db3.cursor()
    
    sql_4 = "DROP TABLE IF EXISTS ID" + str(index)
    
    cursor3.execute(sql_4)
    
    sql_3 = "CREATE TABLE ID" + str(index) + "(comment_num int NOT NULL AUTO_INCREMENT,user_id  VARCHAR(40),user_level VARCHAR(40),comment VARCHAR(600),PRIMARY KEY (comment_num)) default collate = utf8mb4_unicode_ci "
 
    cursor3.execute(sql_3)

    db3.close()


def write_in_database(text1,text2,text3,text4,index):
    
    db2 = pymysql.connect(host='127.0.0.1',port=3306,user='root',password= password,db='2017_database',charset='utf8mb4',cursorclass = pymysql.cursors.DictCursor)
 
    cursor2 = db2.cursor()
    
    sql_2 = "INSERT INTO ID" + str(index) + " (user_id,user_level,comment)" +" VALUES(%s,%s,%s)"

    cursor2.execute(sql_2,(text2,text3,text4))
    
    db2.commit()
    
    db2.close()

    
def get_url_data(base_url,pageNum,word_count,index):
        
    print("爬虫准备就绪...")
    
    base_url_deal = base_url + '%d'
    
    base_url_final = str(base_url_deal)

    for page in range(1,pageNum+1):

        url = base_url_final%(page)
        lxml = requests.get(url, cookies = cookie).content

        selector = etree.HTML(lxml)

        weiboitems = selector.xpath('//div[@class="c"][@id]')
        
        time.sleep(8)  
        
        for item in weiboitems:      
            weibo_id = item.xpath('./@id')[0]
            ctt = item.xpath('./span[@class="ctt"]/text()')
            level = item.xpath('./img/@alt')
      
            text1 = str(word_count)
            text2 = str(weibo_id)
            text4 = str(ctt)
            text3 = str(level)
            
            write_in_database(text1,text2,text3,text4,index)
            
            word_count += 1

    print("成功爬取！")
    print("本事件微博信息入库完毕，共%d条"%(word_count-4))

if __name__ == '__main__':
    
    for index in range(1,10):
        
        create_table(index)
        
        word_count = 1
        
        base_url = get_url(index)
        
        first_url = base_url + '1'
  
        html = requests.get(first_url,cookies = cookie).content
        selector = etree.HTML(html)
        
        controls = selector.xpath('//input[@name="mp"]')
        
        if controls:
            pageNum = int(controls[0].attrib['value'])
        else:
            pageNum = 1
    
        get_url_data(base_url,pageNum,word_count,index)
        
        index += 1
        
        print("进行下一条微博爬取...")

    print("全部完成！")
