# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import pymysql
from craw_pengpainews.util.db import con
# this class for write file
class JsonWriterPipeline(object):
       '''保存到文件中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行'''
       def __init__(self):
        self.file = codecs.open('info.json', 'w', encoding='utf-8')#保存为json文件
       def process_item(self, item, spider):
            line = json.dumps(dict(item)) + "\n"#转为json的
            self.file.write(line)#写入文件中
            return item
       def spider_closed(self, spider):#爬虫结束时关闭文件
            self.file.close()

def checkTitleFromDb(title):
    cursor = con.cursor()
    sqlStr = "select title from pengpai_news where title ='"+title[0]+"'"
    cursor.execute(sqlStr)
    d = cursor.fetchone()
    return d

class insertDbPipeline(object):
        '''
        将内容保存到数据库中
        '''

        def process_item(self, item, spider):
            con = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='root1234',
                db='craw_data',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
            )
            # 使用cursor()方法获取操作游标
            cursor = con.cursor(pymysql.cursors.DictCursor)
            row = checkTitleFromDb(item['title'])
            if row:
                return
            else:
                sql = ("insert into pengpai_news(title, img_url, date, praise_num, content,sub_link)""values( %s, %s, %s, %s, %s,%s)")
                lis = (item['title'], item['url'], item['date'], item['praise_num'], item['content'],item['link'])
                cursor.execute(sql, lis)
                con.commit()
                cursor.close()
                con.close()
                return item