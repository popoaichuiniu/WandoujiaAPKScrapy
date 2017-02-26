# -*- coding: utf-8 -*-
import sys
import os
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from android import settings
from android.items import apkItem
reload(sys)
sys.setdefaultencoding('utf-8')

class AndroidSpider(CrawlSpider):
	name = "android"	
	allowed_domains = ["wandoujia.com"]
	start_urls = [
		'http://www.wandoujia.com/category/app'
	]
	scrapyPageNum=settings.maxAppDownloadNumPerCategory/24#There are 24 apps in one page
	scrapyCategoryAppsUrlPrefix=''
	def parse_start_url(self,response):
		print "111111111111111111111111111111111111111111111111"
		categorysLis=response.xpath("/html/body/div[@class='container']/ul[1]/li")
		print len(categorysLis)
		for liCagy in categorysLis:
			#print liCagy.xpath('./a/span/text()').extract_first()
			dirName=liCagy.xpath('./a/span/text()').extract_first()
			#print settings.APK_STORE
			path=settings.APK_STORE+os.sep+str(dirName)
			if not os.path.exists(path):
				os.makedirs(path)
				print 'create '+path+' successfully!' 
			else :
				print path+' has existed!'
			categoryAppsUrl=liCagy.xpath('./a/@href').extract_first()
			request =Request(categoryAppsUrl, callback=self.parse_categoryApps,meta={'page_title':dirName,'page_num':1})#startNum=1
			yield request
	def parse_categoryApps(self, response):
		#print type(response.meta['page_title'])
		#print type(response.meta['page_num'])
		#print AndroidSpider.scrapyPageNum
		if (response.meta['page_num']==1):
			AndroidSpider.scrapyCategoryAppsUrlPrefix=response.url
		print response.meta['page_num']
		#if(str(response.meta['page_title'])=='系统工具'):
		if(response.meta['page_num']<=AndroidSpider.scrapyPageNum):
			print "2222222222222222222222222222222222222222"+str(response.meta['page_title'])+'page'+str(response.meta['page_num'])
			liApps=response.xpath('//*[@id="j-tag-list"]/li')
			#print len(liApps)
			for appLi in liApps :
				appDetails=appLi.xpath('./div[2]/h2/a/@href').extract_first()
				#print appDetails
				requestAppDetail=Request(appDetails, callback=self.parse_app_detail,meta={'app_type':response.meta['page_title']})
				yield requestAppDetail
			page_num=response.meta['page_num']+1
			nextAppPageUrl=AndroidSpider.scrapyCategoryAppsUrlPrefix+'_'+str(page_num)
			#print nextAppPageUrl				
			nextAppPageRequest =Request(nextAppPageUrl, callback=self.parse_categoryApps,meta={'page_title':response.meta['page_title'],'page_num':page_num})
			yield nextAppPageRequest
	def parse_app_detail(self,response):
			appDetailUrl=response.url.split('/')
			packageName=appDetailUrl[len(appDetailUrl)-1]
			print "3333333333333333333333333333333333333333333"+str(response.meta['app_type'])+str(packageName)
			APPName=response.xpath('/html/body/div[2]/div[2]/div[1]/div[2]/p[1]/span/text()').extract_first()
			APPType=response.meta['app_type']
			version=response.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/dl/dd[5]/text()').extract_first()
			download_url=response.xpath('/html/body/div[2]/div[2]/div[1]/div[3]/a/@href').extract_first()
			permissionList=response.xpath('//*[@id="j-perms-list"]/li/span/text()').extract()
			permission=''
			for pt in permissionList:
				permission=permission+str(pt)+'*'
			#print 
			description=''
			descriptionList=response.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div/text()').extract()
			for des in descriptionList:
				description=description+str(des)
			#print description
			file_store_url=settings.APK_STORE+os.sep+str(response.meta['app_type'])+os.sep+str(APPName)+'.apk'
			appInfoItem=apkItem(packageName=packageName,APPName=APPName,APPType=APPType,version=version,download_url=download_url,file_store_url=file_store_url,permission=permission,description=description)
			yield appInfoItem
			# packageName =scrapy.Field()
			# APPName=scrapy.Field()
			# APPType=scrapy.Field()
			# version=scrapy.Field()
			# download_url=scrapy.Field()
			# file_store_url=scrapy.Field()
			# permission=scrapy.Field()
			# description=scrapy.Field()




		
	
	# def parse(self, response):
	# 	sel = HtmlXPathSelector(response)
	# 	for geturl in sel.select(
	# 		"//span[@class='list_title font14_2']/a/@href"
	# 	).extract():
	# 		link = ('http://apk.hiapk.com' + geturl)
	# 		print link

	# 		request = scrapy.http.Request(
	# 			link,callback=self.parse_item
	# 		)
	# 		print '222222222222222222222222222222222222222222222222222'
			
	# 		yield request  #每一个app的详细页面

	
	# 	pages = sel.select(#每一页的地址
	# 		"//div[@class='page_box']/div[@class='page']/a/@href"
	# 	).extract()
	# 	print('pages: %s' %pages)
		
	# 	if len(pages) > 2 :
	# 		page_link = pages[-1]
	# 		print page_link
	# 		#page_link = page_link.replace('/a/', '')
	# 		request = scrapy.http.Request('http://apk.hiapk.com%s' %page_link, callback=self.parse)
	# 		yield request

	# def parse_item(self, response):			
		
	# 	l = XPathItemLoader(item=apkItem(), response = response)
	# 	l.add_xpath('name','//div[@id="appSoftName"]["@class=detail_title left"]/text()')

	# 	l.add_xpath('download_urls',"//div[@class='code_box_border']/div[@class='button_bg button_3 btn_mar']/a/@href")
	# 	l.add_xpath('type',"//div[@class='detail_left']/div[@class='detail_tip']/a[@id='categoryLink']/text()")
	# 	l.add_xpath('description',"//div[@class='detail_content']/div[@class='soft_description']/div[@class='font12 soft_des_box fixed_height']/pre[@id='softIntroduce']/text()")
	# 	l.add_xpath('version','//div[@id="appSoftName"]["@class=detail_title left"]/text()')

 # 		return l.load_item()


