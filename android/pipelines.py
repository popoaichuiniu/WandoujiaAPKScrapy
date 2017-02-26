# -*- coding: UTF-8 -*-
import pymongo
import requests
class MongoPipeline(object):

    collection_name = 'test'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def download_app(self,download_url,file_path):
    	with open(file_path, 'wb') as handle:
			apks = requests.get(download_url, stream=True)				
			for block in apks.iter_content(1024):
				if not block:
					break
				handle.write(block)


    def process_item(self, item, spider):
    	print '444444444444444444444444444444444444444444'+str(item['APPName'])  
        print self.db[self.collection_name].full_name
        #print type(item['version'])
        cursor=self.db[self.collection_name].find({'packageName':item['packageName']})       
        if(cursor.count()>1):#ignore this case
         	print 'There are more than two similiar packagename in db'
        elif (cursor.count()==1):
        	if(cursor[0]['APPName']==item['APPName']):#Definite that two apps are similiar if two apps' packageName and APPName are  similiar
        		#print cmp(cursor[0]['version'],item['version'])
        		if(cmp(cursor[0]['version'],item['version'])==-1):#ignore that the result of cmp()=1
        			#There is a new version available app
        			self.download_app(item['download_url'],item['file_store_url'])
        			#update db
        			self.db[self.collection_name].update_one({'packageName':item['packageName']},{'version':item['version']})

        	else:#ignore this case
        		print 'There are two similiar packageName app but they dont have similiar APPName(Maybe change)'
        																

        else:#cursor.count()==0
        	self.download_app(item['download_url'],item['file_store_url'])
        	self.db[self.collection_name].insert_one(dict(item))

        return item
























# import requests
# import scrapy
# # import MySQLdb
# # import MySQLdb.cursors
# from android import settings
# from android.items import apkItem
# import os
# # import subprocess
# # import time
# # import urllib
# #from twisted.enterprise import adbapi
# # import codecs
# import sys
# a=1

# typelist=["影音","生活","社交","理财","工具","出行","通讯","购物","阅读","教育","咨询","安全","浏览器","效率","个性化","输入法","拍照"]



# class AndroidPipeline(object):
	
# 	count=0;	
# 	def __init__(self):
# 		# self.dbpool =dbpool		
# 		sys.setdefaultencoding('utf-8')
# 		reload(sys)


# 	# @classmethod
# 	# def from_settings(cls, settings):
# 	# 	dbargs = dict(
# 	# 		host=settings['MYSQL_HOST'],
# 	# 		db=settings['MYSQL_DBNAME'],
# 	# 		user=settings['MYSQL_USER'],
# 	# 		passwd=settings['MYSQL_PASSWD'],
# 	# 		charset='utf8',
# 	# 		cursorclass = MySQLdb.cursors.DictCursor,
# 	# 		use_unicode= True,
# 	# 	)
# 	# 	dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
# 	# 	return cls(dbpool)


# 	def process_item(self, item, spider):
# 		print "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"+str(AndroidPipeline.count)
# 		AndroidPipeline.count=AndroidPipeline.count+1
		
# 		if 'download_urls' in item:
# 			apks = []
# 			dir_path = '%s/%s' % (settings.APK_STORE, spider.name)#保存路径			

			
# 			for download_url in item['download_urls']:				
# 				global us
# 				us = download_url.split('=')[3:]				
# 				ll = '.apk'				
# 				apk_file_name = str('_'.join(us))#				
# 				#print "1111111111111111111111"+str(type(apk_file_name))				
# 				item['names'] = apk_file_name				
# 				print 'item is '
# 				print item['names']
# 				print item['type'][0]
# 				print item['version'][0]
# 				#file_path = '%s/%s.apk' % ("/home/jacy/apks", apk_file_name)
# 				for i in item['type']:
# 					print i				
# 					if i == typelist[0].decode("utf-8"):
# 						create_dir='%s/Video' %(dir_path)
# 						file_path = '%s/Video/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[1].decode("utf-8"):
# 						create_dir='%s/life' %(dir_path)
# 						file_path = '%s/life/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[2].decode("utf-8"):
# 						create_dir='%s/social contact' %(dir_path)
# 						file_path = '%s/social contact/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[3].decode("utf-8"):
# 						create_dir='%s/conduct financial transactions' %(dir_path)
# 						file_path = '%s/conduct financial transactions/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[4].decode("utf-8"):
# 						create_dir='%s/tool' %(dir_path)
# 						file_path = '%s/tool/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[5].decode("utf-8"):
# 						create_dir='%s/Travel' %(dir_path)
# 						file_path = '%s/Travel/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[6].decode("utf-8"):
# 						create_dir='%s/communication' %(dir_path)
# 						file_path = '%s/communication/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[7].decode("utf-8"):
# 						create_dir='%s/shopping' %(dir_path)
# 						file_path = '%s/shopping/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[8].decode("utf-8"):
# 						create_dir='%s/read' %(dir_path)
# 						file_path = '%s/read/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[9].decode("utf-8"):
# 						create_dir='%s/education' %(dir_path)
# 						file_path = '%s/education/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[10].decode("utf-8"):
# 						create_dir='%s/information' %(dir_path)
# 						file_path = '%s/information/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[11].decode("utf-8"):
# 						create_dir='%s/healthy' %(dir_path)
# 						file_path = '%s/healthy/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[12].decode("utf-8"):
# 						create_dir='%s/security' %(dir_path)
# 						file_path = '%s/security/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[13].decode("utf-8"):
# 						create_dir='%s/browser' %(dir_path)
# 						file_path = '%s/browser/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[14].decode("utf-8"):
# 						create_dir='%s/efficiency' %(dir_path)
# 						file_path = '%s/efficiency/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[15].decode("utf-8"):
# 						create_dir='%s/individualization' %(dir_path)
# 						file_path = '%s/individualization/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[16].decode("utf-8"):
# 						create_dir='%s/Input method' %(dir_path)
# 						file_path = '%s/Input method/%s.apk' % (dir_path, apk_file_name)
# 					elif i == typelist[17].decode("utf-8"):
# 						create_dir='%s/photograph' %(dir_path)
# 						file_path = '%s/photograph/%s.apk' % (dir_path, apk_file_name)

# 				print 'description is'				
# 				# for i in item['description']:
# 				# 	print i					
# 				# 	print 'aaaa'

# 				item['description']=item['description'][0]				
# 				# for i in item['version']:
# 				# 	print i					
# 				# 	print 'version'

# 				item['version']=item['version'][0]

# 				print file_path
# 				global using_url
# 				using_url = 'http://apk.hiapk.com' + download_url
# 				apks.append(file_path)
				
# 				print using_url

# 				if not os.path.exists(create_dir):
# 					os.makedirs(create_dir)
				
				
			
# 				#d = self.dbpool.runInteraction(self._do_upinsert,item)				
# 				with open(file_path, 'wb') as handle:
# 					apks = requests.get(using_url, stream=True)
# 					#print type(apks)				
# 					for block in apks.iter_content(1024):
# 						if not block:
# 							break
# 						handle.write(block)
# 			#item['apks'] = apks			
# 		return item

# 	# def _do_upinsert(self, conn, item):		
# 	# 	global a
# 	# 	print 'a is ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss' 
# 	# 	print a
# 	# 	a = a + 1
# 	# 	ss=conn.execute('insert into test(name,type,introduce,version) values("%s","%s","%s","%s")' % (item['names'] ,item['type'] ,item['description'],item['version']))
# 	# 	print ss
		
