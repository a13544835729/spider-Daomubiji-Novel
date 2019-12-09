# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os

class DaomuPipeline(object):
    def process_item(self, item, spider):

        #/home/tarena/盗墓笔记/
        dir='/home/tarena/盗墓笔记/{}/'.format(item['title'])
        if not os.path.exists(dir):
            os.makedirs(dir)
        file_name=dir+item['name'].replace(' ','_')+'.txt'
        with open(file_name,'w') as f:
            f.write(item['content'])
        return item
